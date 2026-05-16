"""
Tests for tools.spec_lint.rules.req_append_only.

PHASE-1 / CHG-0004. Red in TASK-0006, green in TASK-0007.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.git_history import historical_versions
from tools.spec_lint.rules.req_append_only import ReqAppendOnly
from tools.spec_lint.tests.history_helpers import (
    make_repo_with_history,
    req_block,
    spec_file_text,
)


SPEC_REL = "openspec/specs/auth/login.spec.md"


def _check(repo: pathlib.Path, file_rel: str = SPEC_REL):
    versions = list(historical_versions(repo, file_rel))
    return ReqAppendOnly().check_history(versions)


def test_never_green_allows_body_changes(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0022

    REQ never reached tests-green. Editing the body is allowed freely.
    """
    v1 = spec_file_text(req_block("REQ-AUTH-0001", status="draft", description="First."))
    v2 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-red", description="Rewritten.")
    )
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])
    assert _check(repo) == []


def test_frozen_after_green_produces_no_findings(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0023

    REQ went green and no subsequent edits to body. Compliant.
    """
    body = "Frozen description."
    v1 = spec_file_text(req_block("REQ-AUTH-0001", status="draft", description=body))
    v2 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-red", description=body))
    v3 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-green", description=body))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2, v3])
    assert _check(repo) == []


def test_revision_bump_allows_body_change(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0024

    Once green, a body change is permitted IF revision bumps. PHASE-1
    simplification: any bump is accepted regardless of magnitude.
    """
    v1 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-green", revision=1, description="First.")
    )
    v2 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-green", revision=2, description="Reworded.")
    )
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])
    assert _check(repo) == []


def test_silent_body_edit_after_green_produces_finding(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0025

    REQ went green at revision 1; subsequent commit changed body without
    bumping revision. The failure mode this rule exists to catch.
    """
    v1 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-green", revision=1, description="First.")
    )
    v2 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-green", revision=1, description="Edited silently.")
    )
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])

    findings = _check(repo)
    rule_findings = [f for f in findings if f.rule_id == "req-append-only"]
    assert rule_findings, f"Expected ≥1 req-append-only finding, got {findings}"
    assert any("REQ-AUTH-0001" in f.message for f in rule_findings)


def test_acceptance_edit_after_green_also_flagged(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0026

    ADR-0004 §7 freezes both Description and Acceptance. Body change in
    Acceptance counts.
    """
    v1 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-green", revision=1, acceptance="Given A.")
    )
    v2 = spec_file_text(
        req_block("REQ-AUTH-0001", status="tests-green", revision=1, acceptance="Given B.")
    )
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])

    findings = _check(repo)
    assert [f for f in findings if f.rule_id == "req-append-only"]


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0027
    """
    r = ReqAppendOnly()
    assert r.id == "req-append-only"
    assert "ADR-0004" in r.description
