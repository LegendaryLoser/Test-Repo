"""Mutations targeting the ``req-id-format`` rule.

Comprehensive at the regex contract ^REQ-[A-Z0-9]{1,12}-\\d{4}$ — every
boundary class is exercised. All `must-catch`.
"""

from __future__ import annotations

from ._models import Mutation

_RULE = "req-id-format"


def _replace_heading_id(text: str, new_id: str) -> str:
    """Swap the first `## REQ-...` heading and the matching frontmatter `id:`
    line to ``new_id``. Leaves the rest of the block intact."""
    out_lines: list[str] = []
    swapped_heading = False
    swapped_fm = False
    for line in text.splitlines():
        if not swapped_heading and line.startswith("## REQ-"):
            out_lines.append(f"## {new_id}")
            swapped_heading = True
            continue
        if not swapped_fm and line.startswith("id: REQ-"):
            out_lines.append(f"id: {new_id}")
            swapped_fm = True
            continue
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def _swap(new_id: str):
    return lambda text: _replace_heading_id(text, new_id)


MUTATIONS: list[Mutation] = [
    # --- DOMAIN length boundaries ---
    Mutation("REQID-FMT-001", "empty DOMAIN", _RULE, _swap("REQ--0001")),
    Mutation("REQID-FMT-002", "13-char DOMAIN (just over)", _RULE, _swap("REQ-ABCDEFGHIJKLM-0001")),
    Mutation("REQID-FMT-003", "20-char DOMAIN", _RULE, _swap("REQ-ABCDEFGHIJKLMNOPQRST-0001")),
    # --- Number width boundaries ---
    Mutation("REQID-FMT-010", "1-digit number", _RULE, _swap("REQ-AUTH-1")),
    Mutation("REQID-FMT-011", "2-digit number", _RULE, _swap("REQ-AUTH-12")),
    Mutation("REQID-FMT-012", "3-digit number", _RULE, _swap("REQ-AUTH-123")),
    Mutation("REQID-FMT-013", "5-digit number", _RULE, _swap("REQ-AUTH-12345")),
    Mutation("REQID-FMT-014", "6-digit number", _RULE, _swap("REQ-AUTH-123456")),
    Mutation("REQID-FMT-015", "7-digit number", _RULE, _swap("REQ-AUTH-1234567")),
    # --- Number character class ---
    Mutation("REQID-FMT-020", "letter in number (head)", _RULE, _swap("REQ-AUTH-A001")),
    Mutation("REQID-FMT-021", "letter in number (mid)", _RULE, _swap("REQ-AUTH-0A01")),
    Mutation("REQID-FMT-022", "letter in number (tail)", _RULE, _swap("REQ-AUTH-000A")),
    Mutation("REQID-FMT-023", "all letters in number", _RULE, _swap("REQ-AUTH-ABCD")),
    # --- DOMAIN character class ---
    Mutation("REQID-FMT-030", "lowercase first char", _RULE, _swap("REQ-aUTH-0001")),
    Mutation("REQID-FMT-031", "lowercase last char", _RULE, _swap("REQ-AUTh-0001")),
    Mutation("REQID-FMT-032", "all lowercase DOMAIN", _RULE, _swap("REQ-auth-0001")),
    Mutation("REQID-FMT-033", "underscore in DOMAIN", _RULE, _swap("REQ-AU_TH-0001")),
    Mutation("REQID-FMT-034", "hyphen in DOMAIN (extra hyphen total)", _RULE, _swap("REQ-AU-TH-0001")),
    Mutation("REQID-FMT-035", "period in DOMAIN", _RULE, _swap("REQ-AU.TH-0001")),
    Mutation("REQID-FMT-036", "space in DOMAIN", _RULE, _swap("REQ-AU TH-0001")),
]
