"""
Tests for tools.spec_lint.rules.spec_frontmatter_valid.

PHASE-1 / CHG-0003. Red in TASK-0004, green in TASK-0005.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.parser import parse_spec_file
from tools.spec_lint.rules.spec_frontmatter_valid import SpecFrontmatterValid
from tools.spec_lint.tests.conftest import invalid_fixtures_for


def _check(path: pathlib.Path):
    spec = parse_spec_file(path)
    return SpecFrontmatterValid().check(spec)


def test_valid_fixtures_produce_no_findings(valid_fixtures: list[pathlib.Path]) -> None:
    """
    @test-id TEST-SPEC-0009
    @covers (rule: spec-frontmatter-valid)
    """
    for fx in valid_fixtures:
        findings = _check(fx)
        assert findings == [], f"Expected no findings for {fx.name}, got: {findings}"


def test_each_invalid_frontmatter_fixture_produces_a_finding(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0010
    """
    fixtures = invalid_fixtures_for(fixtures_dir, "frontmatter")
    assert fixtures, "no invalid/frontmatter fixtures present"
    for fx in fixtures:
        findings = _check(fx)
        rule_findings = [f for f in findings if f.rule_id == "spec-frontmatter-valid"]
        assert rule_findings, (
            f"Expected ≥1 spec-frontmatter-valid finding for {fx.name}, got: {findings}"
        )


def test_id_mismatch_finding_is_specific(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0011

    The id-mismatch fixture should produce a finding whose message clearly
    names the conflict between heading and frontmatter id. Acts as a regression
    guard against a future implementation that silently flags missing-id.
    """
    findings = _check(fixtures_dir / "invalid" / "frontmatter" / "id_mismatch.spec.md")
    rule_findings = [f for f in findings if f.rule_id == "spec-frontmatter-valid"]
    # At least one finding mentions both IDs.
    matches = [f for f in rule_findings if "REQ-AUTH-0001" in f.message and "REQ-AUTH-0002" in f.message]
    assert matches, f"Expected a mismatch finding naming both IDs, got: {rule_findings}"


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0012
    """
    r = SpecFrontmatterValid()
    assert r.id == "spec-frontmatter-valid"
    assert "ADR-0004" in r.description
