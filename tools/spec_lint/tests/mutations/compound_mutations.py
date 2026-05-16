"""Mutations targeting the ``compound-requirement-detector`` rule.

must-catch: N>1 G/W/T bullets in Acceptance.
known-limitation: prose-only compound REQs (single G/W/T but with "and X
and Y" inside Description) — these need NLP/LLM augmentation to detect.
"""

from __future__ import annotations

from ._models import Mutation

_RULE = "compound-requirement-detector"


def _replace_acceptance(text: str, new_acceptance_body: str) -> str:
    """Replace the body under `### Acceptance` (up to next ### or EOF)."""
    lines = text.splitlines()
    out: list[str] = []
    skipping = False
    for line in lines:
        if skipping:
            if line.startswith("### "):
                out.extend(new_acceptance_body.splitlines())
                out.append("")
                out.append(line)
                skipping = False
                continue
            continue
        if line.strip() == "### Acceptance":
            out.append(line)
            skipping = True
            continue
        out.append(line)
    if skipping:
        # Acceptance was the last section — append the new body.
        out.extend(new_acceptance_body.splitlines())
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def _set_n_bullets(n: int, given_word: str = "Given"):
    body = "\n".join(f"- {given_word} A, when X, then Z{i}." for i in range(n))
    return lambda text: _replace_acceptance(text, body)


MUTATIONS: list[Mutation] = [
    Mutation("COMP-N2", "two G/W/T bullets", _RULE, _set_n_bullets(2)),
    Mutation("COMP-N3", "three G/W/T bullets", _RULE, _set_n_bullets(3)),
    Mutation("COMP-N5", "five G/W/T bullets", _RULE, _set_n_bullets(5)),
    Mutation("COMP-N10", "ten G/W/T bullets", _RULE, _set_n_bullets(10)),
    Mutation("COMP-CASE-UPPER", "two GIVEN bullets all caps", _RULE, _set_n_bullets(2, "GIVEN")),
    Mutation("COMP-CASE-MIXED", "two GiVeN bullets mixed case", _RULE, _set_n_bullets(2, "GiVeN")),
    Mutation(
        "COMP-NOBULLET",
        "two unbulleted Given lines",
        _RULE,
        lambda text: _replace_acceptance(text, "Given A, when X, then Z1.\nGiven B, when X, then Z2."),
    ),
    # --- Known limitations ---
    Mutation(
        "COMP-KL-PROSE-AND",
        "prose-only compound ('do A and B') with single G/W/T",
        _RULE,
        lambda text: _replace_acceptance(
            text, "- Given X, when Y, then the system does A and B."
        ),
        category="known-limitation",
    ),
    Mutation(
        "COMP-KL-NO-GIVEN-PREFIX",
        "When/Then bullets without Given prefix",
        _RULE,
        lambda text: _replace_acceptance(
            text, "- When X, then Y.\n- When P, then Q."
        ),
        category="known-limitation",
    ),
]
