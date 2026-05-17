# Project status

**Authoritative human-readable session-resume document.** Hand-maintained
until PHASE-2's `SessionStart` resume hook + `tools/trace/rebuild.py`
mechanize it. New sessions: read this file first, then the active
PHASE file (per [ARCHITECTURE.md §11](architecture/ARCHITECTURE.md)),
then proceed.

**Schema enforced by:** `tools/ci/tests/test_status_resume.py`
(asserts the five `##` section headers below exist).

---

**Last updated:** 2026-05-17 (architecture audit session, branch `claude/bmad-architecture-review-sV42w`)
**Active phase:** PHASE-1 (paused — BMAD audit track in progress)
**Last master commit:** `455ba06` (PR #15 merged: CHG-0014 + CHG-0031)
**Last branch commit** (`claude/bmad-architecture-review-sV42w`): see `git log -1` — most recent work is CHG-0032 QD triage of all 36 audit streams + this STATUS.md staleness sweep
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

- [~] BMAD adversarial review of architecture (per user request — NEW-3): Waves 1-4 complete (36 streams, ~700 findings, ~70 themes); QD triage complete (qd-triage.md); Wave 5 pending (4 streams targeting Tier-1 empty cells per qd-triage.md §8)
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

## Next session: start here

**Current state of the architecture audit (CHG-0032):**

- Waves 1, 2, 3, 4 all complete — 36 streams total, ~700 raw findings, ~70 themes (de-duplicated).
- All findings consolidated and triaged. Per-stream provenance preserved.
- Quality-Diversity (QD) framework adopted (see Recent decisions row "Adopt Quality-Diversity framework"). Replaces COMPOSITE-V2 Gate 6 marginal-novelty rule with σ × κ Pareto admission + ACGR convergence metric. Research-grounded in MAP-Elites + Mixture-of-Complementary-Agents + ambiguity decomposition.
- Per-method tier assignment complete: 16 Tier A, ~10 Tier B, 1 Tier C, 4 Tier D candidates (COURSE, CHECK, EDIT, VALID2 — deprecation deferred for implementation-audit confirmation).
- Wave 5 empty-cell targets identified: 5 high-importance Axis-D cells empty + (compression × *) has only a Tier-B occupant. See qd-triage.md §8.
- Architecture audit has NOT yet hit the new convergence criterion (Wave 4 ACGR ~45%); Wave 5 projected ~10-15%; Wave 6 projected <5% (target met).

**Read in this order before doing anything else:**

1. This file (STATUS.md), especially the CHG status table, Audit findings ledger, Open architectural questions, and Recent decisions.
2. `openspec/architecture/ARCHITECTURE.md` §1 (principles) and §11 (active phase).
3. `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/qd-triage.md` — the full QD triage. Required reading: §2 (framework definitions), §5 (Tier A/B/C/D catalog), §7 (ACGR convergence diagnostic), §8 (Wave 5 admission targets), §9 (draft clauses for methodology ADR).
4. `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/consolidated.md` — the ~70 themes, organised by tier of confirmation; required if planning resolution CHGs, otherwise reference-only.

**First action on resume:** ask the user which next move they want.

The two defensible orderings are:
- **(a)** Run Wave 5 architecture audit first (4 streams targeting Tier-1 empty cells per qd-triage.md §8). Closes architecture audit to ACGR <15%, then either iterate to Wave 6 or call it converged-enough and move to implementation audit.
- **(b)** Start implementation audit now against `tools/spec_lint/`, `tools/ci/`, `_bmad/`, `.github/workflows/`, using the QD catalog from qd-triage.md §5 dogfood-style. Accept architecture-audit non-convergence on the basis that Wave 4 produced no new BLOCKING findings (only new themes; severity distribution stable).

User's standing direction (Recent decisions, 2026-05-17 "Run implementation audit after architecture audit convergence; consolidate jointly") favours (a). But the implementation audit was originally planned under COMPOSITE-V2, and the QD framework adopted since then changes the convergence calculus — worth re-asking.

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
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/qd-triage.md` — Quality-Diversity triage; per-method σ × κ scoring; QD matrix occupancy; Tier A/B/C/D catalog; ACGR diagnostic; Wave-5 admission targets; methodology ADR draft clauses §§1-11
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
