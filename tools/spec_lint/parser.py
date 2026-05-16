"""
Spec markdown parser.

Permissive: any `## REQ-…` heading is treated as an intended REQ block.
Strict validation is the job of rules, not the parser.

Parses are total — malformed sections produce a None frontmatter and/or a
``parse_findings`` entry rather than raising. Rules see the partial result
and report their own findings.
"""

from __future__ import annotations

import pathlib
import re

import yaml

from .models import Finding, ReqBlock, SpecFile

# Maximally permissive: any `## REQ-<non-whitespace>` is treated as an
# intended REQ block. Strict format judgment (uppercase, length, digit count)
# belongs to rules.req_id_format, not here. This is deliberate — the parser
# must surface even malformed REQ headings so format rules can flag them.
_HEADING_RE = re.compile(r"^## (REQ-\S+)\s*$")


def parse_spec_file(path: pathlib.Path | str) -> SpecFile:
    path = pathlib.Path(path)
    return parse_spec_file_text(path.read_text(), str(path))


def parse_spec_file_text(text: str, path_str: str) -> SpecFile:
    """Parse spec markdown from raw text rather than a path.

    Used by ``git_history.historical_versions`` to parse content obtained
    from ``git show`` without writing it to disk first.
    """
    lines = text.splitlines()

    # Locate every REQ heading: 1-based line numbers.
    heading_positions: list[tuple[int, str]] = []
    for i, line in enumerate(lines, start=1):
        m = _HEADING_RE.match(line)
        if m:
            heading_positions.append((i, m.group(1)))

    requirements: list[ReqBlock] = []
    findings: list[Finding] = []

    for idx, (line_no, heading_id) in enumerate(heading_positions):
        # Block ends at the next REQ heading or EOF (exclusive index into `lines`).
        end_excl = (
            heading_positions[idx + 1][0] - 1 if idx + 1 < len(heading_positions) else len(lines)
        )
        # Lines strictly after the heading line.
        block_lines = lines[line_no:end_excl]

        frontmatter_raw, frontmatter, body_start = _extract_frontmatter(
            block_lines, line_no, path_str, heading_id, findings
        )
        body = "\n".join(block_lines[body_start:])

        requirements.append(
            ReqBlock(
                file=path_str,
                heading_id=heading_id,
                heading_line=line_no,
                frontmatter_raw=frontmatter_raw,
                frontmatter=frontmatter,
                body=body,
            )
        )

    return SpecFile(path=path_str, requirements=requirements, parse_findings=findings)


def _extract_frontmatter(
    block_lines: list[str],
    heading_line: int,
    path_str: str,
    heading_id: str,
    findings: list[Finding],
) -> tuple[str | None, dict | None, int]:
    """Return (raw_text, parsed_dict, body_start_index)."""
    i = 0
    # Skip blank lines after the heading.
    while i < len(block_lines) and block_lines[i].strip() == "":
        i += 1
    if i >= len(block_lines) or block_lines[i].strip() != "---":
        # No frontmatter block at all.
        return None, None, 0

    open_idx = i
    j = i + 1
    while j < len(block_lines) and block_lines[j].strip() != "---":
        j += 1
    if j >= len(block_lines):
        findings.append(
            Finding(
                rule_id="parse-error",
                severity="error",
                file=path_str,
                req_id=heading_id,
                line=heading_line + open_idx + 1,
                message="Unclosed frontmatter block (missing trailing ---)",
            )
        )
        return None, None, 0

    raw = "\n".join(block_lines[open_idx + 1 : j])
    parsed: dict | None
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        findings.append(
            Finding(
                rule_id="parse-error",
                severity="error",
                file=path_str,
                req_id=heading_id,
                line=heading_line + open_idx + 1,
                message=f"YAML parse error: {e}",
            )
        )
        parsed = None
    else:
        if isinstance(loaded, dict):
            parsed = loaded
        else:
            findings.append(
                Finding(
                    rule_id="parse-error",
                    severity="error",
                    file=path_str,
                    req_id=heading_id,
                    line=heading_line + open_idx + 1,
                    message=f"Frontmatter is not a mapping (got {type(loaded).__name__})",
                )
            )
            parsed = None

    return raw, parsed, j + 1
