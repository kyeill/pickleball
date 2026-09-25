# Change log — Pickleball

Newest first. Repo `kyeill/pickleball`, live at https://kyeill.github.io/pickleball/.

## 2026-09-25
- **`matchId` is NOT chronological.** Ordering a day's matches by it put the wrong match last,
  so End DUPR for the latest event read 3.840 instead of Kyle's actual 3.849. New `chainDay()`
  rebuilds a day's true order by following the rating chain (one match's `postRating` is the
  next one's `preRating`), picking the longest exact chain and attaching any stragglers by
  closest fit. `endRating()` uses it.
- **Performance by Event:** new **End DUPR** column (second to last) — bold blue, tinted from
  pale (lowest rating on screen) to saturated (highest).
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
