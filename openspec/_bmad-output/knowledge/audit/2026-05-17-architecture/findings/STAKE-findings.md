# STAKE — stakeholder-simulation (opus) — Wave 4

**Source transcript:** [`raw-transcripts/STAKE-agent-ac2916602be951172.jsonl`](../raw-transcripts/STAKE-agent-ac2916602be951172.jsonl)
**Sub-agent description:** `Stakeholder simulation`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `ac2916602be951172`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke `bmad-advanced-elicitation` with a **stakeholder simulation** method: simulate each of these stakeholders reviewing the architecture and surface what each would object to.

Stakeholders to simulate:
1. **Security engineer** — supply chain, secrets, audit trails, blast radius
2. **SRE / operations lead** — incident response, on-call burden, observability, alerting
3. **Compliance auditor** — provenance, immutability, change-control, separation of duties
4. **Cost / finance owner** — token spend, CI compute, vendor lock-in cost
5. **Open-source steward** — license compatibility (BMAD MIT, Anthropic SDK), reproducibility
6. **Future architect (you in 3 years)** — long-horizon maintainability

Documents (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md, decisions/ADR-0001 through ADR-0008, phases/PHASE-0 through PHASE-5

For each finding: which stakeholder raised it, the concern, the relevant location in the artifact, and why the current architecture doesn't address it.

REQUIRED OUTPUT:
- IDs prefix `STAKE-` (CRIT/SER/PROC inline)
- Minimum 15 findings (≥2 per stakeholder)
- Tag each with stakeholder name
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have read all 15 documents. Now I'll produce the stakeholder simulation findings.

---

**STAKE-CRIT-001 [Security engineer]** — Hooks that auto-push to origin from a `PostToolUse(Bash:git commit)` trigger constitute a remote-code-execution-to-supply-chain pipeline with no signing verification gate. ADR-0005 §6 mandates that every commit hook fast-forwards `HEAD` to origin, and §10 amendment 0001 makes this the "push invariant." A compromised session or an LLM that fabricates a commit message under a developer's identity will publish that artifact to origin before any human review surface fires. The only commit-graph-bypass that is mentioned (`--no-gpg-sign`) is forbidden in CLAUDE.md, but ADR-0008 §6 does not require signed commits — it merely forbids unsigning them. Nothing in the architecture asserts that commits must be GPG- or sigstore-signed in the first place, so the "forbidden" rule has no positive obligation to enforce against.

**STAKE-CRIT-002 [Security engineer]** — The Anthropic API key is implicit but never named in any threat surface. ADR-0007 §6 centralizes "the sole LLM access point" in `packages/anthropic-client/` but says nothing about secret storage, rotation, scope-limiting, per-project key isolation, or what happens when stochastic tests run on PR branches authored by untrusted contributors. PHASE-3 brings the client online without an ADR addressing this. A forked-PR stochastic test can exfiltrate the API key via prompt injection of test corpora unless the key is unavailable to fork-PR CI — no such gate exists.

**STAKE-SER-003 [Security engineer]** — The `.claude/journal/session-<id>.jsonl` files are listed as the canonical truth source (ADR-0005 §1.4) but are `gitignored` (PHASE-0 scope item 11 and the layout note in ARCHITECTURE.md §3). This means the audit "truth" lives on ephemeral container disk and is destroyed at reclaim — yet ADR-0005 §2 says the matrix is derived "from the four sources above." If the journal disappears between sessions, the matrix is no longer reconstructible from sources; only the cache remains, contradicting the "derived cache, never hand-edited" doctrine.

**STAKE-CRIT-004 [SRE / operations lead]** — There is no on-call surface, no paging, no SLO, no error budget, and no runbook anywhere in the architecture. ADR-0008 enumerates 26 CI gates, every one of which can block `main`, but the operational consequence of a failing gate at 3am on a release branch is undefined. PHASE-2 ships a `post_merge_sync.py` hook that fast-forwards a working branch after a merge — if this hook fails partway, the architecture says "aborts the hook with a diagnostic" (ADR-0005 §6 row 3), but it does not say who reads the diagnostic, where it is logged, or what the recovery procedure is.

**STAKE-CRIT-005 [SRE / operations lead]** — Observability is mentioned only via "cost telemetry exported per-call" (PHASE-3 scope item 1) and "cache hit rate is reported per CI run" (ADR-0007 §5). There is no metrics backend, no log aggregation, no traceability of operational events distinct from spec-traceability. The E2E tier in ADR-0003 §3 actually executes against live Google Sheets via clasp deployments — when that test bricks the dev spreadsheet at 2am on the nightly job, nothing in the architecture says how the SRE finds out, rolls back, or alerts the project owner.

**STAKE-SER-006 [SRE / operations lead]** — The `Stop`/`SessionEnd` hook is asserted to be the failsafe for committed-but-unpushed work (ADR-0005 §7, §8). The failure-modes table explicitly admits "residual loss only if both hooks fail to fire (e.g. abrupt container reclaim mid-`PostToolUse`)." This is exactly the failure mode an SRE expects in production (OOM kills, evictions, network partitions during push) and the architecture's only mitigation is two hooks that share the same execution surface. There is no out-of-band reconciliation job that runs against the remote to detect dangling local commits.

**STAKE-CRIT-007 [Compliance auditor]** — Separation of duties is structurally violated. ADR-0005 §6 says the `PreToolUse(Bash:git commit)` hook validates trailers and the `PostToolUse` hook pushes — both run inside the same Claude session, under the same actor identity. The actor that authors the change is the actor that validates it and the actor that publishes it. Compliance frameworks (SOC2 CC8.1, ISO 27001 A.14.2.2) require that change authorship and change deployment cannot be the same principal. The "you merge after review" line in ADR-0002 §6 is the only nod toward human-in-the-loop and is informal prose, not a gated control.

**STAKE-SER-008 [Compliance auditor]** — Immutability claims for the journal (ADR-0005 §1.4: "append-only") are not enforced by any filesystem or storage primitive. The journal lives at `.claude/journal/session-<id>.jsonl` on container disk, gitignored, with no WORM media, no S3 Object Lock, no append-only mount, no checksumming, and no cryptographic chain. A malicious or buggy script that opens the file with `O_TRUNC` destroys the audit trail without detection. ADR-0005 §5 says "partial writes from a crash are discarded by the parser" — that is the only mention of integrity, and it addresses truncation, not tampering.

**STAKE-SER-009 [Compliance auditor]** — Change control has a documentary surface but no approval mechanic. The PHASE files use prose statuses ("status: in-progress", "status: pending") in their frontmatter, and ADR-0008 §3 says the `phase-exit` gate "runs on merge to main." There is no concept of an approver list, no role-based gate, no mandatory reviewer for a phase exit, and no separation between the agent that closes the phase and the agent that authorizes the closure. The "gate-type task" referenced in ADR-0005 §4 and ADR-0008 §6 is not defined in any of the 15 documents.

**STAKE-PROC-010 [Compliance auditor]** — Provenance of the BMAD vendored install is asserted but unverifiable. ADR-0002 §2 says "Version pin: BMAD v6.6.0" pinned in `_bmad/_config/manifest.yaml`, and §6 describes the upgrade as "bump the pinned version… run the script." There is no checksum, no signature, no provenance attestation (SLSA, in-toto), and no verification that the bytes installed match an upstream-published release. The "smoke test" in ADR-0002 §8 confirms behavior, not provenance — a malicious BMAD package that passes the smoke test would be indistinguishable from the real thing.

**STAKE-CRIT-011 [Cost / finance owner]** — Stochastic tier costs are bounded by an annotation (`@cost-budget tokens=<N>`) that the test author writes themselves (ADR-0007 §4). The aggregation runs "per-PR and per-nightly" with no quarterly or monthly ceiling, no per-developer budget, no anomaly detection, and no kill switch. A test author who writes `@cost-budget tokens=10000000` is not flagged — the per-test annotation has no upper bound. PHASE-3 exit criterion says "stochastic tier cost stays within budget for two consecutive nightly runs," which sets a floor of compliance for two runs only.

**STAKE-SER-012 [Cost / finance owner]** — The E2E tier executes "in the deployed GAS runtime" (ADR-0003 §3) via `clasp push` to a dedicated CI service account, and runs nightly per ADR-0008 §4. Google Workspace API quotas are not mentioned anywhere. Apps Script execution quota (6-minute per-trigger limit, daily Drive API quotas) becomes a hard cost ceiling that the architecture has not budgeted for. A second project added in PHASE-5+ doubles the quota draw against the same service account.

**STAKE-SER-013 [Cost / finance owner]** — Vendor lock-in cost is structurally maximized. ADR-0007 §6 mandates "no code outside `packages/anthropic-client/` may import the Anthropic SDK" — but the entire stochastic test tier (ADR-0007 §2) forbids recorded fixtures, meaning the only way to run the test suite is to pay Anthropic per CI run forever. Switching providers requires rewriting every stochastic test, because the assertion forms in §3 are coupled to Claude's specific tool-use schema and response shape. There is no provider-abstraction layer below the client.

**STAKE-SER-014 [Open-source steward]** — BMAD v6.6.0 is asserted to be "MIT-licensed" in ADR-0002 §0, but the architecture vendors ~2.4 MB of BMAD skill markdown directly into `.claude/skills/` (ADR-0002 §3) committed to git. There is no LICENSE inventory, no SPDX manifest, no `THIRD_PARTY_NOTICES`, and no statement of how MIT attribution is preserved when those files are redistributed as part of this repo. If any single BMAD skill carries a non-MIT dependency (e.g., a CC-BY-SA prompt template), the entire vendored bundle inherits an incompatible obligation that is not detected.

**STAKE-SER-015 [Open-source steward]** — Reproducibility of the BMAD install is asymmetric. ADR-0002 §6 says upgrades are "bump pinned version → run the script → substrate PR," and ADR-0002 §8.4 promises "rollback procedure … `git revert <upgrade-sha>` … vendoring makes the prior state unambiguous." However, the install script (`scripts/install_bmad.sh`) is described as "the pinned BMAD install command" without any constraint that the script be deterministic. A re-run of `install_bmad.sh` at the same pinned version on a different machine, OS, or npm/pip cache may produce a different `.claude/skills/` tree, and there is no checksum gate that catches that drift.

**STAKE-PROC-016 [Open-source steward]** — The Anthropic Python and TypeScript SDKs are mentioned as the dependency `packages/anthropic-client/` consumes (PHASE-3 scope item 1, ADR-0007 §6) but their license, version pinning policy, and upgrade cadence are not specified anywhere. PHASE-3 has no equivalent of ADR-0002's vendoring or smoke-test discipline for the Anthropic SDK; the architecture is internally inconsistent about supply chain rigor between BMAD (vendored, smoke-tested, manifest-diffed) and Anthropic (unmentioned).

**STAKE-CRIT-017 [Future architect, 2029]** — The architecture explicitly forbids semantic search for spec lookup (ADR-0004 §6, §8) on the basis of "the paper" — a citation that is never resolved to a specific publication, DOI, or arXiv ID. ARCHITECTURE.md §2 says "a published result on transformer associative memory (referred to throughout as 'the paper')," and ADR-0004 §0 repeats the same anonymous reference. In three years, no one will know which paper this is, whether it has been retracted, whether its findings have been superseded, or whether the threshold values pinned in `tools/spec_lint/config.yaml` (§4) reflect the paper's actual numbers. This is a load-bearing architectural premise stored as folklore.

**STAKE-SER-018 [Future architect, 2029]** — The phase model assumes strict linear sequencing (`phase-exit` "no REQ from a later phase is `tests-green`" — ADR-0008 §3) and is incompatible with hotfix workflows. If a production bug surfaces in PHASE-5 that requires a fix in PHASE-3's anthropic-client, the gate logic forbids the fix from being merged unless the entire phase chain is re-traversed. There is no exception path for security fixes, no concept of a "patch phase," and no escape hatch other than amending ADR-0008 itself.

**STAKE-SER-019 [Future architect, 2029]** — The hook contract in ADR-0005 §6 is tightly coupled to Claude Code's specific hook names (`PreToolUse(Bash:git commit)`, `PostToolUse(mcp__github__merge_pull_request)`, `Stop`, `SessionEnd`). When Claude Code renames these events (as has happened twice already across Anthropic's tooling history per the amendment log pattern), every hook breaks silently and the push invariant (§10) evaporates. There is no abstraction layer between "the agent harness" and "the traceability runtime"; ADR-0002 amendment 0001 already shows this kind of churn happened once for BMAD.

**STAKE-PROC-020 [Future architect, 2029]** — The "atomic REQ" rule (ADR-0004 §3: "one REQ contains one assertion") combined with append-only-with-supersession (§7) and immutable IDs (§1) creates a guaranteed monotonic spec-file growth. After three years of supersession chains, a single feature's spec file will contain dozens of `status: deprecated` REQs interleaved with the current ones, with no archival mechanism. The "near-duplicate" anti-aliasing rule (§4) will increasingly fire false positives against deprecated REQs, forcing either threshold-loosening (defeating the rule) or manual exclusion lists (defeating the immutability principle).

---

**Summary findings by stakeholder count:**
- Security engineer: 3 (STAKE-CRIT-001, STAKE-CRIT-002, STAKE-SER-003)
- SRE/operations lead: 3 (STAKE-CRIT-004, STAKE-CRIT-005, STAKE-SER-006)
- Compliance auditor: 4 (STAKE-CRIT-007, STAKE-SER-008, STAKE-SER-009, STAKE-PROC-010)
- Cost/finance owner: 3 (STAKE-CRIT-011, STAKE-SER-012, STAKE-SER-013)
- Open-source steward: 3 (STAKE-SER-014, STAKE-SER-015, STAKE-PROC-016)
- Future architect: 4 (STAKE-CRIT-017, STAKE-SER-018, STAKE-SER-019, STAKE-PROC-020)

Total: 20 findings, ≥2 per stakeholder. Severity mix: 6 CRIT, 11 SER, 3 PROC. The architecture is internally consistent at the level it operates (spec discipline, traceability, test purity) but is silent or thin on operational concerns (incident response, observability), security primitives (signing, secret management, supply chain attestation), governance controls (separation of duties, immutable audit storage), and long-horizon maintenance (folklore citations, monotonic spec growth, hook-name coupling).
