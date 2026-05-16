---
id: PHASE-3
title: Anthropic client — single LLM access point with stochastic tier
status: pending
entry: PHASE-2 exit criteria all tests-green
---

# PHASE-3 — Anthropic client

## Goal

Deliver `packages/anthropic-client/` as the single sanctioned LLM access point
([ADR-0007 §6](../decisions/ADR-0007-llm-stochastic-assertions.md)). Establish
the stochastic test tier with real Anthropic API calls, no seeding, no fixtures,
and prompt caching enabled by default.

## Entry criteria

- PHASE-2 exit gate passed.

## Scope

1. `packages/anthropic-client/` — TypeScript and Python clients (mirrored
   surface where APIs differ).
   - Model pinning via centralized config.
   - Prompt caching enabled by default where the model supports it.
   - Cost telemetry exported per-call.
2. Adapter declarations in `packages/shared-ts/adapters/` and
   `packages/shared-py/adapters/` for Anthropic transport substitution at the
   network boundary only (see [ADR-0006 §2](../decisions/ADR-0006-testing-tiers.md)).
3. `packages/anthropic-client/tests/` across all four tiers; stochastic tier
   exercises real API with statistical / schema assertions.
4. `openspec/specs/anthropic-client/` — REQ-LLM-* requirements.
5. CI gate `cache-hit-regression` activated (PR fails if cache hit rate
   regresses below pinned threshold).
6. CI gate `direct-anthropic-import-banned` now has a concrete target.

## Exit criteria

- All `REQ-LLM-*` `tests-green` across declared tiers.
- Stochastic tier cost stays within budget for two consecutive nightly runs.
- `cache-hit-regression` baseline established.
- No file outside `packages/anthropic-client/` imports the Anthropic SDK
  (lint passes).

## Out of scope

- Apps Script projects — PHASE-5.
- Shared TS/Py libraries beyond the adapter declarations — PHASE-4.

## Exit gate

`phase-exit` verifies REQ-LLM-* tests-green + cost-budget + cache baseline.
