import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import goodnews as g  # noqa: E402

NOW = datetime(2026, 11, 9, 6, 0, tzinfo=timezone.utc)
SG = {"name": "SG Fixture", "region": "sg", "curated": False}
WORLD = {"name": "World Fixture", "region": "world", "curated": True}


def load(name, feed):
    return g.parse_feed((HERE / "fixtures" / name).read_bytes(), feed)


class GoodNewsTests(unittest.TestCase):
    def test_parses_rss_and_atom(self):
        self.assertEqual(len(load("sample_rss.xml", SG)), 4)
        atom = load("sample_atom.xml", WORLD)
        self.assertEqual(atom[0].link, "https://example.test/e")
        self.assertIsNotNone(atom[0].published)

    def test_filters_negative_neutral_and_stale(self):
        picked = g.select(load("sample_rss.xml", SG), now=NOW, hours=30,
                          per_region=5, already_sent=set())
        titles = [i.title for i in picked["sg"]]
        self.assertEqual(titles, ["Volunteers plant 1,000 trees along new park connector"])

    def test_negative_words_override_curated_feeds(self):
        item = g.Item("Rescue dog survives fire", "x", "s", "world", True, NOW)
        self.assertFalse(g.is_hopeful(item))

    def test_skips_already_sent(self):
        items = load("sample_rss.xml", SG)
        picked = g.select(items, now=NOW, hours=30, per_region=5,
                          already_sent={"https://example.test/a"})
        self.assertEqual(picked["sg"], [])

    def test_digest_escapes_html_and_has_both_sections(self):
        item = g.Item("Kids <3 new library & garden", "https://e.test/?a=1&b=2",
                      "Src", "sg", False, NOW)
        text = g.format_digest({"sg": [item], "world": []}, NOW)
        self.assertIn("Kids &lt;3 new library &amp; garden", text)
        self.assertIn("a=1&amp;b=2", text)
        self.assertIn("Singapore", text)
        self.assertIn("Nothing new passed the filter today.", text)

    def test_state_round_trip_keeps_newest(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sent.json"
            g.save_state(path, ["old", "mid", "new"], keep=2)
            self.assertEqual(g.load_state(path), ["mid", "new"])

    def test_feed_list_is_valid(self):
        import json
        feeds = json.loads((HERE.parent / "feeds.json").read_text())["feeds"]
        self.assertTrue(any(f["region"] == "sg" for f in feeds))
        for f in feeds:
            self.assertIn(f["region"], {"sg", "world"})
            self.assertTrue(f["url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
