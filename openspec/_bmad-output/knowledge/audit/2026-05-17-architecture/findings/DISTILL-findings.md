# DISTILL — distillator (sonnet) — Wave 2

**Source transcript:** [`raw-transcripts/DISTILL-agent-a8263f264435cbc68.jsonl`](../raw-transcripts/DISTILL-agent-a8263f264435cbc68.jsonl)
**Sub-agent description:** `Distillator review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a8263f264435cbc68`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-distillator` skill via the Skill tool to perform a lossless compression pass on the architecture artifact. The compression itself isn't the deliverable — what you discover *during* compression is. Specifically: what concepts in the artifact resist compression because they're redundant, ambiguous, or contradictory?

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Things to look for during compression:
- Concepts described in multiple documents that you can't merge because the descriptions subtly differ
- Sections that should be one paragraph but are several because they're hedged or qualified
- Lists where the items overlap or are not parallel
- Forward references that make compression impossible without restructuring
- Examples that contradict the rule they illustrate (the compressor can't keep both)
- Repeated phrasings that mask actual disagreement
- Single-source-of-truth violations that the compressor exposes by trying to deduplicate

REQUIRED OUTPUT:
- Stable IDs: prefix `DISTILL-` (e.g. DISTILL-01)
- Severity inline as CRITICAL / SERIOUS / PROCESS
- Minimum 12 findings: each = a place where compression failed and what the failure tells you about the source
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I now have all 15 documents fully read. I'll perform the compression analysis and produce the findings.

---

**DISTILL-01** | CRITICAL

**The BMAD installation path is stated inconsistently across documents, making deduplication impossible.**

ARCHITECTURE.md §3 shows the layout with `_bmad/` as the BMAD directory and `.claude/skills/` as the Skills location. ADR-0002's title says "v6.6.0 vendored, native Skills" and its body correctly describes `_bmad/` and `.claude/skills/`. But PHASE-1's scope item 3 references `bmad/config.yaml` (bare `bmad/`, not `_bmad/`) as the BMAD pin location, and PHASE-1 scope item 4 references `.claude/agents/` and `.claude/commands/` wrappers for BMAD personas — a pattern that ADR-0002's own Amendment 0001 explicitly declares obsolete ("The wrapper-isolation strategy from ADR-0002's original revision is dropped — native Skills make it unnecessary"). The compressor cannot merge PHASE-1's scope into a single canonical description of the BMAD install because PHASE-1 describes an install that no longer exists (pre-Amendment 0001 state: `bmad/`, wrappers). This is not a forward reference — PHASE-1 was authored after ADR-0002 Amendment 0001 and still cites the superseded layout. A reader following PHASE-1 to implement the phase would install BMAD at the wrong path and create wrapper files that the ADR says must not exist.

---

**DISTILL-02** | CRITICAL

**ARCHITECTURE.md §9 describes the workflow surface in a way that directly contradicts ADR-0002 Amendment 0001, with no reconciliation path.**

ARCHITECTURE.md §9 states: "BMAD agents live under `bmad/`; Claude Code surfaces them via thin wrappers in `.claude/agents/` and `.claude/commands/`. Wrappers reference BMAD personas by file path, never by name, so a BMAD version upgrade is one wrapper edit per agent." ADR-0002 Amendment 0001 (which amends the same repo) says: "Install path: `_bmad/`… Integration: native Claude Code Skills under `.claude/skills/` (was thin wrappers under `.claude/agents/` and `.claude/commands/`)." The two descriptions are flatly incompatible. ARCHITECTURE.md §9 is a statement of a superseded architecture. When compressing, neither version can be discarded without loss — but keeping both requires asserting a contradiction. The document in §3 shows the correct `_bmad/` layout while §9 describes the old `bmad/` + wrappers model. This is a single-source-of-truth violation: the same ARCHITECTURE.md contains two different answers to "how is BMAD integrated."

---

**DISTILL-03** | CRITICAL

**The "container reclaim, committed but unpushed" failure mode is described differently in ARCHITECTURE.md §8 versus ADR-0005 §8, and the discrepancy conceals a semantic difference in the guarantee.**

ARCHITECTURE.md §8 lists four failure rows. ADR-0005 §8 lists six rows. The missing row in ARCHITECTURE.md is "Container reclaim, committed but unpushed" — which ADR-0005 describes as "Mitigated by per-commit push hook (§6) and by extended checkpoint hook (§7); residual loss only if both hooks fail to fire." ARCHITECTURE.md merges this silently into the row "Container reclaim, push completed → Zero" and "Container reclaim, uncommitted changes → Mitigated by Stop/SessionEnd checkpoint-commit hook." These are not equivalent: a committed-but-unpushed state is neither "push completed" nor "uncommitted." The compressor cannot merge the two tables without losing the specific guarantee about the push-invariant hooks. The summary in ARCHITECTURE.md therefore understates the residual loss risk. Any consumer reading only ARCHITECTURE.md for the crash recovery contract gets a materially incomplete picture.

---

**DISTILL-04** | SERIOUS

**The "red-first" principle (P4) has three different formulations that each exclude an element present in the others.**

ARCHITECTURE.md §1 principle 4: "Every test exists in a failing state in git history before the commit that turns it green." ADR-0005 §4 rule: "A test's first green commit must be preceded by at least one commit where the same test exists in a red state." ADR-0006 §4 rule: "Every test exists in a `tests-red` commit before the `tests-green` commit." These look parallel, but they differ in scope. ARCHITECTURE.md says "failing state" (vague, not tied to the `tests-red` status marker). ADR-0005 uses "red state" and introduces `tools/trace/validate_commit.py` as enforcement. ADR-0006 introduces the `Bootstrap: <reason>` trailer exemption and the `bulk-green-start` gate — neither appears in the principle statement or in ADR-0005. The compressor cannot produce a single canonical definition without either losing the bulk-green-start exemption path (present only in ADR-0006) or inventing a synthesized claim that no single document makes.

---

**DISTILL-05** | SERIOUS

**The no-mock rule has two distinct scopes that are stated as if they are the same rule.**

CLAUDE.md states: "Using `jest.mock`, `sinon.stub`, `unittest.mock.patch`, etc. on in-repo modules" is forbidden. ADR-0006 §2 states the same list but adds `jest.fn().mockImplementation`, `vi.mock`, `unittest.mock.MagicMock`, and `monkeypatch.setattr`. CLAUDE.md's list is a subset of ADR-0006's list, presenting as a complete enumeration when it is not. Additionally, ADR-0006 §2 permits "substituting the HTTP transport at the network boundary (e.g. a real `nock` interceptor that records and replays *real* responses captured from the real service)" — a nuanced carve-out absent from CLAUDE.md. A reader of CLAUDE.md in isolation would not know that nock-style transport substitution is explicitly allowed. A compressor trying to merge the forbidden list must pick one version; neither is complete without the other.

---

**DISTILL-06** | SERIOUS

**The spec flow diagram in ARCHITECTURE.md §5 introduces "TEA" as an authoring agent without defining it, while the operating principles (§1, P5) and ADR-0002 reference it inconsistently.**

ARCHITECTURE.md §1 P5: "OpenSpec for specification, BMAD + TEA for workflow." The spec flow (§5) labels the bottom-up flow "BMAD SM + Dev + TEA" but never defines what TEA produces or which artifacts it owns. ADR-0006 §4 says "TEA-authored failing tests" is a requirement for `EPIC.status = ready-for-dev`. ADR-0002 mentions `tools/tea/` as a PHASE-1 deliverable skeleton. PHASE-1 scope item 5 says "invokes TEA workflows; integration with CI deferred to PHASE-2." PHASE-2 makes no mention of TEA at all (it completes CI integration). Compressing these references into a single statement of what TEA is and when it is integrated is impossible: each document adds a partial fact. TEA never has a dedicated ADR, so its contract is assembled from fragments across five documents, each with a slightly different framing.

---

**DISTILL-07** | SERIOUS

**"Semantic search is forbidden for spec lookup" has a conditional exception that is stated in three incompatible ways.**

ADR-0004 §6: "No tool we ship may use embeddings or semantic search for spec lookup." ADR-0004 §8: "Semantic search is permitted only for human discovery UIs, never for tooling correctness." ARCHITECTURE.md §2: "no agent retrieves a specification by semantic similarity" — no exception stated. The compressor sees three statements: (a) absolute prohibition for tooling, (b) conditional permission for human discovery with a CI gate, (c) absolute prohibition for agents. These are not equivalent. "Tooling" and "agents" are overlapping but not identical categories. If a BMAD agent invokes a human discovery UI, is that permitted under (b) or prohibited under (c)? The two carve-outs (human discovery vs. agent use) are not reconciled anywhere.

---

**DISTILL-08** | SERIOUS

**The checkpoint commit's exemption scope is stated in two documents without specifying which gates are actually exempted.**

ADR-0005 §7 states: "The `Checkpoint: true` trailer makes CI gates skip the commit and makes the next non-checkpoint commit on the branch responsible for restoring P4 compliance." ADR-0008 §6 states: "The `Checkpoint: true` trailer (ADR-0005 §7) is the **only** sanctioned partial-bypass and applies to a specific subset of gates listed in `tools/trace/checkpoint_exemptions.yaml`." These two descriptions give different scopes for the exemption. ADR-0005 says "CI gates skip the commit" (implying all gates skip the checkpoint commit). ADR-0008 says only "a specific subset" listed in a separate file. The actual exemption set is neither in ADR-0005 nor ADR-0008 — it is deferred to a file (`checkpoint_exemptions.yaml`) that is not one of the 15 documents and has not been authored in PHASE-0. A compressor cannot produce a complete statement of the rule.

---

**DISTILL-09** | SERIOUS

**The `openspec/_bmad-output/` staging directory is classified as "non-authoritative" with hard invariants, but the Consequences section of ADR-0002 simultaneously claims it enforces P1 (SoT).**

ADR-0002 §7 states `openspec/_bmad-output/` "is **non-authoritative** and outside the addressable artifact network." ADR-0002 Consequences states: "Output routing under `openspec/` enforces P1 (SoT) for product knowledge" and "P1 preserved: each artifact has exactly one canonical home; drafts never compete with authoritative artifacts." These cannot both be right at the same time. If the staging directory is outside the addressable network, routing output there does not enforce P1 — it creates a liminal zone where the SoT principle is suspended. The claim that "P1 preserved" is a rationalization, not a logical consequence of the design. Compression exposes this: a lossless single sentence either says P1 is enforced or it is not; the document asserts both simultaneously.

---

**DISTILL-10** | SERIOUS

**Phase sequencing has a structural ambiguity: PHASE-3 declares adapter declarations as in-scope but PHASE-4 declares adapter implementations as in-scope, with no boundary definition.**

PHASE-3 scope item 2: "Adapter declarations in `packages/shared-ts/adapters/` and `packages/shared-py/adapters/` for Anthropic transport substitution at the network boundary only." PHASE-4 scope item 1: "GAS adapter interfaces declared in `packages/shared-ts/gas/`" and "Real adapter implementations: `gas-production`, `gas-test-rest`." These overlap spatially (both write to `packages/shared-ts/adapters/` or adjacent directories) with no stated rule about which subdirectory each phase owns. PHASE-3 puts declarations in `shared-ts/adapters/`; PHASE-4 puts interfaces in `shared-ts/gas/`. Is `adapters/` a subdirectory of `gas/`, or are they sibling directories? The compressor cannot produce a single filesystem layout because the two phase descriptions are not consistent with each other.

---

**DISTILL-11** | PROCESS

**The ARCHITECTURE.md §3 layout shows `.claude/agents/` and `.claude/commands/` as "(legacy slot — empty in v6 native-skills model)" but ADR-0001's compliance section says these directories are allowed top-level entries — creating a permanent discrepancy between what is present and what is permitted.**

ARCHITECTURE.md §3 annotates both directories as legacy/empty. ADR-0002 Amendment 0001 confirms they are empty. But PHASE-1 scope item 4 explicitly delivers "`.claude/agents/` and `.claude/commands/` wrappers for BMAD personas" — meaning PHASE-1 will populate directories that ARCHITECTURE.md simultaneously marks as empty legacy slots. If PHASE-1 is implemented per its spec, ARCHITECTURE.md §3's annotation becomes wrong. If the annotation is authoritative, PHASE-1 scope item 4 must be dropped. The compressor cannot keep both — they predict mutually exclusive filesystem states after PHASE-1.

---

**DISTILL-12** | PROCESS

**The `openspec/specs/INDEX.yaml` has two different descriptions of who may edit it, stated in documents that are supposed to be SoT for the same rule.**

ARCHITECTURE.md §3 lists `INDEX.yaml` as "auto-generated deterministic index." ADR-0004 §6: "`openspec/specs/INDEX.yaml` is auto-generated by `tools/spec_lint index`." ADR-0004 §1: "Identifier allocation is by `tools/spec_lint allocate <domain>` against `openspec/specs/INDEX.yaml`. Hand-allocation is permitted but checked." CLAUDE.md states: "Hand-editing `openspec/specs/INDEX.yaml` after PHASE-1" is forbidden. These four statements imply four different states: (a) always auto-generated, (b) auto-generated but hand-allocation permitted before PHASE-1, (c) hand-editing forbidden after PHASE-1, (d) the INDEX is used as a lookup target for hand-allocation. Statement (b) combined with (c) implies hand-allocation is permitted in PHASE-0 and PHASE-1 only — but this temporal scoping appears in no single document. The compressor must either assert a simpler rule (losing the temporal nuance) or synthesize a compound rule that no document states directly.

---

**DISTILL-13** | PROCESS

**The `gate-coverage` gate is simultaneously a meta-gate that enforces itself and a gate that is implemented in PHASE-2 — making the PHASE-0 and PHASE-1 periods formally ungated for principle-without-gate violations.**

ADR-0008 §2: "`gate-coverage` walks every ADR and every principle in ARCHITECTURE.md §1 and verifies that at least one entry in the table above references it. A missing reference fails the build." ADR-0008 Compliance: "`gate-coverage` is the meta-gate that makes this ADR self-enforcing." ADR-0008 Compliance also states: "PHASE-1 and PHASE-2 implement the gates." PHASE-2 scope item 4 lists `gate-coverage` as one of the gates promoted from placeholder to real. This means during PHASE-0 and PHASE-1, `gate-coverage` is a placeholder that exits 0 — so adding a principle without a gate is undetected by CI during those phases. The self-enforcing claim is conditional on PHASE-2 being complete, but the claim is stated unconditionally. The compressor cannot preserve the unconditional claim and also the phase-gate delivery timeline without producing a contradiction.

---

**DISTILL-14** | PROCESS

**The commit trailer `Requirements:` field accepts a list of REQ-IDs, but `Tests-Status:` is a single value — creating an ambiguity when a commit covers requirements at different test statuses.**

ADR-0005 §3 specifies: `Tests-Status: <none|red|red→green|green|deprecated>`. The field is singular. But a commit can simultaneously add a red test for REQ-A and turn REQ-B green (a common pattern in integrated commits). No document addresses how to encode a mixed-status commit. The `Requirements:` field allows multiple IDs (`REQ-X-NNNN[, REQ-Y-NNNN, ...]`) suggesting a single commit may touch multiple requirements. The `Tests-Status:` field has no list form. A compressor attempting to produce the trailer schema must either invent a list encoding (not in any document) or assert the single-value rule (which is incomplete). CLAUDE.md inherits this ambiguity verbatim: it restates the trailer format without resolving it.

---

**DISTILL-15** | PROCESS

**PHASE-5 scope contains two items both numbered `4`, making the scope list non-enumerable and exposing an authoring defect that resists mechanical processing.**

PHASE-5 scope lists items 1, 2, 3, then two items labeled `4` (per-project BMAD output isolation and test suite across all four tiers), then items 5 and 6. A compressor building a canonical deliverable list for PHASE-5 must either drop one item (lossy) or renumber (not authorized without an amendment). This is a minor authoring defect, but it reveals a pattern: PHASE-5 is the phase where no prior phase has validated the format, so it carries the accumulated drift of all earlier phases. The duplicate `4` is the visible symptom of a more systemic problem: phase files have no format lint gate (none of the gates in ADR-0008 validate phase file structure), so authoring errors in phase files are undetected until a human tries to act on them.
