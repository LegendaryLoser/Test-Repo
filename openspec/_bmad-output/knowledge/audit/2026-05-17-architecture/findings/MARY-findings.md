# MARY — persona-mary-analyst (opus) — Wave 3

**Source transcript:** [`raw-transcripts/MARY-agent-a41bb283f821c8a53.jsonl`](../raw-transcripts/MARY-agent-a41bb283f821c8a53.jsonl)
**Sub-agent description:** `Mary analyst persona solo`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `a41bb283f821c8a53`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-agent-analyst` skill via the Skill tool to load Mary, the BMAD business analyst persona. Then, AS Mary, review the architecture artifact below from a requirements-clarity perspective.

This is NOT an interactive conversation. Load the persona, then produce Mary's report as a single output.

Documents (all under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- openspec/architecture/decisions/ADR-0001 through ADR-0008
- openspec/architecture/phases/PHASE-0 through PHASE-5

Mary's perspective is: "Are the requirements precise, unambiguous, testable, and complete?"

Focus areas:
- Which "requirements" are actually statements of intent or design philosophy rather than testable assertions?
- Where are quantifiers, thresholds, or boundary conditions left ambiguous?
- Which acceptance criteria are subjective vs objective?
- Where does the same concept get defined differently in different ADRs?
- Which REQs lack measurable outcomes?
- What requirements are implied but never stated?
- Where would the requirements pass a casual read but fail under hostile interpretation (e.g., a contractor implementing literally what's written)?
- What is the requirements-discipline gap between what the artifact preaches (ADR-0004 §3 atomicity) and what it practices (REQ-ARCH-*)?

REQUIRED OUTPUT:
- Stable IDs: prefix `MARY-` (e.g. MARY-CRIT-01)
- 3 severity tiers: CRITICAL / SERIOUS / PROCESS
- MINIMUM 15 findings
- Speak in first-person as Mary
- 1500-2500 words
- No preamble

Do not read files outside the 15 listed.
```

## Findings deliverable (final assistant message)

I have everything I need. Now producing Mary's report.

---

📊 *Mary, Business Analyst — Requirements Clarity Review of the Frozen Architecture Artifact*

I have walked the architecture artifact and its eight ADRs and six phase files with a single question in front of me: would a hostile contractor, paid by the hour, be able to deliver something I have to accept as compliant while violating the spirit of every principle? The answer is yes, in at least fifteen places. Below is my findings register.

---

**MARY-CRIT-01 — REQ-ARCH-0001 is not testable as written.**
The requirement reads "Repository contains the top-level layout in §3 (no extra top-level directories without an ADR)." Section 3 is a 60-line ASCII tree containing comments, optional slots, and a `<project>/` placeholder. There is no enumerated, machine-readable list of required-vs-optional-vs-forbidden top-level entries. A contractor can produce a layout that matches some subsections, omit others (`.gitignore`? `pyproject.toml`?), and argue compliance. The requirement needs a normative allowlist file (e.g. `tools/spec_lint/allowlist.yaml`) referenced by ID, not a prose tree.

**MARY-CRIT-02 — REQ-ARCH-0007 is unverifiable without a canonical principle text.**
"CLAUDE.md references the five principles in §1 verbatim." Verbatim against what string? `ARCHITECTURE.md` §1 contains the principles formatted as a numbered list with bold labels and prose elaborations. CLAUDE.md repeats them with slightly different punctuation and bold placement. A "verbatim" check will fail or pass depending on whether bold, numbering, and trailing parentheticals are normalized. The principle text must be extracted to a single canonical file (`openspec/architecture/principles.md` or YAML) and both documents must include-by-reference, or the gate is undefined.

**MARY-CRIT-03 — REQ-ARCH-0002 conflates "present" with "valid."**
"ADR-0001 through ADR-0008 plus PHASE-0 through PHASE-5 are all present." Present as files of any content? An empty file with the right name passes. The requirement must specify frontmatter validity, required sections, and minimum content discriminators. Otherwise REQ-ARCH-0002 is a `ls`-equivalence check masquerading as architecture conformance.

**MARY-CRIT-04 — Atomicity is preached by ADR-0004 §3, violated by REQ-ARCH-0001 itself.**
ADR-0004 §3 declares "One REQ contains one assertion. Compound requirements ('the system must do A and B') are split." Yet REQ-ARCH-0001 asserts two things in one breath: (a) layout matches §3, (b) no extra top-level directories without an ADR. That is the textbook compound the rule forbids. REQ-ARCH-0002 is worse — it conjoins eight ADRs and six phase files into a single assertion. By the lint that PHASE-1 promises to ship, the architecture's own requirements would fail `compound-requirement-detector`. This is a requirements-discipline gap the artifact cannot survive its own gates.

**MARY-CRIT-05 — REQ-ARCH-* lacks the frontmatter ADR-0004 §5 mandates.**
ADR-0004 §5 specifies a per-REQ block format with YAML frontmatter (`id`, `revision`, `status`, `introduced`, `phase`, `tier`, `references.epic`, `references.story`, `references.adrs`). REQ-ARCH-0001 through REQ-ARCH-0008 are bullet points in prose with no frontmatter. They cannot be parsed by the index builder, cannot be assigned a tier, cannot be linked to an Epic or Story, and cannot be promoted to `tests-green` by any of the rules described. Either REQ-ARCH-* is exempt (and that exemption must be a named, ADR-bound carve-out) or these requirements are non-conformant. Today the artifact has it both ways.

**MARY-CRIT-06 — "Statistical assertions" never quantifies a threshold.**
ADR-0007 §3 permits "Distributional assertions over N runs. Sample size declared; assertion is a confidence interval, Kolmogorov–Smirnov test, or similar. Sample size and threshold are pinned per test." No global floor exists for N, no minimum confidence level, no policy on whether N=3 with a 50% CI satisfies P2. A contractor will choose N=2 and a 50% CI to keep token cost down and pass review. The ADR must pin defaults (e.g. N ≥ 30, α = 0.05) and an override-with-justification mechanism.

**MARY-CRIT-07 — `anti-aliasing` threshold is unspecified at the ADR layer.**
ADR-0004 §4 says "Pairs above a threshold are a lintable defect. The threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly." There is no default value, no method for choosing it, no calibration procedure, no false-positive tolerance, and no rule for the quarterly review's acceptance criteria. The requirement is a "we will know it when we see it" promise. A reviewer cannot test whether the threshold is correct.

**MARY-CRIT-08 — `cache-hit-regression` "pinned threshold" is named but never set.**
ADR-0007 §5 invokes a "pinned threshold" for cache hit rate. ADR-0008 wires the gate. Neither document pins the threshold or the methodology (rolling window, comparison baseline, exclusions for cold-start runs). PHASE-3 exit criteria simply says "baseline established" — that is a verb, not a number. A contractor establishes baseline = 0%; the gate forever passes. The threshold and the baseline-derivation procedure must be specified normatively.

---

**MARY-SERIOUS-09 — "Cosmetic edits" is undefined in ADR-0004 §7.**
"Cosmetic edits (typo, grammar) bump `revision` and are allowed only if no downstream artifact refers to the prior revision body." Where is the boundary between cosmetic and material? Is "should" → "must" cosmetic? Is reordering bullets cosmetic? Is replacing "user" with "actor" cosmetic? Without a decision table or an explicit governance reviewer, every edit becomes a debate. I recommend an explicit non-cosmetic list (modal verb changes, numeric thresholds, identifier additions, acceptance criterion edits) so the default is "material unless on the list."

**MARY-SERIOUS-10 — "Material change" is defined circularly in two places.**
ADR-0004 §1 says "Material change to a requirement produces a new REQ with `supersedes`." ADR-0004 §7 says "Material edits create a new REQ." Neither defines what *material* is, and §7's definition of "cosmetic" is exclusionary rather than constructive. This is the same concept defined twice without alignment — exactly the kind of cross-document inconsistency P1 forbids.

**MARY-SERIOUS-11 — "Real adapter" is defined inconsistently across ADR-0003, ADR-0006, and ADR-0007.**
ADR-0003 §2: "Node unit tests inject a *different real* adapter (e.g. a Sheets adapter that hits a dedicated test spreadsheet via the Sheets REST API)." ADR-0006 §2: permits "Substituting the **HTTP transport** at the network boundary (e.g. a real `nock` interceptor that records and replays *real* responses captured from the real service)." These two definitions disagree. A `nock` replay against captured responses is not "real-for-real" the way a REST call against a live test spreadsheet is — it is a recorded fixture played back, which ADR-0007 §2 explicitly bans for the LLM tier. The artifact tolerates recorded fixtures in HTTP unit tests while banning them in stochastic tests. The boundary needs a single, ADR-level definition of "real adapter" and an explicit map of which tier permits which substitution.

**MARY-SERIOUS-12 — "Deterministic" is asserted without a definition.**
ADR-0005 §2: "`tools/trace/rebuild.py` regenerates the cache deterministically." Deterministic over what? Same inputs, same OS, same Python minor, same hash seed? Cross-platform? Locale-stable? Time-zone-stable? Order-stable on disk listings? The PHASE-2 exit-criteria property test "rebuild(rebuild(x)) == rebuild(x)" is idempotence, not determinism. The two are different, and the artifact uses them interchangeably.

**MARY-SERIOUS-13 — REQ-ARCH-0006 has a malleable boundary.**
"No file under `openspec/architecture/` contains executable code or test code." What counts as executable? A bash snippet in a fenced block? A YAML pipeline definition? An ADR shows shell pseudocode in §6 of ADR-0005 — the table of hooks references `.py` files. A contractor could embed a one-line shell script in a markdown fence and argue it is documentation, not code. The requirement needs an explicit file-extension list and a "fenced-code-blocks are exempt" carve-out, or it needs to be rephrased as "no `*.py`, `*.ts`, `*.sh`, `*.js` files."

**MARY-SERIOUS-14 — REQ-ARCH-0003 is satisfiable by an empty directory.**
"`openspec/vision.md`, `openspec/briefs/`, `openspec/prd/`, `openspec/epics/`, `openspec/stories/` exist with empty templates only (no product content)." What is the negative-presence test for "no product content"? A two-paragraph "TBD" note is product content under one reading and template scaffolding under another. PHASE-0 §4 names a `_TEMPLATE.md` per directory — REQ-ARCH-0003 doesn't reference those template filenames. Either the requirement should say "exactly the files `_TEMPLATE.md` exist and contain only the documented placeholder text" or it should be replaced with a content-fingerprint assertion.

**MARY-SERIOUS-15 — REQ-ARCH-0008 implementation contract is fictional in PHASE-0.**
"`.claude/settings.json` is present; hooks declared in ADR-0005 are listed (implementations land in PHASE-2)." The requirement says "listed" — listed how? By the event name? By the script path? PHASE-0 §9 says hooks "point at placeholder commands that exit 0 with a TODO comment." A placeholder command path that exits 0 is indistinguishable from a real implementation that does nothing. The requirement needs a discriminator (e.g. the placeholder script must echo a specific sentinel string the test asserts on) so PHASE-0 cannot be confused with PHASE-2.

**MARY-SERIOUS-16 — Push-invariant safety net has a silent-failure escape hatch.**
ADR-0005 §6 amendment 0001 / §8: "residual loss only if both hooks fail to fire (e.g. abrupt container reclaim mid-`PostToolUse`)." The residual-loss case is acknowledged but not requirement-bound. There is no REQ saying "container reclaim mid-hook produces a recoverable artifact via mechanism X." A reviewer cannot determine whether this gap is accepted, mitigated, or simply unsolved. Either it is accepted (then an ADR must say so, with the loss budget) or it is mitigated (then a REQ must name the mechanism).

**MARY-SERIOUS-17 — "Coverage = 100%" is gamed by zero requirements.**
ADR-0006 §5: "**REQ coverage = 100%.** Every non-deprecated REQ has ≥ 1 passing test for its declared tier." At PHASE-0, there are zero non-deprecated REQs that conform to the spec format (per MARY-CRIT-05). 100% of zero is 100%. The gate trivially passes. The requirement must specify a minimum corpus floor below which the gate is "not applicable" rather than "passing" — otherwise PHASE-0 ships with a green coverage gate that means nothing.

**MARY-SERIOUS-18 — "Bulk green-starts" threshold N is unset.**
ADR-0006 §4: "CI gate `bulk-green-start` flags any commit adding > N green tests without the trailer." N is a free variable. A contractor sets N = 10,000 and the gate fires never. The threshold must be pinned in the ADR or in a referenced configuration with an ADR-bound default.

---

**MARY-PROCESS-19 — REQ-ARCH-* are not addressable by the artifact's own ID-plus-path discipline.**
ADR-0004 §2 mandates "ID plus file path" cross-references. REQ-ARCH-0001 lives inside `ARCHITECTURE.md` §10 — there is no `openspec/specs/_meta/architecture.spec.md` containing them. The canonical home column in §4 says "`openspec/architecture/ARCHITECTURE.md` §10," which is a section reference, not a file path to a spec block. The artifact violates its own cross-reference discipline for the very requirements it uses to bootstrap PHASE-0.

**MARY-PROCESS-20 — Phase entry criteria are non-machine-checkable for PHASE-0.**
PHASE-0 entry: "Repository has only `README.md` and `.git/`. Branch `claude/general-session-KXgas` exists." This is satisfied at one historical commit and falsified at every commit thereafter. Once PHASE-0 work begins, the entry criterion is no longer true, and a re-run of the phase-gate logic cannot evaluate it. Entry criteria should be expressed as predicates over the *PR proposing the phase*, not over the current `HEAD`.

**MARY-PROCESS-21 — "Reviewed quarterly" has no calendar owner.**
ADR-0004 §4: the anti-aliasing threshold "is reviewed quarterly (a `gate`-type task)." Owned by whom? Triggered by what? Tracked where? A quarterly task with no calendar entry and no owner is a wish, not a requirement. Either name the role responsible and the cadence enforcement mechanism (a scheduled CI job that opens an issue) or remove the promise.

**MARY-PROCESS-22 — "Pinned per test" is a wide latitude that needs a default.**
ADR-0007 §3 says sample size and threshold are "pinned per test." With no default, every test author re-invents the wheel and reviewers have no standard. There should be a default sample-size table by assertion class (schema invariants: N=1; distributional: N≥30 with α=0.05; idempotence: N≥10) and explicit override syntax.

---

**Summary, in Minto pyramid form.**

*Governing thought.* The artifact preaches requirements discipline that it does not yet practice. It mandates atomic, frontmatter-annotated, ID-addressed, threshold-pinned, statistically-gated requirements — and then ships eight architectural requirements that are compound, prose-only, section-addressed, and threshold-free. The gates that PHASE-1 and PHASE-2 will build are well-specified at the level of intent; they are unbuildable from the current REQ wording because the REQs do not yet conform to the spec-storage discipline that those gates will enforce.

*Supporting arguments.* (1) Six of the eight REQ-ARCH-* assertions fail their own atomicity or testability rules. (2) Three central technical concepts — "material," "real adapter," "deterministic" — are defined inconsistently across ADRs. (3) At least four numerical thresholds (anti-aliasing similarity, cache-hit baseline, bulk-green N, stochastic sample size) are named without values. (4) Two requirements (REQ-ARCH-0003, REQ-ARCH-0006) have malleable boundaries that a literal-minded contractor can satisfy in spirit-violating ways.

*Recommended next move.* Before PHASE-0 declares exit, lift REQ-ARCH-* into `openspec/specs/_meta/architecture.spec.md` with conformant frontmatter, split every compound assertion, pin every threshold to a default value with a named owner for revisions, and resolve the "real adapter" definition mismatch with a single ADR addendum.

I have stayed inside the fifteen documents and have written nothing to disk. Findings above are the deliverable. — Mary.
