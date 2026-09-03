#!/usr/bin/env python3
"""
Pull Kyle's full DUPR history and write data/data.json for the Rating Journal PWA.

Approach A (manual token). DUPR access tokens are short-lived (~1h) and CORS-locked
to dashboard.dupr.com, so the browser app can't call DUPR directly -- this script does
the pull out-of-browser and commits a static data.json the app reads.

Get a token: log in at https://dashboard.dupr.com, open DevTools > Network, click any
request to api.dupr.gg, copy the whole `authorization: Bearer eyJ...` header value.

Run:
    DUPR_TOKEN="Bearer eyJ..." python fetch_dupr.py
    # or:  python fetch_dupr.py "Bearer eyJ..."

The GitHub Action passes the token via the DUPR_TOKEN env var.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import date

API = "https://api.dupr.gg"
PLAYER_ID = 8589525879                    # Kyle Yost
MATCH_PAGE = 25                           # DUPR caps match history at 25/page
OUT = os.path.join(os.path.dirname(__file__), "data", "data.json")


def _token():
    tok = os.environ.get("DUPR_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else "")
    tok = tok.strip()
    if not tok:
        sys.exit("No token. Set DUPR_TOKEN or pass it as the first argument.")
    if not tok.lower().startswith("bearer "):
        tok = "Bearer " + tok
    return tok


def _req(method, path, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        API + path, data=data, method=method,
        headers={"Authorization": token, "Content-Type": "application/json",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        if e.code == 401:
            sys.exit("401 Unauthorized -- the token is expired or wrong. Grab a fresh one.")
        sys.exit(f"{method} {path} failed: HTTP {e.code} {detail}")


def _num(v):
    return None if v in (None, "NR", "") else float(v)


def _title(name):
    """Proper-case a player name: 'steven  scoles' -> 'Steven Scoles'."""
    import re
    return re.sub(r"(^|[\s\-'])([a-z])", lambda m: m.group(1) + m.group(2).upper(),
                  " ".join((name or "").split()).lower())


def fetch_profile(token):
    r = _req("GET", f"/player/v1.0/{PLAYER_ID}", token)["result"]
    return {"id": r["id"], "name": r["fullName"],
            "currentDoubles": _num(r["ratings"]["doubles"])}


def fetch_matches(token):
    hits, off = [], 0
    while True:
        r = _req("POST", "/match/v1.0/history", token,
                 {"limit": MATCH_PAGE, "offset": off})["result"]
        hits += r["hits"]
        total = r["total"]
        off += MATCH_PAGE
        print(f"  ...pulled {min(off, total)}/{total} matches")
        if off >= total:
            break
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


def main():
    token = _token()
    print("Fetching profile...")
    player = fetch_profile(token)
    print(f"  {player['name']} -- current doubles {player['currentDoubles']}")
    print("Fetching match history...")
    raw = fetch_matches(token)
    ids = {p["id"] for m in raw for t in m.get("teams", [])
           for s in ("player1", "player2") if (p := t.get(s)) and p["id"] != PLAYER_ID}
    print(f"Fetching current ratings for {len(ids)} players...")
    now = current_ratings(token, ids)
    matches = transform(raw, now)
    data = {"player": player, "generated": date.today().isoformat(),
            "matches": matches}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    wins = sum(1 for m in matches if m["winner"])
    print(f"Wrote {OUT}: {len(matches)} matches, {wins}-{len(matches) - wins} record.")


if __name__ == "__main__":
    main()
