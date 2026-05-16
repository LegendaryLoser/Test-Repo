"""Mutations targeting the ``xref-resolves`` rule.

Operates on (path, text) pairs. The driver materializes files in tmp_path
so resolution actually goes against the filesystem.

must-catch: broken md link; missing path in REQ-X@path; correct path but
missing REQ-ID at that path.
known-limitation: bare REQ-ID references with no ``@ path`` — out of scope
until a future ``xref-active`` rule.
"""

from __future__ import annotations

from ._models import Mutation

_RULE = "xref-resolves"


def _broken_md_link(text: str) -> str:
    return "See [missing](does_not_exist_NONEXISTENT_xyz.md).\n"


def _missing_path_in_req_ref(text: str) -> str:
    return "Affects REQ-AUTH-0001 @ openspec/specs/auth/NONEXISTENT_xyz.spec.md.\n"


def _wrong_id_at_path(text: str) -> str:
    # Driver guarantees a real spec at openspec/specs/auth/login.spec.md
    # containing REQ-AUTH-0001 only — refer to REQ-AUTH-9999 instead.
    return "Affects REQ-AUTH-9999 @ openspec/specs/auth/login.spec.md.\n"


def _bare_id_no_path(text: str) -> str:
    return "We touched REQ-AUTH-0001 today.\n"


MUTATIONS: list[Mutation] = [
    Mutation("XREF-MD-BROKEN", "markdown link to missing file", _RULE, _broken_md_link),
    Mutation("XREF-REQ-MISSING-PATH", "REQ@path with missing path", _RULE, _missing_path_in_req_ref),
    Mutation("XREF-REQ-WRONG-ID", "REQ@path with REQ-ID not at path", _RULE, _wrong_id_at_path),
    Mutation(
        "XREF-KL-BARE-ID",
        "bare REQ-ID without @ path (no active xref-active rule yet)",
        _RULE,
        _bare_id_no_path,
        category="known-limitation",
    ),
]
