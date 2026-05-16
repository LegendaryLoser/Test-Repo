"""
Rule: req-id-format

Enforces ADR-0004 §1 — REQ identifiers match ``^REQ-[A-Z0-9]{1,12}-\\d{4}$``.

Checks both the heading id (the ``## REQ-…`` line) and the frontmatter ``id``
field when present. Two distinct findings on the same block surface as two
Findings.
"""

from __future__ import annotations

import re

from ..models import Finding, SpecFile

REQ_ID_RE = re.compile(r"^REQ-[A-Z0-9]{1,12}-\d{4}$")


class ReqIdFormat:
    id = "req-id-format"
    description = "REQ-IDs match ^REQ-[A-Z0-9]{1,12}-\\d{4}$ (ADR-0004 §1)"

    def check(self, spec_file: SpecFile) -> list[Finding]:
        findings: list[Finding] = []
        for r in spec_file.requirements:
            if not REQ_ID_RE.match(r.heading_id):
                findings.append(
                    Finding(
                        rule_id=self.id,
                        severity="error",
                        file=r.file,
                        req_id=r.heading_id,
                        line=r.heading_line,
                        message=(
                            f"REQ heading id '{r.heading_id}' does not match "
                            f"REQ-<DOMAIN>-<NNNN> (DOMAIN: 1-12 uppercase alnum; "
                            f"NNNN: 4 digits)"
                        ),
                    )
                )
            if r.frontmatter and "id" in r.frontmatter:
                fm_id = r.frontmatter["id"]
                if not isinstance(fm_id, str) or not REQ_ID_RE.match(fm_id):
                    findings.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=r.file,
                            req_id=r.heading_id,
                            line=r.heading_line,
                            message=(
                                f"Frontmatter id '{fm_id}' does not match "
                                f"REQ-<DOMAIN>-<NNNN>"
                            ),
                        )
                    )
        return findings
