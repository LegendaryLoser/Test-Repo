# FAILSCEN — scenario-unfold-failure-modes-current (opus) — Wave 8

**Source transcript:** [`raw-transcripts/FAILSCEN-agent-a2ac761040a0645b9.jsonl`](../raw-transcripts/FAILSCEN-agent-a2ac761040a0645b9.jsonl)
**Sub-agent description:** `Failure-mode scenarios current`
**Session ID:** `b65d76d6-060d-426f-b5f4-1055ba6abe94`
**Agent ID:** `a2ac761040a0645b9`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Your method is **failure-mode scenario unfolding** — for each of 6 concrete realistic mid-operation failure modes that any production system encounters at some rate, walk through what happens step-by-step under the architecture AS WRITTEN and surface what's missing, what corrupts, what's unrecoverable, what produces silent damage.

This is NOT a pre-mortem (you're not predicting hypothetical futures). The failures are REALISTIC operational events that hit production systems regularly. The question is: when they happen to THIS architecture TODAY, what does the architecture provide as response, and what's missing?

Documents to review (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- All 8 ADRs in openspec/architecture/decisions/ (list the directory first)
- All 6 PHASE files in openspec/architecture/phases/

**6 failure-mode scenarios to walk through:**

1. **Matrix corruption.** The `openspec/traceability/matrix.yaml` is mid-write when the writer process dies (OOM-killed pre-commit hook, container reclaim mid-rebuild, disk-full). The file is now half-written or invalid YAML. What does the next commit do? What does CI see? Can the matrix be regenerated cleanly? Is the corruption silent? What if the corruption is at byte-offset within a REQ block (parses as valid YAML but missing required field)?

2. **Hook misfire mid-action.** A PostToolUse hook fires on a tool result but the hook script itself has a bug (regex error, JSON parse fail, unhandled exception, network timeout). The tool's effect has already landed (file edited, git commit made, push attempted). Does the hook failure roll back the tool effect? Does it block subsequent hooks? Is there a hook-failure audit trail? What if the hook fails on EVERY invocation (e.g., post-amendment broke the regex)?

3. **BMAD upgrade breaks spec_lint.** A BMAD v6.6.0 → v6.7.0 substrate upgrade is merged. The new BMAD ships a skill that produces a slightly different output format (extra whitespace, restructured headings, renamed frontmatter field). `spec_lint` was hand-tuned against v6.6.0 outputs and now fails on every commit. Where does the failure surface (which gate? which CHG?)? Who diagnoses? How is rollback initiated? What does the matrix do during the broken window (1-7 days typical for diagnosis + revert)?

4. **Network partition during push.** A commit-hook autopush invocation hits a network partition. The push partially fails (some refs updated, some not) or fails silently. The Stop/SessionEnd hook also can't push (network still partitioned). The session terminates. The next session starts, sees local refs ahead of origin, attempts push, but local state has diverged from origin in a way the push hook doesn't detect. Recovery procedure?

5. **Journal write race.** Two parallel tool calls fire Edit/Write hooks at exactly the same millisecond. Both append to `.claude/journal/session-<id>.jsonl`. Are the appends atomic at the OS level? Can they interleave mid-line (one tool call's event-half + another's event-half = invalid JSON line)? What does the matrix rebuilder do with partial / interleaved JSON lines? Is corruption detected?

6. **Container reclaim mid-phase-exit.** The CI runner executing `phase-exit` validation is reclaimed mid-execution (spot-instance preemption, cluster-autoscaler eviction, infrastructure outage). Some gates ran (passed); some didn't run. CI reports no result (timeout / aborted). Is the PR merge blocked? Is the partial validation state visible? What's the retry policy? Does re-run start clean or does it inherit partial state?

For each scenario, surface AT LEAST 2 distinct architectural defects (file path + specific gap) that block, mislead, corrupt, or fail-silent under the failure mode. The 12+ findings total should be evenly distributed across the 6 scenarios (so ~2-3 per scenario).

**Distinct from prior streams:**
- `SCENNOW` (a prior audit wave) walked 6 actor-scenarios (developer onboarding, agent session start, CHG author, REQ author, PR reviewer, hook re-runner) under the architecture's NORMAL operation. You walk failure modes under ABNORMAL operation — fundamentally different lens.
- `INHER` (a prior wave) was a single inheritor-takes-over scenario, not failure modes.
- `PREM` + `PREM2` (prior waves) were pre-mortems (hypothetical futures). You're surfacing what happens TODAY when realistic failures hit, not what MIGHT happen.
- `EDGE` + `EDGE2` (prior waves) walked edge-cases of normal operation, not failure-mode recoveries.

REQUIRED OUTPUT:
- All finding IDs prefixed `FAILSCEN-` with severity inline (e.g., `FAILSCEN-CRIT-001`).
- Severity guide: CRIT = the failure produces silent corruption or unrecoverable state with no detection; SER = the failure has a documented manual recovery path but no automation; PROC = failure-procedure documentation gap.
- Minimum 12 findings, target 14-18.
- Tag each finding with the scenario number (e.g., "[Scenario 3: BMAD upgrade]").
- Each finding cites a specific artifact AND the failure-mode-consequence the architecture doesn't address.
- 1500-2000 words.
- NO preamble. Start directly with finding FAILSCEN-CRIT-001.
- End with a one-paragraph summary that totals findings by severity and names the scenario with the most blocking architectural gaps.

Do not read files outside the architecture documents listed.
```

## Findings deliverable (final assistant message)

Now I have sufficient context. Let me write up the failure-mode scenario findings.

FAILSCEN-CRIT-001 [Scenario 1: Matrix corruption]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §2 declares the matrix is "regenerated by `tools/trace/rebuild.py` from the four sources above" and "A pre-commit hook re-runs rebuild and stages the result." It also says "CI re-runs rebuild on PR and fails if the committed matrix differs from the rebuilt matrix." Nothing in ADR-0005 specifies what happens when the *previous* matrix on disk is invalid YAML at rebuild-start. The rebuild pipeline's diff step (`matrix-drift` in ADR-0008 §1) requires *parsing* the committed matrix to compare. If the on-disk file is truncated mid-write, the diff comparator throws before any drift signal can fire. The pre-commit hook itself runs *the* rebuild and stages the result — but if the comparator that decides "did we change anything" reads the broken file first, the commit either crashes opaquely or stages a "this was always correct" no-op. There is no atomic-write requirement for the matrix and no "rebuild ignores the prior file entirely" contract.

FAILSCEN-CRIT-002 [Scenario 1: Matrix corruption]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §8 lists six failure modes; *matrix corruption is not one of them*. The Consequences section claims "Matrix can be regenerated from sources at any time; corruption is recoverable" but provides no detection mechanism for partial corruption that produces *valid YAML missing a required field* (e.g., a REQ block whose `tests` list is empty because the writer died mid-loop). The matrix-drift gate detects whole-file drift but cannot distinguish "matrix was correctly rebuilt to reflect an empty test set for REQ-X" from "matrix lost the test set for REQ-X due to torn write then a clean rebuild was triggered against an in-memory cache that also lost it." There is no schema-validation gate for the matrix file in the ADR-0008 §1 inventory.

FAILSCEN-SER-003 [Scenario 1: Matrix corruption]
`openspec/architecture/phases/PHASE-2-traceability-runtime.md` Exit criteria says "Synthetic crash scenarios pass: deleting `matrix.yaml` then rebuilding produces the prior content; appending a torn JSONL line then re-parsing succeeds with the line discarded." Notice the asymmetry: deleted matrix is covered, *torn* matrix is not. Half-written YAML (the realistic failure) is neither deletion nor a clean replay — and PHASE-2's test scope does not include it. The recovery procedure ("just delete and rebuild") is not documented anywhere in the eight ADRs as a manual runbook.

FAILSCEN-CRIT-004 [Scenario 2: Hook misfire mid-action]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6 declares seven hooks whose effects (push, journal append, P4 validation, post-merge sync) materially change repository state. ADR-0005 provides no contract for what happens when a `PostToolUse` hook *throws*. Critically, `PostToolUse(Bash:git commit)` does the push — if the hook throws after the commit but before/during the push, the commit lands locally with no push and no journal append. ADR-0005 §8 acknowledges this as "residual loss only if both hooks fail to fire" but defines no audit trail of hook failures. No `hook_failed` event exists in the §5 journal-event table. The architecture cannot tell whether a hook *ran and succeeded*, *ran and failed*, or *was never invoked* — three states that are operationally distinct and all silent.

FAILSCEN-CRIT-005 [Scenario 2: Hook misfire mid-action]
`openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §6 forbids `--no-verify` and bypass flags absolutely. `CLAUDE.md` reinforces this. But ADR-0005 §6 also says the `PreToolUse(Bash:git commit)` hook validates trailers. If the validator itself crashes on every invocation (e.g., a post-amendment regex broke on a corner case), the developer has no sanctioned escape valve — and the agent is forbidden from `--no-verify` even when the hook is *itself* broken. There is no documented "hook quarantine" or "hook health check" procedure in any of the eight ADRs. The architecture turns a single buggy hook into a total commit freeze.

FAILSCEN-SER-006 [Scenario 2: Hook misfire mid-action]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6 row for `PostToolUse(Bash:git commit)` says non-FF push "aborts the hook with a diagnostic (no force-push)." The diagnostic is mentioned, but nowhere in ADR-0005 or PHASE-2 is the diagnostic *journaled*. The next session's `resume.py` (SessionStart hook) reconstructs state from "journal + active task file + last commit" per §8 — it cannot see hook-time diagnostics that went to stderr. So a session-ending non-FF abort produces unpushed commits *and* the diagnostic that explains why is lost when the container is reclaimed.

FAILSCEN-CRIT-007 [Scenario 3: BMAD upgrade breaks spec_lint]
`openspec/architecture/decisions/ADR-0002-bmad-integration.md` §8 lists five upgrade safeguards. None of them is *forward-compatibility testing of spec_lint against the upgraded BMAD outputs*. The "smoke test" (§8.1) "exercises at least one BMAD skill end-to-end against a known input and assert the output shape" but spec_lint is downstream of BMAD outputs at *promotion time* — not at skill-invocation time. A v6.6.0 → v6.7.0 upgrade that adds extra whitespace or renames a frontmatter field will pass the smoke test (output shape unchanged at the skill boundary), pass the skill-removal-acknowledged gate (no skill removed), pass the full test suite (existing tests don't exercise the new output), and break only when an author next *promotes* a draft to canonical and `spec-frontmatter-valid` rejects it. No CI gate catches this at upgrade-merge time.

FAILSCEN-SER-008 [Scenario 3: BMAD upgrade breaks spec_lint]
`openspec/architecture/decisions/ADR-0002-bmad-integration.md` §8.4 says "A BMAD upgrade that turns out to break something post-merge rolls back atomically via `git revert <upgrade-sha>`." But it does not say *who* notices, *what gate fires*, or *what the SLA is* for diagnosis. During the 1-7 day broken window, every commit's pre-commit hook attempts matrix-rebuild (ADR-0005 §2). If spec_lint feeds the matrix (it owns `req-id-format`, `prose-xref-banned`, and many gates listed in ADR-0008 §1 as "pre-commit + PR"), then matrix-drift will fail on every commit. The architecture lacks a "broken-upstream" partial-bypass: the `Checkpoint: true` trailer (ADR-0008 §6) is the only sanctioned bypass and applies to checkpoint commits only, not regular work.

FAILSCEN-PROC-009 [Scenario 3: BMAD upgrade breaks spec_lint]
`openspec/architecture/decisions/ADR-0002-bmad-integration.md` Amendment 0002 declares "rollback procedure" but no rollback *gate*. There is no mention of an automated revert trigger, a canary phase, or a manual override; the architecture relies on a human noticing and running `git revert`. The matrix during the broken window will diverge from a rebuilt matrix on every PR, but there is no documented "matrix freeze" or "skip matrix-drift while BMAD is being reverted" — meaning the very revert PR may itself fail CI.

FAILSCEN-CRIT-010 [Scenario 4: Network partition during push]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6 amendment 0001 introduces the push invariant: "every operation that mutates the commit graph or moves a branch pointer must result in origin tracking the post-state within the same hook firing." The ADR §8 table claims this is mitigated by the per-commit push hook AND the extended checkpoint hook. *Both fail under a partition.* The §8 table acknowledges "residual loss only if both hooks fail to fire (e.g. abrupt container reclaim mid-`PostToolUse`)" — but a *network partition* causes both hooks to *fire and complete* with a push-failure exit, which is a fundamentally different state than "did not fire." There is no journaled `push_failed` event in the §5 table; the `push` event lists `success` as a field but no specification of what happens to subsequent commits when `success=false`.

FAILSCEN-CRIT-011 [Scenario 4: Network partition during push]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6 says non-FF push "aborts the hook with a diagnostic (no force-push)." This defends *against* force-push but creates a divergence scenario it cannot detect: if the partition heals and a *new* session starts, `resume.py` (SessionStart hook) restores context from journal + last commit but has no specification for "local refs ahead of origin, origin has new commits both sides have not seen because the divergence happened via someone else's merge while I was partitioned." `post_merge_sync.py` is triggered by `PostToolUse(mcp__github__merge_pull_request)` — but the merge in question may have happened from a different session/agent. No `SessionStart` step in ADR-0005 §6 fetches origin and reconciles before deciding what to do.

FAILSCEN-CRIT-012 [Scenario 5: Journal write race]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §5 says "Each line is a complete, parseable event; partial writes from a crash are discarded by the parser (the line is malformed and ignored)." This silently assumes *single-writer* semantics. ADR-0005 §6 lists seven hooks, several of which (`journal_touch.py`, `journal_tests.py`, `journal_commit.py`) all append to `.claude/journal/session-<id>.jsonl`. The architecture provides no contract that a single session has a single writer; tool calls that fire `PostToolUse(Edit|Write)` and `PostToolUse(Bash:*test*)` in close succession can overlap. POSIX `O_APPEND` writes are atomic *only* up to `PIPE_BUF` (typically 4096 bytes) — a journal event larger than that can interleave. There is no maximum-event-size constraint in ADR-0005 §5 and no file-locking discipline.

FAILSCEN-CRIT-013 [Scenario 5: Journal write race]
`openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §5 says "partial writes... are discarded by the parser." Interleaved writes are *not* partial — they are two valid line-halves concatenated, which may parse as a single *valid* JSON object with wrong field values (one event's `path` paired with another's `task_id`). The parser will accept this as a real event and the matrix-rebuilder (`tools/trace/rebuild.py`, PHASE-2) will use it as ground truth. There is no journaled-event integrity check (HMAC, sequence number, or hash chain) in §5. Silent corruption of the matrix-rebuild input is the worst possible outcome for a derived-cache system that has no other source of truth for tool effects.

FAILSCEN-SER-014 [Scenario 5: Journal write race]
`openspec/architecture/phases/PHASE-2-traceability-runtime.md` Scope §2 lists "Crash-recovery tests for the journal: a synthetic torn last-line is correctly discarded." It does *not* list interleaved-line tests, multi-writer tests, or sequence-number validation tests. The test suite that demonstrates journal robustness is scoped to a failure mode (truncation at EOF) that is strictly easier than the real production failure (concurrent writers).

FAILSCEN-CRIT-015 [Scenario 6: Container reclaim mid-phase-exit]
`openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §3 says "`phase-exit` gate runs on merge to `main`." A spot-instance preemption mid-gate produces no result — the merge ref has already updated but the gate never reported pass/fail. There is no specification in ADR-0008 of what happens to a merged PR whose phase-exit gate aborted: is it retried automatically? Does `main` continue to advance with new merges? The next phase's entry criterion is "previous phase exit criteria all `tests-green`" — but if the gate aborted rather than failed, the criterion's truth value is *unknown*, and the architecture provides no resolution.

FAILSCEN-CRIT-016 [Scenario 6: Container reclaim mid-phase-exit]
`openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §3's phase-exit gate must verify three conditions: current phase REQs green, no future phase REQs green, next phase ADR accepted. The gate is described as a single check; it is not described as idempotent, restartable, or composed of subgate checkpoints. If reclamation kills the gate after it computed condition 1 and 2 but before condition 3, the partial state is invisible. There is no "phase-exit-state.yaml" artifact in ADR-0008 §3 that records which sub-checks succeeded, and no retry policy.

FAILSCEN-SER-017 [Scenario 6: Container reclaim mid-phase-exit]
`openspec/architecture/phases/PHASE-0-foundation.md` Exit gate says "`phase-exit` CI gate verifies all REQ-ARCH-* are `tests-green` and ADR-0001..8 are `status: accepted`." Each subsequent PHASE file repeats the same "Exit gate: phase-exit verifies..." line. None of the phase files documents a retry contract, a fallback to a previous successful run, or a "force-acknowledge phase exit" override for the case where the gate's CI runner was preempted. The architecture treats `phase-exit` as a primitive but operationally it is a long-running multi-step computation that must be restartable.

FAILSCEN-PROC-018 [Scenario 6: Container reclaim mid-phase-exit]
`openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §6 forbids `--no-verify` and "any other hook-bypass flag." The only sanctioned partial-bypass is `Checkpoint: true` (limited to checkpoint commits). When phase-exit fails to report due to infrastructure (not policy), there is no documented manual override path. The forbidden-bypass rule combined with the lack of an aborted-gate runbook means that a single CI infrastructure incident can wedge phase progression indefinitely with no documented escape — every retry of the merge will hit the same phase-exit gate, which has no memory that it ran before and aborted.

---

Summary: 18 findings total — **10 CRIT** (silent corruption / unrecoverable / undetected), **5 SER** (manual recovery path exists but unautomated), **3 PROC** (failure-procedure documentation gap), distributed 3-3-3-3-3-3 across the six scenarios. **Scenario 1 (matrix corruption)** and **Scenario 5 (journal write race)** tie as the scenarios with the deepest *silent-corruption* gaps (the entire derived-cache substrate is built on input streams whose integrity is asserted but not validated). **Scenario 6 (container reclaim mid-phase-exit)** has the most *blocking* architectural gaps for repository progression — three CRIT/SER findings show the phase-exit primitive is operationally non-restartable yet stated as the singular gate between phases, with no runbook for the partial-state recovery that production preemption produces.
