#!/usr/bin/env python3
"""Publish tools/sync_bookmarklet.js as /sync.js and point the bookmark at it.

The bookmark Kyle drags to his bar is a *copy* of whatever code it held that day, so
editing the sync used to mean re-dragging it. It is now a one-line loader that pulls
the current sync.js from the live site, which means this script only has to be rerun
to publish new sync code -- the saved bookmark keeps working untouched.

    python tools/build_bookmarklet.py
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "sync_bookmarklet.js")
OUT = os.path.join(ROOT, "sync.js")
HTML = os.path.join(ROOT, "index.html")
BASE = "https://kyeill.github.io/pickleball"

code = io.open(SRC, encoding="utf-8").read()
io.open(OUT, "w", encoding="utf-8", newline="").write(
    "/* Served to the 🔄 Sync bookmark. Edit tools/sync_bookmarklet.js, then run\n"
    "   python tools/build_bookmarklet.py to republish. */\n" + code)

loader = ("(function(){var s=document.createElement('script');"
          f"s.src='{BASE}/sync.js?_='+Date.now();"
          "s.onerror=function(){alert('Could not load the sync script. Check your connection, then try again.');};"
          "document.body.appendChild(s);})();")
href = "javascript:" + loader.replace("%", "%25").replace("&", "&amp;").replace('"', "&quot;")

html = io.open(HTML, encoding="utf-8").read()
new, n = re.subn(r'(<a class="bm" id="syncBm" href=")[^"]*(")',
                 lambda m: m.group(1) + href + m.group(2), html)
assert n == 1, f"expected one sync bookmark anchor, found {n}"
io.open(HTML, "w", encoding="utf-8", newline="").write(new)
print(f"Published sync.js ({len(code)} chars); bookmark is now a {len(loader)}-char loader")
