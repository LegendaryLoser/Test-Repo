# Project status

**Authoritative human-readable session-resume document.** Hand-maintained
until PHASE-2's `SessionStart` resume hook + `tools/trace/rebuild.py`
mechanize it. New sessions: read this file first, then the active
PHASE file (per [ARCHITECTURE.md §11](architecture/ARCHITECTURE.md)),
then proceed.

**Schema enforced by:** `tools/ci/tests/test_status_resume.py`
(asserts the five `##` section headers below exist).

---

**Last updated:** 2026-05-17 (architecture audit session, branch `claude/bmad-architecture-review-sV42w-bPd8l`)
**Active phase:** PHASE-1 (paused — BMAD audit track in progress)
**Last master commit:** `455ba06` (PR #15 merged: CHG-0014 + CHG-0031)
**Last branch commit** (`claude/bmad-architecture-review-sV42w-bPd8l`): see `git log -1` — most recent work is CHG-0032 TASK-0052 (Wave 8 path-dependence test: 3 streams opened ~30 new clusters; pre-W8 saturation 93% → post-W8 58%; path-dependence empirically substantial). Prior commits this session: TASK-0042 `13f5401`, TASK-0043 `067eefc`, TASK-0044 `9ae2a6a`, TASK-0045 `cd45777`, TASK-0046 `bd702ea`, TASK-0047 `48097c3`, TASK-0048 `78a03a7`, TASK-0049 `b3eab84`, TASK-0050 `e2fc8ad`, TASK-0051 `6c02984`, TASK-0052 (prep) `4abf3a6`.
**Open PRs:** none
**Test count:** 184 passing on master (audit + STATUS.md commits do not change test count)

## CHG status

| CHG  | Title                                                          | Status      | PR  |
|------|----------------------------------------------------------------|-------------|-----|
| 0001 | PHASE-0 verification                                           | merged      | #2  |
| 0002 | ADR-0005 push invariant amendment                              | merged      | #3  |
| 0003 | spec_lint: req-id-format + spec-frontmatter-valid              | merged      | #4  |
| 0004 | spec_lint: req-id-immutable + req-append-only                  | merged      | #5  |
| 0005 | spec_lint: prose-xref-banned + xref-resolves                   | merged      | #6  |
| 0006 | spec_lint: compound-requirement-detector + anti-aliasing       | merged      | #7  |
| 0007 | spec_lint reliability: property tests                          | merged      | #8  |
| 0008 | spec_lint reliability: mutation tests                          | merged      | #9  |
| 0009 | spec_lint reliability: real-corpus dry-run                     | merged      | #10 |
| 0010 | BMAD v6.6.0 vendored install                                   | merged      | #11 |
| 0011 | top-level-allowlist + openspec-validate                        | merged      | #12 |
| 0012 | bmad-direct-reference + mock-in-repo-banned                    | merged      | #13 (stacked w/ 0030) |
| 0013 | CI wiring (spec-lint job real invocations)                     | merged      | #14 |
| 0014 | INDEX subcommand + populate INDEX.yaml                         | merged      | #15 |
| 0030 | Test annotation discipline + 87-test backfill                  | merged      | #13 (stacked) |
| 0031 | Session continuity scaffold                                    | merged      | (in #15) |
| 0032 | Architecture audit (BMAD multi-pass) + QD triage + corpus      | in-progress | TBD |

## Audit findings

Status of every finding from the in-session adversarial audit
(see chat history for full report). C = critical, S = serious,
P = process, NEW = surfaced after the original audit.

| ID    | Severity | Description                                          | Status      | Resolved by                |
|-------|----------|------------------------------------------------------|-------------|----------------------------|
| C1    | CRITICAL | INDEX.yaml empty                                     | CLOSED      | CHG-0014                   |
| C2    | CRITICAL | REQ-ARCH-* in wrong format (bullets, not REQ blocks) | OPEN        | queued CHG-0015            |
| C3    | CRITICAL | PHASE-1 incomplete (5 gates + tools/tea/ missing)    | OPEN        | queued CHG-0020..0025      |
| C4    | CRITICAL | No CI execution of any gates                         | CLOSED      | CHG-0013                   |
| C5    | CRITICAL | P1 + P5 uncovered by any gate                        | OPEN        | queued CHG-0029            |
| S1    | SERIOUS  | mock-in-repo-banned FP on `class Mock(Base)`         | OPEN        | queued CHG-0018            |
| S2    | SERIOUS  | prose-xref-banned ignores inline backticks           | OPEN        | queued CHG-0016            |
| S3    | SERIOUS  | bmad-direct-reference bypassable (string concat)     | OPEN        | queued CHG-0019            |
| S4    | SERIOUS  | 6 rules without REQ-SPEC                             | CLOSED      | CHG-0030                   |
| S5    | SERIOUS  | real_repo_passes trivially-passing P4 violations     | OPEN        | queued CHG-0026            |
| P1    | PROCESS  | ARCHITECTURE.md §3 vs ALLOWED_TOP_LEVEL drift        | OPEN        | queued CHG-0027            |
| P2    | PROCESS  | REQ-status transition rules unclear                  | OPEN        | queued CHG-0028            |
| P3    | PROCESS  | Squash merge commits lose trailers                   | OPEN        | queued CHG-0028            |
| P4    | PROCESS  | CHG envelope drift (proposal lists wrong task count) | OPEN        | queued CHG-0028            |
| P5    | PROCESS  | TASK files stale after implementation                | OPEN        | queued CHG-0028            |
| P6    | PROCESS  | test_mutations.py unannotated                        | CLOSED      | CHG-0030                   |
| NEW-1 | SERIOUS  | `generated_at` exemption violates determinism        | OPEN        | queued CHG-0014b           |
| NEW-2 | SERIOUS  | Tests not derived from REQ Acceptance clauses        | OPEN        | queued ADR-0009 (new ADR)  |
| NEW-3 | PROCESS  | BMAD review skills not in CHG workflow               | IN-PROGRESS | CHG-0032 (this audit is the response; methodology ADR queued) |
| AUDIT-2026-05-17 | INFO | Architecture audit Wave 1 (12) + Wave 2 (8) + Wave 3 (8) + Wave 4 (8) complete = 36 streams; ~700 raw findings → ~70 themes; COMPOSITE-V2 6/7 gates met; Gate 6 marginal novelty trajectory: Wave 2 ~50%, Wave 3 ~30-37%, Wave 4 ~46% (spiked from STAKE+COUNTER new methods). EMPIRICAL FINDING: marginal novelty is methodology-variance-driven, not model-variance-driven. Tight-method permutations converge ~15-30%; new methods spike 60-70%. Implication for methodology ADR: Gate 6 must be defined relative to fixed methodology catalog. Artifact at `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/` | IN-PROGRESS | CHG-0032 |
| QD-TRIAGE-2026-05-17 | INFO | Quality-Diversity triage of all 36 streams complete. Adopted research-grounded QD framework (MAP-Elites + Mixture-of-Complementary-Agents + ambiguity decomposition): four behavioural axes (Lens × Temporal × Decomposition × Severity), σ × κ Pareto admission per cell, ACGR (Archive Coverage Growth Rate) replacing raw marginal novelty as Gate 6. Per-method tier assignment: 16 Tier A, ~10 Tier B, 1 Tier C, 4 Tier D candidates (COURSE, CHECK, EDIT, VALID2). 5 high-importance empty cells identified as Wave 5 admission targets. ACGR re-measurement: Wave 4 ~45% (vs marginal-novelty 46%); Wave 3 ~22%. Wave 5 expected ACGR 10-15%, Wave 6 <5% (convergence). Methodology ADR draft sections (§§1-11) at `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/qd-triage.md` | IN-PROGRESS | CHG-0032 |
| AUDIT-2026-05-17-WAVE-5 | INFO | Wave 5 architecture audit complete: 4 streams targeting Tier-1 empty cells per `qd-triage.md` §8. Streams: `GOV-` (governance-focused validate-prd; 22 findings, 5/14/3 C/S/P), `SEC-` (security-engineer holistic persona; 21 findings, 7/9/5), `GOVDEV-` (governance-focused devil's-advocate; 22 findings, 5/11/6), `META-` (reasoning-tree meta-auditor over the 35-stream corpus; 19 findings, 4/12/3). **Wave-5 total: 84 raw findings (21 CRIT / 46 SER / 17 PROC).** First wave admitted under QD admission rule (cell-fill, not raw novelty); first wave to invoke a candidate 5th axis (meta). All 4 streams used opus; 2 invoked named BMAD skills (`bmad-validate-prd`, `bmad-advanced-elicitation`), 2 used general-purpose subagent with custom prompt (per Wave-4 STAKE/COUNTER precedent). `META-` surfaced specific Wave 1-4 retractions processed via `corrections.md` (TASK-0043). Wave-5 thematic consolidation complete (TASK-0044): ~25 new themes (YYY-WWWW); ACGR re-measured at **~91% ± 16%** (much higher than projected 10-15% — governance and security/ops cells were theme-dense, not sparse). | DONE | CHG-0032 (TASK-0042 + TASK-0043 + TASK-0044) |
| AUDIT-2026-05-17-WAVE-6 | INFO | Wave 6 architecture audit complete: 4 streams continuing per user direction "keep going wave after wave; each cell is important." Streams: `STRUCTGOV-` (structural-governance review; 22 findings, 3/13/6 C/S/P), `SECDISTILL-` (security-focused distillation; 16 findings, 8/5/3), `SCENNOW-` (6-actor scenario unfold from current state; 20 findings, 7/7/6), `PERSRETRO-` (Winston-2029 retrospective from 3 years out; 17 findings, 3/9/5). **Wave-6 total: 75 raw findings (21 CRIT / 34 SER / 20 PROC).** Filled the 2 remaining Tier-1 high-importance Axis-D empty cells + 2 never-occupied Lens × Temporal cells. 2 BMAD-skill invocations + 2 general-purpose with custom prompts (same mixed policy as Wave 5). Concrete drift surfaced: `skill-removal-acknowledged` exists in ADR-0002 §Compliance + PHASE-2 §Scope but NOT in ADR-0008 §1 gate inventory (STRUCTGOV-PROC-005). Wave-6 thematic consolidation complete (TASK-0046): ~29 new themes (XXXX-ZZZZZ; transition from quadruple- to quintuple-letter IDs); ACGR re-measured at **~105% ± 21%** — even higher than Wave 5's ~91%. Two consecutive waves >90% ACGR decisively falsify the original convergence projection. Compression-lens Tier-A gap from `qd-triage.md` §7.4 conditionally resolved via SECDISTILL. | DONE | CHG-0032 (TASK-0045 + TASK-0046) |
| AUDIT-2026-05-17-WAVE-7 | INFO | Wave 7 architecture audit complete: 4 streams targeting remaining forward + post-hoc Lens × Temporal cells per `qd-triage.md` §8.2. Streams: `SCENFUT-` (18-month-forward scenario unfold; 18 findings, 6/6/6 C/S/P), `STRUCTFUT-` (forward structural-growth-pressure; 18 findings, 3/7/8), `DEVRETRO-` (2029-external-critic contrarian retrospective; 18 findings, 8/4/6), `ATTFUT-` (attitudinal-forward discipline-additions; 18 findings, 5/9/4). **Wave-7 total: 72 raw findings (22 CRIT / 26 SER / 24 PROC).** Most balanced wave to date — all 4 streams exactly 18 findings. All 4 used opus + general-purpose subagent with custom prompts (no BMAD skill maps to these specific cells). Key surfaces: SCENFUT identified matrix-at-scale (rebuild.py linear in history with no incremental path) as most blocking 18-month-forward gap; STRUCTFUT identified ADR-and-amendment surface area as most-pressured (10-ADR layout breaks at 50+); DEVRETRO nominated "deferring all product content until PHASE-5" as 2029-canonical mistake + reformulated META-/GOVDEV's gate-coverage-tautology as "meta-gate fallacy"; ATTFUT identified ADR-0009 on credentials/service-account lifecycle as single most-needed addition. Thematic consolidation deferred to TASK-0048. | IN-PROGRESS | CHG-0032 (TASK-0047) |

## Open architectural questions

1. **`generated_at` exemption (REQ-SPEC-0015):** drop entirely (option 1
   in chat), replace with content hash (option 2), or keep as documented
   hole (option 3)? Recommendation: option 1, before CHG-0025 wires
   `index-up-to-date` as a CI gate.
2. **REQ-ARCH-* canonical home (audit C2):** in-place restructure of
   ARCHITECTURE.md §10, separate `architecture-invariants.spec.md`,
   or formal carve-out documented in an ADR? Recommendation: separate
   file (cleanest SoT separation).
3. **Test-spec derivation (NEW-2):** codify in ADR-0009 that every test
   assertion must literally restate the REQ's Acceptance clause? The
   meta-test enforcement is mechanical (CHG-0030 covers presence of
   `@covers`); the deeper question is whether the test ACTUALLY
   verifies the REQ promises.
4. **Allow-marker policy:** when is `<!-- spec-lint: allow X -->`
   justified? Should each marker addition go through `bmad-review-
   adversarial-general`? Currently no markers exist (CHG-0030 closed
   them), but the policy gap is open for future re-additions.
5. **BMAD workflow integration (NEW-3):** which BMAD skills become
   mandatory in the CHG flow? Candidates: `bmad-review-adversarial-
   general` before any PR open; `bmad-code-review` before any GREEN
   commit; `bmad-check-implementation-readiness` before any phase
   exit. Decision required before continuing roadmap.
6. **PHASE-1 exit criteria:** the post-audit roadmap added several CHGs
   (0014b, 0026, 0027, 0028, 0029, 0030, 0031, ADR-0009). Should
   PHASE-1 exit be amended (ADR-0008) to include these, or are they
   informal additions? Currently informal.

## Roadmap

Sequenced from current state. `[x]` merged, `[~]` in flight, `[ ]` queued.

### Tier 0 — discipline foundations (urgent)

- [x] CHG-0030 — annotation discipline + REQ backfill (closed P6, S4)
- [x] CHG-0031 — session continuity scaffold (merged in PR #15)

### Tier 1 — close critical enforcement gaps

- [x] CHG-0013 — CI wiring (closed C4)
- [x] CHG-0014 — INDEX subcommand + populate (closed C1; merged in PR #15)
- [ ] CHG-0014b — drop `generated_at` (closes NEW-1)
- [ ] CHG-0015 — REQ-ARCH canonical home migration (closes C2; expands INDEX to 23)

### Tier 2 — close serious soundness gaps in shipped rules

- [ ] CHG-0016 — xref-resolves + prose-xref-banned inline-backtick + multi-line awareness (closes S2, D1, D2)
- [ ] CHG-0018 — mock-in-repo-banned FP fix (closes S1)
- [ ] CHG-0019 — bmad-direct-reference honest docs + bypass tests (closes S3)
- [ ] CHG-0026 — real_repo_passes redesign (closes S5)

### Tier 3 — complete PHASE-1 gate inventory (audit C3)

- [ ] CHG-0020 — gas-global-outside-adapter
- [ ] CHG-0021 — direct-anthropic-import-banned
- [ ] CHG-0022 — stochastic-tier-bans
- [ ] CHG-0023 — semantic-recall-recall-at-k
- [ ] CHG-0024 — tools/tea/ skeleton
- [ ] CHG-0025 — index-up-to-date CI gate

### Tier 4 — process + SoT consolidation

- [ ] CHG-0027 — cross-doc consistency check (closes P1)
- [ ] CHG-0028 — ADR amendment bundle (REQ-status, merge-commit, CHG/TASK drift policy) (closes P2, P3, P4, P5)
- [ ] CHG-0029 — covering gates for P1 (SoT) + P5 (workflow) principles (closes C5)
- [ ] ADR-0009 — Test-spec derivation discipline (closes NEW-2)

### Tier 5 — PHASE-1 exit + BMAD workflow

- [~] BMAD adversarial review of architecture (per user request — NEW-3): Waves 1-5 complete (40 streams; Wave-5 raw findings persisted, thematic consolidation deferred); QD triage complete for Waves 1-4 (qd-triage.md); Wave-5 thematic consolidation + qd-triage.md §3.5 update + ACGR re-measurement pending (next consolidation pass); Wave 6 conditional on Wave-5 ACGR
- [ ] BMAD adversarial review of implementation (queued; runs after architecture audit converges per Recent decisions)
- [ ] Methodology codification ADR (draft clauses in qd-triage.md §9; authored after BOTH audits converge per Recent decisions)
- [ ] CHG-NN — formal PHASE-1 exit gate run

## Recent decisions

| Date       | Decision                                                            | Rationale                                                     |
|------------|---------------------------------------------------------------------|---------------------------------------------------------------|
| 2026-05-16 | Vendor BMAD v6.6.0 (Option A) instead of install-on-session-start   | Container-reclaim resilience; SoT (P1); 2.6MB one-time cost   |
| 2026-05-16 | `_bmad-output/` as STAGING; promotion required for canonical use    | P1 — drafts must not compete with authoritative artifacts     |
| 2026-05-16 | Native `.claude/skills/` over wrapper agents/commands (ADR-0002 amendment 0001) | Empirical: BMAD v6 ships native skills; wrappers redundant |
| 2026-05-17 | Stack CHG-0030 on PR #13 instead of new branch                      | User preference at AskUserQuestion prompt                     |
| 2026-05-17 | CHG-0014 ships with `generated_at` exemption (deferred to 0014b)    | Get the substrate in place; defer the determinism fix         |
| 2026-05-17 | Adopt test-spec-derivation discipline (ADR-0009 queued)             | Audit + user pushback on hot-fix pattern                      |
| 2026-05-17 | Bring BMAD into the CHG workflow from planning forward              | User request; P5 ("OpenSpec + BMAD + TEA")                    |
| 2026-05-17 | Run BMAD adversarial architecture audit as 12-stream multi-pass (then 8 more in Wave 2) | User request: max rigor, model + methodology diversity         |
| 2026-05-17 | Lock COMPOSITE-V2 as convergence metric (7 gates; Gate 6 = marginal novelty <10%) | User decision after explanation of pairwise-agreement trade-off |
| 2026-05-17 | Codify audit methodology in ADR after BOTH architecture + implementation audits complete | User choice (defer codification until both audits validated)  |
| 2026-05-17 | Run implementation audit after architecture audit convergence; consolidate jointly | User decision; findings may re-sequence resolution            |
| 2026-05-17 | Re-sequence: do not start any Tier 1+ resolution CHG until both audits converge   | User direction ("resolve thoroughly before going ahead with anything") |
| 2026-05-17 | Adopt Quality-Diversity framework (σ × κ Pareto admission, ACGR convergence) replacing COMPOSITE-V2 Gate 6 marginal-novelty rule; codify in methodology ADR | User decision after research synthesis (MAP-Elites, Mixture-of-Complementary-Agents, ambiguity decomposition); satisfies "new methods that provide signal must be admitted" constraint while still producing a defensible stopping rule |
| 2026-05-17 | Full QD triage of all 36 audit streams complete (qd-triage.md); 4 Tier-D deprecation candidates surfaced (COURSE, CHECK, EDIT, VALID2); 5 high-importance empty cells identified as Wave 5 admission targets | Triage produced empirical per-method σ × κ scores from existing audit corpus without re-running streams |
| 2026-05-17 | Rescue-persist the 35 sub-agent raw transcripts + per-stream findings into the repo (raw-transcripts/ + findings/) | Original audit README mistakenly relied on ephemeral container `/tmp/` storage for raw outputs; container reclaim would have lost the corpus. Future audits must persist inline. |
| 2026-05-17 | Author CHG-0032 envelope retroactively (proposal.md + 7 TASK files + REQ-AUDIT-0001 at `openspec/specs/audit/methodology.spec.md`) | Audit work had been carrying dangling `Task: TASK-NNNN` and `Requirements: REQ-AUDIT-0001` trailers that referenced files which did not exist. Retroactive authoring resolves the dangling references and gives the fresh session a canonical scope declaration. P4 violation acknowledged (envelope is descriptive not prescriptive); methodology codification ADR queued to address audit-CHG lifecycle question. |
| 2026-05-17 | Run Wave 5 architecture audit: 4 streams (`GOV-`, `SEC-`, `GOVDEV-`, `META-`) targeting Tier-1 empty cells in the QD matrix | First wave admitted under the QD admission rule (cell-fill, not raw novelty). `SEC-` and `META-` invoked as general-purpose subagents with custom prompts (no BMAD skill maps to their cells); `GOV-` and `GOVDEV-` invoked named BMAD skills with focused biasing. Persistence performed inline this session (not post-hoc rescue): `persist-corpus.py` made incremental — pass 1 ingests new cache transcripts, pass 2 preserves pre-existing on-disk rows from prior sessions. |
| 2026-05-17 | Mixed invocation policy for Wave 5: BMAD skills for in-catalog cells, general-purpose with custom prompts for out-of-catalog cells | Derived from Wave-4 empirical evidence (STAKE+COUNTER, the two highest-κ streams in the entire corpus, used general-purpose with custom prompts). Methodology codification ADR queued to decide whether the catalog admits a single class of methods or two classes (BMAD-skill + general-purpose-prompted). |
| 2026-05-17 | META- corrections applied via append-only audit-of-the-audit log (`corrections.md`) rather than silent in-place edits to consolidated.md and qd-triage.md | Preserves provenance (original framings remain readable); makes each correction traceable to a META- finding ID; models the correction protocol the methodology codification ADR will need. Surgical inline edits limited to mechanically-wrong-and-one-line-fixable cases (THEME-X count, FIRST artifact annotation) + top-of-document pointers. |
| 2026-05-17 | `findings-index.md` brought current with Waves 4 + 5 per-stream tallies; per-theme constituent listing for Waves 4-5 deferred to next consolidation pass | META-CRIT-002 surfaced that the index was stale at Wave 3 (28 streams) while consolidated.md and qd-triage.md both referenced 36 streams. Per-stream tally is the structural skeleton; per-theme listing requires Wave-5 thematic consolidation first. |
| 2026-05-17 | Wave-5 thematic consolidation: ~25 new themes (THEMES YYY-WWWW), ~30 reinforcements of Waves 1-4 themes; qd-triage §3.5 authored with Wave-5 per-method σ × κ (all 4 streams Tier-A) | Wave-5 ACGR re-measured at **~91% ± 16%** — much higher than the §8 projected 10-15%. Cause: governance and security/ops cells were theme-dense (~8 themes/cell), not sparse (2-3 themes/cell) as the projection assumed. The QD admission rule (cell-fill criterion) is vindicated; the convergence threshold (ACGR < 5%) is questioned. |
| 2026-05-17 | Wave 6 candidates surfaced in qd-triage §8.1 but not scheduled — user decision required | Remaining empty cells: `(structural × current × holistic × governance)` likely dense (5-10 themes) and `(compression × * × security/ops)` likely sparse (2-4 themes). Convergence threshold is open: if structural-governance is also theme-dense, ACGR < 5% may not be achievable without changing the denominator definition or accepting higher residual κ. Methodology codification ADR must resolve. |
| 2026-05-17 | User direction: "Keep going wave after wave and don't consider the QD matrix as final till the time we have not run out of signal. Each cell is important." | Reframes the convergence question: the QD matrix denominator and cell-occupancy state are themselves provisional; new methods/cells may still need admission. Terminal condition is signal-exhaustion (no genuinely new findings emerging), not pre-defined ACGR threshold. Wave 6 spawned per this direction with cell-selection mixing Tier-1 Axis-D empty cells + never-occupied (Lens × Temporal) cells. |
| 2026-05-17 | Wave 6 complete: 4 streams (STRUCTGOV, SECDISTILL, SCENNOW, PERSRETRO); 75 raw findings (21 CRIT / 34 SER / 20 PROC); thematic consolidation deferred | 2 BMAD-skill streams (STRUCTGOV via bmad-editorial-review-structure; SECDISTILL via bmad-distillator) + 2 general-purpose-custom-prompt streams (SCENNOW: 6-actor scenario unfold from current state; PERSRETRO: Winston-2029 retrospective from 3 years out). Key empirical surfaces: STRUCTGOV identified amendment-overlay-without-separable-addressing as dominant structural-governance pattern + concrete drift (`skill-removal-acknowledged` missing from ADR-0008 §1); SECDISTILL identified credentials-management as the security topic most damaged by compression (NULL canonical claim); SCENNOW identified Agent-session-start scenario as most blocking (SessionStart hook doesn't exist + STATUS.md not required to exist + agent told to read both); PERSRETRO's most-wished-retraction is ADR-0006 §2's unqualified no-mock rule (18%/project velocity tax × 3 years). |
| 2026-05-17 | Wave-6 thematic consolidation: ~29 new themes (THEMES XXXX-ZZZZZ, including transition from quadruple- to quintuple-letter IDs); ~46 reinforcements of Waves-1-5 themes; qd-triage §3.6 authored (all 4 Wave-6 streams Tier-A); ACGR re-measured at **~105% ± 21%** | Two consecutive waves (5 + 6) at >90% ACGR decisively falsify the original convergence-projection model. Per user direction "keep going wave after wave; don't consider the QD matrix as final," signal-exhaustion observation is the operational terminal condition — Wave 6's 29 new themes / 4 streams = ~7 themes/stream, *more* productive per stream than Wave 5 (~6/stream excluding META). Compression-lens Tier-A gap from `qd-triage.md` §7.4 conditionally resolved via SECDISTILL. Wave 7 candidates surfaced in `qd-triage.md` §8.2: `(scenario × forward-looking)`, `(structural × forward-looking)`, `(contrarian × post-hoc)`, `(attitudinal × forward-looking)`. |
| 2026-05-17 | Wave 7 complete: 4 streams (SCENFUT, STRUCTFUT, DEVRETRO, ATTFUT); 72 raw findings (22 CRIT / 26 SER / 24 PROC); all 4 streams produced exactly 18 findings — Wave 7's most balanced output to date; thematic consolidation deferred to TASK-0048 | All 4 used opus + general-purpose subagent with custom prompts. Empirical highlights: SCENFUT scenario-6 (matrix performance at scale) most blocking 18-month-forward gap; STRUCTFUT's ADR-and-amendment surface area is most-pressured structural dimension (current 10-ADR layout breaks at 50+); DEVRETRO's 2029-canonical-mistake nomination is "deferring all product content until PHASE-5"; ATTFUT's single most-needed addition is ADR-0009 on credentials/service-account lifecycle. DEVRETRO surfaced "meta-gate fallacy" as canonical formulation of META-/GOVDEV's earlier gate-coverage-tautology findings. Methodology codification ADR is now structurally urgent: audit shows no convergence under any reasonable signal-exhaustion interpretation. |
| 2026-05-17 | Wave-7 thematic consolidation: ~24 new themes (THEMES AAAAAA-XXXXXX, transition from quintuple- to sextuple-letter IDs); ~48 reinforcements; qd-triage §3.7 authored (all 4 Wave-7 streams Tier-A); ACGR re-measured at **~87% ± 17%** | Three consecutive waves (5, 6, 7) at >85% ACGR — convergence threshold from original projection (ACGR < 5% for two consecutive waves) is structurally unachievable at current per-wave new-theme rate. First 3-way co-surface in corpus: project-overlay-semantics rediscovered by SCENFUT + STRUCTFUT + ATTFUT independently. ATTFUT's structurally novel as audit's resolution proposer (nominates ADR-0009..0017). DEVRETRO's "meta-gate fallacy" terminology is canonical-shape; methodology ADR should adopt. Cumulative themes after Wave 7: ~149 (Waves 1-7 cumulative). Wave 8 candidates: `(attitudinal × post-hoc)`, `(structural × post-hoc)`, `(compression × post-hoc)`, recursive META-META-. |
| 2026-05-17 | Signal-filter triage of all 867 sub-agent findings (TASK-0049): 4 parallel subagents classified each finding into 7 categories; cross-batch deduplication identified **42 dense duplicate-claim clusters + ~80-110 long-tail singletons = ~120-150 unique architecture defects** (corpus has ~6-7× redundancy vs raw 867); 1 hard contradiction (PREM2-PROC-009 vs META-CRIT-003, both about ADR-0003 existence); per-stream true-σ median ~73% (vs within-batch 99.3%) | The 99.3% within-batch SIGNAL rate misleads about corpus convergence. True effective discovery surface is ~120-150 defects concentrating in 5 macro-areas (path/wrapper drift; governance machinery; security primitives; bootstrap/scale; test/CI discipline). ACGR convergence regression (~87-105% headline for Waves 5-7) is partly illusory — much of "new themes" are framing-refinements of existing clusters; true unique-claim ACGR for Waves 5-7 probably 30-50%. Audit may be substantially closer to convergence than headline ACGR suggested. `signal-ledger.md` is the empirical input for the methodology codification ADR's §6 (measurement discipline) and for cell-pruning. |
| 2026-05-17 | Dual-metric (coverage + QD-score) reformulation REJECTED in favour of saturation-based reformulation: user's three critiques (coverage tautology, ordering bias, audit-type criticality variance) are well-founded per QD literature (Mouret & Clune 2015; Cully & Demiris 2018; Stock 2025); drop coverage as a metric (tautological in post-hoc-cell setup); replace with per-cell saturation (operates within observed cells; no |meaningful| denominator); keep QD-score as depth metric; adopt two-layer framework (domain-general algorithm + audit-type-specific behaviour-descriptor) | TASK-0050 authored `methodology-research-note.md` documenting the three critiques against research literature + proposing the saturation-based reformulation as the operational framework. Dual stopping condition: `saturation ≥ 95% AND ΔQD-score < 5% for two consecutive waves`. Path-dependence acknowledged explicitly (mitigated via method-sequence documentation rather than N-restart bootstrap, which is cost-prohibitive). Input to methodology codification ADR. |
| 2026-05-17 | Cell-finalization (TASK-0051) executed per saturation-based scope: 42 dense clusters mapped to 15 distinct cells via defect-content labeling (not surfacing-method default); per-cell saturation status computed (93% strict K=2 / 80% inclusive K=2); QD-score baseline ~58.8; ΔQD-score W7 = 29% (driven by SCENFUT's W7 admission opening 3 scenario-forward cells); path-dependence inventory shows 60% Wave-1 cluster dominance | Audit close to cluster-level saturation but depth still expanding. Dual stopping NOT met (saturation close to 95% threshold; ΔQD-score at 29% vs <5% target). Decision options: (A) one more wave testing Pareto stability in recently-opened cells likely meets both thresholds; (B) declare convergence-enough at 93% saturation + acknowledge ongoing depth discovery at decreasing rate; (C) continue path-dependence remediation. `cell-occupancy.md` is the Layer-2 instance for the methodology codification ADR. |
| 2026-05-17 | Wave 8 path-dependence test (TASK-0052; user Option C): 3 second-methods (COMPLIRETRO compliance-officer-retrospective, FAILSCEN failure-mode-scenarios, INTRRETRO internal-team-retrospective) added to cells previously occupied by single Wave-6/7 methods. Opened **~30 NEW clusters** (~47%, 78%, 44% NEW per stream). **Pre-W8 93% saturation was decisively wrong; revised to 58%**. 42 clusters → ~72; 15 cells → ~24; QD-score 58.8 → 83.2; W8 ΔQD-score = 29% (same as W7). Path-dependence is empirically substantial, not just theoretical | `wave-8-path-dependence-results.md` authored. 4 methodology implications: (1) path-dependence ~71% cluster expansion under partial bootstrap, documentation-only mitigation insufficient; (2) cell map incomplete by construction (~9 new cells opened); (3) N-restart bootstrap empirically necessary, not just preferable; (4) saturation requires per-cell Pareto-stability evidence, not just K-consecutive-no-new-method. Updated stopping options: A' continue path-dependence (more new clusters expected); B' accept exhaustively-explored-but-path-dependent and pivot to resolution+methodology-ADR+implementation-audit (RECOMMENDED); C' bootstrap-style Wave-1 restart with different method-mix (~2× cost). Audit has likely passed ROI peak; marginal value of each new cluster decreasing. |

## Next session: start here

**Current state of the architecture audit (CHG-0032):**

- Waves 1, 2, 3, 4, 5, 6, 7 all complete — 48 streams total. Cumulative raw findings ~932 across all waves. Waves 1-6: thematic consolidation complete (~125 themes). Wave 7: 72 raw findings (22 CRIT / 26 SER / 24 PROC); thematic consolidation deferred to TASK-0048.
- Per-method tier assignment complete for Waves 1-6 (qd-triage.md §§3.1-3.6); Wave 7 pending §3.7 (next consolidation pass).
- Quality-Diversity (QD) framework adopted. Wave 5 was the first wave under QD admission rule; admission rule is **vindicated** (4/4 Tier-A admissions in Wave 5; same in Wave 6; expected same in Wave 7). Convergence threshold is **decisively questioned**: Wave 5 ACGR ~91% ± 16%, Wave 6 ACGR ~105% ± 21% — both far above the 5% terminal threshold the original projection model predicted.
- User-direction terminal condition is signal-exhaustion (no genuinely new findings/themes emerging), NOT pre-defined ACGR threshold. Wave 7 produced 72 raw findings (18/stream balanced) — audit has NOT run out of signal; continuation expected.
- Remaining empty Lens × Temporal cells after Wave 7: `(attitudinal × post-hoc)`, `(structural × post-hoc)`, `(compression × post-hoc)`, `(compression × forward-looking)`. Plus the recursive META-META-axis (audit META-'s corrections themselves). These are Wave 8+ candidates per "each cell is important."
- META- corrections (19 total) processed via `corrections.md` (TASK-0043); STAKE-CRIT-001 severity recalibration to STAKE-SER-001 still deferred in `findings/STAKE-findings.md`.
- **Methodology codification ADR is now structurally urgent.** Audit shows no convergence under any reasonable interpretation of "signal exhaustion." 2 consecutive waves at >90% ACGR + Wave 7 producing 18 findings/stream means the joint-consolidation prerequisite ("converged") cannot be met without methodology revision. ADR drafting should happen in parallel with continued waves, not after.

**Read in this order before doing anything else:**

1. This file (STATUS.md), especially the CHG status table, Audit findings ledger, Open architectural questions, and Recent decisions.
2. `openspec/architecture/ARCHITECTURE.md` §1 (principles) and §11 (active phase).
3. `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/qd-triage.md` — the full QD triage. Required reading: §2 (framework definitions), §5 (Tier A/B/C/D catalog), §7 (ACGR convergence diagnostic), §8 (Wave 5 admission targets), §9 (draft clauses for methodology ADR).
4. `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/consolidated.md` — the ~70 themes, organised by tier of confirmation; required if planning resolution CHGs, otherwise reference-only.

**First action on resume:** USER DECISION between three UPDATED options post-Wave-8 (per `wave-8-path-dependence-results.md` §5). The pre-W8 Options A/B/C from `cell-occupancy.md` §7 are now superseded; Wave 8's empirical result (~30 new clusters; saturation dropped 93% → 58%; path-dependence substantial) invalidates the pre-W8 projections.

**Option A' — Continue path-dependence remediation.** Spawn Wave 9 with second-methods in the 9 new Wave-8 cells (FAILSCEN's 11-cluster failure-mode cell especially needs a second method to test Pareto stability). Expected ~15-30 new clusters; saturation might rise to 65-75% but unlikely to reach 95%.

**Option B' — Accept exhaustively-explored-but-path-dependent** (RECOMMENDED per `wave-8-path-dependence-results.md` §5). Document the corpus as ~72 clusters + path-dependence-acknowledged-as-fundamental. Pivot to:
- Resolution-CHG sequencing for the 72 clusters
- Methodology codification ADR drafting (uses signal-ledger.md + methodology-research-note.md + cell-occupancy.md + wave-8-path-dependence-results.md as inputs)
- Implementation audit using QD catalog dogfood-style on `tools/spec_lint/`, `tools/ci/`, `_bmad/`, `.github/workflows/`

**Option C' — Bootstrap-style restart.** Re-run Wave 1 with a DIFFERENT method-mix (e.g., persona-retrospective + failure-mode-scenarios FIRST) and compare which clusters surface in both runs. Genuine path-dependence mitigation; ~2× audit cost.

Steps that were DONE in this session (this branch):
- TASK-0042 (`13f5401`): Wave 5 architecture audit.
- TASK-0043 (`067eefc`): META corrections + findings-index Wave 4 + 5 catch-up.
- TASK-0044 (`9ae2a6a`): Wave-5 consolidation.
- TASK-0045 (`cd45777`): Wave 6 architecture audit.
- TASK-0046 (`bd702ea`): Wave-6 consolidation.
- TASK-0047 (`48097c3`): Wave 7 architecture audit.
- TASK-0048 (`78a03a7`): Wave-7 consolidation.
- TASK-0049 (`b3eab84`): Signal-filter triage of 867 findings; `signal-ledger.md` (42 clusters).
- TASK-0050 (`e2fc8ad`): Methodology research note + saturation-based reformulation; `methodology-research-note.md`.
- TASK-0051 (`6c02984`): Cell finalization; `cell-occupancy.md` (15 cells, 93%/80% saturation, QD-score 58.8) — **superseded by TASK-0052**.
- TASK-0052 prep (`4abf3a6`): persist-corpus.py DESC_TO_STREAM extended with Wave-8 entries.
- TASK-0052 (latest commit): Wave 8 path-dependence test; 3 streams; `wave-8-path-dependence-results.md` (~30 new clusters; 42→72; saturation 93%→58%; path-dependence empirically substantial).

Pending work (NOT done in this session):
- TASK-0053+: Conditional on Option A'/B'/C' choice.
- Per-theme constituent-finding listing for Waves 4-8 in `findings-index.md` (stale).
- Severity recalibration of STAKE-CRIT-001 → STAKE-SER-001 per corrections.md META-SER-012.
- Layer 1/Layer 2 split rewrite of `qd-triage.md` (deferred to methodology codification ADR drafting). <!-- spec-lint: allow prose-xref-banned -->

Steps that were DONE in this session (this branch):
- TASK-0042 (`13f5401`): Wave 5 architecture audit (4 streams, 84 raw findings).
- TASK-0043 (`067eefc`): META- corrections log + findings-index Wave 4 + 5 catch-up.
- TASK-0044 (`9ae2a6a`): Wave-5 thematic consolidation (~25 new themes), ACGR ~91% ± 16%.
- TASK-0045 (`cd45777`): Wave 6 architecture audit (4 streams, 75 raw findings).
- TASK-0046 (`bd702ea`): Wave-6 thematic consolidation (~29 new themes), ACGR ~105% ± 21%.
- TASK-0047 (`48097c3`): Wave 7 architecture audit (4 streams, 72 raw findings).
- TASK-0048 (`78a03a7`): Wave-7 thematic consolidation (~24 new themes), ACGR ~87% ± 17%.
- TASK-0049 (`b3eab84`): Signal-filter triage of 867 findings; `signal-ledger.md` authored; 42 dup clusters; ~120-150 unique defects.
- TASK-0050 (latest commit): Methodology research note documenting three structural critiques + saturation-based reformulation + two-layer framework. `methodology-research-note.md` authored as input to methodology codification ADR.

Pending work (NOT done in this session):
- TASK-0051: cell-finalization with revised scope per `methodology-research-note.md` §5 (saturation status, QD-score baseline, path-dependence inventory, Layer 1/Layer 2 split).
- TASK-0052+: dependent on TASK-0051 saturation result (Wave 8 spawn vs methodology ADR drafting vs implementation audit pivot).
- Per-theme constituent-finding listing for Waves 4-7 in `findings-index.md` (stale by ~149 themes).
- Project-overlay-semantics theme ID assignment (3-way co-surface from Wave 7: SCENFUT-CRIT-007 + STRUCTFUT-PROC-018 + ATTFUT-PROC-016).
- Full greedy-ablation σ × κ measurement.
- `|meaningful_cells|` formal enumeration (currently ~55 ± 10; almost certainly under-estimated — empirical theme density implies cell denominator should grow).
- Severity recalibration of STAKE-CRIT-001 → STAKE-SER-001 per `corrections.md` META-SER-012.
- **Methodology codification ADR drafting** — STRUCTURALLY URGENT. Three consecutive waves at >85% ACGR make the convergence-threshold question a hard blocker. The methodology ADR's §6 (Measurement discipline) should adopt DEVRETRO-CRIT-010's "meta-gate fallacy" terminology + define operational signal-exhaustion criterion + revise the convergence threshold given the empirical cell-theme-density data.

**Second action (whichever audit runs next):** apply the QD framework. Score each new stream on σ × κ; place into the cell map (qd-triage.md §4); update ACGR. **Do NOT re-run COURSE, CHECK, EDIT, or VALID2** unless the user explicitly overrides — they are Tier-D candidates pending implementation-audit confirmation of their κ ≈ 0 status.

**Third action:** consolidate architecture + implementation audit findings jointly. Draft the methodology codification ADR using qd-triage.md §9 as the starting point — adopt the eight proposed clauses (operating principle, behavioural axes, admission rule, ACGR convergence criterion, initial method catalog, measurement discipline, deprecation procedure, stopping rule). Allocate an ADR number at draft time (next available is ADR-0009 unless something else takes it first).

**Fourth action:** plan resolution CHG sequence against the joint ledger. Per user direction, do NOT start any Tier 1+ resolution CHG (CHG-0014b drop `generated_at`, CHG-0015 REQ-ARCH migration, etc.) until both audits converge and the joint resolution sequence is approved.

**CHG-0032 envelope (authoritative):**
- `openspec/changes/CHG-0032/proposal.md` — scope declaration, what changes, out of scope, tasks table, rollout, risks
- `openspec/changes/CHG-0032/tasks/TASK-0035.md` through `TASK-0041.md` — per-task summary, definition of done (post-hoc checklist), commit SHA, notes
- `openspec/specs/audit/methodology.spec.md` — REQ-AUDIT-0001 (corpus-persistence requirement); status: draft

**Persistent audit artifact (staging, per ADR-0002 §7):**
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/README.md` — session metadata + method
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/consolidated.md` — ~70 themes across 36 streams; proposed 17-tier resolution sequence (Tier 0 = doc-only sync, Tier 16 = artifact rebaseline)
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/findings-index.md` — per-stream provenance ledger; theme → constituent finding IDs
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/qd-triage.md` — Quality-Diversity triage; per-method σ × κ scoring (Waves 1-4; §3.5 Wave-5 pending); QD matrix occupancy; Tier A/B/C/D catalog; ACGR diagnostic; Wave-5 admission targets; methodology ADR draft clauses §§1-11
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/corrections.md` — Wave-5 META- audit corrections: 19 corrections (4 CRIT / 12 SER / 3 PROC) against consolidated.md, qd-triage.md, and findings-index.md. Authoritative for corrected attributions and counts pending the qd-triage.md §3.5 re-issue (TASK-0044).
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/raw-transcripts/` — 35 sub-agent `.jsonl` transcripts (full conversation logs incl. tool calls); MANIFEST.md maps stream prefix → file; persist-corpus.py is the one-shot extraction tool
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/findings/` — 35 per-stream extracted findings markdown files (sub-agent's initial prompt + final deliverable text); the human-readable evidence base for the audit; use this for re-clustering, implementation-audit calibration, or resolution-CHG drafting

**Convergence projection (under ACGR metric, qd-triage.md §7):** Wave 4 = ~45%; Wave 5 (Tier-1 empty-cell targets + meta-review = 4 streams) projected ~10-15%; Wave 6 (remaining empty cells + confirmation pairs) projected <5% (convergence). Compression × * lens has no Tier-A occupant (DISTILL is Tier B only); flag this as a known gap in the methodology codification ADR. <!-- spec-lint: allow prose-xref-banned -->  <!-- the methodology codification ADR has no allocated ID yet; queued per user direction post-implementation-audit -->

**Commit trailers (per CLAUDE.md, mandatory):**

```
Task: TASK-NNNN
Requirements: REQ-<X>-NNNN[, ...]
Tests-Status: <none|red|red→green|green|deprecated>
Phase: PHASE-1
```

Last TASK number used: TASK-0041 (CHG-0032 envelope authoring). Next available: TASK-0042. No `--no-verify`, no hook bypass.
