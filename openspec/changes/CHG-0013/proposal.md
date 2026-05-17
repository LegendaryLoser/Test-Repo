---
id: CHG-0013
title: CI wiring — replace spec-lint job placeholder with real gate invocations
status: in-progress
date: 2026-05-17
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0008
---

# CHG-0013 — CI wiring

## Why

The post-merge audit (see chat, finding C4) named this the **single
highest-leverage gap in the project**: 13 PHASE-1 lint rules exist as
runnable CLI commands; zero are enforced in CI. Every `.github/workflows/
ci.yml` job still executes a placeholder
`echo "TODO PHASE-X: ..."; exit 0` step. A PR introducing any of the
violations the rules detect (banned mocks, `_bmad/` imports, malformed
REQs, broken cross-references, prose-xrefs, …) merges cleanly today.

The rules don't protect the repo until they run on every PR. Until then,
every claim of "the gate enforces X" in commit messages and PR
descriptions is aspirational.

## What changes

### `.github/workflows/ci.yml` (rewrite of `spec-lint` job only)

Replace the placeholder `run: echo "TODO PHASE-1..."` step with real
steps:

1. `actions/checkout@v4` with `fetch-depth: 0` (history-based rules
   `req-id-immutable` + `req-append-only` need full history).
2. `actions/setup-python@v5` with `python-version: "3.11"` (matches
   `pyproject.toml`'s `requires-python`).
3. Install dev dependencies: `pip install -e ".[dev]"`.
4. `python -m tools.spec_lint validate openspec` — runs every CHG-0003
   through CHG-0012 lint rule over `openspec/` markdown + code rules
   (`bmad-direct-reference`, `mock-in-repo-banned`) over `tools/`,
   `packages/`, `projects/` source. Exits 1 on findings.
5. `python -m tools.spec_lint check-layout` — runs
   `top-level-allowlist` over the repo (REQ-ARCH-0001).
6. `pytest tools/ -v` — runs all 179 tests including
   `test_annotation_discipline` (REQ-SPEC-0013), parser/history/benchmark
   tests, mutation tests, property tests, and architecture invariants
   (REQ-ARCH-0001..0008).

Each step has a `name:` for CI log readability.

### `openspec/specs/_meta/spec-storage.spec.md` extended

- **REQ-SPEC-0014** — `.github/workflows/ci.yml`'s `spec-lint` job runs
  the spec_lint CLI gates and the full pytest suite on every pull
  request, exiting non-zero if any gate reports findings or any test
  fails.

### `tools/ci/tests/test_workflow_wiring.py` (new)

Meta-test parsing `.github/workflows/ci.yml` as YAML and asserting the
`spec-lint` job satisfies REQ-SPEC-0014:
- Triggers on `pull_request` and `push` to master/main.
- Has Python setup, dependency install, validate, check-layout, and
  pytest steps.
- No step's `run:` field contains `TODO PHASE-1` or just `echo`-and-
  exit (the placeholder pattern).

Covers REQ-SPEC-0014. Self-annotated per the CHG-0030 discipline.

## Out of scope

- `trace-gates` job (PHASE-2 deliverable: `matrix-drift`,
  `commit-trailers-valid`, `red-before-green`, `req-coverage-100`,
  `tier-coverage`, `gate-coverage`). Placeholder remains; deferred to
  PHASE-2.
- `unit-integration` job (PHASE-3+: per-package test matrix).
  Placeholder remains; deferred.
- `phase-exit` job (PHASE-2 deliverable). Placeholder remains.
- `e2e.yml` workflow (nightly). Out of CHG-0013 scope.
- `spec-discipline.yml` workflow (named in PHASE-0 layout but never
  populated). Out of scope; treated separately if needed.

## Tasks

- **TASK-0029 (RED)** — meta-test asserting CI wiring contract;
  RED because workflow still has placeholder.
- **TASK-0030 (GREEN)** — rewrite workflow + add REQ-SPEC-0014.
  Meta-test passes.

## Risk

- **`fetch-depth: 0` adds ~seconds to checkout** but is required for
  history-based rules. Acceptable cost.
- **`pytest -v` on 179 tests** takes ~15 seconds locally. CI overhead
  modest.
- **If `validate openspec` finds a new defect** (e.g., reviewer's
  branch introduces a prose-xref), the PR is blocked until fixed. This
  is the intended behavior — that is what the gate is for.
