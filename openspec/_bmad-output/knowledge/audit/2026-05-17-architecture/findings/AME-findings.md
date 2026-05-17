# AME — persona-amelia (sonnet) — Wave 2

**Source transcript:** [`raw-transcripts/AME-agent-ae7dabd92bf0ef542.jsonl`](../raw-transcripts/AME-agent-ae7dabd92bf0ef542.jsonl)
**Sub-agent description:** `Amelia dev implementability critique`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `ae7dabd92bf0ef542`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-agent-dev` skill via the Skill tool to load Amelia, the BMAD senior software engineer persona. Then, AS Amelia, evaluate the architecture artifact from a pure implementability standpoint.

This is NOT an interactive conversation. Load the persona, then immediately produce Amelia's report as a single output.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Amelia's perspective is: "I am the engineer who has to write this code. Can I?"

Focus areas:
- Are the tools, schemas, hooks, and gates specified concretely enough to implement?
- Where would I need to invent a contract because the architecture doesn't pin it?
- Where would I need to make a guess that could go two ways with no way to know which is right?
- Where would my implementation pass the gate but produce wrong behavior because the gate's contract is loose?
- Where are the architecture's prescriptions in tension with practical engineering (e.g., the no-mock rule colliding with stateful test resources)?
- What would I beg the architect to clarify before writing a single line of code?
- What architectural decisions would push me into bypassing them (--no-verify, fake adapters, etc.)?

REQUIRED OUTPUT:
- Stable IDs: prefix `AME-` (e.g. AME-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Speak in first-person as Amelia ("I would have to invent...", "If I implement ADR-0005 §6 literally, the hook will...")
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have all 15 documents. As Amelia, I'll produce the implementability review.

---

**AME-CRIT-01 — The `PreToolUse(Bash:git commit)` hook pattern is un-implementable as specified**

ADR-0005 §6 registers a `PreToolUse(Bash:git commit)` hook for `tools/trace/validate_commit.py`. Claude Code's hook system fires `PreToolUse` on the tool name, not on a substring of the Bash command argument. I would have to intercept every `Bash` tool call and pattern-match the invocation string to detect `git commit`. The architecture nowhere specifies what the hook receives as input — what JSON shape, which environment variables, whether the full command string is available. If I implement this hook and the runtime only passes the tool name `Bash`, I cannot distinguish `git commit` from `git status`. I would have to invent that contract entirely. This is the foundation of P4 enforcement; if I get it wrong, `red-before-green` silently never fires.

**AME-CRIT-02 — `PostToolUse(Bash:*test*)` glob matching is unspecified**

ADR-0005 §6 registers `PostToolUse(Bash:*test*)` for `tools/trace/journal_tests.py`. The architecture assumes Claude Code supports glob matching on Bash command strings within `PostToolUse`. I have no specification of whether `*test*` is a shell glob, a regex, a substring match, or a literal tool-name pattern. If the hook system matches only on the literal tool name `Bash`, this hook never fires. If it fires on every Bash call and I parse the command string, I need to decide: does `pytest` count? Does `npm run test:unit` count? Does `jest --coverage` count? The architecture says "parse test results" but does not specify the parser contract: which output formats (TAP, JUnit XML, pytest's stdout)? I would have to invent parsers for an open-ended set of test runners with no guidance.

**AME-CRIT-03 — `PostToolUse(Edit|Write)` pipe syntax is undocumented**

ADR-0005 §6 uses `PostToolUse(Edit|Write)` — an alternation syntax I cannot find documented anywhere in the architecture. The architecture never tells me whether `|` is a valid separator in hook event names, whether this registers two separate hooks or one with a union trigger, or whether the runtime even supports this form. If I write two separate entries and the runtime deduplicates by key, I lose one. If the pipe is invalid YAML, the settings file won't parse and no hook fires at all. PHASE-0 requires `.claude/settings.json` to declare these hooks, but the exact syntax for the JSON structure is nowhere specified. I would have to guess at the schema.

**AME-CRIT-04 — `tools/trace/validate_commit.py` must walk git history to enforce P4, but it runs pre-commit**

ADR-0005 §4 says `validate_commit.py` "walks git history to verify" red-before-green. It runs as a `PreToolUse(Bash:git commit)` hook — i.e., before the commit is made. At that point the new commit does not yet exist in history. The script can inspect existing history and the staged diff, but it cannot know whether the tests being introduced are currently red without running them. The architecture says nothing about how the validator detects "this test is new and currently failing." I would have to invent: scan the staged diff for new `@test-id` annotations, then check whether those tests appear anywhere in history with a `tests-red` status. But the test results aren't in the commit message at pre-commit time — they're in the `Tests-Status:` trailer the author writes by hand. The validator cannot verify the trailer is truthful without actually running the tests. A gate that can be satisfied by lying is not a gate.

**AME-CRIT-05 — The no-mock rule collides directly with GAS V8 unit testing**

ADR-0006 §2 says unit tests "run on Node" and use "non-GAS real adapters." ADR-0003 §2 says "Node unit tests inject a real adapter (e.g. a Sheets adapter that hits a dedicated test spreadsheet via the Sheets REST API)." But the architecture also says these are `tests/unit/` — not `tests/integration/`. The accepted categorization in ADR-0006 §1 says `integration` is "Real Sheets/Drive/HTTP via REST." If the unit-tier adapter hits a real Sheets REST endpoint, it is by definition integration. The architecture has placed a real-network-call adapter in a tier defined by its absence of real network calls. I cannot satisfy both the no-mock rule and the tier boundary simultaneously. Every test I write for a GAS-touching module will be either a mock (forbidden) or an integration test wearing a unit-test label (inconsistent with the matrix's tier field and ADR-0006's own coverage gate). The `req-coverage-100` gate would reject a `tier: unit` REQ satisfied only by an integration-style test.

**AME-CRIT-06 — The `phase-exit` gate blocks out-of-order phase completion, but PHASE-0's red tests for REQ-ARCH-* cannot be tests-green until PHASE-2 infrastructure exists**

PHASE-0 requires tests for REQ-ARCH-* to be written red-first and turn green as scaffolding completes. The `phase-exit` gate (ADR-0008 §3) runs on merge to main and verifies that exit REQs are `tests-green` in the matrix. The matrix rebuild (`tools/trace/rebuild.py`) is a PHASE-2 deliverable. There is no matrix runtime in PHASE-0 or PHASE-1. PHASE-0's tests live in `tools/ci/tests/test_phase0.py`, but the matrix they would populate doesn't have a functioning builder until PHASE-2. The `phase-exit` gate reads the matrix. If rebuild doesn't run, the matrix stays empty and `tests-green` is never recorded for REQ-ARCH-* entries, so PHASE-0's own exit gate can never pass. I would have to either hand-edit the matrix (explicitly forbidden) or bootstrap a minimal rebuild before PHASE-2, which is out-of-scope. This is circular dependency at the foundational level.

**AME-CRIT-07 — Commit trailer validation requires PHASE-2 hooks, but commit trailer discipline is required from PHASE-0**

ADR-0005 §3 mandates commit trailers on every commit from PHASE-0 onward. CLAUDE.md states this is required from the start. The `commit-trailers-valid` gate is implemented in PHASE-2. In PHASE-0 and PHASE-1, the hook is a placeholder that exits 0 (per PHASE-0 §9: "placeholder commands that exit 0 with a TODO comment"). That means for two entire phases, every commit can have malformed or absent trailers and no gate fires. When PHASE-2 arrives and the real validator activates, it "walks git history" (ADR-0005 §4) — which now contains history that was never validated. The architecture does not specify what happens to those commits: do they fail the gate retroactively? Is there a `Bootstrap: <reason>` exemption for pre-PHASE-2 history? I have no answer; I would have to invent an exemption policy.

---

**AME-SERIOUS-01 — `anti-aliasing` threshold and n-gram parameters are deferred to a file that doesn't exist yet**

ADR-0004 §4 says the n-gram similarity threshold and n-gram size are "pinned in `tools/spec_lint/config.yaml`." That file is a PHASE-1 deliverable. The architecture gives me no starting values. When I implement the `anti-aliasing` lint rule, I have no way to know what threshold to write. Too tight and every pair of requirements fires; too loose and near-duplicate specs slip through. The whole point of the rule is to catch δ-convex lures, but the threshold that makes it effective is the parameter the paper's result depends on. The architecture's answer — "reviewed quarterly" — tells me the threshold matters a lot and gives me nothing to seed it with.

**AME-SERIOUS-02 — `compound-requirement-detector` heuristic is completely unspecified**

ADR-0004 §3 says atomicity is enforced by "spec-lint heuristic `compound-requirement-detector`." It gives one clue: "a REQ that decomposes into more than one Given/When/Then is a defect." But the heuristic must operate on text, not on the TEA decomposition output, because lint runs on the spec files, not on TEA session logs. I would have to invent a text heuristic — keyword detection for "and," "or," conjunction patterns — with unknown false-positive and false-negative rates. The architecture calls this a gate, meaning it blocks PRs. I would be implementing a gate whose contract is "heuristic" with no spec on what makes a detection valid.

**AME-SERIOUS-03 — `tools/trace/rebuild.py` source-of-truth ordering is ambiguous when sources conflict**

ADR-0005 §1 lists four sources of truth "ordered." But the ordering is for precedence when sources conflict, and the architecture never defines a conflict resolution rule. If a test annotation says `@covers REQ-X-0001` but the spec file says `REQ-X-0001` is `status: deprecated`, which wins? If a commit trailer says `Tests-Status: green` but the test runner result in the journal says `failed: 1`, which does rebuild use for REQ status? I would have to invent conflict resolution logic that, if wrong, produces a matrix that passes `matrix-drift` but misrepresents actual coverage state. The gate would pass, the behavior would be wrong.

**AME-SERIOUS-04 — `PostToolUse(Bash:git commit)` push invariant creates a force-free push requirement against concurrent CI**

ADR-0005 §6 says `journal_commit.py` pushes HEAD to origin as a fast-forward and "aborts on non-FF with a diagnostic." In a workflow where a PR is open and CI is running, a concurrent push to the same branch (e.g., a GitHub Actions bot updating branch protection state, or another session) would make the local HEAD non-FF relative to origin. The hook aborts with a diagnostic — but the commit already happened. The work is committed locally but not pushed. PHASE-2's tests are required to cover "commit-without-push" scenarios (PHASE-2 §2), but the architecture does not tell me how the hook's diagnostic causes the session to recover. Does it retry? Does it require human intervention? Does the `checkpoint.py` hook pick it up? The recovery path is unspecified.

**AME-SERIOUS-05 — The stochastic tier's "distributional assertions over N runs" has no definition of N**

ADR-0007 §3 permits "Sample size declared; assertion is a confidence interval, K–S test, or similar. Sample size and threshold are pinned per test." No guidance is given on minimum N, acceptable alpha levels, or how to handle the economics of N calls per test in CI. The `cost-budget` annotation exists, but I would need to decide: does N=3 give statistical power? N=30? For a K–S test with meaningful power against a 10% distribution shift, N is typically in the hundreds. At PHASE-3 I would be writing the first stochastic tests with zero guidance on what constitutes a statistically adequate sample. Whatever N I choose becomes the precedent all future tests follow.

**AME-SERIOUS-06 — `bmad-smoke-test` in PHASE-2 tests "one BMAD skill end-to-end" but the output contract for skills is undefined**

ADR-0002 §8 and PHASE-2 §4 require `tools/ci/smoke_bmad.py` to "exercise at least one BMAD skill end-to-end against a known input and assert the output shape." BMAD skills are markdown-driven LLM workflows. Their outputs are natural-language documents. The architecture says "assert the output shape" but gives no schema, no invariant, and no definition of what "shape" means for a BMAD skill output. I would have to define the assertion contract myself — but if the assertion is too loose (file exists, non-empty), the smoke test provides no real safety. If it's too tight (structural checks against the markdown), it becomes brittle to BMAD version bumps, defeating the upgrade safeguard purpose.

**AME-SERIOUS-07 — REQ-ARCH-0008 declares hooks as exit criteria for PHASE-0, but the hook declaration schema is not specified**

PHASE-0 exit criterion REQ-ARCH-0008 states `.claude/settings.json` "declares all hooks from ADR-0005 §6." The test for this lives in `tools/ci/tests/test_phase0.py` and runs without phase-1+ infrastructure. That test must parse `settings.json` and verify hooks are declared. But the architecture nowhere specifies the JSON schema for hook declarations in `settings.json`. What key path holds the hooks? Is it `{"hooks": [{"event": "...", "command": "..."}]}` or something else? The test I would write to verify REQ-ARCH-0008 must hardcode an assumed schema. If the schema is wrong, the test is testing a fictional contract.

**AME-SERIOUS-08 — `xref-resolves` gate scope is ambiguous across ADR and spec files**

ADR-0004 §2 says "the set of legal references is enumerable; broken references fail CI" and `xref-resolves` checks cross-references. ARCHITECTURE.md §4 says cross-references use "ID plus file path." But ADRs themselves cross-reference each other by relative path (e.g., `[ADR-0004](ADR-0004-spec-storage-discipline.md)`), and spec files cross-reference ADRs in the `references.adrs` frontmatter field as bare IDs (`[ADR-0003]`). The `xref-resolves` rule must handle at minimum three forms: Markdown link with relative path, bare ID in YAML array, and prose reference (which is supposed to be banned but may appear in prose sections). The architecture says the rule "resolves" references but gives no grammar for what constitutes a reference token that requires resolution. I would have to reverse-engineer the full cross-reference syntax from examples.

---

**AME-PROCESS-01 — The `Checkpoint: true` exemption list lives in an unspecified file**

ADR-0008 §6 says "The `Checkpoint: true` trailer is the only sanctioned partial-bypass and applies to a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`." That file does not appear in the layout in ARCHITECTURE.md §3 and has no spec. I would need to create it, but I have no spec for its format, no initial contents, and no test that validates its contents are consistent with the gate definitions in ADR-0008 §1. If I omit a gate from the exemption list, checkpoint commits fail that gate — but if I include too many, real violations slip through on checkpoint commits.

**AME-PROCESS-02 — PHASE-1's scope references `.claude/agents/` and `.claude/commands/` wrappers that ADR-0002 explicitly says are empty slots**

PHASE-1 §4 says "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas (PM, Architect, SM, Dev, PO, TEA) and core commands." But ADR-0002 §3 explicitly states these are "(legacy slot — empty in v6 native-skills model)" and says "no wrapper files" are needed because BMAD v6 uses native skills. PHASE-1's scope is internally inconsistent with the accepted ADR. If I follow ADR-0002, I skip PHASE-1 §4. If I follow PHASE-1 §4, I violate ADR-0002. I would have to choose, and there is no disambiguation path other than an ADR amendment.

**AME-PROCESS-03 — The `bulk-green-start` gate threshold N is not specified**

ADR-0006 §4 says "CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." N is not defined anywhere in the 15 documents. I would have to pick a number. Whatever I pick becomes load-bearing CI behavior with no architectural basis.

**AME-PROCESS-04 — The `stale-staging` gate threshold is deferred indefinitely**

ADR-0002 §7 mentions a future `stale-staging` lint rule "flags drafts sitting unpromoted past a configurable threshold." The threshold is not specified, the unit (days? commits? PRs?) is not specified, and the gate is "deferred CHG" with no CHG number. When PHASE-1 implements `tools/spec_lint`, I need to decide whether to include this rule or skip it. If I skip it, I have no gate for an explicitly mentioned discipline. If I include it, I invent a threshold with no architectural basis, and the resulting gate may produce false positives that block legitimate work.

**AME-PROCESS-05 — `tools/tea/` skeleton in PHASE-1 has no spec**

PHASE-1 §5 says "tools/tea/ skeleton — invokes TEA workflows; integration with CI deferred to PHASE-2." There is no ADR for TEA. There is no spec for what a TEA workflow is, what its inputs and outputs are, what "invoking a TEA workflow" means programmatically, or what the skeleton must contain to satisfy PHASE-1's exit gate. The exit gate for PHASE-1 lists only spec_lint rules and BMAD wrappers — TEA skeleton is in scope but not in exit criteria. I would implement an empty directory with a README and have no way to know if that's sufficient or if there's an expected interface file I've missed.

---

**Questions I would bring to the architect before writing a single line of code:**

1. What is the exact JSON schema for `.claude/settings.json` hooks — specifically the key path, event string format, alternation syntax, and glob patterns?
2. What input does a `PreToolUse(Bash:...)` hook receive — full command string, arguments array, environment?
3. How does `validate_commit.py` determine a test is new and currently failing without running the test suite?
4. What is the conflict resolution rule when journal, commit trailers, and spec frontmatter disagree on a REQ's status?
5. How does PHASE-0's `phase-exit` gate pass when `rebuild.py` doesn't exist until PHASE-2?
6. Is `tier: unit` permitted to include real REST calls, or is that forced to `tier: integration`?
7. What N and alpha level are acceptable for distributional stochastic assertions?
8. What exactly does `bmad-smoke-test` assert — what constitutes a valid "output shape" for a BMAD skill?
