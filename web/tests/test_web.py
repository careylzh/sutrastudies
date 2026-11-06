"""Web app checks: registry integrity, provenance links and build freshness."""
from __future__ import annotations

import csv
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unittest

WEB = pathlib.Path(__file__).resolve().parents[1]
ROOT = WEB.parent
sys.path.insert(0, str(WEB))
import build  # noqa: E402


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = build.collect()

    def test_library_source_ids_are_registered(self):
        with (ROOT / "literature/source-inventory.csv").open(encoding="utf-8", newline="") as fh:
            registered = {row["source_id"] for row in csv.DictReader(fh)}
        for entry in self.app["library"]:
            for sid in entry["source_ids"]:
                self.assertIn(sid, registered, f"{entry['id']} cites unregistered {sid}")

    def test_mantra_notes_carry_locators(self):
        for entry in self.app["library"]:
            if entry["mode"] != "mantra":
                continue
            data = self.app["texts"][entry["id"]]
            self.assertTrue(data["notes"])
            for note in data["notes"]:
                self.assertTrue(note["locator"].strip(), note)
                self.assertTrue(note["kind"].strip(), note)

    def test_phrase_lines_are_complete(self):
        for entry in self.app["library"]:
            if entry["mode"] != "phrases":
                continue
            for line in self.app["texts"][entry["id"]]["lines"]:
                for key in ("n", "ref", "zh", "sa", "en", "zh_gloss", "lit"):
                    self.assertIn(key, line)

    def test_only_reviewed_concepts_render(self):
        tpl = (WEB / "app.template.html").read_text(encoding="utf-8")
        self.assertIn("c.review_status === 'reviewed'", tpl)

    def test_index_is_fresh(self):
        self.assertEqual(build.main(["--check"]), 0)

    def test_inline_script_parses(self):
        html = (WEB / "index.html").read_text(encoding="utf-8")
        script = re.findall(r"<script>(.*?)</script>", html, re.S)[-1]
        if shutil.which("node") is None:
            self.skipTest("node unavailable")
        result = subprocess.run(["node", "--check", "-"], input=script, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
