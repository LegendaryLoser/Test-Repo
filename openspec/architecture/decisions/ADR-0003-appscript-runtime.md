---
id: ADR-0003
title: Apps Script runtime — clasp + TypeScript with mandatory real-runtime E2E
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0003 — Apps Script runtime: clasp + TypeScript with mandatory real-runtime E2E

## Context

Google Apps Script (GAS) projects must be authored, tested, and deployed under
a regime that satisfies operating principles P1–P5
([ARCHITECTURE.md](../ARCHITECTURE.md) §1), especially:

- P3 — tests exercise real production code (no mocks of in-repo modules);
- P2 — stochastic systems get statistical assertions;
- P4 — tests are red before they are green.

GAS executes in Google's V8-based runtime with platform-specific globals
(`SpreadsheetApp`, `DriveApp`, `UrlFetchApp`, etc.). Authoring directly in the
Apps Script editor forfeits unit-testability and version control. Authoring in
JavaScript via `clasp` regains version control but loses type safety. Authoring
in TypeScript via `clasp` is the only path that gives both.

A unit-test tier on Node alone cannot satisfy P3 for the platform-specific
surface, because Node ≠ GAS V8. Therefore an integration tier and an E2E tier
that execute *in the deployed Apps Script runtime* are non-negotiable.

## Decision

1. **Author in TypeScript**, transpiled and pushed via `clasp`. Source under
   `projects/<project>/src/`.
2. **Narrow adapter pattern at the GAS boundary.** Every direct call to a GAS
   global goes through an adapter interface declared in
   `packages/shared-ts/gas/`. Production builds inject the real GAS adapter;
   Node unit tests inject a *different real* adapter (e.g. a Sheets adapter
   that hits a dedicated test spreadsheet via the Sheets REST API). No mock
   adapter is permitted; substitution is real-for-real, not real-for-fake.
3. **Four test tiers per project**, all required:
   - `tests/unit/` — runs on Node; imports production TypeScript modules
     unchanged; uses non-GAS real adapters.
   - `tests/integration/` — runs on Node; uses real Sheets/Drive REST adapters
     against dedicated test artifacts owned by a CI service account.
   - `tests/e2e/` — runs *in the deployed GAS runtime*: `clasp push` to a test
     deployment, invoke via the Apps Script Execution API, assert on the real
     spreadsheet state.
   - `tests/stochastic/` — exercises real Anthropic API calls; assertions are
     statistical or schema-invariant (see
     [ADR-0007](ADR-0007-llm-stochastic-assertions.md)).
4. **Deployment topology per project**:
   - `dev` deployment — used by `tests/e2e/` in CI.
   - `prod` deployment — promoted from `dev` only on a merged `gate`-type task.
5. **No GAS global may be referenced outside an adapter implementation.**
   Lint rule in PHASE-1 enforces.

## Consequences

- Unit tests run fast on Node against real production modules.
- Integration tests are slower but catch real Sheets/Drive semantics.
- E2E tests are slowest; gated to nightly + on-demand
  ([ADR-0008](ADR-0008-ci-gates-and-phase-exits.md)).
- Authoring in TypeScript gives type checking as a free pre-test gate.
- Adapter discipline keeps the deployable surface small and the test surface
  honest.

## Compliance

- Lint rule `gas-global-outside-adapter` (PHASE-1).
- CI matrix runs all four tiers per project; e2e on the schedule defined in
  [ADR-0008](ADR-0008-ci-gates-and-phase-exits.md).
- A project cannot reach `EPIC.status = done` without ≥1 passing E2E test that
  covers each of the Epic's REQs marked `tier: e2e`.
