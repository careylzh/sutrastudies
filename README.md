# Sutra Studies

Sutra Studies is an evidence-grounded, interactive mind map for learning and
revising foundational Buddhist concepts. Its aim is to help curious readers
understand teachings that Buddhist traditions use to diagnose and respond to
suffering, wherever they are, through careful study and introspection.

This repository has two deliberately separate workstreams:

- **Literature and knowledge layer (Codex):** source discovery, textual and
  scholarly review, critical appraisal, concept records, claim provenance, and
  the reviewed JSON export.
- **Web application (Claude Code):** HTML, CSS, JavaScript, interaction design,
  accessibility, tests, and deployment under `web/`.

The project is educational. It does not promise therapeutic outcomes and is not
a substitute for qualified mental-health care, medical care, a teacher, or a
living Buddhist community.

## Start here

Before contributing, read:

1. `AGENTS.md`
2. `PROJECT.md`
3. `STATUS.md`
4. `RUNBOOK.md`
5. `TODO.md`
6. `DECISIONS.md`

Literature work starts with `literature/protocol.yaml`. Web work starts with
`knowledge/README.md`, which defines the reviewed data contract.

## Common commands

```bash
make setup
make checks
```

To work concurrently, use a separate worktree and branch for each agent:

```bash
git worktree add ../sutrastudies-web -b agent/web-app
```

Run Claude Code from `../sutrastudies-web`. Do not run two writing agents in
the same working directory.
