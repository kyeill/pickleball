# Pickleball

A personal, installable web app (PWA) for Kyle's DUPR pickleball history: filter every
match by year / type / event / partner / tag, see subset performance (win %, points won %,
a normalized margin, and a custom **Value** score), watch your rating over time, and break
down how you perform by matchup strength. All from your real DUPR record.

**Live app:** <https://kyeill.github.io/pickleball/>

---

## How it works (the 30-second version)

```
DUPR API  ──fetch_dupr.py──▶  data/data.json  ──┐
                                                 ├──▶  index.html (the PWA)  ──▶  your browser
your cleanup edits  ──▶  data/overrides.json  ──┘
```

- **`data/data.json`** — your matches + ratings, pulled from DUPR. Refreshed by the
  workflow (or by running the script). This is the only file that changes when you refresh.
- **`data/overrides.json`** — *your* edits: event renames, event types, hidden partners,
  and match tags. Committed to the repo so they follow you to every device and survive
  every data refresh.
- **`index.html`** — the whole app. Static; loads the two JSON files. No build step.

The browser can't call DUPR directly (its API is locked to `dashboard.dupr.com` and its
tokens die in ~an hour), so the pull happens here, out of the browser, and the app just
reads the committed JSON.

---

## Setup (one time)

1. **GitHub Pages is already enabled** (Deploy from `main` / root). Live at
   <https://kyeill.github.io/pickleball/>.
2. **Install it on your phone:** open that URL in Safari/Chrome → Share → *Add to Home
   Screen*. It runs full-screen and works offline.

---

## Refreshing your DUPR data (Approach A — token, manual)

DUPR tokens expire in ~1 hour, so for now a refresh is a manual, ~2-minute thing:

1. Log in at <https://dashboard.dupr.com>.
2. Open **DevTools → Network**, filter for `api.dupr`, click around your profile, click any
   request to `api.dupr.gg`, and copy the whole **`authorization: Bearer eyJ...`** value.
3. In this repo: **Actions → Refresh from DUPR → Run workflow**, paste the token, Run.
   It pulls your history, commits `data/data.json`, and Pages redeploys automatically.

You can also run it locally: `DUPR_TOKEN="Bearer eyJ..." python fetch_dupr.py`.

> The pasted token is masked in the logs and dies within the hour, but it is recorded once
> in the run's dispatch-input list. That's the tradeoff of Approach A — **Approach B** below
> removes it.

### Approach B — automated refresh (the TODO we're not forgetting)

Goal: a scheduled refresh with no manual token. It needs a **durable** DUPR credential
(a refresh token, or username/password) stored as a **GitHub Actions Secret**, and a login
step in `fetch_dupr.py` that exchanges it for a fresh access token each run. Then this
workflow gets a `schedule:` trigger like the other repos. Secrets are encrypted and masked;
a private mirror is the safer home for the credential if we go that route. **Do not call the
project done until B is built.**

---

## Editing / cleaning up (events, types, partners, tags)

In the app: expand **Filters → ⚙ Clean up data**. There you can:

- **Rename** an event (tidy DUPR's long names) — give two events the same name to **merge**.
- Set each event's **Type** (Tournament / League).
- **Hide** one-off partners (or events) from the dropdowns — their matches still count.
- **Rename / delete tags** across every match. (Add tags on the **Matches** tab.)

These edits live in your browser as you work. To make them permanent and cross-device,
**save them to the repo — one click, once you've connected GitHub:**

### One-time: connect GitHub (for one-click saving)

1. Create a **fine-grained** token: <https://github.com/settings/personal-access-tokens/new>
   - **Resource owner:** `kyeill`
   - **Repository access:** *Only select repositories* → **`pickleball`**
   - **Permissions → Repository permissions → Contents → Read and write**
   - Generate, copy it.
2. In the app: **Clean up → Save / sync → 🔗 Connect GitHub**, paste the token, **Connect**.

The token is stored **only in your browser** (localStorage) and is sent **only to GitHub's
API** to save this one file — never to the app's host, never into the repo, never to anyone
else. Because it's fine-grained and scoped to just this repo's Contents, the worst it can do
is edit this repo. **Disconnect** removes it from the browser.

### After that: just click Save

**Clean up → Save / sync → 💾 Save to GitHub.** It commits `data/overrides.json` and the live
site refreshes in ~a minute. Do the same on any device once it's connected.

*(The manual **⤓ Export file** / **⤒ Import** buttons still exist as a no-token fallback and
for moving edits between browsers.)*

---

## Files

| Path | What it is |
|---|---|
| `index.html` | The PWA (app shell + all logic). Static, no build. |
| `data/data.json` | Matches + ratings, pulled from DUPR. |
| `data/overrides.json` | Your event renames/types, hidden partners, tags. |
| `fetch_dupr.py` | Pulls DUPR → writes `data/data.json`. Stdlib only. |
| `.github/workflows/refresh.yml` | Manual token-driven refresh (Approach A). |
| `manifest.webmanifest`, `sw.js`, `icons/` | PWA install + offline. |

## Metric definitions

- **Value** = `Win% + 25·Pts% + 100·(oppDUPR − teamDUPR)` — last term is strength of schedule (positive = tougher opponents), at match time.
- **Points won %** — pooled (your points ÷ all points played).
- **Norm margin** — average per-game point margin, each game rescaled to an 11-point game
  (target inferred: 15 if the winning score ≥ 15, else 11) so 11–9 and 15–12 compare fairly.
- **Matchup strength** = (your DUPR + partner's) / 2 − opponents' average DUPR. The toggle
  computes it either at match time or on everyone's current ratings.
