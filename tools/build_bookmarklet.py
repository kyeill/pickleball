#!/usr/bin/env python3
"""Inject tools/sync_bookmarklet.js into index.html as the Sync bookmark's href.

Strips // comments and indentation, then escapes for a javascript: URL inside an
HTML attribute (% -> %25 so the browser's URL-decoding can't mangle it, & and " as
HTML entities). Run after editing the bookmarklet source:

    python tools/build_bookmarklet.py
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "sync_bookmarklet.js")
HTML = os.path.join(ROOT, "index.html")

code = io.open(SRC, encoding="utf-8").read()
lines = []
for ln in code.splitlines():
    s = ln.strip()
    if not s or s.startswith("//"):
        continue
    lines.append(s)
js = " ".join(lines)
assert "//" not in js.replace("https://", ""), "inline // comment would swallow the rest"

href = "javascript:" + js.replace("%", "%25").replace("&", "&amp;").replace('"', "&quot;")
html = io.open(HTML, encoding="utf-8").read()
new, count = re.subn(r'(<a class="bm" id="syncBm" href=")[^"]*(")',
                     lambda m: m.group(1) + href + m.group(2), html)
assert count == 1, f"expected one sync bookmark anchor, found {count}"
io.open(HTML, "w", encoding="utf-8", newline="").write(new)
print(f"Injected bookmarklet ({len(js)} chars) into index.html")
