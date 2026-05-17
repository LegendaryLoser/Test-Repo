"""
Tests for tools.spec_lint.git_history.

Real git, real subprocess, ephemeral tmp_path repos. No mocks.

PHASE-1 / CHG-0004. Red in TASK-0006, green in TASK-0007.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.git_history import historical_versions
from tools.spec_lint.tests.history_helpers import (
    make_repo_with_history,
    req_block,
    spec_file_text,
)


SPEC_REL = "openspec/specs/auth/login.spec.md"


def test_single_commit_yields_one_version(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0013
    @covers REQ-SPEC-0012
    """
    content = spec_file_text(req_block("REQ-AUTH-0001"))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [content])

    versions = list(historical_versions(repo, SPEC_REL))
    assert len(versions) == 1
    assert versions[0].content == content
    assert versions[0].spec_file.requirements[0].heading_id == "REQ-AUTH-0001"


def test_multiple_commits_oldest_first(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0014
    @covers REQ-SPEC-0012
    """
    v1 = spec_file_text(req_block("REQ-AUTH-0001", status="draft"))
    v2 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-red"))
    v3 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-green"))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2, v3])

    versions = list(historical_versions(repo, SPEC_REL))
    assert len(versions) == 3
    assert [v.content for v in versions] == [v1, v2, v3]
    assert [v.spec_file.requirements[0].frontmatter["status"] for v in versions] == [
        "draft",
        "tests-red",
        "tests-green",
    ]


def test_versions_have_distinct_shas_and_timestamps(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0015
    @covers REQ-SPEC-0012
    """
    v1 = spec_file_text(req_block("REQ-AUTH-0001"))
    v2 = spec_file_text(req_block("REQ-AUTH-0001", description="Edited."))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])

    versions = list(historical_versions(repo, SPEC_REL))
    assert len({v.sha for v in versions}) == 2
    assert all(len(v.sha) == 40 for v in versions)
    assert versions[0].timestamp <= versions[1].timestamp


def test_parsed_spec_file_matches_content(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0016
    @covers REQ-SPEC-0012

        The parsed SpecFile attached to each HistoricalVersion must equal what
        parse_spec_file would produce on the same text.
    """
    from tools.spec_lint.parser import parse_spec_file

    content = spec_file_text(req_block("REQ-AUTH-0001"), req_block("REQ-AUTH-0002"))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [content])
    versions = list(historical_versions(repo, SPEC_REL))

    # Materialize the same content on disk and parse it via the file path
    # for a like-for-like comparison.
    on_disk = tmp_path / "snapshot.spec.md"
    on_disk.write_text(content)
    expected = parse_spec_file(on_disk)

    got = versions[0].spec_file
    assert [r.heading_id for r in got.requirements] == [
        r.heading_id for r in expected.requirements
    ]
    assert [r.frontmatter for r in got.requirements] == [
        r.frontmatter for r in expected.requirements
    ]
