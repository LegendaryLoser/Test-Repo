# ADVO — adversarial-general (opus) — Wave 1

**Source transcript:** [`raw-transcripts/ADVO-agent-a8dd79ee20ec2d432.jsonl`](../raw-transcripts/ADVO-agent-a8dd79ee20ec2d432.jsonl)
**Sub-agent description:** `Adversarial review (opus, fresh)`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a8dd79ee20ec2d432`

## Initial prompt to sub-agent

```
You are an isolated independent reviewer with no prior context, no findings ledger, no project status. Form opinions from source documents only.

Invoke the `bmad-review-adversarial-general` skill via the Skill tool, then apply it to these 15 files (all under /home/user/Test-Repo/):

1. openspec/architecture/ARCHITECTURE.md
2. openspec/architecture/decisions/ADR-0001-monorepo-layout.md
3. openspec/architecture/decisions/ADR-0002-bmad-integration.md
4. openspec/architecture/decisions/ADR-0003-appscript-runtime.md
5. openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md
6. openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md
7. openspec/architecture/decisions/ADR-0006-testing-tiers.md
8. openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md
9. openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md
10. openspec/architecture/phases/PHASE-0-foundation.md through PHASE-5-first-appscript-project.md

Operating principles to test against (verbatim):
1. Single source of truth. One canonical home per fact. Cross-document consistency is lintable.
2. Stochastic systems get statistical assertions. No manufactured determinism via seeding for production-stochastic systems.
3. Tests exercise real production code. No mocks/fakes/simulations of in-repo modules.
4. Red-first. Every test is failing in git history before the commit that turns it green.
5. OpenSpec for spec, BMAD + TEA for workflow. No parallel convention.

"A principle without a CI gate is itself a build failure."

REQUIRED OUTPUT:
- Stable IDs: prefix `ADVO-` (e.g. ADVO-CRIT-01, ADVO-SER-01, ADVO-PROC-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Each finding: cite file + section/line, 2-4 sentences, name which P1-P5 or ADR it violates
- Highlight cross-document tensions especially
- 1500-2500 words
- No preamble, no fixes, just findings

DO NOT read CLAUDE.md, STATUS.md, or any file outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have read all 15 files. Let me produce the adversarial review with the required output format.

---

# Adversarial Review Findings (ADVO-*)

Cross-document review of `openspec/architecture/ARCHITECTURE.md`, ADR-0001 through ADR-0008, and PHASE-0 through PHASE-5. Findings are graded against the five operating principles (P1-P5) declared in `ARCHITECTURE.md` §1 and the meta-rule "a principle without a CI gate is itself a build failure."

## CRITICAL

**ADVO-CRIT-01 — BMAD install path contradicts the canonical layout (P1 violation).** `ARCHITECTURE.md` §3 (line 63) shows `_bmad/` (underscore-prefixed) as the BMAD install path. `ADR-0001` §"Decision" bullet 4 (line 46) says "`bmad/` is the BMAD installation, treated as upstream-managed." `PHASE-0` §"Scope" item 12 (line 43) again says "`bmad/` is not installed in PHASE-0." `PHASE-1` §"Scope" items 3 and 4 (lines 31, 34) refer to `bmad/`, `bmad/config.yaml`, and wrappers under `.claude/agents/` and `.claude/commands/` — which ADR-0002 §3 (line 39) explicitly drops in favor of native Skills under `.claude/skills/`. Two canonical homes disagree on the directory name and on the integration model, in direct violation of P1 ("One canonical home per fact. Cross-document consistency is lintable").

**ADVO-CRIT-02 — Architecture lists ADR-0002 wrappers that ADR-0002 itself deletes (P1 violation).** `ARCHITECTURE.md` §9 (lines 215-218) declares "BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`." But `ADR-0002` Amendment 0001 (line 204) records "Integration: native Claude Code Skills under `.claude/skills/` (was thin wrappers under `.claude/agents/` and `.claude/commands/`)" — i.e., the wrapper layer was deleted. ARCHITECTURE.md §9 references the stale model and ARCHITECTURE.md §3 (lines 55-56) even marks `.claude/agents/` and `.claude/commands/` as "legacy slot — empty in v6 native-skills model" while §9 still describes them as the surfacing mechanism. The frozen architecture artifact is internally incoherent.

**ADVO-CRIT-03 — REQ-ARCH-0008 cites a hook list that has since grown an amendment (P1, P5 violation).** `ARCHITECTURE.md` §10 REQ-ARCH-0008 (line 240-241) requires "hooks declared in ADR-0005 are listed." ADR-0005 was amended (Amendment 0001, line 187) to add `PostToolUse(mcp__github__merge_pull_request)` and extend the `Stop`/`SessionEnd` push semantics. PHASE-0 §"Exit criteria" (line 57) restates REQ-ARCH-0008 verbatim without acknowledging the amended hook set, and `.claude/settings.json` declarations are pinned at PHASE-0. There is no statement of which hook list — pre-amendment or post-amendment — PHASE-0 must satisfy, and no migration path. A frozen artifact that points at a mutable spec is not frozen.

**ADVO-CRIT-04 — `gate-coverage` is structurally impossible to satisfy for several principles (meta-rule violation).** `ADR-0008` §1 (lines 23-50) maps every gate to an ADR section but does not map a single gate to P1 or P5 directly. P1 ("single source of truth") is enforced obliquely by `index-up-to-date`, `xref-resolves`, etc., but `gate-coverage` (§2, lines 52-57) "walks every ADR and every principle in ARCHITECTURE.md §1 and verifies that at least one entry in the table above references it." The Enforces column references ADRs, not principles, so a literal walk over principles P1-P5 will fail. The meta-gate is described as self-enforcing, but the inventory it references does not contain principle citations — the gate cannot be passing today on a literal reading of its own definition.

**ADVO-CRIT-05 — Red-first (P4) is logically impossible for the PHASE-0 hook decision (P4 violation).** `PHASE-0` §"Scope" item 9 (line 37) ships `.claude/settings.json` "with hook declarations pointing at placeholder commands that exit 0 with a TODO comment." The placeholder commands trivially pass any test. PHASE-0 §"Exit criteria" REQ-ARCH-0008 (line 57) requires the declarations be present and tests-green. There is no plausible red-state for "the placeholder exits 0," meaning REQ-ARCH-0008 transitions directly from `draft` to `tests-green` without `tests-red`. ADR-0005 §4 (lines 70-72) explicitly forbids this: "A REQ may not skip from `draft` to `tests-green`." The foundation phase violates P4 by construction.

**ADVO-CRIT-06 — ADR-0002 §7 numbering implies missing sections 2-6 (P1 violation, structural defect).** `ADR-0002` jumps from "Decision" sub-items 1-7 (lines 28-65) directly to top-level section "## 7. Staging discipline" (line 67), then `## 8`, `## 9`, then `## Consequences`. There are no sections numbered ## 2 through ## 6 anywhere in the document; the top-level numbering starts at 7. Cross-references to "ADR-0002 §7", "ADR-0002 §8", "ADR-0002 §9" from ADR-0005 amendment log and PHASE-2/PHASE-5 are therefore brittle — any reader following the convention used in every other ADR will look for ## 1 through ## 6 and find Decision sub-items instead. Anti-aliasing under ADR-0004 §4 (line 70) is precisely the kind of defect this ought to fire on.

## SERIOUS

**ADVO-SER-01 — `prose-xref-banned` exemplars would themselves fail the rule (P1 violation, self-referential defect).** `ADR-0004` §2 (lines 51-56) lists "the auth spec / the login requirement / the original ADR" as forbidden prose patterns. `ADR-0002` §7 (line 90) refers to "the act of moving a draft from staging to its canonical home" — prose, no ID. `ADR-0005` §10 amendment (line 187) refers to "PR #2" and "a post-merge rebase" — neither is a stable ID + path. `ADR-0007` §"Consequences" (line 81) refers to "Sonnet 4.6 → 4.7" — no model ID, no path. The lint rule will either fire on its own ADRs at PHASE-1 enablement or its scope is silently narrowed. Either way the documents and the rule are inconsistent.

**ADVO-SER-02 — Test annotation requirements collide with red-first semantics (P3/P4 tension).** `ADR-0005` §3 (lines 53-59) makes `Tests-Status: <none|red|red→green|green|deprecated>` a mandatory trailer. `ADR-0006` §4 (lines 60-66) introduces the `Bootstrap: <reason>` trailer for bulk-green-start. Neither ADR defines what happens when a single commit advances some tests red→green and introduces other tests as net-new red. Is the commit `red→green` or `red`? `ADR-0008` (lines 41, 88-93) declares `red-before-green` and `commit-trailers-valid` as gates but no ADR enumerates the valid combinations or transitions. Practitioners will guess; CI will be silently lenient.

**ADVO-SER-03 — The "no mocks" rule contradicts its own permitted exception (P3 violation).** `ADR-0006` §2 (lines 32-49) bans "hand-rolled fakes (`class FakeFoo implements IFoo`) of in-repo interfaces" while permitting "substituting the HTTP transport at the network boundary (e.g. a real `nock` interceptor that records and replays *real* responses captured from the real service)." A `nock` interceptor that replays recorded responses **is** a record-and-replay mock of the network surface — it does not contact the real service at test time, so the test no longer "exercises real production code" through that path. The exception undermines P3 while the prose claims otherwise. ADR-0007 §2 (line 33) separately bans recorded fixtures for the LLM tier only, which makes this inconsistency worse, not better.

**ADVO-SER-04 — Sample-size confidence intervals at small N are scientifically dishonest (P2 hazard).** `ADR-0007` §3 fourth bullet (lines 45-47) permits "Distributional assertions over N runs. Sample size declared; assertion is a confidence interval, Kolmogorov–Smirnov test, or similar. Sample size and threshold are pinned per test." Nothing pins a **minimum** N, nothing requires power analysis, and nothing prevents authors from declaring `N=5` and a 99% interval that is meaninglessly wide. P2 demands "statistical assertions," but unbounded latitude on N and threshold lets an author claim P2 compliance with a test that asserts essentially nothing. ADR-0008 has no gate that scrutinizes statistical-power validity.

**ADVO-SER-05 — Anti-aliasing threshold pinning circularity (P1 violation).** `ADR-0004` §4 (lines 70-75) says "the threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." `tools/spec_lint/` is delivered in PHASE-1; the config does not yet exist in PHASE-0. ADR-0004 declares the rule in PHASE-0 but the rule's parameters are unspecified until PHASE-1. ADR-0008 §1 (line 34) lists `anti-aliasing` as "every PR" — but in PHASE-0 the gate has no configuration and therefore cannot meaningfully run. Either the gate is silently disabled (violating "every PR") or it fails closed (blocking all PHASE-0 work).

**ADVO-SER-06 — Push invariant is unenforceable on its own terms (P1 violation).** `ADR-0005` §6 (lines 108-112) admits "the invariant is otherwise unenforceable and silently rots." The mitigation is three hooks. ADR-0008 §1 lists no `push-invariant` CI gate; the invariant is declared without a corresponding entry in the gate inventory. By the meta-rule "a principle without a gate is a build failure," and the invariant is functionally a principle of ADR-0005 §6. `gate-coverage` walks ADRs but the invariant lives inside an ADR section without its own gate citation, so the meta-gate will not catch the omission.

**ADVO-SER-07 — Checkpoint exemption file is a back door around P4 (P4 violation).** `ADR-0008` §6 (lines 87-93) names `tools/trace/checkpoint_exemptions.yaml` as "the only sanctioned partial-bypass." Neither ADR-0005 §7 (lines 115-138) nor ADR-0008 enumerates which gates are exempted; the contents of the file are the source of truth. This means the exact scope of "Checkpoint: true" is configuration, not architecture, and can be silently widened in any PR that touches the YAML. P4 enforcement depends on a file the ADRs do not constrain.

**ADVO-SER-08 — PHASE-5 entry criteria reach outside the architecture artifact (P5 violation).** `PHASE-5` §"Entry criteria" (lines 23-27) requires "Product side has produced (in a separate PR chain): `openspec/vision.md`, ≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage, ≥ 1 Story." `ARCHITECTURE.md` §12 (lines 264-269) declares product content is **not** in this document and is empty templates until a "separate product PR." Nothing in any ADR or any phase document specifies how the product PR chain is sequenced relative to PHASE-0 through PHASE-4. PHASE-5 cannot start without product content, but the architecture does not own product content. This is a hidden cross-cut that P5 forbids ("no parallel convention").

**ADVO-SER-09 — Phase-exit and gate-coverage are mutually dependent (structural defect).** `ADR-0008` §3 (lines 60-69) declares `phase-exit` requires the next phase's entry ADR (if any) to be `status: accepted`. `ADR-0008` §"Compliance" (lines 102-106) says "PHASE-0 commits the workflow YAML stubs (jobs declared, scripts as TODO). PHASE-1 and PHASE-2 implement the gates." Therefore at PHASE-0 exit, `gate-coverage` itself is a TODO stub. The meta-gate enforcing "every principle has a gate" is not yet operational at the precise moment PHASE-0 needs to exit. Either PHASE-0 exits with the meta-gate unenforced (defeating its purpose) or PHASE-0 cannot exit (deadlock).

**ADVO-SER-10 — REQ atomicity rule is undefined for compound test annotations (P1 tension).** `ADR-0004` §3 (lines 60-66) requires "one REQ contains one assertion … A REQ that decomposes into more than one Given/When/Then is a defect." `ADR-0006` §6 (lines 78-81) requires `@covers REQ-X-NNNN [, ...]` allowing one test to cover multiple REQs. If atomicity at the REQ side is enforced, then plural `@covers` is either (a) genuinely useful and atomicity is bypassed by combining REQs in tests, or (b) the test is itself testing more than one assertion, contradicting tier coverage clarity. Neither ADR resolves the contradiction.

## PROCESS

**ADVO-PROC-01 — Identifier allocation is racy (P1 weakness).** `ADR-0004` §1 (line 42) describes allocation as "monotonic next-free scan against `openspec/specs/INDEX.yaml`. Hand-allocation is permitted but checked." Concurrent PRs by different sessions or agents will both scan the same INDEX, both allocate the same next ID, and CI will only catch the collision at merge — which is exactly the failure mode P1 wants prevented. No reservation, locking, or merge-time reallocation protocol is specified.

**ADVO-PROC-02 — "Quarterly review" obligations have no owner (P5 weakness).** `ADR-0004` §4 (line 74) mentions "reviewed quarterly (a `gate`-type task)." No ADR defines a `gate`-type task; the term is used in ADR-0001 §"Compliance," ADR-0008 §1 ("phase-exit"), and ADR-0004 §4, but never defined. BMAD + TEA workflow (P5) does not include this terminology, so an unnamed parallel concept is being introduced without an ADR — directly forbidden by ARCHITECTURE.md §12 third bullet.

**ADVO-PROC-03 — PHASE-1 BMAD installation conflicts with ADR-0002's vendored model (P1/P5 process violation).** `PHASE-1` §"Scope" items 3 and 4 (lines 31-34) call for `bmad/` installation "pinned in `bmad/config.yaml`" plus wrappers in `.claude/agents/` and `.claude/commands/`. `ADR-0002` (lines 28-65) replaces `bmad/` with `_bmad/`, replaces `bmad/config.yaml` with `_bmad/_config/manifest.yaml`, drops wrappers entirely. PHASE-1 is the file an implementer reads to know what to build; following PHASE-1 verbatim produces an architecture that violates ADR-0002. The phase file was not updated when ADR-0002 was amended.

**ADVO-PROC-04 — PHASE-5 scope numbering repeats (process defect).** `PHASE-5` §"Scope" (lines 30-50) numbers items 1, 2, 3, **4**, **4**, 5, 6 — item 4 is used twice (lines 36-46 and line 47). This is a trivial editing failure but the file is one of the eight that REQ-ARCH-0002 considers a deliverable; if PHASE-0 exit criteria includes "all ADRs and phase files present," the file is present but malformed. The matrix and audit tools cannot rely on stable item references.

**ADVO-PROC-05 — Append-only journal ignores schema evolution (P1 risk).** `ADR-0005` §5 (lines 75-89) defines the JSONL event schema as a closed table. No version field is included in any event. An append-only log with no schema version is a time bomb: the first amendment to the event shape forces either parser branching by date or rewriting history. ADR-0005 mandates the latter is forbidden ("append-only"). No migration story exists.

**ADVO-PROC-06 — "BMAD + TEA" is asymmetric in document weight (P5 weakness).** ARCHITECTURE.md §1 P5 (lines 32-33) names BMAD and TEA equally. ADR-0002 covers BMAD in depth (210 lines). TEA receives one bullet in ADR-0002 §"Decision" item 7 (lines 63-65) saying tooling integration "lives under `tools/tea/` (PHASE-1+ work; not yet implemented)." No ADR defines TEA's persona surface, its interface to OpenSpec, its test-authoring contract, or its relationship to Stories vs Epics. Half of P5 is unspecified.

**ADVO-PROC-07 — Coverage gate redefines orphan and circular constraints loosely (P1 weakness).** `ADR-0006` §5 (lines 70-75) declares "every test maps to ≥ 1 REQ. No orphans." But the matrix is **derived** from `@covers` annotations (ADR-0005 §1 source 3). A test with a typo in `@covers` (`REQ-AUTH-007` vs `REQ-AUTH-0007`) silently becomes an orphan or a covering test for a non-existent REQ. ADR-0008's `req-coverage-100` gate (line 43) does not specify how typo-induced ghost REQs are surfaced.

**ADVO-PROC-08 — `Material-Architecture-Change: true` trailer is ungoverned (P1 weakness).** `ARCHITECTURE.md` lines 11-13 say "Modifications to the structure described here require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate." ADR-0005 §3 enumerates four mandatory trailers and does not include this one. ADR-0008 §1 has no gate validating that material architectural changes carry the trailer. The escape hatch from ADR-governance exists but is not enforced — anyone can declare a material change without one, and CI will not notice.

**ADVO-PROC-09 — Phase status field is hand-maintained without ADR backing (P1 weakness).** Every phase file's frontmatter has `status: in-progress` or `status: pending`. Nothing in any ADR explains who flips the status, what gate updates it, or how it relates to `phase-exit`. PHASE-0 is `in-progress` and PHASE-1 is `pending`, but a successful PHASE-0 merge to main does not — per any ADR — automatically promote PHASE-1 to `in-progress`. Hand-editing the field violates the spirit of P1 (single source of truth: matrix is the truth, frontmatter is hand-edited cache).
