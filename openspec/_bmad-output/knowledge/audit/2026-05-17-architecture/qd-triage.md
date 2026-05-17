# Quality-Diversity Triage Report — 2026-05-17 Architecture Audit

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative methodology analysis. Input to the methodology codification ADR (queued; see STATUS.md "Recent decisions" row "Codify audit methodology in ADR after BOTH architecture + implementation audits complete").

**Companion documents:**
- [`README.md`](README.md) — audit session metadata + method
- [`consolidated.md`](consolidated.md) — thematic findings (~70 themes; Wave-5 themes pending consolidation)
- [`findings-index.md`](findings-index.md) — per-stream provenance ledger (40 streams as of Wave 5)
- [`corrections.md`](corrections.md) — Wave-5 META- audit corrections against this triage and consolidated.md (19 corrections: 4 CRIT / 12 SER / 3 PROC). Read alongside the σ × κ rows in §3 below; in particular, **PROSE-Wave-1 κ-source-of-THEME-P attribution is incorrect** (META-CRIT-001), **STAKE raw-finding count is 20 not ~25** (META-CRIT-004), **PAIGE κ count is 2 sole + 1 co-surfaced not 3 sole** (META-SER-011), and **`(attitudinal × current-state)` over-saturation count of 12 double-counts cells** (META-SER-008). Inline §3 row text below is preserved as the historical scoring; see corrections.md for the authoritative re-statements pending the §3.5 re-issue.

**Purpose:** Re-frame the 36-stream / ~700-finding / ~70-theme audit corpus through a Quality-Diversity (QD) lens. Produces:

1. Per-method σ (signal rate) × κ (marginal complementarity) scores
2. QD matrix occupancy across four behavioral axes
3. Tier A / B / C / D catalog assignment per method
4. Empty-cell map (Wave 5 admission targets)
5. Re-measurement of convergence under Archive Coverage Growth Rate (ACGR)
6. Concrete clauses for the methodology codification ADR

**Why this document exists.** The Wave 4 supplement (commit `8a9f7ee`) surfaced an empirical finding that destabilises COMPOSITE-V2 Gate 6 as currently defined: marginal novelty is dominated by methodology variance, not model variance. STAKE + COUNTER (two new methods) spiked novelty back to ~46% after Wave 3 had reached ~30-37%. Under the as-stated rule ("<10% marginal novelty"), Gate 6 is structurally unachievable because new methods can always be invented. This forces a choice: (a) freeze the methodology catalog and define convergence relative to it (the consolidated.md "Methodology insight" recommendation), or (b) replace the convergence metric with one that is invariant to method admission. This triage adopts (b), grounded in published Quality-Diversity research (Mouret & Clune 2015, Pierrot et al. 2022, Stock 2025 *WIREs Computational Statistics*) and ensemble complementarity research (Krogh & Vedelsby 1994, Wang et al. 2024 *Mixture-of-Agents*, NeurIPS 2025 *Mixture of Complementary Agents*). The QD framework satisfies the user's "if new methods provide signal, not pursuing them would betray the spirit" constraint while still producing a defensible stopping rule.

---

## 1. Research basis

The framework draws on three converging literatures.

### 1.1 Quality-Diversity optimisation (evolutionary computation)

- **MAP-Elites** (Mouret & Clune 2015; Stock 2025 *WIREs Computational Statistics*). Constructs an archive of diverse high-performing solutions across a user-defined feature space. Core admission rule: a new solution enters the archive iff its cell is empty OR it outperforms the current cell occupant. **The admission criterion is about behaviour-space coverage, not absolute fitness.** A low-fitness solution in an empty cell adds more ensemble value than a high-fitness solution in an occupied cell.
- **Multi-Objective MAP-Elites (MOME)** (Pierrot et al. 2022). Each cell can hold a Pareto front over multiple objectives, not a single elite. Translates directly to our setting: each methodology cell can hold multiple methods if they trade off differently across σ / κ / cost.
- **JEDi — Quality with Just Enough Diversity** (recent QD literature). Focuses evaluations on solutions that matter, downweighting diversity-for-diversity's-sake. Confirms the "diversity is not unconditionally good" finding from the ensemble-learning side.

### 1.2 Ensemble diversity theory (machine learning)

- **Ambiguity decomposition** (Krogh & Vedelsby 1994; generalised in Brown et al. 2005). For regression ensembles: `ensemble_error = average_individual_error − ambiguity`. Diversity reduces ensemble error iff individual competence is preserved. **Strongest theoretical justification for valuing diversity in audit ensembles.**
- **Diversity-accuracy trade-off** (Chandra & Chen 2006 and successors). Diversity is not free; pushing diversity past a point degrades individual quality and net ensemble performance suffers. Implication: there exists an admissible competence floor below which a diverse method is net-negative.

### 1.3 LLM-as-judge ensemble research (recent)

- **Mixture-of-Agents (MoA)** (Wang et al. 2024, arXiv 2406.04692). Layered ensembles outperform individual frontier models. Identifies the "collaborativeness" phenomenon: LLMs generate better responses when shown other models' outputs.
- **Self-MoA / Rethinking MoA** (Wang et al. 2025, arXiv 2502.00674). **A critical negative result:** mixing weaker LLMs *degrades* ensemble quality vs. self-ensembling the strongest single model. Confirms the noise concern in the original "≥50% signal rate" gate proposal — but reframes it: noise comes from *incompetent* diverse methods, not from diversity itself.
- **Mixture of Complementary Agents** (NeurIPS 2025). Introduces a principled framework for proposer selection built on **complementarity** rather than individual quality. Greedy complementarity selection beats individual-fitness selection. **This is the strongest single research signal against the "≥X individual signal rate" admission rule.**
- **Multi-Agent Debate with Adaptive Stability Detection** (ICLR 2025); **Diverse-MAD / Breaking Mental Set** (EMNLP 2024). Premature convergence is a documented pathology of homogeneous LLM ensembles. Explicit confidence expression + heterogeneous foundation models + anti-conformity weighting mitigate it. Strongest agent's individual performance upper-bounds team performance — debate cannot elevate beyond that ceiling.
- **Auditing Multi-Agent LLM Reasoning Trees Outperforms Majority Vote and LLM-as-Judge** (2026 arXiv 2602.09341). Auditing the *reasoning trees* of an ensemble beats voting on its outputs. Relevant as a Wave-5 method candidate (meta-review stream that reviews other streams' findings for soundness).

### 1.4 Synthesis applied to this audit

The right admission criterion for adding a new review method to our audit catalog is **not** "does the method's individual signal rate exceed threshold X." It is:

> Does the method expand the QD archive of audit findings while maintaining individual competence above the ambiguity-decomposition competence floor?

This decomposes into two scores per method:

- **σ (sigma) = individual signal rate** — the fraction of the method's raw findings that pass a signal filter (concreteness + actionability + non-method-artifact). Methods below the competence floor (estimated ~30%) are *dropped* per the Self-MoA finding: their noise overwhelms their diversity contribution.
- **κ (kappa) = marginal complementarity** — the increase in archive coverage when the method is added to the ensemble vs the ensemble without it. Computed via greedy ablation per Mixture-of-Complementary-Agents.

A method is **admitted** if it sits on the σ × κ Pareto frontier for its cell. Methods strictly dominated on both axes by an incumbent are deprecated.

---

## 2. QD framework definitions

### 2.1 Behaviour space — four axes

Each method occupies one cell across four orthogonal axes. Axes were chosen post-hoc by inspecting the 36-stream corpus for dimensions of variation that demonstrably differentiate outputs (theme-overlap matrix examination during this triage). A formal validation of axis orthogonality is deferred to the methodology ADR.

| Axis | Cells | Operational meaning |
|---|---|---|
| **A. Lens orientation** | attitudinal · structural · scenario · persona · contrarian · compression | What stance the method takes toward the artifact |
| **B. Temporal scope** | current-state · post-hoc (retrospective) · forward-looking (pre-mortem / hypothetical) | When the reviewed state is assumed to live |
| **C. Decomposition style** | holistic · exhaustive (branch-walk) · focused (highest-impact) · derivative (from-alternatives) | How the method partitions the artifact for review |
| **D. Severity / dimension bias** | blocking-impl · governance · security/ops · narrative-clarity · cost/value | Which class of defect the method is most likely to surface |

Theoretical cell count: 6 × 3 × 4 × 5 = **360 cells**. Most are not meaningful (e.g., `(compression, forward-looking, exhaustive, security/ops)` is a degenerate combination). Estimated count of meaningful cells from corpus inspection: **~50-60**. Currently occupied: **~22**. This is the QD-archive denominator for ACGR.

### 2.2 σ — individual signal rate

```
σ(M) = |{ findings from M that pass the signal filter }| / |{ raw findings from M }|
```

**Signal filter** is a three-clause AND:

- **Concreteness** — finding identifies a specific artifact (file, section, REQ, gate, hook, ADR) rather than a vague concern.
- **Actionability** — finding maps to a tractable CHG / ADR amendment / code change. "PHASE-5 is structurally unreachable" passes (maps to CHG-AA); "this is a weird design" fails.
- **Non-method-artifact** — finding is not an artifact of the method's own framing. The 1 finding flagged in FIRST- (first-principles deconstruction loop that found itself) is the canonical fail.

**Competence floor:** σ ≥ 0.30 per Self-MoA / ambiguity-decomposition. Methods below this are net-negative additions and are dropped (Tier D).

This triage estimates σ per method by counting findings that ended up in named themes (consolidated.md). It is **not** measured by re-running the signal filter against each raw finding — that level of rigor is deferred to the methodology ADR's red-test phase. Reported σ values carry an uncertainty band of ±10 percentage points.

### 2.3 κ — marginal complementarity

Greedy ablation, per Mixture-of-Complementary-Agents (NeurIPS 2025):

```
κ(M | E) = ArchiveCoverage(E ∪ {M}) − ArchiveCoverage(E)
```

where `E` is the rest of the ensemble (the other 35 streams) and `ArchiveCoverage` counts distinct (cell, theme) pairs.

For this triage, κ is approximated by: **count of themes for which M is the sole or first-surfacing stream**. A method that only confirms themes already surfaced by others has κ ≈ 0; a method that surfaces 10 themes no other method touched has κ ≈ 10.

This is a strictly weaker estimator than full greedy ablation (which would handle multi-way overlap rigorously), but it is computable from the existing findings-index without re-running streams. Full greedy ablation is deferred to the methodology ADR's measurement-discipline section.

### 2.4 σ × κ Pareto admission

Per cell `c`, the set of admitted methods is the Pareto frontier over `(σ, κ)`:

```
admitted(c) = { M ∈ methods(c) : ¬∃ M' ∈ methods(c) with σ(M') ≥ σ(M) ∧ κ(M') ≥ κ(M) ∧ (M' ≠ M) }
```

If `|admitted(c)| > 1`, all admitted methods may run (MOME — Pareto front per cell). If only one method occupies a cell, it is automatically admitted (provided σ ≥ floor).

### 2.5 Tier assignment

| Tier | Rule | Disposition |
|---|---|---|
| **A — Core** | σ ≥ 0.60 AND κ ≥ 3 (cell-rare) — high quality AND high coverage contribution | Run on every audit |
| **A — Core** (alt) | σ ≥ 0.60 AND occupies a high-importance cell (Axis D ∈ {blocking-impl, security/ops}) AND is best-in-cell | Run on every audit |
| **B — Complementary** | σ ≥ 0.40 AND κ ≥ 3 (high marginal coverage despite moderate quality) | Run when budget allows; mandatory if any Axis-A / Axis-D combination would otherwise be empty |
| **C — Experimental** | σ unmeasured (new method) OR small-N data | Run with confirmation pairing (one Tier-A method covering the same cell) until reclassifiable |
| **D — Deprecated** | σ < 0.30 (competence floor) OR (κ < 1 AND already covered by Tier-A in same cell) | Removed from catalog; documented in methodology ADR amendment log |

### 2.6 ACGR — Archive Coverage Growth Rate (convergence metric)

```
archive(W) = { (cell, theme) : at least one method in waves 1..W surfaced theme in cell }
ACGR(W)    = | archive(W) − archive(W-1) | / | meaningful_cells |
```

**Convergence criteria (all three must hold):**

1. `ACGR < 0.05` for two consecutive waves;
2. `≥ 80% of high-importance cells` (Axis D ∈ {blocking-impl, governance, security/ops}) are occupied by ≥ 1 method;
3. Every Axis-A × Axis-C combination admitted into the catalog has at least one Tier-A occupant.

**Why this is invariant to method admission.** Adding a new method either lands its findings in already-archived (cell, theme) pairs (no archive growth, ACGR unaffected by admission), or it surfaces a new (cell, theme) pair — in which case the archive denominator grows by the same magnitude as the numerator, and ACGR tends to a fixed ceiling determined by `|meaningful_cells|`. The naïve marginal-novelty metric instead spikes whenever a new method is added; ACGR does not.

---

## 3. Per-method scoring — all 36 streams

Findings counts from [findings-index.md](findings-index.md); per-method marginal-novelty estimates from [consolidated.md](consolidated.md) §Per-stream marginal novelty. σ estimated as (findings ending up in named themes) / (raw findings) with ±10pp uncertainty. κ counted as unique-theme-contributions; "shared" means co-surfaced with one other stream, "sole" means single-source.

### 3.1 Wave 1 — 12 streams

| # | Stream | Model | Method | QD signature (Lens, Temporal, Decomp, Severity) | Raw findings | σ (est.) | Themes contributed | κ (sole) | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `ARCH-` | opus | adversarial-general (in-context) | (attitudinal, current, holistic, blocking) | 31 | 0.85 | confirmed A-K, L, M, N, sole on L (paired) | 0 sole; high reinforcement | A |
| 2 | `IND-` | opus | adversarial-general (isolated #1) | (attitudinal, current, holistic, blocking) | 27 | 0.80 | confirmed A-K, M, P; THEME-Q reinforcement | 0 sole | A (paired w/ ARCH) |
| 3 | `ADVO-` | opus | adversarial-general (isolated #2) | (attitudinal, current, holistic, blocking) | 24 | 0.80 | confirmed A-K, Q; new EDGE-aligned findings | 0 sole | B (model-perm of ARCH) |
| 4 | `ADVS-` | sonnet | adversarial-general (isolated) | (attitudinal, current, holistic, blocking) | 19 | 0.75 | confirmed A-K, P (sole partial) | 0-1 sole | B (model-perm) |
| 5 | `ADVH-` | haiku | adversarial-general (isolated) | (attitudinal, current, holistic, blocking) | 15 | 0.65 | confirmed A-K, partial coverage; CRIT-12 sole on GAS-runtime cache | 1 sole (W) | B (low-cost model-perm) |
| 6 | `INHER-` | opus | inheritor framing (scenario) | (scenario, post-hoc, holistic, blocking) | 22 | 0.80 | confirmed A-K, sole/early on H (missing artifact types), strong on U | 2-3 sole-ish | **A** |
| 7 | `EDGE-` | opus | edge-case-hunter (exhaustive) | (attitudinal, current, exhaustive, blocking) | 44 | 0.85 | sole-surfacer of THEME-U (ID allocation races); most THEME-D findings; many concrete hook bugs | 4-5 sole | **A** |
| 8 | `READY-` | opus | check-impl-readiness (exhaustive) | (attitudinal, current, exhaustive, blocking) | 19 | 0.85 | confirmed A-K with implementability framing; flagged 6 BLOCKING findings as readiness-grade | 0-1 sole | A (paired w/ EDGE) |
| 9 | `STRUCT-` | opus | editorial-review-structure | (structural, current, holistic, narrative) | 15 | 0.70 | sole on THEME-N (summary-of-summaries drift); contributed to Y, M | 2 sole | **A** (only structural lens) |
| 10 | `PROSE-` | sonnet | editorial-review-prose | (structural, current, focused, narrative) | 14 | 0.65 | sole on P (paper citation), reinforced D, E | 1 sole | B |
| 11 | `PREM-` | opus | advanced-elicitation (pre-mortem) | (contrarian, forward, holistic, security/ops) | 18 | 0.70 | sole on X (append-only calcification); contributed to F, J, MM (PP partial) | 2 sole | **A** (only forward-looking lens until Wave 2 RED) |
| 12 | `PARTY-` | opus | party-mode (6-persona roundtable) | (persona, current, holistic, governance) | 22 | 0.70 | sole on V (UX gaps), reinforced K; PARTY-PROC-01 sole on PHASE-5 "build the cathedral" | 2-3 sole | **A** (only persona-aggregate lens) |

**Wave 1 tier summary:** 6 Tier A, 5 Tier B, 0 Tier C, 0 Tier D.

### 3.2 Wave 2 — 8 streams

| # | Stream | Model | Method | QD signature | Raw findings | σ (est.) | Themes contributed | κ (sole) | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 13 | `SOC-` | opus | advanced-elicitation socratic | (contrarian, current, focused, narrative) | 19 | 0.70 | mostly reinforcements of A-K and existing | 0 sole | C → B (confirmation-class) |
| 14 | `RED-` | opus | advanced-elicitation red-team | (contrarian, forward, exhaustive, security/ops) | 16 | 0.85 | **sole-surfacer of THEME-AA** (supply-chain / adversarial enforcement gap); contributed to CC, EE | **5 sole** | **A** (only adversarial-attacker lens) |
| 15 | `RETRO-` | opus | retrospective (hypothetical post-PHASE-5) | (scenario, post-hoc, holistic, governance) | 19 | 0.80 | **sole on BB, CC, DD, EE, FF, OO** | **6 sole** | **A** (only retrospective-from-future lens) |
| 16 | `VALID-` | opus | validate-prd | (attitudinal, current, exhaustive, governance) | 18 | 0.65 | confirmation-class; VALID-SERIOUS-15 reinforced AA | 0 sole | B (paired w/ READY) |
| 17 | `WIN-` | opus | persona (Winston / architect) self-critique | (persona, current, holistic, blocking) | 22 | 0.75 | **sole on HH, JJ** (BMAD upstream risks, test runner ownership) | 2 sole | **A** (architect-persona lens) |
| 18 | `DISTILL-` | sonnet | distillator (compression-driven) | (compression, current, derivative, narrative) | 15 | 0.55 | mostly reinforcements; uncovered drift via compression delta | 0-1 sole | B (**only compression lens**) |
| 19 | `FIRST-` | sonnet | advanced-elicitation first-principles | (contrarian, current, derivative, blocking) | 13 +1 artifact | 0.55 | **sole on II, KK, LL, NN; partial MM** | **4 sole** | **A** (only first-principles derivative lens) |
| 20 | `AME-` | sonnet | persona (Amelia / dev) implementability | (persona, current, holistic, blocking) | 20 | 0.75 | **sole on GG (hook ABI cluster)**; contributed to MM | 5 sole (GG cluster) | **A** (developer-persona lens) |

**Wave 2 tier summary:** 5 Tier A (RED, RETRO, WIN, FIRST, AME), 3 Tier B (SOC, VALID, DISTILL), 0 Tier C, 0 Tier D.

### 3.3 Wave 3 — 8 streams

| # | Stream | Model | Method | QD signature | Raw findings | σ (est.) | Themes contributed | κ (sole) | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 21 | `PM-` | opus | persona (John / product mgr) | (persona, current, holistic, cost/value) | 20 | 0.70 | **sole on entire THEME-RR cluster** (product workflow primitives) | **~10 sole** (RR sub-findings) | **A** (only product/cost-value lens) |
| 22 | `MARY-` | opus | persona (Mary / analyst) requirements | (persona, current, focused, blocking) | 22 | 0.65 | sole on WW (determinism vs idempotence); reinforced G, O | 1 sole | B (paired w/ READY semantically) |
| 23 | `SALLY-` | sonnet | persona (Sally / UX) 3-user-populations | (persona, current, focused, narrative) | 17 | 0.55 | reinforced V, ZZ partial; mostly confirmations | 0-1 sole | B → C (low κ; reconsider) |
| 24 | `PAIGE-` | sonnet | persona (Paige / tech writer) | (persona, current, focused, narrative) | 20 | 0.65 | **sole on SS, TT, ZZ** | 3 sole | **A** (only tech-writer/narrative-clarity lens) |
| 25 | `EDIT-` | opus | edit-prd defects | (structural, current, holistic, narrative) | ~17 unique | 0.55 | reinforced BB (supersession); few sole | 0-1 sole | C (paired w/ STRUCT; reconsider — possibly D) |
| 26 | `COURSE-` | opus | correct-course | (attitudinal, current, focused, blocking) | 12 | 0.60 | reinforced BB (supersession); largely confirmations | 0 sole | C → D (cell-redundant w/ checkpoint-preview AND validate-prd; high σ but κ ≈ 0) |
| 27 | `CHECK-` | opus | checkpoint-preview | (attitudinal, current, focused, blocking) | 16 | 0.65 | reinforced E (checkpoint interaction); 0 sole | 0 sole | C → D (cell-redundant; same as COURSE rationale) |
| 28 | `DEVIL-` | opus | advanced-elicitation devil's-advocate | (contrarian, current, derivative, governance) | 16 | 0.65 | **sole on UU, VV, XX, YY** (meta-critiques of architecture itself) | **4 sole** | **A** (only meta-critique-of-principles lens) |

**Wave 3 tier summary:** 2 Tier A (PM, PAIGE, DEVIL = 3 in fact — PM, PAIGE, DEVIL), 2 Tier B (MARY, SALLY), 3 Tier C/D (EDIT, COURSE, CHECK).

**Important Tier D candidates surfaced by Wave 3:** COURSE and CHECK both have high σ (~0.60-0.65) but κ ≈ 0 — they occupy a cell already saturated by ARCH/IND/ADVO and add no marginal coverage. Per Self-MoA logic these are net-zero in best case, net-negative in worst case (they add review cost without expanding archive coverage). **Recommendation: deprecate to Tier D.** EDIT- similar (cell-redundant with STRUCT-).

### 3.4 Wave 4 — 8 streams

| # | Stream | Model | Method | QD signature | Raw findings | σ (est.) | Themes contributed | κ (sole) | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 29 | `RED2-` | sonnet | red-team (model-perm of RED) | (contrarian, forward, exhaustive, security/ops) | ~15 | 0.75 | reinforced AA; new ~2 sub-findings in same cluster | 0-1 sole | B (model-perm of RED; admitted for cell density) |
| 30 | `RETRO2-` | sonnet | retrospective (model-perm of RETRO) | (scenario, post-hoc, holistic, governance) | ~15 | 0.75 | **sole on TTT, UUU, VVV** (agent identity, hook-failure taxonomy, model-version transition) | **3 sole** | **A** (sonnet finds different scenario gaps than opus) |
| 31 | `EDGE2-` | sonnet | edge-case-hunter (model-perm of EDGE) | (attitudinal, current, exhaustive, blocking) | ~25-30 | 0.75 | reinforced D, U; minor sole | 0-1 sole | B (model-perm of EDGE; **converged** — supports σ × κ Pareto theory) |
| 32 | `INHER2-` | sonnet | inheritor (model-perm of INHER) | (scenario, post-hoc, holistic, blocking) | ~10 | 0.70 | reinforced INHER themes only | 0 sole | B (**most converged** stream — 12% marginal novelty; supports tight-method admission discipline) |
| 33 | `VALID2-` | sonnet | validate-prd (model-perm of VALID) | (attitudinal, current, exhaustive, governance) | ~12 | 0.60 | confirmations + 1 tactical (shallow-clone CI defeating history walk) | 0-1 sole | C → D (cell-redundant w/ VALID; sonnet permutation adds little) |
| 34 | `PREM2-` | sonnet | pre-mortem (model-perm of PREM) | (contrarian, forward, holistic, security/ops) | ~10 | 0.65 | **sole on WWW, XXX** (CLAUDE.md contested authority, checkpoint off-by-one) | **2 sole** | **A** (sonnet pre-mortem found 2 themes opus PREM missed) |
| 35 | `STAKE-` | opus | **stakeholder-simulation (NEW)** | (persona, forward, exhaustive, security/ops + cost/value) | ~25 | 0.80 | **sole on THEMES AAA-JJJ (10 themes)** | **10 sole** | **A** (highest single-stream κ in entire corpus) |
| 36 | `COUNTER-` | opus | **counter-factual (NEW)** | (contrarian, current, derivative, all-axes) | ~20 | 0.75 | **sole on THEMES KKK-SSS (9 themes)** | **9 sole** | **A** (second-highest single-stream κ; cell-axis-spanning) |

**Wave 4 tier summary:** 4 Tier A (RETRO2, PREM2, STAKE, COUNTER), 3 Tier B (RED2, EDGE2, INHER2), 1 Tier D candidate (VALID2).

### 3.5 Wave 5 — 4 streams (QD admission rule applied)

Wave 5 was the first wave admitted under the σ × κ Pareto admission rule: cells targeted are the 4 high-importance empty cells from §7.3 + the candidate 5th axis (meta). σ values for Wave-5 streams are estimated against the new architecture themes opened (consolidated.md "Wave 5 supplement" § new themes). META- σ is computed differently: signal = corpus-correction findings that verifiably hold against the cited artifacts (high; 16 of 19 confirmed on spot-check during TASK-0043).

| # | Stream | Model | Method | QD signature (Lens, Temporal, Decomp, Severity) | Raw findings | σ (est.) | Themes contributed | κ (sole / co) | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 37 | `GOV-` | opus | validate-prd governance-focused | (attitudinal, current, focused, governance) | 22 | 0.80 | sole on YYY-EEEE (7 new); reinforced ~12 existing | **7 sole** | **A** (only attitudinal-governance-focused method) |
| 38 | `SEC-` | opus | persona security-engineer holistic | (persona, current, holistic, security/ops) | 21 | 0.85 | sole on FFFF-OOOO (10 new security-architectural-primitive themes); reinforced AA/AAA/BBB/CCC/EEE/III/TTT | **10 sole** | **A** (only security-engineer-current-state-holistic method; highest-κ Wave-5 stream) |
| 39 | `GOVDEV-` | opus | advanced-elicitation devil's-advocate (governance-focused) | (contrarian, current, focused, governance) | 22 | 0.80 | sole on PPPP-WWWW (8 new governance/contrarian themes); reinforced THEME-L cluster + DDD/M/MM | **8 sole** | **A** (only contrarian-governance-focused method) |
| 40 | `META-` | opus | reasoning-tree meta-audit | (meta × * × * × *) — candidate 5th axis | 19 | 0.84 | N/A (corrections, not architecture themes); 16/19 spot-verified | (audits the audit; orthogonal to architecture κ) | **A** (only meta-axis method; first wave to invoke 5th axis) |

**Wave 5 tier summary:** **4 Tier A, 0 Tier B, 0 Tier C, 0 Tier D.** All four streams cleared the σ ≥ 0.30 floor with margin AND opened previously-empty cells AND surfaced sole themes (or sole corrections for META-). The 4-for-4 Tier-A admission is consistent with the QD admission rule: when cells are deliberately targeted to fill empty regions of the behavioural map, individual κ is high almost by construction.

**Notes carried forward to §4 and §7:**
- META- is the first stream to invoke a 5th axis. Per §2.1 the framework treats this as a candidate extension; the methodology codification ADR must decide whether to fold "meta" into the axis list or treat meta-streams as an orthogonal class.
- σ estimates fold in the [`corrections.md`](corrections.md) META- adjustments (PROSE κ down 1, PAIGE κ down 1, STAKE raw count 20-not-25, STAKE cell signature spans 3 Axis-B cells per META-SER-004). Tier admission for the original streams is unaffected; numerical revisions deferred to a future re-issue of §3.1-§3.4.
- κ for GOV/GOVDEV is partially reduced by within-cell pairing (both occupy the governance-focused cell pair; some themes co-surfaced — e.g., THEME-AAAA from GOV-CRIT-004 + GOVDEV-CRIT-004 + GOVDEV-SER-010 is a 3-way co-surface that the sole-count approximation here treats as GOV-sole). Greedy ablation would re-distribute attribution; deferred per §2.3.

---

## 4. QD matrix occupancy

### 4.1 Lens × Temporal cell map

Rows = Lens (Axis A). Columns = Temporal (Axis B). Cell content = method count + dominant method.

| Lens \ Temporal | current-state | post-hoc | forward-looking |
|---|---|---|---|
| **attitudinal** | 8 (ARCH/IND/ADVO/ADVS/ADVH/EDGE/EDGE2/READY/VALID/VALID2/COURSE/CHECK) ⚠ **OVER-SATURATED** | — | — |
| **structural** | 3 (STRUCT/PROSE/EDIT) | — | — |
| **scenario** | — | 3 (INHER/INHER2/RETRO/RETRO2 = 4) | — |
| **persona** | 6 (PARTY/WIN/AME/MARY/SALLY/PAIGE/PM = 7) ⚠ **OVER-SATURATED** | — | 1 (STAKE) |
| **contrarian** | 4 (SOC/FIRST/DEVIL/COUNTER) | — | 3 (PREM/PREM2/RED/RED2 = 4) |
| **compression** | 1 (DISTILL) | — | — |

**Empty cells visible (lens × temporal):**
- `(attitudinal, post-hoc)` — no retrospective attitudinal review
- `(attitudinal, forward-looking)` — no pre-mortem attitudinal review
- `(structural, post-hoc)` — no retrospective restructure pass
- `(structural, forward-looking)` — no forward-looking structural review
- `(scenario, current-state)` — no scenario lens applied to current state
- `(scenario, forward-looking)` — no forward-looking scenario (already partly covered by STAKE = persona+forward)
- `(persona, post-hoc)` — no post-hoc persona review
- `(contrarian, post-hoc)` — no contrarian retrospective
- `(compression, post-hoc)` — no historical compression
- `(compression, forward-looking)` — no forward-looking compression (degenerate — likely not meaningful)

**Over-saturated cells (per Self-MoA logic, candidates for thinning):**
- `(attitudinal, current-state)` — 8+ methods crammed into one cell. COURSE, CHECK, VALID2 are dominated and should be Tier D.
- `(persona, current-state)` — 7 methods. SALLY is dominated by PAIGE on narrative; MARY is paired with READY. Candidates for Tier C demotion.

### 4.2 Decomposition × Severity cell map

Rows = Decomposition (Axis C). Columns = Severity bias (Axis D).

| Decomp \ Severity | blocking-impl | governance | security/ops | narrative-clarity | cost/value |
|---|---|---|---|---|---|
| **holistic** | 10+ | 4 (PARTY/RETRO/RETRO2/EDIT) | 2 (PREM/PREM2) | 1 (STRUCT) | 1 (PM) |
| **exhaustive** | 5 (EDGE/EDGE2/READY/VALID/VALID2) | 1 (VALID) | 2 (RED/RED2) + 1 (STAKE) | — | — |
| **focused** | 3 (MARY/COURSE/CHECK) | — | — | 4 (PROSE/SOC/SALLY/PAIGE) | — |
| **derivative** | 1 (FIRST) | 1 (DEVIL) | — | 1 (DISTILL) | 1 (COUNTER spans all) |

**Empty cells visible (decomp × severity):**
- `(holistic, cost/value)` — only PM; sparse
- `(exhaustive, narrative-clarity)` — empty
- `(exhaustive, cost/value)` — empty (high-priority for Wave 5)
- `(focused, governance)` — empty
- `(focused, security/ops)` — empty (potential Wave 5 target)
- `(focused, cost/value)` — empty
- `(derivative, blocking-impl)` — only FIRST; sparse
- `(derivative, security/ops)` — empty
- `(derivative, cost/value)` — only COUNTER (spans); not a dedicated method

**High-importance empty cells** (Axis D ∈ {blocking-impl, governance, security/ops}):
- `(focused, governance)` — no focused governance audit
- `(focused, security/ops)` — no focused security/ops audit
- `(derivative, security/ops)` — no derivative security/ops audit

These are **Wave 5 admission targets** (§7 below).

---

## 5. Tier A / B / C / D catalog (consolidated)

### Tier A — Core (run on every audit)

13 methods. These define the QD archive's minimum sufficient coverage.

1. `ARCH-` / `IND-` — adversarial-general, opus (attitudinal × current × holistic × blocking). Baseline workhorse.
2. `EDGE-` — edge-case-hunter, opus (attitudinal × current × exhaustive × blocking). Sole-surfacer of THEME-U.
3. `READY-` — check-implementation-readiness, opus (attitudinal × current × exhaustive × blocking). Implementability gate.
4. `INHER-` — inheritor framing, opus (scenario × post-hoc × holistic × blocking). Sole-ish on THEME-H.
5. `STRUCT-` — editorial-review-structure, opus (structural × current × holistic × narrative). Sole on THEME-N.
6. `PREM-` — pre-mortem, opus (contrarian × forward × holistic × security/ops). Sole on THEME-X; forward-looking lens.
7. `PARTY-` — party-mode, opus (persona × current × holistic × governance). Sole on THEME-V; persona aggregator.
8. `RED-` — red-team, opus (contrarian × forward × exhaustive × security/ops). Sole on THEME-AA (supply-chain).
9. `RETRO-` — retrospective, opus (scenario × post-hoc × holistic × governance). Sole on 6 themes.
10. `WIN-` / `AME-` — Winston + Amelia persona, opus + sonnet (persona × current × holistic × blocking). Sole on HH, JJ, GG.
11. `FIRST-` — first-principles, sonnet (contrarian × current × derivative × blocking). Sole on 4 themes.
12. `PM-` — John persona, opus (persona × current × holistic × cost/value). Sole on entire THEME-RR product workflow cluster.
13. `PAIGE-` — Paige persona, sonnet (persona × current × focused × narrative). Sole on SS, TT, ZZ.
14. `DEVIL-` — devil's-advocate, opus (contrarian × current × derivative × governance). Sole on 4 meta-critique themes.
15. `STAKE-` — stakeholder-simulation, opus (persona × forward × exhaustive × security/ops + cost/value). **NEW METHOD, sole on 10 themes — highest single-stream κ.**
16. `COUNTER-` — counter-factual, opus (contrarian × current × derivative × axis-spanning). **NEW METHOD, sole on 9 themes.**

(16 listed; some are pairs like WIN+AME counted under a shared cell.)

### Tier B — Complementary (run when budget allows)

Methods that contribute marginal coverage at lower individual quality, or are model-permutations of Tier A methods.

- `ADVO-`, `ADVS-`, `ADVH-` — adversarial-general model permutations of ARCH/IND. Lower σ each, but together provide model-diversity coverage (per Krogh-Vedelsby ambiguity decomposition + ADR-0007 stochastic-tier discipline by analogy).
- `PROSE-` — editorial-prose, sonnet (structural × current × focused × narrative). Sole on THEME-P.
- `SOC-` — socratic, opus. Largely confirmations; admitted to keep elicitation diversity.
- `VALID-` — validate-prd, opus. Implementation-readiness analog.
- `DISTILL-` — distillator, sonnet. Only compression-lens method; admitted on uniqueness grounds (κ via cell-rarity even if sole-themes count low).
- `MARY-` — Mary persona, opus. Sole on WW.
- `RED2-`, `EDGE2-`, `INHER2-` — Wave 4 sonnet model-permutations. Admitted for model-diversity within Tier-A methods.
- `RETRO2-`, `PREM2-` — Wave 4 sonnet model-permutations. Sole on 3 + 2 themes respectively; arguably Tier A but reclassified B due to model-perm derivation. **Promotion candidate: revisit at next audit.**

### Tier C — Experimental / under review

- `SALLY-` — Sally persona, sonnet. Low κ in this audit; possibly cell-redundant with PAIGE. Run paired with PAIGE next audit, re-evaluate.

### Tier D — Deprecated (drop from catalog)

These methods have σ ≥ floor (so not noise-class) but κ ≈ 0 AND occupy already-saturated cells. They add ensemble cost without expanding the archive. Per Self-MoA logic, dropping them improves net ensemble quality.

- `COURSE-` — correct-course. Cell `(attitudinal, current, focused, blocking)` already covered by READY + CHECK + VALID. 0 sole themes. **Drop.**
- `CHECK-` — checkpoint-preview. Same cell as COURSE. 0 sole themes. **Drop.**
- `EDIT-` — edit-prd. Cell `(structural, current, holistic, narrative)` covered by STRUCT. 0-1 sole themes. **Drop.**
- `VALID2-` — validate-prd-sonnet. Model-perm of VALID; adds 1 tactical finding. **Drop**, OR retain only if model-diversity within (attitudinal, exhaustive) is independently valued.

**Estimated cost saving:** 4 deprecated methods × ~15-20 raw findings × downstream consolidation time ≈ 1-2 hours of consolidator effort per audit, plus 4 stream invocations.

---

## 6. Theme-by-theme κ attribution

Of ~70 themes, attributing each to its sole-surfacer or first-surfacer establishes who *earned* admission. Pulled from findings-index.md cross-referenced with consolidated.md.

### Wave 1 themes (26)

| Theme | Sole/first-surfacer | Confirming streams | Attribution |
|---|---|---|---|
| A — BMAD strategy drift | ARCH (in-context advantage) | 11/12 | Tier-A confirmation cascade |
| B — Trailer fragmentation | ARCH/IND (paired) | 10/12 | Tier-A confirmation cascade |
| C — gate-coverage syntactic | ARCH/PREM (PREM-01 strongest) | 9/12 | PREM-distinct framing |
| D — Hook implementation | **EDGE** (sole on most concrete cases) | 10/12 | **EDGE = κ source** |
| E — Red-before-green / checkpoint | EDGE/IND | 9/12 | EDGE = κ source |
| F — Push invariant | PREM (PREM-02 framing) | 8/12 | PREM = κ source |
| G — REQ-ARCH format | ARCH/INHER (INHER-10 sole on compound REQs) | 8/12 | INHER = κ contributor |
| H — Missing artifact-type ADRs | **INHER** (INHER-01, 15-21) | 8/12 | **INHER = primary κ source** |
| I — Test tier semantics | EDGE/PROSE/PREM split | 9/12 | distributed |
| J — Stochastic tier statistical | PREM (PREM-04 cost-budget proxy) | 7/12 | PREM = κ contributor |
| K — Phase ordering circular | ADVO/EDGE | 9/12 | distributed |
| L — CLAUDE↔ARCH duplication | ARCH-CRIT-08 (in-context only) | 5/12 | ARCH-in-context κ |
| M — Amendment-log discipline | STRUCT (STRUCT-04, 05) + IND-PROC | 6/12 | STRUCT = κ contributor |
| N — Summary-of-summaries drift | **STRUCT** (sole) | 5/12 | **STRUCT = κ source** |
| O — Status enum conflict | ARCH/IND/EDGE | 5/12 | distributed |
| P — "The paper" citation | **PROSE** (PROSE-related) | 5/12 | **PROSE = κ source** |
| Q — Anti-aliasing defects | distributed (ADVO/ADVH/ADVS/READY/PREM) | 6/12 | distributed |
| R — Vapor references | distributed (ARCH/INHER/READY) | 9/12 | distributed |
| S — PHASE-5 unreachable | ARCH/PARTY (PARTY-PROC-01 strongest framing) | 5/12 | PARTY = κ contributor |
| T — Operational artifact gaps | IND/INHER/EDGE distributed | 6/12 | distributed |
| U — ID allocation races | **EDGE** (EDGE-10..15) | 5/12 | **EDGE = κ source** |
| V — Inter-agent trust + UX | **PARTY/PREM** (PREM-17 + PARTY-UX-01/02) | 4/12 | **PARTY = κ source** |
| W — Anthropic-client transitive | PREM (PREM-14) + ADVH | 3/12 | PREM = κ contributor |
| X — Append-only calcification | **PREM** (PREM-07 sole) | 1/12 | **PREM = κ sole-source** |
| Y — PHASE-5 numbering bug | distributed | 5/12 | distributed |
| Z — commit-trailers-valid trigger | READY (READY-03) | 3/12 | READY = κ contributor |

**Wave 1 κ summary:** EDGE = 3 sole sources, PREM = 4 sole sources, INHER = 1 sole source + primary on H, STRUCT = 2 sole sources, PROSE = 1 sole source, PARTY = 2 sole sources. These confirm Tier-A status. ARCH/IND/ADVO/ADVS/ADVH together contribute the confirmation density but few sole sources — they are paired-redundant by design, which is exactly what they should be (model-diversity for ambiguity decomposition).

### Wave 2 themes (16)

| Theme | Sole-source | Attribution |
|---|---|---|
| AA — Supply-chain enforcement gap | **RED** | RED κ source |
| BB — ADR supersession protocol | RETRO/PARTY/COURSE distributed | RETRO κ source primary |
| CC — Missing test tiers (security, perf) | RETRO/RED | distributed |
| DD — Phase regression state machine | **RETRO** (sole) | RETRO κ sole |
| EE — Secrets/credentials | RETRO/RED/ARCH | distributed |
| FF — Local dev environment | RETRO/WIN | RETRO+WIN κ contributors |
| GG — Hook ABI cluster | **AME** (5 findings) | AME κ source |
| HH — BMAD upstream dependency | **WIN** (sole) | WIN κ sole |
| II — Network dependency in commit hook | **FIRST** (sole) | FIRST κ sole |
| JJ — Test runner ownership | **WIN** (sole) | WIN κ sole |
| KK — Append-only NOT gated for ADR amendments | **FIRST** (sole) | FIRST κ sole |
| LL — BMAD CWD discipline 4-phase gap | **FIRST** (sole) | FIRST κ sole |
| MM — Retroactive compliance remediation | FIRST/AME/ADVS | distributed |
| NN — PRD→REQ traceability ungated | **FIRST** (sole) | FIRST κ sole |
| OO — Long-running branch matrix conflicts | RETRO/WIN | RETRO κ contributor |
| PP — Anti-aliasing n-gram vs semantic | PREM/FIRST/WIN/DEVIL distributed | distributed |

**Wave 2 κ summary:** RETRO = 2 sole + 4 primary; RED = 1 sole + 1 primary; WIN = 2 sole; AME = 1 sole; FIRST = 4 sole. These four are Tier A. SOC/VALID/DISTILL produced 0 sole — they are confirmation-class (Tier B at best).

### Wave 3 themes (9)

| Theme | Sole-source | Attribution |
|---|---|---|
| RR — Product workflow primitives | **PM** (sole, entire cluster) | PM κ sole |
| SS — Glossary drift | **PAIGE** (sole) | PAIGE κ sole |
| TT — Audience clarity | **PAIGE** (sole) | PAIGE κ sole |
| UU — Principle independence | **DEVIL** (sole) | DEVIL κ sole |
| VV — Principle list append-only | **DEVIL** (sole) | DEVIL κ sole |
| WW — Determinism vs idempotence | **MARY** (sole) | MARY κ sole |
| XX — Trailer signal quality | **DEVIL** (sole) | DEVIL κ sole |
| YY — Stack consolidation | **DEVIL** (sole) | DEVIL κ sole |
| ZZ — Forward references / onboarding | PAIGE/SALLY | PAIGE κ primary |

**Wave 3 κ summary:** PM = 1 cluster (10 sub-findings); PAIGE = 3 sole; DEVIL = 4 sole; MARY = 1 sole. These are Tier A. SALLY contributed 1 reinforcement only; COURSE/CHECK/EDIT = 0 sole. **This is the strongest single piece of evidence for COURSE/CHECK/EDIT Tier-D classification.**

### Wave 4 themes (~17)

| Cluster | Sole-source | Attribution |
|---|---|---|
| AAA-JJJ (10 themes) | **STAKE** (sole on all) | STAKE κ sole — 10 themes, highest in corpus |
| KKK-SSS (9 themes) | **COUNTER** (sole on all) | COUNTER κ sole — 9 themes |
| TTT, UUU, VVV (3 themes) | **RETRO2** (sole) | RETRO2 κ sole |
| WWW, XXX (2 themes) | **PREM2** (sole) | PREM2 κ sole |
| (tactical refinements) | VALID2/EDGE2/RED2 | distributed; near-zero κ |

**Wave 4 κ summary:** STAKE + COUNTER together account for 19 unique themes — they alone explain the 46% Wave 4 marginal-novelty spike. **This is the empirical confirmation that the methodology-variance / model-variance distinction is real.** Sonnet model-permutations (RED2, EDGE2, INHER2) converge as expected; sonnet new-method-extensions (RETRO2, PREM2) added 5 themes — borderline interesting, suggests model + lens interaction warrants more study.

---

## 7. ACGR re-measurement of convergence

### 7.1 Archive trajectory

Computing `archive(W)` for each wave, where archive elements are distinct (cell, theme) pairs. (Cells defined per §2.1; themes per consolidated.md.)

| Wave | Streams added | New (cell, theme) pairs | Cumulative archive | ACGR = Δ / |meaningful_cells| (~55 ± 10 per [`corrections.md`](corrections.md) META-PROC-001) |
|---|---|---|---|---|
| 1 | 12 | 26 themes × ~7 cells active = ~30 pairs | ~30 | n/a (baseline) |
| 2 | +8 | 16 themes × ~5 new cells = ~25 pairs | ~55 | 25/55 = **~45%** |
| 3 | +8 | 9 themes × ~3 cells = ~12 pairs | ~67 | 12/55 = **~22%** |
| 4 | +8 | 17 themes × ~5 cells = ~25 pairs (STAKE+COUNTER opened (persona, forward) and (contrarian, axis-spanning) cells) | ~92 | 25/55 = **~45%** |
| 5 | +4 | ~25 themes × ~2 cells avg = ~50 pairs (GOV/GOVDEV opened (attitudinal/contrarian × governance-focused); SEC opened (persona × security/ops × holistic) with theme-density 10 — high; META invokes 5th axis) | ~142 | 50/55 = **~91% ± 16%** (preliminary, sole-source approximation; see Wave-5 supplement in `consolidated.md`) |

**Interpretation under ACGR:**
- Wave 4's 45% ACGR is identical magnitude to Wave 2's, but the *cause is structurally different*. Wave 2 opened new (lens × temporal) cells via new methods (RED forward/security, RETRO post-hoc/governance). Wave 4 opened (persona × forward, exhaustive × security/ops + cost/value) via STAKE, and (contrarian × derivative × axis-spanning) via COUNTER.
- **Wave 5's ~91% is high and unexpected.** The §8 projection ("Wave 5 ACGR 10-15%") assumed the targeted empty cells were sparse (2-3 themes/cell). Empirically, the security-architectural-primitives cell (`persona × current × holistic × security/ops`) and the governance-machinery cells (`attitudinal/contrarian × current × focused × governance`) turned out to be **theme-dense** (SEC alone opened 10 new themes; GOV+GOVDEV jointly opened 15). The projection was wrong about cell theme-density, not about cell-fill direction.
- **Convergence rule under ACGR was satisfied transiently in Wave 3** (22% < 50% of allowed delta from the previous wave's growth) but not in absolute terms (<5% threshold). Wave 5 regressed the convergence trajectory significantly.
- **Revised Wave 6 prediction:** the remaining high-importance empty cells (per §7.3 updated for Wave 5) are `(structural × current × holistic × governance)` and the compression-lens Tier-A gap. Structural-governance is likely theme-dense (similar to attitudinal-governance discovered above; estimate 5-10 new themes). Compression-lens for security is unknown but likely sparse (compression lens has produced only 1 stream historically — DISTILL — with low κ). **Revised Wave 6 estimated ACGR: 10-25%.** Convergence to <5% likely requires Wave 7 or admission of a saturation rule (e.g., "stop after first wave with ACGR < 10% AND no high-importance empty cells").
- **Methodology implication:** the original prediction model assumed cells are sparse-by-default. Wave 5 falsified this for the governance and security axes. The methodology codification ADR should either (a) calibrate the prediction model against the new theme-density data, or (b) accept that the architecture audit has higher residual κ than the framework predicted and adjust the convergence threshold. Per [`corrections.md`](corrections.md) META-PROC-001, the `|meaningful_cells|` denominator itself has ±10 uncertainty that affects ACGR precision.

### 7.2 Comparison to COMPOSITE-V2 Gate 6

| Metric | Wave 2 | Wave 3 | Wave 4 | Wave 5 |
|---|---|---|---|---|
| COMPOSITE-V2 Gate 6 (marginal novelty) | ~50% | ~30-37% | ~46% (regression) | not re-measured (replaced by ACGR) |
| ACGR | ~45% | ~22% | ~45% | ~91% ± 16% (preliminary) |

The two metrics are roughly correlated but ACGR has a defensible terminal state (the archive is finite-bounded by `|meaningful_cells|`), while marginal novelty does not. **Recommendation: replace COMPOSITE-V2 Gate 6 with ACGR in the methodology ADR.** Wave-5's high ACGR is consistent with the QD admission principle (cell-targeted methods should produce high ACGR) — it indicates the audit is still discovering, not converging.

### 7.3 High-importance cell occupancy check

Cells in Axis D ∈ {blocking-impl, governance, security/ops}:

| Axis D cell | Occupied? | Methods |
|---|---|---|
| (attitudinal × current × holistic × blocking-impl) | ✓ | ARCH/IND/ADVO/ADVS/ADVH |
| (attitudinal × current × exhaustive × blocking-impl) | ✓ | EDGE/EDGE2/READY/VALID/VALID2 |
| (attitudinal × current × focused × blocking-impl) | ✓ | MARY/COURSE(D)/CHECK(D) |
| (attitudinal × current × holistic × governance) | partial | (only VALID partial) — gap |
| (attitudinal × current × exhaustive × governance) | ✓ | VALID |
| (attitudinal × current × focused × governance) | **EMPTY** | (none) |
| (scenario × post-hoc × holistic × blocking-impl) | ✓ | INHER/INHER2 |
| (scenario × post-hoc × holistic × governance) | ✓ | RETRO/RETRO2 |
| (persona × current × holistic × blocking-impl) | ✓ | WIN/AME |
| (persona × current × holistic × governance) | ✓ | PARTY |
| (persona × current × holistic × security/ops) | **EMPTY** | (none) |
| (persona × forward × exhaustive × security/ops) | ✓ | STAKE |
| (contrarian × forward × holistic × security/ops) | ✓ | PREM/PREM2 |
| (contrarian × forward × exhaustive × security/ops) | ✓ | RED/RED2 |
| (contrarian × current × focused × governance) | **EMPTY** | (none) |
| (contrarian × current × derivative × governance) | ✓ | DEVIL |
| (compression × current × derivative × narrative) | ✓ | DISTILL |
| (compression × * × * × security/ops) | **EMPTY** | (none) |
| (structural × current × holistic × governance) | **EMPTY** | (none) |

**High-importance empty cells: 5.** These do not block ACGR convergence (their theme-density is unknown), but they represent the most defensible targets for Wave-5 admission.

**Wave-5 update (post-execution).** Three of the five high-importance empty cells were filled in Wave 5:

| Cell | Status after Wave 5 | Filler | Theme-density observed |
|---|---|---|---|
| (attitudinal × current × focused × governance) | ✓ filled | GOV- | 7 new themes (YYY-EEEE), dense |
| (persona × current × holistic × security/ops) | ✓ filled | SEC- | 10 new themes (FFFF-OOOO), very dense |
| (contrarian × current × focused × governance) | ✓ filled | GOVDEV- | 8 new themes (PPPP-WWWW), dense |
| (compression × * × * × security/ops) | **STILL EMPTY** | — | (Wave-6 candidate; expected sparse per compression-lens history) |
| (structural × current × holistic × governance) | **STILL EMPTY** | — | (Wave-6 candidate; expected dense by analogy to attitudinal-governance) |

Plus the candidate 5th axis was invoked: `(meta × * × * × *)` filled by META- with 19 corpus-correction findings (not architecture themes; processed via [`corrections.md`](corrections.md)).

**Theme-density discovery.** Wave 5 falsified the §8 projection assumption that empty cells would be sparse. Governance and security/ops cells were theme-dense (avg 8 new themes/cell). The high observed ACGR (~91%) is therefore expected, not anomalous — it reflects accurate cell-filling, not over-counting.

### 7.4 Tier-A method × Axis-A coverage check

Every Axis A lens has at least one Tier A method assigned to it:

| Lens | Tier A methods |
|---|---|
| attitudinal | ARCH/IND, EDGE, READY |
| structural | STRUCT |
| scenario | INHER, RETRO |
| persona | PARTY, WIN+AME, PM, PAIGE, STAKE |
| contrarian | PREM, RED, FIRST, DEVIL, COUNTER |
| compression | (no Tier A; DISTILL is Tier B) ⚠ **GAP** |

**Compression × * × * × * has no Tier-A occupant.** DISTILL is the only compression-lens method and its σ (~0.55) keeps it at Tier B. This is acceptable per §2.5 Tier B alt rule (cell-rare ⇒ admitted on uniqueness grounds), but should be flagged in the methodology ADR: compression lens has only one entrant; admission cannot rely on Pareto selection within the cell.

---

## 8. Wave 5 admission targets

Per §7.3 and §7.4, the empty/sparse cells worth targeting in Wave 5:

### Tier-1 targets (high-importance Axis D, empty cell)

1. **`(attitudinal × current × focused × governance)`** — proposed method: **governance-focused review** (a focused-decomposition variant of validate-prd, but biased toward governance defects: REQ-ARCH ownership, ADR amendment discipline, trailer registry). Could be a new BMAD skill (`bmad-review-governance-focused`) or a focused VALID variant.
2. **`(persona × current × holistic × security/ops)`** — proposed method: **security-engineer persona** (an opus persona stream framed as a security engineer reviewing the architecture for threat-model coverage, secrets handling, signed-graph requirements). Distinct from STAKE (which is forward-looking, multi-stakeholder); this is current-state, single-persona, holistic.
3. **`(contrarian × current × focused × governance)`** — proposed method: **governance-focused devil's-advocate** (DEVIL with a focused-decomposition variant biased toward governance specifically). May be redundant with #1; pilot only if #1's findings don't cover.

### Tier-2 targets (medium-importance, empty cell)

4. **`(structural × current × holistic × governance)`** — proposed method: **governance-structural review** (STRUCT variant biased toward governance). Pilot.
5. **`(compression × current × derivative × security/ops)`** — proposed method: **threat-model distillation** (DISTILL applied specifically to security-relevant docs). Pilot.

### Meta-review target

6. **`(meta × * × * × *)`** — proposed method: **reasoning-tree auditor** (per *Auditing Multi-Agent LLM Reasoning Trees* — arXiv 2602.09341). Reviews other streams' findings for soundness; surfaces methodology artifacts and false positives. This is a *new axis* (meta) — would require extending the QD framework to a fifth axis. Recommendation: pilot, but treat the fifth axis as a candidate addition to the methodology ADR rather than a settled extension.

### Wave 5 expected ACGR

- If all 6 targets are pursued: estimated 10-20 new themes (5 cells × 2-3 themes/cell + meta-review surfaces ~5 methodology-artifact findings). Estimated ACGR: ~15-25%.
- If only Tier-1 (#1, #2, #3) pursued: estimated 6-10 new themes. Estimated ACGR: ~10-15%.

**Recommended Wave 5 scope:** Tier-1 targets + meta-review (4 streams). Estimated convergence: Wave 5 ACGR ~10-15%, Wave 6 ACGR <5% (target met).

### 8.1 Wave 5 actual outcome + Wave 6 candidates

**Wave 5 ran with 4 streams** (Tier-1 #1, #2, #3 + meta-review). **Actual ACGR: ~91% ± 16% — much higher than predicted (~10-15%).** Cause: empty cells were theme-dense (~8 new themes/cell average), not sparse (2-3 themes/cell) as the projection assumed. The QD admission rule worked as designed (cell-targeted methods produce high κ); the prediction model under-estimated cell theme-density.

Wave 6 candidates (cells not yet filled or under-saturated):

1. **`(structural × current × holistic × governance)`** — still empty after Wave 5. Estimated theme-density: 5-10 (governance cells have proven dense; structural lens may surface ARCHITECTURE.md cross-document drift specifically about governance machinery). **Recommended Wave-6 stream:** `bmad-editorial-review-structure` with governance focus. Estimate: opens 5-10 new themes; ACGR contribution ~10-20%.
2. **`(compression × * × security/ops)`** — still empty. Estimated theme-density: sparse (compression-lens method DISTILL produced only 1-2 sole themes per pass). **Recommended Wave-6 stream:** `bmad-distillator` applied specifically to ADRs covering security/operations primitives. Estimate: opens 2-4 new themes; ACGR contribution ~5-10%.
3. **Compression-lens Tier-A gap (§7.4)** — DISTILL is the only compression-lens method and is Tier B. **Recommended:** revisit DISTILL's tier classification after the Wave-5 corrections re-issue σ × κ in TASK-0044 successor; if compression-lens remains Tier-B-only, document the gap in the methodology codification ADR rather than forcing a Tier-A admission.

**Convergence outlook for Wave 6:** with the §8 projection model now falsified by Wave 5, the convergence threshold (ACGR < 5% for two consecutive waves) is unlikely to be met at Wave 6 if either Tier-1 cell remains theme-dense. The methodology ADR will need to address whether (a) the threshold is too tight given empirical cell theme-density, (b) the `|meaningful_cells|` denominator was under-estimated (a larger denominator lowers ACGR mechanically), or (c) the audit accepts higher residual ACGR than originally targeted and convergence is declared on cell-occupancy criterion (criterion #2 in §2.6) instead.

---

## 9. Recommendations for the methodology codification ADR

The methodology ADR (queued; see STATUS.md Recent decisions row "Codify audit methodology in ADR after BOTH architecture + implementation audits complete") should encode the following clauses. Numbering as proposed ADR sections.

### §1 Operating principle

> Audits are Quality-Diversity (QD) ensembles. The unit of admission is the method; the admission criterion is `σ × κ` Pareto position within a four-axis behavioural space; the convergence criterion is Archive Coverage Growth Rate (ACGR), not marginal novelty.

### §2 Behavioural axes (formal definition)

Adopt the four axes from §2.1 of this report (Lens × Temporal × Decomposition × Severity), with the operational descriptors enumerated. Cells are the cartesian product; meaningful-cell count is computed once and pinned in the ADR.

### §3 Admission rule

```
admit(M) iff
    σ(M) ≥ 0.30                                  # competence floor
  AND
    (κ(M | E) > 0                                # contributes new coverage
     OR  M is best-in-cell on (σ, κ) Pareto)     # or dominates incumbent
```

Methods admitted are catalogued in Tier A or B per the rules in §2.5 of this report.

### §4 Convergence criterion (replaces COMPOSITE-V2 Gate 6)

```
converged iff
    ACGR < 0.05  for two consecutive waves
  AND
    ≥ 80% of high-importance cells have ≥ 1 admitted method
  AND
    every (Axis-A × Axis-C) cell in the catalog has ≥ 1 Tier-A occupant
```

Retain COMPOSITE-V2 Gates 1-5 and Gate 7 unchanged.

### §5 Method catalog (initial)

Adopt the Tier A / B / C / D assignments from §5 of this report as the initial methodology catalog. **Append-only with explicit ADR amendments** (per ADR-0004 §7 spirit). Catalog extensions require:

- A new method to enter the catalog: ADR amendment with target cell, predicted σ, predicted κ.
- Tier promotion (B → A, C → B): ADR amendment after 2 audits worth of data.
- Tier demotion / deprecation (* → D): ADR amendment with ablation evidence.

### §6 Measurement discipline

- σ measured by running the signal filter on raw findings; baseline floor pinned at 0.30 (revisitable in calibration ADR per THEME-T).
- κ measured by greedy ablation: for each method, recompute archive coverage without it and report the delta.
- ACGR measured per wave with the `meaningful_cells` denominator pinned in §2.

These measurements form a dedicated audit-meta-test suite under `tools/ci/tests/audit_meta/` (referenced but not yet shipped; queued as follow-on CHG).

### §7 Deprecation procedure

The four Tier-D-candidates surfaced in this triage (COURSE, CHECK, EDIT, VALID2) should be deprecated in the ADR amendment-log. Procedure:

1. Confirm via re-running them in one more audit (implementation audit) and demonstrating κ remains ≈ 0.
2. ADR amendment: move from catalog to "deprecated methods" appendix with rationale.
3. Remove from default audit invocation in `bmad-review-multi-pass` skill (or equivalent).

### §8 Stopping rule (ties methodology ADR back to user's original concern)

> The audit terminates when the convergence criterion in §4 is met, even if individual methods continue to be invented. The QD framework guarantees that *some* new methods will continue to be inventable (the behaviour space is open-ended); the convergence criterion is therefore relative to the high-importance cell map, not to the absolute method count. This satisfies the principle "if new methods provide signal, not pursuing them would betray the spirit" by *requiring* new-method admission only when high-importance cells remain empty, and stopping when the cells are filled.

### §9 What this ADR does NOT do

- Does not freeze the audit method catalog (per user's express concern).
- Does not assert ACGR is the unique correct convergence metric — only that it is preferable to raw marginal novelty for the reasons in §1.4 + §7.2.
- Does not replace COMPOSITE-V2 Gates 1-5 + 7 (those measure orthogonal properties — method coverage, model coverage, theme confirmation density, coherence — all of which remain valuable).
- Does not specify the σ / κ measurement scripts (deferred to follow-on CHG; this ADR specifies the discipline, the CHG ships the implementation).

---

## 10. Cross-references

- **Pre-existing audit findings** (STATUS.md ledger): this triage does not introduce new findings; it re-analyses the existing 36-stream corpus.
- **Methodology codification ADR (queued):** this triage is the primary input to that ADR.
- **CHG-0032 envelope (not yet created):** when CHG-0032 is created, this triage moves from staging into the CHG's evidence directory.
- **Implementation audit (queued):** apply the QD framework dogfood-style. Pilot the method catalog from §5 against `tools/spec_lint/`, `tools/ci/`, `_bmad/`, `.github/workflows/`.

## 11. Limitations and uncertainties

- **σ estimates are not measured.** They are inferred from theme-membership rates per stream. The signal filter (§2.2) has not been formally run. Reported σ values carry ±10pp uncertainty.
- **κ estimates approximate greedy ablation.** Sole-theme counts are a lower bound on true κ; multi-way overlap is not accounted for.
- **Behavioural axes are post-hoc.** Axes were chosen by inspection during this triage. A formal validation (axis orthogonality, cell admissibility) is required before the ADR locks them. If validation produces different axes, the per-method scoring re-runs but the QD framework itself is unchanged.
- **`meaningful_cells` denominator is an estimate** (~55). A formal enumeration is required for ACGR to be reproducible across audits.
- **Tier-D candidates need confirmation.** COURSE, CHECK, EDIT, VALID2 are deprecated on the basis of *this audit's* findings only. The implementation audit may surface different κ if these methods perform differently on code+spec corpora than on doc-only corpora.

These limitations are documented for the methodology ADR red-test phase.
