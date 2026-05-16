"""
Rule: req-append-only

Enforces ADR-0004 §7 — once a REQ reaches `status: tests-green`, its
`### Description` and `### Acceptance` bodies are frozen. Cosmetic edits
require a `revision` bump.

PHASE-1 scope simplification (CHG-0004 proposal): the "if no downstream
artifact refers to the prior revision" clause is not yet enforced — treats
all tests-green REQs as frozen modulo revision bumps. Tightening lands
in a CHG-0005 follow-up.
"""

from __future__ import annotations

from ..models import Finding

_FROZEN_SECTIONS = ("### Description", "### Acceptance")


def _extract_section(body: str, header: str) -> str:
    """Return text under a ``### Header`` heading, up to the next ``### ``
    line or end-of-body, stripped of leading/trailing whitespace."""
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


class ReqAppendOnly:
    id = "req-append-only"
    description = "tests-green REQ bodies are frozen unless revision bumps (ADR-0004 §7)"

    def check_history(self, versions: list) -> list[Finding]:
        findings: list[Finding] = []
        # Per-REQ baseline snapshot from the first commit where status became
        # tests-green. Updated on every accepted revision bump so further
        # changes are measured against the most-recent legal baseline.
        baseline: dict[str, tuple[int | None, dict[str, str], str]] = {}

        for version in versions:
            for r in version.spec_file.requirements:
                if r.frontmatter is None:
                    continue
                req_id = r.heading_id
                status = r.frontmatter.get("status")
                revision = r.frontmatter.get("revision")
                sections = {h: _extract_section(r.body, h) for h in _FROZEN_SECTIONS}

                if req_id not in baseline:
                    if status == "tests-green":
                        baseline[req_id] = (revision, sections, version.sha)
                    continue

                base_rev, base_sections, base_sha = baseline[req_id]
                body_changed = sections != base_sections
                rev_bumped = (
                    isinstance(revision, int)
                    and isinstance(base_rev, int)
                    and revision > base_rev
                )

                if body_changed and not rev_bumped:
                    findings.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=version.spec_file.path,
                            req_id=req_id,
                            line=r.heading_line,
                            message=(
                                f"REQ {req_id} body changed at commit "
                                f"{version.sha[:8]} after reaching tests-green at "
                                f"{base_sha[:8]} without a revision bump "
                                f"(revision={revision}, baseline={base_rev})."
                            ),
                        )
                    )
                elif body_changed and rev_bumped:
                    # Accept the new body as the next baseline.
                    baseline[req_id] = (revision, sections, version.sha)

        return findings
