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

## REQ-SPEC-0004
---
id: REQ-SPEC-0004
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `req-id-format` rule correctly classifies REQ-ID strings as valid
(matching `REQ-<DOMAIN>-<NNNN>`) or invalid, per ADR-0004 §1.

### Acceptance
- The `req-id-format` rule's unit tests, mutation tests, and property-
  based tests all pass; the rule reports zero false negatives on the
  documented must-catch corpus.

### Notes
- Implementation: [`tools/spec_lint/rules/req_id_format.py`](../../../tools/spec_lint/rules/req_id_format.py).

## REQ-SPEC-0005
---
id: REQ-SPEC-0005
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `spec-frontmatter-valid` rule enforces ADR-0004 §5: every REQ block
carries required keys (id, revision, status, introduced, supersedes,
phase, tier, references) with valid values.

### Acceptance
- The `spec-frontmatter-valid` rule's unit tests, mutation tests, and
  property-based tests all pass.

### Notes
- Implementation: [`tools/spec_lint/rules/spec_frontmatter_valid.py`](../../../tools/spec_lint/rules/spec_frontmatter_valid.py).

## REQ-SPEC-0006
---
id: REQ-SPEC-0006
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `compound-requirement-detector` rule enforces ADR-0004 §3: each REQ
block contains exactly one assertion; compound bullets are a defect.

### Acceptance
- The `compound-requirement-detector` rule's unit tests, mutation tests,
  and property-based tests all pass.

### Notes
- Implementation: [`tools/spec_lint/rules/compound_requirement_detector.py`](../../../tools/spec_lint/rules/compound_requirement_detector.py).

## REQ-SPEC-0007
---
id: REQ-SPEC-0007
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `prose-xref-banned` rule enforces ADR-0004 §2: prose references to
artifacts are forbidden; every reference uses ID + path. Pattern
categories such as the following fire the rule:

```text
the X spec
the X requirement
the X ADR
```

### Acceptance
- The `prose-xref-banned` rule's unit tests and mutation tests pass.

### Notes
- Implementation: [`tools/spec_lint/rules/prose_xref_banned.py`](../../../tools/spec_lint/rules/prose_xref_banned.py).
- Inline override: `<!-- spec-lint: allow prose-xref-banned -->`.
- Fenced code blocks (triple backtick) are exempt.

## REQ-SPEC-0008
---
id: REQ-SPEC-0008
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `xref-resolves` rule enforces ADR-0004 §2: every markdown link and
every `REQ-X-NNNN @ path` reference resolves to an existing target.

### Acceptance
- The `xref-resolves` rule's unit tests, mutation tests, and property-
  based tests all pass.

### Notes
- Implementation: [`tools/spec_lint/rules/xref_resolves.py`](../../../tools/spec_lint/rules/xref_resolves.py).
- Known limitations (documented; queued for CHG-0016): does not respect
  inline backticks; line-by-line scan misses multi-line REQ@path
  references wrapped across lines.

## REQ-SPEC-0009
---
id: REQ-SPEC-0009
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `anti-aliasing` rule enforces ADR-0004 §4: REQs across the spec
corpus must not be near-duplicates by Jaccard similarity on body
n-grams.

### Acceptance
- The `anti-aliasing` rule's unit tests, mutation tests, and property-
  based tests all pass.

### Notes
- Implementation: [`tools/spec_lint/rules/anti_aliasing.py`](../../../tools/spec_lint/rules/anti_aliasing.py).

## REQ-SPEC-0010
---
id: REQ-SPEC-0010
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `req-id-immutable` rule enforces ADR-0004 §1: REQ IDs once
allocated never change. The rule reads git history per spec file and
flags renames as removals.

### Acceptance
- The `req-id-immutable` rule's unit tests pass.

### Notes
- Implementation: [`tools/spec_lint/rules/req_id_immutable.py`](../../../tools/spec_lint/rules/req_id_immutable.py).
- Runs at commit-time / pre-receive; excluded from the `validate`
  snapshot runner per REQ-SPEC-0001 non-acceptance.

## REQ-SPEC-0011
---
id: REQ-SPEC-0011
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The `req-append-only` rule enforces ADR-0004 §7: REQ blocks may only be
appended or deprecated in place — never removed or renamed silently. The
rule reads git history per spec file.

### Acceptance
- The `req-append-only` rule's unit tests pass.

### Notes
- Implementation: [`tools/spec_lint/rules/req_append_only.py`](../../../tools/spec_lint/rules/req_append_only.py).
- Runs at commit-time / pre-receive; excluded from the `validate`
  snapshot runner per REQ-SPEC-0001 non-acceptance.

## REQ-SPEC-0012
---
id: REQ-SPEC-0012
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
The spec_lint infrastructure modules — parser, git history loader, and
benchmark / dry-run harness — are correct and stable. Each correctly
parses, loads, or measures what its consumers expect.

### Acceptance
- Unit tests in `test_parser.py`, `test_git_history.py`,
  `test_benchmark.py`, and parser property tests all pass.

### Notes
- Implementations under [`tools/spec_lint/`](../../../tools/spec_lint/).
- Bundles parser + history + benchmark for one REQ; if independent
  accountability is later required, split via supersession per ADR-0004 §1.

## REQ-SPEC-0013
---
id: REQ-SPEC-0013
revision: 1
status: tests-green
introduced: CHG-0030
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0005, ADR-0008]
---

### Description
Every Python test function under `tools/` carries both an
`@test-id TEST-<DOMAIN>-<NNNN>` annotation and a
`@covers REQ-<X>-<NNNN>` annotation in REQ-form (not legacy
`@covers (rule: <name>)` form). Enforced by the
`test_annotation_discipline` meta-test.

### Acceptance
- `pytest tools/ci/tests/test_annotation_discipline.py` exits with
  status `0` and reports zero annotation violations.

### Non-acceptance
- REQ-existence cross-check (whether the referenced REQ-ID is actually
  defined in a spec file) is `gate-coverage`'s job (PHASE-2), not this
  rule's.

### Notes
- Implementation: [`tools/ci/tests/test_annotation_discipline.py`](../../../tools/ci/tests/test_annotation_discipline.py).

## REQ-SPEC-0014
---
id: REQ-SPEC-0014
revision: 1
status: tests-green
introduced: CHG-0013
supersedes: null
phase: PHASE-1
tier: integration
references:
  epic: null
  story: null
  adrs: [ADR-0008]
---

### Description
The `spec-lint` job in `.github/workflows/ci.yml` runs the spec_lint
CLI gates and the full pytest suite on every pull request and every
push to master/main. The job exits non-zero if any gate reports
findings or any test fails. Steps include: checkout (with full
history), Python 3.11 setup, dev-dependency install, `validate`,
`check-layout`, and `pytest tools/`.

### Acceptance
- Given the current `.github/workflows/ci.yml`, when
  `pytest tools/ci/tests/test_workflow_wiring.py` is invoked, then it
  exits with status `0` (the spec-lint job contains the required
  structural steps with no PHASE-0 placeholder remaining).

### Non-acceptance
- `trace-gates`, `unit-integration`, and `phase-exit` jobs remain
  PHASE-0 placeholders pending PHASE-2 / PHASE-3+ work; they are not
  in scope for this REQ.
- The e2e workflow (`e2e.yml`) is not in scope.
- The consequence — "a violating PR is blocked from merge" — is the
  outcome the contract enables but is only observable via live CI
  runs; out of scope as a unit-testable assertion.

### Notes
- Implementation: [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml).
- Meta-test: [`tools/ci/tests/test_workflow_wiring.py`](../../../tools/ci/tests/test_workflow_wiring.py).
- Tier `integration` because the test exercises a YAML configuration
  file in conjunction with the CLI commands it invokes; the actual
  end-to-end behavior is observable only via a live CI run.

## REQ-SPEC-0015
---
id: REQ-SPEC-0015
revision: 1
status: tests-green
introduced: CHG-0014
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0004, ADR-0008]
---

### Description
`openspec/specs/INDEX.yaml` is the deterministic, auto-generated index
of every REQ defined in `openspec/specs/*.spec.md`. Per ADR-0004 §6 it
is the sole retrieval surface for tooling. The `python -m tools.spec_lint
index` subcommand regenerates it; `--check` verifies it matches the
current spec corpus (ignoring the `generated_at` timestamp).

### Acceptance
- Given the current source tree, when `python -m tools.spec_lint
  index --check` is invoked from the repository root, then it exits
  with status `0`.

### Non-acceptance
- REQ-ARCH-0001..0008 live in `ARCHITECTURE.md` §10 as bullet points,
  not `*.spec.md` blocks; they are not indexed until CHG-0015 migrates
  them.
- The `--check` comparison ignores `generated_at` — a hand-edited
  timestamp is invisible to this gate. Hand-editing INDEX.yaml after
  PHASE-1 is forbidden separately by CLAUDE.md's "Forbidden" list.

### Notes
- Implementation: [`tools/spec_lint/index.py`](../../../tools/spec_lint/index.py).
- CLI: `python -m tools.spec_lint index` regenerates;
  `python -m tools.spec_lint index --check` verifies.
- The CI `index-up-to-date` gate per ADR-0008 §1 is a separate CHG
  (queued); when wired, CI will fail on stale INDEX in any PR.

## REQ-SPEC-0016
---
id: REQ-SPEC-0016
revision: 1
status: tests-green
introduced: CHG-0031
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0005, ADR-0008]
---

### Description
`openspec/STATUS.md` is the authoritative human-readable session-resume
document, hand-maintained until PHASE-2's `SessionStart` resume hook +
`tools/trace/rebuild.py` mechanize it. It contains the sections a
cold session needs to resume work without re-reading chat history:
CHG status, audit findings ledger, open architectural questions,
sequenced roadmap, and an explicit "next session: start here" pointer.

### Acceptance
- Given the current source tree, when
  `pytest tools/ci/tests/test_status_resume.py` is invoked, then it
  exits with status `0` (STATUS.md exists with all required `##`
  section headers).

### Non-acceptance
- Content freshness (whether listed CHGs / findings / roadmap items
  match reality) is a discipline check, not mechanical — the meta-
  test asserts structure, not currency. PHASE-2's mechanized
  generation will enforce currency.
- `openspec/traceability/matrix.yaml` is the future authoritative
  cache (PHASE-2 deliverable); STATUS.md is the human-readable
  bridge until then.

### Notes
- Implementation: [`openspec/STATUS.md`](../../STATUS.md).
- Meta-test: [`tools/ci/tests/test_status_resume.py`](../../../tools/ci/tests/test_status_resume.py).
- CLAUDE.md "How to start any session" §1 instructs new sessions to
  read STATUS.md before any other artifact.
