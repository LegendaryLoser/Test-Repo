---
id: CHG-0007
title: spec_lint reliability — property-based tests via hypothesis
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

# CHG-0007 — spec_lint reliability: property-based tests

## Why

Eight spec_lint rules now exist (CHG-0003 through CHG-0006). All are tested
against ~30 hand-authored fixtures. That demonstrates *intent*; it does not
measure *reliability* on inputs we did not author.

Per the session decision "measure first, decide later": before adding any
further machinery (BMAD install, remaining lint rules, possible LLM
augmentation), this CHG instruments the existing rules with **property-based
tests** that exercise invariants on `hypothesis`-generated inputs. The
properties are universal claims about the rules — claims that, if false, mean
the rule is wrong in a way no individual fixture exposed.

This is the first of three reliability CHGs:

- CHG-0007 (this one): property-based tests.
- CHG-0008: mutation tests (valid fixtures + targeted faults → must-catch).
- CHG-0009: real-corpus dry-run + uncertain-zone logging + benchmark
  harness. After CHG-0009 produces numbers, we decide whether LLM
  augmentation is worth the substrate cost.

## What changes

### Dependency

`pyproject.toml` gains `hypothesis>=6.100` in `[project.optional-dependencies].dev`.

### Property tests

One file per rule (or rule family). Each declares invariants and uses
`hypothesis` strategies to generate structured-random inputs.

- `tests/properties/test_parser_properties.py`:
  - Round-trip: text containing only valid REQ blocks → `parse_spec_file_text`
    → re-extract heading IDs → equals the original heading IDs in order.
  - Frontmatter parse is deterministic for the same input.
- `tests/properties/test_req_id_format_properties.py`:
  - Any heading matching the strict regex `^REQ-[A-Z0-9]{1,12}-\d{4}$`
    produces no findings.
  - Any heading that fails a *specific* sub-constraint (lowercase, long
    domain, short number, non-digit in number) produces ≥1 finding citing
    that heading.
- `tests/properties/test_spec_frontmatter_valid_properties.py`:
  - Dropping any single required key from a valid frontmatter produces a
    finding naming that key.
  - Substituting any required-enum field with a value outside its enum
    produces a finding.
- `tests/properties/test_compound_properties.py`:
  - For N in 0..10, a REQ with N Given/When/Then bullets produces a finding
    iff N > 1; the finding message names N.
- `tests/properties/test_anti_aliasing_properties.py`:
  - Byte-identical bodies → Jaccard = 1.0; flagged for any threshold ≤ 1.0.
  - Bodies sharing no n-grams → Jaccard = 0.0; never flagged.
  - Jaccard is symmetric: `jaccard(a, b) == jaccard(b, a)`.
  - `check_corpus` never pairs a REQ with itself.
- `tests/properties/test_xref_properties.py`:
  - Markdown links that resolve when written to disk → no findings.
  - Markdown links to non-existent paths → ≥1 finding.

### Property test directory layout

A new `tests/properties/` subdirectory under `tools/spec_lint/tests/`
isolates property tests so they can be selected or skipped by `pytest -k`
when iterating on a single rule.

## PHASE-1 simplifications (proposal documents)

- `hypothesis.settings(max_examples=50)` per property to keep CI fast.
  Larger sample sizes are CHG-0009 benchmark territory, not unit-CI.
- Properties test the **rules as documented**. If a property surfaces a
  genuine gap (e.g., "all-uppercase GIVEN slips through compound"), the gap
  is fixed in this CHG's green commit (red-first preserved for the fix
  commit pair: the property fails → fix the rule → property passes).
- No property tests for `req-id-immutable` or `req-append-only` (history
  rules) in this CHG — those need a hypothesis strategy for *git histories*
  which is its own design. Deferred to a follow-up.

## Out of scope

- Mutation tests (CHG-0008).
- Real-corpus dry-run, uncertain-zone logging, benchmark harness (CHG-0009).
- Any LLM consideration.

## Tasks

- [`TASK-0012`](tasks/TASK-0012.md) — type `test-red`: scaffold the property
  tests with `pytest.fail` stubs and dependency. Tests fail.
- [`TASK-0013`](tasks/TASK-0013.md) — type `impl`: replace stubs with real
  hypothesis property bodies. Tests pass. Any rule defects surfaced are
  fixed in this commit (or a subsequent commit if non-trivial).

## Rollout

- Single PR, intra-phase. Self-merge under hybrid policy.
- Push immediately after each commit (ADR-0005 §6 amendment 0001).
