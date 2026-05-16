"""
Rule: req-append-only

Enforces ADR-0004 §7 — once a REQ reaches `status: tests-green`, its
`### Description` and `### Acceptance` bodies are frozen. Cosmetic edits
require a `revision` bump.

PHASE-1 scope simplification (CHG-0004 proposal): the "if no downstream
artifact refers to the prior revision" clause is not yet enforced — treats
all tests-green REQs as frozen modulo revision bumps. Tightening lands
in a CHG-0005 follow-up.

PHASE-1 / CHG-0004 / TASK-0006 — RED stub. TASK-0007 implements.
"""

from __future__ import annotations

from ..models import Finding


class ReqAppendOnly:
    id = "req-append-only"
    description = "tests-green REQ bodies are frozen unless revision bumps (ADR-0004 §7)"

    def check_history(self, versions: list) -> list[Finding]:
        raise NotImplementedError(
            "ReqAppendOnly.check_history: TASK-0006 RED stub — implemented in TASK-0007"
        )
