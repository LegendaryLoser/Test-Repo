"""Markdown report generator for dry-run results."""

from __future__ import annotations

from .runner import DryRunResult


def render_report(result: DryRunResult, head_sha: str = "unknown") -> str:
    lines: list[str] = []
    lines.append("# spec_lint dry-run baseline")
    lines.append("")
    lines.append(f"- Rules HEAD: `{head_sha}`")
    lines.append(f"- Runtime: {result.runtime_seconds:.2f}s")
    lines.append(f"- Corpora processed: {len(result.corpora)}")
    lines.append("")
    lines.append(
        "_Diagnostic output only — counts will drift as rules and corpora "
        "evolve. Pinned in tests are structural invariants, not specific "
        "counts. Future CHGs may add labels for precision/recall._"
    )
    lines.append("")

    for c in result.corpora:
        lines.append(f"## `{c.name}`")
        lines.append("")
        lines.append(f"- Items loaded: **{c.items_loaded}**")
        lines.append("")
        total_findings = sum(len(v) for v in c.findings_by_rule.values())
        lines.append(f"- Total findings across rules: **{total_findings}**")
        lines.append("")
        for rule_id in sorted(c.findings_by_rule):
            findings = c.findings_by_rule[rule_id]
            lines.append(f"### `{rule_id}`")
            lines.append("")
            lines.append(f"Findings: **{len(findings)}**")
            lines.append("")
            for f in findings[:5]:
                loc = f"{f.file}:{f.line}" if f.line else f.file
                msg = f.message if len(f.message) < 200 else f.message[:197] + "..."
                lines.append(f"- `{loc}` — {msg}")
            if len(findings) > 5:
                lines.append(f"- _… and {len(findings) - 5} more_")
            lines.append("")
            uncertain = c.uncertain_by_rule.get(rule_id, [])
            if uncertain:
                lines.append(f"Uncertain-zone signals: **{len(uncertain)}**")
                for u in uncertain[:5]:
                    lines.append(f"- {u}")
                lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines) + "\n"
