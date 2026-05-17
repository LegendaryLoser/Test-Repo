# RED — advanced-elicitation-red-team (opus) — Wave 2

**Source transcript:** [`raw-transcripts/RED-agent-a89a1487164d515d8.jsonl`](../raw-transcripts/RED-agent-a89a1487164d515d8.jsonl)
**Sub-agent description:** `Red-team review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a89a1487164d515d8`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-advanced-elicitation` skill via the Skill tool, then apply its **red-team method** to the architecture artifact below.

Red-team method: take the position of an adversary trying to BREAK the system the architecture defines. You want to:
- Get malicious code merged that the CI gates don't catch
- Bypass the spec discipline (introduce a back-door REQ)
- Drift the BMAD upgrade safeguards
- Corrupt the journal without triggering torn-line discard
- Make `gate-coverage` pass while a critical gate is silently disabled
- Get a commit to main without proper trailers
- Manipulate the matrix in a way `matrix-drift` won't detect
- Exfiltrate API tokens via test artifacts
- Cause silent test-suite degradation that looks like passing

For each attack vector, describe: the attack, the rule it should violate, why the current architecture lets it through, what gate/control would actually prevent it.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

REQUIRED OUTPUT:
- Stable IDs: prefix `RED-` (e.g. RED-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS (severity = blast radius of the attack)
- MINIMUM 12 attack vectors
- 1500-2500 words
- Honest about which attacks are stopped by the current architecture and which leak through
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have all 15 documents. Now producing the red-team report.

---

# Red-Team Findings — OpenSpec / BMAD Architecture Artifact

Scope: `openspec/architecture/ARCHITECTURE.md`, ADR-0001..0008, PHASE-0..PHASE-5. Posture: hostile adversary attempting to break the SoT / spec-discipline / traceability / supply-chain controls the architecture claims to enforce. Each finding cites the rule it should violate, why the current artifact lets it through, and the missing control. Severity = blast radius, not exploit difficulty.

---

## CRITICAL — direct compromise of merged code, trailers, or the source-of-truth chain

### RED-CRIT-01 — Vendored BMAD skill smuggling executable payload through a "substrate" PR
**Attack.** ADR-0002 §3 vendors 2.4 MB of BMAD skill markdown into `.claude/skills/`. Upgrade PRs are explicitly described as "large, expected; mostly vendored skill markdown" (§6) and reviewed by a human who is primed to scroll past the diff. Hide a malicious skill (or amend an existing one) whose instructions tell Claude to exfiltrate `.env` to a webhook, write a back-door spec, or insert a bypass in `tools/trace/`.
**Rule violated.** P1 (SoT) and ADR-0008 §6 (no bypass), since skills become agent behavior.
**Why it leaks.** The only enforcement at upgrade is (a) `skill-removal-acknowledged` (ADR-0002 §8 item 2 — only catches *removals*, not additions or edits), (b) `bmad-smoke-test` (single skill end-to-end — does not scan content), (c) `bmad-version-pin` (matches a version string to a comment — content-agnostic). Nothing diffs skill *content* against an upstream-known-good signature. The "smoke test" exercises one skill; an attacker only has to keep that one clean.
**Missing control.** A `bmad-skill-content-integrity` gate that pins SHA-256 of every file under `.claude/skills/` and `_bmad/` in a signed manifest, regenerated only by `scripts/install_bmad.sh` against an upstream tag verified by GPG. Diffs to skill markdown in a non-substrate PR should fail.

### RED-CRIT-02 — `Bootstrap:` trailer abuse to land a battery of pre-greened tests covering malicious code
**Attack.** ADR-0006 §4 carves out a `Bootstrap: <reason>` trailer that lets a single commit add ">N green tests" if reviewers approve. Drop in fifty trivially-passing tests that import a Trojan module, declare `@covers` against legitimate REQs, and quietly satisfy `req-coverage-100` for a back-door REQ I introduce in the same CHG. Red-before-green is waived; the back door looks fully tested.
**Rule violated.** P4 (red-first) and ADR-0006 §5 (coverage gate intent).
**Why it leaks.** The threshold N is unpinned in the artifact. "Approving review" is a human gate, not a CI gate. There is no `Bootstrap:` audit trail in the matrix and no constraint that bootstrapped tests must come from a vendored test corpus rather than hand-rolled.
**Missing control.** Pin N in `tools/trace/checkpoint_exemptions.yaml`-equivalent; require `Bootstrap:` commits to carry an `Origin: <upstream-sha>` trailer, and have `red-before-green` allow the bypass only when the test files match a known upstream blob hash.

### RED-CRIT-03 — Checkpoint-commit-laundered green
**Attack.** ADR-0005 §7 says `Checkpoint: true` commits are skipped by CI gates and the *next* non-checkpoint commit is responsible for restoring P4 compliance "either by squash or by ensuring the red/green sequence is recoverable from the full history." Land malicious code in a `wip: checkpoint` commit, then immediately squash with a benign final commit that carries a clean trailer — the squashed range now contains green tests with no red predecessor, but `red-before-green` only walks back to the prior non-checkpoint commit and the malicious change reads as a single "make-it-green" landing.
**Rule violated.** P4; ADR-0005 §4 ("a test's first green commit must be preceded by ≥1 commit where the same test exists in a red state").
**Why it leaks.** The "either by squash or by ensuring recoverability" is a disjunction without a CI-checkable predicate. `tools/trace/checkpoint_exemptions.yaml` is referenced in ADR-0008 §6 but its contents are unspecified, so the gate set being skipped is invisible to review.
**Missing control.** Squashes that subsume any `Checkpoint: true` commit must re-prove red-first by retaining the red commit unsquashed, or the squash gate must be in `checkpoint_exemptions.yaml` with explicit, lint-checked enumeration.

### RED-CRIT-04 — Single LLM access point bypass via a "real adapter" that ships its own SDK
**Attack.** ADR-0007 §6 + ADR-0006 §3 both insist the adapter pattern uses "real implementations." Write a `packages/shared-py/adapters/llm-test-rest.py` that calls the Anthropic API directly via `httpx` (bypassing `packages/anthropic-client/`). The lint rule `direct-anthropic-import-banned` (ADR-0007 §6) is described as banning Anthropic *SDK* imports; raw HTTP to `api.anthropic.com` evades it.
**Rule violated.** ADR-0007 §6 (single LLM access point), P1.
**Why it leaks.** The rule's surface is "import statements" only — model-version drift, cache-hit telemetry, and cost budgeting all happen in the client; bypassing the SDK with raw HTTP defeats every downstream gate.
**Missing control.** `direct-anthropic-import-banned` must also forbid HTTP/HTTPS strings matching `api.anthropic.com` (and AWS Bedrock / GCP Vertex Anthropic surfaces) outside `packages/anthropic-client/`.

### RED-CRIT-05 — Pre-receive trailer validation differs from pre-commit, enabling main-branch landings without trailers
**Attack.** ADR-0008 §1 places `commit-trailers-valid` on a *pre-receive hook* (server-side). ADR-0008 §5 places `commit-trailers-valid` *also* pre-commit. Pre-receive hooks are GitHub-flavored: on a *squash-merge* via the GitHub web UI or `mcp__github__merge_pull_request`, the squash commit message is composed by GitHub from the PR title/body and *will not contain the contributor's trailers* unless the merger pastes them. The pre-receive hook is bypassed because the squash is created server-side by the GitHub merge API itself.
**Rule violated.** ADR-0005 §3 (mandatory trailers on every non-checkpoint commit on `main`).
**Why it leaks.** The artifact never specifies *which* merge strategies are allowed. `PostToolUse(mcp__github__merge_pull_request)` (ADR-0005 §6 amendment 0001) only fast-forwards locally; it does not validate the merge commit's trailers.
**Missing control.** Branch protection must (a) require linear history, (b) forbid squash and merge-commits unless a PR-template-driven check verifies the final commit message includes trailers, and (c) `phase-exit` (which runs on merge to main per ADR-0008 §3) must re-validate trailers on the merge SHA itself.

---

## SERIOUS — broad architectural drift or detectable-but-recoverable harm

### RED-SER-06 — Back-door REQ via the staging promotion path
**Attack.** ADR-0002 §7 declares `openspec/_bmad-output/` non-authoritative; `spec_lint` *excludes* it (frontmatter, REQ-ID format, anti-aliasing, cross-reference rules do not apply). Stage a draft containing a REQ that would fail anti-aliasing (a near-duplicate of an existing REQ) or that smuggles a privileged behavior. Promote it via a `docs`-type TASK — a class of task the artifact never spells out lint coverage for. If the promoter's CHG bundles many drafts in a large PR, the anti-aliasing flag will fire only post-promotion; reviewer fatigue and "the lint will catch it" defer the catch. If the promoting commit hides the REQ inside a long file, anti-aliasing's n-gram window may still miss it (threshold is human-tuned, ADR-0004 §4).
**Rule violated.** ADR-0004 §4 (anti-aliasing) and P1 (SoT).
**Why it leaks.** The promotion-time gating is described prose-only; there is no `promotion-diff-review` gate that re-runs spec_lint *and blocks if a REQ appears in the canonical home in this PR for the first time without an explicit `Promoted-From: <staging-path>` trailer*. The "future" `stale-staging` rule is explicitly deferred — drafts can sit indefinitely, accreting trust.
**Missing control.** Promotion-time `promoted-req-attest` gate, plus mandatory promotion trailer surfaced on the matrix.

### RED-SER-07 — Per-project `config.user.toml` is gitignored — privilege escalation channel
**Attack.** ADR-0002 §9 layer 4 is `_bmad/custom/config.user.toml` *gitignored*. A compromised dev machine writes a user-scoped override redirecting `bmm.planning_artifacts` to a writable directory outside `openspec/_bmad-output/`, or pointing planning to a path that collides with canonical artifacts. Because the file is not in git, no review surface exists; only that contributor's session is affected, but their commits land into shared `main`.
**Rule violated.** Implicit invariant in §7 ("matrix MUST NOT reference any path under `openspec/_bmad-output/`"); §9's "isolation" claim.
**Why it leaks.** `config.user.toml` is unauditable by design (it is gitignored), and the resolver merges it with the highest precedence. Nothing at runtime asserts the *resolved* config points at the expected paths.
**Missing control.** A `SessionStart` assertion (next to the resume hook) that computes the resolved BMAD config and refuses to proceed if any output path falls outside the allowlisted staging directories, logging the refusal as a journal event.

### RED-SER-08 — `gate-coverage` passes while a critical gate is silently disabled
**Attack.** ADR-0008 §2 says `gate-coverage` "verifies that at least one entry in the table above references" each ADR/principle. It walks the **table**, not the **implementation**. Rename `tools/trace/validate_commit.py` internally to a stub that `return 0`s on every input, leaving the table row intact. `gate-coverage` is satisfied — the row exists. The actual gate is dead.
**Rule violated.** ADR-0008 self-enforcing claim.
**Why it leaks.** The gate operates on the markdown table as a static text artifact, not on runtime evidence that each named gate (a) ran, (b) returned non-trivial output, (c) actually failed on a known-bad input.
**Missing control.** A `gate-canary` job that, for every gate in the table, runs the gate against a curated bad-input fixture and asserts it *fails*. Renaming a gate to a no-op then trips the canary.

### RED-SER-09 — Matrix-drift evasion via spec-file edits that compensate journal omissions
**Attack.** The matrix is "regenerated from sources." Sources include git, spec files, test annotations, *and* journals. Edit a spec file to flip a REQ from `tests-red` to `tests-green` while *also* hand-deleting the corresponding `tests_run` journal event line (journals are *files* — append-only by convention, not by filesystem). The rebuilt matrix reads the new spec status; without the journal record, no contradicting evidence surfaces. Add a fabricated `commit` event line consistent with the spec edit.
**Rule violated.** ADR-0005 §5 ("append-only JSONL").
**Why it leaks.** Append-only is a *discipline* enforced only at write time by the hook. The journal file has no integrity check (no per-line MAC, no Merkle chain, no hash linking to git). A malicious or buggy editor can truncate or rewrite arbitrary lines. The "torn-line discard" parser is described as ignoring *malformed* lines — well-formed forged lines are accepted.
**Missing control.** Per-line HMAC keyed on `git rev-parse HEAD` at append time, plus a `journal-integrity` CI gate that recomputes and verifies. Optionally hash-chain each line to the previous.

### RED-SER-10 — Token exfiltration through E2E test artifacts on the dedicated test spreadsheet
**Attack.** ADR-0003 §3 runs E2E tests against a real Google Sheet owned by a CI service account, holding GAS bindings. The test writes assertions into the live spreadsheet. A malicious test (or compromised helper in `packages/shared-ts/`) writes the contents of `process.env` (including `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, GCP creds) into a cell. The spreadsheet is shared with the attacker.
**Rule violated.** None explicit — but P3 ("tests exercise real production code") demands real secrets, and the architecture never bounds the blast radius of that real access.
**Why it leaks.** No section in any read document forbids reading env vars from test code, scrubs the spreadsheet between runs against an allowlist of cells, or constrains the CI service account's outbound write surface.
**Missing control.** (a) Tests run with a scrubbed environment containing only test-scoped credentials; (b) `tests-env-scope` lint forbids `process.env`/`os.environ` reads in test files; (c) post-run a `spreadsheet-allowlist` gate diffs the live test spreadsheet against an expected schema.

### RED-SER-11 — Anti-aliasing tunable as a back-door for near-duplicate REQs
**Attack.** ADR-0004 §4 anti-aliasing threshold is in `tools/spec_lint/config.yaml`, "reviewed quarterly." Submit a CHG that adjusts the threshold up by 0.01 — within review fatigue. In the next CHG, land a near-duplicate REQ that would have tripped the old threshold. Both PRs pass `anti-aliasing`.
**Rule violated.** ADR-0004 §4 spirit (catastrophic-forgetting prevention).
**Why it leaks.** Threshold changes are reviewed prose-only; no gate prevents a threshold relaxation from landing without a re-run of the linter on the entire corpus and a report of newly-suppressed pairs.
**Missing control.** A `threshold-change-impact` gate that, when `config.yaml` changes, runs anti-aliasing under *both* old and new thresholds and surfaces the delta set as required PR-description content.

### RED-SER-12 — Silent stochastic-test degradation under cost pressure
**Attack.** ADR-0007 §4 forbids retry-until-pass loops but permits per-test sample size. Drop sample size from 100 to 5 across half the stochastic tests in a "cost-budget" CHG; the cost-budget gate is happy (smaller budget consumed); the statistical assertions still nominally pass but their power collapses. The suite reports green while actually testing nothing.
**Rule violated.** ADR-0007 §3 ("Sample size and threshold are pinned per test"); P2 (statistical assertions).
**Why it leaks.** "Pinned per test" is enforced as *presence* (annotation exists), not as *power*. A reduction in N below a statistically meaningful floor is not gated. No `power-floor` gate exists.
**Missing control.** A `stochastic-power-floor` gate that, given the per-test assertion type and threshold, computes the minimum N required for a given α/β and fails if the pinned N is below the floor.

---

## PROCESS — controls that can be eroded by paperwork drift

### RED-PROC-13 — `Material-Architecture-Change: true` is unmoderated
**Attack.** ARCHITECTURE.md §preamble allows modifications "via an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate." A contributor adds the trailer to a commit that hand-edits ARCHITECTURE.md §3 (top-level layout), then claims the re-gate passed because PHASE-0 tests still pass. The trailer is a self-attestation.
**Rule violated.** ADR-0001 ("no additional top-level directories may be introduced without an ADR").
**Why it leaks.** The trailer is not bound to "an ADR also lands in the same PR" — it's an escape hatch with no second signal. The "Phase-0 re-gate" is a process step, not a gate name in ADR-0008.
**Missing control.** Either remove the trailer escape hatch or require a paired `ADR-Drafted: ADR-<NNNN>` trailer plus the file's actual presence under `decisions/`.

### RED-PROC-14 — `--no-verify` is forbidden by policy, not by mechanism (on contributor machines)
**Attack.** ADR-0008 §6 forbids `--no-verify` "by CLAUDE.md at the agent level and by branch protection at the repository level for `main`." For a human contributor on a feature branch, `--no-verify` skips pre-commit hooks (matrix rebuild, trailer validation). They push; the PR runs CI which re-validates trailers and matrix-drift — but if the contributor also `--no-verify`'d a commit *and* the pre-receive hook is the only server-side trailer enforcement (RED-CRIT-05), and the PR merges via squash, the original trailer-less commit never reaches main but its diff does, and the squash trailer is whatever GitHub generates.
**Rule violated.** P4-supporting hooks intent.
**Why it leaks.** Pre-commit hooks are contributor-local and trivially bypassable. The architecture relies on CI to re-prove, but CI runs against the PR head, not against the commit-by-commit history that `red-before-green` walks.
**Missing control.** Server-side `red-before-green` re-runs against the merge-base..HEAD range of the PR, plus mandatory linear history (no squash) so per-commit trailers are preserved.

### RED-PROC-15 — Phase-exit ordering exploitable when amendments backfill scope
**Attack.** ADR-0002 amendments 0001 and 0002 add behavior to a PHASE-2 deliverable retroactively (e.g., `skill-removal-acknowledged`, push invariants). PHASE-2 is described in PHASE-2-traceability-runtime.md as already covering them, but a contributor can add a new amendment to any ADR *after* its phase has exited, with the implementation deferred to a phase that has not yet started. The `phase-exit` gate verifies "ADR-0001..8 still `accepted`" but does not verify that all amendments' implementation tasks have landed.
**Rule violated.** Implicit: amendments should not bypass phased delivery.
**Why it leaks.** Amendments are append-only at the *document* level (ADR-0002 amendment log; ADR-0005 §10) but the artifact never says amendments must declare their own phase + REQ-IDs and be gated.
**Missing control.** Every amendment row must declare `phase:` and `req_ids:` columns; `phase-exit` must check that each amendment's REQs are tests-green when its declared phase exits.

### RED-PROC-16 — `Skill-Removal-Acknowledged` trailer is per-skill-id, scoped only to removal
**Attack.** Edit an existing skill to be malicious (RED-CRIT-01 is the code-level form; this is the process form). The `skill-removal-acknowledged` gate (ADR-0002 §8 item 2) compares the *manifest* between base and head — it fires only on entries being *removed*. Modify-in-place is invisible to it. Add-then-rename-back across two commits in the same PR is also invisible (manifest unchanged at PR level).
**Rule violated.** ADR-0002 §8 intent ("upgrades safeguarded").
**Why it leaks.** Manifest-diff is necessary-not-sufficient. The four-layer config merge means custom-overrides under `_bmad/custom/` further mutate skill behavior at runtime without any manifest entry at all.
**Missing control.** Manifest must carry per-skill SHA-256; gate compares hashes, not just presence. Custom-override edits trigger a `bmad-custom-override-review` gate that requires a named approver.

---

## Cross-cutting observations

Several attacks compound: RED-CRIT-01 (malicious skill content), RED-PROC-16 (modify-in-place evades manifest diff), RED-SER-07 (gitignored user config redirects outputs), and RED-SER-09 (journal forgery) form a coherent kill chain — an attacker controlling one contributor's machine can plant a malicious BMAD skill, redirect outputs through the gitignored config, and forge journal evidence that nothing happened. The architecture's defense-in-depth depends on `gate-coverage` being a *meta-gate*; RED-SER-08 shows the meta-gate is itself a table-walker with no canary, so the recursion bottoms out at a single point of failure.

Honest summary of what the architecture **does** catch as written:
- Hand-edits of the matrix (`matrix-drift`, RED-SER-09 only succeeds with cooperative journal forgery).
- Prose cross-references (`prose-xref-banned`).
- Renames of REQ IDs (`req-id-immutable`).
- Direct Anthropic SDK imports outside the client (RED-CRIT-04 evades by going lower-level).
- GAS globals outside adapters.
- Bulk green-starts without the bootstrap trailer (RED-CRIT-02 abuses the sanctioned form).
- Removal of BMAD skills without acknowledgment (RED-PROC-16 evades by editing).

What **slips through** as written:
- Skill-content tampering (no integrity gate).
- Trailer enforcement on server-side merge commits (gate-target mismatch).
- Journal forgery (no integrity chain).
- Power degradation of stochastic tests (no floor).
- Threshold relaxation of anti-aliasing (no impact diff).
- Token exfiltration via test artifacts (no env-scope gate).
- Self-attested `Material-Architecture-Change` (no paired-ADR check).
- Gate-stubbing without canary detection (`gate-coverage` is a table walker).

The architecture is unusually disciplined for a greenfield repo, but its enforcement surface is mostly *additive* (every principle has a gate); it lacks *adversarial* gates (gates that verify gates are real, integrity chains over append-only files, content hashes over vendored substrate). Closing the items above would raise the cost of an inside-the-supply-chain attack from "trivially convenient" to "requires sustained social engineering plus key compromise."
