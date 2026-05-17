"""
Annotation discipline meta-test.

Enforces [`CLAUDE.md`](../../../CLAUDE.md) "How to add a test":

  The test must annotate `@test-id TEST-<DOMAIN>-<NNNN>` and
  `@covers REQ-<X>-<NNNN>[, ...]`.

Walks every ``test_*.py`` under ``tools/``, AST-parses each, enumerates
every ``def test_*`` function, and asserts each docstring contains both
annotations. Findings are reported as a sorted, line-anchored list so a
RED run pinpoints every violation in one go.

PHASE-1 / CHG-0030. Red in TASK-0027, green in TASK-0028 after the
92-test annotation backfill + REQ-SPEC-0004..0013 creation.
"""

from __future__ import annotations

import ast
import pathlib
import re


TOOLS_ROOT = pathlib.Path(__file__).resolve().parents[2]

_TEST_ID_RE = re.compile(r"@test-id\s+TEST-[A-Z][A-Z0-9_-]*-(?:\d+|NNN)")
_COVERS_REQ_RE = re.compile(r"@covers\s+REQ-[A-Z][A-Z0-9_]*-\d+")

def _discover_test_files() -> list[pathlib.Path]:
    out = []
    for p in sorted(TOOLS_ROOT.rglob("test_*.py")):
        if "__pycache__" in p.parts:
            continue
        out.append(p)
    return out


def _enumerate_tests(path: pathlib.Path):
    """Yield (lineno, func_name, docstring) for every def test_* in `path`."""
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            yield node.lineno, node.name, (ast.get_docstring(node) or "")


def _violations() -> list[str]:
    """Return sorted list of `file:line: function: missing-X` strings."""
    out: list[str] = []
    for path in _discover_test_files():
        rel = str(path.relative_to(TOOLS_ROOT)).replace("\\", "/")
        for lineno, name, doc in _enumerate_tests(path):
            missing = []
            if not _TEST_ID_RE.search(doc):
                missing.append("missing @test-id TEST-<DOMAIN>-<NNNN>")
            if not _COVERS_REQ_RE.search(doc):
                missing.append("missing @covers REQ-<X>-<NNNN>")
            for m in missing:
                out.append(f"{rel}:{lineno}: {name}: {m}")
    return sorted(out)


def test_every_test_has_id_and_covers() -> None:
    """
    @test-id TEST-SPEC-0099
    @covers REQ-SPEC-0013
    """
    violations = _violations()
    assert not violations, (
        f"\n{len(violations)} annotation violation(s) found "
        f"(see CLAUDE.md \"How to add a test\"):\n  "
        + "\n  ".join(violations)
    )
