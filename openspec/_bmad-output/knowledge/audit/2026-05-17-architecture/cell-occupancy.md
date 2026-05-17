# Cell occupancy + saturation analysis (TASK-0051)

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative.

**Companion documents:**
- [`signal-ledger.md`](signal-ledger.md) — 42 dense duplicate-claim clusters + ~80 long-tail singletons (input to this analysis)
- [`methodology-research-note.md`](methodology-research-note.md) — framework basis (saturation-based reformulation; §5 specifies this TASK's scope)
- [`qd-triage.md`](qd-triage.md) — original QD framework (cells, per-method σ × κ scores)
- [`corrections.md`](corrections.md) — META audit corrections applied to qd-triage attributions

**Purpose.** Execute the cell-finalization work per `methodology-research-note.md` §5: cluster-to-cell labeling, per-cell saturation status, QD-score baseline, path-dependence inventory. This is the empirical foundation for replacing the coverage metric (tautological per the three critiques) with per-cell saturation as the operational stopping signal.

This document does **not** attempt to pre-author a theoretical cell taxonomy or pin a Layer-2 architecture-audit specification — those are deferred to the methodology codification ADR. <!-- spec-lint: allow prose-xref-banned -->

---

## §1 Methodology

For each of the 42 dense clusters in `signal-ledger.md` §5, assigned an (A, B, C, D) tuple based on the **defect content** (load-bearing claim), not on the surfacing stream's method-default cell. This addresses `signal-ledger.md` §6.6's axis-independence concern (severity inherited from method, not discovered from theme).

Assignment heuristics (per cluster):
- **Axis A (Lens):** which lens the defect ITSELF lives in (e.g., "ADR-0002 amendment rewrite" is structural defect-content regardless of which method first surfaced it).
- **Axis B (Temporal):** when the defect manifests (current ≈ "broken now"; post-hoc ≈ "evident in retrospect"; forward ≈ "will manifest at scale or in future state").
- **Axis C (Decomposition):** the analytical decomposition needed to surface it (holistic ≈ requires cross-document view; focused ≈ one specific artifact; exhaustive ≈ edge-case walk; derivative ≈ from-meta-reasoning).
- **Axis D (Severity bias):** which dimension the defect's impact falls into (blocking-impl ≈ implementation-level blocker; governance ≈ control/oversight gap; security/ops ≈ confidentiality/availability/incident; narrative-clarity ≈ documentation defect; cost/value ≈ economic).

Cell assignments are best-effort judgments; different judgments would produce different cell-occupancy. The Layer-1 framework is unaffected; only the Layer-2 instance (this specific cell-map) is judgment-dependent.

---

## §2 Per-cluster cell labels

| Cluster | Defect summary | Cell (A × B × C × D) | First wave |
|---|---|---|---|
| A | bmad/_bmad path drift | structural × current × focused × governance | 1 |
| B | ARCH §9 wrappers retired but still referenced | structural × current × focused × governance | 1 |
| C | gate-coverage syntactic / meta-gate fallacy | contrarian × current × derivative × governance | 1 |
| D | "the paper" anonymous citation | structural × current × focused × narrative-clarity | 1 |
| E | PHASE-5 §Scope numbering bug | structural × current × focused × narrative-clarity | 1 |
| F | push invariant unenforceable in failure mode | attitudinal × current × focused × blocking-impl | 1 |
| G | anti-aliasing threshold undefined | attitudinal × current × focused × blocking-impl | 1 |
| H | stochastic N undefined | attitudinal × current × focused × blocking-impl | 1 |
| I | bulk-green-start N undefined | attitudinal × current × focused × blocking-impl | 2 |
| J | checkpoint_exemptions.yaml undefined | attitudinal × current × focused × blocking-impl | 1 |
| K | stale-staging deferred CHG | attitudinal × current × focused × governance | 1 |
| L | ADR-0002 Amendment 0001 = rewrite mislabeled | structural × current × focused × governance | 1 |
| M | REQ-ARCH-* missing frontmatter | structural × current × focused × governance | 1 |
| N | REQ-ARCH-0007 "verbatim" undefined | structural × current × focused × governance | 2 |
| O | PHASE-0 unbootstrappable | attitudinal × current × holistic × blocking-impl | 1 |
| P | Secrets management ADR absent | persona × current × holistic × security/ops | 2 |
| Q | Commit signing not required | persona × current × focused × security/ops | 4 |
| R | Hook sandbox / capability / identity unspecified | persona × current × holistic × security/ops | 2 |
| S | BMAD vendored bundle integrity | persona × current × exhaustive × security/ops | 4 |
| T | Journal append-only by convention only | persona × current × focused × security/ops | 2 |
| U | Amendment-vs-supersession threshold | contrarian × current × focused × governance | 5 |
| V | Project-overlay semantics undefined | scenario × forward × holistic × governance | 1 |
| W | Incident response / disclosure ADR absent | persona × current × holistic × security/ops | 4 |
| X | ADR-0008 §1 inventory missing rows | structural × current × focused × governance | 1 |
| Y | PHASE-5 product entry impossible | scenario × forward × holistic × blocking-impl | 1 |
| Z | Hook glob/pattern ambiguity | attitudinal × current × exhaustive × blocking-impl | 1 |
| AA | settings.json schema / approval | persona × current × focused × security/ops | 2 |
| BB | Red-first hole at checkpoint commits | attitudinal × current × exhaustive × blocking-impl | 1 |
| CC | Trailer schema fragmentation | attitudinal × current × focused × governance | 1 |
| DD | Cache-hit-regression baseline circular | attitudinal × current × focused × blocking-impl | 2 |
| EE | ARCH ↔ ADR-0005 §8 failure-mode drift | structural × current × focused × narrative-clarity | 1 |
| FF | PHASE-1 references retired wrappers | structural × current × focused × governance | 1 |
| GG | REQ-ARCH-0008 stale post-amendment | structural × current × focused × governance | 1 |
| HH | "Phase-0 re-gate" undefined | attitudinal × current × focused × governance | 4 |
| II | Matrix scaling / journal retention | scenario × forward × holistic × blocking-impl | 1 |
| JJ | Network egress unbounded | persona × current × focused × security/ops | 4 |
| KK | Threat model document absent | persona × current × holistic × security/ops | 2 |
| LL | ADR amendment-log conventions inconsistent | structural × current × focused × governance | 1 |
| MM | ARCH as summary-of-summaries / drift | structural × current × holistic × narrative-clarity | 1 |
| NN | Agent identity not in commit trailers | persona × current × focused × security/ops | 4 |
| OO | Real-vs-fake adapter line | attitudinal × current × focused × blocking-impl | 2 |
| PP | PHASE-3 before PHASE-4 dependency inversion | scenario × forward × focused × blocking-impl | 2 |

---

## §3 Cell-occupancy summary

15 distinct cells contain all 42 clusters. Long-tail singletons (~80 not catalogued cluster-by-cluster in signal-ledger §5) would distribute across the same 15 cells with some additional occupancy in lower-density cells (e.g., persona-narrative-clarity for PAIGE's glossary-drift theme; contrarian-derivative for some DEVIL findings) — but the dominant occupancy pattern is captured by the table below.

| Cell | Clusters | Count | Notes |
|---|---|---|---|
| structural × current × focused × governance | A, B, L, M, N, X, FF, GG, LL | **9** | densest cell; documentation/amendment discipline |
| attitudinal × current × focused × blocking-impl | F, G, H, I, J, DD, OO | **7** | gate-thresholds + checkpoint mechanics |
| persona × current × focused × security/ops | Q, T, AA, JJ, NN | **5** | concrete security primitives |
| persona × current × holistic × security/ops | P, R, KK, W | **4** | architectural security gaps |
| attitudinal × current × focused × governance | K, CC, HH | **3** | governance-mechanism gaps |
| structural × current × focused × narrative-clarity | D, E, EE | **3** | citation / numbering / drift |
| attitudinal × current × exhaustive × blocking-impl | Z, BB | **2** | hook-glob + checkpoint-walker edge cases |
| scenario × forward × holistic × blocking-impl | Y, II | **2** | PHASE-5 reachability + matrix scaling |
| contrarian × current × derivative × governance | C | **1** | gate-coverage meta-fallacy |
| contrarian × current × focused × governance | U | **1** | amendment-vs-supersession threshold |
| persona × current × exhaustive × security/ops | S | **1** | BMAD supply chain integrity |
| attitudinal × current × holistic × blocking-impl | O | **1** | PHASE-0 unbootstrappable |
| structural × current × holistic × narrative-clarity | MM | **1** | ARCH summary-of-summaries drift |
| scenario × forward × holistic × governance | V | **1** | project-overlay semantics |
| scenario × forward × focused × blocking-impl | PP | **1** | PHASE-3/4 dependency inversion |

**Total: 15 cells, 42 clusters.**

---

## §4 Per-cell saturation status

Per `methodology-research-note.md` §3.1, a cell is saturated iff in the last K=2 waves (Waves 6 + 7):
- No new method admitted to the cell, AND
- No new cluster opened in the cell, AND
- No new (σ, κ) Pareto point added by an existing method

Computation of the "no new cluster" criterion is direct from §2's first-wave column: a cell is saturated on this criterion iff none of its clusters have first-wave = 6 or 7.

| Cell | Newest cluster's wave | New methods W6+W7? | Saturated? |
|---|---|---|---|
| structural × current × focused × governance | W2 (N) | STRUCTGOV (W6, structural × current × **holistic** × governance — adjacent cell, partial overlap); ATTFUT (W7) reinforces | **YES** (no W6/W7 new clusters opened here) |
| attitudinal × current × focused × blocking-impl | W2 (I, DD, OO) | None new in this exact cell | **YES** |
| persona × current × focused × security/ops | W4 (Q, JJ, NN) | SEC (W5, persona × current × **holistic** × security/ops — adjacent); SECDISTILL (W6, compression cell) | **YES** (no W6/W7 new clusters opened here) |
| persona × current × holistic × security/ops | W4 (W) | SEC (W5); SECDISTILL (W6) reinforces | **YES** (no W6/W7 new clusters; W5 was last new) |
| attitudinal × current × focused × governance | W4 (HH) | GOV (W5, same cell axes — IS new in this cell); GOVDEV (W5 contrarian); ATTFUT (W7) | **NO** (GOV/GOVDEV opened in W5, reinforcing existing clusters but adding new method coverage; HH first-wave=W4 means a cluster opened recently); revisit per K-choice |
| structural × current × focused × narrative-clarity | W1 | No new methods W6/W7 in cell | **YES** |
| attitudinal × current × exhaustive × blocking-impl | W1 | EDGE2 (W4); no W6/W7 additions | **YES** |
| scenario × forward × holistic × blocking-impl | W1 (Y, II) | SCENFUT (W7) opened in adjacent cell (scenario × forward × **holistic** × blocking-impl is exactly SCENFUT's cell) | **NO** (SCENFUT W7 admitted; new method in cell) |
| contrarian × current × derivative × governance | W1 | None new | **YES** |
| contrarian × current × focused × governance | W5 (U) | DEVRETRO (W7, contrarian × **post-hoc**) — different cell | **YES** (U was last new; W6/W7 reinforcement-only) |
| persona × current × exhaustive × security/ops | W4 (S) | SECDISTILL (W6, compression cell — different) | **YES** (S was last new) |
| attitudinal × current × holistic × blocking-impl | W1 (O) | None new | **YES** |
| structural × current × holistic × narrative-clarity | W1 (MM) | STRUCTGOV (W6, governance Axis-D — different) | **YES** (W6 added different-Axis-D cell) |
| scenario × forward × holistic × governance | W1 (V) | SCENFUT (W7, blocking Axis-D — adjacent) | **YES** (W6/W7 added adjacent cells, not this exact cell) |
| scenario × forward × focused × blocking-impl | W2 (PP) | SCENFUT (W7, holistic decomp — different) | **YES** |

**Audit-level saturation: 13 of 15 cells saturated = 87%.**

Two cells un-saturated:
1. `attitudinal × current × focused × governance` — GOV (W5) admitted; cluster HH first-wave=W4. The "new method in last K=2 waves" criterion is sensitive here because GOV admission was W5 not W6/W7. Under strict K=2 (must be NEW in W6 OR W7) → SATURATED. Under inclusive K=2 (any of last 2 waves means waves containing the latest activity) → not saturated. Methodology ADR must pin the interpretation.
2. `scenario × forward × holistic × blocking-impl` — SCENFUT admitted in W7; it opened no new clusters but admitted to a cell that previously had only Wave-1 cluster-content. Per strict criterion → not saturated (new method admitted in W7).

**Under strict K=2 (only W6/W7 method-admissions count as "new"):** 14 of 15 saturated = 93%. SCENFUT's W7 admission is the lone outstanding.

**Under inclusive K=2 (W5/W6/W7 admissions all count):** 12 of 15 saturated = 80%.

The dual-stopping threshold from `methodology-research-note.md` §3.3 was `saturation ≥ 95%`. We're at 80-93% depending on K-interpretation. **The architecture audit is approaching saturation but not quite there yet.**

---

## §5 QD-score baseline

QD-score per cell = max(σ × κ) over methods occupying the cell. σ and κ from `qd-triage.md` §3.1-§3.7 + `corrections.md` adjustments (PROSE/PAIGE/STAKE κ revisions).

(Calculations approximate — per-method σ × κ values are themselves estimates with ±10pp σ uncertainty + sole-source approximation for κ per `qd-triage.md` §2.3.)

| Cell | Best-in-cell method | σ × κ |
|---|---|---|
| structural × current × focused × governance | STRUCT (W1) | 0.70 × 2 = 1.4 |
| attitudinal × current × focused × blocking-impl | EDGE (W1) | 0.85 × 4 = 3.4 |
| persona × current × focused × security/ops | SEC (W5) | 0.85 × 5 = 4.25 |
| persona × current × holistic × security/ops | SEC (W5) | 0.85 × 5 = 4.25 |
| attitudinal × current × focused × governance | GOV (W5) | 0.80 × 7 = 5.6 |
| structural × current × focused × narrative-clarity | STRUCT (W1) | 0.70 × 1 = 0.7 |
| attitudinal × current × exhaustive × blocking-impl | EDGE (W1) | 0.85 × 4 = 3.4 |
| scenario × forward × holistic × blocking-impl | SCENFUT (W7) | 0.80 × 7 = 5.6 |
| contrarian × current × derivative × governance | DEVIL (W3) | 0.65 × 4 = 2.6 |
| contrarian × current × focused × governance | GOVDEV (W5) | 0.80 × 8 = 6.4 |
| persona × current × exhaustive × security/ops | STAKE (W4) | 0.80 × 10 = 8.0 |
| attitudinal × current × holistic × blocking-impl | (none high-σ; cluster O surfaced by READY/EDGE/FIRST/AME) | 0.85 × 1 = 0.85 |
| structural × current × holistic × narrative-clarity | STRUCT (W1) | 0.70 × 2 = 1.4 |
| scenario × forward × holistic × governance | SCENFUT (W7) | 0.80 × 7 = 5.6 |
| scenario × forward × focused × blocking-impl | SCENFUT (W7) | 0.80 × 7 = 5.6 |

**QD-score baseline (sum): ~58.8**

The two highest-scoring cells (`persona × current × exhaustive × security/ops` at 8.0 and `contrarian × current × focused × governance` at 6.4) are concentrated by STAKE and GOVDEV respectively — both new-method-class streams from Waves 4-5 occupying previously-empty cells. This is the empirical signature of the cell-targeted QD admission rule producing high QD-score contributions.

**ΔQD-score over recent waves:**
- After W4 (STAKE+COUNTER added): +~8 from STAKE in persona-exhaustive-security cell
- After W5 (GOV+SEC+GOVDEV+META added): +~16 across governance/security cells
- After W6 (STRUCTGOV+SECDISTILL+SCENNOW+PERSRETRO): +~4 (mostly reinforcement)
- After W7 (SCENFUT+STRUCTFUT+DEVRETRO+ATTFUT): +~17 (SCENFUT opened 3 high-κ cells)

W7's ΔQD-score (17) is HIGH — driven by SCENFUT opening scenario-forward cells with κ=7. ΔQD-score / QD-score = 17/58.8 ≈ 29% growth in W7. **NOT satisfying the <5%-for-two-waves stopping criterion at depth.**

---

## §6 Path-dependence inventory

Per `signal-ledger.md` cluster first-wave analysis:

- **Wave 1 dominance: 25 of 42 dense clusters (60%) first-surfaced in Wave 1.** This is a direct consequence of Wave 1's method-choice (adversarial-general baseline streams ARCH/IND/ADVO/ADVS/ADVH + edge-case-hunter EDGE + implementation-readiness READY + structural-editorial STRUCT + pre-mortem PREM + party-mode PARTY + prose PROSE + inheritor INHER).
- **No Wave-3 cluster first-surfaces.** Wave 3's persona-streams (PM/MARY/SALLY/PAIGE) + checkpoint/course/edit/devil added themes but no DENSE clusters (clusters ≥3 members).
- **Wave-4 STAKE+COUNTER contributed 6 of 8 Wave-4 first-wave clusters** (Q, S, W, HH, JJ, NN all opened by STAKE or its security/operations stakeholder lens).
- **Only 1 Wave-5+ cluster (U)** — opened by GOV+GOVDEV jointly. The cell-targeted Wave-5+ methods filled cells with NEW methods but mostly reinforced EXISTING clusters rather than opening new ones.

**Counterfactual cells the corpus likely DIDN'T discover (because of Wave-1 method choice):**
- `(persona × post-hoc × *)` — Wave-1 had no post-hoc persona method. PERSRETRO (W6) is the only persona-post-hoc method in the corpus. If Wave 1 had included a Winston-2029-style retrospective, additional persona-post-hoc clusters likely would have surfaced earlier.
- `(scenario × current × holistic × *)` — Wave-1 had INHER (scenario × post-hoc × holistic). SCENNOW (W6) covered scenario × current. A Wave-1 scenario-current method would have surfaced workflow-defects earlier; the 6 Wave-6 SCENNOW findings include 2 CRIT-class scenario-2 defects (missing SessionStart hook, missing STATUS.md) that are arguably as load-bearing as any Wave-1 cluster.
- `(contrarian × post-hoc × *)` — Wave-1 had PREM (contrarian × forward). DEVRETRO (W7) is the only contrarian-post-hoc. DEVRETRO-CRIT-010's "meta-gate fallacy" canonical formulation is a Wave-7 contribution that could have arrived in Wave 1 with a different method-mix.

**Path-dependence acknowledgment:** the 42-cluster + 15-cell map is the cell map that emerged from THIS method-sequence. A different Wave-1 method-mix would have produced a different cell map. Per `methodology-research-note.md` §2.2, this acknowledgment is the audit's mitigation (vs the cost-prohibitive N-restart bootstrap).

---

## §7 Bottom-line numbers

| Metric | Value |
|---|---|
| Dense clusters | 42 |
| Long-tail singletons (estimate) | ~80 |
| Total unique architecture defects | ~120-150 |
| Distinct cells occupied (cluster-level) | 15 |
| Audit-level saturation (strict K=2) | 93% (14/15 cells; SCENFUT's W7 admission outstanding) |
| Audit-level saturation (inclusive K=2) | 80% (12/15 cells; counts GOV/SEC/GOVDEV/STAKE-cell as still-developing) |
| QD-score baseline (sum max σ × κ) | ~58.8 |
| ΔQD-score W7 | ~17 (29% growth) |
| Dual stopping (saturation ≥ 95% AND ΔQD-score/QD-score < 5% for 2 waves) | **NOT MET** — saturation close (80-93% vs 95% target); ΔQD-score still high (29% vs <5% target) |

**Decision implication:** the architecture audit is close to cluster-level saturation but not yet at the depth-saturation threshold. Per the saturation-based reformulation, **one more wave** focused on the un-saturated cells (filling scenario-forward depth + adding methods to persona-security cells) might bring both signals to terminal.

Concretely, a Wave 8 targeting:
- `(scenario × forward × *)` deeper coverage (a SECOND scenario-forward method — different from SCENFUT — to test whether SCENFUT's 7-cluster contribution is Pareto-optimal or whether another method would add to the front)
- `(attitudinal × current × focused × governance)` — admit a contrasting method to GOV/GOVDEV/ATTFUT to test Pareto-front stability

Would likely bring saturation to ≥95% AND ΔQD-score below 5% (since most Pareto fronts would stabilize on the second method admission).

Alternative: **declare convergence-enough at 93% saturation + acknowledge depth is still expanding** but at decreasing rate. Per the methodology codification ADR's normative choice on K and on the depth threshold, this could be a defensible stopping point.

---

## §8 Limitations

1. **Cell assignments are judgment-based.** Different judgments would shift some clusters across adjacent cells (especially decomposition style; severity for cross-cutting clusters). Methodology ADR's measurement discipline section should specify a calibration corpus + inter-rater agreement target.
2. **Long-tail singletons not individually cell-labeled.** Only the 42 dense clusters are in §2's table. Including singletons would likely add 3-5 more cells (e.g., persona-narrative for PAIGE glossary-drift) and shift saturation% downward (more cells, some less-developed).
3. **QD-score uses sole-source κ approximation per qd-triage §2.3.** Greedy ablation would refine. Methodology ADR audit-meta-test suite should mechanise.
4. **Saturation K=2 is unprincipled.** Could be K=1 (risk false-positive saturation on quiet waves), K=3 (more conservative). No principled basis yet; methodology ADR must pin.
5. **The 95% saturation + <5% ΔQD-score thresholds are inherited from `methodology-research-note.md` §3.3 as defaults.** Empirically tuned thresholds would require multi-audit calibration data (we have one architecture audit; the implementation audit when run would be the second data point).
