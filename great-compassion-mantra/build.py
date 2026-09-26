#!/usr/bin/env python3
"""Build the Great Compassion Mantra viewer.

Reads data/nilakantha-T1060.json and viewer.template.html, embeds the data and writes:
  index.html            a complete standalone page (open it in any browser)
  <artifact path>       optional: the same page without the <!doctype>/<html>/<head>/<body>
                        wrapper, for publishing as a claude.ai artifact (pass the path as argv[1])
"""
import json, pathlib, sys

here = pathlib.Path(__file__).parent
data = json.loads((here / "data" / "nilakantha-T1060.json").read_text(encoding="utf-8"))
tpl = (here / "viewer.template.html").read_text(encoding="utf-8")
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
full = tpl.replace("__DATA__", payload)
(here / "index.html").write_text(full, encoding="utf-8")
print("wrote index.html", len(full), "bytes")

if len(sys.argv) > 1:
    start = full.index("<!--ARTIFACT-START-->") + len("<!--ARTIFACT-START-->")
    inner = full[start:full.index("<!--ARTIFACT-END-->")]
    inner = inner.replace("\n</head>\n<body>", "\n")
    out = pathlib.Path(sys.argv[1]); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(inner.strip() + "\n", encoding="utf-8")
    print("wrote", out, len(inner), "bytes")
