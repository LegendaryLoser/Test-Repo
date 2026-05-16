"""
Rule: compound-requirement-detector

Enforces ADR-0004 §3 — one REQ contains one assertion. A REQ whose
Acceptance section has more than one Given/When/Then bullet is compound by
definition and must be split.

PHASE-1 simplification: only the primary signal (multi-G/W/T) is used.
Prose-conjunction detection ("A and B", "plus") is deferred — high
false-positive risk.
"""

from __future__ import annotations

import re

from .._sections import extract_section
from ..models import Finding, SpecFile

# A "Given" assertion is a line that starts (after optional `-` bullet and
# whitespace) with the word "given" — case-insensitive. Counts both bulleted
# (`- Given …`) and unbulleted (`Given …`) styles.
_GIVEN_LINE_RE = re.compile(r"^\s*(?:-\s*)?given\b", re.IGNORECASE | re.MULTILINE)


class CompoundRequirementDetector:
    id = "compound-requirement-detector"
    description = "REQ has > 1 Given/When/Then in Acceptance (ADR-0004 §3)"

    def check(self, spec_file: SpecFile) -> list[Finding]:
        out: list[Finding] = []
        for r in spec_file.requirements:
            acceptance = extract_section(r.body, "### Acceptance")
            if not acceptance:
                continue
            count = len(_GIVEN_LINE_RE.findall(acceptance))
            if count > 1:
                out.append(
                    Finding(
                        rule_id=self.id,
                        severity="error",
                        file=r.file,
                        req_id=r.heading_id,
                        line=r.heading_line,
                        message=(
                            f"REQ {r.heading_id} has {count} Given/When/Then "
                            f"assertions in Acceptance; ADR-0004 §3 requires "
                            f"one assertion per REQ. Split into {count} REQs."
                        ),
                    )
                )
        return out
