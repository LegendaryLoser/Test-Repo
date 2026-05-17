# Findings Provenance Index — 2026-05-17 Architecture Audit

Cross-reference between the 270 raw findings (across 12 streams) and the
26 themes consolidated in [consolidated.md](consolidated.md).

The raw finding *bodies* are not duplicated here — they exist in the
session transcripts that produced them. This index preserves the *mapping*:
which stream surfaced which finding, and which theme it clusters under.

For each theme, the constituent finding IDs are listed. For each stream,
the per-stream tally is recorded.

---

## Per-stream tally

| Stream | Prefix | Model | Method | C/SER/PROC or BLK/SHOULD/NICE | Total |
|---|---|---|---|---|---|
| In-context | `ARCH-` | opus | adversarial-general | 8 / 14 / 9 | 31 |
| First isolated | `IND-` | opus | adversarial-general | 8 / 12 / 7 | 27 |
| Second isolated | `ADVO-` | opus | adversarial-general | 6 / 10 / 8 | 24 |
| Sonnet isolated | `ADVS-` | sonnet | adversarial-general | 5 / 9 / 5 | 19 |
| Haiku isolated | `ADVH-` | haiku | adversarial-general | 6 / 6 / 3 | 15 |
| Inheritor framing | `INHER-` | opus | scenario | (mixed) | 22 |
| Edge-case hunter | `EDGE-` | opus | branch-walk | (mixed CRIT/SER/PROC) | 44 |
| Implementation readiness | `READY-` | opus | completeness | 6 BLK / 7 SHOULD / 6 NICE | 19 |
| Editorial structure | `STRUCT-` | opus | restructure | (mixed) | 15 |
| Editorial prose | `PROSE-` | sonnet | modal/quantifier | 3 / 7 / 4 | 14 |
| Pre-mortem | `PREM-` | opus | failure-narrative | 4 CRIT, rest SER | 18 |
| Party-mode | `PARTY-` | opus | 6-persona roundtable | 3 / 14 / 5 | 22 |
| **Total** | | | | | **270** |

Plus 19 pre-existing in STATUS.md (`C1-C5`, `S1-S5`, `P1-P6`, `NEW-1..3`).

---

## Per-theme constituent finding IDs

### THEME-A — BMAD strategy / wrapper retirement / path drift

Streams: 11/12 · Severity: CRITICAL · Convergence: Tier A (certain)

Findings: ARCH-CRIT-01, ARCH-CRIT-02, ARCH-CRIT-03, IND-CRIT-01,
IND-CRIT-02, IND-CRIT-03, IND-CRIT-04, IND-PROC-05, ADVO-CRIT-01,
ADVO-CRIT-02, ADVO-PROC-03, ADVS-CRIT-04, ADVS-PROC-01, ADVH-CRIT-02,
ADVH-CRIT-03, EDGE-23, EDGE-24, EDGE-25, READY-01, READY-15, STRUCT-02,
PARTY-DOC-05, INHER-09, PROSE-07, PROSE-13.

Pre-existing: STATUS.md C3 (PHASE-1 incomplete) and S3 (bmad-direct-ref
bypassable) partially.

### THEME-B — Trailer schema fragmentation

Streams: 10/12 · Severity: CRITICAL · Convergence: Tier A

Findings: ARCH-CRIT-04, ARCH-SER-04, ARCH-SER-06, ARCH-SER-08,
ADVO-SER-02, ADVO-SER-04, ADVS-CRIT-02, ADVH-SER-08, EDGE-08, EDGE-09,
EDGE-44, READY-09, READY-10, READY-11, INHER-12, INHER-14, INHER-22,
PROSE-03.

### THEME-C — `gate-coverage` syntactic-not-semantic + uncovered principles

Streams: 9/12 · Severity: CRITICAL · Convergence: Tier A

Findings: ARCH-SER-03, IND-CRIT-06, IND-CRIT-07, IND-SER-01,
ADVO-CRIT-04, ADVS-SERI-01, ADVH-PROC-09, EDGE-41, INHER-02, INHER-11,
PREM-01, STRUCT-12, READY-02.

Pre-existing: STATUS.md C5 (P1 + P5 uncovered).

### THEME-D — Hook implementation correctness

Streams: 10/12 · Severity: SERIOUS (with CRITICAL specific cases) · Tier A

Findings: ARCH-SER-13, EDGE-04, EDGE-05, EDGE-13, EDGE-14, EDGE-15,
EDGE-17, EDGE-27, EDGE-28, EDGE-32, EDGE-33, EDGE-34, INHER-13,
PROSE-09, ADVH-SER-04, READY-03, READY-06, READY-16, PARTY-DOC-01,
PREM-02.

### THEME-E — Red-before-green + checkpoint interaction

Streams: 9/12 · Severity: CRITICAL · Tier A

Findings: ARCH-SER-06, ARCH-SER-08, IND-SER-05, IND-SER-09, ADVO-SER-07,
ADVS-SERI-03, ADVH-SER-08, EDGE-06, EDGE-07, EDGE-08, READY-11,
INHER-07, PREM-03, PREM-12, PARTY-SER-03, PARTY-SER-04, PROSE-12.

### THEME-F — Push invariant unenforceable

Streams: 8/12 · Severity: CRITICAL · Tier A

Findings: ARCH-SER-02, ARCH-SER-13, IND-CRIT-08, ADVO-SER-06,
ADVH-SER-04, EDGE-16, EDGE-17, EDGE-18, EDGE-42, INHER-08, PREM-02,
PARTY-CRIT-01.

### THEME-G — REQ-ARCH-* format + canonical home

Streams: 8/12 · Severity: SERIOUS · Tier A

Findings: ARCH-SER-01, ARCH-PROC-09, IND-PROC-02, ADVS-SERI-02,
ADVH-SER-01, STRUCT-07, INHER-10.

Pre-existing: STATUS.md C2.

### THEME-H — Missing-artifact-type ADRs

Streams: 8/12 · Severity: SERIOUS · Tier A

Findings: ARCH-PROC-01, ARCH-PROC-02, ARCH-PROC-03, ARCH-PROC-04,
ARCH-PROC-06, ARCH-PROC-07, INHER-01, INHER-15, INHER-17, INHER-19,
INHER-20, INHER-21, READY-04, READY-07, READY-19, ADVO-PROC-02,
ADVH-PROC-13 (related), ADVS-PROC-04, PARTY-UX-01.

### THEME-I — Test tier semantics + real-vs-fake adapter

Streams: 9/12 · Severity: SERIOUS · Tier A

Findings: ARCH-SER-05, ARCH-SER-10, IND-SER-04, IND-SER-12, ADVO-SER-03,
ADVH-SER-11, ADVH-CRIT-12, PARTY-SER-01, PARTY-SER-02, PREM-05,
PROSE-05, PROSE-06, PROSE-14, ADVS-SERI-04, ADVS-SERI-07, ADVS-PROC-05,
EDGE-31, EDGE-43, INHER-16.

Pre-existing: STATUS.md S1 (mock FP).

### THEME-J — Stochastic tier statistical + cost-budget proxy

Streams: 7/12 · Severity: SERIOUS · Tier A

Findings: IND-SER-03, IND-SER-10, IND-SER-11, ADVO-SER-04, EDGE-29,
EDGE-30, READY-14, PARTY-REQ-04, PREM-04, PREM-15, ADVS-PROC-04,
INHER-19.

### THEME-K — Phase ordering: circular bootstrap + exit-gate self-reference

Streams: 9/12 · Severity: CRITICAL · Tier A

Findings: ARCH-CRIT-07, ARCH-PROC-05, ARCH-PROC-08, IND-SER-07,
ADVO-CRIT-05, ADVO-SER-09, ADVS-CRIT-01, ADVS-CRIT-03, ADVH-PROC-09,
EDGE-20, EDGE-22, EDGE-36, EDGE-40, READY-05, INHER-06, PARTY-CRIT-02,
PARTY-PROC-03, PREM-16.

### THEME-L — CLAUDE.md ↔ ARCHITECTURE.md verbatim duplication

Streams: 5/12 · Severity: CRITICAL · Tier B

Findings: ARCH-CRIT-08, IND-SER-08, EDGE-35, STRUCT-09, INHER-04.

### THEME-M — Amendment-log discipline inconsistencies

Streams: 6/12 · Severity: SERIOUS · Tier B

Findings: ARCH-SER-09, IND-PROC-01, IND-PROC-03, STRUCT-04, STRUCT-05,
EDGE-14, EDGE-15, PARTY-CRIT-03, PARTY-DOC-03.

### THEME-N — ARCHITECTURE.md summary sections silently drift from ADRs

Streams: 5/12 · Severity: SERIOUS · Tier B

Findings: STRUCT-03, STRUCT-06, STRUCT-08, STRUCT-12, STRUCT-15,
PARTY-DOC-02.

### THEME-O — Status enum / Tests-Status / REQ.status conflict

Streams: 5/12 · Severity: SERIOUS · Tier B

Findings: ARCH-SER-11, IND-PROC-04, EDGE-01, EDGE-02, EDGE-03, READY-08.

Pre-existing: STATUS.md P2.

### THEME-P — "The paper" prose reference

Streams: 5/12 · Severity: SERIOUS · Tier B

Findings: IND-PROC-07, ADVS-CRIT-05, STRUCT-14, INHER-03, ADVO-SER-01
(related).

### THEME-Q — Anti-aliasing rule defects

Streams: 6/12 · Severity: SERIOUS · Tier B

Findings: IND-SER-02, ADVO-SER-05, ADVS-SERI-05, ADVH-SER-06, READY-13,
INHER-21, PREM-06.

### THEME-R — Vapor references (tools/configs that don't exist)

Streams: 9/12 · Severity: SERIOUS · Tier A

Findings: ARCH-CRIT-06, ARCH-SER-08, ARCH-PROC-01, ARCH-PROC-03,
INHER-05, INHER-15, INHER-20, INHER-22, READY-07, READY-11, READY-12,
ADVS-PROC-02, ADVS-PROC-03.

### THEME-S — PHASE-5 entry depends on undelivered product content

Streams: 5/12 · Severity: SERIOUS · Tier B

Findings: ARCH-SER-12, ADVO-SER-08, READY-04, PARTY-PROC-01, plus
embedded in PHASE-K findings.

### THEME-T — Operational artifact gaps (numbers, calibration, baselines)

Streams: 6/12 · Severity: SERIOUS · Tier B

Findings: IND-SER-10, IND-SER-11, ADVO-SER-05 (overlap Q), ADVS-PROC-04,
PARTY-REQ-04, INHER-19, EDGE-29, plus most of THEME-J.

### THEME-U — Identifier allocation races

Streams: 5/12 · Severity: SERIOUS · Tier B

Findings: EDGE-10, EDGE-11, EDGE-12, EDGE-13, EDGE-15, ADVO-PROC-01,
ADVO-PROC-07, INHER-17, INHER-18.

### THEME-V — Inter-agent trust + UX

Streams: 4/12 · Severity: SERIOUS · Tier B

Findings: PREM-17, PARTY-UX-01, PARTY-UX-02, INHER-15 (overlap H).

### THEME-W — Anthropic-client transitive imports + GAS carve-out

Streams: 3/12 · Severity: SERIOUS · Tier B

Findings: PREM-14, ADVH-CRIT-12, READY-14, ADVS-PROC-05.

### THEME-X — Append-only spec calcification (long-horizon)

Streams: 1/12 · Severity: SERIOUS · Tier C

Findings: PREM-07 only.

### THEME-Y — PHASE-5 §Scope numbering bug

Streams: 5/12 · Severity: PROCESS · Tier B

Findings: ADVS-SERI-06, ADVO-PROC-04, STRUCT-10, plus IND-related,
PROSE-related.

### THEME-Z — `commit-trailers-valid` trigger surface contradicted

Streams: 3/12 · Severity: CRITICAL · Tier B (rolled into B for resolution)

Findings: READY-03, ADVS-CRIT-02, ADVH-SER-08.

---

## Findings not yet bucketed into a theme

A small number of findings are tactical specifics that don't form a
distinct cluster. They will be addressed within whichever CHG handles
the relevant ADR.

- ARCH-SER-07 (xref-resolves ID-in-file unverified) — folds into THEME-U
- ARCH-SER-09 (universal amendment-log) — listed under THEME-M
- ADVO-SER-10 (REQ atomicity vs `@covers` arity) — folds into THEME-G
- PARTY-REQ-01 (principles aren't REQs) — folds into THEME-G
- PARTY-REQ-02 (REQ-ARCH-0007 string-match vs semantic) — THEME-L
- PARTY-REQ-03 (compound-detector appeal path) — THEME-G
- INHER-18 (project-overlay collision rules) — THEME-U
- ADVO-SER-08 (sample-size N=5 unbounded) — THEME-J
- ADVS-PROC-04 (cost-tier enumeration missing) — THEME-J / T
- ADVH-CRIT-10 (Epic reconciliation vs staging exclusion contradiction)
  — new mini-theme or fold into THEME-N
- INHER-13 (causality loop first commit) — listed under THEME-D
- READY-18 (`tools/ci/tests/` discovery ungrounded) — THEME-H
- PARTY-PROC-02 (no per-REQ cost estimate) — meta finding; revisit at
  CHG-N (stochastic hardening) or as separate workflow-cost ADR

---

## Audit metadata

- Date: 2026-05-17
- Branch: claude/bmad-architecture-review-sV42w
- Architecture commit reviewed: HEAD at audit-launch time
- Reviewer LLM: claude-opus-4-7[1m] (consolidator), plus 10 sub-agents
  across opus/sonnet/haiku
- Skills used: bmad-review-adversarial-general (×4), bmad-review-edge-
  case-hunter, bmad-check-implementation-readiness, bmad-editorial-
  review-structure, bmad-editorial-review-prose, bmad-advanced-
  elicitation (pre-mortem), bmad-party-mode
- Custom prompts: inheritor-framed adversarial (no specific BMAD skill)
- Temperature variation: not directly controllable via Agent tool;
  proxied through model diversity and prompt-framing diversity

## What is *not* in this audit

- No review of `tools/spec_lint/`, `tools/ci/`, `_bmad/`,
  `.github/workflows/` (deferred to "implementation audit" per STATUS.md
  roadmap; was originally Action #2 in the prior-session task framing
  before re-prioritized).
- No formal validation of the CHG/sprint roadmap (CHG-0014b, 0015,
  0016+) against the audit findings. Findings *may* re-sequence or
  invalidate queued CHGs; that re-sequencing is itself a follow-on
  decision.
- No quantitative scoring of findings (impact × probability × cost-to-
  fix). Severity tiers are qualitative.
