"""
Tests for tools.spec_lint.rules.bmad_direct_reference.

PHASE-1 / CHG-0012. Red in TASK-0025, green in TASK-0026.
"""

from __future__ import annotations

import pathlib
import textwrap

from tools.spec_lint.rules.bmad_direct_reference import BmadDirectReference


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]


def _check(files: list[tuple[pathlib.Path, str]]):
    return BmadDirectReference().check_files(files)


def _file(rel: str, content: str) -> tuple[pathlib.Path, str]:
    return (pathlib.Path(rel), textwrap.dedent(content))


def test_from_bmad_import_flagged() -> None:
    """
    @test-id TEST-SPEC-0085
    @covers REQ-SPEC-0002
    """
    findings = _check([_file("tools/foo/bar.py", "from _bmad.bmm import something\n")])
    assert len(findings) == 1, f"expected 1 finding, got: {findings}"
    f = findings[0]
    assert f.rule_id == "bmad-direct-reference"
    assert f.severity == "error"
    assert "tools/foo/bar.py" in f.file


def test_import_bmad_flagged() -> None:
    """
    @test-id TEST-SPEC-0086
    @covers REQ-SPEC-0002
    """
    findings = _check([_file("packages/x/y.py", "import _bmad.config\n")])
    assert len(findings) == 1, f"expected 1 finding, got: {findings}"
    assert findings[0].rule_id == "bmad-direct-reference"


def test_subprocess_bmad_path_flagged() -> None:
    """
    @test-id TEST-SPEC-0087
    @covers REQ-SPEC-0002
    """
    src = "subprocess.run(['_bmad/scripts/resolve_config.py', '--project-root', '.'])\n"
    findings = _check([_file("projects/demo/src/x.py", src)])
    assert len(findings) == 1, f"expected 1 finding, got: {findings}"
    assert findings[0].rule_id == "bmad-direct-reference"


def test_clean_file_passes() -> None:
    """
    @test-id TEST-SPEC-0088
    @covers REQ-SPEC-0002
    """
    src = textwrap.dedent("""\
        import os
        from pathlib import Path

        def hello():
            return "world"
        """)
    findings = _check([_file("tools/foo/bar.py", src)])
    assert findings == [], f"expected no findings, got: {findings}"


def test_tea_path_allowed() -> None:
    """
    @test-id TEST-SPEC-0089
    @covers REQ-SPEC-0002
    """
    src = "from _bmad.bmm.skills import something\n"
    findings = _check([_file("tools/tea/integration.py", src)])
    assert findings == [], (
        f"tools/tea/ is the authorized integration point per ADR-0002 §6; "
        f"expected no findings, got: {findings}"
    )


def test_docstring_mention_not_flagged() -> None:
    """
    @test-id TEST-SPEC-0090
    @covers REQ-SPEC-0002

    Strings/comments/docstrings mentioning _bmad/ paths must NOT be
    flagged. Only import statements and executable-path forms count.
    """
    src = textwrap.dedent('''\
        """This module talks to _bmad/ subprocess paths but doesn't import them."""

        # The vendored _bmad/ install lives at repo root; see ADR-0002.
        STAGING_DIR = "openspec/_bmad-output"

        def main():
            return STAGING_DIR
        ''')
    findings = _check([_file("tools/foo/explainer.py", src)])
    assert findings == [], f"expected no findings on docstring mentions, got: {findings}"


def test_real_repo_passes() -> None:
    """
    @test-id TEST-SPEC-0091
    @covers REQ-SPEC-0002

    Walk the live tree under tools/, packages/, projects/ and feed
    every relevant file to the rule. Today: zero authorized
    integrations exist (no tools/tea/), and no in-scope file should
    import or execute _bmad/.
    """
    targets: list[tuple[pathlib.Path, str]] = []
    for top in ("tools", "packages", "projects"):
        root = REPO_ROOT / top
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix not in {".py", ".ts", ".tsx", ".js", ".jsx", ".sh"}:
                continue
            try:
                targets.append((p.relative_to(REPO_ROOT), p.read_text()))
            except UnicodeDecodeError:
                continue
    findings = _check(targets)
    assert findings == [], (
        "bmad-direct-reference findings on real repo: "
        + "; ".join(f"{f.file}: {f.message}" for f in findings)
    )
