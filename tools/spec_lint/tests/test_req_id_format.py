"""
Tests for tools.spec_lint.rules.req_id_format.

PHASE-1 / CHG-0003. Red in TASK-0004, green in TASK-0005.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.parser import parse_spec_file
from tools.spec_lint.rules.req_id_format import ReqIdFormat
from tools.spec_lint.tests.conftest import invalid_fixtures_for


def _check(path: pathlib.Path):
    spec = parse_spec_file(path)
    return ReqIdFormat().check(spec)


def test_valid_fixtures_produce_no_findings(valid_fixtures: list[pathlib.Path]) -> None:
    """
    @test-id TEST-SPEC-0006
    @covers REQ-SPEC-0004
    """
    for fx in valid_fixtures:
        findings = _check(fx)
        assert findings == [], f"Expected no findings for {fx.name}, got: {findings}"


def test_invalid_req_id_fixtures_each_produce_a_finding(fixtures_dir: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0007
    @covers REQ-SPEC-0004

        Every fixture in invalid/req_id/ should yield at least one req-id-format
        finding whose rule_id matches and severity is "error".
    """
    fixtures = invalid_fixtures_for(fixtures_dir, "req_id")
    assert fixtures, "no invalid/req_id fixtures present"
    for fx in fixtures:
        findings = _check(fx)
        rule_findings = [f for f in findings if f.rule_id == "req-id-format"]
        assert rule_findings, (
            f"Expected ≥1 req-id-format finding for {fx.name}, got: {findings}"
        )
        for f in rule_findings:
            assert f.severity == "error"
            assert f.req_id is not None
            assert f.line is not None and f.line > 0


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0008
    @covers REQ-SPEC-0004
    """
    r = ReqIdFormat()
    assert r.id == "req-id-format"
    assert "ADR-0004" in r.description
