# PROSE — editorial-review-prose (sonnet) — Wave 1

**Source transcript:** [`raw-transcripts/PROSE-agent-a07c1f539fac023b9.jsonl`](../raw-transcripts/PROSE-agent-a07c1f539fac023b9.jsonl)
**Sub-agent description:** `Editorial prose review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a07c1f539fac023b9`

## Initial prompt to sub-agent

```
You are an isolated copy-editor with no prior context. Invoke the `bmad-editorial-review-prose` skill via the Skill tool. Apply it to the architecture artifact: flag prose-level communication failures that obscure the technical content. The point isn't typos — it's *load-bearing* ambiguity in normative text.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Specifically hunt:
- Modal-verb sloppiness: "should" vs "must" vs "may" used inconsistently for normative statements. A rule stated as "should" cannot fail CI.
- Voice/audience switching: second-person "you" in an ADR (who is "you"?), first-person plural, passive imperatives.
- Pronouns with ambiguous antecedents in normative sentences.
- Words doing too much work without definition: "real adapter", "deterministic", "boundary", "in-process", "the right one".
- Unscoped quantifiers: "every change", "all hooks", "any commit" without a defined population.
- Examples that contradict the rule they illustrate.
- Forward references ("see §10" when §10 was added by amendment and the original reader didn't have it).
- Phrases that sound rigorous but aren't: "in principle", "by convention", "as appropriate".

REQUIRED OUTPUT:
- Stable IDs: prefix `PROSE-` (e.g. PROSE-01; severity inline as CRITICAL/SERIOUS/PROCESS based on whether the prose ambiguity changes what CI can enforce)
- Each finding: file + section + exact quote, what is ambiguous, what reasonable readings exist, which one CI cannot disambiguate
- Minimum 12 findings
- 1200-2000 words

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have read all 15 documents. I will now conduct the editorial review with the specific focus on load-bearing ambiguity in normative text.

---

## Editorial Review: Architecture Artifacts — Prose-Level Communication Failures

**Scope:** ARCHITECTURE.md, ADR-0001 through ADR-0008, PHASE-0 through PHASE-5
**Focus:** Modal-verb sloppiness, voice/audience switching, undefined load-bearing terms, unscoped quantifiers, examples that contradict rules, forward references, and phrases that sound rigorous but aren't.
**Severity scale:** CRITICAL = ambiguity changes what CI can or cannot enforce; SERIOUS = ambiguity creates divergent implementation paths; PROCESS = ambiguity erodes procedural discipline without directly breaking enforcement.

---

**PROSE-01 — CRITICAL**
**File:** `ARCHITECTURE.md` §1, Principle 3
**Exact quote:** "Boundary adapters are real; only network transport may be substituted at the edge."

**What is ambiguous:** "Boundary adapters are real" uses "real" as a technical term without defining it anywhere in this document. A reader encounters it before ADR-0003 or ADR-0006, which use the same word with a context-dependent meaning. "At the edge" is equally undefined: edge of the repo? edge of the process? edge of the network stack? "May be substituted" is a permission grant — but substituted with what? The phrase implies a fake, which would violate P3 as stated in the opening clause of the same sentence.

**Reasonable readings:**
1. The HTTP layer (the literal network socket) may be replaced with a recorded-response replay, but all in-process code is real.
2. Any code that sits at the boundary between the repo and an external service may be swapped, provided the swap is also real code.

**What CI cannot disambiguate:** `mock-in-repo-banned` must know what "at the edge" means to determine whether a substitution is legal. ADR-0006 §2 does clarify "HTTP transport at the network boundary," but that clarification is a forward reference from §1, which the principle is supposed to encode. The principle itself is underspecified enough that an engineer implementing a lint rule from §1 alone would produce an incorrect rule.

---

**PROSE-02 — CRITICAL**
**File:** `ADR-0004` §3, atomicity rule
**Exact quote:** "a REQ that decomposes into more than one Given/When/Then is a defect."

**What is ambiguous:** "decomposes into" is doing two incompatible jobs. A single assertion can legitimately have multiple Given/When/Then scenarios that test the same assertion from different angles (different inputs, different edge cases). The sentence does not distinguish between multiple scenarios for one assertion versus a compound assertion that describes two different behaviors. The `compound-requirement-detector` lint heuristic is supposed to catch the latter, not the former.

**Reasonable readings:**
1. A REQ with two Given/When/Then blocks covering different input paths is a defect.
2. A REQ whose Given/When/Then blocks collectively imply two separate observable behaviors is a defect.

**What CI cannot disambiguate:** The lint rule must pick one interpretation. If it picks (1), it will reject legitimate multi-scenario REQs. If it picks (2), the detection heuristic is behavioral rather than structural and cannot be implemented from this sentence alone. Either way, the normative sentence produces a different rule than the authors intend.

---

**PROSE-03 — CRITICAL**
**File:** `ADR-0005` §3
**Exact quote:** "Every commit (except checkpoint commits, below) must carry: …"

**What is ambiguous:** "Checkpoint commits, below" is a forward reference to §7. An implementer reading §3 to write `validate_commit.py` must chase the reference to learn what distinguishes a checkpoint commit. The exemption is defined by the presence of `Checkpoint: true` in the trailer — but §3 does not state that. "Below" is a relative position marker that breaks when sections are reordered by amendment. More critically, "every commit" has an undefined population: does it include merge commits auto-generated by GitHub? Revert commits? Empty commits?

**Reasonable readings:**
1. Every commit authored by a human or agent must carry the trailers, except those with `Checkpoint: true`.
2. Every commit that reaches the `main` branch must carry the trailers, except checkpoint commits.
3. Every commit that passes through the pre-commit hook must carry the trailers.

**What CI cannot disambiguate:** `commit-trailers-valid` runs on a `pre-receive hook`. GitHub merge commits and revert commits bypass the pre-commit hook path entirely. The rule needs to define "every commit" by hook trigger, not by the abstract population of all commits.

---

**PROSE-04 — SERIOUS**
**File:** `ADR-0002` §8 (Amendment 0002), item 1
**Exact quote:** "Before merging, exercise at least one BMAD skill end-to-end against a known input and assert the output shape."

**What is ambiguous:** "Before merging" names an actor implicitly ("someone" must do this) and a timing ("before merging" in what workflow stage?). "Known input" is undefined — known to whom, stored where? "Assert the output shape" has no definition of what counts as an assertion. The next sentence places implementation in PHASE-2 (`tools/ci/smoke_bmad.py`), making this a forward reference to a tool that does not yet exist.

**Reasonable readings:**
1. A human reviewer must manually run a BMAD skill before clicking Merge.
2. A CI job (`bmad-smoke-test`) runs automatically on every upgrade PR.

**What CI cannot disambiguate:** §8 item 1 says "Implementation: PHASE-2." Until PHASE-2 lands, this rule is unenforceable and the gate table in ADR-0008 lists `bmad-smoke-test` as a real gate. The gate exists in the inventory before its implementation exists, with no explicit statement that the gate is a no-op until PHASE-2. A reader implementing ADR-0008 in PHASE-1 would not know whether to stub or skip this gate.

---

**PROSE-05 — SERIOUS**
**File:** `ADR-0003` §2
**Exact quote:** "Production builds inject the real GAS adapter; Node unit tests inject a *different real* adapter (e.g. a Sheets adapter that hits a dedicated test spreadsheet via the Sheets REST API). No mock adapter is permitted; substitution is real-for-real, not real-for-fake."

**What is ambiguous:** "Inject" is used without specifying the injection mechanism. In a TypeScript codebase without a DI framework, "inject" could mean constructor argument, module import replacement, or environment-variable-gated conditional. The phrase "real-for-real, not real-for-fake" is a mnemonic, not a definition. It does not tell the lint rule `mock-in-repo-banned` how to detect a "fake" substitution versus a "real" one. A hand-rolled `class SheetsTestAdapter implements ISheetsAdapter` that returns hardcoded data — is that "real"?

**Reasonable readings:**
1. Any class that implements the interface and performs actual I/O against a real system is "real."
2. Any class that is checked into the repo and not annotated with a mock library is "real."

**What CI cannot disambiguate:** `mock-in-repo-banned` only detects specific API calls (`jest.mock`, `sinon.stub`, etc.) and hand-rolled fakes of in-repo *interfaces* per ADR-0006 §2. But ADR-0003 §2 describes adapter substitution without specifying what makes the substitute "real" enough to pass lint. The two ADRs use the same word with different definitional specificity.

---

**PROSE-06 — SERIOUS**
**File:** `ADR-0006` §2
**Exact quote:** "Substituting the **HTTP transport** at the network boundary (e.g. a real `nock` interceptor that records and replays *real* responses captured from the real service). This is permitted only for cost or rate-limit reasons, not for correctness reasons, and never for the LLM tier."

**What is ambiguous:** "Real responses captured from the real service" describes a recording workflow, but "real" appears three times with subtly different referents: the interceptor is "real" (not a mock library), the responses are "real" (not invented), the service is "real" (production or staging?). "Not for correctness reasons" is a statement of intent that is entirely unenforceable by CI — CI cannot audit why a developer chose to use `nock`. The qualifier makes the permission feel constrained but provides no enforcement surface.

**Reasonable readings:**
1. Using `nock` is permitted whenever cost is a concern, regardless of developer intent.
2. Using `nock` is forbidden if any test that uses it would pass with an invented response that the real service would not return.

**What CI cannot disambiguate:** No lint rule can detect "correctness reasons." The permission is therefore unconditional in practice, making the qualifier prose noise that creates a false sense of restriction.

---

**PROSE-07 — SERIOUS**
**File:** `ARCHITECTURE.md` §9
**Exact quote:** "BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by file path, never by name, so a BMAD version upgrade is one wrapper edit per agent."

**What is ambiguous:** ADR-0002 Amendment 0001 completely replaced the wrapper strategy with native Skills — `bmad/` became `_bmad/`, `.claude/agents/` and `.claude/commands/` are described as "legacy slots — empty in v6 native-skills model" in the §3 layout diagram. ARCHITECTURE.md §9 still describes the pre-amendment wrapper architecture. The two sections within the same document contradict each other: §3 says wrappers are empty legacy slots; §9 says wrappers reference BMAD personas by file path.

**Reasonable readings:**
1. Wrappers exist and must reference personas by file path (§9's rule).
2. Wrappers do not exist; native Skills replaced them (§3 and ADR-0002 Amendment 0001).

**What CI cannot disambiguate:** `bmad-direct-reference` lint rule (ADR-0002 Compliance) must know which integration model is authoritative. If §9 is authoritative, the rule should permit paths under `.claude/agents/`. If Amendment 0001 is authoritative, those files should not exist at all. REQ-ARCH-0002 says the architecture artifact must be present; it does not require internal consistency.

---

**PROSE-08 — SERIOUS**
**File:** `ADR-0004` §7
**Exact quote:** "cosmetic edits (typo, grammar) bump `revision` and are allowed only if no downstream artifact refers to the prior revision body."

**What is ambiguous:** "No downstream artifact refers to the prior revision body" is a condition that requires comparing artifact content against prior revision content — a historical diff, not a static analysis. The sentence does not define "downstream artifact" (is another REQ a downstream artifact? a test annotation? a commit message trailer?). No lint rule or CI gate in ADR-0008 is listed as enforcing this condition. The `req-append-only` gate enforces append-only at the assertion level but does not address cosmetic-edit permission.

**Reasonable readings:**
1. Any artifact with a cross-reference to the REQ ID counts as "referring to the prior revision body," so cosmetic edits are nearly always forbidden.
2. Only artifacts whose content quotes the specific assertion text (not just the ID) are blocked.

**What CI cannot disambiguate:** The gate `req-append-only` exists but its scope relative to this cosmetic-edit exception is not defined. An implementer would have to invent the rule's scope.

---

**PROSE-09 — SERIOUS**
**File:** `ADR-0005` §6, Push invariant note
**Exact quote:** "every operation that mutates the commit graph or moves a branch pointer must result in origin tracking the post-state within the same hook firing."

**What is ambiguous:** "Within the same hook firing" is a timing constraint on hook execution. The hooks are listed as `PostToolUse(Bash:git commit)` and `PostToolUse(mcp__github__merge_pull_request)` — but the `Stop`/`SessionEnd` hook is described separately in §7, and it also enforces the push invariant. "The same hook firing" therefore has at least two different enforcement surfaces. If a commit is made inside a longer Bash invocation that does multiple git operations, does each `git commit` sub-call trigger a hook firing, or only the outermost?

**Reasonable readings:**
1. Every individual `git commit` call triggers the push hook; push happens per-commit.
2. The push invariant is checked once per tool call (the `Bash:git commit` pattern), regardless of how many commits occur within the Bash invocation.

**What CI cannot disambiguate:** The `PostToolUse(Bash:*test*)` hook in the same table uses a glob pattern for matching. `PostToolUse(Bash:git commit)` presumably matches only the exact command string `git commit`. A `git commit -m "..."` with additional flags may or may not match depending on implementation, and "the same hook firing" would then silently not fire.

---

**PROSE-10 — SERIOUS**
**File:** `ADR-0008` §3
**Exact quote:** "No REQ from a later phase is `tests-green` (we do not allow phases to complete out of order)."

**What is ambiguous:** "From a later phase" requires that every REQ has an unambiguous phase assignment. REQ frontmatter includes a `phase:` field per ADR-0004 §5, but the rule does not state what happens to a REQ that spans phases (e.g., a REQ created in PHASE-3 whose tests were started in PHASE-2 as part of scaffolding). The parenthetical "we do not allow phases to complete out of order" explains the intent but not the boundary condition: what if a REQ is `tests-green` but its phase is not yet the active phase?

**Reasonable readings:**
1. Any REQ with `phase: PHASE-N+1` that is `tests-green` while PHASE-N is active is a gate failure.
2. REQs can go green in any phase; the gate only checks whether the *phase exit criteria* REQs are green at the right time.

**What CI cannot disambiguate:** Reading (1) would block legitimate early testing; reading (2) renders the "no REQ from a later phase" sentence redundant. The `phase-exit` gate implementation must choose, but neither reading is the obvious one.

---

**PROSE-11 — PROCESS**
**File:** `ADR-0002` §6 (Upgrade procedure), item 4
**Exact quote:** "You merge after review."

**What is ambiguous:** "You" is second-person in an ADR — a document that defines decisions for the system, not instructions to a specific person. "You" has no defined antecedent. In the context of this ADR, "you" could mean: a human project owner, the agent (Claude Code), or the engineer reviewing the PR. The distinction matters because ADR-0005 §6 defines a `PostToolUse(mcp__github__merge_pull_request)` hook that fires when the *agent* merges — if a human merges via the GitHub UI, that hook does not fire.

**Reasonable readings:**
1. A human engineer clicks Merge in the GitHub UI.
2. The agent invokes `mcp__github__merge_pull_request`, triggering the post-merge sync hook.

**What CI cannot disambiguate:** If "you" means a human, the post-merge sync hook (ADR-0005 §6) is never triggered for substrate PRs, leaving the working branch potentially diverged. This is not a CI gate failure — it is a silent operational failure.

---

**PROSE-12 — PROCESS**
**File:** `ADR-0005` §7
**Exact quote:** "The `Checkpoint: true` trailer makes CI gates skip the commit and makes the next non-checkpoint commit on the branch responsible for restoring P4 compliance (either by squash or by ensuring the red/green sequence is recoverable from the full history)."

**What is ambiguous:** "Responsible for restoring P4 compliance" is an obligation with no enforcement surface. "By squash or by ensuring the red/green sequence is recoverable" offers two paths, but neither is gated. "Recoverable from the full history" is particularly vague — recoverable by a human reading git log? By `tools/trace/validate_commit.py`? "In principle" (the phrase does not appear here but the reasoning structure is identical) this sounds like a rule; in practice it is a hope, because the next non-checkpoint commit's author must subjectively judge whether P4 is restored.

**Reasonable readings:**
1. The next non-checkpoint commit must carry `Tests-Status: red→green` to demonstrate P4 was not violated.
2. The author of the next commit must ensure, by inspection, that no green test was introduced without a prior red state.

**What CI cannot disambiguate:** `red-before-green` gate in ADR-0008 enforces P4, but checkpoint commits are exempt. Whether the exemption covers the *entire sequence* up to the next non-checkpoint commit, or only the checkpoint commit itself, is unspecified. A bad actor (or careless agent) could insert a green test in a checkpoint commit and the gate would skip it.

---

**PROSE-13 — PROCESS**
**File:** `PHASE-1` §Scope, item 3
**Exact quote:** "`bmad/` installation per [ADR-0002](../decisions/ADR-0002-bmad-integration.md), pinned in `bmad/config.yaml`."

**What is ambiguous:** ADR-0002 Amendment 0001 renamed `bmad/` to `_bmad/` ("Install path: `_bmad/`"). PHASE-1 still refers to `bmad/` (no underscore). The config pin is described as `bmad/config.yaml`, but ADR-0002 §1 names `_bmad/_config/manifest.yaml` as the canonical version source. These are three different paths for what appears to be the same artifact.

**Reasonable readings:**
1. PHASE-1 predates the amendment and refers to the old path; `_bmad/` is the correct target.
2. PHASE-1 is authoritative and `bmad/` (no underscore) is correct for this phase, with `_bmad/` emerging from a later amendment.

**What CI cannot disambiguate:** `top-level-allowlist` lint rule enforces which top-level directories exist. If it allows `bmad/` (no underscore) because PHASE-1 says so, it conflicts with ADR-0002's `_bmad/` mandate. If it allows only `_bmad/`, PHASE-1's exit criterion ("bmad/config.yaml pins v6 minor version") will never be satisfied at the stated path.

---

**PROSE-14 — PROCESS**
**File:** `ADR-0006` §2 (Permitted substitutions)
**Exact quote:** "Substituting **clock** and **randomness sources** through real adapters (e.g. a deterministic clock implementation that is itself production code, used in both prod and test paths). The substitute must be a real component, not a mock."

**What is ambiguous:** "A deterministic clock implementation that is itself production code" is an example that contradicts the surrounding principle. Operating principle P2 states "Determinism is never manufactured by seeding for systems that are not deterministic in production." A deterministic clock implementation does manufacture determinism — it is a controlled time source used in tests to produce repeatable results. The example appears to sanction exactly the behavior P2 forbids, unless clock substitution is categorically excluded from P2's scope. No such exclusion is stated anywhere.

**Reasonable readings:**
1. Clock adapters are exempt from P2's anti-seeding rule because they are not LLM outputs.
2. A deterministic clock is a P2 violation because it manufactures determinism that does not exist in production.

**What CI cannot disambiguity:** P2's gate (`gate-coverage` references it but no specific lint rule is named for clock adapters) cannot distinguish between a P2-exempt deterministic clock and a forbidden seeded randomness source. The example provides cover for behavior the principle would otherwise prohibit.

---

| Finding | File + Section | Exact Quote | Ambiguity | Severity |
|---|---|---|---|---|
| PROSE-01 | `ARCHITECTURE.md` §1, Principle 3 | "Boundary adapters are real; only network transport may be substituted at the edge." | "Real" and "at the edge" are undefined in §1; the lint rule `mock-in-repo-banned` cannot be derived from this sentence alone without forward-referencing ADR-0006 | CRITICAL |
| PROSE-02 | `ADR-0004` §3 | "a REQ that decomposes into more than one Given/When/Then is a defect." | Does not distinguish multiple scenarios from compound assertions; the lint heuristic must choose an interpretation not resolvable from this sentence | CRITICAL |
| PROSE-03 | `ADR-0005` §3 | "Every commit (except checkpoint commits, below) must carry: …" | "Every commit" is an unscoped quantifier that does not exclude GitHub merge commits, revert commits, or empty commits; "below" is a fragile forward reference | CRITICAL |
| PROSE-04 | `ADR-0002` §8, item 1 | "Before merging, exercise at least one BMAD skill end-to-end against a known input and assert the output shape." | Actor, timing, and "known input" undefined; gate listed in ADR-0008 before implementation exists in PHASE-2 with no explicit no-op stub status declared | SERIOUS |
| PROSE-05 | `ADR-0003` §2 | "substitution is real-for-real, not real-for-fake." | "Real" is a mnemonic without definition; does not tell `mock-in-repo-banned` how to distinguish a hand-rolled fake from a legitimate test adapter | SERIOUS |
| PROSE-06 | `ADR-0006` §2 | "permitted only for cost or rate-limit reasons, not for correctness reasons" | Intent-based qualifier is unenforceable by CI; the permission is therefore unconditional in practice | SERIOUS |
| PROSE-07 | `ARCHITECTURE.md` §9 | "BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`." | Directly contradicts §3 layout diagram and ADR-0002 Amendment 0001, which replaced wrappers with native Skills and renamed `bmad/` to `_bmad/` | SERIOUS |
| PROSE-08 | `ADR-0004` §7 | "allowed only if no downstream artifact refers to the prior revision body." | "Downstream artifact" undefined; condition requires historical diff analysis with no named gate; `req-append-only` scope relative to cosmetic-edit exception unspecified | SERIOUS |
| PROSE-09 | `ADR-0005` §6 (Push invariant) | "every operation that mutates the commit graph or moves a branch pointer must result in origin tracking the post-state within the same hook firing." | "Same hook firing" is ambiguous when multiple git operations occur within one Bash invocation; glob matching behavior for `PostToolUse(Bash:git commit)` not specified | SERIOUS |
| PROSE-10 | `ADR-0008` §3 | "No REQ from a later phase is `tests-green`" | Does not handle REQs that span phases or are green before their declared phase is active; implementation of `phase-exit` gate must choose an interpretation not derivable from this sentence | SERIOUS |
| PROSE-11 | `ADR-0002` §6, item 4 | "You merge after review." | "You" in a normative ADR has no defined antecedent; if "you" is a human, the `PostToolUse(mcp__github__merge_pull_request)` sync hook never fires for substrate PRs | PROCESS |
| PROSE-12 | `ADR-0005` §7 | "makes the next non-checkpoint commit on the branch responsible for restoring P4 compliance (either by squash or by ensuring the red/green sequence is recoverable from the full history)." | "Responsible" is an unenforced obligation; "recoverable" has no defined test; checkpoint exemption scope is ambiguous regarding sequences between checkpoint and next non-checkpoint commits | PROCESS |
| PROSE-13 | `PHASE-1` §Scope, item 3 | "`bmad/` installation per ADR-0002, pinned in `bmad/config.yaml`." | Conflicts with ADR-0002 Amendment 0001 (`_bmad/`) and with ADR-0002 §1 (`_bmad/_config/manifest.yaml`); three different paths for the same artifact | PROCESS |
| PROSE-14 | `ADR-0006` §2 | "a deterministic clock implementation that is itself production code, used in both prod and test paths" | Example appears to sanction manufactured determinism that P2 forbids; no explicit exemption for clock adapters from P2's anti-seeding scope | PROCESS |

---

**Summary of the most load-bearing failures:**

PROSE-07 is the highest-impact finding in operational terms: ARCHITECTURE.md §9 describes an integration model (thin wrappers in `.claude/agents/`) that ADR-0002 Amendment 0001 retired. Any engineer reading §9 without cross-checking ADR-0002's amendment log would build the wrong system. A lint rule derived from §9 would conflict with one derived from §3 of the same document.

PROSE-03 is the highest-impact CI-enforcement failure: the undefined population of "every commit" means `commit-trailers-valid` must make an implementation decision that is not specified anywhere. GitHub-generated merge commits are the most common case that would silently break if the rule is naively applied.

PROSE-01 is structurally critical because it is a principle — the highest-normative-level statement — that uses an undefined term ("real") as its operative constraint. Everything downstream (`mock-in-repo-banned`, ADR-0003, ADR-0006) inherits this definitional gap. The gap is filled by the ADRs, but the principle cannot be understood or enforced independently, which undermines the claim that "a principle without a CI gate is a build failure."
