"""
Rule: xref-resolves

Enforces ADR-0004 §2 — every relative markdown link and every
``REQ-X-NNNN @ relative/path.spec.md`` reference must resolve. For REQ
references, the cited spec file must contain a ``## REQ-X-NNNN`` heading.

PHASE-1 / CHG-0005 / TASK-0008 — RED stub. TASK-0009 implements.
"""

from __future__ import annotations

import pathlib

from ..models import Finding


class XrefResolves:
    id = "xref-resolves"
    description = "Markdown link targets and REQ-ID@path references resolve (ADR-0004 §2)"

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        raise NotImplementedError(
            "XrefResolves.check_files: TASK-0008 RED stub — implemented in TASK-0009"
        )
