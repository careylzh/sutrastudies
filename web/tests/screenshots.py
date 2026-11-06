#!/usr/bin/env python3
"""Render web/index.html at phone, tablet and desktop sizes with headless Chrome.

  python3 web/tests/screenshots.py [OUT_DIR]

Writes one PNG per (device, state) to OUT_DIR (default: a new temp directory)
and prints the paths. Each page is framed in an exact-size iframe because
desktop Chrome will not open a window narrower than about 500 px.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

WEB = pathlib.Path(__file__).resolve().parents[1]
CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]
DEVICES = {"phone": (375, 740), "tablet-portrait": (820, 1180), "tablet-landscape": (1180, 820), "desktop": (1440, 900)}
STATES = {
    "reader": ("{current:'nilakantha-dharani'}", False),
    "drawer": ("{current:'nilakantha-dharani'}", True),
    "full-text": ("{current:'nilakantha-dharani',texts:{'nilakantha-dharani':{i:3,seen:3,full:true,done:false,count:0}}}", False),
    "mantra": ("{current:'karandavyuha-six-syllable',texts:{'karandavyuha-six-syllable':{count:27}}}", False),
}


def main() -> int:
    chrome = next((c for c in CHROME_CANDIDATES if c and pathlib.Path(c).exists()), None)
    if not chrome:
        print("Chrome not found; set CHROME=/path/to/chrome", file=sys.stderr)
        return 1
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(tempfile.mkdtemp(prefix="sutrastudies-shots-"))
    out.mkdir(parents=True, exist_ok=True)
    html = (WEB / "index.html").read_text(encoding="utf-8")
    for state, (stored, open_drawer) in STATES.items():
        pre = "<script>try{localStorage.setItem('sutrastudies-web',JSON.stringify(%s))}catch(e){}</script>" % stored
        post = "<style>*{transition:none!important}</style>"
        if open_drawer:
            post += "<script>addEventListener('load',function(){document.getElementById('menuBtn').click()})</script>"
        page = html.replace('<script type="application/json"', pre + '<script type="application/json"', 1).replace("</body>", post + "</body>")
        (out / f"{state}.html").write_text(page, encoding="utf-8")
    with tempfile.TemporaryDirectory() as profiles:
        for device, (w, h) in DEVICES.items():
            for state in STATES:
                frame = out / f"frame-{device}-{state}.html"
                frame.write_text(f'<!doctype html><body style="margin:0"><iframe src="{state}.html" style="border:0;width:{w}px;height:{h}px;display:block"></iframe>', encoding="utf-8")
                png = out / f"{device}-{state}.png"
                subprocess.run([chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={profiles}/{device}-{state}",
                                f"--window-size={max(w, 500)},{h}", "--virtual-time-budget=2500", f"--screenshot={png}", frame.as_uri()],
                               check=True, capture_output=True)
                print(png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
