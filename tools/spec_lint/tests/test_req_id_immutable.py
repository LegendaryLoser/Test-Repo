"""
Tests for tools.spec_lint.rules.req_id_immutable.

PHASE-1 / CHG-0004. Red in TASK-0006, green in TASK-0007.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.git_history import historical_versions
from tools.spec_lint.rules.req_id_immutable import ReqIdImmutable
from tools.spec_lint.tests.history_helpers import (
    make_repo_with_history,
    req_block,
    spec_file_text,
)


SPEC_REL = "openspec/specs/auth/login.spec.md"


def _check(repo: pathlib.Path, file_rel: str = SPEC_REL):
    versions = list(historical_versions(repo, file_rel))
    return ReqIdImmutable().check_history(versions)


def test_unchanged_history_produces_no_findings(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0017

    Three commits, same REQ-ID throughout. Even with body/status changes,
    nothing disappeared.
    """
    v1 = spec_file_text(req_block("REQ-AUTH-0001", status="draft"))
    v2 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-red"))
    v3 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-green"))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2, v3])
    assert _check(repo) == []


def test_deprecation_in_place_produces_no_findings(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0018

    REQ remains in the file with status: deprecated — the legal lifecycle.
    """
    v1 = spec_file_text(req_block("REQ-AUTH-0001", status="tests-green"))
    v2 = spec_file_text(
        req_block("REQ-AUTH-0001", status="deprecated"),
        req_block("REQ-AUTH-0002", status="draft", supersedes="REQ-AUTH-0001"),
    )
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])
    assert _check(repo) == []


def test_removal_produces_a_finding(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0019

    REQ disappears entirely between two commits — the failure mode this rule
    exists to catch.
    """
    v1 = spec_file_text(req_block("REQ-AUTH-0001"))
    v2 = spec_file_text(req_block("REQ-AUTH-0002"))  # 0001 vanished
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])

    findings = _check(repo)
    rule_findings = [f for f in findings if f.rule_id == "req-id-immutable"]
    assert rule_findings, f"Expected ≥1 req-id-immutable finding, got {findings}"
    # The message must name the disappeared REQ-ID so investigators can act.
    assert any("REQ-AUTH-0001" in f.message for f in rule_findings)


def test_rename_appears_as_removal(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0020

    "Rename" is just `add new ID + remove old ID` from this rule's point
    of view. ADR-0004 §1 forbids it; supersession (which keeps the old REQ
    in the file as deprecated) is the only path.
    """
    body = "Same content in both commits."
    v1 = spec_file_text(req_block("REQ-AUTH-0001", description=body))
    v2 = spec_file_text(req_block("REQ-AUTH-0002", description=body))
    repo = make_repo_with_history(tmp_path, SPEC_REL, [v1, v2])

    findings = _check(repo)
    rule_findings = [f for f in findings if f.rule_id == "req-id-immutable"]
    assert any("REQ-AUTH-0001" in f.message for f in rule_findings)


def test_rule_id_and_description_are_stable() -> None:
    """
    @test-id TEST-SPEC-0021
    """
    r = ReqIdImmutable()
    assert r.id == "req-id-immutable"
    assert "ADR-0004" in r.description
