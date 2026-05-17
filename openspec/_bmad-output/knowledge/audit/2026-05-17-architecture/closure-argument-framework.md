# Closure-argument framework for audit-methodology

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative. Input to the methodology codification ADR (queued; no ID allocated). <!-- spec-lint: allow prose-xref-banned -->

**Companion documents (read in this order):**
- This file (the framework spec, audit-type-agnostic)
- [`methodology-research-note.md`](methodology-research-note.md) — three structural critiques that motivated this framework; **the saturation-based reformulation in §3 is SUPERSEDED by this file**; the three critiques in §2 remain valid and are now resolved by the closure-argument construction below.
- [`cell-occupancy.md`](cell-occupancy.md) — empirical cell-occupancy under the post-hoc-cells approach (~93% saturation that proved illusory); preserved as evidence-of-failure that motivates closure-at-axis-level.
- [`wave-8-path-dependence-results.md`](wave-8-path-dependence-results.md) — empirical demonstration that documentation-only path-dependence mitigation is insufficient; ~30 new clusters surfaced by 3 second-method runs; preserved as supporting evidence.
- [`signal-ledger.md`](signal-ledger.md) — 42 dense duplicate-claim clusters across 867 findings; serves as the cluster set the v1.0 instance will distribute across cells.

**Purpose.** Establish a domain-general framework for audit methodology that resolves the structural problems (coverage tautology, ordering bias, audit-type variance) the earlier saturation-based reformulation only partially patched. The framework draws on user-supplied synthesis of QD optimization + active learning + mutation testing + contextual bandits + Bayesian decision theory + semantic versioning. This file is the framework spec; the architecture-audit v1.0 instance is published separately (per `TASK-0053`).

---

## §1 The reframe (why the cell-list-as-primitive approach fails)

The earlier post-hoc-cells approach (qd-triage.md framework + saturation-based reformulation in methodology-research-note.md §3) treated the cell list as the primitive object: discover findings, cluster, cell-label by judgment, compute saturation. Three structural problems emerged from this primitive choice:

1. **Coverage tautology** — cells defined from observed clusters means coverage is 100% by construction.
2. **Ordering bias / path-dependence** — cell discovery depends on method-sequence; Wave 8 empirically demonstrated 71% cluster expansion under partial bootstrap.
3. **Audit-type criticality variance** — cell importance differs by audit type; treating it as universal mis-encodes the decision.

The reframe (per user, 2026-05-17): these are not patchable defects of the post-hoc-cells approach. They are evidence that **the cell list is the wrong primitive**. The corpus had fused three orthogonal concerns into one matrix:

- (a) **Behavioural descriptors** — what makes one cell different from another
- (b) **Quality predicates** — what "pass/fail" means inside a cell
- (c) **Audit-type weights** — which clusters matter for this audit

Separating these resolves all three structural problems. The construction is the 7-step framework below.

---

## §2 The 7-step framework

### Step 1 — Separate the three layers

Treat behavioural descriptors (a), quality predicates (b), and audit-type weights (c) as three orthogonal concerns with separate specifications. Failing to separate produces "descriptor instability": the cell explosion stops being about coverage and reveals itself as continuously-changing definitions of "different" mid-flight.

This separation is canonical in QD literature (Cully & Demiris 2018 §4 explicit) and in Bayesian decision theory (utility function is task-specific input, not feature-of-data).

### Step 2 — Close the descriptor space; derive cells

You cannot defensibly enumerate cells. You can defensibly enumerate the **axes** that generate cells, because axes live in a much smaller and more argumentable space.

For each audit type, pin a finite set of behavioural descriptors (axes). Argue closure at the axis level: "these N axes cover the failure ontology because..." (defeasible argument, not formal proof). The Cartesian product of those axes becomes the constructed cell universe.

Coverage becomes a defensible claim over a derived space: `|filled_cells| / |Cartesian_product_cells|`. Every new perspective in subsequent passes either (i) maps onto an existing axis (no closure-argument disturbance) or (ii) introduces a new axis (rare, auditable event, triggers version bump).

This matches MAP-Elites' original framing (Mouret & Clune 2015 §3.2: "behaviour descriptor specified up front") and ML interpretability practice (LIME/SHAP argue at feature-level, not example-level).

### Step 3 — Trunk-and-frontier budget split

Stop trying to decide whether each long-tail cell is "essential." Run two budgets in every audit pass:

- **Trunk cells:** the committed, always-evaluated subset whose absence would invalidate the audit claim. Small, stable across versions.
- **Frontier cells:** a rotating sample from the long tail, with a fixed compute envelope per pass.

Breakthrough observations from frontier get **promoted** to trunk on the next version cut. Trunk cells whose Pareto front is stable across many passes get **demoted** to sparse sampling.

Audit claim: "100% of trunk + sampled frontier at confidence X." This is honest, defensible, and decouples the long-tail-worry from the audit-completeness-claim.

This pattern has four converging research lineages: active learning's exploit/explore split (Settles 2009), novelty-search archive vs frontier (Lehman & Stanley), regression-suite vs exploratory testing in software (Bach & Bolton), and canary-deployment / probationary-period certification.

### Step 4 — Three operational convergence tests

Stopping is determined by three signals, not one:

1. **Inter-perspective clustering rate.** Run an INDEPENDENT perspective pass (different LLM family, or human-coded baseline, or counterfactual method-set) and measure what fraction of its generated cells collapse into existing clusters at threshold τ. When ≥90% cluster onto existing cells, descriptor saturation is achieved. Maps onto inter-rater reliability (Krippendorff's α, Cohen's κ; ≥90% is the standard "substantial agreement" cutoff in qualitative coding).
2. **Mutation catch rate.** Synthetically perturb known failure modes (a gauntlet of seeded faults) and measure whether the trunk catches them. If catch rate is high and stable across mutation classes, additional cells have low marginal value. Maps onto mutation testing in software (DeMillo, Lipton, Sayward 1978; Just et al. 2014 PIT). The mutation score is established as a robustness metric.
3. **Information gain per new cell.** Measure whether new cells change posterior failure rates of OTHER cells. When ΔH ≈ 0, you're adding cosmetics, not signal. Maps onto Bayesian experimental design (MacKay 1992 "Information-based objective functions for active data selection").

The asymptote is not a problem to overcome — it IS the signal of convergence. Stop counting cells; measure the rate of new-signal-per-cell.

### Step 5 — Audit-type as archetype prior (first-class object)

Don't try to find one canonical cell-weighting. Define a small finite set of audit archetypes, each with a prior weight vector over cell clusters. Examples:

- `conformance` archetype — weights cells about specification-to-implementation alignment
- `drift` archetype — weights cells about cross-document or cross-version inconsistency
- `adversarial` archetype — weights cells about attack-surface + threat-model coverage
- `novelty` archetype — weights cells about new-method-discovery
- `regression` archetype — weights cells about previously-known defects re-emerging

Each audit run instantiates one archetype (or a weighted mix). The cell matrix is shared across all audit types; the importance projection over it is archetype-specific.

This is where the "which cluster matters" judgment lives — encoded once, in one place, where it's reviewable.

Maps onto Bayesian decision theory (prior-over-hypotheses is decision-context-specific input) and onto MOME (Pierrot et al. 2022) generalized to per-cell-Pareto-front-with-archetype-weighted-importance. Also analogues in role-based access control + regulatory-body priority-structures.

### Step 6 — Adaptive depth as a contextual bandit

For per-cell resource allocation across passes, frame as a contextual bandit:

- Each cell carries a posterior failure rate (Beta prior, updated each run).
- Each cell carries a severity weight from the active archetype.
- Per-pass compute is allocated proportional to **expected information gain × severity × novelty bonus**.

Cells with high posterior variance or recent flips get **deepened**. Cells stable-pass for many runs get **demoted to sparse sampling**. Novelty bonus favors cells with low-N sample history.

This is principled adaptive allocation, not hand-tuned. Cells naturally surface as "boring" (stable, low variance, sparse-sample) without manual judgment. Maps onto contextual bandit theory (Auer, Cesa-Bianchi, Fischer 2002; Langford & Zhang 2007; Thompson sampling with Beta priors). For software specifically, Böhme et al. (2017) apply bandits to fuzzing budget allocation.

### Step 7 — Version the matrix; ship v1.0 with explicit closure argument

Treat the QD matrix as a living artifact with **semantic versioning**. Bootstrap by committing to v1.0 with:
- Closure argument at the axis level
- Trunk set
- Frontier sampling policy
- Archetype priors
- Convergence thresholds

Then let the matrix evolve through observed promotions (frontier → trunk), demotions, and axis additions — each as auditable version bumps (v1.0 → v1.1 → v1.2 → v2.0 for axis-set changes).

The bootstrap doesn't need to be "right" — it needs to be **defensible at v1.0 and evolvable**. We are not searching for the true matrix; we are standing up a governance process around an admittedly imperfect one.

Matches semantic versioning (semver.org), ML dataset versioning (DVC, MLflow), and constitutional-governance patterns (IETF RFC, Python PEP, TC39 stages — the constitution evolves through documented amendment).

### The reframe in one sentence

> The problem isn't "which cells matter" — it's "at what level of the construction do I argue closure?" Argue at the axis level (tractable); make audit-type a projection (encodable); make per-cell depth a bandit (principled). The asymptote becomes a measured convergence signal, not an existential threat to the audit claim.

---

## §3 Research reconciliation

| Step | Maps onto | Adoption type |
|---|---|---|
| 1. Separate three layers | Cully & Demiris (2018) §4 algorithm/descriptor/quality separation; Stock (2025) behaviour-descriptor as domain-specific; Berger (1985) Bayesian decision theory utility function | **Canonical** |
| 2. Closure at axis level | Mouret & Clune (2015) §3.2 behaviour-descriptor specified up front; Pugh, Soros, Stanley (2016) completeness arguments; LIME/SHAP feature-level interpretability | **Canonical** |
| 3. Trunk/frontier split | Settles (2009) active learning exploit/explore; Lehman & Stanley novelty-search archive vs frontier; Bach & Bolton software-testing regression vs exploratory; canary deployment | **Canonical synthesis** (four converging lineages) |
| 4. Three convergence signals | (a) Krippendorff's α, Cohen's κ (inter-rater reliability); (b) DeMillo et al. (1978) + Just et al. (2014) mutation testing; (c) MacKay (1992) Bayesian experimental design | **Novel combination of well-established components** |
| 5. Archetype priors | Bayesian decision theory; MOME (Pierrot 2022) per-cell Pareto fronts; role-based access patterns; regulatory-body priority structures | **Canonical adoption** |
| 6. Bandit allocation | Auer, Cesa-Bianchi, Fischer (2002) finite-time bandit; Langford & Zhang (2007) Epoch-Greedy contextual bandits; Thompson sampling; Böhme et al. (2017) adaptive fuzzing | **Canonical adoption** |
| 7. Version the matrix | Semantic versioning (semver.org); DVC + MLflow dataset versioning; IETF RFC / Python PEP / TC39 stages constitutional governance | **Canonical** |

The whole construction echoes how mature ML practice handles open-ended discovery problems. Two close analogues:
- **Adversarial ML testing** (Madry et al. lineage): closure at the perturbation-class level (L∞, L2, semantic), not perturbation-instance level. Trunk = known attack classes; frontier = new attack candidates. Promotion when frontier attack stably defeats trunk defense.
- **RLHF reward modeling** (Christiano, Stiennon, OpenAI lineage; Anthropic constitutional AI): closure at the preference-axis level (helpfulness, harmlessness, honesty), not preference-instance level. Archetype priors map exactly onto preference-weighting / principle-weighting choices.

Both fields had this exact problem and converged on this exact solution.

---

## §4 Operationalization against the five-layer pipeline (PLACEHOLDER)

The user has offered to map this framework onto the existing five-layer pipeline — specifically where the trunk/frontier split lives relative to deterministic checks vs the Gauntlet vs the seeded calibration. Pending that mapping, four open operationalization questions:

1. **Where does the trunk live?** Per-CHG, per-archetype, per-spec-domain? Natural fit: per-archetype, with architecture-audit archetype's trunk dominated by structural-contract + cross-artifact-consistency cells.
2. **Where does the Gauntlet live relative to trunk vs frontier?** Gauntlet = mutation catch rate signal in Step 4. Gauntlet IS the closed-set perturbation suite that trunk must catch. New Gauntlet entries get added when a frontier finding establishes a new attack class.
3. **Where does seeded calibration sit?** Possibly the cold-start for bandit Beta priors (Step 6); possibly the inter-perspective baseline (Step 4 signal 1); possibly both.
4. **How do deterministic checks (spec_lint rules) map onto cells?** Each lint rule is a closed-form check living in a specific cell; the rule set IS the trunk for the structural-contract axis.

These get answered when the operationalization layer is authored. This file's v1.0 instance work (per TASK-0053) does not block on them; v1.0 is a feasibility POC and the operationalization mapping informs v1.1+.

---

## §5 Supersession + preservation

- **SUPERSEDED:** [`methodology-research-note.md`](methodology-research-note.md) §3 (saturation-based reformulation). The saturation patch was a partial fix; this framework subsumes it.
- **STILL VALID:** [`methodology-research-note.md`](methodology-research-note.md) §2 (the three structural critiques). These remain the motivating evidence for this framework; they are now resolved by closure-at-axis-level + archetype-projection + trunk/frontier-budget rather than by saturation.
- **PRESERVED AS EVIDENCE-OF-FAILURE:** [`cell-occupancy.md`](cell-occupancy.md) (93% saturation that proved illusory) and [`wave-8-path-dependence-results.md`](wave-8-path-dependence-results.md) (~30 new clusters under partial bootstrap). These are empirical demonstrations that the post-hoc-cells approach fails; they motivate this framework.
- **INPUT DATA:** [`signal-ledger.md`](signal-ledger.md) (42 clusters) + [`wave-8-path-dependence-results.md`](wave-8-path-dependence-results.md) §2 (~30 new clusters) = ~72 clusters that v1.0 will distribute across axis-derived cells.

---

## §6 v1.0 instance for the architecture-audit archetype (POC stub; full POC in TASK-0053)

This stub is a starting point for the POC; not a final spec. The POC TASK fills in the empirical mapping.

### v1.0 axes for architecture-audit (provisional)

Per the user's example framing, a starting axis set for architecture audits:

1. **Spec-intent axis** — does the architecture's claim of what-it-does match its actual specification? (covers e.g. claim-vs-formal-statement drift)
2. **Structural-contract axis** — do the artifact's structural relationships (cross-document references, amendment-log discipline, frontmatter schemas) hold under their own rules?
3. **Instance-conformance axis** — do specific artifacts conform to the discipline the architecture asserts?
4. **Cross-artifact-consistency axis** — do parallel claims across documents agree?
5. **Adversarial-robustness axis** — under realistic attack (malicious actor, prompt injection, supply-chain compromise), does the architecture defend?

**Closure argument (defeasible):** these 5 axes cover the architecture-audit failure ontology because any architecture defect either (a) is a wrong claim about behaviour (Spec-intent), (b) is a structural inconsistency (Structural-contract or Cross-artifact-consistency), (c) is a discipline-violation by an instance (Instance-conformance), or (d) is an unaddressed adversarial scenario (Adversarial-robustness). New perspectives that don't fit one of these five trigger an axis-add version bump.

This argument is provisional. The POC's job includes stress-testing it against the existing 72 clusters.

### v1.0 Cartesian product (provisional)

5 axes × ~3-5 bins per axis = ~243-3125 theoretical cells; admissibility filter (drop degenerate combinations) probably yields ~30-80 admissible cells. POC pins the exact bin counts.

### v1.0 trunk (provisional sketch)

Trunk = cells whose absence would invalidate the architecture-audit claim. Sketch (subject to POC refinement):
- All cells on the Structural-contract axis
- High-severity-bin cells on Adversarial-robustness
- Top-3 most-cluster-dense cells on Instance-conformance (governance machinery, security primitives, etc.)

Estimated trunk size: 8-15 cells.

### v1.0 frontier (provisional sketch)

Frontier = remaining admissible cells with rotating sample. Per-pass budget: ~3-5 cells per audit wave. Promotion rule: cell qualifies for trunk if it accumulates ≥N findings across ≥M passes.

### v1.0 architecture-audit archetype prior (provisional sketch)

Priority weighting per axis (sum = 1):
- Structural-contract: 0.30
- Adversarial-robustness: 0.25
- Cross-artifact-consistency: 0.20
- Instance-conformance: 0.15
- Spec-intent: 0.10

POC validates by checking whether this prior matches the empirical severity distribution in the 72-cluster set.

### v1.0 convergence-signal status

- **Inter-perspective clustering rate:** infrastructure not yet built (would need a separate-from-corpus baseline pass). v1.0 records the metric definition; v1.1+ measures.
- **Mutation catch rate:** Gauntlet infrastructure pending (per §4 placeholder above). v1.0 records the metric definition; v1.1+ measures.
- **Information gain per new cell:** requires multi-audit posterior data. v1.0 records the metric definition; v2.0+ has enough data to measure.

v1.0 stopping for the architecture audit (retrospectively): the 8 waves we ran fill the trunk + sample the frontier adequately under the provisional v1.0; the audit is **done** relative to v1.0 architecture-audit-archetype.

---

## §7 Limitations + open questions

1. **The closure argument at axis level is defeasible, not formal.** The "these 5 axes cover the failure ontology" claim is reviewable but not proven. Cully (2018) §4.1 acknowledges this as "the hardest single design decision" with no general resolution.
2. **The three convergence signals require infrastructure not yet built.** Inter-perspective baseline pass; Gauntlet seeded-fault suite; multi-audit posterior data. v1.0 specifies; v1.1+ measures. The audit pipeline can run under v1.0 without the measurement infrastructure, with the limitation documented.
3. **Archetype priors are normative.** Different teams could disagree about the weighting for a given audit type. The methodology codification ADR should specify that archetype priors are themselves reviewable artifacts under semver, with disagreements resolved by ADR amendment. <!-- spec-lint: allow prose-xref-banned -->
4. **Bandit cold-start.** With N=1 architecture audit, Beta priors are very uncertain. First several audits look like exploration, not exploit-vs-explore. This is the standard active-learning cold-start; well-handled in literature with diffuse uninformative priors initially.
5. **Cross-archetype findings.** A finding that's high-priority under `adversarial` archetype but low-priority under `conformance` archetype needs a policy for how it surfaces. Probably: each archetype runs its own audit pass; findings get tagged with which archetype surfaced them; cross-archetype reconciliation happens at the resolution-CHG stage.
6. **Versioning overhead.** v1.0 → v1.1 amendments require review process. This is intentional (it's the entire point of treating the matrix as governed) but adds friction. Methodology codification ADR should specify the amendment cadence + lightweight v1.0→v1.1 process. <!-- spec-lint: allow prose-xref-banned -->
7. **Multi-archetype audits.** Real audits may need weighted combinations of archetypes (e.g., implementation audit = 0.4 conformance + 0.3 adversarial + 0.3 regression). The framework supports this; the projection over the matrix is a linear combination of archetype priors. POC need not exercise this; v1.x can.

---

## §8 References

- **Auer, P., Cesa-Bianchi, N., Fischer, P. (2002).** *"Finite-time Analysis of the Multiarmed Bandit Problem."* Machine Learning 47.
- **Bach, J., Bolton, M.** *Rapid Software Testing* methodology. Regression-suite vs exploratory testing pattern.
- **Berger, J. O. (1985).** *Statistical Decision Theory and Bayesian Analysis.* 2nd ed. Springer. Utility function as task-specific input.
- **Böhme, M., Pham, V.-T., Roychoudhury, A. (2017).** *"Coverage-based Greybox Fuzzing as Markov Chain."* IEEE TSE 45(5). Adaptive fuzzing as bandit allocation.
- **Cully, A. & Demiris, Y. (2018).** *"Quality and Diversity Optimization: A Unifying Modular Framework."* IEEE TEVC 22(2). Algorithm/descriptor/quality separation; behaviour-descriptor selection as hardest design choice.
- **DeMillo, R., Lipton, R., Sayward, F. (1978).** *"Hints on Test Data Selection: Help for the Practicing Programmer."* Computer 11(4). Foundational mutation testing.
- **Just, R., Jalali, D., Inozemtseva, L. et al. (2014).** *"Are Mutants a Valid Substitute for Real Faults in Software Testing?"* FSE 2014. Modern mutation testing.
- **Krippendorff, K.** *Content Analysis: An Introduction to Its Methodology.* 4th ed. SAGE. Inter-rater reliability (α).
- **Langford, J. & Zhang, T. (2007).** *"The Epoch-Greedy Algorithm for Contextual Multi-armed Bandits."* NIPS 2007.
- **Lehman, J. & Stanley, K. O. (2011).** *"Abandoning Objectives: Evolution through the Search for Novelty Alone."* Evolutionary Computation 19(2). Archive vs frontier in novelty-search.
- **MacKay, D. J. C. (1992).** *"Information-Based Objective Functions for Active Data Selection."* Neural Computation 4(4). Bayesian experimental design.
- **Mouret, J.-B. & Clune, J. (2015).** *"Illuminating Search Spaces by Mapping Elites."* arXiv 1504.04909. Original MAP-Elites; behaviour descriptor specified up front.
- **Pierrot, T., Macé, V., Chalumeau, F. et al. (2022).** *"Multi-Objective Quality Diversity Optimization."* GECCO 2022. MOME: per-cell Pareto fronts; hypervolume as QD-score.
- **Pugh, J. K., Soros, L. B., Stanley, K. O. (2016).** *"Quality Diversity: A New Frontier for Evolutionary Computation."* Frontiers in Robotics & AI 3. Canonical coverage + QD-score dual.
- **Settles, B. (2009).** *Active Learning Literature Survey.* Computer Sciences Technical Report 1648, University of Wisconsin-Madison.
- **Stock, W. (2025).** *"Quality-Diversity Optimization: A Review."* WIREs Computational Statistics. Behaviour descriptor as domain-specific design choice.
- **Thompson, W. R. (1933).** *"On the Likelihood that One Unknown Probability Exceeds Another in View of the Evidence of Two Samples."* Biometrika 25. Thompson sampling.
- **Semantic Versioning Specification.** semver.org.

(Anthropic constitutional AI + Madry et al. adversarial ML are referenced narratively; cite via Anthropic publications + Madry, Makelov, Schmidt, Tsipras, Vladu 2018 "Towards Deep Learning Models Resistant to Adversarial Attacks" arXiv 1706.06083.)
