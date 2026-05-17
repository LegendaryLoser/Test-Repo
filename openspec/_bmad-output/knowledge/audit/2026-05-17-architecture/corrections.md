# META- audit corrections log

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative.

**Companion documents:**
- [`consolidated.md`](consolidated.md) — the thematic clustering this log corrects
- [`qd-triage.md`](qd-triage.md) — the σ × κ triage this log corrects
- [`findings-index.md`](findings-index.md) — the provenance ledger this log corrects
- [`findings/META-findings.md`](findings/META-findings.md) — the source `META-` audit deliverable from which these corrections derive

**Purpose.** The Wave-5 `META-` stream (reasoning-tree meta-auditor; 19 findings: 4 CRIT / 12 SER / 3 PROC) was run against the existing 35-stream audit corpus per the method described in arXiv 2602.09341. Its deliverable identifies specific defects in `consolidated.md`, `qd-triage.md`, and `findings-index.md`. This log applies those corrections in an append-only audit-of-the-audit trail, rather than silently rewriting the affected sections — preserving provenance (the original framings remain readable in their source files), making the corrections individually traceable to a META- finding, and modelling the correction protocol the methodology codification ADR will need.

**Convention.** Each entry below lists:
- The `META-` finding ID
- The defect (verbatim summary)
- The affected file/section
- The correction (what to read instead of the original framing)
- Status: `applied` (correction is mechanically also applied in-line to the affected file with a pointer back to this log), `annotate` (correction lives in this log only; the original framing in the source file is incorrect but not silently overwritten), or `defer` (correction requires methodology ADR or further analysis before application)

---

## CRIT-class corrections (4)

### META-CRIT-001 — THEME-P misattribution to PROSE

**Defect.** `qd-triage.md` §3.1 row 10 (PROSE) credits PROSE as "sole on P (paper citation)" and §6 Wave-1 themes table row P names PROSE as κ-source for THEME-P. `PROSE-findings.md` contains zero references to "the paper" or any equivalent. Verified surfacers per `consolidated.md` THEME-P constituent list: `IND-PROC-07, ADVS-CRIT-05, STRUCT-14, INHER-03, ADVO-SER-01`.

**Correction.** PROSE is NOT sole-source for THEME-P. Actual κ contribution from PROSE is via THEME-D (Hook implementation; PROSE-09) and THEME-B (Trailer schema; PROSE-03), not THEME-P. PROSE's Tier-B status may still hold on cell-uniqueness grounds (only Wave-1 prose-editorial stream) but its κ count drops by 1 sole-theme.

**Status:** `annotate`. The qd-triage.md text is preserved unedited; readers should treat this log as authoritative for the THEME-P attribution. (Surgical inline edit deferred to the qd-triage re-issue alongside Wave 5 §3.5 in the next consolidation commit.)

### META-CRIT-002 — `findings-index.md` structurally incomplete (Wave 4 missing entirely)

**Defect.** `findings-index.md` documents Wave 1, 2, 3 only (28 streams, ~559 raw findings). The "Grand total (all 28 streams)" row is wrong by 8 streams (~141 findings). Every Wave-4 theme (THEMES AAA-SSS, TTT, UUU, VVV, WWW, XXX) is cited in `consolidated.md` and `qd-triage.md` but has no constituent-finding listing in the index.

**Correction.** `findings-index.md` was updated in this commit to add a Wave 4 per-stream tally (8 rows: RED2, RETRO2, EDGE2, INHER2, VALID2, PREM2, STAKE, COUNTER) and a Wave 5 per-stream tally (4 rows: GOV, SEC, GOVDEV, META). The "Grand total" row was updated to reflect 40 streams (35 sub-agent + ARCH in-context + 4 Wave 5). The per-theme constituent-finding listing for Wave-4 and Wave-5 themes is deferred to the next consolidation pass — it requires a finding-by-finding re-cluster against the full theme set, which is the same scope as Wave-5 thematic consolidation generally.

**Status:** `applied` (per-stream tallies); `defer` (per-theme constituent listings for Waves 4-5 → next consolidation commit).

### META-CRIT-003 — FIRST-CRIT-01 is a self-inflicted method artifact

**Defect.** `FIRST-findings.md` opens with the assertion "ADR-0003 exists but was not in the 15 documents listed. I will not read it," and constructs its lead CRITICAL finding (`FIRST-CRIT-01`) on this premise. The FIRST prompt explicitly listed "ADR-0001 through ADR-0008" (which includes ADR-0003); the file `ADR-0003-appscript-runtime.md` is present on disk. FIRST misread its own prompt. `findings-index.md` cryptically notes "(+1 methodology artifact)" but does not name the artifact; `qd-triage.md` §3.2 still credits FIRST with σ = 0.55 and Tier A.

**Correction.** `FIRST-CRIT-01` is retracted from any theme it was placed in (it does not appear in any of THEMES A-SSS's constituent-finding listings, so the retraction is local to the FIRST stream only). FIRST's Tier-A admission is unaffected — it rests on FIRST-CRIT-02..05 + the 4 sole themes (II, KK, LL, NN), none of which depend on FIRST-CRIT-01. The "(+1 methodology artifact)" annotation in `findings-index.md` is updated to "(+1 methodology artifact: FIRST-CRIT-01, ADR-0003 misread)" so future re-clusterers know which finding to exclude.

**Status:** `applied` (annotation in `findings-index.md`); `annotate` (retraction recorded here for FIRST-CRIT-01 specifically).

### META-CRIT-004 — STAKE / COUNTER raw-count inflation in qd-triage.md

**Defect.** `qd-triage.md` §3.4 row 35 (STAKE) reports "~25" raw findings. `STAKE-findings.md` in-file summary states "Total: 20 findings." The ~25 number is inflated by ~25%. COUNTER's "~20" cannot be reconciled with the numbered sections of `COUNTER-findings.md` (count not in the source). These numbers feed σ which feeds Tier assignment; per `qd-triage.md` §2.2's stated ±10pp uncertainty, counting errors of this magnitude exceed the documented band.

**Correction.** STAKE raw findings: **20** (not ~25). COUNTER raw findings: re-count from `COUNTER-findings.md` deferred to the next consolidation pass. Implications for σ: STAKE's σ ≈ 10 themes / 20 findings = 0.50 (was reported 0.80) IF σ is computed against theme-membership-only as the §2.2 definition reads. If σ is computed against the broader "findings ending up in named clusters" definition, the original 0.80 may still hold — the ambiguity in the σ definition itself is a META- meta-finding that this log surfaces.

**Status:** `annotate` for STAKE count; `defer` for COUNTER count + σ re-computation (next consolidation pass under qd-triage §3.5 re-issue).

---

## SER-class corrections (12)

### META-SER-001 — COURSE/CHECK Tier-D demotion uses a strictly-weaker κ estimator

**Defect.** `qd-triage.md` §3.3 rows 26 (COURSE) and 27 (CHECK) recommend Tier-D demotion on grounds of "κ ≈ 0." Inspection: COURSE-CRIT-01 and COURSE-PROC-10 appear as co-surfacers in `consolidated.md` THEME-BB; CHECK-CRIT-04 sharpens THEME-Q's "advisory vs blocking" framing. The sole-theme-count estimator under-counts co-surfacer contributions; §2.3 itself acknowledges this is "strictly weaker than greedy ablation."

**Correction.** Tier-D demotion for COURSE/CHECK is NOT cancelled — the methodological grounds for tier demotion (cell saturation + low marginal coverage) still hold — but the κ ≈ 0 claim should be re-stated as "κ ≈ 0 sole + N co-surfacer" where N is enumerated per stream. Full greedy ablation (per §2.3) is deferred to the methodology ADR's red-test phase; until then, Tier-D demotion remains a recommendation, not a finding.

**Status:** `annotate`. Tier-D recommendation stands per the original §3.3 caveat ("deprecation deferred for implementation-audit confirmation"); the κ claim is sharpened here.

### META-SER-002 — THEME-Z over-cardinalized (two surfaces, not three)

**Defect.** `consolidated.md` THEME-Z claims `commit-trailers-valid` has "three contradicted trigger surfaces (pre-receive, pre-commit, PreToolUse)." Verification against `ADR-0008-ci-gates-and-phase-exits.md` §5: "`commit-trailers-valid` runs **pre-commit** and rejects malformed messages before they enter history." The "pre-receive" framing traces to `PROSE-03`'s parenthetical and stream derivations (ARCH-SER-08, ADVS-CRIT-02, READY-03, ADVH-SER-08); ADR-0008 §1 does not in fact name pre-receive for this gate.

**Correction.** THEME-Z is real (trigger surfaces are inconsistently named) but mis-cardinalized. Correct framing: "**two** trigger surfaces (pre-commit per ADR-0008 §5; `PreToolUse(Bash:git commit)` per ADR-0005 §6) plus **one stream-introduced misreading** (pre-receive)." The rolled-into-THEME-B disposition stands.

**Status:** `annotate`. THEME-Z severity unchanged (CRITICAL); cardinality framing corrected here.

### META-SER-003 — THEME-X under-counted (Wave-4 STAKE confirmation never folded back)

**Defect.** `consolidated.md` THEME-X reports "Streams: 1/12 · Constituent findings: 1" with attribution to PREM-07 alone. Wave-4 `STAKE-PROC-020` is a near-identical formulation ("'atomic REQ' rule + append-only-with-supersession + immutable IDs → guaranteed monotonic spec-file growth"). The "1/12" count was never updated when Wave 4 added STAKE.

**Correction.** THEME-X actual: **Streams: 2/40 · Constituent findings: 2 (PREM-07, STAKE-PROC-020).** Convergence tier: Tier B (was Tier C — two independent surfacers from different methods + waves). The "11 other streams missed it because they review the current 0-REQ state" interpretation is partially falsified; STAKE's persona-forward-looking lens also surfaced the long-horizon dynamics.

**Status:** `annotate` (this log) + applied inline as a minor correction to the THEME-X count in `consolidated.md` (see the THEME-X annotation appended in this commit).

### META-SER-004 — STAKE cell mis-assignment (single cell understates κ)

**Defect.** `qd-triage.md` §3.4 row 35 places STAKE in cell `(persona, forward, exhaustive, security/ops + cost/value)`. STAKE's actual stakeholder lens spans compliance auditor (current-state framework assessment) and future-architect ("in 3 years" retrospective-from-future) — Axis B (temporal) is not uniformly "forward."

**Correction.** STAKE's true behavioural signature spans `(persona × {current, forward, post-hoc} × exhaustive × {security/ops, cost/value, governance})`. Single-cell-assignment under-attributes STAKE's κ for the Axis-B coverage it provided. Tier-A admission is unaffected; cell-occupancy attribution should record STAKE as occupying three Axis-B cells (with weighted occupancy, per a refinement to the QD admission rule that the methodology ADR should consider).

**Status:** `defer` to methodology ADR's cell-occupancy model. Annotated here.

### META-SER-005 — THEME-S over-generalizes "structurally unreachable"

**Defect.** `consolidated.md` THEME-S claims "PHASE-5 is structurally unreachable." Of 5 constituent findings, only PARTY-PROC-01's "build the cathedral, then wonder if anyone wants to pray" framing makes the structural-unreachability claim. ARCH-SER-12, ADVO-SER-08, READY-04 merely state product content is undelivered. ARCHITECTURE.md §12 explicitly says product content is out of scope; no architectural rule prohibits a separate product PR.

**Correction.** Re-frame THEME-S as "PHASE-5 entry requires product content that no PHASE delivers, and no upstream-of-PHASE-5 ceremony coordinates the product-content PR with the infrastructure phases." This is the weaker, factually defensible claim. The "structurally unreachable" framing is retracted; the underlying scheduling gap is preserved.

**Status:** `annotate`. THEME-S severity unchanged (SERIOUS); claim language softened.

### META-SER-006 — THEME-V conflates pre-mortem hypothetical with present-tense defect

**Defect.** `consolidated.md` THEME-V cites PREM-17 ("TEA dropped PM's 'TBD' hedge, shipped wrong REQ green") as evidence the architecture "treats agents as workflow steps, not as actors whose outputs require provenance." PREM-17 is a hypothetical about a TEA workflow that does not yet exist (PHASE-5 is unimplemented). The theme aggregates a forward-looking pre-mortem about an unimplemented system into a present-tense defect.

**Correction.** Reframe THEME-V: "inter-agent provenance is unaddressed in the architecture; pre-mortem (PREM-17) demonstrates this in a hypothetical TEA workflow, party-mode (PARTY-UX-01/02) demonstrates this in the diagnostic-format gap." Recommended-CHG "ADR for inter-agent provenance" is still actionable today (the absence is a present-tense documentation gap) but the failure-mode evidence is contingent on PHASE-5's eventual delivery.

**Status:** `annotate`. THEME-V severity unchanged.

### META-SER-007 — THEME-WW exceeds MARY's source claim

**Defect.** `consolidated.md` Wave-3 supplement THEME-WW says "ADR-0005 is interchangeable — used determinism and idempotence interchangeably." Verification against `ADR-0005-traceability-and-journaling.md`: the words "determinism" and "idempotence" each appear at most once; the ADR uses "regenerated"/"derived cache" and "discarded by the parser." There is no demonstrated interchangeable usage. The theme framing exceeds what MARY-SER-12 actually demonstrates.

**Correction.** Re-frame THEME-WW as "MARY-SER-12 raised determinism-vs-idempotence as a vocabulary question; ADR-0005 does not use either word frequently enough to demonstrate interchangeability, but also does not pin the distinction explicitly when discussing matrix derivation." Tier-B admission for MARY may rest on weaker evidence than the original theme writeup suggested.

**Status:** `annotate`. Tier-B for MARY held under the cell-rarity rule; re-examine in next σ × κ pass.

### META-SER-008 — `(attitudinal × current-state)` over-saturation count double-counts cells

**Defect.** `qd-triage.md` §4.1 declares `(attitudinal, current-state)` "OVER-SATURATED" with 12 methods. Listed methods include VALID and VALID2 (both also under `(attitudinal × current × exhaustive × governance)`), EDGE and EDGE2 (both also under `(attitudinal × current × exhaustive)`). The 12 count double-counts cell occupants whose dominant Axis-C decomposition style separates them.

**Correction.** True per-cell counts (no double-counting): `(attitudinal × current × holistic × blocking)` = 5 (ARCH/IND/ADVO/ADVS/ADVH); `(attitudinal × current × exhaustive × blocking)` = 3 (EDGE/EDGE2/READY); `(attitudinal × current × exhaustive × governance)` = 2 (VALID/VALID2); `(attitudinal × current × focused × blocking)` = 3 (MARY/COURSE/CHECK). The over-saturation claim still holds in two cells (the first two) but the Tier-D demotion prescription should rest on the per-cell count, not the over-the-Lens-×-Temporal cell count.

**Status:** `annotate`. Tier-D recommendations for COURSE/CHECK/VALID2 not cancelled; rationale tightened here.

### META-SER-009 — Convergence-projection model in consolidated.md falsified by Wave 4

**Defect.** `consolidated.md` "Convergence projection" predicted "Wave 4: ~15-20% marginal novelty." Actual Wave-4 marginal novelty was ~46% (reported in the same document). The projection model is empirically falsified by data in the same artifact. Neither `consolidated.md` nor `qd-triage.md` retract the projection model.

**Correction.** The original projection model is retracted. The QD framework's ACGR-based projection in `qd-triage.md` §7 (~45% Wave 4 ACGR; predicted Wave 5 ~10-15%, Wave 6 <5%) is the replacement; ACGR is invariant to method admission (unlike raw marginal novelty), so the new projection is more defensible. The Wave-4 prediction error is the empirical motivation for the QD framework adoption.

**Status:** `applied` implicitly via the QD adoption (qd-triage.md §1 already names this falsification as the motivation). This log makes the retraction explicit.

### META-SER-010 — THEME-N cluster larger than verified evidence

**Defect.** `consolidated.md` THEME-N ("ARCHITECTURE.md as summary-of-summaries") clusters one verified drift instance (STRUCT-03's ADR-0005 §8 row missing in ARCHITECTURE.md §8) into a broader category ("silent drift") with no second verified instance. STRUCT-03 is correct; the generalisation to "every summary section silently rots" is not demonstrated.

**Correction.** Re-frame THEME-N as "one verified drift instance (STRUCT-03) plus several structural risk patterns (STRUCT-06 inline-rationale ownership; STRUCT-12 epic-reconciliation gate; STRUCT-15 four-tier wording divergence) that share the summary-of-summaries shape but have not been independently verified to have drifted." The recommended CHG (reduce summary sections to pointers) is still actionable; the empirical claim is narrower.

**Status:** `annotate`.

### META-SER-011 — PAIGE κ count inflated by 1

**Defect.** `qd-triage.md` §3.3 row 24 credits PAIGE with "sole on SS, TT, ZZ (3 themes)." `findings-index.md` THEME-ZZ row lists `PAIGE-SER-01, SALLY-SERIOUS-06` — co-surfacer pair, not PAIGE-sole. `qd-triage.md` §3.1 STRUCT row says "ZZ partial" for SALLY — confirming co-surface.

**Correction.** PAIGE: **2 sole themes (SS, TT) + 1 co-surfaced (ZZ with SALLY).** Tier-A admission for PAIGE is unaffected (sole-source on 2 themes + cell-rarity in narrative lens). κ count revised from 3 to 2.

**Status:** `applied` via this log (qd-triage.md row 24 inline edit deferred to next §3.5 re-issue).

### META-SER-012 — STAKE-CRIT-001 severity calibration

**Defect.** `STAKE-CRIT-001` framing ("ADR-0008 §6 does not require signed commits — it merely forbids unsigning them") is factually correct, but ADR-0008 §6 is titled "Bypass discipline" — its scope is bypass-forbidding, not signing-mandating. A missing-feature finding (no signing ADR exists) is SER per architecture's own claims, not CRIT.

**Correction.** STAKE-CRIT-001 should be re-classified STAKE-SER-001. THEME-AAA in `consolidated.md` Wave-4 supplement (the cluster it sits in) should reflect the corrected severity. Other STAKE CRITs (002 secrets management, 004 SRE on-call, 005 observability) are unaffected.

**Status:** `annotate`. (Severity re-classification deferred to the next consolidation pass; the corrected severity is recorded here.)

---

## PROC-class corrections (3)

### META-PROC-001 — ACGR denominator precision exceeds estimate uncertainty

**Defect.** `qd-triage.md` §2.6 + §7 compute ACGR percentages (45%, 22%, 45%) to two significant figures against a "~55 meaningful cells" denominator estimate. §11 acknowledges the estimate is unverified. Precision exceeds the underlying estimate.

**Correction.** ACGR figures should be reported with explicit uncertainty bands. E.g., Wave 4 ACGR = 45% ± 10% (Δ = 25 ± 0 archive growth; denominator = 55 ± 10 meaningful cells). Convergence criterion (ACGR < 5%) is robust to denominator uncertainty in the small-Δ limit, but Pareto-frontier admission per cell is sensitive. Formal enumeration of meaningful cells is required before the methodology ADR locks the denominator.

**Status:** `defer` to methodology ADR. Limitation acknowledged here.

### META-PROC-002 — Anonymous citation hazard for arXiv 2602.09341

**Defect.** `qd-triage.md` §1.3 cites "Auditing Multi-Agent LLM Reasoning Trees Outperforms Majority Vote and LLM-as-Judge (2026 arXiv 2602.09341)." No stream pinned down authors, title beyond corpus-internal naming, or DOI. The audit corpus reproduces the exact anonymous-authority failure mode that THEME-P diagnoses in the underlying architecture artifact.

**Correction.** The arXiv ID 2602.09341 should be replaced with full bibliographic data (authors, year, DOI or arXiv URL) in `qd-triage.md` §1.3 before the methodology ADR is authored. If the citation cannot be resolved to an actual paper, the methodological claim it supports must rest on the in-corpus implementation (the META- stream's own deliverable) rather than on the cited source.

**Status:** `defer` to methodology ADR drafting. Hazard logged here.

### META-PROC-003 — σ precision exceeds documented ±10pp uncertainty

**Defect.** `qd-triage.md` §3 reports per-method σ to two decimal places (0.55, 0.65, 0.70, etc.). §2.2 admits ±10pp uncertainty. When σ-gaps between methods (e.g., MARY 0.65 vs PM 0.70) fall within the uncertainty band, Pareto-dominance claims are not statistically distinguishable.

**Correction.** σ should be reported to one decimal place at most, with explicit uncertainty bands. Tier-admission decisions that rest on σ-comparisons within ±0.10 should be marked as "ambiguous" rather than asserted. The Pareto frontier for cells with multiple methods needs ablation-grade σ measurement, not theme-membership-rate approximation, before the methodology ADR codifies the tier rules.

**Status:** `defer` to methodology ADR's measurement-discipline section + the audit-meta-test suite.

---

## Summary

| Severity | Count | Applied | Annotate-only | Deferred |
|---|---|---|---|---|
| CRIT | 4 | 2 (CRIT-002 partial via findings-index, CRIT-003 partial) | 2 (CRIT-001, CRIT-004) | 0 |
| SER | 12 | 2 (SER-003 inline, SER-009 implicit via QD adoption) | 9 | 1 (SER-004 to ADR) |
| PROC | 3 | 0 | 0 | 3 (all to methodology ADR) |
| **Total** | **19** | **4** | **11** | **4** |

**Next-session sequencing.** Per `STATUS.md` "Next session: start here": this log is the FIRST output of the consolidation step. The remaining work (Wave-5 thematic consolidation in `consolidated.md`; qd-triage.md §3.5 per-method σ × κ for the 4 new streams; ACGR re-measurement; Wave-6 decision) should incorporate these corrections — specifically, the qd-triage.md §3.5 re-issue should fold in the annotated PROSE/PAIGE/STAKE/COUNTER κ adjustments and the STAKE cell-occupancy refinement.
