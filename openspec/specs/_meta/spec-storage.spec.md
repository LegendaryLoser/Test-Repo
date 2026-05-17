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

## REQ-SPEC-0002
---
id: REQ-SPEC-0002
revision: 1
status: tests-green
introduced: CHG-0012
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0002, ADR-0008]
---

### Description
No file under `tools/`, `packages/`, or `projects/` imports from or
executes `_bmad/` paths, except files under `tools/tea/` (the
authorized integration point per ADR-0002 §6). Detection is narrow:
import statements (`import _bmad`, `from _bmad`), dynamic imports
(`__import__`, `importlib.import_module`), subprocess execution paths
(`subprocess.run(["_bmad/..."])`), TS/JS imports / requires, and any
`_bmad/` path component in shell scripts.

### Acceptance
- Given the current source tree, when `python -m tools.spec_lint
  validate openspec` is invoked from the repository root, then the
  `bmad-direct-reference` rule contributes zero findings to the
  combined output, and the command exits with status `0`.

### Non-acceptance
- Docstrings, comments, and string constants that mention `_bmad/`
  for documentation purposes are not flagged — only import-like and
  executable-path forms count.
- The rule itself (`bmad_direct_reference.py`) and its test file
  (`test_bmad_direct_reference.py`) are structurally exempt.

### Notes
- Implementation: [`tools/spec_lint/rules/bmad_direct_reference.py`](../../../tools/spec_lint/rules/bmad_direct_reference.py).
- Inline override: `<!-- spec-lint: allow bmad-direct-reference -->` on
  the same line as the would-be finding.

## REQ-SPEC-0003
---
id: REQ-SPEC-0003
revision: 1
status: tests-green
introduced: CHG-0012
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0006, ADR-0008]
---

### Description
No file under `tools/`, `packages/`, or `projects/` uses banned mock
APIs — `unittest.mock.patch`, `MagicMock`, `Mock`, `monkeypatch.setattr`,
`mocker.patch`, `jest.mock`, `vi.mock`, `sinon.stub`, `sinon.fake` —
to substitute modules within this repository. Target resolution:
string-target patches whose target starts with an external prefix
(e.g. `requests.`, `anthropic.`) are permitted per ADR-0006 §2
network-transport carve-out; everything else (in-repo prefix,
identifier target, no target) is flagged.

### Acceptance
- Given the current source tree, when `python -m tools.spec_lint
  validate openspec` is invoked from the repository root, then the
  `mock-in-repo-banned` rule contributes zero findings to the combined
  output, and the command exits with status `0`.

### Non-acceptance
- Real adapter implementations under
  `packages/shared-{ts,py}/adapters/` are not affected — they are
  production code, not mocks (ADR-0006 §3).
- The rule itself and its test file are structurally exempt.

### Notes
- Implementation: [`tools/spec_lint/rules/mock_in_repo_banned.py`](../../../tools/spec_lint/rules/mock_in_repo_banned.py).
- Inline override: `# spec-lint: allow mock-in-repo-banned` (Python)
  or `// spec-lint: allow mock-in-repo-banned` (TS/JS) on the same line.
