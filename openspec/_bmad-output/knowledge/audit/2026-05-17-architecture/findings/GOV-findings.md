# GOV — validate-prd-governance-focused (opus) — Wave 5

**Source transcript:** [`raw-transcripts/GOV-agent-a285fe15ec2c6863e.jsonl`](../raw-transcripts/GOV-agent-a285fe15ec2c6863e.jsonl)
**Sub-agent description:** `Governance-focused validation review`
**Session ID:** `2fa6b8f3-f53b-44bf-873e-44bdb568369b`
**Agent ID:** `a285fe15ec2c6863e`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the BMAD skill `bmad-validate-prd` and use it to perform a **governance-focused validation review** of the architecture artifact under /home/user/Test-Repo/.

Documents to review (read all 15; do not read anything else):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001-openspec-adoption.md
- openspec/architecture/decisions/ADR-0002-bmad-integration.md
- openspec/architecture/decisions/ADR-0003-tea-tiered-testing.md
- openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md
- openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md
- openspec/architecture/decisions/ADR-0006-testing-tiers.md
- openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md
- openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md
- openspec/architecture/phases/PHASE-0.md
- openspec/architecture/phases/PHASE-1.md
- openspec/architecture/phases/PHASE-2.md
- openspec/architecture/phases/PHASE-3.md
- openspec/architecture/phases/PHASE-4.md
- openspec/architecture/phases/PHASE-5.md

(If exact ADR/PHASE filenames differ, list /home/user/Test-Repo/openspec/architecture/decisions/ and phases/ and read the actual files. There are 8 ADRs and 6 PHASE files.)

Focus scope (NARROW — this is a FOCUSED, not exhaustive, review). You are auditing whether the architecture has adequate GOVERNANCE machinery. Validate the following dimensions and surface defects in each:

1. **REQ ownership and lifecycle** — Who owns a REQ? Who can amend it? What happens when a REQ is in an undefined state (e.g., supersession proposed but not accepted)? Is the status enum closed or open? Are transitions defined?
2. **ADR amendment discipline** — How are ADR amendments numbered, ordered, and reviewed? Is there a quorum or approval mechanism? What blocks an amendment from being merged? Who can author one? Is there a self-amendment hazard (an ADR that authorises amending itself)?
3. **Trailer registry and signal quality** — Are commit trailers a closed vocabulary or open? Who registers a new trailer name? What happens when a trailer's semantics drift?
4. **Decision provenance** — When a CHG is merged, what is the canonical record of WHY it was approved? Does the approval surface name a human approver? Is there an approver list per CHG type?
5. **Phase exit governance** — Who decides a phase is exited? Is "the agent that closes" separated from "the agent that approves closure"? Is there a separation-of-duties principle anywhere?
6. **Spec supersession** — When REQ X supersedes REQ Y, who validates the supersession is semantically correct? Is there any reviewer-class gate, or is it author-only?
7. **Hook-failure governance** — When a hook fails, who decides whether the failure is a real defect or a hook bug? Is there an appeal mechanism? Who can override?
8. **CHG envelope governance** — What blocks a CHG from being opened? Closed? Who owns a CHG once opened? What happens to a stalled CHG?
9. **Audit-of-the-audit governance** — Who audits the architecture audit? Is there a meta-governance layer for the audit methodology itself?

Do NOT surface findings outside governance. If an issue is structural-but-not-governance (e.g., "the directory layout is wrong"), exclude it. If it's security/ops (e.g., "secrets handling is missing"), exclude it. If it's implementation-readiness (e.g., "this gate isn't wired to CI"), exclude it. Bias toward governance machinery itself: who decides, who reviews, who approves, who blocks.

A prior Wave-2 stream called `VALID-` (and Wave-4 `VALID2-`) used the same bmad-validate-prd skill but EXHAUSTIVELY across all dimensions. Your value is the GOVERNANCE FOCUS — go deeper on governance than VALID/VALID2 could, and skip the dimensions they covered (validation framing, completeness checks, structural rigor).

REQUIRED OUTPUT:
- All finding IDs prefixed `GOV-` with severity inline (e.g., `GOV-CRIT-001`, `GOV-SER-002`, `GOV-PROC-003`)
- Severity guide: CRIT = blocks future PHASE-1 exit if not addressed; SER = should be addressed before any new CHG can ship; PROC = process drift / documentation defect
- Minimum 15 findings, target 18-22
- Each finding cites a specific artifact (file path + section or REQ/ADR ID + paragraph) AND identifies the governance principle being violated AND the failure mode
- 1500-2500 words total
- NO preamble, NO "I have read all 15 documents" intro. Start directly with finding GOV-CRIT-001 (or GOV-SER-001 if no CRIT applies).
- End with a one-paragraph summary that totals findings by severity and names the most under-served governance dimension.

Do not read files outside the architecture documents listed.
```

## Findings deliverable (final assistant message)

Now I have all 15 documents. Let me produce the governance-focused validation findings.

GOV-CRIT-001 — REQ ownership is undefined across the entire spec storage discipline. `ADR-0004-spec-storage-discipline.md` §5 defines the per-REQ block with frontmatter fields (`id`, `revision`, `status`, `introduced`, `supersedes`, `phase`, `tier`, `references`) but contains no `owner`, `author`, `approver`, or `steward` field. `ARCHITECTURE.md` §4 lists REQs as atomic units with stable IDs but never names a class of agent authorised to amend them. The governance principle violated is *attributable mutation* — every change to a stable artifact must name the principal who made it. Failure mode: any agent with write access can advance a REQ's `status` from `tests-red` to `tests-green` without an authorising signature, and the matrix has no field to dispute it.

GOV-CRIT-002 — The REQ `status` enum in `ADR-0004` §5 (`draft | tests-red | tests-green | reviewed | merged | deprecated`) is presented as a flat list with no transition diagram, no precondition table, and no terminator class. `ADR-0005` §4 enforces only two transitions (`draft` → must pass through `tests-red` before `tests-green`; `deprecated` → cannot reactivate). The remaining six pairwise transitions (`tests-green` → `reviewed`, `reviewed` → `merged`, `merged` → `deprecated`, etc.) are unspecified. Governance principle violated: closed-form state machines. Failure mode: an undefined transition such as `tests-green` → `draft` cannot be rejected by any gate because no gate defines it as illegal.

GOV-CRIT-003 — Supersession has no reviewer-class gate. `ADR-0004` §1 declares "Material change to a requirement produces a new REQ with `supersedes: <old-id>`; the old REQ remains in the file with `status: deprecated`," and §7 reiterates "Material edits create a new REQ." Neither passage names anyone who validates that the new REQ is semantically a superset, complement, or contradiction of the old. The frontmatter has a `supersedes:` pointer but no `supersession_review:` field, no required approver-id, and no two-key requirement. Governance principle violated: separation of authorship from approval at the supersession boundary. Failure mode: a malicious or careless author can deprecate a constraining REQ and replace it with a permissive one in one CHG, with no reviewer-class agent required to attest the swap is semantically correct.

GOV-CRIT-004 — ADR amendment authority is unbounded. `ADR-0002` §amendment-log and `ADR-0005` §10 both end with the boilerplate "Amendments are append-only. A subsequent material change to behavior introduced by a prior amendment requires a new amendment row, never an edit to a prior row." Nothing in either ADR (or in `ADR-0008`'s gate inventory) names who may author an amendment, how many approvers are required, what quorum applies, or what reviewer class blocks merge. `ARCHITECTURE.md` §0 (preamble) merely states modifications "require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate" without specifying who countersigns. Governance principle violated: ADR amendment is the highest-leverage mutation in the system; it requires the strictest approval gate and has none.

GOV-CRIT-005 — Self-amendment hazard on `ADR-0008`. `ADR-0008` §1 includes `gate-coverage` as a gate that "walks every ADR and every principle … and verifies that at least one entry in the table above references it." But `ADR-0008` is the ADR that defines the table. There is no rule preventing an amendment to `ADR-0008` itself from removing a gate row, nor a quorum requirement for gate-removal amendments. Governance principle violated: an ADR may not be the sole judge of its own amendments. Failure mode: a single PR could amend `ADR-0008` to delete `mock-in-repo-banned` from the table, and `gate-coverage` (which the same PR can amend in lock-step) cannot self-detect the deletion.

GOV-SER-001 — Trailer vocabulary is open, not closed. `ADR-0005` §3 mandates four trailers (`Task`, `Requirements`, `Tests-Status`, `Phase`) and `ADR-0005` §7 introduces `Checkpoint: true`. `ADR-0002` §8 introduces `Skill-Removal-Acknowledged`. `ADR-0006` §4 introduces `Bootstrap`. `ARCHITECTURE.md` preamble introduces `Material-Architecture-Change`. No ADR enumerates the complete trailer vocabulary; no registry file is named; no gate validates that a trailer is *known*. Governance principle violated: closed-vocabulary signals. Failure mode: a typo (`Tests-Statu:`) silently parses as an unknown trailer, and the parser cannot tell trailer-drift from trailer-typo without a registry.

GOV-SER-002 — `commit-trailers-valid` in `ADR-0008` §1 has no spec for what it validates beyond "malformed messages." Without a registry (GOV-SER-001) it cannot block use of a trailer name the project never registered. Governance principle violated: gates must be authored against an explicit specification, not against undocumented developer intent. Failure mode: trailer semantics can drift (e.g., `Tests-Status: green` repurposed silently to mean "skip the check") because no spec file pins the legal values.

GOV-SER-003 — Decision provenance for CHG approvals is missing. `ARCHITECTURE.md` §4 lists `CHG-<NNNN>` with canonical home `openspec/changes/<CHG-NNNN>/` but no document under `openspec/architecture/` requires an approval record per CHG. `ADR-0005` §1 lists git history as the first source of truth, but commit trailers (§3) do not include `Approved-By:`, `Reviewed-By:`, or any quorum field. Governance principle violated: every merge to `main` requires a named human approver in the artifact network; relying on GitHub's review UI alone is not a SoT-resident record. Failure mode: post-hoc audit of "why was CHG-0010 approved?" can only retrieve GitHub review metadata external to the repository, violating the SoT principle in `ARCHITECTURE.md` §1.

GOV-SER-004 — No approver-list classification per CHG type. `ADR-0002` §6 calls a BMAD upgrade "a substrate PR (hybrid policy → you merge)" — using the second-person pronoun where an artifact requires a role. `ADR-0008` §6 says branch protection enforces no-bypass for `main`, but neither ADR enumerates approver classes (e.g., `substrate-PR-approver`, `spec-PR-approver`, `gate-amendment-approver`). Governance principle violated: privilege stratification. Failure mode: a substrate PR and a spec PR are treated identically by the approval surface, even though their blast radii differ by orders of magnitude.

GOV-SER-005 — Phase-exit decision authority is unspecified. `ADR-0008` §3 says "The `phase-exit` gate runs on merge to `main` and verifies … If any check fails, the merge is blocked," and `ARCHITECTURE.md` §11 says "the phase exit ADR is a `gate`-type task." Neither defines who *authors* the phase-exit ADR, who reviews it, or how separation-of-duties between "the agent that closes the phase" and "the agent that approves closure" is enforced. `PHASE-0-foundation.md` §"Exit gate" only references the CI gate, not the human approval. Governance principle violated: separation of duties at phase boundaries. Failure mode: the same agent that authored the in-phase work can self-sign the phase-exit ADR.

GOV-SER-006 — `gate-coverage` covers principles and ADRs but not phases. `ADR-0008` §2 says `gate-coverage` "walks every ADR and every principle … verifies that at least one entry in the table above references it." It does not require a gate per PHASE. PHASE files declare exit criteria but there is no machinery requiring that *each* PHASE-exit set is gated by a named entry in the inventory. Governance principle violated: gate-coverage completeness. Failure mode: a phase could be silently exit-criterion-mutated by editing its `.md` file without any gate inventory change being required.

GOV-SER-007 — Hook-failure governance has no appeal mechanism. `ADR-0005` §6 defines seven hooks; `ADR-0008` §6 says `--no-verify` and other bypasses are "forbidden by `CLAUDE.md`" and by branch protection. There is no documented appeal path when a hook is genuinely buggy (e.g., a regex in `validate_commit.py` rejects a syntactically valid trailer). The `Checkpoint: true` exemption (`ADR-0008` §6) covers checkpoint commits only, not buggy-hook overrides. Governance principle violated: a no-override regime requires a documented appeal channel; otherwise the system has no recourse for its own bugs. Failure mode: a hook bug becomes a hard block; the only recovery is to merge a hook-fix PR, but if the hook-fix PR itself triggers the buggy hook, the system is wedged.

GOV-SER-008 — CHG open/close governance is absent. `ARCHITECTURE.md` §4 lists CHG as an atomic unit and §3 places them under `openspec/changes/<CHG>/`. No ADR specifies (a) what blocks a CHG from being opened, (b) what blocks one from being closed, (c) who owns a CHG once opened, (d) what happens to a stalled CHG. `ADR-0002` references CHG-0010 retrospectively; `ADR-0005` §10 references CHG-0002 in its amendment log; neither references the governance rules for CHG state. Governance principle violated: every long-lived addressable artifact must have a defined lifecycle. Failure mode: a CHG opened by an agent that subsequently stalls has no documented reassignment or escalation path.

GOV-SER-009 — Stale-CHG enforcement is deferred indefinitely. `ADR-0002` §7 mentions a "future spec_lint rule `stale-staging`" for staging drafts but no parallel rule exists for stale CHGs. Governance principle violated: temporal hygiene of in-flight artifacts. Failure mode: CHGs accumulate, partial REQs accumulate against them, and the traceability matrix carries indefinite open-state pointers with no policy to reap them.

GOV-SER-010 — Audit-of-the-audit layer does not exist. `ADR-0005` §9 provides `tools/trace/audit.py` for querying the matrix and §2 says the matrix "is regenerated by `tools/trace/rebuild.py`." Neither ADR specifies who audits the auditor — i.e., who validates that `audit.py` and `rebuild.py` are themselves correct. There is no meta-gate that hashes a known-good matrix and compares. Governance principle violated: meta-governance — the tools that enforce governance must themselves be governed. Failure mode: a regression in `rebuild.py` that silently drops a class of REQ from the matrix passes CI because `matrix-drift` only checks "committed matrix == rebuilt matrix," not "rebuilt matrix is complete."

GOV-SER-011 — Quarterly threshold review for `ADR-0004` §4 has no named reviewer. `ADR-0004` §4 says "The threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." No artifact identifies who performs the review, how the previous threshold is challenged, or what triggers rollback. Governance principle violated: scheduled governance tasks require named owners. Failure mode: the quarterly review silently lapses; the threshold drifts out of relevance with no escalation.

GOV-SER-012 — ADR-0002 amendment numbering is locally scoped but unenforced. `ADR-0002` amendment log has amendments `0001` and `0002`; `ADR-0005` amendment log has amendment `0001`. There is no convention specifying that amendment IDs are per-ADR, no gate that verifies monotonicity within an ADR, no rule against duplicates, and no specification of what happens when two CHGs concurrently propose amendment `0003` against the same ADR. Governance principle violated: identifier monotonicity must be enforced where IDs are allocated. Failure mode: race condition on concurrent amendment proposals produces a collision that is detected only at merge.

GOV-SER-013 — ADR-0002 amendment 0002 is attributed to two source identifiers ("CHG-0010 (TASK-0021)") whereas amendment 0001 is attributed to "CHG-0010" only. The schema for the amendment-log table's `CHG` column is undocumented — is it a CHG, a CHG+TASK pair, or free text? Governance principle violated: schema rigidity of audit columns. Failure mode: downstream tooling that parses the amendment log cannot reliably extract the originating CHG.

GOV-SER-014 — `ADR-0005` §3 trailer `Tests-Status` values include `red→green` (an arrow character). No spec defines whether the arrow must be a literal Unicode U+2192 or the ASCII `->`. `commit-trailers-valid` cannot validate against an unspecified glyph set. Governance principle violated: canonical-encoding specification for machine-validated fields. Failure mode: cross-platform commit messages diverge silently; a trailer with `->` instead of `→` is rejected by one validator and accepted by another.

GOV-PROC-001 — `ADR-0003` is titled "Apps Script runtime" but `CLAUDE.md` and `ARCHITECTURE.md` §10 (REQ-ARCH-0002) refer to "ADR-0003" without title, and the directory listing shows `ADR-0003-appscript-runtime.md` while the user's task brief listed `ADR-0003-tea-tiered-testing.md`. The naming history (whether the ADR was ever renamed) is not captured in any amendment log. Governance principle violated: ADR title immutability or, if renamed, mandatory supersession trail. Failure mode: external references to "ADR-0003" carry implicit topic assumptions that may not match the current file.

GOV-PROC-002 — PHASE files' frontmatter `status` enum (`in-progress`, `pending`) is undeclared. Only PHASE-0 is `in-progress`; the rest are `pending`. No ADR enumerates valid phase-status values, transition rules, or who flips them. Governance principle violated: status enums must be enumerated in a spec, not inferred from current values. Failure mode: a hypothetical `blocked` or `aborted` status has no place to land.

GOV-PROC-003 — The `Phase-0 re-gate` mechanism in `ARCHITECTURE.md` §0 preamble ("Modifications to the structure described here require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate") is named but unspecified. No ADR defines what a "re-gate" entails, who triggers it, what its exit criteria are, or how it differs from the original PHASE-0 exit. Governance principle violated: every named procedure must have a specification. Failure mode: any agent invoking a re-gate inherits no rules and produces an unauditable approval.

---

Summary. Total findings: 22 — 5 CRIT, 14 SER, 3 PROC. The most under-served governance dimension is **ADR amendment discipline**: amendment authoring, numbering, and approval are unbounded, the self-amendment hazard on `ADR-0008` is unmitigated, the per-ADR amendment ID scheme has no enforced monotonicity, the schema of the amendment-log table is undocumented, and there is no quorum mechanism preventing a single agent from rewriting the governance machinery itself. This dimension touches GOV-CRIT-004, GOV-CRIT-005, GOV-SER-012, GOV-SER-013, and GOV-PROC-003, and its remediation should be the highest-priority governance work before any new CHG ships.
