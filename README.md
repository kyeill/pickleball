# Pickleball

A personal, installable web app (PWA) for Kyle's DUPR pickleball history: filter every
match by year / type / event / partner / tag, see subset performance (win %, points won %,
a normalized margin, and a custom **Value** score), watch your rating over time, and break
down how you perform by matchup strength. All from your real DUPR record.

**Live app:** <https://kyeill.github.io/pickleball/>

---

## How it works (the 30-second version)

```
DUPR (your browser) ──🔄 Sync bookmark──▶  data/data.json  ──┐
                                                 ├──▶  index.html (the PWA)  ──▶  your browser
your cleanup edits  ──▶  data/overrides.json  ──┘
```

- **`data/data.json`** — your matches + ratings, pulled from DUPR. Updated by the
  🔄 Sync bookmark. This is the only file that changes when you refresh.
- **`data/overrides.json`** — *your* edits: event renames, event types, hidden partners,
  and match tags. Committed to the repo so they follow you to every device and survive
  every data refresh.
- **`index.html`** — the whole app. Static; loads the two JSON files. No build step.

DUPR's API only answers requests made from dashboard.dupr.com with your login cookie, so the
sync runs *there*, as a bookmark, and hands the data to the app, which saves it to the repo.

---

## Setup (one time)

1. **GitHub Pages is already enabled** (Deploy from `main` / root). Live at
   <https://kyeill.github.io/pickleball/>.
2. **Install it on your phone:** open that URL in Safari/Chrome → Share → *Add to Home
   Screen*. It runs full-screen and works offline.

---

## Syncing your DUPR data

Sync whenever you've played. It runs in your own browser while you're logged in to DUPR, so **no
DUPR token or password is stored anywhere**.

### One-time setup (desktop Chrome)

1. Open the app → **🔄 Sync from DUPR** card (bottom of the page) → drag the **🔄 Sync to
   Pickleball** button to your bookmarks bar.
2. Connect GitHub in that same browser (see *connect GitHub* below) — the sync saves with it.

### Each sync (~30 seconds)

1. Open <https://dashboard.dupr.com>, logged in.
2. Click **🔄 Sync to Pickleball**. The app opens in a new tab, shows progress, saves
   `data/data.json` to GitHub, and opens the updated app. Other devices see it ~1 minute later.

If DUPR returns fewer matches than you already have, nothing is saved (a guard against DUPR
changing its data format). Pop-up blocked? Allow pop-ups for dashboard.dupr.com.

> **Why not automatic?** Until 2026-09 a GitHub Action refreshed daily with a copied DUPR token.
> DUPR then moved its API to `api.dupr.com`, switched to an httpOnly `dupr_at` cookie, and started
> rejecting copied tokens from anywhere but your browser, so the Action was retired.

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
| `tools/sync_bookmarklet.js` | Readable source of the 🔄 Sync bookmark (runs on dashboard.dupr.com). |
| `tools/build_bookmarklet.py` | Injects that source into `index.html` — run after editing it. |
| `manifest.webmanifest`, `sw.js`, `icons/` | PWA install + offline. |

## Metric definitions

- **Value** = `Win% + 25·Pts% + 50·(oppDUPR − teamDUPR)` — last term is strength of schedule (positive = tougher opponents), it follows the at-time/now toggle.
- **Points won %** — pooled (your points ÷ all points played).
- **Norm margin** — average per-game point margin, each game rescaled to an 11-point game
  (target inferred: 15 if the winning score ≥ 15, else 11) so 11–9 and 15–12 compare fairly.
- **Matchup strength** = (your DUPR + partner's) / 2 − opponents' average DUPR. The toggle
  computes it either it follows the at-time/now toggle.or on everyone's current ratings.
