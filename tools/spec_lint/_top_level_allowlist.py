"""
Canonical allowlist for the repository's top-level tracked entries.

Single source of truth (P1) shared by:
- `tools/spec_lint/rules/top_level_allowlist.py` — the runnable lint rule.
- `tools/ci/tests/test_phase0.py::test_arch_0001_top_level_layout` — the
  architecture invariant test.

Keep aligned with `openspec/architecture/ARCHITECTURE.md` §3. A drift
between this module and §3 is itself a defect (CI for that cross-doc
consistency lands in PHASE-2 via `tools/trace`). Additions to either
set require an ADR per `REQ-ARCH-0001` and
[ADR-0001](../../openspec/architecture/decisions/ADR-0001-monorepo-layout.md).
"""

from __future__ import annotations


REQUIRED_TOP_LEVEL_DIRS: frozenset[str] = frozenset({
    ".claude",
    ".github",
    "openspec",
})


ALLOWED_TOP_LEVEL_ENTRIES: frozenset[str] = frozenset({
    "README.md",
    "CLAUDE.md",
    ".gitignore",
    "pyproject.toml",
    ".claude",
    ".github",
    "openspec",
    "tools",
    "_bmad",
    "scripts",
    "packages",
    "projects",
})
