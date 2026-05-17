---
id: CHG-0012
title: bmad-direct-reference + mock-in-repo-banned gates
status: in-progress
date: 2026-05-17
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0002
    - ADR-0006
    - ADR-0008
---

# CHG-0012 — `bmad-direct-reference` + `mock-in-repo-banned` gates

## Why

Per [`ADR-0008` §1](../../architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md),
the next two PHASE-1 gates owned by `tools/spec_lint`:

| Gate                       | Enforces                                                                                                             |
|----------------------------|----------------------------------------------------------------------------------------------------------------------|
| `bmad-direct-reference`    | [`ADR-0002`](../../architecture/decisions/ADR-0002-bmad-integration.md) §6 — no file under `tools/`, `packages/`, or `projects/` may import from or execute `_bmad/`, except authorized integration points (`tools/tea/` when it exists). |
| `mock-in-repo-banned`      | [`ADR-0006`](../../architecture/decisions/ADR-0006-testing-tiers.md) §2 — no `jest.mock`, `vi.mock`, `sinon.stub`, `unittest.mock.patch`, `MagicMock`, `Mock`, `monkeypatch.setattr`, `mocker.patch` applied to modules within this repository. |

Both rules are CrossFileRules (operate over a file set, not parsed
spec files). The vendored `_bmad/` from CHG-0010 makes
`bmad-direct-reference` testable end-to-end against the real tree.

## Design

### `bmad-direct-reference`

**Scan**: `*.py`, `*.ts`, `*.tsx`, `*.js`, `*.jsx`, `*.sh` files under
`tools/`, `packages/`, `projects/`. Other top-level dirs (`_bmad/`,
`scripts/`, `openspec/`, `.claude/`) are out of scope — the gate is
about project code, not BMAD itself or supporting scripts.

**Detect** (import / execution, not arbitrary mentions — to avoid false
positives on docstrings or constants that describe the rule):

- Python: `^\s*import\s+_bmad`, `^\s*from\s+_bmad`,
  `__import__\(["']_bmad`, `importlib\.import_module\(["']_bmad`.
- TS / JS: `from\s+["'].*_bmad/`, `require\(["'].*_bmad/`.
- Shell / subprocess paths: `subprocess\.\w+\(\s*\[\s*["']_bmad/` and
  the equivalent string-list forms.

**Allow** (currently): paths under `tools/tea/` (per ADR-0002 §6) once
that subtree exists. Today `tools/tea/` does not exist, so the gate
allows nothing in this position — equivalent to "any in-scope file
referencing `_bmad/` fails".

**Inline allow marker**: `<!-- spec-lint: allow bmad-direct-reference -->`
on the same line. The rule's own implementation file is exempted
structurally (path-based skip) rather than via markers — markers in
Python source files are noisy and the rule's source is the single
authoritative description.

### `mock-in-repo-banned`

**Scan**: `*.py`, `*.ts`, `*.tsx`, `*.js`, `*.jsx` files under `tools/`,
`packages/`, `projects/`. Both production and test code — production
mocks would be a bigger smell than test mocks.

**Detect** (the explicit list from ADR-0006 §2, plus the common Python
import variants):

- Python: `unittest\.mock\.patch`, `mock\.patch`, `patch\(`,
  `patch\.object\(`, `MagicMock\(`, `Mock\(`,
  `monkeypatch\.setattr\(`, `mocker\.patch`.
- JS / TS: `jest\.mock\(`, `jest\.fn\(\)\.mockImplementation`,
  `vi\.mock\(`, `sinon\.stub\(`, `sinon\.fake\(`.

**Target resolution** (per ADR-0006 §2 "applied to **modules within this
repository**"):

- For `patch("X")` and `patch.object(X, ...)`: extract `X`. If `X` is a
  string literal starting with `tools.`, `packages.`, or `projects.`,
  flag. If `X` is a string literal starting with anything else
  (`requests.`, `anthropic.`, `boto3.`, …), allow — those are external
  modules; ADR-0006 §2 permits network-transport substitution at the
  edge.
- For everything else (no target, identifier target, complex
  expression target): flag conservatively. The author must replace
  with a real adapter (per [`ADR-0006`](../../architecture/decisions/ADR-0006-testing-tiers.md)
  §3) or add an explicit allow marker.

**Inline allow marker**: `<!-- spec-lint: allow mock-in-repo-banned -->`
on the same line. Same structural exemption for the rule's own
source file as `bmad-direct-reference`.

## What changes

### Rules
- `tools/spec_lint/rules/bmad_direct_reference.py` (new) — CrossFileRule.
- `tools/spec_lint/rules/mock_in_repo_banned.py` (new) — CrossFileRule.

### Requirements
- `openspec/specs/_meta/spec-storage.spec.md` extended with:
  - `REQ-SPEC-0002` — `bmad-direct-reference` passes on the live tree.
  - `REQ-SPEC-0003` — `mock-in-repo-banned` passes on the live tree.

### CLI
- `tools/spec_lint/__main__.py:_cmd_validate` adds both rules to the
  CrossFileRule list.

### Tests
- `tools/spec_lint/tests/test_bmad_direct_reference.py` — synthetic
  fixtures for every detection variant + the real-repo smoke probe.
- `tools/spec_lint/tests/test_mock_in_repo_banned.py` — same shape.

## Tasks

- **TASK-0025 (RED)** — failing tests + skeleton rules + CLI not yet
  wired.
- **TASK-0026 (GREEN)** — real implementations + REQ-SPEC-0002 +
  REQ-SPEC-0003 + CLI wiring.

## Out of scope

- TS / JS detection runs but matches nothing today (no `*.ts` / `*.js`
  files in scope dirs). The patterns are in place for PHASE-3 / PHASE-5
  when the first project lands.
- Hand-rolled `class FakeFoo` detection from ADR-0006 §2. Reliable
  detection requires interface-resolution (does this class implement an
  in-repo interface?) which needs richer parsing. Deferred to a future
  CHG.
- `tools/tea/` exemption — `tools/tea/` does not exist today; the
  exemption path is wired into the rule but matches nothing. When TEA
  lands, no rule change needed.
- Property-based / mutation tests for the new rules. The CHG-0009
  benchmark harness has its own cadence; new rules pick up dry-run
  coverage in the next benchmark refresh.
