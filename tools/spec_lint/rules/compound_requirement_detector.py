"""
Rule: compound-requirement-detector

Enforces ADR-0004 §3 — one REQ contains one assertion. A REQ whose
Acceptance section has more than one Given/When/Then bullet is compound by
definition and must be split.

PHASE-1 simplification: only the primary signal (multi-G/W/T) is used.
Prose-conjunction detection ("A and B", "plus") is deferred — high
false-positive risk.

PHASE-1 / CHG-0006 / TASK-0010 — RED stub. TASK-0011 implements.
"""

from __future__ import annotations

from ..models import Finding, SpecFile


class CompoundRequirementDetector:
    id = "compound-requirement-detector"
    description = "REQ has > 1 Given/When/Then in Acceptance (ADR-0004 §3)"

    def check(self, spec_file: SpecFile) -> list[Finding]:
        raise NotImplementedError(
            "CompoundRequirementDetector.check: TASK-0010 RED stub — "
            "implemented in TASK-0011"
        )
