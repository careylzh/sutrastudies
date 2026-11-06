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

## Contents

- [`web/`](web/) — the site: one page with a drawer of curated texts. It has
  the Great Compassion Mantra phrase reader and the six-syllable mantra from
  *The Basket’s Display* as a repetition counter, with sourced notes and a
  concepts panel fed by the reviewed knowledge export. Open `web/index.html`.
- [`great-compassion-mantra/`](great-compassion-mantra/) — a tap-through,
  line-by-line reader for the 大悲咒 (Nīlakaṇṭha Dhāraṇī, Taishō T. 1060) with
  the Taishō Chinese, Lokesh Chandra's reconstructed Sanskrit and English side
  by side, plus a statistics drawer. Open `great-compassion-mantra/index.html`
  in a browser.

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
make web      # rebuild the site after data or export changes
```

To work concurrently, use a separate worktree and branch for each agent:

```bash
git worktree add ../sutrastudies-web -b agent/web-app
```

Run Claude Code from `../sutrastudies-web`. Do not run two writing agents in
the same working directory.
