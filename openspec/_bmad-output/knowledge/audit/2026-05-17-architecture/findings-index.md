# Findings Provenance Index — 2026-05-17 Architecture Audit

Cross-reference between the ~770 raw findings (across 40 streams in 5
waves) and the consolidated themes in [consolidated.md](consolidated.md).
Per-theme constituent listings cover Waves 1-3 fully; Wave 4 and Wave 5
constituent listings are deferred to the next consolidation pass — see
[corrections.md](corrections.md) META-CRIT-002 for the rationale.

The raw finding *bodies* are not duplicated here — they exist in the
per-stream findings files under [`findings/`](findings/) and in the raw
transcripts under [`raw-transcripts/`](raw-transcripts/). This index
preserves the *mapping*: which stream surfaced which finding, and which
theme it clusters under (for Waves 1-3).

For each theme, the constituent finding IDs are listed. For each stream,
the per-stream tally is recorded.

---

## Per-stream tally

### Wave 1 — 12 streams (broad methodology coverage)

| Stream | Prefix | Model | Method | C/SER/PROC | Total |
|---|---|---|---|---|---|
| In-context | `ARCH-` | opus | adversarial-general | 8 / 14 / 9 | 31 |
| First isolated | `IND-` | opus | adversarial-general | 8 / 12 / 7 | 27 |
| Second isolated | `ADVO-` | opus | adversarial-general | 6 / 10 / 8 | 24 |
| Sonnet isolated | `ADVS-` | sonnet | adversarial-general | 5 / 9 / 5 | 19 |
| Haiku isolated | `ADVH-` | haiku | adversarial-general | 6 / 6 / 3 | 15 |
| Inheritor framing | `INHER-` | opus | scenario | (mixed) | 22 |
| Edge-case hunter | `EDGE-` | opus | branch-walk | (mixed) | 44 |
| Implementation readiness | `READY-` | opus | completeness | 6/7/6 | 19 |
| Editorial structure | `STRUCT-` | opus | restructure | (mixed) | 15 |
| Editorial prose | `PROSE-` | sonnet | modal/quantifier | 3 / 7 / 4 | 14 |
| Pre-mortem | `PREM-` | opus | failure-narrative | 4 CRIT+rest SER | 18 |
| Party-mode | `PARTY-` | opus | 6-persona roundtable | 3 / 14 / 5 | 22 |
| **Wave 1 total** | | | | | **270** |

### Wave 2 — 8 streams (methodology + model diversity)

| Stream | Prefix | Model | Method | C/SER/PROC | Total |
|---|---|---|---|---|---|
| Socratic elicitation | `SOC-` | opus | advanced-elicitation socratic | 5 / 10 / 4 | 19 |
| Red-team adversary | `RED-` | opus | advanced-elicitation red-team | 5 / 7 / 4 | 16 |
| Post-PHASE-5 retrospective | `RETRO-` | opus | retrospective (hypothetical) | 4 CRIT-WRONG + 3 CRIT-MISSING + 5 SER-MISSING + 2 PROC | 19 |
| Spec-validation | `VALID-` | opus | validate-prd | 8 / 8 / 2 | 18 |
| Winston solo (architect) | `WIN-` | opus | persona self-critique | 6 / 12 / 4 | 22 |
| Compression-based | `DISTILL-` | sonnet | distillator | 3 / 7 / 5 | 15 |
| First-principles | `FIRST-` | sonnet | advanced-elicitation first-principles | 5 / 6 / 4 | 13 (+1 methodology artifact: `FIRST-CRIT-01` retracted — FIRST misread its own prompt re: ADR-0003, which WAS in the listed 15 documents; see [corrections.md](corrections.md) META-CRIT-003) |
| Amelia solo (dev) | `AME-` | sonnet | persona implementability | 7 / 8 / 5 | 20 |
| **Wave 2 total** | | | | | **142** |

### Wave 3 — 8 streams (personas + editorial mutations)

| Stream | Prefix | Model | Method | C/SER/PROC | Total |
|---|---|---|---|---|---|
| John solo (PM) | `PM-` | opus | persona product-mgmt | 6 / 9 / 5 | 20 |
| Mary solo (analyst) | `MARY-` | opus | persona requirements | 8 / 10 / 4 | 22 |
| Sally solo (UX) | `SALLY-` | sonnet | persona UX (3-user-populations) | 5 / 7 / 5 | 17 |
| Paige solo (tech writer) | `PAIGE-` | sonnet | persona knowledge-curation | 4 / 8 / 8 | 20 |
| Edit-PRD defects | `EDIT-` | opus | edit-prd | 7 / 10 / 7 | 24 (paginated; actual ~17 unique) |
| Course-correction | `COURSE-` | opus | correct-course | 4 / 5 / 3 | 12 |
| Checkpoint-preview | `CHECK-` | opus | checkpoint-preview | 4 / 8 / 4 | 16 |
| Devil's advocate | `DEVIL-` | opus | advanced-elicitation devil's-advocate | 4 / 7 / 5 | 16 |
| **Wave 3 total** | | | | | **~147** (some EDIT- entries split into multiple findings) |

### Wave 4 — 8 streams (sonnet model-permutations + 2 new methods)

| Stream | Prefix | Model | Method | C/SER/PROC | Total |
|---|---|---|---|---|---|
| Red-team sonnet | `RED2-` | sonnet | advanced-elicitation red-team | (mixed) | ~15 |
| Retrospective sonnet | `RETRO2-` | sonnet | retrospective | (mixed) | ~15 |
| Edge-case-hunter sonnet | `EDGE2-` | sonnet | edge-case-hunter | (mixed) | ~25-30 |
| Inheritor sonnet | `INHER2-` | sonnet | inheritor-framing | (mixed) | ~10 |
| Spec-validation sonnet | `VALID2-` | sonnet | validate-prd | (mixed) | ~12 |
| Pre-mortem sonnet | `PREM2-` | sonnet | advanced-elicitation pre-mortem | (mixed) | ~10 |
| Stakeholder simulation | `STAKE-` | opus | stakeholder-simulation (NEW) | 5 / 12 / 3 | 20 (originally reported as ~25 in qd-triage.md §3.4; corrected per [corrections.md](corrections.md) META-CRIT-004) |
| Counter-factual | `COUNTER-` | opus | counter-factual (NEW) | (mixed) | ~20 (count needs re-verification per [corrections.md](corrections.md) META-CRIT-004) |
| **Wave 4 total** | | | | | **~130** |

### Wave 5 — 4 streams (QD admission: cell-targeted methods)

| Stream | Prefix | Model | Method | C/SER/PROC | Total | Cell (Lens × Temporal × Decomp × Severity) |
|---|---|---|---|---|---|---|
| Governance-focused validation | `GOV-` | opus | validate-prd-governance-focused | 5 / 14 / 3 | 22 | attitudinal × current × focused × governance |
| Security engineer (holistic) | `SEC-` | opus | persona-security-engineer-holistic | 7 / 9 / 5 | 21 | persona × current × holistic × security/ops |
| Devil's advocate (governance focus) | `GOVDEV-` | opus | advanced-elicitation devil's-advocate (governance-focused) | 5 / 11 / 6 | 22 | contrarian × current × focused × governance |
| Reasoning-tree meta-auditor | `META-` | opus | reasoning-tree-meta-audit | 4 / 12 / 3 | 19 | meta × * × * × * (candidate 5th axis) |
| **Wave 5 total** | | | | | **84** | |

### Grand total (all 40 streams)

| | Count |
|---|---|
| Wave 1 raw findings | 270 |
| Wave 2 raw findings | 142 |
| Wave 3 raw findings | ~147 |
| Wave 4 raw findings | ~130 |
| Wave 5 raw findings | 84 |
| **Grand total raw findings** | **~770** |
| Distinct themes (after dedup, Waves 1-4 only) | ~70 |
| Wave-5 distinct themes (next consolidation pass) | pending |
| Pre-existing in STATUS.md (C/S/P/NEW) | 19 |
| META- corrections logged | 19 (4 / 12 / 3) — see [corrections.md](corrections.md) |

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

## Wave 2 themes added

### THEME-AA — Adversarial enforcement gap (no gates that verify gates)

Streams: RED, VALID (orthogonal angle) · Severity: CRITICAL · Convergence: Tier B

Findings: RED-CRIT-01 (BMAD skill content smuggling), RED-CRIT-04 (raw HTTP bypass), RED-CRIT-05 (squash-merge trailer bypass), RED-SER-08 (gate-coverage canary missing), RED-SER-09 (journal forgery), RED-SER-10 (token exfiltration via E2E spreadsheet), RED-SER-12 (silent stochastic power degradation), VALID-SERIOUS-15 (gate-coverage self-test missing).

### THEME-BB — ADR supersession protocol (`superseded_by` unused)

Streams: PARTY, IND, RETRO, COURSE · Severity: CRITICAL · Convergence: Tier A

Findings: PARTY-CRIT-03, IND-PROC-01, RETRO-CRIT-07, COURSE-CRIT-01, COURSE-PROC-10, EDIT-CRIT-05.

### THEME-CC — Missing test tiers (security, performance)

Streams: RETRO, RED · Severity: CRITICAL · Convergence: Tier B

Findings: RETRO-CRIT-04, RED-SER-10 (security-tier overlap).

### THEME-DD — Phase regression state machine

Streams: RETRO · Severity: CRITICAL · Convergence: Tier C

Findings: RETRO-CRIT-06.

### THEME-EE — Secrets/credentials specification

Streams: RETRO, RED, ARCH · Severity: CRITICAL · Convergence: Tier B

Findings: RETRO-CRIT-05, RED-SER-10, ARCH-PROC-06.

### THEME-FF — Local development environment

Streams: RETRO, WIN · Severity: SERIOUS · Convergence: Tier C

Findings: RETRO-SER-06, WIN-CRIT-21.

### THEME-GG — Hook ABI / Claude Code hook syntax

Streams: AME, ADR-0005-implementation related · Severity: CRITICAL · Convergence: Tier B

Findings: AME-CRIT-01, AME-CRIT-02, AME-CRIT-03, AME-CRIT-04, AME-SERIOUS-07.

### THEME-HH — BMAD upstream dependency risks (license, internal API)

Streams: WIN · Severity: SERIOUS · Convergence: Tier C

Findings: WIN-CRIT-08, WIN-CRIT-09.

### THEME-II — Network dependency in commit hook

Streams: FIRST, ADVH (related) · Severity: CRITICAL · Convergence: Tier C

Findings: FIRST-CRIT-05, ADVH-SER-04 (related on hook-abort UX).

### THEME-JJ — Test runner ownership

Streams: WIN, AME · Severity: SERIOUS · Convergence: Tier C

Findings: WIN-CRIT-21, AME-PROCESS-04 (related).

### THEME-KK — Append-only NOT gated for ADR amendments

Streams: FIRST · Severity: SERIOUS · Convergence: Tier C

Findings: FIRST-PROC-01.

### THEME-LL — BMAD CWD discipline 4-phase gap

Streams: FIRST · Severity: PROCESS · Convergence: Tier C

Findings: FIRST-PROC-03.

### THEME-MM — Retroactive compliance remediation protocol

Streams: FIRST, AME, ADVS · Severity: SERIOUS · Convergence: Tier B

Findings: FIRST-PROC-04, AME-CRIT-07, ADVS-CRIT-01.

### THEME-NN — PRD→REQ traceability ungated

Streams: FIRST · Severity: SERIOUS · Convergence: Tier C

Findings: FIRST-SERI-02.

### THEME-OO — Long-running branch matrix conflicts

Streams: RETRO, WIN · Severity: SERIOUS · Convergence: Tier C

Findings: RETRO-SER-10, WIN-CRIT-06 (related on derived-cache thrash).

### THEME-PP — Anti-aliasing n-gram vs semantic similarity

Streams: PREM, FIRST, WIN, DEVIL · Severity: SERIOUS · Convergence: Tier B

Findings: PREM-06, FIRST-SERI-01, WIN-CRIT-05, DEVIL-SER-07.

## Wave 3 themes added

### THEME-RR — Product workflow primitives missing (experimentation, removal, metrics)

Streams: PM, PARTY (partial), DEVIL · Severity: CRITICAL · Convergence: Tier B

Findings: PM-CRIT-03, PM-CRIT-04, PM-CRIT-05, PM-CRIT-06, PM-SER-08, PM-SER-09, PM-SER-15, PM-PROC-16, PM-PROC-17, PM-PROC-18, PM-PROC-19, PM-PROC-20, PARTY-PROC-01 (overlap with THEME-S).

### THEME-SS — Glossary and terminology drift

Streams: PAIGE · Severity: CRITICAL · Convergence: Tier C

Findings: PAIGE-CRIT-03, PAIGE-SER-04, PAIGE-SER-05.

### THEME-TT — Audience clarity

Streams: PAIGE · Severity: SERIOUS · Convergence: Tier C

Findings: PAIGE-SER-07.

### THEME-UU — Principle independence / meta-architecture

Streams: DEVIL · Severity: CRITICAL · Convergence: Tier C

Findings: DEVIL-CRIT-01.

### THEME-VV — Principle list append-only protection

Streams: DEVIL · Severity: PROCESS · Convergence: Tier C

Findings: DEVIL-PRO-12.

### THEME-WW — Determinism vs idempotence (terminology + property test)

Streams: MARY · Severity: SERIOUS · Convergence: Tier C

Findings: MARY-SERIOUS-12.

### THEME-XX — Trailer signal quality (checkpoint auto-production)

Streams: DEVIL · Severity: SERIOUS · Convergence: Tier C

Findings: DEVIL-SER-11.

### THEME-YY — Stack consolidation (BMAD/TEA/OpenSpec as one)

Streams: DEVIL · Severity: PROCESS · Convergence: Tier C

Findings: DEVIL-PRO-13.

### THEME-ZZ — Forward references / reading order / onboarding

Streams: PAIGE, SALLY · Severity: SERIOUS · Convergence: Tier C

Findings: PAIGE-SER-01, SALLY-SERIOUS-06 (related on STATUS.md being unspecified).

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
