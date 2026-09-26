# Great Compassion Mantra viewer

A one-screen, tap-through reader for the 大悲咒 (Nīlakaṇṭha Dhāraṇī, T. 1060). Each tap fades to the next phrase, showing the Taishō Chinese, Lokesh Chandra's reconstructed Sanskrit, an English gloss and a Chinese gloss (釋義) together. The triple-line button opens a drawer with statistics (phrase, character and word counts, page counts for the whole sutra), display toggles, a jump grid and the source list.

## Files

| Path | What it is |
| --- | --- |
| `data/nilakantha-T1060.json` | The source of truth: 82 aligned phrases plus sutra-level metadata and citations. Edit this, not the HTML. |
| `viewer.template.html` | The page, with a `__DATA__` placeholder. |
| `build.py` | Embeds the JSON into the template. Writes `index.html`; with a path argument also writes the wrapper-less variant used for the claude.ai artifact. |
| `index.html` | Built output. Open it directly in a browser. |

Rebuild after editing the data or template:

```sh
python3 build.py                      # index.html only
python3 build.py /path/to/artifact.html
```

## Sources

- **Chinese text.** Verbatim from the CBETA TEI P5 XML edition of the Taishō canon, vol. 20 no. 1060, 千手千眼觀世音菩薩廣大圓滿無礙大悲心陀羅尼經, translated by Bhagavaddharma (唐 伽梵達摩), file `T/T20/T20n1060.xml` in [cbeta-org/xml-p5](https://github.com/cbeta-org/xml-p5). The Taishō numbers the dhāraṇī's phrases 一 to 八十二 in inline notes, and this viewer keeps that division, each phrase carrying its Taishō line reference (0107b25 to 0107c25). The popular 84-line recitation text differs only in chanting phrase 81 (唵悉殿都曼哆囉鉢馱耶) as three lines. Rare glyphs 㖿 and 㘄 are kept as the canon prints them; recitation editions usually write 耶 and 楞.
- **Sanskrit.** Lokesh Chandra, *The Thousand-armed Avalokiteśvara*, vol. 1 (New Delhi: Abhinav Publications / IGNCA, 1988), reconstruction of Bhagavaddharma's version, as reproduced line-aligned in the Wikipedia article "Nīlakaṇṭha Dhāraṇī". A `(?)` marks a reading Chandra left uncertain (phrase 70). Where one Sanskrit word spans two Chinese phrases the split is marked with hyphens (`namo āryā-` / `-valokiteśvarāya`).
- **English gloss.** After the English rendering that accompanies Chandra's reconstruction in that article, regularised so every Taishō phrase carries its own fragment.
- **Chinese gloss (釋義).** A modern Chinese rendering of the same meaning prepared for this viewer. The Taishō line itself is a phonetic transliteration, not a translation.

Note on provenance: the Chinese text was fetched and parsed programmatically from the CBETA file. The Sanskrit and English columns were transcribed from the published Chandra reconstruction without live access to the Wikipedia page in the session that built this, so a word-level spot check against that table is worthwhile before treating them as authoritative.

## Word and character counts

Counts in the drawer are computed at load time from the JSON. Chinese characters count CJK code points only. Sanskrit words are counted after joining hyphen-split words and dropping parenthetical alternatives. English words are counted per phrase after stripping punctuation.
