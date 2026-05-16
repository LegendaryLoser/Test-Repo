---
id: CHG-0011
title: top-level-allowlist + openspec-validate gates (spec_lint runnable CLI)
status: in-progress
date: 2026-05-16
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0001
    - ADR-0004
    - ADR-0008
---

# CHG-0011 — `top-level-allowlist` + `openspec-validate` gates

## Why

Per [`ADR-0008` §1](../../architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md),
the next two PHASE-1 gates owned by `tools/spec_lint` are:

| Gate                  | Enforces           |
|-----------------------|--------------------|
| `top-level-allowlist` | [`ADR-0001`](../../architecture/decisions/ADR-0001-monorepo-layout.md) — top-level layout matches ARCHITECTURE.md §3 |
| `openspec-validate`   | [`ADR-0004`](../../architecture/decisions/ADR-0004-spec-storage-discipline.md) — every spec file in `openspec/` conforms to its format |

Both are runnable today (existing rule infrastructure handles each
individually). Two pieces are still missing:

1. **A `RepoRule` protocol + the `top-level-allowlist` rule itself.** The
   existing `Rule`, `CrossFileRule`, `CorpusRule`, `HistoricalRule`
   protocols all assume per-file or whole-corpus input. None fits a
   "check repository layout against an allowlist" check. A new protocol
   parametrized on `repo_root` is the minimal addition.
2. **A runnable spec_lint CLI.** Currently every rule is exercised only
   by pytest. `openspec-validate` is the aggregator — it runs every
   relevant rule across `openspec/` and reports. Once it exists,
   PHASE-2's `phase-exit` gate and the placeholder CI workflow can both
   call it instead of `pytest tools/spec_lint`.

## What changes

### `tools/spec_lint/_top_level_allowlist.py` (new)

Extracts `REQUIRED_TOP_LEVEL_DIRS` and `ALLOWED_TOP_LEVEL_ENTRIES`
constants from `tools/ci/tests/test_phase0.py` into a single source of
truth importable by both the lint rule and the architecture invariant
test (P1 — duplicate constant resolved).

### `tools/spec_lint/rules/top_level_allowlist.py` (new)

`TopLevelAllowlist` rule. Implements the new `RepoRule` protocol
(added to `tools/spec_lint/rules/base.py`). `check_repo(repo_root)`
runs `git ls-files`, derives the set of tracked top-level entries, and
returns one `Finding` per:

- Missing required entry (`severity=error`).
- Unexpected tracked entry not in the allowlist (`severity=error`).

### `tools/spec_lint/__main__.py` (new)

CLI entry point. `python -m tools.spec_lint <subcommand>`:

- `validate [path]` — runs every applicable rule over `openspec/`
  (or the given path). Exits 0 if no findings, 1 otherwise. Prints
  Findings to stderr in the standard `path:line: severity: rule_id: msg`
  format.
- `check-layout` — invokes `TopLevelAllowlist.check_repo(<cwd>)` and
  reports findings the same way.

### `tools/ci/tests/test_phase0.py` (refactor)

`test_arch_0001_top_level_layout` becomes a thin wrapper that calls
`TopLevelAllowlist.check_repo(repo_root)` and asserts no findings.
Constants imports moved to `tools.spec_lint._top_level_allowlist`.
No behavior change; resolves duplication.

### `openspec/specs/_meta/spec-storage.spec.md` (new)

Creates `REQ-SPEC-0001` — *"every spec file under `openspec/` conforms
to the format enforced by `tools/spec_lint`'s rules"* — covered by
`openspec-validate`. This is the PHASE-1 scope item 6 deliverable.

### `openspec/architecture/ARCHITECTURE.md` §3 (precision fix)

Adds `.gitignore` and `pyproject.toml` to the documented top-level
layout. Both are tracked in git and currently in
`ALLOWED_TOP_LEVEL_ENTRIES` but missing from the §3 tree diagram. SoT
alignment, no semantic change.

## Tasks

- **TASK-0022 (RED)** — write failing tests for both gates.
- **TASK-0023 (GREEN)** — implement rule + CLI + REQ-SPEC + ARCHITECTURE.md fix.

## Out of scope

- Wiring `openspec-validate` into `.github/workflows/ci.yml` (separate
  CHG; the placeholder echo step in the current workflow is a deliberate
  PHASE-0 stub. CHG-0017 or similar promotes all CI placeholders to real
  invocations together once PHASE-1 gates are all implemented).
- Other PHASE-1 gates (`bmad-direct-reference`, `mock-in-repo-banned`,
  `gas-global-outside-adapter`, `index-up-to-date`,
  `direct-anthropic-import-banned`, `stochastic-tier-bans`,
  `semantic-recall-recall-at-k`). Each gets its own CHG.
- Parsing ARCHITECTURE.md §3 to derive the allowlist programmatically
  (future SoT improvement; current state keeps the Python constant as
  SoT with the architecture invariant test asserting alignment).
