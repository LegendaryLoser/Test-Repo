"""
Property-based tests for tools.spec_lint.rules.xref_resolves.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import pytest


def test_links_to_existing_files_never_flagged() -> None:
    """
    @test-id TEST-SPEC-0075
    Property: for any markdown file whose links all point at sibling files
    that exist on disk, the rule produces zero findings.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_links_to_missing_files_always_flagged() -> None:
    """
    @test-id TEST-SPEC-0076
    Property: for any markdown link target that does not exist anywhere on
    the filesystem under the source's parent, the rule produces ≥1 finding
    citing that target.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")


def test_http_links_are_always_skipped() -> None:
    """
    @test-id TEST-SPEC-0077
    Property: any link target beginning with http://, https://, mailto:,
    ftp://, or ftps:// produces no finding regardless of source path.
    """
    pytest.fail("RED: TASK-0012 stub — implemented in TASK-0013")
