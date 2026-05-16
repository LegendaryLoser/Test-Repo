---
id: CHG-0006
title: spec_lint — compound-requirement-detector + anti-aliasing
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

# CHG-0006 — spec_lint: compound-requirement-detector + anti-aliasing

## Why

Fourth slice of PHASE-1 spec_lint. Both rules enforce ADR-0004 §3 and §4,
the atomicity and anti-aliasing requirements that follow directly from the
paper's results on transformer associative memory.

- **`compound-requirement-detector`** ([`ADR-0004` §3](../../architecture/decisions/ADR-0004-spec-storage-discipline.md)) —
  one REQ contains one assertion. A REQ whose Acceptance section has more
  than one Given/When/Then bullet is compound by definition and must be
  split.
- **`anti-aliasing`** ([`ADR-0004` §4](../../architecture/decisions/ADR-0004-spec-storage-discipline.md)) —
  pairwise n-gram similarity across all REQ Description+Acceptance bodies
  in the corpus; pairs above a configurable threshold are flagged. These
  are the paper's δ-convex lures — the failure mode where two distinct
  specifications occupy near-identical positions in any retrieval space
  and become indistinguishable to a semantic-recall consumer.

## What changes

### New abstractions

- `tools/spec_lint/rules/base.py` — adds `CorpusRule` protocol with
  `check_corpus(spec_files: list[SpecFile]) -> list[Finding]`. Fourth
  sibling alongside `Rule`, `HistoricalRule`, `CrossFileRule`. Anti-aliasing
  is the first CorpusRule; future global rules (e.g. orphan-REQ detection)
  use the same protocol.
- `tools/spec_lint/_sections.py` — shared `extract_section(body, header)`
  helper. CHG-0004 had a local copy in `req_append_only.py`; this CHG
  introduces the shared module without touching the existing copy (small
  refactor to consolidate lands later if it pays for itself).

### Config file

- `tools/spec_lint/config.yaml` — declared by ADR-0004 §4 as the home of
  the n-gram size and similarity threshold. Quarterly review is a
  `gate`-type task per the ADR. Default at PHASE-1: character 4-grams,
  Jaccard threshold 0.7. Tunable as the corpus grows.

### Rules

- `rules/compound_requirement_detector.py` — counts Given/When/Then bullets
  in each REQ's Acceptance section. > 1 → finding citing the count.
- `rules/anti_aliasing.py` — for every unordered pair of REQs across the
  corpus, computes Jaccard similarity over character n-grams of
  Description+Acceptance. Above threshold → finding citing the partner
  REQ and the similarity score.

### Tests

- `tests/test_compound_requirement_detector.py` — single-G/W/T (clean),
  two-G/W/T (finding), zero-G/W/T (clean), draft REQ with no Acceptance
  section (clean — the frontmatter rule catches structural defects).
- `tests/test_anti_aliasing.py` — identical bodies (finding), near-duplicate
  bodies (finding), distinct bodies (clean), single REQ (clean, no pair),
  threshold respected (custom config), char-vs-word n-gram modes.

## PHASE-1 scope simplifications (documented for the record)

- Compound detection uses the **primary** signal (multi-G/W/T) only.
  Prose-conjunction detection (`A and B`, `plus`) is a secondary signal
  with high false-positive risk; deferred to a follow-up CHG if needed.
- Anti-aliasing uses Jaccard over character n-grams as a fast, dependency-
  free baseline. Once we have a real spec corpus we can revisit (TF-IDF,
  MinHash, embedding distance) without changing the rule's external
  contract.
- The "quarterly review" gate-type task for the threshold is documented in
  the proposal but not scheduled here; it lands when calendar tooling is
  available (PHASE-3+).

## Tasks

- [`TASK-0010`](tasks/TASK-0010.md) — type `test-red`: stubs, config file,
  protocol addition, helper module, real test bodies. Tests fail at NIE.
- [`TASK-0011`](tasks/TASK-0011.md) — type `impl`: implement both rules.
  Tests pass.

## Rollout

- Single PR, intra-phase. Self-merge under hybrid policy.
- Push immediately after each commit (ADR-0005 §6 amendment 0001).
