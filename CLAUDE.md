# CLAUDE.md — session guidance

This repository is governed by
[`openspec/architecture/ARCHITECTURE.md`](openspec/architecture/ARCHITECTURE.md).
Read it before doing anything else. Every constraint below is a restatement of
something defined more precisely in that document or its ADRs.

## Operating principles (verbatim, in priority order)

1. **Single source of truth (SoT).** One canonical home per fact. Cross-document
   consistency is lintable.
2. **Stochastic systems get statistical assertions.** Determinism is never
   manufactured by seeding for systems that are not deterministic in production.
3. **Tests exercise real production code.** No mocks, fakes, or simulations of
   in-repo modules. Boundary adapters are real; only network transport may be
   substituted at the edge.
4. **Red-first.** Every test exists in a failing state in git history before
   the commit that turns it green.
5. **OpenSpec for specification, BMAD + TEA for workflow.** No parallel
   convention is introduced.

A principle without a CI gate is a build failure. See
[`ADR-0008`](openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md).

## How to start any session

1. Read `openspec/architecture/ARCHITECTURE.md` §11 — identify the active phase.
2. Read the active phase file in `openspec/architecture/phases/`.
3. Run the SessionStart resume hook output (printed automatically once
   PHASE-2 lands): it tells you the in-flight task, last commit, and next
   action.
4. Work only inside the active phase scope. Anything outside scope is an ADR
   amendment or a deferred task.

## How to identify any artifact

By stable ID and file path only. Examples:

- `REQ-AUTH-0007 @ openspec/specs/auth/login.spec.md`
- `TASK-0042 @ openspec/changes/CHG-0011/tasks/TASK-0042.md`
- `ADR-0005 @ openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md`

Prose references ("the auth spec", "the login change") are lintable defects
([`ADR-0004` §2](openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md)).

## How to commit

Every commit must carry these trailers
([`ADR-0005` §3](openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md)):

```
Task: TASK-<NNNN>
Requirements: REQ-<X>-<NNNN>[, REQ-<Y>-<NNNN>, ...]
Tests-Status: <none|red|red→green|green|deprecated>
Phase: PHASE-<N>
```

Checkpoint commits (auto-produced by the Stop hook) carry
`Checkpoint: true` and are exempt from a defined subset of gates.

`--no-verify`, `--no-gpg-sign`, and any other hook bypass are forbidden.

## How to add a test

- The test must be red-first: a prior commit must contain the test in a
  failing state.
- The test must annotate `@test-id TEST-<DOMAIN>-<NNNN>` and
  `@covers REQ-<X>-<NNNN>[, ...]`.
- No mock of any in-repo module. Use a real adapter
  ([`ADR-0006`](openspec/architecture/decisions/ADR-0006-testing-tiers.md)).
- For LLM-using code, use the stochastic tier rules
  ([`ADR-0007`](openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md)).

## How to add a requirement

- New requirements live in `openspec/changes/<CHG>/specs/`, applied to
  `openspec/specs/<domain>/<feature>.spec.md` on merge.
- One assertion per REQ. Compound requirements are a defect.
- IDs are immutable. Renames are forbidden; supersession is the only path.
- The new REQ must reference its Story and Epic.

## Forbidden

- Adding a file outside the layout in `ARCHITECTURE.md` §3 without an ADR.
- Hand-editing `openspec/traceability/matrix.yaml`.
- Hand-editing `openspec/specs/INDEX.yaml` after PHASE-1.
- Importing the Anthropic SDK outside `packages/anthropic-client/`.
- Referencing a GAS global outside an adapter implementation.
- Using `jest.mock`, `sinon.stub`, `unittest.mock.patch`, etc. on in-repo
  modules.
- Adding `seed=`, recorded fixtures, or exact-equality assertions in
  `tests/stochastic/`.
- Bypassing any hook.

## When in doubt

Ask. The cost of one clarifying question is much lower than the cost of an
unauthorized architectural change.
