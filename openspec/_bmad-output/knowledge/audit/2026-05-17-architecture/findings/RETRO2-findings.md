# RETRO2 — retrospective (sonnet) — Wave 4

**Source transcript:** [`raw-transcripts/RETRO2-agent-a3608f6b3b6e5586e.jsonl`](../raw-transcripts/RETRO2-agent-a3608f6b3b6e5586e.jsonl)
**Sub-agent description:** `Retrospective sonnet permutation`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a3608f6b3b6e5586e`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke `bmad-retrospective`. Apply as if PHASE-5 just shipped — what did the architecture get WRONG and what was MISSING?

Documents (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md, openspec/architecture/decisions/ADR-0001 through ADR-0008, openspec/architecture/phases/PHASE-0 through PHASE-5

Look back: what should have been specified at PHASE-0 to avoid mid-flight rework? Categorize WRONG (specified incorrectly) and MISSING (not specified at all). Focus on operational failures (hooks didn't fire when expected), adoption failures (developer friction caused bypass), cost failures (stochastic tests bankrupted budget), governance failures, identity/trust failures.

REQUIRED OUTPUT:
- IDs prefix `RETRO2-` (CRIT/SER/PROC inline)
- Minimum 12 findings split between WRONG and MISSING
- Past-tense narrative (the retrospective method)
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have all the information needed to write the retrospective. Let me compose it directly.

---

## PHASE-5 Post-Mortem Retrospective — Architecture Findings

**Scope:** Everything designed from PHASE-0 through PHASE-5 completion.
**Method:** Isolated review of the 15 canonical documents. Each finding is past-tense, categorized, and assigned a failure class. Findings that should have been locked at PHASE-0 are marked accordingly.

---

### WRONG — Specified Incorrectly

---

**RETRO2-CRIT-001 | Operational Failure — Hook Lifecycle Was Declared Before the Runtime Existed**

The architecture as specified in ADR-0005 §6 and REQ-ARCH-0008 mandated that all hooks be declared in `.claude/settings.json` at PHASE-0, but their implementations were deferred to PHASE-2. This produced a two-phase gap — running across PHASE-0 and PHASE-1 — during which the hook declarations existed as exit-0 placeholders. The commit-trailer validation hook (`PreToolUse(Bash:git commit)`) that was supposed to enforce red-first discipline, the mandatory trailers, and the push invariant was silent throughout. That silence was architecturally load-bearing: every commit authored in PHASE-0 and PHASE-1 was authored under the belief that P4 and P3 were enforced, when in fact no enforcement existed. The specification treated hook declarations as an acceptable substitute for hook enforcement at the phase where enforcement was most needed — foundation commits. The correct design would have been to constrain PHASE-0 scope to only artifacts that zero-enforcement hooks could not corrupt (read-only structural files), or to make PHASE-0 exit require at minimum a `commit-trailers-valid` implementation even if no other hook was live. The deferral as written was specified incorrectly: enforcement was described as a phased deliverable when it was actually a foundational trust requirement.

---

**RETRO2-SER-002 | Adoption Failure — ADR-0002 Was Rewritten Mid-Flight Without a Companion Gate Revision**

ADR-0002 Amendment 0001 represented a complete behavioral rewrite — the original wrapper-isolation strategy was abandoned, the install path changed from `bmad/` to `_bmad/`, and the integration model shifted from thin wrappers to native Skills. The amendment mechanism was used correctly in form, but the gate table in ADR-0008 was not updated atomically. Between the moment Amendment 0001 was accepted and the moment `top-level-allowlist`, `bmad-direct-reference`, and `bmad-version-pin` gates were wired to the new paths, any PR touching BMAD integration passed gates that were checking the wrong paths. The specification stated that "a missing gate is itself a build failure," but that self-enforcing property depended on gates referencing the correct paths — which they did not during the amendment window. The correct design would have required that any ADR amendment that changes a path or a boundary also carry a mandatory accompanying gate-table diff as part of the same PR. This coupling was not specified. It should have been at PHASE-0 in the gate-coverage meta-gate definition.

---

**RETRO2-CRIT-003 | Operational Failure — Push Invariant Was Discovered by Incident, Not Designed In**

ADR-0005 Amendment 0001 was explicitly motivated by "a real divergence observed on `claude/general-session-KXgas` after PR #2 merged." The push invariant — that every commit hook must immediately push to origin — was not in the original specification. This means the architecture shipped PHASE-0 through part of PHASE-2 with a known-dangerous failure mode: committed-but-unpushed work was lost on container reclaim. The failure mode was not hypothetical; it was observed in production. The architecture was written as if push-on-commit was an optimization, when it was actually a correctness requirement for any ephemeral-container development model. The correct design would have recognized at PHASE-0 that session journals are gitignored (by design), that the container is ephemeral, and that therefore the only durable state is what reached origin — making push-on-commit a first-class invariant rather than a later amendment. The omission was in the original specification, not in the implementation.

---

**RETRO2-SER-004 | Cost Failure — Stochastic Budget Annotation Was Specified But Not Budgeted Across the Delivery Roadmap**

ADR-0007 §4 required every stochastic test to carry a `@cost-budget tokens=<N>` annotation and established that CI aggregates per-PR and per-nightly budgets. The gate `cost-budget` was deferred to PHASE-2. However, neither ADR-0007 nor ADR-0008 specified what the total token budget was for the repository across all projects, nor how budget headroom would be managed as the number of projects under `projects/` grew. PHASE-5 introduced the first project with a stochastic tier. When that project's stochastic tests were added, they were individually annotated — but there was no repository-level budget ceiling, no mechanism for a new project to claim a budget allocation, and no CI signal for approaching the ceiling before exceeding it. The only specified gate was a per-PR failure after the budget was already exceeded. The correct design would have established a budget registry at PHASE-0 and required each stochastic-tier REQ to reference an allocated budget slot. The cost model was specified at the test level but not at the system level.

---

**RETRO2-SER-005 | Governance Failure — The ADR Amendment Process Had No Scope Guard**

The amendment mechanism was correctly specified as append-only (ADR-0002 and ADR-0005 each contain amendment logs). However, the amendment rows were not constrained in scope. Amendment 0001 of ADR-0002 was described as a "complete rewrite." A complete rewrite of an ADR through the amendment mechanism is semantically equivalent to supersession, but without the identity break that supersession entails. The original ADR-0002 text, which designed a wrapper-isolation strategy, remained visible at the top of the document, making it architecturally ambiguous which sections governed until the reader reached the amendment log at the bottom. Any tooling that parsed ADRs without reading the amendment log would have processed contradicted text. The correct design, which should have been specified at PHASE-0, would have distinguished between additive amendments (new sections, new rules) and superseding amendments (rules that cancel prior text), with the latter triggering the same ADR-supersession protocol used for REQs.

---

**RETRO2-PROC-006 | Adoption Failure — PHASE-1 Referenced ADR-0003 Before ADR-0003 Was Listed in Its Own Scope**

PHASE-1's scope referenced ADR-0003 as a source of lint rules to enforce (`gas-global-outside-adapter`), and the PHASE-1 file named it explicitly in its goal statement. ADR-0003 defined the Apps Script adapter and deployment topology. But PHASE-0's exit criteria required only ADR-0001 through ADR-0008 to be `status: accepted` — it did not require ADR-0003 to be internally consistent with the actual clasp and GAS deployment infrastructure available at the time PHASE-1 began. ADR-0003 specified four test tiers and a `dev`/`prod` deployment topology, including a CI service account, before any CI service account had been provisioned, any `clasp` configuration had been validated, and any Apps Script project had been created. The specification outpaced the infrastructure. The correct design would have required that any ADR describing runtime topology declare its infrastructure dependencies, and that those dependencies be verified as part of the ADR acceptance gate rather than discovered in PHASE-5 when the first project was actually stood up.

---

### MISSING — Not Specified at All

---

**RETRO2-CRIT-007 | Identity/Trust Failure — No Trust Model for the Claude Code Agent Identity Was Specified**

The architecture specified that hooks enforce commit discipline, that `--no-verify` is forbidden, and that branch protection blocks bypasses on `main`. It did not specify who or what was trusted to author commits at all. There was no requirement for a verified agent identity on commits, no specification of which GitHub actor owned the CI service account that pushed from hooks, no policy on whether checkpoint commits were distinguishable by their author from human commits, and no requirement that the push invariant hooks authenticated to origin with a verifiable credential scoped to the minimum necessary permissions. A credential with write access to `main` that fired on every commit hook was an unspecified trust surface. This was an entire threat class — credential scope, hook authentication, and agent-identity attribution — that did not exist in the specification. It should have been an ADR at PHASE-0.

---

**RETRO2-CRIT-008 | Operational Failure — No Recovery Protocol for Hook Failures Was Specified**

ADR-0005 §8 meticulously catalogued failure modes for crashes and container reclaims, with loss guarantees for each. ADR-0005 §6 described seven hooks. Neither document specified what happened when a hook itself failed. If `journal_commit.py` crashed mid-execution after the commit was written but before the push completed, the push invariant was violated silently. If `checkpoint.py` encountered a non-fast-forward condition and aborted with a diagnostic (as specified in ADR-0005 §6), the specification said the hook "aborts with a diagnostic" — but did not say whether the session ended cleanly, whether the journal recorded a `session_end` event, or whether a subsequent session would detect the inconsistency. The failure-mode table treated hooks as atomic, when hooks are themselves programs that can fail, timeout, or produce partial output. The missing specification was a hook-failure taxonomy with explicit recovery invariants for each hook, similar in form to the crash-failure table that existed for container-level failures.

---

**RETRO2-SER-009 | Governance Failure — No Model Version Transition Protocol Was Specified**

ADR-0007 §3 acknowledged that model upgrades (Sonnet 4.6 to 4.7, etc.) would require re-running stochastic tests and a PR against `packages/anthropic-client/`. ADR-0007's consequences section stated this explicitly. But no ADR specified the full transition protocol: what constituted an acceptable stochastic re-baseline, how long the transition window was, whether old-model tests could be deprecated in the same PR that introduced new-model tests, how the `cache-hit-regression` baseline transferred across model boundaries, and who had authority to sign off on a model transition. Model retirement is not a rare edge case — it is a recurring operational event with a known cadence. The omission left each model transition as an ad-hoc governance event. This should have been an ADR at PHASE-0, even if the protocol was simple. The absence of a protocol meant each transition was resolved by convention, and conventions are not lintable.

---

**RETRO2-SER-010 | Adoption Failure — No Onboarding Constraint for New Projects Was Specified**

ADR-0001 described the `projects/` layout. ADR-0002 §9 described per-project BMAD output isolation. PHASE-5 described the first project's setup. But nothing in the specification required or enumerated a checklist that a new project must satisfy before its first commit reached `main`. The check list was implied by the architecture — per-project `_bmad/custom/config.toml`, per-project `openspec/` overlay, CI matrix entry, service account credential, `clasp.json` pointing at a provisioned `dev` deployment — but it was not canonical. Each requirement lived in a different document. A developer starting the second project in PHASE-5+1 had to reconstruct the checklist from five documents. The consequence was that the second project's onboarding introduced divergence from the first project's structure that was only caught by diff review rather than by a gate. The missing artifact was a `projects/_TEMPLATE/` directory (analogous to `openspec/changes/_TEMPLATE/`) with a machine-readable checklist of required files and their structural constraints, gated by `project-onboarding-lint` in CI.

---

**RETRO2-SER-011 | Cost Failure — No Promotion Staleness Budget Was Specified**

ADR-0002 §7 mentioned a future `stale-staging` lint rule that would flag drafts sitting unpromoted past a configurable threshold, explicitly marking it as "deferred CHG." The deferral was made without specifying what the threshold would be, how the threshold interacted with phase duration, or what the escalation path was when a draft exceeded the threshold. By PHASE-5, the `openspec/_bmad-output/` staging directory had accumulated drafts from across PHASE-2, PHASE-3, and PHASE-4 — each produced by a BMAD skill, each requiring human triage to determine whether it should be promoted or discarded. The accumulation was not a failure of process; it was a predictable consequence of specifying promotion as a TASK under an explicit CHG without specifying the maximum lag between draft creation and triage decision. The architecture described promotion in full detail but was silent on the time horizon. The missing specification was a concrete threshold, expressed as a phase boundary (not a wall-clock duration), beyond which an unpromoted draft was a gate failure rather than a reminder.

---

**RETRO2-PROC-012 | Governance Failure — No Conflict Resolution Protocol for Simultaneous ADR Amendment Proposals Was Specified**

The ADR amendment mechanism was specified as append-only with sequential amendment numbers. The specification did not address what happened when two concurrent CHGs both proposed amendments to the same ADR. In a multi-session development model with parallel PRs, two sessions could both author Amendment 0002 to the same ADR in separate branches. The specification's answer — derived from git's merge mechanics — was that one would win and one would conflict, resolved by rebase. But rebase resolution of amendment log rows is not semantically neutral: the amendment that lost the conflict had to renumber itself, and the specification did not require the renumbered amendment to be re-reviewed. The missing specification was a lock protocol for in-flight ADR amendments, either via a convention (only one open PR may amend a given ADR at a time, enforced by a CI gate that reads open PR bodies) or via a reservation mechanism in the amendment table where an empty reserved row was committed before the amendment body was authored. Without this, amendment numbering was reliable in single-session development and fragile in parallel development.

---

**RETRO2-CRIT-013 | Operational Failure — No Degraded-Mode Specification for Partial Phase Exit Was Specified**

ADR-0008 §3 specified that `phase-exit` blocked merge to `main` when phase exit criteria were not met. The specification was binary: either all REQ-IDs in the phase were `tests-green`, or the merge was blocked. There was no provision for a declared-incomplete phase transition, where a phase was tagged as `partially-exited` with an explicit list of deferred REQ-IDs that were moved to the next phase as blocking items. In practice, PHASE-5's exit gate required "no unresolved principle violations," but the mechanism for declaring a violation resolved was an ADR amendment — which itself required a PR, which itself required phase-exit to pass. This created a circular dependency: a principle violation discovered in PHASE-5 had to be resolved by an ADR amendment, but the ADR amendment PR was blocked by the same phase-exit gate it was trying to satisfy. The missing specification was an explicit phase-amendment track: a parallel CHG type that could merge to `main` ahead of the phase-exit gate, carrying `Phase-Amendment: true` in its trailer, with an exemption enumerated in `tools/trace/checkpoint_exemptions.yaml`. Without this, any architectural correction discovered at PHASE-5 was structurally impossible to merge without a workaround that violated the very principles being corrected.

---

### Summary Assessment

Of the 13 findings above, 5 were in the WRONG category — things the specification addressed but addressed incorrectly — and 8 were in the MISSING category — entire failure classes the specification did not address at all. The MISSING findings were, as a class, more damaging than the WRONG findings, because they were invisible to CI. A WRONG specification at least produced a gate; the gate could be fixed. A MISSING specification produced no gate, and the absence was only discovered when the failure mode materialized in production.

The four most load-bearing items, each of which should have been a PHASE-0 deliverable, were: the push invariant as a first-class invariant rather than a later amendment (RETRO2-CRIT-003), the hook-failure taxonomy (RETRO2-CRIT-008), the agent identity and trust model (RETRO2-CRIT-007), and the circular dependency in the phase-exit gate for architectural corrections discovered mid-phase (RETRO2-CRIT-013). Each of these represented a case where the architecture correctly identified the risk — ephemeral containers, hook-mediated enforcement, service-account credentials, phase gates — and then stopped exactly one layer short of specifying what happened when that mechanism itself failed.
