"""
Rule: anti-aliasing

Enforces ADR-0004 §4 — pairwise n-gram similarity across all REQ
Description+Acceptance bodies in the corpus; pairs above a configurable
threshold are flagged. These are the paper's δ-convex lures: distinct
specifications occupying near-identical positions in any retrieval space.

Configuration: ``tools/spec_lint/config.yaml`` under ``anti_aliasing``.
Constructor accepts an override dict for tests.

PHASE-1 / CHG-0006 / TASK-0010 — RED stub. TASK-0011 implements.
"""

from __future__ import annotations

import pathlib

from ..models import Finding, SpecFile


class AntiAliasing:
    id = "anti-aliasing"
    description = (
        "Pairs of REQs with high n-gram similarity in Description+Acceptance "
        "(ADR-0004 §4, paper-derived)"
    )

    def __init__(self, config: dict | None = None):
        self._config_override = config

    def check_corpus(self, spec_files: list[SpecFile]) -> list[Finding]:
        raise NotImplementedError(
            "AntiAliasing.check_corpus: TASK-0010 RED stub — implemented in TASK-0011"
        )
