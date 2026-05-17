"""
CI workflow wiring meta-test.

Asserts that ``.github/workflows/ci.yml``'s ``spec-lint`` job actually
invokes the spec_lint CLI + pytest, rather than the PHASE-0 placeholder
``echo "TODO PHASE-1..."; exit 0`` step.

PHASE-1 / CHG-0013. Red in TASK-0029, green in TASK-0030.
"""

from __future__ import annotations

import pathlib
import re

import yaml


REPO = pathlib.Path(__file__).resolve().parents[3]
CI_YML = REPO / ".github" / "workflows" / "ci.yml"

_PLACEHOLDER_RE = re.compile(r"TODO\s+PHASE-1")
_VALIDATE_RE = re.compile(r"python\s+-m\s+tools\.spec_lint\s+validate")
_CHECK_LAYOUT_RE = re.compile(r"python\s+-m\s+tools\.spec_lint\s+check-layout")
_PYTEST_RE = re.compile(r"\bpytest\b")
_PIP_INSTALL_RE = re.compile(r"pip\s+install")
_SETUP_PYTHON_RE = re.compile(r"actions/setup-python")


def _load_workflow():
    return yaml.safe_load(CI_YML.read_text())


def _spec_lint_steps() -> list[dict]:
    wf = _load_workflow()
    jobs = wf.get("jobs", {})
    spec_lint = jobs.get("spec-lint")
    assert spec_lint is not None, "spec-lint job missing from ci.yml"
    return spec_lint.get("steps", [])


def _run_commands(steps: list[dict]) -> list[str]:
    """Collect every step's ``run:`` field as a single string per step."""
    out: list[str] = []
    for step in steps:
        run = step.get("run")
        if isinstance(run, str):
            out.append(run)
    return out


def _uses(steps: list[dict]) -> list[str]:
    """Collect every step's ``uses:`` field."""
    out: list[str] = []
    for step in steps:
        u = step.get("uses")
        if isinstance(u, str):
            out.append(u)
    return out


def test_spec_lint_job_invokes_real_gates() -> None:
    """
    @test-id TEST-SPEC-0100
    @covers REQ-SPEC-0014
    """
    # Workflow file present + parseable.
    assert CI_YML.is_file(), f"{CI_YML} not found"
    wf = _load_workflow()
    assert isinstance(wf, dict), "ci.yml did not parse to a mapping"

    # Trigger contract.
    # PyYAML parses unquoted ``on:`` as boolean True in some contexts.
    on = wf.get("on") or wf.get(True)
    assert on is not None, "ci.yml has no `on:` trigger block"
    assert "pull_request" in on, "spec-lint must run on pull_request"
    assert "push" in on, "spec-lint must run on push (master/main)"

    steps = _spec_lint_steps()
    assert steps, "spec-lint job has no steps"

    runs = _run_commands(steps)
    uses = _uses(steps)
    all_run_text = "\n".join(runs)

    # No placeholder.
    placeholders = [r for r in runs if _PLACEHOLDER_RE.search(r)]
    assert not placeholders, (
        f"spec-lint job still has TODO PHASE-1 placeholder run step(s):\n  "
        + "\n  ".join(placeholders)
    )

    # Structural steps present.
    assert any("actions/checkout" in u for u in uses), \
        "spec-lint job missing actions/checkout step"
    assert any(_SETUP_PYTHON_RE.search(u) for u in uses), \
        "spec-lint job missing actions/setup-python step"

    # Real invocations present.
    missing = []
    if not _PIP_INSTALL_RE.search(all_run_text):
        missing.append("pip install (dependency install step)")
    if not _VALIDATE_RE.search(all_run_text):
        missing.append("python -m tools.spec_lint validate")
    if not _CHECK_LAYOUT_RE.search(all_run_text):
        missing.append("python -m tools.spec_lint check-layout")
    if not _PYTEST_RE.search(all_run_text):
        missing.append("pytest")
    assert not missing, (
        "spec-lint job missing the following gate invocations:\n  - "
        + "\n  - ".join(missing)
    )
