# SCENFUT — scenario-unfold-forward-eighteen-months (opus) — Wave 7

**Source transcript:** [`raw-transcripts/SCENFUT-agent-a259180743a48e765.jsonl`](../raw-transcripts/SCENFUT-agent-a259180743a48e765.jsonl)
**Sub-agent description:** `Scenario unfold forward eighteen months`
**Session ID:** `2fa6b8f3-f53b-44bf-873e-44bdb568369b`
**Agent ID:** `a259180743a48e765`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Your method is **forward scenario unfolding** — you walk concrete scenarios that play out 18 months from now, after PHASE-5 has shipped and the architecture has accumulated some operational hindsight. NOT a pre-mortem (you're not catastrophising specific failures); NOT a retrospective (you're not Winston-in-2029); your temporal lens is forward but proximal (18 months from PHASE-5 first ship).

Documents to review (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- All 8 ADRs in openspec/architecture/decisions/ (list the directory; ADR-0001 through ADR-0008)
- All 6 PHASE files in openspec/architecture/phases/ (list the directory; PHASE-0 through PHASE-5)

Scenarios to unfold forward (18 months from PHASE-5 ship, i.e., late 2027):

1. **A new architectural decision arises.** The team realises they need an ADR-0009 (e.g., "how to evolve the BMAD vendoring discipline as upstream BMAD ships v7"). Walk the steps to author + accept + integrate ADR-0009 under the architecture-as-written. What's smooth? What's clunky? What's structurally undefined?
2. **The spec_lint rules drift from their original threshold.** Three quarterly threshold reviews have not happened. A new contributor proposes recalibrating. What's the procedure? Who decides? Is there a recovery from a multi-quarter drift?
3. **A second project starts (per PHASE-5's scaling promise).** Per-project BMAD output isolation (PHASE-5 §Scope) is asserted, but the second project surfaces shared-vs-isolated decisions that the architecture didn't anticipate. What ADR amendments are forced? Which stay informal?
4. **An LLM-as-judge experiment** is proposed (separate provider, A/B test against Claude on a specific extraction task). Per ADR-0007 §6, all LLM access goes through `packages/anthropic-client/`. Walk the steps to admit the second provider. How much architecture change is required?
5. **A security incident is suspected.** A team member observes that a recent commit looks anomalous (trailer values inconsistent with the diff). Walk the response: who investigates, what tools surface the relevant data, how is the incident scoped, how is the matrix and journal queried for impact? What's missing?
6. **The matrix becomes uncomfortably slow.** After 18 months of work, `rebuild.py` runs take >3 minutes locally and the cache hit rate has degraded. Walk the diagnosis + remediation. What does the architecture offer? What does the engineer have to invent?

For each scenario, surface at least 2 distinct defects in the architecture-as-written that would block, mislead, or silently corrupt the 18-month-forward execution. Findings should be specific (file + section + what the actor experiences at 18 months) and cite the architectural cause.

Distinct from prior streams:
- SCENNOW (Wave 6, scenario × current × holistic × blocking) walked current-state scenarios. Yours is 18-month-forward.
- PERSRETRO (Wave 6, persona × post-hoc × holistic × *) was Winston-2029 from 3 years out. Yours is 18 months forward — close enough to be tractable, far enough to surface real drift; not retrospective.
- PREM / PREM2 / RED / RED2 / STAKE all had forward-looking lenses but focused on failure narratives (pre-mortem) or stakeholder simulation. Yours is scenario-unfold without the failure framing — what unfolds, not what fails.
- INHER / INHER2 / RETRO / RETRO2 are scenario × post-hoc. Yours is scenario × forward.

REQUIRED OUTPUT:
- Finding IDs prefixed `SCENFUT-` with severity inline (e.g., `SCENFUT-CRIT-001`, `SCENFUT-SER-002`, `SCENFUT-PROC-003`).
- Severity guide: CRIT = blocks the 18-month scenario without architectural amendment; SER = scenario proceeds with significant friction or invented procedure; PROC = procedural gap surfaced by the scenario.
- Minimum 12 findings, target 14-18 (≥2 per scenario).
- Tag each finding with the scenario number.
- 1200-1800 words.
- NO preamble. Start directly with finding SCENFUT-CRIT-001 (or SER-001 if no CRIT).
- End with a one-paragraph summary that totals by severity and names the scenario with the most blocking 18-month-forward gaps.

Do not read files outside the architecture documents listed.
```

## Findings deliverable (final assistant message)

Now I have complete context to unfold the six forward scenarios. Let me produce the findings.

SCENFUT-CRIT-001 [Scenario 1: ADR-0009 authoring]
The architecture defines no procedure for *introducing* a new ADR. ARCHITECTURE.md §10 (REQ-ARCH-0002) hard-codes "ADR-0001 through ADR-0008 are all present" as an exit criterion. At 18 months, the contributor proposing ADR-0009 finds that REQ-ARCH-0002 — a `tests-green` invariant — does not include ADR-0009 in its enumeration. Whether passing the test still requires "exactly 0001..0008" or "at least 0001..0008" is undefined. ADR-0008 §2 `gate-coverage` walks "every ADR" but the architecture nowhere specifies how the walk discovers new ADRs (filename glob vs. an enumerated list). Authors must invent both the spec amendment path and the gate-discovery mechanism before ADR-0009 can land.

SCENFUT-SER-002 [Scenario 1: ADR acceptance ceremony]
No ADR file defines a state machine for ADRs themselves. ADR-0001..0008 all carry `status: accepted` from inception (dated 2026-05-16), with no documented `proposed → accepted → superseded` transition, no quorum, no signing party, and no relation to phase-exit. CLAUDE.md says "no decision unless it's an ADR" but the architecture never says who accepts an ADR or in what commit. At 18 months the author of ADR-0009 has no procedure to point to, and the gate `phase-exit` (ADR-0008 §3) only checks that "the next phase's entry ADR (if any) is `status: accepted`" — not how it got there.

SCENFUT-PROC-003 [Scenario 1: ADR integration into matrix]
ADR-0005 §9 lists `audit` targets but not `audit ADR-NNNN`. The audit CLI cannot answer "which REQs, tests, and commits reference ADR-0009?" deterministically. The ADR-as-artifact is in §4's ID table but absent from the audit interface — a silent omission the team will rediscover only when investigating impact for the new decision.

SCENFUT-CRIT-004 [Scenario 2: spec_lint threshold drift]
ADR-0004 §4 says the anti-aliasing threshold is "pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." No artifact in the architecture creates the quarterly task, owns it, or escalates when it slips. There is no `quarterly-review-overdue` gate in ADR-0008 §1's inventory. At 18 months a contributor sees three missed reviews and cannot determine whether the current threshold was decided by ADR, by a PR review, or by drift; the architecture provides no recovery procedure other than "open another quarterly task" — which there is no calendar to remind anyone to do.

SCENFUT-SER-005 [Scenario 2: who owns the threshold]
ADR-0004 names no owner for the lint threshold. ADR-0008 §1 assigns *gates* to owners (`tools/spec_lint`) but the *parameter* tuning has no responsible role. BMAD personas (PM, Architect, SM, Dev, PO, TEA) are referenced as workflow surface in ARCHITECTURE.md §9 but none are designated as policy owner for measurement thresholds. The contributor's recalibration PR has no defined reviewer; spec_lint changes that touch `config.yaml` will pass the same CI gates as code, with no second-order check that "this is a policy change."

SCENFUT-PROC-006 [Scenario 2: ratchet vs. recalibration]
ADR-0004 §4 says the threshold "is pinned" but never says it is a ratchet. If a multi-quarter drift surfaces 17 false positives because the corpus grew, the contributor cannot tell whether the right move is to *loosen* the threshold (risking new aliasing collisions) or to *raise* it and force a retroactive cleanup. Architecture-as-written gives no policy direction; the choice will be made ad-hoc, and any precedent set silently becomes the new norm.

SCENFUT-CRIT-007 [Scenario 3: shared specs across projects]
ARCHITECTURE.md §3 specifies `projects/<project>/openspec/` "extends root specs by reference" — and ADR-0001 §Consequences echoes it — but neither defines the *extends* mechanism, the resolution order between root and project specs, or what happens when two projects need *incompatible* extensions of the same root REQ. At 18 months, project B needs to override `REQ-AUTH-0007`'s tier from `integration` to `e2e`; ADR-0004 §1 says identifiers are immutable and frontmatter changes constitute supersession — meaning each project's overlay must supersede with a new ID, breaking cross-project comparability. The architecture forces an ADR amendment to admit this case.

SCENFUT-SER-008 [Scenario 3: per-project matrix scoping]
ADR-0005 §2 defines a single matrix at `openspec/traceability/matrix.yaml`. Nothing in the architecture says whether per-project matrices exist, or whether the root matrix subsumes them. With one project, ambiguity is harmless; with two, `rebuild.py` must either scan both `projects/*/openspec/` overlays (no spec says so), produce per-project artifacts (no spec says so), or merge — risking REQ-ID collisions between projects whose domain prefixes overlap (e.g. both have `REQ-AUTH-*`). ADR-0004 §1 scopes counters "to the domain," not "to the project + domain." The collision is a silent corruption: an existing audit invocation returns the wrong artifact, with no error.

SCENFUT-PROC-009 [Scenario 3: shared adapter ownership]
ADR-0006 §3 says external systems are accessed via interfaces in `packages/shared-ts/adapters/` with "at minimum two real implementations." A second project that needs a *third* adapter (e.g. a `gas-staging-rest`) has no governance defined: is the new adapter a PR against `packages/shared-ts/` (shared cost) or against the project (no path defined for project-local adapters in the layout)? ARCHITECTURE.md §3 shows `packages/shared-ts/` but no `projects/<name>/packages/`. The team will either fork the shared adapter (violating SoT) or shoehorn project-specific code into a shared package (violating ownership) — neither is what the architecture intended, but architecture-as-written forces one.

SCENFUT-CRIT-010 [Scenario 4: second LLM provider]
ADR-0007 §6 says "no code outside `packages/anthropic-client/` may import the Anthropic SDK" with lint rule `direct-anthropic-import-banned`. The rule name and the package name are both Anthropic-specific. To admit OpenAI/Vertex/Gemini for an A/B judge experiment, the team must either (a) rename the package and the lint rule — breaking REQ-ID immutability for `REQ-LLM-*` and forcing a PHASE-3 re-gate, or (b) shim the second provider through `anthropic-client` (a fake-adapter pattern explicitly forbidden by ADR-0006 §2 "real-for-real, not real-for-fake"). The architecture nowhere considers multi-provider — at 18 months this is a blocking ADR-0007 amendment.

SCENFUT-SER-011 [Scenario 4: cost-budget and cache-hit per provider]
ADR-0007 §4 (cost budget) and §5 (prompt-caching discipline) and ADR-0008 §1 gates `cost-budget` and `cache-hit-regression` are written assuming one provider with one cache and one token-cost model. The judge experiment runs *both* providers in the same PR; the architecture has no per-provider budget, no per-provider cache baseline, and `cache-hit-regression` will fire spuriously when the comparator (which may not support caching) is exercised. The team must invent per-provider budget telemetry before the experiment can pass CI.

SCENFUT-PROC-012 [Scenario 4: tier semantics for cross-provider tests]
ADR-0007 §1 says "the `tests/stochastic/` tier exercises code that depends on `packages/anthropic-client/`." A cross-provider A/B test depends on *both* clients. ADR-0006's tier table has no entry for cross-provider comparison; ADR-0007 §3's permitted assertion forms include nothing about *comparative* assertions between two stochastic systems. The contributor authoring the experiment must invent a fifth tier or stretch `stochastic` semantics in a way the architecture didn't anticipate.

SCENFUT-CRIT-013 [Scenario 5: trailer-vs-diff anomaly]
ADR-0005 §3 mandates trailers and §4 says `validate_commit.py` walks history to verify red-before-green. Neither hook validates that the trailer's `Requirements:` REQ-IDs actually match the files touched in the diff. A commit whose `Requirements: REQ-AUTH-0007` trailer is plausible but whose diff touches only `REQ-BILLING-0042` files will pass the PreToolUse hook. At 18 months the suspicious commit can only be triaged by a human reading the diff against the trailer — no tool surfaces "trailer/diff mismatch." This is a silent integrity gap, not a gated invariant.

SCENFUT-SER-014 [Scenario 5: incident response procedure]
The architecture has no incident-response artifact. `tools/trace/audit.py` (ADR-0005 §9) answers ID-scoped queries but cannot answer "show all commits in the last 30 days whose `Tests-Status` claims `green` but whose diff has no test files." There is no `audit COMMIT-<sha>` form, no `audit PR-<n>` form, no journal query interface beyond what `rebuild.py` consumes. The investigator must invent ad-hoc `git log --grep`/`jq` plumbing and reason from raw `.claude/journal/` files — losing reproducibility and creating a precedent for shadow tooling.

SCENFUT-PROC-015 [Scenario 5: who is the responder]
ADR-0008 §1 assigns gate owners; ARCHITECTURE.md §9 names BMAD personas; nothing names a security-incident role. CLAUDE.md says "ask" when in doubt but there is no security on-call, no escalation chain, no defined containment authority (e.g. who can revert vs. who needs review). A real anomaly at 18 months stalls on "who decides to revert the suspicious commit on `main`?"

SCENFUT-CRIT-016 [Scenario 6: matrix scaling not designed for]
ADR-0005 §2 says `rebuild.py` regenerates the matrix deterministically from "git + spec files + test annotations + journals." Nothing in the ADR or PHASE-2 sets a performance budget, defines incrementality, or specifies caching. At 18 months with several projects and 18 months of journals (potentially gigabytes of `.claude/journal/session-<id>.jsonl`), `rebuild.py` walks the full corpus on every commit (pre-commit hook, ADR-0008 §5). The engineer attempting remediation finds no architectural hook for incremental rebuild: the ADR insists on full determinism *from sources*, which by construction grows linearly with history. There is no defined "matrix epoch" or "journal compaction" path.

SCENFUT-SER-017 [Scenario 6: cache-hit-rate degradation telemetry]
The phrase "cache hit rate has degraded" applies to two different caches in the architecture: ADR-0007 §5 (prompt cache) and ADR-0005 §2 (matrix as cache). They share the word "cache" but no shared telemetry surface, dashboard, or even a glossary disambiguation. The engineer triaging "the cache is slow" must first disambiguate which one, against an architecture that does not distinguish them in any one place. There is no `cache-health` gate analogous to `cache-hit-regression`.

SCENFUT-PROC-018 [Scenario 6: journal compaction and retention]
ARCHITECTURE.md §3 says `.claude/journal/` is "gitignored runtime"; ADR-0005 §1 makes journals a source of truth. The contradiction surfaces at scale: a gitignored runtime artifact cannot be a durable source of truth across container reclaims unless it is exported somewhere. ADR-0005 §8's "container reclaim, push succeeded" → "Zero" loss assumes the matrix has already absorbed the journal contents; if `rebuild.py` slows enough that pre-commit hook compaction is throttled or skipped (no spec forbids skipping), the journal becomes the sole record of red-first sequencing — and is gitignored. The engineer has no architecture-blessed compaction strategy and risks losing P4 provenance during remediation.

---

Summary: 18 findings total — 6 CRIT (001, 004, 007, 010, 013, 016), 6 SER (002, 005, 008, 011, 014, 017), 6 PROC (003, 006, 009, 012, 015, 018). Every scenario produced at least three findings with at least one CRIT. The scenario with the most blocking 18-month-forward gaps is **Scenario 6 (matrix performance at scale)**: it surfaces a CRIT (no incremental rebuild path designed into ADR-0005), a SER (cache-term overloading between two distinct caches), and a PROC (journal-as-SoT vs. journal-as-gitignored-runtime contradiction) that together imply the matrix subsystem will silently corrupt or become unusable as the corpus scales, with no architectural escape hatch short of an ADR-0005 amendment. Scenarios 1 (new-ADR procedure) and 3 (second project shared/isolated boundary) are close seconds; both force ADR amendments before their 18-month execution can even begin.
