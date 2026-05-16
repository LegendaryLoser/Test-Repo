---
id: ADR-0007
title: LLM tier — stochastic assertions, no seeding, no recorded fixtures
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0007 — LLM tier: stochastic assertions, no seeding, no recorded fixtures

## Context

Principle P2 — stochastic systems get statistical assertions — exists because
production LLM behavior is stochastic and seeding is not available for the
deployed Claude API. Tests that assert exact string equality against an LLM
response are false comfort: they pass on the recorded fixture and tell us
nothing about production.

## Decision

### 1. Stochastic tier targets

The `tests/stochastic/` tier exercises code that depends on
`packages/anthropic-client/` (the sole LLM access point). Other code paths
are exercised by `unit` / `integration` / `e2e` tiers as usual.

### 2. Forbidden in `tests/stochastic/`

- `seed=` arguments to Anthropic API calls or downstream randomness.
- Recorded response fixtures replayed in lieu of real API calls.
- Exact-equality assertions against generated text.
- Snapshot tests against generated text.
- Retry-until-pass loops.

### 3. Permitted assertion forms

- **Schema invariants.** The response conforms to a JSON Schema / Pydantic
  model / Zod schema. Tool-use arguments validate against the tool's input
  schema.
- **Structural invariants.** Number of items returned is in `[lo, hi]`;
  required fields present; references resolve.
- **Property-based invariants.** Idempotence under harmless perturbations of
  input; monotonicity; commutativity where claimed.
- **Distributional assertions over N runs.** Sample size declared; assertion
  is a confidence interval, Kolmogorov–Smirnov test, or similar. Sample size
  and threshold are pinned per test.
- **Sandwich-layer assertions.** A deterministic post-processing layer
  (parser, normalizer, validator) is wrapped around the LLM call. The
  deterministic layer is unit-tested; the stochastic test asserts the
  LLM-plus-sandwich composition meets contract.

### 4. Cost containment

- Stochastic tests carry a `@cost-budget tokens=<N>` annotation. CI
  aggregates per-PR and per-nightly budgets; exceeding the budget fails the
  build.
- Stochastic tests run on a schedule defined in
  [ADR-0008](ADR-0008-ci-gates-and-phase-exits.md): on every PR for tests
  marked `@cost-tier cheap`, nightly for `@cost-tier full`.

### 5. Prompt-caching discipline

`packages/anthropic-client/` defaults to prompt caching where supported by
the model. Cache hit rate is reported per CI run; a regression below a pinned
threshold fails the build (separate from correctness gates).

### 6. Single LLM access point

No code outside `packages/anthropic-client/` may import the Anthropic SDK
directly. Lint rule `direct-anthropic-import-banned` (PHASE-1) enforces.
Rationale: cost telemetry, caching, and model-version pinning are centralized.

## Consequences

- LLM tests are slower and cost real tokens. Accepted; this is the only honest
  way to test stochastic behavior.
- Adding a new LLM-using feature requires designing a sandwich layer or
  property the test can assert on. This is a feature, not a bug — it forces
  contract clarity at design time.
- Model upgrades (Sonnet 4.6 → 4.7, etc.) become a single PR against
  `packages/anthropic-client/` plus a re-run of stochastic tests.

## Compliance

- Lint rule `direct-anthropic-import-banned` (PHASE-1).
- Lint rule `stochastic-tier-bans` (PHASE-1): scans `tests/stochastic/` for
  forbidden patterns in §2.
- CI gate `cost-budget` (PHASE-2).
- CI gate `cache-hit-regression` (PHASE-3, when `packages/anthropic-client/`
  exists).
