# ADVS — adversarial-general (sonnet) — Wave 1

**Source transcript:** [`raw-transcripts/ADVS-agent-a101c290244165df1.jsonl`](../raw-transcripts/ADVS-agent-a101c290244165df1.jsonl)
**Sub-agent description:** `Adversarial review (sonnet)`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a101c290244165df1`

## Initial prompt to sub-agent

```
You are an isolated independent reviewer with no prior context, no findings ledger, no project status. Form opinions from source documents only.

Invoke the `bmad-review-adversarial-general` skill via the Skill tool, then apply it to these 15 files (all under /home/user/Test-Repo/):

1. openspec/architecture/ARCHITECTURE.md
2. openspec/architecture/decisions/ADR-0001-monorepo-layout.md
3. openspec/architecture/decisions/ADR-0002-bmad-integration.md
4. openspec/architecture/decisions/ADR-0003-appscript-runtime.md
5. openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md
6. openspec/architecture/decisions/ADR-0005-traceability-and-journaling.md
7. openspec/architecture/decisions/ADR-0006-testing-tiers.md
8. openspec/architecture/decisions/ADR-0007-llm-stochastic-assertions.md
9. openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md
10. openspec/architecture/phases/PHASE-0-foundation.md through PHASE-5-first-appscript-project.md

Operating principles (verbatim):
1. Single source of truth. One canonical home per fact. Cross-document consistency is lintable.
2. Stochastic systems get statistical assertions.
3. Tests exercise real production code. No mocks of in-repo modules.
4. Red-first. Every test is failing in git history before the commit that turns it green.
5. OpenSpec for spec, BMAD + TEA for workflow.

"A principle without a CI gate is itself a build failure."

REQUIRED OUTPUT:
- Stable IDs: prefix `ADVS-` (e.g. ADVS-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Each finding: cite file + section/line, 2-4 sentences, name which P1-P5 or ADR it violates
- Cross-document tensions especially valuable
- 1500-2500 words
- No preamble, no fixes, just findings

DO NOT read CLAUDE.md, STATUS.md, or any file outside the 15 listed.
```

## Findings deliverable (final assistant message)

Now I have read all 15 documents. I will produce the adversarial findings report.

---

## Adversarial Review — Architecture & ADR Corpus

**Reviewed artifacts:** ARCHITECTURE.md, ADR-0001 through ADR-0008, PHASE-0 through PHASE-5
**Reviewer posture:** Independent, no prior context, source documents only.

---

### CRITICAL

---

**ADVS-CRIT-01 — Circular bootstrap: red-first tests cannot exist before the tools that detect red-first violations**

`ARCHITECTURE.md §11`, `PHASE-0 exit criteria`, `ADR-0005 §4`, `ADR-0006 §4`, `ADR-0008 §1` gate `red-before-green`.

PHASE-0 mandates that REQ-ARCH-* tests be written "red-first" and turn green as scaffolding completes. Yet the `red-before-green` CI gate that enforces P4 is not implemented until PHASE-2, and the `tools/trace/validate_commit.py` that walks history to verify the red/green sequence does not exist until PHASE-2. The tests written in PHASE-0 are therefore committed without any mechanical enforcement of the red-first rule. By the time PHASE-2 lands and `validate_commit.py` walks history, the PHASE-0 tests are already `tests-green` commits — there is no prior-commit with the test in a failing state that is discoverable in the same way, because the validator did not run at commit time. P4 is violated for the entire PHASE-0 test corpus and PHASE-2 cannot retroactively enforce it. Neither the ADRs nor the phase files acknowledge this gap or provide a remediation path.

---

**ADVS-CRIT-02 — `commit-trailers-valid` gate fires on a hook that does not exist in PHASE-0 or PHASE-1**

`ADR-0005 §3`, `ADR-0005 §6`, `ADR-0008 §1`, `PHASE-0 scope §9`, `PHASE-2 scope §4`.

ADR-0005 §3 mandates trailers on every commit. ADR-0008 §1 shows `commit-trailers-valid` listed as a `pre-receive hook` gate. PHASE-0 only commits `.claude/settings.json` with placeholder hooks that `exit 0`. This means the `PreToolUse(Bash:git commit)` hook declared in ADR-0005 §6 is a no-op through the end of PHASE-1. Every commit made in PHASE-0 and PHASE-1 — including the commits that are supposed to set up the traceability system — can be pushed without valid trailers, and there is no pre-receive hook on the server side documented anywhere. The table in ADR-0008 §1 says the trigger is `pre-receive hook` but the three workflow files mentioned in §4 all run `on: pull_request`, not as server-side hooks. The gate is therefore unenforceable for direct pushes to any branch during PHASE-0 and PHASE-1, violating P1 (single source of truth — trailers are a truth source) and undermining every assumption the PHASE-2 rebuild makes about git history integrity.

---

**ADVS-CRIT-03 — `phase-exit` gate cannot fire because no phase has `tests-green` REQs until PHASE-2's matrix-drift gate exists**

`ADR-0008 §3`, `PHASE-0 exit criteria`, `PHASE-1 exit criteria`.

ADR-0008 §3 says: "The `phase-exit` gate runs on merge to `main` and verifies: the current phase's exit REQs are all `tests-green` in the matrix." The matrix is built by `tools/trace/rebuild.py`, which is not implemented until PHASE-2. PHASE-0 ships only an empty `matrix.yaml`. Merging PHASE-0 work to `main` with the `phase-exit` gate enabled means the gate reads an empty matrix and would either spuriously pass (no REQs listed → trivially satisfied) or require a special bootstrapping exemption that is never documented. PHASE-0's exit section does not address this paradox. This violates ADR-0008 §3's self-stated preconditions and makes the gate-coverage claim in §2 — "Adding a principle without a gate is therefore impossible" — false for PHASE-0 and PHASE-1.

---

**ADVS-CRIT-04 — ARCHITECTURE.md §9 describes a BMAD integration model that contradicts ADR-0002's amendment**

`ARCHITECTURE.md §9`, `ADR-0002 Amendment 0001`.

ARCHITECTURE.md §9 states: "BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by file path." ADR-0002 Amendment 0001 explicitly rejects this model: "The original ADR text designed a wrapper-isolation strategy based on outdated assumptions … that turned out to be neither how BMAD v6 works nor necessary." The amendment establishes that `.claude/agents/` and `.claude/commands/` are "legacy slots — empty in v6 native-skills model." The Architecture document — declared the frozen authoritative artifact — contains a factual description of the integration that has been superseded by an amendment. ARCHITECTURE.md §9 has never been updated to reflect this. This is a direct violation of P1 (single source of truth) embedded in the document that is the declared source of truth. PHASE-1's scope item 4 further compounds this by listing `.claude/agents/` and `.claude/commands/` wrappers as PHASE-1 deliverables — another artifact contradicted by ADR-0002 Amendment 0001.

---

**ADVS-CRIT-05 — `prose-xref-banned` lint rule is violated by the ADR corpus itself, before the rule exists**

`ADR-0004 §2`, `ARCHITECTURE.md §2`, `ADR-0001 Compliance`, `PHASE-1`.

ADR-0004 §2 states that "illustrative prose references are a lintable defect" and lists patterns such as "the paper", "the original ADR". ARCHITECTURE.md §2 explicitly reads: "A published result on transformer associative memory (referred to throughout as 'the paper')." ADR-0004's own Context section repeats "the paper" six times without a stable ID or file path. No REQ-ID or file path is ever assigned to this referenced work. ADR-0002 also uses "the paper" formulation indirectly through ADR-0004's terms. When PHASE-1 activates the `prose-xref-banned` rule, it would — if consistently applied — flag the architecture's own context section. Since the lint rule is explicitly configured to scan `openspec/architecture/` (implied by `xref-resolves` gate), this creates a corpus that cannot pass its own rules without remediation not planned in any phase scope.

---

### SERIOUS

---

**ADVS-SERI-01 — `gate-coverage` meta-gate has no coverage for P5 ("OpenSpec for specification, BMAD + TEA for workflow")**

`ADR-0008 §1`, `ADR-0008 §2`, `ARCHITECTURE.md §1 P5`.

ADR-0008 §2 states that `gate-coverage` "walks every ADR and every principle in ARCHITECTURE.md §1 and verifies that at least one entry in the table above references it." Examining the gate table in §1, no gate explicitly references P5. Gates reference ADR-0001 through ADR-0007. P5's enforcement would require a gate that detects when a convention parallel to OpenSpec or BMAD+TEA is introduced — but no such gate exists and none is named. The `gate-coverage` gate itself would pass because it presumably matches on ADR references, not on direct P5 citation. P5 is therefore mechanically unenforceable, which by the document's own standard ("a principle without a gate is a gate-coverage failure") constitutes a build failure.

---

**ADVS-SERI-02 — REQ-ARCH-* requirements have no canonical spec file, violating ADR-0004's storage format**

`ARCHITECTURE.md §10`, `ADR-0004 §5`, `ADR-0004 §6`.

ARCHITECTURE.md §10 defines REQ-ARCH-0001 through REQ-ARCH-0008 inline in a prose section. ADR-0004 §5 mandates the per-REQ block format with YAML frontmatter including `id`, `revision`, `status`, `introduced`, `supersedes`, `phase`, `tier`, `references`. ADR-0004 §6 states that `openspec/specs/INDEX.yaml` is "the sole retrieval surface for tooling." REQ-ARCH-* requirements embedded as prose in ARCHITECTURE.md have no YAML frontmatter, no INDEX.yaml entry, and no canonical spec file path (they would need to live in `openspec/specs/arch/` or similar). The `index-up-to-date` and `spec-frontmatter-valid` gates would fail against any attempt to reference these REQs once PHASE-1 and PHASE-2 tooling runs. Neither PHASE-0 nor any subsequent phase scope addresses moving REQ-ARCH-* into a properly formatted spec file.

---

**ADVS-SERI-03 — `Checkpoint: true` commits undermine P4 in multi-session scenarios with no defined recovery protocol**

`ADR-0005 §7`, `ADR-0006 §4`, `ARCHITECTURE.md §1 P4`.

ADR-0005 §7 states that the `Checkpoint: true` trailer "makes the next non-checkpoint commit on the branch responsible for restoring P4 compliance (either by squash or by ensuring the red/green sequence is recoverable from the full history)." This obligation is placed on "the next commit" but there is no hook, gate, or lint rule that enforces it. A session that ends mid-red-test with a checkpoint, followed by a new session that adds a green commit, could produce a history where the red-before-green sequence is interrupted by a checkpoint commit with `Tests-Status: none`. The `red-before-green` gate is described as walking history — it is unspecified whether it treats checkpoints as transparent or as opaque. The `tools/trace/checkpoint_exemptions.yaml` file referenced in ADR-0008 §6 is mentioned once, never defined in scope for any phase, and has no corresponding REQ-CI-* requirement.

---

**ADVS-SERI-04 — ADR-0003's "real-for-real adapter substitution" is not defined for clock and randomness, creating a P3 gap**

`ADR-0003 §2`, `ADR-0006 §2`, `ARCHITECTURE.md §1 P3`.

ADR-0003 §2 states that "node unit tests inject a different real adapter (e.g. a Sheets adapter that hits a dedicated test spreadsheet via the Sheets REST API). No mock adapter is permitted; substitution is real-for-real, not real-for-fake." ADR-0006 §2 permits "substituting clock and randomness sources through real adapters." A "deterministic clock implementation that is itself production code, used in both prod and test paths" is exactly what determinism-by-seeding looks like when renamed. The prohibition in P2 is "Determinism is never manufactured by seeding for systems that are not deterministic in production." A deterministic clock substituted in tests is manufacturing determinism for a system that uses wall-clock time in production. This is a semantic loophole in ADR-0006 §2 that directly contradicts P2, and no ADR addresses the tension.

---

**ADVS-SERI-05 — `anti-aliasing` threshold is defined as "pinned in `tools/spec_lint/config.yaml`" but that file has no defined owner or review gate**

`ADR-0004 §4`, `ADR-0008 §1`.

ADR-0004 §4 states: "The threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." The quarterly review is described as a `gate`-type task, but no REQ-ID covers it, no phase scope creates it, and ADR-0008 §1's gate table has no entry for "quarterly-anti-aliasing-review." A quarterly task that is not tracked in the traceability system — the very system that exists to make all work accountable — is invisible to the tooling. There is no mechanism to detect when the last review occurred or whether one is overdue, violating P1 (single source of truth for all work) and making the anti-aliasing protection silently stale.

---

**ADVS-SERI-06 — PHASE-5 scope item §3 is duplicated as §4, indicating missing content**

`PHASE-5-first-appscript-project.md scope`.

PHASE-5's scope section lists items numbered 1 through 6, but items 3 and 4 both bear the numeral "4" in the source. The actual item 3 ("Real adapter wiring against shared-ts") has no number and the numbered item 4 appears twice — once for the BMAD output isolation work and once for "Test suite across all four tiers." This is either a copy-paste error that dropped an entire scope item or a numbering defect that makes the scope ambiguous. In a document where scope items are the basis for task decomposition and traceability, an unnumbered or mis-numbered scope item cannot be traced to a TASK-NNNN without ambiguity. This violates P1 at the phase-document level.

---

**ADVS-SERI-07 — `nock` HTTP interceptor permission in ADR-0006 §2 creates an unenforceable carve-out that the no-mock rule cannot distinguish**

`ADR-0006 §2`, `ADR-0008 §1`, `ARCHITECTURE.md §1 P3`.

ADR-0006 §2 states that "a real `nock` interceptor that records and replays real responses captured from the real service" is permitted "only for cost or rate-limit reasons, not for correctness reasons." The `mock-in-repo-banned` lint rule bans mock APIs applied to modules within this repository, but `nock` operates at the network transport layer and is explicitly permitted. However, there is no CI gate that distinguishes between a `nock` interceptor backed by a "real response capture" vs. one backed by hand-authored fixture data. A developer can introduce a `nock` interceptor with fabricated responses and the lint rule will not fire because `nock` is not in the banned list. The distinction between "real captured" and "fabricated" is a code review judgment, not a mechanical gate. This makes P3 partially unenforceable without tooling that is never specified.

---

**ADVS-SERI-08 — ADR-0002's `bmad-version-pin` gate depends on a comment in `install_bmad.sh` as a source of truth**

`ADR-0002 Compliance`, `PHASE-2 scope §4`, `ARCHITECTURE.md §1 P1`.

ADR-0002 Compliance section and PHASE-2 §4 describe a `bmad-version-pin` gate that "asserts `_bmad/_config/manifest.yaml` version matches the comment in `scripts/install_bmad.sh`." Comparing a machine-readable field in a YAML manifest against a human-authored comment in a shell script is a fragile single source of truth arrangement. Comments are cosmetic by convention; they have no schema, no enforced format, and no lintable structure. The gate's correctness depends on the comment being syntactically parseable in a defined way that is never documented in the ADR. If the comment format drifts (e.g. a developer updates it differently), the gate either false-fires or silently passes, violating P1's requirement that "cross-document consistency is lintable."

---

### PROCESS

---

**ADVS-PROC-01 — ADR-0001 references `bmad/` as the BMAD installation directory but the actual directory is `_bmad/`**

`ADR-0001 Decision`, `ADR-0002 Amendment 0001`.

ADR-0001's Decision section lists `bmad/` as a top-level directory: "BMAD installation, treated as upstream-managed." ADR-0002 Amendment 0001 changed the install path to `_bmad/` (underscore-prefixed, per upstream convention). ADR-0001 was never amended to reflect this. ARCHITECTURE.md §3's directory tree correctly shows `_bmad/` but ADR-0001 still says `bmad/`. The `top-level-allowlist` lint rule (owned by ADR-0001) would need to allow `_bmad/`, not `bmad/` — but the ADR that owns the allowlist contains the wrong name. Whoever implements the lint rule in PHASE-1 must read both documents and adjudicate a discrepancy that should have been resolved by amending ADR-0001.

---

**ADVS-PROC-02 — No phase file defines how a phase-exit ADR is created or who signs it off**

`ARCHITECTURE.md §11`, `ADR-0008 §3`.

ARCHITECTURE.md §11 states: "A phase cannot start until the prior phase's exit criteria are all `tests-green` and the phase exit ADR is signed off." ADR-0008 §3 does not mention a "phase exit ADR"; it describes a `phase-exit` CI gate that checks REQ-IDs. No phase file (PHASE-0 through PHASE-5) defines the artifact called "phase exit ADR," its format, who creates it, what ID scheme it uses, or how "signed off" is mechanically detected. This is an undocumented artifact type that the phased delivery model depends on. Because it lacks a stable ID format and canonical home, it cannot be referenced by the traceability system, violating ADR-0004 §1's identifier discipline.

---

**ADVS-PROC-03 — `stale-staging` gate is deferred to an unspecified CHG with no phase assignment**

`ADR-0002 §7`, `ADR-0008 §1`.

ADR-0002 §7 introduces a "future spec_lint rule `stale-staging`" flagging unpromoted drafts past a "configurable threshold." This is listed as a "deferred CHG" with no CHG number, no TASK-NNNN, no phase assignment, and no REQ-ID. ADR-0008 §1's gate table does not include `stale-staging`. The gate-coverage check would not flag it because it was never added to the table. A deferred gate that was never formally registered means BMAD staging content can accumulate indefinitely without mechanical pressure to promote or purge it. This is an operational risk dressed up as a deferral decision.

---

**ADVS-PROC-04 — ADR-0007 §4's `@cost-budget tokens=<N>` annotation format is undefined and has no allocation authority**

`ADR-0007 §4`, `ADR-0008 §1` gate `cost-budget`.

ADR-0007 §4 states that stochastic tests carry a `@cost-budget tokens=<N>` annotation and that CI aggregates per-PR and per-nightly budgets. The annotation format, the unit of `N` (input tokens? output tokens? combined?), the per-PR and per-nightly aggregate limits, and the authority that sets those limits are all unspecified. No phase scope creates a `REQ-CI-*` requirement for the `cost-budget` gate's configuration. No ADR defines who can change the budget threshold and what review process governs that change. A gate whose threshold is undocumented and whose configuration has no owner is a gate that can be trivially gamed by setting `N` to an arbitrarily large value, defeating the cost containment purpose.

---

**ADVS-PROC-05 — PHASE-3 scope creates "TypeScript and Python clients (mirrored surface)" with no ADR governing the mirroring contract**

`PHASE-3 scope §1`, `ADR-0003`, `ADR-0007`.

PHASE-3 §1 describes `packages/anthropic-client/` as "TypeScript and Python clients (mirrored surface where APIs differ)." The qualification "where APIs differ" is the operative constraint — it acknowledges that the two clients are not identical. There is no ADR or REQ governing the mirroring contract: what constitutes an acceptable divergence, how divergences are detected, and how the test coverage of one client's stochastic tier relates to the other's. If the Python client diverges from the TypeScript client in a meaningful way, the stochastic tests authored against one may not reveal regressions in the other. Neither ADR-0007 nor any phase file defines a cross-language equivalence gate, leaving the "mirrored surface" claim unenforceable.
