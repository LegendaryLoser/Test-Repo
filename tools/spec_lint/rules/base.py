"""Rule protocols — what every spec_lint rule satisfies."""

from __future__ import annotations

import pathlib
from typing import Protocol

from ..models import Finding, SpecFile


class Rule(Protocol):
    """A single-file rule. Sees one parsed spec file at a time."""

    id: str
    description: str

    def check(self, spec_file: SpecFile) -> list[Finding]: ...


class HistoricalRule(Protocol):
    """A rule that needs full git history of one spec file.

    Introduced in CHG-0004 alongside ``git_history.historical_versions``.
    """

    id: str
    description: str

    def check_history(self, versions: list) -> list[Finding]: ...


class CrossFileRule(Protocol):
    """A rule that scans arbitrary markdown (not just REQ-block-bearing
    spec files). Introduced in CHG-0005. The caller supplies the file set."""

    id: str
    description: str

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]: ...


class CorpusRule(Protocol):
    """A rule that needs every parsed spec file at once. Introduced in
    CHG-0006 for anti-aliasing (pairwise n-gram similarity across the whole
    spec corpus)."""

    id: str
    description: str

    def check_corpus(self, spec_files: list[SpecFile]) -> list[Finding]: ...
