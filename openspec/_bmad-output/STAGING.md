# `openspec/_bmad-output/` — STAGING (non-authoritative)

This directory holds **drafts** produced by BMAD skills. It is **NOT** the
source of truth for any artifact type. Per
[`ADR-0002`](../architecture/decisions/ADR-0002-bmad-integration.md) §7,
**no traceability artifact — matrix, INDEX, REQ cross-references — ever
references a path under `_bmad-output/`.**

## Routing

Configured per [`ADR-0002`](../architecture/decisions/ADR-0002-bmad-integration.md) §5:

- `openspec/_bmad-output/planning/` — briefs, PRDs, epics, architectures
  emitted by BMAD planning workflows.
- `openspec/_bmad-output/implementation/` — sprint status, stories,
  reviews, retrospectives.
- `openspec/_bmad-output/knowledge/` — research and reference docs.

## Promotion protocol (draft → canonical)

A BMAD draft becomes authoritative only after a **promotion task**
(type `docs`) moves it to its canonical home with proper frontmatter and
an allocated stable ID:

| Draft type | Canonical home | ID format |
|---|---|---|
| Brief | `openspec/briefs/<BRIEF-NNNN>.md` | `BRIEF-NNNN` |
| PRD | `openspec/prd/<PRD-NNNN>.md` | `PRD-NNNN` |
| Epic | `openspec/epics/<EPIC-NNNN>.md` | `EPIC-NNNN` |
| Story | `openspec/stories/<STORY-NNNN>.md` | `STORY-NNNN` |
| Architecture | `openspec/architecture/decisions/<ADR-NNNN>-*.md` | `ADR-NNNN` |
| Specs | `openspec/specs/<domain>/<feature>.spec.md` (REQ blocks) | `REQ-<DOMAIN>-NNNN` |

Promotion task workflow:

1. Open a CHG with one `docs`-type task per artifact being promoted.
2. The task reads the staging draft, adds frontmatter (id, status,
   introduced, references…), assigns the stable ID via
   `tools/spec_lint allocate <domain>` (PHASE-1+).
3. Move (don't copy — single source) the content to its canonical home.
4. Delete the staging file, or move it to
   `openspec/_bmad-output/<type>/_archived/<timestamp>-<name>.md` if
   you want to keep the raw BMAD output for traceability of the
   generation step.

## Per-project isolation (PHASE-5+)

Repo-level `_bmad/config.toml` sets the **default** routing. Per-project
overrides land in `projects/<name>/_bmad/custom/config.toml` using
BMAD's standard 4-layer config merge (see
[`ADR-0002`](../architecture/decisions/ADR-0002-bmad-integration.md) §9).
When Claude Code runs with CWD = `projects/<name>/`, the resolver picks
up the per-project override and routes outputs under
`projects/<name>/openspec/_bmad-output/`.

## What lint rules see

Per [`ADR-0002`](../architecture/decisions/ADR-0002-bmad-integration.md) §7:

- **`top-level-allowlist`** — allows `openspec/_bmad-output/` (it's
  inside `openspec/` so not a top-level concern).
- **All other spec_lint rules** — **exclude** paths under
  `openspec/_bmad-output/` by default. Drafts here are not bound by REQ
  format, frontmatter, atomicity, anti-aliasing, or cross-reference
  rules. Bind those rules at promotion time, not before.
- **`matrix-drift`** (PHASE-2) — the matrix builder MUST NOT index any
  path under `openspec/_bmad-output/`. The matrix only knows about
  canonical homes.
- **`stale-staging`** (future, deferred CHG) — flags drafts that have
  sat unpromoted past a configurable threshold (default: 14 days).
  Forces triage; prevents accumulation.

## Why this exists

BMAD generates good drafts. Drafts are not authoritative artifacts.
Without an explicit staging boundary, BMAD outputs would silently
duplicate the SoT for briefs/PRDs/epics/etc. — violating P1. The
boundary makes the duplication impossible: lint rules and the matrix
ignore staging; only promotion brings content into the addressable
artifact network.
