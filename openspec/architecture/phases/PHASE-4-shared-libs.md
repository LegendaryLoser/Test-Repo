---
id: PHASE-4
title: Shared libraries — packages/shared-ts and packages/shared-py
status: pending
entry: PHASE-3 exit criteria all tests-green
---

# PHASE-4 — Shared libraries

## Goal

Deliver shared TypeScript utilities used by Apps Script projects and the
Python ML scaffolding used for non-Apps-Script work. Both follow the same
adapter discipline and test-tier rules as the rest of the repo.

## Entry criteria

- PHASE-3 exit gate passed.

## Scope

1. `packages/shared-ts/`
   - GAS adapter interfaces declared in `packages/shared-ts/gas/` (Sheets,
     Drive, UrlFetch, Properties, Cache, Lock, Script).
   - Real adapter implementations: `gas-production`, `gas-test-rest` (REST
     against test artifacts).
   - Utility modules consumed across Apps Script projects.
2. `packages/shared-py/`
   - ML scaffolding skeleton (training/eval harness, dataset adapters,
     experiment tracking adapter — all real adapters, no mocks).
   - Sandwich layers used by stochastic tests.
3. `openspec/specs/shared-ts/` and `openspec/specs/shared-py/` —
   `REQ-LIBTS-*` and `REQ-LIBPY-*` requirements.
4. Adapter tests across all four tiers per adapter.

## Exit criteria

- All `REQ-LIBTS-*` and `REQ-LIBPY-*` `tests-green`.
- `gas-global-outside-adapter` lint passes against `packages/shared-ts/`
  (only adapter implementations may reference GAS globals).
- Integration tier exercises real Sheets/Drive against a dedicated test
  spreadsheet.

## Out of scope

- Apps Script projects — PHASE-5.

## Exit gate

`phase-exit` verifies REQ-LIBTS-* and REQ-LIBPY-* tests-green.
