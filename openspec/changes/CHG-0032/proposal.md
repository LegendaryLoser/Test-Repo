---
id: CHG-0032
title: Architecture audit (BMAD multi-pass) + QD triage + corpus persistence
status: in-progress
date: 2026-05-17
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0002
    - ADR-0005
    - ADR-0008
---

# CHG-0032 — Architecture audit (BMAD multi-pass) + QD triage + corpus persistence

## Why

Two drivers:

1. **User direction:** maximum-rigor multi-perspective adversarial review
   of the 15-document architecture artifact (ARCHITECTURE.md + 8 ADRs +
   6 PHASE files) before resuming any queued implementation roadmap.
   Closes the open audit finding NEW-3 (BMAD review skills not in CHG
   workflow) per STATUS.md.
2. **Methodology question:** the project's previously declared
   convergence metric (COMPOSITE-V2 Gate 6 — "<10% marginal novelty")
   turned out to be structurally unachievable. The Wave 4 supplement
   surfaced an empirical finding that marginal novelty is dominated by
   methodology variance, not model variance, so any genuinely new method
   spikes novelty back to ~60-70%. A research-grounded replacement
   metric was needed.

## What changes

This CHG bundles audit execution + measurement-framework adoption +
evidence persistence. **It does not author the methodology codification
ADR** (per user direction, that ADR is queued for after both
architecture and implementation audits converge). It also does not
start any Tier 1+ resolution CHGs.

### Architecture audit corpus

Seven waves of multi-perspective adversarial review (and continuing per user
direction "keep going wave after wave"):

- **Wave 1:** 12 streams across diverse methods (adversarial-general,
  edge-case-hunter, implementation-readiness, editorial-structure,
  editorial-prose, pre-mortem, party-mode, inheritor framing) and
  diverse models (opus, sonnet, haiku).
- **Wave 2:** 8 streams adding socratic, red-team, retrospective,
  validate-prd, Winston persona, distillator, first-principles, Amelia
  persona.
- **Wave 3:** 8 streams adding John PM, Mary analyst, Sally UX, Paige
  tech writer, edit-PRD, correct-course, checkpoint-preview, devil's
  advocate.
- **Wave 4:** 8 streams: 6 sonnet model-permutations of prior methods
  (red-team, retrospective, edge-case-hunter, inheritor, validate-prd,
  pre-mortem) and 2 new methods (stakeholder-simulation,
  counter-factual).
- **Wave 5:** 4 streams targeting Tier-1 empty cells per
  `qd-triage.md` §8: governance-focused validation (`GOV-`),
  security-engineer persona (`SEC-`), governance devil's-advocate
  (`GOVDEV-`), and reasoning-tree meta-auditor (`META-`). First wave
  admitted under the QD admission rule; first wave to invoke a
  candidate 5th axis (meta).
- **Wave 6:** 4 streams finishing Tier-1 high-importance empty cells +
  2 never-occupied (Lens × Temporal) cells per `qd-triage.md` §4.1:
  structural-governance (`STRUCTGOV-`), security-focused distillation
  (`SECDISTILL-`), scenario-unfold-current-state (`SCENNOW-`),
  Winston-2029 persona-retrospective (`PERSRETRO-`).
- **Wave 7:** 4 streams targeting remaining forward + post-hoc
  (Lens × Temporal) cells per `qd-triage.md` §8.2: 18-month-forward
  scenario unfold (`SCENFUT-`), forward structural-growth-pressure
  (`STRUCTFUT-`), 2029-external-critic contrarian retrospective
  (`DEVRETRO-`), attitudinal-forward discipline-additions
  (`ATTFUT-`).

Total: 48 streams. Raw findings: ~700 (Waves 1-4) + 84 (Wave 5) + 75
(Wave 6) + 72 (Wave 7) ≈ ~932. Themes: ~70 from Waves 1-4 + ~25 new
from Wave 5 + ~29 new from Wave 6 ≈ ~125 (Waves 1-6 consolidated);
Wave-7 thematic consolidation deferred to a follow-on task.

### Consolidation and triage

Artifacts at `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/`:

- `README.md` — session metadata.
- `consolidated.md` — thematic clustering (~70 themes) with 17-tier
  proposed resolution sequence.
- `findings-index.md` — per-stream provenance ledger and theme →
  constituent finding ID mapping.
- `qd-triage.md` — Quality-Diversity triage of all 36 streams; per-
  method σ × κ scoring; Tier A/B/C/D catalog; QD matrix occupancy;
  empty-cell Wave-5 admission targets; ACGR convergence metric
  diagnostic; 8 draft clauses (§§1-11) for the methodology
  codification ADR.

### Quality-Diversity framework adoption

Replaces COMPOSITE-V2 Gate 6 with σ × κ Pareto admission per cell + ACGR
(Archive Coverage Growth Rate) convergence metric. Grounded in published
research: MAP-Elites (Mouret & Clune 2015; Stock 2025), Multi-Objective
MAP-Elites (Pierrot et al. 2022), ambiguity decomposition (Krogh &
Vedelsby 1994), Mixture of Complementary Agents (NeurIPS 2025),
Self-MoA negative result (Wang et al. 2025), Multi-Agent Debate
stability research (ICLR 2025). See `qd-triage.md` §1 for citations
and §2 for definitions.

### Corpus persistence

47 sub-agent raw transcripts (35 from Waves 1-4 + 4 from Wave 5 + 4
from Wave 6 + 4 from Wave 7) plus per-stream extracted findings
markdown persisted into `raw-transcripts/` and `findings/`
subdirectories. Manifest at `raw-transcripts/MANIFEST.md`; extraction
tool at `raw-transcripts/persist-corpus.py`. The 48th stream
(`ARCH-`, in-context) has no separate transcript. The extraction
tool is incremental: each re-run ingests new cache-resident
transcripts whose description is in `DESC_TO_STREAM` and preserves
rows for transcripts already on disk from prior sessions.

### REQ-AUDIT-0001

New requirement at `openspec/specs/audit/methodology.spec.md`. Captures
the corpus-persistence obligation. Status: `draft`; full enforcement
deferred to the methodology codification ADR.

### Session-resume infrastructure

`openspec/STATUS.md` updated across multiple sweeps to reflect audit
progress, decisions made, and the "Next session: start here" pointer.

## Out of scope

- **Methodology codification ADR.** Draft clauses are in
  `qd-triage.md` §9; full authoring is queued for after the
  implementation audit converges and the joint resolution sequence is
  approved. Per user direction (STATUS.md Recent decisions
  2026-05-17 row "Codify audit methodology in ADR after BOTH
  architecture + implementation audits complete").
- **Implementation audit.** Queued as a separate CHG; uses the QD
  catalog from `qd-triage.md` §5 dogfood-style against `tools/spec_lint/`,
  `tools/ci/`, `_bmad/`, and `.github/workflows/`.
- **Wave 5 thematic consolidation.** Wave 5 raw findings are persisted
  per TASK-0042 but their integration into `consolidated.md`
  (new-theme identification, sole-source attribution), `qd-triage.md`
  §3.5 (per-stream σ × κ), and ACGR re-measurement are deferred to a
  follow-on consolidation task. Predicted ACGR per `qd-triage.md` §7:
  10-15%; this prediction is testable only after the consolidation pass.
- **Wave 6.** Conditional on the Wave-5 ACGR re-measurement. Per
  `qd-triage.md` §2.6 the architecture audit terminates when ACGR < 5%
  for two consecutive waves.
- **Resolution CHGs.** The 17-tier resolution sequence in
  `consolidated.md` (CHG-A through CHG-CC) is a *proposal*. No
  resolution CHG starts until both audits converge per user direction
  (STATUS.md Recent decisions 2026-05-17 row "Re-sequence: do not start
  any Tier 1+ resolution CHG until both audits converge").
- **σ × κ measurement automation.** The triage estimated σ and κ from
  theme membership counts. The methodology ADR's red-test phase will
  add tools at `tools/ci/tests/audit_meta/` to mechanise both measures.

## Tasks

| Task | Type | Status | Summary | Commit |
|------|------|--------|---------|--------|
| TASK-0035 | docs | done | Wave 1 audit (12 streams) consolidated | `cc7ce61` |
| TASK-0036 | docs | done | Wave 2+3 supplement (16 streams) | `dc3e4fa` |
| TASK-0037 | docs | done | Wave 4 supplement (8 streams); methodology-variance finding | `8a9f7ee` |
| TASK-0038 | docs | done | Quality-Diversity triage of all 36 streams | `28a06b8` |
| TASK-0039 | docs | done | STATUS.md staleness sweep | `50b21f8` |
| TASK-0040 | docs | done | Corpus rescue: 35 transcripts + findings + manifest | `04be686` |
| TASK-0041 | docs | done | Author CHG-0032 envelope retroactively (this proposal + 7 TASK files + REQ-AUDIT-0001) | `5df73fb` |
| TASK-0042 | docs | done | Architecture audit Wave 5 (4 streams: governance, security, governance-devil's-advocate, meta-auditor) | `13f5401` |
| TASK-0043 | docs | done | META- audit corrections log + findings-index Wave 4 + Wave 5 catch-up | `067eefc` |
| TASK-0044 | docs | done | Wave-5 thematic consolidation (~25 new themes) + qd-triage §3.5 + ACGR re-measurement (~91% ± 16%) | `9ae2a6a` |
| TASK-0045 | docs | done | Architecture audit Wave 6 (4 streams: STRUCTGOV, SECDISTILL, SCENNOW, PERSRETRO; 75 raw findings) | `cd45777` |
| TASK-0046 | docs | done | Wave-6 thematic consolidation (~29 new themes) + qd-triage §3.6 + ACGR re-measurement (~105% ± 21%) | `bd702ea` |
| TASK-0047 | docs | done | Architecture audit Wave 7 (4 streams: SCENFUT, STRUCTFUT, DEVRETRO, ATTFUT; 72 raw findings) | `48097c3` |
| TASK-0048 | docs | done | Wave-7 thematic consolidation (~24 new themes) + qd-triage §3.7 + ACGR re-measurement (~87% ± 17%) | `78a03a7` |
| TASK-0049 | docs | done | Signal-filter triage of 867 findings: 42 dup clusters, 1 contradiction, ~120-150 unique defects (signal-ledger.md) | `b3eab84` |
| TASK-0050 | docs | done | Methodology research note: dual-metric critique (coverage tautology, ordering bias, audit-type variance) + saturation-based reformulation + two-layer framework (methodology-research-note.md) | `e2fc8ad` |
| TASK-0051 | docs | done | Cell finalization: 42 clusters → 15 cells; saturation 93% strict / 80% inclusive; QD-score baseline ~58.8; W7 ΔQD-score 29% (cell-occupancy.md) | `6c02984` |
| TASK-0052 | docs | done | Wave 8 path-dependence test (Option C): 3 streams (COMPLIRETRO, FAILSCEN, INTRRETRO) opened ~30 new clusters; 42 → 72 clusters; saturation 93% → 58%; path-dependence empirically substantial (wave-8-path-dependence-results.md) | `cad45f4` |
| TASK-0053 | docs | queued | POC instantiate v1.0 closure-argument-framework for architecture-audit archetype against 72-cluster corpus (closure-argument-framework.md is the spec; TASK-0053 is the fresh-session POC) | (queued for fresh session) |

See `tasks/` for per-task detail.

## Rollout

The audit's deliverables are STAGING-only per ADR-0002 §7. Nothing in
this CHG modifies authoritative artifacts (specs, INDEX.yaml entries
other than REQ-AUDIT-0001, source code, or CI gates). No CI gate or
test count is changed.

Next-session actions are documented in STATUS.md "Next session: start
here" section. The first action is a user decision: run Wave 5
architecture audit, or start the implementation audit, or both.

## Risk

- **Retroactive envelope authoring (THEME-MM).** The proposal and TASK
  files were authored *after* the work they describe, violating
  red-first discipline (P4). The next session inheriting this work
  must treat the envelope as descriptive (a faithful record of what
  was done) rather than prescriptive (an upfront contract). The
  methodology codification ADR is expected to address whether audit
  CHGs need a different lifecycle than implementation CHGs.
- **REQ-AUDIT-0001 status = draft.** The corpus-persistence assertion
  has no mechanical enforcement gate yet. A future audit could fail
  to persist and `spec_lint validate` would not catch it. Enforcement
  is deferred to the methodology codification ADR.
- **`Requirements: REQ-AUDIT-0001` in trailers TASK-0036 and TASK-0037
  pre-dated the REQ's existence.** This commit retroactively makes the
  references valid. Future commits should not allocate REQ-IDs in
  trailers before authoring the matching spec block. <!-- spec-lint: allow prose-xref-banned -->
- **QD framework adoption ahead of formal ADR.** STATUS.md Recent
  decisions records the QD framework adoption, but the codification
  ADR has not landed. If the implementation audit invalidates parts of
  the framework, those changes must propagate to `qd-triage.md` and
  the queued methodology codification ADR. <!-- spec-lint: allow prose-xref-banned --> The triage's §11
  limitations section flags the unmeasured σ / κ values and the
  post-hoc behavioural-axis choice as the most exposed assumptions.
- **Audit findings remain unresolved.** ~70 themes, including 12 Tier-A
  CRITICAL themes (BMAD strategy drift, trailer schema fragmentation,
  gate-coverage syntactic-not-semantic, hook implementation, red-before-
  green checkpoint, push invariant, phase ordering, etc.). The
  resolution program is a multi-month effort if pursued in full;
  scope decisions are listed in `consolidated.md` "Decision points
  before kicking off the resolution program."
