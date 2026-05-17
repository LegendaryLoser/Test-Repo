"""
Property-based tests for tools.spec_lint.rules.req_id_format.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

from hypothesis import given, settings, strategies as st

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.rules.req_id_format import ReqIdFormat
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text

FAKE_PATH = "/fake/openspec/specs/test.spec.md"

# Strict ID matching ADR-0004 §1.
_VALID_ID = st.from_regex(r"\AREQ-[A-Z0-9]{1,12}-\d{4}\Z", fullmatch=True)


def _check(spec_text: str):
    return ReqIdFormat().check(parse_spec_file_text(spec_text, FAKE_PATH))


@settings(max_examples=50, deadline=None)
@given(req_id=_VALID_ID)
def test_valid_req_ids_produce_no_findings(req_id: str) -> None:
    """
    @test-id TEST-SPEC-0061
    @covers REQ-SPEC-0004
    """
    text = spec_file_text(req_block(req_id))
    findings = [f for f in _check(text) if f.rule_id == "req-id-format"]
    assert findings == []


@settings(max_examples=50, deadline=None)
@given(
    domain_upper=st.from_regex(r"\A[A-Z0-9]{1,12}\Z", fullmatch=True),
    number=st.integers(min_value=0, max_value=9999),
    swap_index=st.integers(min_value=0, max_value=20),
)
def test_lowercase_domain_always_flagged(
    domain_upper: str, number: int, swap_index: int
) -> None:
    """
    @test-id TEST-SPEC-0062
    @covers REQ-SPEC-0004

        Take a valid uppercase DOMAIN, lowercase one alphabetic position. The
        resulting REQ heading must be flagged. Numeric-only DOMAIN values
        (no alphabetic chars to lowercase) are skipped by the hypothesis
        assume(...).
    """
    # Find at least one alphabetic char to lowercase
    alpha_positions = [i for i, c in enumerate(domain_upper) if c.isalpha()]
    if not alpha_positions:
        return  # all-digit domain; no lowercase to apply
    pos = alpha_positions[swap_index % len(alpha_positions)]
    mutated = domain_upper[:pos] + domain_upper[pos].lower() + domain_upper[pos + 1 :]
    req_id = f"REQ-{mutated}-{number:04d}"
    text = spec_file_text(req_block(req_id))
    findings = [f for f in _check(text) if f.rule_id == "req-id-format"]
    assert findings, f"Expected ≥1 finding for {req_id!r}"


@settings(max_examples=50, deadline=None)
@given(
    domain=st.from_regex(r"\A[A-Z0-9]{1,12}\Z", fullmatch=True),
    width=st.integers(min_value=1, max_value=8).filter(lambda w: w != 4),
)
def test_wrong_number_width_always_flagged(domain: str, width: int) -> None:
    """
    @test-id TEST-SPEC-0063
    @covers REQ-SPEC-0004
    """
    number = "1" * width
    req_id = f"REQ-{domain}-{number}"
    text = spec_file_text(req_block(req_id))
    findings = [f for f in _check(text) if f.rule_id == "req-id-format"]
    assert findings, f"Expected ≥1 finding for {req_id!r}"


@settings(max_examples=50, deadline=None)
@given(
    extra_chars=st.text(alphabet=st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"), min_size=1, max_size=10),
    number=st.integers(min_value=0, max_value=9999),
)
def test_domain_over_12_chars_always_flagged(extra_chars: str, number: int) -> None:
    """
    @test-id TEST-SPEC-0064
    @covers REQ-SPEC-0004
    """
    domain = "ABCDEFGHIJKLM" + extra_chars  # 13+ chars guaranteed
    req_id = f"REQ-{domain}-{number:04d}"
    text = spec_file_text(req_block(req_id))
    findings = [f for f in _check(text) if f.rule_id == "req-id-format"]
    assert findings, f"Expected ≥1 finding for {req_id!r}"
