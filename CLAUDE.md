# Notes for Claude (dupr-journal)

Personal DUPR tracker PWA for Kyle Yost (DUPR id `8589525879`, duprId `E9XNLO`). Static
site on GitHub Pages (`main`/root), no build. See README for the user-facing story.

## Architecture
- `index.html` — the whole app. Async IIFE: fetches `./data/data.json` then
  `./data/overrides.json`, merges committed overrides with `localStorage` (local wins),
  renders. Two tabs (Overview / Matches), collapsible filters, chart with year→quarter zoom,
  matchup-strength breakdown with a then/now basis toggle, event-grouped table, match log
  with tagging, and a Clean-up panel.
- `fetch_dupr.py` — stdlib-only DUPR pull → `data/data.json`. Token from `DUPR_TOKEN` env or
  argv[1]. Produces `{player:{id,name,currentDoubles(number)}, generated, matches:[...]}`.
- `data/overrides.json` — durable user edits: `{meta:{events:{<rawEventStr>:{name,type,hidden}},
  partnersHidden:[]}, tags:{<matchId>:[...]}}`. Edited in-browser, exported, committed.

## DUPR API facts (api.dupr.gg, Bearer JWT; tokens ~1h, CORS-locked to dashboard.dupr.com)
- `POST /match/v1.0/history` `{limit,offset}` — **max limit 25**, paginate. Carries per-match
  scores, winner, every player, and Kyle's `preMatchDoubleRating` + `matchDoubleRatingImpact`
  (his rating curve is reconstructable from matches; no separate rating-history endpoint).
- `GET /player/v1.0/{id}` — profile incl. current doubles rating. `currentDoubles` comes back
  as a **string** ("3.849") — coerce to number (fetch_dupr does).

## Metrics (Kyle-confirmed)
Value = `Win%(0-100) + 25·Pts%(0-1)` (~68.7 overall). Pts% pooled. Norm margin = avg per-game
margin rescaled to 11 (target 15 if winner score ≥15 else 11). Matchup bands on
(you+partner)/2 − opp avg DUPR, cutoffs ±0.10 / ±0.25.

## ⚠️ Open work
**Approach B (automated refresh)** is NOT built. Current refresh = manual token via
`workflow_dispatch`. B needs a durable DUPR credential (refresh token / creds) as an Actions
Secret + a login step in fetch_dupr.py + a `schedule:` trigger. Don't call the project done
until B lands. See the memory note `project_dupr_journal`.
