# VALID — validate-prd (opus) — Wave 2

**Source transcript:** [`raw-transcripts/VALID-agent-a6d85136a8adf5f6a.jsonl`](../raw-transcripts/VALID-agent-a6d85136a8adf5f6a.jsonl)
**Sub-agent description:** `Spec validation review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a6d85136a8adf5f6a`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-validate-prd` skill via the Skill tool. The artifact you're validating is not literally a PRD — it's an architecture artifact — but apply the same validation rigor (completeness, internal consistency, testability of requirements, traceability of decisions to consequences).

Treat the 15 architecture documents as if they were a single multi-part specification. For each section, ask the questions the validator skill is designed to ask:
- Is every requirement testable?
- Is every decision linked to a consequence and a compliance check?
- Are there hidden assumptions that aren't documented?
- Does the specification's structure match its claimed contract (e.g., "frozen artifact" but PHASE-0 is in-progress)?
- Are there cross-section dependencies that are stated only one way (A depends on B, but B doesn't mention A)?
- Is the acceptance criteria for "specification complete" itself well-defined?

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

REQUIRED OUTPUT:
- Stable IDs: prefix `VALID-` (e.g. VALID-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- Minimum 12 validation failures
- Each finding: which validation question failed, file/section, what an acceptable answer would look like, what the artifact gives instead
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have read all 15 documents. Let me produce the validation report.

# Architecture Specification Validation Report

## VALID-CRIT-01 — "Frozen artifact" claim contradicts PHASE-0 in-progress status

**Question failed:** Does the specification's structure match its claimed contract?

**File/Section:** `openspec/architecture/ARCHITECTURE.md` lines 10-13 vs. `openspec/architecture/phases/PHASE-0-foundation.md` line 4 (`status: in-progress`).

**What the artifact gives:** ARCHITECTURE.md asserts it and its referenced ADRs/phases "constitute the **frozen architecture artifact**." Yet PHASE-0 is `status: in-progress`, and PHASE-0's scope (items 1–11) includes producing the very files claimed to be frozen. The artifact is simultaneously claimed as both the input to and the output of PHASE-0.

**Acceptable answer:** Either (a) PHASE-0 status changes to `complete` before the freeze claim takes effect, with explicit acknowledgment that the frozen artifact is the post-PHASE-0 snapshot; or (b) the freeze claim is reworded to apply only to the structural narrative (§§1–12) and not to the in-progress implementation artifacts. A defined transition event (commit SHA, gate green) should anchor "frozen."

---

## VALID-CRIT-02 — Path mismatch between ARCHITECTURE.md §3 and ADR-0001/ADR-0002

**Question failed:** Is the specification internally consistent across sections?

**File/Section:** `ARCHITECTURE.md` §3 (uses `_bmad/`, `.claude/skills/`) vs. `ADR-0001` lines 45-46 (references `bmad/` without underscore) vs. `ADR-0002` §3 (declares `_bmad/`).

**What the artifact gives:** ADR-0001's "Rules" section says `bmad/` (no underscore) is the BMAD installation. ADR-0002 amendment 0001 explicitly changed the install path to `_bmad/`. ADR-0001 was never amended to match. PHASE-1 scope item 3 also says `bmad/` installation pinned in `bmad/config.yaml`. PHASE-0 scope item 12 says "`bmad/` is **not** installed in PHASE-0" — also stale.

**Acceptable answer:** ADR-0001 needs an amendment row updating the path nomenclature, OR ADR-0002's amendment 0001 should have triggered a synchronized edit + amendment to ADR-0001. PHASE-0 and PHASE-1 should be updated to match.

---

## VALID-CRIT-03 — Hook for `mcp__github__merge_pull_request` has no defined failure semantics

**Question failed:** Is every requirement testable?

**File/Section:** `ADR-0005` §6, line 98, and §8 row 5.

**What the artifact gives:** The hook is declared to `git fetch origin`, fast-forward, push. There is no statement of behavior when (a) fetch fails (network error), (b) the working branch is not the merged PR's branch, (c) the upstream has diverged and a fast-forward is impossible. §8's "residual loss only if both hooks fail to fire" is hand-wavy — what counts as "fail to fire" is not defined and not testable.

**Acceptable answer:** Enumerate the failure cases with explicit observable outcomes (abort with diagnostic, retry policy, journal event emitted). Define a test contract such as "given divergent upstream, hook MUST emit `push_failed` event and exit non-zero" so PHASE-2 can write a red test.

---

## VALID-CRIT-04 — REQ-ARCH-0002 is not atomic (violates its own ADR-0004 §3)

**Question failed:** Is every requirement atomic and testable per the spec's own atomicity rule?

**File/Section:** `ARCHITECTURE.md` §10, REQ-ARCH-0002.

**What the artifact gives:** "`openspec/architecture/ARCHITECTURE.md` plus ADR-0001 through ADR-0008 plus PHASE-0 through PHASE-5 are all present." This is one REQ asserting the existence of 15 distinct files — a compound requirement. ADR-0004 §3 mandates one assertion per REQ and explicitly cites "the system must do A and B" as the defect. By the spec's own rule, REQ-ARCH-0002 should fire `compound-requirement-detector`.

**Acceptable answer:** Split into REQ-ARCH-0002a through REQ-ARCH-0002o (one per file), or split into three REQs (ARCHITECTURE.md present, all 8 ADRs present, all 6 phases present) with the existence of each ADR/phase asserted in lower-level REQs.

---

## VALID-CRIT-05 — REQ-ARCH-0007 "verbatim" is unverifiable as stated

**Question failed:** Is every requirement testable?

**File/Section:** `ARCHITECTURE.md` §10, REQ-ARCH-0007.

**What the artifact gives:** "Root `CLAUDE.md` is present and references the five principles in §1 verbatim." But ARCHITECTURE.md §1 mixes the principle name (bold), the principle body, and per-principle elaboration. CLAUDE.md (per the embedded instructions) presents the five principles in a slightly different form ("Tests exercise real production code" — same; principle 5 wording matches). "Verbatim" needs a precise byte-level or sentence-level definition. As written, a lint rule cannot decide pass/fail without an oracle copy of the canonical text.

**Acceptable answer:** Define a canonical principle text fragment (e.g., a YAML block under `openspec/architecture/principles.yaml`) that both ARCHITECTURE.md §1 and CLAUDE.md must include verbatim. The test diffs the extracted blocks.

---

## VALID-CRIT-06 — ADR-0002 sections numbered out of order; §1–6 then jump to §7

**Question failed:** Does the specification's structure match standard ADR contract?

**File/Section:** `ADR-0002`, headers at lines 67 ("## 7."), 98 ("## 8."), 124 ("## 9.").

**What the artifact gives:** Decision section uses numbered list items 1–7. Then standalone `## 7. Staging discipline`, `## 8. Upgrade safeguards`, `## 9. Per-project output isolation` appear at the same heading level as Context/Decision/Consequences, conflating in-document numbering systems. There is no §1–§6 at H2 level — the numbering looks like a continuation but isn't. Cross-references like "(§7)" inside Consequences are ambiguous (does it mean Decision item 7 or section 7?).

**Acceptable answer:** Renumber the headings as `## Amendment 0002 — Staging discipline (§7)` etc., or fold §7-§9 into the Decision section as items, or restructure as named subsections (`## Staging discipline`) without numeric headers.

---

## VALID-CRIT-07 — One-way dependency between ADR-0005 push invariant and PHASE-2

**Question failed:** Are cross-section dependencies stated bidirectionally?

**File/Section:** `ADR-0005` §6 amendment 0001 vs. `PHASE-2` scope.

**What the artifact gives:** ADR-0005's amendment 0001 says the push-invariant implementations "land in PHASE-2." PHASE-2 scope item 1 mentions `journal_commit.py` and `post_merge_sync.py` and `checkpoint.py` with amendment refs — good. However, ADR-0008's CI gate inventory does **not** list any "push-invariant" gate or test. The amendment's enforcement surface ("the three hooks marked above") has no CI gate guaranteeing the hooks remain wired. If `.claude/settings.json` drops one of the three hook declarations post-PHASE-2, no gate fails.

**Acceptable answer:** Add a `hook-declarations-present` gate to ADR-0008 §1 enforcing that the hooks named in ADR-0005 §6 are present in `.claude/settings.json`. PHASE-2 must list this gate among its deliverables.

---

## VALID-CRIT-08 — REQ-ARCH-0008 cannot fail in any meaningful way until PHASE-2

**Question failed:** Is the acceptance criteria for "specification complete" itself well-defined?

**File/Section:** `ARCHITECTURE.md` §10, REQ-ARCH-0008; `PHASE-0` exit criteria.

**What the artifact gives:** REQ-ARCH-0008 requires `.claude/settings.json` to declare "hooks declared in ADR-0005 are listed (implementations land in PHASE-2)." The PHASE-0 hook commands "exit 0 with a TODO comment" (per PHASE-0 §9). The REQ passes if the file merely lists hook names — it doesn't assert the hook *names* match ADR-0005 §6's table. A future PR that adds a placeholder for `made_up_hook` would still pass. The REQ is structurally trivial.

**Acceptable answer:** Reword: "REQ-ARCH-0008 — `.claude/settings.json` declares exactly the seven hook event/command pairs named in ADR-0005 §6 table, no more, no fewer; commands may point to TODO placeholders during PHASE-0." Add a test that diffs declared hooks against the ADR table.

---

## VALID-SERIOUS-09 — Anti-aliasing threshold is unspecified and undecidable

**Question failed:** Is every decision linked to a verifiable compliance check?

**File/Section:** `ADR-0004` §4.

**What the artifact gives:** "Pairs above a threshold are a lintable defect. The threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly." The threshold value is not in the ADR. The config file does not yet exist (PHASE-1 deliverable). A reviewer cannot validate whether the threshold is appropriate. The "reviewed quarterly" claim has no compliance check (no gate referenced in ADR-0008).

**Acceptable answer:** ADR pins a starting numerical value (e.g., "Jaccard 0.85 over 5-grams") with rationale; quarterly review is itself a `gate`-type task tracked under a stable TASK-ID with a recurrence mechanism, and a CI gate verifies the most recent review timestamp is < 90 days old.

---

## VALID-SERIOUS-10 — ADR-0006 §2 permits "monkeypatch.setattr" exception with hidden assumption

**Question failed:** Are there hidden assumptions that aren't documented?

**File/Section:** `ADR-0006` §2.

**What the artifact gives:** The ban list says "applied to **modules within this repository**." The permitted-narrowly list allows HTTP transport substitution via `nock` "that records and replays *real* responses." This silently assumes "real responses" survive contract drift on the upstream service — but the cited justification ("cost or rate-limit reasons") doesn't address what happens when the recorded fixture diverges from the live service. The recorded-replay path looks indistinguishable from the forbidden "recorded response fixtures" of ADR-0007 §2.

**Acceptable answer:** Either name the permitted recording mechanism precisely (with a freshness policy — e.g., re-record nightly via CI; gate on staleness), or forbid recorded replay entirely. Resolve the apparent conflict with ADR-0007 §2 which forbids "Recorded response fixtures replayed in lieu of real API calls."

---

## VALID-SERIOUS-11 — ADR-0007 §5 cache-hit threshold unpinned but gated

**Question failed:** Is every decision linked to a consequence and a compliance check?

**File/Section:** `ADR-0007` §5; `ADR-0008` `cache-hit-regression` gate.

**What the artifact gives:** "Cache hit rate is reported per CI run; a regression below a pinned threshold fails the build." The threshold is not pinned in the ADR. PHASE-3 exit criterion says "`cache-hit-regression` baseline established" — meaning the baseline is established *after* the gate is operational, creating a chicken-and-egg: the gate cannot fail (no baseline) until the first run, and the first run cannot regress against a non-existent prior. The gate is non-binding on the first PR that creates the baseline.

**Acceptable answer:** Specify the bootstrap rule explicitly: "First measurement establishes the baseline; subsequent runs gate against baseline minus tolerance X%; baseline is itself stored at `tools/ci/cache_baseline.json` and updates require an explicit `Baseline-Update: <reason>` trailer."

---

## VALID-SERIOUS-12 — Per-commit push hook can conflict with branch protection on `main`

**Question failed:** Are there hidden assumptions that aren't documented?

**File/Section:** `ADR-0005` §6, `journal_commit.py` row; `ADR-0008` §6.

**What the artifact gives:** PostToolUse(git commit) "pushes `HEAD` to origin as a fast-forward." If the current branch is `main` and branch protection requires PR review, the push will fail. The ADR's "non-FF aborts the hook with a diagnostic" handles divergence but not protected-branch rejection. ADR-0008 §6 forbids `--no-verify`, but a developer on a protected branch will have committed locally with no way to push — and the hook's failure semantics for this case are undefined.

**Acceptable answer:** Add a row to ADR-0005 §8 failure-mode table covering "push rejected by branch protection." Specify behavior (e.g., abort with diagnostic instructing PR workflow; do not auto-create PRs; journal a `push_blocked` event).

---

## VALID-SERIOUS-13 — Two scope items labeled "3." and "4." duplicated in PHASE-5

**Question failed:** Does the specification's structure match its contract?

**File/Section:** `PHASE-5-first-appscript-project.md` lines 33-50.

**What the artifact gives:** Scope item "3. Real adapter wiring against shared-ts." is followed by "4. Per-project BMAD output isolation" (a multi-line block), then "4. Test suite across all four tiers, each red-first." — item "4" appears twice. There is no item "5" before "5. CI matrix entry." This is a structural defect; an automated requirement extractor referencing "PHASE-5 scope item 4" cannot resolve unambiguously.

**Acceptable answer:** Renumber so each scope item has a unique sequential index. Add a lint check on phase files asserting scope-item numbers are contiguous and unique.

---

## VALID-SERIOUS-14 — ADR-0001 §Rules forbids new top-level dirs but ARCHITECTURE.md §3 already adds undocumented ones

**Question failed:** Is internal consistency maintained between layout source and its constraint ADR?

**File/Section:** `ADR-0001` line 49, "No additional top-level directories may be introduced without an ADR" vs. `ARCHITECTURE.md` §3.

**What the artifact gives:** ARCHITECTURE.md §3 layout includes top-level entries `_bmad/`, `tools/`, `packages/`, `projects/`, `scripts/`, `.claude/`, `.github/`, `openspec/`, `README.md`, `CLAUDE.md`, `.gitignore`, `pyproject.toml`. ADR-0001 §Decision mentions only `projects/`, `packages/`, `tools/`, `bmad/`, `openspec/`. The presence of `_bmad/`, `scripts/`, `pyproject.toml`, `CLAUDE.md` as top-level entries is not justified in ADR-0001. ADR-0002 amendment may cover `_bmad/`, but `pyproject.toml` and `scripts/` lack an authoring ADR.

**Acceptable answer:** Either ADR-0001 lists every permitted top-level entry exhaustively (and ADR-0002 amendment 0001 cross-references its addition), or a separate ADR enumerates the allowlist that `top-level-allowlist` enforces. The constraint is currently unauditable: a reviewer cannot tell which directories are sanctioned.

---

## VALID-SERIOUS-15 — Gate "gate-coverage" is self-referential without bootstrap proof

**Question failed:** Is the decision linked to a compliance check that itself terminates?

**File/Section:** `ADR-0008` §2.

**What the artifact gives:** "`gate-coverage` walks every ADR and every principle ... and verifies that at least one entry in the table above references it." But `gate-coverage` itself appears in the table row as the gate enforcing "this ADR §2." Self-reference is not inherently wrong, but the ADR doesn't address: how is `gate-coverage` itself tested? What if `gate-coverage` is silently broken (always returns 0/pass)? No meta-test is required.

**Acceptable answer:** Specify that `gate-coverage` ships with a self-test: a synthetic ADR file lacking gate coverage is added to a test fixture; `gate-coverage` must detect it. PHASE-2 scope should list this test.

---

## VALID-SERIOUS-16 — REQ-ARCH-* tier and frontmatter missing

**Question failed:** Does the spec match the contract its own ADR-0004 §5 sets?

**File/Section:** `ARCHITECTURE.md` §10 vs. `ADR-0004` §5 storage format.

**What the artifact gives:** ADR-0004 §5 mandates per-REQ YAML frontmatter with `id`, `revision`, `status`, `introduced`, `supersedes`, `phase`, `tier`, `references`. The REQ-ARCH-* entries in ARCHITECTURE.md §10 are bullet sentences with no frontmatter, no tier declaration, no status. ADR-0006 §5 says "A REQ marked `tier: e2e` requires a passing E2E test" — but REQ-ARCH-* have no tier declared, so `tier-coverage` gate cannot run on them.

**Acceptable answer:** Either store REQ-ARCH-* in proper REQ block format per ADR-0004 §5 (likely in `openspec/specs/_meta/architecture.spec.md`) and reference them from ARCHITECTURE.md §10, or carve a documented exception in ADR-0004 for architecture REQs and define how `tier-coverage` handles them.

---

## VALID-PROCESS-17 — Phase exit ADRs referenced but no ADR-0009+ exists

**Question failed:** Are there cross-section dependencies stated only one way?

**File/Section:** `ARCHITECTURE.md` §11 ("the phase exit ADR is signed off"), ADR-0008 §3 ("the next phase's entry ADR (if any) is `status: accepted`").

**What the artifact gives:** Both documents reference "phase exit ADR" / "phase entry ADR" as gating artifacts, but no ADRs for phase transitions exist in `decisions/`. PHASE-0 through PHASE-5 files have `status:` in frontmatter; whether that status is itself the "signed-off ADR" or whether a separate ADR is required is undefined. The `phase-exit` gate cannot evaluate "next phase's entry ADR" if no such ADR template or naming convention exists.

**Acceptable answer:** Either (a) declare that phase frontmatter `status: accepted` *is* the ADR equivalent, with rules for who/how it transitions, or (b) define a naming scheme (e.g., `ADR-PHASE-N-EXIT-XXXX`) and provide a template ADR. Update both ARCHITECTURE.md §11 and ADR-0008 §3 to point at the chosen convention.

---

## VALID-PROCESS-18 — ADR-0007 §5 references "model supports it" without listing models

**Question failed:** Is every requirement testable without an oracle?

**File/Section:** `ADR-0007` §5; PHASE-3 scope item 1.

**What the artifact gives:** "Prompt caching enabled by default where the model supports it." The set of supporting models is not enumerated, neither in ADR-0007 nor in PHASE-3. A lint check or unit test asserting "caching is enabled for X" cannot know which X. CLAUDE.md is referenced as model "Opus 4.7" — whether caching applies is not specified.

**Acceptable answer:** Pin a model-capability matrix in `packages/anthropic-client/config.yaml` (or in ADR-0007 §5), reference it from the test, and update on each model addition. The cache-hit regression gate must read from this matrix to know which calls are expected to cache.

---

## Summary

The architecture is internally cohesive in vision but has 18 validation defects of varying severity: 8 CRITICAL (testability, internal contradiction, self-reference without bootstrap), 8 SERIOUS (under-specified thresholds, undocumented assumptions, structural numbering errors), and 2 PROCESS (missing convention definitions for phase-exit ADRs and model capability matrix). The most consequential issues are the "frozen artifact" / PHASE-0-in-progress paradox (VALID-CRIT-01), the path-naming drift between ADR-0001 and ADR-0002 (VALID-CRIT-02), and the violation of ADR-0004 §3's own atomicity rule by REQ-ARCH-0002 (VALID-CRIT-04). Several gates declared in ADR-0008 reference compliance against unpinned thresholds (anti-aliasing, cache-hit), making the corresponding gates currently undecidable. Cross-document dependencies are present but mostly one-way: amendments to ADR-0002 and ADR-0005 did not back-propagate updates into ADR-0001, ARCHITECTURE.md §3, or PHASE-0/1 scope items.

Files reviewed:
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
