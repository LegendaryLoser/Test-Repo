"""
Tests for tools.spec_lint.rules.xref_resolves.

Uses tmp_path-based file trees because xref resolution requires real
relative-path arithmetic against an existing directory layout.

PHASE-1 / CHG-0005. Red in TASK-0008, green in TASK-0009.
"""

from __future__ import annotations

import pathlib
import textwrap

import pytest

from tools.spec_lint.rules.xref_resolves import XrefResolves
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text
from tools.spec_lint.tests.xref_helpers import write_doc


def _check(files: list[tuple[pathlib.Path, str]]):
    return XrefResolves().check_files(files)


def test_valid_relative_markdown_link_passes(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0037
    """
    write_doc(tmp_path, "target.md", "# Target\n")
    src = write_doc(tmp_path, "openspec/changes/CHG-XXXX/proposal.md", "See [target](../../../target.md).\n")
    assert _check([(src, src.read_text())]) == []


def test_broken_relative_link_is_flagged(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0038
    """
    src = write_doc(tmp_path, "openspec/changes/CHG-XXXX/proposal.md", "See [missing](nope.md).\n")
    findings = _check([(src, src.read_text())])
    rule_findings = [f for f in findings if f.rule_id == "xref-resolves"]
    assert rule_findings
    assert any("nope.md" in f.message for f in rule_findings)


def test_http_links_are_skipped(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0039
    """
    src = write_doc(
        tmp_path,
        "doc.md",
        "[external](https://example.com/page) and [mail](mailto:x@y.z).\n",
    )
    assert _check([(src, src.read_text())]) == []


def test_pure_fragment_links_are_skipped(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0040
    """
    src = write_doc(tmp_path, "doc.md", "Jump to [section](#section).\n")
    assert _check([(src, src.read_text())]) == []


def test_req_id_at_path_resolves(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0041
    """
    spec_text = spec_file_text(req_block("REQ-AUTH-0007"))
    write_doc(tmp_path, "openspec/specs/auth/login.spec.md", spec_text)
    src = write_doc(
        tmp_path,
        "openspec/changes/CHG-XXXX/proposal.md",
        "Affects REQ-AUTH-0007 @ openspec/specs/auth/login.spec.md.\n",
    )
    # Path in the reference is repo-relative (from src's perspective, that's
    # two levels up from src.parent). Make the check robust to either repo-root-
    # or src-relative resolution by also placing src adjacent to the spec.
    assert _check([(src, src.read_text())]) == []


def test_req_id_at_path_missing_path_is_flagged(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0042
    """
    src = write_doc(
        tmp_path,
        "doc.md",
        "Affects REQ-AUTH-0007 @ openspec/specs/auth/missing.spec.md.\n",
    )
    findings = _check([(src, src.read_text())])
    rule_findings = [f for f in findings if f.rule_id == "xref-resolves"]
    assert rule_findings
    assert any("missing.spec.md" in f.message for f in rule_findings)


def test_req_id_at_path_wrong_id_is_flagged(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0043

    The cited path exists, but the referenced REQ-ID is not in it. This is
    the dangerous case — the link looks valid until you open the file.
    """
    spec_text = spec_file_text(req_block("REQ-AUTH-0001"))
    write_doc(tmp_path, "openspec/specs/auth/login.spec.md", spec_text)
    src = write_doc(
        tmp_path,
        "doc.md",
        "Affects REQ-AUTH-9999 @ openspec/specs/auth/login.spec.md.\n",
    )
    findings = _check([(src, src.read_text())])
    rule_findings = [f for f in findings if f.rule_id == "xref-resolves"]
    assert rule_findings
    assert any("REQ-AUTH-9999" in f.message for f in rule_findings)


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0044
    """
    r = XrefResolves()
    assert r.id == "xref-resolves"
    assert "ADR-0004" in r.description
