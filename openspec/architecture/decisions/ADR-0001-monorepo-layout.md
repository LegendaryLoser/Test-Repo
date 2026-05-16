---
id: ADR-0001
title: Monorepo layout
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0001 — Monorepo layout

## Context

Multiple Google Apps Script projects must be developed and maintained side by
side. They share Python ML scaffolding, an Anthropic API client, CI tooling,
spec-hygiene tooling, and traceability runtime. They share governance: the same
five operating principles ([ARCHITECTURE.md](../ARCHITECTURE.md) §1) apply to
every project.

Alternatives considered:

1. **Polyrepo, one repo per project.** Rejected: shared packages would be
   versioned externally, traceability would fragment across repos, and
   cross-project spec hygiene (paper-derived anti-aliasing in
   [ADR-0004](ADR-0004-spec-storage-discipline.md)) would lose its global view.
2. **Monorepo with all code under a single `src/` tree.** Rejected: Apps Script
   projects must be `clasp`-deployable independently; per-project `appsscript.json`
   and `.clasp.json` need their own directories.
3. **Monorepo with per-project directories under `projects/` and shared code
   under `packages/`.** Selected.

## Decision

Adopt the layout in [ARCHITECTURE.md](../ARCHITECTURE.md) §3.

Rules:

- `projects/<project>/` is the deployable unit. Each project has its own
  `appsscript.json`, `.clasp.json`, `CLAUDE.md`, and project-scoped
  `openspec/` overlay.
- `packages/<package>/` is consumed by `projects/` and other `packages/`.
  Packages are versioned by git only; no published registry.
- `tools/<tool>/` is internal tooling (lint, trace runtime, CI helpers, TEA
  integration). Not consumed by `projects/` at runtime.
- `bmad/` is the BMAD installation, treated as upstream-managed; see
  [ADR-0002](ADR-0002-bmad-integration.md).
- `openspec/` is the SoT for all specification, traceability, architecture,
  and product content.
- No additional top-level directories may be introduced without an ADR.

## Consequences

- Every change can be traced to a project, a package, or a tool — flat,
  unambiguous attribution for the traceability matrix
  ([ADR-0005](ADR-0005-traceability-and-journaling.md)).
- Per-project specs extend root specs by reference; no duplication.
- A project can be removed by deleting its `projects/<project>/` directory and
  marking its REQs deprecated; no other surface changes.

## Compliance

- `REQ-ARCH-0001` enforces top-level layout.
- Spec-lint rule `top-level-allowlist` (PHASE-1) enforces the
  "no extra top-level directories without an ADR" constraint.
