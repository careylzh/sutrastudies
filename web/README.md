# Web app

A single-page reader for a curated library of texts. The ☰ button opens a
drawer with the **Texts** list, **About this text** (source-located notes),
**Concepts** (reviewed entries from the knowledge export only), and the
controls for the current text's mode. Open `web/index.html` directly in a
browser; no server or install is needed.

## Files

| Path | Role |
| --- | --- |
| `library.json` | The curated registry: one entry per text, in display order. |
| `data/*.json` | Per-text data owned by the web workstream (e.g. the mantra entry). |
| `../great-compassion-mantra/data/nilakantha-T1060.json` | Dhāraṇī data, reused in place. |
| `../knowledge/exports/mindmap.json` | Reviewed concepts (read-only input owned by the literature workstream). |
| `app.template.html` | Page, styles and script, with a `__DATA__` placeholder. |
| `build.py` | Validates every input and embeds them into `index.html`. |
| `index.html` | Built output. It is committed so the app opens without a build. |
| `tests/` | `unittest` checks, run by `make web-checks`. |

## Library entry contract

```json
{
  "id": "kebab-case, stable, never reused",
  "mode": "phrases | mantra",
  "data": "path relative to web/",
  "title_native": "大悲心陀羅尼", "native_lang": "zh-Hant",
  "title_en": "…", "subtitle": "…", "tradition": "canon or tradition context",
  "source_ids": ["S001"]
}
```

- `source_ids` must exist in `literature/source-inventory.csv`; they link
  the text to reviewed concepts in the export. Leave it empty until the
  literature workstream registers the text.
- **phrases** data needs `lines[]` (`n, ref, lit, zh, sa, en, zh_gloss`,
  optional `zh_lit`, `note_zh`), `sutra{}` and `sources[]`. Phrase-mode
  statistics currently assume the T. 1060 data shape.
- **mantra** data needs `mantra{text, lang, as_given}`, `text{}` (bibliographic
  identity, URL, license), `notes[]` (each with `kind`, `locator`, `text`), and
  `attribution`. Notes paraphrase the source, carry an exact locator, and say
  whether they come from the sūtra, the translator's apparatus or a translation
  alternative.

## Commands

```sh
make web          # rebuild web/index.html
make web-checks   # build freshness, registry/provenance links, script syntax
```
