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

Skeleton — TASK-0022 RED. Real implementation lands in TASK-0023.
"""

from __future__ import annotations

import pathlib

from ..models import Finding


class TopLevelAllowlist:
    id = "top-level-allowlist"
    description = (
        "Top-level tracked entries match ARCHITECTURE.md §3 + ADR-0001 (REQ-ARCH-0001)"
    )

    def check_repo(self, repo_root: pathlib.Path) -> list[Finding]:
        # TASK-0022 skeleton — returns no findings unconditionally so that
        # TASK-0022 tests assertion-fail (red), not import-fail. Real
        # implementation in TASK-0023.
        del repo_root
        return []
