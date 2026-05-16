"""Mutations targeting the ``prose-xref-banned`` rule.

Operates on (path, text) pairs. The seed is a clean doc; each mutation
injects a prose pattern that must be flagged.

must-catch: every denylist pattern in plain text.
known-limitation: novel prose patterns not in the denylist; this is open-
ended by design.
"""

from __future__ import annotations

from ._models import Mutation

_RULE = "prose-xref-banned"


def _set_text(text: str):
    return lambda _seed: text


MUTATIONS: list[Mutation] = [
    Mutation("PROSE-SPEC", "the X spec", _RULE, _set_text("We will update the auth spec.\n")),
    Mutation("PROSE-SPECS", "the X specs", _RULE, _set_text("We will update the auth specs.\n")),
    Mutation("PROSE-REQ", "the X requirement", _RULE, _set_text("The login requirement must change.\n")),
    Mutation("PROSE-REQS", "the X requirements", _RULE, _set_text("The login requirements must change.\n")),
    Mutation("PROSE-ADR", "the X ADR", _RULE, _set_text("Implements the testing ADR.\n")),
    Mutation("PROSE-EPIC", "the X epic", _RULE, _set_text("Adds to the auth epic.\n")),
    Mutation("PROSE-STORY", "the X story", _RULE, _set_text("Closes the login story.\n")),
    Mutation("PROSE-CHANGE", "the X change", _RULE, _set_text("Reverts the auth change.\n")),
    Mutation(
        "PROSE-MULTI",
        "two patterns on one line",
        _RULE,
        _set_text("Touches the auth spec and the login requirement.\n"),
    ),
    Mutation(
        "PROSE-KL-NOVEL",
        "novel pattern not in denylist",
        _RULE,
        _set_text("Refers to the authentication subsystem.\n"),
        category="known-limitation",
    ),
]
