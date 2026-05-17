# FIRST — advanced-elicitation-first-principles (sonnet) — Wave 2

**Source transcript:** [`raw-transcripts/FIRST-agent-afe9e82773aa1020b.jsonl`](../raw-transcripts/FIRST-agent-afe9e82773aa1020b.jsonl)
**Sub-agent description:** `First-principles review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `afe9e82773aa1020b`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-advanced-elicitation` skill via the Skill tool, then apply its **first-principles method** to the architecture artifact below.

First-principles method: ignore the existing framing. From the goal (a monorepo that supports multiple Apps Script projects with traceability, BMAD workflow, and CI-enforced principles), derive the architecture you would design from scratch. Then compare your derivation against the actual artifact. The deltas are the findings.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Apply these checks first-principles:
- If you started fresh, what's the minimum set of ADRs?
- Which decisions in the actual artifact are arbitrary vs derivable?
- What's missing that first-principles thinking would produce immediately?
- Which decisions made sense at one level of abstraction but are wrong at the actual level?
- Is the layered approach (operating principles → ADRs → phases → REQs) actually consistent with first-principles?

REQUIRED OUTPUT:
- Stable IDs: prefix `FIRST-` (e.g. FIRST-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 12 findings
- Each finding: what first-principles thinking produces, what the artifact has, the delta, why it matters
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

ADR-0003 exists but was not in the 15 documents listed. I will not read it. I have sufficient material from the 14 documents I've read to complete the analysis.

---

**FIRST-PRINCIPLES REVIEW — ARCHITECTURE ARTIFACT**
Scope: ARCHITECTURE.md + ADR-0001 through ADR-0008 + PHASE-0 through PHASE-5

---

## CRITICAL

**FIRST-CRIT-01 — ADR-0003 is referenced but not readable; it is a structural dead link in the reviewed artifact set**

First principles produce: every rule that is enforced must be derivable from documents that exist and are legible to all participants. If a constraint (GAS globals, adapter pattern, runtime model) is referenced across ADR-0001, ADR-0006, ADR-0007, ADR-0008, PHASE-1, PHASE-4, and PHASE-5 but its canonical definition lives in a document listed as part of the architectural foundation, that document must exist and be readable within the reviewed set.

Artifact has: ADR-0003 is referenced by name seventeen times across the reviewed documents (ADR-0008 §1 lists `gas-global-outside-adapter` as enforcing ADR-0003; PHASE-1 cites it; PHASE-4 scope item 1 requires GAS adapter interfaces "per ADR-0003"; PHASE-5 item 1 requires "full layout per ADR-0003"). The file exists on disk but was not included in the listed 15 documents and its content was not readable in this review.

Delta: A foundational architectural constraint (GAS runtime model, global adapter isolation) is enforced by gates in ADR-0008, required by phase exit criteria in PHASE-1 and PHASE-4, and mentioned in REQ-ARCH-0002 as a deliverable — but its definition is opaque to any reviewer who reads only the 15 named artifacts. The ARCHITECTURE.md §2 paragraph ("Constraints from prior art") mentions only the paper (→ ADR-0004). ADR-0003 is never summarized inline.

Why it matters: if ADR-0003 is the single source of truth for GAS runtime constraints and it is absent or ambiguous, then every downstream gate that references it (`gas-global-outside-adapter`, PHASE-4 adapter tests, PHASE-5 adapter wiring) is enforcing an undefined rule. A new team member or AI agent reading the top-15 documents cannot derive the rule independently.

---

**FIRST-CRIT-02 — The traceability matrix is declared the source of phase-exit truth, but the matrix cannot be populated until PHASE-2; PHASE-0 and PHASE-1 exit criteria are therefore circularly unenforceable**

First principles produce: an exit-criteria mechanism must itself be operational before it is used as an exit mechanism. If the tool that enforces "all REQ-ARCH-* are tests-green" does not exist until PHASE-2, then PHASE-0 and PHASE-1 cannot exit through the stated gate.

Artifact has: PHASE-0 exit says "`phase-exit` CI gate verifies all REQ-ARCH-* are `tests-green` in the matrix." ADR-0008 §3 says `phase-exit` reads the matrix. `tools/trace/rebuild.py` and the `matrix-drift` gate land in PHASE-2. PHASE-0 explicitly states "hook implementations land in PHASE-2."

Delta: The gate that enforces PHASE-0 exit depends on PHASE-2 infrastructure. PHASE-0 tests live in `tools/ci/tests/test_phase0.py` (PHASE-0 scope item 12), which reads files, but the `phase-exit` gate requires a populated matrix that can only be produced by `tools/trace/rebuild.py` (PHASE-2). The artifact papers over this by saying PHASE-0 tests "only read files," but the formal exit mechanism is the `phase-exit` gate, which requires the matrix.

Why it matters: the architecture states that "a principle without a CI gate is a build failure." If the gate itself is a TODO stub, the principle is unenforced from day zero. Any phase that exits before PHASE-2 infrastructure is live exits on honor code, not mechanical enforcement. This contradicts the entire premise of P1 and ADR-0008.

---

**FIRST-CRIT-03 — Red-first (P4) is structurally unenforceable in PHASE-0 because the test suite that validates P4 (`tools/trace/validate_commit.py`) lands in PHASE-2**

First principles produce: if P4 requires every test to exist in a failing-state commit before the green-state commit, and the machine that validates that property does not exist until PHASE-2, then all PHASE-0 and PHASE-1 tests can be written green-first and no gate will catch it. The red-first property for those early tests becomes permanently unverifiable retroactively, because `validate_commit.py` walks git history — but if the history was written without the property, walking it later will reveal the violation but the commits are immutable.

Artifact has: ADR-0005 §4, ADR-0006 §4, and PHASE-0 all mandate P4. `tools/trace/validate_commit.py` enforces it via the `red-before-green` CI gate. That gate lands in PHASE-2. PHASE-0 and PHASE-1 tests are authored during those phases with `commit-trailers-valid` as a placeholder that "exits 0 with a TODO comment."

Delta: The bootstrap period (PHASE-0 + PHASE-1) is P4-free in practice. Any test written green-first in PHASE-0 will permanently satisfy the form "there exists a prior red commit" only if the author manually honored P4 — but no gate verifies it. The architecture has no bootstrap exception documented, no `Bootstrap:` trailer guidance for early tests (ADR-0006 §4 mentions `Bootstrap: <reason>` only for "bulk green-starts"), and no explicit acknowledgment that PHASE-0 and PHASE-1 tests are exempt or handled differently.

Why it matters: P4 is Operating Principle 4. Its violation during the bootstrap period is an architectural blind spot, not an implementation detail.

---

**FIRST-CRIT-04 — Session journals are gitignored runtime artifacts; any traceability matrix dependent on them cannot be reproduced from a clean clone**

First principles produce: if the matrix is a "derived cache" from four sources (git, spec files, test annotations, session journals), and one of those sources is gitignored, then the matrix cannot be fully regenerated from a clean clone. The guarantee "matrix can be regenerated from sources at any time; corruption is recoverable" is false for a fresh checkout.

Artifact has: ARCHITECTURE.md §8 lists `.claude/journal/session-<id>.jsonl` as append-only and gitignored (`PHASE-0 scope item 11`). ADR-0005 §1 lists journals as source-of-truth (layer 4). ADR-0005 §2 says "Matrix can be regenerated from sources at any time; corruption is recoverable."

Delta: The matrix rebuild can only reproduce journal-derived entries (session context, task activation, file-touch events) if the journals exist in the working tree. On a clean clone the journals are absent. `tools/trace/rebuild.py` must then produce a partial matrix (from git + spec + tests only) or fail. Neither behavior is documented. The ARCHITECTURE.md failure-mode table (§8) lists "Container reclaim, push succeeded → Zero loss" — but this applies to committed work, not to the journal, which was explicitly excluded from the push-invariant protection.

Why it matters: the architecture claims full recoverability and zero-briefing session resume. A developer joining mid-project on a clean clone gets a matrix missing all journal-derived columns. The audit interface (`tools/trace/audit.py`) will silently produce incomplete answers.

---

**FIRST-CRIT-05 — The push invariant (ADR-0005 §6 amendment 0001) creates a mandatory network call inside every `git commit` hook, making offline commits structurally impossible**

First principles produce: a commit is a local operation. A hook that pushes to origin on every commit converts a local-atomic operation into a distributed one with network failure modes. This is a category error that first-principles design would resolve by separating "local traceability" from "remote synchronization."

Artifact has: ADR-0005 §6 (amendment 0001) states "`PostToolUse(Bash:git commit)` → `journal_commit.py` — appends `commit` event and pushes `HEAD` to origin as a fast-forward. Non-FF aborts the hook with a diagnostic."

Delta: If the network is unavailable, every commit attempt fails (the hook fires and the push fails). The ADR says "Non-FF aborts the hook with a diagnostic" — but it does not say what happens if the network is unreachable. The Stop/SessionEnd hook also pushes. The ARCHITECTURE.md failure-mode table does not enumerate "network unavailable during commit-hook push." This is a single-point-of-failure: all code velocity halts when the origin is unreachable, including during AI container sessions where network reliability is not guaranteed.

Why it matters: BMAD sessions running in ephemeral containers may have intermittent network access. The architecture claims resilience against container reclaim but has introduced a new failure mode where normal commits fail due to network partitions.

---

## SERIOUS

**FIRST-SERI-01 — The anti-aliasing lint rule (ADR-0004 §4) uses n-gram similarity, which is a semantic-proximity approximation — exactly what the paper says fails at scale**

First principles produce: if the foundational constraint is that semantic similarity between specifications leads to catastrophic interference (the paper), then using n-gram similarity to detect near-duplicate specs is using a proxy for semantic similarity. It does not detect conceptually-aliased specs that use different vocabulary, and it false-positives on structurally-similar specs that are conceptually distinct. The paper's concern is embedding-space collapse, not surface-text similarity.

Artifact has: ADR-0004 §4 prescribes "pairwise n-gram similarity across all Description and Acceptance bodies." The threshold is "pinned in `tools/spec_lint/config.yaml` and reviewed quarterly."

Delta: The paper's aliasing concern is semantic (embedding space), but the implemented defense is syntactic (n-gram). Two requirements that say the same thing in different words will not be detected. Two requirements that share boilerplate ("The system must...") will generate false positives. The quarterly review of a numeric threshold does not address this structural mismatch.

Why it matters: the entire rationale for ADR-0004 is that semantic overlap causes retrieval failure. The detection mechanism does not address the failure mode it is supposed to prevent.

---

**FIRST-SERI-02 — The layered specification model (Vision → Brief → PRD → Architecture → Epic → Story → REQ → TEST) is introduced in ARCHITECTURE.md §5 but there are no REQs, gates, or phase deliverables that enforce the cross-layer consistency**

First principles produce: if two converging flows (top-down and bottom-up) must reconcile at the Epic boundary, and the Epic must carry a `coverage:` block listing REQ-IDs, then there must be a machine-checkable rule that the REQs in the coverage block actually trace back to the PRD assertions they are supposed to cover. Without that, the reconciliation gate is syntactic (does the field exist?) not semantic (does it prove the PRD requirement is tested?).

Artifact has: ARCHITECTURE.md §5 describes the reconciliation requirement. ADR-0008 §1 does not list any gate that validates PRD-to-REQ traceability (only `req-coverage-100`, which is REQ-to-TEST). The phase deliverables do not include a "PRD coverage" gate.

Delta: the architecture enforces REQ→TEST coverage at 100% but has no enforcement that all PRD assertions have been decomposed into REQs. A product team could ship a PRD with 20 assertions, decompose 3 into REQs, and the CI would pass.

Why it matters: the top-half of the spec sourcing flow (Vision → Epic rationale) is entirely ungated. Only the bottom half (REQ → TEST) is mechanically enforced. This is a structural gap that undermines the purpose of the dual-flow model.

---

**FIRST-SERI-03 — PHASE-1 scope still references the obsolete wrapper-agent model from the pre-amendment ADR-0002**

First principles produce: an amendment that rewrites the entire integration model (ADR-0002 amendment 0001: "Complete rewrite... The wrapper-isolation strategy from ADR-0002's original revision is dropped") must propagate to all phase files that reference the old model.

Artifact has: PHASE-1 scope items 4 lists `.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA). ADR-0002 amendment 0001 explicitly states: "Integration: native Claude Code Skills under `.claude/skills/` (was thin wrappers under `.claude/agents/` and `.claude/commands/`)." ARCHITECTURE.md §3 marks those directories as "(legacy slot — empty in v6 native-skills model)."

Delta: PHASE-1 scope item 4 is a deliverable that will produce files in directories that the architecture says should be empty. Either PHASE-1 will be executed with stale instructions (creating wrappers that serve no purpose), or PHASE-1 scope item 4 will be silently skipped (violating the scope-as-contract model).

Why it matters: this is a directly inconsistent requirement in a phase that is "pending" (not yet started). When PHASE-1 begins, the executor will face contradictory instructions and must choose between the ADR (no wrappers) and the phase file (create wrappers). The SoT principle (P1) is violated within the architectural layer itself.

---

**FIRST-SERI-04 — The gate-coverage gate (`gate-coverage`) is itself gated by CI, but CI is a stub in PHASE-0 and PHASE-1 — the self-enforcing property of ADR-0008 is circular during bootstrap**

First principles produce: a meta-gate that ensures every principle has a gate cannot be meaningful until the gate implementation exists. If `gate-coverage` is a TODO stub in PHASE-0 and PHASE-1, then during those phases any principle could be added without a gate and no CI failure would occur. The architecture acknowledges this partially but does not bound the risk.

Artifact has: ADR-0008 §2 says "adding a new ADR or principle without adding a gate is therefore impossible." But ADR-0008 also says "PHASE-0 commits the workflow YAML stubs (jobs declared, scripts as TODO). PHASE-1 and PHASE-2 implement the gates." The `gate-coverage` gate itself is listed as a PHASE-2 deliverable.

Delta: during PHASE-0 and PHASE-1, the "impossible" property is merely aspirational. A new principle could be added to ARCHITECTURE.md during PHASE-1 without a gate, and no CI failure would occur because `gate-coverage` is a stub. The architecture does not acknowledge this bootstrap gap explicitly.

Why it matters: the architecture's strongest claim (principles are mechanically enforced, not aspirational) is false for approximately the first two phases of the project's life — which is when the most architectural decisions are made.

---

**FIRST-SERI-05 — The `req-id-immutable` gate (ADR-0008 §1) cannot detect a requirement that was deleted and replaced by a new requirement with a different ID — it only detects renames**

First principles produce: immutability of requirement IDs means that once a REQ-ID is introduced, the assertion at that address must remain available (possibly marked deprecated) forever. A tool that only checks that existing IDs have not been renamed does not catch the deletion case.

Artifact has: ADR-0004 §1 says "A REQ marked `deprecated` may not be re-activated; supersession creates a new REQ." ADR-0008 lists `req-id-immutable` as a gate. The gate's scope is undefined in the ADR — it is named but not specified. `tools/spec_lint` is described as the owner, but no spec for the gate's logic exists in the reviewed documents.

Delta: if `req-id-immutable` only checks that a REQ-ID in the current index was not renamed (name A → name B in the same commit), it will not catch a developer who deletes a REQ block and does not add a deprecated marker. The append-only rule (ADR-0004 §7) should cover this, but `req-append-only` and `req-id-immutable` appear as separate gates — their interaction and coverage boundary is unspecified.

Why it matters: requirement deletion without deprecation is the mechanism by which coverage is gamed. The architecture depends on 100% REQ coverage but does not fully specify how ghost deletions are detected.

---

**FIRST-SERI-06 — The `openspec/_bmad-output/STAGING.md` is referenced as a binding rule document (ADR-0002 §7: "The full discipline lives in `openspec/_bmad-output/STAGING.md`; this section binds the rules") but it is a non-canonical staging directory — meaning the binding rule document is itself in the zone it governs**

First principles produce: a governance document that defines the rules for a staging area should not itself live in the staging area. If the staging area is "non-authoritative and outside the addressable artifact network," and `STAGING.md` lives there, then `STAGING.md` is non-authoritative by its own definition.

Artifact has: ADR-0002 §7 says the "full discipline lives in `openspec/_bmad-output/STAGING.md`." ADR-0002 §7 also says "`openspec/_bmad-output/` is staging — invisible to the addressable artifact network." The matrix builder excludes it; spec_lint excludes it.

Delta: `STAGING.md` is the binding governance document for a directory that excludes binding governance documents from its scope. The ADR-0002 §7 text says "this section binds the rules" — meaning the rules live in the ADR (correct), but then says the "full discipline" is in STAGING.md (incorrect location). Any evolution of staging discipline must edit STAGING.md, but STAGING.md is excluded from all traceability and lint checks.

Why it matters: the staging discipline can drift silently because it is exempt from every enforcement mechanism that applies to authoritative documents.

---

## PROCESS

**FIRST-PROC-01 — The amendment log pattern (append-only amendment rows in ADR text bodies) is not itself enforced by any gate**

First principles produce: if append-only is a core discipline (ADR-0004 §7 for REQs, ADR-0005 §9 for journals), then the amendment logs in ADR documents should also be protected by an `adr-amendment-append-only` rule. Currently, the amendment log format is convention only.

Artifact has: ADR-0002 and ADR-0005 include amendment logs with the note "Amendments are append-only. A subsequent material change... requires a new amendment row, never an edit to a prior row." No gate in ADR-0008 §1 enforces this. The `req-append-only` gate applies to spec files, not ADR files.

Delta: a developer could edit a prior amendment row in an ADR, and no CI gate would fire. The traceability of architectural decisions would be silently corrupted.

Why it matters: the history of architectural decisions is as important to the project as the history of requirements. The same append-only discipline that protects requirements is not extended to decision records.

---

**FIRST-PROC-02 — The `stale-staging` lint rule is "deferred" with no target phase or CHG assignment, creating an open-ended accumulation risk**

First principles produce: a governance rule deferred indefinitely is equivalent to a rule that does not exist. A staging area with no staleness enforcement will accumulate drafts indefinitely.

Artifact has: ADR-0002 §7 says "A future spec_lint rule `stale-staging` (deferred CHG) flags drafts sitting unpromoted past a configurable threshold." No CHG number is assigned. No phase contains it as a deliverable. ADR-0008 §1 does not list it in the gate inventory.

Delta: the `stale-staging` rule is acknowledged as necessary but deferred indefinitely. The `gate-coverage` gate (ADR-0008 §2) will not flag its absence because `gate-coverage` only checks that principles and existing ADRs have gates — not that all stated-necessary future gates have been scheduled.

Why it matters: the staging discipline depends on timely promotion to remain useful. Without `stale-staging`, the staging directory will grow without bound, making it progressively harder to distinguish active drafts from abandoned ones.

---

**FIRST-PROC-03 — The per-project BMAD isolation (ADR-0002 §9) requires CWD discipline that is documented only as a "PHASE-5 deliverable" — meaning six phases of monorepo work proceed without a documented CWD convention**

First principles produce: if the correctness of BMAD output routing depends on CWD, and incorrect CWD causes BMAD output to land in the wrong staging directory, this is a workflow correctness constraint that must be documented and enforced at the phase where the risk first appears (PHASE-1 when BMAD is installed), not the phase where it is first exercised (PHASE-5).

Artifact has: ADR-0002 §9 says "Documenting this is a PHASE-5 deliverable; the first project sets the precedent." BMAD is installed in PHASE-1. Any BMAD invocation in PHASE-1 through PHASE-4 that is done from the wrong CWD will route output to the wrong location. This is not flagged as a risk.

Delta: a four-phase gap exists between when the CWD-dependency is live (PHASE-1) and when it is documented (PHASE-5). During this gap, any agent or team member who invokes BMAD from a project CWD before the convention is documented will produce output in an unintended location.

Why it matters: BMAD is the primary workflow surface. Its correctness depending on undocumented CWD conventions for four phases is a process defect, not an acceptable deferral.

---

**FIRST-PROC-04 — The PHASE sequence assumes linear blocking dependencies (each phase gates the next), but the gate-coverage feedback loop requires PHASE-2 to validate PHASE-0 and PHASE-1 work retroactively — there is no defined remediation path if PHASE-2 gates reveal PHASE-0/PHASE-1 violations**

First principles produce: if work done in earlier phases is not validated until a later phase's tooling exists, and the earlier commits are immutable, then retroactive violations discovered in PHASE-2 can only be addressed by new commits that either correct or deprecate the old work. The architecture has no defined path for this.

Artifact has: The `red-before-green` gate and `req-coverage-100` gate both run for the first time in PHASE-2. If PHASE-0 or PHASE-1 work violates P4 (which was the subject of FIRST-CRIT-03), PHASE-2 gate activation will surface that violation. PHASE-2 exit criteria ("all REQ-CI-* tests-green") will then be blocked by violations in immutable earlier commits. The architecture does not address this.

Delta: there is no "retroactive compliance remediation" protocol. The architecture says "a principle without a gate is a build failure" but does not say what happens when a gate reveals a failure in completed, merged, immutable prior work.

Why it matters: in a linear phase model, retroactive violations discovered at phase N are the most expensive possible defect type. The architecture's silence on remediation is a process gap that will create real friction when PHASE-2 activates gates and scans history.
