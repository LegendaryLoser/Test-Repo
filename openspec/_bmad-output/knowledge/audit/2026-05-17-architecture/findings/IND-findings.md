# IND — adversarial-general (opus) — Wave 1

**Source transcript:** [`raw-transcripts/IND-agent-a537eb5fa60f4e72c.jsonl`](../raw-transcripts/IND-agent-a537eb5fa60f4e72c.jsonl)
**Sub-agent description:** `Independent architecture adversarial review`
**Session ID:** `5a4de7c4-d271-4b87-9aa6-c969dd59f654`
**Agent ID:** `a537eb5fa60f4e72c`

## Initial prompt to sub-agent

```
You are running as an isolated, independent reviewer. You have no access to prior conversation context, no prior findings ledger, and no project status document. Form your own opinions from the source documents only.

## Task

Perform a cynical adversarial review of an architecture artifact. Invoke the `bmad-review-adversarial-general` skill via the Skill tool to load the BMAD reviewer methodology, then apply it to the documents listed below.

## Documents to review (15 files, all under /home/user/Test-Repo/)

1. openspec/architecture/ARCHITECTURE.md
2. openspec/architecture/decisions/ADR-0001-monorepo-layout.md
3. openspec/architecture/decisions/ADR-0002-bmad-integration.md
4. openspec/architecture/decisions/ADR-0003-appscript-runtime.md
5. openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md
6. openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md
7. openspec/architecture/decisions/ADR-0006-testing-tiers.md
8. openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md
9. openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md
10. openspec/architecture/phases/PHASE-0-foundation.md
11. openspec/architecture/phases/PHASE-1-spec-hygiene.md
12. openspec/architecture/phases/PHASE-2-traceability-runtime.md
13. openspec/architecture/phases/PHASE-3-anthropic-client.md
14. openspec/architecture/phases/PHASE-4-shared-libs.md
15. openspec/architecture/phases/PHASE-5-first-appscript-project.md

## Operating principles to test the artifact against (verbatim from the project)

1. **Single source of truth (SoT).** One canonical home per fact. Cross-document consistency is lintable.
2. **Stochastic systems get statistical assertions.** Determinism is never manufactured by seeding for systems that are not deterministic in production.
3. **Tests exercise real production code.** No mocks, fakes, or simulations of in-repo modules. Boundary adapters are real; only network transport may be substituted at the edge.
4. **Red-first.** Every test exists in a failing state in git history before the commit that turns it green.
5. **OpenSpec for specification, BMAD + TEA for workflow.** No parallel convention is introduced.

A principle without a CI gate is itself a build failure.

## Required output

A structured findings report with:

- **Stable IDs** using the prefix `IND-` (for "independent review") followed by severity tier and zero-padded number, e.g. `IND-CRIT-01`, `IND-SER-01`, `IND-PROC-01`.
- **Three severity tiers**: CRITICAL (internally contradictory or block correctness), SERIOUS (gaps or weakened enforcement), PROCESS (workflow, conventions, drift).
- **Minimum 15 findings.** Find at least that many; the BMAD skill requires at least 10 and this artifact is large enough to warrant more.
- **Each finding** must cite the specific file and section/line where the issue lives, describe the problem in 2-4 sentences, and state which operating principle (P1-P5) or named ADR it conflicts with.
- **Cross-document tension detection** is especially valuable — call out cases where two documents in this set say different things.

## What NOT to do

- Do not read any file outside the 15 listed above. Do not read STATUS.md, CLAUDE.md (you may infer its required content from REQ-ARCH-0007), tools/, _bmad/, or any prior findings document.
- Do not soften findings. The point is adversarial — be skeptical, assume the authors missed things.
- Do not propose fixes; just report findings. Fixes are downstream.

## Output budget

Report in 1500-3000 words. Concise findings beat verbose ones. Do not include preamble or skill-invocation commentary; just the report.
```

## Findings deliverable (final assistant message)

I have all 15 documents. Now I'll produce the adversarial findings report.

# Independent Adversarial Review — Architecture Artifact

**Reviewer:** isolated, no prior context. Source documents only. Findings prefixed `IND-`.

---

## CRITICAL findings (internally contradictory or block correctness)

### IND-CRIT-01 — Top-level layout in ARCHITECTURE.md §3 contradicts ADR-0001 and ADR-0002

`ARCHITECTURE.md` §3 lists `_bmad/` (underscore-prefixed) as the BMAD install path, citing "ADR-0002 amendment 0001". But `ADR-0001` §"Decision" still says `bmad/` (no underscore) is the BMAD installation, and ARCHITECTURE.md §9 also says "BMAD agents live under `bmad/`". Two top-level directories (`bmad/` vs `_bmad/`) cannot both be the canonical home. This is a direct P1 (Single Source of Truth) violation, baked into the very document that demands SoT. ADR-0001 was never amended to reflect ADR-0002's rewrite.

### IND-CRIT-02 — ARCHITECTURE.md §9 describes a wrapper model that ADR-0002 explicitly retired

ARCHITECTURE.md §9 reads: "BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by file path…". ADR-0002 §3 and amendment 0001 say native Skills are used instead, that `.claude/agents/` and `.claude/commands/` are legacy/empty slots, and that "no wrapper files" exist. ARCHITECTURE.md is supposed to be the authoritative narrative; it propagates the rejected design. P1 fails again.

### IND-CRIT-03 — PHASE-1 reinstates the retired wrapper design

`PHASE-1-spec-hygiene.md` §Scope item 4 mandates: "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA) and core commands", and §Exit criteria requires "All BMAD wrapper files in `.claude/agents/` and `.claude/commands/` resolve their `Load:` paths." This is in direct conflict with ADR-0002 amendment 0001 ("No wrapper files"). The exit gate cannot be satisfied without violating ADR-0002. P5 (no parallel convention) and P1 both broken.

### IND-CRIT-04 — PHASE-1 pins BMAD via `bmad/config.yaml`; ADR-0002 pins via `_bmad/_config/manifest.yaml`

PHASE-1 §Scope item 3 says "`bmad/` installation per ADR-0002, pinned in `bmad/config.yaml`". ADR-0002 §Decision item 1 says version is pinned in `_bmad/_config/manifest.yaml`, and §Compliance reinforces this. Two distinct canonical homes for the version pin — the principle most catastrophically violated by exactly this kind of drift. There is also no `bmad/config.yaml` anywhere in ADR-0002's layout.

### IND-CRIT-05 — PHASE-0 forbids what PHASE-1 requires (BMAD install timing)

PHASE-0 scope item 12 says: "`bmad/` is **not** installed in PHASE-0; it lands in PHASE-1 alongside `tools/spec_lint`." But ARCHITECTURE.md §3 shows the layout including `_bmad/` and `.claude/skills/` populated, and REQ-ARCH-0001 (a PHASE-0 exit criterion) requires "Repository contains the top-level layout in §3 (no extra top-level directories without an ADR)." If `_bmad/` and `.claude/skills/` are in §3 but PHASE-0 forbids installing them, REQ-ARCH-0001's PHASE-0 exit gate cannot pass. The phase contradicts its own exit criterion.

### IND-CRIT-06 — ADR-0008 §1 gate inventory does not enforce P2 or P5

ADR-0008 §2 ("gate-coverage gate") asserts every principle in ARCHITECTURE.md §1 must be referenced by at least one gate. Scanning the inventory: P2 (stochastic systems get statistical assertions) is referenced only indirectly via ADR-0007 gates; P5 (OpenSpec for spec, BMAD+TEA for workflow; no parallel conventions) has no gate row that names it at all. Per the document's own meta-rule ("a principle without a CI gate is a build failure"), the artifact ships with two principles uncovered. `gate-coverage` either fails on day one or its specification is too loose to detect this.

### IND-CRIT-07 — PHASE-2 introduces gates that ADR-0008's inventory does not list

PHASE-2 §Scope item 4 introduces `skill-removal-acknowledged`, `bmad-version-pin`, and `bmad-smoke-test` gates. ADR-0008 §1 is supposed to be the complete gate inventory ("This ADR enumerates **every** CI gate"). Those three gates do not appear in the table. Either ADR-0008 is not the single source of truth for gates (P1 violated), or PHASE-2 introduces ungated gates (`gate-coverage` semantics broken — the gate cannot map to any ADR row, so the meta-gate must fail).

### IND-CRIT-08 — Push invariant is unenforceable in the failure mode it claims to fix

ADR-0005 §6 (amendment) and §8 admit: "residual loss only if both hooks fail to fire (e.g. abrupt container reclaim mid-`PostToolUse`)." The very scenario the invariant was added to fix (container reclaim after commit before push) remains possible if reclaim happens between the commit completing and the PostToolUse hook firing — exactly the timing window that originally motivated the amendment. The ADR text simultaneously presents the invariant as authoritative and acknowledges its own gap, with no compensating gate. P-by-CI-gate principle broken: the invariant has no enforcement that catches the failure mode it was created for.

---

## SERIOUS findings (gaps, weakened enforcement, missing mechanisms)

### IND-SER-01 — "A principle without a CI gate is a build failure" is not actually a gate

ARCHITECTURE.md §1 and ADR-0008 both elevate the meta-principle that an unenforced principle is itself a build failure. `gate-coverage` claims to implement this. But `gate-coverage` is described as walking "every ADR and every principle in ARCHITECTURE.md §1" — there is no specification of how it parses principles, what counts as "referencing", or how it distinguishes a referenced-but-uncovered principle from a referenced-and-covered one. Without that, the gate is a slogan, not a check. The artifact violates its own rule (a principle without a precisely specified gate is a build failure) by relying on a vaguely specified meta-gate.

### IND-SER-02 — Anti-aliasing rule has no defined threshold

ADR-0004 §4 says n-gram similarity threshold is "pinned in `tools/spec_lint/config.yaml` and reviewed quarterly." No threshold value is given anywhere in the architecture artifact. Without a concrete number, two reviewers will disagree on whether the rule is implemented correctly; it cannot be red-tested in PHASE-1 because the green condition is undefined. This is precisely the kind of stochastic/threshold quantity that P2 demands be pinned with sample sizes — none is given.

### IND-SER-03 — Stochastic distributional assertions lack a corpus-wide policy

ADR-0007 §3 permits "confidence interval, Kolmogorov–Smirnov test, or similar" with "sample size and threshold pinned per test." There is no guidance on multiple-comparisons correction across the test suite, on flaky-test rate budgets, or on how confidence intervals interact with `req-coverage-100`. With dozens of stochastic tests each at, say, p=0.05, the false-failure rate on a green PR will be unacceptable — yet there is no gate, no budget, and no documented policy. P2 is claimed but only partially specified.

### IND-SER-04 — No definition of "boundary adapter" vs "in-repo module"

P3 and ADR-0006 §2 ban mocks of in-repo modules and permit transport substitution at the boundary, but neither defines what counts as "the network boundary" precisely. ADR-0006 §2 permits "real `nock` interceptor that records and replays *real* responses captured from the real service" — recorded responses are explicitly *banned* in ADR-0007 §2 for the LLM tier. The general rule and the specific rule do not align: a recorded response replayed by nock is a fixture, exactly the thing P2 forbids for stochastic systems and that P3 superficially welcomes for other tiers. The boundary line is fuzzy where it matters most.

### IND-SER-05 — Checkpoint commits create an unspecified P4 escape hatch

ADR-0005 §7 lets checkpoint commits skip "a defined subset of gates" (per `tools/trace/checkpoint_exemptions.yaml`). The exempted subset is not enumerated in the architecture artifact. CLAUDE.md guidance (per REQ-ARCH-0007) is supposed to cite the five principles verbatim, but the principle "every test exists in a failing state in git history before the commit that turns it green" has a silent carve-out for any branch that produced checkpoint commits whose squash strategy is at the next-non-checkpoint committer's discretion. P4 is weakened by an unspecified amount.

### IND-SER-06 — Red-before-green check walks "git history" — undefined scope

ADR-0005 §4: "`tools/trace/validate_commit.py` walks git history to verify." Walks back how far? Across rebases? Across squash merges to main? PHASE-2 §Scope describes a "synthetic local-and-bare-remote git repo" test but no semantics for history rewrites. P4 enforcement against a squashed PR (which Git increasingly defaults to) destroys the red-commit ancestor; the gate then cannot find the red state and either fails legitimate work or silently lets non-red-first work through.

### IND-SER-07 — REQ-ARCH-0008 references ADR-0005 hook list, but the list grew via amendment after REQ-ARCH-0008 was defined

REQ-ARCH-0008 says ".claude/settings.json is present; hooks declared in ADR-0005 are listed". ADR-0005 §10 amendment 0001 added `PostToolUse(mcp__github__merge_pull_request)` and extended others. PHASE-0 must declare all hooks from ADR-0005 §6 — but the amendment changed the hook list after PHASE-0's scope was specified. There is no statement of whether PHASE-0 needs to be re-gated. ARCHITECTURE.md §10 says material architecture changes require Phase-0 re-gate; an amendment that materially changes a PHASE-0 exit criterion is exactly that, but is not flagged.

### IND-SER-08 — INDEX.yaml is auto-generated; CLAUDE.md forbids hand-editing it after PHASE-1 only

CLAUDE.md per its own quoted text "Hand-editing `openspec/specs/INDEX.yaml` after PHASE-1." But ADR-0004 §6 says INDEX is auto-generated full stop, and is "the sole retrieval surface for tooling." If the file is truly auto-generated, hand-editing should be forbidden always, not just after PHASE-1. The "after PHASE-1" qualifier implies hand-editing is permitted during PHASE-0/PHASE-1, weakening P1.

### IND-SER-09 — Pre-receive hook for commit-trailers-valid conflicts with checkpoint commits

ADR-0008 §1 lists `commit-trailers-valid` with trigger "pre-receive hook" and ADR-0005 §3 says the same. Pre-receive runs on the *server* on push; checkpoint commits (which omit standard trailers in favor of `Checkpoint: true`) will be pushed too. Nothing in ADR-0008 explains how the pre-receive hook recognises checkpoint exemptions, and the §6 bypass-discipline language says "any other hook-bypass flag are forbidden" — checkpoint commits effectively bypass the trailer rule. Either checkpoints get rejected at push (breaking ADR-0005 §6 push invariant on Stop hook) or the gate has an unspecified exception path.

### IND-SER-10 — `cost-budget` gate has no defined budget

ADR-0007 §4 says "CI aggregates per-PR and per-nightly budgets; exceeding the budget fails the build." No numeric budget is set anywhere in ADR-0007, ADR-0008, or any phase document. A budget gate without a budget cannot be implemented as specified. PHASE-3 §Exit criteria says "Stochastic tier cost stays within budget for two consecutive nightly runs" — also without a numeric budget.

### IND-SER-11 — `cache-hit-regression` baseline is circular

ADR-0007 §5 says regression below "a pinned threshold" fails the build. PHASE-3 §Exit criteria says "`cache-hit-regression` baseline established." The baseline is established in PHASE-3 *as* the exit criterion, but the gate is listed in ADR-0008 §1 as "every PR (PHASE-3+)" — meaning the gate has no operational threshold until the very PR that exits PHASE-3, creating a chicken-and-egg whereby the gate cannot block the regression it was designed to catch on the first PHASE-3+ PR.

### IND-SER-12 — ADR-0006 §2 allows "real" deterministic clocks but P2 forbids manufactured determinism

ADR-0006 §2 permits substituting clock/randomness via "a deterministic clock implementation that is itself production code, used in both prod and test paths." But for any system whose behavior depends on the clock (rate limiters, backoff jitter, time-based caches), a deterministic clock in test paths only is exactly what P2 forbids: manufactured determinism for a production-stochastic system. The "used in both prod and test paths" caveat doesn't save it — production usually uses the wall clock; only tests pin it. The exception is wider than P2 admits.

---

## PROCESS findings (workflow, conventions, drift)

### IND-PROC-01 — Amendment workflow contradicts immutability

ADR-0002 amendment 0001 says "Complete rewrite to match BMAD v6.6.0 empirical reality." ADR-0004 §1 says "Identifiers are immutable. Renames are forbidden; supersession is the only permitted change" and §7 says specs that are referenced are frozen. An ADR is identified by ID and referenced by other ADRs/phases. A "complete rewrite" of ADR-0002 violates the immutability discipline applied to specs. The amendment log allows rewriting body text while keeping the same ID — the same defect the spec rules call "catastrophic forgetting" in ADR-0004.

### IND-PROC-02 — PHASE-0 declares status "in-progress" but the artifact under review claims to be the immutable substrate

PHASE-0 frontmatter says `status: in-progress`. ARCHITECTURE.md preamble calls itself "the **frozen architecture artifact**." If PHASE-0 is in-progress, then ARCHITECTURE.md, ADRs, and phases are mid-stream, not frozen. Either the freeze claim is premature or the phase status is stale. P1: one fact (is the artifact frozen?) with two answers in two files.

### IND-PROC-03 — Date dishonesty risk: every ADR carries the same date (2026-05-16)

All eight ADRs frontmatter say `date: 2026-05-16`. Today's date per session context is 2026-05-17. Either eight ADRs were genuinely drafted in one day (plausible for a scaffolding push, but then the amendment log on ADR-0002/0005 with separate CHG numbers suggests later edits without date updates), or dates are being copy-pasted. The amendment log mechanism in ADR-0002/0005 has no date column on amendment rows, so post-amendment date drift is unobservable.

### IND-PROC-04 — Phase-exit gate uses status from spec frontmatter, but spec status enum is undefined in one direction

ADR-0004 §5 gives the status enum: `draft | tests-red | tests-green | reviewed | merged | deprecated`. ADR-0006 §5 uses "non-deprecated REQ" for coverage. ADR-0005 §4 forbids going from `draft` direct to `tests-green`. No rule defines the transition `tests-green → reviewed → merged`, and `phase-exit` (ADR-0008 §3) checks "tests-green" status. A REQ that has progressed to `reviewed` or `merged` may no longer be "tests-green" in spec frontmatter terms; the gate may then fail spuriously.

### IND-PROC-05 — ADR-0001 mentions `bmad/` as upstream-managed; ADR-0002 says it is vendored and committed

ADR-0001 §Decision: "`bmad/` is the BMAD installation, treated as upstream-managed". ADR-0002 §4: "Both `_bmad/` and `.claude/skills/` are committed to git." Vendored is the opposite of upstream-managed. P1 broken at the foundational layout ADR.

### IND-PROC-06 — Per-project openspec overlay is mentioned but unspecified

ARCHITECTURE.md §3 layout shows `projects/<project>/openspec/` (project-scoped). PHASE-5 §Scope item 4 mentions promoting drafts to `projects/<name>/openspec/briefs/`. There is no ADR governing how project-scoped REQ IDs interact with root REQ IDs (collision rules, allocation scope, INDEX merge semantics). ADR-0004 §1 says IDs are "scoped to the domain" — but `<domain>` rules across projects are not given. Two projects can both allocate `REQ-AUTH-0001` and both be locally consistent yet collide globally.

### IND-PROC-07 — Reference to "the paper" with no citation

ARCHITECTURE.md §2 and ADR-0004 reference "a published result on transformer associative memory ('the paper')". No DOI, arXiv ID, authors, or title appears anywhere. ADR-0004 §2 itself bans prose references ("the original ADR") as lintable defects. The phrase "the paper" is precisely the pattern banned. The architecture's own rule against fuzzy references is broken by the architecture's own foundational citation. P1 and ADR-0004 §2 violated by ADR-0004 itself.

---

**Total findings: 27 (8 CRITICAL, 12 SERIOUS, 7 PROCESS).** The dominant failure pattern is cross-document drift between ARCHITECTURE.md, ADR-0001, ADR-0002, ADR-0008, and the phase files — the very pattern P1 (SoT) and `gate-coverage` are supposed to make impossible. The artifact is approving its own scaffolding via principles it has not yet wired up.
