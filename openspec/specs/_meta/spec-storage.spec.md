# Spec storage discipline (meta)

Meta-specs for `tools/spec_lint`. Each REQ here is enforced by exactly
one runnable lint rule.

## REQ-SPEC-0001
---
id: REQ-SPEC-0001
revision: 1
status: tests-green
introduced: CHG-0011
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
Every spec file under `openspec/` parses cleanly and conforms to the
format enforced by `tools/spec_lint`'s per-file, cross-file, and corpus
rules: REQ ID format, frontmatter validity, atomicity (no compound
requirements), anti-aliasing, cross-reference resolution, no prose
cross-references.

### Acceptance
- Given the current `openspec/` tree, when `python -m tools.spec_lint
  validate openspec` is invoked from the repository root, then the
  command exits with status `0` and prints no findings to stderr.

### Non-acceptance
- Historical rules (`req-id-immutable`, `req-append-only`) — those
  require git history per file and run at commit time, not in this
  snapshot validator.
- Staged BMAD drafts under `openspec/_bmad-output/` per
  [ADR-0002](../../architecture/decisions/ADR-0002-bmad-integration.md) §7.
- Template scaffolds under `openspec/changes/_TEMPLATE/`.

### Notes
- The CLI lives in [`tools/spec_lint/__main__.py`](../../../tools/spec_lint/__main__.py).
- Exclusions are codified in `_EXCLUDED_REL_PREFIXES` in that module.
