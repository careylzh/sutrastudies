# Project Context

## Purpose

Build a clear, accessible mind map for learning and revising foundational
Buddhist concepts. The map should help readers see relationships among
diagnoses of suffering, ethical conduct, meditation, wisdom, and liberation
without flattening meaningful differences among Buddhist traditions.

## Intended audience

The initial audience is an interested beginner or returning learner who wants a
conceptual orientation rather than a devotional, sectarian, or academic-only
reference. Terms should be understandable in plain English while retaining
source-language forms and interpretive caveats when they matter.

## Product boundary

The product has two layers:

1. An auditable literature and knowledge layer that produces reviewed concepts,
   relationships, source records, and confidence labels.
2. An HTML/JavaScript web app that renders and supports exploration of that
   knowledge layer.

Claude Code is responsible for the web application. Codex is responsible for
the literature review and reviewed knowledge export. The interface between them
is `knowledge/exports/mindmap.json` and its JSON Schema.

## Initial review question

What concepts and relationships are necessary for a beginner to understand how
major Buddhist traditions describe suffering, its causes, its cessation, and
the paths of practice, and where do primary texts and responsible scholarship
show shared ground, divergent interpretation, or translation difficulty?

## Initial conceptual boundary

The first release should orient readers around a small, defensible core rather
than attempt an encyclopedia. Candidate clusters for screening include:

- the Four Noble Truths;
- dukkha, craving, ignorance, and dependent arising;
- impermanence, not-self, and emptiness, with tradition-specific boundaries;
- the Noble Eightfold Path and the three trainings;
- karma and rebirth, without reducing karma to fate or cosmic reward;
- mindfulness, concentration, loving-kindness, compassion, and wisdom;
- refuge, awakening, nirvana/nibbana, and the bodhisattva ideal where relevant.

This is a provisional map for review, not a set of accepted claims.

## Evidence boundaries

- The repository currently contains no reviewed Buddhist source corpus.
- No concept is publication-ready merely because it appears in the provisional
  scope above.
- Claims of historical consensus, psychological effect, or health benefit need
  evidence suited to those claims; canonical authority alone is insufficient.
- Cross-tradition synthesis must expose differences instead of manufacturing a
  lowest-common-denominator Buddhism.
- The project may explain how teachings are used for reflection, but it cannot
  promise that using the site will alleviate a particular person's suffering.

## Quality goals

- Trace every public concept and relationship to evidence.
- Make tradition, language, translation, and confidence visible without
  overwhelming a beginner.
- Separate text-reported teaching, scholarly interpretation, and editorial
  explanation.
- Include contradictory and boundary evidence.
- Meet baseline web accessibility and work without requiring an account.

## Open questions

1. Which traditions and canons should the first release cover explicitly?
2. Should the first review be a bounded starter corpus or a reproducible
   database search suitable for a systematic evidence map?
3. Which translations and licenses are acceptable for quotations in a public
   web application?
4. How should users move between a plain-language learning view and detailed
   textual/scholarly provenance?
5. Does the initial release include empirical contemplative-science evidence,
   or reserve that for a separately appraised layer?
