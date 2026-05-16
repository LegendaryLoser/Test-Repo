"""
Git-history adapter for spec_lint.

Wraps `git log` / `git show` via real subprocess against real git. No mocks
per ADR-0006 §2. Tests use ephemeral repos under pytest's tmp_path.

PHASE-1 simplifications (CHG-0004 proposal documents):
- No --follow. File renames within history are not tracked.
- Cross-file REQ moves are out of scope.

PHASE-1 / CHG-0004 / TASK-0006 — RED stub. TASK-0007 implements.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

from .models import SpecFile


@dataclass(frozen=True)
class HistoricalVersion:
    sha: str
    timestamp: datetime
    content: str
    spec_file: SpecFile


def historical_versions(
    repo: pathlib.Path | str, file_rel: pathlib.Path | str
) -> Iterator[HistoricalVersion]:
    """Yield each historical version of a spec file, oldest first.

    RED stub — TASK-0007 implements.
    """
    raise NotImplementedError(
        "historical_versions: TASK-0006 RED stub — implemented in TASK-0007"
    )
