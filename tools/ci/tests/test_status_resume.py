"""
Session-resume meta-test.

Asserts ``openspec/STATUS.md`` exists and contains the sections a
cold session needs to resume work without re-reading chat history.

PHASE-1 / CHG-0031. Red in TASK-0033, green in TASK-0034.
"""

from __future__ import annotations

import pathlib


REPO = pathlib.Path(__file__).resolve().parents[3]
STATUS = REPO / "openspec" / "STATUS.md"

_REQUIRED_SECTIONS = (
    "## CHG status",
    "## Audit findings",
    "## Open architectural questions",
    "## Roadmap",
    "## Next session: start here",
)


def test_status_resume_file_has_required_sections() -> None:
    """
    @test-id TEST-SPEC-0105
    @covers REQ-SPEC-0016
    """
    assert STATUS.is_file(), f"openspec/STATUS.md missing (expected at {STATUS})"
    text = STATUS.read_text()
    lines = text.splitlines()
    missing = [s for s in _REQUIRED_SECTIONS if s not in lines]
    assert not missing, (
        f"openspec/STATUS.md is missing required sections:\n  - "
        + "\n  - ".join(missing)
    )
