# INHER2 — inheritor-framing (sonnet) — Wave 4

**Source transcript:** [`raw-transcripts/INHER2-agent-ab662e321df46151f.jsonl`](../raw-transcripts/INHER2-agent-ab662e321df46151f.jsonl)
**Sub-agent description:** `Inheritor framing sonnet`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `ab662e321df46151f`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Take a specific framing: you are a senior engineer joining this project 2 years from now. The original authors have all left. Your task is to ship the first new feature. Read the documents and identify what would prevent you (the inheritor) from doing your job without re-asking the original team.

Documents (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md, decisions/ADR-0001 through ADR-0008, phases/PHASE-0 through PHASE-5

Inheritor questions: if a rule says "reviewed quarterly (a `gate`-type task)" but the task type isn't defined, what do I do? If two ADRs disagree about a file path, which wins? If a gate is named in a phase but not in the gate inventory, do I trust the phase? If `tools/spec_lint allocate` is referenced but missing, do I hand-allocate or build the tool? If the architecture is "frozen" but PHASE-0 is "in-progress", which timestamp is the freeze date?

REQUIRED OUTPUT:
- IDs prefix `INHER2-` (CRIT/SER/PROC inline based on whether inheritor is blocked, slowed, or annoyed)
- Minimum 15 findings
- First-person inheritor voice ("I cannot tell whether...", "I would have to assume...")
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I now have all 15 documents. Here is the inheritor review.

---

**INHER2-0001 [CRIT] — The architecture is simultaneously "frozen" and PHASE-0 is "in-progress": I cannot establish a valid starting state.**

ARCHITECTURE.md line 13 states this document and its ADRs constitute "the frozen architecture artifact." PHASE-0's frontmatter declares `status: in-progress`. Those two facts cannot coexist without a timestamp or a definition of what "frozen" means relative to a phase that has not exited. I would have to assume one of three things: (a) "frozen" refers only to the document's structure, not the repo's state; (b) PHASE-0 has been completed but its status field was never updated; (c) the architecture was written speculatively and no real implementation exists. All three lead to different starting actions. I cannot tell which is true without asking a human, and there is no human to ask.

---

**INHER2-0002 [CRIT] — The `gate`-type task is used but never defined anywhere in these 15 documents.**

ADR-0004 §4 says the anti-aliasing threshold is "reviewed quarterly (a `gate`-type task)." ARCHITECTURE.md §11 says "The phase exit ADR is a `gate`-type task." ADR-0003 §4 says promotion from `dev` to `prod` occurs "only on a merged `gate`-type task." But no document defines what a `gate`-type task is: what its frontmatter looks like, where it lives, how it differs from any other task under `openspec/changes/<CHG>/tasks/`, what workflow it triggers, or what approvals it requires. I cannot execute a prod promotion, a quarterly threshold review, or a phase exit without knowing what artefact I am supposed to produce.

---

**INHER2-0003 [CRIT] — `tools/spec_lint allocate` is referenced but the tool does not exist; no guidance covers the interim.**

ADR-0004 §1 states: "Identifier allocation is by `tools/spec_lint allocate <domain>` against `openspec/specs/INDEX.yaml`. Hand-allocation is permitted but checked." The tool is defined as PHASE-1 work. PHASE-0 is `in-progress`, so the tool may never have been built. The fallback "hand-allocation is permitted" is immediately followed by "but checked" — checked by what, if the tool does not exist? I would have to hand-allocate IDs and accept that no gate will verify them until PHASE-1 ships. That creates a window where I silently introduce duplicate or mis-formatted IDs that will fail later. The word "checked" does not tell me the check mechanism when the tool is absent.

---

**INHER2-0004 [CRIT] — Two documents disagree on the BMAD install path.**

ADR-0002 Amendment 0001 explicitly states the install path changed from `bmad/` to `_bmad/` (underscore-prefixed). PHASE-1's scope item 3 says "bmad/ installation per ADR-0002." PHASE-1 was written with the old path. ADR-0001's layout section also lists `bmad/` (no underscore) in the rules prose ("bmad/ is the BMAD installation"). ARCHITECTURE.md §3 shows `_bmad/` in the directory tree. Three documents say `_bmad/`, two documents say `bmad/`. If I follow PHASE-1 as written, I create `bmad/`, which fails the `top-level-allowlist` gate that is also defined in PHASE-1. I cannot follow both documents simultaneously.

---

**INHER2-0005 [CRIT] — PHASE-1 scope item 4 references `.claude/agents/` and `.claude/commands/` wrappers for BMAD personas, but ADR-0002 explicitly says those slots are empty in the v6 native-skills model.**

PHASE-1 §4 says: "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA) and core commands." ADR-0002 Amendment 0001 says the wrapper-isolation strategy was dropped because "native Skills are a better-engineered alternative." ARCHITECTURE.md §3 labels both directories "(legacy slot — empty in v6 native-skills model)." If I execute PHASE-1 as written I create wrapper files in directories the architecture says must be empty. If I skip step 4, I deviate from the phase scope without an ADR amendment. There is no path that satisfies both documents.

---

**INHER2-0006 [CRIT] — The `gate-coverage` gate checks that every gate in the inventory references every ADR and every principle, but several gates in ADR-0008 §1 are gated on PHASE-2 delivery — meaning `gate-coverage` itself cannot pass until PHASE-2 ships, yet `gate-coverage` runs on every PR starting from PHASE-0.**

ADR-0008 §2 says "`gate-coverage` walks every ADR and every principle … A missing reference fails the build." ADR-0008 §1 lists 26 gates; many are implemented in PHASE-1 and PHASE-2. PHASE-0 commits "workflow YAML stubs (jobs declared, scripts as TODO)." If `gate-coverage` runs on every PR and it checks that all ADR-referenced gates exist in the table, it would fail every PHASE-0 PR because the gate implementations are TODO placeholders. Either `gate-coverage` has a phase-aware carve-out (undefined), or every PHASE-0 PR is broken by design, or the gate only runs when implementations exist (contradicting "every PR"). I cannot determine which.

---

**INHER2-0007 [CRIT] — The `checkpoint_exemptions.yaml` file is referenced but never specified.**

ADR-0008 §6 states: "The `Checkpoint: true` trailer … applies to a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`." No document lists what those gates are, what the file format is, or who may edit it. Since `tools/trace/` is a PHASE-2 deliverable, the file may not exist at all. I cannot know whether a checkpoint commit will block the `commit-trailers-valid` gate, the `red-before-green` gate, or others, without a source of truth for the exemption list.

---

**INHER2-0008 [SER] — A named gate appears in a phase but has no entry in the ADR-0008 gate inventory.**

PHASE-2 scope item 4 includes "bmad-version-pin gate" and "bmad-smoke-test" gate. ADR-0008 §1 does not list `bmad-version-pin` or `bmad-smoke-test` in the gate inventory table. The `gate-coverage` gate would therefore not know these gates exist and would not check that ADRs reference them. These gates are described in ADR-0002 §8 but are not wired into the canonical gate inventory. If I encounter a failing `bmad-version-pin` check I would have no way to find its canonical definition from the gate inventory — I would have to grep across all ADRs.

---

**INHER2-0009 [SER] — The `openspec/STATUS.md` that CLAUDE.md declares authoritative does not appear in the 15 specified documents and cannot be read per the task constraint; but CLAUDE.md instructs me to read it first as the "single authoritative session-resume document."**

CLAUDE.md § "How to start any session" step 1 says: "Read `openspec/STATUS.md` first. Single authoritative session-resume document: current CHG, open PRs, audit findings ledger, open architectural questions, sequenced roadmap, recent decisions, and 'next session: start here' pointer." That file is not among the 15 documents I was asked to review, and no phase document describes its format, who maintains it, or what happens if it is stale. If it does not exist or is outdated, I have no starting point. Its maintenance model ("Hand-maintained until PHASE-2's SessionStart resume hook mechanizes it") means it is purely human-dependent, and the humans have left.

---

**INHER2-0010 [SER] — No document defines what "the paper" is or provides a citation that survives without the original team.**

ARCHITECTURE.md §2 and ADR-0004 both refer to "the paper" as a "published result on transformer associative memory." The anti-aliasing thresholds in `tools/spec_lint/config.yaml` are explicitly derived from the paper's results, and the quarterly review of those thresholds is tied to re-reading the paper's implications. No title, author list, DOI, arXiv ID, or URL is given. Two years from now I cannot locate the paper to assess whether the n-gram threshold is still appropriate, whether there is a more recent result that supersedes it, or whether the quarterly threshold review has ever been done.

---

**INHER2-0011 [SER] — The scope of PHASE-0 (item 12) says BMAD is not installed in PHASE-0, but REQ-ARCH-0008 says hooks pointing at `tools/trace/` must be declared in PHASE-0, and `tools/trace/` is a PHASE-2 deliverable.**

PHASE-0 scope item 9 says `.claude/settings.json` contains "hook declarations pointing at placeholder commands that exit 0 with a TODO comment." REQ-ARCH-0008 exit criterion says "hooks declared in ADR-0005 are listed." ADR-0005 §6 lists seven hooks, all pointing at `tools/trace/*.py`. If PHASE-0 is still in-progress and all hooks are placeholder no-ops, then no commit in the repo has ever been validated by the `commit-trailers-valid` hook. That means any prior commits may lack the mandatory trailers, which means the moment I implement the real hook in PHASE-2 it will retroactively fail against history. The phase plan does not address this bootstrapping contradiction.

---

**INHER2-0012 [SER] — Two separate numbering schemes for PHASE-5 scope items (two items labeled "4") make the spec ambiguous.**

PHASE-5 scope has two consecutive items both numbered "4": the first is the per-project BMAD output isolation block; the second is "Test suite across all four tiers, each red-first." I cannot determine whether this is a drafting error or whether one item was intentionally renumbered and the other is a ghost. If the test-suite item (second "4") was meant to be item "5," then items 5 and 6 in the original plan are displaced and the PHASE-5 scope has six items, not five. This matters because exit-criteria reference the scope; a displaced item might be interpreted as out-of-scope.

---

**INHER2-0013 [SER] — The `stale-staging` gate is described as a "deferred CHG" but no CHG number is given, no phase is assigned, and no entry exists in the gate inventory.**

ADR-0002 §7 says: "A future spec_lint rule `stale-staging` (deferred CHG) flags drafts sitting unpromoted past a configurable threshold." ADR-0008 §1's gate inventory does not list `stale-staging`. No CHG number is cited. "Configurable threshold" is not defined anywhere. I cannot tell when this gate is supposed to land, whether it is my responsibility to create the CHG, or whether there is already an open CHG for it that I should search for. The gate-coverage gate would not catch its absence because it is not in the inventory.

---

**INHER2-0014 [PROC] — "Reviewed quarterly (a `gate`-type task)" for the anti-aliasing threshold has no calendar anchor, no review owner, and no record of prior reviews.**

ADR-0004 §4 requires the anti-aliasing threshold and n-gram size to be reviewed quarterly. There is no initial review date recorded in the document, no record of whether any quarterly review has ever occurred, and no designated owner role. Two years after the original team left, I have no way to determine whether the current thresholds in `tools/spec_lint/config.yaml` are still defensible. If I do a quarterly review, I have no template for what the review produces or how to record the outcome.

---

**INHER2-0015 [PROC] — The PHASE-1 exit criterion requires `bmad/config.yaml` to pin the BMAD version, but ADR-0002 specifies the canonical version source is `_bmad/_config/manifest.yaml`.**

PHASE-1 exit criterion says: "`bmad/config.yaml` pins v6 minor version." ADR-0002 §1 says: "Pinned in `_bmad/_config/manifest.yaml` at install time (canonical version source)." The file names and paths disagree. If I satisfy the PHASE-1 exit criterion by creating `bmad/config.yaml`, I create a file at the wrong path (under the old `bmad/` prefix) that also doesn't match what the `bmad-version-pin` gate in PHASE-2 checks (`scripts/install_bmad.sh` vs `_bmad/_config/manifest.yaml`). The exit criterion is stale relative to Amendment 0001 of ADR-0002 but was never updated.

---

**INHER2-0016 [PROC] — The `bulk-green-start` gate is referenced in ADR-0006 §4 but is absent from the ADR-0008 gate inventory.**

ADR-0006 §4 says: "CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." The value of N is not specified anywhere in these documents. ADR-0008 §1 does not list `bulk-green-start`. `gate-coverage` would therefore not detect its absence. I cannot know whether this gate was intentionally dropped, whether it is implied by `red-before-green`, or whether N was supposed to be defined in a config file that does not yet exist.

---

**INHER2-0017 [PROC] — The PHASE-1 exit criterion for BMAD wrapper resolution ("All BMAD wrapper files in `.claude/agents/` and `.claude/commands/` resolve their `Load:` paths") references a `Load:` field syntax that is never defined in any of these 15 documents.**

PHASE-1 exit criteria item 4 says wrapper files must "resolve their `Load:` paths." No document defines what a `Load:` field is, what format it takes, which tool resolves it, or what "resolves" means mechanically. This is particularly confusing because ADR-0002 Amendment 0001 says wrappers are no longer needed at all in the v6 native-skills model. The exit criterion references a concept from the abandoned wrapper strategy and applies it to files the architecture says should be empty.

---

**Summary of blocking issues for the inheritor attempting to ship the first feature:**

I cannot determine whether PHASE-0 is truly complete (INHER2-0001), which means I do not know if I am in PHASE-1 or still in PHASE-0. The BMAD path conflict (INHER2-0004) and the wrapper conflict (INHER2-0005) mean I cannot complete PHASE-1 without violating at least one document. The undefined `gate`-type task (INHER2-0002) means I cannot perform a phase exit or a prod promotion. The missing `tools/spec_lint` (INHER2-0003) means I cannot allocate IDs safely. Without resolving INHER2-0001, INHER2-0002, INHER2-0004, and INHER2-0005, I cannot advance to PHASE-2, which is a prerequisite for PHASE-3, which is a prerequisite for PHASE-5 — the phase that actually ships the first feature.
