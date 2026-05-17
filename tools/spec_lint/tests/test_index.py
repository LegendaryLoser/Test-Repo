"""
Tests for tools.spec_lint.index — the INDEX.yaml builder.

PHASE-1 / CHG-0014. Red in TASK-0031 (skeletons raise NotImplementedError),
green in TASK-0032.
"""

from __future__ import annotations

import pathlib
import textwrap

import pytest
import yaml

from tools.spec_lint.index import build_index_data, check_index, write_index


REPO = pathlib.Path(__file__).resolve().parents[3]
REAL_SPECS = REPO / "openspec" / "specs"
REAL_INDEX = REAL_SPECS / "INDEX.yaml"


def _write_spec(root: pathlib.Path, rel: str, content: str) -> pathlib.Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def _minimal_req(req_id: str, *, status: str = "tests-green") -> str:
    return textwrap.dedent(f"""\
        # Fixture spec

        ## {req_id}
        ---
        id: {req_id}
        revision: 1
        status: {status}
        introduced: CHG-0001
        supersedes: null
        phase: PHASE-1
        tier: unit
        references:
          epic: null
          story: null
          adrs: [ADR-0004]
        ---

        ### Description
        Fixture body.

        ### Acceptance
        - Given X, when Y, then Z.
        """)


def test_build_index_includes_known_req_from_tmp(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0101
    @covers REQ-SPEC-0015
    """
    specs_root = tmp_path / "openspec" / "specs"
    _write_spec(specs_root, "demo/feature.spec.md", _minimal_req("REQ-DEMO-0001"))
    data = build_index_data(specs_root, tmp_path)

    assert data["version"] == 1
    assert isinstance(data.get("generated_at"), str)
    assert len(data["requirements"]) == 1
    entry = data["requirements"][0]
    assert entry["id"] == "REQ-DEMO-0001"
    assert entry["file"].endswith("demo/feature.spec.md")
    assert entry["revision"] == 1
    assert entry["status"] == "tests-green"
    assert entry["phase"] == "PHASE-1"
    assert entry["tier"] == "unit"


def test_build_index_real_repo_contains_all_req_spec_entries() -> None:
    """
    @test-id TEST-SPEC-0102
    @covers REQ-SPEC-0015
    """
    data = build_index_data(REAL_SPECS, REPO)
    ids = sorted(e["id"] for e in data["requirements"])
    # Today: REQ-SPEC-0001..0014 (REQ-ARCH-* live in ARCHITECTURE.md §10 as
    # bullet points and will be migrated by CHG-0015 to proper spec format).
    expected_min = {f"REQ-SPEC-{n:04d}" for n in range(1, 15)}
    missing = expected_min - set(ids)
    assert not missing, (
        f"INDEX should contain all 14 REQ-SPEC entries; missing: {sorted(missing)}"
    )


def test_check_detects_planted_stale_index(tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-0103
    @covers REQ-SPEC-0015
    """
    specs_root = tmp_path / "openspec" / "specs"
    _write_spec(specs_root, "demo/a.spec.md", _minimal_req("REQ-DEMO-0001"))

    # Write a deliberately-wrong INDEX (claims a DIFFERENT REQ exists).
    target = specs_root / "INDEX.yaml"
    target.write_text(yaml.safe_dump({
        "version": 1,
        "generated_at": "2026-01-01T00:00:00Z",
        "requirements": [
            {
                "id": "REQ-DEMO-9999",
                "file": "openspec/specs/demo/never.spec.md",
                "revision": 1,
                "status": "tests-green",
                "tier": "unit",
                "phase": "PHASE-1",
                "supersedes": None,
                "superseded_by": None,
            }
        ],
    }, sort_keys=False))

    result = check_index(specs_root, tmp_path, target)
    assert result != 0, f"expected non-zero for stale INDEX, got {result}"


def test_check_real_repo_index_is_up_to_date() -> None:
    """
    @test-id TEST-SPEC-0104
    @covers REQ-SPEC-0015

    This is the ultimate green target: the real repo's INDEX.yaml is
    consistent with what build_index_data would produce. Fails in RED
    because the skeleton raises NotImplementedError; fails just after
    GREEN's implementation lands but BEFORE INDEX.yaml is regenerated;
    passes once both arrive in the same commit.
    """
    result = check_index(REAL_SPECS, REPO, REAL_INDEX)
    assert result == 0, (
        f"INDEX.yaml is stale (check_index returned {result}); "
        f"regenerate with `python -m tools.spec_lint index`"
    )
