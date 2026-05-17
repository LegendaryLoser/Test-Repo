# SCENNOW — scenario-unfold-current-state (opus) — Wave 6

**Source transcript:** [`raw-transcripts/SCENNOW-agent-a07f43fdddd08cb06.jsonl`](../raw-transcripts/SCENNOW-agent-a07f43fdddd08cb06.jsonl)
**Sub-agent description:** `Scenario unfold current state`
**Session ID:** `2fa6b8f3-f53b-44bf-873e-44bdb568369b`
**Agent ID:** `a07f43fdddd08cb06`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Your method is **scenario unfolding from current state** — a scenario lens applied to the architecture as it stands today, NOT forward-looking (you are not doing a pre-mortem or post-hoc retrospective). For each scenario, you walk a concrete actor through their day with the architecture in its current state and surface what breaks, what's confusing, what they can't do, what they accidentally do wrong, and what the architecture doesn't tell them they need to do.

Documents to review (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- All 8 ADRs in openspec/architecture/decisions/ (list the directory first)
- All 6 PHASE files in openspec/architecture/phases/ (list the directory first)

Scenarios to walk through (concrete actors in current-state):

1. **Developer onboarding day 1.** A new contributor arrives, clones the repo, reads CLAUDE.md, reads ARCHITECTURE.md, opens their editor, and tries to make their first contribution. What do they get stuck on? What conventions are silent? What gate fires that they have no documentation for? What permission do they need that no one told them?

2. **Agent session start.** A fresh Claude Code session starts in this repo. It reads CLAUDE.md, runs the SessionStart hook (which doesn't exist yet — what happens?), tries to figure out the active phase, tries to follow the "First action on resume" pointer in STATUS.md. What does it actually do? Where does it stall? What does it assume that the architecture doesn't actually pin?

3. **Author of a new CHG.** Someone wants to open a new CHG in the current architecture. They need to: pick a CHG number, create the directory, author a proposal.md, author TASK files, link to REQs. What's the procedure? Where is it documented? What conflicts with what (e.g., who allocates the next CHG number — is there a race condition)?

4. **Author of a new REQ.** Someone wants to add a new requirement (REQ). They need to: choose a domain, choose an ID, write the REQ block, satisfy the spec_lint rules, link to a Story and Epic that don't exist yet. What's the procedure? Where does it break?

5. **Reviewer of a PR.** A reviewer arrives at a PR. They need to: understand the CHG context, verify the test discipline (red-first), check the trailers, check for missing artifacts. What does the architecture give them as a reviewing tool? What do they have to figure out from prose? What checks are mechanical vs. manual?

6. **Re-running an audit / a hook.** Someone needs to re-run an audit, a CI gate, a hook locally to investigate something. How do they invoke it? What does success look like? What is the diagnostic format? What if it fails — is there a debug mode?

For each scenario, surface at least 2 distinct defects in the architecture as it currently stands that block, mislead, or silently corrupt the actor's actions. Findings should be specific (file + section + what the actor experiences) and cite the architectural cause (the missing principle, ambiguous procedure, contradicting rule, or unspecified affordance).

Distinct from prior streams:
- INHER (Wave 1, scenario × post-hoc × holistic × blocking) was about "an architect inheriting this architecture from someone else" — a one-step retrospective scenario. Yours is a current-state walk-through with multiple actors.
- RETRO (Wave 2, scenario × post-hoc × holistic × governance) was a hypothetical post-PHASE-5 retrospective. Yours is current-state, not post-PHASE-N.
- PARTY (Wave 1, persona-roundtable) used personas in a roundtable; yours uses scenarios with individual actors taking concrete actions step-by-step.
- STAKE (Wave 4, persona × forward × * × security/ops) was forward-looking multi-stakeholder. Yours is current-state and scenario-by-scenario, not stakeholder-by-stakeholder.

REQUIRED OUTPUT:
- All finding IDs prefixed `SCENNOW-` with severity inline (e.g., `SCENNOW-CRIT-001`).
- Severity guide: CRIT = an actor in a documented scenario cannot proceed without information the architecture does not provide; SER = an actor can proceed but predictably does the wrong thing; PROC = procedural gap that the actor must invent rules for.
- Minimum 12 findings, target 15-20 (≥2 findings per scenario).
- Tag each finding with the scenario number (e.g., "[Scenario 3: Author of a new CHG]").
- 1500-2200 words.
- NO preamble. Start directly with finding SCENNOW-CRIT-001 (or SCENNOW-SER-001 if no CRIT applies).
- End with a one-paragraph summary that totals by severity and names the scenario that has the most blocking gaps.

Do not read files outside the architecture documents listed.
```

## Findings deliverable (final assistant message)

Now I have read all the architecture documents. Let me produce the scenario-by-scenario analysis.

SCENNOW-CRIT-001 [Scenario 1: Developer onboarding day 1] **No installation, bootstrap, or local-setup instructions exist anywhere in the architecture.** `CLAUDE.md` directs the contributor to `ARCHITECTURE.md`, which directs them to ADRs and phase files. None of the eight ADRs or six phase files explain how to set up Python, Node, clasp, install BMAD, configure GCP service-account credentials for the integration tier, or even what Python version to use. PHASE-0 lists "ci.yml stubs" but never names a `bootstrap.sh` or a `pyproject.toml` content surface. The contributor cannot run a single test or hook locally and the architecture documents do not acknowledge this gap. ARCHITECTURE.md §3 lists `pyproject.toml` as "tracked; enforced by `top-level-allowlist`" with no mention of what it must contain.

SCENNOW-CRIT-002 [Scenario 1: Developer onboarding day 1] **`commit-trailers-valid` is a pre-receive hook the contributor cannot satisfy on first commit.** ADR-0005 §3 mandates four trailers (`Task`, `Requirements`, `Tests-Status`, `Phase`); ADR-0008 §5 says the gate runs pre-commit AND pre-receive. A first-day contributor who has not yet read ADR-0005 will compose a normal commit message and have it bounced server-side with no documented diagnostic format. CLAUDE.md mentions trailers but does not explain how to obtain a `TASK-<NNNN>` ID before the very first commit (chicken-and-egg: the task lives in `openspec/changes/<CHG>/tasks/` which the contributor has not yet authored).

SCENNOW-SER-003 [Scenario 1: Developer onboarding day 1] **The "first contribution" path requires a CHG, but PHASE-0 has no procedure for opening one.** PHASE-0 scope item 6 reserves `openspec/changes/_TEMPLATE/` but never specifies the template contents. A contributor wanting to fix even a typo must either route through an undocumented CHG procedure or violate the trailer rules. CLAUDE.md "How to commit" gives no escape hatch (e.g. "trivial-fix" trailer) and `Checkpoint: true` is reserved for the Stop hook only.

SCENNOW-PROC-004 [Scenario 1: Developer onboarding day 1] **Permissions, secrets, and service-account provisioning are silent.** ADR-0003 requires "dedicated test artifacts owned by a CI service account" for the integration tier and ADR-0007 requires real Anthropic API tokens for the stochastic tier. No ADR or phase document explains how the contributor obtains, stores, or rotates these credentials, where in `.claude/settings.json` `env` they belong (§3 layout names `settings.json` only as "permissions, env, hooks"), or what `.env` shape the project expects. The contributor will create their own convention and `.gitignore` already covers `.claude/settings.local.json` but nothing else.

SCENNOW-CRIT-005 [Scenario 2: Agent session start] **The `SessionStart` hook does not exist yet but CLAUDE.md tells the agent to "Run the SessionStart resume hook output."** CLAUDE.md step 4 says the output is "printed automatically once PHASE-2 lands"; the current phase is PHASE-0 (per `phases/PHASE-0-foundation.md` frontmatter `status: in-progress`). A fresh agent thus follows an instruction that has no implementation, with no fallback described. The agent will silently skip the step or fabricate an action — the architecture does not say which.

SCENNOW-CRIT-006 [Scenario 2: Agent session start] **`STATUS.md` is referenced as the "single authoritative session-resume document" but is not in the architecture's REQ-ARCH-* exit criteria and is not enumerated in the layout.** CLAUDE.md step 1 requires `openspec/STATUS.md`; ARCHITECTURE.md §3 layout does not list `STATUS.md`; PHASE-0 scope does not require its existence; REQ-ARCH-0002 through REQ-ARCH-0008 do not mention it. The agent will fail to find the document on resume and has no instruction for what to do (improvise? abort? read git log?).

SCENNOW-SER-007 [Scenario 2: Agent session start] **"Active phase" is determined by phase-file frontmatter `status:` field which has no enforcement that exactly one phase is `in-progress`.** PHASE-0 is `in-progress`; PHASE-1..5 are `pending`. There is no spec_lint rule listed in ADR-0008 §1 that checks "exactly one phase has status: in-progress at any time." If a session leaves two phases marked in-progress (e.g. after partial promotion), the agent's "Read the active phase file" step (CLAUDE.md step 3) has no deterministic resolution.

SCENNOW-PROC-008 [Scenario 2: Agent session start] **The agent must "work only inside the active phase scope" but the scope tests are not yet runnable.** CLAUDE.md final paragraph of "How to start any session" demands phase-scope adherence. PHASE-0's exit tests "live in `tools/ci/tests/test_phase0.py`" (PHASE-0 §Exit criteria) but `tools/ci/` is itself unimplemented at PHASE-0 — it is a PHASE-2-owned directory per ADR-0008 §1 ("Owner | tools/ci"). The agent has no way to verify whether a proposed edit is "inside the active phase scope" except by re-reading the phase file's prose.

SCENNOW-CRIT-009 [Scenario 3: Author of a new CHG] **No procedure for allocating the next CHG number exists, and the existing CHG numbers reveal a non-monotonic allocation: CHG-0002, CHG-0010, CHG-0011, CHG-0012, CHG-0042 are all referenced across ADRs.** ADR-0005 §10 cites CHG-0002, ADR-0002 cites CHG-0010 / CHG-0011 / CHG-0012, ADR-0004 §5 example cites CHG-0042. There is no `tools/spec_lint allocate <chg>` analogue (ADR-0004 §1 covers REQ allocation only). Two authors opening a CHG simultaneously will collide; the architecture provides no advisory-lock or claim convention. PHASE-0 §Scope item 6 says only "`openspec/changes/_TEMPLATE/` directory with empty change-proposal skeleton."

SCENNOW-SER-010 [Scenario 3: Author of a new CHG] **A CHG's required artifacts are not enumerated anywhere.** ARCHITECTURE.md §4 names `CHG-<NNNN>` and `openspec/changes/<CHG-NNNN>/`. ADR-0004 mentions changes only as the `introduced:` frontmatter value. No document lists what files a CHG directory must contain — is it `proposal.md`? `tasks/`? `specs/`? CLAUDE.md says "New requirements live in `openspec/changes/<CHG>/specs/`" implying a `specs/` subdir, and §4 table puts tasks at `openspec/changes/<CHG>/tasks/<TASK-NNNN>.md`, but the `gate`-type vs `docs`-type vs implementation-type task taxonomy referenced in ADR-0002 §7 and ADR-0008 §3 is never defined.

SCENNOW-PROC-011 [Scenario 3: Author of a new CHG] **TASK numbering is global (`TASK-<NNNN>`, see §4 table) but ADR-0002 amendment 0002 cites `CHG-0010 (TASK-0021)` and PHASE-0 / PHASE-1 do not require any TASK index.** Two CHGs concurrently authoring tasks would race on the next TASK number with no allocation tool described. ADR-0004 §1 covers REQ-ID allocation only. Authors will invent local numbering and conflict at merge.

SCENNOW-CRIT-012 [Scenario 4: Author of a new REQ] **A new REQ must reference a Story and Epic (CLAUDE.md "How to add a requirement") but those artifacts are required to be empty templates per REQ-ARCH-0003 throughout PHASE-0..4.** REQ-ARCH-0003 says `openspec/epics/`, `openspec/stories/` "exist with empty templates only (no product content)." PHASE-5 entry criteria say product content is filled "in a separate PR chain." Between PHASE-0 and the product PR chain, a contributor adding a REQ literally cannot satisfy the frontmatter `references.epic` / `references.story` fields shown in ADR-0004 §5. The architecture forbids dummy values (anti-aliasing, prose-xref-banned, broken-xref) but provides no transitional rule.

SCENNOW-SER-013 [Scenario 4: Author of a new REQ] **`anti-aliasing` lint uses a "pinned threshold and n-gram size in `tools/spec_lint/config.yaml`" reviewed quarterly (ADR-0004 §4) but the file does not exist until PHASE-1 and PHASE-0 lists no placeholder.** A PHASE-1 author writing their first REQ will not know whether their wording will fire `anti-aliasing` until the rule is implemented. There is no documented "dry-run" mode or way for the author to compute the score locally. Worse, the threshold value is never named even as a placeholder, so it can be calibrated to silently pass an author's first batch and then fail later authors.

SCENNOW-PROC-014 [Scenario 4: Author of a new REQ] **Domain allocation is unbounded and unregistered.** ADR-0004 §1 says `DOMAIN` is "uppercase alphanumeric ≤ 12 chars." Existing REQ-IDs in the architecture span `REQ-ARCH`, `REQ-SPEC`, `REQ-CI`, `REQ-LLM`, `REQ-LIBTS`, `REQ-LIBPY` (across ADRs and phase files). There is no domain registry, so a new author can introduce `REQ-AUTH` (used in CLAUDE.md examples) or `REQ-AUTHENTICATION` ambiguously. The paper's anti-aliasing concern applies to domain names just as much as to descriptions, but no lint rule covers it.

SCENNOW-CRIT-015 [Scenario 5: Reviewer of a PR] **The reviewer has no canonical command to "show the CHG context for this PR."** ADR-0005 §9 provides `tools/trace/audit.py <id>` but the `<id>` choices are REQ / TASK / STORY / EPIC / PHASE — *not* CHG. The reviewer must read PR title for the CHG ID, then manually open `openspec/changes/<CHG>/` and walk its contents. No `audit CHG-NNNN` summary is specified. Given that a PR is itself a CHG (§4 table), this is a foundational omission.

SCENNOW-SER-016 [Scenario 5: Reviewer of a PR] **`red-before-green` "walks git history" (ADR-0005 §4) but the reviewer cannot run the same walk locally with a documented invocation.** PHASE-2 lists `tools/trace/validate_commit.py` and `tools/trace/audit.py`. Neither documents a flag like `audit --red-first PR-NNN` or `validate_commit --branch <name>`. The reviewer's only mechanical check is "wait for CI to pass"; if CI fails, the diagnostic format is unspecified (no ADR pins a JSON or human-readable schema for hook failure output).

SCENNOW-PROC-017 [Scenario 5: Reviewer of a PR] **The trailer set is closed (`Task`, `Requirements`, `Tests-Status`, `Phase`) yet several additional trailers have been quietly admitted by ADRs: `Checkpoint: true` (ADR-0005 §7), `Bootstrap: <reason>` (ADR-0006 §4), `Material-Architecture-Change: true` (ARCHITECTURE.md preamble), `Skill-Removal-Acknowledged: <id>` (ADR-0002 §8).** There is no single trailer catalog the reviewer can consult to know which trailers are valid and which are mandatory for which commit types. `commit-trailers-valid` will either reject these unknown trailers (blocking legitimate work) or silently accept any string (defeating the purpose).

SCENNOW-CRIT-018 [Scenario 6: Re-running an audit / a hook] **No ADR specifies how to invoke a hook locally outside of Claude Code firing it.** ADR-0005 §6 lists hooks by event (e.g. `PostToolUse(Bash:git commit)`) bound to scripts under `tools/trace/`. The architecture never says whether running `python tools/trace/validate_commit.py <args>` is supported, what the arg shape is, what env vars it expects, or what its exit codes mean. A contributor investigating why a hook fired cannot reproduce the failure outside the Claude Code event loop.

SCENNOW-SER-019 [Scenario 6: Re-running an audit / a hook] **There is no documented debug mode, log surface, or diagnostic format for hook failures.** ADR-0005 §6 says the `journal_commit.py` hook "aborts the hook with a diagnostic (no force-push)" for non-FF cases, and PHASE-2 §Scope says "non-FF cases halt with a diagnostic instead of force-pushing," but the *content* of the diagnostic is unspecified (machine-readable JSON? human prose? exit code?). The investigator has no way to know whether their failed push is a permissions issue, a non-FF, or a network failure without reading hook source.

SCENNOW-PROC-020 [Scenario 6: Re-running an audit / a hook] **Re-running an audit against a particular commit / branch / point-in-time is not specified.** `tools/trace/audit.py <id>` (ADR-0005 §9) is described as "answering deterministically" for IDs, but the audit's reconciliation source (git + journal + spec files + tests) varies by checkout state. The architecture does not say whether audit takes a `--at <sha>` flag, whether the journal is per-working-tree or global, or whether re-running against a colleague's session journal is supported. A reviewer investigating "did this REQ ever go through red?" has no documented invocation.

**Summary.** Twenty findings across six scenarios: 7 CRIT (actor cannot proceed with the information given), 7 SER (actor proceeds and predictably does the wrong thing), 6 PROC (actor must invent rules). The scenario with the most blocking gaps is **Scenario 2: Agent session start** (CRIT-005, CRIT-006, SER-007, PROC-008 — two CRIT findings, including the central paradox that CLAUDE.md instructs the agent to run a hook that does not exist and read a STATUS.md document that is not required to exist), tightly followed by **Scenario 1: Developer onboarding** (CRIT-001 plus CRIT-002 — no bootstrap path and a pre-receive trailer gate the contributor literally cannot satisfy on first commit). The pervasive structural defect across all scenarios is *temporal coupling*: nearly every authoritative instruction is gated on infrastructure that lands in PHASE-2+, but the active phase is PHASE-0 and no transitional procedure is documented.
