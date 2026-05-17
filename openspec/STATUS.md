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
**Last branch commit** (`claude/bmad-architecture-review-sV42w`): this commit (CHG-0032 architecture audit Wave 1+2 in flight)
**Open PRs:** none
**Test count:** 184 passing on master (audit commits do not change test count)

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
| 0014 | INDEX subcommand + populate INDEX.yaml                         | OPEN        | #15 |
| 0030 | Test annotation discipline + 87-test backfill                  | merged      | #13 (stacked) |
| 0031 | Session continuity scaffold                                    | merged      | (in #15) |
| 0032 | Architecture audit (BMAD multi-pass, COMPOSITE-V2)             | in-progress | TBD |

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
| AUDIT-2026-05-17 | INFO | Architecture audit Wave 1 (12) + Wave 2 (8) + Wave 3 (8) complete = 28 streams; ~559 raw findings → ~51 themes; COMPOSITE-V2 6/7 gates met; Gate 6 marginal novelty improving (Wave 1 baseline → Wave 2: ~50% → Wave 3: ~30-37%); theme-discovery rate halving per wave; projection: Gate 6 met in Wave 5 or 6; artifact at `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/` | IN-PROGRESS | CHG-0032 |

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
- [~] CHG-0031 — session continuity scaffold (this CHG)

### Tier 1 — close critical enforcement gaps

- [x] CHG-0013 — CI wiring (closed C4)
- [~] CHG-0014 — INDEX subcommand + populate (closes C1)
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

- [ ] BMAD adversarial review of architecture (per user request — NEW-3)
- [ ] BMAD adversarial review of implementation
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

## Next session: start here

**Status as of this commit:** CHG-0032 architecture audit Wave 1 (12
streams) complete and consolidated to
`openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/`. Wave 2
(8 sub-agents) running in background as of commit time; results will
land in a follow-up commit. COMPOSITE-V2 convergence metric locked
(see Recent decisions table); Gate 6 (marginal novelty <10%) is the
gating check.

**First action on resume:** check whether Wave 2 completed (sub-agent
output files in `/tmp/claude-0/-home-user-Test-Repo/.../tasks/`). If yes,
re-measure marginal novelty against COMPOSITE-V2 Gate 6. If <10%,
architecture audit converges; proceed to second action. If ≥10%, plan
Wave 3 with further orthogonal methods.

**Second action:** run BMAD multi-pass implementation audit against
`tools/spec_lint/`, `tools/ci/`, `_bmad/`, `.github/workflows/` using the
same COMPOSITE-V2 methodology (Wave 1 = 8-10 streams across diverse
methods/models, iterate until Gate 6 met).

**Third action:** consolidate architecture + implementation audit
findings jointly into a single ledger. Draft the audit-methodology ADR
(ADR-0009 or higher, allocated post-consolidation) codifying COMPOSITE-V2
for all future architecture and project-level audits. Per-project audits
applied dogfood-style.

**Fourth action:** plan resolution CHG sequence against the joint
ledger. Per user direction, do NOT start any Tier 1+ resolution CHG
(CHG-0014b drop `generated_at`, CHG-0015 REQ-ARCH migration, etc.) until
both audits converge and the joint resolution sequence is approved.

**Persistent audit artifact:**
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/README.md`
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/consolidated.md` (26 themes, 270 raw findings, proposed 17-tier resolution sequence)
- `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/findings-index.md` (per-stream provenance)
