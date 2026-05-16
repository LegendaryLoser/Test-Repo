---
id: CHG-0008
title: spec_lint reliability — mutation tests (CI-gating)
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

# CHG-0008 — spec_lint reliability: mutation tests

## Why

Second of three reliability CHGs. Property tests (CHG-0007) verified that
each rule satisfies its named invariants on `hypothesis`-generated inputs;
they did not surface any defects. That bounds what coarse invariants can
catch.

**Mutation testing is direct fault injection.** Take known-good fixtures,
apply targeted faults that *should* be caught, assert the appropriate
rule catches each. A surviving mutation = a real reliability gap.

Per the prior session direction, **missed mutations gate CI as red errors**.
A surviving mutation blocks PR merge; the fix is to either tighten the
rule or refine the mutation (with rationale).

## What changes

### Mutation framework — `tools/spec_lint/tests/mutations/`

- `_models.py` — `Mutation` dataclass: `id`, `description`, `expected_rule_id`,
  `apply(seed_text) -> mutated_text`, `category` ∈
  `{"must-catch", "known-limitation"}`.
- `runner.py` — `run_mutation(seed, mutation) -> (mutated, findings)` and
  `assert_caught(mutation, findings)` helpers.
- One module per rule with its mutation corpus.

### Mutation corpora

**Comprehensive at the rule's input contract:**

- `req_id_format_mutations.py` — exhaustive at the regex boundary:
  missing prefix; one lowercase letter at each position; each invalid number
  width (1..3, 5..7 digits); non-digit in number; DOMAIN length boundaries
  (0, 1, 12, 13, 20); underscore/symbol in DOMAIN; trailing whitespace on
  heading. All `must-catch`.
- `spec_frontmatter_valid_mutations.py` — exhaustive over the YAML contract:
  drop each of the 8 required keys; substitute each of `status` and `tier`
  with values outside the enum; revision as 0, -1, "1" (string), 1.5; bad
  CHG/PHASE/REQ-ID formats for `introduced`/`phase`/`supersedes`; missing
  each of the 3 required `references.*` sub-keys; references as list/string;
  references.adrs as string. All `must-catch`.
- `compound_mutations.py` — must-catch: N bullets in `{2, 3, 5, 10}`;
  case variants of "Given"; bulleted vs unbulleted. Known-limitation:
  "system must do X **and** Y" prose without G/W/T (no current signal);
  "When… then…" without "Given" prefix.
- `anti_aliasing_mutations.py` — must-catch: identical bodies; bodies
  differing only by trailing punctuation; bodies differing in one word.
  Known-limitation: paraphrase preserving meaning but with low n-gram
  overlap (LLM-augmentation territory).
- `xref_resolves_mutations.py` — must-catch: broken markdown link;
  `REQ-X-NNNN @ path` where path missing; `@ path` where REQ-ID absent in
  file. Known-limitation: REQ-ID-only reference without `@ path` (rule
  doesn't try to resolve bare IDs; that's `xref-active`, a future rule).
- `prose_xref_banned_mutations.py` — must-catch: each denylist pattern in
  a plain sentence; multi-pattern lines. Known-limitation: novel prose
  patterns not yet in the denylist (open-ended; we accept the boundary).

### Driver — `tests/test_mutations.py`

One parametrized test per rule that iterates the rule's must-catch set and
asserts each mutation is caught. Known-limitation mutations are run
separately and **logged but do not fail the test** — they're informational
signals about where deterministic rules end.

### Defect-fix protocol

If a must-catch mutation survives:

1. The driver test fails (PR is blocked).
2. **Fix the rule** in this same CHG. Each fix is its own commit with a
   `Defect-Surfaced-By: MUT-<id>` trailer and `Tests-Status: red→green`.
3. If the surviving mutation turns out to require LLM augmentation rather
   than a deterministic fix, **reclassify it as known-limitation** with
   an explicit ADR amendment or rationale comment — never silently move it.
   That reclassification is itself a substrate change you would merge.

## PHASE-1 scope simplifications (documented for the record)

- History rules (`req-id-immutable`, `req-append-only`) — mutation tests
  for git histories need their own mutation engine on commit graphs.
  Deferred to a later CHG.
- The "novel prose patterns" known-limitation for `prose-xref-banned` is
  inherently open-ended; we mark it and move on.

## Tasks

- [`TASK-0014`](tasks/TASK-0014.md) — type `test-red`: framework + per-rule
  mutation corpora + driver test with NIE stubs. Tests fail.
- [`TASK-0015`](tasks/TASK-0015.md) — type `impl`: implement framework
  runner. Driver tests run; any surviving must-catch mutations are
  surfaced as test failures.
- `TASK-0016+` (created as needed) — fix each surviving mutation with its
  own commit pair.

## Rollout

- Single PR initially; if defects surface in TASK-0015, the PR grows with
  fix commits. If more than 3 defects surface, the proposal splits and
  CHG-0009 covers the residue.
- Self-merge under hybrid policy *only* if no surviving mutations require
  ADR amendment (reclassification of must-catch → known-limitation is
  substrate change → you merge).
