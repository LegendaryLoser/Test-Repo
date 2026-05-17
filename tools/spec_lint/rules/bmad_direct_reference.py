"""
Rule: bmad-direct-reference

Enforces [ADR-0002](../../../openspec/architecture/decisions/ADR-0002-bmad-integration.md)
§6 + Compliance — no file under ``tools/``, ``packages/``, or
``projects/`` may import from or execute ``_bmad/``, except authorized
integration points (``tools/tea/`` when it exists).

Detection is intentionally narrow (imports + executable paths only) so
that docstrings, comments, and string constants describing the rule
do not self-flag.

Skeleton — TASK-0025 RED. Real implementation lands in TASK-0026.
"""

from __future__ import annotations

import pathlib

from ..models import Finding


class BmadDirectReference:
    id = "bmad-direct-reference"
    description = (
        "No file under tools/, packages/, projects/ may import or execute "
        "_bmad/ paths except tools/tea/ (ADR-0002 §6)"
    )

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        del files
        return []
