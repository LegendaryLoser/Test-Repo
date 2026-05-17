# COURSE — correct-course (opus) — Wave 3

**Source transcript:** [`raw-transcripts/COURSE-agent-a5bd87ec9c9916dce.jsonl`](../raw-transcripts/COURSE-agent-a5bd87ec9c9916dce.jsonl)
**Sub-agent description:** `Correct-course change management`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a5bd87ec9c9916dce`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-correct-course` skill via the Skill tool. Apply it to the architecture artifact — identifying where the architecture itself needs a course correction now (not in some future phase, but immediately) to remain coherent.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

The skill is normally invoked when "significant changes during sprint execution" are needed. Apply it here as: "the architecture artifact is currently drifting — what course corrections would you propose RIGHT NOW to prevent the drift from becoming irrecoverable?"

For each finding, frame as:
- Drift observed (with specific file/section/quote)
- What the drift will cause if uncorrected
- The correction needed (not described in detail; just named)
- Cost of correcting now vs cost of correcting after N more PRs have built on top of the drift

Focus areas:
- Decisions that look stable but are actually accumulating exception cases
- Conventions that are being violated under exception pressure
- Amendments that should be supersessions
- Deferred work whose deferral compounds risk
- Choices that were right at PHASE-0 but are wrong now given what's been learned

REQUIRED OUTPUT:
- Stable IDs: prefix `COURSE-` (e.g. COURSE-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 12 findings
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have all 15 documents loaded. Now I'll produce the course-correction analysis directly.

---

# Architecture Course-Correction Proposal

**Date:** 2026-05-17 | **Active phase:** PHASE-0 (in-progress) | **Scope:** the frozen architecture artifact under `openspec/architecture/`

The architecture artifact is, on its face, internally well-organized: eight ADRs, six phase files, a top-level narrative, and a manifest of CI gates that close the loop. But under a Correct-Course lens — treating the artifact itself as the in-flight work product — there is meaningful drift already accumulating, and the drift has the specific signature the methodology is meant to catch: stable-looking decisions accreting exception cases, amendments doing the work of supersessions, and PHASE-0 obligations being silently relocated into later phases. Below, twelve findings across three severity tiers. Each names the drift, what it costs to leave it, the correction it needs, and the relative cost of fixing it now versus after the next N PRs build on top of it.

---

## CRITICAL — fix before any further PR

### COURSE-CRIT-01 — ADR-0002 amendment 0001 is a supersession masquerading as an amendment

**Drift observed.** `ADR-0002` amendment row 0001 (`openspec/architecture/decisions/ADR-0002-bmad-integration.md` §"Amendment log") states: *"Complete rewrite to match BMAD v6.6.0 empirical reality. Install path: `_bmad/` (was `bmad/`). Integration: native Claude Code Skills under `.claude/skills/` (was thin wrappers under `.claude/agents/` and `.claude/commands/`). … The wrapper-isolation strategy from ADR-0002's original revision is dropped."* A "complete rewrite" that drops the original strategy is the definitional case of supersession under ADR-0004 §1 ("Material change … produces a new REQ with `supersedes: <old-id>`; the old REQ remains … with `status: deprecated`"). ADR-0002's `supersedes`/`superseded_by` frontmatter fields are both `null`.

**What it will cause uncorrected.** Future ADRs will follow the precedent. The append-only amendment log becomes the carve-out for arbitrarily large pivots, and the supersession discipline ADR-0004 enshrines for REQs gets quietly excluded from ADRs themselves. The most consequential ADR in the repo (BMAD integration) becomes an unreviewable palimpsest.

**Correction.** Retire ADR-0002 as `superseded_by: ADR-0009`; introduce ADR-0009 carrying the v6.6.0 content; preserve the original text in ADR-0002 with `status: superseded`.

**Cost now vs later.** Now: one ADR file rename, one new ADR, one cross-reference sweep (ARCHITECTURE.md §3, §9; PHASE-1 §3,4; PHASE-2 §3; PHASE-5 §4; ADR-0008 gate table). After 5 more PRs that cite "ADR-0002 §7/§8/§9": every citation becomes ambiguous (was §7 from amendment 0001 or 0002?), and the same fix requires rewriting all of them.

### COURSE-CRIT-02 — `.claude/agents/` and `.claude/commands/` are simultaneously dead and live

**Drift observed.** `ARCHITECTURE.md` §3 lists `.claude/agents/` and `.claude/commands/` as "(legacy slot — empty in v6 native-skills model)". `ARCHITECTURE.md` §9 still reads: *"BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`."* `PHASE-1-spec-hygiene.md` §4 still mandates: *"`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas … and core commands"* and §"Exit criteria" still gates on *"All BMAD wrapper files in `.claude/agents/` and `.claude/commands/` resolve their `Load:` paths."* ADR-0002 amendment 0001 explicitly dropped the wrapper strategy. ADR-0008 §1 still references `bmad-direct-reference` against paths consistent with the dead model.

**What it will cause uncorrected.** PHASE-1, the next phase to enter, has an exit criterion that is impossible to satisfy (no wrappers will exist) and one that contradicts ADR-0002. The phase will either be declared green dishonestly or block forever; either way the matrix becomes untrustworthy.

**Correction.** Rewrite ARCHITECTURE.md §9 and PHASE-1 §3,4 and §"Exit criteria" to the native-Skills model; delete the legacy-slot rows from the layout diagram or annotate them as "must remain empty, enforced by `top-level-allowlist`".

**Cost now vs later.** Now: three section edits. After PHASE-1 work starts: a phase rewrite mid-flight, plus a retraction of any wrapper artifacts created in good faith from the stale text.

### COURSE-CRIT-03 — Layout diagram contradicts ADR-0002 about install path

**Drift observed.** `ARCHITECTURE.md` §3 shows `_bmad/` (correct, per amendment 0001), but ADR-0001 §"Decision" and §"Compliance" still read *"`bmad/` is the BMAD installation"* and reference `bmad/config.yaml`. PHASE-1 §3 and PHASE-1 §"Exit criteria" cite `bmad/config.yaml` (was renamed to `_bmad/_config/manifest.yaml` per ADR-0002 amendment 0001). PHASE-0 §12 states *"`bmad/` is **not** installed in PHASE-0"* using the dead name.

**What it will cause uncorrected.** Every gate or test written against either the old or the new path is half-wrong. The `top-level-allowlist` gate in ADR-0008 cannot be implemented without knowing which path is authoritative.

**Correction.** Sweep `bmad/` → `_bmad/` across ADR-0001, PHASE-0 §12, PHASE-1 §3 and exit criteria, ADR-0008 §1 (if implicitly affected). Update `bmad/config.yaml` → `_bmad/_config/manifest.yaml`.

**Cost now vs later.** Now: a global find/replace with eyes on ~6 sites. After PHASE-1 lands a real BMAD install: the install will succeed but the surrounding tests/gates will reference a path that does not exist, surfacing as red CI on every PR until tracked down.

### COURSE-CRIT-04 — PHASE-0 declares hooks PHASE-0 cannot test

**Drift observed.** `PHASE-0` §"Scope" item 9 commits hook *declarations*. `REQ-ARCH-0008` requires `.claude/settings.json` "is present; hooks declared in ADR-0005 are listed". `ADR-0005` §6 amendment 0001 has *added* two hooks (`PostToolUse(Bash:git commit)` push extension, `PostToolUse(mcp__github__merge_pull_request)`) and §7 extends the `Stop`/`SessionEnd` checkpoint with push-on-clean-tree logic. PHASE-0's REQ-ARCH-0008 was written before these existed. There is no gate that the *expanded* hook set is declared at PHASE-0; the green-status of REQ-ARCH-0008 against the pre-amendment hook list is therefore stale.

**What it will cause uncorrected.** PHASE-0 closes "green" on a hook list that omits the push invariant. The push invariant lands in PHASE-2 (per ADR-0005 §6 and PHASE-2 §1) but is never declared in `.claude/settings.json` because PHASE-0 already passed.

**Correction.** Either (a) widen REQ-ARCH-0008 to enumerate the post-amendment hook set explicitly and re-rate PHASE-0, or (b) introduce REQ-ARCH-0009 covering the push-hook declarations and add it to PHASE-0 exit. Option (a) is cheaper but violates ID immutability; option (b) is the disciplined fix.

**Cost now vs later.** Now: one REQ added, one PHASE-0 §"Exit criteria" line added. After PHASE-2 lands the push hooks: the hooks will be implemented but undeclared in settings, causing them never to fire, which is the *exact* failure mode amendment 0001 was written to prevent.

---

## SERIOUS — fix within the current phase

### COURSE-SER-05 — Anti-aliasing threshold is undefined and deferred to "quarterly review"

**Drift observed.** `ADR-0004` §4 says the threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and "reviewed quarterly (a `gate`-type task)". The config file does not exist yet (PHASE-1 deliverable), and no concrete value, no baseline corpus, no calibration procedure is specified.

**What it will cause uncorrected.** PHASE-1 will land a threshold chosen by whichever PR is first to need it, becoming the de facto standard with zero evidence behind it. The paper-derived rationale (δ-convex lures) demands a *calibrated* threshold; an uncalibrated number is theatre.

**Correction.** Add a deliverable to PHASE-0 or PHASE-1 to produce a calibration test fixture (synthetic aliased pairs) plus a pinned threshold derived from it.

**Cost now vs later.** Now: one paragraph in ADR-0004 §4 plus a single PHASE-1 deliverable. After PHASE-1: changing the threshold invalidates whatever specs were graded against the prior value.

### COURSE-SER-06 — `_bmad/_config/manifest.yaml` vs `scripts/install_bmad.sh` is a two-source-of-truth problem

**Drift observed.** `ADR-0002` §1 names the manifest as "canonical version source". `ADR-0008` row `bmad-version-pin` exists only implicitly (referenced by PHASE-2 §4) and exists to enforce that the manifest "matches the comment in `scripts/install_bmad.sh`". Two locations, both authoritative, reconciled by a gate. This is *exactly* the pattern P1 (Single Source of Truth) forbids.

**What it will cause uncorrected.** Every BMAD upgrade is a coordinated edit across two files; a slip produces a CI failure that is interpreted as "the gate is wrong" and the gate gets bypassed.

**Correction.** Make the install script *read* the manifest (or vice versa); delete the second source. The gate then becomes a no-op or a syntactic check on the read.

**Cost now vs later.** Now: rewrite of one shell script and one ADR sentence. After PHASE-2 ships `bmad-version-pin`: deleting the second source breaks the gate and requires re-implementing it.

### COURSE-SER-07 — ADR-0008 has no entry for the BMAD upgrade gates it now requires

**Drift observed.** `ADR-0002` §"Compliance" lists `skill-removal-acknowledged`, `bmad-smoke-test`, and a `bmad-version-pin` check. `ADR-0008` §1 gate inventory does not include any of these rows, yet ADR-0008 §2's `gate-coverage` meta-gate "walks every ADR and every principle … and verifies that at least one entry in the table above references it. A missing reference fails the build." `gate-coverage` will itself fail on day one.

**What it will cause uncorrected.** PHASE-2 cannot exit (gate-coverage red), so the architecture cannot reach PHASE-3.

**Correction.** Add three rows to ADR-0008 §1 for `skill-removal-acknowledged`, `bmad-smoke-test`, `bmad-version-pin`, all mapped to ADR-0002.

**Cost now vs later.** Now: three table rows. After PHASE-2 implementation work begins on `gate-coverage`: the gate fails, work stops, the rows get added under time pressure with the risk of being defined wrong.

### COURSE-SER-08 — `stale-staging` and `semantic-recall-recall-at-k` deferral compounds risk

**Drift observed.** Two gates carry "(deferred CHG)" or "(if used)" qualifiers in ADR-0002 §"Compliance" and ADR-0008 §1. Both are listed in inventories but neither has a phase assignment, an owner, or an exit gate forcing the deferral to ever resolve.

**What it will cause uncorrected.** They will never land. The `gate-coverage` meta-gate either tolerates them (in which case it is not actually a coverage check) or rejects them (in which case PHASE-2 cannot exit).

**Correction.** Either remove these gates from the architecture artifact and reintroduce them when their CHG opens, or assign them to a concrete phase (PHASE-1 for stale-staging, PHASE-2 for semantic-recall-recall-at-k) and create the REQ-CI-* requirements that block phase exit.

**Cost now vs later.** Now: a decision and a sentence per gate. After PHASE-2: the meta-gate either lies or blocks; the deferral becomes permanent technical debt.

### COURSE-SER-09 — PHASE-5 carries two `4.` numbered items

**Drift observed.** `PHASE-5-first-appscript-project.md` §"Scope" has both an item `4.` for "Per-project BMAD output isolation" and a second item `4.` for "Test suite across all four tiers". This is a mechanical defect but the kind ADR-0004 §3 (atomicity) is meant to prevent: the two items have different concerns, different exit conditions, and one will be silently treated as the other.

**What it will cause uncorrected.** When a PR claims "PHASE-5 item 4 done", reviewers will not know which 4. The phase-exit gate has no concrete REQ-ID for either; closure by description ("the BMAD isolation work") is a `prose-xref-banned` violation by spirit if not letter.

**Correction.** Renumber; introduce REQ-ARCH-* IDs for each PHASE-5 scope item so the phase-exit gate has something concrete to evaluate.

**Cost now vs later.** Now: trivial. After PHASE-5 has begun: which "4" is closed becomes a live question on a long-lived branch.

---

## PROCESS — fix the process before it produces more drift

### COURSE-PROC-10 — Amendment log lives inside the amended document, violating the spec-storage form

**Drift observed.** ADR-0002 §"Amendment log" and ADR-0005 §10 "Amendment log" are inside the documents they amend. ADR-0004 §7 (append-only at the assertion level) requires that material edits to a frozen artifact create a *new* artifact. By analogy with REQs, ADRs should not be edited in place; the amendment-log pattern circumvents this with no ADR justifying the divergence.

**What it will cause uncorrected.** ADRs become the soft spot in the spec-discipline regime. The very document defining storage discipline (ADR-0004) is itself being applied non-uniformly. Future contributors will infer that frontmatter immutability is suggestion-grade.

**Correction.** Decide and document: either ADRs are exempt from ADR-0004 §7 (and that exemption is itself an ADR), or amendments become supersession ADRs. Either resolution is fine; the absence of a resolution is not.

**Cost now vs later.** Now: one short ADR. After every future architectural change: the precedent calcifies, and the cost of unwinding it is one new ADR *plus* one supersession per past amendment.

### COURSE-PROC-11 — REQ-ARCH-* coverage at PHASE-0 is incomplete relative to the document it gates

**Drift observed.** PHASE-0 has eight REQ-ARCH-* exit criteria. The architecture defines: top-level layout, atomic-unit IDs, spec-sourcing reconciliation, spec storage format, traceability matrix as cache, session-persistence guarantees, workflow surface, the principle-gate one-to-one. Only some of these get a REQ-ARCH at PHASE-0 (layout, ADR presence, templates, INDEX parse, xref resolution, no-code-in-arch, CLAUDE.md verbatim, hook declarations). The fact that ARCHITECTURE.md §3 changed (per COURSE-CRIT-03) without any REQ-ARCH detecting the inconsistency is direct evidence the REQ set is too sparse.

**What it will cause uncorrected.** The architecture artifact will continue to drift internally with no mechanical detection. The principle "cross-document consistency is lintable" (P1) is not actually lintable as currently scoped.

**Correction.** Add REQ-ARCH-0009 (or supersede 0001..0008 to widen coverage) requiring cross-ADR consistency: every path mentioned in any ADR resolves to the same path in every other ADR and in ARCHITECTURE.md §3.

**Cost now vs later.** Now: one REQ, one test. After every future ADR amendment: each amendment must hand-audit all peers for drift, which is what we are doing right now in this proposal.

### COURSE-PROC-12 — "Material-Architecture-Change: true" trailer is declared and undefined

**Drift observed.** `ARCHITECTURE.md` lines 11–13 mention a `Material-Architecture-Change: true` commit trailer as one of the two paths to modify the architecture. No ADR defines its semantics, no gate enforces it, ADR-0005 §3 (mandatory trailers) does not list it, and the gate inventory in ADR-0008 §1 has no row for it.

**What it will cause uncorrected.** The trailer will be added casually to commits the author thinks are "important" and ignored on those that are quietly material. The escape hatch from "ADR required" is itself ungoverned, which is the exact failure mode ADR-0008's gate-coverage gate was built to eliminate.

**Correction.** Either (a) remove the trailer from ARCHITECTURE.md and force ADRs as the only path, or (b) add an ADR specifying when the trailer applies, who can authorize it, and which gates inspect it.

**Cost now vs later.** Now: one ARCHITECTURE.md edit or one short ADR. After the first commit uses the trailer: precedent is set for an undefined mechanism, and rescinding it retroactively requires re-judging that commit.

---

## Summary triage

| Severity | ID | Recommended path |
|---|---|---|
| CRITICAL | COURSE-CRIT-01 | Open CHG to supersede ADR-0002 with ADR-0009 |
| CRITICAL | COURSE-CRIT-02 | Edit ARCHITECTURE.md §9 + PHASE-1 §3,4 + exit criteria in same CHG |
| CRITICAL | COURSE-CRIT-03 | Path sweep `bmad/` → `_bmad/` in same CHG |
| CRITICAL | COURSE-CRIT-04 | Add REQ-ARCH-0009 for expanded hook set, add to PHASE-0 exit |
| SERIOUS | COURSE-SER-05 | PHASE-1 deliverable: anti-aliasing calibration fixture + pinned threshold |
| SERIOUS | COURSE-SER-06 | Make install_bmad.sh read the manifest; delete second source |
| SERIOUS | COURSE-SER-07 | Add three gate rows to ADR-0008 §1 |
| SERIOUS | COURSE-SER-08 | Assign or remove `stale-staging` and `semantic-recall-recall-at-k` |
| SERIOUS | COURSE-SER-09 | Renumber PHASE-5; assign REQ-IDs to scope items |
| PROCESS | COURSE-PROC-10 | ADR clarifying amendment-vs-supersession policy for ADRs themselves |
| PROCESS | COURSE-PROC-11 | Widen REQ-ARCH set for cross-document consistency |
| PROCESS | COURSE-PROC-12 | Define or delete `Material-Architecture-Change: true` |

**Change scope classification:** MAJOR. Four CRITICAL findings touch ARCHITECTURE.md, two ADRs, two phase files, and the REQ-ARCH set. Recommended handoff: an Architect-led CHG that opens ADR-0009 (BMAD integration, native Skills, supersedes ADR-0002), bundles the path sweep, widens REQ-ARCH-0008 or adds REQ-ARCH-0009, and lands a single PR before any PHASE-0 work attempts to close green. Subsequent CHGs (one per SERIOUS, one per PROCESS) can land sequentially. Doing this before PHASE-1 begins is materially cheaper than threading the fixes through phase work already in flight.
