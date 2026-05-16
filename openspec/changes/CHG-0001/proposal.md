---
id: CHG-0001
title: PHASE-0 verification — author red-first tests for REQ-ARCH-0001..0008
status: in-progress
date: 2026-05-16
phase: PHASE-0
references:
  story: null            # PHASE-0 substrate predates the product story chain
  epic: null
  adrs:
    - ADR-0001
    - ADR-0002
    - ADR-0003
    - ADR-0004
    - ADR-0005
    - ADR-0006
    - ADR-0007
    - ADR-0008
---

# CHG-0001 — PHASE-0 verification

## Why

The bootstrap commit `832a63d` landed the architecture artifact as an exempt
substrate commit (`Bootstrap: true`). The remaining PHASE-0 obligation is to
verify the substrate mechanically — every `REQ-ARCH-NNNN` in
`openspec/architecture/ARCHITECTURE.md` §10 must have a passing test before
PHASE-0 can be marked done and PHASE-1 can begin.

## What changes

1. Add Python tooling skeleton: `pyproject.toml`, `tools/ci/`,
   `tools/ci/tests/`. Rationale for Python (over TypeScript) is recorded in
   this proposal:

   - Hook startup latency matters
     ([`ADR-0005` §6](../../architecture/decisions/ADR-0005-traceability-and-journaling.md));
     Python cold-starts faster than `node + tsx`.
   - Anti-aliasing
     ([`ADR-0004` §4](../../architecture/decisions/ADR-0004-spec-storage-discipline.md))
     is n-gram similarity — trivial in Python, heavier in TypeScript.
   - Property-based invariants on `rebuild` and journal recovery
     ([`ADR-0005` §2, §8](../../architecture/decisions/ADR-0005-traceability-and-journaling.md))
     are first-class with `hypothesis`; TypeScript equivalents are weaker.
   - Python is already mandatory (`packages/shared-py/`); no new language.
   - Hook command paths in `.claude/settings.json` already use `.py`.

   TypeScript remains the language for `projects/` (clasp) and
   `packages/shared-ts/`. This is consistent with
   [`ADR-0003`](../../architecture/decisions/ADR-0003-appscript-runtime.md)
   and [`ADR-0006`](../../architecture/decisions/ADR-0006-testing-tiers.md).

2. Add `tools/ci/tests/test_phase0.py` with eight tests, one per
   `REQ-ARCH-NNNN`. Tests read files only — no other infrastructure required.

3. Red-first sequence enforced by two commits:
   - `TASK-0001` commit: test file present with `pytest.fail(...)` stubs (RED).
   - `TASK-0002` commit: stubs replaced with real assertions (GREEN).

## Tasks

- [`TASK-0001`](tasks/TASK-0001.md) — type `test-red`: scaffold tooling + RED stubs.
- [`TASK-0002`](tasks/TASK-0002.md) — type `impl`: implement assertions; turn green.

## Rollout

- Lands on `claude/general-session-KXgas`, merges to `master` as a single PR.
- Closes PHASE-0. PHASE-1 may begin only after the `phase-exit` gate (PHASE-2
  deliverable) is in place; until then PHASE-0 closure is verified manually
  by running `pytest tools/ci/tests/test_phase0.py` locally.

## Notes

- `Requirements:` trailer on each commit lists all eight `REQ-ARCH-NNNN`,
  since the test file is one artifact covering all of them.
- `Tests-Status:` on TASK-0001 commit is `red`; on TASK-0002 commit is
  `red→green`.
- No CI gate is yet wired (the workflow files are PHASE-0 placeholders).
  Local verification only until PHASE-2 lands `tools/trace`.
