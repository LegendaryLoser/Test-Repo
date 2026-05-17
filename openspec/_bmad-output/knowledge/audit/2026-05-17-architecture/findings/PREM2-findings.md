# PREM2 — advanced-elicitation-pre-mortem (sonnet) — Wave 4

**Source transcript:** [`raw-transcripts/PREM2-agent-a2a0f163139591ae3.jsonl`](../raw-transcripts/PREM2-agent-a2a0f163139591ae3.jsonl)
**Sub-agent description:** `Pre-mortem sonnet`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a2a0f163139591ae3`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke `bmad-advanced-elicitation` with the **pre-mortem** method.

Pre-mortem framing:
> Imagine 18 months from now. The architecture has shipped through PHASE-5. The first Apps Script project is in production. The project has FAILED — never reached production, or reached production and suffered catastrophic incident, or is technically working but unmaintainable to the point of rewrite. Working backward, what caused the failure?

Documents (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md, decisions/ADR-0001 through ADR-0008, phases/PHASE-0 through PHASE-5

Categories: operational failures (hooks, gates, push invariant), adoption failures (developer friction causing bypass), cost failures (stochastic tests draining quota), governance failures (P1 violations gate-coverage can't detect), identity/trust failures (LLM agents acting on contested instructions).

REQUIRED OUTPUT:
- IDs prefix `PREM2-` (CRIT/SER/PROC inline by P(failure) × impact)
- Minimum 12 failure modes
- For each: scenario narrative, root cause in specific document, why current architecture doesn't prevent it
- Past-tense (pre-mortem method)
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have all 15 documents. I'll execute the pre-mortem analysis directly since the task specifies the method and the required output format precisely.

---

**PRE-MORTEM ANALYSIS — Architecture Post-Mortem, 18 Months Forward**

*It is November 2027. The PHASE-5 retrospective concluded three weeks ago. What follows is the reconstruction of how this project failed, drawn from git history, incident reports, and the session journals that survived.*

---

**PREM2-CRIT-001 — The Push Invariant Fired Too Late: Work Was Already Gone**

The push invariant described in ADR-0005 §6 and §7 depended on two hooks firing correctly on every session exit: `PostToolUse(Bash:git commit)` and `Stop`/`SessionEnd`. In practice, the Claude Code container was reclaimed mid-`PostToolUse` on three separate occasions during PHASE-3. Each time, the commit had completed but neither the per-commit push nor the checkpoint push had fired. The result was committed-but-unpushed work sitting in a container that was then garbage-collected.

The root cause was architectural: ADR-0005 §8 acknowledged this residual failure mode explicitly ("residual loss only if both hooks fail to fire") but provided no detection mechanism. There was no out-of-band heartbeat, no dead-man's-switch, and no CI gate that checked whether origin tracked the expected HEAD. The failure was silent. The next session resumed from the last pushed commit, not the last committed one, and the `rebuild.py` journal reconstruction produced a matrix that referenced commits that no longer existed on the remote. The `matrix-drift` gate then blocked all further PRs until the orphaned matrix entries were manually triaged — which required hand-editing the matrix, which was itself a build failure per ADR-0005 §2.

The architecture documented the failure mode, acknowledged it as residual, and provided no recovery path that didn't itself violate another invariant.

---

**PREM2-CRIT-002 — Gate Coverage Passed But a Principle Wasn't Gated**

The `gate-coverage` meta-gate in ADR-0008 §2 walked every ADR and every principle in ARCHITECTURE.md §1 and verified that at least one table entry referenced each. What it did not do — and what the ADR never specified — was verify that the referenced gate was *implemented*, *passing*, and *actually executed on PRs touching relevant code*. During PHASE-2, the `cost-budget` gate was declared in the table and wired to a CI job, but the job script exited 0 unconditionally because the budget aggregation logic was deferred as a TODO. The `gate-coverage` check passed because the table row existed. No one noticed that the gate was a stub for six weeks, during which stochastic tests were merged that collectively exceeded the per-nightly token budget by a factor of eight. The first real-API nightly run after the stub was replaced with a real implementation failed catastrophically, and the team discovered that twelve merged REQs had been validated against a gate that was never actually checking anything.

The root cause is in ADR-0008 §2: the gate coverage check verified presence of a gate reference, not operational validity of the gate. A principle without a *functioning* gate is still a build failure — but the architecture had no mechanism to distinguish a functioning gate from a stub that exits 0.

---

**PREM2-CRIT-003 — Red-First History Was Rewritten; P4 Enforcement Became Unverifiable**

`red-before-green` in ADR-0008 required `tools/trace/validate_commit.py` to walk git history to verify that every green test had a prior red commit. This worked correctly until a developer on PHASE-4 performed an interactive rebase to clean up a branch before merge. The rebase rewrote commit SHAs. The journal, which logged events against specific SHAs per ADR-0005 §5, now contained `commit` events referencing SHAs that no longer existed. `rebuild.py` silently skipped journal entries referencing unknown SHAs. The rebuilt matrix dropped the red-commit entries for fourteen tests, making those tests appear to have been introduced in a green state. `red-before-green` then blocked the PR. The developer's only recourse was the `Bootstrap: <reason>` trailer mechanism in ADR-0006 §4, which required an approving review — but the reviewer, seeing "Bootstrap: rebase cleanup," approved it without understanding that this permanently erased the P4 audit trail for those tests.

The root cause is that ADR-0005 §5 bound journal events to git SHAs without accounting for history rewriting. ADR-0008 provided no gate that detected SHA-journal divergence. The architecture's traceability model assumed append-only git history — a reasonable assumption for `main`, but not enforced for feature branches prior to merge.

---

**PREM2-SER-004 — The BMAD Staging Area Became the Real Source of Truth**

ADR-0002 §7 declared `openspec/_bmad-output/` as staging — non-authoritative, excluded from the matrix and INDEX.yaml, subject to a future `stale-staging` lint rule that was explicitly deferred. The deferral meant that for the entire duration of PHASES 1 through 4, drafts accumulated in staging without promotion pressure. By the time PHASE-5 arrived, there were 47 BMAD-generated draft artifacts in staging, several of which had been cross-referenced from CLAUDE.md and from session journals as if they were canonical artifacts. Developers working on PHASE-5 stories could not determine which version of a brief or PRD section was authoritative — the staging copy had been updated three times, the canonical location had the original, and the spec-lint `prose-xref-banned` rule did not cover references inside `openspec/_bmad-output/` itself (per ADR-0002 §7's explicit exclusion of staging from lint).

The `stale-staging` gate was deferred with the note "flags drafts sitting unpromoted past a configurable threshold." It was never implemented. The architecture anticipated the accumulation problem and chose to defer the solution rather than prevent it. By PHASE-5, the cost of the deferral exceeded any savings it had produced.

---

**PREM2-SER-005 — Stochastic Test Costs Drained API Quota Mid-Sprint**

ADR-0007 §4 required every stochastic test to carry a `@cost-budget tokens=<N>` annotation and specified that CI would aggregate per-PR and per-nightly budgets. The `cost-budget` gate was gated behind PHASE-2. During PHASE-3, which was the phase that established the stochastic tier, developers wrote twelve stochastic tests with token budgets that were individually reasonable but collectively excessive. The per-PR aggregation gate did not exist yet (it landed in PHASE-2's exit, but PHASE-3's stochastic tests were written before the gate was validated against a corpus of that size). On the first full nightly run after PHASE-3 was merged, the aggregated token spend was $340. The API key's monthly budget was $500. The nightly run exhausted the remaining budget in four nights, causing all subsequent CI to fail on authentication errors rather than test failures. Development stopped for six days while billing was renegotiated.

The root cause is a sequencing gap: ADR-0007 §4 defined cost containment rules, but ADR-0008 deferred the `cost-budget` gate to PHASE-2 without establishing a baseline budget estimate for the tests that would be written in PHASE-3. The architecture enforced cost containment only after costs had already been incurred.

---

**PREM2-SER-006 — Per-Project BMAD CWD Convention Was Never Enforced**

ADR-0002 §9 specified that sessions working on a specific project must run with CWD set to `projects/<name>/` for BMAD to pick up per-project overrides. This was documented as a workflow constraint with "Documenting this is a PHASE-5 deliverable." It was a documentation deliverable, not a gate. No CI check, no hook, and no lint rule verified that BMAD sessions actually ran from the correct CWD. During PHASE-5, two of the first three AI agent sessions ran from the repo root, causing all BMAD output to land in `openspec/_bmad-output/` instead of `projects/<name>/openspec/_bmad-output/`. Those drafts were processed through the repo-level promotion workflow, which assigned REQ IDs from the global namespace rather than the project namespace. By the time the error was detected, six requirements had been promoted with IDs that collided with IDs being allocated for a second project being planned in parallel. REQ IDs are immutable per ADR-0004 §1; the collision required deprecating and superseding six requirements before either project had a passing test.

---

**PREM2-SER-007 — The Compound-Requirement Heuristic Produced False Negatives at Scale**

ADR-0004 §3 specified that atomicity was enforced by the `compound-requirement-detector` spec-lint heuristic plus TEA's behavior decomposition. By PHASE-4, `openspec/specs/` contained 214 requirements. The heuristic — described only as a "heuristic" without a specification of its detection algorithm — had a false-negative rate that was not tested against a corpus of known compound requirements. Eighteen compound requirements survived into `tests-green` status before a reviewer noticed that a single REQ was exercising two independent behaviors under one test annotation, meaning a test that failed for one behavior would also suppress the other behavior's coverage. The architecture's atomicity enforcement depended on an unspecified heuristic and a manual TEA review step; neither had a measurable accuracy guarantee. When the heuristics failed silently, the compound requirements were frozen by ADR-0004 §7's append-only rule: a `tests-green` REQ cannot be materially edited. Correcting the error required deprecating and superseding eighteen requirements, with cascading updates to test annotations, matrix entries, and Epic coverage blocks.

---

**PREM2-SER-008 — The Phase-Exit Gate Checked Order But Not Completeness**

ADR-0008 §3 specified that the `phase-exit` gate verified that the current phase's exit REQs were all `tests-green` and that no REQ from a *later* phase was `tests-green`. It did not verify that every REQ *assigned to the current phase* was included in the exit criteria. During PHASE-3, two `REQ-LLM-*` requirements were created in `openspec/specs/anthropic-client/` but their `phase: PHASE-3` frontmatter was incorrectly set to `phase: PHASE-4` due to a copy-paste error. The `phase-exit` gate for PHASE-3 passed because neither of those REQs appeared in PHASE-3's exit criteria. Those requirements were never tested at PHASE-3 scope. When PHASE-4 ran, the requirements were not on the PHASE-4 deliverable list either. They remained in `tests-red` status and were eventually swept into PHASE-5 as technical debt, where they conflicted with PHASE-5's Apps Script scope.

The root cause is that the `phase-exit` gate was defined reactively (check the exit REQ list) rather than proactively (check all REQs attributed to this phase against the exit list). No gate detected the orphan.

---

**PREM2-PROC-009 — ADR-0003 Was Referenced Throughout But Never Existed**

PHASE-1, PHASE-4, and ADR-0008 all referenced `ADR-0003-appscript-runtime.md`. The gate `gas-global-outside-adapter` was described as enforcing ADR-0003. The PHASE-1 scope listed ADR-0003 as one of the documents whose lint rules it would implement. Yet ADR-0003 was not among the eight ADRs present in the repository. REQ-ARCH-0002 required ADR-0001 through ADR-0008 to be present, and REQ-ARCH-0005 required all cross-references in `openspec/architecture/` to resolve to existing files. These requirements were meant to catch exactly this problem. They were authored as red tests in PHASE-0 and were supposed to turn green as PHASE-0 completed.

If those tests were genuinely red-first and turned green, ADR-0003 existed. If the tests turned green via a mechanism other than ADR-0003's presence — or if the tests themselves were incomplete — then the entire Apps Script adapter discipline (the constraint that GAS globals may only appear inside adapter implementations) was enforced by a gate referencing a document that was never written. The lint rule `gas-global-outside-adapter` was implemented without a canonical definition of what constituted a GAS global or what adapter boundaries looked like. By PHASE-4, different developers had different interpretations. The first PHASE-5 project introduced two direct `SpreadsheetApp` calls in a utility module, both of which passed the lint rule because the rule's pattern matching was calibrated against assumptions from a document that didn't exist to define the canonical set.

---

**PREM2-PROC-010 — Checkpoint Commits Accumulated and Suppressed P4 Audit**

ADR-0005 §7 specified that the `Checkpoint: true` trailer caused CI gates to skip the commit, and that the next non-checkpoint commit on the branch was responsible for restoring P4 compliance. The mechanism relied on a clean linear history where a single non-checkpoint commit followed checkpoint commits. In practice, the `Stop`/`SessionEnd` hook fired on every session exit, including very short sessions that only read files. Long-running features accumulated fifteen to twenty checkpoint commits before a substantive commit. The `red-before-green` validator was designed to walk history and find the prior red state — but with many checkpoint commits interspersed, the walk became expensive and the exemption logic for `Checkpoint: true` commits had an off-by-one error: it skipped checkpoint commits *inclusively* in both directions, meaning a red-state commit immediately adjacent to a checkpoint commit was itself treated as exempt. Three tests that were introduced green (P4 violations) were not caught because their prior commits were all `Checkpoint: true` and the validator's window skipped over the violation.

---

**PREM2-PROC-011 — The Anti-Aliasing Threshold Was Never Reviewed**

ADR-0004 §4 specified that the anti-aliasing threshold and n-gram size were pinned in `tools/spec_lint/config.yaml` and "reviewed quarterly (a gate-type task)." The quarterly review was a `gate`-type task — meaning it had to be a TASK under a CHG, with a commit carrying the appropriate trailers. No CHG was ever opened to schedule the quarterly review. The review never happened. By PHASE-4, the corpus had grown to the point where the pinned threshold (calibrated on the PHASE-0 empty corpus) was too aggressive: it flagged thirty-one genuinely distinct requirements as near-duplicates, blocking all PRs until the threshold was raised. Raising the threshold required understanding the original calibration rationale, which existed nowhere except in a BMAD draft in staging that had never been promoted. The team raised the threshold empirically until the false positives disappeared. In doing so, they also silenced three genuine near-duplicates that should have been merged. The paper's failure mode — δ-convex lures causing false recall — was now present in the spec corpus, undetected.

---

**PREM2-PROC-012 — Identity Ambiguity: LLM Agent Acted on Contested CLAUDE.md**

CLAUDE.md at the repo root stated that it was "session guidance" and was "checked into the codebase." It also declared that "identity/trust" concerns applied to LLM agents acting on contested instructions. During PHASE-5, a developer opened a PR that amended CLAUDE.md to add a project-specific instruction that overrode the five operating principles for the project's domain. The PR passed all CI gates — none of the gates in ADR-0008 checked CLAUDE.md content for principle compliance. Claude Code agents running in the PR's branch began executing sessions with the amended CLAUDE.md in scope. Because the agents treated the in-scope CLAUDE.md as authoritative (it was the nearest session-guidance document), they began producing commits that did not carry the mandatory trailers, citing the amended instruction as authorization. Those commits passed the `commit-trailers-valid` pre-receive hook because the hook validated trailer *format*, not whether the agent had authorization to omit trailers. The PR was eventually rejected during human review, but four commits had already been merged to the feature branch with non-compliant trailers, and the traceability matrix had been rebuilt against them.

The root cause: ADR-0008's `gate-coverage` walk verified that each principle had a gate enforcing it against *code*, but no gate enforced that CLAUDE.md itself could not silently override principles. The architecture's trust model assumed CLAUDE.md was an append-only, human-curated document. It provided no mechanism to detect or block contested amendments.

---

**PREM2-PROC-013 — The stale-staging Gate Deferral Became Permanent**

ADR-0002 §7 described the `stale-staging` gate as "a future spec_lint rule (deferred CHG) flags drafts sitting unpromoted past a configurable threshold." It was listed under the compliance section as an aspirational gate. It appeared in no phase file as a deliverable. No CHG was assigned to it. By the time PHASE-5 ended, the gate existed only as a comment in the ADR. The `gate-coverage` check in ADR-0008 §2 walked ADRs to verify that each had a gate referencing it — but the `stale-staging` reference in ADR-0002 §7 was written as a future gate, not a present one. The `gate-coverage` logic, which checked for ADR references in the gate inventory table, did not verify that every ADR *section* that described a constraint had a corresponding gate. `stale-staging` was a constraint with no gate, which per ARCHITECTURE.md §1 should itself be a build failure — but the meta-gate could not detect constraints described in amendment sections of ADRs rather than in their primary decision text.

---

**PREM2-PROC-014 — The Bulk-Green-Start Gate Had No Upper Bound on N**

ADR-0006 §4 specified that the `bulk-green-start` gate flagged "any commit adding > N green tests without the `Bootstrap: <reason>` trailer." The value of N was not defined in the ADR. It was deferred to the implementation in PHASE-2. The PHASE-2 implementer set N to 50, reasoning that no legitimate commit would add 50 tests simultaneously. During PHASE-4's shared library development, a developer added 48 tests across two commits — 24 and 24, both below the threshold — all in green state, with no prior red commits. The gate was not triggered. `red-before-green` validation was supposed to catch this, but the SHA-journal divergence described in PREM2-CRIT-003 had already compromised that gate's reliability. The combination of an arbitrarily set threshold and a previously damaged history-walk allowed 48 P4-violating tests to reach `tests-green` status and anchor the traceability matrix.

---

**Summary of Structural Gaps**

The architecture's failure was not a failure of any single decision. It was the accumulation of seventeen months of compounding edge cases against a system that had correctly identified its own failure modes and then either deferred the mitigations (stale-staging, cost-baseline estimation, CWD enforcement, quarterly threshold review) or implemented mitigations that were necessary but not sufficient (push-invariant hooks that could not fire if the container was reclaimed before they ran, gate-coverage that checked presence but not operation, history-walk validation that assumed append-only commit graphs).

The most structurally dangerous pattern: the architecture used the phrase "deferred CHG" four times across the ADRs. None of those CHGs were assigned to a phase. Nothing in the phase exit gates checked whether deferred CHGs had been scheduled. Deferred work that is not on a phase exit criterion is work that will never be done — and in this architecture, undone deferred work meant unenforced constraints, which meant silent principle violations.

---

**Advanced Elicitation Options**
*No party-mode agents are active in this session.*

Choose a number (1-5), [r] to Reshuffle, [a] List All, or [x] to Proceed:

1. **Self-Consistency Validation** — Generate a second independent pre-mortem pass and compare for consistency; surface any failure modes each pass missed that the other caught
2. **Red Team vs Blue Team** — Adversarially attack the current failure mode list (Blue defends the architecture; Red argues the failures couldn't have been prevented even with better design)
3. **5 Whys Deep Dive** — Take the highest-severity finding (PREM2-CRIT-001 or PREM2-CRIT-003) and drill to true root cause past the proximate architectural gap
4. **Comparative Analysis Matrix** — Score each failure mode against dimensions: P(occurrence), detectability, recoverability, blast radius — to produce a prioritized remediation order
5. **First Principles Analysis** — Strip the architecture back to its five operating principles and ask whether any principle is internally contradictory in a way that makes some failure modes structurally inevitable

r. Reshuffle with 5 new options
a. List all methods with descriptions
x. Proceed / No Further Actions
