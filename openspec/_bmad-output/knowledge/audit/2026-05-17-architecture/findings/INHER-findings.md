# INHER — inheritor-framing (opus) — Wave 1

**Source transcript:** [`raw-transcripts/INHER-agent-a0f191f798cfff918.jsonl`](../raw-transcripts/INHER-agent-a0f191f798cfff918.jsonl)
**Sub-agent description:** `Inheritor-framed review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a0f191f798cfff918`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Frame your review through a specific scenario: you are a senior engineer joining this project 2 years from now. The original authors have all left. Your job is to ship the first new feature against this architecture. Read the 15 documents and identify everything that would prevent you (the inheritor) from doing your job without re-asking the original team.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Specific inheritor questions to ask:
- If a rule says "reviewed quarterly (a `gate`-type task)" but `gate`-type task isn't defined, what do I do?
- If a gate name appears in a phase but not in the gate inventory, do I trust the phase or the inventory?
- If two ADRs disagree about a file path, which one is authoritative?
- If a hook is supposed to enforce an invariant but the invariant text admits the hook doesn't catch the original failure mode, do I trust the invariant?
- If `tools/spec_lint allocate` is referenced but doesn't exist, am I supposed to hand-allocate, or build the missing tool first?
- If the architecture is "frozen" but PHASE-0 is "in-progress", which timestamp is the freeze date?
- If "the paper" is cited but never identified, where do I learn the theoretical foundations the architecture is built on?
- If CLAUDE.md and ARCHITECTURE.md restate the same five principles verbatim, which one wins on disagreement?
- If a checkpoint commit appears in the history between my red and green commits, will the red-before-green gate find my red commit?

REQUIRED OUTPUT:
- Stable IDs: prefix `INHER-` (e.g. INHER-01; severity inline as CRITICAL/SERIOUS/PROCESS based on whether the inheritor is blocked, slowed, or merely annoyed)
- Each finding: the inheritor's question, what the documents do/don't answer, what the inheritor would have to invent or guess
- Minimum 15 findings
- 1500-2500 words
- Speak in inheritor first-person ("I cannot tell whether…", "I would have to assume…")
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have read all 15 documents. Now I'll produce the inheritor review.

---

# Inheritor Review — INHER-01 through INHER-22

I am the senior engineer who has inherited this repository two years after the original authors departed. My task is to ship the first new feature. Below is what I cannot do without re-asking a team that does not exist.

## INHER-01 (CRITICAL) — The `gate`-type task is undefined

I cannot tell what a `gate`-type task *is*. `ADR-0004 §4` tells me the anti-aliasing threshold is "reviewed quarterly (a `gate`-type task)". `ARCHITECTURE.md §11` tells me "The phase exit ADR is a `gate`-type task." `ADR-0003 §4` says `prod` is "promoted from `dev` only on a merged `gate`-type task." `PHASE-5` says production deployment is a "separate `gate`-type task on the merged PR." Four uses, one term, zero definitions. The taxonomy of TASK types (`docs`-type appears once in `ADR-0002 §7`) is referenced but never enumerated. I would have to invent the schema — does a gate-type task carry a `type:` frontmatter field? Does it require a specific approver list? Does it create a tag, a release, or just a commit? Does the `phase-exit` CI gate look for it? I cannot ship the first feature without knowing whether my promotion-to-prod task needs to declare `type: gate` and what that triggers.

## INHER-02 (CRITICAL) — Gate inventory and phase scope disagree on `bmad-version-pin` and `bmad-smoke-test`

`ADR-0008 §1` is the gate inventory. `PHASE-2` scope lists four gates that **do not appear in `ADR-0008 §1`**: `skill-removal-acknowledged`, `bmad-version-pin`, `bmad-smoke-test`, and the implicit `stale-staging` (`ADR-0002 §7`, deferred). `ADR-0008 §2` says `gate-coverage` "walks every ADR and every principle... and verifies that at least one entry in the table above references it. A missing reference fails the build." So either `gate-coverage` itself fails the moment PHASE-2 lands these gates (they are not in the table), or the table is the wrong source of truth. The documents do not say which one wins. I would have to guess: edit `ADR-0008 §1` as part of my first feature, or treat the phase as the source of truth and accept silent inconsistency. Neither is something I should be doing as a first-day inheritor.

## INHER-03 (CRITICAL) — "The paper" is never identified

`ARCHITECTURE.md §2` introduces "a published result on transformer associative memory (referred to throughout as 'the paper')". `ADR-0004` opens with "A published result on transformer associative memory ('the paper') establishes that semantic-recall systems exhibit: finite effective rank... positive competitor mass... power-law forgetting... δ-convex lures." There is no title, no author, no DOI, no arXiv ID, no year, no link. The entire spec-storage discipline (`ADR-0004`), the anti-aliasing rule, the `semantic-recall-recall-at-k` gate threshold, and the prohibition on semantic spec lookup all hang from a citation I cannot resolve. If I want to tune the n-gram threshold (`tools/spec_lint/config.yaml`, reviewed quarterly) or evaluate whether a new embedding model is safe to introduce, I have no theoretical foundation to consult. I would have to guess thresholds from first principles or search arXiv blindly.

## INHER-04 (SERIOUS) — CLAUDE.md and ARCHITECTURE.md restate the same principles; precedence is undeclared

The five principles appear verbatim in both `ARCHITECTURE.md §1` and `CLAUDE.md`. `CLAUDE.md` says it is "a restatement of something defined more precisely in [ARCHITECTURE.md]". But `REQ-ARCH-0007` says `CLAUDE.md` "references the five principles in §1 verbatim" — so the verbatim duplication is enforced. If a future amendment changes the wording in one but not the other, which one wins? `CLAUDE.md` says ARCHITECTURE wins ("defined more precisely"), but the `gate-coverage` and verbatim-citation rules would still pass against the now-divergent CLAUDE.md. I would have to invent a "single source" rule and add a lint gate that one mirrors the other. The Single Source of Truth principle (P1) is violated by the very document that declares it.

## INHER-05 (CRITICAL) — `tools/spec_lint allocate` is referenced but does not exist in any phase scope

`ADR-0004 §1` says "Identifier allocation is by `tools/spec_lint allocate <domain>` against `openspec/specs/INDEX.yaml`. Hand-allocation is permitted but checked." `PHASE-1` scope lists "implementation of every gate owned by `tools/spec_lint`" — but `allocate` is a sub-command, not a gate. Nothing in any phase explicitly schedules its implementation. The forbidden list in `CLAUDE.md` says "Hand-editing `openspec/specs/INDEX.yaml` after PHASE-1" — so after PHASE-1 I must use a tool that may or may not exist. I cannot tell whether (a) `allocate` is implicitly included in PHASE-1, (b) it is supposed to be built by me as part of my feature, or (c) hand-allocation under the "permitted but checked" carve-out is the intended path. As a first-day inheritor allocating my first REQ-ID, I am blocked.

## INHER-06 (SERIOUS) — The freeze date and the in-progress date conflict

`ARCHITECTURE.md` says "This document and the ADRs / phase files it references constitute the **frozen architecture artifact**." But `PHASE-0` is `status: in-progress` and PHASE-1 through PHASE-5 are `status: pending`. All ADRs are dated `2026-05-16`; `CLAUDE.md` says today is `2026-05-17`. If the architecture is "frozen" while the foundation phase is still "in-progress", I cannot tell whether the freeze is (a) the ADR signature dates, (b) the moment PHASE-0 exits, (c) the moment all phases exit, or (d) immediately on file commit. The phrase "frozen architecture artifact" implies my changes must go through "an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate" — but `Material-Architecture-Change` appears nowhere else, and "re-gate" is undefined when PHASE-0 has never finished gating in the first place. I would have to guess what triggers a re-gate.

## INHER-07 (CRITICAL) — Checkpoint commits and red-before-green are silently incompatible

`ADR-0005 §4` says "A test's first green commit must be preceded by at least one commit where the same test exists in a red state. `tools/trace/validate_commit.py` walks git history to verify." `ADR-0005 §7` says the `Checkpoint: true` trailer "makes CI gates skip the commit and makes the next non-checkpoint commit on the branch responsible for restoring P4 compliance (either by squash or by ensuring the red/green sequence is recoverable from the full history)." If my red commit is followed by a checkpoint commit (auto-created by `Stop`), and then by my green commit, will `validate_commit.py` find the red? "Walks git history" suggests yes — the red commit is still in the history. "Squash" suggests no — the recommendation is to collapse the checkpoint. Worse, `ADR-0008 §6` says checkpoint exemptions live in `tools/trace/checkpoint_exemptions.yaml` (a file that does not exist yet and whose schema is undocumented). I cannot tell whether my next development workflow needs to squash before pushing, or whether the gate is tolerant. I would have to invent a squash policy.

## INHER-08 (SERIOUS) — Push invariant admits the failure mode it claims to fix

`ADR-0005 §6` (post-amendment 0001) states: "every operation that mutates the commit graph or moves a branch pointer must result in origin tracking the post-state within the same hook firing. The three hooks marked above are the enforcement surface; the invariant is otherwise unenforceable and silently rots (the failure mode is 'committed but unpushed when the container is reclaimed' — recoverable via merge history only if the commits also reached master through a PR merge, otherwise lost)." So the invariant exists, the invariant is "otherwise unenforceable", and the failure mode survives the enforcement. `ADR-0005 §8` row 5 confirms "residual loss only if both hooks fail to fire". If the hook is meant to enforce an invariant but the invariant text explicitly admits the hook does not catch the original failure mode, I cannot trust the invariant. I would have to guess whether to add a server-side pre-receive enforcement, a periodic reconciler, or a separate watchdog. None is documented.

## INHER-09 (SERIOUS) — Layout disagreement: `bmad/` vs `_bmad/` and the wrapper-layer ghost

`ADR-0001` references `bmad/` (no underscore) and links to `ADR-0002` for rules. `ADR-0002 §2` says "Install path: `_bmad/`" with underscore. `ARCHITECTURE.md §3` shows `_bmad/`. `PHASE-1 §3` says "`bmad/` installation per ADR-0002, pinned in `bmad/config.yaml`" — no underscore, and the config file does not exist under either path per `ADR-0002` (the manifest is `_bmad/_config/manifest.yaml`). Worse, `ARCHITECTURE.md §9` describes "thin wrappers in `.claude/agents/` and `.claude/commands/`" — but `ADR-0002 amendment 0001` explicitly drops the wrapper-isolation strategy and says those slots are "legacy ... empty". `PHASE-1 §4` still schedules `.claude/agents/` and `.claude/commands/` wrappers. Three documents, three different stories. Which is authoritative? The amendment log says CHG-0010 was the rewrite, but it did not propagate edits to PHASE-1 or ARCHITECTURE.md §9 or ADR-0001. If I want to wire a new BMAD skill, I cannot tell where it lives or whether wrappers are required.

## INHER-10 (SERIOUS) — Compound-requirement defects in the requirements themselves

`ADR-0004 §3` says "One REQ contains one assertion. Compound requirements ('the system must do A and B') are split". But `REQ-ARCH-0007` reads: "`CLAUDE.md` (root) is present **and** references the five principles in §1 verbatim." That is two assertions: existence and content. `REQ-ARCH-0008` reads: "`.claude/settings.json` is present; hooks declared in ADR-0005 are listed." Two assertions joined by a semicolon. If `compound-requirement-detector` runs over architecture REQs, the architecture itself fails the lint. If it does not run there, the rule exempts the most important specs. I cannot tell which is intended, and I would have to invent a scoping rule before my first REQ.

## INHER-11 (CRITICAL) — `gate-coverage` walks ADRs but the gate list omits at least three ADRs by direct mapping

`ADR-0008 §2` says `gate-coverage` walks every ADR and verifies "at least one entry in the table above references it." The gate inventory references ADR-0001 through ADR-0007 by name in the "Enforces" column. But where is the gate that enforces `ADR-0002 §9` (per-project output isolation)? Where is the gate for `ADR-0003 §4` (deployment topology)? Where is the gate that enforces `ADR-0005 §6` (the push invariant) — `commit-trailers-valid` and `red-before-green` enforce different sections? `gate-coverage` is defined coarsely ("references the ADR") so it passes vacuously, but the coverage it claims is illusory. If I want to know which gate catches my mistake of forgetting to push after a rebase, no gate in the inventory names that invariant. I would have to invent one or trust the hook (which §6 admits cannot enforce the invariant alone — see INHER-08).

## INHER-12 (SERIOUS) — The `Bootstrap:` trailer is the only documented escape and its review path is undefined

`ADR-0006 §4` says "Bulk green-starts ... require a `Bootstrap: <reason>` trailer and an approving review; CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." Three problems: (1) `bulk-green-start` does not appear in the `ADR-0008 §1` gate inventory; (2) `N` is not pinned anywhere; (3) "approving review" — by whom, with what mechanism — is unspecified. If I import a battery of green tests when standing up my first feature's test harness, I cannot tell what `N` is, who approves, or whether the gate even runs. I would have to guess `N` and route review through whatever mechanism I invent.

## INHER-13 (SERIOUS) — Hook ordering and `PostToolUse(Bash:git commit)` race

`ADR-0005 §6` lists `PostToolUse(Bash:git commit)` as `journal_commit.py` which "appends `commit` event **and pushes `HEAD` to origin as a fast-forward**". But `ADR-0008 §5` says "`index-up-to-date` and `matrix-drift` run pre-commit and rewrite the affected files. Commit proceeds with the rewritten files staged." So pre-commit rewrites files into the commit, commit completes, then `journal_commit.py` pushes. If `matrix-drift` rewrites the matrix during commit, but `tools/trace/rebuild.py` (the source) is what produces that rewrite — and `rebuild.py` reads the journal, which is appended only by `PostToolUse` after the commit completes — there is a causality loop on the first commit of a session. The first commit cannot produce a matrix that includes itself. The documents never describe how the bootstrap is handled. I would have to invent a "matrix excludes the current commit" rule or run rebuild twice.

## INHER-14 (PROCESS) — `Material-Architecture-Change: true` trailer is undefined

`ARCHITECTURE.md` opens "Modifications to the structure described here require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate." That trailer appears nowhere else — not in `ADR-0005 §3` (mandatory trailers), not in `ADR-0008 §6` (bypass discipline), not in `checkpoint_exemptions.yaml`. I cannot tell whether `commit-trailers-valid` accepts it, rejects it, or ignores it. I cannot tell what "Phase-0 re-gate" entails operationally — re-run all REQ-ARCH-* tests? Re-sign ADRs? Open a new CHG? As the inheritor making my first architectural amendment, I am blind.

## INHER-15 (SERIOUS) — `STATUS.md` is the session-start required reading and it is not in PHASE-0 scope

`CLAUDE.md` step 1 of "How to start any session" says "Read `openspec/STATUS.md` first. Single authoritative session-resume document." Nothing in PHASE-0 scope creates `openspec/STATUS.md`. Nothing in `REQ-ARCH-*` requires it. The footnote says it is "Hand-maintained until PHASE-2's `SessionStart` resume hook mechanizes it." But hand-maintained by whom, with what update cadence, and audited against what? If the file does not exist on my first day, the very first instruction in `CLAUDE.md` cannot be followed. I would have to invent the document and seed it from git log + ADR log.

## INHER-16 (SERIOUS) — Tier coverage rule and `tier:` frontmatter contradict the four-tier model

`ADR-0004 §5` shows the frontmatter `tier:` field with values `unit | integration | e2e | stochastic` — singular. `ADR-0006 §5` says "A REQ marked `tier: e2e` requires a passing E2E test (unit tests do not satisfy the REQ)." But many REQs naturally need both unit and integration coverage. If `tier:` is a scalar, the spec model forbids multi-tier coverage. If it is a list, the YAML example in `ADR-0004 §5` is wrong. `ADR-0003 §3` says "Four test tiers per project, all required" — implying every project exercises all four. The conflict is unresolved. For my first feature, I cannot tell whether a single REQ takes one tier or many. I would have to guess the schema.

## INHER-17 (PROCESS) — The CHG numbering scheme has historical gaps and no allocation rule

`ADR-0002` references `CHG-0010` (rewrite), `CHG-0011` (`top-level-allowlist`), `CHG-0012` (`bmad-direct-reference`), `CHG-0010 (TASK-0021)`. `ADR-0005` references `CHG-0002`. `ADR-0004 §5` example REQ uses `introduced: CHG-0042`. There is no CHG allocation tool described, no `tools/spec_lint allocate-chg` equivalent, no INDEX of CHGs. If I am opening CHG-0043 for my first feature, I do not know whether the numbering is contiguous, monotonic, or per-author. The matrix presumably learns the CHG from a directory, but the directory's creation rules are undocumented.

## INHER-18 (SERIOUS) — Project-scoped openspec overlay rules are unspecified

`ADR-0001` mentions "Per-project specs extend root specs by reference; no duplication" and `projects/<project>/openspec/` as a "project-scoped specs (extends root)". No ADR describes the overlay semantics: do project REQs use a different domain prefix to avoid collision with root? Does the project INDEX.yaml federate with the root, or is there one global INDEX? Are project REQs allowed to supersede root REQs? PHASE-5 is "the load test for the architecture" but does not introduce these semantics; it consumes them. As the inheritor placing my first project under `projects/<myproject>/`, I cannot tell whether `REQ-MYPROJ-0001` lives in the root INDEX or a per-project one. The matrix builder behavior is undefined.

## INHER-19 (PROCESS) — `cost-tier: cheap` vs `cost-tier: full` are referenced but unenumerated

`ADR-0007 §4` introduces `@cost-tier cheap` and `@cost-tier full`. No ADR lists the full taxonomy or the per-tier dollar/token budget. `ADR-0008` schedules `cost-budget` on "every PR + nightly" — but the per-PR ceiling and the nightly ceiling are not pinned in the document. PHASE-3 says "Stochastic tier cost stays within budget for two consecutive nightly runs" without defining the budget. I would have to invent token budgets out of thin air for my first stochastic test.

## INHER-20 (PROCESS) — Empty `_TEMPLATE` files are required but their schemas are not given

`PHASE-0 §4` requires empty templates: `openspec/briefs/_TEMPLATE.md`, `prd/_TEMPLATE.md`, `epics/_TEMPLATE.md`, `stories/_TEMPLATE.md`, and `changes/_TEMPLATE/`. No ADR specifies what frontmatter or section structure these templates must contain. `ADR-0004 §5` describes REQ block format but not Brief, PRD, Epic, or Story formats. The Epic-coverage rule in `ARCHITECTURE.md §5` says an Epic carries a `coverage:` block — but does not show the frontmatter alongside. I would have to invent the frontmatter for every product artifact type.

## INHER-21 (SERIOUS) — Anti-aliasing threshold review cadence is unowned

`ADR-0004 §4` says the n-gram threshold "is pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." Quarterly by whom, kicked off by what mechanism, tracked in what artifact? No cron job is documented, no calendar reminder, no responsibility ledger. If I am the only engineer on the project two years from now, I cannot tell whether the threshold has been reviewed on schedule or whether I am the person who must review it. I would have to invent a recurring-task ledger.

## INHER-22 (PROCESS) — `tools/trace/checkpoint_exemptions.yaml` is undocumented

`ADR-0008 §6` says `Checkpoint: true` "applies to a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`." The file's schema, default contents, and authorship policy are nowhere defined. If my first feature triggers a checkpoint commit, I cannot predict which gates skip and which fire. I would have to read the implementation (in a phase that has not been built) to find out.

---

## Bottom line as the inheritor

I cannot ship the first feature without first writing — under my own authority — at least seven artifacts that the original team should have left me: a TASK-type taxonomy (INHER-01), a reconciled gate inventory (INHER-02), a citation for "the paper" (INHER-03), the precedence rule between CLAUDE.md and ARCHITECTURE.md (INHER-04), the `allocate` tool or a hand-allocation discipline (INHER-05), the freeze/re-gate operational definition (INHER-06), and a squash-vs-history rule for checkpoint commits crossing red-green boundaries (INHER-07). Every one of these is a decision the original team owed me and did not leave. The architecture's central promise — "session resume requires zero human re-briefing" — is unmet on day one for an inheritor who has no team to brief them.
