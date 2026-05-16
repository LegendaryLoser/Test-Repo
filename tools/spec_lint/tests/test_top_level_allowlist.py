"""
Tests for tools.spec_lint.rules.top_level_allowlist.

PHASE-1 / CHG-0011. Red in TASK-0022, green in TASK-0023.

Each test uses a tmp_path that is initialized as a real git repo so the
rule's `git ls-files` invocation has something to read. A pure-fs probe
would be simpler but `TopLevelAllowlist.check_repo()` is specified to
use git ls-files (so untracked working-tree noise — .venv, __pycache__ —
is invisible to the gate). Tests therefore must commit fixture files to
make them tracked.
"""

from __future__ import annotations

import pathlib
import subprocess

import pytest

from tools.spec_lint.rules.top_level_allowlist import TopLevelAllowlist
from tools.spec_lint._top_level_allowlist import (
    ALLOWED_TOP_LEVEL_ENTRIES,
    REQUIRED_TOP_LEVEL_DIRS,
)


def _git(repo: pathlib.Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _init_repo_with(repo: pathlib.Path, entries: dict[str, str]) -> None:
    """Create a git repo at `repo`, populate `entries` (path -> content),
    commit them so they appear in `git ls-files`."""
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    _git(repo, "config", "commit.gpgsign", "false")
    for rel, content in entries.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")


def _findings_by_message(findings) -> list[str]:
    return sorted(f.message for f in findings)


def test_clean_repo_with_full_allowlist_passes(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0078
    @covers REQ-ARCH-0001
    """
    entries = {}
    for name in ALLOWED_TOP_LEVEL_ENTRIES:
        if name.endswith(".md") or name.endswith(".toml") or name == ".gitignore":
            entries[name] = "fixture\n"
        else:
            entries[f"{name}/.keep"] = ""
    _init_repo_with(tmp_path, entries)

    findings = TopLevelAllowlist().check_repo(tmp_path)
    assert findings == [], f"expected no findings on clean repo, got: {findings}"


def test_missing_required_dir_surfaces_finding(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0079
    @covers REQ-ARCH-0001
    """
    # Populate everything *except* one required dir.
    omitted = "openspec"
    assert omitted in REQUIRED_TOP_LEVEL_DIRS
    entries = {}
    for name in ALLOWED_TOP_LEVEL_ENTRIES:
        if name == omitted:
            continue
        if name.endswith(".md") or name.endswith(".toml") or name == ".gitignore":
            entries[name] = "fixture\n"
        else:
            entries[f"{name}/.keep"] = ""
    _init_repo_with(tmp_path, entries)

    findings = TopLevelAllowlist().check_repo(tmp_path)
    assert len(findings) == 1, f"expected 1 finding, got: {findings}"
    f = findings[0]
    assert f.rule_id == "top-level-allowlist"
    assert f.severity == "error"
    assert omitted in f.message
    assert "missing" in f.message.lower() or "required" in f.message.lower()


def test_unexpected_top_level_entry_surfaces_finding(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0080
    @covers REQ-ARCH-0001
    """
    entries = {}
    for name in ALLOWED_TOP_LEVEL_ENTRIES:
        if name.endswith(".md") or name.endswith(".toml") or name == ".gitignore":
            entries[name] = "fixture\n"
        else:
            entries[f"{name}/.keep"] = ""
    entries["docs/index.md"] = "# Docs\n"  # unexpected top-level dir
    _init_repo_with(tmp_path, entries)

    findings = TopLevelAllowlist().check_repo(tmp_path)
    assert len(findings) == 1, f"expected 1 finding, got: {findings}"
    f = findings[0]
    assert f.rule_id == "top-level-allowlist"
    assert f.severity == "error"
    assert "docs" in f.message
    assert "unexpected" in f.message.lower() or "allowlist" in f.message.lower()


def test_real_repo_passes(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0081
    @covers REQ-ARCH-0001

    Run the rule against the real repo this test-suite lives in. The
    repo's current state is expected to satisfy the allowlist; if it
    doesn't, that is the failure this rule is designed to catch and the
    test should fail loudly.
    """
    del tmp_path  # not used; intentionally probing the real repo
    repo_root = pathlib.Path(__file__).resolve().parents[3]
    findings = TopLevelAllowlist().check_repo(repo_root)
    assert findings == [], f"real repo has top-level findings: {findings}"
