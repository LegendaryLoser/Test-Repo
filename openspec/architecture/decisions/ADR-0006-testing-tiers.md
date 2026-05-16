---
id: ADR-0006
title: Testing tiers and the no-mock rule
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0006 — Testing tiers and the no-mock rule

## Context

Principle P3 — tests exercise real production code — is the principle most
often eroded by convenience. This ADR pins the testing contract so that
erosion fails CI rather than going unnoticed.

## Decision

### 1. Four tiers, every project

| Tier         | Runner                | Real systems exercised                                |
|--------------|----------------------|-------------------------------------------------------|
| `unit`       | Node / pytest         | Production modules, in-process real adapters.         |
| `integration`| Node / pytest         | Real Sheets/Drive/HTTP via REST (test artifacts).     |
| `e2e`        | Apps Script runtime   | Deployed GAS code, real Sheets/Drive.                 |
| `stochastic` | Node / pytest         | Real Anthropic API (see [ADR-0007](ADR-0007-llm-stochastic-assertions.md)). |

Every REQ declares its tier in frontmatter. CI runs the tier each REQ declares.

### 2. The no-mock rule

Banned across all tiers:

- `jest.mock`, `jest.fn().mockImplementation`, `vi.mock`, `sinon.stub`,
  `unittest.mock.patch`, `unittest.mock.MagicMock`, `monkeypatch.setattr`
  applied to **modules within this repository**.
- Hand-rolled fakes (`class FakeFoo implements IFoo`) of in-repo interfaces.

Permitted, narrowly:

- Substituting the **HTTP transport** at the network boundary (e.g. a real
  `nock` interceptor that records and replays *real* responses captured from
  the real service). This is permitted only for cost or rate-limit reasons,
  not for correctness reasons, and never for the LLM tier.
- Substituting **clock** and **randomness sources** through real adapters
  (e.g. a deterministic clock implementation that is itself production code,
  used in both prod and test paths). The substitute must be a real component,
  not a mock.

### 3. Adapter pattern

External systems (Sheets, Drive, HTTP, Anthropic, filesystem, clock) are
accessed via interfaces declared in `packages/shared-ts/adapters/` or
`packages/shared-py/adapters/`. Each interface has at minimum two real
implementations: a production one and a test one. The test implementation
is real code (e.g. hits a dedicated test spreadsheet) — it is not a mock.

### 4. Red-first (P4)

- Every test exists in a `tests-red` commit before the `tests-green` commit.
- `tools/trace/validate_commit.py` walks history to enforce.
- Bulk green-starts (e.g. importing a battery of passing tests in one
  commit) require a `Bootstrap: <reason>` trailer and an approving review;
  CI gate `bulk-green-start` flags any commit adding > N green tests
  without the trailer.

### 5. Coverage gate

- **REQ coverage = 100%.** Every non-deprecated REQ has ≥ 1 passing test for
  its declared tier. Every test maps to ≥ 1 REQ. No orphans.
- **Tier coverage.** A REQ marked `tier: e2e` requires a passing E2E test
  (unit tests do not satisfy the REQ).
- **Line and branch coverage** are measured and reported but **not gated**
  (gameable; we gate behavior, not lines).

### 6. Test identifiers

Every test is annotated with `@test-id TEST-<DOMAIN>-<NNNN>` and
`@covers REQ-<X>-<NNNN>[, ...]`. `tools/trace/rebuild.py` parses
annotations to build the matrix.

## Consequences

- Test code is heavier (real adapters cost more than mocks) but tests fail
  for production reasons, not for test-double drift.
- E2E and stochastic tiers have real costs (API quota, latency); gated by
  schedule in [ADR-0008](ADR-0008-ci-gates-and-phase-exits.md).
- Adding a tier (e.g. a `chaos` tier later) is an ADR amendment plus a CI
  matrix entry; no architectural shift.

## Compliance

- Lint rule `mock-in-repo-banned` (PHASE-1) detects banned mock APIs applied
  to in-repo module paths.
- CI gate `req-coverage-100` (PHASE-2) is computed from the matrix.
- CI gate `red-before-green` (PHASE-2) enforces P4.
