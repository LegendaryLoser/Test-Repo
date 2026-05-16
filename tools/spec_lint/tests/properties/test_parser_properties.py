"""
Property-based tests for tools.spec_lint.parser.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

from hypothesis import given, settings, strategies as st

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text

FAKE_PATH = "/fake/openspec/specs/test.spec.md"

# Strategy: a single well-formed REQ-ID per ADR-0004 §1.
_REQ_ID = st.from_regex(r"\AREQ-[A-Z0-9]{1,12}-\d{4}\Z", fullmatch=True)


@settings(max_examples=50, deadline=None)
@given(req_ids=st.lists(_REQ_ID, min_size=1, max_size=5, unique=True))
def test_parser_extracts_every_well_formed_req_heading(req_ids: list[str]) -> None:
    """
    @test-id TEST-SPEC-0058
    """
    text = spec_file_text(*(req_block(rid) for rid in req_ids))
    spec = parse_spec_file_text(text, FAKE_PATH)
    assert [r.heading_id for r in spec.requirements] == req_ids


@settings(max_examples=50, deadline=None)
@given(req_ids=st.lists(_REQ_ID, min_size=1, max_size=3, unique=True))
def test_parser_round_trip_preserves_heading_ids(req_ids: list[str]) -> None:
    """
    @test-id TEST-SPEC-0059
    """
    text1 = spec_file_text(*(req_block(rid) for rid in req_ids))
    ids1 = [r.heading_id for r in parse_spec_file_text(text1, FAKE_PATH).requirements]
    text2 = spec_file_text(*(req_block(rid) for rid in ids1))
    ids2 = [r.heading_id for r in parse_spec_file_text(text2, FAKE_PATH).requirements]
    assert ids1 == ids2


@settings(max_examples=50, deadline=None)
@given(req_ids=st.lists(_REQ_ID, min_size=0, max_size=5, unique=True))
def test_parser_is_deterministic(req_ids: list[str]) -> None:
    """
    @test-id TEST-SPEC-0060
    """
    text = spec_file_text(*(req_block(rid) for rid in req_ids)) if req_ids else "# empty\n"
    a = parse_spec_file_text(text, FAKE_PATH)
    b = parse_spec_file_text(text, FAKE_PATH)
    assert [r.heading_id for r in a.requirements] == [r.heading_id for r in b.requirements]
    assert [r.frontmatter for r in a.requirements] == [r.frontmatter for r in b.requirements]
