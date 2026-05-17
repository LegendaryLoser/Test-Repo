# Raw audit corpus — manifest

Mechanically generated from the sub-agent task transcripts. Each row maps a stream prefix (as cited in `findings-index.md` and `consolidated.md`) to the raw `.jsonl` transcript and the extracted per-stream findings markdown. Generator is incremental — see [`persist-corpus.py`](persist-corpus.py): pass 1 ingests new transcripts from the container-local cache `/root/.claude/projects/-home-user-Test-Repo/<session>/subagents/`; pass 2 preserves rows for transcripts already on disk in `raw-transcripts/` from prior sessions.

**Note:** the `ARCH-` stream is not in this manifest. It was the in-context pass run by the main session (not a sub-agent), so it has no separate transcript — its findings live in the main-session transcript which is not part of this corpus.

**Total streams:** 43 sub-agent streams across waves 1, 2, 3, 4, 5, 6 (+ the in-context `ARCH-` stream).

**Total raw transcript size:** 7,501,752 bytes (~7.2 MB).

## Stream → transcript mapping

| Wave | Prefix | Method | Model | Agent ID | Raw transcript | Findings | Size (KB) |
|------|--------|--------|-------|----------|----------------|----------|-----------|
| 1 | `ADVH` | adversarial-general | haiku | `a75442bf62c957926` | [`raw-transcripts/ADVH-agent-a75442bf62c957926.jsonl`](raw-transcripts/ADVH-agent-a75442bf62c957926.jsonl) | [`findings/ADVH-findings.md`](findings/ADVH-findings.md) | 139 |
| 1 | `ADVO` | adversarial-general | opus | `a8dd79ee20ec2d432` | [`raw-transcripts/ADVO-agent-a8dd79ee20ec2d432.jsonl`](raw-transcripts/ADVO-agent-a8dd79ee20ec2d432.jsonl) | [`findings/ADVO-findings.md`](findings/ADVO-findings.md) | 149 |
| 1 | `ADVS` | adversarial-general | sonnet | `a101c290244165df1` | [`raw-transcripts/ADVS-agent-a101c290244165df1.jsonl`](raw-transcripts/ADVS-agent-a101c290244165df1.jsonl) | [`findings/ADVS-findings.md`](findings/ADVS-findings.md) | 149 |
| 1 | `EDGE` | edge-case-hunter | opus | `abf3f95219d0706c3` | [`raw-transcripts/EDGE-agent-abf3f95219d0706c3.jsonl`](raw-transcripts/EDGE-agent-abf3f95219d0706c3.jsonl) | [`findings/EDGE-findings.md`](findings/EDGE-findings.md) | 182 |
| 1 | `IND` | adversarial-general | opus | `a537eb5fa60f4e72c` | [`raw-transcripts/IND-agent-a537eb5fa60f4e72c.jsonl`](raw-transcripts/IND-agent-a537eb5fa60f4e72c.jsonl) | [`findings/IND-findings.md`](findings/IND-findings.md) | 151 |
| 1 | `INHER` | inheritor-framing | opus | `a0f191f798cfff918` | [`raw-transcripts/INHER-agent-a0f191f798cfff918.jsonl`](raw-transcripts/INHER-agent-a0f191f798cfff918.jsonl) | [`findings/INHER-findings.md`](findings/INHER-findings.md) | 151 |
| 1 | `PARTY` | party-mode | opus | `a72db282c4e152bde` | [`raw-transcripts/PARTY-agent-a72db282c4e152bde.jsonl`](raw-transcripts/PARTY-agent-a72db282c4e152bde.jsonl) | [`findings/PARTY-findings.md`](findings/PARTY-findings.md) | 163 |
| 1 | `PREM` | advanced-elicitation-pre-mortem | opus | `a1c78e2a771a55c60` | [`raw-transcripts/PREM-agent-a1c78e2a771a55c60.jsonl`](raw-transcripts/PREM-agent-a1c78e2a771a55c60.jsonl) | [`findings/PREM-findings.md`](findings/PREM-findings.md) | 176 |
| 1 | `PROSE` | editorial-review-prose | sonnet | `a07c1f539fac023b9` | [`raw-transcripts/PROSE-agent-a07c1f539fac023b9.jsonl`](raw-transcripts/PROSE-agent-a07c1f539fac023b9.jsonl) | [`findings/PROSE-findings.md`](findings/PROSE-findings.md) | 162 |
| 1 | `READY` | check-implementation-readiness | opus | `a75c2119fca66f68b` | [`raw-transcripts/READY-agent-a75c2119fca66f68b.jsonl`](raw-transcripts/READY-agent-a75c2119fca66f68b.jsonl) | [`findings/READY-findings.md`](findings/READY-findings.md) | 158 |
| 1 | `STRUCT` | editorial-review-structure | opus | `a503ec7eb147f2205` | [`raw-transcripts/STRUCT-agent-a503ec7eb147f2205.jsonl`](raw-transcripts/STRUCT-agent-a503ec7eb147f2205.jsonl) | [`findings/STRUCT-findings.md`](findings/STRUCT-findings.md) | 163 |
| 2 | `AME` | persona-amelia | sonnet | `ae7dabd92bf0ef542` | [`raw-transcripts/AME-agent-ae7dabd92bf0ef542.jsonl`](raw-transcripts/AME-agent-ae7dabd92bf0ef542.jsonl) | [`findings/AME-findings.md`](findings/AME-findings.md) | 158 |
| 2 | `DISTILL` | distillator | sonnet | `a8263f264435cbc68` | [`raw-transcripts/DISTILL-agent-a8263f264435cbc68.jsonl`](raw-transcripts/DISTILL-agent-a8263f264435cbc68.jsonl) | [`findings/DISTILL-findings.md`](findings/DISTILL-findings.md) | 161 |
| 2 | `FIRST` | advanced-elicitation-first-principles | sonnet | `afe9e82773aa1020b` | [`raw-transcripts/FIRST-agent-afe9e82773aa1020b.jsonl`](raw-transcripts/FIRST-agent-afe9e82773aa1020b.jsonl) | [`findings/FIRST-findings.md`](findings/FIRST-findings.md) | 161 |
| 2 | `RED` | advanced-elicitation-red-team | opus | `a89a1487164d515d8` | [`raw-transcripts/RED-agent-a89a1487164d515d8.jsonl`](raw-transcripts/RED-agent-a89a1487164d515d8.jsonl) | [`findings/RED-findings.md`](findings/RED-findings.md) | 162 |
| 2 | `RETRO` | retrospective | opus | `aeb34831758a76536` | [`raw-transcripts/RETRO-agent-aeb34831758a76536.jsonl`](raw-transcripts/RETRO-agent-aeb34831758a76536.jsonl) | [`findings/RETRO-findings.md`](findings/RETRO-findings.md) | 216 |
| 2 | `SOC` | advanced-elicitation-socratic | opus | `a4656be4309772170` | [`raw-transcripts/SOC-agent-a4656be4309772170.jsonl`](raw-transcripts/SOC-agent-a4656be4309772170.jsonl) | [`findings/SOC-findings.md`](findings/SOC-findings.md) | 159 |
| 2 | `VALID` | validate-prd | opus | `a6d85136a8adf5f6a` | [`raw-transcripts/VALID-agent-a6d85136a8adf5f6a.jsonl`](raw-transcripts/VALID-agent-a6d85136a8adf5f6a.jsonl) | [`findings/VALID-findings.md`](findings/VALID-findings.md) | 158 |
| 2 | `WIN` | persona-winston | opus | `a6fb8d990ac9e7901` | [`raw-transcripts/WIN-agent-a6fb8d990ac9e7901.jsonl`](raw-transcripts/WIN-agent-a6fb8d990ac9e7901.jsonl) | [`findings/WIN-findings.md`](findings/WIN-findings.md) | 153 |
| 3 | `CHECK` | checkpoint-preview | opus | `abfee06201b816a17` | [`raw-transcripts/CHECK-agent-abfee06201b816a17.jsonl`](raw-transcripts/CHECK-agent-abfee06201b816a17.jsonl) | [`findings/CHECK-findings.md`](findings/CHECK-findings.md) | 157 |
| 3 | `COURSE` | correct-course | opus | `a5bd87ec9c9916dce` | [`raw-transcripts/COURSE-agent-a5bd87ec9c9916dce.jsonl`](raw-transcripts/COURSE-agent-a5bd87ec9c9916dce.jsonl) | [`findings/COURSE-findings.md`](findings/COURSE-findings.md) | 166 |
| 3 | `DEVIL` | advanced-elicitation-devils-advocate | opus | `a8f3b70caeadee42d` | [`raw-transcripts/DEVIL-agent-a8f3b70caeadee42d.jsonl`](raw-transcripts/DEVIL-agent-a8f3b70caeadee42d.jsonl) | [`findings/DEVIL-findings.md`](findings/DEVIL-findings.md) | 166 |
| 3 | `EDIT` | edit-prd | opus | `a8dad88abd4233ac9` | [`raw-transcripts/EDIT-agent-a8dad88abd4233ac9.jsonl`](raw-transcripts/EDIT-agent-a8dad88abd4233ac9.jsonl) | [`findings/EDIT-findings.md`](findings/EDIT-findings.md) | 157 |
| 3 | `MARY` | persona-mary-analyst | opus | `a41bb283f821c8a53` | [`raw-transcripts/MARY-agent-a41bb283f821c8a53.jsonl`](raw-transcripts/MARY-agent-a41bb283f821c8a53.jsonl) | [`findings/MARY-findings.md`](findings/MARY-findings.md) | 157 |
| 3 | `PAIGE` | persona-paige-tech-writer | sonnet | `a11b22fa6de0406c3` | [`raw-transcripts/PAIGE-agent-a11b22fa6de0406c3.jsonl`](raw-transcripts/PAIGE-agent-a11b22fa6de0406c3.jsonl) | [`findings/PAIGE-findings.md`](findings/PAIGE-findings.md) | 158 |
| 3 | `PM` | persona-john-pm | opus | `aff1cc97ec9565394` | [`raw-transcripts/PM-agent-aff1cc97ec9565394.jsonl`](raw-transcripts/PM-agent-aff1cc97ec9565394.jsonl) | [`findings/PM-findings.md`](findings/PM-findings.md) | 153 |
| 3 | `SALLY` | persona-sally-ux | sonnet | `a8d1b481c259c823c` | [`raw-transcripts/SALLY-agent-a8d1b481c259c823c.jsonl`](raw-transcripts/SALLY-agent-a8d1b481c259c823c.jsonl) | [`findings/SALLY-findings.md`](findings/SALLY-findings.md) | 151 |
| 4 | `COUNTER` | counter-factual | opus | `a2d388c1125c79145` | [`raw-transcripts/COUNTER-agent-a2d388c1125c79145.jsonl`](raw-transcripts/COUNTER-agent-a2d388c1125c79145.jsonl) | [`findings/COUNTER-findings.md`](findings/COUNTER-findings.md) | 177 |
| 4 | `EDGE2` | edge-case-hunter | sonnet | `af0aa3c13cbacf00d` | [`raw-transcripts/EDGE2-agent-af0aa3c13cbacf00d.jsonl`](raw-transcripts/EDGE2-agent-af0aa3c13cbacf00d.jsonl) | [`findings/EDGE2-findings.md`](findings/EDGE2-findings.md) | 275 |
| 4 | `INHER2` | inheritor-framing | sonnet | `ab662e321df46151f` | [`raw-transcripts/INHER2-agent-ab662e321df46151f.jsonl`](raw-transcripts/INHER2-agent-ab662e321df46151f.jsonl) | [`findings/INHER2-findings.md`](findings/INHER2-findings.md) | 147 |
| 4 | `PREM2` | advanced-elicitation-pre-mortem | sonnet | `a2a0f163139591ae3` | [`raw-transcripts/PREM2-agent-a2a0f163139591ae3.jsonl`](raw-transcripts/PREM2-agent-a2a0f163139591ae3.jsonl) | [`findings/PREM2-findings.md`](findings/PREM2-findings.md) | 168 |
| 4 | `RED2` | advanced-elicitation-red-team | sonnet | `a0eb113fde740437e` | [`raw-transcripts/RED2-agent-a0eb113fde740437e.jsonl`](raw-transcripts/RED2-agent-a0eb113fde740437e.jsonl) | [`findings/RED2-findings.md`](findings/RED2-findings.md) | 163 |
| 4 | `RETRO2` | retrospective | sonnet | `a3608f6b3b6e5586e` | [`raw-transcripts/RETRO2-agent-a3608f6b3b6e5586e.jsonl`](raw-transcripts/RETRO2-agent-a3608f6b3b6e5586e.jsonl) | [`findings/RETRO2-findings.md`](findings/RETRO2-findings.md) | 222 |
| 4 | `STAKE` | stakeholder-simulation | opus | `ac2916602be951172` | [`raw-transcripts/STAKE-agent-ac2916602be951172.jsonl`](raw-transcripts/STAKE-agent-ac2916602be951172.jsonl) | [`findings/STAKE-findings.md`](findings/STAKE-findings.md) | 154 |
| 4 | `VALID2` | validate-prd | sonnet | `aa3cd57497916d4b8` | [`raw-transcripts/VALID2-agent-aa3cd57497916d4b8.jsonl`](raw-transcripts/VALID2-agent-aa3cd57497916d4b8.jsonl) | [`findings/VALID2-findings.md`](findings/VALID2-findings.md) | 180 |
| 5 | `GOV` | validate-prd-governance-focused | opus | `a285fe15ec2c6863e` | [`raw-transcripts/GOV-agent-a285fe15ec2c6863e.jsonl`](raw-transcripts/GOV-agent-a285fe15ec2c6863e.jsonl) | [`findings/GOV-findings.md`](findings/GOV-findings.md) | 156 |
| 5 | `GOVDEV` | advanced-elicitation-devils-advocate-governance-focused | opus | `a359e11aa2d88c000` | [`raw-transcripts/GOVDEV-agent-a359e11aa2d88c000.jsonl`](raw-transcripts/GOVDEV-agent-a359e11aa2d88c000.jsonl) | [`findings/GOVDEV-findings.md`](findings/GOVDEV-findings.md) | 161 |
| 5 | `META` | reasoning-tree-meta-audit | opus | `a092d80da9871922c` | [`raw-transcripts/META-agent-a092d80da9871922c.jsonl`](raw-transcripts/META-agent-a092d80da9871922c.jsonl) | [`findings/META-findings.md`](findings/META-findings.md) | 426 |
| 5 | `SEC` | persona-security-engineer-holistic | opus | `a594ed19164462bb9` | [`raw-transcripts/SEC-agent-a594ed19164462bb9.jsonl`](raw-transcripts/SEC-agent-a594ed19164462bb9.jsonl) | [`findings/SEC-findings.md`](findings/SEC-findings.md) | 152 |
| 6 | `PERSRETRO` | persona-winston-retrospective-from-future | opus | `a2707d2bf03b2fb71` | [`raw-transcripts/PERSRETRO-agent-a2707d2bf03b2fb71.jsonl`](raw-transcripts/PERSRETRO-agent-a2707d2bf03b2fb71.jsonl) | [`findings/PERSRETRO-findings.md`](findings/PERSRETRO-findings.md) | 150 |
| 6 | `SCENNOW` | scenario-unfold-current-state | opus | `a07f43fdddd08cb06` | [`raw-transcripts/SCENNOW-agent-a07f43fdddd08cb06.jsonl`](raw-transcripts/SCENNOW-agent-a07f43fdddd08cb06.jsonl) | [`findings/SCENNOW-findings.md`](findings/SCENNOW-findings.md) | 146 |
| 6 | `SECDISTILL` | distillator-security-focused | opus | `a3dbddc9bf6b4c61b` | [`raw-transcripts/SECDISTILL-agent-a3dbddc9bf6b4c61b.jsonl`](raw-transcripts/SECDISTILL-agent-a3dbddc9bf6b4c61b.jsonl) | [`findings/SECDISTILL-findings.md`](findings/SECDISTILL-findings.md) | 130 |
| 6 | `STRUCTGOV` | editorial-review-structure-governance-focused | opus | `a93bfc6e74549fbc2` | [`raw-transcripts/STRUCTGOV-agent-a93bfc6e74549fbc2.jsonl`](raw-transcripts/STRUCTGOV-agent-a93bfc6e74549fbc2.jsonl) | [`findings/STRUCTGOV-findings.md`](findings/STRUCTGOV-findings.md) | 163 |

## How to use this corpus

- **For per-finding text:** read `findings/<PREFIX>-findings.md`. That file contains the sub-agent's final deliverable — the complete list of findings it produced. Cross-reference with `findings-index.md` per-theme rows (e.g., THEME-A finding `EDGE-23` lives inside `findings/EDGE-findings.md`).
- **For full transcript including tool calls and intermediate reasoning:** read `raw-transcripts/<PREFIX>-agent-*.jsonl`. Each line is a JSON object with a `type` field (`user`/`assistant`/`tool_result`/`attachment`).
- **For re-clustering:** the per-stream findings markdown is the input. `consolidated.md`'s themes are one clustering of these findings; a different clusterer can produce a different (and auditable) clustering from the same inputs.
- **For implementation-audit calibration:** when scoring a new method's σ × κ, the new method's outputs are compared against this corpus to determine which new findings overlap and which are novel.

## Extraction tool

The extraction is performed by [`persist-corpus.py`](persist-corpus.py) checked in alongside this manifest. The tool is incremental and idempotent: each re-run ingests any new cache-resident transcripts whose description is in `DESC_TO_STREAM`, and preserves rows for transcripts already on disk in `raw-transcripts/` from prior sessions. The tool is **not** wired into CI. To extend the corpus with a new wave: append entries to `DESC_TO_STREAM`, ensure the wave's sub-agent transcripts are still in the local cache, and re-run.

## Provenance

- Initial extraction: 2026-05-17 (Waves 1-4, 35 streams; corpus rescue from container-local cache before reclaim).
- Subsequent extractions append new waves' transcripts; pre-existing rows are preserved.
- Source: container-local cache `/root/.claude/projects/-home-user-Test-Repo/<session-id>/subagents/`.
- Initial-extraction transcripts cross-checked against `findings-index.md` per-stream tally; per-stream finding counts in the transcript match the index within ±1 (counting variation due to how compound findings are enumerated in some streams). New-wave additions are cross-checked at the wave's TASK file.

## Unmapped transcripts

These transcripts were found in the source cache but their description is not in `DESC_TO_STREAM`. They are **not** ingested into the audit corpus (no raw copy, no findings extraction, no manifest row above). They are listed here for future investigation in case an audit-relevant transcript was spawned with an off-catalog description and needs to be recovered before the cache is reclaimed. To ingest one: add its description to `DESC_TO_STREAM` and re-run.

- `agent-a0feaa6b98527b7af` — description: `Re-read STATUS.md after sweep`
- `agent-a13539ac839e9255c` — description: `Sample findings + raw-transcripts format`
- `agent-a841871f48d0f5fd7` — description: `Audit qd-triage §8 + consolidated tail`
- `agent-ac90c4628f8088b2c` — description: `Read methodology.spec.md + INDEX`
- `agent-acaf8e5b7029de64f` — description: `Read CHG-0032 envelope thoroughly`
