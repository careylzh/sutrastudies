# Decision Log

Record consequential research, product, schema, and coordination choices. Do
not silently rewrite an accepted decision; add a superseding entry.

## D-001 — Adapt the reference repository's agentic evidence workflow

- Date: 2026-08-31
- Status: accepted
- Decision: Reuse the durable control-file, source-inventory, claim-ledger,
  runbook, validation, and handover pattern from `paper-sst-math`, while
  replacing its paper/submission-specific machinery with a Buddhist concept
  review and web-app handoff.
- Rationale: The governance and provenance pattern transfers; the reference
  repository's subject matter, sources, claims, and submission constraints do
  not.
- Consequences: Project state lives in versioned files and public content must
  be traceable to reviewed evidence.

## D-002 — Separate research and web implementation by worktree

- Date: 2026-08-31
- Status: accepted
- Decision: Codex owns the literature and reviewed knowledge layer; Claude Code
  owns the HTML/JavaScript app. Each works on a separate branch and Git
  worktree.
- Rationale: Separate checkouts prevent file and Git-index races while allowing
  both workstreams to progress concurrently.
- Consequences: Shared-file and schema changes require explicit coordination;
  the reviewed JSON export is the integration boundary.

## D-003 — Use a source-aware, tradition-aware graph contract

- Date: 2026-08-31
- Status: provisional pending Claude review
- Decision: Represent concepts and typed relationships in a versioned JSON
  export that carries tradition tags, source terms, claim IDs, source IDs,
  confidence, qualifications, and review state.
- Rationale: A simple label/link graph would hide translation choices,
  contested interpretations, and evidentiary limits that materially affect
  Buddhist concepts.
- Consequences: The UI may simplify presentation, but it must not discard the
  ability to expose provenance and qualifications.

## D-004 — Begin with a bounded core, not a claim of Buddhist completeness

- Date: 2026-08-31
- Status: provisional
- Decision: Plan the first release around a small beginner-oriented core while
  explicitly recording tradition and canon coverage.
- Rationale: “Basic Buddhism” is not a neutral or exhaustive category. A
  bounded release can be audited and expanded without manufacturing consensus.
- Consequences: `PROJECT.md` lists candidate clusters only; inclusion awaits a
  frozen protocol and source review.

## Decision template

### D-XXX — Short title

- Date: YYYY-MM-DD
- Status: proposed/accepted/superseded
- Decision:
- Evidence and alternatives:
- Consequences:
- Supersedes:
