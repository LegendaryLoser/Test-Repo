"""
Property-based tests for tools.spec_lint.rules.compound_requirement_detector.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import pytest


def test_N_given_bullets_flag_iff_N_gt_1() -> None:
    """
    @test-id TEST-SPEC-0069
    Property: for N in 0..10, a REQ with N Given/When/Then bullets in its
    Acceptance produces a finding iff N > 1. The finding message contains N.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_case_does_not_affect_count() -> None:
    """
    @test-id TEST-SPEC-0070
    Property: 'Given', 'GIVEN', 'given', 'GiVeN' all count as the same
    assertion. Two bullets, any case → finding.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")
