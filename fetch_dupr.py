#!/usr/bin/env python3
"""
Pull Kyle's full DUPR history and write data/data.json for the Rating Journal PWA.

DUPR's API is CORS-locked to dashboard.dupr.com, so the browser app can't call it
directly -- this script does the pull out-of-browser and commits a static data.json
the app reads.

Auth (changed 2026-09): the API moved from api.dupr.gg to api.dupr.com and no longer
takes an `Authorization: Bearer` header. The dashboard now authenticates with a
`dupr_at` cookie (an httpOnly JWT, so page scripts/bookmarklets can't read it).

Get the credential: log in at https://dashboard.dupr.com, open DevTools (F12) >
Application > Cookies > https://dashboard.dupr.com (or api.dupr.com), click `dupr_at`,
and copy its Value (starts with eyJ). Do NOT log out afterwards -- that revokes it.

Run:
    DUPR_TOKEN="eyJ..." python fetch_dupr.py
    # or:  python fetch_dupr.py "eyJ..."

The GitHub Action passes it via the DUPR_TOKEN env var. `dupr_at=eyJ...` and
`Bearer eyJ...` are accepted too; the prefix is stripped.
"""
import json, os, re, sys, time, urllib.request, urllib.error
from datetime import date

API = "https://api.dupr.com"
PLAYER_ID = 8589525879                    # Kyle Yost
MATCH_PAGE = 25                           # DUPR has capped match history at 25/page
OUT = os.path.join(os.path.dirname(__file__), "data", "data.json")


def _token():
    tok = os.environ.get("DUPR_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else "")
    tok = tok.strip().strip("'\"").strip()
    tok = re.sub(r"^(bearer\s+|dupr_at=)", "", tok, flags=re.I).strip().rstrip(";")
    if not tok:
        sys.exit("No token. Set DUPR_TOKEN or pass it as the first argument.")
    if not tok.startswith("eyJ"):
        sys.exit("DUPR_TOKEN doesn't look like a dupr_at cookie value (it should start "
                 "with eyJ). Re-copy the Value of the dupr_at cookie.")
    return tok


def _token_days_left(tok):
    """Days until the JWT's own exp, or None if it can't be read.
    Only an upper bound: DUPR revokes tokens early (e.g. on logout)."""
    try:
        import base64
        payload = tok.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        exp = json.loads(base64.urlsafe_b64decode(payload)).get("exp")
        return (exp - time.time()) / 86400.0 if exp else None
    except Exception:
        return None


# DUPR 5xx/429s and network blips are transient (their API 503'd mid-run on
# 2026-09-05), so ride them out rather than failing the whole refresh.
RETRY_CODES = {429, 500, 502, 503, 504}


class NotFound(Exception):
    """The endpoint doesn't exist (404/405) -- lets callers try an alternative."""


def _req(method, path, token, body=None, attempts=4):
    data = json.dumps(body).encode() if body is not None else None
    last = ""
    for i in range(attempts):
        # Mirror what the dashboard sends: the dupr_at cookie plus its origin headers.
        req = urllib.request.Request(
            API + path, data=data, method=method,
            headers={"Cookie": f"dupr_at={token}",
                     "Content-Type": "application/json", "Accept": "application/json",
                     "Origin": "https://dashboard.dupr.com",
                     "Referer": "https://dashboard.dupr.com/",
                     "X-Dupr-Client-Capabilities": "totp,webauthn",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/152.0.0.0 Safari/537.36"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:200].replace("\n", " ")
            if e.code in (401, 403):
                sys.exit(f"{e.code} from DUPR -- the dupr_at token was rejected (expired, or "
                         "revoked by logging out). Copy a fresh dupr_at cookie and update "
                         "the DUPR_TOKEN secret.")
            if e.code in (404, 405):
                raise NotFound(f"{method} {path}: HTTP {e.code}")
            last = f"HTTP {e.code} {detail}"
            if e.code not in RETRY_CODES:
                sys.exit(f"{method} {path} failed: {last}")
        except Exception as e:                      # URLError, timeouts, partial reads
            last = f"{type(e).__name__}: {e}"
        if i < attempts - 1:
            wait = 3 * (2 ** i)                     # 3s, 6s, 12s
            print(f"  ...DUPR unavailable ({last}); retrying in {wait}s")
            time.sleep(wait)
    # Upstream is down, not our problem to fix: exit 75 (EX_TEMPFAIL) so the
    # workflow can skip this run with a warning instead of a red failure.
    print(f"::warning::DUPR's API is unavailable ({method} {path}: {last}). "
          "Skipping this refresh; the next scheduled run will retry.")
    sys.exit(75)


def _num(v):
    return None if v in (None, "NR", "") else float(v)


def _title(name):
    """Proper-case a player name: 'steven  scoles' -> 'Steven Scoles'."""
    return re.sub(r"(^|[\s\-'])([a-z])", lambda m: m.group(1) + m.group(2).upper(),
                  " ".join((name or "").split()).lower())


def fetch_profile(token):
    r = _req("GET", f"/player/v1.0/{PLAYER_ID}", token)["result"]
    return {"id": r["id"], "name": r["fullName"],
            "currentDoubles": _num(r["ratings"]["doubles"])}


def _page(token, off):
    """One page of match history as (hits, total). The dashboard now uses
    POST /player/v1.0/{id}/history; fall back to the older /match endpoint."""
    try:
        r = _req("POST", f"/player/v1.0/{PLAYER_ID}/history", token,
                 {"filters": {"eventFormat": None}, "limit": MATCH_PAGE, "offset": off,
                  "sort": {"order": "DESC", "parameter": "MATCH_DATE"}})
    except NotFound:
        r = _req("POST", "/match/v1.0/history", token, {"limit": MATCH_PAGE, "offset": off})
    res = r.get("result", r)
    if isinstance(res, list):
        return res, None
    if isinstance(res, dict) and isinstance(res.get("hits"), list):
        return res["hits"], res.get("total")
    keys = sorted(res) if isinstance(res, dict) else type(res).__name__
    sys.exit(f"Unrecognised match-history response shape (result keys: {keys}). "
             "DUPR changed the API again -- fetch_dupr.py needs updating.")


def fetch_matches(token):
    hits, off = [], 0
    while True:
        page, total = _page(token, off)
        hits += page
        off += MATCH_PAGE
        print(f"  ...pulled {len(hits)}/{total if total is not None else '?'} matches")
        if not page or len(page) < MATCH_PAGE or (total is not None and off >= total):
            break
    if hits and "teams" not in hits[0]:
        sys.exit(f"Match records have an unexpected shape (keys: {sorted(hits[0])}). "
                 "DUPR changed the API again -- fetch_dupr.py needs updating.")
    return hits


def current_ratings(token, ids):
    out = {}
    for i, pid in enumerate(sorted(ids)):
        try:
            r = _req("GET", f"/player/v1.0/{pid}", token)["result"]
            out[pid] = _num(r["ratings"]["doubles"])
        except SystemExit:
            raise
        except Exception:
            out[pid] = None
        if i % 25 == 0:
            print(f"  ...current ratings {i + 1}/{len(ids)}")
    return out


def _slot_ratings(team, slot):
    """Return (preMatchDouble, impact) for player1/player2 on a team."""
    n = "Player1" if slot == "player1" else "Player2"
    pm = team.get("preMatchRatingAndImpact", {}) or {}
    return pm.get("preMatchDoubleRating" + n), pm.get("matchDoubleRatingImpact" + n)


def transform(raw, now_ratings):
    out = []
    for m in raw:
        teams = m.get("teams", [])
        me = mine = None
        for t in teams:
            for slot in ("player1", "player2"):
                p = t.get(slot)
                if p and p.get("id") == PLAYER_ID:
                    me, mine = t, slot
        if not me:
            continue
        other = next((t for t in teams if t is not me), None)
        partner_slot = "player2" if mine == "player1" else "player1"
        partner = me.get(partner_slot)
        pre, impact = _slot_ratings(me, mine)
        post = (pre + impact) if (pre is not None and impact is not None) else None

        def pinfo(p):
            return {"id": p["id"], "name": _title(p["fullName"]),
                    "ratingThen": (p.get("postMatchRating") or {}).get("doubles"),
                    "ratingNow": now_ratings.get(p["id"])}

        opps = [pinfo(other[s]) for s in ("player1", "player2")
                if other and other.get(s)] if other else []

        def games(team):
            return [g for g in (team.get(f"game{i}") for i in range(1, 6))
                    if g not in (-1, None)] if team else []

        out.append({
            "matchId": m["matchId"], "date": m["eventDate"],
            "event": (m.get("league") or "").strip() or m.get("venue"),
            "venue": m.get("venue"), "format": m["eventFormat"],
            "confirmed": m.get("confirmed"), "winner": me.get("winner"),
            "scores": games(me), "oppScores": games(other),
            "partner": pinfo(partner) if partner else None,
            "opponents": opps,
            "preRating": round(pre, 4) if pre is not None else None,
            "impact": round(impact, 5) if impact is not None else None,
            "postRating": round(post, 4) if post is not None else None,
        })
    out.sort(key=lambda x: (x["date"], x["matchId"]))
    return out


def _existing_count():
    try:
        with open(OUT, encoding="utf-8") as f:
            return len(json.load(f).get("matches", []))
    except Exception:
        return 0


def diagnose(token):
    """After a 401, try the plausible auth variants and print only status codes and
    DUPR's short error text (never the token) so the right one is obvious in the log."""
    import base64
    try:
        seg = token.split(".")
        hdr = json.loads(base64.urlsafe_b64decode(seg[0] + "=" * (-len(seg[0]) % 4)))
        pl = json.loads(base64.urlsafe_b64decode(seg[1] + "=" * (-len(seg[1]) % 4)))
        print(f"  token shape: alg={hdr.get('alg')} kid={'yes' if hdr.get('kid') else 'no'} "
              f"claims={sorted(k for k in pl if k not in ('sub', 'email'))} "
              f"token_type={pl.get('token_type')} iss={pl.get('iss')} aud={pl.get('aud')}")
    except Exception as e:
        print(f"  token shape: unreadable ({type(e).__name__})")
    base = {"Content-Type": "application/json", "Accept": "application/json",
            "Origin": "https://dashboard.dupr.com", "Referer": "https://dashboard.dupr.com/",
            "X-Dupr-Client-Capabilities": "totp,webauthn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"}
    auth = {"cookie": {"Cookie": f"dupr_at={token}"},
            "bearer": {"Authorization": f"Bearer {token}"},
            "cookie+bearer": {"Cookie": f"dupr_at={token}", "Authorization": f"Bearer {token}"},
            "x-api-key": {"x-api-key": token}}
    calls = [("GET", f"/player/v1.0/{PLAYER_ID}", None),
             ("POST", f"/player/v1.0/{PLAYER_ID}/history",
              {"filters": {"eventFormat": None}, "limit": 1, "offset": 0,
               "sort": {"order": "DESC", "parameter": "MATCH_DATE"}})]
    print("  auth diagnosis (status per variant):")
    for host in ("https://api.dupr.com", "https://api.dupr.gg"):
        for name, extra in auth.items():
            for method, path, body in calls:
                h = dict(base); h.update(extra)
                req = urllib.request.Request(host + path, method=method, headers=h,
                                             data=json.dumps(body).encode() if body else None)
                try:
                    with urllib.request.urlopen(req, timeout=20) as r:
                        res = f"{r.status} OK"
                except urllib.error.HTTPError as e:
                    msg = e.read().decode(errors="replace")[:90].replace("\n", " ")
                    res = f"{e.code} {msg}"
                except Exception as e:
                    res = f"ERR {type(e).__name__}"
                print(f"    {host[8:]:13} {name:14} {method:4} {path.split(str(PLAYER_ID))[-1] or '/':9} -> {res}")


def main():
    token = _token()
    # Liveness first; on a 401, print a variant-by-variant diagnosis before failing.
    try:
        req = urllib.request.Request(API + f"/player/v1.0/{PLAYER_ID}", headers={
            "Cookie": f"dupr_at={token}", "Accept": "application/json",
            "Origin": "https://dashboard.dupr.com", "Referer": "https://dashboard.dupr.com/",
            "X-Dupr-Client-Capabilities": "totp,webauthn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"})
        urllib.request.urlopen(req, timeout=30).close()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            print(f"Token check got {e.code}; diagnosing...")
            diagnose(token)
    except Exception:
        pass                                  # network trouble: let _req's retries handle it
    days = _token_days_left(token)
    if days is not None:
        if days <= 0:
            sys.exit("The dupr_at token has expired. Copy a fresh one from DUPR and update "
                     "the DUPR_TOKEN secret (Settings → Secrets and variables → Actions).")
        print(f"Token's own expiry is ~{days:.0f} days away (DUPR can revoke it sooner).")
        if days < 7:
            print(f"::warning::DUPR token expires in ~{days:.0f} days — "
                  "refresh the DUPR_TOKEN secret soon so the daily refresh keeps working.")
    print("Fetching profile...")
    player = fetch_profile(token)            # doubles as the real "is the token alive" check
    print(f"  {player['name']} -- current doubles {player['currentDoubles']}")
    print("Fetching match history...")
    raw = fetch_matches(token)
    ids = {p["id"] for m in raw for t in m.get("teams", [])
           for s in ("player1", "player2") if (p := t.get(s)) and p["id"] != PLAYER_ID}
    print(f"Fetching current ratings for {len(ids)} players...")
    now = current_ratings(token, ids)
    matches = transform(raw, now)
    # Never let an API change silently shrink the committed history.
    had = _existing_count()
    if len(matches) < had:
        sys.exit(f"Refusing to write: got {len(matches)} matches but data.json already has "
                 f"{had}. DUPR's response may have changed -- check before overwriting.")
    data = {"player": player, "generated": date.today().isoformat(),
            "matches": matches}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    wins = sum(1 for m in matches if m["winner"])
    print(f"Wrote {OUT}: {len(matches)} matches, {wins}-{len(matches) - wins} record.")


if __name__ == "__main__":
    main()
