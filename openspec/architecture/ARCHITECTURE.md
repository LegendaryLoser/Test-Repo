# Architecture

Authoritative structural narrative for this monorepo. This document describes
*how the repository is organized*, *which artifacts are sources of truth*,
*which constraints are enforced by CI*, and *how a session resumes after a
crash*. It does **not** describe any product. Product content lives in
`openspec/vision.md`, `openspec/briefs/`, `openspec/prd/`, `openspec/epics/`,
and `openspec/stories/`.

This document and the ADRs / phase files it references constitute the
**frozen architecture artifact**. Modifications to the structure described
here require an ADR or a `Material-Architecture-Change: true` commit trailer
and a Phase-0 re-gate.

---

## 1. Operating principles

The repository exists to enforce, mechanically, the following five principles
on every change. Each principle is enforced by at least one CI gate; a missing
gate is itself a build failure (see [ADR-0008](decisions/ADR-0008-ci-gates-and-phase-exits.md)).

1. **Single source of truth (SoT).** One canonical home per fact. Cross-document
   consistency is lintable.
2. **Stochastic systems get statistical assertions.** Determinism is never
   manufactured by seeding for systems that are not deterministic in production.
3. **Tests exercise real production code.** No mocks, fakes, or simulations of
   in-repo modules. Boundary adapters are real; only network transport may be
   substituted at the edge.
4. **Red-first.** Every test exists in a failing state in git history before
   the commit that turns it green.
5. **OpenSpec for specification, BMAD + TEA for workflow.** No parallel
   convention is introduced.

## 2. Constraints from prior art

The repository design is bound by a published result on transformer associative
memory (referred to throughout as "the paper"). Its implications for spec and
artifact storage are encoded in
[ADR-0004](decisions/ADR-0004-spec-storage-discipline.md). The short version:
no agent retrieves a specification by semantic similarity; every cross-reference
is a stable ID plus a file path; near-duplicate specifications are a
lintable defect.

## 3. Top-level layout

```
/
├── README.md
├── CLAUDE.md                           # session-level guidance (added in PHASE-0)
├── .gitignore                          # tracked; enforced by `top-level-allowlist`
├── pyproject.toml                      # tracked; enforced by `top-level-allowlist`
├── .claude/
│   ├── settings.json                   # permissions, env, hooks
│   ├── agents/                         # (legacy slot — empty in v6 native-skills model)
│   ├── commands/                       # (legacy slot — empty in v6 native-skills model)
│   ├── skills/                         # BMAD-installed Claude Code Skills (vendored, see ADR-0002)
│   └── journal/                        # append-only per-session journals (gitignored runtime)
├── .github/workflows/
│   ├── ci.yml                          # PR gate: lint + unit + integration
│   ├── e2e.yml                         # nightly + on-demand
│   └── spec-discipline.yml             # enforces ADR-0004 + ADR-0005 + ADR-0008
├── _bmad/                              # BMAD v6 vendored install (see ADR-0002 amendment 0001)
│   ├── _config/                        # install manifest + skill catalog
│   ├── bmm/                            # BMad Method Module
│   ├── core/                           # BMAD core
│   ├── custom/                         # per-project skill customizations
│   ├── scripts/                        # BMAD runtime scripts
│   ├── config.toml                     # routed paths for planning/implementation/knowledge
│   └── config.user.toml
├── openspec/                           # SoT for specification, traceability, architecture
│   ├── vision.md                       # empty template until product PR
│   ├── briefs/
│   ├── prd/
│   ├── architecture/                   # THIS DOCUMENT lives here
│   │   ├── ARCHITECTURE.md
│   │   ├── decisions/                  # ADRs
│   │   └── phases/                     # phase entry/exit criteria
│   ├── epics/
│   ├── stories/
│   ├── specs/                          # current spec snapshot
│   │   ├── INDEX.yaml                  # auto-generated deterministic index
│   │   └── <domain>/<feature>.spec.md
│   ├── changes/                        # in-flight OpenSpec proposals (PR-scoped)
│   ├── _bmad-output/                   # STAGING — BMAD drafts; non-authoritative; see ADR-0002 §7
│   └── traceability/
│       └── matrix.yaml                 # derived cache; truth = journals + git + specs + tests
├── scripts/
│   └── install_bmad.sh                 # pinned BMAD install command (see ADR-0002)
├── tools/
│   ├── spec_lint/                      # ADR-0004 enforcement (Python-importable)
│   ├── trace/                          # ADR-0005 runtime (journal, rebuild, validate)
│   ├── tea/                            # TEA workflow integration
│   └── ci/                             # shared CI helpers
├── packages/
│   ├── anthropic-client/               # single LLM access point
│   ├── shared-ts/                      # shared by Apps Script projects
│   └── shared-py/                      # ML scaffolding
└── projects/
    └── <project>/                      # one Apps Script project per directory
        ├── CLAUDE.md
        ├── openspec/                   # project-scoped specs (extends root)
        ├── src/                        # TypeScript (clasp)
        ├── tests/{unit,integration,e2e,stochastic}/
        ├── .clasp.json
        └── appsscript.json
```

Layout rationale: [ADR-0001](decisions/ADR-0001-monorepo-layout.md).

## 4. Atomic units and their identifiers

Every unit of work is addressable by a stable identifier. No agent ever refers
to a unit by prose description.

| Unit             | ID format                    | Canonical home                                       |
|------------------|------------------------------|------------------------------------------------------|
| Requirement      | `REQ-<DOMAIN>-<NNNN>`        | `openspec/specs/<domain>/<feature>.spec.md`          |
| Architecture req | `REQ-ARCH-<NNNN>`            | `openspec/architecture/ARCHITECTURE.md` §10          |
| Task             | `TASK-<NNNN>`                | `openspec/changes/<CHG>/tasks/<TASK-NNNN>.md`        |
| Test             | `TEST-<DOMAIN>-<NNNN>`       | annotation/docstring in `<package>/tests/...`        |
| Change / PR      | `CHG-<NNNN>`                 | `openspec/changes/<CHG-NNNN>/`                       |
| Phase            | `PHASE-<N>`                  | `openspec/architecture/phases/PHASE-<N>-*.md`        |
| ADR              | `ADR-<NNNN>`                 | `openspec/architecture/decisions/`                   |
| Epic             | `EPIC-<NNNN>`                | `openspec/epics/EPIC-<NNNN>.md`                      |
| Story            | `STORY-<NNNN>`               | `openspec/stories/STORY-<NNNN>.md`                   |
| Commit           | git SHA                      | git                                                  |

Identifier rules (enforced by `tools/spec_lint`, defined in
[ADR-0004](decisions/ADR-0004-spec-storage-discipline.md)):

- Identifiers are immutable. Renames are forbidden; supersession is the only
  permitted change.
- IDs are allocated by monotonic next-free scan against `openspec/specs/INDEX.yaml`.
- Cross-references use the ID *and* the file path (e.g. `REQ-SPEC-0001 @
  openspec/specs/_meta/spec-storage.spec.md`). Prose references like "the
  auth spec" are a lintable defect. <!-- spec-lint: allow prose-xref-banned -->

## 5. Spec sourcing — bidirectional, reconciled at the Epic boundary

Specifications are produced by two converging flows that meet at the Epic
artifact. Neither flow alone is sufficient; both are required for an Epic to
reach `ready-for-dev`.

```
Top-down (BMAD PM + Architect):
    Vision  →  Brief  →  PRD  →  Architecture  →  Phases  →  Epic (rationale + scope)
                                                                ↑
                                                                |
                                                          reconciliation
                                                                |
                                                                ↓
Bottom-up (BMAD SM + Dev + TEA):
    Story  →  Behaviors (Given/When/Then)  →  Acceptance criteria  →  REQ-IDs  →  TEST-IDs
```

Reconciliation gate (enforced in
[ADR-0008](decisions/ADR-0008-ci-gates-and-phase-exits.md)):

- An Epic carries a `coverage:` block listing REQ-IDs that satisfy it.
- `EPIC.status = ready-for-dev` requires: PM rationale present; Architect
  approval present; ≥1 Story decomposed with REQ-IDs; every covering REQ has
  TEA-authored failing tests.
- `EPIC.status = done` requires: every covering REQ is `tests-green` and the
  Epic's exit assertions pass.

## 6. Spec storage format

Defined in full in [ADR-0004](decisions/ADR-0004-spec-storage-discipline.md).
Summary: Markdown body, YAML frontmatter per requirement block, one assertion
per REQ, append-only at the assertion level. `openspec/specs/INDEX.yaml` is the
sole retrieval surface for tooling; semantic search is forbidden for spec
lookup.

## 7. Traceability — derived cache, never hand-edited

Defined in full in [ADR-0005](decisions/ADR-0005-traceability-and-journaling.md).
Summary:

- **Truth**: append-only session journals (`.claude/journal/session-<id>.jsonl`)
  + git + spec files with REQ blocks + test annotations.
- **Cache**: `openspec/traceability/matrix.yaml`.
- `tools/trace/rebuild.py` regenerates the cache deterministically. CI fails the
  PR if the committed matrix differs from the rebuilt matrix.
- Pre-commit hook re-runs rebuild and stages the result.
- Coverage gate: 100% REQ coverage (every REQ has ≥1 test, every test maps to
  ≥1 REQ, no orphans, status transitions monotonic and P4-compliant).

## 8. Session persistence and crash recovery

Defined in full in [ADR-0005](decisions/ADR-0005-traceability-and-journaling.md).
Summary of failure modes and guarantees:

| Failure                                    | Loss                                  |
|--------------------------------------------|----------------------------------------|
| Crash mid-Edit/Write, container survives   | Zero on disk (atomic rename)           |
| Crash mid-commit                           | Zero (commit object is atomic; rebuild fills journal) |
| Container reclaim, push completed          | Zero                                   |
| Container reclaim, uncommitted changes     | Mitigated by `Stop`/`SessionEnd` checkpoint-commit hook |
| Container reclaim mid-tool-call            | At most the in-flight tool call's reasoning context |

Claude's reasoning context between tool calls is not persisted; it is
*reconstructed* on resume from the journal + active task file + last commit.
Session resume requires zero human re-briefing.

## 9. Workflow surface — BMAD + TEA via Claude Code

Defined in full in [ADR-0002](decisions/ADR-0002-bmad-integration.md). BMAD
agents live under `bmad/`; Claude Code surfaces them via thin wrappers in
`.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by
file path, never by name, so a BMAD version upgrade is one wrapper edit per
agent.

## 10. Architecture requirements (REQ-ARCH-*)

These requirements are exit criteria for `PHASE-0`. They are testable; failures
block the phase.

- **REQ-ARCH-0001** — Repository contains the top-level layout in §3 (no extra
  top-level directories without an ADR).
- **REQ-ARCH-0002** — `openspec/architecture/ARCHITECTURE.md` plus ADR-0001
  through ADR-0008 plus PHASE-0 through PHASE-5 are all present.
- **REQ-ARCH-0003** — `openspec/vision.md`, `openspec/briefs/`, `openspec/prd/`,
  `openspec/epics/`, `openspec/stories/` exist with empty templates only (no
  product content).
- **REQ-ARCH-0004** — `openspec/specs/INDEX.yaml` exists and parses; empty
  `requirements:` block is permitted at PHASE-0.
- **REQ-ARCH-0005** — Every cross-reference inside `openspec/architecture/`
  resolves to an existing file (no dead links).
- **REQ-ARCH-0006** — No file under `openspec/architecture/` contains executable
  code or test code.
- **REQ-ARCH-0007** — `CLAUDE.md` (root) is present and references the five
  principles in §1 verbatim.
- **REQ-ARCH-0008** — `.claude/settings.json` is present; hooks declared in
  ADR-0005 are listed (implementations land in PHASE-2).

Tests for REQ-ARCH-* are authored in PHASE-0 as red tests and turn green as
PHASE-0 implementation completes.

## 11. Phased delivery

Each phase has explicit entry and exit criteria expressed as REQ-IDs that must
be `tests-green`. Phase files live under `openspec/architecture/phases/`.

| Phase   | Scope                                                                 |
|---------|-----------------------------------------------------------------------|
| PHASE-0 | Foundation: this architecture artifact, CLAUDE.md, settings.json, traceability scaffolding (red tests). |
| PHASE-1 | Spec hygiene: `tools/spec_lint` green; paper-derived rules enforced.  |
| PHASE-2 | Traceability runtime: `tools/trace` hooks + rebuild + CI gate green.  |
| PHASE-3 | `packages/anthropic-client` green with stochastic-tier tests.         |
| PHASE-4 | `packages/shared-ts` and `packages/shared-py` green.                  |
| PHASE-5 | First Apps Script project under `projects/` reaches E2E-green.        |

A phase cannot start until the prior phase's exit criteria are all `tests-green`
and the phase exit ADR is signed off. The phase exit ADR is a `gate`-type task.

## 12. What is *not* in this document

- Product vision, product brief, PRD, epics, stories — these are empty templates
  until a separate product PR fills them.
- Code, tests, hook implementations, lint rules — these land in PHASE-0 through
  PHASE-5 PRs.
- Any decision not captured in an ADR — if it isn't an ADR, it isn't decided.
