---
id: CHG-0030
title: Test annotation discipline — meta-test + backfill + REQ-SPEC for every rule
status: in-progress
date: 2026-05-17
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0004
    - ADR-0005
    - ADR-0006
    - ADR-0008
---

# CHG-0030 — test annotation discipline (meta-test + backfill + REQ coverage)

## Why

The audit (see chat) found three compounding discipline gaps:

1. **5 tests in `test_mutations.py` have no `@test-id` annotation.**
2. **84 tests across the suite have no `@covers` annotation at all.**
3. **3 tests use legacy `@covers (rule: <name>)` form** instead of the
   required `@covers REQ-<X>-<NNNN>` form per
   [`CLAUDE.md`](../../../CLAUDE.md) "How to add a test".

Total: 92 of 117 test functions (79%) violate the annotation discipline.

The audit also found that **8 lint rules have no covering `REQ-SPEC`**
(req-id-format, spec-frontmatter-valid, compound-requirement-detector,
prose-xref-banned, xref-resolves, anti-aliasing, req-id-immutable,
req-append-only). Plus the spec_lint infrastructure (parser, git
history, benchmark) and the new annotation discipline itself have no
REQ. Without these REQs, `@covers` cannot be written compliantly —
there is nothing to point to.

CHG-0030 closes both gaps in one bundled CHG because they are linked:
the annotation discipline cannot be enforced until the REQs exist; the
REQs without test coverage would be empty by construction.

This is the **first CHG in the post-audit roadmap**. It precedes CI
wiring (CHG-0013) because the meta-test it ships becomes part of CI's
gate inventory the moment CI is wired.

## What changes

### New REQs (`openspec/specs/_meta/spec-storage.spec.md` extended)

- **REQ-SPEC-0004** — `req-id-format` rule correctly classifies REQ-ID strings.
- **REQ-SPEC-0005** — `spec-frontmatter-valid` rule enforces ADR-0004 §5.
- **REQ-SPEC-0006** — `compound-requirement-detector` rule enforces ADR-0004 §3.
- **REQ-SPEC-0007** — `prose-xref-banned` rule enforces ADR-0004 §2 prose ban.
- **REQ-SPEC-0008** — `xref-resolves` rule resolves cross-references per ADR-0004 §2.
- **REQ-SPEC-0009** — `anti-aliasing` rule enforces ADR-0004 §4.
- **REQ-SPEC-0010** — `req-id-immutable` rule enforces ADR-0004 §1 (history-based).
- **REQ-SPEC-0011** — `req-append-only` rule enforces ADR-0004 §7 (history-based).
- **REQ-SPEC-0012** — spec_lint infrastructure (parser, git history loader,
  benchmark harness) is correct.
- **REQ-SPEC-0013** — every Python test function in `tools/` carries both
  `@test-id TEST-<DOMAIN>-<NNNN>` and `@covers REQ-<X>-<NNNN>` annotations
  (the meta-discipline).

### Meta-test

- **`tools/ci/tests/test_annotation_discipline.py`** — single test that
  AST-walks every `test_*.py` under `tools/`, enumerates every
  `def test_*` function, and asserts each docstring contains both
  `@test-id TEST-...` and `@covers REQ-<X>-<NNNN>` (REQ-form only).
  Covers REQ-SPEC-0013.

### Annotation backfills

- **5 tests in `test_mutations.py`** get new `@test-id` allocations:
  TEST-SPEC-MUT-FRONTMATTER-NNN, MUT-COMPOUND-NNN, MUT-ALIAS-NNN,
  MUT-PROSE-NNN, MUT-XREF-NNN (consistent with the existing
  TEST-SPEC-MUT-REQID-NNN convention).
- **84 tests** get `@covers REQ-SPEC-NNNN` added per the file-to-REQ
  mapping in §"Mapping" below.
- **3 tests** convert from `@covers (rule: <name>)` to `@covers
  REQ-SPEC-NNNN`.

### Mapping (file → REQ)

| Test file | Covers |
|---|---|
| `ci/tests/test_phase0.py` | REQ-ARCH-0001..0008 (per-test, already compliant) |
| `spec_lint/tests/test_req_id_format.py` + properties | REQ-SPEC-0004 |
| `spec_lint/tests/test_spec_frontmatter_valid.py` + properties | REQ-SPEC-0005 |
| `spec_lint/tests/test_compound_requirement_detector.py` + properties | REQ-SPEC-0006 |
| `spec_lint/tests/test_prose_xref_banned.py` | REQ-SPEC-0007 |
| `spec_lint/tests/test_xref_resolves.py` + properties | REQ-SPEC-0008 |
| `spec_lint/tests/test_anti_aliasing.py` + properties | REQ-SPEC-0009 |
| `spec_lint/tests/test_req_id_immutable.py` | REQ-SPEC-0010 |
| `spec_lint/tests/test_req_append_only.py` | REQ-SPEC-0011 |
| `spec_lint/tests/test_parser.py`, `test_git_history.py`, `test_benchmark.py` + parser properties | REQ-SPEC-0012 |
| `spec_lint/tests/test_mutations.py` | per-test: REQ-SPEC-0004/0005/0006/0007/0008/0009 |
| `spec_lint/tests/test_openspec_validate.py` | REQ-SPEC-0001 (already compliant) |
| `spec_lint/tests/test_top_level_allowlist.py` | REQ-ARCH-0001 (already compliant) |
| `spec_lint/tests/test_bmad_direct_reference.py` | REQ-SPEC-0002 (already compliant) |
| `spec_lint/tests/test_mock_in_repo_banned.py` | REQ-SPEC-0003 (already compliant) |
| `ci/tests/test_annotation_discipline.py` (new) | REQ-SPEC-0013 |

## Tasks

- **TASK-0027 (RED)** — add meta-test only. 92 violations expected.
- **TASK-0028 (GREEN)** — add 10 REQs + backfill all 92 annotations.
  Meta-test passes.

## Out of scope

- `real_repo_passes` tests added in CHG-0011 (S5 finding — they never
  spent time in RED state, so they technically violate P4). Deferred to
  the queued **CHG-0026**; tracked but not fixed here.
- CI wiring (CHG-0013) — the meta-test ships as a unit test today;
  becomes a real CI gate when CHG-0013 wires the workflow.
- REQ-existence cross-check — the meta-test only enforces
  *annotation format*, not whether the referenced REQ-ID actually
  exists in any spec file. That cross-check is `gate-coverage`
  (PHASE-2).

## Risks acknowledged

- **Scope:** 87 file edits in GREEN commit. Auditable as a coherent
  pass (one `@covers` per test, one TEST-SPEC ID per missing one) but
  not a small diff.
- **REQ granularity:** REQ-SPEC-0012 bundles three modules (parser,
  history, benchmark). If they need separate accountability later, split
  via supersession (ADR-0004 §1 — IDs are immutable, never renamed).
