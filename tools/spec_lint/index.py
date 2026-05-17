"""
INDEX.yaml builder.

Walks `openspec/specs/` for `*.spec.md`, parses each, and emits a
deterministic YAML index per the schema in INDEX.yaml's header.

Per [`ADR-0004` §6](../../openspec/architecture/decisions/ADR-0004-spec-storage-discipline.md),
INDEX.yaml is the "sole retrieval surface for tooling" — once populated
(CHG-0014) it becomes the substrate for PHASE-2's matrix builder and
gates.

Skeleton — TASK-0031 RED. Real implementation lands in TASK-0032.
"""

from __future__ import annotations

import pathlib


def build_index_data(
    specs_root: pathlib.Path,
    repo_root: pathlib.Path,
) -> dict:
    raise NotImplementedError("CHG-0014 TASK-0032 will implement build_index_data")


def write_index(
    specs_root: pathlib.Path,
    repo_root: pathlib.Path,
    target: pathlib.Path,
) -> None:
    raise NotImplementedError("CHG-0014 TASK-0032 will implement write_index")


def check_index(
    specs_root: pathlib.Path,
    repo_root: pathlib.Path,
    target: pathlib.Path,
) -> int:
    raise NotImplementedError("CHG-0014 TASK-0032 will implement check_index")
