"""
Property-based tests for tools.spec_lint.rules.req_id_format.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import pytest


def test_valid_req_ids_produce_no_findings() -> None:
    """
    @test-id TEST-SPEC-0061
    Property: any heading matching ^REQ-[A-Z0-9]{1,12}-\\d{4}$ produces
    no findings from the format rule.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_lowercase_domain_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0062
    Property: any heading whose DOMAIN segment contains a lowercase letter
    produces ≥1 finding.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_wrong_number_width_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0063
    Property: any heading whose number segment is not exactly 4 digits
    produces ≥1 finding.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_domain_over_12_chars_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0064
    Property: any heading whose DOMAIN segment exceeds 12 characters
    produces ≥1 finding.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")
