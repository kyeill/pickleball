# Change log — Pickleball

Newest first. Repo `kyeill/pickleball`, live at https://kyeill.github.io/pickleball/.

## 2026-09-03
- **Approach B — automated refresh shipped.** Discovered DUPR access tokens last **~168 days**
  and only grant API read access (not a password), so the automation stores a *token*, never a
  password. `refresh.yml` now runs **daily** using the `DUPR_TOKEN` repo secret (manual dispatch
  can still paste a one-off token); commits `data/data.json` on change. `fetch_dupr.py` decodes
  the JWT exp, prints a `::warning::` under 21 days, and exits cleanly once expired. Verified: a
  dispatched run pulled all 111 matches successfully. Kyle sets/refreshes the secret himself.
- Added an SVG browser-tab favicon; removed the Opponents table from Analysis.
- Performance by Event: added a "Clear filters" link (shown when filtered); removed the total row.
- Moved the full Match Log to the bottom of Analysis; Overview now shows an event-scoped match
  list (click a Performance-by-Event row) with a prompt when nothing is selected.

## 2026-09-02
- **Big UI pass.** Tabs became *Overview* (KPIs, Performance by Event, per-event rating chart,
  match list) and *Analysis* (overall rating chart, Performance by Matchup Strength). Charts got
  a real date x-axis; quarter zoom removed; new event-level rating chart. Added a **Level** filter
  (top + per-event control in clean-up, auto-detected + overridable); removed the Result filter.
  Filters: Year desc, Event chronological-by-start-date desc, Partner alphabetical. Player names
  proper-cased. Match Log capitalized; rows show opponents / partner / event (Type). Bands
  relabeled ("DUPR actual", bare Underdog/Favored, Even ±0.10). 🏆-suffixed events highlight
  light green. Dropped the monospace font. New lime pickleball logo + icons.
- Renamed app + repo to **Pickleball** (was `dupr-journal`); URL is now `/pickleball/`.
- **One-click "Save to GitHub"** for `overrides.json` via the Contents API (fine-grained token
  in localStorage) with 409-retry; SW switched to network-first so deploys always reach clients.
- **Value metric** gained a strength-of-schedule term: `Win% + 25·Pts% + 50·(oppDUPR − teamDUPR)`,
  following the then/now toggle. Reduced event types to Tournament / League.
- Clean-up tools: rename/merge/hide events + **set Type**, hide one-off partners; per-event dates;
  same-named events stay separate rows in clean-up but merge in filters/tables.

## 2026-09-02 (earlier — initial build)
- Reverse-engineered the DUPR API (`api.dupr.gg`), pulled Kyle's full 111-match history +
  opponents' current ratings, and shipped the app: filterable subset stats, rating-over-time
  chart, matchup-strength breakdown, per-event table, match log. Static PWA on GitHub Pages;
  `fetch_dupr.py` for data; `overrides.json` for durable cleanup edits.
- Started as an interactive Artifact prototype, then scaffolded the real repo (Approach A =
  manual token refresh) before automating.
