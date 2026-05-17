# EDGE2 — edge-case-hunter (sonnet) — Wave 4

**Source transcript:** [`raw-transcripts/EDGE2-agent-af0aa3c13cbacf00d.jsonl`](../raw-transcripts/EDGE2-agent-af0aa3c13cbacf00d.jsonl)
**Sub-agent description:** `Edge-case hunter sonnet permutation`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `af0aa3c13cbacf00d`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke `bmad-review-edge-case-hunter`. Walk every branching path and boundary condition in the architecture documents — flag unhandled cases.

Documents (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md, decisions/ADR-0001 through ADR-0008, phases/PHASE-0 through PHASE-5

Hunt edges in: status transitions (REQ status enum, Tests-Status trailer), phase entry/exit conditions, hook firing windows (suspend/resume, fire-twice, never-fire), trailer combinations (Checkpoint+Bootstrap?), identifier allocation races, cross-reference rot (REQ-ID @ moved path), amendment-log corner cases (concurrent amendments, amendment of amendment), checkpoint commit corners (first-on-branch, between red+green), per-project openspec collisions, match-fail asymmetries (silent-pass vs fail-closed).

REQUIRED OUTPUT:
- IDs prefix `EDGE2-` (CRIT/SER/PROC inline)
- Minimum 15 unhandled edges
- For each: scenario, unhandled branch, location, what breaks
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have enough to perform the full analysis and produce the findings.

---

**EDGE2-CRIT-001**

**Scenario:** Two agents (or two concurrent sessions) both call `tools/spec_lint allocate <domain>` against `openspec/specs/INDEX.yaml` at the same instant on separate branches. Both read the same highest-allocated counter, both write the same next ID (e.g. `REQ-AUTH-0008`), and both commit.

**Unhandled branch:** ADR-0004 §1 says allocation is by "monotonic next-free scan against INDEX.yaml" but specifies no locking or merge-conflict protocol. When both PRs are open simultaneously, CI runs `xref-resolves` and `req-id-immutable` independently per branch — both pass. On merge of the second PR, two distinct REQs share an ID with different bodies. `req-id-immutable` fires only if the ID is *edited*, not if it is *duplicated*.

**Location:** `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §1, §6

**What breaks:** Traceability matrix maps one TEST to two conflicting REQ bodies. Audit output is non-deterministic. The `anti-aliasing` gate may catch it if the bodies are similar enough, but if they cover different domains it will silently pass.

---

**EDGE2-CRIT-002**

**Scenario:** A spec file (e.g. `openspec/specs/auth/login.spec.md`) is renamed or moved to `openspec/specs/auth/signin.spec.md` in the same commit that adds new content. Cross-references in other files still read `REQ-AUTH-0007 @ openspec/specs/auth/login.spec.md`.

**Unhandled branch:** ADR-0004 §2 says cross-references use "ID plus file path" and the `xref-resolves` gate checks that references resolve to existing files. However, the gate only runs on PR diff — it validates that references *in the diff* resolve. It does not walk the *entire repo* for all inbound references to the old path. The gate description says "the set of legal references is enumerable; broken references fail CI" but provides no mechanism to enumerate all inbound references to a renamed file across the repo.

**Location:** `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §2; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §1 (`xref-resolves`)

**What breaks:** After merge, existing documents silently point to a non-existent path. The next PR touching those documents will trigger the gate, but the rot is live on `main` in the interim.

---

**EDGE2-CRIT-003**

**Scenario:** A checkpoint commit (carrying `Checkpoint: true`) lands between the red commit and the green commit for the same test. CI exempts checkpoints from some gates. The `red-before-green` gate (ADR-0005 §4, ADR-0006 §4) walks git history looking for "the same test in a red state" before its green commit. A checkpoint commit in that window has `Tests-Status: none` and the test file exists in the checkpoint (it was a WIP commit of partially written test code that does not yet fail — e.g. it was not yet runnable).

**Unhandled branch:** The history walk of `validate_commit.py` must correctly classify the test state in the checkpoint. There is no definition of how "exists in a red state" is determined when a checkpoint commit contains the test file in a partially-written (non-compilable / non-runnable) form. It may be neither red nor green — the gate has no third classification.

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §4, §7; `openspec/architecture/decisions/ADR-0006-testing-tiers.md` §4

**What breaks:** `red-before-green` may pass (checkpoint exemption), but the spirit of P4 is violated — the test was never actually in a *failing* state in history. Alternatively, the gate may erroneously reject valid commits by treating the unrunnable checkpoint state as "never red."

---

**EDGE2-CRIT-004**

**Scenario:** A `Checkpoint: true` commit is created on a branch where the branch has *no upstream configured* (a freshly created local branch that has never been pushed). The checkpoint hook runs `git rev-list @{u}..HEAD` and then tries to push.

**Unhandled branch:** `@{u}` resolves only when a tracking upstream is configured. If the branch was created locally with no `-u` flag and no prior push, `@{u}` fails with a fatal error (`fatal: no upstream configured for branch`). The checkpoint hook's behavior on this error is not specified — it may abort without pushing, or crash mid-hook, leaving the `session_end` journal event unwritten and the work unpushed at container reclaim.

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6, §7

**What breaks:** On container reclaim, committed work on the branch is lost. The failure mode described in §8 as "mitigated" is not actually mitigated for untracked branches.

---

**EDGE2-CRIT-005**

**Scenario:** The `PostToolUse(Bash:git commit)` hook fires and attempts a fast-forward push. Simultaneously (within the same CI run or a concurrent session), another agent has pushed commits to the same branch (e.g. auto-merge of a dependent PR, or a co-author session). The push fails as non-FF. The hook "aborts with a diagnostic" per ADR-0005 §6 — but the commit already exists locally.

**Unhandled branch:** After the non-FF abort, the locally committed but unpushed state persists. The hook does not retry or fall back to a pull-then-push. The `Stop`/`SessionEnd` checkpoint hook will also fail for the same reason (the upstream has diverged). No mechanism recovers the committed work short of a manual `git push --force` (forbidden) or a `git pull --rebase` (not specified as a hook behavior).

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6, §7, §8

**What breaks:** Committed work is stuck locally with no automated recovery path. The failure table in §8 says this case is "mitigated" — it is not, when both hooks abort on the same non-FF condition.

---

**EDGE2-SER-006**

**Scenario:** The `PostToolUse(Bash:*test*)` hook matches on the glob `*test*` in the bash command string. A developer runs `git stash` (no test substring) — fine. But a command like `git commit -m "attestation ..."` or `clasp push --latest` contains no "test" substring. However, `pytest --collect-only` does match `*test*` through `pytest`. More critically, `cat tests/README.md` also matches `*test*` via `tests`. The hook fires on non-test commands, attempts to parse test output from a `cat` result, and appends a malformed or empty `tests_run` event.

**Unhandled branch:** The glob `*test*` is ambiguous — it matches any bash command containing the substring "test" anywhere in the string, including file paths, arguments, or command names unrelated to test execution. No filtering by exit code or output format is specified.

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §6 (hook table)

**What breaks:** Spurious `tests_run` events pollute the journal. `rebuild.py` reads journals as a source of truth — phantom `new_red[]` or `new_green[]` arrays corrupt the matrix and may trigger false `red-before-green` violations.

---

**EDGE2-SER-007**

**Scenario:** A `Checkpoint: true` commit is the *first commit on a new branch* (the branch was just created and the checkpoint is the only commit diverging from base). The next non-checkpoint commit is expected to "restore P4 compliance" (ADR-0005 §7). But if that next commit carries `Tests-Status: red→green` for a test that exists in the checkpoint commit, `red-before-green` walks history and finds: (1) green commit, (2) checkpoint (Tests-Status: none, exempt), (3) base branch where test did not exist. The test was never explicitly red.

**Unhandled branch:** ADR-0005 §7 says the next non-checkpoint commit is "responsible for restoring P4 compliance either by squash or by ensuring the red/green sequence is recoverable from the full history." There is no gate that mechanically validates this obligation is met, and "recoverable" is undefined — no algorithm is specified for the history walk in this case.

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §7; `openspec/architecture/decisions/ADR-0006-testing-tiers.md` §4

**What breaks:** P4 (red-first) silently violated. The `red-before-green` gate has no documented behavior for the checkpoint-as-first-commit shape.

---

**EDGE2-SER-008**

**Scenario:** The REQ status enum in ADR-0004 §5 lists `draft | tests-red | tests-green | reviewed | merged | deprecated`. ADR-0005 §4 defines transition rules only for the `draft → tests-red → tests-green` path and the `deprecated` terminal. The states `reviewed` and `merged` are listed in the enum but have no defined valid predecessors, successors, or enforcement gates.

**Unhandled branch:** No gate checks that a REQ only transitions `tests-green → reviewed → merged` (or any other valid sequence). A REQ could be set to `merged` directly from `draft` without any test coverage, and no CI gate catches it. Similarly, `reviewed → draft` (a regression) is syntactically valid but semantically forbidden — and there is no gate for it.

**Location:** `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §5; `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §4

**What breaks:** A REQ can reach `merged` state without passing through `tests-red` and `tests-green`. The coverage gate `req-coverage-100` checks for passing tests per REQ, but only for non-deprecated REQs — a REQ at `merged` with no tests may be counted as covered if the gate checks `tests-green` status rather than actual test presence.

---

**EDGE2-SER-009**

**Scenario:** Two PRs targeting `main` both amend the same ADR (e.g. both add amendment rows to ADR-0005's amendment log). PR-A is merged first. PR-B's branch was branched before PR-A merged. PR-B's diff adds its amendment row to the *pre-PR-A* amendment table, which no longer matches the current `main` version after PR-A's merge.

**Unhandled branch:** The amendment log is append-only (ADR-0002 §, ADR-0005 §10: "amendments are append-only... a subsequent change requires a new amendment row, never an edit to a prior row"). There is no gate that validates amendment row sequence numbers are globally monotonic or that concurrent amendment adds are conflict-detected. `git merge` may auto-resolve the table append as a non-conflicting diff if both PRs added rows at the end, silently producing a table with two "Amendment 0002" rows (one from each PR).

**Location:** `openspec/architecture/decisions/ADR-0002-bmad-integration.md` Amendment log; `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §10

**What breaks:** Duplicate amendment sequence numbers in the log. The `req-append-only` gate targets REQ-level appends, not ADR amendment tables. No gate covers ADR amendment integrity.

---

**EDGE2-SER-010**

**Scenario:** PHASE-1 references `ADR-0003-appscript-runtime.md` in its goal section: "Make every rule in ADR-0004 ... ADR-0001, ADR-0002, ADR-0003, ADR-0006, and ADR-0007 mechanically enforced." PHASE-1 scope lists `tools/spec_lint/` as the implementation site. However, the `gas-global-outside-adapter` lint rule enforces ADR-0003 §5 — but ADR-0003 §3 (four test tiers per project), §4 (deployment topology), and the requirement that E2E tests actually run against deployed GAS are not enforceable by a static lint rule alone. No gate in ADR-0008 §1 covers these aspects of ADR-0003.

**Unhandled branch:** The `gate-coverage` meta-gate (ADR-0008 §2) "walks every ADR and every principle ... and verifies that at least one entry in the table references it." The table has exactly one entry for ADR-0003 (`gas-global-outside-adapter`). The `gate-coverage` gate will pass even though ADR-0003's runtime test requirements (§3, §4) have no mechanical gate.

**Location:** `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §1, §2; `openspec/architecture/decisions/ADR-0003-appscript-runtime.md` §3, §4

**What breaks:** A project can exist without any E2E tier implementation, the `gate-coverage` gate passes (because one gate references ADR-0003), and no CI gate enforces the four-tier requirement per project.

---

**EDGE2-SER-011**

**Scenario:** ADR-0006 §4 says bulk green-starts require `Bootstrap: <reason>` and flags commits "adding > N green tests without the trailer." The value of N is not defined in any ADR, phase file, or ARCHITECTURE.md. `tools/spec_lint/config.yaml` is mentioned for the anti-aliasing threshold but not for this N.

**Unhandled branch:** N is an unspecified configuration value. If not pinned before PHASE-2 implementation, the gate implementor chooses N arbitrarily. If N=0, every green test commit requires Bootstrap (breaking ordinary commits). If N=1000, the gate is effectively disabled for all practical batches. There is no ADR amendment or config file defined as the canonical source of N.

**Location:** `openspec/architecture/decisions/ADR-0006-testing-tiers.md` §4; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §1

**What breaks:** The `bulk-green-start` gate either over-triggers or is trivially bypassed, depending on implementor choice. The constraint is unenforced until someone defines N, which is an undefined dependency.

---

**EDGE2-PROC-012**

**Scenario:** The `SessionStart` hook (`tools/trace/resume.py`) fires when a new session begins. The session journal is in `.claude/journal/` (gitignored). After container reclaim, the journal file is gone. The hook must reconstruct state from "journal + active task file + last commit" (ARCHITECTURE.md §8). If the journal is empty (new container) and the last commit's trailers reference `TASK-0042` but `TASK-0042` has been closed/completed in a prior session, the hook prints the wrong "next action."

**Unhandled branch:** The spec says "session resume requires zero human re-briefing" (ARCHITECTURE.md §8) but the resume algorithm is only described at the level of "print active phase, in-flight task, last commit, next action." There is no defined behavior when the task referenced in the last commit trailer is in `task_complete` status (the journal event for which is also lost). The hook may resume a completed task as if it were in-flight.

**Location:** `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §5, §6; `openspec/architecture/ARCHITECTURE.md` §8

**What breaks:** Agent resumes work on a completed task, potentially duplicating work or creating conflicting commits referencing a closed TASK-ID.

---

**EDGE2-PROC-013**

**Scenario:** Per-project specs under `projects/<name>/openspec/` extend root specs "by reference" (ADR-0001). The root `openspec/specs/INDEX.yaml` is the "sole retrieval surface for tooling." However, project-scoped specs live under `projects/<name>/openspec/specs/`, not under `openspec/specs/`. The `index-up-to-date` gate re-generates `openspec/specs/INDEX.yaml` — it is undefined whether this gate also indexes project-scoped specs or only root specs.

**Unhandled branch:** If project-scoped REQs are not in the root INDEX.yaml, they are invisible to `tools/trace/rebuild.py` (which uses the index), `audit.py`, the `req-coverage-100` gate, and the `anti-aliasing` cross-project similarity check. Two projects could define near-duplicate REQs that should be shared — violating P1 (single source of truth) — with no gate catching it.

**Location:** `openspec/architecture/decisions/ADR-0001-monorepo-layout.md`; `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §6; `openspec/architecture/ARCHITECTURE.md` §3

**What breaks:** Project-scoped REQs fall outside all traceability gates. Coverage reports are incomplete. Anti-aliasing never fires across the project boundary.

---

**EDGE2-PROC-014**

**Scenario:** PHASE-0 exit requires all REQ-ARCH-* to be `tests-green` in the matrix. But PHASE-0 also states: "No traceability runtime implementation" and hooks are placeholder exit-0 scripts. The pre-commit hook that re-runs `rebuild.py` is a placeholder. Therefore, when the PHASE-0 tests turn green, the matrix is not automatically updated by the placeholder hook — it must be hand-updated (which is forbidden: "No human or agent may hand-edit it") or not updated until PHASE-2 lands.

**Unhandled branch:** The `phase-exit` gate verifies "exit REQs are all `tests-green` in the matrix." If the matrix is an empty stub (as initialized in PHASE-0 scope item 7: "empty cache") and the rebuild tool doesn't exist yet, the matrix never reflects the green tests. The `phase-exit` gate is itself a PHASE-0 TODO placeholder — so it passes trivially. But this means the transition from PHASE-0 to PHASE-1 has no real enforcement, creating a window where the next phase begins without genuine exit-criteria verification.

**Location:** `openspec/architecture/phases/PHASE-0-foundation.md`; `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §2; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §3

**What breaks:** PHASE-0 exit is self-certifying — the exit gate is a placeholder that always passes, so PHASE-1 can begin regardless of whether REQ-ARCH-* tests are actually green. The constraint is unenforceable until PHASE-2, which is two phases later.

---

**EDGE2-PROC-015**

**Scenario:** A cosmetic edit (typo fix) to a `tests-green` REQ body is permitted only "if no downstream artifact refers to the prior revision body" (ADR-0004 §7). Determining whether any downstream artifact refers to the prior *body* (not just the *ID*) requires comparing the old body text against all downstream references — but downstream artifacts reference REQs by ID + path only, never by body text. No artifact legitimately quotes the REQ body verbatim; the `prose-xref-banned` rule explicitly forbids descriptive references.

**Unhandled branch:** The condition "no downstream artifact refers to the prior revision body" can never be true by violation of `prose-xref-banned`, and is always vacuously true if references are ID-only. This means the cosmetic-edit exemption condition is either always trivially satisfied (any typo fix is always safe) or the condition itself is undefined in terms of what "refers to the body" means when only ID references are legal. The `req-append-only` gate is not defined to distinguish cosmetic from material edits.

**Location:** `openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md` §7; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §1 (`req-append-only`)

**What breaks:** The `req-append-only` gate has no defined algorithm for the cosmetic-edit exception. If it treats all body changes as material, it blocks legitimate typo fixes. If it allows all changes with a `revision` bump, it permits silent material changes to frozen REQs — undermining P4 and the supersession rule.

---

**EDGE2-PROC-016**

**Scenario:** PHASE-5 entry criteria require that "Product side has produced (in a separate PR chain): `openspec/vision.md`, ≥ 1 brief, ≥ 1 PRD section, ≥ 1 Epic with coverage, ≥ 1 Story." The `phase-exit` gate (ADR-0008 §3) checks that "the next phase's entry ADR (if any) is `status: accepted`." PHASE-5's entry criteria include an external dependency (a product PR chain) that is not an ADR and carries no machine-readable status.

**Unhandled branch:** The `phase-exit` gate for PHASE-4 has no mechanism to verify the product-side content exists and is complete. It can only check ADR status. The PHASE-5 entry condition is therefore unenforced by any gate — PHASE-5 can begin without a vision, brief, PRD, Epic, or Story.

**Location:** `openspec/architecture/phases/PHASE-5-first-appscript-project.md`; `openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md` §3

**What breaks:** PHASE-5 begins without product content. The project is built against undefined requirements, producing REQs with no Epic/Story coverage — which immediately fails `req-coverage-100` because REQ frontmatter requires `epic:` and `story:` references (ADR-0004 §5).

---

**EDGE2-PROC-017**

**Scenario:** The `PostToolUse(Edit|Write)` hook fires after every file write. A BMAD skill writes a draft to `openspec/_bmad-output/planning/draft.md`. The hook appends a `file_touch` event to the journal with `path = openspec/_bmad-output/planning/draft.md`. `rebuild.py` reads journals as a truth source and processes `file_touch` events. ADR-0002 §7 says "the matrix MUST NOT reference any path under `openspec/_bmad-output/`" and the "matrix builder excludes the directory unconditionally."

**Unhandled branch:** `rebuild.py` must know to ignore `file_touch` events for paths under `_bmad-output/`. This exclusion is stated for the matrix builder but not for the journal event itself. If `rebuild.py` parses all `file_touch` events before filtering by path, staging paths enter intermediate rebuild state and may be cross-referenced by `task_id` fields — associating a BMAD staging write with a formal TASK, which the matrix should not contain.

**Location:** `openspec/architecture/decisions/ADR-0002-bmad-integration.md` §7; `openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md` §5, §6

**What breaks:** Matrix `rebuild.py` implementation must explicitly filter `file_touch` events by path, but this filter is not specified in ADR-0005. If omitted, staging paths appear in the task-to-file mapping in the matrix, violating the hard invariant in ADR-0002 §7 without any gate catching it (the `matrix-drift` gate only catches drift between committed matrix and rebuilt matrix — it does not validate the rebuild algorithm's exclusion logic).
