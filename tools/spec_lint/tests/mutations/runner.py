"""Mutation runner."""

from __future__ import annotations

from typing import Callable

from ._models import Mutation


def run_mutation(
    seed: str, mutation: Mutation, rule_check: Callable[[str], list]
):
    """Apply ``mutation`` to ``seed``, run ``rule_check`` on the mutated
    text, return ``(mutated_text, findings)``."""
    mutated = mutation.apply(seed)
    findings = rule_check(mutated)
    return mutated, findings


def assert_caught(mutation: Mutation, findings: list) -> None:
    """Raise ``AssertionError`` if no finding from
    ``mutation.expected_rule_id`` is present in ``findings``. Used to gate
    must-catch mutations in CI."""
    matching = [
        f for f in findings if getattr(f, "rule_id", None) == mutation.expected_rule_id
    ]
    assert matching, (
        f"Mutation {mutation.id} ({mutation.description}) was NOT caught by "
        f"rule {mutation.expected_rule_id}. "
        f"Findings produced: {findings!r}. "
        f"This is a false-negative gap: either tighten the rule (preferred) "
        f"or reclassify the mutation to known-limitation with a documented "
        f"rationale."
    )
