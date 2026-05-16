"""Rule protocols — what every spec_lint rule satisfies."""

from __future__ import annotations

from typing import Protocol

from ..models import Finding, SpecFile


class Rule(Protocol):
    """A single-file rule. Sees one spec file at a time."""

    id: str
    description: str

    def check(self, spec_file: SpecFile) -> list[Finding]: ...


class HistoricalRule(Protocol):
    """A rule that needs full git history of one spec file.

    Introduced in CHG-0004 alongside ``git_history.historical_versions``.
    Cross-file rules arrive in CHG-0006 with a third protocol.
    """

    id: str
    description: str

    def check_history(self, versions: list) -> list[Finding]: ...
