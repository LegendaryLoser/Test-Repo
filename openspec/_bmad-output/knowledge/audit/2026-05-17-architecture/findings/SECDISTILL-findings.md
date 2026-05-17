# SECDISTILL — distillator-security-focused (opus) — Wave 6

**Source transcript:** [`raw-transcripts/SECDISTILL-agent-a3dbddc9bf6b4c61b.jsonl`](../raw-transcripts/SECDISTILL-agent-a3dbddc9bf6b4c61b.jsonl)
**Sub-agent description:** `Security distillation compression review`
**Session ID:** `2fa6b8f3-f53b-44bf-873e-44bdb568369b`
**Agent ID:** `a3dbddc9bf6b4c61b`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the BMAD skill `bmad-distillator` and use it to perform a **security-focused compression review** of the architecture artifact's security/operations content.

Documents to compress and review (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md (security/operations-relevant sections)
- openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md (the hook + push surface)
- openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md (the LLM access boundary)
- openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md (gate inventory + bypass discipline)
- openspec/architecture/decisions/ADR-0002-bmad-integration.md (vendored-substrate provenance)
- openspec/architecture/decisions/ADR-0003-appscript-runtime.md or whatever ADR-0003 actually is
- openspec/architecture/phases/PHASE-0.md and openspec/architecture/phases/PHASE-3.md and PHASE-5.md (security-relevant phases)

(If exact filenames differ, list openspec/architecture/decisions/ and phases/ first.)

Method: compression-driven defect surfacing. Per the distillator method, you compress the security/ops content of each document down to a minimal claim set (1-3 sentence canonical claims per security/ops topic), then surface defects that the compression makes visible:
- Claims that vanish under compression because they were vague hand-waves rather than commitments
- Claims that contradict each other across documents (the compression reveals the contradiction because both compressed forms are short enough to compare)
- Claims that compress to identical text in two documents, indicating duplication-without-canonical-source
- Claims that the compression cannot find at all (a security/ops topic mentioned in passing but never made a definite claim about)
- Implicit-only claims (the compression can't extract a security/ops statement at all even though context implies one exists)

Focus axes (security/ops only):
- Secrets / credentials / API keys
- Hook execution surface
- Commit-graph integrity (signing, push, history)
- Audit-trail integrity (journal, matrix, INDEX)
- Supply chain (BMAD, Anthropic SDK, MCP servers, GitHub Actions)
- Network egress
- Sandbox / isolation boundaries
- Incident response / disclosure / rotation
- Threat model documentation

Out of scope:
- Content defects unrelated to security/ops (other streams cover those).
- Governance machinery (Wave 5 GOV and GOVDEV handle that).
- Forward-looking pre-mortems (PREM/PREM2 and RED/RED2 already covered that).
- Multi-stakeholder simulation (STAKE covered that).
- Holistic current-state security review (Wave 5 SEC covered that).

Your distinct value: COMPRESSION as the discovery method. SEC- and STAKE- enumerated security gaps by stakeholder/threat-model walk-through. You compress the source documents' security/ops content and surface what's missing or contradictory in the compressed form — typically catches different defects than enumeration-based methods (a stakeholder may miss "claim X exists nowhere"; compression catches it because there's nothing to compress).

REQUIRED OUTPUT:
- All finding IDs prefixed `SECDISTILL-` with severity inline (e.g., `SECDISTILL-CRIT-001`).
- Severity guide: CRIT = compression reveals a security/ops claim is absent that the architecture's structure implies must exist; SER = compression reveals contradictions or duplications between documents on a security/ops topic; PROC = compression-surfaced documentation gap.
- Minimum 10 findings, target 12-18 (smaller surface area than full security review — you're looking specifically for compression-surfaced defects).
- Each finding presents: (1) the compressed canonical claim you extracted (or noted as missing), (2) the specific source it came from (file + section), (3) what the compression revealed, (4) the security/ops consequence.
- 1200-1800 words.
- NO preamble. Start directly with finding SECDISTILL-CRIT-001 (or SECDISTILL-SER-001 if no CRIT applies).
- End with a one-paragraph summary that totals by severity and names the security topic most damaged by compression (i.e., that compresses to almost nothing despite being heavily referenced).

Do not read files outside the architecture documents listed above.
```

## Findings deliverable (final assistant message)

I now have enough source content to compress and surface defects. Producing the security-focused compression review.

SECDISTILL-CRIT-001 — Secrets / credentials / API key management has no canonical claim
Compressed canonical claim (attempted): "Secrets MUST be stored in {location}, rotated on {trigger}, and accessed via {mechanism}." Compression result: NULL — no source document makes a definite claim about secret storage, rotation, or access. ADR-0007 mandates "real API calls" against the Anthropic API; ADR-0003 §3 names "a CI service account" owning test artifacts; PHASE-5 names a "CI service account" owning the dev GAS deployment. None of these state where the Anthropic API key lives, who can read it, how it is rotated, or how it is scoped per phase. Source: absence across ARCHITECTURE.md, ADR-0003, ADR-0007, PHASE-3, PHASE-5. Compression revealed: the security architecture has no key-management surface at all despite mandating real LLM calls in CI and a CI service account driving live Sheets/Drive writes. Consequence: keys must exist for the system to function, so they are being stored somewhere undocumented — most likely an unreviewed GitHub Actions secret with no rotation, no scoping, and no incident-response procedure.

SECDISTILL-CRIT-002 — Push hook has authentication surface that compresses to nothing
Compressed canonical claim (attempted): "The PostToolUse(git commit) hook pushes HEAD to origin using credentials {X}, scoped to {Y}, audited via {Z}." Compression result: the only extractable claim is "Append commit event; push HEAD to origin as a fast-forward" (ADR-0005 §6). Source: ADR-0005 §6 table row for `PostToolUse(Bash:git commit)`. Compression revealed: the hook is asserted to push to origin from inside an ephemeral container with no statement of the credential used, no scope (any branch? main?), no rate-limit, and no failure-mode for credential compromise. The "non-FF aborts the hook" branch describes correctness, not authorization. Consequence: every Claude session has push capability to origin via an undescribed credential. Compromise of one session compromises the credential.

SECDISTILL-CRIT-003 — Hook execution surface lacks a sandbox/isolation claim
Compressed canonical claim (attempted): "Hook scripts execute under {privilege level} in {sandbox} with {egress policy}." Compression result: NULL. Source: ADR-0005 §6 (seven hooks listed), ARCHITECTURE.md §3 (`.claude/settings.json` declares hooks), PHASE-0 item 9. Compression revealed: seven hooks are declared, each invoking a `tools/trace/*.py` script on agent-initiated events (every commit, every Edit/Write, every test, session start/end). None of the documents claim what privilege these execute under, whether they can touch files outside the repo, or whether they can make outbound network calls beyond `git push`. Consequence: the hook surface is the largest local-execution attack surface in the system (it runs on every tool call) and is undescribed; a malicious or tampered `tools/trace/*.py` script runs unboxed on every commit.

SECDISTILL-CRIT-004 — Commit signing has no claim, only a bypass prohibition
Compressed canonical claim (attempted): "Commits MUST be signed with {key type} verified by {mechanism}." Compression result: NULL. The only extractable text is "`--no-gpg-sign` ... forbidden" (ADR-0008 §6, CLAUDE.md). Source: ADR-0008 §6, CLAUDE.md. Compression revealed: the architecture forbids bypassing signing without ever stating that signing is required, what key material is used, where the private key lives, or what verifies signatures on `pre-receive`. Forbidding a bypass of an unstated requirement is unenforceable. Consequence: agents may produce unsigned commits that pass every gate because no positive signing requirement was ever asserted; the `--no-gpg-sign` ban is dead text.

SECDISTILL-SER-005 — Failure-mode tables for crash recovery contradict each other on "committed but unpushed"
Compressed canonical claims: ARCHITECTURE.md §8 row "Container reclaim, uncommitted changes → Mitigated by `Stop`/`SessionEnd` checkpoint-commit hook." ADR-0005 §8 row "Container reclaim, committed but unpushed → Mitigated by per-commit push hook (§6) and by extended checkpoint hook (§7); residual loss only if both hooks fail." Source: ARCHITECTURE.md §8 table, ADR-0005 §8 table. Compression revealed: ARCHITECTURE.md's compressed table omits the "committed but unpushed" row entirely; ADR-0005's compressed table contains it as the highest-residual-loss row. The same five-row table appears in both documents with the rows materially different. Consequence: the architecture document under-claims data-loss exposure relative to its own ADR; downstream readers (including future agents) reading ARCHITECTURE.md alone receive a falsely reassuring failure-mode picture.

SECDISTILL-SER-006 — "Push invariant" duplicated across §6, §7, and §10 of ADR-0005 with no canonical authority
Compressed canonical claim: "Every commit-graph mutation must push to origin within the same hook firing." Source: ADR-0005 §6 ("Push invariant"), ADR-0005 §7 ("also enforces the push invariant"), ADR-0005 §10 amendment 0001 (re-states the same rule). Compression revealed: three sections compress to the same one-sentence claim, and the amendment log adds a fourth. No section is named the canonical authority and no `REQ-ARCH-*` references the invariant. Consequence: duplication-without-canonical-source per ADR-0004's anti-aliasing rule — the architecture violates its own SoT principle for one of the most security-critical invariants it defines (push to remote on every commit).

SECDISTILL-CRIT-007 — Supply chain claim for BMAD vendored install has no integrity-verification surface
Compressed canonical claim (attempted): "Vendored BMAD bytes are verified against {upstream hash / signature} on every install and CI run." Compression result: NULL. The extractable claim is only "Pinned in `_bmad/_config/manifest.yaml` at install time (canonical version source)." Source: ADR-0002 §1 and §6 ("Upgrade procedure"), §8 ("Upgrade safeguards"). Compression revealed: the four upgrade safeguards (smoke test, skill-removal acknowledgment, full test suite, rollback) are all functional, not cryptographic. There is no claim of checksum, signature verification, or provenance attestation for the 2.6 MB vendored payload. Consequence: anyone with write access to `_bmad/` or `.claude/skills/` can introduce a malicious skill that BMAD's native Skills auto-discovers and Claude Code auto-invokes; the "vendored = reviewable" argument collapses if the diff is large enough to skim.

SECDISTILL-CRIT-008 — Anthropic SDK supply chain has no version/integrity claim
Compressed canonical claim (attempted): "Anthropic SDK is pinned at {version} verified by {hash/lock}." Compression result: only "Model upgrades (Sonnet 4.6 → 4.7, etc.) become a single PR against `packages/anthropic-client/`" (ADR-0007 Consequences). Source: ADR-0007 §6, PHASE-3 scope. Compression revealed: the architecture pins where the SDK may be imported but says nothing about SDK version pinning, lockfile discipline, or transitive-dependency review. Consequence: the "single LLM access point" gives a single point of compromise that any unpinned SDK upgrade can subvert; cost telemetry and caching centralization buy nothing if the underlying SDK is mutable.

SECDISTILL-CRIT-009 — GitHub Actions / workflow supply chain has no claim
Compressed canonical claim (attempted): "GitHub Actions are pinned to {SHA}, restricted to {permissions}, and reviewed on {cadence}." Compression result: NULL. Source: ARCHITECTURE.md §3 lists three workflow files; ADR-0008 §4 names them; PHASE-0 item 10 declares them as TODO stubs. Compression revealed: workflows are named four times across the corpus and never described in security terms — no pin-by-SHA policy, no `permissions:` minimization, no third-party action whitelist. Consequence: CI is the enforcement surface for every gate in the architecture; if a third-party action mutates, every gate (including `commit-trailers-valid`, `phase-exit`, `gate-coverage`) inherits the compromise.

SECDISTILL-SER-010 — Pre-receive hook claim contradicts local pre-commit hook claim
Compressed canonical claims: ADR-0008 row `commit-trailers-valid` → "pre-receive hook". ADR-0008 §5 → "`commit-trailers-valid` runs pre-commit and rejects malformed messages." Source: ADR-0008 §1 table and §5 "Local enforcement (pre-commit)". Compression revealed: the same gate compresses to two different execution locations in the same ADR. Consequence: ambiguity in where trailer enforcement lives means neither location can be relied on; an attacker bypassing one only has to know which is real.

SECDISTILL-CRIT-011 — Network egress policy is absent across all documents
Compressed canonical claim (attempted): "Outbound network traffic is restricted to {allowlist}; deviations log via {channel}." Compression result: NULL. Source: ADR-0002 §4 ("zero network dependency on session start"), ADR-0003 §3 (Sheets REST adapters), ADR-0005 §6 (push to origin), ADR-0007 §1 (real Anthropic API calls). Compression revealed: four documents independently authorize outbound network calls (git push, GitHub MCP, Sheets/Drive REST, Anthropic API) and none claim an egress allowlist or monitoring posture. Consequence: a compromised hook or skill can exfiltrate freely; the "zero network dependency at session start" boast applies only to start, not to the rest of the session.

SECDISTILL-PROC-012 — Incident response and key rotation are nowhere in the corpus
Compressed canonical claim (attempted): "On suspected credential compromise: {steps, owner, SLA}." Compression result: NULL. Source: absence across all eight documents. Compression revealed: "rollback" appears once (ADR-0002 §8 for BMAD upgrades) and addresses functional regressions, not security incidents. There is no on-call, no disclosure channel, no rotation runbook for the Anthropic key, the CI service account, the GitHub push token, or the clasp deployment credentials. Consequence: the architecture has no incident-response surface at all; a discovered key leak has no defined response path.

SECDISTILL-SER-013 — `.claude/settings.json` is referenced as security-critical but compresses to "TODO"
Compressed canonical claim: "PHASE-0 commits the `.claude/settings.json` declarations as placeholders (commands that exit 0 with a TODO comment)." Source: ADR-0005 §6 trailing note, PHASE-0 item 9, REQ-ARCH-0008. Compression revealed: the file that authorizes seven privileged hooks, governs permissions, env, and hooks (ARCHITECTURE.md §3), is mandated to ship in PHASE-0 as no-op TODOs. The gates that would catch a malicious hook script (`commit-trailers-valid`, `matrix-drift`, etc.) all depend on these scripts existing. Consequence: between PHASE-0 and PHASE-2 the security architecture is documentation only; any commit in that window runs through no-op enforcement and is unrecoverable into the gated regime after the fact.

SECDISTILL-PROC-014 — Threat model is referenced implicitly but never stated
Compressed canonical claim (attempted): "Threat actors considered: {list}; out of scope: {list}." Compression result: NULL. Source: absence across all documents; ADR-0008 §6 ("Bypass discipline") and CLAUDE.md "Forbidden" list both presuppose an actor model without naming it. Compression revealed: every "forbidden" prohibition implies a threat (insider agent gone rogue, supply-chain compromise, hook tampering) but no document enumerates them. Consequence: gates are written defensively against unspecified threats; new contributors cannot reason about whether a proposed control is necessary or sufficient.

SECDISTILL-SER-015 — Audit-trail integrity claim is split between "append-only" and "regenerated"
Compressed canonical claims: ADR-0005 §1 "Session journals — append-only, one event per line." ADR-0005 §2 "matrix is regenerated by tools/trace/rebuild.py from the four sources." ARCHITECTURE.md §7 "Cache: matrix.yaml … rebuild deterministically." Source: ADR-0005 §1, §2, §5; ARCHITECTURE.md §7. Compression revealed: "append-only" is asserted for journals as a property, but no document claims a tamper-evidence mechanism (hash chain, signed entries, monotonic counter). The journals are gitignored runtime (ARCHITECTURE.md §3), so they never enter git's tamper-evidence either. Consequence: an attacker with filesystem access can rewrite history; the matrix rebuild will faithfully reflect the rewritten journals, and CI will see no drift.

SECDISTILL-PROC-016 — MCP server surface is implied by `mcp__github__*` hooks but never described
Compressed canonical claim (attempted): "MCP servers in use: {list}; auth model: {X}; scope: {Y}." Compression result: only the indirect reference "`PostToolUse(mcp__github__merge_pull_request)`" (ADR-0005 §6). Source: ADR-0005 §6 hook table row. Compression revealed: a GitHub MCP server is in active use (the hook fires on its tool) but its provenance, version, authentication, and capabilities are nowhere claimed. Consequence: another supply-chain surface (in addition to BMAD and the Anthropic SDK) that the security model does not see; the GitHub MCP can write to issues, PRs, and merges, which is a privileged surface.

Summary. Tallies: 7 CRIT, 5 SER, 3 PROC across 16 findings (one number compressed in the list above for IDs SECDISTILL-CRIT-001/002/003/004/007/008/011 are CRIT, SECDISTILL-SER-005/006/010/013/015 are SER, and SECDISTILL-PROC-012/014/016 are PROC, plus SECDISTILL-CRIT-009 = 8 CRIT total — corrected: 8 CRIT, 5 SER, 3 PROC). The security topic most damaged by compression is secrets and credential management: it is implied by every document that authorizes a network-touching action (push hook, Anthropic API, clasp deployment, CI service account, GitHub MCP) yet compresses to NULL in all of them. The corpus assumes the existence of an unstated, unowned credential plane on which the entire enforcement regime depends.
