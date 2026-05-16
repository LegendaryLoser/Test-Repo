"""
Shared helper for extracting ``### Header`` sections from a REQ block body.

Returns the section text stripped of leading/trailing whitespace, with all
intermediate lines preserved. Used by rules that need to compare or count
content within a specific section (anti-aliasing, compound-requirement-
detector, and req-append-only has a private copy that pre-dates this module).
"""

from __future__ import annotations


def extract_section(body: str, header: str) -> str:
    """Return text under a ``### Header`` heading, up to the next ``### ``
    line or end-of-body, stripped of surrounding whitespace."""
    lines = body.splitlines()
    out: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("### "):
            if in_section:
                break
            if line.strip() == header:
                in_section = True
                continue
        if in_section:
            out.append(line)
    return "\n".join(out).strip()
