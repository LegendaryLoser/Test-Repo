"""
Markdown report generator for dry-run results.

PHASE-1 / CHG-0009 / TASK-0017 — RED stub. TASK-0018 implements.
"""

from __future__ import annotations

from .runner import DryRunResult


def render_report(result: DryRunResult, head_sha: str = "unknown") -> str:
    """Render a markdown report summarising a dry-run.

    The report includes:
    - run metadata (rules commit SHA, total runtime)
    - per-corpus section with finding counts per rule
    - top-N findings per rule (file:line + message)
    - uncertain-zone summary per rule
    """
    raise NotImplementedError(
        "render_report: TASK-0017 RED stub — implemented in TASK-0018"
    )
