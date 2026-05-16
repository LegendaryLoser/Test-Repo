"""Mutations targeting the ``anti-aliasing`` rule.

Anti-aliasing operates over the whole corpus, so its "mutations" produce
a CORPUS (list of two specs) where the second is a near-duplicate of the
first. The driver runs check_corpus over the resulting pair.

must-catch: char-4-gram-near-duplicates within the default 0.7 threshold.
known-limitation: paraphrase preserving meaning but with low overlap — that
needs LLM augmentation to catch.
"""

from __future__ import annotations

from ._models import Mutation

_RULE = "anti-aliasing"


def _identical(text: str) -> str:
    """Return a second spec identical to the first (different REQ-ID, same
    body). The driver knows to interpret the result as ``[seed, mutated]``."""
    return text.replace("REQ-AUTH-0001", "REQ-AUTH-0002", 1)


def _trailing_punct(text: str) -> str:
    out = _identical(text)
    # Append a period to the Description; n-gram overlap stays high.
    return out.replace("Single-assertion description.", "Single-assertion description..")


def _one_word_substitute(text: str) -> str:
    out = _identical(text)
    # Description swap: "Single-assertion" → "Single-axiom" (single-word edit)
    return out.replace("Single-assertion description.", "Single-axiom description.")


def _paraphrase(text: str) -> str:
    """Different wording, same meaning. Likely below the 0.7 Jaccard
    threshold — KNOWN LIMITATION of deterministic n-gram comparison."""
    out = _identical(text)
    return out.replace(
        "Single-assertion description.",
        "A solitary, isolated proposition forming the body.",
    ).replace(
        "Given X, when Y, then Z.",
        "Provided P holds, after Q transpires, R is observed.",
    )


MUTATIONS: list[Mutation] = [
    Mutation("AA-IDENTICAL", "byte-identical bodies, different IDs", _RULE, _identical),
    Mutation("AA-PUNCT", "trailing-punctuation-only difference", _RULE, _trailing_punct),
    Mutation("AA-ONEWORD", "single-word substitution", _RULE, _one_word_substitute),
    Mutation(
        "AA-KL-PARAPHRASE",
        "semantically equivalent paraphrase with low n-gram overlap",
        _RULE,
        _paraphrase,
        category="known-limitation",
    ),
]
