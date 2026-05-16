"""
Spec markdown parser.

PHASE-1 / CHG-0003 / TASK-0004 — RED stub.
TASK-0005 supplies the real implementation.
"""

from __future__ import annotations

import pathlib

from .models import SpecFile


def parse_spec_file(path: pathlib.Path | str) -> SpecFile:
    """Parse a spec markdown file into a SpecFile.

    RED stub: not yet implemented. See TASK-0005.
    """
    raise NotImplementedError(
        "parse_spec_file: TASK-0004 RED stub — implemented in TASK-0005"
    )
