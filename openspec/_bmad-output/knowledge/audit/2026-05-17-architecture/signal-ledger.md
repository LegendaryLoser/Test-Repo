# Signal ledger — 2026-05-17 architecture audit

**Status:** STAGING (per [`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7). Non-authoritative.

**Companion documents:**
- [`README.md`](README.md) — audit session metadata
- [`consolidated.md`](consolidated.md) — thematic clustering (~149 themes across Waves 1-7)
- [`findings-index.md`](findings-index.md) — per-stream provenance ledger
- [`qd-triage.md`](qd-triage.md) — per-method σ × κ scoring
- [`corrections.md`](corrections.md) — META- audit-of-the-audit corrections (19 entries)

**Purpose.** Apply the §2.2 signal filter from `qd-triage.md` (concreteness + actionability + non-method-artifact) to every finding in the corpus, deduplicate across streams, identify contradictions, and surface the underlying unique-claim cluster set. This is the empirical foundation for the methodology codification ADR's §6 (measurement discipline) and for the cell-labeling/pruning decision the next consolidation pass will make.

**Method.** 4 parallel subagents classified all 867 sub-agent findings (47 streams across 7 waves; the in-context `ARCH-` 31 findings are not classified here). Each finding received one of seven labels: SIGNAL / DUPLICATE_OF / CONTRADICTS / METHOD_ARTIFACT / NOT_ACTIONABLE / NOT_CONCRETE / OUT_OF_SCOPE. Cross-batch duplicates were flagged separately by each subagent and reconciled in this aggregation pass.

---

## §1 Headline numbers

| Metric | Count |
|---|---|
| Total sub-agent streams | 47 |
| Total sub-agent findings classified | 867 |
| Within-batch SIGNAL | 861 (99.3%) |
| Within-batch non-SIGNAL | 6 |
| Cross-batch LIKELY-DUPLICATE flags | ~210 (24%) |
| Hard contradictions identified | 1 |
| Framing-difference quasi-contradictions | 1 |
| **Unique-claim clusters identified** | **42** |
| Long-tail singleton claims | ~80-110 |
| **Effective unique architecture defects (clusters + singletons)** | **~120-150** |

**Key finding.** The 99.3% within-batch SIGNAL rate is misleading. The corpus has massive cross-batch redundancy: 210 findings (24%) were flagged as likely-duplicates of findings in other batches, and the underlying unique-claim space resolves to ~42 dense clusters + ~80-110 long-tail singleton claims. **The audit's effective discovery surface is ~120-150 unique architecture defects, not ~867 findings.**

This has direct implications for the QD matrix:
- The ~149 themes in `consolidated.md` over-count the unique defect surface by ~1.0-1.2× (themes are reasonably close to unique-claim count, but several themes are themselves duplicates after cross-wave alignment).
- ACGR computed against per-finding counts is inflated relative to ACGR against unique claims.
- The convergence threshold question may be much closer to resolution than the ~91%/~105%/~87% ACGR series suggested — the audit may have already largely converged on the unique-claim set, and recent waves have been refining framings rather than discovering new defects.

---

## §2 Per-stream true σ (after cross-batch deduplication)

True σ = (within-batch SIGNAL count that is NOT cross-batch-flagged-as-dup) / (total findings in stream). Cross-batch flags listed in the source ledgers count the finding as dup IF it points outward (i.e., this stream's finding duplicates an earlier-wave stream's finding).

| Wave | Stream | Total | Within-batch SIGNAL | Cross-batch dup-outward | True σ (unique-signal) |
|---|---|---|---|---|---|
| 1 | ADVH | 15 | 15 | ~7 | ~53% |
| 1 | ADVO | 25 | 25 | ~13 | ~48% |
| 1 | ADVS | 18 | 18 | ~10 | ~44% |
| 1 | EDGE | 44 | 44 | ~3 | ~93% |
| 1 | IND | 27 | 27 | ~2 | ~93% |
| 1 | INHER | 22 | 22 | ~15 | ~32% |
| 1 | PARTY | 22 | 22 | ~6 | ~73% |
| 1 | PREM | 18 | 18 | ~1 | ~94% |
| 1 | PROSE | 14 | 14 | ~3 | ~79% |
| 1 | READY | 19 | 19 | ~2 | ~89% |
| 1 | STRUCT | 15 | 15 | ~6 | ~60% |
| 2 | AME | 20 | 20 | ~10 | ~50% |
| 2 | DISTILL | 15 | 15 | ~7 | ~53% |
| 2 | FIRST | 15 | 14 | ~3 | ~73% |
| 2 | RED | 16 | 16 | ~2 | ~88% |
| 2 | RETRO | 19 | 19 | ~6 | ~68% |
| 2 | SOC | 19 | 19 | ~5 | ~74% |
| 2 | VALID | 18 | 18 | ~7 | ~61% |
| 2 | WIN | 22 | 22 | ~7 | ~68% |
| 3 | CHECK | 16 | 16 | ~7 | ~56% |
| 3 | COURSE | 12 | 12 | ~6 | ~50% |
| 3 | DEVIL | 16 | 16 | ~2 | ~88% |
| 3 | EDIT | 24 | 24 | ~10 | ~58% |
| 3 | MARY | 22 | 21 | ~8 | ~59% |
| 3 | PAIGE | 19 | 19 | ~6 | ~68% |
| 3 | PM | 20 | 20 | ~1 | ~95% |
| 3 | SALLY | 17 | 17 | ~6 | ~65% |
| 4 | COUNTER | 15 | 15 | ~2 | ~87% |
| 4 | EDGE2 | 17 | 17 | ~3 | ~82% |
| 4 | INHER2 | 17 | 17 | ~3 | ~82% |
| 4 | PREM2 | 14 | 13 | ~1 | ~86% |
| 4 | RED2 | 12 | 12 | ~0 | 100% |
| 4 | RETRO2 | 13 | 13 | ~1 | ~92% |
| 4 | STAKE | 20 | 20 | ~6 | ~70% |
| 4 | VALID2 | 14 | 14 | ~3 | ~79% |
| 5 | GOV | 22 | 22 | ~7 | ~68% |
| 5 | SEC | 21 | 21 | ~2 | ~90% |
| 5 | GOVDEV | 22 | 22 | ~3 | ~86% |
| 5 | META | 19 | 19 | ~0 | 100% |
| 6 | STRUCTGOV | 22 | 22 | ~0 | 100% |
| 6 | SECDISTILL | 16 | 16 | ~12 | ~25% |
| 6 | SCENNOW | 20 | 20 | ~1 | ~95% |
| 6 | PERSRETRO | 17 | 17 | ~2 | ~88% |
| 7 | SCENFUT | 18 | 18 | ~1 | ~94% |
| 7 | STRUCTFUT | 18 | 17 | ~2 | ~83% |
| 7 | DEVRETRO | 18 | 18 | ~3 | ~83% |
| 7 | ATTFUT | 18 | 18 | ~3 | ~83% |

**Median true σ: ~73%.** Wave-1 baseline-adversarial streams (ADVH/ADVO/ADVS/INHER) drop into 30-60% true σ — they are largely confirmatory of EDGE/IND/PREM/READY's findings. Wave-4 sonnet permutations sit at 80-90% (sonnet variants did find some new framing). New methods (RED2, META, STRUCTGOV) sit at 90-100% — they cover cells that no prior stream touched. **SECDISTILL at 25% true σ is the lowest** — it largely re-discovered Wave-5 SEC's security findings using compression as the method, which produced overlapping defects.

The substantial gap between within-batch σ (99.3%) and median true σ (~73%) is the **redundancy tax** of running many streams against the same artifact. This is consistent with the QD framework's expectation (Wave-1 adversarial-general baseline streams ARE supposed to be confirmatory; the value is convergence-on-truth, not unique-discovery).

---

## §3 Non-SIGNAL findings (6 within-batch)

| ID | Classification | Source |
|---|---|---|
| FIRST-CRIT-01 | METHOD_ARTIFACT | FIRST misread its own prompt re: ADR-0003 (which WAS in the listed 15 documents); finding rests on the false premise that ADR-0003 is missing. Pre-flagged in [`corrections.md`](corrections.md) META-CRIT-003. |
| PREM2-PROC-009 | NOT_CONCRETE (effectively method artifact) | Same ADR-0003 misreading; PREM2 inherited FIRST's confusion. CONTRADICTS META-CRIT-003 — PREM2 is the incorrect side; META's verification (ADR-0003 exists) is correct. |
| MARY-SERIOUS-12 | METHOD_ARTIFACT | THEME-WW claim ("determinism vs idempotence interchangeable in ADR-0005") exceeds what ADR-0005 actually says — verified per [`corrections.md`](corrections.md) META-SER-007. |
| STRUCTFUT-PROC-018 | DUPLICATE_OF(SCENFUT-CRIT-007) | Same project-overlay-semantics defect, different framing (3-way co-surface with ATTFUT-PROC-016). |
| DEVRETRO-CRIT-002 | DUPLICATE_OF(PERSRETRO-CRIT-001) | Same no-mock-absolutism defect, external "test theatre" reframing. |
| ATTFUT-PROC-016 | DUPLICATE_OF(SCENFUT-CRIT-007) | Same project-overlay-semantics defect, attitudinal framing. |

---

## §4 Contradictions

### §4.1 Hard contradictions (1)

**PREM2-PROC-009 vs META-CRIT-003.** PREM2-PROC-009 asserts that ADR-0003 is absent from the architecture; META-CRIT-003 verified (and is verifiable by inspection of `openspec/architecture/decisions/`) that `ADR-0003-appscript-runtime.md` exists on disk and was in the listed 15 documents. META is correct; PREM2-PROC-009 is retracted (status: METHOD_ARTIFACT, as above). Same defect class as FIRST-CRIT-01 (whose retraction is documented in [`corrections.md`](corrections.md) META-CRIT-003); both streams inherited a misreading of "ADR-0001 through ADR-0008" as excluding ADR-0003.

### §4.2 Framing-difference quasi-contradictions (1)

**PM-CRIT-04 vs DEVIL-PRO-16.** PM frames red-first discipline as foreclosing spike-driven discovery (productivity argument). DEVIL frames phase-exit ordering as serializing work that could be parallel (workflow argument). The two findings target adjacent defects but make compatible claims; not a true contradiction, but the resolution-CHG sequence will need to reconcile them.

---

## §5 Duplicate-claim clusters (the 42 most-replicated defects)

Each cluster is a single underlying defect surfaced by multiple findings across multiple streams. Cluster size is the count of findings in the cluster; the canonical claim is the one-line synthesis.

### Cluster A: bmad/_bmad/wrappers path drift (~18 findings)

ARCHITECTURE.md §3, ADR-0001 §0/§3, ADR-0002 §1, PHASE-1 §Scope all carry different naming for the BMAD substrate (`bmad/` vs `_bmad/`, with/without wrapper directories). Members: IND-CRIT-01, ADVO-CRIT-01, ADVS-PROC-01, INHER-09, PROSE-07, STRUCT-02, READY-01, EDGE-23/24/25, ADVH-0002, DISTILL-01, COURSE-CRIT-03, VALID-CRIT-02, PAIGE-CRIT-04, SOC-CRIT-05, WIN-CRIT-16, EDIT-CRIT-02, STRUCTGOV-CRIT-001. Maps to existing THEME-A.

### Cluster B: ARCH §9 wrappers retired but still referenced (~13 findings)

ADR-0002 Amendment 0001 retired the wrapper layer; ARCHITECTURE.md §9 and PHASE-1 §Scope still reference it. Members: IND-CRIT-02, ADVO-CRIT-02, ADVS-CRIT-04, DISTILL-02, COURSE-CRIT-02, EDIT-CRIT-01, CHECK-CRIT-01, PAIGE-CRIT-01, FIRST-SERI-03, AME-PROCESS-02, IND-CRIT-03, READY-15, INHER2-0005, VALID2-009. Maps to existing THEME-A.

### Cluster C: gate-coverage syntactic-not-semantic / meta-gate fallacy (~16 findings)

`gate-coverage` verifies that a row exists in ADR-0008 §1 referencing each ADR/principle; does not verify the gate actually enforces what the row claims. Members: IND-CRIT-06, IND-SER-01, ADVO-CRIT-04, ADVS-SERI-01, INHER-11, PREM-01, RED-SER-08, WIN-CRIT-10, FIRST-SERI-04, SOC-SER-03, CHECK-PROC-14, CHECK-SER-12, VALID-SERIOUS-15, DISTILL-13, GOVDEV-CRIT-002, DEVRETRO-CRIT-010, GOV-CRIT-005, PREM2-CRIT-002. Maps to existing THEME-C. DEVRETRO-CRIT-010 contributes the canonical "meta-gate fallacy" terminology.

### Cluster D: "the paper" anonymous citation (~11 findings)

ARCHITECTURE.md §2 and ADR-0004 Context cite "a published result on transformer associative memory ('the paper')" with no DOI/arXiv/authors. Self-violates ADR-0004 §2 `prose-xref-banned`. Members: IND-PROC-07, ADVS-CRIT-05, STRUCT-14, INHER-03, WIN-CRIT-01, EDIT-CRIT-03, PAIGE-CRIT-02, SALLY-SERIOUS-07, INHER2-0010, STAKE-CRIT-017, PERSRETRO-PROC-002. Maps to existing THEME-P.

### Cluster E: PHASE-5 §Scope numbering bug (~12 findings)

PHASE-5 has two items numbered "4." (one inserted by amendment without renumbering). Members: STRUCT-10, ADVO-PROC-04, ADVS-SERI-06, PARTY-DOC-06, INHER2-0012, DISTILL-15, SOC-PROC-02, VALID-SERIOUS-13, EDIT-SER-09, COURSE-SER-09, CHECK-PROC-16, PAIGE-PROC-07, STRUCTGOV-SER-008. Maps to existing THEME-Y. **High-density cluster (12 findings for a single typo) is evidence of over-replication; this single defect is over-counted by ~10x.**

### Cluster F: push invariant unenforceable in failure mode (~16 findings)

ADR-0005 §6 Amendment 0001 mandates auto-push but ADR-0005 §8 admits residual loss "if both hooks fail to fire" — push invariant has no out-of-band reconciliation. Members: ARCH-SER-02, ARCH-SER-13 (in-context, not counted), IND-CRIT-08, ADVO-SER-06, ADVH-SER-04, EDGE-16/17/18/42, INHER-08, PREM-02, PARTY-CRIT-01, ADVH-0004, EDGE2-CRIT-005, PREM2-CRIT-001, RETRO2-CRIT-003. Maps to existing THEME-F.

### Cluster G: anti-aliasing threshold undefined/uncalibrated (~13 findings)

ADR-0004 §4 says "threshold and n-gram size are pinned in `tools/spec_lint/config.yaml`" with no actual value, no calibration data, no owner for the quarterly review. Members: AME-SERIOUS-01, WIN-CRIT-05, CHECK-CRIT-04, COURSE-SER-05, MARY-CRIT-07, RETRO-SER-02, VALID-SERIOUS-09, IND-SER-02, ADVO-SER-05, ADVH-0006, RED-SER-11, SCENFUT-CRIT-004, PERSRETRO-SER-001. Maps to existing THEME-Q.

### Cluster H: stochastic N / min-power undefined (~10 findings)

ADR-0007 §3 mandates statistical assertions but doesn't specify minimum N, α, or power. Members: AME-SERIOUS-05, WIN-CRIT-15, CHECK-SER-08, SOC-SER-04, MARY-CRIT-06, ADVO-SER-04, PREM-15, IND-SER-03, RED-SER-12, VALID2-010. Maps to existing THEME-J.

### Cluster I: bulk-green-start N undefined (~9 findings)

ADR-0006 §4's `Bootstrap: <reason>` exemption has no N threshold; "bulk" is undefined. Members: AME-PROCESS-03, CHECK-SER-06, SOC-SER-06, SALLY-SERIOUS-11, MARY-SERIOUS-18, EDGE2-SER-011, PREM2-PROC-014, INHER2-0016, MARY-PROCESS-22. Maps to existing THEME-MM cluster (retroactive remediation).

### Cluster J: checkpoint_exemptions.yaml undefined (~12 findings)

ADR-0008 §6 names `tools/trace/checkpoint_exemptions.yaml` as the authoritative exemption list; file is not in PHASE-0 scope, has no REQ-CI covering it, has no consistency check. Members: WIN-CRIT-12, SALLY-SERIOUS-09, AME-PROCESS-01, PAIGE-PROC-02, DISTILL-08, INHER-22, INHER2-0007, EDGE-39, ADVO-SER-07, READY-11, SEC-PROC-017, ATTFUT-PROC-015.

### Cluster K: stale-staging deferred CHG never registered (~14 findings)

ADR-0002 §7 references a `stale-staging` lint deferred to a CHG that has no ID, no owner, no SLA. Members: FIRST-PROC-02, COURSE-SER-08, PAIGE-PROC-06, SALLY-PROCESS-15, AME-PROCESS-04, ADVH-0003, ADVS-PROC-03, INHER-05, RED2-PROC-010, PREM2-SER-004, PREM2-PROC-013, VALID2-011, INHER2-0013, RETRO2-SER-011.

### Cluster L: ADR-0002 Amendment 0001 = rewrite mislabeled as amendment (~7 findings)

ADR-0002 Amendment 0001 reads "Complete rewrite" — should have been supersession per ADR-0004 §1 immutability rule. Members: COURSE-CRIT-01, EDIT-CRIT-05, WIN-CRIT-20, RETRO-CRIT-07, IND-PROC-01, PARTY-CRIT-03, GOVDEV-CRIT-004.

### Cluster M: REQ-ARCH-* missing frontmatter / wrong format (~7 findings)

ARCHITECTURE.md §10's REQ-ARCH-0001..0008 are prose bullets, not REQ blocks with frontmatter per ADR-0004 §5. Members: MARY-CRIT-05, MARY-PROCESS-19, VALID-SERIOUS-16, STRUCT-07, ADVS-SERI-02, INHER-10, STRUCTGOV-SER-003. Maps to existing THEME-G.

### Cluster N: REQ-ARCH-0007 "verbatim" undefined (~6 findings)

REQ-ARCH-0007 requires CLAUDE.md to cite ARCHITECTURE.md §1 principles "verbatim" — no equality function specified (byte? whitespace-normalized? semantic?). Members: MARY-CRIT-02, VALID-CRIT-05, EDIT-PROC-03, GOVDEV-PROC-019, STRUCTGOV-SER-013, ATTFUT-CRIT-004.

### Cluster O: PHASE-0 unbootstrappable (matrix builder dependency) (~10 findings)

PHASE-0 exit requires `tests-green in matrix` but `rebuild.py` is a PHASE-2 deliverable; circular bootstrap. Members: FIRST-CRIT-02, AME-CRIT-06, WIN-CRIT-13, FIRST-SERI-04, READY-05, EDGE-22, EDGE-36, EDGE2-PROC-014, VALID2-005, GOVDEV-PROC-020. Maps to existing THEME-K.

### Cluster P: Secrets management ADR absent (~6 findings)

No ADR specifies secret storage / rotation / scoping / revocation for Anthropic API key, CI service account, clasp credentials, GitHub MCP token. Members: STAKE-CRIT-002, SEC-CRIT-001, RETRO-CRIT-05, ATTFUT-CRIT-001, SCENNOW-PROC-004, SECDISTILL-CRIT-001. Maps to existing THEME-BBB.

### Cluster Q: Commit signing not required (~3 findings)

`--no-gpg-sign` forbidden but no positive signing requirement; forbidding a non-existent feature is vacuous. Members: STAKE-CRIT-001 (severity should be SER per [`corrections.md`](corrections.md) META-SER-012), SEC-CRIT-003, SECDISTILL-CRIT-004. Maps to existing THEME-AAA.

### Cluster R: Hook sandbox / capability / identity unspecified (~3 findings)

Hooks run arbitrary Python with full ambient privilege; no uid separation, capability list, file allowlist, or egress allowlist. Members: SEC-CRIT-002, SECDISTILL-CRIT-003, RED-CRIT-03. Maps to existing THEME-FFFF (Wave-5).

### Cluster S: BMAD vendored bundle integrity (~6 findings)

No checksum / signature / SLSA-provenance / SPDX-manifest for the 2.4 MB vendored BMAD substrate. Members: STAKE-PROC-010, STAKE-SER-014, STAKE-PROC-016, SEC-CRIT-005, SECDISTILL-CRIT-007, SECDISTILL-CRIT-008. Maps to existing THEMES-FFF (BMAD) + JJJ (Anthropic SDK).

### Cluster T: Journal append-only by convention only (~5 findings)

ADR-0005 §5 declares journal append-only as a property, not enforced by WORM/hash-chain/external-shipment. Members: STAKE-SER-008, SEC-SER-009, SECDISTILL-SER-015, RED-SER-09, FIRST-CRIT-04. Maps to existing THEME-EEE.

### Cluster U: Amendment-vs-supersession threshold missing (~4 findings)

No rule for when an amendment should instead be a supersession; ADR-0002 Amendment 0001 set the precedent that any size of change can be an "amendment." Members: GOV-CRIT-004, GOVDEV-CRIT-004, STRUCTFUT-CRIT-003, PERSRETRO-PROC-004. Maps to existing THEME-UUUU.

### Cluster V: Project-overlay semantics undefined (~7 findings)

ADR-0001 §3 mentions `projects/<project>/openspec/` "extends root specs by reference" — no extend mechanism, no conflict resolution, no namespacing rule. 3-way co-surface in Wave 7. Members: SCENFUT-CRIT-007, STRUCTFUT-PROC-018 (DUP), ATTFUT-PROC-016 (DUP), EDGE2-PROC-013, EDGE-11, IND-PROC-06, INHER-18.

### Cluster W: Incident response / disclosure ADR absent (~7 findings)

No SECURITY.md location, no on-call surface, no rotation runbook, no incident escalation. Members: STAKE-CRIT-004, SEC-PROC-018, SECDISTILL-PROC-012, SCENFUT-SER-014, SCENFUT-PROC-015, ATTFUT-SER-012, DEVRETRO-PROC-016. Maps to existing THEME-CCC (SRE/ops).

### Cluster X: ADR-0008 §1 inventory missing rows (~5 findings)

`skill-removal-acknowledged`, `bmad-version-pin`, `bmad-smoke-test`, `bulk-green-start` named elsewhere but not in the canonical inventory. Members: READY-02, COURSE-SER-07, INHER2-0008, IND-CRIT-07, STRUCTGOV-PROC-005.

### Cluster Y: PHASE-5 product entry impossible / structurally unreachable (~10 findings)

PHASE-5 entry requires `vision.md`, briefs, PRD section, Epic, Story — all "in a separate product PR chain" that no PHASE delivers. Members: READY-04, ADVO-SER-08, ARCH-SER-12 (in-context), PM-CRIT-02, PM-PROC-18, PARTY-PROC-01, INHER-19, EDGE2-PROC-016, VALID2-012, DEVRETRO-SER-014. Maps to existing THEME-S (note: framing was over-stated per [`corrections.md`](corrections.md) META-SER-005; revised claim: "PHASE-5 entry requires undelivered product content with no scheduling ceremony," not "structurally unreachable").

### Cluster Z: Hook glob/pattern ambiguity (`*test*`, `Edit|Write`) (~8 findings)

ADR-0005 §6 hook patterns are syntactically ambiguous. Members: AME-CRIT-01, AME-CRIT-02, AME-CRIT-03, EDGE-27, EDGE-28, READY-06, READY-16, EDGE2-SER-006.

### Cluster AA: settings.json schema / approval (~5 findings)

`.claude/settings.json` declares hooks/permissions; no schema, no diff-review gate. Members: AME-SERIOUS-07, VALID-CRIT-07, VALID-CRIT-08, SEC-SER-014, RETRO-SER-05.

### Cluster BB: Red-first hole at checkpoint commits (~13 findings)

ADR-0005 §7 checkpoint commits + ADR-0006 §4 `red-before-green` interact in undefined ways; checkpoint between red+green is unhandled. Members: IND-SER-05, IND-SER-09, ADVO-SER-07, EDGE-06, EDGE-07, READY-11, INHER-07, PARTY-SER-04, PREM-12, RED-CRIT-03, SOC-CRIT-02, CHECK-CRIT-03, GOVDEV-CRIT-005. Maps to existing THEME-E.

### Cluster CC: Trailer schema fragmentation (~15 findings)

`Tests-Status`, `Bootstrap`, `Material-Architecture-Change`, `Checkpoint`, `Skill-Removal-Acknowledged` defined in different ADRs; no canonical enumeration; `commit-trailers-valid` validates form not content. Members: ARCH-CRIT-04 (in-context), ADVO-SER-02, EDGE-08/09/44, READY-09/10/11, INHER-12/14, PROSE-03, COUNTER-015, GOV-SER-001/002/014, GOVDEV-SER-007, SCENNOW-PROC-017. Maps to existing THEME-B.

### Cluster DD: Cache-hit-regression baseline circular (~4 findings)

`cache-hit-regression` gate compares against "baseline" not defined; baseline is the cache-hit-rate which the gate is meant to protect. Members: WIN-CRIT-14, CHECK-SER-07, VALID-SERIOUS-11, MARY-CRIT-08. Maps to existing THEME-J.

### Cluster EE: ARCHITECTURE.md ↔ ADR-0005 §8 failure-mode tables drift (~5 findings)

ARCHITECTURE.md §8 table is missing the post-amendment row from ADR-0005 §8; same table, different content. Members: STRUCT-03, DISTILL-03, EDIT-PROC-07, PAIGE-SER-06, SECDISTILL-SER-005. Maps to existing THEME-N.

### Cluster FF: PHASE-1 references retired wrappers (~6 findings)

PHASE-1 §Scope includes wrapper-layer deliverables retired by ADR-0002 Amendment 0001. Members: IND-CRIT-03, READY-15, EDGE-23, ADVO-PROC-03, INHER2-0005, VALID2-009. (Overlaps with Cluster B but tighter PHASE-1-specific framing.)

### Cluster GG: REQ-ARCH-0008 stale relative to amended hook set (~3 findings)

REQ-ARCH-0008 enumerates hooks but ADR-0005 §6 Amendment 0001 added `PostToolUse(mcp__github__merge_pull_request)`; REQ-ARCH-0008 not updated. Members: COURSE-CRIT-04, EDIT-CRIT-07, EDGE-26.

### Cluster HH: "Phase-0 re-gate" undefined (~4 findings)

ARCHITECTURE.md §0 preamble mentions a "Phase-0 re-gate" triggered by `Material-Architecture-Change` trailer; procedure, scope, exit criteria all undefined. Members: GOV-PROC-003, INHER2-0001, ATTFUT-CRIT-003, PERSRETRO-SER-005.

### Cluster II: Matrix scaling / journal retention (~5 findings)

`rebuild.py` walks full history; no incremental path; gitignored journals grow unbounded. Members: SCENFUT-CRIT-016, SCENFUT-PROC-018, ATTFUT-PROC-017, STAKE-PROC-020, PREM-07. Spans existing THEMES-X + new THEME-EEEEEE/GGGGGG.

### Cluster JJ: Network egress unbounded (~3 findings)

7 outbound destinations (Anthropic, Sheets/Drive, Apps Script, clasp, GitHub MCP, BMAD upstream, origin) with no allowlist or egress proxy. Members: SEC-SER-013, SECDISTILL-CRIT-011, STAKE-SER-012 (partial).

### Cluster KK: Threat model document absent (~3 findings)

No STRIDE / LINDDUN / trust boundary diagram. Members: SEC-SER-010, SECDISTILL-PROC-014, RED-CRIT-01 (partial).

### Cluster LL: ADR amendment-log conventions inconsistent (~4 findings)

ADR-0002 has unnumbered "Amendment log" trailing section; ADR-0005 has numbered "§10 Amendment log"; other 6 ADRs have no amendment-log section at all. Members: STRUCT-04, STRUCT-05, PARTY-DOC-03, STRUCTGOV-PROC-003. Maps to existing THEME-M.

### Cluster MM: ARCHITECTURE.md as summary-of-summaries / drift (~5 findings)

§7, §8, §3 contain summary tables/comments duplicating ADR content; no cross-document equality lint. Members: STRUCT-03, STRUCT-06, STRUCT-08, STRUCT-12, STRUCT-15. Maps to existing THEME-N. Note [`corrections.md`](corrections.md) META-SER-010 narrows this cluster to STRUCT-03 as the one verified instance.

### Cluster NN: Agent identity not in commit trailers (~3 findings)

No trailer distinguishes agent commits from human commits; incident-response blast-radius scoping impossible. Members: SEC-SER-008, RETRO2-CRIT-007, RED2-CRIT-001 (partial). Maps to existing THEME-TTT (Wave-4 RETRO2).

### Cluster OO: Real-vs-fake adapter line / no-mock ambiguity (~6 findings)

ADR-0006 §2 bans in-repo mocks; "real adapter" boundary undefined; nock-replay carve-out contradicts ADR-0007. Members: MARY-SERIOUS-11, DISTILL-05, VALID-SERIOUS-10, DEVIL-CRIT-03, AME-CRIT-05, WIN-CRIT-04. Maps to existing THEME-I.

### Cluster PP: PHASE-3 before PHASE-4 dependency inversion (~3 findings)

PHASE-3 (Anthropic client) precedes PHASE-4 (shared adapters) but conceptually depends on the adapter framework. Members: DEVIL-SER-06, RETRO-SER-04, DISTILL-10. Maps to existing THEME-K (phase ordering).

---

(Additional ~50-80 long-tail singleton claims — each found by 1-2 streams only — are not enumerated cluster-by-cluster here. They appear in the per-stream findings files and the consolidated.md theme entries. Most are concrete and actionable but represent narrower defects than the 42 clusters above.)

---

## §6 Implications for the QD matrix and methodology ADR

1. **The 99.3% within-batch SIGNAL rate is not the relevant σ.** The methodology ADR's §6 (measurement discipline) should specify σ measurement at the unique-claim-cluster level, not the raw-finding level. Per-stream true σ (after cross-batch dedup) is the more honest measurement: median ~73%, range 25%-100%.

2. **The corpus's effective discovery surface is ~120-150 unique architecture defects.** This is ~6-7× smaller than the 867 sub-agent findings + 31 in-context findings. The QD archive — `(cell, theme)` pairs — should be measured against this unique-claim surface, not the per-finding surface.

3. **Several existing themes in `consolidated.md` are redundant.** Cluster E (PHASE-5 §4 numbering) appears as 12 findings → 1 typo. Cluster B (ARCH §9 wrappers) and Cluster A (bmad/_bmad path drift) are nearly the same defect (ADR-0002 Amendment 0001 wasn't propagated). The methodology ADR's §3 (admission rule) should specify that cluster merging happens before σ × κ is computed.

4. **The ACGR convergence regression is partly illusory.** Waves 5-7 produced high raw ACGR (~91% / ~105% / ~87%) but a substantial fraction of "new themes" are framing-refinements of existing clusters (e.g., DEVRETRO-CRIT-010's "meta-gate fallacy" naming is a sharper framing of an existing cluster, not a new defect). True unique-claim ACGR for Waves 5-7 is much lower — probably in the 30-50% range. **The audit may be much closer to convergence than the headline ACGR suggested.**

5. **The 42 dense clusters concentrate in ~5 macro-areas:**
   - Path/wrapper/substrate drift (A, B, FF): ADR-0002 Amendment 0001 propagation
   - Governance machinery (C, L, U, X, Y, GG, HH, LL): amendment lifecycle, gate-coverage, ADR-0008 inventory, PHASE-5 reachability
   - Security primitives (P, Q, R, S, T, JJ, KK, NN): secrets, signing, sandbox, supply-chain, egress, threat-model
   - Bootstrap/scale (O, II): PHASE-0 unbootstrappable, matrix scaling
   - Test/CI discipline (G, H, I, J, BB, DD, OO, PP): thresholds, sample sizes, exemptions, fixture rules
   
   These 5 macro-areas are the natural resolution-CHG groupings. The methodology ADR's resolution-sequence section could use this as input.

6. **Cell-pruning recommendation (preview).** Conservative pruning (drop empty + merge Jaccard > 0.7) would eliminate ~15-20 cells whose theme density is 0 or trivially over-counted by E-class clusters. Moderate pruning (collapse axes that don't differentiate) would likely collapse Axis D (severity bias) into Axis C (decomposition style) — severity is heavily inherited from method choice, not discovered from theme content. The effective `|meaningful_cells|` denominator is probably 25-35, not the original ~55.

7. **The QD admission rule is still vindicated.** Cell-targeted Wave-5/6/7 methods all hit Tier A; cell-fill criterion produced high marginal coverage. But the convergence threshold and cell-count both need re-pinning against the empirical unique-claim data above.

---

## §7 Provenance

Subagent transcripts for the 4 triage runs are not separately preserved (this is a meta-analysis on the existing corpus, not a new audit wave). The classifications above were aggregated from the structured ledger output of each subagent's deliverable. Re-running this triage would require re-spawning the 4 subagents with the prompts in this commit's `TASK-0049.md` (or equivalent successor).

The 6 within-batch non-SIGNAL findings and the 1 hard contradiction are individually verifiable by inspecting the cited source artifacts (which the META- stream already did for FIRST-CRIT-01 and MARY-SERIOUS-12 — see [`corrections.md`](corrections.md)).

The 42 duplicate clusters are best-effort aggregations; greedy ablation (per `qd-triage.md` §2.3) would refine the membership boundaries. The methodology ADR's audit-meta-test suite (queued) should mechanise this measurement.
