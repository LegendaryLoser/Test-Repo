"""
Tests for tools.spec_lint.rules.prose_xref_banned.

Pure inline-text tests — the rule never dereferences paths, so a synthetic
pathlib.Path is enough.

PHASE-1 / CHG-0005. Red in TASK-0008, green in TASK-0009.
"""

from __future__ import annotations

import pathlib
import textwrap

import pytest

from tools.spec_lint.rules.prose_xref_banned import ProseXrefBanned


FAKE_PATH = pathlib.Path("/fake/openspec/changes/CHG-XXXX/proposal.md")


def _check(text: str):
    return ProseXrefBanned().check_files([(FAKE_PATH, text)])


def test_clean_text_with_ids_passes() -> None:
    """
    @test-id TEST-SPEC-0028
    @covers REQ-SPEC-0007
    """
    text = textwrap.dedent(
        """\
        # Change proposal

        Touches REQ-AUTH-0001 @ openspec/specs/auth/login.spec.md and
        ADR-0004 @ openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md.
        """
    )
    assert _check(text) == []


def test_prose_the_X_spec_is_flagged() -> None:
    """
    @test-id TEST-SPEC-0029
    @covers REQ-SPEC-0007
    """
    text = "We will update the auth spec to include OAuth.\n"
    findings = _check(text)
    rule_findings = [f for f in findings if f.rule_id == "prose-xref-banned"]
    assert rule_findings
    assert all(f.line == 1 for f in rule_findings)


def test_prose_the_X_requirement_is_flagged() -> None:
    """
    @test-id TEST-SPEC-0030
    @covers REQ-SPEC-0007
    """
    text = "The login requirement must change.\n"
    assert [f for f in _check(text) if f.rule_id == "prose-xref-banned"]


def test_prose_the_X_ADR_is_flagged() -> None:
    """
    @test-id TEST-SPEC-0031
    @covers REQ-SPEC-0007
    """
    text = "Implements the testing ADR.\n"
    assert [f for f in _check(text) if f.rule_id == "prose-xref-banned"]


def test_code_blocks_are_excluded() -> None:
    """
    @test-id TEST-SPEC-0032
    @covers REQ-SPEC-0007

        Prose patterns inside fenced code blocks are documentation of the rule
        or examples, not actual references — they must not be flagged.
    """
    text = textwrap.dedent(
        """\
        # ADR-0004 example

        Prose references like:
        ```
        the auth spec
        the login requirement
        ```
        are forbidden in real documents.
        """
    )
    assert _check(text) == []


def test_inline_allow_marker_skips_the_line() -> None:
    """
    @test-id TEST-SPEC-0033
    @covers REQ-SPEC-0007
    """
    text = (
        "We discuss the auth spec here intentionally. "
        "<!-- spec-lint: allow prose-xref-banned -->\n"
    )
    assert _check(text) == []


def test_pattern_followed_by_id_on_same_line_is_allowed() -> None:
    """
    @test-id TEST-SPEC-0034
    @covers REQ-SPEC-0007

        A prose-like phrase that is immediately disambiguated by a stable ID
        on the same line is treated as parenthetical and skipped.
    """
    text = (
        "Touches the auth spec REQ-AUTH-0001 @ openspec/specs/auth/login.spec.md.\n"
    )
    assert _check(text) == []


def test_multiple_files_each_attribute_their_findings() -> None:
    """
    @test-id TEST-SPEC-0035
    @covers REQ-SPEC-0007
    """
    p1 = pathlib.Path("/fake/a.md")
    p2 = pathlib.Path("/fake/b.md")
    files = [
        (p1, "the auth spec\n"),
        (p2, "clean text with REQ-AUTH-0001.\n"),
    ]
    findings = ProseXrefBanned().check_files(files)
    rule_findings = [f for f in findings if f.rule_id == "prose-xref-banned"]
    assert len(rule_findings) == 1
    assert rule_findings[0].file == str(p1)


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0036
    @covers REQ-SPEC-0007
    """
    r = ProseXrefBanned()
    assert r.id == "prose-xref-banned"
    assert "ADR-0004" in r.description
