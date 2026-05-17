# CHECK — checkpoint-preview (opus) — Wave 3

**Source transcript:** [`raw-transcripts/CHECK-agent-abfee06201b816a17.jsonl`](../raw-transcripts/CHECK-agent-abfee06201b816a17.jsonl)
**Sub-agent description:** `Checkpoint-preview focused review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `abfee06201b816a17`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-checkpoint-preview` skill via the Skill tool. Apply it to the architecture artifact — focus attention where it matters most.

The skill is normally invoked when "the user says 'checkpoint', 'human review', or 'walk me through this change'." Apply it here as: "I am about to merge the architecture artifact (15 documents) to main. Walk me through where I should focus my attention — what would I miss on a casual read that I would deeply regret missing?"

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

For each finding:
- Specific location requiring attention (file/section)
- What a casual reader would miss
- Why missing it matters in the next 6 months
- Concrete what-to-check (test, verify, or question to ask before merge)

Focus areas:
- Quietly load-bearing assumptions
- Decisions presented as conclusions that are actually unresolved trade-offs
- Implicit contracts between sections that aren't surfaced
- Where the document's tone implies certainty but the substance is provisional
- Where review fatigue would skip over a critical decision

REQUIRED OUTPUT:
- Stable IDs: prefix `CHECK-` (e.g. CHECK-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 12 findings
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have full context across all 15 documents. Let me produce the structured findings report.

# Checkpoint Review — Architecture Artifact (15 documents)

The artifact is unusually coherent — a rare quality. That coherence is also its primary risk: review fatigue sets in by ADR-0005, and several decisions that *sound* like conclusions are actually unresolved trade-offs hidden inside crisp prose. The findings below are ranked by what you would most regret missing in the next 6 months, not by where they appear in the documents.

---

## CRITICAL

### CHECK-CRIT-01 — ADR-0002 silently contradicts ARCHITECTURE.md §3 about `.claude/agents/` and `.claude/commands/`

**Location:** `openspec/architecture/ARCHITECTURE.md` §3 (lines 56–57) vs `openspec/architecture/decisions/ADR-0002-bmad-integration.md` §3 + Amendment 0001.
**What a casual reader misses:** ARCHITECTURE.md §3 still describes `.claude/agents/` and `.claude/commands/` as "legacy slot — empty in v6 native-skills model." ADR-0002 says wrappers are gone. But ARCHITECTURE.md §9 (lines 215–218) still says "Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by file path…". §9 was *not* updated when ADR-0002 was rewritten. PHASE-1 scope item 4 (`PHASE-1-spec-hygiene.md:34`) also still requires the wrapper files: "All BMAD wrapper files in `.claude/agents/` and `.claude/commands/` resolve their `Load:` paths" — a now-impossible exit criterion.
**Why this matters in 6 months:** PHASE-1 will fail its own exit gate because the wrappers don't exist (native skills replaced them). Someone will either re-introduce wrappers to satisfy the gate (re-creating the maintenance burden ADR-0002 amendment removed), delete the criterion silently, or stall the phase.
**What to check before merge:** Diff ARCHITECTURE.md §9 against ADR-0002 §3 and reconcile in one direction. Rewrite PHASE-1 scope item 4 and exit criterion 4 to reflect native Skills. Confirm `REQ-ARCH-0008` and the §3 "legacy slot" comments agree with PHASE-1.

### CHECK-CRIT-02 — The `push invariant` (ADR-0005 §6 amendment) is unenforced during PHASE-0 and PHASE-1

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6 + Amendment 0001; `openspec/architecture/phases/PHASE-0-foundation.md` scope item 9.
**What a casual reader misses:** The push invariant is described as a hard guarantee ("every operation that mutates the commit graph or moves a branch pointer must result in origin tracking the post-state within the same hook firing"). But PHASE-0 commits hooks as "placeholder commands that exit 0 with a TODO comment." Real enforcement lands in PHASE-2. For all of PHASE-0 and PHASE-1, the failure mode the invariant exists to prevent — "committed but unpushed when container is reclaimed" — is wide open, and the amendment was added precisely because this failure was observed in reality.
**Why this matters in 6 months:** The architecture artifact itself, plus all PHASE-1 spec-lint work, will be authored under a regime that has the known failure mode. Loss of a substantial branch is plausible. The risk is highest *now* because PHASE-0 work has not yet established the muscle memory.
**What to check before merge:** Decide whether PHASE-0/PHASE-1 sessions run with an *external* Stop hook (manual scripts, not the placeholder) or accept the risk and document it explicitly. Add the decision to `openspec/STATUS.md` so the next session knows.

### CHECK-CRIT-03 — `red-before-green` enforcement has a structural hole around `Checkpoint: true` commits

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §7; `openspec/architecture/decisions/ADR-0006-testing-tiers.md` §4; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §6.
**What a casual reader misses:** Checkpoint commits skip CI gates. The text says "the next non-checkpoint commit on the branch [is] responsible for restoring P4 compliance (either by squash or by ensuring the red/green sequence is recoverable from the full history)." No mechanism is named to *verify* the next commit actually restored compliance. `tools/trace/validate_commit.py` walks history — but if a checkpoint commit sits between the red commit and the green commit, what does the walker do? It is not specified. The `checkpoint_exemptions.yaml` is mentioned but never enumerated.
**Why this matters in 6 months:** Once checkpoints become routine (PHASE-2), agents will get a free pass on P4 if `validate_commit.py` simply skips checkpoint commits. The principle that is meant to be the most rigorously enforced (red-first) becomes the easiest to launder.
**What to check before merge:** Either (a) define `checkpoint_exemptions.yaml` contents in ADR-0005 §7 or ADR-0008 §6 now (don't defer), or (b) add a CI gate that asserts every checkpoint commit is followed by either a squash, a rebase that removes it, or a non-checkpoint commit whose author certifies P4 compliance. Ask: "Can a chain of checkpoint commits silently absorb a green-before-red sequence?"

### CHECK-CRIT-04 — The `anti-aliasing` lint rule has no calibration story

**Location:** `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §4.
**What a casual reader misses:** The rule computes n-gram similarity across *all* spec descriptions and acceptance bodies, with threshold pinned in `tools/spec_lint/config.yaml` and "reviewed quarterly." No initial threshold, no n-gram size, no false-positive policy, no escape hatch. As the corpus grows, near-duplicate REQs *will* appear legitimately (cross-domain repetition like "input must validate against schema"). Without a calibration baseline, the gate will either be tuned to silence (useless) or stay strict and block legitimate work.
**Why this matters in 6 months:** When PHASE-3+ specs ramp up, this gate is the most likely to become "the one everyone disables." If it dies, ADR-0004's paper-derived foundation dies with it — the whole rationale for the SoT discipline assumes anti-aliasing is real.
**What to check before merge:** Force a decision now on (a) initial n-gram size and threshold, (b) whether the gate is advisory or blocking in PHASE-1, (c) what an explicit "intentional near-duplicate" annotation looks like. Without these, the rule is decorative.

---

## SERIOUS

### CHECK-SER-05 — `audit.py` is the only listed query surface; no concurrency or staleness contract

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §9.
**What a casual reader misses:** The audit interface is described as "deterministic" but reads from a *cache* (`matrix.yaml`) that the user has just been told is regenerated from sources. If `audit REQ-X-NNNN` runs against a stale matrix, the answer is wrong. There's no `--rebuild-first` flag, no staleness check, no contract about what "deterministic" means when journals have advanced past the committed matrix.
**Why this matters in 6 months:** Agents will trust `audit` output. Wrong audit output in a session-resume context (PHASE-2 SessionStart hook) means the next session resumes on a false picture of the in-flight task.
**What to check:** Specify in ADR-0005 §9 whether `audit` rebuilds-on-read, asserts freshness, or warns on staleness. Decide before PHASE-2 implements it.

### CHECK-SER-06 — `bulk-green-start` threshold `N` is undefined

**Location:** `openspec/architecture/decisions/ADR-0006-testing-tiers.md` §4.
**What a casual reader misses:** "CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." `N` is never named. This is a P4 escape hatch (the `Bootstrap:` trailer plus reviewer approval) whose threshold is the only thing standing between disciplined red-first and "we just imported 200 tests, sorry."
**Why this matters in 6 months:** PHASE-3 (Anthropic client) and PHASE-5 (first Apps Script project) will both have moments where multi-test imports are tempting. If `N` is set casually later, it'll be set generously.
**What to check:** Pin `N` in ADR-0006 §4 now. Suggest N=1: any green commit adding a new test requires either a prior red commit or a `Bootstrap:` trailer.

### CHECK-SER-07 — `cache-hit-regression` baseline is established in PHASE-3 but pinned threshold has no source

**Location:** `openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md` §5; `openspec/architecture/phases/PHASE-3-anthropic-client.md` exit criteria.
**What a casual reader misses:** "Cache hit rate is reported per CI run; a regression below a pinned threshold fails the build." Pinned by whom? PHASE-3 says "baseline established." A baseline established by PHASE-3's first run is just whatever PHASE-3 happened to ship — it isn't a target. The mechanism creates the appearance of a guard while measuring against itself.
**Why this matters in 6 months:** When `packages/anthropic-client/` is refactored, the cache-hit metric will either flap (if too tight) or never fire (if it's just the rolling average of recent runs). A regression detector that never detects regression is technical-debt theater.
**What to check:** Decide whether the threshold is (a) absolute and pinned by ADR amendment, or (b) relative to a rolling window with an explicit hysteresis. Document the policy in ADR-0007 §5.

### CHECK-SER-08 — `stochastic` tier distributional assertions: no policy on flakiness budget

**Location:** `openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md` §3.
**What a casual reader misses:** "Distributional assertions over N runs. Sample size declared; assertion is a confidence interval, Kolmogorov–Smirnov test, or similar. Sample size and threshold are pinned per test." This is correct in principle. But: a confidence-interval-based test fails some percentage of the time *by design* (e.g. 5% at α=0.05). With many such tests, *some* will fail on every CI run. There is no policy for: per-PR re-run budget, false-positive rate ceiling, who triages a flake-vs-real-regression call.
**Why this matters in 6 months:** Stochastic CI noise is the #1 reason teams disable stochastic gates. The architecture document forbids retry-until-pass loops (correctly) but supplies no alternative for handling expected statistical noise.
**What to check:** Add a §3.1 to ADR-0007 covering false-positive budget and triage policy. Ask: "What happens when a CI run shows two stochastic tests failing at p<0.05?"

### CHECK-SER-09 — `mock-in-repo-banned` rule definition leaves contract testing in limbo

**Location:** `openspec/architecture/decisions/ADR-0006-testing-tiers.md` §2.
**What a casual reader misses:** The rule bans `jest.mock`, etc., applied to in-repo modules. But contract tests of an *interface* (e.g. asserting that two real adapter implementations behave identically) often use test doubles that satisfy the interface. ADR-0006 §3 says "each interface has at minimum two real implementations" — production and test — but doesn't explain how new adapter implementations are introduced without a transient period of mocking, or how contract tests verify interface conformance.
**Why this matters in 6 months:** Adding a third adapter (e.g. a chaos-injecting Sheets adapter) becomes harder than necessary because the regime over-constrains. People will work around it.
**What to check:** Clarify in ADR-0006 §3 whether contract tests of an interface (testing that adapter A and adapter B return equivalent results given equivalent inputs) are categorized as integration tests or get their own pattern.

### CHECK-SER-10 — Phase ordering is asserted but the architecture artifact itself violates it

**Location:** `openspec/architecture/phases/PHASE-0-foundation.md` exit criteria; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §3.
**What a casual reader misses:** `phase-exit` "verifies… no REQ from a later phase is `tests-green` (we do not allow phases to complete out of order)." But PHASE-0 tests for REQ-ARCH-* "live in `tools/ci/tests/test_phase0.py` and are runnable without any phase-1+ infrastructure." `tools/ci/` is mentioned only in passing in ARCHITECTURE.md §3, and PHASE-1 owns `tools/spec_lint/`, not `tools/ci/`. Where does `tools/ci/` enter? The artifact is silent on which phase introduces it, yet PHASE-0 depends on it.
**Why this matters in 6 months:** PHASE-0 either (a) cannot complete because `tools/ci/` doesn't exist, or (b) silently introduces `tools/ci/` outside any phase scope, violating the "phase scope is binding" rule.
**What to check:** Add `tools/ci/` skeleton explicitly to PHASE-0 scope, or move REQ-ARCH-* tests under `tools/spec_lint/` and defer them to PHASE-1. Reconcile.

### CHECK-SER-11 — Identifier monotonicity assumes single-writer INDEX.yaml

**Location:** `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §1 + §6; `openspec/architecture/ARCHITECTURE.md` §4.
**What a casual reader misses:** "IDs are allocated by monotonic next-free scan against `openspec/specs/INDEX.yaml`." Two parallel branches each running `tools/spec_lint allocate` will both get `REQ-AUTH-0042`. The collision surfaces only at merge. There's no mention of allocation reservation, merge-time renumbering policy, or whether the immutability rule (§1) survives the renaming forced by a collision.
**Why this matters in 6 months:** As soon as two developers work in parallel on the same domain (inevitable in PHASE-3+), this fires. The "renames are forbidden" rule means the *second* PR to merge has to deprecate and re-add, which is expensive and confusing.
**What to check:** Add an allocation-collision policy to ADR-0004 §1. Common patterns: per-branch reserved ranges, lease-based allocation, or merge-time auto-renumber with `Renumber:` trailer.

### CHECK-SER-12 — The `gate-coverage` meta-gate is self-referential and unverified

**Location:** `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §2.
**What a casual reader misses:** "`gate-coverage` walks every ADR and every principle… and verifies that at least one entry in the table above references it." This relies on parsing ADR text to extract "what this ADR claims to need." There's no schema for "an ADR's enforceable claims." The gate is described as "self-enforcing" but it depends on prose extraction.
**Why this matters in 6 months:** When ADR-0009 lands, either (a) `gate-coverage` doesn't see its claims and silently passes, or (b) the gate fails ambiguously and gets disabled. The meta-gate is the foundation of the entire enforcement story (ARCHITECTURE.md §1: "a missing gate is itself a build failure").
**What to check:** Define the contract for "what `gate-coverage` reads from an ADR." A frontmatter field like `enforced_by: [gate-name, ...]` would make the gate mechanical instead of NLP-flavored.

---

## PROCESS

### CHECK-PROC-13 — ADR amendment numbering inconsistency

**Location:** `openspec/architecture/decisions/ADR-0002-bmad-integration.md` Amendment log: amendments labeled "0001" and "0002"; section titles say "(Amendment 0001.)" and "(Amendment 0002.)" but the rewrite-everything change is "Amendment 0001" while the §7/§8/§9 additions are "Amendment 0002." Body text in §7 says "(Amendment 0002.)" — fine. But the Amendment log says Amendment 0001's CHG is CHG-0010 and Amendment 0002's CHG is "CHG-0010 (TASK-0021)" — both reference CHG-0010, suggesting they were authored in the same change but split into two amendments.
**What a casual reader misses:** The amendment log is meant to be the audit trail. Two amendments from the same CHG suggest the amendment-creation process is malleable, which undermines append-only discipline.
**Why this matters:** Future ADR archaeology depends on amendments being atomic. If reviewers learn that one CHG can produce multiple amendments without rule, the audit value degrades.
**What to check:** Document the policy: one CHG → one amendment, or amendments-per-section-cluster are fine. Make the policy explicit in ADR-0005 (which has the cleaner amendment log).

### CHECK-PROC-14 — `CLAUDE.md` references `ADR-0008` for "a principle without a CI gate is a build failure" but ADR-0008's `gate-coverage` only checks the gate inventory table, not the actual implementation

**Location:** `CLAUDE.md` line citing "A principle without a CI gate is a build failure"; `ADR-0008` §2.
**What a casual reader misses:** A principle can have a gate *row* in the table but no *implementation*. PHASE-0 explicitly ships placeholders that "exit 0 with a TODO comment." `gate-coverage` will pass throughout PHASE-0 and PHASE-1 even though no principle is actually enforced. The claim in CLAUDE.md is true in form but false in substance.
**Why this matters:** Sets a habit of trusting `gate-coverage` as a sufficiency proof. It isn't — it's a *necessary* proof only.
**What to check:** Add a second meta-gate that checks every gate row has a non-placeholder implementation, or stage `gate-coverage` to upgrade from "table-row present" to "implementation present" at PHASE-2 exit. Mention the staged definition in ADR-0008.

### CHECK-PROC-15 — PHASE-5 entry criteria silently introduce a product-side dependency the phase plan cannot satisfy

**Location:** `openspec/architecture/phases/PHASE-5-first-appscript-project.md` entry criteria.
**What a casual reader misses:** "Product side has produced (in a separate PR chain): `openspec/vision.md`, ≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage, ≥ 1 Story." No phase owns the product-side work. PHASE-0 commits *empty templates* (REQ-ARCH-0003). PHASE-1–4 are all infrastructure. PHASE-5 cannot start until product content arrives — and the artifact never says when that arrives or who owns it.
**Why this matters in 6 months:** PHASE-5 is the "load test." If the product side stalls, the load test never runs, and the architecture is never validated end-to-end. The artifact frames this as someone else's problem; in practice it'll be your problem.
**What to check:** Either add a "PHASE-4.5: product seed" with an owner, or change PHASE-5 entry criteria from "product side has produced…" to "if no product content exists, PHASE-5 ships a minimal demo project authored by the architecture team." Don't leave the dependency hanging.

### CHECK-PROC-16 — PHASE-5 has two scope items numbered "4"

**Location:** `openspec/architecture/phases/PHASE-5-first-appscript-project.md` scope lines 36–47.
**What a casual reader misses:** Item 4 is "Per-project BMAD output isolation" (the long block). Item 4 also appears as "Test suite across all four tiers, each red-first." Two scope items share a number; the second silently shadows the first in any "scope item 4" reference.
**Why this matters:** When a future task says "PHASE-5 scope item 4," which one is meant? Minor today, painful when someone audits PHASE-5 completion.
**What to check:** Renumber. Trivial fix, but it's the kind of defect the artifact itself forbids elsewhere (atomicity of identifiers).

---

**Net assessment:** Merge-blocking findings are CHECK-CRIT-01 (internal contradiction in artifact), CHECK-CRIT-02 (live risk during PHASE-0/1), and CHECK-CRIT-03 (P4 enforcement hole). The others are merge-acceptable if you log them in `openspec/STATUS.md` as known follow-ups with explicit owners; do not let them quietly become assumptions.
