# spec_lint dry-run baseline

- Rules HEAD: `1b1300709acc`
- Runtime: 3.94s
- Corpora processed: 2

_Diagnostic output only — counts will drift as rules and corpora evolve. Pinned in tests are structural invariants, not specific counts. Future CHGs may add labels for precision/recall._

## `openspec_docs`

- Items loaded: **11**

- Total findings across rules: **15**

### `prose-xref-banned`

Findings: **14**

- `tools/spec_lint/benchmark/corpora/openspec_docs/commands.md:565` — Prose reference pattern 'the X change' detected: 'the completed change'. Use ID + path per ADR-0004 §2 or add `<!-- spec-lint: allow prose-xref-banned -->`.
- `tools/spec_lint/benchmark/corpora/openspec_docs/concepts.md:50` — Prose reference pattern 'the X spec(s)' detected: 'the main specs'. Use ID + path per ADR-0004 §2 or add `<!-- spec-lint: allow prose-xref-banned -->`.
- `tools/spec_lint/benchmark/corpora/openspec_docs/concepts.md:404` — Prose reference pattern 'the X spec(s)' detected: 'the current specs'. Use ID + path per ADR-0004 §2 or add `<!-- spec-lint: allow prose-xref-banned -->`.
- `tools/spec_lint/benchmark/corpora/openspec_docs/concepts.md:485` — Prose reference pattern 'the X spec(s)' detected: 'the entire spec'. Use ID + path per ADR-0004 §2 or add `<!-- spec-lint: allow prose-xref-banned -->`.
- `tools/spec_lint/benchmark/corpora/openspec_docs/concepts.md:538` — Prose reference pattern 'the X spec(s)' detected: 'the same spec'. Use ID + path per ADR-0004 §2 or add `<!-- spec-lint: allow prose-xref-banned -->`.
- _… and 9 more_

### `xref-resolves`

Findings: **1**

- `tools/spec_lint/benchmark/corpora/openspec_docs/getting-started.md:3` — Broken markdown link: '../README.md#quick-start' (resolved to /home/user/Test-Repo/tools/spec_lint/benchmark/corpora/README.md)

---

## `promise_nfr`

- Items loaded: **969**

- Total findings across rules: **34**

### `anti-aliasing`

Findings: **34**

- `tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0036:3` — REQ REQ-PRMS-0036 body has Jaccard similarity 0.71 with REQ REQ-PRMS-0075 @ tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0075:3 (threshold 0.70). ADR-0004 §4: near-duplicates...
- `tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0103:3` — REQ REQ-PRMS-0103 body has Jaccard similarity 0.71 with REQ REQ-PRMS-0104 @ tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0104:3 (threshold 0.70). ADR-0004 §4: near-duplicates...
- `tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0108:3` — REQ REQ-PRMS-0108 body has Jaccard similarity 0.75 with REQ REQ-PRMS-0109 @ tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0109:3 (threshold 0.70). ADR-0004 §4: near-duplicates...
- `tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0113:3` — REQ REQ-PRMS-0113 body has Jaccard similarity 0.73 with REQ REQ-PRMS-0114 @ tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0114:3 (threshold 0.70). ADR-0004 §4: near-duplicates...
- `tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0182:3` — REQ REQ-PRMS-0182 body has Jaccard similarity 0.85 with REQ REQ-PRMS-0183 @ tools/spec_lint/benchmark/corpora/promise_nfr/PROMISE_exp.arff::req-0183:3 (threshold 0.70). ADR-0004 §4: near-duplicates...
- _… and 29 more_

### `compound-requirement-detector`

Findings: **0**


---

