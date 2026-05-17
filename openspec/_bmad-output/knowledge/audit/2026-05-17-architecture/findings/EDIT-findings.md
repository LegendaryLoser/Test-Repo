# EDIT — edit-prd (opus) — Wave 3

**Source transcript:** [`raw-transcripts/EDIT-agent-a8dad88abd4233ac9.jsonl`](../raw-transcripts/EDIT-agent-a8dad88abd4233ac9.jsonl)
**Sub-agent description:** `Edit-PRD architecture-as-document`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a8dad88abd4233ac9`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-edit-prd` skill via the Skill tool. Apply it to the architecture artifact — treating the 15 documents as a single multi-part PRD that needs editing.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

The skill's normal output is proposed edits. For this review, INSTEAD output the *defects you would have to fix* if asked to edit — without making the edits. Each defect is a finding.

Focus areas an editor would catch:
- Sections that can't be edited without breaking cross-references elsewhere
- Sentences that conflict with sentences in another document
- Examples that don't illustrate the rule they're attached to
- Definitions that are circular (term A defined using term B defined using term A)
- Conclusions that don't follow from premises within the document
- Promises in the abstract that the body doesn't deliver
- Sections that are clearly post-hoc rationalizations (smell test)
- Where an editor would refuse to ship without a rewrite

REQUIRED OUTPUT:
- Stable IDs: prefix `EDIT-` (e.g. EDIT-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 12 findings
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have read all 15 documents. Now I'll produce the editor's defect findings as instructed.

---

# Editor Defect Findings — Architecture Artifact (15 documents)

## CRITICAL — Cannot ship without rewrite

### EDIT-CRIT-01 — Layout diagram contradicts itself within a single section
`ARCHITECTURE.md` §3 shows `.claude/agents/` and `.claude/commands/` as "legacy slot — empty in v6 native-skills model," and yet §9 (Workflow surface) says "Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by file path…" These two statements are mutually exclusive: either the directories are empty legacy slots, or they hold the wrappers that constitute the workflow surface. Both cannot be edited without touching the other. An editor cannot resolve §9 without rewriting §3, and the rewrite cascades into ADR-0002 (which itself was rewritten in Amendment 0001 specifically to delete the wrapper model) and into PHASE-1 scope item 4, which still says "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA) and core commands." A reviewer would refuse to ship the artifact until §9 is rewritten to match the post-Amendment-0001 native-skills model.

### EDIT-CRIT-02 — Phase scope contradicts its own dependency ordering
`PHASE-0` §Scope item 12 explicitly states "`bmad/` is **not** installed in PHASE-0; it lands in PHASE-1." `PHASE-1` Scope item 3 says "`bmad/` installation per ADR-0002, pinned in `bmad/config.yaml`." But `ARCHITECTURE.md` §3 shows the install path as `_bmad/` (underscore-prefixed), and ADR-0002 §Decision item 2 declares "Install path: `_bmad/` (underscore-prefixed, per upstream's convention)." PHASE-0 and PHASE-1 both still use the legacy `bmad/` path. An editor cannot fix the PHASE-1 file without also fixing the directory the file references, and the pin file (`bmad/config.yaml` vs. `_bmad/_config/manifest.yaml`) is named differently in each document. This is a critical cross-reference defect across three files.

### EDIT-CRIT-03 — Promised content not delivered: "the paper"
`ARCHITECTURE.md` §2 promises constraints from "a published result on transformer associative memory (referred to throughout as 'the paper')," and ADR-0004 §Context elaborates on the paper's four properties. Nowhere is the paper cited — no title, no authors, no DOI, no URL, no reference list. The principle in ARCHITECTURE.md §1 #2 ("Stochastic systems get statistical assertions") is allegedly derived from it; ADR-0004 §4 ("Anti-aliasing") references its "δ-convex lures." An editor cannot ship a load-bearing premise with no source. This is unfalsifiable as written and any reviewer would block the merge.

### EDIT-CRIT-04 — Circular definition of "the matrix" vs. "the truth"
`ARCHITECTURE.md` §7 defines the matrix as a "derived cache, never hand-edited," with truth = "journals + git + specs + tests." ADR-0005 §2 says the same. But ADR-0005 §1 lists "Session journals" as a source of truth, and §6 declares that the journal is *written by hooks* `journal_commit.py`, `journal_touch.py`, `journal_tests.py` — which derive their content from… commits, file touches, and test runs. The journal is therefore a derived cache of the same underlying actions as the matrix, yet it is declared the truth. The definition is circular: "matrix is derived from journal" + "journal is derived from the actions the matrix also observes" + "matrix can be regenerated from sources" — but the sources include the journal which is itself derivative. An editor cannot rewrite §7 without untangling §1 and §6 of ADR-0005.

### EDIT-CRIT-05 — ADR-0002 amendment narrative is post-hoc rationalization
ADR-0002 §Context states "The original ADR text designed a wrapper-isolation strategy based on outdated assumptions about BMAD exposing personas as Claude Code subagents — that turned out to be neither how BMAD v6 works nor necessary, since native Skills are a better-engineered alternative we couldn't have improved upon." The amendment log row 0001 then says "Complete rewrite to match BMAD v6.6.0 empirical reality." This fails the smell test on multiple grounds: (a) an ADR that has been *completely rewritten* is no longer the same decision, it is a new decision — supersession is mandatory per ADR-0004 §1's identifier immutability rule, which ADR-0002 violates; (b) the phrase "we couldn't have improved upon" is editorial puffery, not architectural reasoning; (c) the original wrapper-isolation design is invoked in `ARCHITECTURE.md` §9 and `PHASE-1` Scope item 4, both of which still reflect the *pre*-amendment ADR. An editor would force this to be a new ADR (ADR-0009 superseding ADR-0002) rather than a rewrite-in-place.

### EDIT-CRIT-06 — Push invariant amendment introduces an unenforceable safety claim
ADR-0005 §6 (added in amendment 0001) claims a "push invariant: every operation that mutates the commit graph or moves a branch pointer must result in origin tracking the post-state within the same hook firing." It then immediately concedes "the invariant is otherwise unenforceable and silently rots." §8's failure table explicitly notes "residual loss only if both hooks fail to fire (e.g. abrupt container reclaim mid-`PostToolUse`)." The "invariant" is therefore not an invariant; it is a best-effort policy. The CLAUDE.md operating principles section says "A principle without a CI gate is a build failure" (citing ADR-0008), yet there is no gate listed in ADR-0008 §1 named `push-invariant` or similar — only hooks, which fire client-side. An editor would either rename it ("push policy") or demand a gate. Shipping it as an "invariant" is misleading.

### EDIT-CRIT-07 — REQ-ARCH-0008 is undermined by PHASE-0 §Scope item 9
`ARCHITECTURE.md` §10 REQ-ARCH-0008 says ".claude/settings.json is present; hooks declared in ADR-0005 are listed (implementations land in PHASE-2)." This is consistent with PHASE-0 §Scope item 9 which says hooks "point at placeholder commands that exit 0 with a TODO comment." But ADR-0005 §6 amendment 0001 adds two new hooks (`PostToolUse(mcp__github__merge_pull_request)` and the extended `Stop/SessionEnd` push behavior) without updating REQ-ARCH-0008's wording to account for the moving target. Worse, the test for REQ-ARCH-0008 (referenced in PHASE-0 as `tools/ci/tests/test_phase0.py`) would need to know which hooks were declared as-of which amendment date; the REQ is silent on amendment-tracking. An editor must rewrite REQ-ARCH-0008 to state the verification rule precisely ("settings.json declares exactly the hooks in the current revision of ADR-0005 §6") or accept that the REQ is unverifiable.

## SERIOUS — Substantive defects that block clean editing

### EDIT-SER-01 — Example illustrates the wrong rule
ADR-0004 §2 lists three forbidden patterns under `prose-xref-banned`:

```
the auth spec
the login requirement
the original ADR
```

The third example, "the original ADR," fires inside ADR-0002 §Context, which uses the phrase "The original ADR text designed a wrapper-isolation strategy." This is not just a coincidence — it is a textbook instance of the very pattern ADR-0004 forbids. An editor cannot leave the example as written without flagging that the rule, if it were running, would block ADR-0002. Either the example must change or ADR-0002 must.

### EDIT-SER-02 — Branch name leaks operational state into an immutable artifact
`PHASE-0` §Entry criteria item 2 states "Branch `claude/general-session-KXgas` exists." ADR-0005 amendment-log entry 0001 also cites "a real divergence observed on `claude/general-session-KXgas` after PR #2 merged." A phase entry criterion that references a specific session branch name is not portable — anyone restarting the phase from a fresh clone on a different branch name fails entry. An editor would have to rewrite the entry criterion in branch-agnostic terms, but doing so disconnects it from the historical ADR-0005 narrative.

### EDIT-SER-03 — Section numbering in ADR-0002 jumps without warning
ADR-0002 numbers its Decision block 1–7, then begins a new top-level section called "## 7. Staging discipline for `openspec/_bmad-output/`." This second §7 is a *different* §7 from item 7 in the Decision block. An editor reading "see §7" elsewhere in the file cannot disambiguate. The same defect occurs at §8 and §9. ADR-0002 §Compliance cites "(§7)" and "(§8)" and "(§9)" in the Consequences without disambiguation. An editor would have to renumber every section and audit every cross-reference, including the ones from PHASE-2 and PHASE-5 ("`ADR-0002` §7", "`ADR-0002` §8", "`ADR-0002` §9").

### EDIT-SER-04 — Conclusions overshoot their premises in ADR-0002 §Consequences
ADR-0002 §Consequences ends with "**Per-project isolation works via BMAD's standard config merge** — upgrade-resistant, no custom code needed." Yet ADR-0002 §9 itself admits "This isolation is reliable today — verified against the vendored BMAD source. It is *not yet exercised* (no projects exist); first exercise lands in PHASE-5." The Consequences section asserts what §9 explicitly downgrades to "verified but not exercised." An editor either weakens the Consequences claim or strengthens §9, but cannot ship both.

### EDIT-SER-05 — ADR-0006 §4 redefines a term ADR-0005 already defined
ADR-0006 §4 introduces "Bulk green-starts (e.g. importing a battery of passing tests in one commit) require a `Bootstrap: <reason>` trailer." This is a *new* mandatory commit trailer not listed in ADR-0005 §3's exhaustive trailer schema ("Task / Requirements / Tests-Status / Phase" plus the optional `Checkpoint: true`). ADR-0008 §6 lists `Checkpoint: true` as "the **only** sanctioned partial-bypass" — but `Bootstrap:` is also a partial-bypass mechanism for the red-before-green gate. The two ADRs contradict each other on the trailer schema. An editor cannot reconcile without amending one.

### EDIT-SER-06 — ADR-0006 §2 "Permitted, narrowly" silently introduces a forbidden category
ADR-0006 §2 bans `monkeypatch.setattr` on in-repo modules, but the "Permitted" subsection allows "Substituting **clock** and **randomness sources** through real adapters." This is fine in principle, but the prose adds "a deterministic clock implementation that is itself production code." A deterministic clock used "in both prod and test paths" violates principle P2 from ARCHITECTURE.md §1 ("Determinism is never manufactured by seeding for systems that are not deterministic in production"). The clock-in-production-is-deterministic carve-out is unargued; an editor would have to either justify it or strike it.

### EDIT-SER-07 — Audit interface promises capabilities the data sources don't support
ADR-0005 §9 says `audit STORY-NNNN` returns "REQs, tests, completion %." Stories are defined in `ARCHITECTURE.md` §4 with canonical home `openspec/stories/STORY-<NNNN>.md`. ADR-0005's data sources (§1) are git, spec files, test annotations, and journals — none of which contains a Story → REQ mapping. ADR-0004's spec frontmatter (§5) does include `references.story` per REQ, so reverse lookup is possible, but "completion %" requires an authoritative Story-acceptance schema that does not exist in any of the 15 documents. The promised audit answer cannot be computed from the declared sources. An editor must either delete the promise or add the schema.

### EDIT-SER-08 — Reconciliation gate (ARCHITECTURE.md §5) doesn't follow from premises
`ARCHITECTURE.md` §5 says "`EPIC.status = ready-for-dev` requires: PM rationale present; Architect approval present; ≥1 Story decomposed with REQ-IDs; every covering REQ has TEA-authored failing tests." This is the *output* of a reconciliation gate, but the Epic schema is not specified anywhere in the 15 documents — there is no template, no frontmatter spec, no field list for `EPIC.status` values, no `coverage:` block schema. Compare to ADR-0004 §5, which gives the full REQ block in detail. An editor cannot validate that the gate is implementable without the schema, and shipping a load-bearing claim about Epic structure with no schema is a hole.

### EDIT-SER-09 — PHASE-5 scope numbering is broken
PHASE-5 §Scope lists items 1, 2, 3, 4, 4, 5, 6 — two consecutive items numbered 4 (one for "Per-project BMAD output isolation" and one for "Test suite across all four tiers"). This is a basic editorial defect, but it has downstream consequences: cross-references "PHASE-5 scope item 4" become ambiguous, and any traceability matrix entry pointing at PHASE-5 task 4 cannot disambiguate. An editor cannot fix without renumbering and re-running every reference.

### EDIT-SER-10 — Test ID format inconsistent across documents
ARCHITECTURE.md §4 table gives `TEST-<DOMAIN>-<NNNN>` as the Test ID format. ADR-0005 §3 trailer block does not list test IDs in trailers. ADR-0006 §6 says "Every test is annotated with `@test-id TEST-<DOMAIN>-<NNNN>`." But ADR-0005 §1 sub-item 3 says tests declare "`@test-id TEST-X-NNNN`" — a different placeholder (`X` not `DOMAIN`). The cross-document inconsistency would block a lint rule that tries to enforce the format. An editor must converge on one placeholder.

## PROCESS — Process / structural defects an editor would flag

### EDIT-PROC-01 — Status field semantics undefined
Every ADR carries `status: accepted`; phase files carry `status: in-progress` (PHASE-0) or `status: pending` (PHASE-1..5). Nowhere in the 15 documents is the enumeration of legal `status` values defined for ADRs or phases. ADR-0004 §5 defines REQ statuses ("draft | tests-red | tests-green | reviewed | merged | deprecated"), but ADRs and phases use a separate vocabulary that is undocumented. An editor cannot validate the field without knowing the legal set.

### EDIT-PROC-02 — Amendment log is invented per-ADR, not standardized
ADR-0002 has an "Amendment log" with rows 0001 and 0002. ADR-0005 has an "Amendment log" with row 0001. Other ADRs (0001, 0003, 0004, 0006, 0007, 0008) have *no* amendment log section at all. There is no master rule saying every ADR shall have an amendment log; there is no rule saying it shall be section §N. An editor adding an amendment to ADR-0004 cannot know whether to add a §-numbered section or a trailing block. The convention is undocumented and inconsistent.

### EDIT-PROC-03 — Verbatim-quoting requirement is unverifiable
REQ-ARCH-0007 requires "root `CLAUDE.md` cites the five principles in §1 verbatim." CLAUDE.md (per the project-instructions header) lists five principles. Comparing them to ARCHITECTURE.md §1 reveals they are paraphrased, not verbatim: ARCHITECTURE.md principle 1 reads "Single source of truth (SoT). One canonical home per fact. Cross-document consistency is lintable." CLAUDE.md principle 1 reads "Single source of truth (SoT). One canonical home per fact. Cross-document consistency is lintable." These appear identical here, but CLAUDE.md adds a heading style ("Operating principles (verbatim, in priority order)") and inserts an instruction ("A principle without a CI gate is a build failure") that is not in ARCHITECTURE.md §1. An editor would have to either weaken REQ-ARCH-0007 to "paraphrases" or excise the extra prose from CLAUDE.md.

### EDIT-PROC-04 — Cross-reference syntax is itself a lintable prose-xref
ADR-0004 §2 requires cross-references in the form "`REQ-SPEC-0001 @ openspec/specs/_meta/spec-storage.spec.md`." Yet ARCHITECTURE.md §10 REQ-ARCH-0002 lists "ADR-0001 through ADR-0008 plus PHASE-0 through PHASE-5" — a *range* expression. Ranges with "through" are arguably prose references because they don't enumerate explicit file paths. Similarly, ARCHITECTURE.md §1 cites "see ADR-0008" without the ID+path form. An editor must either tighten the rule or strike the range syntax across the corpus.

### EDIT-PROC-05 — Date semantics for ADRs and phase exits are absent
Every ADR carries `date: 2026-05-16`. Today's date is 2026-05-17 (per the project context). Phase entry criteria refer to "PHASE-N exit gate passed" without a date — there is no rule preventing phase work from beginning *before* the prior phase's gate, only a CI gate that prevents merge. An editor cannot determine whether the dates on ADRs are creation dates, acceptance dates, or last-edit dates; the field is undocumented. Given Amendment 0001 in ADR-0002 was a complete rewrite, the `date` of 2026-05-16 may be misleading.

### EDIT-PROC-06 — Gate inventory in ADR-0008 §1 conflicts with phase scope
ADR-0008 §1 lists `skill-removal-acknowledged` neither in the gate table nor in §3 phase-exit logic, yet PHASE-2 §Scope item 4 lists "`skill-removal-acknowledged` gate per `ADR-0002` §8" as a deliverable. Likewise PHASE-2 introduces `bmad-version-pin` and `bmad-smoke-test` gates that ADR-0008's "every gate" inventory does not contain. ADR-0008 §2 "gate-coverage" gate claims to walk every ADR and verify a gate references it — under that rule, ADR-0002 §8's amendment-introduced gates would fail gate-coverage on the day ADR-0008 is read in isolation. An editor must update ADR-0008's gate inventory to keep it the SoT it claims to be.

### EDIT-PROC-07 — "Single source of truth" is violated by the artifact about SoT
P1 in ARCHITECTURE.md §1 is "Single source of truth (SoT). One canonical home per fact." Yet the failure-mode table appears in *two* places: ARCHITECTURE.md §8 and ADR-0005 §8. The two tables overlap in rows ("Crash mid-Edit/Write", "Crash mid-commit", "Container reclaim, push succeeded", "Container reclaim, uncommitted") but use slightly different wording — ARCHITECTURE.md §8 says "push completed" where ADR-0005 §8 says "push succeeded." This is precisely the "near-duplicate specification" pattern ADR-0004 §4 forbids. An editor would have to delete one table and replace it with a one-line reference, or accept that the document violates its own most-cited principle.
