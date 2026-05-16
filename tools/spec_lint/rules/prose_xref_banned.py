"""
Rule: prose-xref-banned

Enforces ADR-0004 §2 — references like "the auth spec" or "the login
requirement" are forbidden; every cross-reference must be by stable ID +
file path. Prose references are the channel through which semantic-recall
failure modes enter the system.

Inline allow marker (per-line escape valve):
    <!-- spec-lint: allow prose-xref-banned -->

Exemption: if a denylist match is followed on the same line by a stable
ID (REQ/ADR/CHG/EPIC/STORY/PHASE), the prose is treated as parenthetical
to an explicit reference and skipped.

PHASE-1 / CHG-0005 / TASK-0008 — RED stub. TASK-0009 implements.
"""

from __future__ import annotations

import pathlib

from ..models import Finding


class ProseXrefBanned:
    id = "prose-xref-banned"
    description = "Prose references to specs/REQs are forbidden; use ID + path (ADR-0004 §2)"

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        raise NotImplementedError(
            "ProseXrefBanned.check_files: TASK-0008 RED stub — implemented in TASK-0009"
        )
