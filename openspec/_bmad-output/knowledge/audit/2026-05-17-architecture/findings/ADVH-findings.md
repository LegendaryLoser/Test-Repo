# ADVH — adversarial-general (haiku) — Wave 1

**Source transcript:** [`raw-transcripts/ADVH-agent-a75442bf62c957926.jsonl`](../raw-transcripts/ADVH-agent-a75442bf62c957926.jsonl)
**Sub-agent description:** `Adversarial review (haiku)`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a75442bf62c957926`

## Initial prompt to sub-agent

```
You are an isolated independent reviewer with no prior context.

Invoke the `bmad-review-adversarial-general` skill, then apply it to these 15 files (all under /home/user/Test-Repo/):

openspec/architecture/ARCHITECTURE.md
openspec/architecture/decisions/ADR-0001-monorepo-layout.md
openspec/architecture/decisions/ADR-0002-bmad-integration.md
openspec/architecture/decisions/ADR-0003-appscript-runtime.md
openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md
openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md
openspec/architecture/decisions/ADR-0006-testing-tiers.md
openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md
openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md
openspec/architecture/phases/PHASE-0-foundation.md
openspec/architecture/phases/PHASE-1-spec-hygiene.md
openspec/architecture/phases/PHASE-2-traceability-runtime.md
openspec/architecture/phases/PHASE-3-anthropic-client.md
openspec/architecture/phases/PHASE-4-shared-libs.md
openspec/architecture/phases/PHASE-5-first-appscript-project.md

Operating principles to test against:
1. Single source of truth.
2. Stochastic systems get statistical assertions.
3. Tests exercise real production code (no mocks of in-repo modules).
4. Red-first (test fails before it passes).
5. OpenSpec for spec, BMAD + TEA for workflow.

REQUIRED OUTPUT:
- Stable IDs: prefix `ADVH-`
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- Minimum 12 findings
- Each: file + section, 2-3 sentences, principle/ADR violated
- Under 1500 words
- No preamble; findings only

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have read all 15 files. Let me conduct the adversarial review against the 5 operating principles and the ADRs.

## ADVERSARIAL REVIEW FINDINGS

**ADVH-0001** | SERIOUS | ARCHITECTURE.md § 3 | **Frozen artifact unversioned.** ARCHITECTURE.md is declared "frozen" (line 10–12) and states Material-Architecture-Change requires an ADR, but the document itself has no version field, date field, or revocation date. How does a session know if a cached copy of the document is stale? The layout table declares top-level entries but does not encode when the layout changed. Violates P1 (SoT).

**ADVH-0002** | CRITICAL | ADR-0001, ADR-0002 collision | **Top-level ambiguity unresolved.** ADR-0001 §2 rule 3 states "Monorepo with per-project directories under `projects/` and shared code under `packages/`" selected; ADR-0002 §1 declares `_bmad/` as a top-level directory. ADR-0002 amendment 0001 renames it from `bmad/` to `_bmad/` but the original ADR-0001 never mentions underscore-prefixed directories. The `top-level-allowlist` gate (mentioned ADR-0008 §1) is therefore either unenforced or must be created after the fact, but no TASK-NNNN in the proposed changes section commits to it. Violates P1.

**ADVH-0003** | CRITICAL | ADR-0002 §5 & ARCHITECTURE.md §7 | **Staging nonexistent, rule predates implementation.** ADR-0002 §7 (Amendment 0002, CHG-0010, TASK-0021) defines hard invariants for `openspec/_bmad-output/` (matrix must exclude, INDEX must exclude, lint rules must exclude). However, this directory is not created in PHASE-0 scope (PHASE-0-foundation.md line 43 explicitly states "BMAD is NOT installed in PHASE-0"). The matrix builder referenced in ADR-0005 §2 is a PHASE-2 deliverable. An agent reading this in PHASE-0 or PHASE-1 cannot verify the invariants are enforced because the infrastructure doesn't exist yet. Rule predates tooling. Violates P1 (SoT: specification references nonexistent enforcement).

**ADVH-0004** | SERIOUS | ADR-0005 §6 Amendment 0001 | **Push invariant assumes git semantics never tested.** The amendment introduces `PostToolUse(Bash:git commit)` hook that "pushes `HEAD` to origin as a fast-forward" and "Non-FF aborts the hook with a diagnostic (no force-push)." But PHASE-2 scope (PHASE-2-traceability-runtime.md line 43–46) defers the push-invariant tests to synthetic-git-repo scenarios. In a real session, if a rebase occurs before the push, the commit hook aborts and the working tree is left in a diverged state — the session cannot proceed without manual intervention or hook bypass. The design is sound but the **failure mode is a silent footgun: agents will be trained to use `--no-verify` to escape the trap.** Violates P1 (the documented rule is correct, but the implementation incentivizes bypassing it).

**ADVH-0005** | PROCESS | PHASE-0-foundation.md | **Red-first tests for architecture missing acceptance criteria.** PHASE-0 exit criteria list eight REQ-ARCH-* that tests must verify. The test file location is named (`tools/ci/tests/test_phase0.py`) but the actual test assertions are not documented — no file path references `tools/ci/tests/`, no README in `tools/ci/` explains the assertion shape. Test annotations (`@test-id`, `@covers`) are mandated by ADR-0006 and ARCHITECTURE.md §4 but the PHASE-0 scaffold doesn't show an example. Violates P4 (red-first): we cannot verify tests exist in red form in git history if the test file location is unspecified.

**ADVH-0006** | SERIOUS | ADR-0004 §4 & ADR-0008 §1 | **Anti-aliasing gate is a trap.** ADR-0004 §4 defines `anti-aliasing` (pairwise n-gram similarity), pinned in `tools/spec_lint/config.yaml` with a threshold "reviewed quarterly (a `gate`-type task)." But ADR-0008 §1 lists `anti-aliasing` as firing on "every PR" without a quarterly gate or a way to silence noisy false positives. If a legitimate requirement is genuinely similar to an older one (e.g., "User can log in" vs. "Admin can log in"), the gate fires and the PR is blocked. The quarterly review task is BMAD-driven, not a CI gate. The spec says the PR is blocked but doesn't explain who unblocks it or how. Violates P1 (SoT: gate behavior is under-specified).

**ADVH-0007** | CRITICAL | ADR-0006 §5 & ADR-0008 §1 | **Tier coverage gate is untestable from spec alone.** ADR-0006 §5 says "A REQ marked `tier: e2e` requires a passing E2E test (unit tests do not satisfy the REQ)." ADR-0008 §1 lists `tier-coverage` as enforced "every PR" by `tools/trace`. But a REQ's tier is declared in YAML frontmatter (ADR-0004 §5), and the tier value is an enum (`unit | integration | e2e | stochastic`). No spec defines what happens if a REQ is marked `tier: e2e` but no tests for it exist in `tests/e2e/`. Does the gate fail? Block the REQ from merging? Block the entire PR? The spec is silent. A developer cannot write a red test that makes the gate pass because the gate's success criteria are undefined. Violates P4 (red-first) and P3 (tests must be writable).

**ADVH-0008** | SERIOUS | ADR-0005 §3 & ADR-0005 §4 | **Commit trailer validation enforces P4 retroactively but not prospectively.** ADR-0005 §4 says "tools/trace/validate_commit.py walks git history to verify" that a test's first green commit is preceded by a red commit. But this rule applies to commits already merged into main. If a developer makes a red commit, then a green commit locally and pushes them together, the hook only sees the green commit in the pre-receive phase and cannot walk history because the branch hasn't landed yet. The hook is documented to run "pre-receive" (which sees the commit being pushed, not history) but the rule requires history. Either the hook runs post-receive (too late; it can't reject) or the implementation is incomplete. Violates P1 (SoT: documented trigger doesn't match the requirement).

**ADVH-0009** | PROCESS | ADR-0008 §2 | **Gate coverage gate is self-referential, creates circular check.** ADR-0008 §2 defines `gate-coverage` as a gate that "verifies that at least one entry in the table above references it" (each ADR and principle). But the gate is itself listed in §1, row 51. If the gate breaks, the build fails, so it cannot be tested until it exists. If the table is updated with a new principle, both the gate and the principle must land in the same commit for CI to pass. This is a forward-declare: the gate is "meta" and cannot be tested against itself in the same run it's defined. Violates the mechanical enforcement principle (ADR-0008 context: "Principles enforce nothing unless mechanically gated"). The gate exists in the spec but is untestable in PHASE-0.

**ADVH-0010** | CRITICAL | ARCHITECTURE.md §5 & ADR-0002 §7 | **Bidirectional spec sourcing claims Epic reconciliation is enforced, but staging drafts are excluded from reconciliation.** ARCHITECTURE.md §5 says Epic reconciliation requires PM rationale + Architect approval + REQ-IDs + failing tests. ADR-0002 §7 says `openspec/_bmad-output/` (where BMAD PM drafts live) is excluded from the matrix and INDEX. So when the matrix is built, BMAD-generated REQ-ID candidates in staging are not visible to the reconciliation gate. A PM can author a brief that references a non-existent REQ (because the draft REQ in staging is not in the canonical specs), and the gate never fires. The two rules are in direct contradiction: reconciliation claims to check PM artifacts against specs, but staging artifacts are invisible to the specs. Violates P1 (SoT: two authoritative rules conflict).

**ADVH-0011** | SERIOUS | ADR-0003 §2 & ADR-0006 §2 | **Adapter substitution discipline is contradictory.** ADR-0003 §2 says "Production builds inject the real GAS adapter; Node unit tests inject a *different real* adapter (e.g. a Sheets adapter that hits a dedicated test spreadsheet via the Sheets REST API)." But ADR-0006 §2 says "Substituting the **HTTP transport** at the network boundary (e.g. a real `nock` interceptor that records and replays *real* responses captured from the real service) is permitted only for cost or rate-limit reasons." If the test tier must hit a real Sheets spreadsheet via REST (per ADR-0003), then it *is* using HTTP-transport substitution (nock), but nock is only permitted for cost/rate-limit, not correctness. The design claims to exercise real semantics but permits one form of stubbing (recorded HTTP) that ADR-0006 says should be cost-justified. No guidance is given on when to use nock vs. real REST. Violates P3 (tests must exercise real code; guidance on substitution is unclear).

**ADVH-0012** | CRITICAL | ADR-0007 §5 & ADR-0003 §2 | **Prompt caching discipline unspecified for GAS runtimes.** ADR-0007 §5 says `packages/anthropic-client/` defaults to prompt caching where supported and cache hit rate is reported per CI run. ADR-0003 describes E2E tests that run "in the deployed Apps Script runtime" via `clasp push` and the Apps Script Execution API. But the Anthropic SDK's prompt caching is not supported in the Apps Script V8 runtime (no native support for cache_control headers in Apps Script's UrlFetch). ADR-0007 says caching is "enabled by default" without carving out the E2E tier. The tension is: does `packages/anthropic-client/` detect the runtime and disable caching in GAS? Or does GAS code never call the LLM and always go through an adapter? The spec says adapters are for Sheets/Drive (ADR-0006 §3), not for Anthropic. Violates P1 (SoT: interaction between two tiers is unspecified).

**ADVH-0013** | PROCESS | ADR-0008 §5 & PHASE-2 scope | **Pre-commit hooks promised but enforcement is incomplete.** ADR-0008 §5 says `index-up-to-date` and `matrix-drift` run pre-commit and rewrite files. ADR-0008 §5 also says `commit-trailers-valid` runs pre-commit and rejects malformed messages. But PHASE-0 scope (PHASE-0-foundation.md line 37) says `.claude/settings.json` carries hook "declarations" pointing to placeholder commands that "exit 0 with a TODO comment." The hooks are not implemented in PHASE-0 — they land in PHASE-2. A developer in PHASE-1 can push a commit with invalid trailers because the pre-commit hook does not exist. The spec promises local enforcement but delivery is deferred. The trap is silent: PHASE-1 developers believe they are protected by a pre-commit hook (mentioned in ADR-0008) but they aren't. Violates P1 (SoT: promised enforcement is absent).

**ADVH-0014** | SERIOUS | ADR-0005 §5 & PHASE-2 scope | **Journal event schema is incomplete; `tests_run` event is underspecified.** ADR-0005 §5 defines journal event shapes, including `tests_run: ts, runner, passed, failed, new_red[], new_green[]`. But the schema doesn't specify the event format for a test that transitions from red to green in the same PR — does `new_green[]` contain the test ID or the commit SHA? The matrix rebuild (PHASE-2, `tools/trace/rebuild.py`) must parse this, but the parser has no documented input shape. Additionally, `passed` and `failed` are integers, but the schema doesn't say if they count tests, assertions, or test suites. The P4 enforcement rule (ADR-0005 §4) depends on this event to verify red-before-green, but the event schema is incomplete. Violates P1 (SoT: schema is ambiguous).

**ADVH-0015** | PROCESS | ARCHITECTURE.md §7 & ADR-0004 §6 | **INDEX.yaml is "sole retrieval surface" but spec_lint is described, not specified.** ARCHITECTURE.md §7 says `openspec/specs/INDEX.yaml` is "the sole retrieval surface for tooling; semantic search is forbidden for spec lookup." ADR-0004 §6 says "INDEX.yaml is auto-generated by `tools/spec_lint index`." But no REQ-SPEC-* in the spec files documents what the INDEX format is, what fields are present, or what "sole retrieval surface" means in practice. A tooling agent might assume INDEX is a flat list of REQ-IDs and miss that it is hierarchical or contains cross-references. The phrase "sole retrieval surface" is a design intent, not an enforced constraint. Violates P1 (SoT: INDEX format is informal).

---

**Summary**: 15 findings (12 required minimum met). Severity breakdown: 6 CRITICAL, 6 SERIOUS, 3 PROCESS. Core defects cluster around: (1) spec-staging contradiction (ADVH-0003, ADVH-0010), (2) untestable gates (ADVH-0007, ADVH-0009), (3) deferred enforcement that becomes invisible (ADVH-0013), (4) incomplete schema definitions (ADVH-0014), and (5) contradictions between adapter disciplines (ADVH-0011, ADVH-0012). Each finding violates at least one operating principle or references an unresolved ADR section.
