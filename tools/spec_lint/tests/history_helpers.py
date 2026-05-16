"""
Helpers for tests that need real git history.

Real subprocess, real git, no mocks. Each helper operates inside a caller-
supplied tmp_path so tests stay isolated.
"""

from __future__ import annotations

import pathlib
import subprocess


def _run(cmd: list[str], cwd: pathlib.Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)


def make_repo_with_history(
    tmp_path: pathlib.Path, file_rel: str, versions: list[str]
) -> pathlib.Path:
    """Initialize a git repo at ``tmp_path``; commit each version of
    ``file_rel`` sequentially. Returns the repo path.

    Each version becomes its own commit with message ``version N``. Author
    name/email are pinned so commits are reproducible across machines.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init", "-q", "-b", "main"], cwd=repo)
    _run(["git", "config", "user.email", "spec-lint-test@example.invalid"], cwd=repo)
    _run(["git", "config", "user.name", "spec-lint-test"], cwd=repo)
    _run(["git", "config", "commit.gpgsign", "false"], cwd=repo)

    target = repo / file_rel
    target.parent.mkdir(parents=True, exist_ok=True)

    for i, content in enumerate(versions, start=1):
        target.write_text(content)
        _run(["git", "add", file_rel], cwd=repo)
        _run(["git", "commit", "-q", "--allow-empty-message", "-m", f"version {i}"], cwd=repo)

    return repo


# ---------------------------------------------------------------------------
# Reusable spec-block builders for tests. Keep these flexible enough that
# tests can vary one field at a time without copy-pasting boilerplate.
# ---------------------------------------------------------------------------


def req_block(
    req_id: str,
    *,
    status: str = "draft",
    revision: int = 1,
    description: str = "Single-assertion description.",
    acceptance: str = "Given X, when Y, then Z.",
    introduced: str = "CHG-0001",
    supersedes: str | None = None,
    phase: str = "PHASE-1",
    tier: str = "unit",
) -> str:
    """Return a single REQ block as it would appear inside a spec file."""
    supersedes_yaml = "null" if supersedes is None else supersedes
    return (
        f"## {req_id}\n"
        f"---\n"
        f"id: {req_id}\n"
        f"revision: {revision}\n"
        f"status: {status}\n"
        f"introduced: {introduced}\n"
        f"supersedes: {supersedes_yaml}\n"
        f"phase: {phase}\n"
        f"tier: {tier}\n"
        f"references:\n"
        f"  epic: EPIC-0001\n"
        f"  story: STORY-0001\n"
        f"  adrs: []\n"
        f"---\n"
        f"\n"
        f"### Description\n"
        f"{description}\n"
        f"\n"
        f"### Acceptance\n"
        f"- {acceptance}\n"
    )


def spec_file_text(*req_blocks: str, title: str = "Test spec") -> str:
    """Concatenate blocks with a title preamble into a complete spec file."""
    return f"# {title}\n\n" + "\n".join(req_blocks)
