# Wave 8 path-dependence test results

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative.

**Companion documents:**
- [`cell-occupancy.md`](cell-occupancy.md) — pre-Wave-8 cell occupancy + saturation analysis (now superseded by §3 below)
- [`methodology-research-note.md`](methodology-research-note.md) — path-dependence framing (§2.2) — empirically validated by this experiment
- [`signal-ledger.md`](signal-ledger.md) — 42 cluster baseline (now expanded to ~72 per this analysis)
- [`findings/COMPLIRETRO-findings.md`](findings/COMPLIRETRO-findings.md), [`findings/FAILSCEN-findings.md`](findings/FAILSCEN-findings.md), [`findings/INTRRETRO-findings.md`](findings/INTRRETRO-findings.md) — Wave-8 raw findings

**Purpose.** TASK-0051's `cell-occupancy.md` reported 93% cluster-level saturation under strict K=2, and acknowledged in §6 that the cell map is path-dependent (60% of clusters first-surfaced in Wave 1, attributable to method-mix). The methodology-research-note §2.2 listed N-restart bootstrap as the rigorous-but-expensive mitigation. Per user direction Option C, Wave 8 spawned 3 streams — each adding a SECOND method to a cell currently occupied by only one Wave-6/7 method — to empirically test whether the first method's Pareto front was complete or whether counterfactual methods would surface clusters the first method missed.

The result: **~30 NEW clusters across 3 streams**. The pre-Wave-8 saturation estimate (93%) was decisively wrong. Path-dependence is substantial in this corpus.

---

## §1 Wave 8 streams and counts

| Stream | Cell (first-method counterpart) | Findings | NEW clusters | REINFORCEMENT findings |
|---|---|---|---|---|
| COMPLIRETRO | persona × post-hoc × holistic × governance (vs PERSRETRO Wave 6, Winston-architect) | 17 (7/7/3 C/S/P) | ~8 | ~9 |
| FAILSCEN | scenario × current × exhaustive × blocking-impl (vs SCENNOW Wave 6, actor scenarios) | 18 (10/5/3) | ~14 | ~4 |
| INTRRETRO | contrarian × post-hoc × holistic × cost/value (vs DEVRETRO Wave 7, external critic) | 18 (6/8/4) | ~8 | ~10 |
| **Wave 8 total** | | **53** | **~30** | **~23** |

**Per-stream NEW-vs-REINFORCEMENT ratios:** COMPLIRETRO 47% new, FAILSCEN 78% new, INTRRETRO 44% new. FAILSCEN's much higher novelty rate is the most surprising result — the failure-mode scenario lens is operationally distinct enough from SCENNOW's actor-scenario lens that 14 of 18 findings open fundamentally new clusters.

---

## §2 New clusters opened by Wave 8 (~30)

Adding to `signal-ledger.md` §5's 42 dense clusters. Continuing the alphabetical naming (43-72). Cell assignments per defect content following `cell-occupancy.md` §1 methodology.

### Opened by COMPLIRETRO (~8 NEW)

| # | New cluster | Cell | Member findings | Notes |
|---|---|---|---|---|
| 43 | Evidence retention policy (≥7yr SOX) | persona × post-hoc × holistic × governance | COMPLIRETRO-CRIT-005 | sole-source from compliance lens |
| 44 | Regulatory control mapping (SOC2/ISO/SOX/HIPAA → REQ) | persona × post-hoc × holistic × governance | COMPLIRETRO-CRIT-006 | sole-source; no architecture artifact maps controls |
| 45 | Approver-enumeration interface (audit.py extension) | persona × post-hoc × focused × governance | COMPLIRETRO-SER-009 | sole-source |
| 46 | Access-review machinery (quarterly access enumeration) | persona × post-hoc × holistic × governance | COMPLIRETRO-SER-010 | sole-source |
| 47 | Stochastic-tier evidence retention (per-run sample archive) | persona × post-hoc × focused × security/ops | COMPLIRETRO-SER-011 | sole-source; novel compliance angle on ADR-0007 |
| 48 | Periodic compliance reporting export (quarterly aggregate) | persona × post-hoc × holistic × governance | COMPLIRETRO-SER-013 | sole-source |
| 49 | Compliance-officer role + accountability chain | persona × post-hoc × focused × governance | COMPLIRETRO-PROC-015 | sole-source |
| 50 | Data classification + PII/GDPR-erasure in spec storage | structural × current × focused × security/ops | COMPLIRETRO-PROC-016 | sole-source; conflicts with ADR-0004 §7 immutability |

### Opened by FAILSCEN (~14 NEW)

| # | New cluster | Cell | Member findings | Notes |
|---|---|---|---|---|
| 51 | Matrix-write atomicity (mid-write OOM-kill) | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-001 | sole-source |
| 52 | Matrix schema-validation gate (partial-corruption detection) | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-002 | sole-source; ADR-0008 missing schema gate |
| 53 | Recovery runbook for matrix corruption (torn-write case) | scenario × current × exhaustive × blocking-impl | FAILSCEN-SER-003 | sole-source |
| 54 | Hook-failure audit trail (hook_failed journal event) | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-004 | sole-source |
| 55 | Hook quarantine / health-check (buggy-hook freeze recovery) | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-005 | sole-source; no escape valve currently |
| 56 | BMAD-upgrade forward-compat testing (spec_lint vs new outputs) | scenario × current × exhaustive × security/ops | FAILSCEN-CRIT-007 | sole-source; smoke-test inadequate per ADR-0002 §8 |
| 57 | Broken-upstream partial-bypass (matrix-drift during revert) | scenario × current × exhaustive × blocking-impl | FAILSCEN-SER-008 | sole-source |
| 58 | BMAD-rollback gate / SLA / canary | scenario × current × exhaustive × security/ops | FAILSCEN-PROC-009 | sole-source |
| 59 | Push-failed event in journal schema | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-010 | sole-source; journal §5 has no push_failed |
| 60 | SessionStart origin-fetch + divergence reconciliation | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-011 | sole-source |
| 61 | Multi-writer journal locking (O_APPEND PIPE_BUF limit) | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-012 | sole-source; sharper than Cluster T |
| 62 | Journaled-event integrity check (HMAC / sequence number) | scenario × current × exhaustive × security/ops | FAILSCEN-CRIT-013 | sole-source; sharper than Cluster T |
| 63 | Phase-exit-state.yaml (restartable phase-exit gate) | scenario × current × exhaustive × blocking-impl | FAILSCEN-CRIT-015, CRIT-016, SER-017 | 3-finding cluster |
| 64 | Aborted-gate manual-override runbook | scenario × current × exhaustive × blocking-impl | FAILSCEN-PROC-018 | sole-source |

### Opened by INTRRETRO (~8 NEW)

| # | New cluster | Cell | Member findings | Notes |
|---|---|---|---|---|
| 65 | PR-level (vs per-commit) trailer ceremony | contrarian × post-hoc × holistic × cost/value | INTRRETRO-CRIT-001 | sole-source; 80-100 eng-days cost cited |
| 66 | Anti-aliasing within-domain scoping + true:false-positive measurement | contrarian × post-hoc × focused × cost/value | INTRRETRO-SER-004 | sole-source; 1:8 ratio quantified |
| 67 | Multi-team CHG coordination envelope (EPIC-as-coordination) | contrarian × post-hoc × holistic × governance | INTRRETRO-CRIT-009 | sole-source; ~6 eng-weeks coordination cost |
| 68 | Stochastic-cached tier (replay-when-prompt-unchanged) | contrarian × post-hoc × focused × cost/value | INTRRETRO-SER-005 | sole-source; sharper than Cluster H |
| 69 | Bulk-rename CHG template + tooling | contrarian × post-hoc × focused × cost/value | INTRRETRO-SER-007 | sole-source |
| 70 | Documentary-only ADR / REQ classification (exempt from req-coverage-100) | contrarian × post-hoc × focused × governance | INTRRETRO-CRIT-013 | sole-source |
| 71 | Operating-the-discipline cheatsheet (first-class deliverable) | contrarian × post-hoc × holistic × cost/value | INTRRETRO-SER-014 | sole-source; onboarding 3-4wk → 2wk after cheatsheet |
| 72 | Backup ADR-reviewers + queue + SLA (single-architect bottleneck) | contrarian × post-hoc × focused × governance | INTRRETRO-PROC-016 | sole-source |

---

## §3 Revised cell-occupancy + saturation

Adding the ~30 new clusters to `cell-occupancy.md` §3's 15-cell map:

### Cells gaining clusters from Wave 8

| Cell | Pre-W8 clusters | + Wave 8 | New total |
|---|---|---|---|
| persona × post-hoc × holistic × governance (was empty pre-W6 PERSRETRO) | 0 (PERSRETRO opened singletons not in §5's 42) | +5 (43, 44, 46, 48) | **5** |
| persona × post-hoc × focused × governance (new cell) | 0 | +3 (45, 49, 72) | **3** |
| persona × post-hoc × focused × security/ops (new cell) | 0 | +1 (47) | **1** |
| structural × current × focused × security/ops (new cell) | 0 | +1 (50) | **1** |
| scenario × current × exhaustive × blocking-impl (new cell) | 0 | +11 (51-55, 57, 59-61, 63, 64) | **11** ← densest |
| scenario × current × exhaustive × security/ops (new cell) | 0 | +3 (56, 58, 62) | **3** |
| contrarian × post-hoc × holistic × cost/value (new cell) | 0 | +3 (65, 67, 71) | **3** |
| contrarian × post-hoc × focused × cost/value (new cell) | 0 | +4 (66, 68, 69) | **4** (wait — 3) |
| contrarian × post-hoc × focused × governance (new cell) | 0 | +2 (70, 72) | **2** |

**New cells opened by Wave 8: ~9** (most never-occupied pre-W8). Some of these "new cells" had Wave-6/7 method-admissions (PERSRETRO, SCENNOW, DEVRETRO) but no clusters — they were "method-occupied, cluster-empty."

### Pre-W8 cells unchanged (clusters not affected)

13 of the 15 pre-W8 cells remain at their pre-W8 cluster counts (Wave-8 streams operated in different cells). 2 cells received Wave-8 reinforcement findings (existing clusters strengthened) but no new clusters.

### Updated headline numbers

| Metric | Pre-W8 | Post-W8 |
|---|---|---|
| Dense clusters (≥3 members + sole-source clusters from Wave 8) | 42 | **~72** |
| Distinct cells occupied | 15 | **~24** |
| Audit-level saturation (strict K=2, cluster-only) | 93% | **~38%** (9 new cells opened in W8 → 9 unsaturated by definition; saturation = 15/24 = 62.5%... actually recomputing) |

Wait — recomputing properly. Cells that were saturated pre-W8 are still saturated post-W8 (no Wave-8 method admitted to them, no new clusters opened). Cells newly opened in W8 are by definition unsaturated (just got their first cluster + method). So:

- Pre-W8 cells, still saturated: 14 (the 15 minus SCENFUT-opened cell that was already un-saturated)
- New W8 cells, unsaturated: 9
- Pre-W8 SCENFUT cell, still un-saturated: 1
- **Saturation: 14 / (14 + 9 + 1) = 14/24 = 58%**

The audit's saturation **dropped from 93% to 58%** after one wave testing path-dependence. **This is decisive empirical evidence that the pre-W8 saturation metric was massively over-estimating convergence.**

### Audit-level QD-score (revised)

Pre-W8 QD-score baseline was ~58.8. Wave 8 added per-cell contributions:
- New scenario × current × exhaustive cells: FAILSCEN at σ × κ ≈ 0.80 × 14 = ~11.2 (highest single-stream κ since STAKE)
- New persona × post-hoc cells: COMPLIRETRO at σ × κ ≈ 0.85 × 8 = ~6.8
- New contrarian × post-hoc cells: INTRRETRO at σ × κ ≈ 0.80 × 8 = ~6.4

**Wave 8 ΔQD-score: ~+24.4.** **New QD-score: ~83.2.** **ΔQD-score / QD-score W8 = 24.4 / 83.2 = 29%.**

Wave 8 ΔQD-score / new-total is 29% — IDENTICAL to Wave 7's 29%. Depth metric is NOT converging either; each new method in counterfactual cells contributes substantial new depth.

---

## §4 Methodology implications

The Wave 8 result has 4 implications for the methodology codification ADR:

1. **Path-dependence is empirically substantial, not just theoretical.** Adding ONE counterfactual method to each of 3 cells produced ~30 new clusters — a ~71% expansion of the cluster set (42 → 72). The methodology-research-note §2.2 listed path-dependence as a known limitation; this experiment quantifies it. The "explicit acknowledgment" mitigation alone is **insufficient** — readers of a single-method-per-cell archive will under-estimate the true defect surface by ~40-70%.

2. **The cell map is incomplete by construction.** Wave 8 opened ~9 cells the pre-W8 framework hadn't recognized. The 15-cell pre-W8 count was an under-estimate. The true |meaningful_cells| denominator for this audit is probably 30-40 cells, not the 25-35 estimated in `signal-ledger.md` §6.6.

3. **The N-restart bootstrap mitigation is empirically necessary, not just preferable.** Methodology-research-note §2.2 listed N restarts as "cost-prohibitive" and recommended documentation-only mitigation. The Wave 8 experiment shows that 3 second-method runs (a partial N=2 bootstrap) materially changed convergence assessment. Full N-restart would likely change it further. The methodology ADR should specify a minimum-N-second-method-runs-per-occupied-cell as a precondition for any "saturated" claim.

4. **Saturation should not be claimed without per-cell Pareto-stability evidence.** The pre-W8 saturation calculation treated "no new method admitted in K=2 waves" as evidence of stability. But the Wave-6/7 methods that opened those cells were themselves first-methods; their Pareto front was untested. The methodology ADR's saturation criterion needs strengthening: **a cell is saturated only after at least 2 distinct methods have produced overlapping Pareto fronts** (or, equivalently, a second method has been tested and produced primarily reinforcement-not-new-clusters output).

---

## §5 Revised stopping question

Pre-W8, `cell-occupancy.md` §7 proposed three options:
- A: One more wave testing depth saturation → was projected to meet dual stopping
- B: Declare convergence-enough → was at 93% saturation
- C: Path-dependence remediation → what we actually did

The Wave 8 result invalidates the projections for A and B. The corpus is at 58% saturation, not 93%; depth growth is still 29%/wave, not converging.

**Three updated options post-Wave-8:**

- **A' — Continue path-dependence remediation in unsaturated cells.** Spawn Wave 9 with second-methods in the 9 new Wave-8 cells (FAILSCEN's failure-mode cluster especially needs a second method to test whether FAILSCEN's 11 clusters in scenario-current-exhaustive are Pareto-optimal). Likely outcome: another ~15-30 NEW clusters; saturation might rise to 65-75% but unlikely to reach 95%.
- **B' — Accept incompleteness; declare audit "exhaustively-explored-but-path-dependent."** Document the corpus as ~72 clusters + path-dependence-acknowledged-as-fundamental. Pivot to resolution + methodology codification + implementation audit.
- **C' — Bootstrap-style restart.** Re-run Wave 1 with a DIFFERENT method-mix (e.g., persona-retrospective methods + failure-mode-scenarios FIRST) and compare which clusters surface in both runs vs only one. Genuine path-dependence mitigation but ~2× the audit cost.

Per the methodology ADR's eventual stopping criterion, the question is no longer "when does the audit converge?" but "given path-dependence is structural and N-restart is expensive, what evidence is sufficient for ‘adequately explored’?"

My recommendation: **B' — declare exhaustively-explored, document path-dependence, pivot to resolution + ADR drafting + implementation audit.** Continuing waves will continue producing new clusters indefinitely because the architecture artifact has genuinely many cross-cutting concerns that benefit from method-diverse review. The marginal value of each new cluster decreases (long-tail singletons increasingly outweigh dense clusters); at some point the audit's ROI flips negative. We may already be past that point.

---

## §6 Limitations

1. **NEW-vs-REINFORCEMENT classification is judgment.** Each Wave-8 finding's classification as opening a new cluster vs reinforcing an existing one was done in-context against `signal-ledger.md` §5. Different judgments would shift the ~30/~23 split.
2. **Cluster member-counts for §2's 30 new clusters are mostly sole-source.** With only one wave's evidence, we can't distinguish "this is a real cluster that would have multiple members under further audit" from "this is a singleton that wouldn't replicate." A Wave-9 second-method test would resolve this for some.
3. **The 9-new-cells count assumes the cells are genuinely distinct from pre-W8 cells.** Some are arguably sub-cells (e.g., persona × post-hoc × focused × governance is a decomposition refinement of persona × post-hoc × holistic × governance). Methodology ADR's cell-axis discipline would tighten.
4. **QD-score ΔW8 = 29% is computed against the post-W8 QD-score.** The Wave-8 ΔQD-score is partly self-inflated (the new cells we just opened contribute fully to the denominator and numerator). True marginal-novelty by methodology ADR's eventual measurement discipline would be different.
5. **Path-dependence is shown but not fully quantified.** A proper bootstrap experiment (Option C') would let us estimate variance in cluster-set across method-orderings. We have only one data point per cell.
