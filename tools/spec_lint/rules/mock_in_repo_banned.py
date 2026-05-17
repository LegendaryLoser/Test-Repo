"""
Rule: mock-in-repo-banned

Enforces [ADR-0006](../../../openspec/architecture/decisions/ADR-0006-testing-tiers.md)
§2 — no ``jest.mock``, ``vi.mock``, ``sinon.stub``/``sinon.fake``,
``unittest.mock.patch``, ``MagicMock``, ``Mock``, ``monkeypatch.setattr``,
or ``mocker.patch`` applied to modules within this repository.

Boundary adapters must be real per ADR-0006 §3; only network transport
may be substituted at the edge (e.g. ``patch("requests.get")``).

Target resolution:
- ``patch("X")`` and friends — if X starts with an in-repo prefix
  (``tools.``, ``packages.``, ``projects.``, ``_bmad.``), flag. If X
  starts with anything else, allow.
- Everything else (no target, identifier target, complex expression)
  — flag conservatively.

Allow marker: ``spec-lint: allow mock-in-repo-banned`` on the same line.
Rule's own implementation + test files are structurally exempt.
"""

from __future__ import annotations

import pathlib
import re

from ..models import Finding


_PY_PATCH_STRING = re.compile(
    r"""\b(?:unittest\.mock\.|mock\.|mocker\.)?patch\s*\(\s*["']([^"']+)["']"""
)
_PY_PATCH_OBJECT = re.compile(
    r"""\b(?:unittest\.mock\.|mock\.|mocker\.)?patch\.object\s*\("""
)
_PY_MAGICMOCK = re.compile(r"\b(?:unittest\.mock\.|mock\.)?MagicMock\s*\(")
_PY_MOCK = re.compile(r"\b(?:unittest\.mock\.|mock\.)?Mock\s*\(")
_PY_MONKEYPATCH = re.compile(r"\bmonkeypatch\.setattr\s*\(")
_PY_MOCKER_PATCH_STR = re.compile(r"""\bmocker\.patch\s*\(\s*["']([^"']+)["']""")

_JS_JEST_MOCK = re.compile(r"\bjest\.mock\s*\(")
_JS_JEST_FN_MOCK_IMPL = re.compile(r"\bjest\.fn\s*\(\s*\)\.mockImplementation")
_JS_VI_MOCK = re.compile(r"\bvi\.mock\s*\(")
_JS_SINON = re.compile(r"\bsinon\.(?:stub|fake)\s*\(")

_IN_REPO_PREFIXES = ("tools.", "packages.", "projects.", "_bmad.")

_ALLOW_MARKER = "spec-lint: allow mock-in-repo-banned"

_OWN_FILE_SUFFIXES = (
    "tools/spec_lint/rules/mock_in_repo_banned.py",
    "tools/spec_lint/tests/test_mock_in_repo_banned.py",
)


def _posix(path: pathlib.Path) -> str:
    return path.as_posix()


class MockInRepoBanned:
    id = "mock-in-repo-banned"
    description = (
        "Banned mock APIs (unittest.mock.patch, MagicMock, jest.mock, …) "
        "applied to in-repo modules are forbidden (ADR-0006 §2)"
    )

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        findings: list[Finding] = []
        for path, text in files:
            findings.extend(self._check_one(path, text))
        return findings

    def _check_one(
        self, path: pathlib.Path, text: str
    ) -> list[Finding]:
        path_str = _posix(path)
        if any(path_str.endswith(s) for s in _OWN_FILE_SUFFIXES):
            return []

        suffix = path.suffix
        if suffix == ".py":
            checks = self._check_python_line
        elif suffix in (".ts", ".tsx", ".js", ".jsx"):
            checks = self._check_js_line
        else:
            return []

        out: list[Finding] = []
        for i, line in enumerate(text.splitlines(), start=1):
            if _ALLOW_MARKER in line:
                continue
            msg = checks(line)
            if msg is None:
                continue
            out.append(
                Finding(
                    rule_id=self.id,
                    severity="error",
                    file=path_str,
                    line=i,
                    message=msg,
                )
            )
        return out

    def _check_python_line(self, line: str) -> str | None:
        # String-target patches: extract target, allow if external.
        for pattern in (_PY_PATCH_STRING, _PY_MOCKER_PATCH_STR):
            m = pattern.search(line)
            if m:
                target = m.group(1)
                if any(target.startswith(p) for p in _IN_REPO_PREFIXES):
                    return (
                        f"patch target {target!r} is in-repo (ADR-0006 §2). "
                        f"Use a real adapter (ADR-0006 §3) or add "
                        f"`# {_ALLOW_MARKER}` if this is an authorized edge case."
                    )
                return None

        # Anything else: conservative flag.
        for pattern, descr in (
            (_PY_PATCH_OBJECT, "patch.object(...)"),
            (_PY_MAGICMOCK, "MagicMock(...)"),
            (_PY_MOCK, "Mock(...)"),
            (_PY_MONKEYPATCH, "monkeypatch.setattr(...)"),
        ):
            if pattern.search(line):
                return (
                    f"{descr} cannot be resolved to an external target "
                    f"(ADR-0006 §2 bans in-repo mocks; conservative flag). "
                    f"Use a real adapter or add `# {_ALLOW_MARKER}`."
                )
        return None

    def _check_js_line(self, line: str) -> str | None:
        for pattern, descr in (
            (_JS_JEST_MOCK, "jest.mock(...)"),
            (_JS_JEST_FN_MOCK_IMPL, "jest.fn().mockImplementation(...)"),
            (_JS_VI_MOCK, "vi.mock(...)"),
            (_JS_SINON, "sinon.stub/fake(...)"),
        ):
            if pattern.search(line):
                return (
                    f"{descr} is banned by ADR-0006 §2 unless targeting "
                    f"external transport. Use a real adapter or add "
                    f"`// {_ALLOW_MARKER}`."
                )
        return None
