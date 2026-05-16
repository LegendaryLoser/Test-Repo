---
id: CHG-0009
title: spec_lint reliability — real-corpus dry-run + benchmark harness
status: in-progress
date: 2026-05-16
phase: PHASE-1
references:
  story: null
  epic: null
  adrs:
    - ADR-0004
    - ADR-0006
    - ADR-0008
---

# CHG-0009 — spec_lint reliability: real-corpus dry-run

## Why

Third reliability CHG. CHG-0007 verified rules satisfy named invariants
on hypothesis-generated inputs. CHG-0008 surfaced and fixed defects via
targeted mutations. **This CHG measures rule behavior on real, externally-
authored content** — the failure mode CHG-0007/0008 cannot test (out-of-
distribution inputs we did not author).

Output: structured baseline report committed to the repo. After this lands,
we have measured signal on how the deterministic rules behave on real
content; we can then decide whether LLM augmentation is worth the substrate
cost (the original deferred question).

## Honest framing on "statistical sufficiency"

The session direction was *"statistically sufficient data for our use case."*
A precise reading:

- **Statistical sufficiency for precision/recall measurement requires labels.**
  Without ground-truth labels on each corpus item ("is this a real defect?"),
  we can compute finding *density* and *rate* but not precision or recall.
- **More unlabeled corpora do not increase statistical power.** They
  increase coverage diversity, which is what surfaces unhandled patterns —
  a separate goal.
- **For this CHG, we vendor 2 corpora and report unlabeled findings.**
  A future CHG handles labeling and computes calibrated metrics.

## Vendored corpora (this CHG)

After researching public-domain options
([sources cited in TASK-0017](tasks/TASK-0017.md)), two corpora are
vendor-eligible — explicit redistributable licenses, manageable size,
direct relevance to a subset of rules:

1. **OpenSpec docs snapshot** — `github.com/Fission-AI/OpenSpec`,
   commit `8498042fe8a738e8ad6facd94a5fc7f5025bf81d`,
   `docs/*.md` (~170 KB, MIT).
   - Tests: `prose-xref-banned`, `xref-resolves`.
   - Format: native markdown; not REQ-block-structured.

2. **PROMISE NFR / PROMISE_exp** —
   `github.com/AleksandarMitrevski/se-requirements-classification`,
   commit `1f5dc4501a1956f21011083594d925bac49f198c`,
   `0-datasets/PROMISE_exp/PROMISE_exp.arff` (~50 KB, CC BY-SA 3.0).
   - 969 labeled requirements (444 FR + 525 NFR), real software
     specifications.
   - Tests: `anti-aliasing` (pairwise similarity over real requirement
     text), and `compound-requirement-detector` (synthetic wrapping —
     transformation noted in the report).
   - Attribution preserved verbatim in vendored MANIFEST.

## Candidate corpora identified but DEFERRED

Documented for future CHGs:

- **EARS-Based Functional Requirements (9529 reqs)** — referenced in
  MDPI Systems 2025 paper; needs license verification before vendoring.
- **PURE dataset (7445 samples)** — used in research; needs license
  verification.
- **NoRBERT fine-grained PROMISE** —
  `github.com/tobhey/NoRBERT`; extension of PROMISE with finer labels;
  vendor if first-round shows we need finer requirement-class signal.
- **Cucumber/Gherkin .feature files** — would directly stress
  `compound-requirement-detector` since each Scenario should be one
  Given/When/Then. Per-repo MIT-licensed examples exist; license aggregation
  across multiple sources adds friction.
- **This repo's own `openspec/`** — closed-loop self-check; useful as a
  sanity baseline but tiny and self-authored.

Adding any of these in a future CHG is a corpus-vendoring PR plus a
loader extension; framework scaffolded in this CHG accommodates them.

## What changes

### Benchmark module — `tools/spec_lint/benchmark/`

- `__init__.py`
- `loaders.py` — per-corpus loaders:
  - `load_openspec_docs(corpus_dir) -> list[tuple[Path, str]]`
  - `load_promise_arff(arff_path) -> list[SpecFile]` (each requirement
    becomes a synthetic SpecFile with the original text in Description).
- `runner.py` — `run_dry_run(corpora, rules) -> DryRunResult`. Iterates
  every applicable rule against every corpus; collects findings;
  separates findings from uncertain-zone signals (rule-specific).
- `report.py` — `render_report(result) -> str`. Generates a markdown
  report with per-corpus + per-rule sections, finding counts, uncertain-
  zone counts, top-N examples.

### Vendored corpora

- `tools/spec_lint/benchmark/corpora/openspec_docs/` — 11 .md files
  from OpenSpec `docs/` (the entire directory, ~170 KB).
- `tools/spec_lint/benchmark/corpora/openspec_docs/MANIFEST.md` —
  source URL, commit SHA, license, fetched-on date, attribution.
- `tools/spec_lint/benchmark/corpora/promise_nfr/` — PROMISE_exp.arff
  and the original tera-PROMISE README, both verbatim.
- `tools/spec_lint/benchmark/corpora/promise_nfr/MANIFEST.md` —
  source URL, commit SHA, **CC BY-SA 3.0 attribution preserved exactly
  as in the dataset header** per license requirements, fetched-on date.

### Baseline report (committed)

- `tools/spec_lint/benchmark/reports/baseline.md` — generated by the
  GREEN commit's run; committed so future runs can diff. Carries the
  commit SHA of the rules being measured, so a finding-count change is
  attributable to either rule changes or corpus changes.

### Tests

- `tools/spec_lint/tests/test_benchmark.py` — loaders return expected
  shape; runner aggregates correctly; report renders to non-empty
  markdown. Doesn't pin specific finding counts (those drift as rules
  evolve); pins structural invariants.

## Out of scope

- Ground-truth labeling — separate CHG once we agree on labeling protocol.
- Precision/recall computation — depends on labels.
- LLM-augmented rule comparison — depends on labels + on a decision to
  pull anthropic-client forward.
- Additional corpora beyond the two vendored — explicitly deferred above.

## Tasks

- [`TASK-0017`](tasks/TASK-0017.md) — type `test-red`: vendor corpora;
  scaffold benchmark framework with NIE stubs; real test bodies.
- [`TASK-0018`](tasks/TASK-0018.md) — type `impl`: implement loaders,
  runner, report. Run dry-run; commit baseline report.

## Rollout

- Single PR. Vendoring brings a ~220 KB content addition (well-attributed).
- Self-merge under hybrid policy (no substrate change; vendoring is an
  additive corpus PR, not an architecture change).
