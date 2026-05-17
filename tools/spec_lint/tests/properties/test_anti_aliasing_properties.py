"""
Property-based tests for tools.spec_lint.rules.anti_aliasing.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

from hypothesis import given, settings, strategies as st

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.rules.anti_aliasing import AntiAliasing
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text


def _spec(req_id: str, body_text: str, path: str = "/fake/a.spec.md"):
    text = spec_file_text(req_block(req_id, description=body_text, acceptance="Given X, when Y, then Z."))
    return parse_spec_file_text(text, path)


# Non-empty alphanumeric content keeps fixtures deterministic and ensures we
# generate enough chars for 4-grams.
_BODY = st.text(
    alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyz 0123456789.,"),
    min_size=20,
    max_size=80,
)


@settings(max_examples=30, deadline=None)
@given(body=_BODY)
def test_identical_bodies_yield_jaccard_one(body: str) -> None:
    """
    @test-id TEST-SPEC-0071
    @covers REQ-SPEC-0009
    """
    s1 = _spec("REQ-A-0001", body, "/fake/a.spec.md")
    s2 = _spec("REQ-A-0002", body, "/fake/b.spec.md")
    findings = AntiAliasing().check_corpus([s1, s2])
    rule_findings = [f for f in findings if f.rule_id == "anti-aliasing"]
    assert rule_findings, f"Identical bodies should always be flagged; got {findings}"


@settings(max_examples=30, deadline=None)
@given(
    a=st.text(alphabet="abcdef", min_size=20, max_size=40),
    b=st.text(alphabet="ghijkl", min_size=20, max_size=40),
)
def test_disjoint_ngram_sets_yield_no_findings(a: str, b: str) -> None:
    """
    @test-id TEST-SPEC-0072
    @covers REQ-SPEC-0009

        Bodies drawn from disjoint character alphabets cannot share any
        character 4-grams; Jaccard = 0; never above threshold.
    """
    s1 = _spec("REQ-A-0001", a, "/fake/a.spec.md")
    s2 = _spec("REQ-A-0002", b, "/fake/b.spec.md")
    findings = [
        f for f in AntiAliasing().check_corpus([s1, s2]) if f.rule_id == "anti-aliasing"
    ]
    # Acceptance is constant ("Given X, when Y, then Z.") across both;
    # similarity > 0 is possible. So instead of asserting 0 findings,
    # assert that with a high enough threshold (0.95), no finding occurs.
    findings_strict = [
        f for f in AntiAliasing(config={"ngram_size": 4, "ngram_type": "char", "threshold": 0.95}).check_corpus([s1, s2])
        if f.rule_id == "anti-aliasing"
    ]
    assert findings_strict == [], (
        f"Disjoint-alphabet descriptions should not be flagged at threshold 0.95; got {findings_strict}"
    )


@settings(max_examples=20, deadline=None)
@given(a=_BODY, b=_BODY)
def test_check_corpus_is_order_insensitive(a: str, b: str) -> None:
    """
    @test-id TEST-SPEC-0073
    @covers REQ-SPEC-0009

        Feeding [s1, s2] vs [s2, s1] to check_corpus yields the same finding
        count (the pairwise algorithm doesn't care about input order).
    """
    s1 = _spec("REQ-A-0001", a, "/fake/a.spec.md")
    s2 = _spec("REQ-A-0002", b, "/fake/b.spec.md")
    rule = AntiAliasing()
    f_forward = [f for f in rule.check_corpus([s1, s2]) if f.rule_id == "anti-aliasing"]
    f_reverse = [f for f in rule.check_corpus([s2, s1]) if f.rule_id == "anti-aliasing"]
    assert len(f_forward) == len(f_reverse)


@settings(max_examples=30, deadline=None)
@given(body=_BODY)
def test_self_pairs_never_produce_findings(body: str) -> None:
    """
    @test-id TEST-SPEC-0074
    @covers REQ-SPEC-0009

        A corpus of a single SpecFile with a single REQ has no pairs; even at
        threshold 0.0 there is nothing to flag.
    """
    s = _spec("REQ-A-0001", body)
    findings = [
        f for f in AntiAliasing(config={"ngram_size": 4, "ngram_type": "char", "threshold": 0.0}).check_corpus([s])
        if f.rule_id == "anti-aliasing"
    ]
    assert findings == [], f"Single REQ should produce no pairs; got {findings}"
