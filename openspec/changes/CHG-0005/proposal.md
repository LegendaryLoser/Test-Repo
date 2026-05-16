---
id: CHG-0005
title: spec_lint — prose-xref-banned + xref-resolves (cross-file rules)
status: in-progress
date: 2026-05-16
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0004
    - ADR-0008
---

# CHG-0005 — spec_lint: prose-xref-banned + xref-resolves

## Why

Third slice of PHASE-1 spec_lint. Both rules in this CHG enforce
[`ADR-0004` §2](../../architecture/decisions/ADR-0004-spec-storage-discipline.md):

- **`prose-xref-banned`** — phrases like "the auth spec" or "the login requirement" are forbidden inside artifact-bearing files. <!-- spec-lint: allow prose-xref-banned -->
  Every reference must be by stable ID + file path. This is the paper-derived
  discipline — prose references are the channel through which semantic-recall
  failure modes (false recall, near-neighbor collapse) enter the system.
- **`xref-resolves`** — every relative markdown link and every
  `REQ-X-NNNN @ path` reference must resolve to an existing file (and, for
  REQ references, the file must contain that REQ-ID).

These are the first rules that operate over **arbitrary markdown** rather
than parsed REQ blocks; they take a `list[tuple[Path, str]]` of (path, text)
pairs. The caller decides which files to include — for tests, synthetic
fixtures; for the eventual CLI / CI gate, the set of files in `openspec/`.

## What changes

### Rules

- `tools/spec_lint/rules/prose_xref_banned.py` — denylist of prose patterns (`the X spec`, `the X requirement`, `the X ADR`, …). <!-- spec-lint: allow prose-xref-banned -->
  Excludes code blocks and lines marked with the inline allow marker
  `spec-lint: allow prose-xref-banned`. A pattern that is followed (within
  the same line) by a stable ID is allowed (the prose is parenthetical to
  an explicit reference).
- `tools/spec_lint/rules/xref_resolves.py` — two passes per file:
  - Markdown links `[text](https://example.com/path)` — relative paths must
    resolve from the file's directory; absolute URLs (`http`, `https`,
    `mailto`) and pure fragments (`#anchor`) are skipped.
  - References of the form `REQ-X-NNNN @ relative/path.spec.md` — the path
    must exist and the spec at that path must contain a REQ block with the
    cited ID.

### Tests

- `tools/spec_lint/tests/test_prose_xref_banned.py` — inline-text scenarios
  (no on-disk fixtures needed; the rule never dereferences paths).
- `tools/spec_lint/tests/test_xref_resolves.py` — tmp_path-based scenarios
  using a new `xref_helpers.write_doc(...)` helper to lay out a file tree
  with the relationships under test.

## PHASE-1 scope simplifications (called out for the record)

- The `prose-xref-banned` heuristic is intentionally narrow: a small
  denylist plus the inline allow marker. False positives are expected as
  the corpus grows; each one is either a real prose ref to fix or a
  pattern to refine in a follow-up CHG.
- `xref-resolves` requires the cited REQ-IDs to live at the referenced
  path; it does **not** yet validate the supersession chain or that the
  cited REQ is non-deprecated. That tightening is `xref-active` and lands
  in a future CHG once the spec corpus has supersession history to test.

## Tasks

- [`TASK-0008`](tasks/TASK-0008.md) — type `test-red`: rule stubs + helper
  + real test bodies. Tests fail at NIE.
- [`TASK-0009`](tasks/TASK-0009.md) — type `impl`: implement both rules.
  Tests pass.

## Rollout

- Single PR, intra-phase. Self-merge under hybrid policy.
- Push immediately after each commit (ADR-0005 §6 amendment 0001).
