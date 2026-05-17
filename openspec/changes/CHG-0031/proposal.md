---
id: CHG-0031
title: Session continuity scaffold (STATUS.md + meta-test + CLAUDE.md pointer)
status: in-progress
date: 2026-05-17
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0005
    - ADR-0008
---

# CHG-0031 — Session continuity scaffold

## Why

User-flagged urgency: this session is running long and **cross-session
state recovery is not currently designed for**. The architecture
specifies (per [`ADR-0005` §2](../../architecture/decisions/ADR-0005-traceability-and-journaling.md))
a traceability matrix at `openspec/traceability/matrix.yaml` regenerated
by `tools/trace/rebuild.py` (PHASE-2). Until PHASE-2 lands that
infrastructure, a new session arriving at this repo has only:

- `git log` (commits with trailers — but merge commits drop them)
- `openspec/specs/INDEX.yaml` (REQs only, no commit/task linkage)
- The CHG envelopes themselves (drift from reality possible)

Missing: the **decision context**, **audit-finding ledger**, **open
architectural questions**, and **roadmap with priorities**. These
exist in this session's chat but evaporate when the session ends.

This CHG ships the minimum viable resume artifact and points new
sessions at it, so progress is recoverable without re-litigating
decisions.

## What changes

### `openspec/STATUS.md` (new)

Human-readable session-resume document. Sections:

- Last updated, active phase, last master commit, open PRs, test count.
- **CHG status table** — every CHG with status (merged/open/queued)
  and PR link.
- **Audit findings ledger** — every finding from the in-session audit
  with status (CLOSED/OPEN/IN-PROGRESS) and the CHG that resolves it.
- **Open architectural questions** — decisions pending across sessions.
- **Sequenced roadmap** — Tier 0..5 with checkbox status.
- **Recent decisions** — short log of consequential calls made in
  recent sessions with the rationale.
- **Next session: start here** — explicit pointer to the next action.

Hand-maintained for now; the PHASE-2 `SessionStart` resume hook
mentioned in `ARCHITECTURE.md` §11 will eventually emit a generated
version of this same content.

### `CLAUDE.md` addendum (one paragraph in "How to start any session")

Adds STATUS.md as the first artifact to read, before the active phase
file. New sessions know where to look.

### `tools/ci/tests/test_status_resume.py` (new)

Meta-test asserting `openspec/STATUS.md` exists and contains all
required sections. Prevents the resume artifact from silently
decaying (e.g., someone refactoring it without preserving the
schema).

### `openspec/specs/_meta/spec-storage.spec.md` extended

- **REQ-SPEC-0016** — `openspec/STATUS.md` exists and contains the
  sections required for a cold session to resume work without
  re-reading the chat history.

## Out of scope

- **`tools/trace/rebuild.py`** — PHASE-2 deliverable. Hand-built
  matrix.yaml would itself violate CLAUDE.md's "Hand-editing
  matrix.yaml is forbidden" rule. STATUS.md carries the human-readable
  equivalent until PHASE-2 ships rebuild.py.
- **BMAD workflow integration** — the user's broader request to run
  BMAD reviews from the planning phase forward. STATUS.md will
  document this as the next session's first action; the actual
  invocation happens in a follow-up CHG once continuity is secured.
- **Decisions log automation** — for now, decisions are added to
  STATUS.md manually as part of each CHG's GREEN commit. Mechanization
  is a future concern.

## Tasks

- **TASK-0033 (RED)** — meta-test asserting STATUS.md present + required
  sections. RED because STATUS.md doesn't exist yet.
- **TASK-0034 (GREEN)** — write STATUS.md, update CLAUDE.md pointer,
  add REQ-SPEC-0016. Meta-test passes.

## Risk

- **STATUS.md drift.** If someone updates the implementation without
  updating STATUS.md, the resume artifact gets stale. Mitigation:
  meta-test asserts STRUCTURAL sections exist but cannot assert
  CONTENT freshness; that's a discipline check, not mechanical.
  Future: CHG that mechanizes "STATUS.md must list every merged CHG"
  via parsing `openspec/changes/`.
- **Hand-maintained matrix.yaml** is explicitly out of scope to avoid
  the CLAUDE.md forbidden-list violation. STATUS.md fills the gap
  with weaker semantics until PHASE-2.
