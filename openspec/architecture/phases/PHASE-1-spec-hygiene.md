---
id: PHASE-1
title: Spec hygiene — tools/spec_lint green, BMAD installed
status: pending
entry: PHASE-0 exit criteria all tests-green
---

# PHASE-1 — Spec hygiene

## Goal

Make every rule in [ADR-0004](../decisions/ADR-0004-spec-storage-discipline.md),
the lint-style rules in [ADR-0001](../decisions/ADR-0001-monorepo-layout.md),
[ADR-0002](../decisions/ADR-0002-bmad-integration.md),
[ADR-0003](../decisions/ADR-0003-appscript-runtime.md),
[ADR-0006](../decisions/ADR-0006-testing-tiers.md), and
[ADR-0007](../decisions/ADR-0007-llm-stochastic-assertions.md)
mechanically enforced.

Install BMAD v6 so PHASE-2+ can invoke its workflows.

## Entry criteria

- PHASE-0 exit gate passed.

## Scope

1. `tools/spec_lint/` — implementation of every gate owned by `tools/spec_lint`
   in [ADR-0008 §1](../decisions/ADR-0008-ci-gates-and-phase-exits.md).
2. `tools/spec_lint/tests/` — red-first tests for each rule.
3. `bmad/` installation per [ADR-0002](../decisions/ADR-0002-bmad-integration.md),
   pinned in `bmad/config.yaml`.
4. `.claude/agents/` and `.claude/commands/` wrappers for BMAD personas
   (PM, Architect, SM, Dev, PO, TEA) and core commands.
5. `tools/tea/` skeleton — invokes TEA workflows; integration with CI deferred
   to PHASE-2.
6. Spec hygiene REQs created: `openspec/specs/_meta/spec-storage.spec.md`
   containing `REQ-SPEC-*` requirements that the lint rules cover.

## Exit criteria

- Every gate in [ADR-0008 §1](../decisions/ADR-0008-ci-gates-and-phase-exits.md)
  owned by `tools/spec_lint` is implemented and has ≥ 1 passing test that
  was red in a prior commit.
- `REQ-SPEC-*` requirements covering each lint rule are `tests-green`.
- `bmad/config.yaml` pins v6 minor version; `bmad-direct-reference` gate
  passes against the repo.
- All BMAD wrapper files in `.claude/agents/` and `.claude/commands/` resolve
  their `Load:` paths.

## Out of scope

- Traceability runtime (`tools/trace/`) implementation — PHASE-2.
- Anthropic client — PHASE-3.
- Any product specs.

## Exit gate

`phase-exit` verifies the above + ADR-0001..8 still `accepted`.
