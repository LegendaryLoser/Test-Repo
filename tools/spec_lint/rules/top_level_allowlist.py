"""
Rule: top-level-allowlist

Enforces [ADR-0001](../../../openspec/architecture/decisions/ADR-0001-monorepo-layout.md)
+ `REQ-ARCH-0001` — the set of git-tracked top-level entries matches
the allowlist documented in
[ARCHITECTURE.md](../../../openspec/architecture/ARCHITECTURE.md) §3.

Failure modes surfaced:
- A directory in `REQUIRED_TOP_LEVEL_DIRS` is missing from the tracked
  tree (severity=error).
- A tracked top-level entry is not present in `ALLOWED_TOP_LEVEL_ENTRIES`
  (severity=error). Adding one requires an ADR amendment.

Source of truth for both sets:
``tools/spec_lint/_top_level_allowlist.py``.
"""

from __future__ import annotations

import pathlib
import subprocess

from .._top_level_allowlist import ALLOWED_TOP_LEVEL_ENTRIES, REQUIRED_TOP_LEVEL_DIRS
from ..models import Finding


class TopLevelAllowlist:
    id = "top-level-allowlist"
    description = (
        "Top-level tracked entries match ARCHITECTURE.md §3 + ADR-0001 (REQ-ARCH-0001)"
    )

    def check_repo(self, repo_root: pathlib.Path) -> list[Finding]:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        tracked_top_level = {
            line.split("/", 1)[0] for line in result.stdout.splitlines() if line
        }

        findings: list[Finding] = []
        repo_str = str(repo_root)

        for name in sorted(REQUIRED_TOP_LEVEL_DIRS - tracked_top_level):
            findings.append(
                Finding(
                    rule_id=self.id,
                    severity="error",
                    file=repo_str,
                    message=(
                        f"Required top-level entry missing from tracked tree: {name!r} "
                        f"(see ARCHITECTURE.md §3 + REQ-ARCH-0001)"
                    ),
                )
            )

        for name in sorted(tracked_top_level - ALLOWED_TOP_LEVEL_ENTRIES):
            findings.append(
                Finding(
                    rule_id=self.id,
                    severity="error",
                    file=repo_str,
                    message=(
                        f"Unexpected top-level entry not in allowlist: {name!r} "
                        f"(adding one requires an ADR amendment per ADR-0001)"
                    ),
                )
            )

        return findings
