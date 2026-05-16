"""
PHASE-0 verification tests.

Each test corresponds to one REQ-ARCH-NNNN clause in
openspec/architecture/ARCHITECTURE.md §10. Tests are RED in this commit
(TASK-0001); TASK-0002 replaces every pytest.fail with real assertions.

Annotations below are parsed by tools/trace (PHASE-2). For now they are
documentary.
"""

from __future__ import annotations

import pathlib

import pytest


def test_arch_0001_top_level_layout(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0001
    @covers REQ-ARCH-0001
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0002_architecture_artifacts_present(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0002
    @covers REQ-ARCH-0002
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0003_empty_product_templates(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0003
    @covers REQ-ARCH-0003
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0004_specs_index_parses(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0004
    @covers REQ-ARCH-0004
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0005_architecture_xrefs_resolve(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0005
    @covers REQ-ARCH-0005
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0006_no_executable_code_in_architecture(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0006
    @covers REQ-ARCH-0006
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0007_claude_md_principles_verbatim(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0007
    @covers REQ-ARCH-0007
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")


def test_arch_0008_settings_declares_all_hooks(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0008
    @covers REQ-ARCH-0008
    """
    pytest.fail("RED: TASK-0001 — assertion not yet authored, see TASK-0002")
