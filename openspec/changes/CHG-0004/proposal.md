---
id: CHG-0004
title: spec_lint — req-id-immutable + req-append-only (git-history rules)
status: in-progress
date: 2026-05-16
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0004
    - ADR-0006
    - ADR-0008
---

# CHG-0004 — spec_lint: req-id-immutable + req-append-only

## Why

Second slice of PHASE-1 spec_lint. The two rules in this CHG share a new
substrate — **git history walking** — that the simpler per-file rules in
CHG-0003 did not need. Splitting them off keeps the PR reviewable and
isolates the new adapter for focused testing.

The rules being enforced:

- **`req-id-immutable`** ([`ADR-0004` §1](../../architecture/decisions/ADR-0004-spec-storage-discipline.md)) —
  a REQ-ID, once introduced, never disappears from the spec file. The only
  permitted lifecycle move is `status: deprecated`; the REQ block stays in
  the file. Renames are forbidden; supersession is the only path.
- **`req-append-only`** ([`ADR-0004` §7](../../architecture/decisions/ADR-0004-spec-storage-discipline.md)) —
  once a REQ reaches `status: tests-green`, its `### Description` and
  `### Acceptance` bodies are frozen. Cosmetic edits require a `revision`
  bump.

## What changes

### New adapter: `tools/spec_lint/git_history.py`

Wraps `git log` + `git show` via subprocess to retrieve historical content of
a spec file. Real subprocess against real git — no mock per
[`ADR-0006` §2](../../architecture/decisions/ADR-0006-testing-tiers.md).
Yields `HistoricalVersion(sha, timestamp, content, spec_file)` tuples ordered
oldest→newest.

PHASE-1 scope simplifications (documented explicitly):
- No `--follow`. File renames within history are not tracked. Cross-file REQ
  moves are out of scope until CHG-0006.
- Works against the current working repo; tests use ephemeral repos under
  pytest's `tmp_path`.

### New rule protocol: `HistoricalRule`

Distinct from the per-file `Rule` protocol added in CHG-0003. Signature
takes a `list[HistoricalVersion]` for one spec file at a time.

### Rules
- `rules/req_id_immutable.py` — walks the version list, computes the set
  difference between adjacent commits' REQ-ID sets, flags any ID that
  vanished.
- `rules/req_append_only.py` — for each REQ that ever reached
  `tests-green`, walks subsequent versions and flags body changes without
  a `revision` bump.

### Tests
- `tools/spec_lint/tests/history_helpers.py` — `make_repo_with_history(tmp_path,
  file_rel, versions)`: initializes a git repo, commits each `content` in
  sequence with `user.name = "Test"`, returns the repo path. Real git,
  real subprocess.
- `tools/spec_lint/tests/test_git_history.py` — adapter exercises:
  empty history, single commit, multiple commits, content equality with
  the file on disk at HEAD.
- `tools/spec_lint/tests/test_req_id_immutable.py` — scenarios:
  unchanged history (clean), deprecation in place (clean), removal
  (finding), rename (finding).
- `tools/spec_lint/tests/test_req_append_only.py` — scenarios:
  never-green (clean), frozen-after-green (clean), revision-bump-with-body-change
  (clean), silent-body-edit-after-green (finding).

## Out of scope

- `--follow` and cross-file REQ moves — deferred to CHG-0006 alongside the
  cross-file rules (`anti-aliasing`, `compound-requirement-detector`).
- "If no downstream artifact refers to the prior revision body" clause of
  ADR-0004 §7 — requires the cross-reference graph from CHG-0005. For
  PHASE-1 the rule treats *all* tests-green REQ bodies as frozen modulo
  revision bumps; tightening to "downstream-referenced only" lands in a
  CHG-0005 follow-up.
- CLI entry point — still deferred until enough rules exist to justify.
- Wiring lint into CI — still PHASE-2 work alongside `tools/trace`.

## Tasks

- [`TASK-0006`](tasks/TASK-0006.md) — type `test-red`: adapter stub,
  rule stubs, history helpers, full test bodies. Tests fail at NIE.
- [`TASK-0007`](tasks/TASK-0007.md) — type `impl`: implement adapter and
  both rules. Tests pass.

## Rollout

- Single PR, intra-phase. Self-merge under hybrid policy.
- Push immediately after each commit (ADR-0005 §6 amendment 0001).
