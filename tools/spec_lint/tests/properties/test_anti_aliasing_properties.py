"""
Property-based tests for tools.spec_lint.rules.anti_aliasing.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import pytest


def test_identical_bodies_yield_jaccard_one() -> None:
    """
    @test-id TEST-SPEC-0071
    Property: two REQs with byte-identical Description+Acceptance bodies
    produce a finding for any threshold ≤ 1.0.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_disjoint_ngram_sets_yield_jaccard_zero() -> None:
    """
    @test-id TEST-SPEC-0072
    Property: two REQs whose bodies share no n-grams of the configured size
    never produce a finding, regardless of threshold > 0.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_jaccard_is_symmetric() -> None:
    """
    @test-id TEST-SPEC-0073
    Property: feeding [s1, s2] and [s2, s1] to check_corpus produces the
    same finding count (the rule's internal pairing is order-insensitive).
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_self_pairs_never_produce_findings() -> None:
    """
    @test-id TEST-SPEC-0074
    Property: a corpus of N REQs never produces a finding pairing a REQ
    with itself, even when threshold == 0.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")
