"""Rule protocol — what every spec_lint rule satisfies."""

from __future__ import annotations

from typing import Protocol

from ..models import Finding, SpecFile


class Rule(Protocol):
    """A single-file rule. Cross-file rules are introduced in CHG-0006."""

    id: str
    description: str

    def check(self, spec_file: SpecFile) -> list[Finding]: ...
