# STRUCT — editorial-review-structure (opus) — Wave 1

**Source transcript:** [`raw-transcripts/STRUCT-agent-a503ec7eb147f2205.jsonl`](../raw-transcripts/STRUCT-agent-a503ec7eb147f2205.jsonl)
**Sub-agent description:** `Editorial structure review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a503ec7eb147f2205`

## Initial prompt to sub-agent

```
You are an isolated structural editor with no prior context. Invoke the `bmad-editorial-review-structure` skill via the Skill tool. Apply it to the architecture artifact: identify cuts, reorganizations, and simplifications that would preserve or improve comprehension. Focus on cases where the structure itself signals a deeper problem (e.g. a section that doesn't fit anywhere is usually a missing concept; a paragraph that repeats content in three places is usually a Single-Source-of-Truth violation in disguise).

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Specifically look for:
- Section-numbering anomalies (e.g. two §7s, missing §10, amendment sections wedged into the original section numbering)
- Concepts described in multiple documents with subtly different definitions
- Long enumerations that should be a table; tables that should be prose; prose that should be a separate document
- "Forward references" that need a concept defined later in the artifact to make sense
- Amendment-log conventions that differ between documents
- ADRs with no Compliance section, no Amendment-log section, no Consequences section — structural omissions
- Phase files whose scope/exit/entry pattern doesn't match siblings

REQUIRED OUTPUT:
- Stable IDs: prefix `STRUCT-` (e.g. STRUCT-01; severity inline as CRITICAL/SERIOUS/PROCESS based on impact)
- Each finding: file + section, structural problem, what it signals (often a deeper conceptual gap), proposed restructure
- Minimum 12 findings
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have a complete picture. Let me produce the structural review.

## Document Summary
- **Purpose:** Authoritative architecture artifact governing a monorepo: defines layout, principles, ADRs, and phased delivery contract.
- **Audience:** Engineering agents (human + LLM) resuming sessions, authoring code/specs, and enforcing CI gates.
- **Reader type:** humans (with strong LLM-agent secondary usage given CLAUDE.md routing)
- **Structure model:** Strategic/Context (Pyramid) for ARCHITECTURE.md and ADRs; Tutorial/Guide (Linear) with consistent schema for PHASE files (Reference/Database expectations).
- **Current length:** ~9,600 words across 15 files; 12 numbered top-level sections in ARCHITECTURE.md, 8 ADRs, 6 PHASE files.

## Recommendations

### STRUCT-01 [CRITICAL] - MOVE/RESTRUCTURE - ADR-0002 section numbering is broken; amendment sections (§7, §8, §9) wedged into the original Decision numbering
**File + section:** `/home/user/Test-Repo/openspec/architecture/decisions/ADR-0002-bmad-integration.md` — the seven numbered points in `## Decision` end at item 7 ("No project code depends on BMAD directly"), then the file jumps to `## 7. Staging discipline` (a sibling `##` heading), `## 8. Upgrade safeguards`, `## 9. Per-project output isolation`. There are now **two §7s** (one inside Decision, one as a top-level header) and the amendment-introduced sections sit between `## Decision` and `## Consequences`, breaking the standard ADR schema.
**What it signals:** A deeper SoT defect — Amendment 0002 added material *decisions* but pretended they were standalone sections rather than admitting they belong **inside** `## Decision`. The structure encodes "these are afterthoughts," but the Compliance section and Consequences section both reference them as first-class decisions. The amendment log claims they were added; the structure denies it.
**Proposed restructure:** Renumber the amendment-added sections as Decision items 8, 9, 10 (continuing the existing Decision enumeration). Move them physically inside `## Decision`. Keep the cross-references in Consequences and Compliance pointing at "Decision §8/§9/§10". This restores the canonical ADR schema (Context → Decision → Consequences → Compliance → Amendment log) and eliminates the ambiguous "§7" reference (which currently could mean either of two §7s).

### STRUCT-02 [CRITICAL] - QUESTION/CUT - Two parallel BMAD install-path conventions co-exist across documents
**File + section:** `ARCHITECTURE.md §3` shows `_bmad/` (underscore-prefixed) in the layout tree. `ADR-0002 §2` confirms `_bmad/` ("was `bmad/`" per amendment 0001). But `PHASE-1-spec-hygiene.md` Scope item 3 still says `bmad/` (no underscore), and item 3 references `bmad/config.yaml`; the Exit criteria say `bmad/config.yaml pins v6 minor version`. `ADR-0001` Rules item 4 says `bmad/` (no underscore). `ARCHITECTURE.md §9` says "BMAD agents live under `bmad/`".
**What it signals:** A Single-Source-of-Truth violation — the rename happened in ADR-0002 amendment 0001 but the cross-document consistency lint that ADR-0004 promises does not yet exist, so `ARCHITECTURE.md §9`, `ADR-0001` §3 (Rules item 4), and `PHASE-1` were left stale. The structure (one fact in three places) guarantees this drift.
**Proposed restructure:** Pick one canonical home for the install-path fact (ADR-0002 §2, since that is where the version pin and install command live). Replace every other mention with a stable reference (`see ADR-0002 §2 @ openspec/architecture/decisions/ADR-0002-bmad-integration.md`). Update the three stale prose mentions to `_bmad/`. Add a `path-drift-lint` row to the ADR-0008 gate table.

### STRUCT-03 [CRITICAL] - MOVE/MERGE - ARCHITECTURE.md §7 and §8 are stubs that repeat ADR-0005; ADR-0005 §8 repeats ARCHITECTURE.md §8
**File + section:** `ARCHITECTURE.md §7 Traceability` and `§8 Session persistence` are each ~6-line summaries that say "Defined in full in ADR-0005" then reproduce the failure-mode table from ADR-0005 §8 (almost verbatim). ADR-0005 §8 is the same table with minor wording differences.
**What it signals:** Classic SoT violation in disguise — the architecture document tried to be a "narrative overview" while the ADR is the "detail." Both end up restating the same table, with subtle divergences (the ARCHITECTURE.md table omits the post-amendment row "Container reclaim, committed but unpushed" that ADR-0005 §8 added). When the ADR was amended, the architecture overview rotted.
**Proposed restructure:** Reduce ARCHITECTURE.md §7 and §8 to a single sentence each, pointing to `ADR-0005 @ openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md §2` and `§8` respectively. Delete the failure-mode table from ARCHITECTURE.md entirely. The "narrative overview" desire is satisfied by §1 (operating principles) and §4 (atomic units table); detailed contracts belong in their ADR.

### STRUCT-04 [SERIOUS] - QUESTION - Inconsistent amendment-log conventions across ADRs
**File + section:** ADR-0002 has `## Amendment log` with two rows (0001, 0002). ADR-0005 has `## 10. Amendment log` — numbered as a Decision sub-section. ADR-0001, ADR-0003, ADR-0004, ADR-0006, ADR-0007, ADR-0008 have **no Amendment log section at all** (none has been amended, but the schema is silently absent).
**What it signals:** No fixed ADR template exists, despite ADR-0004 prescribing strict spec discipline. The architecture promises structural consistency but its own schema for ADRs is unwritten.
**Proposed restructure:** Either (a) define an ADR schema explicitly in ADR-0004 (or a new ADR-0009 "ADR schema") with required sections: `Context → Decision → Consequences → Compliance → Amendment log` (latter empty until first amendment); or (b) state in CLAUDE.md/ARCHITECTURE.md that the schema is the union of sections seen across ADRs. Apply identically: ADR-0005 §10 should be `## Amendment log` (un-numbered, sibling to Compliance) — matching ADR-0002. All six un-amended ADRs should carry an empty `## Amendment log` heading so the schema is visible.

### STRUCT-05 [SERIOUS] - MOVE - Push invariant defined in ADR-0005 §6 amendment but referenced in body before amendment log
**File + section:** `ADR-0005 §6` ends with a paragraph "**Push invariant** (introduced by amendment, see §10): every operation that mutates the commit graph...". This paragraph is a forward reference to §10 (Amendment log) to explain why §6 has the content it has.
**What it signals:** The amendment log is acting as both audit trail *and* normative reference. Readers must jump to §10 to understand why the table in §6 contains certain rows. This is a structural admission that amendments are first-class decisions, not addenda — same defect as STRUCT-01.
**Proposed restructure:** Promote the "Push invariant" paragraph into its own numbered sub-section in `## Decision` (e.g. §6a or renumber to §7 with the existing §7 "Checkpoint commits" becoming §8, etc.). The amendment-log row stays for historical attribution but does not need to be cross-referenced in normative content. Same fix as STRUCT-01 but for ADR-0005.

### STRUCT-06 [SERIOUS] - CONDENSE - ARCHITECTURE.md §3 top-level layout tree is a 60-line ASCII tree that duplicates content from multiple ADRs
**File + section:** `ARCHITECTURE.md §3` shows the layout with inline comments (`# tracked; enforced by 'top-level-allowlist'`, `# (legacy slot — empty in v6 native-skills model)`, `# see ADR-0002 amendment 0001`, `# STAGING — BMAD drafts; non-authoritative; see ADR-0002 §7`).
**What it signals:** The layout tree is the single source of truth (per the layout-rationale link to ADR-0001), but inline comments encode information owned by other ADRs (BMAD vendoring, staging discipline, enforcement). When ADR-0002 was amended, the comments needed updating in two places.
**Proposed restructure:** Strip inline rationale comments from the tree — leave only the directory/file names. Move the rationale into ADR-0001's `## Decision` section as a table (path → owner-ADR → enforcement-gate). The tree is *layout*; the ownership/enforcement annotations are *governance* — different documents.

### STRUCT-07 [SERIOUS] - MOVE - ARCHITECTURE.md §10 "Architecture requirements" should live in a spec file, not in ARCHITECTURE.md
**File + section:** `ARCHITECTURE.md §10` enumerates `REQ-ARCH-0001` through `REQ-ARCH-0008`. The atomic-units table in §4 says the canonical home for `REQ-ARCH-*` is "ARCHITECTURE.md §10". But ADR-0004 §5 prescribes a strict spec format (frontmatter, Description, Acceptance, Non-acceptance, Notes) and §6 says `INDEX.yaml` is the sole retrieval surface — but `REQ-ARCH-*` REQs are listed in prose bullets that violate the prescribed format.
**What it signals:** Self-contradiction. The architecture exempts itself from its own spec-storage discipline (ADR-0004) by storing its requirements in markdown bullets rather than the YAML-frontmatter-per-REQ format prescribed for every other domain.
**Proposed restructure:** Move the eight REQ-ARCH-* into `openspec/specs/_meta/architecture.spec.md` using the ADR-0004 §5 format. ARCHITECTURE.md §10 becomes a one-line pointer with the list of IDs. Update the §4 atomic-units table entry for "Architecture req" to point at the new canonical home.

### STRUCT-08 [SERIOUS] - CUT - ARCHITECTURE.md §12 "What is *not* in this document" is anti-pattern
**File + section:** `ARCHITECTURE.md §12` lists three bullets: "product vision is empty", "code lands in PHASE-0–5", "decisions not captured in an ADR aren't decided".
**What it signals:** Negation-by-enumeration is a structural smell — each bullet is already established earlier (product separation in the intro paragraph; phasing in §11; ADR-as-only-decision-vehicle is implicit in the ADR convention). A "what is not in this document" section indicates the author wasn't sure §11 was conclusive.
**Proposed restructure:** Cut §12 entirely. Move bullet 1 to the intro paragraph (already mostly there). Move bullet 3 to §1 (operating principles) or to a new sentence near §11. Bullet 2 is redundant with §11's phase table.

### STRUCT-09 [SERIOUS] - CONDENSE - Operating principles enumerated verbatim in three places (ARCHITECTURE.md §1, CLAUDE.md, REQ-ARCH-0007 requires verbatim citation)
**File + section:** `ARCHITECTURE.md §1` lists the five principles. `CLAUDE.md` (per the system reminder) re-lists them verbatim. `REQ-ARCH-0007` requires `CLAUDE.md` to cite them verbatim.
**What it signals:** Three places hold the same numbered list. The verbatim-citation requirement is a workaround for not having a single source. When a principle is rephrased, three files drift.
**Proposed restructure:** Designate ARCHITECTURE.md §1 as SoT. CLAUDE.md replaces the verbatim list with a one-line pointer + an imported list (the SessionStart hook prints it at session start, per PHASE-2). `REQ-ARCH-0007` becomes "CLAUDE.md references ARCHITECTURE.md §1 by stable path". If a hook can't yet import, generate CLAUDE.md mechanically from ARCHITECTURE.md §1 — and lint that they match (this lint would also enforce STRUCT-02-style consistency).

### STRUCT-10 [SERIOUS] - MOVE - PHASE-5 Scope has two "item 4"s (duplicate numbering)
**File + section:** `PHASE-5-first-appscript-project.md` `## Scope` lists items 1, 2, 3, 4 (BMAD output isolation), then `4. Test suite across all four tiers, each red-first.`, then 5, 6. There are two `4.` entries.
**What it signals:** PHASE-5 was edited to add the BMAD output-isolation block (item 4) without renumbering subsequent items. The structural error means any reference to "PHASE-5 Scope item 4" is ambiguous.
**Proposed restructure:** Renumber the second `4.` to `5.` and bump subsequent items. Add a stable-ID convention for phase scope items (e.g. `SCOPE-5.4`) so future references are deterministic — matching the architecture's broader stable-ID discipline.

### STRUCT-11 [PROCESS] - PRESERVE/QUESTION - Phase file schema inconsistencies
**File + section:** Compare phase file structures: PHASE-0 has `Goal → Entry → Scope → Exit → Out of scope → Exit gate`; PHASE-1 follows the same; PHASE-2 follows the same; PHASE-3 follows the same; PHASE-4 follows the same; PHASE-5 follows the same. The schema is consistent across all six, but `Entry criteria` content varies — PHASE-0 lists two bullets ("Repository has only README.md", "Branch claude/general-session-KXgas exists"), while PHASE-1–5 each have one bullet ("PHASE-N-1 exit gate passed").
**What it signals:** Schema is structurally consistent. But PHASE-0 leaks a branch name into Entry criteria — a session-specific detail in a frozen architecture artifact. Branch names belong in `STATUS.md`, not in a phase file.
**Proposed restructure:** Remove the branch-name bullet from PHASE-0 Entry criteria. Move it to `STATUS.md` (referenced in CLAUDE.md as the session-resume document). Phase files are frozen substrate; STATUS.md is the live ledger.

### STRUCT-12 [SERIOUS] - MERGE - ARCHITECTURE.md §5 "Spec sourcing" diagram restates Epic reconciliation gate prose already in ADR-0008
**File + section:** `ARCHITECTURE.md §5` has an ASCII diagram showing top-down / bottom-up convergence at Epic, then prose listing the reconciliation gate ("EPIC.status = ready-for-dev requires: PM rationale present...", "EPIC.status = done requires..."). ADR-0008 §1 owns gates and would naturally own `epic-reconciliation` — but no such gate row exists in ADR-0008's inventory.
**What it signals:** The reconciliation rule is described in ARCHITECTURE.md but **not gated** in ADR-0008. ADR-0008's own meta-promise ("a principle without a gate is a gate-coverage failure") is violated by ADR-0008 itself. The structure (rule in narrative, not in gate inventory) masks the missing gate.
**Proposed restructure:** Either (a) add an `epic-reconciliation` gate row to ADR-0008 §1 enforcing the rules in ARCHITECTURE.md §5, and reduce ARCHITECTURE.md §5 to the diagram + a pointer; or (b) drop the gate-enforcement claim from ARCHITECTURE.md §5 and demote it to design intent. Current state (rule asserted, gate missing) is a self-contradiction.

### STRUCT-13 [PROCESS] - MOVE - ADR-0008 §1 gate inventory is reference data; should be a separate yaml/csv file
**File + section:** `ADR-0008 §1` is a 24-row table with columns `Gate | Enforces | Trigger | Owner`. The `gate-coverage` meta-gate (§2) "walks every ADR and every principle... and verifies that at least one entry in the table above references it."
**What it signals:** The table is reference data being consumed by tooling, embedded in prose markdown. Every gate addition requires editing markdown; the meta-gate must parse markdown tables. This is the classic "long enumeration that should be a table" → in this case, the table is already a table, but it should be a *machine-readable file* (yaml/csv) that the markdown renders from or links to.
**Proposed restructure:** Move the gate inventory to `tools/ci/gates.yaml` (or similar machine-readable home). ADR-0008 §1 becomes a one-line pointer ("inventory at `tools/ci/gates.yaml`, schema below") plus a schema block. `gate-coverage` reads the yaml directly. This eliminates the markdown-parsing dependency and prevents row-count drift between docs/tools.

### STRUCT-14 [SERIOUS] - QUESTION - "The paper" referenced as authority across multiple documents with no citation
**File + section:** `ARCHITECTURE.md §2` refers to "a published result on transformer associative memory (referred to throughout as 'the paper')". `ADR-0004 Context` references "the paper" with the same construct. Neither document cites the paper (no title, authors, arXiv ID, DOI).
**What it signals:** A foundational authority is invoked but unanchored. The structure makes the paper retrievable only by reputation, not by ID — the very anti-pattern ADR-0004 forbids for in-repo specs ("prose references are a lintable defect").
**Proposed restructure:** Add a `## References` section to ADR-0004 (the natural canonical home, since it derives discipline from the paper). Cite the paper with full bibliographic data and a stable identifier (DOI or arXiv ID). ARCHITECTURE.md §2 replaces "the paper" with a pointer to that citation. This is the same stable-ID-plus-path discipline applied externally.

### STRUCT-15 [PROCESS] - MERGE - ADR-0003 §3 (Four test tiers) duplicates ADR-0006 §1 (Four tiers, every project)
**File + section:** `ADR-0003 §3` enumerates `unit / integration / e2e / stochastic` with descriptions. `ADR-0006 §1` enumerates the same four tiers in a table with descriptions that differ in wording but not substance. ADR-0003 says `tests/stochastic/` "exercises real Anthropic API calls; assertions are statistical or schema-invariant (see ADR-0007)"; ADR-0006 §1 row for stochastic says "Real Anthropic API (see ADR-0007)".
**What it signals:** Two ADRs own the same fact. ADR-0006 is named "Testing tiers and the no-mock rule" — clearly the canonical home. ADR-0003 ("Apps Script runtime") added its own tier description rather than reference ADR-0006. The structure invites drift: a future tier change must touch both.
**Proposed restructure:** Strip ADR-0003 §3's tier enumeration; replace with "Apps Script projects use the four tiers defined in `ADR-0006 §1 @ openspec/architecture/decisions/ADR-0006-testing-tiers.md`; the GAS-specific adapter rules in §2 (this ADR) apply at the boundary." ADR-0006 §1 remains canonical. Cross-document SoT enforced.

## Summary
- **Total recommendations:** 15
- **Estimated reduction:** ~1,200 words across the 15 documents (~12% of original), plus elimination of multiple structural ambiguities and SoT defects.
- **Meets length target:** No target specified.
- **Comprehension trade-offs:** None — every recommendation either consolidates duplication, restores a schema, or moves data to its rightful home. The ARCHITECTURE.md narrative loses some apparent self-sufficiency (sections that summarize ADRs shrink to pointers), but readers gain a single retrievable source for each fact. Critical: STRUCT-01, STRUCT-02, STRUCT-03, STRUCT-09, STRUCT-12 all surface the same underlying issue — the SoT principle (P1) is asserted but the documents themselves violate it, because the cross-document consistency lint (also promised but not yet implemented) does not exist. These structural fixes either prevent or expose that violation.
