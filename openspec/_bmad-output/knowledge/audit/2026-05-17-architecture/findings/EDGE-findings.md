# EDGE — edge-case-hunter (opus) — Wave 1

**Source transcript:** [`raw-transcripts/EDGE-agent-abf3f95219d0706c3.jsonl`](../raw-transcripts/EDGE-agent-abf3f95219d0706c3.jsonl)
**Sub-agent description:** `Edge-case hunter review`
**Session ID:** `82ac77b3-a37e-41a2-bb48-489a4c5d66af`
**Agent ID:** `abf3f95219d0706c3`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Invoke the `bmad-review-edge-case-hunter` skill via the Skill tool. Apply it to architecture documents (not code) — walk every branching path, status transition, phase entry/exit condition, hook firing window, boundary condition, and special-case carve-out described in the documents, and flag unhandled cases.

Documents (all under /home/user/Test-Repo/):

1. openspec/architecture/ARCHITECTURE.md
2-9. openspec/architecture/decisions/ADR-0001 through ADR-0008 (.md files)
10-15. openspec/architecture/phases/PHASE-0 through PHASE-5 (.md files)

Edge-case categories to specifically hunt:
- Status transitions: REQ status enum (draft|tests-red|tests-green|reviewed|merged|deprecated) — every transition pair, especially backward/forbidden ones.
- Phase entry/exit conditions — what happens when entry condition is partially satisfied, or one phase's exit changes the next phase's entry.
- Hook firing windows — what if a hook fires before/after the expected event, or during a crash, or twice, or never.
- Trailer combinations — what if a commit has Checkpoint:true AND Bootstrap:reason? What if it has Material-Architecture-Change:true and no ADR?
- Identifier allocation races — two concurrent allocations of REQ-X-NNNN.
- Cross-reference rot — REQ-ID @ file/path where the path has been renamed, the REQ has been deprecated, the file no longer contains the ID.
- Amendment-log corner cases — amendment of an amendment, amendment that contradicts a prior amendment, multiple concurrent amendments.
- Checkpoint commit corner cases — checkpoint between red and green commits; checkpoint as the first commit on a branch; checkpoint with a non-checkpoint commit between it and the green.
- Per-project openspec overlay — same REQ-ID allocated at root and at project; precedence.
- Match-fail asymmetry — gate that silently passes on missing data vs gate that fails closed.

REQUIRED OUTPUT:
- Stable IDs: prefix `EDGE-` (e.g. EDGE-01, EDGE-02; severity inline as CRITICAL/SERIOUS/PROCESS)
- Each finding: scenario description, the unhandled branch, the specific file/section that fails to handle it, and what breaks
- Minimum 15 unhandled edges
- 1500-2500 words
- No preamble, no fixes

Do not read files outside the 15 listed. Do not read CLAUDE.md, STATUS.md, or tools/.
```

## Findings deliverable (final assistant message)

Now I have all 15 documents. Let me perform exhaustive path analysis on every branching condition, status transition, hook window, and boundary across these documents.

```json
[
  {
    "location": "ADR-0004 §5 + ADR-0006 §4: status enum vs Tests-Status trailer enum",
    "trigger_condition": "REQ status enum and commit Tests-Status enum overlap incompletely; mapping unspecified",
    "guard_snippet": "Define explicit mapping table: REQ.status transitions <-> allowed Tests-Status trailer values (e.g. tests-red REQ requires Tests-Status: red)",
    "potential_consequence": "EDGE-01 CRITICAL: a commit with Tests-Status: green can land while REQ.status is still draft, bypassing the draft->tests-red->tests-green progression in ADR-0005 §4"
  },
  {
    "location": "ADR-0005 §4 transition rules",
    "trigger_condition": "REQ marked reviewed or merged then needs corrective edit; no transition path defined",
    "guard_snippet": "Add rules covering: tests-green->reviewed->merged, plus the only-deprecate-then-supersede rule for merged REQs",
    "potential_consequence": "EDGE-02 CRITICAL: reviewed and merged statuses appear in ADR-0004 §5 enum but ADR-0005 §4 only forbids draft->green and re-activation of deprecated, leaving reviewed/merged transitions wholly unguarded"
  },
  {
    "location": "ADR-0005 §4 + ADR-0006 §4",
    "trigger_condition": "Test flips green->red after a flake, then green again; second green has no red predecessor in the new run",
    "guard_snippet": "validate_commit.py must accept re-green if any prior commit on branch ever held the test red, not require the immediately prior commit",
    "potential_consequence": "EDGE-03 SERIOUS: red-before-green walks history, but rule is ambiguous about whether 'preceded by at least one' allows a green->red->green sequence; ambiguity becomes silent acceptance or false rejection"
  },
  {
    "location": "ADR-0005 §6 hook table + §7 checkpoint description",
    "trigger_condition": "Stop hook fires twice (e.g. container suspend then resume both trip Stop) producing duplicate checkpoint commits",
    "guard_snippet": "checkpoint.py must check `git log -1 --format=%s` for 'wip: checkpoint <session-id>' before creating another; squash or skip",
    "potential_consequence": "EDGE-04 PROCESS: duplicate checkpoints accumulate, the 'next non-checkpoint commit responsible for restoring P4' rule cannot resolve which checkpoint to squash against"
  },
  {
    "location": "ADR-0005 §6 PostToolUse(Bash:git commit)",
    "trigger_condition": "Commit succeeds but PostToolUse hook crashes before journal_commit appends event",
    "guard_snippet": "rebuild.py must reconcile git log against journal and back-fill missing `commit` events on next run with provenance=reconstructed",
    "potential_consequence": "EDGE-05 SERIOUS: ADR-0005 §8 claims 'rebuild fills missing journal entry' but rebuild.py spec in PHASE-2 only lists idempotence/torn-line tests, not back-fill of missing commit events"
  },
  {
    "location": "ADR-0005 §7 + ADR-0008 §6",
    "trigger_condition": "Branch starts with a checkpoint commit (e.g. session opens, immediate Stop)",
    "guard_snippet": "checkpoint.py must refuse first-commit-on-branch checkpoint, or mark with Bootstrap: branch-init for the gate to skip",
    "potential_consequence": "EDGE-06 SERIOUS: 'next non-checkpoint commit responsible for restoring P4 compliance' has no anchor when the checkpoint is the only/first commit; subsequent green commit cannot prove red-before-green"
  },
  {
    "location": "ADR-0005 §7 + ADR-0006 §4",
    "trigger_condition": "Checkpoint commit inserted between the red and green commits of a test",
    "guard_snippet": "validate_commit.py must ignore Checkpoint:true commits when walking history for red-before-green",
    "potential_consequence": "EDGE-07 CRITICAL: Checkpoint:true skips gates but ADR-0006 §4 says validator 'walks history' — it is unspecified whether checkpoint commits are transparent to the walk; false rejections likely"
  },
  {
    "location": "ADR-0006 §4 Bootstrap trailer + ADR-0005 §7 Checkpoint trailer",
    "trigger_condition": "Commit carries both Checkpoint:true and Bootstrap:<reason>",
    "guard_snippet": "Define trailer precedence; reject combinations: Checkpoint+Bootstrap, Checkpoint+Material-Architecture-Change, Checkpoint+Skill-Removal-Acknowledged",
    "potential_consequence": "EDGE-08 SERIOUS: nothing in ADR-0005, ADR-0006, or ADR-0008 §6 forbids stacking exemption trailers, allowing a single commit to bypass all of: P4, bulk-green-start, and material-architecture review"
  },
  {
    "location": "ARCHITECTURE.md line 12-13 + ADR-0008 §1 gate table",
    "trigger_condition": "Commit carries Material-Architecture-Change: true but no ADR in the diff",
    "guard_snippet": "Add gate `material-arch-needs-adr`: trailer true implies diff under openspec/architecture/decisions/ADR-*.md",
    "potential_consequence": "EDGE-09 CRITICAL: ARCHITECTURE.md asserts the trailer triggers a Phase-0 re-gate, but ADR-0008 §1 has no gate verifying the trailer is honest; agent can self-declare and bypass review"
  },
  {
    "location": "ADR-0004 §1 identifier allocation",
    "trigger_condition": "Two concurrent PRs both run `spec_lint allocate <domain>` and allocate the same REQ-X-0042",
    "guard_snippet": "Treat allocation as advisory; rely on a PR-time `req-id-collision` gate that fails the second merger with reallocation instructions",
    "potential_consequence": "EDGE-10 CRITICAL: monotonic next-free scan against INDEX.yaml is local; concurrent allocation produces duplicate immutable IDs, which then cannot be renamed (rule forbids)"
  },
  {
    "location": "ARCHITECTURE.md §4 + ADR-0001 + ADR-0004 §1",
    "trigger_condition": "Same REQ-ID allocated at root openspec/specs/ and at projects/<p>/openspec/ overlay",
    "guard_snippet": "Spec_lint must scan project overlays and fail on duplicate REQ-IDs across overlays; or define overlay precedence + namespacing (REQ-PROJ-NAME-DOMAIN-NNNN)",
    "potential_consequence": "EDGE-11 CRITICAL: ADR-0001 says 'project specs extend root specs by reference; no duplication' but the overlay mechanism is undefined; same REQ-ID can resolve to two different bodies in two paths"
  },
  {
    "location": "ADR-0004 §2 cross-reference discipline",
    "trigger_condition": "REQ-ID is valid but file path renamed (e.g. domain rename) — `xref-resolves` evaluates path that no longer exists",
    "guard_snippet": "xref-resolves must accept canonical-by-ID lookups via INDEX.yaml; flag stale paths separately from missing IDs",
    "potential_consequence": "EDGE-12 SERIOUS: every old commit/document references REQ-X-NNNN @ old/path; ADR-0004 forbids renames of ID but not of file path; bulk path renames silently break every prior reference"
  },
  {
    "location": "ADR-0004 §1 + §7 supersession + ADR-0008 `xref-resolves`",
    "trigger_condition": "Document references REQ-X-NNNN that is now status:deprecated and superseded_by REQ-X-NNNN+5",
    "guard_snippet": "Distinguish reference-to-active vs reference-to-deprecated; require references to deprecated REQs to be replaced or carry a `historical-reference` annotation",
    "potential_consequence": "EDGE-13 SERIOUS: a reference resolves syntactically but points to a deprecated REQ; coverage calculations may double-count or miss the superseding REQ"
  },
  {
    "location": "ADR-0002 amendment log + ADR-0005 amendment log",
    "trigger_condition": "Amendment 0002 contradicts Amendment 0001 (e.g. 0001 introduces hook, 0002 removes it)",
    "guard_snippet": "Amendments must include `affects-amendment: 0001` field and either `supersedes` or `extends`; lint rule forbids silent contradiction",
    "potential_consequence": "EDGE-14 SERIOUS: ADR-0002 says 'A subsequent material change to behavior introduced by a prior amendment requires a new amendment row, never an edit to a prior row' but no mechanism distinguishes additive from contradictory amendments; readers must mentally merge"
  },
  {
    "location": "ADR-0002 amendment log",
    "trigger_condition": "Two amendments to the same ADR opened concurrently and assigned amendment 0003 in parallel",
    "guard_snippet": "Treat amendment number like REQ-ID: allocate at merge, not at draft; reject second merge with renumber instructions",
    "potential_consequence": "EDGE-15 PROCESS: amendment IDs use the same monotonic counter risk as REQ-IDs but the ADR provides no allocation discipline; collisions produce two amendment-0003 rows"
  },
  {
    "location": "ADR-0005 §6 PostToolUse(Bash:git commit) push step",
    "trigger_condition": "Push fails because remote rejected non-FF; hook 'aborts with a diagnostic (no force-push)' but the commit is already in local history",
    "guard_snippet": "On non-FF abort, hook must also create a recovery instruction file or block further commits until the divergence is resolved",
    "potential_consequence": "EDGE-16 CRITICAL: agent receives only a diagnostic, may continue committing on top of unpushed work; the push invariant is silently violated for every subsequent commit until manual intervention"
  },
  {
    "location": "ADR-0005 §6 PostToolUse(mcp__github__merge_pull_request)",
    "trigger_condition": "Working branch was deleted on merge (default GitHub behavior) when post_merge_sync.py runs",
    "guard_snippet": "post_merge_sync.py must detect deleted-on-merge and switch to main/default branch instead of failing to FF a nonexistent ref",
    "potential_consequence": "EDGE-17 SERIOUS: post_merge_sync assumes working branch still exists upstream; deleted branches make `git fetch + FF` fail and the push invariant 'enforcement surface' silently rots"
  },
  {
    "location": "ADR-0005 §6 hook table — hook firing during crash",
    "trigger_condition": "Container reclaimed mid-`PostToolUse(Bash:git commit)`, after commit but before push",
    "guard_snippet": "SessionStart hook must detect `@{u}..HEAD` non-empty and push before printing the resume report",
    "potential_consequence": "EDGE-18 SERIOUS: ADR-0005 §8 lists this as 'residual loss only if both hooks fail to fire' but the SessionStart resume hook is not enumerated as a push-invariant enforcement surface; recovery is left to luck"
  },
  {
    "location": "ADR-0005 §5 journal_events table — torn-line policy",
    "trigger_condition": "Crash writes a non-malformed but semantically incomplete event (e.g. tests_run with passed but no failed field)",
    "guard_snippet": "Parser must validate against per-event schema, not just JSONL well-formedness; reject schema-invalid lines with provenance loss flag",
    "potential_consequence": "EDGE-19 SERIOUS: ADR-0005 §5 says 'partial writes from a crash are discarded by the parser (the line is malformed and ignored)' but a partial write that completes after a comma boundary is still valid JSON; it survives parsing with missing fields"
  },
  {
    "location": "ADR-0008 §3 phase-exit gate",
    "trigger_condition": "Current phase's exit REQs are tests-green, but a REQ from a *prior* phase regresses to tests-red",
    "guard_snippet": "phase-exit must verify all REQs from current and prior phases are tests-green, not only current-phase exit REQs",
    "potential_consequence": "EDGE-20 CRITICAL: gate only checks current-phase exit REQs + 'no later-phase REQ green' + next-phase ADR accepted; prior-phase regression is invisible to phase-exit"
  },
  {
    "location": "ADR-0008 §3 phase-exit gate",
    "trigger_condition": "A later phase has no entry ADR (phase exit references 'next phase entry ADR if any')",
    "guard_snippet": "Define which phases require an entry ADR vs which inherit from prior; current spec 'if any' silently permits skipping",
    "potential_consequence": "EDGE-21 PROCESS: 'if any' carve-out makes the check pass for any phase whose author omitted to define an entry ADR — match-fail asymmetry favoring silent pass"
  },
  {
    "location": "PHASE-0 entry + PHASE-1 entry + ADR-0008 §3",
    "trigger_condition": "PHASE-0 entry says 'Repository has only README.md and .git/' but PHASE-0 itself adds CLAUDE.md, ADRs, etc.; partial entry satisfaction unhandled",
    "guard_snippet": "Distinguish 'entry-at-start' from 'entry-on-resume'; allow resuming PHASE-0 with partial scope present",
    "potential_consequence": "EDGE-22 PROCESS: a session restarting PHASE-0 mid-flight finds README + ADRs + CLAUDE.md present and the entry condition is literally false; phase cannot legitimately re-enter"
  },
  {
    "location": "PHASE-1 §Scope item 4 + ADR-0002 amendment 0001",
    "trigger_condition": "PHASE-1 scope lists `.claude/agents/` and `.claude/commands/` wrappers; ADR-0002 amendment 0001 drops the wrapper-isolation strategy entirely",
    "guard_snippet": "Update PHASE-1 scope to remove wrapper items, or add explicit deprecation note pointing to amendment",
    "potential_consequence": "EDGE-23 CRITICAL: phase scope contradicts current ADR; entry/exit becomes ambiguous — does PHASE-1 require wrappers (per PHASE-1.md) or forbid them (per ADR-0002 amendment 0001)?"
  },
  {
    "location": "PHASE-1 §Exit + ADR-0002 §Compliance",
    "trigger_condition": "PHASE-1 exit requires 'BMAD wrapper files in .claude/agents/ and .claude/commands/ resolve their Load: paths' but ARCHITECTURE.md §3 marks those directories '(legacy slot — empty in v6 native-skills model)'",
    "guard_snippet": "Remove the wrapper exit clause from PHASE-1; replace with .claude/skills/ population check",
    "potential_consequence": "EDGE-24 CRITICAL: PHASE-1 cannot exit because the exit predicate references files that ARCHITECTURE.md says should be empty"
  },
  {
    "location": "PHASE-1 §Scope item 3 ('bmad/' install) vs ARCHITECTURE.md §3 + ADR-0002 (`_bmad/`)",
    "trigger_condition": "PHASE-1 references 'bmad/' but architecture and ADR use '_bmad/' (underscore-prefixed)",
    "guard_snippet": "Rename references in PHASE-1 from bmad/ to _bmad/, or vice versa; one canonical name only",
    "potential_consequence": "EDGE-25 SERIOUS: bmad-direct-reference lint rule (ADR-0002 §Compliance) checks against `_bmad/`; PHASE-1 scope references `bmad/`; the gate evaluates a path that does not exist and silently passes"
  },
  {
    "location": "PHASE-0 §Scope items 9 (.claude/settings.json) + ADR-0005 §6 amendment 0001",
    "trigger_condition": "PHASE-0 declares hooks 'from ADR-0005 §6' but amendment 0001 added new hooks; REQ-ARCH-0008 unclear whether it covers amended set",
    "guard_snippet": "REQ-ARCH-0008 must explicitly enumerate amendment-introduced hooks (post_merge_sync, extended checkpoint push) or reference amendment log",
    "potential_consequence": "EDGE-26 SERIOUS: a PHASE-0 reading the original §6 satisfies REQ-ARCH-0008; the amendment hooks are absent from declarations and never land in PHASE-2, breaking the push invariant"
  },
  {
    "location": "PHASE-2 §Scope + ADR-0005 §6 hook table",
    "trigger_condition": "PostToolUse(Edit|Write) hook fires on Read tool when the tool returns and writes a journal event — pattern ambiguity",
    "guard_snippet": "Specify exact tool name match (Edit, Write, NotebookEdit); exclude Read explicitly",
    "potential_consequence": "EDGE-27 PROCESS: `PostToolUse(Edit|Write)` glob is informal; matchers in settings.json may catch unrelated tools, polluting file_touch events"
  },
  {
    "location": "ADR-0005 §6 PostToolUse(Bash:*test*)",
    "trigger_condition": "Bash command contains 'test' in non-test context (e.g. `cat README.md | grep contest`)",
    "guard_snippet": "Match anchored: `(npm|pytest|jest|vitest|node --test) ...` not glob `*test*`",
    "potential_consequence": "EDGE-28 SERIOUS: journal_tests.py is invoked for non-test commands, attempts to parse non-test output, may produce false tests_run events that corrupt matrix"
  },
  {
    "location": "ADR-0007 §4 + ADR-0008 §1 cost-budget gate",
    "trigger_condition": "Stochastic test has no @cost-budget annotation",
    "guard_snippet": "stochastic-tier-bans must additionally enforce presence of @cost-budget; treat absence as fail-closed (assume infinite cost)",
    "potential_consequence": "EDGE-29 SERIOUS: ADR-0007 §4 says 'tests carry annotation' but neither §2 nor §Compliance gates its presence; missing annotation fails open, test runs with unbounded budget"
  },
  {
    "location": "ADR-0007 §2 + §3",
    "trigger_condition": "Sandwich layer is deterministic and asserts exact equality post-LLM; appears to violate §2 exact-equality ban",
    "guard_snippet": "Clarify exception scope: exact-equality forbidden against raw LLM text; permitted against deterministic sandwich output",
    "potential_consequence": "EDGE-30 PROCESS: §2 forbids exact-equality against generated text; §3 sandwich-layer permits assertions on composed output; lint cannot distinguish, will either over-fire or under-fire"
  },
  {
    "location": "ADR-0006 §2 substitution carve-out + ADR-0007 §2 ban on recorded fixtures",
    "trigger_condition": "ADR-0006 permits nock 'records and replays real responses' for cost reasons; ADR-0007 forbids 'recorded response fixtures replayed in lieu of real API calls'",
    "guard_snippet": "ADR-0006 §2 must explicitly exclude the LLM tier from the nock carve-out; reconcile language",
    "potential_consequence": "EDGE-31 SERIOUS: language is 'never for the LLM tier' in ADR-0006 §2, but the boundary between LLM tier and integration tests of LLM-adjacent code is undefined; tests using anthropic-client adapter could replay fixtures legally"
  },
  {
    "location": "ADR-0008 §1 + §5 — index-up-to-date gate",
    "trigger_condition": "Pre-commit hook rewrites INDEX.yaml; gate also runs on PR; PR-time rebuild produces different INDEX (e.g. timestamp differences)",
    "guard_snippet": "rebuild must be deterministic (sorted keys, no timestamps); CI must compare canonical-form not byte-form",
    "potential_consequence": "EDGE-32 SERIOUS: ADR-0004 §6 says 'auto-generated' but does not specify determinism guarantees; pre-commit and PR-time rebuilds may diverge by environment, producing infinite drift loops"
  },
  {
    "location": "ADR-0004 §7 append-only + revision bump",
    "trigger_condition": "Two cosmetic edits race on the same REQ in concurrent PRs; both bump revision to 2",
    "guard_snippet": "revision must be allocated at merge with conflict-detection, not at commit; or use a content-hash instead of integer",
    "potential_consequence": "EDGE-33 PROCESS: concurrent revision bumps create silent shadowing — first-merged revision-2 is overwritten by second-merged revision-2 with different body"
  },
  {
    "location": "ADR-0004 §3 atomicity + spec storage",
    "trigger_condition": "A REQ later determined to be compound is split into REQ-X-NNNN and REQ-X-NNNN+1; the immutability rule forbids changing REQ-X-NNNN",
    "guard_snippet": "Splitting requires deprecating original + creating two new REQs with supersedes pointing to original; document the split protocol",
    "potential_consequence": "EDGE-34 SERIOUS: ADR-0004 §3 says 'compound requirements are split' but §1 forbids material change to existing REQ; the only legal path (deprecate + 2 supersede) is unstated, leading to ad-hoc handling"
  },
  {
    "location": "ADR-0008 §2 gate-coverage",
    "trigger_condition": "Principle text in ARCHITECTURE.md §1 is paraphrased (not verbatim); REQ-ARCH-0007 requires verbatim cite",
    "guard_snippet": "REQ-ARCH-0007 test must hash-compare against the canonical principle list; gate-coverage scans both verbatim form and CLAUDE.md form",
    "potential_consequence": "EDGE-35 SERIOUS: 'references the five principles verbatim' is a string-match assertion with no canonical source; if ARCHITECTURE.md §1 wording drifts vs CLAUDE.md, the gate either fires constantly or is never updated"
  },
  {
    "location": "PHASE-0 exit gate + ADR-0008 §3 phase-exit (current phase REQs all green)",
    "trigger_condition": "PHASE-0 exit gate runs on merge to main; REQ-ARCH-* tests are themselves authored in PHASE-0 'red-first then green'",
    "guard_snippet": "Phase exit must verify the tests turned green via the red-first sequence, not just current-state green; PHASE-0 specifically must allow Bootstrap commits for the initial test corpus",
    "potential_consequence": "EDGE-36 SERIOUS: PHASE-0 cannot satisfy red-before-green for REQ-ARCH-* without a prior red state; but Bootstrap-trailer + bulk-green-start gate (ADR-0006 §4) is the only escape, and PHASE-0 scope does not declare its use"
  },
  {
    "location": "ADR-0002 §7 staging + ADR-0008 §1 lint rules",
    "trigger_condition": "A spec_lint rule (e.g. prose-xref-banned) scans a non-staging file that happens to be inside a directory named _bmad-output elsewhere (e.g. projects/<n>/openspec/_bmad-output/)",
    "guard_snippet": "Lint rule exclusion must match all paths matching glob `**/openspec/_bmad-output/**`, not just root",
    "potential_consequence": "EDGE-37 SERIOUS: ADR-0002 §7 says 'exclude openspec/_bmad-output/' (root path); per-project _bmad-output (PHASE-5/ADR-0002 §9) under projects/<n>/openspec/_bmad-output/ is not covered by the exclusion glob, so lint will fire on per-project drafts"
  },
  {
    "location": "ADR-0002 §9 per-project config + ADR-0001 + PHASE-5 §Scope item 4",
    "trigger_condition": "Session is launched with CWD = repo root while working on projects/<n>/; BMAD resolves to repo-level config, output lands in wrong staging dir",
    "guard_snippet": "Add a gate or pre-tool guard: when editing under projects/<n>/, fail BMAD invocations whose CWD != projects/<n>/",
    "potential_consequence": "EDGE-38 SERIOUS: ADR-0002 §9 says 'sessions working on a project must run with CWD = projects/<name>/'; no enforcement gate exists; default behavior silently writes drafts to the repo-level dir"
  },
  {
    "location": "ADR-0008 §6 + ADR-0005 §7",
    "trigger_condition": "Checkpoint exemptions file `tools/trace/checkpoint_exemptions.yaml` is missing or empty",
    "guard_snippet": "Define fail-closed default: missing exemptions file means no gates are skipped, even with Checkpoint:true",
    "potential_consequence": "EDGE-39 CRITICAL: ADR-0008 §6 says 'partial-bypass applies to a specific subset of gates listed in checkpoint_exemptions.yaml' but does not say what happens when the file is absent (PHASE-2 deliverable); a missing file could fail open (skip all) or fail closed (skip none)"
  },
  {
    "location": "ARCHITECTURE.md §11 + ADR-0008 §3 'no later-phase REQ tests-green'",
    "trigger_condition": "PHASE-5 needs to land a REQ that incidentally exercises a PHASE-3 area; later-phase REQ becomes green before PHASE-3 exits",
    "guard_snippet": "Distinguish 'phase scope' from 'phase ownership' of REQ; or permit later-phase REQ green if its phase's entry was satisfied transitively",
    "potential_consequence": "EDGE-40 SERIOUS: gate 'no REQ from a later phase is tests-green' makes opportunistic forward work illegal even when it would help; rule is binary with no waiver"
  },
  {
    "location": "ADR-0007 §6 + PHASE-3 + ADR-0008 cache-hit-regression",
    "trigger_condition": "cache-hit-regression gate is declared 'PHASE-3+' but PHASE-3 entry needs gate-coverage green; gate-coverage requires every ADR has a gate referencing it",
    "guard_snippet": "Pre-PHASE-3 gate-coverage must accept 'deferred: PHASE-3+' marker for cache-hit-regression instead of treating as missing",
    "potential_consequence": "EDGE-41 PROCESS: gate-coverage at PHASE-0..2 sees cache-hit-regression listed in table but not active; either fails or silently accepts, neither behavior is specified"
  },
  {
    "location": "ADR-0005 §6 + Stop hook + branch protection",
    "trigger_condition": "Stop hook fires on a branch where remote @{u} does not exist (e.g. first push of a new branch)",
    "guard_snippet": "checkpoint.py must `git push -u origin HEAD` when no upstream is set; differentiate from non-FF",
    "potential_consequence": "EDGE-42 SERIOUS: §7 'if `git rev-list @{u}..HEAD` is non-empty' fails with 'no upstream' error when @{u} is undefined; hook may abort, leaving the new branch entirely unpushed"
  },
  {
    "location": "ADR-0006 §2 + clock/randomness adapter carve-out",
    "trigger_condition": "Clock adapter is 'real component used in both prod and test paths'; test path config selects a deterministic clock — is selection logic a mock?",
    "guard_snippet": "Define 'config-driven adapter selection' as permitted; explicitly forbid runtime monkey-patching even when the substitute is real code",
    "potential_consequence": "EDGE-43 PROCESS: the carve-out is wide enough to permit 'real fake'; without a gate examining whether the deterministic clock is also exercised in prod, P3 erodes silently"
  },
  {
    "location": "ADR-0008 §1 commit-trailers-valid + ADR-0005 §3",
    "trigger_condition": "Commit trailer Requirements: lists a REQ-ID that does not yet exist in INDEX.yaml (commit creates the REQ in same diff)",
    "guard_snippet": "validate_commit.py must check trailer REQ-IDs against the post-commit state of the diff, not the pre-commit INDEX",
    "potential_consequence": "EDGE-44 CRITICAL: trailers are pre-receive validated; a commit that introduces both the REQ and the trailer pointing to it gets rejected because the REQ does not yet exist at validation time"
  }
]
```
