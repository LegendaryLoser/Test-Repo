# PREM — advanced-elicitation-pre-mortem (opus) — Wave 1

**Source transcript:** [`raw-transcripts/PREM-agent-a1c78e2a771a55c60.jsonl`](../raw-transcripts/PREM-agent-a1c78e2a771a55c60.jsonl)
**Sub-agent description:** `Pre-mortem advanced elicitation`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a1c78e2a771a55c60`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-advanced-elicitation` skill via the Skill tool with the **pre-mortem** method specifically.

The artifact under pre-mortem: a 15-document architecture artifact for a multi-Apps-Script-project monorepo with strict spec-discipline, traceability-runtime, and BMAD-driven workflow.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Pre-mortem framing:
> Imagine it is 18 months from now. The architecture described in these documents has shipped through PHASE-5 and the first Apps Script project is in production. The project has FAILED — either it never reached production at all, or it reached production and immediately suffered a catastrophic incident, or it is technically working but unmaintainable to the point where the team has decided to rewrite. Working backward, what specifically caused the failure? Which document, section, principle, or omission was the root cause?

Identify the failure modes the architecture has baked in. Look especially at:
- Operational failure modes (hooks that don't fire when they should, gates that lie about coverage, push invariants that don't enforce, journal corruption that goes unnoticed)
- Adoption failure modes (developer friction that causes bypass, ambiguity that causes drift, missing artifact types that cause local invention)
- Cost failure modes (stochastic tests that drain API quota silently, BMAD upgrades that break in unrecoverable ways)
- Governance failure modes (P1 violations the gate-coverage gate cannot detect, principles that sound enforced but aren't)
- Identity / trust failure modes (LLM agents acting on contested instructions, agents trusting unverified outputs from other agents)

REQUIRED OUTPUT:
- Stable IDs: prefix `PREM-` (e.g. PREM-01; severity inline as CRITICAL/SERIOUS/PROCESS based on probability × impact of the failure mode)
- Each finding: failure scenario narrative (1-2 sentences), root cause traced to specific document/section/omission, why current architecture doesn't prevent it
- Minimum 12 failure modes
- 1500-2500 words
- Speak in completed-failure past tense as the pre-mortem method demands
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I now have the full 15-document architecture artifact. Proceeding directly with the pre-mortem method as instructed by the user (skipping the menu since the method is pre-specified).

---

# Pre-Mortem — Architecture Artifact (15 documents)

The year is November 2027. PHASE-5 shipped 11 months ago. The first Apps Script project (`projects/first-app`) reached `dev` deployment, struggled into `prod`, and the team has since voted to abandon the framework and rewrite on a vanilla `clasp` + GitHub Actions stack. The post-incident review identified the following baked-in failure modes. They are listed in roughly the order in which they detonated.

---

**PREM-01 — CRITICAL — The `gate-coverage` gate was syntactic, not semantic.**
By month four, three principle violations had shipped to `main` because `gate-coverage` (ADR-0008 §2) only verified that *some* entry in the gate inventory table referenced each ADR/principle by string, not that the named gate actually enforced the asserted behavior. A junior contributor edited `prose-xref-banned` to whitelist comments, the gate kept its name, the inventory row was unchanged, `gate-coverage` stayed green, and prose cross-references began accumulating. Root cause: ADR-0008 §2 specifies a textual cross-reference check ("at least one entry... references it") with no contract for what the gate must assert. The architecture promised "a principle without a gate is a gate-coverage failure" (ARCHITECTURE.md §1) but delivered "a principle without a *named row* is a gate-coverage failure." The semantic gap was the entire failure.

**PREM-02 — CRITICAL — The push invariant was unenforceable in the only failure mode it claimed to cover.**
ADR-0005 §6 amendment 0001 introduced per-commit and per-merge push hooks to close the "committed but unpushed at container reclaim" window. In practice, the amendment's own §8 notes the residual risk: "abrupt container reclaim mid-`PostToolUse`." Over 18 months, four sessions hit exactly that window; two lost a half-day of TASK work each and one lost a P4-critical red-test commit that, when reconstructed, no longer mapped to the same SHA, breaking the `red-before-green` audit retroactively. Root cause: the architecture treated `PostToolUse` as atomic with the tool call. It is not. The fix would have required a transactional log shipped *before* the tool call returned, which neither hook can provide. The amendment created the appearance of safety while leaving the original failure mode resident.

**PREM-03 — CRITICAL — Red-first (P4) was enforceable only on linear history.**
ADR-0005 §4 and ADR-0006 §4 enforced red-before-green by walking git history. By month seven, every feature branch went through `git rebase -i` to clean up checkpoint commits, and the resulting linearization frequently *squashed away* the red commit. `tools/trace/validate_commit.py` had no canonical view of "the red commit existed" once the SHA was gone. The team responded by adding a `Bootstrap: rebase` trailer to bypass — which became universal within two months. P4 was effectively dead by month nine. Root cause: the architecture conflated *git history* with *the historical record of test states*. The journal (ADR-0005 §5) could have been the truth source, but `validate_commit.py` was specified to walk git, not the journal. The two diverged silently.

**PREM-04 — CRITICAL — Stochastic tests bankrupted the Anthropic budget in the third nightly run.**
ADR-0007 §4 required `@cost-budget tokens=<N>` annotations and a per-PR/per-nightly aggregate gate. Engineers wrote distributional assertions over N runs (ADR-0007 §3) with N=200 because smaller N produced statistically meaningless intervals. The `cost-budget` gate aggregated *declared* budgets, not *measured* spend, so a test annotated with `@cost-budget tokens=50000` that actually consumed 480000 tokens (because the sandwich layer retried internally on schema-fails) passed the gate. The nightly cost crossed $1,800/day by month six. Root cause: ADR-0007 §4 specifies the annotation but not the reconciliation with measured cost telemetry exported by `packages/anthropic-client/`. The two signals existed; nothing made them confront each other.

**PREM-05 — SERIOUS — The "no mock of in-repo modules" rule banned the only tractable test for stateful adapters.**
ADR-0006 §3 demanded "real-for-real" substitution at the GAS boundary, with a test adapter that hits a "dedicated test spreadsheet." By month five, two parallel CI runs collided on the test spreadsheet's row counters and the project's integration tier flaked at ~12%. The team's first instinct — partition by run-id into separate sheets — required a sheet-per-run, exhausting the service account's Drive quota in week two. The architecture forbade an in-memory adapter because that would constitute a "fake of an in-repo interface" (ADR-0006 §2). Root cause: ADR-0006 conflated "mock of an in-repo *module*" (correctly forbidden) with "in-memory implementation of an in-repo *interface*" (legitimate). The wording in §2 banned both, and §3's adapter pattern offered no escape for stateful resources with quotas.

**PREM-06 — SERIOUS — Anti-aliasing lint produced unfixable false positives at scale.**
ADR-0004 §4 specified pairwise n-gram similarity above a threshold as a lintable defect. After ~600 REQs accumulated across `shared-ts`, `shared-py`, `anthropic-client`, and `first-app`, the lint surfaced 80–120 alerts per PR, dominated by genuinely-different REQs sharing boilerplate ("Given the adapter is configured, when..."). The "reviewed quarterly" threshold (ADR-0004 §4) was raised twice, then the rule was disabled in `tools/spec_lint/config.yaml` with a `# TODO: rethink` comment that survived to project death. Root cause: the rule applied raw n-gram similarity to `Description` and `Acceptance` bodies, which inevitably share BDD structure. The paper's δ-convex lures argument calls for similarity over *semantic content*, but the rule was implemented over *surface text*. The ADR did not specify which.

**PREM-07 — SERIOUS — Spec immutability calcified the corpus.**
ADR-0004 §1 made IDs immutable and §7 made `tests-green` REQs append-only. By month ten, the first refactor of `packages/shared-ts/gas/Sheets` deprecated 47 REQs and added 51 supersession-REQs in a single CHG. The traceability matrix grew to 22MB and `tools/trace/rebuild.py` took 4m17s, breaking the pre-commit hook's UX. More damagingly, every spec read now required following 2–4 supersession chains. Developers stopped reading specs, started reading code, and the spec corpus drifted from reality. Root cause: ADR-0004 §1 and §7 enforced append-only without specifying any garbage-collection or compaction path. Supersession was the *only* permitted change (ADR-0004 §1), which made it the *universal* change, which destroyed the corpus's signal-to-noise ratio.

**PREM-08 — SERIOUS — The bidirectional Epic reconciliation gate had no decidable failure path.**
ARCHITECTURE.md §5 required PM-rationale + Architect-approval + Story-decomposition + TEA-tests for `ready-for-dev`. In practice, top-down and bottom-up flows produced REQs with the same intent but different IDs, different domains, and different tiers. The reconciliation gate could verify *presence* of inputs but not *agreement* between flows. Three Epics shipped with redundant REQ pairs (`REQ-AUTH-0007` from PM, `REQ-LOGIN-0003` from TEA) that both passed independently and both ended up green; one of them was wrong, and production silently inherited the wrong contract. Root cause: ARCHITECTURE.md §5 describes the converging diagram but ADR-0008 has no `epic-reconciliation` gate. The "reconciliation gate (enforced in ADR-0008)" claim in §5 is unsupported by ADR-0008's actual inventory.

**PREM-09 — SERIOUS — The `_bmad-output/` staging directory became a shadow spec store.**
ADR-0002 §7 made staging non-authoritative and forbade matrix/INDEX references to it. The `stale-staging` rule was "deferred CHG" — never implemented. By month eight, BMAD drafts in `openspec/_bmad-output/planning/` were being read by humans, copy-pasted (not promoted) into PRD prose, and referenced by GitHub issue links. None of this triggered a lint failure because lint excluded the directory entirely (ADR-0002 §7 hard invariant 3). The single source of truth (P1) was technically preserved while being practically destroyed: the *authoritative* artifacts said one thing, the *referenced* artifacts said another. Root cause: ADR-0002 §7 protected the addressable artifact network from staging contamination but did nothing to prevent staging from becoming a parallel, unaddressable network.

**PREM-10 — SERIOUS — BMAD v6.7 dropped two skills without a deprecation window.**
ADR-0002 §8 required `Skill-Removal-Acknowledged: <skill-id>` trailers on upgrade PRs. v6.7 (December 2026) removed `bmad-foo-skill` and `bmad-bar-skill`. The upgrade PR added both trailers, passed the gate, and merged. Three weeks later, two existing change proposals' task files referenced those skills by name in TASK markdown. There was no gate ensuring the referenced-skill set was a subset of the installed-skill set. Existing CHGs broke silently — `claude` would respond "I don't have that skill" with no traceability event. Root cause: ADR-0002 §8 safeguard 2 protected against *removal without acknowledgment* but not against *acknowledged removal that broke in-flight work*. The smoke test (safeguard 1) exercised "one BMAD skill end-to-end" — exactly one, not a coverage check.

**PREM-11 — SERIOUS — The 4-layer config merge made per-project behavior unauditable.**
ADR-0002 §9 documented BMAD's 4-layer config merge with the user-scoped layer (`config.user.toml`) gitignored. When `projects/first-app` started misrouting BMAD output to the *repo-level* staging directory (causing PREM-09's spread), the diagnosis required inspecting four files across two `.gitignore` boundaries on the affected developer's machine. The architecture had no way to assert "the *effective* config for project X is Y" — only "the *committed* config files exist." The `Workflow constraint: sessions working on a specific project must run with CWD = projects/<name>/` (§9) was documented in prose; no gate enforced it. Root cause: ADR-0002 §9 documents the merge but provides no resolver-output snapshot artifact and no CI assertion on effective config.

**PREM-12 — SERIOUS — Checkpoint commits poisoned P4 audits.**
ADR-0005 §7 made checkpoint commits exempt from a defined gate subset and put responsibility on "the next non-checkpoint commit" to restore P4 compliance. In practice, branches accumulated 8–15 checkpoint commits before squash. The "next non-checkpoint commit" was often a squash that elided the red commit's existence (see PREM-03). The `checkpoint_exemptions.yaml` (ADR-0008 §6) listed which gates skipped checkpoints, but no gate verified that the post-squash history actually contained the required red-before-green sequence. Root cause: ADR-0005 §7 transferred a compliance obligation to a commit that the squash workflow then deleted. The obligation was never realized.

**PREM-13 — SERIOUS — Session resume reconstructed reasoning context that the journal could not capture.**
ARCHITECTURE.md §8 claimed "Session resume requires zero human re-briefing" and ADR-0005 §5 enumerated journal event types. None of the event types captured *why* a path was chosen — only *that* files were touched, tests ran, commits landed. After three container reclaims on a single non-trivial TASK in month nine, the resumed sessions repeatedly relitigated the same architectural choice in opposite directions, producing oscillating commits and finally a contradiction in `REQ-LIBTS-0042`. The journal recorded the oscillation; it did not prevent it. Root cause: ADR-0005 §5's event taxonomy is purely operational. The "reconstruct reasoning context" claim in ARCHITECTURE.md §8 is unsupported by the event schema.

**PREM-14 — CRITICAL — The Anthropic-client single-access-point gate had no boundary for transitive imports.**
ADR-0007 §6 banned direct Anthropic SDK imports outside `packages/anthropic-client/`. By month nine, three transitive dependencies (an MCP server, a BMAD skill helper, a vendored eval harness) pulled in the SDK indirectly. `direct-anthropic-import-banned` (ADR-0007 §6, ADR-0008) was implemented as a static-import grep. Transitive imports passed, cost telemetry leaked, and prompt caching was bypassed because the transitive paths constructed their own client. The `cache-hit-regression` gate (ADR-0007 §5) detected the resulting drop, was deemed flaky, and was muted. Root cause: ADR-0007 §6 specifies the prohibition at the import site but not at the dependency-graph closure. The lint rule realized the weaker contract.

**PREM-15 — SERIOUS — The "no mock" rule pushed LLM tests into the only banned escape hatch.**
ADR-0006 §2 banned recorded fixtures *except* for HTTP transport substitution "never for the LLM tier." ADR-0007 §2 banned recorded fixtures for the stochastic tier. Together they forced every LLM-touching test to hit the real API. The test author's only remaining lever was reducing N (sample size in distributional assertions). Tests with N=5 passed CI but had so wide a confidence interval that the assertion was effectively vacuous. The lint rule `stochastic-tier-bans` (ADR-0007 §2 compliance) had no minimum-N check. Root cause: ADR-0007 §3 says "sample size and threshold are pinned per test" but does not constrain pinning to statistically meaningful values. Statistical-assertion theater shipped under a CI-green banner.

**PREM-16 — SERIOUS — The phase-exit gate prevented forward progress under partial failure.**
ADR-0008 §3 required "no REQ from a later phase is `tests-green`." When a security vulnerability in `packages/anthropic-client/` (PHASE-3) needed a hotfix while PHASE-5 was 40% complete, the fix-test commit would have created a PHASE-3 green-after-PHASE-5-tests-were-also-green situation, which `phase-exit` correctly blocked — and incorrectly refused to allow even with the documented `Material-Architecture-Change: true` trailer (ARCHITECTURE.md §0 prelude), because no logic mapped that trailer to phase-exit exemptions. The team merged via `--no-verify` (forbidden by CLAUDE.md and ADR-0008 §6), normalizing bypass. Root cause: ADR-0008 §3 specified a monotonic phase ordering with no in-band exception for cross-phase fixes. The forbidden-bypass rule became the only available tool.

**PREM-17 — SERIOUS — LLM agents acted on contested instructions from other agents without verification.**
The architecture is silent on inter-agent trust. BMAD personas, surfaced as Claude Code skills (ADR-0002), produced outputs (drafts in `_bmad-output/`, TASK proposals, REQ sketches) that subsequent agent invocations consumed as ground truth. When a TEA agent in month seven derived an "acceptance criterion" from a PM agent's brief that the PM agent had hedged with "TBD — confirm with stakeholder," the TEA agent dropped the hedge, wrote the test, made it green, and the REQ shipped. Neither ADR-0002 nor any other document defined a contract for inter-agent provenance, hedge-preservation, or "this output is unconfirmed" markers. Root cause: omission across the artifact set. The architecture treated agents as workflow steps, not as actors whose outputs require provenance metadata.

**PREM-18 — PROCESS — Journal corruption went unnoticed for six weeks.**
ADR-0005 §5 specified "partial writes from a crash are discarded by the parser (the line is malformed and ignored)." In month eleven, a misconfigured filesystem flushed two journals' final 800 bytes mid-line. The parser discarded the torn lines. Nobody noticed the silent data loss because no gate compared *expected* event counts (from git + tests-run logs) against *observed* event counts. `rebuild.py` happily produced a matrix from incomplete journals, and `matrix-drift` stayed green because both committed and rebuilt versions used the same corrupted source. Root cause: ADR-0005 §2 made the matrix a "derived cache" but the architecture trusted that the four sources were each self-consistent. No cross-source reconciliation gate existed; the audit interface (ADR-0005 §9) was query-only, not validating.

---

**Synthesis.** The architecture failed because its enforcement mechanism (CI gates) and its principles (P1–P5) were related by name and table-row, not by mechanical contract. Several gates measured proxies (string presence, declared budget, static imports) of behaviors they claimed to enforce (semantic correctness, actual cost, transitive constraint). Several principles were stated to be CI-enforced but had no implementable contract in the ADRs that defined them. The `gate-coverage` meta-gate (PREM-01) made the substitution invisible. Vendored BMAD (ADR-0002), append-only specs (ADR-0004), and the no-mock rule (ADR-0006) each shifted operational burden onto humans in ways the architecture did not predict. The "zero human re-briefing" promise (ARCHITECTURE.md §8) and the "tests exercise real production code" principle (P3) were the two most-cited reasons for the rewrite vote — both because they were *almost* delivered, in a way that produced confidence without correctness.
