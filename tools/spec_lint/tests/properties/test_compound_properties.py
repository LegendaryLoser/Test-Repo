"""
Property-based tests for tools.spec_lint.rules.compound_requirement_detector.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

from hypothesis import given, settings, strategies as st

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.rules.compound_requirement_detector import (
    CompoundRequirementDetector,
)
from tools.spec_lint.tests.history_helpers import spec_file_text

FAKE_PATH = "/fake/test.spec.md"


def _block_with_n_givens(n: int, given_word: str = "Given") -> str:
    bullets = "\n".join(f"- {given_word} A, when X, then Z{i}." for i in range(n))
    return (
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
        "---\n\n"
        "### Description\nA description.\n\n"
        f"### Acceptance\n{bullets}\n"
    )


def _check(spec_text: str):
    spec = parse_spec_file_text(spec_text, FAKE_PATH)
    return CompoundRequirementDetector().check(spec)


@settings(max_examples=22, deadline=None)
@given(n=st.integers(min_value=0, max_value=10))
def test_N_given_bullets_flag_iff_N_gt_1(n: int) -> None:
    """
    @test-id TEST-SPEC-0069
    """
    text = spec_file_text(_block_with_n_givens(n))
    findings = [f for f in _check(text) if f.rule_id == "compound-requirement-detector"]
    if n > 1:
        assert findings, f"Expected ≥1 finding for n={n}"
        assert any(str(n) in f.message for f in findings), (
            f"Expected message to cite count {n}; got {[f.message for f in findings]}"
        )
    else:
        assert findings == [], f"Expected no findings for n={n}; got {findings}"


@settings(max_examples=20, deadline=None)
@given(
    given_word=st.sampled_from(["Given", "GIVEN", "given", "GiVeN", "gIvEn"]),
    n=st.integers(min_value=2, max_value=6),
)
def test_case_does_not_affect_count(given_word: str, n: int) -> None:
    """
    @test-id TEST-SPEC-0070
    """
    text = spec_file_text(_block_with_n_givens(n, given_word=given_word))
    findings = [f for f in _check(text) if f.rule_id == "compound-requirement-detector"]
    assert findings, f"Expected ≥1 finding for given_word={given_word!r}, n={n}"
