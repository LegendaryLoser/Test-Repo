---
id: CHG-0003
title: spec_lint — req-id-format + spec-frontmatter-valid rules
status: in-progress
date: 2026-05-16
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0004
    - ADR-0008
---

# CHG-0003 — spec_lint: req-id-format + spec-frontmatter-valid

## Why

PHASE-1 entry criteria are met (PHASE-0 closed via PR #2; ADR-0005 amendment
landed via PR #3). PHASE-1 obligates every spec-lint rule from
[`ADR-0008` §1](../../architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md)
to be implemented with red-first tests.

This is the first slice. It introduces the spec_lint package and the two
simplest rules (single-file inspection, no git-history walking,
no cross-file analysis). Subsequent CHGs add the harder rules:

- CHG-0004 — `req-id-immutable` + `req-append-only` (need git-history walking).
- CHG-0005 — `prose-xref-banned` + `xref-resolves` (cross-document scans).
- CHG-0006 — `compound-requirement-detector` + `anti-aliasing` (n-gram similarity).
- CHG-0007 — BMAD v6 install + `.claude/` wrappers.

## What changes

### New package: `tools/spec_lint/`

- `models.py` — `Finding`, `ReqBlock`, `SpecFile` dataclasses.
- `parser.py` — `parse_spec_file(path) -> SpecFile`. Permissive parser:
  identifies any `## REQ-…` heading as an intended REQ block, extracts the
  immediately-following `--- ... ---` YAML frontmatter and the body sections.
  Strict validation is the job of rules, not the parser.
- `rules/base.py` — `Rule` protocol (single-file). Cross-file `Rule` arrives
  in CHG-0006.
- `rules/req_id_format.py` — enforces
  [`ADR-0004` §1](../../architecture/decisions/ADR-0004-spec-storage-discipline.md):
  `^REQ-[A-Z0-9]{1,12}-\d{4}$`.
- `rules/spec_frontmatter_valid.py` — enforces
  [`ADR-0004` §5](../../architecture/decisions/ADR-0004-spec-storage-discipline.md):
  required keys present with valid types; `id` matches the heading; `status`
  and `tier` in their enums; `revision` is a positive int; `introduced` /
  `phase` / `supersedes` use the correct ID formats; `references` has the
  required sub-keys.
- `tests/fixtures/valid/` — positive specs that both rules accept.
- `tests/fixtures/invalid/{req_id,frontmatter}/` — negative specs each
  designed to trip exactly one class of violation.
- `tests/{test_parser,test_req_id_format,test_spec_frontmatter_valid}.py` —
  red in TASK-0004, green in TASK-0005.

### Substrate-adjacent fix: `spec-lint` → `spec_lint` in path references

[`ARCHITECTURE.md`](../../architecture/ARCHITECTURE.md) §3,
[`ADR-0004`](../../architecture/decisions/ADR-0004-spec-storage-discipline.md),
[`ADR-0008`](../../architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md),
all PHASE files, and the CI workflow YAML referenced the tool by path as
`tools/spec-lint/` (hyphen). Python packages cannot contain hyphens in their
importable name, so the tests `from tools.spec_lint.parser import …` require
the directory to be `tools/spec_lint/`. All **path-form** references are
renamed; **prose/identifier** references (job names, "spec-lint rule X",
gate IDs containing hyphens like `req-id-format`) are unchanged.

Treated as a typo-class fix rather than a substantive substrate change;
called out here for the record.

### Tooling: `pyproject.toml` and `tools/__init__.py`

- `pyproject.toml` gains `pythonpath = ["."]` under `[tool.pytest.ini_options]`
  so tests can import `from tools.spec_lint.<module>`.
- `tools/__init__.py` (empty) makes `tools` an importable package, consistent
  with the existing `tools/ci/__init__.py`.

## Out of scope

- The remaining ADR-0008 spec-lint rules (split across CHG-0004 / 0005 / 0006).
- A CLI entry point — deferred until enough rules exist to justify one.
- Wiring lint into CI workflows — workflows still PHASE-0 placeholders;
  real CI invocation lands in PHASE-2 (`tools/trace`).
- `openspec/specs/_meta/spec-storage.spec.md` (REQ-SPEC-* requirements that
  formally bind these rules) — added in CHG-0007 once all PHASE-1 rules and
  BMAD are in place, since REQ allocation should follow rule completeness.

## Tasks

- [`TASK-0004`](tasks/TASK-0004.md) — type `test-red`: scaffold package +
  stubs that raise `NotImplementedError`, fixtures, real test bodies.
  Tests fail because stubs raise NIE.
- [`TASK-0005`](tasks/TASK-0005.md) — type `impl`: implement parser and two
  rules. Tests pass.

## Rollout

- Single PR. Intra-phase, no ADR amendment, no substrate behavioral change.
  Under the hybrid merge policy I will self-merge after pushing.
- Per the new push invariant (ADR-0005 §6 amendment 0001, merged in PR #3),
  every commit is pushed immediately after creation.
