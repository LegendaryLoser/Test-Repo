---
id: ADR-0002
title: BMAD integration (v6.6.0 vendored, native Skills, openspec-routed output)
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0002 — BMAD integration (v6.6.0 vendored, native Skills, openspec-routed output)

## Context

We use BMAD personas (PM, Architect, SM, Dev, PO) and the Test Architect
(TEA) discipline as the workflow surface. BMAD v6.6.0 is released (April
2026), MIT-licensed, and ships a "Skills Architecture" that installs
directly into Claude Code's native `.claude/skills/` directory — no
wrapper layer is required.

This ADR captures the actual integration after the BMAD install was
empirically validated in CHG-0010. The original ADR text designed a
wrapper-isolation strategy based on outdated assumptions about BMAD
exposing personas as Claude Code subagents — that turned out to be
neither how BMAD v6 works nor necessary, since native Skills are a
better-engineered alternative we couldn't have improved upon.

## Decision

1. **Version pin: BMAD v6.6.0.** Pinned in `_bmad/_config/manifest.yaml`
   at install time (canonical version source). The pinned install command
   lives in [`scripts/install_bmad.sh`](../../../scripts/install_bmad.sh).

2. **Install path: `_bmad/`** (underscore-prefixed, per upstream's
   convention). Contains BMAD core, the `bmm` module, custom-overrides
   slot, and runtime scripts. **Total size: ~172 KB.**

3. **Integration: native Claude Code Skills under `.claude/skills/`.**
   BMAD installs 42 Skills directly. No wrapper files. Claude Code
   discovers them automatically. **Total size: ~2.4 MB.**

4. **Vendored storage.** Both `_bmad/` and `.claude/skills/` are committed
   to git. This aligns with our SoT principle (P1) and our container-
   reclaim resilience design (ADR-0005 §8): zero network dependency on
   session start; reproducible across machines. Upgrades are deliberate
   substrate PRs (rare cadence; v6.x minors land months apart).

5. **Output routing under `openspec/_bmad-output/`.** BMAD's `bmm` module
   has three configurable output paths:
   - `bmm.planning_artifacts` → `openspec/_bmad-output/planning`
   - `bmm.implementation_artifacts` → `openspec/_bmad-output/implementation`
   - `bmm.project_knowledge` → `openspec/_bmad-output/knowledge`
   This keeps all BMAD-generated content inside the OpenSpec namespace —
   the SoT for product knowledge. No top-level `docs/` directory is
   created (install side effect; cleaned up by the install script).

6. **Upgrade procedure:**
   - Bump the pinned version in [`scripts/install_bmad.sh`](../../../scripts/install_bmad.sh).
   - Run the script.
   - Open a substrate PR with the diff (large, expected; mostly
     vendored skill markdown).
   - You merge after review.

7. **No project code depends on BMAD directly.** Tooling integration lives
   under `tools/tea/` (PHASE-1+ work; not yet implemented). All BMAD
   skill invocation is via Claude Code's native skill system.

## Consequences

- Zero network dependency at session start.
- Upgrades are atomic (one substrate PR per version bump) and reviewable
  (diff shows exactly what changed).
- The 2.6 MB commit is a one-time cost; most repos vendor larger
  dependencies without trouble.
- BMAD's native Skills are first-class Claude Code constructs — no
  wrapper maintenance burden, no per-version adapter code.
- Output routing under `openspec/` enforces P1 (SoT) for product knowledge.

## Compliance

- **`bmad-direct-reference` lint rule** (PHASE-1, CHG-0012) checks that
  no file under `tools/`, `packages/`, or `projects/` references a path
  under `_bmad/` except authorized integration points (`tools/tea/`
  when it exists).
- **`top-level-allowlist` lint rule** (PHASE-1, CHG-0011) enforces that
  `_bmad`, `scripts`, `.claude` (with `skills/` inside) are the BMAD-
  related top-level entries.
- The pinned version in `_bmad/_config/manifest.yaml` is checked in CI
  against the `install_bmad.sh` version comment (PHASE-2).

## Amendment log

| Amendment | CHG     | Sections | Summary                                                                                                         |
|-----------|---------|----------|-----------------------------------------------------------------------------------------------------------------|
| 0001      | CHG-0010 | All       | Complete rewrite to match BMAD v6.6.0 empirical reality. Install path: `_bmad/` (was `bmad/`). Integration: native Claude Code Skills under `.claude/skills/` (was thin wrappers under `.claude/agents/` and `.claude/commands/`). Output routing under `openspec/_bmad-output/` documented. Vendored storage selected over install-on-session-start after user-confirmed cost/benefit analysis. The wrapper-isolation strategy from the original ADR is dropped — native Skills make it unnecessary. |

Amendments are append-only. A subsequent material change to behavior
introduced by a prior amendment requires a new amendment row, never an
edit to a prior row.
