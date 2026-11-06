# Status

Date: 2026-11-06

## Current state

The repository has an initial agentic scaffold adapted from
`paper-sst-math`. It separates the literature/knowledge workstream from the web
application, defines safe concurrent-agent ownership, and establishes a
versioned JSON contract between them.

One Buddhist source has passed identity, access, license, integrity, and
text-extraction screening but is not yet substantively appraised or included:
the official 84000 translation of the *Kāraṇḍavyūha* (Toh 116), requested by the
user. The evidence matrix, claims ledger, and reviewed mind-map export remain
empty. Candidate concepts in `PROJECT.md` are scoping prompts, not verified
content.

## Latest completed task

- Merged the literature scaffold into the main line alongside the Great
  Compassion Mantra viewer (PR #1).
- Added `web/`: one library-driven app (D-005) with a drawer of curated texts.
  It offers the Nīlakaṇṭha Dhāraṇī (phrase reader) and the six-syllable mantra
  from *The Basket’s Display* (repetition counter, with paraphrased notes
  located in the 84000 translation). The concepts panel reads only reviewed
  entries from the export and currently shows an honest empty state.
- Deployed the site to GitHub Pages (https://careylzh.github.io/sutrastudies/) through a GitHub Actions
  workflow that runs `make checks` before publishing.
- Added web engineering rules to `AGENTS.md`, web commands to `RUNBOOK.md`,
  and `make web` / `make web-checks` (included in `make checks`).

## Earlier completed task

- Added durable project, agent, status, task, decision, claim, and runbook files.
- Added a literature-review protocol, search log, source inventory, appraisal
  template, and evidence matrix.
- Added the reviewed mind-map JSON Schema and an empty conforming export for
  Claude's app to consume.
- Added automated repository checks and concurrent-worktree guidance.
- Preserved the unchanged official 84000 PDF of *The Basket’s Display* under
  `sutras/`, with version, canon, translator, license, URL, and checksum
  provenance; registered it as pending source S001.

## Known limitations

- Review tradition/canon coverage and rigor level still require a project
  decision before substantive searching.
- The JSON validator checks structural and referential invariants but does not
  replace scholarly review.
- The web app has no reviewed concepts to show yet; phrase-mode statistics
  assume the T. 1060 data shape.
- T. 1060 sources are not yet registered in the source inventory.

## Next three actions

1. Decide and record first-release tradition, canon, language, and source
   boundaries, then freeze the starter review protocol.
2. Appraise S001 (*The Basket’s Display*) and publish its first reviewed
   concepts so the mantra entry's concepts panel has real content.
3. Register the T. 1060 sources (Codex) and give the dhāraṇī library entry
   their source IDs (Claude).

## Last validated state

- Branch: `agent/web-app` (fast-forwarded into `main`)
- Validation: `make checks` (repository validator and web checks)
- Commit: see `git log -1` on `main`
