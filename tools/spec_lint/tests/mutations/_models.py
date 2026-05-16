"""Mutation framework data model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Mutation:
    """A targeted fault injection.

    ``id`` is unique across all mutations in the corpus.
    ``apply`` takes a seed input (the form depends on the rule:
    spec markdown text, or a (path, text) pair) and returns the mutated
    input in the same shape.
    ``category`` is "must-catch" (gates CI) or "known-limitation"
    (logged only).
    """

    id: str
    description: str
    expected_rule_id: str
    apply: Callable[[str], str]
    category: str = "must-catch"
