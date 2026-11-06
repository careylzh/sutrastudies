# Reviewed Knowledge Interface

This directory is the boundary between literature review and the web app.

- `schema/mindmap.schema.json` is the versioned interchange contract.
- `exports/mindmap.json` contains only content approved for the corresponding
  review state.

Claude should load the export as data and must tolerate an empty concept list.
Codex should not edit application code to compensate for unsupported content,
and Claude should not promote fixtures or editorial guesses into this export.

## ID conventions

- Concepts: `concept-` plus a stable lowercase slug.
- Edges: `edge-` plus a stable descriptive slug.
- Claims: `C` plus three digits, as recorded in `CLAIMS.md`.
- Sources: `S` plus three digits, as recorded in the source inventory.

## Relationship vocabulary

Initial edge types are `part_of`, `prerequisite_for`, `supports`, `cultivates`,
`counteracts`, `conditioned_by`, `contrasts_with`, `interpreted_as`, and
`textually_linked`. Additions require a schema update, a decision-log entry,
and coordination with the web owner.

The vocabulary encodes editorial relationships, not metaphysical certainty.
Every edge therefore carries provenance, qualifications, confidence, and review
state.
