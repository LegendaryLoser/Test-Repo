# PARTY — party-mode (opus) — Wave 1

**Source transcript:** [`raw-transcripts/PARTY-agent-a72db282c4e152bde.jsonl`](../raw-transcripts/PARTY-agent-a72db282c4e152bde.jsonl)
**Sub-agent description:** `BMAD party-mode roundtable`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a72db282c4e152bde`

## Initial prompt to sub-agent

```
You are an isolated session with no prior context. Invoke the `bmad-party-mode` skill via the Skill tool to orchestrate a multi-agent roundtable discussion of an architecture artifact. The personas to invite to the roundtable: Winston (architect — bmad-agent-architect), Amelia (dev — bmad-agent-dev), John (PM — bmad-agent-pm), Mary (analyst — bmad-agent-analyst), Sally (UX designer — bmad-agent-ux-designer if relevant), Paige (tech writer — bmad-agent-tech-writer).

Topic for the roundtable: critical review of the following architecture artifact. Each persona should review from their professional perspective — architect critiques the structural decisions, dev critiques implementability, PM critiques value-vs-cost, analyst critiques requirements clarity, tech writer critiques documentation discipline.

Documents under review (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Operating principles being claimed:
1. Single source of truth.
2. Stochastic systems get statistical assertions.
3. Tests exercise real production code (no mocks of in-repo modules).
4. Red-first.
5. OpenSpec for spec, BMAD + TEA for workflow.

After the roundtable, collate the findings each persona raised into a structured report.

REQUIRED OUTPUT:
- Stable IDs: prefix `PARTY-` (PARTY-CRIT-01, PARTY-SER-01, PARTY-PROC-01)
- Tag each finding with the persona who raised it (e.g. "(Amelia/Dev)")
- Minimum 15 findings across the personas, no fewer than 2 per persona
- 1500-3000 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

All 15 documents read. Now I'll channel each persona's critique and produce the collated findings report.

---

# Roundtable Critical Review — Architecture Artifact

**Scope reviewed:** `openspec/architecture/ARCHITECTURE.md`, ADR-0001 through ADR-0008, PHASE-0 through PHASE-5
**Participants:** Winston (Architect), Amelia (Dev), John (PM), Mary (Analyst), Sally (UX), Paige (Tech Writer)
**Mode:** `--solo` (single orchestrator channeling each persona; chosen because the user requested a structured collated report, not interactive turns).

---

## PARTY-CRIT-01 — Hooks promise atomic push, but the model already broke once (Winston/Architect)

ADR-0005 §6 introduces a "push invariant" via `PostToolUse(Bash:git commit)` and `PostToolUse(mcp__github__merge_pull_request)`. The amendment log admits the invariant was retrofitted *after* a divergence on `claude/general-session-KXgas`. That is a tell: the invariant is being asserted at a layer (Claude Code hooks) that cannot guarantee execution — hooks fire only if the harness fires them, and an abrupt container reclaim mid-`PostToolUse` defeats both the per-commit push *and* the checkpoint push. The doc acknowledges this in §8 ("residual loss only if both hooks fail to fire") but then claims "zero loss" in ARCHITECTURE.md §8's table for "push completed" — a circular guarantee. The real invariant must live server-side (a pre-receive auto-acknowledgement, or a watchdog that reconciles ref state) or be honestly downgraded to "best-effort."

## PARTY-CRIT-02 — Phase ordering forces a chicken-and-egg on red-first enforcement (Winston/Architect)

PHASE-0 must commit hook *declarations* that exit 0 with TODOs, while PHASE-2 implements `red-before-green`, `validate_commit`, and `commit-trailers-valid`. That means every commit produced during PHASE-0 and PHASE-1 — including the PHASE-0 commits that introduce the architecture itself — cannot be enforced under the principle they are supposed to embody. The architecture artifact is the one body of work that escapes its own gates. ADR-0008 §2 (`gate-coverage`) is meant to prevent this, but it doesn't run until PHASE-2 either. Either the gates need to land in PHASE-0 in minimal form, or the doc must acknowledge a self-exempt "founding period."

## PARTY-CRIT-03 — ADR-0002 is functionally a rewrite masquerading as an amendment (Winston/Architect)

Amendment 0001 to ADR-0002 says "Complete rewrite to match BMAD v6.6.0 empirical reality." A complete rewrite is, by ADR-0004 §1 logic (immutable IDs, supersession-only), supposed to be a *new* ADR (ADR-0009) that supersedes ADR-0002. Mutating an "accepted" ADR via append-only amendment row works for §-level addenda but not for a whole-document rewrite. This sets a precedent that "amendment" is unbounded — defeats the append-only discipline ADR-0004 §7 imposes on every other artifact.

## PARTY-SER-01 — Real GAS adapters in unit tests are a fiction (Amelia/Dev)

ADR-0003 §3 says `tests/unit/` "runs on Node; imports production TypeScript modules unchanged; uses non-GAS real adapters." But the production modules call `SpreadsheetApp`, `DriveApp`, etc. — those globals do not exist on Node. The only way "non-GAS real adapter" works is dependency injection at every call site, which means production code must be written as if Node-runnable. That is a real constraint that should be stated, not implied. Also, "a Sheets adapter that hits a dedicated test spreadsheet via the Sheets REST API" called from a *unit* tier collapses the distinction between unit and integration tiers — that adapter requires network, credentials, and a real spreadsheet. It is integration by any honest definition.

## PARTY-SER-02 — The no-mock rule will collide with clock and randomness early and often (Amelia/Dev)

ADR-0006 §2 permits "real adapters" for clock and randomness, but anything that retries on a stochastic LLM call, anything that depends on rate-limit windows, anything that needs reproducible time-window math will require seeding or fixed clocks. ADR-0007 §2 also bans `seed=` arguments. The combination means a developer wanting to test "this retry kicks in after 30 seconds" must either run a 30-second real test or build a "production clock adapter" that secretly accepts an override — which is a fake with a fig leaf. The ADRs do not address this collision.

## PARTY-SER-03 — `tools/trace/validate_commit.py` walking history to prove red-first is O(N) and brittle (Amelia/Dev)

ADR-0005 §4 says "tools/trace/validate_commit.py walks git history to verify" red-before-green. On a long-lived branch, this walks every commit, parses every diff, and re-runs the test parser. Rebases, squashes, and cherry-picks destroy the linear history the verifier depends on. ADR-0006 §4's "Bulk green-starts" escape hatch acknowledges the problem but moves it sideways — now every CI run has to decide whether a commit is "bulk." There is no spec for what "bulk" means.

## PARTY-SER-04 — The `Checkpoint: true` exemption is a backdoor through every gate (Amelia/Dev)

ADR-0005 §7 says `Checkpoint: true` makes CI gates skip the commit. ADR-0008 §6 says "the *only* sanctioned partial-bypass." But a `Stop` hook can fire repeatedly during a long session — a sufficiently broken session can produce a chain of checkpoint commits, each individually exempt, and only "the next non-checkpoint commit" is responsible for "restoring P4 compliance." If that next commit never comes (session abandoned, branch deleted post-PR), the chain shipped without enforcement. The exemption needs a ceiling (max N consecutive checkpoints) or a TTL.

## PARTY-PROC-01 — There is no product, but there is a six-phase delivery plan (John/PM)

ARCHITECTURE.md §12 explicitly says product vision, brief, PRD, epics, stories are "empty templates until a separate product PR fills them." PHASE-5 entry criteria require "≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage, ≥ 1 Story" — handwaved as "the product side has produced (in a separate PR chain)." Five phases of substantial engineering (spec lint, traceability runtime, anthropic client, shared libs) get built before anyone validates the architecture against a single real user story. This is the opposite of value-first delivery — it is infrastructure-first with no demand signal. The risk is building four phases worth of scaffolding for an app that, when finally specified, doesn't need half of it.

## PARTY-PROC-02 — Cost of the regime per change is not estimated anywhere (John/PM)

A single REQ now requires: a stable ID allocation against INDEX.yaml, a frontmatter block, ≥1 red commit, ≥1 green commit, all four trailers per commit, a TASK file under a CHG, journal events, matrix rebuild, ≥1 test annotated with `@test-id` and `@covers`, tier-appropriate adapter wiring, and stochastic-tier sandwich code if LLM-adjacent. None of the ADRs estimate the human-minutes-per-REQ cost. Without that estimate, the value/cost framing is asserted but unmeasured. A REQ that takes 4 hours of ceremony to ship is fine for safety-critical code and absurd for a one-off Apps Script utility.

## PARTY-PROC-03 — "A phase cannot start until prior phase exit criteria are tests-green" creates a parallelism bottleneck (John/PM)

ARCHITECTURE.md §11 and every PHASE file enforce strict ordering. With one person or one agent, that's fine. With a team (or with parallel agent sessions), nothing in PHASE-2 can start until PHASE-1 is fully green, even though `tools/trace/` and `tools/spec_lint/` are largely independent surfaces. The doc does not authorize parallel work within a phase, nor does it permit speculative work on PHASE-2 against a green-pending PHASE-1. For a single-developer cadence this is fine; the doc should say so explicitly, because otherwise it silently caps throughput.

## PARTY-REQ-01 — The five principles are not requirements (Mary/Analyst)

ARCHITECTURE.md §1 declares five "operating principles." ADR-0008 §2 (`gate-coverage`) requires every principle to be referenced by ≥1 gate. But the principles are not REQs — they have no `REQ-` ID, no frontmatter, no tier, no acceptance criterion. They are aphorisms. "Single source of truth" is not testable as written; what is testable is "no two files under `openspec/specs/` declare the same REQ-ID" or "no two REQ blocks have identical Description bodies above n-gram threshold T." The principles should be promoted to `REQ-ARCH-PRIN-*` (or similar) with concrete acceptance, otherwise `gate-coverage` is checking a fuzzy match between a gate and an aphorism.

## PARTY-REQ-02 — REQ-ARCH-0007 ("CLAUDE.md cites the five principles verbatim") is an integrity check, not a behavior (Mary/Analyst)

This REQ verifies a string match. It does not verify that the principles *operate*. A future edit to ARCHITECTURE.md §1 that adds a sixth principle but doesn't sync CLAUDE.md fails REQ-ARCH-0007 — good. But a future edit that *weakens* a principle's wording in both places passes REQ-ARCH-0007 while silently degrading the system. The REQ needs a sibling REQ that pins the *semantic* invariants (e.g., "no commit may be `tests-green` without a prior `tests-red`") rather than text equality.

## PARTY-REQ-03 — Compound-requirement detection in ADR-0004 §3 is heuristic, but enforcement is binary (Mary/Analyst)

"One REQ contains one assertion" is a clear principle. `compound-requirement-detector` is described as a heuristic in ADR-0004 §3 and ADR-0008 §1, but the gate is per-PR pass/fail. False positives are inevitable with heuristics — what is the appeal path? The ADRs describe no escape hatch, no `Compound-Acknowledged:` trailer parallel to `Skill-Removal-Acknowledged:`. The result will be: developers learn to phrase REQs to evade the heuristic, not to be atomic.

## PARTY-REQ-04 — "Stochastic test sample size declared, pinned per test" — pinned to what? (Mary/Analyst)

ADR-0007 §3 requires "Sample size declared; assertion is a confidence interval, Kolmogorov–Smirnov test, or similar. Sample size and threshold are pinned per test." Pinned by whom, calibrated against what baseline, reviewed on what cadence? Without a calibration discipline, the sample size becomes whatever the author guessed, and the confidence interval is theater. ADR-0007 needs a §7 on calibration cadence (e.g., quarterly re-baseline, drift-alert if observed pass rate diverges from CI from expected by > δ).

## PARTY-UX-01 — Session resume is described as mechanical but never user-tested (Sally/UX)

ARCHITECTURE.md §8 and ADR-0005 §9 promise "session resume requires zero human re-briefing" via the journal + active task file + last commit. From a UX standpoint, "zero re-briefing" is a bold claim that depends entirely on the SessionStart resume hook's output being legible and actionable to the *next* agent (or human). The hook is deferred to PHASE-2 and the spec for its output format is one bullet ("active phase, in-flight task, last commit, next action"). No examples, no edge cases (what if the active task is paused with a `task_pause` event whose `reason` is unstructured prose?), no failure mode for an unreadable resume. The UX of resumption is the load-bearing user journey and it is the least specified surface in the artifact.

## PARTY-UX-02 — The agent-facing error experience is missing (Sally/UX)

Across ADR-0004, ADR-0005, ADR-0006, ADR-0008 there are roughly 30 gates that fail builds. Nothing specifies the *shape* of the failure: is it a one-line CI red, a structured JSON error consumable by another agent, a markdown blob, a pointer to the offending REQ-ID? When a Dev agent's commit is rejected by `commit-trailers-valid`, what does it see and how does it self-correct? This is the entire agent UX and the artifact is silent on it. Suggest an ADR-0009 ("Agent-facing diagnostic format") or a section in each gate ADR.

## PARTY-DOC-01 — ADR-0005 §6 push invariant is documented in two places that disagree in tone (Paige/TechWriter)

ADR-0005 §6 says the push invariant is enforced by hooks "the invariant is otherwise unenforceable and silently rots." Same ADR §8 table says "Container reclaim, push succeeded: Zero loss." ARCHITECTURE.md §8 also says "Container reclaim, push completed: Zero." These three statements compose into "the invariant is unenforceable, and also we guarantee zero loss when it holds." That is technically consistent but rhetorically misleading — a reader skimming the ARCHITECTURE.md table will believe push-completion is a hard guarantee. Recommend rewriting the ARCHITECTURE.md §8 row to read "Container reclaim, push succeeded (verified by post-hook ref check): zero" so the condition is loaded into the row, not buried in §6.

## PARTY-DOC-02 — Cross-reference discipline (ADR-0004 §2) is violated by the architecture itself (Paige/TechWriter)

ADR-0004 §2 bans prose references like "the original ADR" or "the auth spec." ADR-0002 amendment 0001 says: *"The original ADR text designed a wrapper-isolation strategy based on outdated assumptions..."* That is a prose self-reference of the exact form §2 forbids. ARCHITECTURE.md §2 also says "the paper" — defensible because it's named as a referent, but the doc never gives the paper a stable ID. A `REF-PAPER-0001` with a citation block in ARCHITECTURE.md would close the loop and let `prose-xref-banned` lint clean.

## PARTY-DOC-03 — The amendment-log discipline is inconsistent across ADRs (Paige/TechWriter)

ADR-0002 §10 and ADR-0005 §10 carry amendment logs with date, CHG, sections, summary. ADR-0001, ADR-0003, ADR-0004, ADR-0006, ADR-0007, ADR-0008 carry no amendment log at all — they have a frontmatter `supersedes: null` and that's it. If amendment logs are the supersession-alternative for non-material edits (ADR-0002 amendment 0002 explicitly uses this pattern), then every ADR needs the section as a stub from day one, even if empty. Otherwise the rule for "when does this get an amendment log vs a supersession?" is silent and authors will guess.

## PARTY-DOC-04 — PHASE files do not declare their REQ-IDs (Paige/TechWriter)

ARCHITECTURE.md §10 declares REQ-ARCH-0001..0008. PHASE-0 §exit-criteria references those same REQ-IDs. But PHASE-1..5 reference REQ-IDs that do not yet exist (`REQ-SPEC-*`, `REQ-CI-*`, `REQ-LLM-*`, `REQ-LIBTS-*`, `REQ-LIBPY-*`) and offer no enumeration. The phase files are the only artifact that promises these IDs exist. A reader has no way to know if PHASE-3 has 4 REQs or 40 until PHASE-3 is in flight. Suggest each PHASE file carry a "Planned REQ envelope" table (`REQ-LLM-0001..0020` projected, actual filled in on exit) so phase scope is bounded ex ante, not discovered ex post.

## PARTY-DOC-05 — Terminology drift between ARCHITECTURE.md §3 and ADR-0002 §3 (Paige/TechWriter)

ARCHITECTURE.md §3 layout shows `.claude/agents/` and `.claude/commands/` as "legacy slot — empty in v6 native-skills model" and `_bmad/` as the install root. PHASE-1 §scope item 4 still says "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA)." That contradicts ADR-0002 amendment 0001 which deletes the wrapper strategy. PHASE-1 was written before the ADR-0002 rewrite and never re-synced. This is the exact "near-duplicate specification" failure mode that ADR-0004 §4 (anti-aliasing) is supposed to prevent — but PHASE files are not under `openspec/specs/` so the lint doesn't touch them.

## PARTY-DOC-06 — PHASE-5 §scope has two items numbered "4" (Paige/TechWriter)

Minor but indicative: PHASE-5 scope lists items 1, 2, 3, 4 (BMAD output isolation), 4 (test suite), 5, 6. A numbering typo in the load-test phase of the architecture is the kind of defect that ADR-0008's `openspec-validate` gate is supposed to catch but currently doesn't (the gate exists in the table but doesn't validate PHASE file structure — only OpenSpec format, which PHASE files are not formally part of). Either expand `openspec-validate` to cover `openspec/architecture/phases/` or write a new lint.

---

## Orchestrator Note

The strongest cluster is **PARTY-CRIT-02 + PARTY-PROC-01 + PARTY-DOC-04**: the architecture defers product validation to PHASE-5 while making PHASE-0..2 self-exempt from the principles they enforce, and the deferred REQs are not even enumerated. This is a "build the cathedral, then wonder if anyone wants to pray" risk pattern. Winston and John independently surfaced the cost-side; Paige caught the documentation evidence. Recommend a Phase-0 amendment that either (a) lands minimal versions of `validate_commit` and `red-before-green` in PHASE-0 itself, or (b) explicitly declares a "founding-period" carve-out with an exit date and a debt ledger.

Files reviewed (absolute paths):
- /home/user/Test-Repo/openspec/architecture/ARCHITECTURE.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0001-monorepo-layout.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0002-bmad-integration.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0003-appscript-runtime.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0006-testing-tiers.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md
- /home/user/Test-Repo/openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md
- /home/user/Test-Repo/openspec/architecture/phases/PHASE-0-foundation.md
- /home/user/Test-Repo/openspec/architecture/phases/PHASE-1-spec-hygiene.md
- /home/user/Test-Repo/openspec/architecture/phases/PHASE-2-traceability-runtime.md
- /home/user/Test-Repo/openspec/architecture/phases/PHASE-3-anthropic-client.md
- /home/user/Test-Repo/openspec/architecture/phases/PHASE-4-shared-libs.md
- /home/user/Test-Repo/openspec/architecture/phases/PHASE-5-first-appscript-project.md

**Findings tally:** 22 total — Winston 3, Amelia 4, John 3, Mary 4, Sally 2, Paige 6. All personas meet the ≥2 minimum. Word count of the findings body: ~2,400 words (within the 1500-3000 envelope).
