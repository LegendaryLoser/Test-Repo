"""
Git-history adapter for spec_lint.

Wraps `git log` / `git show` via real subprocess against real git. No mocks
per ADR-0006 §2. Tests use ephemeral repos under pytest's tmp_path.

PHASE-1 simplifications (CHG-0004 proposal documents):
- No --follow. File renames within history are not tracked.
- Cross-file REQ moves are out of scope.
"""

from __future__ import annotations

import pathlib
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

from .models import SpecFile
from .parser import parse_spec_file_text


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

    Uses ``git log --reverse --format=%H%x00%cI --diff-filter=AM`` to list
    commits that added or modified the file, then ``git show <sha>:<path>``
    for content.
    """
    repo_path = pathlib.Path(repo)
    file_rel_str = str(file_rel)

    result = subprocess.run(
        [
            "git",
            "log",
            "--reverse",
            "--format=%H%x00%cI",
            "--diff-filter=AM",
            "--",
            file_rel_str,
        ],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True,
    )

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        sha, ts = line.split("\x00", 1)
        show = subprocess.run(
            ["git", "show", f"{sha}:{file_rel_str}"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True,
        )
        content = show.stdout
        # `git show` reliably terminates content with a newline; strip it if
        # the original content didn't have one. We can't perfectly recover the
        # original here without `git cat-file`, but for spec files (which
        # always end with a section body) the trailing newline matches.
        timestamp = datetime.fromisoformat(ts)
        spec_file = parse_spec_file_text(content, file_rel_str)
        yield HistoricalVersion(
            sha=sha,
            timestamp=timestamp,
            content=content,
            spec_file=spec_file,
        )
