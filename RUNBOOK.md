# Runbook

## Start a work session

```bash
git status --short --branch
git log --oneline -5
make checks
```

Read the files listed in `AGENTS.md`, then choose one coherent task from
`TODO.md`.

## Concurrent-agent setup

Keep each agent in a separate worktree:

```bash
git worktree add ../sutrastudies-web -b agent/web-app
```

Use the current checkout for literature work and `../sutrastudies-web` for
Claude. Before editing shared control files, inspect both branches. Exchange
work through commits; merge or cherry-pick only validated slices.

If both branches change the schema or shared control files, reconcile those
changes deliberately in one integration branch. Do not resolve conflicts by
blindly taking one side.

## Literature workflow

1. Confirm the question, audience, source boundary, exclusions, and rigor level
   in `literature/protocol.yaml` before full screening.
2. Record each platform, exact query, filters, timestamp, result count, and
   chaining step in `literature/search-log.md`.
3. Assign stable source IDs in `literature/source-inventory.csv`; record access,
   screening stage, decision, and reason.
4. For every included source, create a structured note from
   `literature/notes/SOURCE_NOTE_TEMPLATE.md`.
5. Add comparable evidence to `literature/evidence-matrix.csv`.
6. Add or update material claims in `CLAIMS.md`, including contradictions and
   exact locators.
7. Publish only reviewed concepts and edges to
   `knowledge/exports/mindmap.json`.
8. Run `make checks` and inspect the diff before committing.

Never describe a rapid or bounded review as systematic. Do not count a source
as substantively examined unless its relevant full text was read and appraised.

## Knowledge-export workflow

- Treat `knowledge/schema/mindmap.schema.json` as the interface contract.
- Keep stable concept, edge, claim, and source IDs.
- Every `claim_ids` and `source_ids` value must resolve to a corresponding
  record before publication.
- Set `review_status` honestly. Only `reviewed` concepts and edges belong in a
  public release unless the UI explicitly presents a research/draft mode.
- Coordinate schema changes with Claude and record them in `DECISIONS.md`.

## Web workflow

Claude owns the implementation under `web/`. Development fixtures must be
stored under `web/fixtures/` and labeled synthetic. The app should read the
reviewed export, not parse Markdown research files.

When `web/` exists, Claude should add its setup, test, build, and accessibility
commands here and connect them to a joint release check.

## Handover

1. Run relevant checks.
2. Update `STATUS.md`, `TODO.md`, `DECISIONS.md`, and `CLAIMS.md` as applicable.
3. Review `git diff --check` and `git status --short`.
4. Commit a coherent slice only.
5. Record the validated commit and the next three actions in `STATUS.md`.
