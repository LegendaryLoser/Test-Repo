"""
Rule: mock-in-repo-banned

Enforces [ADR-0006](../../../openspec/architecture/decisions/ADR-0006-testing-tiers.md)
§2 — no ``jest.mock``, ``vi.mock``, ``sinon.stub``, ``unittest.mock.patch``,
``MagicMock``, ``Mock``, ``monkeypatch.setattr``, or ``mocker.patch``
applied to modules within this repository. Boundary adapters must be
real per ADR-0006 §3; only network transport may be substituted at the
edge.

Target resolution:
- ``patch("X")`` and ``patch.object(X, ...)`` — if X is a string literal
  starting with ``tools.``, ``packages.``, or ``projects.``, flag.
  External prefixes (``requests.``, ``anthropic.``, …) are allowed.
- Everything else (no target, identifier target, complex expression
  target) — flag conservatively.

Skeleton — TASK-0025 RED. Real implementation lands in TASK-0026.
"""

from __future__ import annotations

import pathlib

from ..models import Finding


class MockInRepoBanned:
    id = "mock-in-repo-banned"
    description = (
        "Banned mock APIs (unittest.mock.patch, MagicMock, jest.mock, …) "
        "applied to in-repo modules are forbidden (ADR-0006 §2)"
    )

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        del files
        return []
