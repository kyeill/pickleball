# Change log — Pickleball

Newest first. Repo `kyeill/pickleball`, live at https://kyeill.github.io/pickleball/.

## 2026-09-25
- **Rating order now comes from DUPR's processing chain, globally.** `ORDER` chains all 110 rated
  matches by `postRating → preRating` (one start at 3.0206, one end at 3.8495 = the live profile
  rating). `LATE` flags the 15 matches DUPR rated *after* later-dated ones — Kyle's spring-2025
  ladder league, hand-entered months afterwards. End DUPR, the chart's daily close and the Match
  Log all order by that chain and skip late entries when genuine ones exist. Four days whose
  matches were *all* late entries are left out of the curve (they'd invent a spike: 2025-03-27
  would read 3.632 when the real rating was ~3.02); the caption says how many. SW cache rj-v18.
- **An event's "end" is the last match played on time, not the last processed.** Hand-entered
  matches stay flagged after the date collapse, so the spring league reports the 3.375 it
  finished the season on rather than 3.632 (which included the June tournament's gains).
- **New Change column** right of End DUPR on both tables: the rating movement across that
  event/date (finishing rating − starting rating of the matches used), green up / clay down.
- **Match Log sorting**: Newest / Oldest / Biggest DUPR gain / Biggest DUPR drop.
- **New "DUPR changes" box** at the top of Analysis: Per match / Per date / Per event as
  **absolute** average movement (how big a typical swing is), then a divider, then signed Per win
  and Per loss. Labels are just "Per match (20)". Match/win/loss use the last 6 months, date and
  event the last 12. Fixed windows — it ignores the filters, and says so.
- **Removed the caption lines under both charts and the metric-definitions footer.**
- **Rating *changes* are now 2 dp everywhere** (Change column, DUPR-changes tiles, Match Log
  impact, chart tooltips); ratings themselves stay at 3 dp.
- **Subset performance (tab 1) is pinned to actual ratings too** — only the filters move it.
- **Change bars now use a fixed scale**: a half-bar = 400 pts, so bar lengths mean the same thing
  in both tables and under any filter.
- **Deleted the unused `DUPR_TOKEN` and `DUPR_REFRESH_TOKEN` repo secrets** — the sync bookmark
  replaced them, and the repo now holds no DUPR credentials at all.
- **Performance by Event / by Date lost their DUPR actual/now toggle** — both always use the
  at-the-time ratings (`agg(list,'then')`). The toggle now lives only on Performance by Matchup
  Strength, which still drives the Subset performance KPIs.
- Dropped the "N excluded — missing a rating to classify" footer under Matchup Strength. The one
  unrated match is 2025-04-03 Ladder League (1–11 loss with Richard Mason): confirmed, but DUPR
  attached no pre/post rating to it.
- **The first rated match's group shows no change** ("—", no bar) in both tables and the chart
  tooltip — nothing precedes it to measure from.
- **Rating changes now read as whole points** (thousandths): the Change column, the DUPR-changes
  tiles, Match Log chips and chart tooltips show "+354 pts", "13 pts", "-9 pts". Ratings
  themselves stay as 3-decimal numbers. This retires the 2-dp rounding that flattened every
  recent match to 0.00.
- Column headers: "Opp then→now" → **Opponent** (all three tables), "End DUPR" → **DUPR**.
- **The bar moved from Win % to the rating change.** Win % is now a plain number; a new column
  between End DUPR and Change holds a diverging bar with zero on the centre line — green to the
  right, clay to the left, widths scaled to the biggest move on screen. Hidden under 760px.
- **Per event / date / match order, and fixed sample sizes** — the most recent 50 matches, 20 wins and
  20 losses — instead of a 6-month window, and drop their counts from the label. Per date and
  per event stay on 12 months with counts. Tab 1's "Pts won" → "Pts Won".
- **Current DUPR tile** (blue, 3 dp) added at the far left of both KPI boxes. Tab 1 dropped the
  Matches tile — the total rides along in the Win % footer as "62–49 (111)" — and the opponent
  tile is now labelled "Avg Opp (Now: 3.73)".
- **🏆 day rows**: only the event's final date is highlighted, not every day of it.
- **Late-entry events collapse onto their final date.** Any event containing hand-entered
  matches (the 2025 spring ladder league, six raw DUPR names merged into one event) now reports
  every match on its last date — 2025-05-29, 30 matches, finishing 3.632. Those matches stop
  counting as stray afterwards, so the day keeps the rating the event really ended on, no day is
  hidden from the chart any more (21 day-rows → 14), and the tooltip counts unrated matches too.
- **Date rows are clickable**: clicking filters everything to that day (new `F.date`, shown in
  the filter summary, cleared by ✕ Clear filters or by clicking the row again). SW cache rj-v25.
- **New "Performance by Date" table** on Analysis, directly under the rating chart: same columns
  as Performance by Event (M / Win% / Pts% / Margin / Value / End DUPR / Opp then→now) but one row
  per day, newest first, with the day's events underneath the date and 🏆 days highlighted. Its
  End DUPR matches the chart dot for every charted day; the four all-late-entry days are listed
  with an "entered late" note (they're the ones the chart omits). SW cache rj-v22.
- **Chart dots recoloured.** Overview (by event): gold for 🏆 events, grey otherwise (was
  win/loss green). Analysis (by day): green when the closing rating rose from the previous dot,
  clay when it fell. Both tooltips show the rating at the end of that day to 3 dp, and dots are
  slightly larger (r 3.6). SW cache rj-v20.
- **Overview's per-event chart now plots the event's finishing rating** (the End DUPR value, at
  the event's last date, 3 dp in the tooltip) instead of its average rating, so hovering a dot
  matches the table above it. SW cache rj-v19.
- **`matchId` is NOT chronological.** Ordering a day's matches by it put the wrong match last,
  so End DUPR for the latest event read 3.840 instead of Kyle's actual 3.849. New `chainDay()`
  rebuilds a day's true order by following the rating chain (one match's `postRating` is the
  next one's `preRating`), picking the longest exact chain and attaching any stragglers by
  closest fit. `endRating()` uses it.
- **Performance by Event:** new **End DUPR** column (second to last) — bold blue text, normal
  row background (the colour-scale tint was tried and dropped).
- **Analysis rating chart:** one dot per **day** instead of per match (21 dots for 110 matches),
  placed at that day's closing rating and coloured by the change from the *previous day's*
  close: green up, clay down. Days with no matches in the current filter fade rather than
  disappear; tooltip shows date, match count, W-L, the change and the closing rating.
  SW cache rj-v15.

## 2026-09-16 (later)
- **Replaced the daily GitHub Action with a 🔄 Sync bookmark.** Even a fresh, complete `dupr_at`
  (plus `dupr_rt`) was rejected from GitHub's servers in every variant (cookie ignored, Bearer
  "Invalid token", both hosts) while working in Kyle's browser. The sync now runs on
  dashboard.dupr.com, posts the raw history to the app, and the app transforms it (JS port,
  verified identical to the Python on an edge-case fixture) and commits `data/data.json` with the
  existing GitHub connection. Guards: no save if fewer matches; no commit if unchanged.
- Removed `fetch_dupr.py` and `.github/workflows/refresh.yml` (in git history). Stale banner now
  appears after 21 days and points at the sync card. SW cache rj-v13.

## 2026-09-16
- **DUPR changed its auth; refresh had been failing (401) since ~2026-09-07.** The API moved from
  `api.dupr.gg` to **`api.dupr.com`**, and the credential moved from an `Authorization: Bearer`
  header to an httpOnly **`dupr_at` cookie**. That is why the old token 401'd while its JWT still
  showed ~17 days left, why the bookmarklet found nothing (httpOnly cookies are invisible to page
  scripts), and why Chrome's "Copy as cURL" showed no auth at all (it strips cookies).
- `fetch_dupr.py`: new host, sends `Cookie: dupr_at=…` plus the dashboard's origin headers; uses
  the dashboard's `POST /player/v1.0/{id}/history` with a fallback to the legacy
  `/match/v1.0/history`; accepts the secret as a bare JWT, `dupr_at=…`, or `Bearer …`; fails
  loudly on an unrecognised response shape; and **refuses to write a data.json with fewer matches
  than the committed one**. Expiry warning now reads as an upper bound only.
- Removed the bookmarklet (it can't read an httpOnly cookie); the in-app 🔄 card, README and
  workflow comment now describe copying `dupr_at` from DevTools → Application → Cookies.
  SW cache rj-v12.

## 2026-09-05
- **Hardened the refresh against DUPR outages.** DUPR's API went down (502/503 site-wide) and
  failed the afternoon scheduled run — the token was fine (~28 days left) and the morning run had
  already succeeded. `fetch_dupr.py` now retries 5xx/429/network errors (3s→6s→12s backoff) and,
  if the upstream is still down, prints a `::warning::` and exits **75**; the workflow treats 75 as
  "skip this run" (stays green, no failure email) while a bad/expired token still exits 1 → red.
- Title-cased "Rating Over Time" / "— By Event" / "Event Matches"; Match Log shows the partner as
  `[Partner]`.
- Top filters became **multi-select checkbox dropdowns** (Year/Type/Level/Event/Partner): tick
  several values, panel stays open while selecting, "All" clears, button summarises the selection.

## 2026-09-03
- **Approach B — automated refresh shipped.** DUPR tokens only grant API read access (not a
  password), so the automation stores a *token*, never a password. `refresh.yml` runs **daily**
  using the `DUPR_TOKEN` repo secret (manual dispatch can still paste a one-off token); commits
  `data/data.json` on change. `fetch_dupr.py` decodes the JWT exp, prints a `::warning::` under
  21 days, and exits cleanly once expired. Verified working via dispatch (pulled 111 matches).
  Token lifetime varies — Kyle's old one was ~168 days but a fresh login gave ~30, so the secret
  needs refreshing ~monthly (logout+login rotates the token; re-copying reuses the old one).
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
