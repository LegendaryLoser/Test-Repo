---
id: ADR-0002
title: BMAD integration (v6, wrapper-isolated)
status: accepted
date: 2026-05-16
supersedes: null
superseded_by: null
---

# ADR-0002 — BMAD integration (v6, wrapper-isolated)

## Context

We use BMAD personas (PM, Architect, SM, Dev, PO) and the Test Architect (TEA)
expansion pack as the workflow surface. BMAD has two active lines:

- **v4 (`.bmad-core/`)** — stable, broad community documentation, TEA
  retrofitted.
- **v6 (`bmad/` modular)** — active development line, modular module boundaries
  (`bmm`, `cis`, `tea`), TEA expansion is first-class.

We must also surface BMAD agents and commands to Claude Code without coupling
project code to BMAD's internal file layout — otherwise a BMAD upgrade becomes
a cross-cutting refactor.

## Decision

1. **Adopt BMAD v6**, installed under `bmad/` at the repo root. Version is
   pinned in `bmad/config.yaml`.
2. **Wrapper isolation.** Claude Code consumes BMAD via thin wrappers in
   `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD persona
   and workflow files **by file path**, not by name. A wrapper is one
   front-matter block plus a `Load: bmad/<module>/agents/<file>.md` directive.
3. **No project code depends on BMAD directly.** All BMAD-aware tooling lives
   under `tools/tea/`.
4. **TEA workflows** are the source of truth for test-design conventions
   (acceptance decomposition, gate decisions). PHASE-1 wires `tools/tea/` to
   invoke TEA workflows from CI.
5. **Downgrade path to v4** is preserved by the wrapper layer: a downgrade
   replaces `bmad/` and edits the `Load:` lines in `.claude/agents/`; no other
   surface changes.

## Consequences

- Upgrading BMAD is a single PR: bump `bmad/config.yaml`, re-run BMAD installer,
  resolve wrapper `Load:` paths if any moved.
- New BMAD agents are exposed to Claude Code by adding a wrapper file; no other
  surface changes.
- Custom BMAD workflows live under `bmad/workflows/` (local overrides) so
  upstream changes do not silently alter our behavior.

## Compliance

- Wrapper-only access is enforced by spec-lint rule `bmad-direct-reference`
  (PHASE-1): no file under `tools/`, `packages/`, or `projects/` may reference
  a path under `bmad/` except `tools/tea/`.
- BMAD version pin is checked in CI against `bmad/config.yaml`.
