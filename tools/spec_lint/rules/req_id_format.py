"""
Rule: req-id-format

Enforces ADR-0004 §1 — REQ identifiers match
``^REQ-[A-Z0-9]{1,12}-\\d{4}$``.

PHASE-1 / CHG-0003 / TASK-0004 — RED stub.
TASK-0005 supplies the real implementation.
"""

from __future__ import annotations

from ..models import Finding, SpecFile


class ReqIdFormat:
    id = "req-id-format"
    description = "REQ-IDs match ^REQ-[A-Z0-9]{1,12}-\\d{4}$ (ADR-0004 §1)"

    def check(self, spec_file: SpecFile) -> list[Finding]:
        raise NotImplementedError(
            "ReqIdFormat.check: TASK-0004 RED stub — implemented in TASK-0005"
        )
