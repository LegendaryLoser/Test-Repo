# Methodology research note: dual metrics, the coverage tautology, path-dependence, and audit-type variance

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative. Input to the methodology codification ADR (queued; no ID allocated). <!-- spec-lint: allow prose-xref-banned -->

**Companion documents:**
- [`qd-triage.md`](qd-triage.md) — Quality-Diversity triage framework currently in use (cells, σ × κ, ACGR)
- [`signal-ledger.md`](signal-ledger.md) — empirical finding triage (867 findings → 42 dense clusters)
- [`corrections.md`](corrections.md) — META- audit-of-the-audit corrections
- [`consolidated.md`](consolidated.md) — thematic clustering of findings

**Purpose.** Document three methodological critiques of the current QD framework that emerged during user-driven analysis on 2026-05-17, cite the relevant research, and propose a saturation-based reformulation that addresses them. This note is the empirical + theoretical foundation for the revised scope of TASK-0050 (cell finalization) and for the methodology codification ADR.

---

## §1 The original framework and where it came from

[`qd-triage.md`](qd-triage.md) §1 grounds the existing framework in three converging literatures:

1. **Quality-Diversity optimization** — MAP-Elites (Mouret & Clune 2015), MOME (Pierrot et al. 2022), Stock (2025) *WIREs Computational Statistics*. Behaviour-space + per-cell admission; coverage as primary metric.
2. **Ensemble diversity theory** — Krogh & Vedelsby (1994) ambiguity decomposition; Chandra & Chen (2006) accuracy-diversity trade-off. Diversity reduces error iff individual competence preserved.
3. **LLM-as-judge ensemble research** — Mixture-of-Agents (Wang et al. 2024); Self-MoA / Mixture-of-Complementary-Agents (Wang et al. 2025, NeurIPS 2025). κ as marginal complementarity score.

The current framework adopts:
- **Behaviour space:** 4 axes (Lens × Temporal × Decomposition × Severity)
- **Per-method scoring:** σ (signal rate) × κ (marginal complementarity)
- **Admission rule:** σ ≥ 0.30 floor + (κ > 0 OR Pareto-best-in-cell)
- **Convergence metric:** ACGR (Archive Coverage Growth Rate) < 5% for two consecutive waves

Per the user's dual-metric proposal (this session), the natural extension is to add a **depth metric (QD-score)** alongside the existing **breadth metric (coverage)**, restoring the canonical QD dual.

---

## §2 Three structural critiques

The user's three critiques expose problems that aren't addressed by the existing framework or by a naive dual-metric extension.

### §2.1 Critique 1: the coverage tautology

**Claim.** If cells are defined post-hoc from observed clusters, coverage is tautologically 100% — every cell we identified has ≥1 cluster, by construction.

**Verification against our corpus.** `qd-triage.md` §11 ("Limitations") explicitly acknowledges: "Behavioural axes are post-hoc — chosen by inspection during this triage." The ~55 meaningful-cells estimate is itself post-hoc judgment about which cartesian-product combinations are "real." Under any reasonable post-hoc denominator, observed coverage approaches 100%.

Three candidate denominators, each problematic:
| Denominator | Coverage | Problem |
|---|---|---|
| |observed_cells| | ~100% | Tautological |
| |empirically estimated meaningful| = ~55 | ~40-65% | Circular (estimate used the observations) |
| |theoretical cartesian product| = 360 (6 × 3 × 4 × 5) | ~6-9% | Meaningless (most cells are structurally degenerate, e.g., `(compression × forward-looking × exhaustive × narrative)`) |

**Research basis for the critique.** Mouret & Clune (2015) §3.2 specify that MAP-Elites requires the behaviour space be **pre-defined from theory before the algorithm runs.** Their robot-locomotion example uses `(forward-velocity-binned-to-10-buckets × turning-radius-binned-to-10-buckets)` = 100 cells fixed a priori; coverage measures how many of those 100 pre-defined cells the algorithm filled. Cully & Demiris (2018) §4.1 explicitly identify behaviour-descriptor choice as "the hardest single design decision in QD" and note that post-hoc selection produces non-falsifiable coverage claims.

**Mitigations available in literature:**
- **Pre-defined cells from theory** (canonical MAP-Elites). Requires authoring an a-priori cell taxonomy before any sampling. Hard for audit problems where the relevant axes only become visible after seeing some findings.
- **Saturation in place of coverage** — drop the |meaningful| denominator entirely. Measure per-cell saturation: each observed cell stops contributing when no new method adds to its Pareto front. Audit terminates when all observed cells saturate. This is the approach taken by novelty-search lineage (Lehman & Stanley 2008 onward) when the search space is open-ended.
- **Behaviour-descriptor sensitivity analysis** (Cully 2018 §6) — author multiple plausible cell taxonomies and check whether convergence results are robust across them. Methodologically clean; expensive.

### §2.2 Critique 2: ordering bias / path dependence

**Claim.** The identification of "load-bearing cells" depends on which methods we ran in which order. A different wave sequence would have produced a different cell map, and therefore a different adaptive-depth allocation.

**Verification against our corpus.** Wave 1 chose adversarial-general methods (ARCH/IND/ADVO/ADVS/ADVH) which dominated attitudinal-current cells with 5 streams. Per `signal-ledger.md` §5, **25 of the 42 dense clusters first surfaced in Wave 1**, and the majority of those are attitudinal-current. Had Wave 1 instead used persona-scenario methods (PARTY/STAKE-equivalent first), different clusters would have anchored, and our perception of "load-bearing cells" would skew differently. The 42 clusters are a property of `(architecture-artifact + method-sequence + clustering-judgment)`, not of the artifact alone.

**Research basis for the critique.** Mouret & Clune (2015) §5.1 explicitly flag initial-population sensitivity as a MAP-Elites weakness; they recommend large initial populations + many generations to dilute the effect, but acknowledge full path-independence is unachievable. Lehman & Stanley (2011) *"Abandoning Objectives"* discusses novelty-search path-dependence in detail: the order in which novelty is rewarded determines the structure of the eventually-discovered behaviour-space. In our audit, "novelty" maps to "first-surfacing-stream" and the path-dependence is direct.

**Mitigations available in literature:**
- **Random restart with method-set bootstrap.** Run the audit N times with different initial method orderings; cells appearing in all N runs are robust; cells unique to one ordering are bias-attributable. Standard practice in evolutionary-computation reproducibility studies (e.g., Cully 2018 §5 reports N=20 restarts as typical). Expensive: N× audit cost.
- **Counterfactual replay.** For each finding, estimate whether it would have been surfaced under alternative method-sequences. Hard to do rigorously; usually requires a separate Monte Carlo simulation.
- **Explicit acknowledgment + method-sequence documentation.** Treat the cell map as "the cell map that emerged from THIS sequence on THIS artifact." Don't claim universality. Most pragmatic; relies on transparency rather than mitigation.
- **Bayesian-prior cell weighting.** Down-weight cells whose discovery depended on Wave-1 method-choice. Adds judgment-load and propagates assumptions.

For our audit, **explicit acknowledgment + method-sequence documentation** is the realistic mitigation. The 42 clusters are method-sequence-dependent; the methodology codification ADR should say so. <!-- spec-lint: allow prose-xref-banned -->

### §2.3 Critique 3: criticality varies by audit/artifact type

**Claim.** The 4-axis framework — and especially Axis D (Severity bias) — was designed for THIS architecture audit. Different audit types weight different cells as "high-importance"; the framework cannot be applied universally without per-audit-type re-specification.

**Verification.** Axis D's high-importance values are `{blocking-impl, governance, security/ops}` per `qd-triage.md` §2.5 and §7.3. These priorities are architecture-audit-specific. For other audit types:

| Audit type | Likely Axis D priorities |
|---|---|
| Architecture audit (this) | blocking-impl, governance, security/ops |
| Implementation audit (queued) | correctness, performance, security |
| UX / product audit | usability, accessibility, brand-consistency |
| Data audit | accuracy, freshness, privacy, lineage |
| Documentation audit | discoverability, completeness, audience-fit |
| Security-only audit | exploitability, blast-radius, detectability |

Other axes also vary: an implementation audit might collapse Axis C (Decomp) because code-review decomposition styles vary less than spec-review styles; a data audit might split Axis B (Temporal) into point-in-time vs longitudinal vs streaming.

**Research basis for the critique.** Stock (2025) §3.4 explicitly notes "the behaviour descriptor is the most important design choice in Quality-Diversity; it determines what diversity means for the problem." MAP-Elites for locomotion uses `(forward-vel × turning-radius)`; MAP-Elites for soft-robot morphology uses `(limb-count × symmetry-axis)`; MAP-Elites for music generation uses `(rhythmic-complexity × harmonic-novelty)`. The algorithm is domain-general; the behaviour space is domain-specific. Treating them as separable concerns is the discipline that makes QD applicable across domains.

**Mitigation in literature.** **Two-layer specification:** a domain-general algorithm (MAP-Elites mechanism, coverage + QD-score dual, admission rules) plus a domain-specific behaviour-descriptor (the cell axes + criticality assignment). Each new domain authors its own behaviour-descriptor; the algorithm doesn't change.

For our framework this means the methodology codification ADR needs two clearly-separated layers, not a single conflated specification.

---

## §3 The saturation-based reformulation

The three critiques together do **not** sink the dual-metric philosophy — they constrain what each metric can claim and push the framework toward a saturation-based reformulation that QD literature already favors for open-ended-behaviour-space problems.

### §3.1 Replace coverage with saturation

Rather than `coverage = occupied / meaningful` (tautological in our setup), use:

```
cell_saturated(c) iff
    no new method admitted to cell c in last K consecutive waves
  AND
    no new theme opened in cell c in last K consecutive waves
  AND
    Pareto front of (σ, κ) within cell c stable in last K consecutive waves
```

Saturation operates within observed cells only, so:
- No tautology (saturation isn't `observed / observed`)
- No |meaningful| denominator needed
- Path-dependence still present (a different ordering would saturate different cells) but at least the metric is well-defined for the cells we did observe

Audit-level saturation = % of observed cells that have saturated.

### §3.2 Keep QD-score as the depth metric

`QD-score = Σ (per-cell max σ × κ)` summed across observed cells, per Pugh, Soros, Stanley (2016). Or for MOME: `Σ (per-cell hypervolume of (σ, κ) Pareto front)` per Pierrot et al. (2022). Either definition works; choose based on whether we want a scalar elite per cell or a Pareto-front per cell.

QD-score has terminal state because per-cell hypervolume is bounded above by the (σ, κ) Pareto frontier achievable across all methods; once that frontier is found, additional methods can't increase it.

### §3.3 Dual stopping condition

```
audit_terminates iff
    audit_saturation ≥ 0.95             # 95% of observed cells saturated
  AND
    ΔQD-score / QD-score < 0.05         # depth growth below 5%/wave
  for two consecutive waves
```

Both signals operate within observed cells; both have terminal states; neither has the tautology or circular-denominator problems.

### §3.4 Adaptive depth on load-bearing cells (with path-dependence acknowledgment)

Load-bearing cells = cells containing dense clusters (≥3 cluster-members per `signal-ledger.md` §5). Adaptive depth means:
- Allocate Wave-N+1 method budget preferentially to load-bearing cells whose Pareto front is still expanding
- Stop allocating to load-bearing cells that have saturated
- Acknowledge in the methodology ADR that "load-bearing" is path-dependent: the cells identified as load-bearing depend on which methods discovered them first

This is the **Multi-Objective MAP-Elites with quality-driven niching** pattern (Janmohamed et al. 2024). Our adaptive-depth rule weights by observed cluster-density; the methodology ADR documents the path-dependence as a known limitation.

---

## §4 Two-layer framework specification

Following the Stock (2025) and MAP-Elites domain-general / domain-specific separation, the methodology codification ADR should specify TWO layers:

### Layer 1 (domain-general, audit-type-independent)

The algorithm and metrics that apply to any audit type:

1. **Behaviour space:** a cartesian product of N orthogonal behavioural axes (audit-type chooses the axes).
2. **Methods:** units of analysis (LLM stream + prompt; or human reviewer + checklist) that occupy cells with σ × κ scores.
3. **Per-cell admission:** Pareto-front of methods on (σ, κ); σ floor for individual competence.
4. **Per-cell saturation:** no new methods, no new themes, no new Pareto points in K waves.
5. **QD-score:** sum of per-cell hypervolume (or per-cell max σ × κ for scalar formulation).
6. **Dual stopping:** audit_saturation ≥ T_sat AND ΔQD-score < T_depth for K consecutive waves.
7. **Adaptive depth allocation:** budget weighted by per-cell cluster-density (or other criticality signal).
8. **Path-dependence note required:** every audit run documents its method-sequence and acknowledges cell-map dependence.

### Layer 2 (architecture-audit instance)

The specific behavioural axes + criticality assignment for THIS audit type:

1. **Axes:** Lens (6 cells) × Temporal (3) × Decomposition (4) × Severity bias (5) = 360 theoretical cells.
2. **Cell-admissibility filter:** authored a-priori list of which cartesian-product combinations are non-degenerate (estimated ~30-50 admissible cells; needs explicit pinning before next audit).
3. **Axis-D criticality (audit-type-specific):** `{blocking-impl, governance, security/ops}` high-importance > `{narrative-clarity, cost/value}` lower-importance.
4. **Initial method catalog:** Tier A/B per `qd-triage.md` §5.
5. **Path-dependence specifics:** this run started with Wave-1 adversarial-general dominant; documented in `signal-ledger.md` §6.

Implementation audit, UX audit, data audit, etc. would each be Layer-2 instances with their own axes and criticality.

---

## §5 Implications for TASK-0050 revised scope

Original TASK-0050 (preview in `signal-ledger.md` §6) was "cell-label + prune for coverage measurement." Revised scope addresses the three critiques:

1. **Cluster-to-cell labeling** — still useful (gives per-cell cluster density for adaptive depth).
2. **Saturation measurement per observed cell** — for each cell that has ≥1 cluster, has the Pareto front stabilized in recent waves? Output: per-cell saturation status table.
3. **QD-score baseline** — sum of per-cell max(σ × κ). Output: scalar baseline + per-cell contribution breakdown.
4. **Path-dependence inventory** — which 25-of-42 clusters were Wave-1-attitudinal-dominated? Which cells would different ordering have surfaced? Output: best-effort counterfactual table flagging cells with high method-sequence dependence.
5. **Drop coverage metric.** Replace with audit_saturation = % of observed cells saturated. Compute current value.
6. **Document Layer 1 / Layer 2 split** in `qd-triage.md` — clearly separate the domain-general framework from the architecture-audit instance. Set up the methodology codification ADR's structural skeleton.

Note: TASK-0050 does NOT attempt to pre-author a theoretical cell taxonomy from first principles. That's a deeper methodology shift and is out of scope; if pursued it would be a separate TASK or part of the methodology codification ADR's drafting.

---

## §6 Open questions remaining

The three critiques expose problems the saturation-based reformulation addresses, but several deeper questions remain unresolved:

1. **Behaviour-descriptor universality.** Even after the Layer 1/2 split, the question "what makes a good cell taxonomy for audit type X" remains. Cully (2018) §4.1 calls this "the hardest single design decision" — we have no general answer.
2. **Adaptive-depth fairness.** Concentrating depth on load-bearing cells means under-investing in lightly-occupied cells that might contain rare-but-important defects. The Multi-Objective MAP-Elites literature doesn't fully resolve this; it's an active research area.
3. **Method-sequence randomization cost.** Mitigating path-dependence via N restarts is N× expensive; for human-driven audits this is rarely affordable. Cheaper mitigations (counterfactual replay, Bayesian priors) introduce judgment-load.
4. **Inter-audit composability.** If implementation audit Layer 2 has different axes than architecture audit Layer 2, can the two corpora be jointly consolidated? This affects the user-direction "consolidate jointly post-both-audits" decision (STATUS.md 2026-05-17 Recent decisions).
5. **Saturation-criterion K choice.** "No change for K consecutive waves" — what K? K=2 is the original `qd-triage.md` §2.6 default. K=3 is more conservative. K=1 risks false-positive saturation on quiet waves. No principled basis for the choice yet.

These belong in the methodology codification ADR's "Limitations and open questions" section. <!-- spec-lint: allow prose-xref-banned -->

---

## §7 References

- **Cully, A. & Demiris, Y. (2018).** *"Quality and Diversity Optimization: A Unifying Modular Framework."* IEEE Transactions on Evolutionary Computation 22(2): 245-259. Modular framework for QD; behaviour-descriptor selection as the hardest design choice.
- **Janmohamed, H., Bossens, D. et al. (2024).** *"Multi-Objective MAP-Elites with Quality-Driven Niching."* GECCO 2024. Adaptive depth allocation in MOME.
- **Krogh, A. & Vedelsby, J. (1994).** *"Neural Network Ensembles, Cross Validation, and Active Learning."* NeurIPS 1994. Ambiguity decomposition: diversity reduces ensemble error iff individual competence preserved.
- **Lehman, J. & Stanley, K. O. (2008, 2011).** *"Abandoning Objectives: Evolution through the Search for Novelty Alone."* Evolutionary Computation. Novelty-search lineage; path-dependence in open-ended behaviour spaces.
- **Mouret, J.-B. & Clune, J. (2015).** *"Illuminating Search Spaces by Mapping Elites."* arXiv 1504.04909. Original MAP-Elites; pre-defined behaviour space; initial-population sensitivity.
- **Pierrot, T., Macé, V., Chalumeau, F. et al. (2022).** *"Multi-Objective Quality Diversity Optimization."* GECCO 2022. MOME: per-cell Pareto fronts; QD-score as sum of hypervolumes.
- **Pugh, J. K., Soros, L. B., Stanley, K. O. (2016).** *"Quality Diversity: A New Frontier for Evolutionary Computation."* Frontiers in Robotics & AI. First formalization of coverage + QD-score as the canonical QD dual.
- **Stock, W. (2025).** *"Quality-Diversity Optimization: A Review."* WIREs Computational Statistics. Surveys QD across domains; emphasizes behaviour-descriptor as the domain-specific design choice.
- **Wang, J., Wang, J., Athiwaratkun, B. et al. (2024).** *"Mixture-of-Agents Enhances Large Language Model Capabilities."* arXiv 2406.04692.
- **Wang, J. et al. (2025).** *"Rethinking Mixture-of-Agents: Is Mixing Different LLMs Beneficial?"* arXiv 2502.00674. Self-MoA negative result.
- **NeurIPS 2025.** *"Mixture of Complementary Agents."* Complementarity-based admission rule (κ score).
- ~~arXiv 2602.09341~~ *"Auditing Multi-Agent LLM Reasoning Trees..."* — citation flagged by `corrections.md` META-PROC-002 as anonymous-authority hazard; the META- meta-audit method drew on it. Verify before relying on this citation in the methodology codification ADR. <!-- spec-lint: allow prose-xref-banned -->
