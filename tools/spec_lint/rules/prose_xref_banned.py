"""
Rule: prose-xref-banned

Enforces ADR-0004 §2 — references like "the auth spec" or "the login
requirement" are forbidden; every cross-reference must be by stable ID +
file path. Prose references are the channel through which semantic-recall
failure modes enter the system.

Inline allow marker (per-line escape valve):
    <!-- spec-lint: allow prose-xref-banned -->

Exemption: if a denylist match is followed on the same line by a stable
ID (REQ/ADR/CHG/EPIC/STORY/PHASE), the prose is treated as parenthetical
to an explicit reference and skipped.
"""

from __future__ import annotations

import pathlib
import re

from ..models import Finding

_PATTERNS = [
    (re.compile(r"\bthe \w+ specs?\b", re.IGNORECASE), "the X spec(s)"),
    (re.compile(r"\bthe \w+ requirements?\b", re.IGNORECASE), "the X requirement(s)"),
    (re.compile(r"\bthe \w+ ADR\b"), "the X ADR"),
    (re.compile(r"\bthe \w+ epic\b", re.IGNORECASE), "the X epic"),
    (re.compile(r"\bthe \w+ story\b", re.IGNORECASE), "the X story"),
    (re.compile(r"\bthe \w+ change\b", re.IGNORECASE), "the X change"),
]

_ID_RE = re.compile(
    r"\b(?:REQ-[A-Z0-9_]+-\d+|ADR-\d+|CHG-\d+|EPIC-\d+|STORY-\d+|PHASE-\d+)\b"
)
_ALLOW_MARKER = "spec-lint: allow prose-xref-banned"
_CODE_FENCE = re.compile(r"^\s*```")


class ProseXrefBanned:
    id = "prose-xref-banned"
    description = "Prose references to specs/REQs are forbidden; use ID + path (ADR-0004 §2)"

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        findings: list[Finding] = []
        for path, text in files:
            findings.extend(self._check_one(path, text))
        return findings

    def _check_one(self, path: pathlib.Path, text: str) -> list[Finding]:
        out: list[Finding] = []
        in_code = False
        for i, line in enumerate(text.splitlines(), start=1):
            if _CODE_FENCE.match(line):
                in_code = not in_code
                continue
            if in_code:
                continue
            if _ALLOW_MARKER in line:
                continue
            for pattern, descr in _PATTERNS:
                m = pattern.search(line)
                if not m:
                    continue
                # Same-line ID after the match → treat the prose as
                # parenthetical to an explicit reference.
                if _ID_RE.search(line[m.end():]):
                    continue
                out.append(
                    Finding(
                        rule_id=self.id,
                        severity="error",
                        file=str(path),
                        line=i,
                        message=(
                            f"Prose reference pattern '{descr}' detected: "
                            f"{m.group()!r}. Use ID + path per ADR-0004 §2 "
                            f"or add `<!-- {_ALLOW_MARKER} -->`."
                        ),
                    )
                )
        return out
