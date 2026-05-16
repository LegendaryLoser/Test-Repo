"""
Rule: req-id-immutable

Enforces ADR-0004 §1 — a REQ-ID, once introduced, never disappears from the
spec file. The only permitted lifecycle change is `status: deprecated`; the
REQ block stays in the file. Renames are forbidden; supersession is the
only path.
"""

from __future__ import annotations

from ..models import Finding


class ReqIdImmutable:
    id = "req-id-immutable"
    description = "REQ-IDs once introduced never disappear (ADR-0004 §1)"

    def check_history(self, versions: list) -> list[Finding]:
        if len(versions) < 2:
            return []
        findings: list[Finding] = []
        prev = versions[0]
        for curr in versions[1:]:
            prev_ids = {r.heading_id for r in prev.spec_file.requirements}
            curr_ids = {r.heading_id for r in curr.spec_file.requirements}
            for req_id in sorted(prev_ids - curr_ids):
                prev_block = next(
                    (r for r in prev.spec_file.requirements if r.heading_id == req_id),
                    None,
                )
                findings.append(
                    Finding(
                        rule_id=self.id,
                        severity="error",
                        file=prev.spec_file.path,
                        req_id=req_id,
                        line=prev_block.heading_line if prev_block else None,
                        message=(
                            f"REQ {req_id} present at commit {prev.sha[:8]} but "
                            f"absent at commit {curr.sha[:8]}. ADR-0004 §1: REQ-IDs "
                            f"are immutable; mark status: deprecated, do not remove."
                        ),
                    )
                )
            prev = curr
        return findings
