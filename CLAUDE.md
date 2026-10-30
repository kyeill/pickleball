# Notes for Claude (pickleball)

Personal DUPR tracker PWA for Kyle Yost (DUPR id `8589525879`, duprId `E9XNLO`).
Repo **kyeill/pickleball**, live at <https://kyeill.github.io/pickleball/>. Static site on
GitHub Pages (`main`/root), **no build step**. Local folder is still named `dupr-journal`.
README is the user-facing story; LOG.md is the change history.

## Files
| Path | What it is |
|---|---|
| `index.html` | The whole app — markup, CSS and one async IIFE. |
| `sync.js` | Served to the Sync bookmark; generated from `tools/sync_bookmarklet.js`. |
| `data/data.json` | `{player:{id,name,currentDoubles}, generated, syncedAt, matches[]}` |
| `data/overrides.json` | `{meta:{events:{<rawEvent>:{name,type,level,hidden}}, partnersHidden[]}}` |
| `data/players.json` | `{generated, players:{<id>:{name, history:[[date,rating]], lastMatch}}}` |
| `data/watchlist.json` | `{main:[{id,name}], additional:[...]}` — the Players tab, Kyle's spelling wins |
| `tools/sync_bookmarklet.js` | Sync source. **After editing run `python tools/build_bookmarklet.py`.** |
| `tools/backfill_players.py` | One-off: rebuilt `players.json` from every committed `data.json`. |

## App structure (three tabs)
- **Overview** — Subset performance KPIs, then an **Event / Date toggle** (`t1Mode`, top right of
  the tab row, defaults to Event) that swaps between Performance by Event + per-event chart and
  Performance by Date + per-day chart. The match list below follows the row you click.
- **Analysis** — **Performance by Ranking** (4×4 partner-rating × opponent-rating matrix, metric
  chips Avg DUPR / Margin / Win % / Pts % / Value, All row and column) over the full Match Log.
  First visit each session seeds the Year filter to the newest year.
- **Players** — two ranked columns from `watchlist.json` (current DUPR, last match as an age);
  clicking one shows an Opponent metrics box and their matches against Kyle.

Filters (`F`) are global: Year/Type/Level/Event/Partner multi-selects, W/L chips, `date`, and
`pb`/`ob` from a matrix cell. `passBase` is everything except the cell; `pass` adds it, so the
matrix renders from `passBase` and does not collapse when you pick a cell.

## Conventions
- **Rating colour ramp** `rampColor(t)`: blue → green → yellow. Ratings map 3.5–4.0
  (`duprColor`), Value 0–100, Avg DUPR ±10 pts, Margin ±5, Win % 25–75%, Pts % 40–60%.
- **Rating changes are whole "points"** = thousandths (`ptsTxt`): 0.013 → "13 pts".
- **Change in tables** = this row's rating minus the row below, both rounded with the cell's own
  `toFixed(3)` first so the column always reconciles with what you can see.
- Ratings are always **at the time** (`ratingThen`); the old DUPR actual/now toggle is gone.
- Bump `CACHE` in `sw.js` on every shell change (network-first SW).

## DUPR API (api.dupr.com, `dupr_at` cookie)
- Auth is an **httpOnly `dupr_at` cookie**, not a Bearer header, and **copied tokens only work
  inside the logged-in browser** — that is why the sync runs as a bookmark and the old GitHub
  Action was retired. No DUPR credential is stored anywhere.
- `POST /player/v1.0/{id}/history` `{filters:{eventFormat:null},limit,offset,sort}` — page size 25;
  works for **any** player id, which is how the Players tab gets other people's last match.
- `GET /player/v1.0/{id}` — profile; `ratings.doubles` is a **string**. No last-match field.
- **`matchId` is not chronological.** `ORDER` chains every rated match by
  `postRating → preRating`; `LATE` flags matches DUPR rated after later-dated ones (Kyle's
  spring-2025 league, hand-entered months late). Events containing late matches collapse onto
  their final date, and `spanOf`/`endRating` prefer on-time matches.

## Sync flow
Bookmark (a loader fetching `/sync.js`, so it never needs re-dragging) runs on
dashboard.dupr.com → opens `…/pickleball/?sync=1` → fetches profile, paged history, opponents'
current ratings and the watchlist → `postMessage`s raw data after the app's `pb-ready` (origins
checked both ways) → app's `duprToData()` builds data.json and appends a dated point per player →
commits both files via `ghPutJSON()` (Contents API, fine-grained PAT in localStorage `gh-token`).
`data.json` and `players.json` are compared and written **independently**; sessionStorage
`pb-fresh` shows the new data until Pages redeploys.

## Mobile (≤620px)
Phones get **Overview only** — tabs hidden, Analysis and Players `display:none`, both charts
hidden (too small to read), date rows rendered as two lines via `data-l` labels, match rows
stacked under the W/L badge. Dark mode is the default on phones (`pb-theme` remembers a choice);
`color-scheme: light dark` stops Chrome's auto-dark from force-darkening the page.
