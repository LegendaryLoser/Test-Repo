# Architecture Audit — Consolidated Findings

**Audit date:** 2026-05-17
**Status:** STAGING (non-authoritative; input to future CHG envelopes)
**Streams:** Wave 1: 12 · Wave 2: 8 · Wave 3: 8 · Wave 4: 8 · Wave 5: 4 · **Total: 40** (see [README.md](README.md)). Wave-5 thematic consolidation in progress — see "Wave 5 supplement" section near the end.
**Raw findings:** Wave 1: 270 · Wave 2: 142 · Wave 3: ~147 · Wave 4: ~130 · Wave 5: 84 · **Total: ~770** (plus 19 pre-existing in STATUS.md)
**Distinct themes after dedup:** Wave 1: 26 · Wave 2: +16 · Wave 3: +9 · Wave 4: +~17 · Wave 5: pending consolidation (next pass) · **Total to date: ~70 (Waves 1-4 only)**
**Convergence:** Originally measured under COMPOSITE-V2 Gate 6 (marginal novelty); destabilised by Wave 4's ~46% rebound (STAKE+COUNTER new methods spiked novelty). Replaced by Archive Coverage Growth Rate (ACGR) per `qd-triage.md` §2.6. Wave 4 ACGR ~45%; Wave 5 ACGR pending re-measurement after consolidation; projected ~10-15%; Wave 6 (if pursued) projected <5% (convergence target).
**Provenance:** [findings-index.md](findings-index.md)
**META- audit corrections:** [corrections.md](corrections.md) — Wave-5 reasoning-tree meta-auditor produced 19 corrections against the Waves-1-4 consolidation (4 CRIT / 12 SER / 3 PROC); read alongside the original framings below. Inline annotations cross-reference the META- finding ID.

---

## Executive summary

The architecture artifact has high defect density. Across 12 orthogonal
review streams against 15 documents, **novel findings continued to
surface in every stream** — convergence rate was 30-40%, meaning no
single pass exhausted the defect space.

Two structural patterns dominate:

1. **Amendment drift.** ADR-0002 was rewritten via amendment 0001 (BMAD
   strategy changed from wrappers to native Skills, install path renamed
   `bmad/` → `_bmad/`). ADR-0005 was extended via amendment 0001 (push
   invariant added, new hooks introduced). Neither amendment was
   propagated downstream — ARCHITECTURE.md §9, ADR-0001, PHASE-0,
   PHASE-1 all still describe the pre-amendment world. This generates
   roughly 30 of the 270 raw findings, concentrated in THEME-A.

2. **Proxy enforcement.** Multiple CI gates measure proxies of the
   behaviors they claim to enforce: `gate-coverage` checks string
   presence not semantic correctness; `cost-budget` aggregates declared
   not measured spend; `direct-anthropic-import-banned` is a static-import
   grep that misses transitive imports; `commit-trailers-valid` claims
   `pre-receive hook` trigger but workflow files run `on: pull_request`.
   The meta-gate makes the substitutions invisible. Concentrated in
   THEME-D and several of the pre-mortem findings.

A third structural pattern is **vapor references**: tools (`spec_lint
allocate`), trailers (`Material-Architecture-Change`, `Bootstrap`),
artifact types (`gate`-type task, phase-exit ADR), and config files
(`tools/spec_lint/config.yaml`, `tools/trace/checkpoint_exemptions.yaml`)
that are referenced in normative text but never specified, owned, or
scheduled. Concentrated in THEMES C, I, J, M, Z.

The artifact is not implementation-ready for PHASE-1 or PHASE-2 without
resolving at least the 6 BLOCKING findings the readiness pass surfaced,
and the BMAD strategy drift is so loud that it generates noise across
every other review.

---

## Confidence tiers

Findings clustered by how many independent streams surfaced the same
issue.

| Tier | Streams that found it | Interpretation |
|---|---|---|
| **Tier A — Certain** | 6 or more | Independently reproduced by 50%+ of streams. Resolve unconditionally. |
| **Tier B — Confirmed** | 3-5 | Multiple streams converged. High confidence; recommend resolving unless out-of-scope. |
| **Tier C — Surfaced** | 1-2 | Single-stream catch. Still valid; validate before scheduling. |

The themes below are sorted by combined Tier-A + Tier-B count, then by
severity.

---

## Themes

Each theme = a root-cause cluster across the 12 streams. The "Streams"
column counts how many of the 12 streams independently surfaced at
least one finding in this theme.

### THEME-A — BMAD strategy / wrapper retirement / `bmad/` ↔ `_bmad/` drift

**Severity:** CRITICAL · **Streams:** 11/12 · **Constituent findings:** ~30

ADR-0002 Amendment 0001 retired wrapper-style integration (`.claude/agents/`,
`.claude/commands/`) in favor of native Claude Code Skills under
`.claude/skills/`, and renamed the install path from `bmad/` to `_bmad/`.
Three downstream documents still describe the pre-amendment world:

- **ARCHITECTURE.md §9** still says "BMAD agents live under `bmad/`;
  Claude Code surfaces them via thin wrappers in `.claude/agents/` and
  `.claude/commands/`."
- **ARCHITECTURE.md §3** correctly shows `_bmad/` and marks the wrapper
  slots as legacy — so the two sections of the same document
  contradict each other.
- **ADR-0001 §Rules item 4** says "`bmad/` is the BMAD installation".
  ADR-0001 has no amendment log section, so the contradiction is
  un-versioned.
- **PHASE-0 §Scope item 12** says "`bmad/` is **not** installed in
  PHASE-0".
- **PHASE-1 §Scope items 3-4** require building `bmad/config.yaml`
  (canonical version pin is at `_bmad/_config/manifest.yaml` per
  ADR-0002 §1) and `.claude/agents/`/`.claude/commands/` wrappers
  (which ADR-0002 forbids).
- **PHASE-1 exit criterion** requires "All BMAD wrapper files [...]
  resolve their `Load:` paths" — literally unsatisfiable under the
  current native-Skills model.

Constituent findings include: ARCH-CRIT-01, ARCH-CRIT-02, ARCH-CRIT-03,
IND-CRIT-01, IND-CRIT-02, IND-CRIT-03, IND-CRIT-04, IND-PROC-05,
ADVO-CRIT-01, ADVO-CRIT-02, ADVO-PROC-03, ADVS-CRIT-04, ADVS-PROC-01,
ADVH-CRIT-02, EDGE-23, EDGE-24, EDGE-25, READY-01, READY-15, STRUCT-02,
PARTY-DOC-05, INHER-09, PROSE-07, PROSE-13.

**Recommended CHG:** doc-only sync of ARCHITECTURE.md §9, ADR-0001,
PHASE-0, PHASE-1 to the post-amendment reality. Add a
`cross-doc-bmad-paths` lint rule to prevent recurrence.

---

### THEME-B — Trailer schema fragmentation

**Severity:** CRITICAL · **Streams:** 10/12 · **Constituent findings:** ~18

ADR-0005 §3 lists four mandatory trailers (Task, Requirements,
Tests-Status, Phase). At least four additional trailers are referenced
elsewhere without being in any registry:

- `Checkpoint: true` (ADR-0005 §7)
- `Bootstrap: <reason>` (ADR-0006 §4) + `bulk-green-start` gate not in
  ADR-0008 inventory
- `Material-Architecture-Change: true` (ARCHITECTURE.md preamble) — never
  enumerated, never validated
- `Skill-Removal-Acknowledged: <skill-id>` (ADR-0002 §8)

ADR-0008 §6 claims `Checkpoint: true` is "the **only** sanctioned
partial-bypass" — directly contradicted by the existence of `Bootstrap`.
`tools/trace/checkpoint_exemptions.yaml` is referenced as the source of
truth for which gates the checkpoint trailer exempts, but the file's
schema, default contents, and authorship policy are never specified.
Without an enumerable trailer registry, `commit-trailers-valid` cannot
be implemented.

Edge-case interactions surfaced:
- `EDGE-08`: combining `Checkpoint: true + Bootstrap: <reason>` not forbidden
- `EDGE-44`: commit that introduces both a REQ and its Requirements trailer
  is rejected because the REQ doesn't yet exist at pre-receive time
- `EDGE-09`: `Material-Architecture-Change: true` with no ADR in the diff
  has no gate
- `PROSE-03`: "every commit must carry trailers" has an undefined
  population (GitHub merge commits, reverts, empties all silently exempt)

Constituent findings: ARCH-CRIT-04, ARCH-SER-04, ARCH-SER-06, ARCH-SER-08,
ADVO-SER-02, ADVO-SER-04, ADVH-SER-08, EDGE-08, EDGE-09, EDGE-44,
READY-09, READY-10, READY-11, INHER-12, INHER-14, INHER-22, PROSE-03,
ADVS-CRIT-02.

**Recommended CHG:** ADR-0005 §3 amendment defining the full trailer
registry (mandatory + optional + bypass), schema for
`checkpoint_exemptions.yaml`, and resolution of the pre-receive vs
pre-commit vs PreToolUse trigger conflict. Must precede any PHASE-2
work that touches `validate_commit.py` or `commit-trailers-valid`.

---

### THEME-C — `gate-coverage` meta-gate is syntactic, not semantic

**Severity:** CRITICAL · **Streams:** 9/12 · **Constituent findings:** ~13

ADR-0008 §2's `gate-coverage` "walks every ADR and every principle in
ARCHITECTURE.md §1 and verifies that at least one entry in the table
above references it." Multiple failure modes:

1. **Syntactic vs semantic:** the gate checks that an entry references
   the ADR by name; it cannot verify the named gate actually enforces
   the asserted behavior (PREM-01). A junior contributor can edit
   `prose-xref-banned` to whitelist comments, the gate keeps its name,
   `gate-coverage` stays green, drift accumulates.
2. **Principle coverage:** the inventory's `Enforces` column references
   ADRs, not principles. A literal walk over P1-P5 finds no gates
   directly named against P1 or P5. STATUS.md C5 already tracks this;
   ADVO-CRIT-04, IND-CRIT-06, ADVS-SERI-01 reconfirm with detail.
3. **Per-section granularity:** ADR-0002 (9 sections + 2 amendments) is
   "covered" by a single gate that references the ADR header. Sections
   like §7 staging, §8 upgrade safeguards, §9 per-project isolation can
   have zero gates and `gate-coverage` still passes (ARCH-SER-03,
   INHER-11).
4. **Bootstrap circularity:** the gate itself is in the inventory.
   PHASE-2 is the phase that builds it. Pre-PHASE-2 commits cannot be
   gated by `gate-coverage` because it doesn't exist yet (ADVH-PROC-09,
   ADVO-SER-09, ADVS-CRIT-03).
5. **PHASE-2-introduced gates not in inventory:** `skill-removal-
   acknowledged`, `bmad-version-pin`, `bmad-smoke-test`, `stale-staging`
   are introduced by PHASE-2 / ADR-0002 §7-§8 but absent from ADR-0008 §1.
   The meta-gate cannot map them (IND-CRIT-07, READY-02, INHER-02,
   ADVS-PROC-03, EDGE-41).

Constituent findings: ARCH-SER-03, IND-CRIT-06, IND-SER-01, ADVO-CRIT-04,
ADVS-SERI-01, ADVH-PROC-09, EDGE-41, INHER-11, INHER-02, PREM-01,
STRUCT-12, READY-02, IND-CRIT-07, plus STATUS.md C5.

**Recommended CHG:** rewrite ADR-0008 §2 to define semantic gate
correctness contracts; add per-principle gate citations; expand
inventory to include all referenced gates; resolve bootstrap by
permitting PHASE-0 placeholder gates with an explicit "real
implementation lands in PHASE-N" annotation that itself is gated.

---

### THEME-D — Hook implementation correctness (glob patterns, race conditions, surface mismatches)

**Severity:** SERIOUS (multiple CRITICAL specific cases) · **Streams:** 10/12 · **Constituent findings:** ~17

The hook table in ADR-0005 §6 mixes shell glob patterns, MCP tool names,
and Bash command prefixes without a precise matching grammar.

- **`PostToolUse(Bash:*test*)`** (EDGE-28, READY-16) matches
  `pytest`, `npm test`, `jest`, but also `git test-rev-parse`,
  `latest`, `attest`, `grep contest`. `journal_tests.py` will fire on
  non-test commands, producing corrupt `tests_run` events.
- **`PostToolUse(Bash:git commit)`** (PROSE-09) — does `git commit -m
  "..."` match? Glob unspecified. Multiple git operations in one Bash
  invocation: one hook firing or many?
- **`PostToolUse(Edit|Write)`** (EDGE-27) — glob may catch unrelated
  tools; `Read` accidentally included?
- **`PostToolUse(mcp__github__merge_pull_request)`** (ARCH-SER-13,
  EDGE-17, PREM-02) — after PR merge, working branch is divergent from
  main and may be deleted upstream. "FF the working branch" no-ops or
  errors.
- **First-commit causality loop** (INHER-13) — `matrix-drift` pre-commit
  hook rewrites matrix from `rebuild.py`; `rebuild.py` reads journal;
  journal is appended only by `PostToolUse` after commit completes.
  First commit cannot produce a matrix that includes itself.
- **Stop hook duplicate firing** (EDGE-04) — container suspend then
  resume produces duplicate checkpoint commits.
- **Pre-receive vs pre-commit vs PreToolUse** (READY-03) —
  `commit-trailers-valid` has three conflicting trigger surfaces across
  ADR-0008 §1, §5, and ADR-0005 §6. Each leaves a different bypass.
- **`commit-msg` hook** (READY-06) — PHASE-2 introduces a hook not
  declared in ADR-0005 §6; breaks REQ-ARCH-0008.

Constituent findings: EDGE-04, EDGE-05, EDGE-13, EDGE-14, EDGE-15,
EDGE-17, EDGE-27, EDGE-28, EDGE-32, EDGE-33, EDGE-34, INHER-13,
PROSE-09, ADVH-SER-04, READY-06, READY-16, PARTY-DOC-01, ARCH-SER-13,
READY-03, PREM-02.

**Recommended CHG:** ADR-0005 §6 amendment with precise hook matching
grammar (anchored runner allowlist for tests, exact-prefix for git
commands, behavior on suspend/resume, FF target resolution for merged-and-
deleted branches), and bootstrap rule for first-commit-on-empty-journal.

---

### THEME-E — Red-before-green + checkpoint commit interaction

**Severity:** CRITICAL · **Streams:** 9/12 · **Constituent findings:** ~15

ADR-0005 §4 says `validate_commit.py` "walks git history" to verify
red-before-green. ADR-0005 §7 makes checkpoint commits exempt from "a
defined subset of gates" via `checkpoint_exemptions.yaml`. The
interaction is unspecified:

- Checkpoint between red and green (EDGE-07, IND-CRIT-08): does the walk
  treat checkpoints as transparent or opaque?
- Branch starting with a checkpoint (EDGE-06): "next non-checkpoint
  commit" has no anchor
- Squash/rebase destroys the red commit ancestor (PREM-03, ADVH-SER-08,
  PARTY-SER-03)
- Pre-receive `commit-trailers-valid` will reject checkpoint commits at
  push (IND-SER-09)
- "The next non-checkpoint commit is responsible for restoring P4"
  obligation has no enforcement surface (PROSE-12, PARTY-SER-04)
- No cap on consecutive checkpoints (PARTY-SER-04, PREM-12)
- Bulk-green-start `Bootstrap` trailer is the only other escape; not in
  trailer registry (ARCH-SER-06)

Constituent findings: ARCH-SER-08, IND-SER-05, ADVO-SER-07, ADVS-SERI-03,
ADVH-SER-08, EDGE-06, EDGE-07, EDGE-08, READY-11, INHER-07, PREM-03,
PREM-12, PARTY-SER-04, PROSE-12, ARCH-SER-06, IND-SER-09, PARTY-SER-03.

**Recommended CHG:** ADR-0005 §7 amendment fully specifying checkpoint
semantics (validator transparency rule, ceiling on consecutive
checkpoints, mandatory squash policy or transparent walk).
`checkpoint_exemptions.yaml` schema in same CHG (depends on THEME-B).

---

### THEME-F — Push invariant unenforceable in its motivating failure mode

**Severity:** CRITICAL · **Streams:** 8/12 · **Constituent findings:** ~12

ADR-0005 §6 Amendment 0001 added the push invariant to close the
"committed but unpushed at container reclaim" window. The amendment's
own §8 admits "residual loss only if both hooks fail to fire (e.g.
abrupt container reclaim mid-`PostToolUse`)" — which is the precise
scenario that motivated the amendment. No gate enforces the invariant
(ADR-0008 has no `push-invariant` row).

- The amendment creates the appearance of safety while leaving the
  failure mode resident (PREM-02, IND-CRIT-08)
- Push hook abort on non-FF leaves working tree diverged; trains agents
  to use `--no-verify` to escape (ADVH-SER-04, EDGE-16)
- Branch deleted on merge breaks post_merge_sync (EDGE-17)
- No upstream tracking on first push of new branch (EDGE-42)
- SessionStart resume hook is not enumerated as a push-invariant
  enforcement surface (EDGE-18)
- "Container reclaim, push completed: zero loss" claim is misleading
  given the upstream conditions (PARTY-DOC-01)

Constituent findings: ARCH-SER-02, IND-CRIT-08, ADVO-SER-06, ADVH-SER-04,
EDGE-16, EDGE-17, EDGE-18, EDGE-42, INHER-08, PREM-02, PARTY-CRIT-01,
ARCH-SER-13.

**Recommended CHG:** either ship a server-side post-receive verification
gate (the only honest enforcement surface) or downgrade the language in
ARCHITECTURE.md §8 from "zero loss" to "best-effort". Same CHG should
fix the post_merge_sync semantics (depends on THEME-D).

---

### THEME-G — REQ-ARCH-* canonical home + format

**Severity:** SERIOUS · **Streams:** 8/12 · **Constituent findings:** ~8

REQ-ARCH-0001 through 0008 sit in ARCHITECTURE.md §10 as prose bullets,
not as ADR-0004 §5 REQ blocks. They lack every required field
(revision, status, introduced, supersedes, phase, tier, references) and
have no Acceptance criteria in Given/When/Then form. The architecture
exempts itself from its own spec-storage discipline.

STATUS.md C2 already tracks the format defect; the audit adds detail:
- REQ-ARCH-0007 and REQ-ARCH-0008 are themselves compound requirements
  (INHER-10) — violate ADR-0004 §3 atomicity
- REQ-ARCH-0002 hardcodes "ADR-0001 through ADR-0008" counts (ARCH-PROC-09)
- INDEX.yaml has no REQ-ARCH-* entries → `index-up-to-date` can't enforce
- `tools/spec_lint allocate` doesn't exist → can't allocate clean IDs
  for any migration

Constituent findings: STATUS.md C2, ARCH-SER-01, ARCH-PROC-09,
IND-PROC-02, ADVS-SERI-02, ADVH-SER-01, STRUCT-07, INHER-10.

**Recommended CHG:** migrate REQ-ARCH-* to
`openspec/specs/_meta/architecture-invariants.spec.md` in proper
ADR-0004 §5 format. Split compound REQs. Drop hardcoded counts in
favor of dynamic enumeration. Depends on THEME-H (spec_lint allocate).

---

### THEME-H — Missing-artifact-type ADRs (STATUS.md, CHG, TEA, Epic/Story, secrets, branches, TASK types)

**Severity:** SERIOUS · **Streams:** 8/12 · **Constituent findings:** ~18

Several first-class artifacts referenced throughout the architecture
have no defining ADR:

| Artifact | Referenced in | Defining ADR |
|---|---|---|
| `STATUS.md` | CLAUDE.md, every session | None |
| CHG envelope structure | §4 atomic units, every phase | None (template-only) |
| TEA scope/skills/interface | P5, §5 reconciliation | None (one bullet in ADR-0002) |
| Epic file format | §5, PHASE-5, ADR-0005 §9 | None |
| Story file format | §4, every phase | None |
| Secrets management | ADR-0003, ADR-0007 | None |
| Branch / PR conventions | ADR-0005 §6, PHASE-0 entry | None |
| `gate`-type TASK | ADR-0004 §4, ARCHITECTURE.md §11, ADR-0003 §4, PHASE-5 | None (used 4× undefined) |
| `docs`-type TASK | ADR-0002 §7, STAGING.md | None |
| Phase-exit ADR | ARCHITECTURE.md §11 | None (referenced as if extant) |
| `_TEMPLATE.md` schemas | PHASE-0 scope item 4 | None |
| `cost-tier: cheap/full` enum | ADR-0007 §4, ADR-0008 §1 | None (referenced, not enumerated) |
| `tier:` scalar vs list | ADR-0004 §5 vs ADR-0003 §3 | Contested (INHER-16) |
| REQ domain registry | ADR-0004 §1 | None (each phase lazily adds) |

Constituent findings: ARCH-PROC-01..07, INHER-01, INHER-15..21,
READY-04, READY-07, READY-19, ADVO-PROC-02, ADVH-PROC-13,
ADVS-PROC-04, PARTY-UX-01.

**Recommended CHG:** one ADR per missing type. Probably 7-10 small
ADRs, allocated through the same `spec_lint allocate` work in THEME-H/G.
Multi-month effort if all are pursued; prioritize STATUS.md, CHG
envelope, TASK-type taxonomy (these unblock everything else).

---

### THEME-I — Test tier semantics, real-vs-fake adapter line, P3 vs P2 tension

**Severity:** SERIOUS · **Streams:** 9/12 · **Constituent findings:** ~15

ADR-0006 §2 permits "real" adapter substitutions and "HTTP transport"
nock interceptors. ADR-0007 §2 bans recorded fixtures for the LLM tier.
The boundary is undefined:

- **Recorded responses are fixtures** (ARCH-SER-05, IND-SER-04,
  ADVO-SER-03, ADVH-SER-11, ADVS-SERI-07) — ADR-0006's "real captured"
  is structurally identical to ADR-0007's banned "recorded fixture".
  Distinguishable only by intent, which CI cannot detect.
- **Deterministic clock = manufactured determinism** (IND-SER-12,
  PROSE-14, EDGE-43, ADVS-SERI-04) — exactly what P2 forbids, renamed.
- **No behavior equivalence contract** between paired real adapters
  (ARCH-SER-10) — Sheets REST and Sheets GAS have different semantics
  (locking, transactions, batching).
- **Unit tier with REST adapter is integration** (PARTY-SER-01) —
  collapses tier distinction; requires network/credentials/real
  spreadsheet from a "unit" test.
- **Stateful real adapters at quota** (PREM-05) — bans the only
  tractable test pattern (in-memory implementation of in-repo interface);
  collapse of "module mock" vs "interface implementation".
- **Clock/randomness adapter for retry-on-timeout** (PARTY-SER-02) —
  requires deterministic clock; no real clock satisfies the test.
- **GAS V8 runtime has no `cache_control`** (ADVH-CRIT-12) — ADR-0007
  §5 "enabled by default" contradicts runtime capability.
- **`tier:` scalar vs four-tiers-per-project tension** (INHER-16) —
  REQ frontmatter is scalar; ADR-0003 §3 says "all required".
- **TS/Python client mirroring contract** (ADVS-PROC-05) — "where APIs
  differ" silently authorizes drift.

Constituent findings: ARCH-SER-05, ARCH-SER-10, IND-SER-04, IND-SER-12,
ADVO-SER-03, ADVH-SER-11, PARTY-SER-01, PARTY-SER-02, PREM-05, PROSE-05,
PROSE-06, PROSE-14, ADVS-SERI-04, ADVS-SERI-07, EDGE-31, EDGE-43,
ADVH-CRIT-12, INHER-16, ADVS-PROC-05.

**Recommended CHG:** ADR-0006 + ADR-0007 amendment defining (a) the
boundary between "real adapter" and "fake of in-repo interface",
(b) carve-out or removal of deterministic clock from P2, (c) behavior
equivalence test contract for paired real adapters, (d) `tier:`
scalar-vs-list resolution, (e) GAS runtime carve-out for prompt caching.

---

### THEME-J — Stochastic tier statistical weakness + cost-budget proxy

**Severity:** SERIOUS · **Streams:** 7/12 · **Constituent findings:** ~10

ADR-0007 §3 permits distributional assertions over N runs with "sample
size and threshold pinned per test." No floor on N, no power-analysis
contract, no calibration cadence. Result: an author can declare N=5
and a 99% interval that is meaninglessly wide; the test passes CI while
asserting essentially nothing (ADVO-SER-04, PREM-15, ADVS-PROC-04).

`cost-budget` (ADR-0007 §4) aggregates the *declared* `@cost-budget`
annotation values, not *measured* spend (PREM-04). A test annotated
`@cost-budget tokens=50000` that actually consumes 480000 (sandwich
layer retries on schema-fails) passes the gate. Cost telemetry exported
by `packages/anthropic-client/` and the budget gate are not
reconciled.

- No multiple-comparisons correction across stochastic suite (IND-SER-03)
  — dozens of p=0.05 tests give unacceptable green-PR false-failure rate
- No definition of `cost-tier: cheap` vs `cost-tier: full` (INHER-19)
- `cache-hit-regression` baseline circularly defined (IND-SER-11) —
  established by the same PR that exits PHASE-3
- `@cost-budget` annotation has no presence-required check (EDGE-29)
  — missing annotation fails open
- Sandwich-layer exception scope ambiguous re: exact-equality ban (EDGE-30)

Constituent findings: IND-SER-03, ADVO-SER-04, READY-14, PARTY-REQ-04,
PREM-04, PREM-15, ADVS-PROC-04, EDGE-29, EDGE-30, INHER-19,
IND-SER-10, IND-SER-11.

**Recommended CHG:** ADR-0007 §3-§5 amendment: minimum-N floor,
calibration discipline, declared-vs-measured reconciliation gate,
`cost-tier` enumeration, baseline pinning protocol, multiple-comparisons
policy.

---

### THEME-K — Phase ordering: circular bootstrap, exit-gate self-reference, monotonic-only

**Severity:** CRITICAL · **Streams:** 9/12 · **Constituent findings:** ~13

Multiple phase-ordering pathologies:

- **PHASE-0 placeholder commands trivially pass** (ADVO-CRIT-05) →
  REQ-ARCH-* go `draft → tests-green` without passing through
  `tests-red`. Violates ADR-0005 §4 by construction.
- **`phase-exit` gate is built in PHASE-2** (ADVS-CRIT-03, READY-05) →
  PHASE-0 has no way to evaluate its own exit gate. The first
  application of the gate is to the phase that builds it.
- **`gate-coverage` is built in PHASE-2** (ADVO-SER-09, ADVH-PROC-09) →
  meta-gate enforcing "every principle has a gate" not operational at
  PHASE-0/1 exit.
- **Amendment 0001 of ADR-0005 added hooks** (IND-SER-07) but
  REQ-ARCH-0008 was not updated; PHASE-0 re-gate was not triggered.
  Material change with no re-gate.
- **`phase-exit` allows opportunistic forward work to fail** (EDGE-40) —
  binary rule with no waiver; blocks PHASE-3 hotfix during PHASE-5
  (PREM-16); forces `--no-verify`, normalizes bypass.
- **Phase-exit ignores prior-phase regression** (EDGE-20) — gate only
  checks current-phase exit REQs; PHASE-2 REQ regressing to red is
  invisible to PHASE-3 phase-exit.
- **PHASE-0 cannot legitimately re-enter** (EDGE-22) — entry criterion
  "Repository has only README.md" false once PHASE-0 has begun.
- **Strict ordering caps parallel throughput** (PARTY-PROC-03).
- **PHASE-1 paused; status enum incomplete** (ARCH-PROC-05).
- **PHASE-0 entry hardcodes ephemeral branch** (ARCH-PROC-08).

Constituent findings: ADVO-CRIT-05, ADVS-CRIT-01, ADVS-CRIT-03,
ADVO-SER-09, ADVH-PROC-09, IND-SER-07, EDGE-20, EDGE-22, EDGE-36,
EDGE-40, READY-05, INHER-06, PARTY-CRIT-02, PARTY-PROC-03,
ARCH-PROC-05, ARCH-PROC-08, PREM-16, ARCH-CRIT-07.

**Recommended CHG:** new ADR authorizing (a) PHASE-2 carve-out for the
minimum traceability runtime to land alongside PHASE-1 work, (b)
phase-status enum (`pending|in-progress|paused|complete|superseded`),
(c) `phase-exit` waiver for cross-phase hotfixes with audit trail,
(d) "prior-phase regression" checks, (e) re-gate trigger for
amendments that change PHASE-0 scope. Foundational; unblocks everything.

---

### THEME-L — CLAUDE.md ↔ ARCHITECTURE.md verbatim duplication (P1 violation)

**Severity:** CRITICAL · **Streams:** 5/12 · **Constituent findings:** ~5

ARCHITECTURE.md §1 lists the five principles. REQ-ARCH-0007 requires
CLAUDE.md to cite them verbatim. Two SoTs for the same fact. No
precedence rule. No lint gate enforces consistency. Drift silent.

ARCH-CRIT-08, INHER-04, STRUCT-09, IND-SER-08, EDGE-35.

**Recommended CHG:** designate ARCHITECTURE.md §1 as SoT; CLAUDE.md
imports via xref; verbatim-citation REQ replaced with consistency-lint
REQ; SessionStart hook (PHASE-2) materializes the imported copy at
runtime instead of storing it as text.

---

### THEME-M — Amendment-log discipline inconsistent across ADRs

**Severity:** SERIOUS · **Streams:** 6/12 · **Constituent findings:** ~9

Only ADR-0002 and ADR-0005 have amendment-log sections. Six other ADRs
(0001, 0003, 0004, 0006, 0007, 0008) have none. Schema is not in
ADR-0004's spec format. Other defects in the existing amendment-log
machinery:

- ADR-0002 amendment 0001 says "Complete rewrite" — violates
  immutability discipline (IND-PROC-01, PARTY-CRIT-03). Should have
  been ADR-0009 superseding ADR-0002.
- Amendment rows have no date column → post-amendment date drift
  unobservable (IND-PROC-03).
- Amendment 0001 of ADR-0005 added hooks; ADR-0005 §10 is the only
  place that lists them, requiring forward-reference from §6
  (STRUCT-05).
- Concurrent amendments race on amendment number (EDGE-15).
- Amendment of amendment / contradiction unhandled (EDGE-14).

Constituent findings: ARCH-SER-09, IND-PROC-01, IND-PROC-03, STRUCT-04,
STRUCT-05, EDGE-14, EDGE-15, PARTY-CRIT-03, PARTY-DOC-03.

**Recommended CHG:** ADR-0004 amendment defining ADR amendment-log
schema (required section, date column, append-only, supersedes/extends
classification); stub amendment-log section in all 8 ADRs; rule for
when amendment vs supersession is appropriate.

---

### THEME-N — ARCHITECTURE.md as summary-of-summaries: silent drift from ADRs

**Severity:** SERIOUS · **Streams:** 5/12 · **Constituent findings:** ~6

ARCHITECTURE.md §7 (traceability) and §8 (session persistence) are
~6-line summaries of ADR-0005, including a failure-mode table.
ADR-0005 §8 contains the same table. ARCHITECTURE.md §8's table is
missing the post-amendment row that ADR-0005 §8 added — proof of
silent drift (STRUCT-03).

Same pattern: §3 layout tree carries inline rationale comments owned
by other ADRs (STRUCT-06); §5 Epic reconciliation rules stated but no
`epic-reconciliation` gate in ADR-0008 inventory (STRUCT-12);
ADR-0003 §3 and ADR-0006 §1 both enumerate four tiers with subtly
different wording (STRUCT-15); §12 "What is *not* in this document" is
negation-by-enumeration anti-pattern (STRUCT-08).

The cross-document consistency lint that ADR-0004 promises does not
exist, so every "summary section" in ARCHITECTURE.md silently rots.

Constituent findings: STRUCT-03, STRUCT-06, STRUCT-08, STRUCT-12,
STRUCT-15, PARTY-DOC-02.

**Recommended CHG:** reduce ARCHITECTURE.md §7, §8, §3 inline comments
to pointers; promote Epic reconciliation gate to ADR-0008 inventory;
merge ADR-0003 §3 into ADR-0006 §1 reference; cut §12. Cross-document
consistency lint as its own follow-up CHG.

---

### THEME-O — Status enum / Tests-Status / REQ.status conflated and ambiguous

**Severity:** SERIOUS · **Streams:** 5/12 · **Constituent findings:** ~7

ADR-0004 §5 REQ status enum: `draft | tests-red | tests-green | reviewed
| merged | deprecated` (6 values).
ADR-0005 §3 Tests-Status trailer enum: `none | red | red→green | green |
deprecated` (5 values, names differ).
ADR-0005 §4 forbids `draft → tests-green` but says nothing about
`tests-green → reviewed → merged → deprecated`.
ADR-0006 §5 coverage gate uses "non-deprecated" — ambiguous about
`draft` and `reviewed` populations.

Edge cases:
- Test flips green→red→green from a flake (EDGE-03)
- `reviewed` and `merged` transitions wholly unguarded (EDGE-02)
- Commit with `Tests-Status: green` while REQ.status is `draft`
  bypasses progression (EDGE-01)

Constituent findings: STATUS.md P2, ARCH-SER-11, IND-PROC-04, EDGE-01,
EDGE-02, EDGE-03, READY-08.

**Recommended CHG:** reconcile the two enums (one mapping table);
explicit transition rules for every pair; coverage-gate population
explicitly defined.

---

### THEME-P — "The paper" prose reference (self-referential P1 violation)

**Severity:** SERIOUS · **Streams:** 5/12 · **Constituent findings:** ~5

ARCHITECTURE.md §2 and ADR-0004 Context invoke "a published result on
transformer associative memory ('the paper')" repeatedly. No DOI,
authors, title, arXiv ID, or year. ADR-0004 §2's own
`prose-xref-banned` rule lists "the original ADR" as the forbidden
pattern — "the paper" is structurally identical, applied to an
external work. The artifact's foundational citation violates the
artifact's own citation rule.

Constituent findings: IND-PROC-07, ADVS-CRIT-05, STRUCT-14, INHER-03,
ADVO-SER-01.

**Recommended CHG:** add `## References` section to ADR-0004 with full
bibliographic data; replace "the paper" with stable `REF-PAPER-0001`
identifier; ARCHITECTURE.md §2 cites by ID.

---

### THEME-Q — Anti-aliasing rule defects

**Severity:** SERIOUS · **Streams:** 6/12 · **Constituent findings:** ~7

ADR-0004 §4 anti-aliasing rule:
- Threshold "pinned in `tools/spec_lint/config.yaml` and reviewed
  quarterly (a `gate`-type task)" — config file unspecified, threshold
  value unspecified, quarterly review has no owner (ADVO-SER-05,
  ADVH-SER-06, ADVS-SERI-05, READY-13).
- Surface-text n-gram similarity, but the paper's δ-convex-lures
  argument requires *semantic* similarity (PREM-06). Wrong implementation
  of the right idea.
- Will inevitably flag BDD-boilerplate-sharing REQs at scale (PREM-06
  scenario).
- "Reviewed quarterly" cadence unowned, no calendar artifact (INHER-21).
- Gate is "every PR" but configuration is PHASE-1 deliverable —
  gate has nothing to enforce until PHASE-1 (IND-SER-02 related).

Constituent findings: ADVO-SER-05, ADVH-SER-06, IND-SER-02, INHER-21,
READY-13, PREM-06, ADVS-SERI-05.

**Recommended CHG:** redesign rule to operate on semantic similarity
(embedding-based with appeal path) OR retain surface-text with explicit
boilerplate-allowlist; pin threshold value in the ADR (not in
`tools/spec_lint/config.yaml`); assign quarterly-review owner via
the gate-task-type ADR (depends on THEME-H).

---

### THEME-R — Vapor references: tools and config that don't exist

**Severity:** SERIOUS · **Streams:** 9/12 · **Constituent findings:** ~12

Items referenced as if extant but not implemented or specified:

- `tools/spec_lint allocate <domain>` (ADR-0004 §1) — never shipped;
  no phase commissions it (ARCH-CRIT-06, INHER-05).
- `tools/spec_lint/config.yaml` (ADR-0004 §4) — never specified.
- `tools/trace/checkpoint_exemptions.yaml` (ADR-0008 §6) — schema
  undefined; not in any phase scope (ARCH-SER-08, READY-11, INHER-22).
- `tools/ci/` (ADR-0008 §1 owner column, ADR-0002 §7
  `tools/ci/smoke_bmad.py`) — no phase has it in scope (READY-12).
- `tools/tea/` (PHASE-1 §5) — invokes "TEA workflows" with no contract
  defined (READY-07, ARCH-PROC-03).
- "Phase exit ADR" (ARCHITECTURE.md §11) — referenced as artifact type
  but no template, no ID format, no creation rules (ADVS-PROC-02).
- `_TEMPLATE.md` schemas (PHASE-0 §4) — files required, contents not
  specified (INHER-20).
- `STATUS.md` (CLAUDE.md step 1) — not in any phase scope (INHER-15,
  ARCH-PROC-01).
- `stale-staging` lint rule (ADR-0002 §7) — "deferred CHG" with no CHG
  number, no scheduling (ADVS-PROC-03).

Constituent findings: ARCH-CRIT-06, ARCH-SER-08, ARCH-PROC-01,
ARCH-PROC-03, INHER-05, INHER-15, INHER-20, INHER-22, READY-07,
READY-11, READY-12, ADVS-PROC-02, ADVS-PROC-03.

**Recommended CHG:** ADR-0004 amendment scheduling `tools/spec_lint
allocate`; phase scope changes adding `tools/ci/`, `tools/tea/`,
`checkpoint_exemptions.yaml`, `_TEMPLATE` schemas, STATUS.md. May
fragment into multiple smaller CHGs by tool.

---

### THEME-S — PHASE-5 entry depends on undelivered product content

**Severity:** SERIOUS · **Streams:** 5/12 · **Constituent findings:** ~7

PHASE-5 entry requires `vision.md`, ≥1 brief, ≥1 PRD section, ≥1 Epic
with coverage, ≥1 Story — all in "a separate product PR chain" that no
phase delivers. ARCHITECTURE.md §12 says product content is out of
scope. No PHASE-X produces it. PHASE-5 is structurally unreachable.

5 phases of infrastructure built before any product validation (PARTY-
PROC-01 — "build the cathedral, then wonder if anyone wants to pray").

Constituent findings: ARCH-SER-12, ADVO-SER-08, PARTY-PROC-01,
READY-04, INHER-19 partial, plus implicit in many phase-ordering
findings.

**Recommended CHG:** insert a product-content phase (PHASE-PROD) into
the phase model, OR amend §12 to make product content part of the
architecture artifact itself, OR rebind PHASE-5 to a "first project,
product-content-permitting" rule. Major decision.

---

### THEME-T — Operational artifact gaps (cost numbers, calibration, baselines)

**Severity:** SERIOUS · **Streams:** 6/12 · **Constituent findings:** ~8

Concrete numeric / operational values referenced but never pinned:

- Per-PR `cost-budget` ceiling (IND-SER-10, ADVS-PROC-04)
- Per-nightly `cost-budget` ceiling
- `cache-hit-regression` baseline threshold
- Anti-aliasing similarity threshold
- Anti-aliasing n-gram size
- `bulk-green-start` threshold N
- `stale-staging` configurable threshold
- Stochastic-tier minimum N
- Confidence-interval / p-value defaults
- Token-budget units (input? output? combined?)
- Approving-review actor for `Bootstrap`

These are not single-decision issues; each requires a calibration
discipline (initial value, drift detection, review cadence, owner).

**Recommended CHG:** central `tools/ci/calibration.yaml` (or similar)
that pins every numeric value with metadata (initial date, last
review, owner, drift detection). One ADR establishes the discipline;
each operational gap fills it in.

---

### THEME-U — Identifier allocation races and collisions

**Severity:** SERIOUS · **Streams:** 5/12 · **Constituent findings:** ~7

- REQ-ID concurrent allocation (EDGE-10, ADVO-PROC-01) — two PRs both
  scan INDEX, both allocate next free ID, immutable so cannot rename.
- Project overlay collisions (EDGE-11, ARCH-PROC-04 related) — same
  REQ-ID at root and at `projects/<p>/`; overlay precedence undefined.
- Amendment number concurrent allocation (EDGE-15).
- CHG number allocation has no tool (INHER-17).
- File path renames silently break every prior REQ-ID @ path reference
  (EDGE-12, ARCH-PROC-09 related).
- References to deprecated REQs not distinguished from references to
  active REQs (EDGE-13).
- Typo-induced ghost REQs in `@covers` annotations (ADVO-PROC-07).

Constituent findings: EDGE-10, EDGE-11, EDGE-12, EDGE-13, EDGE-15,
ADVO-PROC-01, ADVO-PROC-07, INHER-17, INHER-18.

**Recommended CHG:** ADR-0004 amendment with merge-time reallocation
protocol; project-overlay namespacing rule; per-class ID allocation
tool (`spec_lint allocate-chg`, `spec_lint allocate-amendment`); xref
must validate ID-in-file not just path-exists.

---

### THEME-V — Inter-agent trust + UX gaps

**Severity:** SERIOUS · **Streams:** 4/12 · **Constituent findings:** ~5

The architecture treats agents as workflow steps, not as actors whose
outputs require provenance. Surfaced by PREM-17, PARTY-UX-01,
PARTY-UX-02, INHER-15.

- No inter-agent trust contract; no hedge-preservation rule (PREM-17 —
  TEA dropped PM's "TBD" hedge, shipped wrong REQ green).
- Session resume hook output format spec is one bullet (PARTY-UX-01) —
  load-bearing UX least specified.
- Agent-facing diagnostic format for the ~30 gates is completely
  unspecified (PARTY-UX-02). What does a Dev agent see when
  `commit-trailers-valid` rejects?

**Recommended CHG:** ADR for agent diagnostic format (structured
output for downstream agents to parse); ADR for inter-agent
provenance (hedge-preservation, unconfirmed-output markers, audit
of derivation chains).

---

### THEME-W — Anthropic-client transitive imports + GAS-runtime carve-out

**Severity:** SERIOUS · **Streams:** 3/12 · **Constituent findings:** ~4

- `direct-anthropic-import-banned` is a static-import grep (PREM-14) —
  transitive imports via MCP/BMAD/vendored harnesses bypass; cost
  telemetry leaks; cache bypassed.
- GAS V8 has no native `cache_control` (ADVH-CRIT-12) — ADR-0007 §5
  "enabled by default" silently false in E2E tier.
- `direct-anthropic-import-banned` is "every PR" from PHASE-1 but no
  production target until PHASE-3 (READY-14) — intermediate state
  unspecified.
- TS/Python mirroring contract undefined (ADVS-PROC-05).

**Recommended CHG:** ADR-0007 amendment with closure of import
prohibition (dep-graph not static-import); GAS-runtime carve-out
documented; intermediate-state contract for `direct-anthropic-import-
banned` between PHASE-1 and PHASE-3; cross-language equivalence gate.

---

### THEME-X — Append-only spec calcification (long-horizon risk)

**Severity:** SERIOUS · **Streams:** 2/40 · **Constituent findings:** 2 (PREM-07, STAKE-PROC-020) <!-- corrected per META-SER-003; see corrections.md -->

PREM-07 surfaced this in Wave 1; STAKE-PROC-020 surfaced an
independent formulation in Wave 4. ADR-0004 §1 + §7 enforce
append-only. At scale (~600 REQs), supersession chains 4-deep produce
a 22 MB matrix and a 4m17s rebuild; developers stop reading specs,
drift ensues. The architecture has no garbage-collection or
compaction path. STAKE-PROC-020 adds that the near-duplicate
anti-aliasing rule (§4) will increasingly fire false positives
against deprecated REQs, forcing either threshold-loosening or
manual exclusion lists.

Two independent surfacers from different methods + waves (PREM
forward-looking pre-mortem; STAKE persona-stakeholder simulation
including a future-architect lens). Originally classified Tier C
based on the (since-corrected) 1/12 count; revised to Tier B per
two-independent-surfacer criterion.

**Recommended CHG:** ADR-0004 amendment with compaction protocol
(merge superseded chains under a single canonical REQ at a defined
threshold; retain history in a separate compacted archive).
Lower-priority but flag for PHASE-5+ work.

---

### THEME-Y — PHASE-5 §Scope numbering bug (two §4s)

**Severity:** PROCESS · **Streams:** 5/12 · **Constituent findings:** ~5

Trivial editing defect, but it appears in the architecture artifact
that is supposed to be lintable. Indicative of the broader cross-
document-consistency gap.

ADVS-SERI-06, ADVO-PROC-04, STRUCT-10, PROSE related, IND-PROC related.

**Recommended CHG:** trivial doc fix (renumber); expand
`openspec-validate` gate to cover PHASE-* files structurally.

---

### THEME-Z — `commit-trailers-valid` trigger surface contradicted three ways

**Severity:** CRITICAL · **Streams:** 3/12 · **Constituent findings:** ~3

Already captured under THEME-B (trailer schema), pulled out as a
separate theme because it's so tactical: the gate's trigger surface
is named `pre-receive hook` (ADR-0008 §1), `pre-commit` (ADR-0008 §5),
and `PreToolUse(Bash:git commit)` (ADR-0005 §6). Each leaves a
different bypass open. Implementation cannot proceed until the
canonical surface is named once (READY-03, ADVS-CRIT-02, ADVH-SER-08).

Rolled into THEME-B for resolution sequencing.

---

## Pre-existing findings (STATUS.md) — disposition after this audit

| Pre-existing | Status after audit | Mapped to theme |
|---|---|---|
| C1 (INDEX empty) | CLOSED (CHG-0014 merged) | — |
| C2 (REQ-ARCH format) | OPEN; expanded by THEME-G | G |
| C3 (PHASE-1 incomplete) | OPEN; subsumed by THEME-A (BMAD drift) | A |
| C4 (no CI execution) | CLOSED (CHG-0013) | — |
| C5 (P1 + P5 uncovered) | OPEN; reinforced by THEME-C | C |
| S1 (mock FP) | OPEN; tactical, falls under THEME-I | I |
| S2 (xref inline backticks) | OPEN; tactical, EDGE-12 related | (specific) |
| S3 (bmad-direct-ref bypassable) | OPEN; tactical, THEME-A related | A |
| S4 (6 rules without REQ-SPEC) | CLOSED (CHG-0030) | — |
| S5 (real_repo_passes trivial) | OPEN; tactical | (specific) |
| P1-P5 process gaps | OPEN; subsumed by THEMES H, M, U | H, M, U |
| P6 (test_mutations unannotated) | CLOSED (CHG-0030) | — |
| NEW-1 (generated_at exemption) | OPEN; specific to CHG-0014b | (specific) |
| NEW-2 (tests not derived from REQ Acceptance) | OPEN; queued as ADR-0009 (not yet authored) | (specific) |
| NEW-3 (BMAD review skills not in CHG workflow) | OPEN; this audit is partly a response | (specific) |

12 still-open pre-existing findings now have thematic homes. The new
audit adds ~26 themes covering ~80-100 distinct issues beyond the
pre-existing ledger.

---

## Proposed resolution sequence

Sequenced by dependency and risk. Each tier is a coherent unit of
work that closes a thematic cluster.

### Tier 0 — Doc-only sync (low-risk, high-noise-reduction)

Land these first. Each is small, doc-only, but eliminates the
contradictions that infect every other review.

- **CHG-A** — BMAD strategy sync (THEME-A): sync ARCHITECTURE.md §9,
  ADR-0001, PHASE-0, PHASE-1 to native-Skills + `_bmad/` reality.
- **CHG-B** — ADR-0002 §7 renumber (THEME-A continued): fix the §7
  collision; amendment-introduced sections become Decision items 8-10.
- **CHG-C** — PHASE-5 §Scope numbering fix (THEME-Y).
- **CHG-D** — "The paper" citation (THEME-P): add ADR-0004 References
  section with stable `REF-PAPER-0001`.

### Tier 1 — Schema definitions (medium, foundational)

- **CHG-E** — Trailer registry + checkpoint exemptions schema
  (THEMES B, Z): full trailer registry, `checkpoint_exemptions.yaml`
  schema, resolve pre-receive/pre-commit/PreToolUse trigger conflict.
  Blocks any PHASE-2 work on `validate_commit.py`.
- **CHG-F** — REQ allocator (THEME-R partial): ship
  `tools/spec_lint allocate <domain>`; unblocks all ID allocation in
  subsequent CHGs.
- **CHG-G** — Status enum reconciliation (THEME-O): one mapping
  table; explicit transitions; coverage-gate population defined.
- **CHG-H** — TASK-type taxonomy ADR (THEME-H partial): defines `gate`-
  type, `docs`-type, `code`-type, etc. Unblocks every reference to
  these types.

### Tier 2 — Phase-reordering authorization

- **CHG-I** — Phase-reorder ADR (THEME-K): authorizes PHASE-2a
  (traceability runtime MVP) alongside PHASE-1 completion; defines
  phase-status enum; cross-phase hotfix waiver; prior-phase regression
  check; re-gate trigger for amendments affecting earlier phases.
  Required before any PHASE-2 implementation.

### Tier 3 — Meta-gate strengthening

- **CHG-J** — `gate-coverage` rewrite (THEME-C): semantic gate
  correctness contracts; per-principle and per-section coverage;
  bootstrap rule for self-coverage; expand inventory.
- **CHG-K** — Push invariant honest enforcement (THEME-F): server-side
  post-receive gate, or downgrade promise language.
- **CHG-L** — `phase-exit` gate fixes (THEME-K continued): prior-phase
  regression, opportunistic forward work waiver.

### Tier 4 — Test tier hardening

- **CHG-M** — Real-vs-fake adapter boundary (THEME-I): ADR-0006 +
  ADR-0007 amendment; deterministic clock disposition; behavior
  equivalence; `tier:` schema; GAS caching carve-out.
- **CHG-N** — Stochastic tier statistical hardening (THEME-J):
  minimum-N, calibration discipline, declared-vs-measured cost
  reconciliation, `cost-tier` enumeration, baseline pinning,
  multiple-comparisons policy.
- **CHG-O** — Anti-aliasing rule redesign (THEME-Q).
- **CHG-P** — Anthropic-client transitive-import closure (THEME-W).

### Tier 5 — Hook implementation hardening (prep for PHASE-2a code)

- **CHG-Q** — Hook matching grammar (THEME-D): glob specificity, race
  conditions, first-commit causality loop, post-merge sync semantics.

### Tier 6 — Missing artifact-type ADRs (cluster — can parallelize)

- **CHG-R1** — STATUS.md ADR (THEME-H)
- **CHG-R2** — CHG envelope structure ADR (THEME-H)
- **CHG-R3** — TEA scope/skills/interface ADR (THEME-H)
- **CHG-R4** — Epic/Story format ADR (THEME-H)
- **CHG-R5** — Secrets management ADR (THEME-H)
- **CHG-R6** — Branch/PR conventions ADR (THEME-H)
- **CHG-R7** — `_TEMPLATE.md` schemas ADR (THEME-H)

### Tier 7 — REQ-ARCH-* migration

- **CHG-S** — REQ-ARCH-* migration (THEME-G): move to
  `architecture-invariants.spec.md`; split compounds; drop hardcoded
  counts. Depends on CHG-F, CHG-H.

### Tier 8 — CLAUDE.md/ARCHITECTURE.md SoT

- **CHG-T** — Operating-principles SoT designation + consistency lint
  (THEME-L).

### Tier 9 — Identifier discipline

- **CHG-U** — ID allocation hardening (THEME-U): merge-time
  reallocation, project-overlay namespacing, `allocate-chg`,
  `allocate-amendment`, xref ID-in-file validation.

### Tier 10 — Amendment discipline

- **CHG-V** — Universal amendment-log + amendment-vs-supersession
  rule (THEME-M): stub sections in 6 ADRs; date column; classification.

### Tier 11 — Operational calibration

- **CHG-W** — `tools/ci/calibration.yaml` discipline (THEME-T).

### Tier 12 — Cross-doc consistency lint + ARCHITECTURE.md slimming

- **CHG-X** — Reduce ARCHITECTURE.md summary sections to pointers;
  promote Epic reconciliation gate; merge tier enumeration into
  ADR-0006; cut §12 (THEME-N).
- **CHG-Y** — Cross-doc consistency lint rule (general — THEME-N
  enforcement layer).

### Tier 13 — Inter-agent trust + UX

- **CHG-Z1** — Agent diagnostic format ADR (THEME-V).
- **CHG-Z2** — Inter-agent provenance ADR (THEME-V).

### Tier 14 — Phase-5 product workflow

- **CHG-AA** — Product workflow phase (THEME-S): the largest open
  question — does product content become part of architecture, or get
  its own phase, or trigger a rebind of PHASE-5?

### Tier 15 — Long-horizon discipline

- **CHG-BB** — Spec compaction protocol (THEME-X).

### Tier 16 — Architecture artifact rebaseline

- **CHG-CC** — Re-issue ARCHITECTURE.md as authoritative; PHASE-0
  re-gate against the post-audit corpus.

---

## Decision points before kicking off the resolution program

1. **Scope.** Resolve all 26 themes, or triage and accept a defined
   risk-debt list? "Resolve thoroughly" is a multi-month program. A
   minimum-viable-architecture might address Tier 0-3 only (~12 CHGs).
2. **Phase-2 timing.** Build PHASE-2a (traceability runtime MVP) in
   parallel with Tier 1-2 doc work, or strictly serial (all docs first,
   then code)?
3. **Product workflow (THEME-S).** Insert PHASE-PROD into the phase
   model, amend §12 to bring product content into architecture, or
   delete PHASE-5 entirely until product workflow is defined?
4. **Amendment vs supersession (THEME-M).** Treat ADR-0002 amendment
   0001 as informally legal historical precedent, or formally
   supersede ADR-0002 with ADR-0009? Affects the
   amendment-discipline ADR design.
5. **Long-horizon compaction (THEME-X).** Do we accept ADR-0004's
   append-only without compaction (and revisit at scale), or design
   compaction now?
6. **BMAD review in CHG workflow (STATUS.md NEW-3).** Make
   adversarial-review skill invocation mandatory for every CHG
   proposal? This audit's own provenance is governed by that open
   question.
7. **Single-author throughput vs parallel agents (PARTY-PROC-03).**
   Architecture currently assumes strict serial phase ordering. With
   multiple parallel agents/sessions, this caps throughput. Acceptable
   for now or amend?

---

## Convergence diagnostic

After Wave 1 (12 streams), novel findings continued to surface in every
stream. User direction was to lock COMPOSITE-V2 as the convergence
metric and iterate until Gate 6 (<10% marginal novelty) is met.

## Waves 2 and 3 supplement

### Wave 2 — 8 sub-agents (methodology diversity)

Methods added: socratic elicitation (SOC-), first-principles (FIRST-),
red-team (RED-), retrospective (RETRO-), distillator (DISTILL-),
validate-prd (VALID-), Winston solo (WIN-), Amelia solo (AME-).

**Wave 2 marginal novelty: ~50%** (added 16 new themes).

New themes:
- **THEME-AA — Adversarial enforcement gap** (RED-): supply-chain
  attacks against vendored substrate, content-integrity gates,
  journal-forgery defenses, gate-coverage canaries
- **THEME-BB — ADR supersession protocol** (RETRO/PARTY/COURSE): `superseded_by`
  frontmatter exists but unused; complete rewrites should supersede
- **THEME-CC — Missing test tiers (security, perf)** (RETRO)
- **THEME-DD — Phase regression state machine** (RETRO): no protocol
  for prior-phase regression detected during current-phase work
- **THEME-EE — Secrets/credentials specification** (RETRO/RED/ARCH)
- **THEME-FF — Local development environment** (RETRO): no Node/Python/clasp pins
- **THEME-GG — Hook ABI / Claude Code hook syntax** (AME): glob/regex/
  alternation/payload unspecified
- **THEME-HH — BMAD upstream dependency risks** (WIN): license,
  internal config-resolver behavior
- **THEME-II — Network dependency in commit hook** (FIRST): offline
  commits structurally impossible
- **THEME-JJ — Test runner ownership** (WIN): no phase claims pyproject.toml
- **THEME-KK — Append-only NOT gated for ADR amendments** (FIRST)
- **THEME-LL — BMAD CWD discipline 4-phase gap** (FIRST)
- **THEME-MM — Retroactive compliance remediation** (FIRST/AME): PHASE-2
  gates activate against immutable PHASE-0/1 history
- **THEME-NN — PRD→REQ traceability ungated** (FIRST): only REQ→TEST enforced
- **THEME-OO — Long-running branch matrix conflicts** (RETRO): no merge driver
- **THEME-PP — Anti-aliasing n-gram vs semantic** (PREM/FIRST): wrong defense

### Wave 3 — 8 sub-agents (persona + editorial mutation)

Methods added: PM solo (PM-), analyst solo (MARY-), UX solo (SALLY-),
tech writer solo (PAIGE-), edit-PRD (EDIT-), correct-course (COURSE-),
checkpoint-preview (CHECK-), devil's advocate (DEVIL-).

**Wave 3 marginal novelty: ~30-37%** (added 9 new themes).

New themes:
- **THEME-RR — Product workflow primitives missing** (PM): no
  experimentation, A/B, feature flags, cohorts, success metrics, or
  removal/deprecation telemetry
- **THEME-SS — Glossary and terminology drift** (PAIGE): no canonical
  glossary; "SoT", "P4", "staging", "promotion", "addressable artifact
  network", "substrate PR", "gate-type task", "sandwich layer"
  scattered; "Apps Script"/"AppScript"/"appscript" co-exist
- **THEME-TT — Audience clarity** (PAIGE): documents conflate AI agent
  and human readers without disambiguation
- **THEME-UU — Principle independence / meta-architecture** (DEVIL):
  the five principles aren't independent — P2/P3 derivable from P1;
  P5 is tooling not principle; P4 is workflow. `gate-coverage` exists
  to police a structure that's itself an artifact of too many principles
- **THEME-VV — Principle list append-only protection** (DEVIL):
  `gate-coverage` creates pressure to SHRINK principle list (remove
  failing items) rather than ADD gates
- **THEME-WW — Determinism vs idempotence** (MARY): used interchangeably
  in ADR-0005, but PHASE-2 property test is idempotence not determinism
- **THEME-XX — Trailer signal quality / checkpoint reconciliation** (DEVIL):
  auto-produced checkpoint trailers at moments of uncertainty pollute matrix
- **THEME-YY — Stack consolidation** (DEVIL): BMAD/TEA/OpenSpec is one
  system trying to look like three; integration seams ARE the
  parallel-convention cost P5 was meant to forbid
- **THEME-ZZ — Forward references and reading order** (PAIGE): no
  documented onboarding path; implied order has forward refs

### Per-stream marginal novelty (Wave 2+3)

| Stream | Wave | Marginal novelty |
|--------|------|------------------|
| SOC- | 2 | ~30% |
| RED- | 2 | ~70-80% (supply-chain category) |
| RETRO- | 2 | ~60% |
| VALID- | 2 | ~30% |
| WIN- | 2 | ~50% |
| DISTILL- | 2 | ~40% |
| FIRST- | 2 | ~50% |
| AME- | 2 | ~60% (hook ABI category) |
| PM- | 3 | ~50% (product workflow category) |
| MARY- | 3 | ~50% |
| CHECK- | 3 | ~25-35% |
| COURSE- | 3 | ~15-25% |
| EDIT- | 3 | ~25-35% |
| DEVIL- | 3 | ~40-50% (meta-critiques) |
| SALLY- | 3 | ~20-30% |
| PAIGE- | 3 | ~30-40% |

### COMPOSITE-V2 gate status

| Gate | Status |
|------|--------|
| 1. Method coverage (8 categories) | ✓ MET (12+ methods used) |
| 2. Model coverage (≥3 models) | ✓ MET (opus + sonnet + haiku) |
| 3. Theme confirmation ≥90% (≥2 streams) | ✓ MET (~98%) |
| 4. Strong theme ≥75% (≥3 streams) | ✓ MET (~92%) |
| 5. Critical-theme ≥5 streams | ✓ MET (all critical themes 8+ streams) |
| 6. **Marginal novelty <10%** | **✗ NOT MET (~30-37% Wave 3)** |
| 7. Coherence floor ≥15% | ≈ within tolerance |

### Convergence projection

Theme-discovery rate is halving per wave (Wave 1 baseline: 2.2/pass;
Wave 2: 2.0/pass; Wave 3: 1.1/pass). If trend holds:

- Wave 4: ~15-20% marginal novelty (still above target)
- Wave 5: ~7-12% (likely meets target)
- Wave 6: <10% (target definitively met)

User direction: continue iterating to Gate 6 strictly. Wave 4 will use
remaining methods (model permutations on previous attitude-driven passes,
unused advanced-elicitation methods, additional persona-pair combos).

## Wave 4 supplement (8 streams, complete)

Methods added: red-team-sonnet (RED2-), retrospective-sonnet (RETRO2-),
edge-case-hunter-sonnet (EDGE2-), inheritor-sonnet (INHER2-),
validate-prd-sonnet (VALID2-), pre-mortem-sonnet (PREM2-),
stakeholder-simulation-opus (STAKE-, NEW METHOD),
counter-factual-opus (COUNTER-, NEW METHOD).

**Wave 4 marginal novelty: ~46%** (spike from STAKE+COUNTER new methods).

New themes (~17 added by Wave 4):

### From STAKE- (stakeholder simulation, ~10 new themes)

- **THEME-AAA — Commit signing / signed-graph requirement** (STAKE-CRIT-001):
  no signing obligation; `--no-gpg-sign` forbidden but no positive
  sign requirement
- **THEME-BBB — Secrets threat model + fork-PR isolation** (STAKE-CRIT-002):
  Anthropic API key never named in threat surface; fork-PR stochastic
  tests could exfiltrate via prompt injection
- **THEME-CCC — Operational / SRE surface** (STAKE-CRIT-004, 005):
  zero on-call surface; no SLO, runbook, paging, observability; 26 CI
  gates can block main at 3am with undefined consequence
- **THEME-DDD — Separation of duties** (STAKE-CRIT-007): same actor
  authors + validates + publishes; violates SOC2 CC8.1, ISO 27001 A.14.2.2
- **THEME-EEE — Journal storage integrity primitives** (STAKE-SER-008):
  no WORM, no S3 Object Lock, no cryptographic chain; `O_TRUNC` destroys
  audit trail silently
- **THEME-FFF — Supply chain attestation** (STAKE-PROC-010, SER-014, SER-015):
  no SLSA / in-toto / SPDX / checksum manifest for vendored 2.4 MB BMAD bundle
- **THEME-GGG — Cost upper bounds + kill switches** (STAKE-CRIT-011):
  `@cost-budget` has no upper bound; author can write tokens=10000000 unflagged
- **THEME-HHH — Vendor quota awareness** (STAKE-SER-012): Google Apps
  Script 6-min trigger limit, Drive API daily quotas not mentioned
- **THEME-III — Vendor lock-in / provider abstraction** (STAKE-SER-013):
  stochastic tier forbids fixtures = pay Anthropic per CI run forever
- **THEME-JJJ — Anthropic SDK supply chain asymmetry** (STAKE-PROC-016):
  BMAD has vendor+pin+smoke discipline; Anthropic SDK has nothing comparable

### From COUNTER- (counter-factual, ~9 new themes)

- **THEME-KKK — One-REQ-per-file alternative** (COUNTER-001): multi-REQ
  files chosen but never argued for
- **THEME-LLL — Matrix-on-demand vs committed** (COUNTER-002): `matrix-drift`
  gate exists *because* file is committed; remove commit and gate disappears
- **THEME-MMM — Trailer sidecar vs message-embedded** (COUNTER-005):
  trailers fight git tooling; `Checkpoint:` exemption is evidence of fragility
- **THEME-NNN — Phase DAG with explicit `requires:`** (COUNTER-006):
  numerical order ≠ dependency order; DAG more enforceable not less
- **THEME-OOO — Inverted `gate-coverage`** (COUNTER-008): gates declare
  what they enforce; ADR-0008 §1 becomes derived
- **THEME-PPP — Per-task event store** (COUNTER-011): dominant query is
  `audit TASK-NNNN`; session-scoped journals hit storage sub-optimally
- **THEME-QQQ — Anthropic-client transport/contract split** (COUNTER-013):
  mixes singleton (transport) with per-feature (sandwich layers)
- **THEME-RRR — Epic-vs-REQ reconciliation layer** (COUNTER-014):
  per-REQ surfaces drift commit-by-commit; Epic-level introduces fact-in-two-places
- **THEME-SSS — Trailer schema as machine-validated** (COUNTER-015):
  each ADR adds trailer keys without updating ADR-0005 §3 enumeration

### From RETRO2- (~3 new themes)

- **THEME-TTT — Agent identity attribution** (RETRO2-CRIT-007): no
  verified agent identity on commits; CI service account scope not specified
- **THEME-UUU — Hook-failure taxonomy** (RETRO2-CRIT-008): ADR-0005 §8
  catalogues container failures, not hook failures (hooks themselves can
  fail/timeout/produce partial output)
- **THEME-VVV — Model version transition protocol** (RETRO2-SER-009):
  Sonnet 4.6→4.7 cadence is recurring; no protocol for re-baseline

### From PREM2- (~2 new themes)

- **THEME-WWW — CLAUDE.md as contested authority surface** (PREM2-PROC-012):
  developer amends CLAUDE.md to override principles; agents treat in-scope
  CLAUDE.md as authoritative; no gate checks CLAUDE.md content for principle
  compliance
- **THEME-XXX — Checkpoint walker off-by-one** (PREM2-PROC-010): exempts
  red-state commits adjacent to checkpoints

### Confirmations + tactical additions (Wave 4)

The remaining ~5 Wave-4 themes are sharpenings of existing themes
(VALID2 on shallow-clone CI defeating history walk; EDGE2 on cosmetic-edit
exemption being undefined; RED2 sub-threshold green-start evasion).

## COMPOSITE-V2 status after Wave 4

| Gate | Status |
|------|--------|
| 1. Method coverage | ✓ MET (~15+ methods used) |
| 2. Model coverage | ✓ MET (opus + sonnet + haiku) |
| 3. Theme confirmation ≥90% | ✓ MET (~98%) |
| 4. Strong theme ≥75% (≥3 streams) | ✓ MET (~88% post-Wave-4) |
| 5. Critical-theme ≥5 streams | ✓ MET |
| 6. **Marginal novelty <10%** | **✗ NOT MET (~46% Wave 4 average)** |
| 7. Coherence floor ≥15% | ≈ within tolerance |

## Methodology insight for the codification ADR

Marginal novelty is empirically NOT a function of model diversity or
stream count. It is a function of methodology variance:

- **Tight-method permutations** (INHER2, EDGE2): converge to ~15-30%
- **Loose-method permutations** (RETRO2, VALID2, PREM2, RED2): plateau ~40-50%
- **Genuinely new methods** (STAKE, COUNTER): spike to ~60-70%

This means COMPOSITE-V2 Gate 6 set at "<10% marginal novelty" is only
achievable by exhausting the *methodology space*, not the model space.
Once all methodologies have been tried, marginal novelty drops, because
new model-permutations within tried methods converge.

**Practical implication for the methodology ADR:** the convergence
threshold must be defined relative to a specific methodology corpus.
"<10% marginal novelty using methods M1...M_n" is meaningful;
"<10% marginal novelty in absolute terms" is unachievable because
new methods can always be invented.

Recommended ADR formulation:
- Define a fixed methodology catalog (e.g., 15 named methods).
- Convergence = "<10% marginal novelty across model permutations
  within the catalog."
- Catalog extensions are explicit ADR amendments.
