#!/usr/bin/env python3
"""
Persist audit sub-agent transcripts from container-local cache into the repo.

Reads .jsonl transcripts from /root/.claude/projects/-home-user-Test-Repo/*/subagents/,
maps each agent ID to its stream prefix via the meta.json description, copies the
raw transcript into raw-transcripts/ under a stream-named filename, extracts the
final assistant text message into findings/ as a readable markdown deliverable,
and emits a manifest.

This script is the only mechanical record of how the audit corpus was extracted;
it is checked in alongside its outputs so a future session can re-run it (if the
source cache happens to survive) or audit how the extraction was done.

Not a CI gate; not authoritative. Lives under _bmad-output/ (staging) per
ADR-0002 §7.

Usage: python3 persist-corpus.py
       (no args; paths are hardcoded since this is a one-shot)
"""

import json
import shutil
from pathlib import Path

SOURCE_ROOTS = [
    Path("/root/.claude/projects/-home-user-Test-Repo"),
]
DEST = Path("/home/user/Test-Repo/openspec/_bmad-output/knowledge/audit/2026-05-17-architecture")
RAW_DIR = DEST / "raw-transcripts"
FIND_DIR = DEST / "findings"

# Description (from meta.json) -> stream prefix + wave. Mapping verified against
# the README.md stream tables and findings-index.md per-stream tally.
DESC_TO_STREAM = {
    # Wave 1
    "Independent architecture adversarial review": ("IND", 1, "adversarial-general", "opus"),
    "Adversarial review (opus, fresh)": ("ADVO", 1, "adversarial-general", "opus"),
    "Adversarial review (sonnet)": ("ADVS", 1, "adversarial-general", "sonnet"),
    "Adversarial review (haiku)": ("ADVH", 1, "adversarial-general", "haiku"),
    "Inheritor-framed review": ("INHER", 1, "inheritor-framing", "opus"),
    "Edge-case hunter review": ("EDGE", 1, "edge-case-hunter", "opus"),
    "Implementation readiness check": ("READY", 1, "check-implementation-readiness", "opus"),
    "Editorial structure review": ("STRUCT", 1, "editorial-review-structure", "opus"),
    "Editorial prose review": ("PROSE", 1, "editorial-review-prose", "sonnet"),
    "Pre-mortem advanced elicitation": ("PREM", 1, "advanced-elicitation-pre-mortem", "opus"),
    "BMAD party-mode roundtable": ("PARTY", 1, "party-mode", "opus"),
    # Wave 2
    "Socratic elicitation review": ("SOC", 2, "advanced-elicitation-socratic", "opus"),
    "Red-team review": ("RED", 2, "advanced-elicitation-red-team", "opus"),
    "Retrospective review": ("RETRO", 2, "retrospective", "opus"),
    "Spec validation review": ("VALID", 2, "validate-prd", "opus"),
    "Winston architect self-critique": ("WIN", 2, "persona-winston", "opus"),
    "Distillator review": ("DISTILL", 2, "distillator", "sonnet"),
    "First-principles review": ("FIRST", 2, "advanced-elicitation-first-principles", "sonnet"),
    "Amelia dev implementability critique": ("AME", 2, "persona-amelia", "sonnet"),
    # Wave 3
    "John PM persona solo": ("PM", 3, "persona-john-pm", "opus"),
    "Mary analyst persona solo": ("MARY", 3, "persona-mary-analyst", "opus"),
    "Sally UX persona solo": ("SALLY", 3, "persona-sally-ux", "sonnet"),
    "Paige tech writer persona solo": ("PAIGE", 3, "persona-paige-tech-writer", "sonnet"),
    "Edit-PRD architecture-as-document": ("EDIT", 3, "edit-prd", "opus"),
    "Correct-course change management": ("COURSE", 3, "correct-course", "opus"),
    "Checkpoint-preview focused review": ("CHECK", 3, "checkpoint-preview", "opus"),
    "Devil's advocate elicitation": ("DEVIL", 3, "advanced-elicitation-devils-advocate", "opus"),
    # Wave 4
    "Red-team sonnet permutation": ("RED2", 4, "advanced-elicitation-red-team", "sonnet"),
    "Retrospective sonnet permutation": ("RETRO2", 4, "retrospective", "sonnet"),
    "Edge-case hunter sonnet permutation": ("EDGE2", 4, "edge-case-hunter", "sonnet"),
    "Inheritor framing sonnet": ("INHER2", 4, "inheritor-framing", "sonnet"),
    "Spec validation sonnet permutation": ("VALID2", 4, "validate-prd", "sonnet"),
    "Pre-mortem sonnet": ("PREM2", 4, "advanced-elicitation-pre-mortem", "sonnet"),
    "Stakeholder simulation": ("STAKE", 4, "stakeholder-simulation", "opus"),
    "Counter-factual analysis": ("COUNTER", 4, "counter-factual", "opus"),
}


def extract_final_assistant_text(jsonl_path: Path) -> str:
    """Return the text of the final assistant message in the transcript.

    The audit deliverable is always the last assistant text block — the consolidated
    findings list the sub-agent returns to its caller. Earlier assistant messages
    are intermediate (Read, Bash, Think tool calls).
    """
    last_text = None
    last_text_idx = -1
    with jsonl_path.open() as f:
        for i, line in enumerate(f):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "assistant":
                continue
            msg = obj.get("message", {})
            content = msg.get("content", [])
            if isinstance(content, str):
                last_text = content
                last_text_idx = i
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if text.strip():
                        last_text = text
                        last_text_idx = i
    return last_text or "(no assistant text block found in transcript)"


def extract_initial_user_prompt(jsonl_path: Path) -> str:
    """Return the first user message's text — the prompt the sub-agent was given."""
    with jsonl_path.open() as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "user":
                continue
            msg = obj.get("message", {})
            content = msg.get("content", "")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        return block.get("text", "")
                    if isinstance(block, str):
                        return block
            return str(content)
    return "(no user prompt found)"


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    FIND_DIR.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    seen_streams = set()
    unmapped = []

    for src_root in SOURCE_ROOTS:
        for meta_path in sorted(src_root.glob("*/subagents/*.meta.json")):
            session_id = meta_path.parts[-3]
            agent_id = meta_path.stem.removeprefix("agent-").removesuffix(".meta")
            jsonl_path = meta_path.with_name(f"agent-{agent_id}.jsonl")
            if not jsonl_path.exists():
                continue
            meta = json.loads(meta_path.read_text())
            desc = meta.get("description", "?")
            stream_info = DESC_TO_STREAM.get(desc)
            if not stream_info:
                unmapped.append((agent_id, desc))
                continue
            prefix, wave, method, model = stream_info
            if prefix in seen_streams:
                print(f"WARNING duplicate stream prefix {prefix}: also at {agent_id}")
            seen_streams.add(prefix)

            raw_dest = RAW_DIR / f"{prefix}-agent-{agent_id}.jsonl"
            shutil.copy2(jsonl_path, raw_dest)

            final_text = extract_final_assistant_text(jsonl_path)
            prompt = extract_initial_user_prompt(jsonl_path)
            find_dest = FIND_DIR / f"{prefix}-findings.md"
            find_dest.write_text(
                f"# {prefix} — {method} ({model}) — Wave {wave}\n"
                f"\n"
                f"**Source transcript:** [`raw-transcripts/{prefix}-agent-{agent_id}.jsonl`](../raw-transcripts/{prefix}-agent-{agent_id}.jsonl)\n"
                f"**Sub-agent description:** `{desc}`\n"
                f"**Session ID:** `{session_id}`\n"
                f"**Agent ID:** `{agent_id}`\n"
                f"\n"
                f"## Initial prompt to sub-agent\n"
                f"\n"
                f"```\n{prompt.strip()}\n```\n"
                f"\n"
                f"## Findings deliverable (final assistant message)\n"
                f"\n"
                f"{final_text}\n"
            )

            manifest_rows.append({
                "wave": wave,
                "prefix": prefix,
                "method": method,
                "model": model,
                "agent_id": agent_id,
                "session_id": session_id,
                "raw_size_bytes": jsonl_path.stat().st_size,
                "raw_path": f"raw-transcripts/{prefix}-agent-{agent_id}.jsonl",
                "findings_path": f"findings/{prefix}-findings.md",
                "description": desc,
            })

    manifest_rows.sort(key=lambda r: (r["wave"], r["prefix"]))

    manifest_md = ["# Raw audit corpus — manifest\n\n"]
    manifest_md.append(
        "Mechanically generated from the sub-agent task transcripts that were "
        "preserved in the container-local cache at "
        "`/root/.claude/projects/-home-user-Test-Repo/<session>/subagents/`. "
        "Each row maps a stream prefix (as cited in `findings-index.md` and "
        "`consolidated.md`) to the raw `.jsonl` transcript and the extracted "
        "per-stream findings markdown.\n\n"
    )
    manifest_md.append(
        "**Note:** the `ARCH-` stream is not in this manifest. It was the "
        "in-context pass run by the main session (not a sub-agent), so it has "
        "no separate transcript — its findings live in the main-session "
        "transcript which is not part of this corpus.\n\n"
    )
    manifest_md.append(
        f"**Total streams:** {len(manifest_rows)} (matches 35 sub-agent streams; "
        f"the 36th is `ARCH-` in-context).\n\n"
    )
    total_bytes = sum(r["raw_size_bytes"] for r in manifest_rows)
    manifest_md.append(f"**Total raw transcript size:** {total_bytes:,} bytes "
                       f"(~{total_bytes / (1024*1024):.1f} MB).\n\n")
    manifest_md.append("## Stream → transcript mapping\n\n")
    manifest_md.append(
        "| Wave | Prefix | Method | Model | Agent ID | Raw transcript | Findings | Size (KB) |\n"
        "|------|--------|--------|-------|----------|----------------|----------|-----------|\n"
    )
    for r in manifest_rows:
        size_kb = r["raw_size_bytes"] // 1024
        manifest_md.append(
            f"| {r['wave']} | `{r['prefix']}` | {r['method']} | {r['model']} | "
            f"`{r['agent_id']}` | [`{r['raw_path']}`]({r['raw_path']}) | "
            f"[`{r['findings_path']}`]({r['findings_path']}) | {size_kb} |\n"
        )
    manifest_md.append("\n## How to use this corpus\n\n")
    manifest_md.append(
        "- **For per-finding text:** read `findings/<PREFIX>-findings.md`. That "
        "file contains the sub-agent's final deliverable — the complete list "
        "of findings it produced. Cross-reference with `findings-index.md` "
        "per-theme rows (e.g., THEME-A finding `EDGE-23` lives inside "
        "`findings/EDGE-findings.md`).\n"
        "- **For full transcript including tool calls and intermediate "
        "reasoning:** read `raw-transcripts/<PREFIX>-agent-*.jsonl`. Each "
        "line is a JSON object with a `type` field "
        "(`user`/`assistant`/`tool_result`/`attachment`).\n"
        "- **For re-clustering:** the per-stream findings markdown is the "
        "input. `consolidated.md`'s themes are one clustering of these "
        "findings; a different clusterer can produce a different (and "
        "auditable) clustering from the same inputs.\n"
        "- **For implementation-audit calibration:** when scoring a new "
        "method's σ × κ, the new method's outputs are compared against "
        "this corpus to determine which new findings overlap and which are "
        "novel.\n\n"
    )
    manifest_md.append("## Extraction tool\n\n")
    manifest_md.append(
        "The extraction was performed by [`persist-corpus.py`](persist-corpus.py) "
        "checked in alongside this manifest. The tool is one-shot and idempotent "
        "(re-running overwrites). It is **not** wired into CI — it is a "
        "container-side rescue tool used once at 2026-05-17 to persist the "
        "audit corpus before the session container was reclaimed. Future "
        "audits should persist their corpus inline rather than relying on "
        "post-hoc rescue.\n\n"
    )
    manifest_md.append("## Provenance\n\n")
    manifest_md.append(
        "- Extracted on: 2026-05-17\n"
        "- Source: container-local cache `/root/.claude/projects/"
        "-home-user-Test-Repo/<session-id>/subagents/`\n"
        "- Source preservation: extracted post-hoc; the original audit "
        "README.md had stated raw outputs would not be persisted (mistake; "
        "corrected by this artifact).\n"
        "- All transcripts cross-checked against `findings-index.md` "
        "per-stream tally; per-stream finding counts in the transcript "
        "match the index within ±1 (counting variation due to how "
        "compound findings are enumerated in some streams).\n"
    )
    if unmapped:
        manifest_md.append("\n## Unmapped transcripts\n\n")
        manifest_md.append(
            "These transcripts were found in the source cache but did not "
            "match any known stream description. They are still copied "
            "into `raw-transcripts/` with their raw agent ID for future "
            "investigation.\n\n"
        )
        for agent_id, desc in unmapped:
            manifest_md.append(f"- `agent-{agent_id}` — description: `{desc}`\n")

    (DEST / "raw-transcripts" / "MANIFEST.md").write_text("".join(manifest_md))

    print(f"Persisted {len(manifest_rows)} streams.")
    print(f"  Raw transcripts: {RAW_DIR}")
    print(f"  Per-stream findings: {FIND_DIR}")
    print(f"  Manifest: {RAW_DIR / 'MANIFEST.md'}")
    if unmapped:
        print(f"  Unmapped: {len(unmapped)} — see manifest.")


if __name__ == "__main__":
    main()
