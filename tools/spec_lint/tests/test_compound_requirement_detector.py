"""
Tests for tools.spec_lint.rules.compound_requirement_detector.

PHASE-1 / CHG-0006. Red in TASK-0010, green in TASK-0011.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.rules.compound_requirement_detector import (
    CompoundRequirementDetector,
)
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text


FAKE_PATH = "/fake/openspec/specs/test.spec.md"


def _parse(text: str):
    return parse_spec_file_text(text, FAKE_PATH)


def _block_with_acceptance_lines(req_id: str, *acceptance_lines: str) -> str:
    """Single-purpose block builder: lets each test express exactly the
    Acceptance shape that exercises the rule."""
    acc_body = "\n".join(f"- {line}" for line in acceptance_lines)
    return (
        f"## {req_id}\n"
        f"---\n"
        f"id: {req_id}\n"
        f"revision: 1\n"
        f"status: draft\n"
        f"introduced: CHG-0001\n"
        f"supersedes: null\n"
        f"phase: PHASE-1\n"
        f"tier: unit\n"
        f"references:\n"
        f"  epic: EPIC-0001\n"
        f"  story: STORY-0001\n"
        f"  adrs: []\n"
        f"---\n"
        f"\n"
        f"### Description\n"
        f"A description.\n"
        f"\n"
        f"### Acceptance\n"
        f"{acc_body}\n"
    )


def test_single_given_when_then_is_clean() -> None:
    """
    @test-id TEST-SPEC-0045
    """
    text = spec_file_text(req_block("REQ-AUTH-0001"))
    findings = CompoundRequirementDetector().check(_parse(text))
    assert findings == []


def test_two_given_when_then_bullets_is_flagged() -> None:
    """
    @test-id TEST-SPEC-0046

    The exact failure mode this rule exists to catch: a single REQ whose
    Acceptance has two distinct Given/When/Then assertions. Should be split
    into two REQs.
    """
    block = _block_with_acceptance_lines(
        "REQ-AUTH-0001",
        "Given valid creds, when login is invoked, then a session is returned.",
        "Given invalid creds, when login is invoked, then an error is returned.",
    )
    text = spec_file_text(block)
    findings = CompoundRequirementDetector().check(_parse(text))
    rule_findings = [f for f in findings if f.rule_id == "compound-requirement-detector"]
    assert rule_findings
    assert any("2" in f.message for f in rule_findings)
    assert all(f.req_id == "REQ-AUTH-0001" for f in rule_findings)


def test_three_given_when_then_bullets_is_flagged() -> None:
    """
    @test-id TEST-SPEC-0047
    """
    block = _block_with_acceptance_lines(
        "REQ-AUTH-0001",
        "Given A, when X, then Z1.",
        "Given B, when X, then Z2.",
        "Given C, when X, then Z3.",
    )
    text = spec_file_text(block)
    findings = CompoundRequirementDetector().check(_parse(text))
    assert [f for f in findings if f.rule_id == "compound-requirement-detector"]


def test_no_acceptance_section_does_not_crash() -> None:
    """
    @test-id TEST-SPEC-0048

    A REQ missing its Acceptance section is a frontmatter/structural defect
    (caught by spec-frontmatter-valid). compound-requirement-detector must
    return no findings for this case — it is not the right rule to flag it.
    """
    text = (
        "## REQ-AUTH-0001\n"
        "---\n"
        "id: REQ-AUTH-0001\n"
        "revision: 1\n"
        "status: draft\n"
        "introduced: CHG-0001\n"
        "supersedes: null\n"
        "phase: PHASE-1\n"
        "tier: unit\n"
        "references:\n"
        "  epic: EPIC-0001\n"
        "  story: STORY-0001\n"
        "  adrs: []\n"
        "---\n"
        "\n"
        "### Description\n"
        "Body without Acceptance.\n"
    )
    findings = CompoundRequirementDetector().check(_parse(text))
    assert findings == []


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0049
    """
    r = CompoundRequirementDetector()
    assert r.id == "compound-requirement-detector"
    assert "ADR-0004" in r.description
