---
id: PHASE-2
title: Traceability runtime — hooks, rebuild, CI gates green
status: pending
entry: PHASE-1 exit criteria all tests-green
---

# PHASE-2 — Traceability runtime

## Goal

Replace the PHASE-0 placeholder hooks with real implementations. Wire up the
matrix rebuild, commit-trailer validation, journal append, and CI gates
defined in [ADR-0005](../decisions/ADR-0005-traceability-and-journaling.md) and
[ADR-0008](../decisions/ADR-0008-ci-gates-and-phase-exits.md).

## Entry criteria

- PHASE-1 exit gate passed.

## Scope

1. `tools/trace/` implementations:
   - `resume.py` (SessionStart hook)
   - `validate_commit.py` (PreToolUse:git commit + commit-msg hook)
   - `journal_commit.py` — appends `commit` event **and pushes `HEAD` to
     origin as a fast-forward** (push invariant, ADR-0005 §6 amendment 0001;
     aborts on non-FF with a diagnostic).
   - `journal_touch.py`, `journal_tests.py`
   - `post_merge_sync.py` (PostToolUse:mcp__github__merge_pull_request hook;
     ADR-0005 §6 amendment 0001) — fetches origin, fast-forwards the working
     branch to its updated upstream, pushes the FF.
   - `checkpoint.py` (Stop / SessionEnd) — extended to push
     committed-but-unpushed work even when the tree is clean (ADR-0005 §7
     amendment 0001).
   - `rebuild.py` (matrix regeneration from sources)
   - `audit.py` (CLI query interface)
2. `tools/trace/tests/` — red-first tests for each module, including:
   - Property tests for `rebuild.py` idempotence: rebuild(rebuild(x)) == rebuild(x).
   - Crash-recovery tests for the journal: a synthetic torn last-line is
     correctly discarded.
   - P4 enforcement tests: commits violating red-before-green are rejected.
   - Push-invariant tests (ADR-0005 §6 amendment 0001) against a synthetic
     local-and-bare-remote git repo: commit-without-push, merge-without-sync,
     and checkpoint-with-committed-but-unpushed scenarios all resolve to a
     pushed state; non-FF cases halt with a diagnostic instead of force-pushing.
3. `.claude/settings.json` updated: hooks point at real implementations.
4. CI gates promoted from PHASE-0 placeholders to real:
   - `matrix-drift`, `commit-trailers-valid`, `red-before-green`,
     `req-coverage-100`, `tier-coverage`, `phase-exit`, `gate-coverage`,
     `cost-budget`.
   - `matrix-drift` and the matrix builder MUST exclude
     `openspec/_bmad-output/` per
     [`ADR-0002` §7](../decisions/ADR-0002-bmad-integration.md).
   - `skill-removal-acknowledged` gate per
     [`ADR-0002` §8](../decisions/ADR-0002-bmad-integration.md): compares
     `_bmad/_config/skill-manifest.csv` between base and head; blocks PRs
     that remove a skill without a
     `Skill-Removal-Acknowledged: <skill-id>` trailer.
   - `bmad-version-pin` gate: asserts `_bmad/_config/manifest.yaml`
     version matches the comment in `scripts/install_bmad.sh`.
   - `bmad-smoke-test`: exercises one BMAD skill end-to-end on every
     BMAD upgrade PR (lives in `tools/ci/smoke_bmad.py`).
5. `openspec/specs/_meta/ci-gates.spec.md` — REQ-CI-* requirements covering
   each gate.

## Exit criteria

- All gates in [ADR-0008 §1](../decisions/ADR-0008-ci-gates-and-phase-exits.md)
  not owned by `tools/spec_lint` are implemented and passing on the current
  repo state.
- `gate-coverage` passes (every ADR / principle has ≥ 1 gate referencing it).
- `audit REQ-ARCH-0001` (and similar) returns deterministic output that
  reconciles with git + journal.
- Synthetic crash scenarios pass: deleting `matrix.yaml` then rebuilding
  produces the prior content; appending a torn JSONL line then re-parsing
  succeeds with the line discarded.

## Out of scope

- Anthropic client — PHASE-3.
- Shared libraries — PHASE-4.

## Exit gate

`phase-exit` verifies all REQ-CI-* tests-green and the synthetic
crash-recovery suite passes.
