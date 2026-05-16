"""
Mutation runner.

PHASE-1 / CHG-0008 / TASK-0014 — RED stub. TASK-0015 implements.
"""

from __future__ import annotations

from ._models import Mutation


def run_mutation(seed: str, mutation: Mutation, rule_check):
    """Apply the mutation to the seed, run ``rule_check`` on the mutated
    input, return (mutated_text, findings).

    ``rule_check`` is a callable that accepts the mutated text and returns
    a list[Finding]. The caller is responsible for setting up the parsing
    and rule invocation appropriate for the rule under test.
    """
    raise NotImplementedError(
        "run_mutation: TASK-0014 RED stub — implemented in TASK-0015"
    )


def assert_caught(mutation: Mutation, findings) -> None:
    """Raise AssertionError if no finding from ``mutation.expected_rule_id``
    is present in ``findings``."""
    raise NotImplementedError(
        "assert_caught: TASK-0014 RED stub — implemented in TASK-0015"
    )
