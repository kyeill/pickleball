#!/usr/bin/env python3
"""Build data/players.json: a dated rating history for everyone Kyle has played.

Every committed data/data.json carries each opponent's and partner's rating as of
that sync, so git history already holds a sparse time series -- no DUPR calls needed.
This replays those commits and writes one entry per player.

Run once (or again after old history changes):
    python tools/backfill_players.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "players.json")
SRC = "data/data.json"


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def snapshots():
    """(date, parsed data.json) for every commit that touched it, oldest first."""
    lines = [l for l in git("log", "--format=%H %ad", "--date=short", "--", SRC).splitlines() if l]
    for line in reversed(lines):
        sha, date = line.split(" ", 1)
        raw = git("show", f"{sha}:{SRC}")
        if not raw.strip():
            continue
        try:
            yield date.strip(), json.loads(raw)
        except json.JSONDecodeError:
            print(f"  ...skipping {sha[:7]}: unreadable JSON")


def main():
    players = {}
    me = None
    seen = 0
    for date, data in snapshots():
        seen += 1
        me = data.get("player") or me
        if me and me.get("currentDoubles") is not None:
            p = players.setdefault(str(me["id"]), {"name": me.get("name", ""), "history": {}})
            p["history"][date] = round(float(me["currentDoubles"]), 4)
        for m in data.get("matches", []):
            for person in list(m.get("opponents") or []) + ([m["partner"]] if m.get("partner") else []):
                rating = person.get("ratingNow")
                if rating in (None, "", "NR"):
                    continue
                p = players.setdefault(str(person["id"]), {"name": person.get("name", ""), "history": {}})
                if person.get("name"):
                    p["name"] = person["name"]
                p["history"][date] = round(float(rating), 4)

    if not players:
        sys.exit("No snapshots found -- is this a git checkout with history?")

    out = {}
    for pid, p in players.items():
        hist = sorted(p["history"].items())
        out[pid] = {"name": p["name"], "history": [[d, r] for d, r in hist]}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"generated": sorted({d for p in out.values() for d, _ in p["history"]})[-1],
                   "players": out}, f, indent=1, ensure_ascii=False)
    pts = sum(len(p["history"]) for p in out.values())
    print(f"Read {seen} snapshots -> {len(out)} players, {pts} dated ratings -> {OUT}")


if __name__ == "__main__":
    main()
