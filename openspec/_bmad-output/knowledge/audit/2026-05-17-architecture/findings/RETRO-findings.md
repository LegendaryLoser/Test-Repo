# RETRO — retrospective (opus) — Wave 2

**Source transcript:** [`raw-transcripts/RETRO-agent-aeb34831758a76536.jsonl`](../raw-transcripts/RETRO-agent-aeb34831758a76536.jsonl)
**Sub-agent description:** `Retrospective review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `aeb34831758a76536`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-retrospective` skill via the Skill tool. Apply it as if PHASE-5 has just completed (in a hypothetical timeline where everything was implemented and shipped per the documents below). The retrospective looks back at the architecture artifact and identifies what worked, what didn't, and what should have been different from the start.

Documents under review (the artifact as it stands today, before any implementation):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5 (all under /home/user/Test-Repo/openspec/architecture/)

Retrospective framing:
> Imagine you have just exited PHASE-5. The first Apps Script project shipped. Look back at the architecture artifact (the 15 documents). What did the documents get RIGHT? What did they get WRONG? What was MISSING that you wish you had specified at PHASE-0? What was OVERSPECIFIED that you wish you had left flexible?

For the WRONG and MISSING categories, those are the findings. Use stable IDs prefix `RETRO-`.

REQUIRED OUTPUT:
- IDs prefix `RETRO-` (e.g. RETRO-CRIT-01, RETRO-SER-01, RETRO-PROC-01)
- Severity tiers CRITICAL / SERIOUS / PROCESS
- Minimum 12 findings (split between WRONG and MISSING categories)
- Each finding: what category (wrong/missing), specific file/section if applicable, what should have been done instead, why the rework cost would have been avoided if specified at PHASE-0
- 1500-2500 words
- Speak in completed past tense
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have read all 15 documents. Now producing the retrospective findings.

---

# Retrospective: Architecture Artifact Post-PHASE-5

Looking back from the far side of PHASE-5, the architectural artifact authored at PHASE-0 (ARCHITECTURE.md plus ADR-0001 through ADR-0008 plus PHASE-0 through PHASE-5) shaped the entire delivery arc. The five operating principles held up; vendored BMAD held up; the no-mock rule survived contact with reality. But several decisions cost real rework, and several gaps forced ADR amendments we should have written into the originals. The findings below catalog what the documents got WRONG and what was MISSING, in two severity tiers (CRITICAL and SERIOUS) plus a PROCESS tier for meta-level drift.

---

## CRITICAL findings (WRONG)

**RETRO-CRIT-01 — Single integer-counter REQ allocation produced a merge-time bottleneck (WRONG).**
ADR-0004 §1 specified that `REQ-<DOMAIN>-<NNNN>` IDs were allocated by "monotonic next-free scan against `openspec/specs/INDEX.yaml`." In PHASE-3 and PHASE-5, when two parallel CHGs both allocated REQ-LLM-NNNN and REQ-PROJ-NNNN respectively, every second PR collided at merge and required manual re-allocation plus a matrix rebuild. The artifact treated INDEX.yaml as if it were single-writer; in practice it was the most contested file in the repo. What should have been done instead: ADR-0004 should have specified per-branch ID reservation (allocator hands out a block of IDs per CHG at branch creation) or hash-prefixed IDs that cannot collide. Had this been specified at PHASE-0, we would have avoided the rebase-and-renumber churn that consumed a measurable fraction of PHASE-3 and PHASE-5 PRs and forced one mid-phase amendment to ADR-0004 that was never written.

**RETRO-CRIT-02 — The "no executable code under openspec/architecture/" rule contradicted the placeholder hook commands (WRONG).**
REQ-ARCH-0006 in ARCHITECTURE.md §10 prohibited executable code under `openspec/architecture/`. But PHASE-0 §3 item 9 required `.claude/settings.json` to declare hooks "pointing at placeholder commands that exit 0 with a TODO comment." Those commands had to live somewhere; they ended up under `tools/ci/placeholders/` with no specification at all, then were silently replaced in PHASE-2. The artifact never said where placeholders go, who owns their deprecation, or how their removal is gated. What should have been done instead: PHASE-0 should have specified a `tools/_placeholders/` location with explicit lifecycle and a `placeholder-removal-acknowledged` trailer required for any PR that turns a placeholder into a real implementation. The rework: every PHASE-2 PR that replaced a placeholder had to litigate this in review.

**RETRO-CRIT-03 — The hook chain's atomicity guarantees were overstated (WRONG).**
ADR-0005 §8 claimed "Crash mid-commit: Zero loss (git commit is atomic; rebuild fills missing journal entry)." This was wrong in two ways. First, `git commit` is atomic for the object but not for the index-plus-working-tree; a crash between `git add` and `git commit` left torn state that `rebuild.py` could not infer. Second, the `PostToolUse(Bash:git commit)` hook that pushed HEAD ran *after* the commit, so a crash between commit-and-push produced exactly the failure mode amendment 0001 to ADR-0005 later patched. What should have been done instead: ADR-0005 §8 should have been written conservatively from the start, with the push-invariant designed in rather than retrofitted via amendment 0001. The amendment exists because the original was wrong; specifying the conservative model at PHASE-0 would have avoided the incident on `claude/general-session-KXgas` that motivated the amendment.

**RETRO-CRIT-04 — The four-tier testing model had no story for security and performance (WRONG).**
ADR-0006 §1 enumerated `unit`, `integration`, `e2e`, `stochastic` as the only tiers. PHASE-3 shipped an Anthropic client with no specified place for secret-handling tests; PHASE-5 shipped an Apps Script project with no specified place for quota-exhaustion or latency-regression tests. Both ended up squatting in `tests/integration/` against the tier's stated intent. What should have been done instead: ADR-0006 §1 should have included `security` and `performance` tiers (or explicit non-tiers with sanctioned alternatives), with cost and gating policy. The rework: every PHASE-5 reviewer had to relitigate where security tests belonged, and one project shipped with no perf budget at all.

---

## SERIOUS findings (WRONG)

**RETRO-SER-01 — ADR-0002's "vendored 2.6 MB" assumption did not anticipate the diff blast radius (WRONG).**
ADR-0002 §4 said vendored storage is a "one-time cost; most repos vendor larger dependencies without trouble." In practice, BMAD v6.6.0 → v6.7.0 (a minor) produced a 3,400-line diff PR that no single reviewer could meaningfully audit, and `gh pr` rendering choked on it. The "deliberate substrate PR" was theoretically reviewable; in practice it was rubber-stamped. What should have been done instead: ADR-0002 should have specified a `substrate-diff-coverage` policy: vendored diffs above N lines require automated diff classification (added skills, removed skills, modified-skills) plus per-class sign-off, not a single human review. Avoided cost: PHASE-1 spent significant time arguing about a BMAD upgrade because the artifact gave no guidance on review depth.

**RETRO-SER-02 — Anti-aliasing thresholds were unspecified and untunable at PHASE-0 (WRONG).**
ADR-0004 §4 deferred the n-gram threshold to `tools/spec_lint/config.yaml` with "reviewed quarterly." The first PHASE-1 commit of the config picked an arbitrary threshold; PHASE-3's REQ-LLM-* set tripped the rule constantly because LLM-related requirements *naturally* share vocabulary ("the model", "the response", "the prompt"). What should have been done instead: ADR-0004 should have specified domain-scoped thresholds (REQ-LLM-* compared only against other REQ-LLM-*, not against REQ-AUTH-*), and should have specified an initial threshold derived from a calibration corpus. Avoided cost: most of PHASE-3's spec-lint failures were false positives that consumed reviewer attention.

**RETRO-SER-03 — The "stochastic tier" was the only place stochastic behavior was acknowledged (WRONG).**
ADR-0007 isolated stochastic discipline to `tests/stochastic/`. But by PHASE-5, the Apps Script project's E2E tests were *also* stochastic in practice — Google's Sheets API has propagation lag, the Execution API has tail latency, and `clasp push` is not deterministic. We needed property-based assertions in `tests/e2e/` and had no sanction for them. What should have been done instead: ADR-0007 should have generalized to "any tier whose backing system is stochastic uses statistical assertions" and ADR-0006 should have cross-referenced it for the e2e tier. Avoided cost: PHASE-5 reviewers debated whether retry-until-pass was permitted in e2e (ADR-0007 §2 banned it for stochastic; ADR-0006 did not mention it) and shipped at least one flaky test before resolving.

**RETRO-SER-04 — Phase ordering forced PHASE-3 (Anthropic client) before PHASE-4 (shared libs), inverting a real dependency (WRONG).**
ARCHITECTURE.md §11 ordered PHASE-3 (anthropic-client) before PHASE-4 (shared-ts/shared-py). The Anthropic client needed adapter declarations from `packages/shared-ts/adapters/` to satisfy ADR-0006 §3, so PHASE-3 §2 ended up declaring "Adapter declarations in `packages/shared-ts/adapters/`" as PHASE-3 scope, which is a PHASE-4 deliverable. The phase boundary leaked. What should have been done instead: either PHASE-4 should have come first (shared adapter declarations are foundational), or PHASE-3 and PHASE-4 should have been merged into a single phase with two exit gates. The rework: PHASE-4 had to relitigate adapter signatures that PHASE-3 had already shipped, with backwards-compatibility constraints we never intended.

**RETRO-SER-05 — REQ-ARCH-0008 declared hooks at PHASE-0 but the hook contract was unspecified (WRONG).**
REQ-ARCH-0008 required `.claude/settings.json` to declare all hooks from ADR-0005 §6 at PHASE-0. ADR-0005 §6 listed hook *events* and *purposes*, but not the input/output contract (what JSON shape each hook receives, what exit codes mean, how stdout interacts with the tool call). When PHASE-2 implemented the real hooks, half the hook signatures had to be invented from scratch and the settings.json declarations had to be revised. What should have been done instead: ADR-0005 §6 should have included a hook ABI table with exact JSON schemas. Avoided cost: the PHASE-0 declarations were placeholders for a contract that didn't exist; PHASE-2 had to design the contract and rewrite the declarations.

---

## CRITICAL findings (MISSING)

**RETRO-CRIT-05 — No specification for handling secrets, credentials, or `.env` files (MISSING).**
None of the 15 documents addressed how secrets (Anthropic API key, GAS service-account JSON, GitHub PATs for the merge hooks) are stored, rotated, injected into CI, or kept out of vendored content. PHASE-3 needed an `ANTHROPIC_API_KEY`; PHASE-5 needed a service-account JSON for the dev GAS deployment; the merge hooks needed write tokens. Each was solved ad-hoc, with the project-specific decision encoded in `.github/workflows/` rather than in an ADR. What should have been done instead: an ADR-0009 (Secrets and credential handling) drafted at PHASE-0 specifying secret stores, rotation cadence, the lint rule that bans secret-shaped strings, and the CI gate that verifies no secret entered the matrix or the journal. Avoided cost: PHASE-3 shipped with a hand-rolled secret-scanning shell script that was later replaced; PHASE-5 had one near-miss where a service-account JSON almost landed in `openspec/_bmad-output/`.

**RETRO-CRIT-06 — No specification for what happens when a phase's exit criteria fail in production (MISSING).**
ADR-0008 §3 (phase-exit gate) specified that a phase merge is *blocked* if exit criteria fail, but said nothing about what happens if a phase has merged and a regression later violates an earlier phase's exit criteria. In PHASE-5, a refactor in `packages/anthropic-client/` broke `cache-hit-regression` — a PHASE-3 exit criterion. The artifact had no rollback procedure, no "phase regression" status, and no specification of whether PHASE-5 work could continue while PHASE-3 was red. What should have been done instead: PHASE-5 or ADR-0008 should have specified a `phase-regression` state machine: which gates are blocking, which are advisory, what trailer authorizes a temporary regression, who signs off. Avoided cost: the regression was litigated in PR comments for several rounds before the team converged on an ad-hoc policy.

**RETRO-CRIT-07 — The artifact had no migration path for an ADR that was wrong (MISSING).**
ADR-0002 itself was rewritten under amendment 0001 because the original (wrapper-isolation) was based on outdated assumptions. The artifact specified amendments as append-only rows in an amendment log, but specified no protocol for *replacing* an ADR whose decision was wrong rather than incomplete. The amendment 0001 to ADR-0002 was effectively a complete rewrite documented as an amendment, which obscured the change. What should have been done instead: the artifact should have specified ADR supersession as the protocol for "the decision was wrong" (ADR-0002 superseded by ADR-0010, with `superseded_by` set), reserving amendments for "the decision is right but extends or clarifies." Avoided cost: PHASE-1 onlookers had to read ADR-0002 plus its amendment to know the current state; a superseded-by chain would have been clearer and is the convention the YAML frontmatter already anticipated (`supersedes` / `superseded_by` fields exist but went unused).

---

## SERIOUS findings (MISSING)

**RETRO-SER-06 — No specification of the developer's local environment (MISSING).**
None of the 15 documents specified the local toolchain: which Node version, which Python version, which `clasp` version, which OS family is supported. PHASE-3 contributors had to discover empirically that `packages/anthropic-client/` required Node 20 for the SDK; PHASE-5 contributors discovered `clasp` needed login via a service account flow that worked differently on macOS and Linux. What should have been done instead: an ADR-0010 (Local development environment) pinning runtime versions, declaring supported OS, and pinning the `clasp` flow. The CI environment was specified by implication via workflow YAML; the local environment was not specified at all.

**RETRO-SER-07 — No specification for how the architecture artifact itself is amended (MISSING).**
ARCHITECTURE.md §1 said the artifact is "frozen" and that modifications "require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate." But what triggers a Phase-0 re-gate was undefined. Does every commit to ARCHITECTURE.md re-run PHASE-0 tests? What if the change is purely typographical? What constitutes "material"? PHASE-1 and PHASE-2 each had at least one PR that touched ARCHITECTURE.md and stalled on whether re-gating was required. What should have been done instead: a section "How this artifact changes" with three categories (typo, clarification, material) and explicit gate behavior for each.

**RETRO-SER-08 — No specification for project sunset (MISSING).**
ADR-0001 §Consequences mentioned that "a project can be removed by deleting its `projects/<project>/` directory and marking its REQs deprecated; no other surface changes." But "marking REQs deprecated" is a non-trivial operation in ADR-0004's append-only model, and the artifact specified no playbook for sunsetting an Apps Script deployment (revoking the service account, archiving the spreadsheet, removing the CI matrix entry, cleaning up `tests/e2e/` artifacts). PHASE-5 shipped exactly one project; there is no second project yet, but the moment we sunset the first we will have to invent the procedure. What should have been done instead: a `PHASE-6` template or an ADR-0011 (Project lifecycle) specifying the sunset playbook.

**RETRO-SER-09 — The cost-budget gate had no specification of who pays or what budget (MISSING).**
ADR-0007 §4 introduced `@cost-budget tokens=<N>` annotations and a `cost-budget` CI gate, but specified neither a default budget nor who reviews budget changes. PHASE-3 stochastic tests landed with budgets pulled from thin air; PHASE-5 added more without any specified ceiling. The gate fires only on regression against an unstated baseline. What should have been done instead: ADR-0007 §4 should have specified a per-phase token budget ceiling and a sign-off authority for raising it. Avoided cost: PHASE-3's stochastic budget grew several-fold over the phase with no recorded approval.

**RETRO-SER-10 — No specification of how the matrix evolves across long-running branches (MISSING).**
ADR-0005 §2 specified that the matrix is regenerated and committed, and that CI fails if the committed matrix differs from the rebuilt matrix. This worked beautifully for short-lived PRs. For long-lived branches (the BMAD upgrade branch lived through several main-branch matrix changes), the merge-conflict resolution on `matrix.yaml` was a daily ritual. What should have been done instead: ADR-0005 §2 should have specified that `matrix.yaml` uses a "regenerate on merge" strategy with a merge-driver that always takes the rebuilt result, avoiding any human-resolved conflict. Avoided cost: every long-running branch ate matrix conflicts until PHASE-2 invented the merge driver after the fact.

---

## PROCESS findings

**RETRO-PROC-01 — The artifact assumed BMAD was workflow-ready before BMAD had been empirically exercised (PROCESS).**
ADR-0002's original (before amendment 0001) committed to a wrapper-isolation strategy based on assumptions about BMAD that turned out to be wrong. The artifact should have flagged ADR-0002 as `status: provisional` until PHASE-1 had actually installed BMAD. What should have been done instead: the artifact should have included a `status: provisional` lifecycle state for ADRs that depend on external systems not yet validated, and a "validation task" that flips them to `accepted`. Avoided cost: amendment 0001 to ADR-0002 is essentially the validation result, miscategorized as an amendment.

**RETRO-PROC-02 — Phase exit criteria were specified in terms of REQs that did not yet exist (PROCESS).**
PHASE-1 exit criteria referenced `REQ-SPEC-*` and PHASE-2 referenced `REQ-CI-*`, but neither REQ family was created at PHASE-0 — they were created by the phase that depended on them. This is structurally fine but operationally surprising: the first PHASE-1 PR had to allocate REQ-SPEC-0001 before any rule existed to allocate it. What should have been done instead: PHASE-0 should have created stub REQ files for each phase's planned REQ families, so allocation was a fill-in operation rather than a bootstrapping operation.

---

**Closing assessment.** The artifact's five-principle spine and CI-gate-as-enforcement design held up beautifully through PHASE-5 — those were the right calls. The wrongs and missings above clustered in three areas: (1) ID and matrix mechanics under concurrency, (2) the boundary between the architecture and the operational details (secrets, environments, lifecycles), and (3) the meta-protocol for changing the artifact itself. None of the findings invalidate the architecture; all of them describe rework that a more thorough PHASE-0 would have avoided. The single highest-leverage change a do-over would make is RETRO-CRIT-07 — specifying a clean ADR supersession protocol — because it would have given us a clean way to encode the lessons from RETRO-CRIT-01 through RETRO-SER-10 as we discovered them, rather than accumulating them as amendments and tribal knowledge.
