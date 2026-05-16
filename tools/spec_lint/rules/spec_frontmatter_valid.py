"""
Rule: spec-frontmatter-valid

Enforces ADR-0004 §5 — REQ frontmatter has required keys with valid values.

PHASE-1 / CHG-0003 / TASK-0004 — RED stub.
TASK-0005 supplies the real implementation.
"""

from __future__ import annotations

from ..models import Finding, SpecFile


class SpecFrontmatterValid:
    id = "spec-frontmatter-valid"
    description = "REQ frontmatter has required keys with valid values (ADR-0004 §5)"

    def check(self, spec_file: SpecFile) -> list[Finding]:
        raise NotImplementedError(
            "SpecFrontmatterValid.check: TASK-0004 RED stub — implemented in TASK-0005"
        )
