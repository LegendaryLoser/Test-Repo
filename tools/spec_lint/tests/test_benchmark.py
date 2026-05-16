"""
Tests for the benchmark harness.

PHASE-1 / CHG-0009. Red in TASK-0017, green in TASK-0018.

These tests pin STRUCTURAL invariants (loader returns the right shape,
runner aggregates without crashing, report renders to non-empty markdown).
They do NOT pin specific finding counts — those drift as rules and corpora
evolve, and pinning them would couple the tests to incidental tuning.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.benchmark.loaders import (
    load_openspec_docs,
    load_promise_arff,
)
from tools.spec_lint.benchmark.report import render_report
from tools.spec_lint.benchmark.runner import (
    CorpusResult,
    DryRunResult,
    run_dry_run,
)


CORPORA_ROOT = (
    pathlib.Path(__file__).resolve().parent.parent / "benchmark" / "corpora"
)


def test_openspec_loader_returns_all_md_files() -> None:
    """
    @test-id TEST-SPEC-BENCH-0001
    """
    docs_dir = CORPORA_ROOT / "openspec_docs"
    pairs = load_openspec_docs(docs_dir)
    # 11 user-facing docs + LICENSE/MANIFEST excluded.
    assert len(pairs) >= 10, f"Expected ≥10 md files, got {len(pairs)}"
    assert all(p.suffix == ".md" for p, _ in pairs)
    assert all(text for _, text in pairs)
    # Exclusions: MANIFEST and LICENSE must not appear.
    names = {p.name for p, _ in pairs}
    assert "MANIFEST.md" not in names
    assert "LICENSE" not in names


def test_promise_loader_extracts_all_requirements() -> None:
    """
    @test-id TEST-SPEC-BENCH-0002

    PROMISE_exp has 969 requirements (444 FR + 525 NFR).
    """
    arff = CORPORA_ROOT / "promise_nfr" / "PROMISE_exp.arff"
    specs = load_promise_arff(arff)
    assert 900 <= len(specs) <= 1000, f"Unexpected count: {len(specs)}"
    for s in specs:
        assert len(s.requirements) == 1
        req = s.requirements[0]
        assert req.heading_id.startswith("REQ-PRMS-")
        assert req.frontmatter is not None
        assert req.body  # non-empty


def test_run_dry_run_returns_results_for_both_corpora() -> None:
    """
    @test-id TEST-SPEC-BENCH-0003
    """
    result = run_dry_run(CORPORA_ROOT)
    assert isinstance(result, DryRunResult)
    assert len(result.corpora) == 2
    names = {c.name for c in result.corpora}
    assert names == {"openspec_docs", "promise_nfr"}
    for c in result.corpora:
        assert c.items_loaded > 0
        assert isinstance(c.findings_by_rule, dict)
        assert isinstance(c.uncertain_by_rule, dict)


def test_render_report_produces_nonempty_markdown() -> None:
    """
    @test-id TEST-SPEC-BENCH-0004
    """
    result = run_dry_run(CORPORA_ROOT)
    md = render_report(result, head_sha="abc1234")
    assert isinstance(md, str)
    assert len(md) > 200
    # Must mention each corpus name and the head sha.
    assert "openspec_docs" in md
    assert "promise_nfr" in md
    assert "abc1234" in md
    # Must look like markdown.
    assert md.startswith("#") or md.startswith("# ")
