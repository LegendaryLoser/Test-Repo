# SOC — advanced-elicitation-socratic (opus) — Wave 2

**Source transcript:** [`raw-transcripts/SOC-agent-a4656be4309772170.jsonl`](../raw-transcripts/SOC-agent-a4656be4309772170.jsonl)
**Sub-agent description:** `Socratic elicitation review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a4656be4309772170`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-advanced-elicitation` skill via the Skill tool, then apply its **socratic method** specifically to the architecture artifact below.

Socratic method: instead of asserting findings, *interrogate the artifact*. For each suspect area, formulate the questions a careful reader would ask. The questions that the documents do not satisfactorily answer ARE the findings.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001-monorepo-layout.md through ADR-0008-ci-gates-and-phase-exits.md
- openspec/architecture/phases/PHASE-0-foundation.md through PHASE-5-first-appscript-project.md

Operating principles to test against:
1. Single source of truth.
2. Stochastic systems get statistical assertions.
3. Tests exercise real production code (no mocks of in-repo modules).
4. Red-first.
5. OpenSpec for spec, BMAD + TEA for workflow.

REQUIRED OUTPUT:
- Stable IDs: prefix `SOC-` (e.g. SOC-CRIT-01, SOC-SER-01, SOC-PROC-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Each finding format: **Question** | **Source of the question (file/section/quote)** | **What the artifact answers** | **What's left unanswered** | **Why the gap matters**
- 1500-2500 words
- No preamble; findings only

Do not read files outside the 15 listed. No CLAUDE.md, no STATUS.md, no tools/.
```

## Findings deliverable (final assistant message)

Now I have all 15 documents read. Let me compose the socratic review.

# Socratic Review of Architecture Artifact

## CRITICAL Findings

---

**SOC-CRIT-01 — Where does the journal live when origin diverges and the push-invariant hook aborts?**

*Source:* `ADR-0005 §6` table row for `PostToolUse(Bash:git commit)`: "push `HEAD` to origin as a fast-forward. Non-FF aborts the hook with a diagnostic (no force-push)." Also `PHASE-2` scope item 1, `journal_commit.py` description: "aborts on non-FF with a diagnostic."

*What the artifact answers:* The hook will not force-push, and a diagnostic is emitted.

*What's left unanswered:* If `PostToolUse(Bash:git commit)` aborts on a non-FF condition, was the commit already created on the local branch? If yes, then the commit exists locally but origin has not been updated — the precise failure mode §8 promises to prevent ("Container reclaim, committed but unpushed"). The hook's failure to push is the very state §6 was added to forbid. The artifact lists the failure mode as "Mitigated by per-commit push hook (§6) and by extended checkpoint hook (§7); residual loss only if both hooks fail to fire," but a *deliberate hook abort* is precisely a hook firing without mitigation.

*Why the gap matters:* The push invariant amendment 0001 was motivated by exactly this loss vector. Saying "the hook aborts on non-FF" without specifying remediation (rebase? fetch + retry? require human action?) means the invariant is conditional rather than total — and the conditional path is never characterized.

---

**SOC-CRIT-02 — How does `red-before-green` reconcile with `Checkpoint: true` squashing?**

*Source:* `ADR-0005 §7`: "The `Checkpoint: true` trailer makes CI gates skip the commit and makes the next non-checkpoint commit on the branch responsible for restoring P4 compliance (either by squash or by ensuring the red/green sequence is recoverable from the full history)." `ADR-0006 §4` and `ADR-0008` `red-before-green` gate.

*What the artifact answers:* The mechanism is "either squash or recoverable from history." The next commit owns the restoration.

*What's left unanswered:* Who decides which strategy? How does the gate distinguish "this is a valid squash that erased a legitimate red-first sequence" from "this is a green test that never had a red predecessor and the author hand-squashed to hide it"? `validate_commit.py` "walks git history" — but if the history was squashed, the red commit is no longer in git history. The squash strategy and the walking strategy contradict each other.

*Why the gap matters:* P4 is one of the five named principles; the principal enforcement mechanism (history walk) cannot survive the principal exemption mechanism (squash). Either P4 has an exploit, or checkpoint commits cannot be squashed — pick one and say so.

---

**SOC-CRIT-03 — What constitutes a "real adapter" vs. "a fake adapter not called a mock"?**

*Source:* `ADR-0006 §3`: "Each interface has at minimum two real implementations: a production one and a test one. The test implementation is real code (e.g. hits a dedicated test spreadsheet) — it is not a mock." `ADR-0003 §2`: "real-for-real, not real-for-fake."

*What the artifact answers:* Two implementations; the test one must "hit a dedicated test spreadsheet" or similar.

*What's left unanswered:* The clock-and-randomness exception in `ADR-0006 §2` allows a "deterministic clock implementation that is itself production code." What if I write a `DeterministicSheetsAdapter` and declare it production code that's also used in tests? The criterion "is itself production code" is a sociological assertion, not a structural one. No lint rule can distinguish "real test implementation" from "fake with delusions of grandeur." The `mock-in-repo-banned` gate detects mock APIs (`jest.mock`, `sinon.stub`) — it cannot detect a hand-rolled class that happens not to use those APIs.

*Why the gap matters:* P3 is one of the five principles. Its enforcement gate detects a pattern (mock library calls), not the prohibition (in-repo simulation). `ADR-0006 §2` explicitly bans "Hand-rolled fakes (`class FakeFoo implements IFoo`)" but the gate doesn't see them. The principle is partly unenforced and the artifact does not say which part.

---

**SOC-CRIT-04 — What happens to existing red commits when `tests/stochastic/` distributional assertions flap?**

*Source:* `ADR-0007 §3`: "Distributional assertions over N runs. Sample size declared; assertion is a confidence interval, Kolmogorov–Smirnov test, or similar." `ADR-0007 §2`: "Retry-until-pass loops" forbidden.

*What the artifact answers:* Distributional, no retries.

*What's left unanswered:* A confidence interval test has a Type I error rate by definition — say α=0.05. With dozens of stochastic tests, ~5% will fail on each run by random chance even when production is correct. The artifact bans retry-until-pass and requires `red-before-green`. So: a passing test fails by chance; how does CI distinguish this from a genuine red? Does it require a green re-run, contradicting the no-retry rule? The artifact does not say.

*Why the gap matters:* Without a defined policy, every stochastic test failure halts the pipeline indefinitely. Either α is set absurdly low (then statistical power suffers), or there is an unspoken retry policy (then P4's red-first ordering is ambiguous in stochastic tests), or the principle quietly excludes stochastic tests from `red-before-green` (then ADR-0008 should say so).

---

**SOC-CRIT-05 — Why is BMAD permitted under `_bmad/` but `bmad/` is referenced as the install location throughout PHASE-1 and ADR-0001?**

*Source:* `PHASE-1 §3` says `bmad/` (no underscore). `ADR-0001 §3` says "`bmad/` is the BMAD installation." `ADR-0002` amendment 0001 says "Install path: `_bmad/` (was `bmad/`)." `ARCHITECTURE.md §3` shows `_bmad/`.

*What the artifact answers:* ADR-0002 was amended to `_bmad/`.

*What's left unanswered:* ADR-0001 §3 still says `bmad/`; PHASE-1 still says `bmad/`. The five principles include "Single source of truth." Two ADRs and one PHASE file disagree on the location of one of the largest directories in the repo. The `bmad-direct-reference` lint rule in `ADR-0002 §Compliance` says "no file under `tools/`, `packages/`, or `projects/` references a path under `_bmad/`" — but PHASE-1 §3 references `bmad/`. Which path does the gate check?

*Why the gap matters:* This is a Principle 1 violation inside the document that declares Principle 1. The lint rule that would catch it (cross-document path consistency) is not in the gate inventory.

---

## SERIOUS Findings

---

**SOC-SER-01 — What does "every cross-reference uses ID *and* the file path" do when the file moves?**

*Source:* `ADR-0004 §2`: "Every cross-reference uses **ID plus file path**, e.g. `REQ-SPEC-0001 @ openspec/specs/_meta/spec-storage.spec.md`." Identifiers are "immutable."

*What the artifact answers:* IDs don't move. References use ID+path.

*What's left unanswered:* What if `openspec/specs/_meta/spec-storage.spec.md` is renamed because the `_meta` directory is reorganized? Every `@ <path>` reference across the repo breaks. The artifact says renames are forbidden for *IDs*, not for *file paths*. The `xref-resolves` gate would fail until every reference is updated. There is no documented refactor protocol for a path rename.

*Why the gap matters:* Path immutability is implied but not declared. Either file renames are also forbidden (and that should be an ADR), or they require a CHG that updates every consumer (and that should be a documented task type).

---

**SOC-SER-02 — Who allocates `TASK-NNNN` IDs and against what counter?**

*Source:* `ARCHITECTURE.md §4` table lists `TASK-<NNNN>` with home `openspec/changes/<CHG>/tasks/<TASK-NNNN>.md`. Identifier rules (§4 and ADR-0004 §1) say "IDs are allocated by monotonic next-free scan against `openspec/specs/INDEX.yaml`."

*What the artifact answers:* IDs scan against `INDEX.yaml`.

*What's left unanswered:* `INDEX.yaml` (per ADR-0004 §6) is for *spec* requirements. TASK-NNNN is not a REQ; it lives under `changes/`. No index is named for task allocation. If two concurrent PRs both create TASK-0042, the conflict resolves only at merge time, with no lint until then. The artifact also lists Epic, Story, Change, ADR, Phase IDs — none have a stated allocator.

*Why the gap matters:* "Monotonic" plus "concurrent PRs" plus "no single allocator" is a known recipe for collision. The artifact promises monotonicity without naming the mechanism.

---

**SOC-SER-03 — How is `gate-coverage` itself covered?**

*Source:* `ADR-0008 §2`: "`gate-coverage` walks every ADR and every principle in [ARCHITECTURE.md §1] and verifies that at least one entry in the table above references it. A missing reference fails the build."

*What the artifact answers:* `gate-coverage` is a meta-gate. ADR-0008 §Compliance says it is "self-enforcing."

*What's left unanswered:* `gate-coverage` is itself a gate. By its own rule, *it* must reference an ADR or principle. The artifact gestures at "self-enforcing" but does not name the ADR `gate-coverage` enforces. It enforces *ADR-0008*. But ADR-0008 enforces "Principles enforce nothing unless mechanically gated" — a meta-principle that is not in the §1 list. So either §1 is incomplete or `gate-coverage` has no covered principle.

*Why the gap matters:* The whole edifice rests on `gate-coverage`. A circular justification (gate-coverage enforces the rule that gates must enforce things) is not falsifiable. The artifact needs to either (a) admit one bootstrap rule sits outside the meta-rule, or (b) elevate the meta-principle into §1.

---

**SOC-SER-04 — What sample size and which test for "distributional assertions"?**

*Source:* `ADR-0007 §3`: "Sample size declared; assertion is a confidence interval, Kolmogorov–Smirnov test, or similar. Sample size and threshold are pinned per test."

*What the artifact answers:* Per-test pinning.

*What's left unanswered:* There is no rule defining how the pinned values are reviewed. ADR-0004 §4 requires anti-aliasing thresholds to be "reviewed quarterly (a `gate`-type task)." Stochastic thresholds get no such cadence. Sample sizes drift; tests with low power pass when production is broken. The artifact provides the form (KS, CI) but no power discipline.

*Why the gap matters:* Principle 2 is "stochastic systems get statistical assertions." A statistical assertion with un-reviewed sample size becomes ceremonial: "we ran 3 samples and the CI was wide; test passed." The principle is met in form, defeated in substance.

---

**SOC-SER-05 — What is the "PHASE-0 placeholder hook" implementation contract?**

*Source:* `PHASE-0 §Scope` item 9: "`.claude/settings.json` with hook **declarations** pointing at placeholder commands that exit 0 with a TODO comment." `ADR-0005 §6`: "Hook implementations land in PHASE-2."

*What the artifact answers:* The hooks exit 0 with TODO.

*What's left unanswered:* From PHASE-0 to the day PHASE-2 ships, every commit operation runs hooks that exit 0 — meaning `commit-trailers-valid`, `red-before-green`, and `matrix-drift` enforcement do not exist locally. Anything committed during PHASE-0 and PHASE-1 enters history *without* enforcement of the very rules ADR-0005 declares mandatory. The artifact does not say how PHASE-1 commits will be retroactively validated, nor whether PHASE-1 history is exempted.

*Why the gap matters:* The architecture artifact is itself being written under no enforcement. ADR-0005's premise is "the matrix is a cache over append-only sources of truth" — but the sources accumulated under the no-enforcement window may not satisfy the invariants the cache assumes.

---

**SOC-SER-06 — How does `bulk-green-start` count "N green tests" without first knowing the test inventory?**

*Source:* `ADR-0006 §4`: "Bulk green-starts (e.g. importing a battery of passing tests in one commit) require a `Bootstrap: <reason>` trailer and an approving review; CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer."

*What the artifact answers:* A trailer-plus-review bypass for bulk green imports.

*What's left unanswered:* `bulk-green-start` is not in the gate inventory in `ADR-0008 §1`. So the `gate-coverage` check ("every ADR has ≥ 1 gate") does not require it. The gate appears in ADR-0006 §4 with no row in ADR-0008. The threshold "N" is not pinned anywhere. The artifact mentions a gate that may not be enforced.

*Why the gap matters:* The principle "every principle has a gate" relies on every gate appearing in the inventory. A gate named in an ADR but absent from the inventory means the inventory is not the SoT it claims to be.

---

**SOC-SER-07 — How does the artifact reconcile "checked in for diff review" with "no human or agent may hand-edit"?**

*Source:* `ADR-0005 §2`: "The file is checked in so that diffs are reviewable, but: No human or agent may hand-edit it."

*What the artifact answers:* `matrix-drift` gate enforces against rebuild.

*What's left unanswered:* If the only purpose of checking it in is diff review, but every change must equal `rebuild()`, then the diff is fully recoverable by running `rebuild()` against `HEAD~1`. Checking in derived output to enforce a no-edit rule is a workaround for the absence of a derived-cache CI artifact. There is no discussion of the alternative (compute on read, never check in) or its cost.

*Why the gap matters:* SoT (Principle 1) says "one canonical home per fact." The matrix is, by construction, not a canonical home — it is a cache. Committing a cache makes it indistinguishable in git from a SoT. A future reader who finds a diff is asked to "review" content they cannot actually approve or reject — the cache is regenerated regardless.

---

**SOC-SER-08 — Where is the contract for "real Anthropic API" cost when CI sample size grows?**

*Source:* `ADR-0007 §4`: "Stochastic tests carry a `@cost-budget tokens=<N>` annotation. CI aggregates per-PR and per-nightly budgets; exceeding the budget fails the build."

*What the artifact answers:* Per-test budget; aggregate gate.

*What's left unanswered:* If a CI run hits the budget cap, what happens? The build fails — meaning a PR is blocked not by a correctness issue but by aggregate token cost. The artifact does not describe (a) what authors do when budgets are exceeded, (b) how budgets are raised (an ADR? a config change?), (c) whether tests are skipped or the build is hard-failed. The interaction with `red-before-green` (which requires a red commit) is also unspecified — a stochastic red costs tokens too.

*Why the gap matters:* The cost-budget gate is one of two PR-level economic gates. Its operational semantics determines whether the project has bounded or unbounded test cost. The artifact pins the form, omits the policy.

---

**SOC-SER-09 — What is the relationship between Epic `coverage:` block and `req-coverage-100`?**

*Source:* `ARCHITECTURE.md §5`: "An Epic carries a `coverage:` block listing REQ-IDs that satisfy it." `ADR-0006 §5`: "REQ coverage = 100%. Every non-deprecated REQ has ≥ 1 passing test."

*What the artifact answers:* Two separate coverage notions.

*What's left unanswered:* A REQ may pass `req-coverage-100` (has a test) without belonging to any Epic's `coverage:` block. Is a REQ-without-Epic legal? The "bidirectional reconciliation" requires Epic→REQ — implying REQ→Epic is also required. If so, there should be an `epic-coverage` gate ensuring no orphan REQs. There is none.

*Why the gap matters:* The reconciliation gate is described in §5 but not enumerated in ADR-0008. A REQ floating outside the Epic system passes coverage gates while violating the spec-sourcing model.

---

**SOC-SER-10 — How does "no migration required" get verified for BMAD upgrades?**

*Source:* `ADR-0002 §8.5`: "Compatibility statement. Each upgrade PR's description declares the prior version, the new version, and whether spec-format migrations were required... 'no migration required' or names the migration."

*What the artifact answers:* The PR description declares it.

*What's left unanswered:* There is no gate that *verifies* the declaration. A reviewer reads "no migration required" — if it turns out a migration *was* required, the only signal is downstream test failure. The smoke test (§8.1) exercises "at least one BMAD skill," but the artifact does not say which skill or whether it covers spec-format changes. The four safeguards are listed; none verifies the compatibility statement itself.

*Why the gap matters:* The compatibility statement is the kind of contract that rots silently. A required-but-unverified declaration is documentation, not enforcement.

---

## PROCESS Findings

---

**SOC-PROC-01 — Why does ADR-0002 number its amendment sections §7, §8, §9 instead of being inserted next to relevant existing sections?**

*Source:* `ADR-0002` jumps from §6 to §7-§9 (all introduced by Amendment 0002), then "Consequences" and "Compliance" (the original sections). The original numbered sections 1–6 are inside the "Decision" block.

*What the artifact answers:* Append-only amendment style.

*What's left unanswered:* ADR-0004 (and others) renumber sections internally. ADR-0002 mixes flat numbering and decision-numbering. There is no documented ADR template forbidding this drift. Readers parsing ADR-0002 §7 find "Staging discipline" — which is unrelated to the original §6 numbering scheme. Cross-references like "ADR-0002 §7" depend on this non-canonical numbering surviving the next amendment.

*Why the gap matters:* Principle 1 (SoT) implies a consistent artifact format. The amendment style isn't lintable; future amendments will accumulate the same drift.

---

**SOC-PROC-02 — Why does PHASE-5 have two scope items numbered "4"?**

*Source:* `PHASE-5 §Scope` contains "4. Per-project BMAD output isolation..." and then "4. Test suite across all four tiers..."

*What the artifact answers:* (Nothing; it appears to be a numbering error.)

*What's left unanswered:* If a downstream task references "PHASE-5 §Scope item 4," which item does it mean? `xref-resolves` would not catch this because the reference resolves to a section that exists — twice. Prose references are banned (ADR-0004 §2), but list-item references inside a phase file have no discipline.

*Why the gap matters:* A duplicated identifier inside the document that defines identifier immutability is symbolic, but also operational: the duplication breaks downstream addressability.

---

**SOC-PROC-03 — Why is PHASE-0 still `in-progress` while the document declares itself the "frozen architecture artifact"?**

*Source:* `PHASE-0` frontmatter: `status: in-progress`. `ARCHITECTURE.md §opening`: "This document and the ADRs / phase files it references constitute the **frozen architecture artifact**."

*What the artifact answers:* Status is in-progress; artifact is frozen.

*What's left unanswered:* "Frozen" and "in-progress" are inconsistent. If the artifact is frozen and PHASE-0 implements it, then the implementation is in-progress while the design is frozen — fine. But the architecture document also defines REQ-ARCH-0001..8, whose tests are written *during* PHASE-0. So the design is being written and tested simultaneously, which is exactly what P4 (red-first) is meant to prevent at the test level.

*Why the gap matters:* The architecture document is the only artifact in the repo that bypasses its own red-first principle, and the artifact does not acknowledge the exemption.

---

**SOC-PROC-04 — Where is the spec for `_TEMPLATE` files?**

*Source:* `PHASE-0 §Scope` item 4 lists `_TEMPLATE.md` for briefs, prd, epics, stories. `ADR-0004` defines spec format for REQs, not templates.

*What the artifact answers:* Empty templates exist.

*What's left unanswered:* No ADR defines the content of `_TEMPLATE.md`. When a brief is created, what required sections must it carry? Is `_TEMPLATE.md` itself addressable by ID? Does `prose-xref-banned` apply to it? If a template has placeholder text, does anti-aliasing flag templates against each other?

*Why the gap matters:* Templates are the seed material for every product artifact. Undefined template structure means each product PR will invent its own structure — degrading SoT before product content even arrives.
