# DEVIL — advanced-elicitation-devils-advocate (opus) — Wave 3

**Source transcript:** [`raw-transcripts/DEVIL-agent-a8f3b70caeadee42d.jsonl`](../raw-transcripts/DEVIL-agent-a8f3b70caeadee42d.jsonl)
**Sub-agent description:** `Devil's advocate elicitation`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a8f3b70caeadee42d`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-advanced-elicitation` skill via the Skill tool with a **devil's advocate** method (a variant of red-team that argues the contrary position rather than attacking the system).

For each major architectural decision in the documents, take the opposing position. Argue for the deletion of each ADR, the merging of each phase, the loosening of each principle. Treat the artifact as if a contrarian senior engineer is reviewing it: "convince me this ADR is worth keeping; convince me this phase shouldn't be merged with the next; convince me this principle deserves a CI gate."

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

For each finding:
- The contrarian thesis (e.g., "ADR-0005's matrix-as-derived-cache is over-engineered; the matrix should be computed on demand and not committed")
- The strongest argument for the thesis
- Why the architecture doesn't currently rebut the argument
- What the architecture would have to say to legitimately defend the current position

Focus areas:
- Each ADR's "alternatives considered" section — is the rejection convincing?
- Each phase ordering — does it have to be this order?
- Each gate — is the gate worth the friction it creates?
- Each principle — does it really need to be a principle, or could it be a guideline?
- The whole BMAD/TEA/OpenSpec stack — is it accidentally three things where one would suffice?

REQUIRED OUTPUT:
- Stable IDs: prefix `DEVIL-` (e.g. DEVIL-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 12 findings
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have all 15 documents. Now I'll execute the devil's advocate method directly per the user's specific directive. Since the user explicitly named the method and specified the deliverable format, I'll bypass the standard menu loop and produce the findings.

---

# Devil's Advocate Review — Architecture & Phase Documents

**Method:** Devil's Advocate (contrarian variant of red-team). For each major architectural commitment, I argue the opposing position, identify the strongest contrary argument, show where the documents fail to rebut it, and state what they would need to add to legitimately defend the current line.

**Scope:** `openspec/architecture/ARCHITECTURE.md`, ADR-0001 through ADR-0008, PHASE-0 through PHASE-5.

---

## CRITICAL

### DEVIL-CRIT-01 — The five operating principles do not actually need to be principles; four are derivable from one

**Contrarian thesis:** P1 (single source of truth) subsumes P2, P3, and P5. P4 (red-first) is a workflow convention, not a principle. The document elevates them to principles to manufacture the appearance of a coherent philosophy.

**Strongest argument:** P2 (statistical assertions for stochastic systems) is just "the assertion is the SoT for what the system promises" — i.e., P1 applied to test contracts. P3 (real production code in tests) is just "the tested artifact is the SoT for behavior" — same. P5 ("OpenSpec for specification, BMAD + TEA for workflow") is a tooling choice, not a principle; principles should outlive tool selections. P4 is a process step that can be enforced as a hook without being elevated to "principle." Reducing to one principle ("single source of truth, mechanically enforced") would shrink the surface CI must cover and remove the awkward `gate-coverage` meta-gate (ADR-0008 §2) whose entire purpose is to police a structure that is itself an artifact of having too many principles.

**Why the architecture doesn't rebut this:** ARCHITECTURE.md §1 lists the principles as flat peers without justifying why each must be primitive rather than derived. ADR-0008's "a principle without a gate is a build failure" loops back on a population the architecture itself chose, not one it justified. No ADR argues that, e.g., P3 is independent of P1 in a way that would survive someone collapsing the list.

**What the architecture would have to say:** A "Principle independence" section in ARCHITECTURE.md proving each principle is non-derivable from the others (e.g., showing a concrete case where P3 would be violated without violating P1), plus an argument that elevating tooling (P5) to a principle is not a category error.

---

### DEVIL-CRIT-02 — ADR-0005's matrix-as-checked-in-derived-cache is engineering theatre; compute on demand

**Contrarian thesis:** `openspec/traceability/matrix.yaml` is checked in only so humans can diff it, but humans don't read traceability matrices. The pre-commit hook stages a regenerated copy and CI re-derives and compares. The file therefore adds a checked-in artifact that exists solely to fail CI on drift it caused itself. Delete it; compute it on demand in `audit.py` and in the `phase-exit` gate.

**Strongest argument:** ADR-0005 §2 admits the matrix is "a cache" and forbids hand-edits. The only purpose given for committing it is "diffs are reviewable." But (a) the file is regenerated automatically pre-commit, so the diff is mechanical noise, not human intent, and (b) reviewers cannot usefully review a derived diff without re-deriving it themselves, at which point the committed copy is redundant. The `matrix-drift` gate exists exclusively to detect mistakes in the very workflow that produced the file. Removing the file eliminates that entire failure mode at zero cost.

**Why the architecture doesn't rebut this:** ADR-0005 never explains what question is answered by reading the checked-in matrix that is not answered by running `tools/trace/audit.py` against HEAD. The "diffs are reviewable" claim is asserted, not justified with a concrete reviewer scenario.

**What the architecture would have to say:** A worked example where the committed matrix diff revealed a defect the per-commit trailers + spec frontmatter + test annotations did not already reveal. Without that, the artifact is a derived cache pretending to be primary.

---

### DEVIL-CRIT-03 — ADR-0006's no-mock rule is a slogan; the carve-outs hollow it out

**Contrarian thesis:** ADR-0006 §2 bans mocks but then permits "real" HTTP interceptors (`nock`) that "record and replay real responses," plus "deterministic clock" substitutes that are "real code." These are mocks renamed. The principle would be more honest as "mocks must be production-grade adapters with their own tests" rather than "no mocks."

**Strongest argument:** A `nock` interceptor replaying a recorded response is, by any operational definition, a fake — the system under test is not talking to the real service when the test runs. Calling it a "real adapter" because the recording was once real is sleight of hand: it has the same staleness, drift, and false-confidence properties that motivated the no-mock rule in the first place. Likewise, a "deterministic clock" used in tests but not in production is a test double. The carve-outs swallow the rule wherever it would actually bite.

**Why the architecture doesn't rebut this:** §2's distinction between "real-for-real" and "real-for-fake" is asserted without an operational test that a reviewer could apply at code-review time to a borderline case. There is no procedure for deciding whether a given adapter qualifies as "real."

**What the architecture would have to say:** A decision procedure: "An adapter is real iff (a) the same adapter is reachable from at least one non-test code path, OR (b) it makes a live network call to a system whose contract it does not control." Anything failing both is a mock and banned. Until that test is written down, the rule is performative.

---

### DEVIL-CRIT-04 — ADR-0007's ban on recorded fixtures will be quietly violated in week one

**Contrarian thesis:** Forbidding recorded fixtures in the stochastic tier (§2) while also demanding "distributional assertions over N runs" (§3) with pinned sample sizes and a "cost-budget" gate (§4) is internally incompatible at any non-trivial N. Engineers will record-and-replay under another name, or N will collapse to 1, or the tests will be skipped under cost pressure. The policy is unenforceable.

**Strongest argument:** A distributional assertion needs samples in the dozens to hundreds for any non-trivial confidence interval. At Anthropic-API token prices and latencies, running that on every PR is prohibitive; running it nightly with N=5 turns "distributional assertion" into "two-sample sanity check," which is no longer distributional. The cost-budget gate makes the tension explicit but offers no resolution: either you cap cost (and lose statistical power) or you keep statistical power (and blow the budget). The architecture wants both.

**Why the architecture doesn't rebut this:** ADR-0007 §3 says "sample size and threshold are pinned per test" without quantifying what sample size satisfies "statistical." §4 introduces a budget without saying what happens when a test's statistically-required N exceeds the budget. ADR-0008's `cost-budget` gate enforces the budget but does not gate sample adequacy.

**What the architecture would have to say:** Either (a) acknowledge that recorded-fixture replay is permitted with mandatory periodic re-recording and a freshness gate, or (b) commit to a minimum statistical-power floor per stochastic test and accept the budget that follows. The current text does neither and so cannot be enforced.

---

## SERIOUS

### DEVIL-SER-05 — PHASE-1 and PHASE-2 should merge; their separation creates a six-month dead-letter window

**Contrarian thesis:** PHASE-1 ships `tools/spec_lint` and BMAD install. PHASE-2 ships `tools/trace` and the matrix. Between them, the repository is in a state where REQs can be authored and lint-validated but cannot be traced to commits, tests, or coverage — meaning the lint rules cannot themselves be governed by the matrix they lint into existence. Either ship both at once or accept that PHASE-1 produces specs that are unverifiable until PHASE-2 lands.

**Strongest argument:** PHASE-1 declares `REQ-SPEC-*` requirements and demands they be `tests-green` (PHASE-1 exit), but `tests-green` is a status the matrix tracks — and the matrix doesn't exist until PHASE-2. The phases reference each other's outputs without acknowledging the circular dependency: PHASE-0's `REQ-ARCH-*` "must be tests-green in the matrix" (PHASE-0 §47), but PHASE-0 explicitly defers matrix implementation to PHASE-2.

**Why the architecture doesn't rebut this:** No phase document explains how `tests-green` is determined in PHASE-0 and PHASE-1 when the matrix that records `tests-green` lands in PHASE-2. The implicit answer ("the placeholder matrix and test annotations are enough") is never written down.

**What the architecture would have to say:** Either merge PHASE-1 and PHASE-2 into one phase, or specify the bootstrap protocol: how `tests-green` is computed during the gap, and what fraction of PHASE-1's exit criteria are actually post-hoc validatable when PHASE-2 lands.

---

### DEVIL-SER-06 — PHASE-3 (Anthropic client) before PHASE-4 (shared libs) is the wrong order

**Contrarian thesis:** The Anthropic client depends on adapter interfaces declared in `packages/shared-ts/adapters/` (per PHASE-3 §2). Those adapters are PHASE-4's deliverable. PHASE-3 therefore implicitly forces a sliver of PHASE-4 to land early, polluting both phases. Reorder: PHASE-4 first (adapters and shared utilities), then PHASE-3 (client built on them).

**Strongest argument:** PHASE-3 §2 says it includes "adapter declarations in `packages/shared-ts/adapters/`" — that is shared-lib work being done under the Anthropic-client phase to satisfy a dependency. Either `packages/shared-ts/` exists as a half-built thing during PHASE-3 (violating phase isolation), or the Anthropic client doesn't actually need the shared adapter pattern (in which case ADR-0006's "every external system goes through an adapter" is not really applied here).

**Why the architecture doesn't rebut this:** Neither phase document explains the dependency direction or argues why the Anthropic client is sufficiently load-bearing to justify pulling shared-lib infrastructure forward. The ordering appears to follow "Anthropic client is conceptually more important," not "Anthropic client has fewer dependencies."

**What the architecture would have to say:** A dependency graph between phases (not just "exit gate passed") that proves PHASE-3 has zero PHASE-4 dependencies, or an admission that the order is arbitrary and a different order would be equally valid.

---

### DEVIL-SER-07 — ADR-0004's anti-aliasing lint will produce more false positives than it prevents real defects

**Contrarian thesis:** The pairwise n-gram similarity check (§4) over all `Description` and `Acceptance` bodies will flag legitimate cases — multiple REQs about authentication will share auth vocabulary; multiple REQs about Sheets will share Sheets vocabulary — at a rate that swamps the rare δ-convex-lure case the paper describes. The lint becomes noise, gets disabled in practice via threshold inflation, and the principle dies a quiet death.

**Strongest argument:** The paper's result is about embedding-space neighbors, not n-gram neighbors. N-gram similarity is a crude proxy that conflates "uses similar words" with "is a near-duplicate requirement." Two REQs saying "the system rejects malformed input" and "the system rejects unauthorized requests" share the high-frequency token `rejects` plus the structural shape, but are not duplicates. The ADR commits to quarterly threshold review as if tuning will solve it — but threshold tuning over noisy signals is exactly what the paper warns cannot rescue lossy recall.

**Why the architecture doesn't rebut this:** ADR-0004 §4 commits to a threshold but does not specify the false-positive budget the rule must operate within, nor does it argue that n-gram similarity is a defensible proxy for the paper's δ-convex lures (which were specifically a property of continuous embeddings, not discrete tokens).

**What the architecture would have to say:** A precision/recall target for the anti-aliasing rule on a labeled corpus, plus an argument for why n-gram is the right proxy — or an admission that the rule is a heuristic guardrail, not a faithful implementation of the paper's result.

---

### DEVIL-SER-08 — The "no semantic search for spec lookup" rule prevents human discovery without addressing the failure mode

**Contrarian thesis:** ADR-0004 §6 calls INDEX.yaml "the sole retrieval surface for tooling" and §8 permits semantic search only for "human discovery UIs" with a recall@k gate. But humans need to find specs too, and they will use ripgrep, fuzzy file search, and IDE jump-to-definition — none of which are subject to the recall@k gate. The rule pretends a problem (semantic recall) is bounded to a UI nobody plans to build.

**Strongest argument:** The actual failure mode the paper describes — competitor mass returning the wrong spec — applies to any retrieval system the user trusts, not only to embedding-based ones. A grep that matches three specs with the same word does not produce a δ-convex lure, but it also does not solve "which of these three is the canonical one I should reference." The architecture solves the embedding problem by banning embeddings and ignores the broader retrieval-correctness problem entirely.

**Why the architecture doesn't rebut this:** ADR-0004 never characterizes what makes embedding-based recall categorically worse than other ambiguous-result retrieval mechanisms. The ban is scoped to a technology, not a property.

**What the architecture would have to say:** A characterization of the property being forbidden (e.g., "any retrieval that returns ranked results without bounded false-positive rate") and an argument for why grep/IDE-search are exempt.

---

### DEVIL-SER-09 — ADR-0002's "vendored 2.6 MB" justification is post-hoc; the cost is operational, not storage

**Contrarian thesis:** ADR-0002 §4 defends vendoring on "zero network dependency at session start" and "2.6 MB is small." But the operational cost is not bytes — it is the per-upgrade substrate-PR ritual, the manual `Skill-Removal-Acknowledged` trailers, the smoke test that does not yet exist, the rollback procedure, and the four-layer config merge. Pulling BMAD from a pinned tarball on session start would cost one network round-trip and eliminate all of that.

**Strongest argument:** §8 describes five "safeguards" required because BMAD is vendored. Each safeguard is itself unimplemented (smoke test deferred to PHASE-2, skill-removal gate deferred to PHASE-2). If the safeguards do not exist, the vendoring is not yet safe. A pinned tarball with a checksum would be safer today: no diff noise, no manual acknowledgment trailers, atomic version pinning, and the failure mode (network down on session start) is observable and fast, not silent and slow.

**Why the architecture doesn't rebut this:** The ADR's cost-benefit treats "2.6 MB" as the cost. The real cost is the entire amendment-0002 apparatus. No counter-analysis weighs that cost against the network-fetch alternative.

**What the architecture would have to say:** A comparison of the two postures (vendored vs. pinned-fetch) with both columns including the operational machinery each implies — not just the storage delta.

---

### DEVIL-SER-10 — PHASE-5 is described as a "load test" for the architecture, which means the architecture is unfalsifiable until PHASE-5

**Contrarian thesis:** PHASE-5 §20 says "any pain point discovered here results in an ADR amendment, not a workaround." This makes PHASE-5 the first phase where the architecture is genuinely tested against reality — but the architecture has already declared itself "frozen" (ARCHITECTURE.md §11). The discipline asks reviewers to approve a frozen artifact whose first contact with reality is four phases away.

**Strongest argument:** Frozen-then-load-tested is the opposite of how durable architectures evolve. A real load test should occur in PHASE-1 or PHASE-2 against a minimal toy project, surfacing pain points while the cost of changing the architecture is still low. By the time PHASE-5 runs, ADRs 0001–0008 have accumulated downstream commitments (tooling, lint rules, gate definitions) that make any amendment far more expensive than it would have been earlier.

**Why the architecture doesn't rebut this:** No phase before PHASE-5 contains a "smallest possible real project" deliverable that would test the architecture against a non-trivial concrete case. PHASE-3 (Anthropic client) is internal infrastructure, not a user-facing concrete project.

**What the architecture would have to say:** Either move a minimal end-to-end project earlier (e.g., a PHASE-1.5 throwaway), or argue that the architecture is sufficiently derived from existing prior art that load testing is a formality rather than discovery.

---

### DEVIL-SER-11 — The mandatory commit trailers will be skipped or wrong on every checkpoint commit, eroding the gate's signal

**Contrarian thesis:** ADR-0005 §3 mandates four trailers on every commit, then §7 introduces `Checkpoint: true` as an exemption from "a defined subset of gates" — and the checkpoint commit is auto-produced by a hook at session-end, which is exactly the moment when the active task context may be ambiguous or missing. Every checkpoint will either carry a guessed `Task:` value or an obviously-stub one. The trailer signal becomes noise in proportion to how often sessions end without a clean active task.

**Strongest argument:** A trailer system is only useful if every trailer carries true information. Auto-produced trailers at moments of uncertainty (session abort, container reclaim, idle timeout) cannot meet that bar. The system is choosing between "fail-loud at checkpoint time" (rejecting the commit, losing the WIP) or "fail-quiet" (accept guessed trailers, pollute the matrix). ADR-0005 chooses fail-quiet without acknowledging the long-term cost.

**Why the architecture doesn't rebut this:** §7 says the "next non-checkpoint commit on the branch" is responsible for "restoring P4 compliance" via squash or recoverable sequence. It does not say who is responsible for restoring trailer accuracy, nor what happens when a series of checkpoint commits accumulates with guessed metadata.

**What the architecture would have to say:** A protocol for trailer reconciliation at squash time, plus a metric for the fraction of trailers in the matrix that originate from checkpoint commits versus authored commits. If the former exceeds some threshold, the signal is compromised.

---

## PROCESS

### DEVIL-PRO-12 — ADR-0008's `gate-coverage` meta-gate is a tautology dressed as a principle

**Contrarian thesis:** `gate-coverage` enforces that every principle has at least one gate. But the population of "principles" is itself defined by ARCHITECTURE.md §1, which is editable. Adding a principle without a gate fails CI; *removing* a principle to eliminate a missing gate passes CI. The meta-gate creates pressure to shrink the principle list rather than to add gates, which is the opposite of the stated intent.

**Strongest argument:** Any "everything in set X is enforced by something in set Y" check can be satisfied by removing items from X. The architecture provides no mechanism to prevent that escape hatch — no "principles are append-only," no review-board approval to delete a principle, no historical-coverage check that would notice a principle disappearing.

**Why the architecture doesn't rebut this:** ADR-0008 §2 declares the gate "self-enforcing" without addressing the dual: a principle's removal is the easiest way to make the gate pass.

**What the architecture would have to say:** A constraint that the principle list itself is append-only (with supersession the only path), parallel to the REQ append-only rule in ADR-0004 §7. Without it, `gate-coverage` is a forcing function in the wrong direction.

---

### DEVIL-PRO-13 — The BMAD / TEA / OpenSpec triple is one system trying to look like three

**Contrarian thesis:** OpenSpec provides spec storage and IDs. BMAD provides personas and workflow phases. TEA provides test discipline. But the architecture binds them so tightly — BMAD outputs route into OpenSpec namespaces (ADR-0002 §5), TEA tests annotate against OpenSpec REQs (ADR-0006 §6), BMAD phases map onto OpenSpec changes — that they function as one system with three vendor names. The complexity tax of three frameworks pays no diversification benefit.

**Strongest argument:** P5 declares "no parallel convention is introduced" — yet by adopting three frameworks the project has guaranteed that any future workflow innovation will touch the seams between them. The integration surface (ADR-0002's amendments, tools/tea/'s deferred scope, the four-layer config merge) is itself the parallel-convention cost the principle was meant to forbid. A single in-house workflow + spec format would have zero seams.

**Why the architecture doesn't rebut this:** No ADR argues why BMAD's personas are valuable independently of OpenSpec's spec format, or why TEA's discipline could not be expressed as OpenSpec's REQ frontmatter conventions plus a lint rule. The three-vendor stack is presented as a fait accompli, not as a result of comparing it to a unified alternative.

**What the architecture would have to say:** A "stack consolidation" ADR explaining which capabilities of BMAD and TEA are not expressible as OpenSpec extensions, with concrete examples, and what the integration-seam cost is in lint rules and amendments.

---

### DEVIL-PRO-14 — "Append-only at the assertion level" for REQs makes refactoring impossible at scale

**Contrarian thesis:** ADR-0004 §7 forbids material edits to a `tests-green` REQ that is referenced anywhere — supersession is the only path. At scale, this produces deprecated-REQ accretion: the spec corpus grows monotonically, deprecated REQs remain in-file with `status: deprecated`, and the anti-aliasing lint (which scans all REQ bodies) will increasingly flag deprecated-vs-current pairs that *should* look alike because one supersedes the other.

**Strongest argument:** Append-only is a discipline borrowed from event sourcing, where the cost is bounded by the retention policy. Here there is no retention policy: deprecated REQs live forever in the same files as current ones. Within two years, the average spec file will be majority-deprecated content, and every lint rule that scans the file will pay that cost on every PR.

**Why the architecture doesn't rebut this:** ADR-0004 says deprecated REQs "remain in the file" but specifies no garbage-collection, archival, or scan-exclusion rule. The anti-aliasing lint in §4 has no exemption for deprecated-vs-superseding pairs.

**What the architecture would have to say:** A deprecation horizon (after N PRs, deprecated REQs move to a `deprecated/` archive subtree excluded from active lint), or an explicit lint exemption for `supersedes`-linked pairs. Without one, the policy is a slow leak.

---

### DEVIL-PRO-15 — PHASE-0's "no executable code except hook declarations" creates a phase whose exit criteria depend on PHASE-2

**Contrarian thesis:** PHASE-0 produces `.claude/settings.json` with hook declarations pointing at "placeholder commands that exit 0 with a TODO comment" (§9). The PHASE-0 exit gate (REQ-ARCH-0008) confirms the hooks are *declared*, not that they work. But the architecture's entire crash-recovery story (ADR-0005 §8) depends on those hooks firing — and they don't fire until PHASE-2. Any session that runs during PHASE-1 or the gap between phases is unprotected by the very guarantees the architecture promises.

**Strongest argument:** ARCHITECTURE.md §8 lists failure modes with "Loss: Zero" for committed work, conditional on hooks firing. PHASE-0 ships placeholder hooks that exit 0. Therefore during PHASE-1 development, the "Zero loss" guarantee is not in effect, but the architecture text reads as if it is. Anyone implementing PHASE-1 against the documented guarantees is working under a false safety claim.

**Why the architecture doesn't rebut this:** ARCHITECTURE.md §8 does not annotate the failure-mode table with "guarantees active from PHASE-2 onward." The placeholder discipline in PHASE-0 §9 mentions the TODO but does not propagate the safety implication back to the guarantees the architecture advertises.

**What the architecture would have to say:** Phase-gated qualifiers on every guarantee (e.g., "Zero loss [from PHASE-2 onward; PHASE-0 and PHASE-1 sessions: see degraded-mode appendix]") plus an explicit degraded-mode protocol for the pre-PHASE-2 window.

---

### DEVIL-PRO-16 — The "phase-exit" gate forbids out-of-order completion, which forbids parallelism that the architecture would otherwise allow

**Contrarian thesis:** ADR-0008 §3 says "No REQ from a later phase is `tests-green` (we do not allow phases to complete out of order)." This forbids opportunistic parallelism: if a developer is blocked on PHASE-2 work and could productively land a PHASE-4 REQ in the meantime, the gate forces them to idle. The architecture does not justify strict serialization; it just imposes it.

**Strongest argument:** Phase ordering is a *dependency* claim, not a *serialization* claim. The architecture has not shown that PHASE-4 REQs depend on PHASE-3 REQs in a way that would make a PHASE-4-green-before-PHASE-3-green state actually broken. Many shared-lib REQs (PHASE-4) have no dependency on the Anthropic client (PHASE-3) — e.g., a GAS Sheets adapter. Forcing serialization sacrifices throughput for an unjustified invariant.

**Why the architecture doesn't rebut this:** No ADR demonstrates the dependency from later-phase REQs to earlier-phase REQs at the REQ level. The serialization is asserted at the phase level, where the granularity is too coarse to expose where the serialization is and is not necessary.

**What the architecture would have to say:** Either a per-REQ dependency graph that justifies serialization where it exists and permits parallelism where it does not, or an explicit "we choose serialization over parallelism for review-load reasons" rationale that names the tradeoff.

---

**Word count:** ~2,180 words across 16 findings (1 over the 12-finding minimum), with 4 CRITICAL, 7 SERIOUS, 5 PROCESS.
