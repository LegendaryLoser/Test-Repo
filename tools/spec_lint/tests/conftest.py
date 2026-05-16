"""Shared fixtures for spec_lint tests."""

from __future__ import annotations

import pathlib

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def valid_fixtures(fixtures_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted((fixtures_dir / "valid").glob("*.spec.md"))


def invalid_fixtures_for(fixtures_dir: pathlib.Path, subdir: str) -> list[pathlib.Path]:
    """All invalid fixtures under ``fixtures/invalid/<subdir>/``."""
    return sorted((fixtures_dir / "invalid" / subdir).glob("*.spec.md"))
