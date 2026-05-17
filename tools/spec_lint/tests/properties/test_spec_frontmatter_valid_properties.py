"""
Property-based tests for tools.spec_lint.rules.spec_frontmatter_valid.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import re

from hypothesis import given, settings, strategies as st

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.rules.spec_frontmatter_valid import SpecFrontmatterValid
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text

FAKE_PATH = "/fake/test.spec.md"

_REQUIRED_KEYS = (
    "id",
    "revision",
    "status",
    "introduced",
    "supersedes",
    "phase",
    "tier",
    "references",
)
_STATUS_VALUES = {"draft", "tests-red", "tests-green", "reviewed", "merged", "deprecated"}
_TIER_VALUES = {"unit", "integration", "e2e", "stochastic"}


def _check(spec_text: str):
    spec = parse_spec_file_text(spec_text, FAKE_PATH)
    return SpecFrontmatterValid().check(spec)


def _drop_key(block: str, key: str) -> str:
    """Remove a ``key: ...`` line from a frontmatter block (mapping or
    block-scalar value)."""
    out: list[str] = []
    in_block_value = False
    indent: int | None = None
    for line in block.splitlines():
        if in_block_value:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() == "" or (indent is not None and current_indent > indent):
                continue
            in_block_value = False
        m = re.match(rf"^( *){re.escape(key)}\s*:", line)
        if m:
            indent = len(m.group(1))
            in_block_value = True
            continue
        out.append(line)
    return "\n".join(out)


@settings(max_examples=20, deadline=None)
@given(key=st.sampled_from(_REQUIRED_KEYS))
def test_dropping_any_required_key_yields_a_named_finding(key: str) -> None:
    """
    @test-id TEST-SPEC-0065
    @covers REQ-SPEC-0005
    """
    block = req_block("REQ-AUTH-0001")
    mutated_block = _drop_key(block, key)
    text = spec_file_text(mutated_block)
    findings = [f for f in _check(text) if f.rule_id == "spec-frontmatter-valid"]
    assert findings, f"Expected ≥1 finding when dropping {key!r}"
    assert any(key in f.message for f in findings), (
        f"Expected message to name dropped key {key!r}; got {[f.message for f in findings]}"
    )


@settings(max_examples=30, deadline=None)
@given(bad_status=st.text(min_size=1, max_size=20).filter(lambda s: s not in _STATUS_VALUES and ":" not in s and "\n" not in s))
def test_invalid_status_enum_always_flagged(bad_status: str) -> None:
    """
    @test-id TEST-SPEC-0066
    @covers REQ-SPEC-0005
    """
    block = req_block("REQ-AUTH-0001", status=bad_status)
    text = spec_file_text(block)
    findings = [f for f in _check(text) if f.rule_id == "spec-frontmatter-valid"]
    assert findings, f"Expected ≥1 finding for status={bad_status!r}"


@settings(max_examples=30, deadline=None)
@given(bad_tier=st.text(min_size=1, max_size=20).filter(lambda s: s not in _TIER_VALUES and ":" not in s and "\n" not in s))
def test_invalid_tier_enum_always_flagged(bad_tier: str) -> None:
    """
    @test-id TEST-SPEC-0067
    @covers REQ-SPEC-0005
    """
    block = req_block("REQ-AUTH-0001", tier=bad_tier)
    text = spec_file_text(block)
    findings = [f for f in _check(text) if f.rule_id == "spec-frontmatter-valid"]
    assert findings, f"Expected ≥1 finding for tier={bad_tier!r}"


@settings(max_examples=20, deadline=None)
@given(bad_revision=st.integers(min_value=-100, max_value=0))
def test_non_positive_revision_always_flagged(bad_revision: int) -> None:
    """
    @test-id TEST-SPEC-0068
    @covers REQ-SPEC-0005
    """
    block = req_block("REQ-AUTH-0001", revision=bad_revision)
    text = spec_file_text(block)
    findings = [f for f in _check(text) if f.rule_id == "spec-frontmatter-valid"]
    assert findings, f"Expected ≥1 finding for revision={bad_revision}"
