# OpenSpec docs snapshot

## Source

- Repository: https://github.com/Fission-AI/OpenSpec
- Commit SHA: `8498042fe8a738e8ad6facd94a5fc7f5025bf81d`
- Path within source: `docs/`
- Fetched: 2026-05-16
- Vendored by: CHG-0009 TASK-0017

## License

MIT License — see [`LICENSE`](LICENSE) (verbatim copy from the source repo).
Copyright (c) 2024 OpenSpec Contributors. Redistribution permitted with
copyright notice preserved.

## Contents

11 markdown files comprising the full OpenSpec v6 user-facing documentation:

- `cli.md`, `commands.md`, `concepts.md`, `customization.md`,
  `getting-started.md`, `installation.md`, `migration-guide.md`,
  `multi-language.md`, `opsx.md`, `supported-tools.md`, `workflows.md`.

Files are byte-equal to the source at the pinned commit.

## What this corpus tests

Direct dry-run target for rules that operate on arbitrary markdown:

- `prose-xref-banned` — does the rule fire (or fail to fire) on real
  documentation prose?
- `xref-resolves` — do real-world markdown link patterns resolve under
  the rule's resolution algorithm?

These rules do not require REQ-block structure. OpenSpec's docs are not
REQ-formatted; REQ-block-specific rules (`req-id-format`,
`spec-frontmatter-valid`, `compound-requirement-detector`,
`anti-aliasing`, `req-id-immutable`, `req-append-only`) are NOT exercised
against this corpus.

## Upgrade procedure

To refresh:

1. Pin a new commit SHA from `https://github.com/Fission-AI/OpenSpec`.
2. `git clone --depth 1 https://github.com/Fission-AI/OpenSpec /tmp/openspec`.
3. `git -C /tmp/openspec checkout <new-sha>`.
4. Replace files in this directory; update `Commit SHA` and `Fetched`
   above.
5. Re-run `python -m tools.spec_lint.benchmark.runner` and commit the
   updated baseline report.
