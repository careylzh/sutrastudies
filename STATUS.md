# Status

Date: 2026-08-31

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
- The web app has not yet been created or tested.

## Next three actions

1. Decide and record first-release tradition, canon, language, and source
   boundaries.
2. Freeze the starter review protocol and run documented discovery searches.
3. Have Claude scaffold `web/` against the empty reviewed export and schema.

## Last validated state

- Branch: `agent/literature-scaffold`
- Validation: `make checks`
- Commit: pending
