# Architecture Audit — 2026-05-17

**Target:** the 15-document architecture artifact under
`openspec/architecture/` (ARCHITECTURE.md + 8 ADRs + 6 PHASE files).

**Status:** STAGING (per
[`ADR-0002`](../../../../architecture/decisions/ADR-0002-bmad-integration.md) §7
and [`STAGING.md`](../../../STAGING.md)). Non-authoritative. Not referenced
by the matrix, INDEX, or any spec.

## What this directory contains

| File / subdir | Purpose |
|---|---|
| `README.md` | This file. Session metadata + method. |
| `consolidated.md` | Main deliverable: thematic clustering of all findings, convergence analysis, proposed CHG sequence. Now spans all 4 waves (~70 themes; previously only Wave 1). |
| `findings-index.md` | Flat one-line-per-finding index across all 36 streams (provenance ledger). |
| `qd-triage.md` | Quality-Diversity triage of all 36 streams: per-method σ × κ scoring; Tier A/B/C/D catalog; QD matrix occupancy; empty-cell Wave-5 targets; ACGR convergence metric; draft clauses for the methodology codification ADR. Wave-5 §3.5 (per-stream σ × κ for the 4 new streams) pending; see corrections.md for known defects awaiting the §3.5 re-issue. |
| `corrections.md` | Wave-5 META- audit corrections: 19 corrections (4 CRIT / 12 SER / 3 PROC) against consolidated.md, qd-triage.md, and findings-index.md. Read alongside those documents; this log is authoritative for the corrected attributions and counts pending the next consolidation pass. |
| `signal-ledger.md` | Per-finding signal-filter triage of all 867 sub-agent findings: classification (SIGNAL/DUPLICATE_OF/CONTRADICTS/METHOD_ARTIFACT/NOT_ACTIONABLE/NOT_CONCRETE/OUT_OF_SCOPE), 42 duplicate-claim clusters, 1 hard contradiction, per-stream true-σ (after cross-batch dedup), 5 macro-area resolution groupings. Headline: ~120-150 unique architecture defects underlie the 867 findings — the corpus has substantial redundancy. |
| `methodology-research-note.md` | Three structural critiques of the QD framework (coverage tautology, ordering bias / path-dependence, audit-type criticality variance) with research-literature grounding (Pugh 2016, Cully 2018, Pierrot 2022, Mouret & Clune 2015, Stock 2025, etc.); proposes saturation-based reformulation (replace coverage; keep QD-score; dual stopping) + two-layer framework (domain-general + audit-specific). Input to methodology codification ADR + revised TASK-0051 scope. |
| `raw-transcripts/` | 35 sub-agent task transcripts as `.jsonl` files, named by stream prefix (e.g. `EDGE-agent-abf3f95219d0706c3.jsonl`). Full conversation logs including tool calls, intermediate reasoning, and final deliverables. ~5.7 MB total. See [`raw-transcripts/MANIFEST.md`](raw-transcripts/MANIFEST.md) for the stream → file mapping. The 36th stream (`ARCH-`) was the in-context pass and has no separate transcript. |
| `findings/` | 35 per-stream extracted findings markdown files (e.g. `EDGE-findings.md`). Each file contains the sub-agent's initial prompt and its final assistant message (the audit deliverable for that stream). Derived from `raw-transcripts/` by [`raw-transcripts/persist-corpus.py`](raw-transcripts/persist-corpus.py). ~776 KB total. |

## Why this audit exists

Triggered by the prior session's roadmap (STATUS.md "Next session: start here"
and STATUS.md NEW-3, audit-findings ledger). The architecture artifact was
declared "frozen" but had absorbed 19 prior audit findings without all of
them being closed (12 still open). The user requested a thorough,
maximally-rigorous, multi-perspective re-review before resuming any queued
implementation roadmap (CHG-0014b, CHG-0015, etc.).

## Method

12 review streams against the same 15-document corpus. Maximum variance
applied across four axes:

1. **Model diversity** — opus, sonnet, haiku (proxy for temperature variation,
   which the Claude Code Agent tool does not expose directly).
2. **Methodology diversity** — adversarial-general, edge-case-hunter,
   implementation-readiness, editorial-structure, editorial-prose,
   pre-mortem, party-mode roundtable, inheritor framing.
3. **Context diversity** — one in-context pass (full conversation +
   STATUS.md awareness); 11 isolated sub-agent passes (no prior context).
4. **Persona diversity** — within the party-mode pass, 6 BMAD personas
   reviewed from their professional angle.

## Streams

| ID prefix | Method | Model | Context | Findings |
|---|---|---|---|---|
| `ARCH-` | adversarial-general | opus | in-context | 31 |
| `IND-` | adversarial-general | opus | isolated | 27 |
| `ADVO-` | adversarial-general | opus | isolated | 24 |
| `ADVS-` | adversarial-general | sonnet | isolated | 19 |
| `ADVH-` | adversarial-general | haiku | isolated | 15 |
| `INHER-` | inheritor framing (custom) | opus | isolated | 22 |
| `EDGE-` | edge-case-hunter | opus | isolated | 44 |
| `READY-` | check-implementation-readiness | opus | isolated | 19 |
| `STRUCT-` | editorial-review-structure | opus | isolated | 15 |
| `PROSE-` | editorial-review-prose | sonnet | isolated | 14 |
| `PREM-` | advanced-elicitation (pre-mortem) | opus | isolated | 18 |
| `PARTY-` | party-mode (6 personas) | opus | isolated | 22 |
| **Total raw** | | | | **270** |

Plus 19 pre-existing findings in
`openspec/STATUS.md` (audit-findings ledger, prefixes `C`/`S`/`P`/`NEW`).

## Caveats

- ~~Raw stream outputs are not persisted as separate files~~ **(Corrected
  2026-05-17.)** The original README claimed raw outputs lived only in
  ephemeral container `/tmp/` storage. That was a recoverability defect:
  on container reclaim the corpus would have been lost. The 35 sub-agent
  transcripts were rescued post-hoc from the container-local
  `/root/.claude/projects/-home-user-Test-Repo/<session>/subagents/`
  cache and persisted into [`raw-transcripts/`](raw-transcripts/) with
  per-stream findings extracted into [`findings/`](findings/). See
  [`raw-transcripts/MANIFEST.md`](raw-transcripts/MANIFEST.md). The
  `ARCH-` stream (in-context pass) is the one exception — no separate
  transcript exists; its findings live in the main-session transcript
  which is not persisted.
- The audit was performed against the in-tree architecture as of the
  most recent commit on `claude/bmad-architecture-review-sV42w`. STATUS.md
  open question #5 about BMAD review integration into the CHG workflow
  is the open governance question that determines whether this audit
  itself should have followed a formal CHG-envelope shape.
- "Consolidated" means thematically deduplicated. The thematic
  clustering is the consolidator's judgment (this session) and is itself
  reviewable — the per-finding index preserves the raw provenance and
  the per-stream findings markdown preserves the raw text, so a later
  reviewer can fully re-cluster from source.
- **Lesson for future audits:** persist the corpus inline (per-stream
  findings markdown written into the audit directory as each sub-agent
  returns) rather than relying on post-hoc rescue from a container-
  local cache. The cache happened to survive long enough this time;
  next time it may not.
