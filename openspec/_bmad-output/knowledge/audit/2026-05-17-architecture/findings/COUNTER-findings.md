# COUNTER — counter-factual (opus) — Wave 4

**Source transcript:** [`raw-transcripts/COUNTER-agent-a2d388c1125c79145.jsonl`](../raw-transcripts/COUNTER-agent-a2d388c1125c79145.jsonl)
**Sub-agent description:** `Counter-factual analysis`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a2d388c1125c79145`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke `bmad-advanced-elicitation` with a **counter-factual analysis** method: for each major architectural commitment, ask "what if this decision had been made differently?" and identify what the artifact has *not* considered about the alternative.

Documents (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md, decisions/ADR-0001 through ADR-0008, phases/PHASE-0 through PHASE-5

Counter-factuals to explore:
- What if `openspec/` were many small files instead of a small canonical set?
- What if the matrix were computed on demand rather than committed?
- What if BMAD were on-demand-installed rather than vendored?
- What if the four-tier testing model had three tiers, or five (security, performance)?
- What if commit trailers were a separate sidecar file rather than message-embedded?
- What if phase ordering were a DAG rather than a linear chain?
- What if `_bmad-output/` did not exist (BMAD outputs go straight to canonical homes)?
- What if `gate-coverage` were inverted (a gate must declare which principles it enforces, not the reverse)?
- What if the architecture were product-first (PHASE-0 = ship a real Apps Script demo)?
- What if no ADRs existed (everything in ARCHITECTURE.md)?

For each: state the alternative, what argument the architecture would have to rebut, and what consideration is missing from the current decision rationale.

REQUIRED OUTPUT:
- IDs prefix `COUNTER-` (CRIT/SER/PROC inline by how much the missing consideration would change the design)
- Minimum 12 counter-factuals
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have all 15 documents. Now I'll produce the counter-factual analysis directly, skipping the elicitation menu (the user pre-selected counter-factual analysis and specified the output format).

---

## COUNTER-001 [CRIT] — Many small `openspec/` files vs. small canonical set

**Alternative.** Instead of one canonical `feature.spec.md` containing many REQ blocks, decompose into one file per REQ (`openspec/specs/<domain>/<feature>/REQ-X-NNNN.md`) — fully atomic at the filesystem layer, mirroring the addressing scheme.

**Rebuttal the architecture would need.** ADR-0004 §5 implicitly assumes co-location of related REQs inside a single feature file aids human reading. But the paper-derived rationale (ADR-0004 §1–§4) is purely about *retrieval*, not authoring; retrieval is by ID-plus-path, which is even *cheaper* under one-file-per-REQ — `cat openspec/specs/auth/login/REQ-AUTH-0007.md` is `O(1)` with no need for the in-file scan a multi-REQ file requires.

**Missing consideration.** ADR-0004 never argues *for* multi-REQ files; it only argues against semantic recall. Under one-file-per-REQ, `append-only at the assertion level` (§7) becomes a filesystem property (immutable file, supersession = new file), making the rule self-enforcing instead of lint-enforced. Anti-aliasing (§4) becomes simpler too: pairwise n-gram is over files, not over blocks. The current design imports a soft cost (atomicity becomes a lint heuristic) without rebutting the file-per-REQ alternative.

---

## COUNTER-002 [SER] — Matrix computed on demand vs. committed

**Alternative.** `matrix.yaml` is *not* committed. CI computes it during the PR check; `tools/trace/audit.py` computes it on demand locally.

**Rebuttal the architecture would need.** ADR-0005 §2 says "the file is checked in so that diffs are reviewable" and uses `matrix-drift` as the consistency gate. But the gate exists precisely *because* the file is committed; remove the commit and the gate disappears with it.

**Missing consideration.** The ADR never quantifies what reviewability of matrix diffs buys, given humans are forbidden to hand-edit (§2) and the file is mechanically derived. A derivation is reviewed by reviewing its inputs (spec frontmatter changes, test annotation changes, trailer changes) — all already in the diff. The cost of the current design is bimodal: every PR touching specs/tests/journals produces large matrix churn, blowing up review surface and triggering merge conflicts on parallel PRs. Counter-factual: a cache regenerated at session start (cheap, deterministic) plus `audit` for queries would eliminate `matrix-drift`, eliminate merge conflicts on derived data, and remove a class of bugs where the committed cache lies because a rebuild bug shipped.

---

## COUNTER-003 [SER] — BMAD on-demand install vs. vendored

**Alternative.** `scripts/install_bmad.sh` runs at SessionStart hook (or first-use). `_bmad/` and `.claude/skills/` are gitignored. Version pinned in script; install is hermetic.

**Rebuttal the architecture would need.** ADR-0002 §4 cites "zero network dependency on session start" and "reproducible across machines" as reasons to vendor 2.6 MB. But network dependency is already present for `clasp`, Sheets REST adapters, Anthropic API, and `gh` MCP — the "zero network" claim is partial.

**Missing consideration.** Amendment 0001 explicitly notes the wrapper-isolation strategy from the original ADR was "dropped — native Skills make it unnecessary"; this strongly suggests the architecture is sensitive to BMAD upgrades touching layout. Vendoring the 2.6 MB *into git* means every BMAD upgrade is a giant diff (Amendment 0002 admits this) that pollutes `git log`, `git blame`, and PR review. The architecture has not considered the alternative where a lockfile-style pin (sha256 + version) is committed and the install runs at session start — this gives reproducibility *and* a small repo. The skill-removal-acknowledged gate (§8.2) works just as well over a manifest snapshot as over vendored content.

---

## COUNTER-004 [SER] — Three or five test tiers vs. four

**Alternative-A (three).** Collapse `integration` into `e2e`: there is one "real systems" tier, parametrized by deployment target.
**Alternative-B (five).** Add `security` (auth-bypass, injection) and/or `performance` (latency budgets, regression).

**Rebuttal the architecture would need.** ADR-0006 §1 asserts four tiers per project but never justifies *why four*. The `integration` tier is defined as "real Sheets/Drive/HTTP via REST"; the `e2e` tier is "deployed GAS code, real Sheets/Drive". The only difference is the runtime (Node vs. GAS V8) — under ADR-0003, Node-on-real-Sheets and GAS-on-real-Sheets test orthogonal properties only because GAS V8 is platform-specific. That justifies the tier *for GAS projects*, not for Anthropic-client or shared-py.

**Missing consideration.** ADR-0006 §1 mandates "every REQ declares its tier" and "CI runs the tier each REQ declares" — but in projects without a GAS runtime, `e2e` is undefined. The ADR does not rebut the five-tier variant (security/performance) despite both being CI gates the principles (P3) implicitly cover: security tests are real-code tests; performance tests are statistical. Adding a tier is described as "ADR amendment plus a CI matrix entry" (Consequences) but the cost of *retrofitting* an existing REQ corpus to a new tier is not addressed. Counter-factual: declare two axes — "runtime" (node | gas | api) and "property" (functional | security | performance | stochastic) — and let the cross-product define tiers. Current model conflates these into a single dimension and bakes the conflation into spec frontmatter.

---

## COUNTER-005 [PROC] — Sidecar trailer file vs. message-embedded

**Alternative.** Trailers live in `.git-trailers/<sha>.yaml` (committed alongside the change), not in commit messages. `commit-trailers-valid` checks the sidecar.

**Rebuttal the architecture would need.** ADR-0005 §3 wants traceability to ride on git's existing object model. Sidecars introduce a second file per commit and a new failure mode (commit lands without sidecar). But message-embedded trailers fight git tooling: `git rebase`, `git cherry-pick`, `git revert`, squash merges, and most code-review surfaces all collapse, drop, or reformat trailers; the `Checkpoint: true` exemption (§7) is evidence of this fragility.

**Missing consideration.** The ADR never addresses what happens when GitHub's "Squash and merge" mangles trailers across many commits — does the squash inherit all `Requirements:` lines? Just the last? The push-invariant amendment (§10 Amendment 0001) was provoked by a real divergence on `claude/general-session-KXgas` *because* commit-graph operations are slippery; trailers ride on the same fragile substrate. A sidecar is reviewable in the PR, surviveable across rebases (the file is the unit), and naturally supports compound information (multi-REQ tasks) without one-line cramming. Counter-factual cost: one more file to write per commit (the same hook already writes; the change is target). Counter-factual benefit: trailers stop being a hidden gate that bypasses standard git workflows.

---

## COUNTER-006 [CRIT] — Phase DAG vs. linear chain

**Alternative.** PHASE-3 (anthropic-client) and PHASE-4 (shared libs) are independent and could land in parallel; PHASE-5 depends on both. Express as a DAG; CI gates per-edge, not per-prior-phase.

**Rebuttal the architecture would need.** ADR-0008 §3 enforces "no REQ from a later phase is `tests-green`" — strictly linear. ARCHITECTURE.md §11 says "a phase cannot start until the prior phase's exit criteria are all `tests-green`". The implicit rebuttal is simplicity: linearity is easier to gate.

**Missing consideration.** Read the actual dependencies. PHASE-3 (anthropic-client) needs PHASE-2 (traceability) but does not need anything from PHASE-1 *for the anthropic client itself* beyond spec hygiene; PHASE-4 (shared libs) needs PHASE-2 but its `shared-py` half does not need PHASE-3 at all. PHASE-5 needs PHASE-3 (LLM-using project) and PHASE-4 (shared-ts adapters). Linearizing them forces `packages/shared-py/` to wait on `packages/anthropic-client/` for no technical reason, just to satisfy `phase-exit`. Counter-factual: a `requires:` block in each PHASE file (DAG edges) and a `phase-graph-valid` gate. This is *more* enforceable, not less, because the architecture would have to make dependencies explicit rather than implicit in their numbering. The current design ships a hidden assumption (numerical order = dependency order) that is locally false.

---

## COUNTER-007 [SER] — No `_bmad-output/` vs. BMAD writes to canonical homes directly

**Alternative.** BMAD's `bmm.planning_artifacts` points at `openspec/briefs/`, `bmm.implementation_artifacts` at `openspec/changes/`, `bmm.project_knowledge` at `openspec/architecture/`. No staging. Promotion is implicit in the BMAD output.

**Rebuttal the architecture would need.** ADR-0002 §7 says staging exists because BMAD drafts are "non-authoritative", "outside the addressable artifact network", and the matrix/INDEX/lint must not see them. The implicit argument: BMAD outputs are not initially well-formed enough to clear spec_lint.

**Missing consideration.** This is an indictment of BMAD's output quality, not a design requirement. If BMAD output is reliable enough for `_bmad-output/STAGING.md` to define a finite promotion protocol, it is reliable enough to write to a `draft/` sub-tree *inside* the canonical home, where spec_lint can be scoped to skip `status: draft` rather than skipping a whole directory. Counter-factual benefit: one fewer top-level subtree, no `stale-staging` gate needed (drafts that don't graduate to non-draft status are surfaced by the same coverage gates), and no "promotion is a `docs`-type TASK" ceremony. The current design's missing consideration: BMAD writes Markdown that humans then edit; the human edit *is* the promotion. Forcing a file move on top of editing is friction without correctness gain.

---

## COUNTER-008 [CRIT] — Inverted `gate-coverage` (gates declare what they enforce)

**Alternative.** Each CI gate, in its own implementation file, declares `@enforces ADR-0004 §1, P3` as machine-parseable metadata. `gate-coverage` rebuilds the inventory from gate code; ADR-0008 §1's table becomes a *derived* artifact.

**Rebuttal the architecture would need.** ADR-0008 §1's hand-maintained table is the current SoT; gates are referenced *from* the table to the principle/ADR. The implicit rebuttal: the table is human-readable architectural narrative.

**Missing consideration.** This violates Principle P1 (single source of truth) at the meta level. The fact a gate enforces ADR-0004 §1 is asserted in two places: the gate's implementation (which must know what it checks) and ADR-0008's table. They can drift, and `gate-coverage` only checks the table is non-empty per principle, not that the *gate actually still enforces what the table claims*. Inverted design: gate metadata is SoT; `gate-coverage` rebuilds the table; PR shows the diff in the derived table when a gate's coverage changes. ADR-0008 has not considered that its own SoT/derivation discipline (applied to specs in ADR-0004 and matrix in ADR-0005) is *not* applied to itself.

---

## COUNTER-009 [CRIT] — Product-first PHASE-0 (ship a demo)

**Alternative.** PHASE-0 = ship one trivial Apps Script demo end-to-end (one cell write via `clasp`). PHASE-1+ = retrofit the architectural substrate to harden it.

**Rebuttal the architecture would need.** ARCHITECTURE.md §1's principles are "enforced on every change" — that requires the substrate to exist before any change lands. PHASE-0 (foundation) is the substrate. Product-first would let early commits skip every gate.

**Missing consideration.** The current design's risk: PHASE-0 through PHASE-4 ship *no demonstrated product value*, and PHASE-5 is explicitly named "the load test for the architecture" — meaning the architecture's first contact with reality is after five phases of design. PHASE-5 §exit-criteria already concedes pain points "result in an ADR amendment, not a workaround", admitting the architecture will need revision. Counter-factual: a product-first PHASE-0 surfaces architectural defects *before* eight ADRs are written, eliminating the need to amend them. The current rationale never weighs "five phases of investment in unfalsified architectural claims" against "one phase to validate the claims cheaply". This is a classic waterfall risk; the architecture has not considered it because the architecture is itself the deliverable, and product-first would demote it.

---

## COUNTER-010 [SER] — No ADRs (everything in ARCHITECTURE.md)

**Alternative.** ARCHITECTURE.md is the sole architectural artifact; sections replace ADRs; amendments are commits to those sections.

**Rebuttal the architecture would need.** ADRs preserve the decision context and the alternatives considered, separately from the current state, so a future reader can see *why* a decision was taken. ARCHITECTURE.md is a snapshot; ADRs are a history.

**Missing consideration.** The current architecture has already partially betrayed this rationale: ADR-0002 was rewritten in Amendment 0001 ("complete rewrite to match BMAD v6.6.0 empirical reality"), discarding the original wrapper-isolation context. If ADRs are subject to complete rewrites when reality contradicts them, the historical-context argument is weakened — what survives is the current decision plus an amendment log. That is what ARCHITECTURE.md sections plus git history already provide. Counter-factual: collapse ADR-0001 through ADR-0008 into ARCHITECTURE.md §§ with the same content; the amendment logs become git history, which is searchable, blameable, and timestamped without parallel infrastructure. The cost of the current design: eight files where one would do, eight files to keep in cross-reference sync, eight `xref-resolves` lint runs. The architecture has not articulated what an ADR provides that a section + git blame does not.

---

## COUNTER-011 [SER] — Append-only journal vs. structured per-task event store

**Alternative.** Instead of `session-<id>.jsonl`, use one file per task (`task-<id>.jsonl`) and one per commit (`commit-<sha>.json`). Crash recovery reads only the active task file.

**Rebuttal the architecture would need.** ADR-0005 §5 chooses session-scoped JSONL because partial writes are line-discardable. Per-task files would have the same property.

**Missing consideration.** Session-scoped journals interleave events across tasks (task_activate A, file_touch, task_pause A, task_activate B, ...), which forces `rebuild.py` to do a per-event sort/group by `task_id` to answer "what happened in TASK-0042". Per-task storage makes that lookup `O(1)`. The current design has not considered that the dominant query (`audit TASK-0042`) hits the storage layout sub-optimally. Counter-factual cost: more files. Counter-factual benefit: simpler audit, simpler `resume.py`, no cross-session correlation needed to reconstruct task state.

---

## COUNTER-012 [PROC] — Hand-maintained `STATUS.md` vs. derived

**Alternative.** `openspec/STATUS.md` is generated by `tools/trace/status.py` from journal + git + matrix + open PRs. CLAUDE.md tells Claude to *run the command*, not read the file.

**Rebuttal the architecture would need.** CLAUDE.md (project instructions) explicitly says STATUS.md is "hand-maintained until PHASE-2's `SessionStart` resume hook mechanizes it". So the architecture has *considered* this and deferred it. But the deferral has a cost: between today and PHASE-2 landing, every session must trust a human-written summary whose freshness has no gate.

**Missing consideration.** The ADRs assert (ADR-0005 §8) "session resume requires zero human re-briefing", but PHASE-0 ships with a *human-briefing-required* STATUS.md. There is an inconsistency between the principle (mechanical resume) and the current artifact (hand-maintained gate-less file). The architecture has not considered the alternative of a *minimal mechanical STATUS.md right now* — even a 10-line generator over `git log` + open PRs would beat hand-maintenance. Deferring full mechanization is reasonable; deferring all mechanization while asserting the principle is enforced is a gap.

---

## COUNTER-013 [SER] — Anthropic client per-tier vs. single package

**Alternative.** `packages/anthropic-client/` is split into `anthropic-transport/` (network, caching) and `anthropic-contract/` (sandwich layers, schemas). The "single LLM access point" becomes "single LLM *transport* point"; sandwich-layer code lives near its consumers.

**Rebuttal the architecture would need.** ADR-0007 §6 centralizes "cost telemetry, caching, and model-version pinning" — all transport concerns. Sandwich-layer code (ADR-0007 §3) is not transport.

**Missing consideration.** The current package mixes transport (a singleton concern) with contract enforcement (a per-feature concern). Forcing every sandwich into one package creates a chokepoint where every LLM-using feature blocks on edits to a single package. Counter-factual: transport is the lint-enforced singleton; contracts are per-feature, lint-enforced to import only from `anthropic-transport/`. ADR-0007 has not considered that the same rationale (centralize what must be central, decentralize what need not be) applies internally to its own package.

---

## COUNTER-014 [SER] — Bidirectional reconciliation at Epic vs. at REQ

**Alternative.** ARCHITECTURE.md §5's top-down and bottom-up flows reconcile at the REQ, not the Epic. Each REQ has a `top-down-rationale:` and `bottom-up-acceptance:` block; the Epic is a thin coverage roll-up.

**Rebuttal the architecture would need.** The current design treats Epic as the contract object: Epic carries `coverage:` listing REQ-IDs, `ready-for-dev` gates on Epic, `done` gates on Epic. Reconciling lower is heavier per-REQ.

**Missing consideration.** Reconciliation at the Epic layer means a misaligned REQ (PM-rationale present, bottom-up acceptance missing) is invisible until the whole Epic is closed. Per-REQ reconciliation surfaces drift commit-by-commit, in line with red-first (P4). The architecture has not considered that a top-down/bottom-up reconciliation point higher than the smallest atomic unit (the REQ) re-introduces a "fact in two places" pattern (PM rationale at Epic, acceptance at REQ) — a soft P1 violation. The counter-factual makes the REQ self-describing with both flows attached.

---

## COUNTER-015 [PROC] — Commit-trailer schema vs. free-form key:value

**Alternative.** Trailers are validated against a published JSON Schema in `tools/trace/trailer-schema.json`; new trailer keys require a schema PR.

**Rebuttal the architecture would need.** ADR-0005 §3 fixes four trailers (`Task`, `Requirements`, `Tests-Status`, `Phase`) and ADR-0005 §7 + Amendment 0001 introduces `Checkpoint:`; further trailers (`Bootstrap:` ADR-0006 §4, `Skill-Removal-Acknowledged:` ADR-0002 §8, `Material-Architecture-Change:` ARCHITECTURE.md preamble) accrue across ADRs.

**Missing consideration.** Each ADR adds a trailer key as a side effect, never updating ADR-0005 §3's enumeration. There is no single place that lists all valid trailers; `validate_commit.py` (PHASE-2) will have to discover them from across the ADRs. The architecture has not considered that trailer keys are themselves an addressable artifact class that deserves stable IDs (and a schema), the same discipline applied to REQs. Counter-factual: a `TRAILER-<key>` registry with schema and owning ADR — closes a P1 gap the current design ships with.
