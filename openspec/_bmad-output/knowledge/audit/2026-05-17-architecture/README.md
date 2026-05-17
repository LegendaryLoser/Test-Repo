# Architecture Audit — 2026-05-17

**Target:** the 15-document architecture artifact under
`openspec/architecture/` (ARCHITECTURE.md + 8 ADRs + 6 PHASE files).

**Status:** STAGING (per
[`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7
and [`STAGING.md`](../../../STAGING.md)). Non-authoritative. Not referenced
by the matrix, INDEX, or any spec.

## What this directory contains

| File | Purpose |
|---|---|
| `README.md` | This file. Session metadata + method. |
| `consolidated.md` | Main deliverable: thematic clustering of all findings, convergence analysis, proposed CHG sequence. |
| `findings-index.md` | Flat one-line-per-finding index across all 12 streams (provenance ledger). |

## Why this audit exists

Triggered by the prior session's roadmap (STATUS.md "Next session: start here"
and STATUS.md NEW-3, audit-findings ledger). The architecture artifact was
declared "frozen" but had absorbed 19 prior audit findings without all of
them being closed (12 still open). The user requested a thorough,
maximally-rigorous, multi-perspective re-review before resuming any queued
implementation roadmap (CHG-0014b, CHG-0015, etc.).

## Method

12 review streams against the same 15-document corpus. Maximum variance
applied across four axes:

1. **Model diversity** — opus, sonnet, haiku (proxy for temperature variation,
   which the Claude Code Agent tool does not expose directly).
2. **Methodology diversity** — adversarial-general, edge-case-hunter,
   implementation-readiness, editorial-structure, editorial-prose,
   pre-mortem, party-mode roundtable, inheritor framing.
3. **Context diversity** — one in-context pass (full conversation +
   STATUS.md awareness); 11 isolated sub-agent passes (no prior context).
4. **Persona diversity** — within the party-mode pass, 6 BMAD personas
   reviewed from their professional angle.

## Streams

| ID prefix | Method | Model | Context | Findings |
|---|---|---|---|---|
| `ARCH-` | adversarial-general | opus | in-context | 31 |
| `IND-` | adversarial-general | opus | isolated | 27 |
| `ADVO-` | adversarial-general | opus | isolated | 24 |
| `ADVS-` | adversarial-general | sonnet | isolated | 19 |
| `ADVH-` | adversarial-general | haiku | isolated | 15 |
| `INHER-` | inheritor framing (custom) | opus | isolated | 22 |
| `EDGE-` | edge-case-hunter | opus | isolated | 44 |
| `READY-` | check-implementation-readiness | opus | isolated | 19 |
| `STRUCT-` | editorial-review-structure | opus | isolated | 15 |
| `PROSE-` | editorial-review-prose | sonnet | isolated | 14 |
| `PREM-` | advanced-elicitation (pre-mortem) | opus | isolated | 18 |
| `PARTY-` | party-mode (6 personas) | opus | isolated | 22 |
| **Total raw** | | | | **270** |

Plus 19 pre-existing findings in
`openspec/STATUS.md` (audit-findings ledger, prefixes `C`/`S`/`P`/`NEW`).

## Caveats

- Raw stream outputs are not persisted as separate files (the agent
  task-transcript outputs in `/tmp/` are the authoritative raw record;
  this audit captures their content via the consolidated thematic
  clustering and the per-finding index).
- The audit was performed against the in-tree architecture as of the
  most recent commit on `claude/bmad-architecture-review-sV42w`. STATUS.md
  open question #5 about BMAD review integration into the CHG workflow
  is the open governance question that determines whether this audit
  itself should have followed a formal CHG-envelope shape.
- "Consolidated" means thematically deduplicated. The thematic
  clustering is the consolidator's judgment (this session) and is itself
  reviewable — the per-finding index preserves the raw provenance so a
  later reviewer can re-cluster.
