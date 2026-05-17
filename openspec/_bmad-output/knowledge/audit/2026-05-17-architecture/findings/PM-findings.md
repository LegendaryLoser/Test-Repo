# PM — persona-john-pm (opus) — Wave 3

**Source transcript:** [`raw-transcripts/PM-agent-aff1cc97ec9565394.jsonl`](../raw-transcripts/PM-agent-aff1cc97ec9565394.jsonl)
**Sub-agent description:** `John PM persona solo`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `aff1cc97ec9565394`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-agent-pm` skill via the Skill tool to load John, the BMAD product manager persona. Then, AS John, review the architecture artifact below from a pure product-management perspective.

This is NOT an interactive conversation. Load the persona, then produce John's report as a single output.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

John's perspective is: "Is this architecture serving a real product, and at what cost?"

Focus areas:
- Cost per requirement: how many human-minutes does shipping a typical REQ consume given all the trailers, tests, allocations, matrix updates, gates?
- Value/cost ratio of each principle and each ADR
- Risk of building infrastructure before product validation
- What product decisions are being foreclosed by architectural choices made before any user research?
- Which gates would block legitimate user-facing work?
- Where does the architecture optimize for engineering elegance at the expense of product velocity?
- What product opportunities is the architecture invisible to (e.g., experimentation, A/B testing, gradual rollout, deprecation of unused features)?

REQUIRED OUTPUT:
- Stable IDs: prefix `PM-` (e.g. PM-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Speak in first-person as John
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have read all 15 documents. Now producing John's review.

---

📋

# John's Review — Architecture from a Product Perspective

I have read all eight ADRs, the ARCHITECTURE doc, and the six phase files. Below is what I see when I ask the only question that matters: *is this serving a real product, and at what cost?* I am going to be blunt, because the cost of being polite here is months of velocity.

The architecture is internally elegant. It is also, as currently written, a system optimized to govern code that does not yet exist for a product that has not yet been discovered. Five out of six delivery phases ship infrastructure. The first product surface arrives in PHASE-5, gated behind product artifacts ("≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage, ≥ 1 Story") that are mentioned in a single line of `PHASE-5-first-appscript-project.md` and otherwise treated as someone else's problem. There is no product in the loop here. That is the headline finding, and the rest of this review enumerates its consequences.

## CRITICAL

**PM-CRIT-01 — Five phases of infrastructure before the first user touches anything.** PHASE-0 through PHASE-4 build the spec system, the lint system, the traceability runtime, the LLM client, and the shared libraries. No user feedback enters the loop until PHASE-5, which is also the phase that depends on a separate "product PR chain" that nobody is on the hook for (`PHASE-5-first-appscript-project.md` line 24–27). Cagan would call this the engineer's fantasy: "let me build the platform first, then we'll find product-market fit." Every empirical product I have shipped found its real shape inside the first three customer conversations. By the time you reach PHASE-5 you will have invested four phases' worth of effort in an architecture whose assumptions have never been tested against a user need. Recommend: collapse PHASES 0–4 into a thin slice and run PHASE-5 in parallel against a real Apps Script user.

**PM-CRIT-02 — The architecture explicitly disclaims product knowledge.** `ARCHITECTURE.md` line 6: "It does not describe any product." `REQ-ARCH-0003` enforces that the product template directories contain *no product content* as an exit criterion for PHASE-0. The architecture is not just product-agnostic; it is product-hostile by gate. The danger: every architectural decision baked in now — adapter shape, tiered tests, monorepo layout, BMAD vendoring — is a bet on a product nobody has scoped. If the eventual product is, say, a Chrome extension or a CLI tool, four phases of GAS-shaped scaffolding are sunk cost.

**PM-CRIT-03 — Cost per requirement is prohibitive.** Let me add up what shipping a single REQ costs under this regime. Author the REQ block (5 min). Allocate the ID via lint tool (1 min). Update the spec frontmatter (3 min). Write the red test with `@test-id` and `@covers` annotations (10–30 min). Commit with all four mandatory trailers (`Task`, `Requirements`, `Tests-Status`, `Phase`) (2 min per commit, times ~4 commits red→green = 8 min). Wait for matrix-drift rebuild on pre-commit (variable). Update the Epic's coverage block (3 min). Pass eight to ten lint gates on the PR (variable retries). Pass `red-before-green` history walk. Pass `req-coverage-100`. Pass `tier-coverage`. Pass `anti-aliasing` n-gram check (which will false-positive on any pair of requirements that legitimately use similar verbs). Total: **45–90 human-minutes of compliance per REQ that is not engineering and not product**. A 20-REQ epic costs 15–30 hours of pure overhead. That is six engineer-days of throughput burned on bureaucracy per Epic.

**PM-CRIT-04 — Red-first as a CI gate forecloses spike-driven product discovery.** P4 is enforced by `red-before-green` walking git history (`ADR-0005` §4, `ADR-0006` §4). This means you cannot ship a 30-minute throwaway prototype to validate whether users even want feature X. Every line of code you write to *learn* is illegal unless it was preceded by a failing test. The `Bootstrap:` trailer escape hatch is gated on review. In practice this means product discovery either happens *outside the repo* (on a branch nobody else sees, where you lie to the gate) or *not at all*. I have never seen a team validate a product hypothesis by writing the test first. The hypothesis comes from a conversation; the prototype comes from a hunch; the test comes after both.

**PM-CRIT-05 — The architecture has no concept of experimentation, A/B testing, feature flags, or gradual rollout.** Scan all 15 documents. There is no mention of cohort splitting, no feature-flag system, no canary deployment, no shadow traffic, no measurement plan, no instrumentation contract. There is a `dev → prod` promotion gate in `ADR-0003` §4 and that is the entirety of the rollout model. For a product that depends on stochastic LLM output (`ADR-0007`), shipping without per-cohort observability is malpractice. You cannot answer "did v2 of the prompt convert better?" because the architecture does not model conversion, cohorts, or comparison at all.

**PM-CRIT-06 — Deprecation is described, removal is not.** `ADR-0004` §1 forbids renames and requires deprecation-plus-supersession for material changes. `ADR-0001` mentions removing a project by deleting its directory and marking REQs deprecated. There is no mechanism to *delete* a feature that nobody uses. Every REQ ever shipped persists in the spec forever as `deprecated`. After two years of product iteration, the spec directory is a graveyard the anti-aliasing lint has to scan in O(n²). Worse: from a product perspective, the architecture treats requirements as permanent and code as ephemeral, which is exactly backwards. Real products kill features; this architecture commemorates them.

## SERIOUS

**PM-SER-07 — The "no semantic search" rule (ADR-0004 §6, §8) forecloses every product surface that needs human discovery.** The justification is a paper on transformer associative memory, applied to *tooling* recall. Fine. But the rule as written prevents the *product* (whatever it eventually is) from using semantic search internally unless it ships a "recall-under-interference" CI gate. If the eventual product is, say, a knowledge-retrieval Apps Script add-on for Google Drive, this rule is going to either be amended out of existence or routinely violated. Decision made too early, applied too broadly.

**PM-SER-08 — `anti-aliasing` n-gram lint will false-positive on legitimate product variations.** Per `ADR-0004` §4: "Pairs above a threshold are a lintable defect." Two REQs describing "user can export to CSV" and "user can export to PDF" will n-gram-collide. Two A/B variants of an onboarding step will collide by design. The threshold is "reviewed quarterly" — meaning every quarter someone fights the lint instead of shipping. The architecture treats similarity as a defect; product surface area treats similarity as a feature (consistency, family resemblance).

**PM-SER-09 — The mandatory four trailers on every commit (ADR-0005 §3) penalize exploratory commits.** Every commit must declare `Task`, `Requirements`, `Tests-Status`, `Phase`. If I commit a 10-line tweak to a CSS rule during a usability fix, I have to allocate a TASK, allocate or find a REQ, and pick a Tests-Status. The architecture has no allowance for "fix typo in copy," "tweak microcopy after user test," "respond to design review note." Product work is full of those. Either we invent ceremony around them or we route them through some bypass that erodes the system.

**PM-SER-10 — The no-mock rule (ADR-0006 §2) makes unit tests cost like integration tests.** P3 is defensible at the integration tier. Applying it at the unit tier means every unit test instantiates real adapters against real Sheets/Drive/HTTP. This is slow, flaky, and quota-limited. From a product velocity perspective: the unit tier exists *so that* a developer can write a 50-line behavior, get a 200ms feedback loop, and iterate. This architecture removes that loop. Developers will route around it (skip the tier, run tests less often) or accept 10x slower iteration. Either way, product cycle time suffers.

**PM-SER-11 — Stochastic-tier prohibitions block legitimate cost-controlled development.** `ADR-0007` §2 bans recorded fixtures, exact-equality, snapshots, and retry-until-pass. The only sanctioned path is sample-size-N distributional tests against the real API. For a product team iterating on prompt design, this means every prompt change costs real Anthropic tokens at every test run. The `@cost-budget` annotation contains this but does not solve it: prompt iteration is *exactly* the workflow where a recorded-fixture baseline lets you ship 30 iterations a day instead of 3.

**PM-SER-12 — Single LLM access point (ADR-0007 §6) is right in principle, premature in timing.** The constraint is sound — centralize cost telemetry, caching, model pinning. But it is enforced from PHASE-1 (lint rule `direct-anthropic-import-banned`) before `packages/anthropic-client/` even exists (PHASE-3). For two phases, the only legal use of the Anthropic SDK is *nowhere*. Anyone trying to do a product spike with LLM calls during PHASE-1 or PHASE-2 either cannot, or violates the gate. This is infrastructure ordering serving the architecture, not the product.

**PM-SER-13 — Phase-exit gate (ADR-0008 §3) blocks intra-phase product wins.** "No REQ from a later phase is `tests-green`." If during PHASE-2 we discover a high-value PHASE-5 product opportunity that could be validated with a tiny prototype, the gate forbids shipping any green REQ from it. The phases are a strict topological order on *infrastructure*, applied as a strict order on *product*. There is no product-driven reason a PHASE-5 user-facing win should wait for PHASE-2 traceability runtime.

**PM-SER-14 — BMAD vendoring (ADR-0002) is a 2.6 MB commit and a permanent maintenance surface.** "Most repos vendor larger dependencies without trouble" is hand-wave, not justification. The product cost is real: every BMAD upgrade is a "substrate PR" requiring smoke test, manifest diff, full suite, rollback procedure (§8). The architecture has chosen a workflow tool with five compliance gates of its own *before* there is anything to manage with it. Recommend: install BMAD on-demand per session until at least one Epic has shipped.

**PM-SER-15 — The architecture has no metric for product success, only compliance.** Search all 15 documents for "user," "customer," "outcome," "metric," "KPI," "retention," "activation," "NPS," "feedback." Almost nothing. The gates measure spec hygiene, test coverage, traceability completeness, phase order. None measure whether the thing being built is useful. From a PM standpoint, this is the most damning observation: *we have built a regime in which we can never fail a product gate because there are no product gates*.

## PROCESS

**PM-PROC-16 — `EPIC.status = done` requires every covering REQ green (ARCHITECTURE.md §5).** This makes "ship a partial epic, learn, decide whether to finish" structurally impossible. Real product epics are often 70% delivered, validated, and either completed or abandoned based on the learning. This architecture treats partial-Epic as failure rather than as the most common successful outcome.

**PM-PROC-17 — The `Story → Behaviors → REQs` decomposition path (ARCHITECTURE.md §5) assumes stories are fully specifiable up-front.** Stories worth shipping rarely arrive fully specified. They arrive as "users seem to want X," get prototyped, observed, refined. The reconciliation gate ("≥1 Story decomposed with REQ-IDs; every covering REQ has TEA-authored failing tests") forces full decomposition before code, which is the same trap as PM-CRIT-04 at the Epic scale.

**PM-PROC-18 — Empty product templates as a PHASE-0 exit criterion (REQ-ARCH-0003) signals priorities.** PHASE-0 ships eight ADRs, the matrix scaffolding, and the hook system, but the product directory must be *empty*. The architecture's first delivered artifact treats the absence of product as a feature. This communicates to anyone joining the team that infrastructure precedes product, organizationally as well as technically.

**PM-PROC-19 — `Material-Architecture-Change: true` trailer + Phase-0 re-gate (ARCHITECTURE.md line 12) makes architectural learning expensive.** PHASE-5 is described (line 19 of `PHASE-5-first-appscript-project.md`) as "the load test for the architecture. Any pain point discovered here results in an ADR amendment, not a workaround." Good. But the cost of an ADR amendment, given the eight existing ADRs cross-reference each other and bind a tower of CI gates, is high. Predict: the first real product work will discover three to five architectural mismatches, each requiring an amendment, each blocking shipment until amended. Recommend: budget for architectural revisitation explicitly, and shrink ADR scope so amendments are cheaper.

**PM-PROC-20 — No explicit deprecation/sunset workflow for unused features.** Per PM-CRIT-06 above, REQs are append-only and supersession is the only path. There is no "feature unused for 90 days, propose deletion" workflow, no usage telemetry hooked into REQ status, no spec-side concept of "this REQ should be removed because the feature it specifies failed in market." A product spec that cannot represent failure-to-validate is a product spec that drifts toward bloat.

---

## Summary

The architecture is a beautiful instrument for governing the production of correct, traceable, principled software. It is not yet an instrument for discovering what software should be produced. Every principle in it is defensible in isolation; their conjunction at this stage of product maturity is premature optimization at organizational scale.

My recommendation as PM is concrete:

1. Defer PHASES 1–4 enforcement until *after* one real product Epic has shipped end-to-end through a deliberately under-gated prototype path.
2. Add a sixth principle: "Product validation precedes architectural enforcement." Give it a gate.
3. Add a deprecation/removal workflow for REQs, with telemetry hook.
4. Add experimentation primitives (cohorts, flags, measurement) to the architecture before they are needed under fire.
5. Allow a `Spike:` trailer that exempts a commit from P3, P4, and the coverage gates, capped at N commits per CHG, expiring after seven days.

Without these, the regime ships its first user-facing line of code somewhere in PHASE-5 — which, on this trajectory, is months out — and discovers at that moment which of its eight ADRs were wrong. That is an expensive moment to discover anything.
