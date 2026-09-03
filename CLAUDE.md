# Notes for Claude (pickleball)

Personal DUPR tracker PWA for Kyle Yost (DUPR id `8589525879`, duprId `E9XNLO`,
email kylehyost@gmail.com). Repo **kyeill/pickleball**, live at
https://kyeill.github.io/pickleball/. Static site on GitHub Pages (`main`/root), no build.
Local working folder is still named `dupr-journal`. Displayed app name is "Pickleball".
See README for the user-facing story; see LOG.md for change history.

## Architecture
- `index.html` — the whole app. Async IIFE: fetches `./data/data.json` then
  `./data/overrides.json`, merges committed overrides with `localStorage` (local wins), renders.
  **Two tabs** — *Overview* (KPIs, Performance by Event, per-event rating chart, event-scoped
  match list) and *Analysis* (overall rating chart, Performance by Matchup Strength, full Match
  Log). Collapsible sticky-when-collapsed filter bar (Year/Type/Level/Event/Partner). Charts
  use a real date x-axis; zoom is All + years only. Matchup + event tables share a
  "DUPR actual / DUPR now" basis toggle (global `basis`). Clean-up panel edits events
  (rename/merge-by-name, Type, Level, hide, 🏆-highlight), hides one-off partners, and saves
  overrides to the repo via the GitHub Contents API (token in localStorage `gh-token`).
  Standard sans throughout (Archivo for headings; no monospace). SW `sw.js` (cache rj-v5,
  network-first). Lime pickleball logo (header SVG + `favicon.svg` + `icons/`).
- `fetch_dupr.py` — stdlib-only DUPR pull → `data/data.json`. Token from `DUPR_TOKEN` env or
  argv[1]; title-cases player names; warns/exits on token expiry. Output:
  `{player:{id,name,currentDoubles(number)}, generated, matches:[...]}`.
- `data/overrides.json` — durable user edits:
  `{meta:{events:{<rawEventStr>:{name,type,level,hidden}}, partnersHidden:[]}, tags:{}}`.
  Edited in-browser, saved to the repo (Save to GitHub) or exported/committed.

## DUPR API facts (api.dupr.gg, Bearer JWT; CORS-locked to dashboard.dupr.com)
- **Access token lifetime varies** (JWT exp − iat): Kyle's long-standing one was ~168 days, but a
  fresh normal login gave ~30 days — so plan on ~monthly secret refreshes. Tokens only grant API
  read access — NOT a password. `sub` is the base64 email. Re-copying a token without logging out
  reuses the old one; a real logout+login rotates it. `POST /auth/v1.0/login` takes
  `{email,password}` (unused; the token approach avoids storing a password).
- `POST /match/v1.0/history` `{limit,offset}` — **max limit 25**, paginate. Per-match scores,
  winner, players, and Kyle's `preMatchDoubleRating`+`matchDoubleRatingImpact` (rating curve
  reconstructable; no rating-history endpoint).
- `GET /player/v1.0/{id}` — profile incl. current doubles rating (comes back as a **string** →
  coerce to number).

## Metrics (Kyle-confirmed)
`Value = Win%(0-100) + 25·Pts%(0-1) + 50·(oppDUPR − teamDUPR)` — last term is strength of
schedule; `VALUE_K=50`; it follows the then/now toggle. Pts% pooled. Norm margin = avg per-game
margin rescaled to 11 (target 15 if winner score ≥15 else 11). Matchup bands on
(you+partner)/2 − opp avg DUPR, cutoffs ±0.10 / ±0.25. Only two event types: Tournament / League
(legacy Ladder/Other coerce to League).

## Refresh (Approach B — done)
`.github/workflows/refresh.yml` runs **daily** using the `DUPR_TOKEN` repo secret (a
`workflow_dispatch` can paste a one-off token; `${{ inputs.token || secrets.DUPR_TOKEN }}`),
pulls, commits `data/data.json` when changed → Pages redeploys. `fetch_dupr.py` prints a
`::warning::` under 21 days to token expiry and exits cleanly once expired (GitHub emails Kyle).
Kyle sets/refreshes the secret himself (~2×/yr); Claude never handles the token/password.
