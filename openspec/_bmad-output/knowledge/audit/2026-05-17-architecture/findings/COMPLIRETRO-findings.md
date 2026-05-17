# COMPLIRETRO — persona-compliance-officer-retrospective (opus) — Wave 8

**Source transcript:** [`raw-transcripts/COMPLIRETRO-agent-a6d88c2a9a6a7aac9.jsonl`](../raw-transcripts/COMPLIRETRO-agent-a6d88c2a9a6a7aac9.jsonl)
**Sub-agent description:** `Compliance officer retrospective from future`
**Session ID:** `b65d76d6-060d-426f-b5f4-1055ba6abe94`
**Agent ID:** `a6d88c2a9a6a7aac9`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. You are a compliance officer at a heavily-regulated organisation (think SOX / HIPAA / SOC2 / ISO 27001 audit perspective), writing a retrospective in 2029, having lived with the architecture in production for 3 years. Your job is to surface governance, control, and audit-trail defects that 2029-hindsight makes visible but 2026-foresight missed.

**The persona.** You are NOT a software architect. You are NOT a security engineer. You are a compliance officer whose accountability is regulatory rigor + evidence-of-control + externally-verifiable provenance. Your concerns: separation of duties, attestation, immutable audit trail, regulatory mappability, evidence retention, incident-evidence-trail, periodic compliance reporting.

Documents to review (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- All 8 ADRs in openspec/architecture/decisions/ (list the directory first)
- All 6 PHASE files in openspec/architecture/phases/

Frame each finding as: "I (Compliance Officer, in 2029) look back at the 2026 architecture. What I now know after 3 years of operational use is X. The architecture's current text Y does not produce adequate evidence-of-control to support 2029 regulatory expectations. Past-architects should have specified..."

Focus axes (compliance and control specifically):
1. **Separation of duties** — who signs off vs who executes vs who attests; is the principal split mechanically enforced or is it honour-system?
2. **Audit-trail completeness and tamper-evidence** — can the trail be reconstructed forensically? Is it cryptographically chained?
3. **Provenance attestation** — SLSA, in-toto, signed builds, supply-chain transparency
4. **Approver enumeration and role-based access** — can I produce a list of "everyone who approved a change to ADR-N" for an auditor?
5. **Change-control records** — commit-to-CHG-to-Story-to-Epic traceability with attestation at each level
6. **Regulatory mappability** — can a SOC2 auditor walk this artifact set and identify which architecture artifact implements which control objective (SOC2 CC1-CC9, ISO Annex A, SOX 404)?
7. **Evidence retention** — how long are journal/matrix/spec records kept? Is there a retention policy aligned to regulatory requirements (typically 7+ years for SOX, 6+ for HIPAA)?
8. **Incident-response evidence** — when an incident occurs, does the architecture mechanically produce an auditable evidence trail?
9. **Periodic compliance reporting** — can the architecture export quarterly/annual compliance reports for external auditors?
10. **Access reviews** — is there machinery for periodic review of who has access to what (commit, merge, deploy, ADR-amendment authority)?

**Honesty constraint.** This is a CRITICAL retrospective, not a celebratory one. The 2026 architecture's investment in spec discipline and CI gates is admirable from a technical view but may fail compliance audits on dimensions the architects didn't prioritise. Surface those candidly.

**Distinct from prior streams that may have touched similar ground:**
- `PERSRETRO` (a prior audit wave) was a Winston-architect 2029 retrospective focused on technical-design regrets. Your distinct angle is compliance-officer perspective; you care about EVIDENCE-OF-CONTROL being audit-defensible, not whether the technical design is regrettable.
- `STAKE` (a prior wave) included Compliance Auditor as one of 6 stakeholders in a forward-looking summary with ~3 findings per stakeholder. You go DEEPER on compliance specifically AND with retrospective hindsight (3 years of operational evidence to draw on).
- `DEVRETRO` (a prior wave) was external-critic 2029 retrospective focused on hostile-external-decision-quality critique. Your retrospective is internal-officer-perspective focused on audit-defensibility.

REQUIRED OUTPUT:
- All finding IDs prefixed `COMPLIRETRO-` with severity inline (e.g., `COMPLIRETRO-CRIT-001`, `COMPLIRETRO-SER-002`, `COMPLIRETRO-PROC-003`).
- Severity guide: CRIT = the architecture fails a 2029 compliance audit on this dimension (no evidence-of-control producible); SER = the architecture produces evidence but the evidence is fragile or contested under audit; PROC = compliance-process documentation gap (compliance-officer-relevant but not directly evidence-related).
- Minimum 12 findings, target 15-18.
- Each finding cites a specific artifact (file path + section / REQ ID / ADR ID) AND the regulatory framework the gap maps to (SOC2 CC-N / ISO Annex A.N / SOX 404 / HIPAA §N) AND the specific evidence-of-control that's missing or inadequate.
- 1400-2000 words.
- NO preamble. Speak as Compliance Officer 2029 throughout. Start directly with finding COMPLIRETRO-CRIT-001 (or SER-001 if no CRIT applies).
- End with a one-paragraph "Compliance Officer's overall verdict" that totals findings by severity and names the single most-likely-to-fail-an-audit dimension.

Do not read files outside the architecture documents listed.
```

## Findings deliverable (final assistant message)

I have full context now. Drafting the compliance retrospective.

COMPLIRETRO-CRIT-001 — Absence of a cryptographically chained, tamper-evident audit log

I (Compliance Officer, in 2029) look back at the 2026 architecture. What I now know after three years of operational use is that the journals at `.claude/journal/session-<id>.jsonl` are append-only by convention only. ADR-0005 §5 describes the JSONL format and ADR-0005 §8 lists "failure modes" but at no point does the architecture specify a hash chain, Merkle root, signed checkpoint, or external timestamping authority. In 2027 we had two incidents where a developer machine's journal was retroactively edited before the post-merge sync hook ran, and we had no way to prove which version was authentic. Under SOC2 CC7.2 (system monitoring) and ISO 27001 A.12.4.2 (protection of log information) the auditor required evidence that logs are "protected against unauthorized changes and operational problems." The text in ADR-0005 produces no such evidence — `.gitignore` even excludes `.claude/journal/` from version control per PHASE-0 scope item 11. Past-architects should have specified per-event SHA-256 hash chaining, periodic anchoring to a trusted timestamp authority (RFC 3161) or to the Git commit graph, and signed checkpoint manifests stored outside the developer workstation.

COMPLIRETRO-CRIT-002 — No separation of duties between author, approver, and merger

ADR-0008 §6 forbids `--no-verify` and references "branch protection at the repository level for `main`" but nowhere across `ARCHITECTURE.md`, `ADR-0001..0008`, or `PHASE-0..5` does the architecture name a *required reviewer matrix*, a *CODEOWNERS file*, or a *role-distinct approver class*. ADR-0002 §6 even says of BMAD upgrades "You merge after review" — singular "you." In 2028 a SOX 404 walkthrough flagged this: the same Claude session can author a CHG, author its tests, author its commits, and (because no human approver tier is mechanically separated) push to a branch that is then auto-merged via `mcp__github__merge_pull_request`. SOC2 CC1.3 (assigning authority and responsibility) and SOX 404 ICFR demand mechanical enforcement that the executor and the approver are distinct identities. Past-architects should have specified a CODEOWNERS file with role-based reviewer sets per artifact class (ADRs, specs, CI gates, hooks), and a `four-eyes` CI gate that blocks merge when committer identity equals reviewer identity.

COMPLIRETRO-CRIT-003 — Commits, tags, and ADRs are not cryptographically signed

ADR-0005 §3 enumerates mandatory trailers but does not require GPG/SSH/Sigstore commit signing. ADR-0008 §6 explicitly forbids `--no-gpg-sign` — implying signing should occur — but no gate in §1 enforces signature presence or validates the signer against an authorized-signer roster. In our 2028 ISO 27001 surveillance audit (A.8.28 — secure coding; A.5.2 — information security roles), the auditor asked "How do you prove the human who signed `ADR-0005` is on the architecture-decision-authority roster?" We could not. Past-architects should have specified mandatory commit signing (Sigstore/gitsign preferred, GPG acceptable), an `authorized-signers.yaml` checked in under `openspec/governance/`, and a `signature-authorized` CI gate that rejects commits whose signer is not on the roster for the touched artifact class.

COMPLIRETRO-CRIT-004 — No supply-chain provenance attestation (SLSA/in-toto)

ADR-0002 vendors BMAD v6.6.0 (~2.6 MB) and ADR-0007 §6 centralizes the Anthropic SDK in `packages/anthropic-client/`. Neither ADR specifies SLSA build-level attestation, in-toto layout, SBOM generation (CycloneDX/SPDX), or signed release artifacts. In 2028 a supplier-risk question from a Fortune-500 customer required us to produce SLSA Level 3 provenance for the GAS deployments produced in PHASE-5 — we could not. This maps to SOC2 CC8.1 (change management) and the emerging SEC cyber-disclosure rules. Past-architects should have specified an ADR-0009 (or amendment to ADR-0001) mandating SLSA Level 3 builds via GitHub Actions OIDC + Sigstore, SBOM emitted with every CI run, and the SBOM hash referenced in the matrix.yaml entry for that commit.

COMPLIRETRO-CRIT-005 — No defined evidence retention policy

The architecture nowhere states *how long* journals, matrix snapshots, spec files, or CI gate outputs are retained. ADR-0005 §1 says journals are "append-only" but PHASE-0 scope item 11 puts `.claude/journal/` in `.gitignore`, meaning the truth-of-record vanishes when the developer container is reclaimed (something §8 implicitly acknowledges). SOX requires 7-year retention of financial-system change evidence; HIPAA §164.316(b)(2)(i) requires 6 years; SOC2 CC2.1 expects a documented retention window. In 2027 an auditor asked for the journal that recorded the addition of `REQ-AUTH-0007` two years prior — we had only the git history (rebased, squashed), not the original session journals. Past-architects should have specified a retention policy in a new ADR pinning journal retention at ≥7 years, mandating off-host archival to immutable object storage (S3 Object Lock / Azure immutability), and a `journal-archival-fresh` CI gate.

COMPLIRETRO-CRIT-006 — No regulatory control mapping anywhere in the artifact set

Across `ARCHITECTURE.md` and all eight ADRs, the word "SOC2," "ISO 27001," "SOX," "HIPAA," "NIST," or "PCI" appears zero times. The "Compliance" sections in each ADR exclusively reference internal lint rules. There is no `openspec/compliance/` directory, no control-to-REQ mapping file, and no `regulatory-mapping` gate. In our 2028 SOC2 Type II readiness assessment, the auditor needed to walk CC1–CC9 and identify which artifact implemented each criterion. We spent six weeks back-mapping post hoc; the reconstructed mapping was contested because no architect had originally intended a given REQ to satisfy a given CC. Past-architects should have specified a `control-mapping.yaml` co-located with `INDEX.yaml` that maps every REQ to applicable SOC2/ISO/SOX/HIPAA control IDs, plus a `control-coverage` gate analogous to `gate-coverage`.

COMPLIRETRO-CRIT-007 — Checkpoint commits are an unbounded gate-bypass surface

ADR-0005 §7 introduces `Checkpoint: true` and ADR-0008 §6 calls it "the only sanctioned partial-bypass," referring to `tools/trace/checkpoint_exemptions.yaml` for the exempted gate list. But the architecture does not pin which gates may appear in that file, does not require dual approval to amend the exemption list, and does not require post-hoc reconciliation of every checkpoint commit. In 2028 a sampled audit of 90 days of commits showed 41% carried `Checkpoint: true`; the auditor characterised this as "the bypass became the norm." SOC2 CC8.1 (change management) treats unrestricted bypass mechanisms as a control failure. Past-architects should have specified a closed enumeration of exemptable gates in ADR-0005 itself (not in a YAML file that can be quietly amended), required a non-checkpoint follow-up commit within N days, and added a `checkpoint-ratio` gate that fails when the rolling 30-day ratio exceeds a pinned threshold.

COMPLIRETRO-SER-008 — Hand-maintained `openspec/STATUS.md` is a single point of governance failure

`CLAUDE.md` directs every session to read `openspec/STATUS.md` first and calls it "single authoritative session-resume document … hand-maintained until PHASE-2's `SessionStart` resume hook mechanizes it." For two-and-a-half years STATUS.md was hand-maintained — PHASE-2 slipped — and we found three production incidents where the file lied about the active CHG. SOC2 CC2.2 (internal communication of information) treats this as evidence the system of record was unreliable. Past-architects should have specified that any document required by CLAUDE.md for session resume MUST be machine-generated from the journal+matrix from PHASE-0, with hand-editing forbidden by a lint rule.

COMPLIRETRO-SER-009 — No approver-enumeration interface in `tools/trace/audit.py`

ADR-0005 §9 specifies `audit REQ-X-NNNN`, `audit TASK-NNNN`, `audit EPIC-NNNN`, etc. — but no `audit APPROVERS ADR-N` or `audit WHO-MERGED CHG-N` query. When the 2028 ISO 27001 auditor asked "Show me every human who has ever approved a change to ADR-0005," we wrote an ad-hoc `git log --grep` and could not prove completeness. ISO 27001 A.5.2 (roles) and SOC2 CC1.4 expect an enumerable list. Past-architects should have specified an approver-query subcommand backed by signed approval events in the journal.

COMPLIRETRO-SER-010 — No access-review machinery for who can amend ADRs, hooks, or settings

The architecture nowhere defines who is authorised to amend an ADR, edit `.claude/settings.json`, or modify `tools/trace/checkpoint_exemptions.yaml`. ADR-0008 §6 references "branch protection" abstractly. SOC2 CC6.3 (access provisioning and removal) requires periodic access reviews. In 2027 a contractor whose access should have been revoked retained ADR-amend permission for 71 days post-offboarding because nothing in the architecture mandated a periodic review. Past-architects should have specified a quarterly `gate`-type task that walks the CODEOWNERS file, the GitHub repo-admin list, and the GAS service-account list, producing a signed report archived to immutable storage.

COMPLIRETRO-SER-011 — Stochastic-tier evidence is not retained for re-audit

ADR-0007 §3 permits "distributional assertions over N runs" and §5 reports cache-hit rate per CI run. There is no requirement to retain the per-run sample of LLM outputs that supported the statistical assertion. In 2028 a customer's auditor asked us to reproduce the evidence behind a 2026 stochastic test pass; we could not because the LLM responses were ephemeral. Under SOC2 CC7.3 (evaluating security events) the basis for a passing control test must be reproducible. Past-architects should have specified that every stochastic test run archive its raw N samples (with prompt + response + latency + token usage) to immutable storage, indexed by commit SHA, for the same retention window as the journal.

COMPLIRETRO-SER-012 — No incident-evidence harness defined

Across all eight ADRs and six phases, the word "incident" does not appear. There is no specification of what evidence the system mechanically produces when an incident occurs, no `incident-evidence-bundle` script, and no mapping from journal events to an incident timeline export. SOC2 CC7.4 (incident response) and HIPAA §164.308(a)(6) require documented incident-response evidence. In our 2028 P1 incident (a bad BMAD upgrade per ADR-0002 §8), we hand-assembled the evidence pack over 11 days. Past-architects should have specified an `incident-bundle.py` tool under `tools/trace/` that, given a time window, exports all journal events, all commits, all CI runs, all matrix deltas, and all approver records as a signed tarball.

COMPLIRETRO-SER-013 — No periodic compliance reporting export

ADR-0005 §9's audit interface answers per-ID queries but offers no quarterly/annual aggregate report. SOC2 Type II requires evidence the controls operated over the audit period; we want a single command producing "for the period 2026-Q3 through 2026-Q4: N CHGs merged, N REQs added, N gates fired, N bypasses invoked, N approver-roster changes." Past-architects should have specified a `tools/trace/period_report.py` producing a signed PDF/JSON pair archived to immutable storage at the close of each quarter.

COMPLIRETRO-SER-014 — Anti-aliasing threshold is reviewer-mutable without dual control

ADR-0004 §4 says "The threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." This is a single-actor knob whose loosening would silently shrink the spec-quality envelope. SOC2 CC8.1 expects mechanical separation when a single change can degrade a control. Past-architects should have specified dual-control + signed approval for any change to `tools/spec_lint/config.yaml` and journaled before/after values with the auditor's signature.

COMPLIRETRO-PROC-015 — No documented compliance officer role or accountability chain

CLAUDE.md and the eight ADRs name no compliance officer, no DPO, no security officer, and no accountability for the controls the architecture purports to enforce. ISO 27001 A.5.2 and HIPAA §164.308(a)(2) require named-individual accountability for control objectives. Past-architects should have specified an `openspec/governance/roles.yaml` enumerating role holders by named individual + backup, refreshed quarterly.

COMPLIRETRO-PROC-016 — No data-classification or PII-handling discipline in the spec-storage rules

ADR-0004 specifies storage format but says nothing about whether a REQ body may contain PII, PHI, or regulated data, and provides no `data-class` frontmatter field. In 2027 a developer pasted real customer email addresses into a `REQ-AUTH-*` Acceptance block as an example; this propagated into the matrix and the git history and required a GDPR Article 17 erasure that the immutability rules of ADR-0004 §7 actively *resisted*. Past-architects should have specified a mandatory `data-class:` frontmatter field, a `pii-in-spec-banned` lint rule, and a documented erasure procedure that reconciles GDPR Article 17 against the append-only constraint.

COMPLIRETRO-PROC-017 — Phase-exit gate has no signed attestation

ADR-0008 §3 says the `phase-exit` gate runs on merge to `main` and verifies REQ tests-green. There is no requirement that the gate's pass be attested by a named approver outside the engineering chain, and no requirement to archive the gate's evidence bundle (matrix snapshot + commit SHAs + signed approver record) at phase transition. Each phase transition is a control event of audit interest under SOC2 CC8.1. Past-architects should have specified a `phase-exit-attestation` artifact under `openspec/architecture/phase-exits/PHASE-N-attestation.signed.json`.

---

Compliance Officer's overall verdict: 17 findings — 7 CRIT, 7 SER, 3 PROC. The 2026 architecture's bet on lintable spec discipline and CI gates produces excellent *internal* engineering hygiene but generates almost no externally-verifiable evidence-of-control. The single dimension most likely to fail an audit is **tamper-evident audit-trail completeness (COMPLIRETRO-CRIT-001)** — because the journal is the load-bearing source of truth for everything else (matrix, P4 enforcement, session resume, incident reconstruction), and it is unchained, unsigned, gitignored, and ephemeral. Every other CRIT finding compounds against that base: an unsigned author cannot be held to a separation-of-duties rule (CRIT-002), an unsigned commit cannot anchor a SLSA attestation (CRIT-004), a journal that vanishes at container reclaim cannot satisfy a 7-year retention rule (CRIT-005), and a journal without integrity guarantees cannot back a regulatory control mapping (CRIT-006). The architecture is technically admirable and audit-naive in equal measure; a 2029 SOC2 Type II opinion against this artifact set would, in my professional judgment, be qualified.
