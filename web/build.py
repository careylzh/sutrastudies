#!/usr/bin/env python3
"""Build the Sutra Studies web app.

Reads web/library.json (the curated text registry), each entry's data file and
the reviewed knowledge export (knowledge/exports/mindmap.json), validates them,
embeds everything into web/app.template.html and writes web/index.html.

  python3 web/build.py            write web/index.html
  python3 web/build.py --check    fail if web/index.html is missing or stale
  python3 web/build.py OUT.html   also write the wrapper-less claude.ai artifact variant
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
EXPORT = ROOT / "knowledge" / "exports" / "mindmap.json"
MODES = {"phrases": ("lines", "sutra", "sources"), "mantra": ("mantra", "text", "notes", "attribution")}
ENTRY_KEYS = {"id", "mode", "data", "title_native", "native_lang", "title_en", "subtitle", "tradition", "source_ids"}


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect() -> dict:
    """Load and validate the library, its data files and the knowledge export."""
    errors: list[str] = []
    library = load(HERE / "library.json")
    texts: dict[str, dict] = {}
    seen: set[str] = set()
    for entry in library.get("texts", []):
        eid = entry.get("id", "<missing>")
        missing = ENTRY_KEYS - entry.keys()
        if missing:
            errors.append(f"{eid}: missing keys {sorted(missing)}")
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", eid) or eid in seen:
            errors.append(f"{eid}: id must be unique kebab-case")
        seen.add(eid)
        if entry["mode"] not in MODES:
            errors.append(f"{eid}: unknown mode {entry['mode']!r}")
            continue
        for sid in entry["source_ids"]:
            if not re.fullmatch(r"S\d{3,}", sid):
                errors.append(f"{eid}: invalid source id {sid!r}")
        path = (HERE / entry["data"]).resolve()
        if not path.is_file() or ROOT not in path.parents:
            errors.append(f"{eid}: data file {entry['data']} not found inside the repository")
            continue
        if "fixtures" in path.relative_to(ROOT).parts:
            errors.append(f"{eid}: fixtures are synthetic and cannot ship in the library")
        data = load(path)
        if data.get("synthetic"):
            errors.append(f"{eid}: data marked synthetic cannot ship in the library")
        absent = [k for k in MODES[entry["mode"]] if k not in data]
        if absent:
            errors.append(f"{eid}: {entry['mode']} data lacks {absent}")
        texts[eid] = data
    if not texts:
        errors.append("library has no usable texts")
    knowledge = load(EXPORT)
    if errors:
        raise SystemExit("web build failed:\n  " + "\n  ".join(errors))
    public = [{k: v for k, v in e.items() if k != "data"} for e in library["texts"]]
    return {"library": public, "texts": texts, "knowledge": knowledge}


def render() -> str:
    payload = json.dumps(collect(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (HERE / "app.template.html").read_text(encoding="utf-8").replace("__DATA__", payload)


def main(argv: list[str]) -> int:
    full = render()
    out = HERE / "index.html"
    if argv[:1] == ["--check"]:
        if not out.is_file() or out.read_text(encoding="utf-8") != full:
            print("web/index.html is stale; run `make web`", file=sys.stderr)
            return 1
        print("web/index.html is up to date")
        return 0
    out.write_text(full, encoding="utf-8")
    print("wrote web/index.html", len(full), "bytes")
    if argv:
        start = full.index("<!--ARTIFACT-START-->") + len("<!--ARTIFACT-START-->")
        inner = full[start:full.index("<!--ARTIFACT-END-->")].replace("\n</head>\n<body>", "\n")
        target = pathlib.Path(argv[0])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(inner.strip() + "\n", encoding="utf-8")
        print("wrote", target, len(inner), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
