# Audit methodology (meta)

Meta-spec for multi-stream architecture audit corpora. This file is the
canonical home of `REQ-AUDIT-*` requirements. Per the user's standing
direction (STATUS.md Recent decisions, 2026-05-17), the methodology
codification ADR is queued for authoring after *both* the architecture
and implementation audits converge. Until then, only the operational
requirements that the audit work itself proved necessary are captured
here. Additional REQs (σ × κ admission rule, ACGR convergence metric,
Tier A/B/C/D catalog discipline, etc.) will land with the codification
ADR.

## REQ-AUDIT-0001
---
id: REQ-AUDIT-0001
revision: 1
status: draft
introduced: CHG-0032
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: null
  story: null
  adrs: [ADR-0002, ADR-0005]
---

### Description
Multi-stream architecture audits that spawn sub-agents persist the raw
sub-agent transcripts and per-stream extracted findings into the audit
artifact directory at `openspec/_bmad-output/knowledge/audit/<date>-
architecture/raw-transcripts/` and `findings/` respectively, with a
`raw-transcripts/MANIFEST.md` mapping each stream prefix to its
transcript and findings files. Persistence occurs before session
container reclaim, so that the audit corpus survives ephemeral
container storage loss and supports downstream re-clustering,
Tier-D deprecation confirmation, resolution-CHG drafting, and use
of the corpus as the evidence base for the methodology codification
ADR.

### Acceptance
- Given the architecture audit directory at
  `openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/`,
  when `raw-transcripts/MANIFEST.md` and the per-stream findings files
  are inspected, then `MANIFEST.md` lists at least 35 stream rows
  matching the per-stream tally in
  [`findings-index.md`](../../_bmad-output/knowledge/audit/2026-05-17-architecture/findings-index.md),
  and every `raw_path` and `findings_path` cell in `MANIFEST.md`
  resolves to an existing file.

### Non-acceptance
- Status is `draft` (not `tests-green`): the mechanical enforcement
  test is deferred to the methodology codification ADR. This is a
  red-first violation (the persistence happened in TASK-0040 before
  the REQ existed); see THEME-MM (Retroactive compliance remediation)
  in [`consolidated.md`](../../_bmad-output/knowledge/audit/2026-05-17-architecture/consolidated.md)
  for the broader pattern, which the methodology codification ADR is
  expected to address.
- The `ARCH-` stream (Wave 1, in-context) is exempt from the
  manifest count: in-context passes have no separate sub-agent
  transcript. The 36-stream → 35-transcript gap is intentional and
  documented in `MANIFEST.md`.
- Future audits (the queued implementation audit; subsequent
  architecture audits) inherit this REQ; the queued methodology
  codification ADR (no allocated ID yet) will formalise the enforcement
  gate. <!-- spec-lint: allow prose-xref-banned -->

### Notes
- The persistence happened post-hoc via
  [`raw-transcripts/persist-corpus.py`](../../_bmad-output/knowledge/audit/2026-05-17-architecture/raw-transcripts/persist-corpus.py),
  a one-shot rescue tool. Future audits should persist inline (each
  sub-agent's findings written into `findings/` as it returns) rather
  than relying on rescue from the container-local cache.
- The README at
  [`openspec/_bmad-output/knowledge/audit/2026-05-17-architecture/README.md`](../../_bmad-output/knowledge/audit/2026-05-17-architecture/README.md)
  originally claimed raw outputs would not be persisted; that was a
  recoverability defect corrected by CHG-0032 TASK-0040.
