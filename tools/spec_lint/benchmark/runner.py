"""
Dry-run runner.

PHASE-1 / CHG-0009 / TASK-0017 — RED stub. TASK-0018 implements.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass, field

from ..models import Finding


@dataclass
class CorpusResult:
    name: str
    items_loaded: int
    findings_by_rule: dict[str, list[Finding]] = field(default_factory=dict)
    uncertain_by_rule: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class DryRunResult:
    corpora: list[CorpusResult] = field(default_factory=list)
    runtime_seconds: float = 0.0


def run_dry_run(corpora_root: pathlib.Path) -> DryRunResult:
    """Execute the full dry-run across all vendored corpora.

    Applicable rules per corpus:
    - OpenSpec docs → prose-xref-banned, xref-resolves.
    - PROMISE NFR → anti-aliasing, compound-requirement-detector.

    Also populates each corpus's ``uncertain_by_rule`` with rule-specific
    near-threshold signals — informational, not gating.
    """
    raise NotImplementedError(
        "run_dry_run: TASK-0017 RED stub — implemented in TASK-0018"
    )
