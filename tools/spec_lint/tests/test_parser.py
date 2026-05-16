"""
Tests for tools.spec_lint.parser.

The parser is deliberately permissive — strict validation is rules' job.
These tests pin the parser contract; rule tests pin rule behavior.

PHASE-1 / CHG-0003. Red in TASK-0004, green in TASK-0005.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.parser import parse_spec_file


def test_parser_extracts_single_req_block(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0001
    @covers REQ-SPEC-0001 (to be introduced in CHG-0003 spec-storage spec)
    """
    spec = parse_spec_file(fixtures_dir / "valid" / "simple.spec.md")
    assert len(spec.requirements) == 1
    req = spec.requirements[0]
    assert req.heading_id == "REQ-AUTH-0001"
    assert req.frontmatter is not None
    assert req.frontmatter["id"] == "REQ-AUTH-0001"
    assert req.frontmatter["status"] == "draft"
    assert "### Description" in req.body


def test_parser_extracts_multi_req_blocks(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0002
    """
    spec = parse_spec_file(fixtures_dir / "valid" / "multi_req.spec.md")
    assert len(spec.requirements) == 2
    ids = [r.heading_id for r in spec.requirements]
    assert ids == ["REQ-SEARCH-0001", "REQ-SEARCH-0002"]
    # Each block carries its own frontmatter — not the other's.
    assert spec.requirements[0].frontmatter["revision"] == 1
    assert spec.requirements[1].frontmatter["revision"] == 2
    assert spec.requirements[1].frontmatter["supersedes"] == "REQ-SEARCH-0001"


def test_parser_handles_missing_frontmatter(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0003

    A REQ heading with no `---` block parses; ``frontmatter`` is None.
    The frontmatter-valid rule (not the parser) flags this as a defect.
    """
    spec = parse_spec_file(fixtures_dir / "invalid" / "frontmatter" / "missing_block.spec.md")
    assert len(spec.requirements) == 1
    req = spec.requirements[0]
    assert req.heading_id == "REQ-AUTH-0001"
    assert req.frontmatter is None
    assert req.frontmatter_raw is None


def test_parser_heading_line_is_1_based(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0004
    """
    spec = parse_spec_file(fixtures_dir / "valid" / "simple.spec.md")
    text = (fixtures_dir / "valid" / "simple.spec.md").read_text().splitlines()
    actual_line = next(i + 1 for i, l in enumerate(text) if l.startswith("## REQ-"))
    assert spec.requirements[0].heading_line == actual_line


def test_parser_path_is_recorded(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0005
    """
    p = fixtures_dir / "valid" / "simple.spec.md"
    spec = parse_spec_file(p)
    assert spec.path == str(p)
    for r in spec.requirements:
        assert r.file == str(p)
