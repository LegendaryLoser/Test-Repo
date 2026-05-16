"""
Tests for the spec_lint CLI (``python -m tools.spec_lint``).

PHASE-1 / CHG-0011. Red in TASK-0022, green in TASK-0023.

These are subprocess-based on purpose — the CLI is the unit of behavior
that CI invokes. In-process testing would skip argparse, stdout/stderr
routing, and exit-code propagation, all of which matter.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import textwrap


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]


def _run(*args: str, cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    # Force the repo root onto PYTHONPATH so ``python -m tools.spec_lint``
    # resolves regardless of the subprocess's cwd. ``python -m`` only auto-
    # adds cwd to sys.path, which is wrong when cwd is a tmp_path fixture.
    env["PYTHONPATH"] = (
        f"{REPO_ROOT}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)
    )
    return subprocess.run(
        [sys.executable, "-m", "tools.spec_lint", *args],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )


def test_validate_real_openspec_exits_zero() -> None:
    """
    @test-id TEST-SPEC-0082
    @covers REQ-SPEC-0001
    """
    result = _run("validate", "openspec")
    assert result.returncode == 0, (
        f"expected exit 0 on clean openspec/ tree, got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_validate_surfaces_planted_ill_formed_req(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0083
    @covers REQ-SPEC-0001
    """
    spec_dir = tmp_path / "openspec" / "specs" / "demo"
    spec_dir.mkdir(parents=True)
    (spec_dir / "broken.spec.md").write_text(textwrap.dedent("""\
        ---
        id: REQ-NOPE-0001
        ---

        ## req-broken-id-lowercase

        Body.
        """))

    result = _run("validate", str(tmp_path / "openspec"), cwd=REPO_ROOT)
    assert result.returncode == 1, (
        f"expected exit 1 on planted ill-formed REQ, got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    combined = result.stdout + result.stderr
    assert "broken.spec.md" in combined, (
        f"expected planted file in output, got:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_check_layout_surfaces_unexpected_entry(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0084
    @covers REQ-ARCH-0001
    """
    # Build a synthetic repo with the allowlist + one unexpected dir.
    from tools.spec_lint._top_level_allowlist import ALLOWED_TOP_LEVEL_ENTRIES

    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "t@e.com"], cwd=tmp_path, check=True
    )
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "config", "commit.gpgsign", "false"], cwd=tmp_path, check=True
    )
    for name in ALLOWED_TOP_LEVEL_ENTRIES:
        if name.endswith(".md") or name.endswith(".toml") or name == ".gitignore":
            (tmp_path / name).write_text("x\n")
        else:
            d = tmp_path / name
            d.mkdir(exist_ok=True)
            (d / ".keep").write_text("")
    surprise = tmp_path / "unexpected_dir"
    surprise.mkdir()
    (surprise / "f.txt").write_text("")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "fixture"], cwd=tmp_path, check=True
    )

    result = _run("check-layout", cwd=tmp_path)
    assert result.returncode == 1, (
        f"expected exit 1 with planted unexpected dir, got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    combined = result.stdout + result.stderr
    assert "unexpected_dir" in combined, (
        f"expected unexpected_dir in output, got:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
