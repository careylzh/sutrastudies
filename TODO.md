# Task Ledger

Status values: `todo`, `in progress`, `blocked`, `done`, or
`done with limitation`.

## Repository and coordination

| Task | Status | Owner | Dependencies | Acceptance criteria |
|---|---|---|---|---|
| Establish agentic repository scaffold | done | Codex | Reference repository | Control files, workstream boundaries, literature workspace, schema, and checks exist |
| Establish safe concurrent-agent workflow | done | Codex/Claude | Git | Separate worktrees and branches; ownership documented; shared-file edits coordinated |
| Scaffold web application | todo | Claude | Knowledge schema | Accessible HTML/JS app under `web/` loads the empty/reviewed export and passes its tests |

## Literature review

| Task | Status | Owner | Dependencies | Acceptance criteria |
|---|---|---|---|---|
| Confirm first-release review boundary | todo | User/Codex | Project choices | Traditions, canons, languages, date boundary, source types, and rigor level recorded |
| Freeze review protocol | todo | Codex | Review boundary | `literature/protocol.yaml` has operational eligibility criteria and dated deviations |
| Run source discovery | todo | Codex | Frozen protocol | Exact searches, platforms, dates, filters, counts, and citation chaining logged |
| Screen and inventory sources | todo | Codex | Discovery results | Stable source IDs, access levels, decisions, reasons, duplicate/overlap status recorded |
| Extract and critically appraise sources | todo | Codex | Included full texts | Each included source has a structured note with exact locators and design-appropriate appraisal |
| Build claim-evidence ledger | todo | Codex | Appraised sources | Each material concept statement and relationship has support, qualifications, status, and provenance |

## Knowledge handoff

| Task | Status | Owner | Dependencies | Acceptance criteria |
|---|---|---|---|---|
| Define mind-map interchange schema | done with limitation | Codex/Claude | Initial product boundary | Versioned schema covers concepts, typed edges, provenance, traditions, and review state; Claude review pending |
| Publish first reviewed concept cluster | todo | Codex | Claims ledger | Export validates; every concept and edge is source-backed; draft material is excluded |
| Integrate reviewed export in app | todo | Claude | First reviewed export | UI renders supported fields and visibly handles uncertainty, traditions, and unavailable detail |
| Add joint release check | todo | Codex/Claude | App tests and reviewed content | One command validates research data, app tests, accessibility checks, and broken references |
