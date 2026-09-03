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

## Refreshing your DUPR data (Approach B — automated)

The refresh runs **daily on its own**. DUPR access tokens last **~168 days (~5.5 months)** and
only grant API read access to your data — they are **not your password**. So the automation just
stores a token as a repo secret; no password is ever stored or exchanged.

### One-time setup

1. Get a token: log in at <https://dashboard.dupr.com>, open **DevTools → Network**, filter for
   `api.dupr`, click around your profile, click any request to `api.dupr.gg`, and copy the whole
   **`authorization: Bearer eyJ...`** value.
2. Store it as a secret: repo **Settings → Secrets and variables → Actions → New repository
   secret** → Name **`DUPR_TOKEN`**, Value = the whole `Bearer eyJ...` string → Add secret.

That's it. The **Refresh from DUPR** workflow runs daily, pulls your history, commits
`data/data.json` (only when something changed), and Pages redeploys.

### Keeping it running (~twice a year)

When the token nears expiry the daily run prints a **warning** (visible in the Actions tab); when
it finally expires the run **fails** and GitHub emails you. Either way: grab a fresh token
(step 1) and update the **`DUPR_TOKEN`** secret. A fresh login mints a new ~168-day token.

### Manual / local runs

- Run it now without waiting: **Actions → Refresh from DUPR → Run workflow** (leave the token box
  blank to use the stored secret, or paste a fresh one for a one-off).
- Locally: `DUPR_TOKEN="Bearer eyJ..." python fetch_dupr.py`.

> Security: the token is stored **encrypted** in GitHub's secret store, masked in logs, and only
> workflows on your own `main` branch can read it (fork PRs cannot). It is a read-only DUPR API
> token, not your password, and it self-expires. Use it on a public repo comfortably; the only
> practical risk is your GitHub account itself, so keep that protected.

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
| `.github/workflows/refresh.yml` | Daily automated refresh using the `DUPR_TOKEN` secret. |
| `manifest.webmanifest`, `sw.js`, `icons/` | PWA install + offline. |

## Metric definitions

- **Value** = `Win% + 25·Pts% + 50·(oppDUPR − teamDUPR)` — last term is strength of schedule (positive = tougher opponents), it follows the at-time/now toggle.
- **Points won %** — pooled (your points ÷ all points played).
- **Norm margin** — average per-game point margin, each game rescaled to an 11-point game
  (target inferred: 15 if the winning score ≥ 15, else 11) so 11–9 and 15–12 compare fairly.
- **Matchup strength** = (your DUPR + partner's) / 2 − opponents' average DUPR. The toggle
  computes it either it follows the at-time/now toggle.or on everyone's current ratings.
