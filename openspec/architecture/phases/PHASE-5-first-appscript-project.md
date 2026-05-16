---
id: PHASE-5
title: First Apps Script project — end-to-end green under the full regime
status: pending
entry: PHASE-4 exit criteria all tests-green
---

# PHASE-5 — First Apps Script project

## Goal

Stand up the first concrete Apps Script project under `projects/`, exercising
the entire regime end-to-end: real BMAD workflow, OpenSpec change, red-first
TEA tests, traceability matrix entries, all four test tiers green, deployed
to a `dev` GAS deployment via clasp, E2E tests passing against the live
spreadsheet.

This phase is the **load test** for the architecture. Any pain point
discovered here results in an ADR amendment, not a workaround.

## Entry criteria

- PHASE-4 exit gate passed.
- Product side has produced (in a separate PR chain):
  `openspec/vision.md`, ≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage,
  ≥ 1 Story.

## Scope

1. `projects/<name>/` with full layout per
   [ADR-0001](../decisions/ADR-0001-monorepo-layout.md) and
   [ADR-0003](../decisions/ADR-0003-appscript-runtime.md).
2. `.clasp.json` pointing at a `dev` GAS deployment owned by a CI service
   account.
3. Real adapter wiring against shared-ts.
4. Test suite across all four tiers, each red-first.
5. CI matrix entry for the project; e2e runs nightly + on PRs touching the
   project.
6. Traceability matrix entries for every REQ in the project.

## Exit criteria

- Every REQ in the project is `tests-green` at its declared tier.
- E2E tier produces a passing run against the deployed GAS code at least
  once on the merge commit to main.
- The project's Epic reaches `EPIC.status = done`.
- No principle violation surfaced in PHASE-5 was resolved by a workaround;
  each was either fixed by an ADR amendment or remains an open ADR-amendment
  proposal blocking promotion to `prod`.

## Out of scope

- Production deployment promotion (separate `gate`-type task on the merged
  PR).
- Additional projects (each subsequent project is its own PR chain following
  the same template).

## Exit gate

`phase-exit` verifies project REQs tests-green, Epic done, ≥ 1 nightly E2E
green, no unresolved principle violations.
