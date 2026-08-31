# Agent Rules

These rules apply to every coding, research, and writing agent in this
repository.

## Required reading

Before starting, read `PROJECT.md`, `STATUS.md`, `TODO.md`, `RUNBOOK.md`,
`DECISIONS.md`, and recent Git history. Inspect files before editing and treat
the repository as durable project memory rather than relying on chat context.

## Ownership and concurrent work

- Codex owns `literature/`, `knowledge/`, `CLAIMS.md`, and research-facing
  updates to the control files.
- Claude Code owns `web/` and implementation-facing updates to the control
  files.
- `README.md`, `AGENTS.md`, `PROJECT.md`, `STATUS.md`, `TODO.md`, `RUNBOOK.md`,
  and `DECISIONS.md` are shared. Before editing them, pull or inspect the other
  agent's latest commits and keep changes narrow.
- Use separate Git worktrees and branches. Never run two writing agents in the
  same checkout.
- Do not stage or commit another agent's unrelated changes. Prefer small,
  coherent commits that can be merged or cherry-picked.
- The web app consumes `knowledge/exports/mindmap.json`; it must not scrape
  research notes or infer content from draft prose.
- Schema changes require a decision-log entry and coordination with the web
  owner before merge.

## Research integrity

- Do not fabricate texts, citations, translations, quotations, historical
  claims, lineages, practices, health effects, or scholarly consensus.
- Verify bibliographic identity and exact locators before a source supports a
  published claim. Label full-text, excerpt-only, abstract-only, and
  metadata-only access honestly.
- Record searches and eligibility decisions. Preserve null, negative,
  contradictory, and tradition-specific evidence.
- Distinguish source-explicit statements from agent inference and editorial
  explanation. Do not turn a pedagogical simplification into a historical fact.
- Prefer primary Buddhist texts for what a text teaches and critical
  scholarship for historical, comparative, linguistic, and interpretive claims.
  Modern teachers may illuminate a tradition but do not establish universal
  Buddhist consensus.
- Record the canon, language, translation, translator, edition, passage, and
  tradition relevant to a textual claim. Do not silently merge Pali, Sanskrit,
  Chinese, Tibetan, or modern interpretive vocabularies.
- Avoid treating Buddhism as a single timeless doctrine. Mark disagreements,
  translation alternatives, historical layers, and school-specific readings.
- Quotations must be short, necessary, accurately transcribed, and compatible
  with copyright and licensing constraints. Prefer paraphrase plus a locator.

## Reader safety and scope

- Describe practices as teachings or invitations, not guaranteed treatments.
- Do not claim that a concept or practice cures, prevents, or reliably reduces a
  mental-health condition without evidence appropriate to that claim.
- Do not imply that suffering is a personal failure, that painful circumstances
  are deserved, or that professional help is spiritually inferior.
- Clearly distinguish canonical doctrine, historical interpretation,
  contemporary application, and the project's own pedagogical framing.
- Preserve terms whose translation is contested; show a plain-language gloss
  alongside the original term instead of pretending the gloss is exhaustive.

## Knowledge and app editing

- Every published concept or edge must trace to entries in the source inventory
  and `CLAIMS.md`.
- Use stable IDs. Do not recycle deleted IDs for different concepts or sources.
- Keep interpretation and UI presentation separate from evidence fields.
- The reviewed export must validate against
  `knowledge/schema/mindmap.schema.json` before the app consumes it.
- Claude may create fixtures for UI development, but fixtures must be visibly
  labeled synthetic and must not be merged into the reviewed export.

## Validation and handover

Before ending a completed session:

1. Complete or revert incomplete agent-created changes.
2. Run `make checks` and workstream-specific tests.
3. Update `STATUS.md` and any changed task, decision, or claim records.
4. Review `git diff --check` and `git status --short`.
5. Commit only a coherent, validated slice.
6. Leave the next three recommended actions in `STATUS.md`.
