# RED2 — advanced-elicitation-red-team (sonnet) — Wave 4

**Source transcript:** [`raw-transcripts/RED2-agent-a0eb113fde740437e.jsonl`](../raw-transcripts/RED2-agent-a0eb113fde740437e.jsonl)
**Sub-agent description:** `Red-team sonnet permutation`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a0eb113fde740437e`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke `bmad-advanced-elicitation` with the **red-team** method. Adversarial position: a hostile attacker trying to BREAK the system.

Documents under /home/user/Test-Repo/:
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Find attack vectors for: malicious code merge bypassing CI, spec discipline bypass, BMAD upgrade safeguard drift, journal corruption that evades torn-line discard, `gate-coverage` passing while critical gate disabled, commits to main without trailers, matrix manipulation that `matrix-drift` misses, API token exfiltration via test artifacts, silent test-suite degradation, supply chain compromise via vendored substrate.

For each: attack, rule violated, why current architecture lets it through, missing control.

REQUIRED OUTPUT:
- IDs prefix `RED2-` (CRIT/SER/PROC inline)
- Minimum 12 attack vectors
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have sufficient depth to execute the red-team analysis. Let me produce the report.

---

**RED2-CRIT-001 — Checkpoint Trailer Exemption Used to Smuggle Malicious Code Past All Commit Gates**

Attack: An attacker (or compromised agent session) crafts a commit containing modified source code — e.g., an exfiltration backdoor inserted into `packages/anthropic-client/` — and attaches the trailer `Checkpoint: true` to the commit message. Per ADR-0005 §7 and ADR-0008 §6, the `Checkpoint: true` trailer is the "only sanctioned partial-bypass" and exempts the commit from "a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`."

Rule violated: ADR-0008 §6 (bypass discipline); ADR-0005 §7 (checkpoint commits exempt from a subset of gates). ARCHITECTURE.md §1 Principle P3 (tests exercise real production code).

Why current architecture lets it through: The exemption list lives in `tools/trace/checkpoint_exemptions.yaml`, a file in the repo. The architecture does not specify which gates are on the exemption list, how that file is protected from modification, or who audits it. If an attacker modifies `checkpoint_exemptions.yaml` to add `req-coverage-100`, `matrix-drift`, or `red-before-green` to the exempted set, then stages a source-code change in a checkpoint commit, all those gates go silent. The `PreToolUse(Bash:git commit)` hook validates trailers but is a pre-commit hook — it runs locally, and a compromised agent can craft the checkpoint trailer on any commit. The `Stop`/`SessionEnd` hook that produces checkpoint commits only fires at session end, but nothing prevents an agent from manually issuing a commit with `Checkpoint: true` at any point.

Missing control: `checkpoint_exemptions.yaml` must itself be gated (hash-pinned or protected by branch protection); checkpoint commits must be restricted to source-file types (no modifications to `packages/`, `tools/`, or `projects/`); a separate gate must verify that checkpoint commits contain only non-executable artifact changes (journal entries, status fields).

---

**RED2-CRIT-002 — API Token Exfiltration via Stochastic Test Artifacts Logged to Journal**

Attack: A malicious contributor adds a stochastic test that reads the `ANTHROPIC_API_KEY` environment variable (legitimately available to stochastic tests calling the real Anthropic API) and encodes it into a test assertion value — e.g., a schema assertion that happens to match a base64-encoded fragment of the key. The test passes, the journal event `tests_run` appends a `new_green[]` entry with the test ID, and the full API response (containing the exfiltrated data embedded in model output) is logged to `.claude/journal/session-<id>.jsonl`.

Rule violated: ADR-0007 §2 (forbidden patterns in stochastic tests), ADR-0006 §2 (no-mock rule), ARCHITECTURE.md §1 Principle P2.

Why current architecture lets it through: The `stochastic-tier-bans` lint rule in ADR-0007 scans for exact forbidden patterns: `seed=`, recorded fixtures, exact-equality assertions, snapshot tests, retry-until-pass loops. It does not ban reading environment variables (`os.environ`, `process.env`), does not ban embedding env var values in assertion strings, and does not validate that the assertion is actually statistical rather than structurally encoding sensitive data. The journal is gitignored at `.claude/journal/` (per PHASE-0 scope item 11) but the journal runs during CI, and CI logs are typically accessible to contributors. The test itself is real code calling the real API, which satisfies the architecture's own constraints — making it invisible to the no-mock gate.

Missing control: `stochastic-tier-bans` must scan for `os.environ`, `process.env`, and all env-reading APIs; CI must scrub API key patterns from journal output before archiving; a separate secret-scanning gate (the architecture has `run_secret_scanning` in the MCP tool list but no ADR gate for it) must run on journal artifacts.

---

**RED2-CRIT-003 — Supply Chain Compromise via Vendored BMAD Substrate in `.claude/skills/`**

Attack: A BMAD v6.x minor upgrade PR (routine cadence; "v6.x minors land months apart") introduces a modified skill markdown file under `.claude/skills/` that contains a hidden instruction to the Claude Code agent — e.g., a system-prompt injection embedded in a skill's Markdown that instructs the agent to append `--no-verify` to git commands or to exfiltrate the active session's env vars to a URL encoded in the skill body.

Rule violated: ADR-0002 §8 (upgrade safeguards), ARCHITECTURE.md §1 Principle P1 (SoT). CLAUDE.md ("Bypassing any hook" is forbidden).

Why current architecture lets it through: The upgrade safeguards in ADR-0002 §8 consist of: (1) smoke test — exercises one BMAD skill end-to-end; (2) skill-removal acknowledgment — compares `_bmad/_config/skill-manifest.csv` between base and head; (3) full test suite must pass; (4) rollback procedure. None of these controls scans skill Markdown content for prompt-injection patterns. The smoke test exercises the skill's output shape, not its hidden instructions. The skill-removal gate only checks for removed skills, not modified content within existing skills. The `bmad-direct-reference` lint rule checks that no project code imports from `_bmad/`, but `.claude/skills/` is where Claude Code reads skills from, and no lint rule covers that path. Since skills are processed by the Claude Code agent itself, a malicious system-prompt fragment in a skill file bypasses all code-level gates.

Missing control: Upgrade PRs must include a diff-content scan of all `.claude/skills/*.md` files for prompt-injection patterns (instruction overrides, URL exfiltration, git flag manipulation); the smoke test must validate skill behavior under adversarial input, not just happy-path shape; a content-hash manifest for skills must be committed and verified in CI.

---

**RED2-CRIT-004 — `gate-coverage` Passing While a Critical Gate Is Disabled**

Attack: An attacker modifies `.github/workflows/ci.yml` to comment out the job step that runs `req-coverage-100` while leaving the gate listed in the ADR-0008 §1 table untouched. The `gate-coverage` meta-gate "walks every ADR and every principle in ARCHITECTURE.md §1 and verifies that at least one entry in the table above references it." It verifies the table — not that the referenced gate actually runs in CI.

Rule violated: ADR-0008 §2 (gate-coverage gate), ARCHITECTURE.md §1 ("A principle without a CI gate is a build failure").

Why current architecture lets it through: `gate-coverage` is described as verifying references within the ADR-0008 §1 inventory table. There is no stated mechanism by which `gate-coverage` cross-references the actual job definitions in `.github/workflows/ci.yml` or `spec-discipline.yml` against the table entries. The table is a Markdown document; the workflow YAML is a separate file. An attacker who can modify workflow YAML (any contributor with a PR) can disable a gate step while the `gate-coverage` tool continues to see the gate name in the Markdown table and reports clean. This is especially dangerous because the disabled gate could be `red-before-green` (allowing green-only commits) or `matrix-drift` (allowing hand-edited matrix).

Missing control: `gate-coverage` must parse the actual workflow YAML files and verify each gate name in the table appears as an active (non-commented, non-skipped) step or job in the workflow; any discrepancy must fail the build. Workflow files themselves must be protected by branch protection rules requiring code-owner review.

---

**RED2-SER-005 — Journal Corruption That Evades Torn-Line Discard: Multi-Line Valid JSON Attack**

Attack: An attacker with write access to the journal file (or a compromised `PostToolUse` hook that writes events) appends a line that is valid JSONL but contains fabricated traceability data — e.g., a `commit` event with `trailers_valid: true` and `tests_status: "red→green"` referencing a REQ-ID that was never actually tested. The torn-line discard mechanism described in ADR-0005 §5 discards malformed (syntactically broken) lines. A fabricated but syntactically valid JSONL line passes the parser and enters the traceability sources of truth.

Rule violated: ADR-0005 §1 (journal is a source of truth), §5 (torn-line discard), ARCHITECTURE.md §7 (traceability is derived from journals + git + specs + tests).

Why current architecture lets it through: The architecture states "partial writes from a crash are discarded by the parser (the line is malformed and ignored)." This defense targets the crash scenario — a truncated write. It provides no integrity guarantee against a complete, syntactically valid but semantically fabricated line. The journal is gitignored (`.claude/journal/` per PHASE-0 §11) — it is not under git's protection and is not checksummed. `tools/trace/rebuild.py` regenerates the matrix from journals, but if the journal contains a fabricated `commit` event asserting that `TEST-AUTH-0001` turned green for `REQ-AUTH-0007`, rebuild will reflect that, and `matrix-drift` will pass because the committed matrix matches the (corrupted) rebuild.

Missing control: Journal events must be cross-validated against git history — every `commit` event in the journal must have a corresponding git object with matching SHA and trailers; a journal event claiming `trailers_valid: true` for a SHA that doesn't match real git history must be rejected at rebuild time with a hard error. Journal files should be HMAC-signed by the hook that writes them.

---

**RED2-SER-006 — Commits to `main` Without Trailers via `post_merge_sync.py` Fast-Forward Push**

Attack: The `PostToolUse(mcp__github__merge_pull_request)` hook runs `post_merge_sync.py`, which fetches origin and fast-forwards the working branch, then pushes. This push is a direct push to origin, not a PR. If the fast-forward produces a new commit object (e.g., merge commit on origin) that lands on the working branch without having been validated by `validate_commit.py` on the agent's side, that merge commit bypasses the `PreToolUse(Bash:git commit)` hook entirely — the agent never issued a `git commit` command; the commit was created by GitHub's merge machinery.

Rule violated: ADR-0005 §3 (mandatory commit message trailers), ADR-0008 gate `commit-trailers-valid`.

Why current architecture lets it through: `commit-trailers-valid` runs as a pre-receive hook (ADR-0008 §5), but a pre-receive hook on GitHub must be configured as a server-side hook or enforced by a branch protection rule requiring a status check. The architecture declares `commit-trailers-valid` runs "pre-receive" but the actual CI gate in `.github/workflows/` only runs on PRs. GitHub merge commits (squash, merge, rebase merge) are created by GitHub's backend and bypass local pre-commit hooks entirely. The `post_merge_sync.py` hook then fast-forwards and pushes — but it does not re-validate the merge commit's trailers before pushing. Merge commits to `main` will consistently lack `Task:`, `Requirements:`, `Tests-Status:`, and `Phase:` trailers.

Missing control: `post_merge_sync.py` must validate the trailer block of the fetched merge commit before fast-forwarding; if trailers are absent, the hook must refuse the sync and emit a diagnostic requiring manual intervention; alternatively, GitHub branch protection must be configured to require the `commit-trailers-valid` check on direct pushes, not only on PR contexts.

---

**RED2-SER-007 — Matrix Manipulation That `matrix-drift` Misses: Staging Directory Laundering**

Attack: An attacker creates a spec file under `openspec/_bmad-output/` (the staging area) containing real REQ-ID format blocks that claim `status: tests-green`. Because ADR-0002 §7 and PHASE-2 explicitly state that "the matrix builder MUST exclude `openspec/_bmad-output/` from index/matrix construction," `rebuild.py` never processes these files. But if `spec_lint` also excludes the staging directory from canonical checks (as stated: "spec_lint rules MUST exclude `openspec/_bmad-output/` from canonical checks"), then a near-duplicate REQ in staging that shadows a real REQ in canonical space is invisible to `anti-aliasing` lint, invisible to `req-id-format` lint, and invisible to `matrix-drift`. An agent that reads staging content (e.g., during BMAD output review) may treat the staging REQ's `status: tests-green` as authoritative, driving incorrect state transitions.

Rule violated: ADR-0002 §7 (staging hard invariants), ADR-0004 §4 (anti-aliasing), ARCHITECTURE.md §1 Principle P1 (single source of truth).

Why current architecture lets it through: The exclusion of `openspec/_bmad-output/` is a double-edged sword — it correctly prevents phantom REQs from entering the matrix, but it also prevents lint rules from detecting staging content that directly contradicts or aliases canonical content. No control is described that scans staging content for REQ-ID collisions with canonical space. The "stale-staging" gate is explicitly deferred to a future CHG and is not yet a CI gate. An agent operating from a session resuming at a staging-heavy state may read staging REQ data and act on it as if it were canonical.

Missing control: A cross-space collision detector must run on every PR: scan staging for REQ-ID strings that duplicate IDs already in `openspec/specs/`; flag any staging file whose REQ-IDs overlap with canonical space as a build failure. The `stale-staging` gate must not remain deferred — it is a correctness gate, not a hygiene gate.

---

**RED2-SER-008 — Silent Test-Suite Degradation via `@covers` Annotation Drift**

Attack: A developer refactors a test file and — accidentally or maliciously — changes the `@test-id` or `@covers` annotation to reference a deprecated REQ or a non-existent REQ-ID. The test continues to pass (it still exercises the code); only its traceability claim changes. `rebuild.py` parses annotations and builds the matrix from them. `req-coverage-100` then reports that the original REQ (which the test formerly covered) now has zero covering tests and fails CI — but only if the original REQ is still `tests-green` in the matrix. If the attacker simultaneously sets the REQ status to `deprecated` in the spec file in the same PR, the `req-coverage-100` gate skips deprecated REQs, and the formerly-covered behavior now has no test, no REQ, and no CI failure.

Rule violated: ADR-0005 §4 (status transition rules — "a REQ marked deprecated may not be re-activated"), ADR-0006 §5 (REQ coverage 100%), ADR-0004 §7 (append-only at assertion level).

Why current architecture lets it through: The `req-append-only` gate checks that REQ blocks are append-only — it blocks deletion. But the deprecation path is explicitly permitted: a REQ goes to `deprecated` status through the status transition rules. Nothing prevents a valid deprecation of a REQ that still has an active, passing test — the architecture only prohibits the reverse (re-activating deprecated REQs). The `red-before-green` gate validates the red/green sequence for tests that are turning green; it does not validate that a currently-green test is being illegitimately severed from its REQ by deprecating the REQ while the test still passes.

Missing control: Any PR that deprecates a REQ must demonstrate that all tests previously annotated with `@covers <REQ-ID>` have been updated or explicitly retired (via `@test-id` removal); `validate_commit.py` must check that no `tests-green` REQ transitions to `deprecated` in the same commit that removes its covering test annotations, without a corresponding `Bootstrap: <reason>` trailer and explicit reviewer approval.

---

**RED2-SER-009 — BMAD Upgrade Safeguard Drift: Smoke Test Scope Collapse**

Attack: The BMAD smoke test `tools/ci/smoke_bmad.py` is a PHASE-2 deliverable that "exercises at least one BMAD skill end-to-end against a known input." Over time, as BMAD upgrades happen, the smoke test continues to exercise the same single skill (e.g., `bmad-help` or a simple document skill). A malicious BMAD upgrade modifies a higher-risk skill (e.g., `bmad-dev-story`, which drives code implementation) while the smoke test only exercises a benign skill. The `skill-removal-acknowledged` gate checks for removed skills but not for modified skill behavior. The full test suite (`P3 discipline — every PR runs the full test suite`) catches regressions in project code that uses BMAD output, but does not catch changes to BMAD skill instructions that alter agent behavior without breaking existing tests.

Rule violated: ADR-0002 §8 (upgrade safeguards, specifically safeguard #1 smoke test and #3 full test suite), ARCHITECTURE.md §1 Principle P5 (BMAD for workflow — a hijacked BMAD skill introduces a parallel convention by altering the workflow surface).

Why current architecture lets it through: Safeguard #1 specifies "at least one BMAD skill end-to-end" — the minimum. The architecture does not specify which skill, nor require coverage of high-risk skills. The smoke test scope is entirely up to the PHASE-2 implementation author and can collapse to the cheapest possible assertion. The compatibility statement requirement (safeguard #5) only covers "spec-format migrations," not behavior changes. No gate compares skill instruction content between versions; the `skill-removal-acknowledged` gate only fires on removals.

Missing control: The smoke test must be parameterized to cover all skills in `_bmad/_config/skill-manifest.csv` in rotation (at minimum, all skills that were touched in the upgrade diff); a diff-based content-change gate must flag any skill whose Markdown body changed in an upgrade PR and require explicit `Skill-Behavior-Changed: <skill-id>` acknowledgment in addition to the removal acknowledgment.

---

**RED2-PROC-010 — Malicious Code Merge via Spec Discipline Bypass: `openspec/_bmad-output/` Promotion Without CHG**

Attack: An attacker places production code — not spec content — inside `openspec/_bmad-output/` under a convincing directory name (e.g., `openspec/_bmad-output/implementation/packages/anthropic-client/src/client.ts`). Since `openspec/_bmad-output/` is excluded from `spec_lint` canonical checks and excluded from the matrix builder, the file is invisible to all lint and traceability gates. The attacker then opens a PR that moves this file to its canonical location `packages/anthropic-client/src/client.ts` via a rename — framing it as a "promotion" in the PR description. The promotion commit has normal trailers and a plausible TASK reference. The diff reviewer sees a rename from staging, which appears routine (promotion is the documented workflow). The actual malicious code in the file is not the subject of any failing test (it was never red-first, because staging is excluded from all gates).

Rule violated: ADR-0002 §7 (promotion is a `docs`-type TASK — but the architecture does not restrict promotion to docs-type content only), ADR-0006 §4 (red-first P4 — the test for the promoted code was never in a failing state), ARCHITECTURE.md §1 Principle P4 (red-first).

Why current architecture lets it through: The promotion protocol in ADR-0002 §7 states promotion is "a `docs`-type TASK under an explicit CHG" but does not restrict the content type that may be promoted. Code files under `openspec/_bmad-output/` are not a lintable defect (lint excludes the directory). The `red-before-green` gate validates red/green sequences for tests already in canonical space; a newly promoted source file that has never had a red test never triggers the gate because there is no prior commit with a red test to validate against. The gate only validates test-status transitions in git history, not the absence of a prior red test for new files.

Missing control: Promotion commits must be restricted to Markdown spec files, YAML artifacts, and planning documents (content type allowlist enforced by a lint rule on promotion commits); any PR that introduces a new file under `packages/`, `projects/`, or `tools/` without a prior commit containing a red test for that file must be blocked by an extended `red-before-green` rule that also covers new-file introductions, not just test-status transitions.

---

**RED2-PROC-011 — `red-before-green` Gate Circumvention via `Bootstrap:` Trailer Abuse**

Attack: ADR-0006 §4 states that "Bulk green-starts (e.g. importing a battery of passing tests in one commit) require a `Bootstrap: <reason>` trailer and an approving review; CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." An attacker adds exactly `N` (the threshold) green tests per commit, spread across multiple commits in a PR, each commit staying below the bulk threshold. Each commit adds `N-1` passing tests that cover newly written production code, all without a prior red commit. The `red-before-green` gate validates per-test whether a prior red commit exists, but if the tests are brand new (no prior history), there is no prior state to compare against — the gate can only detect a transition from red to green, not the absence of a prior red state.

Rule violated: ADR-0005 §4 (red-before-green P4), ADR-0006 §4 (red-first), ARCHITECTURE.md §1 Principle P4.

Why current architecture lets it through: `tools/trace/validate_commit.py` "walks git history to verify" the red-before-green sequence. Walking history for tests that have never appeared in history before produces empty results — there is no prior red state, so the validation trivially passes. The `bulk-green-start` gate threshold `N` creates a bright-line evasion: stay under `N` and the gate is silent. The architecture does not state that a test's first appearance must be in a red state; it states that a test's first *green* commit must be preceded by a *red* commit. If the test is introduced in a green state in its very first commit, and stays below the bulk threshold, both `red-before-green` and `bulk-green-start` are satisfied by vacuous truth.

Missing control: `validate_commit.py` must treat a test's first appearance in any state other than red as a violation (the test must appear in a red-state commit before it may appear in a green-state commit); a "first-appearance gate" that flags any test annotation appearing for the first time in a green state, without a `Bootstrap:` trailer, must be added as a distinct gate entry in ADR-0008 §1.

---

**RED2-PROC-012 — Spec Discipline Bypass via Prose Cross-Reference in Non-Architecture Files**

Attack: The `prose-xref-banned` lint rule fires on "patterns that name an artifact by description instead of by stable ID + path." ADR-0004 §2 gives examples: "the auth spec," "the login requirement," "the original ADR." An attacker adds a spec file in `openspec/specs/<domain>/` that uses a prose cross-reference such as "per the requirement introduced in Phase 3" — a reference that is not an ID+path but also does not match any of the example patterns. The lint rule's pattern set is finite and example-driven; a paraphrase of the banned patterns that has the same semantic effect but different surface syntax evades the rule.

Rule violated: ADR-0004 §2 (cross-reference discipline), ARCHITECTURE.md §1 Principle P1 (SoT — a prose reference breaks the deterministic lookup chain).

Why current architecture lets it through: The `prose-xref-banned` rule is described as firing "on patterns such as" the listed examples — the "such as" is a signal that the pattern set is illustrative, not exhaustive. There is no formal grammar for what constitutes a valid cross-reference; the rule is a heuristic pattern matcher. A sufficiently novel paraphrase escapes detection. Additionally, `prose-xref-banned` explicitly applies to files under `openspec/architecture/` (as per the context), but ADR-0004 §2 scopes it to "illustrative prose references" generally. If the lint rule only covers architecture files and not `openspec/specs/<domain>/` files, spec files themselves are unprotected from prose cross-references.

Missing control: The `prose-xref-banned` rule must be inverted: rather than maintaining a blocklist of prose patterns, it must maintain an allowlist of valid cross-reference forms (the `REQ-X-NNNN @ path` format and its variants), and flag any cross-reference that does not match the allowlist; this positive grammar approach is exhaustive by construction. The rule must be verified to apply to all files under `openspec/` including `openspec/specs/`, not only `openspec/architecture/`.

---

**Summary Table**

| ID | Severity | Category | Core Exploit |
|---|---|---|---|
| RED2-CRIT-001 | CRIT | Gate bypass | Checkpoint trailer on source code commits neutralizes all gates |
| RED2-CRIT-002 | CRIT | Exfiltration | API token embedded in stochastic test output → journal |
| RED2-CRIT-003 | CRIT | Supply chain | Prompt injection in vendored BMAD skill Markdown |
| RED2-CRIT-004 | CRIT | Gate bypass | `gate-coverage` verifies table, not actual workflow job execution |
| RED2-SER-005 | SER | Integrity | Valid JSONL fabrication evades torn-line discard |
| RED2-SER-006 | SER | Trailer bypass | Merge commits from GitHub bypass local PreToolUse hook |
| RED2-SER-007 | SER | Matrix corruption | Staging REQ-IDs shadow canonical space, invisible to all lint |
| RED2-SER-008 | SER | Degradation | Deprecating a REQ silently removes passing test coverage |
| RED2-SER-009 | SER | Drift | BMAD smoke test scope collapses to trivial skill over time |
| RED2-PROC-010 | PROC | Promotion abuse | Code smuggled via staging, promoted without red-first history |
| RED2-PROC-011 | PROC | Gate evasion | Sub-threshold green-start commits evade `red-before-green` |
| RED2-PROC-012 | PROC | Lint evasion | Novel prose cross-reference paraphrase evades pattern blocklist |
