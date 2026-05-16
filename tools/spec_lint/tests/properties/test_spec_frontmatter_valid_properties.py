"""
Property-based tests for tools.spec_lint.rules.spec_frontmatter_valid.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import pytest


def test_dropping_any_required_key_yields_a_named_finding() -> None:
    """
    @test-id TEST-SPEC-0065
    Property: for every required key K, dropping K from a known-good
    frontmatter produces ≥1 finding whose message contains K.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_invalid_status_enum_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0066
    Property: any value for `status` outside the enum produces ≥1 finding
    citing the offending value.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_invalid_tier_enum_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0067
    Property: any value for `tier` outside the enum produces ≥1 finding.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_non_positive_revision_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0068
    Property: any non-positive integer revision (and any non-int) produces
    ≥1 finding.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")
