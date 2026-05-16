---
id: CHG-0002
title: ADR-0005 amendment 0001 — push invariant
status: in-progress
date: 2026-05-16
phase: PHASE-0
references:
  story: null
  epic: null
  adrs:
    - ADR-0005
---

# CHG-0002 — ADR-0005 amendment 0001: push invariant

## Why

A real divergence was observed on `claude/general-session-KXgas` immediately
after `PR #2` merged: a post-merge rebase advanced the local branch pointer
to master without a follow-up push. The existing
[`ADR-0005` §6 / §7](../../architecture/decisions/ADR-0005-traceability-and-journaling.md)
hooks did not catch it; only an external user-side Stop hook
(`~/.claude/stop-hook-git-check.sh`) surfaced it. That makes the protection
non-architectural: removing the external hook reintroduces silent rot.

Initial response was to propose a new `ADR-0009` introducing per-CHG branches
and four new hooks. On review, that overengineered the fix:

1. Branches are a transient PR-mechanism artifact, not a unit of work
   ([`ADR-0005` §1, §3](../../architecture/decisions/ADR-0005-traceability-and-journaling.md)
   already establishes commits as the atomic unit).
2. The existing hook declarations already cover the necessary firing points;
   they simply need extended responsibilities.

This change implements the minimal fix.

## What changes

[`ADR-0005`](../../architecture/decisions/ADR-0005-traceability-and-journaling.md)
gains an amendment log (§10) and three behavioral extensions:

- **§6 row amend**: `PostToolUse(Bash:git commit)` — also pushes `HEAD`
  to origin as a fast-forward; non-FF aborts the hook with a diagnostic
  (no force-push).
- **§6 row add**: `PostToolUse(mcp__github__merge_pull_request)` →
  `tools/trace/post_merge_sync.py` — fetches origin, fast-forwards the
  working branch to its updated upstream, pushes the FF.
- **§7 paragraph amend**: `Stop` / `SessionEnd` checkpoint also pushes
  committed-but-unpushed work even when the tree is clean.
- **§8 row add**: failure-mode table documents the residual loss window
  (both per-commit and checkpoint hooks must fail to fire).
- **§10 new section**: amendment log; this CHG is row 0001.

[`PHASE-2`](../../architecture/phases/PHASE-2-traceability-runtime.md)
scope is updated to list the new hook implementations and the synthetic
push-invariant tests.

[`.claude/settings.json`](../../../.claude/settings.json) gains the new
`mcp__github__merge_pull_request` matcher under `PostToolUse` and the
amended TODO comments on the existing matchers, so PHASE-2 implementations
slot into already-declared hook positions.

## Out of scope

- Hook **implementations** — they remain PHASE-2 work, red-first.
- Per-CHG branches — explicitly rejected as over-scope; commits are atomic
  enough.
- ADR-0009 — not created; the failure mode is fully addressed by
  amending ADR-0005.

## Tasks

- [`TASK-0003`](tasks/TASK-0003.md) — type `docs`: author the amendment.

## Rollout

- Single commit, single task.
- Substrate change (modifies `openspec/architecture/`), so this PR follows
  the hybrid policy: I open it, you merge it.
- On merge, PHASE-1 work (CHG-0003 onward) proceeds with the amended
  PHASE-2 scope already on record.
