# Change log — Pickleball

Newest first. Repo `kyeill/pickleball`, live at https://kyeill.github.io/pickleball/.

## 2026-10-30 — cleanup pass
- **Removed dead code** (index.html 96.1K → 90.9K): the Performance by Matchup Strength block was
  still being computed on every render into an element deleted weeks ago; the DUPR-changes KPI
  renderer and `BANDS`/`MARGIN_BANDS` likewise had no markup left. Dropped the orphaned
  `.basisToggle` wiring — with no toggle in the UI, ratings are simply always at-the-time, so
  `agg()` lost its basis argument. Swept stale CSS (`.winbar`, `.track`, `.facthead`, `.m-date`,
  `.note`, `.bandname`, `#dkpis`, `.kpi-bar`, `tr.tot`, `.ic.del`).
- **Removed the vestigial tag feature** — storage, merge, import and export plumbing with no UI
  left and an always-empty `{}`; `overrides.json` drops its `tags` key.
- Deleted the leftover `__pycache__/` and empty `.github/` from the retired Python era.
- **Docs rewritten**: CLAUDE.md now describes the three tabs, the filter model, the colour and
  points conventions, the DUPR API facts and the sync flow; README covers the Players tab,
  the ranking matrix and the current metric definitions.

## 2026-10-26
- Clicking a player shows **one Opponent box** — Value, Record (win %), Margin, Pts % — over the
  matches they played against you. The Partner box was dropped entirely — each with Value,
  Record (win % underneath) and Margin, followed by the matches against you only; the
  "As my partner" list and the "Against me X–X" headings are gone.
- **Ranking matrix cells are clickable**: a cell filters the app (and so the Match Log) to those
  matches, an All row/column cell filters the whole row or column, clicking again clears, and the
  selection shows in the filter bar ("w/ 3.5–3.75 · vs 3.75–4.0"). The matrix itself is built
  before that filter, so the grid stays whole while you navigate it.
- Match rows carry **no bold except the DUPR change** (and the W/L badge).
- **Tighter colour ranges in the matrix** so the ramp reaches its ends at realistic values:
  Avg DUPR saturates at ±10 pts (was ±30), Pts % spans 40–60% (was 0–100), Win % spans 25–75%.
- Match rows: the **DUPR change moves above the score** and loses its parentheses; the score sits
  underneath in parentheses, still coloured per game.
- Phone tweaks: **Win % dropped from Performance by Event** and the event name given the freed
  width (no name clips at 390px now), plus breathing room under the Event/Date toggle.
- **No charts on phones** — both tab-1 rating charts are hidden below 620px; at that width they
  were too small to read. Phones get the KPIs, the table and the match list.
- **Phones now mirror tab 1** (KPIs, Performance by Event or Date, the match list and the sync
  card); Analysis and Players are desktop-only. The date rows keep their two-line phone layout
  (now on `#dtTable1`) and the four-column match row stacks under the badge below 620px.
- Match rows drop to the table's 13px. Match rows: the whole league line (level · event · date) is bold, and the impact is in
  parentheses.
- **Match rows are four columns**: W/L · event + date over partner · opponents (best first,
  "[4.16] Name") · score over impact. One 14px size throughout, only the event name bold.
  Columns sized from the data — 232px fits "[4.00] Jackson Nicholas Nesbitt", 152px fits
  "10-12, 11-8, 14-12". Each game in a multi-game match is coloured on its own with a grey comma,
  and the impact uses the ranking table's ramp instead of flat green/red.
- Earlier pass: both top lines at 14px, the impact right-aligned under the score, the score
  coloured green/clay by result, and the line-3 separator changed from a pipe to a hyphen.
- **Match Log rows restructured**: line 1 leads with the opponents' average rating then the
  opponents, line 2 is the partner's rating then their name then the DUPR impact, line 3 is
  level/type · event | date. Only the score sits on the right. Every rating carries the colour
  ramp. Avg DUPR and Margin in the matrix now use that ramp too, centred on zero (±30 pts, ±5).
- **Analysis opens on the latest year**: the first time you land on the tab in a session it sets
  the Year filter to 2026 (visible in the filter bar, clears normally, never re-applies).
  Bucket boundaries kept at 3.5 / 3.75 / 4.0 — on 2026 matches they are already well spread
  (partner 39/18/15/7, opponents 9/32/22/16); it was the 2025 ladder league skewing the all-time
  view. "Total DUPR" removed; Avg DUPR is the default metric.
- Sync card now appears on **Overview only**. Matrix: subheader removed, nothing dimmed (colour
  is full strength), metrics relabelled and reordered — **Total DUPR** (new, the cell's summed
  points, now the default), Avg DUPR, Margin, Win %, Pts %, Value.
- **Tab 2 is just Performance by Ranking + Match Log** — the DUPR changes box and the movement
  scatter were removed. The matrix is ordered strongest-first (4.0+ top and left) with 2px rules
  before the All row and column. Players: the grey-out now keys off the *label*, so anything
  reading "4 months" or more greys out (it used to use a day count and disagreed at the edge).
- **Tab 2 was: DUPR changes · Partner vs opponents matrix · movement scatter · Match Log.**
  The rating chart, Performance by Date and Performance by Matchup Strength were removed (tab 1's
  Event/Date toggle covers the first two), and the factor table was replaced by a 4×4 matrix of
  partner rating vs opponent rating with metric chips — DUPR impact, Win %, Margin, Pts won,
  Value — plus an All row and column, match counts per cell, and colour (diverging around zero
  for impact/margin, the rating ramp otherwise). Players: grey-out moved from 3 to 4 months.
- **Tab 2: "DUPR movement by factor"** — Partner / Opponents / Result / Margin / Matchup, each
  level showing M, Win%, net pts with a diverging bar, and what a win and a loss are worth there.
  Plus **"Movement vs matchup strength"**, a scatter of every match (x = opponents − your team,
  y = points) with a least-squares fit. Both respect the top filters.
- Players tab: anything under a month reads **"<1 month"**; rows quiet for 3+ months grey out, and your own row is tinted to your rating; **KYLE YOST** added to Main (an
  all-caps watchlist name is left as written), with his own last match taken from his data.
- Date mode on tab 1 no longer shows a Clear filters link.
- **Event / Date toggle on tab 1**, top right in line with the tab names. Event keeps the old
  view; Date swaps in Performance by Date and a per-day rating chart (with its own zoom chips),
  and the match list below follows whichever row you click. Tab 2 is untouched.
- **Value is colour-graded too** (0 blue → 50 green → 100 yellow), in the tables and the KPI.
- **Last match reads as age** — "4 days", "2 months", "1+ year" — with the exact date on hover.
- **Ratings are colour-graded**: blue at 3.5 → green → yellow at 4.0 (clamped outside), applied to
  every DUPR cell and both Current DUPR tiles, with darker shades in light mode.
- **Watchlist sync works**: 116 players, all 24 tracked with ratings and **DUPR's own last-match
  dates** — so DUPR does expose other players' match history (`POST /player/v1.0/{id}/history`).
  The profile payload has no date field (fields: age, badges, duprId, enablePrivacy, fullName,
  gender, id, imageUrl, isPlayer1, lucraConnected, ratings, registered, shortAddress,
  showRatingBanner, sponsor, status, verifiedEmail), so the history call is the only route.
- **Names come from the watchlist, not DUPR**: DUPR abbreviates some surnames ("Christine V.",
  "Laura H.", "Truc T.") and mangles case ("Megan kortering", "Puneet  soni").
- **Sync froze at "Tracked players: 24 of 24"** — `playersChanged` referenced `freshPlayers`
  before its `const`, so the message handler threw a ReferenceError the moment data arrived and
  the overlay sat on its last progress line. Declaration moved above first use.
- The **Sync bookmark is now a loader** that fetches `/sync.js` from the live site, so editing the
  sync no longer means re-dragging the bookmark (which is why the watchlist code never ran).
- Sync also **saves `players.json` on its own** when only tracked ratings moved; it used to bail
  out with "already up to date" whenever `data.json` was unchanged and discard them.
- Verified end to end against a local cross-origin harness with a stubbed GitHub: 116 players,
  24 with a last-match date, new ids populated.
- Watchlist completed: ids for Christine Vo, Jordan Scheller, Kenny Ngo, Megan Kortering,
  Puneet Soni, Michael Kortering, Jacob Scheller, Melanie Wong; Cameron David and Daniel Kasten
  removed. 24 tracked (11 main / 13 additional); the 9 never played show "rating arrives on the
  next sync" until one runs.
- Players tab: shows **DUPR's own spelling** of each name, and **clicking a player** opens a card
  underneath with their matches split into *as my partner* and *against me*, each with the full
  Match Log detail and a W–L count. Added Emily Shaffer's id.
- **New Players tab** — two ranked columns (Main / Additional) from `data/watchlist.json`, each
  showing current DUPR and last match date, strongest first; names awaiting a DUPR id sit at the
  bottom marked as such. Desktop only; the phone view stays on its single page.
- **The sync now tracks watchlist players**: a profile call for the rating plus a one-row history
  call for their own last match date (falls back to "last time you played them" if DUPR won't
  share it), and it commits `data/players.json` alongside `data.json` so the series grows.
- **Backfilled a rating history for every player Kyle has played.** Each committed `data.json`
  carries opponents' and partners' current ratings as of that sync, so git history already held a
  sparse time series. `tools/backfill_players.py` replays all 11 snapshots (2026-09-02 → 10-25)
  into `data/players.json`: **107 players, 1,059 dated ratings**, 105 of them with 2+ points.
  No DUPR calls needed.

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
- **Change is now measured against the row directly below**, in both tables, instead of an
  event's own first-to-last span. Events interleave in time — the Fusion ladder ran before and
  after Tourney for Tendo — so the old delta swallowed whatever happened in between and read
  -26 pts where the DUPR column had barely moved. The column now always reconciles with the DUPR
  beside it, matches the chart's day-over-day change, and the oldest row shows "—".
  Ratings are rounded with the cell's own `toFixed(3)` *before* subtracting, so the change always
  equals the subtraction you can do by eye (full precision, or `Math.round`, landed a point off
  at ties: 3.8236 prints as 3.824, and 3.8215 prints as 3.821 but `Math.round`s to 3.822).
- **Phones start in dark mode** (set before first paint by a small inline script) and the ◐ Theme
  choice is now **remembered** in localStorage `pb-theme` — previously it reset on every reload.
- Rating chart opens zoomed to the **latest year on phones only** (desktop keeps All); phone stat label "Matches" → "M".
- **Phones now get one view**: the tab bar, Performance by Event, Subset performance, DUPR
  changes, Matchup Strength and the Match Log are hidden under 620px, leaving Rating Over Time
  and Performance by Date. Date rows render as **two lines** — date + its events, then
  Matches / Win % / DUPR / Change with small captions (cells carry `data-l` labels).
- **Declared `color-scheme: light dark`** (meta + CSS). Without it Chrome on Android's auto dark
  theme darkens the page itself and leaves author colours alone, which is what made text read as
  black on a dark background on the phone while desktop was fine.
- **Mobile: the page had no `<meta name="viewport">`**, so phones laid it out at 980px and shrank
  it, and none of the existing breakpoints ever fired. Added the tag, then reworked the phone
  rules: ≤620px keeps Event / M / Win% / Value / DUPR / Change (drops Pts%, Margin, the change bar
  and Opponent — the old rule wrongly dropped DUPR); ≤440px narrows to Event / Win% / DUPR /
  Change and trims both KPI boxes to their first three tiles. Tables no longer overflow at 375px.
- **Levels stripped from the 22 event names** too (levels were pinned first, so the labels still
  show them). Clean-up event list now sorts **newest first** instead of alphabetically.
- **Bulk rename**: stripped the leading year from all 22 event names in `data/overrides.json`
  and **pinned each event's level explicitly** (18 written) so levels survive future renames.
  Level also falls back to the display name when neither the override nor DUPR's raw name has one.
- **Event labels reworked.** Performance by Event: bold name, then "4.0 Tournament | 2026-07".
  Performance by Date second line: "[4.0 Tournament] Event name" per event. Sub-lines are bigger
  (11.5px, weight 500).
  Match Log third line: "4.0 Tournament - Event name".
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
