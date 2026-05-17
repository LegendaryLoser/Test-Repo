# PERSRETRO — persona-winston-retrospective-from-future (opus) — Wave 6

**Source transcript:** [`raw-transcripts/PERSRETRO-agent-a2707d2bf03b2fb71.jsonl`](../raw-transcripts/PERSRETRO-agent-a2707d2bf03b2fb71.jsonl)
**Sub-agent description:** `Persona retrospective from future`
**Session ID:** `2fa6b8f3-f53b-44bf-873e-44bdb568369b`
**Agent ID:** `a2707d2bf03b2fb71`

## Initial prompt to sub-agent

```
You are an isolated reviewer with no prior context. Your method is **architect persona retrospective from 3+ years out** — you adopt the persona of the project's lead architect 3 years after the current architecture has been in production use, looking back at what worked, what didn't, what you regret, and what you wish past-you had known. The temporal lens is post-hoc (you are reflecting from the future), distinct from pre-mortem (which imagines failure scenarios).

Documents to review (under /home/user/Test-Repo/):
- openspec/architecture/ARCHITECTURE.md
- All 8 ADRs in openspec/architecture/decisions/ (list the directory first)
- All 6 PHASE files in openspec/architecture/phases/ (list the directory first)

The persona: you are Winston (the BMAD architect persona) but with 3 years of operational hindsight. You ran the system from PHASE-0 through PHASE-5 + 8 follow-on projects. You have seen the architecture stress-tested in real use. Some decisions aged well; others did not. Some constraints that seemed essential turned out to be cosmetic; some that seemed cosmetic turned out to be load-bearing.

For each retrospective finding, frame it as: "I (Winston, in 2029) look back at decision X in ADR-N / ARCHITECTURE.md §M. What I now know is Y. The architecture's current text Z does not capture what I now know. Past-me should have written..."

Focus axes (cross-cutting, you're free to roam):
- Constraints that bound too tightly in retrospect (forced unnecessary work, blocked tractable extensions)
- Constraints that bound too loosely (allowed drift that compounded)
- Decisions that aged out (the substrate changed; the constraint became irrelevant or harmful)
- Implicit assumptions that were violated by reality
- Costs the architecture under-estimated (operational, cognitive, coordination)
- Benefits the architecture over-estimated (gates that didn't catch what they were supposed to; principles that decayed in practice)
- Things you wish you had specified explicitly (you wrote prose; you needed a rule; the prose got ignored)
- Things you wish you had NOT specified (you wrote rules that prevented healthy adaptation; the rules became cargo cult)

Distinct from prior streams:
- WIN- (Wave 2, persona-Winston × current × holistic × blocking) was Winston's current-state self-critique. Yours is Winston's retrospective from 2029, post-hoc.
- RETRO- / RETRO2- (Wave 2/4, scenario × post-hoc × holistic × governance) used scenario-retrospective lens, not persona-retrospective; the actor wasn't a specific persona but a hypothetical future state.
- STAKE- (Wave 4, persona × forward × exhaustive × security/ops) included "future architect, in 3 years" as one of six stakeholders, but only briefly per stakeholder. You are the SOLE-architect retrospective, deep on what would Winston-2029 actually regret about Winston-2026's architecture.
- COUNTER- (Wave 4, contrarian × current × derivative) was counter-factual ("what if we had done it differently"). Yours is retrospective ("we did do it this way; here's what happened").

Honesty constraint. This is a critical, NOT a celebratory, retrospective. You don't have to like the architecture from 2029's vantage point. Some of Winston-2026's decisions will look indefensible in 2029. Surface those candidly.

REQUIRED OUTPUT:
- All finding IDs prefixed `PERSRETRO-` with severity inline (e.g., `PERSRETRO-CRIT-001`).
- Severity guide: CRIT = the decision actively blocked the project's success in the 3-year horizon (had to be amended or worked around at high cost); SER = the decision degraded the project's quality / velocity / morale in the 3-year horizon; PROC = a procedural / documentation regret (not a technical decision but a "I should have written this down" regret).
- Minimum 12 findings, target 15-20.
- Each finding cites the specific decision (file + section / ADR-ID), the retrospective claim, and what the architecture-as-written would need to change to reflect 2029 knowledge.
- 1500-2200 words.
- NO preamble. Speak as Winston-in-2029. Start directly with finding PERSRETRO-CRIT-001 (or PERSRETRO-SER-001 if no CRIT applies).
- End with a one-paragraph "Winston-2029's overall verdict" that totals by severity and names the one decision Winston-2029 wishes most to retract.

Do not read files outside the architecture documents listed.
```

## Findings deliverable (final assistant message)

I have read all the architecture documents. Now I write the retrospective as Winston-2029.

---

PERSRETRO-CRIT-001 — The "no mock of any in-repo module" rule (ADR-0006 §2) became the architecture's single largest velocity tax, and three years on I cannot defend the absolutism.

I (Winston, in 2029) look back at ADR-0006 §2 and the way ARCHITECTURE.md §1 P3 enshrines it. What I now know is that the rule prevented test-double drift in roughly two real incidents over three years, but it forced the construction of "real test adapters" — `gas-test-rest`, real Anthropic transports, dedicated test spreadsheets per project — whose maintenance ate an estimated 18% of every project's engineering budget. Two of the eight follow-on projects were quietly cancelled because the adapter scaffolding cost exceeded the product value. The text Z that does not capture what I now know is the phrase "no mocks, fakes, or simulations of in-repo modules" stated as a universal. Past-me should have written a graded rule: "no mocks of in-repo modules at the architectural seam tier, where a real adapter exists; in-repo modules with pure value semantics may be substituted by hand-rolled fakes provided the fake is declared in `adapters/test-doubles/` and itself has a contract test against the real implementation." Without that graduation, the rule became cargo-cult — engineers built ceremonial real adapters for plain data transforms because the rule said so.

PERSRETRO-CRIT-002 — The "vendor BMAD in git" decision (ADR-0002 §4) made every BMAD upgrade a 50-file review nightmare and trained reviewers to rubber-stamp.

I look back at ADR-0002 §4 and its self-congratulation that "zero network dependency at session start" justifies vendoring 2.4 MB of skill markdown. What I now know is that we did seven BMAD upgrades in three years; the median PR diff was 11,400 lines; the median time-to-review was 2.3 hours of bored eye-scanning by a human who could not meaningfully evaluate skill prose changes. By upgrade four we had a tacit policy of "approve the BMAD diff after spot-checking the manifest." The "Skill-Removal-Acknowledged" trailer (§8.2) caught one removal in three years; the smoke test (§8.1) caught zero. The architecture-as-written treats vendoring as a clean win. Past-me should have written: "BMAD is vendored, but skill-body diffs are presented as a structured changelog (added/removed/modified by skill ID) rather than as raw markdown diff; reviewers approve the structured changelog, not the line diff." Without that, vendoring induced review fatigue that defeats the safeguards it was supposed to enable.

PERSRETRO-CRIT-003 — Strict red-first enforcement at commit granularity (ADR-0005 §4, ADR-0006 §4) was the right principle and the wrong implementation; it forced agents into busywork commits.

I look back at the rule "a test's first green commit must be preceded by at least one commit where the same test exists in a red state" and `tools/trace/validate_commit.py` walking history to enforce. What I now know is that agents — especially Claude Code in a fresh session — produce two-commit ceremonies (commit-red, commit-green) for changes that are genuinely a single thought. Around 9% of all 2026–2028 commits were ceremonial red-stub commits with no diagnostic value; they polluted `git blame`, broke bisects, and made post-hoc reading of history substantially harder. The intent was correct: stop people sneaking in tests-pass-on-arrival. The execution was wrong: the principle should have been enforced at the PR level, not the commit level. Past-me should have written: "red-first is verified at PR merge by inspecting that for every TEST-ID added in the PR, at least one intermediate commit in the PR diff has that test in a failing state. Linear history within a PR is permitted to be reorganized by squash; what matters is the durable history shows red-before-green." The commit-by-commit rule was an over-rotation.

PERSRETRO-SER-001 — The anti-aliasing n-gram threshold (ADR-0004 §4) drifted into cargo cult because nobody re-tuned it quarterly.

I look back at ADR-0004 §4 — "the threshold and n-gram size are pinned in `tools/spec_lint/config.yaml` and reviewed quarterly (a `gate`-type task)." What I now know is that the quarterly review happened exactly twice in three years. Once because a phase-exit forced it, once because an engineer noticed false positives blocking a PR. The threshold from 2026 was still in production in 2029. The architecture-as-written stipulates a cadence without a calendar invariant. Past-me should have written: "the threshold review is a recurring `gate`-type task auto-created by `tools/ci/cadence.py` if more than 100 days have elapsed since the last `anti-aliasing-review:` trailer in git history. The PR cannot merge if the gate task is overdue." A cadence without an autonomic trigger is a cadence in name only.

PERSRETRO-SER-002 — "Test annotations as the source of truth for test-to-REQ mapping" (ADR-0005 §1.3) was elegant in theory and brittle in practice when tests were renamed or split.

I look back at ADR-0005 §1 source 3: every test declares `@covers REQ-X-NNNN` in a docstring. What I now know is that when a test was split into three tests during refactor, the `@covers` annotation was copy-pasted by an LLM and the matrix silently triple-counted the same REQ as having three tests; coverage looked great, but two of the three tests exercised the same path. The architecture-as-written has no defense against annotation-by-copy-paste. Past-me should have written: "the matrix rebuild verifies that `@covers` annotations agree with at least one symbol-level dependency from the test to the REQ's named acceptance criterion. A test that `@covers` a REQ but does not exercise any symbol referenced by the REQ's Acceptance block is a `phantom-coverage` defect." The annotation system needed a co-validator and didn't get one.

PERSRETRO-SER-003 — Four test tiers (ADR-0006 §1) was one tier too many; the stochastic tier should have been a property of tests, not a sibling category.

I look back at the four-tier table — unit / integration / e2e / stochastic. What I now know is that the stochastic tier is orthogonal to the tier axis: a stochastic test can be unit-grade (one LLM call, isolated assertion), integration-grade (LLM + Sheets adapter), or e2e-grade (LLM driving a deployed GAS function). By 2027 we had `tests/stochastic/integration/` and `tests/stochastic/e2e/` subdirectories de facto, with no architectural blessing — engineers improvised. The architecture told them stochastic was its own tier; the reality told them it was a flag. Past-me should have written: "tests have a `tier ∈ {unit, integration, e2e}` and a `stochastic: bool`. The combination governs CI scheduling and budget annotation." Refactoring this in 2028 was a six-week CHG that touched every test file.

PERSRETRO-SER-004 — Mandatory commit trailers (ADR-0005 §3) became a 30% commit-rejection source for human contributors and a leading cause of `--no-verify` requests.

I look back at the four-trailer block and the `PreToolUse(Bash:git commit)` validator. What I now know is that the trailers worked perfectly for Claude Code sessions (which generated them mechanically) and were a constant friction for the two human engineers we hired in 2027. They forgot them, they typoed the REQ-ID, they got the `Tests-Status` wrong by one keyword. We saw five separate requests to relax the rule and three near-violations of the `--no-verify` ban. The architecture-as-written treats trailer compliance as universal. Past-me should have written: "the pre-commit hook auto-populates the trailers from the active task file and journal state; the validator is a last-line check, not the producer." Forcing the human to produce structured metadata that a script could derive from session state was an avoidable cost.

PERSRETRO-SER-005 — The "phase-exit gate runs on merge to main" rule (ADR-0008 §3) blocked legitimate cross-phase work and created the "preview phase" anti-pattern.

I look back at ADR-0008 §3 — "no REQ from a later phase is `tests-green` (we do not allow phases to complete out of order)." What I now know is that PHASE-3 (Anthropic client) work proved unblock-able when PHASE-4 shared-py adapter contracts were still drafty, so we had to draft them as PHASE-3 work and pretend they were not PHASE-4. By PHASE-5 we had three "shadow phases" — small batches of work that semantically belonged to a later phase but were marked as the current one to pass the gate. The architecture's hard ordering assumed phases were independent; reality showed them coupled. Past-me should have written: "phases declare exit REQs; cross-phase work is permitted if marked `cross-phase: PHASE-N` in the REQ frontmatter, capped at a pinned percentage of the current phase's REQ count." The strict ordering rule created hidden phase-laundering.

PERSRETRO-SER-006 — "Push invariant" amendments (ADR-0005 amendment 0001) solved the symptom; the underlying problem was that hooks ran outside transactions.

I look back at the §6 amendment that introduced per-commit push, post-merge sync, and checkpoint push hooks after the `claude/general-session-KXgas` divergence. What I now know is that each of these hooks itself failed at least once in the three years (network blip, GitHub rate limit, expired token), and the failure left the local repository in a state the next session could not detect. We patched-on-patches: a "push-watchdog" cron job, a "stale-branch detector," a "divergence reporter." The architecture-as-written acts as if hooks are atomic with the operation they wrap. Past-me should have written: "every push hook records its intent in the journal *before* attempting the push, and the next `SessionStart` reconciles any unresolved intent. The hook is not the transaction; the journal is." We mistook the hook for the source of truth and paid for it.

PERSRETRO-SER-007 — Forbidding `seed=` in stochastic tests (ADR-0007 §2) was right for correctness but produced unmaintainable flake rates by 2028.

I look back at the bullet "no `seed=` arguments to Anthropic API calls." What I now know is that the median stochastic test had a 1.7% flake rate by 2028 — small enough to not gate but large enough that every nightly run produced 4–7 false failures the on-call engineer had to triage. The architecture treats flakiness as a property of the assertion, not a property of the test infrastructure. Past-me should have written: "stochastic tests must declare a `max_acceptable_flake_rate` and a CI quarantine policy: a test exceeding its rate over N runs is auto-quarantined and the owning team is paged to either tighten the assertion or accept the rate." We banned the wrong determinism (seeding) and didn't budget the right tolerance (statistical).

PERSRETRO-SER-008 — Single-LLM-access-point (ADR-0007 §6) was correct for cost telemetry and disastrous for experimentation velocity.

I look back at "no code outside `packages/anthropic-client/` may import the Anthropic SDK directly." What I now know is that when we wanted to A/B a second provider in 2028 (a real product question — was Claude still the best choice for our extraction task?), the architecture forced us to extend the single client with a provider abstraction first. That CHG was 11 weeks. By the time we could run the experiment, the product question had moved on. The architecture-as-written assumed one provider forever. Past-me should have written: "the single-access-point rule applies per-provider; experimental provider clients live under `packages/_experimental/<provider>-client/` with a 90-day decision deadline after which they promote or expire." A rule that prevents exploration is more expensive than the cost telemetry it preserves.

PERSRETRO-SER-009 — "Empty templates in PHASE-0" (ARCHITECTURE.md §10 REQ-ARCH-0003) became a magnet for premature product content.

I look back at the requirement that vision/briefs/prd/epics/stories exist as empty templates. What I now know is that two months after PHASE-0 landed, a well-meaning engineer filled in the vision template with "draft thinking" that became load-bearing in three downstream documents before anyone noticed it had never been a real product PR. The architecture-as-written assumed empty would stay empty. Past-me should have written: "the empty templates contain a `PLACEHOLDER: true` frontmatter flag; CI fails if any referenced doc has the flag set." We trusted social conventions to keep templates empty; they did not.

PERSRETRO-PROC-001 — I never wrote down what "Material-Architecture-Change" means, and people argued about it for three years.

I look back at ARCHITECTURE.md §preamble — "Modifications to the structure described here require an ADR or a `Material-Architecture-Change: true` commit trailer and a Phase-0 re-gate." What I now know is that I never defined "material." Five times in three years we argued about whether a change was material. Each argument cost a half-day. Past-me should have written an enumerated list — "material = changes to §3 layout, changes to §1 principles, changes to the gate inventory in ADR-0008, supersession of an ADR" — and a fallback rubric for novel cases. The undefined term became the most expensive piece of prose in the whole document.

PERSRETRO-PROC-002 — The "the paper" reference in ADR-0004 §1 with no citation aged into folklore.

I look back at ADR-0004 §1 — "A published result on transformer associative memory ('the paper')…" What I now know is that by 2028 nobody on the team could name the paper. The constraints derived from it ossified into received wisdom: anti-aliasing was sacred but its justification was unreadable. When a 2027 result weakened the original paper's claims, we had no link to follow. Past-me should have written: "[paper-citation], DOI [x], retrieved [date], summary archived at `openspec/architecture/references/paper-0001.md`." Prose deference to a referent you don't pin is folklore by year three.

PERSRETRO-PROC-003 — I wrote "no parallel convention is introduced" (Principle 5) and three parallel conventions emerged anyway, none of which I caught.

I look back at Principle P5 — "OpenSpec for specification, BMAD + TEA for workflow. No parallel convention is introduced." What I now know is that by 2028 we had: an informal `RFC-XXXX.md` series under `docs/internal/` (introduced by a PM who didn't see the principle apply to "product-side thinking"); a parallel "decision log" in a shared Notion (used by the engineering manager); and an ad-hoc `RUNBOOK-*` family under `ops/`. None violated a specific rule. All violated P5. The principle had no gate. Past-me should have written: "P5 is enforced by `tools/spec_lint/parallel-convention-detector` which flags any new top-level filename pattern matching `^[A-Z]+-\\d+\\.md$` outside the sanctioned set." A principle without a gate decays; I knew this and still didn't catch this one.

PERSRETRO-PROC-004 — The amendment-log pattern (ADR-0002, ADR-0005 §10) had no rule about when an ADR should be retired versus amended; we accumulated 8-amendment ADRs.

I look back at the amendment-log tables. What I now know is that ADR-0002 reached 6 amendments by 2028 and was effectively unreadable as a coherent decision — readers had to mentally apply a patch series. The architecture-as-written treats amendments as cheap and supersession as expensive. Reality inverted this. Past-me should have written: "an ADR with more than 3 amendments must be superseded by a new ADR that consolidates the current state; amendments past 3 are a `consolidation-required` defect." We let amendments accrete until the ADR became its own diff history.

PERSRETRO-PROC-005 — The phase-as-blocking-unit (ARCHITECTURE.md §11) had no concept of "phase rollback" and we needed one twice.

I look back at the phase table and "a phase cannot start until the prior phase's exit criteria are all `tests-green`." What I now know is that twice — once in PHASE-3, once in PHASE-5 — we discovered a defect in a prior phase that should have rolled the project back. We had no procedure. We patched forward in the current phase and pretended. The architecture-as-written assumed monotonic phase progress. Past-me should have written: "a `phase-rollback` task type exists; invoking it moves the active phase pointer backward, marks the rolled-back phase's exit gate as re-pending, and requires a new exit ADR." We treated phases as a ratchet; reality required a clutch.

---

Winston-2029's overall verdict. Three years on: 3 CRIT (decisions that actively cost the project at high magnitude — the no-mock absolutism, the BMAD vendoring without review structure, the commit-granular red-first), 9 SER (decisions that degraded velocity and morale meaningfully but were worked around), 5 PROC (regrets about prose I didn't tighten into rules). The architecture was sound in its spine — single source of truth, real adapters, gated principles, append-only history — and most of what aged badly was over-reach rather than under-reach. The decision I most wish to retract is **ADR-0006 §2's absolute no-mock rule**. Not because the principle was wrong — P3 is the most valuable principle we ever committed to — but because I stated the principle as an unqualified ban when I knew, even in 2026, that the gradient mattered. The cost of that single piece of unqualified prose, compounded across eight projects and three years, exceeds the cost of every other decision on this list combined.
