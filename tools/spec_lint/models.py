"""Data models for spec_lint. Pure dataclasses; no behavior."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    """A single rule violation, stable enough to compare in tests."""

    rule_id: str
    severity: str          # "error" | "warning"
    file: str
    message: str
    req_id: str | None = None
    line: int | None = None

    def __str__(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line is not None else self.file
        rid = f" [{self.req_id}]" if self.req_id else ""
        return f"{loc}: {self.severity}: {self.rule_id}{rid}: {self.message}"


@dataclass
class ReqBlock:
    """One REQ block parsed from a spec file. Parser stays permissive — strict
    validation is the job of rules, not the parser."""

    file: str
    heading_id: str             # the REQ-... string in the `## ...` heading
    heading_line: int           # 1-based line number of the heading
    frontmatter_raw: str | None # the YAML text between --- markers, if any
    frontmatter: dict | None    # parsed YAML, or None on parse failure / absence
    body: str                   # everything after the closing --- of frontmatter


@dataclass
class SpecFile:
    """A parsed spec markdown file."""

    path: str
    requirements: list[ReqBlock] = field(default_factory=list)
    parse_findings: list[Finding] = field(default_factory=list)
