# SALLY — persona-sally-ux (sonnet) — Wave 3

**Source transcript:** [`raw-transcripts/SALLY-agent-a8d1b481c259c823c.jsonl`](../raw-transcripts/SALLY-agent-a8d1b481c259c823c.jsonl)
**Sub-agent description:** `Sally UX persona solo`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a8d1b481c259c823c`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-agent-ux-designer` skill via the Skill tool to load Sally, the BMAD UX designer persona. Then, AS Sally, review the architecture artifact from a user-experience perspective.

This is NOT an interactive conversation. Load the persona, then produce Sally's report as a single output.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Sally's perspective: the users of this system include (a) human developers, (b) AI agents, (c) future maintainers. All three are user populations whose experience the architecture shapes.

Focus areas:
- What does a developer experience when a gate rejects their commit? Is the diagnostic actionable?
- What does an AI agent see when it must resume mid-session per ADR-0005 §9? Is the resume output legible?
- What does a contributor see when they want to allocate a REQ-ID? What's the friction?
- Onboarding journey: what's the first hour like for a new developer reading these docs?
- What error states does the architecture have no UX for?
- Where does the architecture assume technical fluency it shouldn't?
- What feedback loops are slow, opaque, or missing entirely?
- The session-resume promise ("zero human re-briefing") — what does its UX actually look like?
- What's the UX when a phase-exit gate fails for reasons the contributor cannot fix without an ADR amendment?

REQUIRED OUTPUT:
- Stable IDs: prefix `SALLY-` (e.g. SALLY-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Speak in first-person as Sally
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have read all 15 required documents. As Sally, I will deliver the UX review.

---

**SALLY'S UX REVIEW — Architecture Artifacts**
**User Populations: Human Developers / AI Agents / Future Maintainers**
**Review date: 2026-05-17**

---

I've spent time inside this architecture the way a new developer would — entering cold, following the breadcrumb trail from CLAUDE.md through ARCHITECTURE.md and all eight ADRs to all six phase files. What follows is my honest account of what I found from a human-centered design standpoint. The system has genuine structural integrity; it also has real gaps between the experience it promises and the experience it delivers.

---

### CRITICAL FINDINGS

**SALLY-CRIT-01 — Gate rejection messages are design-free**

When `commit-trailers-valid` rejects a commit, the developer gets whatever the hook script outputs — and the architecture never specifies what that output looks like. ADR-0005 §3 and ADR-0008 §5 describe the rule (four trailers required) but say nothing about the diagnostic message a rejected user actually sees. There is no requirement for the hook to name the missing trailer, provide an example of a valid one, or link to documentation. A developer who has never seen the trailer format before gets a bare rejection with no recovery path described in any of these documents. For an AI agent resuming mid-session, this is potentially unrecoverable without human intervention — the exact failure mode the architecture claims to eliminate. A gate that doesn't explain itself is a gate that generates tickets.

**SALLY-CRIT-02 — The "zero human re-briefing" promise is unverifiable until PHASE-2**

ARCHITECTURE.md §8 and ADR-0005 §8 both assert that session resume requires zero human re-briefing. This is the system's highest-value UX promise. But the `resume.py` hook that actually delivers this experience is a PHASE-0 placeholder — it exits 0 with a TODO comment. That means from now until PHASE-2 ships (potentially months away, since phases are sequential and cannot be skipped), every session resume relies entirely on the developer reading STATUS.md manually and correctly interpreting it. The claim is in the architecture; the implementation is deferred; the gap is invisible to anyone reading these documents for the first time. The promise and the delivery are in different phases with no warning label on the promise.

**SALLY-CRIT-03 — Phase-exit gate failure has no escalation path for the contributor who cannot fix it**

ADR-0008 §3 specifies that the `phase-exit` gate blocks merges when exit REQs are not all `tests-green`. There is no described path for the case where a REQ cannot be made green without an ADR amendment — for example, a stochastic test that statistically fails above the budget threshold because the model changed. The contributor's options are: (a) figure out independently that an ADR amendment is the required path, (b) try --no-verify (explicitly forbidden), or (c) escalate to human review (not described anywhere). The architecture is precise about what blocks the merge but silent about what a trapped contributor does next. This is a dead end in the user journey, and it will happen.

**SALLY-CRIT-04 — REQ-ID allocation has hidden friction that will cause errors**

ADR-0004 §1 says: "Identifier allocation is by `tools/spec_lint allocate <domain>` against `openspec/specs/INDEX.yaml`. Hand-allocation is permitted but checked." This is a two-sentence description of a workflow that a first-time contributor must execute correctly or produce a lintable defect. The DOMAIN format rules (uppercase alphanumeric, ≤ 12 chars), the monotonic counter scope, the tool invocation — none of this is surfaced in CLAUDE.md or ARCHITECTURE.md in a way a new person can act on immediately. The tool doesn't exist yet (PHASE-1 deliverable), so currently hand-allocation is the only path, and the only guidance for that path is "it's permitted but checked." What gets checked? By what? When? A contributor working during PHASE-0 has no actionable answer.

**SALLY-CRIT-05 — The AI agent resume output format is unspecified**

ADR-0005 §6 says the `SessionStart` hook will "Print active phase, in-flight task, last commit, next action." That is the entire specification of the resume experience for an AI agent. Four fields. No format. No example. No ordering. No handling of the case where there is no in-flight task, or where the journal is empty, or where the last commit was a checkpoint. An AI agent parsing unstructured text from a script it has never seen before — with no schema — is asked to reconstruct context from whatever `resume.py` decides to print. This is not a UX; it is a hope.

---

### SERIOUS FINDINGS

**SALLY-SERIOUS-06 — Onboarding entry point is CLAUDE.md, but CLAUDE.md sends you to STATUS.md first**

CLAUDE.md's "How to start any session" tells a new developer to read STATUS.md first. STATUS.md is described as the "authoritative session-resume document" — but it is maintained by hand and its format is nowhere specified in the 15 documents I reviewed. A new developer following the prescribed path hits an unspecified document as their first substantive interaction with the system. The document may or may not exist, may or may not have the fields described, and contains no schema that tooling validates. The onboarding journey's first step lands on an artifact with no quality guarantee.

**SALLY-SERIOUS-07 — The "paper" is a ghost reference throughout the architecture**

ADR-0004's entire rationale rests on "a published result on transformer associative memory" referred to as "the paper." It is cited multiple times across ADR-0004 and ARCHITECTURE.md §2 as the authoritative basis for the anti-aliasing rules, the n-gram thresholds, and the prohibition on semantic search. The paper has no citation, no DOI, no URL, no title, no authors. A future maintainer who needs to revisit the threshold — or a new team member trying to understand why near-duplicate specs are banned — has no way to find the source. The architecture's most intellectually load-bearing reference is invisible. This is a single source of truth violation inside the document that defines single source of truth.

**SALLY-SERIOUS-08 — The BMAD staging/promotion workflow has no user-facing checklist**

ADR-0002 §7 defines the promotion protocol for moving BMAD drafts from `openspec/_bmad-output/` to canonical homes. It specifies that promotion is a `docs`-type TASK under an explicit CHG, that the matrix records the promotion commit, and that spec_lint validates the promoted artifact. None of this is surfaced as a step-by-step action a developer can follow. What frontmatter does a promoted spec need? In what order do you create the TASK, move the file, commit, and update the matrix? The rules exist; the workflow for executing them does not.

**SALLY-SERIOUS-09 — `Checkpoint: true` exemptions are invisible**

ADR-0008 §6 says: "The `Checkpoint: true` trailer is the only sanctioned partial-bypass and applies to a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`." That file does not exist until PHASE-2. During PHASE-0 and PHASE-1, every checkpoint commit fires against placeholder hooks, so the exemptions are moot — but a developer reading the architecture cannot know which gates are skipped and which are enforced for checkpoint commits. The authoritative list is in a file that doesn't exist yet, referenced from a document the developer is reading now.

**SALLY-SERIOUS-10 — The four-layer BMAD config merge is described but not diagrammed or illustrated**

ADR-0002 §9 describes the 4-layer config merge for per-project BMAD output isolation. The mechanic is correct and important, but it is written as a numbered list of file paths. A developer setting up a second project — referencing only these documents — must mentally simulate how the merge works to know which config file to edit for their case. There is no example showing what a repo-level config looks like, what a project-level override looks like, and what the merged result looks like. The cognitive burden is real; the surface is fragile; and the only test ("verify the BMAD resolver picks up the override") doesn't land until PHASE-5.

**SALLY-SERIOUS-11 — Red-first enforcement has an unreachable error state for the bulk-green case**

ADR-0006 §4 says: "Bulk green-starts ... require a `Bootstrap: <reason>` trailer and an approving review; CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." `N` is not defined. The trailer format is given but not validated anywhere until PHASE-2's gate implementation. A developer who legitimately needs to bootstrap tests during PHASE-0 has no way to know what value of N triggers the gate, and the only documentation of the process is one sentence. The approval path ("an approving review") is not linked to any PR process.

**SALLY-SERIOUS-12 — The `prose-xref-banned` lint rule creates a false negative for humans reading the docs**

ADR-0004 §2 bans prose references like "the auth spec" or "the original ADR" as lintable defects. The ARCHITECTURE.md and the ADRs themselves use prose references extensively in their rationale sections. ARCHITECTURE.md §2 says "the paper" repeatedly. ADR-0004 discusses "the paper" and "this repository." These are acceptable in prose documentation — but the rule creates a real confusion point: a developer who reads "prose references are a lintable defect" and then reads the very ADR that states this rule, sees prose references used freely. The scope of the rule (spec files under `openspec/specs/`) versus prose documentation is never stated explicitly. The distinction is implied; it is not written.

---

### PROCESS FINDINGS

**SALLY-PROCESS-13 — The phase sequencing is strict but the wait time is not communicated**

The six phases are sequential, each gated on the prior phase's full `tests-green`. From a new developer's standpoint, there is no estimate of how long a phase takes, no concept of "in-progress work for phase N" existing alongside phase N-1, and no signal about how long they might wait before the infrastructure they need is available. PHASE-5 entry requires a product PR chain (vision, brief, PRD, Epic, Story) plus four prior phases of infrastructure — but the product work can begin in parallel. That parallelism is never mentioned. A contributor wanting to write product specs is given no signal that they can start before PHASE-4 exits.

**SALLY-PROCESS-14 — The `anti-aliasing` threshold is pinned but its review cadence is buried**

ADR-0004 §4 says the n-gram threshold "is reviewed quarterly (a `gate`-type task)." There is no task, no TASK-ID, no calendar integration, no owner, and no process for what happens when the quarterly review concludes the threshold needs to change. A future maintainer six months in will either forget this exists or not know where to find it. The review cadence is good policy; its operational surface is absent.

**SALLY-PROCESS-15 — The `stale-staging` gate is deferred with no conditions for activation**

ADR-0002 §7 mentions a future `stale-staging` spec_lint rule that will flag drafts sitting unpromoted past a configurable threshold, then marks it as "a deferred CHG." There is no CHG-ID, no phase, no owner, no activation criterion. As a result, the `openspec/_bmad-output/` directory can accumulate indefinitely unpromoted drafts without any CI signal. The architecture acknowledges the problem and defers the solution with no visibility into when or why it will land. This is a known UX gap that has been explicitly documented and then left open-ended.

**SALLY-PROCESS-16 — The CWD-scoping requirement for BMAD project sessions is undocumented until PHASE-5**

ADR-0002 §9 says: "sessions working on a specific project must run with CWD set to `projects/<name>/` for BMAD to pick up per-project overrides" and marks documenting this as "a PHASE-5 deliverable." This is a runtime behavior constraint that affects every developer who works on any project in the repo — but it is invisible to those developers until the first project (PHASE-5) sets the precedent. Any developer running BMAD skills from the repo root while intending to work on a project will silently route output to the wrong directory, with no warning and no gate to catch it before PHASE-5.

**SALLY-PROCESS-17 — The audit CLI is specified but its output format is unspecified**

ADR-0005 §9 describes `tools/trace/audit.py <id>` with five invocation patterns and their expected semantic answers. What the output actually looks like — machine-readable JSON, human-readable text, structured YAML — is never defined. For an AI agent that might need to parse `audit EPIC-NNNN` output to make a decision about epic coverage, the output format is the entire interface. For a human developer, a format that's hard to scan is friction. The spec describes what questions the tool answers, not what a correct answer looks like.

---

**Summary by tier:**

| Tier | Count | Core theme |
|---|---|---|
| CRITICAL | 5 | Missing diagnostic feedback, undelivered promises, trapped user states |
| SERIOUS | 7 | Invisible dependencies, missing examples, scope ambiguity |
| PROCESS | 5 | Deferred work with no activation signals, undocumented operational cadences |

The architecture is rigorous and internally consistent. Its primary UX deficit is that it is written for the system designer, not the system user. Every principle has a gate; almost no gate has a human-legible failure message. Every workflow has rules; almost no workflow has a step-by-step path a person can follow without inferring from the rules. The session-resume promise is the centerpiece experience — and it is not delivered until PHASE-2, with no warning label on the promise itself.
