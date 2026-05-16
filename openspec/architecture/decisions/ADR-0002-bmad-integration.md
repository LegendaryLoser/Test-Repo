---
id: ADR-0002
title: BMAD integration (v6.6.0 vendored, native Skills, openspec-routed output)
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0002 — BMAD integration (v6.6.0 vendored, native Skills, openspec-routed output)

## Context

We use BMAD personas (PM, Architect, SM, Dev, PO) and the Test Architect
(TEA) discipline as the workflow surface. BMAD v6.6.0 is released (April
2026), MIT-licensed, and ships a "Skills Architecture" that installs
directly into Claude Code's native `.claude/skills/` directory — no
wrapper layer is required.

This ADR captures the actual integration after the BMAD install was
empirically validated in CHG-0010. The original ADR text designed a
wrapper-isolation strategy based on outdated assumptions about BMAD
exposing personas as Claude Code subagents — that turned out to be
neither how BMAD v6 works nor necessary, since native Skills are a
better-engineered alternative we couldn't have improved upon.

## Decision

1. **Version pin: BMAD v6.6.0.** Pinned in `_bmad/_config/manifest.yaml`
   at install time (canonical version source). The pinned install command
   lives in [`scripts/install_bmad.sh`](../../../scripts/install_bmad.sh).

2. **Install path: `_bmad/`** (underscore-prefixed, per upstream's
   convention). Contains BMAD core, the `bmm` module, custom-overrides
   slot, and runtime scripts. **Total size: ~172 KB.**

3. **Integration: native Claude Code Skills under `.claude/skills/`.**
   BMAD installs 42 Skills directly. No wrapper files. Claude Code
   discovers them automatically. **Total size: ~2.4 MB.**

4. **Vendored storage.** Both `_bmad/` and `.claude/skills/` are committed
   to git. This aligns with our SoT principle (P1) and our container-
   reclaim resilience design (ADR-0005 §8): zero network dependency on
   session start; reproducible across machines. Upgrades are deliberate
   substrate PRs (rare cadence; v6.x minors land months apart).

5. **Output routing under `openspec/_bmad-output/`.** BMAD's `bmm` module
   has three configurable output paths:
   - `bmm.planning_artifacts` → `openspec/_bmad-output/planning`
   - `bmm.implementation_artifacts` → `openspec/_bmad-output/implementation`
   - `bmm.project_knowledge` → `openspec/_bmad-output/knowledge`
   This keeps all BMAD-generated content inside the OpenSpec namespace —
   the SoT for product knowledge. No top-level `docs/` directory is
   created (install side effect; cleaned up by the install script).

6. **Upgrade procedure:**
   - Bump the pinned version in [`scripts/install_bmad.sh`](../../../scripts/install_bmad.sh).
   - Run the script.
   - Open a substrate PR with the diff (large, expected; mostly
     vendored skill markdown).
   - You merge after review.

7. **No project code depends on BMAD directly.** Tooling integration lives
   under `tools/tea/` (PHASE-1+ work; not yet implemented). All BMAD
   skill invocation is via Claude Code's native skill system.

## 7. Staging discipline for `openspec/_bmad-output/`

(Amendment 0002.) The `openspec/_bmad-output/` directory holds **drafts**
produced by BMAD skills. It is **non-authoritative** and outside the
addressable artifact network. The full discipline lives in
[`openspec/_bmad-output/STAGING.md`](../../_bmad-output/STAGING.md);
this section binds the rules.

**Hard invariants:**

- **The matrix MUST NOT reference any path under `openspec/_bmad-output/`.**
  Matrix builder (PHASE-2) excludes the directory unconditionally.
- **INDEX.yaml MUST NOT reference any path under `openspec/_bmad-output/`.**
  REQ-IDs live only in canonical spec files.
- **spec_lint rules MUST exclude `openspec/_bmad-output/` from canonical
  checks.** REQ-ID format, frontmatter, atomicity, anti-aliasing, and
  cross-reference rules do not apply to staging drafts. Bind those
  rules at *promotion time* (when the draft moves to its canonical
  home), not before.

**Promotion** is the act of moving a draft from staging to its canonical
home (`openspec/{briefs,prd,epics,stories,architecture}/` or
`openspec/specs/<domain>/<feature>.spec.md`) with a stable ID and
frontmatter. Promotion is a `docs`-type TASK under an explicit CHG;
the matrix records the promotion commit; spec_lint validates the
promoted artifact.

A future spec_lint rule **`stale-staging`** (deferred CHG) flags drafts
sitting unpromoted past a configurable threshold — forces triage,
prevents accumulation.

## 8. Upgrade safeguards

(Amendment 0002.) A BMAD version bump is a substrate PR (hybrid policy
→ you merge). The following safeguards apply at every upgrade:

1. **Smoke test.** Before merging, exercise at least one BMAD skill
   end-to-end against a known input and assert the output shape.
   Implementation: PHASE-2 work; lives in `tools/ci/smoke_bmad.py`.
2. **Skill-removal acknowledgment.** A CI check compares
   `_bmad/_config/skill-manifest.csv` between base and head. If a skill
   is *removed* without a `Skill-Removal-Acknowledged: <skill-id>`
   trailer on the upgrade commit, the PR is blocked. Implementation:
   PHASE-2 alongside other trace gates.
3. **Full test suite must pass.** Existing P3 discipline — every PR
   runs the full test suite. A breaking change in a referenced skill
   surfaces as a failing test.
4. **Rollback procedure.** A BMAD upgrade that turns out to break
   something post-merge rolls back atomically via `git revert <upgrade-sha>`.
   Vendoring makes the prior state unambiguous (every byte was in git);
   the revert restores it without network dependency.
5. **Compatibility statement.** Each upgrade PR's description declares
   the prior version, the new version, and whether spec-format
   migrations were required. (Spec-format versioning is itself a
   future concern; for now the statement reads "no migration
   required" or names the migration.)

## 9. Per-project output isolation (PHASE-5+)

(Amendment 0002.) BMAD v6 provides a **4-layer config merge** (verified
empirically in `_bmad/scripts/resolve_config.py`):

```
1. {project-root}/_bmad/config.toml              (installer-owned team)
2. {project-root}/_bmad/config.user.toml         (installer-owned user)
3. {project-root}/_bmad/custom/config.toml       (human-authored team, committed)
4. {project-root}/_bmad/custom/config.user.toml  (human-authored user, gitignored)
```

`{project-root}` is the working directory passed to BMAD's resolver. When
Claude Code runs with CWD = `projects/<name>/`, the resolver merges in
project-scoped overrides under `projects/<name>/_bmad/custom/config.toml`.
The `custom/` layer is **installer-untouched** — overrides survive BMAD
upgrades unchanged.

**Per-project output isolation:**

- Repo-level (in `_bmad/config.toml`, set at install): default routing
  to `openspec/_bmad-output/{planning,implementation,knowledge}`.
- Per-project override (in `projects/<name>/_bmad/custom/config.toml`,
  hand-authored when the project is created): routes to
  `projects/<name>/openspec/_bmad-output/{planning,implementation,knowledge}`.

The promotion protocol in §7 still applies per-project: a project's
drafts promote to *that project's* canonical homes (`projects/<name>/openspec/briefs/`,
etc., using the project-scoped openspec overlay from
[`ADR-0001`](ADR-0001-monorepo-layout.md)).

**Workflow constraint:** sessions working on a specific project must run
with CWD set to `projects/<name>/` for BMAD to pick up per-project
overrides. Sessions at the repo root use repo-level defaults (for
cross-project / monorepo-level BMAD work). Documenting this is a PHASE-5
deliverable; the first project sets the precedent.

**This isolation is reliable today** — verified against the vendored
BMAD source. It is *not yet exercised* (no projects exist); first
exercise lands in PHASE-5.

## Consequences

- Zero network dependency at session start.
- Upgrades are atomic (one substrate PR per version bump) and reviewable
  (diff shows exactly what changed).
- The 2.6 MB commit is a one-time cost; most repos vendor larger
  dependencies without trouble.
- BMAD's native Skills are first-class Claude Code constructs — no
  wrapper maintenance burden, no per-version adapter code.
- Output routing under `openspec/` enforces P1 (SoT) for product knowledge.
- **`openspec/_bmad-output/` is staging — invisible to the addressable
  artifact network. P1 preserved: each artifact has exactly one canonical
  home; drafts never compete with authoritative artifacts.** (§7)
- **Upgrades are safeguarded at four levels** (smoke test, manifest
  diff, test suite, rollback procedure). A bad upgrade is recoverable. (§8)
- **Per-project isolation works via BMAD's standard config merge** —
  upgrade-resistant, no custom code needed. (§9)

## Compliance

- **`bmad-direct-reference` lint rule** (PHASE-1, CHG-0012) checks that
  no file under `tools/`, `packages/`, or `projects/` references a path
  under `_bmad/` except authorized integration points (`tools/tea/`
  when it exists).
- **`top-level-allowlist` lint rule** (PHASE-1, CHG-0011) enforces that
  `_bmad`, `scripts`, `.claude` (with `skills/` inside) are the BMAD-
  related top-level entries.
- **`matrix-drift` gate** (PHASE-2) excludes `openspec/_bmad-output/`
  from index/matrix construction.
- **`skill-removal-acknowledged` gate** (PHASE-2) blocks BMAD upgrade
  PRs that remove skills without explicit acknowledgment.
- **`stale-staging` gate** (deferred CHG) flags long-unpromoted drafts.
- The pinned version in `_bmad/_config/manifest.yaml` is checked in CI
  against the `install_bmad.sh` version comment (PHASE-2).

## Amendment log

| Amendment | CHG     | Sections | Summary                                                                                                         |
|-----------|---------|----------|-----------------------------------------------------------------------------------------------------------------|
| 0001      | CHG-0010 | All       | Complete rewrite to match BMAD v6.6.0 empirical reality. Install path: `_bmad/` (was `bmad/`). Integration: native Claude Code Skills under `.claude/skills/` (was thin wrappers under `.claude/agents/` and `.claude/commands/`). Output routing under `openspec/_bmad-output/` documented. Vendored storage selected over install-on-session-start after user-confirmed cost/benefit analysis. The wrapper-isolation strategy from the original ADR is dropped — native Skills make it unnecessary. |
| 0002      | CHG-0010 (TASK-0021) | §7, §8, §9 + Consequences + Compliance | Address the SoT defect surfaced in chat: `openspec/_bmad-output/` becomes explicit **STAGING** with hard invariants (matrix/INDEX/lint never reference it; promotion is the only path to canonical). Adds **upgrade safeguards** (smoke test, skill-removal acknowledgment, rollback). Documents **per-project output isolation** via BMAD's verified 4-layer config merge — reliable today, exercised first in PHASE-5. |

Amendments are append-only. A subsequent material change to behavior
introduced by a prior amendment requires a new amendment row, never an
edit to a prior row.
