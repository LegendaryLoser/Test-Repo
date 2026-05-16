---
id: CHG-0010
title: Install BMAD v6.6.0 (vendored) + amend ADR-0002 to match reality
status: in-progress
date: 2026-05-16
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0001
    - ADR-0002
---

# CHG-0010 — Install BMAD v6.6.0 (vendored) + ADR-0002 amendment

## Why

[`ADR-0002`](../../architecture/decisions/ADR-0002-bmad-integration.md) was
written before BMAD v6.6.0 was actually examined. The install probe in
this session surfaced three substantive mismatches between the ADR and
upstream reality:

1. **Install path:** ADR says `bmad/`; BMAD installs to `_bmad/`
   (underscore-prefixed).
2. **Integration mechanism:** ADR designed thin wrappers in
   `.claude/agents/` and `.claude/commands/`. BMAD v6 uses native Claude
   Code Skills installed directly into `.claude/skills/` (42 of them,
   the "Skills Architecture" feature added in v6).
3. **Side-effect directories:** install creates `docs/` and
   default-named subdirs under the configured output folder, even when
   the underlying config points elsewhere.

The mismatches reflect a real simplification — native skills are
**better** than the wrapper-isolation we designed because BMAD handles
versioning, manifest generation, and upgrades natively. No wrapper layer
to maintain. The ADR amendment captures the actual integration.

## Decision: vendor everything (selected via session AskUserQuestion)

Per the cost/benefit comparison surfaced in chat: vendoring `_bmad/` + 
`.claude/skills/` (~2.6 MB total) aligns with our SoT principle (P1),
preserves container-reclaim resilience (ADR-0005 §8), and pays a one-time
commit cost for permanent reproducibility. Network is required only on
upgrade (substrate PR cadence — rare).

Routed BMAD outputs under `openspec/_bmad-output/{planning,implementation,
knowledge}/` so all BMAD-generated content stays inside the OpenSpec
namespace (P1 again — single source of truth for product knowledge).

## What changes

### Install
- Run `npx bmad-method install --yes --tools claude-code --modules bmm
  --action install --user-name "spec-lint" --output-folder openspec/_bmad-output
  --set bmm.planning_artifacts=openspec/_bmad-output/planning
  --set bmm.implementation_artifacts=openspec/_bmad-output/implementation
  --set bmm.project_knowledge=openspec/_bmad-output/knowledge`.
- Captured in `scripts/install_bmad.sh` for reproducibility / upgrades.

### Vendored files
- `_bmad/` (~172 KB) — BMAD core + bmm module + config.
- `.claude/skills/` (~2.4 MB, 42 skills) — native Claude Code Skills.
- `openspec/_bmad-output/.gitkeep` — preserves the routing namespace.
- `scripts/install_bmad.sh` — pinned install command.

### Cleanup
- Empty `docs/` (BMAD side effect) — **removed**.
- Empty default-named `openspec/_bmad-output/{planning-artifacts,
  implementation-artifacts}/` (created at install before config takes
  effect) — **removed** since the configured names take precedence.

### Substrate amendments

- **[`ADR-0002`](../../architecture/decisions/ADR-0002-bmad-integration.md)**
  — large rewrite (amendment 0001):
  - Install path: `_bmad/` not `bmad/`.
  - Drop wrapper-isolation; document native skills under `.claude/skills/`.
  - Routed output configuration documented.
  - Upgrade path: `scripts/install_bmad.sh` + commit the diff.
- **[`ARCHITECTURE.md` §3](../../architecture/ARCHITECTURE.md)** — layout
  tree updated: `bmad/` → `_bmad/`; `.claude/skills/` added.
- **[`tools/ci/tests/test_phase0.py`](../../../tools/ci/tests/test_phase0.py)**
  `ALLOWED_TOP_LEVEL_ENTRIES`: add `_bmad`; remove `bmad`. `.claude` stays
  (it now contains `skills/` in addition to `settings.json`, `agents/`,
  `commands/`); `scripts` added.
- **[`.gitignore`](../../../.gitignore)** — none needed (we vendor; not
  gitignoring).

## Out of scope

- The 4 new lint rules (`top-level-allowlist`, `bmad-direct-reference`,
  `mock-in-repo-banned`, `openspec-validate`) — split into CHG-0011 and
  CHG-0012 per the session plan.
- Extending reliability instrumentation to cover the new rules — CHG-0013
  through CHG-0015.
- LLM augmentation decision — CHG-0016 after all reliability data is in.

## Tasks

- [`TASK-0019`](tasks/TASK-0019.md) — type `impl`: install BMAD; vendor
  the files; cleanup empty dirs; add install script. Will leave
  TEST-ARCH-0001 RED because the allowlist doesn't yet include `_bmad`.
- [`TASK-0020`](tasks/TASK-0020.md) — type `docs`: amend ADR-0002,
  ARCHITECTURE.md §3, and TEST-ARCH-0001's allowlist. Tests return to green.

## Rollout

- **Substrate change** — under hybrid policy, you merge.
- Large diff (2.6 MB) expected — most of it is vendored skill markdown
  and BMAD scripts; the architectural change is in ADR-0002, ARCHITECTURE.md,
  and a handful of lines in the test allowlist.
- Push immediately after each commit per the push invariant.
