---
id: ADR-0008
title: CI gates and phase-exit enforcement
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0008 — CI gates and phase-exit enforcement

## Context

Principles enforce nothing unless mechanically gated. This ADR enumerates every
CI gate, maps it to the principle or ADR it enforces, and pins the schedule
each gate runs on. **A principle without a gate is a gate-coverage failure**
and itself fails the build.

## Decision

### 1. Gate inventory

| Gate                              | Enforces           | Trigger             | Owner          |
|-----------------------------------|--------------------|---------------------|----------------|
| `openspec-validate`               | OpenSpec format    | every PR            | tools/spec_lint|
| `top-level-allowlist`             | ADR-0001           | every PR            | tools/spec_lint|
| `bmad-direct-reference`           | ADR-0002           | every PR            | tools/spec_lint|
| `gas-global-outside-adapter`      | ADR-0003           | every PR            | tools/spec_lint|
| `req-id-format`                   | ADR-0004 §1        | every PR            | tools/spec_lint|
| `req-id-immutable`                | ADR-0004 §1        | every PR            | tools/spec_lint|
| `prose-xref-banned`               | ADR-0004 §2        | every PR            | tools/spec_lint|
| `xref-resolves`                   | ADR-0004 §2        | every PR            | tools/spec_lint|
| `compound-requirement-detector`   | ADR-0004 §3        | every PR            | tools/spec_lint|
| `anti-aliasing`                   | ADR-0004 §4        | every PR            | tools/spec_lint|
| `spec-frontmatter-valid`          | ADR-0004 §5        | every PR            | tools/spec_lint|
| `index-up-to-date`                | ADR-0004 §6        | pre-commit + PR     | tools/spec_lint|
| `req-append-only`                 | ADR-0004 §7        | every PR            | tools/spec_lint|
| `semantic-recall-recall-at-k`     | ADR-0004 §8        | every PR (if used)  | tools/spec_lint|
| `matrix-drift`                    | ADR-0005 §2        | pre-commit + PR     | tools/trace    |
| `commit-trailers-valid`           | ADR-0005 §3        | pre-receive hook    | tools/trace    |
| `red-before-green`                | ADR-0005 §4, P4    | every PR            | tools/trace    |
| `mock-in-repo-banned`             | ADR-0006 §2        | every PR            | tools/spec_lint|
| `req-coverage-100`                | ADR-0006 §5, P3    | every PR            | tools/trace    |
| `tier-coverage`                   | ADR-0006 §5        | every PR            | tools/trace    |
| `direct-anthropic-import-banned`  | ADR-0007 §6        | every PR            | tools/spec_lint|
| `stochastic-tier-bans`            | ADR-0007 §2        | every PR            | tools/spec_lint|
| `cost-budget`                     | ADR-0007 §4        | every PR + nightly  | tools/ci       |
| `cache-hit-regression`            | ADR-0007 §5        | every PR (PHASE-3+) | tools/ci       |
| `phase-exit`                      | this ADR §3        | merge to main       | tools/trace    |
| `gate-coverage`                   | this ADR §2        | every PR            | tools/ci       |

### 2. Gate coverage gate

`gate-coverage` walks every ADR and every principle in
[ARCHITECTURE.md](../ARCHITECTURE.md) §1 and verifies that at least one entry
in the table above references it. A missing reference fails the build.
Adding a new ADR or principle without adding a gate is therefore impossible.

### 3. Phase exits

A phase has exit criteria expressed as REQ-IDs that must be `tests-green`.
The `phase-exit` gate runs on merge to `main` and verifies:

- The current phase's exit REQs are all `tests-green` in the matrix.
- No REQ from a later phase is `tests-green` (we do not allow phases to
  complete out of order).
- The next phase's entry ADR (if any) is `status: accepted`.

If any check fails, the merge is blocked.

### 4. CI workflows

- `.github/workflows/ci.yml` — runs on every PR: gates marked "every PR".
- `.github/workflows/spec-discipline.yml` — runs on every PR; isolates
  spec-lint and trace gates for clarity.
- `.github/workflows/e2e.yml` — runs nightly + manual dispatch; runs the
  `e2e` tier for every project plus `cost-tier: full` stochastic tests.

### 5. Local enforcement (pre-commit)

- `index-up-to-date` and `matrix-drift` run pre-commit and rewrite the
  affected files. Commit proceeds with the rewritten files staged.
- `commit-trailers-valid` runs pre-commit and rejects malformed messages
  before they enter history.

### 6. Bypass discipline

- `--no-verify`, `--no-gpg-sign`, and any other hook-bypass flag are
  forbidden by [CLAUDE.md](../../../CLAUDE.md) at the agent level and by
  branch protection at the repository level for `main`.
- The `Checkpoint: true` trailer (ADR-0005 §7) is the **only** sanctioned
  partial-bypass and applies to a specific subset of gates listed in
  `tools/trace/checkpoint_exemptions.yaml`.

## Consequences

- Every principle has a gate. Every gate has an owner. Every owner is in
  this repo (no external dependency for enforcement).
- Adding a principle without a gate is impossible (`gate-coverage` fails).
- Adding a gate is cheap (table row + implementation + a red test).

## Compliance

- `gate-coverage` is the meta-gate that makes this ADR self-enforcing.
- PHASE-0 commits the workflow YAML stubs (jobs declared, scripts as TODO).
- PHASE-1 and PHASE-2 implement the gates.
