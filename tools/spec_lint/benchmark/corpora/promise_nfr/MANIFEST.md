# PROMISE NFR / PROMISE_exp snapshot

## Source

- Mirror repository: https://github.com/AleksandarMitrevski/se-requirements-classification
- Commit SHA: `1f5dc4501a1956f21011083594d925bac49f198c`
- Path within source: `0-datasets/PROMISE_exp/PROMISE_exp.arff`
  and `0-datasets/tera-PROMISE NFR/README.txt`
- Fetched: 2026-05-16
- Vendored by: CHG-0009 TASK-0017

## Upstream attribution (preserved per CC BY-SA 3.0)

The following is reproduced verbatim from the ARFF dataset header:

> This is a PROMISE Software Engineering Repository data set made publicly
> available in order to encourage repeatable, verifiable, refutable, and/or
> improvable predictive models of software engineering.
>
> If you publish material based on PROMISE data sets then, please
> follow the acknowledgment guidelines posted on the PROMISE repository
> web page http://promisedata.org/repository .
>
> (c) 2007  Jane Cleland-Huang  jhuang@cti.depaul.edu
> This data set is distributed under the
> Creative Commons Attribution-Share Alike 3.0 License
> http://creativecommons.org/licenses/by-sa/3.0/

Citation: Cleland-Huang, J. (2007). PROMISE NFR dataset. DePaul University.

The expanded variant (PROMISE_exp; 969 requirements) was produced by
Lima et al. (2019) extending the original PROMISE NFR set.

## License

**Creative Commons Attribution-ShareAlike 3.0** — see the upstream URL
in the attribution block above. ShareAlike applies to derivative works
*of the dataset itself*; analysis output (our benchmark reports) is a
separate work of analysis, not a derivative of the data, and is governed
by the repository's licensing decisions for code/reports separately.

## Contents

- `PROMISE_exp.arff` — ARFF-format dataset, 969 requirements total
  (444 Functional + 525 Non-Functional). Verbatim from the mirror.
- `tera-PROMISE-README.txt` — original README from the tera-PROMISE
  hosting of the dataset. Verbatim.

## What this corpus tests

Real software-requirement text from 15 academic projects:

- `anti-aliasing` — pairwise Jaccard similarity over 969 requirement
  bodies. Surfaces real near-duplicates that exist in research-curated
  requirements, calibrating the threshold against natural text variance.
- `compound-requirement-detector` — each requirement is wrapped as a
  synthetic REQ block with the original text in Description and Acceptance;
  the wrapping is a transformation (loader-level), not in the source data.

REQ-format-specific rules (`req-id-format`, `spec-frontmatter-valid`,
`req-id-immutable`, `req-append-only`) are NOT exercised — PROMISE has no
REQ-IDs or git history; wrapping cannot fabricate them faithfully.

`prose-xref-banned` and `xref-resolves` are not exercised either —
requirements are short atomic sentences without cross-references.

## Upgrade procedure

PROMISE / PROMISE_exp is a stable academic dataset (2007 / 2019); refresh
is rare. To update the mirror reference:

1. Verify the new mirror's commit and that the dataset is still
   CC BY-SA 3.0.
2. Replace `PROMISE_exp.arff`; update `Commit SHA` and `Fetched` above.
3. Re-run benchmark; commit updated baseline.
