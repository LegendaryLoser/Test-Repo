"""
Rule: req-id-immutable

Enforces ADR-0004 §1 — a REQ-ID, once introduced, never disappears from the
spec file. The only permitted lifecycle change is `status: deprecated`; the
REQ block stays in the file. Renames are forbidden; supersession is the
only path.

PHASE-1 / CHG-0004 / TASK-0006 — RED stub. TASK-0007 implements.
"""

from __future__ import annotations

from ..models import Finding


class ReqIdImmutable:
    id = "req-id-immutable"
    description = "REQ-IDs once introduced never disappear (ADR-0004 §1)"

    def check_history(self, versions: list) -> list[Finding]:
        raise NotImplementedError(
            "ReqIdImmutable.check_history: TASK-0006 RED stub — implemented in TASK-0007"
        )
