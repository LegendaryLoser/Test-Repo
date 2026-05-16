"""Shared fixtures for tools/ci tests."""

from __future__ import annotations

import pathlib

import pytest


@pytest.fixture(scope="session")
def repo_root() -> pathlib.Path:
    """Absolute path to the repository root, regardless of pytest invocation cwd."""
    here = pathlib.Path(__file__).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "pyproject.toml").is_file() and (candidate / "openspec").is_dir():
            return candidate
    raise RuntimeError("Could not locate repo root from " + str(here))
