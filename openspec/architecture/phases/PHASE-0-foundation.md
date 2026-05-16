---
id: PHASE-0
title: Foundation — architecture artifact, session-level scaffolding
status: in-progress
entry: repository is empty (only README.md, initial commit)
---

# PHASE-0 — Foundation

## Goal

Produce the immutable architectural substrate on which every later phase
depends. No executable code in this phase except hook **declarations**
(implementations land in PHASE-2).

## Entry criteria

- Repository has only `README.md` and `.git/`.
- Branch `claude/general-session-KXgas` exists.

## Scope

1. `openspec/architecture/ARCHITECTURE.md`
2. `openspec/architecture/decisions/ADR-0001` through `ADR-0008`
3. `openspec/architecture/phases/PHASE-0` through `PHASE-5`
4. Empty templates:
   - `openspec/vision.md`
   - `openspec/briefs/_TEMPLATE.md`
   - `openspec/prd/_TEMPLATE.md`
   - `openspec/epics/_TEMPLATE.md`
   - `openspec/stories/_TEMPLATE.md`
5. `openspec/specs/INDEX.yaml` (empty `requirements:` block)
6. `openspec/changes/_TEMPLATE/` directory with empty change-proposal skeleton
7. `openspec/traceability/matrix.yaml` (empty cache, regeneration is a no-op
   until specs exist)
8. Root `CLAUDE.md` referencing the five principles verbatim
9. `.claude/settings.json` with hook **declarations** pointing at placeholder
   commands that exit 0 with a TODO comment
10. `.github/workflows/` with `ci.yml`, `spec-discipline.yml`, `e2e.yml` as job
    declarations whose steps are TODO placeholders
11. `.gitignore` covering `.claude/journal/`, `.claude/settings.local.json`,
    Node and Python artifacts
12. `bmad/` is **not** installed in PHASE-0; it lands in PHASE-1 alongside
    `tools/spec-lint`

## Exit criteria

All of the following REQ-ARCH-* must be `tests-green` in the matrix:

- `REQ-ARCH-0001` — top-level layout matches ARCHITECTURE.md §3.
- `REQ-ARCH-0002` — all ADRs and phase files present.
- `REQ-ARCH-0003` — empty product templates present, no product content.
- `REQ-ARCH-0004` — `openspec/specs/INDEX.yaml` parses.
- `REQ-ARCH-0005` — all cross-references in `openspec/architecture/` resolve.
- `REQ-ARCH-0006` — no executable code under `openspec/architecture/`.
- `REQ-ARCH-0007` — root `CLAUDE.md` cites the five principles verbatim.
- `REQ-ARCH-0008` — `.claude/settings.json` declares all hooks from ADR-0005 §6.

Tests for REQ-ARCH-* are written in PHASE-0 itself, red-first, and turn green
as the scaffolding completes. The tests live in `tools/ci/tests/test_phase0.py`
and are runnable without any phase-1+ infrastructure (they only read files).

## Out of scope

- Any spec lint rule implementation (PHASE-1).
- Any traceability runtime implementation (PHASE-2).
- BMAD installation (PHASE-1).
- Any product content (separate product PR).

## Exit gate

`phase-exit` CI gate verifies all REQ-ARCH-* are `tests-green` and ADR-0001..8
are `status: accepted`.
