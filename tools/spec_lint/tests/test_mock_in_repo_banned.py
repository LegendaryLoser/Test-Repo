"""
Tests for tools.spec_lint.rules.mock_in_repo_banned.

PHASE-1 / CHG-0012. Red in TASK-0025, green in TASK-0026.
"""

from __future__ import annotations

import pathlib
import textwrap

from tools.spec_lint.rules.mock_in_repo_banned import MockInRepoBanned


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]


def _check(files: list[tuple[pathlib.Path, str]]):
    return MockInRepoBanned().check_files(files)


def _file(rel: str, content: str) -> tuple[pathlib.Path, str]:
    return (pathlib.Path(rel), textwrap.dedent(content))


def test_patch_in_repo_string_flagged() -> None:
    """
    @test-id TEST-SPEC-0092
    @covers REQ-SPEC-0003
    """
    src = textwrap.dedent("""\
        from unittest.mock import patch

        def test_x():
            with patch("tools.spec_lint.parser.parse_spec_file") as m:
                pass
        """)
    findings = _check([_file("tools/foo/tests/test_x.py", src)])
    assert len(findings) >= 1, f"expected at least 1 finding, got: {findings}"
    assert any(f.rule_id == "mock-in-repo-banned" for f in findings)


def test_patch_external_module_allowed() -> None:
    """
    @test-id TEST-SPEC-0093
    @covers REQ-SPEC-0003

    Per ADR-0006 §2, the ban is "applied to modules within this
    repository". Mocking ``requests.get`` for HTTP-transport reasons
    is permitted at the edge.
    """
    src = textwrap.dedent("""\
        from unittest.mock import patch

        def test_external():
            with patch("requests.get") as m:
                m.return_value.status_code = 200
        """)
    findings = _check([_file("tools/foo/tests/test_x.py", src)])
    assert findings == [], (
        f"external module mock must be allowed per ADR-0006 §2, got: {findings}"
    )


def test_magicmock_call_flagged_conservatively() -> None:
    """
    @test-id TEST-SPEC-0094
    @covers REQ-SPEC-0003

    ``MagicMock()`` with no target can imitate anything in-repo;
    conservative interpretation flags it. Author must replace with a
    real adapter (ADR-0006 §3) or add an explicit allow marker.
    """
    src = textwrap.dedent("""\
        from unittest.mock import MagicMock

        def test_y():
            m = MagicMock()
            m.some_method.return_value = 42
        """)
    findings = _check([_file("packages/x/tests/test_y.py", src)])
    assert len(findings) >= 1, f"expected at least 1 finding, got: {findings}"


def test_monkeypatch_setattr_flagged() -> None:
    """
    @test-id TEST-SPEC-0095
    @covers REQ-SPEC-0003
    """
    src = textwrap.dedent("""\
        def test_z(monkeypatch):
            monkeypatch.setattr("tools.spec_lint.parser.something", lambda: 1)
        """)
    findings = _check([_file("tools/foo/tests/test_z.py", src)])
    assert len(findings) >= 1, f"expected at least 1 finding, got: {findings}"


def test_allow_marker_suppresses() -> None:
    """
    @test-id TEST-SPEC-0096
    @covers REQ-SPEC-0003
    """
    src = textwrap.dedent("""\
        from unittest.mock import MagicMock

        def test_legitimate_external():
            m = MagicMock()  # spec-lint: allow mock-in-repo-banned
            m.return_value = 1
        """)
    findings = _check([_file("tools/foo/tests/test_q.py", src)])
    assert findings == [], (
        f"allow marker on same line must suppress; got: {findings}"
    )


def test_clean_file_passes() -> None:
    """
    @test-id TEST-SPEC-0097
    @covers REQ-SPEC-0003
    """
    src = textwrap.dedent("""\
        def test_addition():
            assert 1 + 1 == 2
        """)
    findings = _check([_file("tools/foo/tests/test_clean.py", src)])
    assert findings == [], f"expected no findings on clean file, got: {findings}"


def test_real_repo_passes() -> None:
    """
    @test-id TEST-SPEC-0098
    @covers REQ-SPEC-0003

    Walk the live tree under tools/, packages/, projects/ and confirm
    no banned mock APIs are used. Today: zero mocks exist in the repo.
    """
    targets: list[tuple[pathlib.Path, str]] = []
    for top in ("tools", "packages", "projects"):
        root = REPO_ROOT / top
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix not in {".py", ".ts", ".tsx", ".js", ".jsx"}:
                continue
            try:
                targets.append((p.relative_to(REPO_ROOT), p.read_text()))
            except UnicodeDecodeError:
                continue
    findings = _check(targets)
    assert findings == [], (
        "mock-in-repo-banned findings on real repo: "
        + "; ".join(f"{f.file}: {f.message}" for f in findings)
    )
