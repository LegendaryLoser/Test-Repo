# READY — check-implementation-readiness (opus) — Wave 1

**Source transcript:** [`raw-transcripts/READY-agent-a75c2119fca66f68b.jsonl`](../raw-transcripts/READY-agent-a75c2119fca66f68b.jsonl)
**Sub-agent description:** `Implementation readiness check`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a75c2119fca66f68b`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-check-implementation-readiness` skill via the Skill tool. Apply it to validate whether the architecture artifact is complete enough for implementation phases to proceed without ambiguity.

The architecture artifact consists of 15 files under /home/user/Test-Repo/:

- openspec/architecture/ARCHITECTURE.md (the structural narrative)
- openspec/architecture/decisions/ADR-0001 through ADR-0008 (8 architecture decision records)
- openspec/architecture/phases/PHASE-0 through PHASE-5 (6 phase entry/exit specs)

Mapping to the skill's expected inputs:
- The "Architecture spec" is ARCHITECTURE.md + the 8 ADRs.
- "Phases / Epics" are the 6 PHASE-* files (treat each phase as a high-level epic).
- "PRD" and "UX" are intentionally NOT yet authored — vision.md/briefs/prd/epics/stories are empty templates (architecture artifact §12 says product content is out of scope). Flag this absence as a readiness gap if it blocks any phase from starting.

For each readiness gap, ask:
- Is there a defined input artifact for every output the phase must produce?
- Are all REQ-IDs the phase references actually defined somewhere?
- Are all gate names the phase references defined in ADR-0008?
- Are all hook names the phase references defined in ADR-0005?
- Are all tools (`tools/<x>`) the phase references defined in ARCHITECTURE.md §3 layout?
- Are all status enums, trailer names, file formats referenced internally consistent?
- Does any phase have an exit criterion that no later phase reads as an entry criterion (orphaned outputs)?
- Does any phase have an entry criterion that no earlier phase produces (unreachable phases)?

REQUIRED OUTPUT:
- Stable IDs: prefix `READY-` (e.g. READY-01, READY-02; severity inline as BLOCKING/SHOULD-FIX/NICE-TO-HAVE — map to CRITICAL/SERIOUS/PROCESS for downstream consolidation)
- Each finding: phase or artifact affected, what's missing, what breaks if implementation proceeds without it
- Minimum 12 findings
- 1500-2500 words
- No preamble, no fixes

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have read all 15 files. Now I'll produce the readiness analysis as the user requested.

# Implementation Readiness Review — Architecture Artifact

## READY-01 — BLOCKING — PHASE-1 BMAD install path contradicts ADR-0002 (`bmad/` vs `_bmad/`)

**Affected:** PHASE-1-spec-hygiene.md §Scope items 3 and 4; ADR-0002 §Decision items 1–3; ARCHITECTURE.md §3.

PHASE-1 §Scope says "`bmad/` installation per ADR-0002, pinned in `bmad/config.yaml`" and "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA) and core commands." Both statements are inconsistent with ADR-0002 (amendment 0001), which mandates install path `_bmad/` (underscore-prefixed), the manifest at `_bmad/_config/manifest.yaml` (not `bmad/config.yaml`), and an explicit "**No wrapper files**" stance under "Integration: native Claude Code Skills under `.claude/skills/`." ARCHITECTURE.md §3 further marks `.claude/agents/` and `.claude/commands/` as "(legacy slot — empty in v6 native-skills model)." PHASE-1 has not been updated for the ADR-0002 amendment. If implementation proceeds, PHASE-1 will install BMAD to the wrong directory, fail the `top-level-allowlist` and `bmad-direct-reference` gates listed in its own exit criteria, and produce wrapper files that violate ARCHITECTURE.md §3.

## READY-02 — BLOCKING — `bmad-version-pin` and `bmad-smoke-test` gates referenced by PHASE-2 are not in ADR-0008 §1

**Affected:** PHASE-2-traceability-runtime.md §Scope item 4; ADR-0008 §1 Gate inventory.

PHASE-2 §Scope item 4 names `skill-removal-acknowledged`, `bmad-version-pin`, and `bmad-smoke-test` as CI gates to implement. ADR-0008 §1's Gate inventory table does not contain any of these three rows. ADR-0008 §2 (`gate-coverage`) states "A missing reference fails the build. Adding a new ADR or principle without adding a gate is therefore impossible." Since these gates trace back to ADR-0002 §7/§8 but are not enumerated in ADR-0008's authoritative inventory, the `gate-coverage` meta-gate will either fail on the PHASE-2 PR (if interpreted strictly: each ADR must have a gate in the inventory) or quietly skip them (defeating the purpose). The reverse direction — `gate-coverage` walking each gate to its ADR — has no defined home for these three. The PHASE-2 exit criterion "All gates in ADR-0008 §1 not owned by `tools/spec_lint`" then literally excludes them.

## READY-03 — BLOCKING — `commit-trailers-valid` trigger conflict between ADR-0008 §1 and §5

**Affected:** ADR-0008 §1 (Gate inventory row `commit-trailers-valid`) and §5 (Local enforcement).

The inventory row lists `commit-trailers-valid` Trigger column as "pre-receive hook." §5 says "`commit-trailers-valid` runs pre-commit and rejects malformed messages before they enter history." ADR-0005 §6's hooks table identifies `PreToolUse(Bash:git commit)` running `tools/trace/validate_commit.py`. Three different gating surfaces (pre-receive, pre-commit, PreToolUse) for the same enforcement. Implementation cannot proceed until the canonical enforcement surface is named once. If implementers pick "pre-receive," local agents bypass it; if "pre-commit," server-side pushes bypass it; if "PreToolUse," non-Claude-Code commits bypass it.

## READY-04 — BLOCKING — No PRD/Vision artifact exists, but PHASE-5 entry depends on it

**Affected:** PHASE-5-first-appscript-project.md §Entry criteria; ARCHITECTURE.md §12; user-confirmed empty `openspec/vision.md`, `briefs/`, `prd/`, `epics/`, `stories/`.

PHASE-5 §Entry criteria require "Product side has produced (in a separate PR chain): `openspec/vision.md`, ≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage, ≥ 1 Story." ARCHITECTURE.md §12 explicitly excludes product content from this artifact. No phase produces this content; no ADR commissions it; no roadmap names an owner. The Epic reconciliation flow in ARCHITECTURE.md §5 (top-down meets bottom-up at the Epic) is the gating contract for `EPIC.status = ready-for-dev`, which PHASE-5 must reach. With product content uncommissioned, PHASE-5 has an unsatisfiable entry criterion and the architecture artifact is therefore not implementation-ready end-to-end — it is only implementation-ready through PHASE-4. Flag this as the most consequential gap.

## READY-05 — BLOCKING — `phase-exit` gate semantics conflict with PHASE-0 self-bootstrap

**Affected:** ADR-0008 §3; PHASE-0-foundation.md §Exit criteria/Exit gate; ARCHITECTURE.md §11.

ADR-0008 §3 says "`phase-exit` gate runs on merge to `main` and verifies: The current phase's exit REQs are all `tests-green` in the matrix." But PHASE-0's exit gate is `phase-exit` and PHASE-2 is the phase that builds the matrix and the `phase-exit` runtime (PHASE-2 §Scope item 4 lists `phase-exit` among gates "promoted from PHASE-0 placeholders to real"). PHASE-0 has no way to evaluate its own exit gate because the matrix and runtime do not exist yet. PHASE-0 §Exit criteria explicitly say "Tests for REQ-ARCH-* are written in PHASE-0 itself, red-first, and turn green as the scaffolding completes" — but `red-before-green` and `matrix-drift` are also PHASE-2-implemented. The bootstrap order is undefined: either PHASE-0 ships without `phase-exit` (and the principle "every phase has an exit gate" is silently violated for one phase), or PHASE-0 cannot complete.

## READY-06 — BLOCKING — Hook name mismatch: `commit-msg` vs `PreToolUse(Bash:git commit)`

**Affected:** ADR-0005 §6; ADR-0008 §5; PHASE-2-traceability-runtime.md §Scope item 1.

PHASE-2 §Scope item 1 lists "`validate_commit.py` (PreToolUse:git commit + commit-msg hook)" — naming two different hook surfaces. ADR-0005 §6's hooks table only declares `PreToolUse(Bash:git commit)`. A git `commit-msg` hook is a different mechanism (git-native, runs for non-Claude-Code commits as well). ADR-0005 §6 does not declare a `commit-msg` hook. REQ-ARCH-0008 requires "`.claude/settings.json` is present; hooks declared in ADR-0005 are listed" — but PHASE-2 introduces a hook that was never declared in ADR-0005, breaking the single-source-of-truth principle for hook inventory.

## READY-07 — SHOULD-FIX — `tools/tea/` referenced but layout in ARCHITECTURE.md §3 is the only definition

**Affected:** ARCHITECTURE.md §3 (`tools/tea/`); ADR-0002 §Decision item 7; PHASE-1 §Scope item 5.

ARCHITECTURE.md §3 lists `tools/tea/` with the comment "TEA workflow integration." ADR-0002 §Decision item 7 says "`tools/tea/` (PHASE-1+ work; not yet implemented)." PHASE-1 §Scope item 5 says "`tools/tea/` skeleton — invokes TEA workflows; integration with CI deferred to PHASE-2." Neither PHASE-1 nor any ADR defines what TEA actually is, what its workflows are, what its interface looks like, or what "integration with CI" means. ARCHITECTURE.md §1 invokes "BMAD + TEA for workflow" as a principle but defines neither acronym. PHASE-1 cannot ship `tools/tea/` without a contract — implementers will improvise, and PHASE-2 cannot wire it to CI without a defined interface.

## READY-08 — SHOULD-FIX — Status enum inconsistency between ADR-0005 §3 and ADR-0004 §5

**Affected:** ADR-0005 §3 (commit trailer `Tests-Status`); ADR-0004 §5 (REQ block `status`); CLAUDE.md "How to commit."

ADR-0005 §3 specifies `Tests-Status: <none|red|red→green|green|deprecated>` (5 values, includes the transitional `red→green`). ADR-0004 §5's REQ frontmatter `status` enum is `draft | tests-red | tests-green | reviewed | merged | deprecated` (6 values, names differ — `red` vs `tests-red`, `green` vs `tests-green`, includes `reviewed` and `merged` which the commit trailer omits, omits `none` which the trailer includes). These are different fields but their referents overlap. ADR-0005 §4 then says "A REQ may not skip from `draft` to `tests-green`; it must pass through `tests-red`" — using the REQ enum verbatim, so the field is "REQ status." But ADR-0005 §3's trailer is "Tests-Status," conflating test state with REQ state. The `red-before-green` gate cannot be implemented unambiguously until the two enums and their semantic mapping are reconciled.

## READY-09 — SHOULD-FIX — `Material-Architecture-Change: true` trailer mentioned once and never defined

**Affected:** ARCHITECTURE.md preamble; ADR-0005 §3.

ARCHITECTURE.md preamble says modifications "require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate." ADR-0005 §3's trailer specification — which is "every commit must carry" — lists only `Task`, `Requirements`, `Tests-Status`, `Phase`. `Material-Architecture-Change` is not enumerated, not validated by any gate in ADR-0008 §1, and "Phase-0 re-gate" is not defined as a procedure. CLAUDE.md also fails to mention it. Implementation will either silently drop the trailer or implement it ad-hoc.

## READY-10 — SHOULD-FIX — `Bootstrap:` trailer (ADR-0006 §4) is undeclared in ADR-0005 §3 trailer list

**Affected:** ADR-0006 §4 (`Bootstrap: <reason>` trailer + `bulk-green-start` gate); ADR-0005 §3; ADR-0008 §1.

ADR-0006 §4 introduces `Bootstrap: <reason>` as a mandatory trailer to permit > N green tests in a single commit, gated by `bulk-green-start`. Neither the trailer nor the gate appears in ADR-0005 §3 (mandatory trailer list), nor in ADR-0008 §1 (gate inventory), nor in CLAUDE.md (commit guidance). The `commit-trailers-valid` gate (ADR-0008 §1) cannot recognize trailers that aren't in its source ADR. Implementers will not know whether `bulk-green-start` is a real gate or aspirational text; CI will either silently miss it or fail unpredictably.

## READY-11 — SHOULD-FIX — `Checkpoint: true` trailer has an exemption file that no phase commits

**Affected:** ADR-0008 §6 references `tools/trace/checkpoint_exemptions.yaml`; no phase lists this file in scope.

ADR-0008 §6 states "the `Checkpoint: true` trailer (ADR-0005 §7) is the **only** sanctioned partial-bypass and applies to a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`." Neither PHASE-0 (which authors hook declarations), PHASE-1 (`tools/spec_lint`), nor PHASE-2 (`tools/trace` implementations) lists `checkpoint_exemptions.yaml` in scope. Without this file, the checkpoint mechanism — central to crash recovery in ADR-0005 §7 and ADR-0005 §8 — cannot work: every checkpoint commit will fail `red-before-green` and `commit-trailers-valid` since no gate knows to skip it.

## READY-12 — SHOULD-FIX — `tools/ci/` is referenced as a gate owner but has no implementation phase

**Affected:** ADR-0008 §1 Owner column ("tools/ci"); ARCHITECTURE.md §3 (`tools/ci/`); ADR-0002 §7 (`tools/ci/smoke_bmad.py`).

ADR-0008 §1 names `tools/ci` as the owner for `cost-budget`, `cache-hit-regression`, and `gate-coverage`. ADR-0002 §7 (per the §8 amendment 0002 references) names `tools/ci/smoke_bmad.py`. No phase has `tools/ci/` in scope. PHASE-0 only commits workflow YAML stubs. PHASE-2 §Scope item 4 lists those gates among ones to promote but assigns them to `tools/trace/`, not `tools/ci/`. Either `tools/ci/` is a planning omission (no phase builds it) or there is an unresolved ownership conflict between `tools/trace/` and `tools/ci/` for these gates. Coverage assertions for these gates cannot be evaluated in PHASE-2 without a clear owner.

## READY-13 — SHOULD-FIX — Anti-aliasing threshold `tools/spec_lint/config.yaml` referenced but not commissioned

**Affected:** ADR-0004 §4; PHASE-1 §Scope.

ADR-0004 §4 says the anti-aliasing threshold "is pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." PHASE-1 §Scope lists `tools/spec_lint/` and `tools/spec_lint/tests/` but never names `config.yaml`, the threshold value, the n-gram size, or the quarterly review task. The `anti-aliasing` gate (ADR-0008 §1) cannot ship without the pinned threshold. Implementers will pick a value, calling it temporary; the "reviewed quarterly" cadence has no scheduling artifact in any phase, no ADR amendment hook, no owner.

## READY-14 — SHOULD-FIX — Phase 3's `direct-anthropic-import-banned` lives in PHASE-1 inventory but has no concrete target until PHASE-3

**Affected:** ADR-0008 §1 (lints owned by `tools/spec_lint`, every PR); PHASE-1 §Exit criteria; PHASE-3 §Scope item 6.

ADR-0008 §1 lists `direct-anthropic-import-banned` Trigger as "every PR," owned by `tools/spec_lint`. PHASE-1 §Exit criteria require "Every gate in ADR-0008 §1 owned by `tools/spec_lint` is implemented and has ≥ 1 passing test that was red in a prior commit." PHASE-3 §Scope item 6 says "CI gate `direct-anthropic-import-banned` now has a concrete target." This means the rule exists from PHASE-1 but has nothing to detect against until PHASE-3. ADR-0006 §5 demands 100% REQ coverage; if the lint rule is REQ-backed by `REQ-SPEC-*`, the test in PHASE-1 must be a self-test (lint runs on a synthetic fixture). PHASE-1 §Scope item 6 names `openspec/specs/_meta/spec-storage.spec.md` but not the corresponding test data layout. The intermediate state — rule live, no production target, REQ-coverage gate at 100% — is unspecified.

## READY-15 — NICE-TO-HAVE — Orphaned PHASE-1 output: BMAD wrappers under `.claude/agents/` and `.claude/commands/`

**Affected:** PHASE-1 §Scope item 4; ARCHITECTURE.md §3; PHASE-2/3/4/5 §Entry criteria.

PHASE-1 §Scope item 4 commissions `.claude/agents/` and `.claude/commands/` wrappers. No later phase has an entry criterion that depends on these wrappers — PHASE-2's hook implementations are independent of BMAD wrappers; PHASE-3, 4, 5 reach Epics through the reconciliation flow in ARCHITECTURE.md §5 which doesn't textually require these wrappers. Per ADR-0002 (amendment 0001), these directories are "legacy slot — empty in v6 native-skills model." This is an orphaned output: produced in PHASE-1, read by no later phase, and contradicted by ADR-0002 (ties back to READY-01). Even if READY-01 is resolved by deleting these wrappers from PHASE-1 scope, the orphan analysis still helps confirm no downstream entry criterion is silently broken by their removal.

## READY-16 — NICE-TO-HAVE — Hook `PostToolUse(Bash:*test*)` glob pattern is ambiguous

**Affected:** ADR-0005 §6 hooks table.

ADR-0005 §6 declares hook trigger `PostToolUse(Bash:*test*)` for `journal_tests.py`. The glob `*test*` matches `npm test`, `pytest`, `jest`, but also `git test-rev-parse`, `latest`, `attest`, and any command containing "test" as a substring. No allow-list or runner detection is specified. Implementers in PHASE-2 will need to invent a runner-detection contract that ADR-0005 should have pinned (e.g. a closed enumeration: `pytest`, `npm test`, `jest`, `vitest`, `clasp run e2e`). Without it, the `tests_run` journal events will be inconsistent across sessions, undermining ADR-0005 §1's "Sources of truth" guarantee that journals are reliable.

## READY-17 — NICE-TO-HAVE — REQ-LIBPY, REQ-LIBTS, REQ-LLM, REQ-SPEC, REQ-CI ID domains are introduced lazily

**Affected:** ARCHITECTURE.md §4 (Identifier table); ADR-0004 §1; PHASE-1, 2, 3, 4 §Scope and §Exit criteria.

ARCHITECTURE.md §4 enumerates only `REQ-ARCH-*` explicitly. ADR-0004 §1 generalizes the format. Each later phase introduces a new domain: PHASE-1 (`REQ-SPEC-*`), PHASE-2 (`REQ-CI-*`), PHASE-3 (`REQ-LLM-*`), PHASE-4 (`REQ-LIBTS-*`, `REQ-LIBPY-*`). The domain inventory is implicit — assembled by reading all phase files. ADR-0004 §1 says "DOMAIN is uppercase alphanumeric ≤ 12 chars," but does not pin the canonical list. The `req-id-format` gate (ADR-0008 §1) presumably accepts any compliant format, so this is procedural rather than blocking — but the lack of a central domain registry (e.g. in `openspec/specs/INDEX.yaml` schema) means typos like `REQ-LIBS-*` vs `REQ-LIBTS-*` will not fail lint until much later. A pre-PHASE-1 inventory in ARCHITECTURE.md §4 would harden the contract.

## READY-18 — NICE-TO-HAVE — `tools/ci/tests/test_phase0.py` is named in PHASE-0 but no test-discovery convention is documented

**Affected:** PHASE-0 §Exit criteria final paragraph; ARCHITECTURE.md §3 (`tools/ci/`).

PHASE-0 §Exit criteria say tests "live in `tools/ci/tests/test_phase0.py` and are runnable without any phase-1+ infrastructure (they only read files)." ARCHITECTURE.md §3 shows `tools/ci/` but no `tests/` subdir. No phase commissions a Python or Node test-runner configuration for `tools/`. ADR-0006 §1's four tiers map to `projects/<project>/tests/{unit,integration,e2e,stochastic}/` and `packages/<package>/tests/`, not to `tools/`. The PHASE-0 self-test layer is therefore architecturally ungrounded — implementers must invent a runner location and a CI invocation that ADR-0006 doesn't cover. Resolvable inline but worth flagging because it's the first thing PHASE-0 implementers will hit.

## READY-19 — NICE-TO-HAVE — STATUS.md and `SessionStart` resume hook output described in CLAUDE.md but not in any phase scope

**Affected:** CLAUDE.md "How to start any session" steps 1 and 4; ADR-0005 §6 hooks table.

CLAUDE.md (project guidance) tells agents to "Read `openspec/STATUS.md` first" and to "Run the SessionStart resume hook output (printed automatically once PHASE-2 lands)." `STATUS.md` is not in PHASE-0 scope (PHASE-0 §Scope items 1–12 do not include it). ADR-0005 §6 names the `SessionStart` hook running `tools/trace/resume.py` (commissioned in PHASE-2 §Scope item 1), but `resume.py`'s output format and its relationship to `STATUS.md` are unspecified. Two facts (STATUS.md content, resume hook output) appear to overlap with no SoT designation, violating principle P1. This is procedural until PHASE-2 implementers must decide which is canonical.

---

**Roll-up:** The artifact is internally consistent enough for PHASE-0 scaffolding work to begin on a best-effort basis, but six BLOCKING findings (READY-01 through READY-06) prevent PHASE-1 and PHASE-2 implementation from proceeding without ambiguity. The most severe is READY-04: no product artifact exists, no phase commissions one, and PHASE-5 cannot start without it. The PHASE-1 / ADR-0002 contradiction (READY-01) and the trio of CI-gate inventory gaps (READY-02, READY-06, READY-10) reflect amendment drift — ADR-0002 amendment 0001/0002 and ADR-0005 amendment 0001 have not been threaded back through the phase files or ADR-0008. Recommend treating amendment-propagation as its own readiness CHG before PHASE-1 starts.

**File paths reviewed:**
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
