"""
Rule: spec-frontmatter-valid

Enforces ADR-0004 §5 — REQ frontmatter has required keys with valid values.

Required keys: id, revision, status, introduced, supersedes, phase, tier,
references. `references` must be a mapping with `epic`, `story`, `adrs`
sub-keys; `adrs` must be a list.

Type / enum constraints:
- id: REQ-<DOMAIN>-<NNNN> AND must equal heading id.
- revision: positive int.
- status: ∈ {draft, tests-red, tests-green, reviewed, merged, deprecated}.
- introduced: CHG-NNNN.
- supersedes: null or REQ-<DOMAIN>-<NNNN>.
- phase: PHASE-N.
- tier: ∈ {unit, integration, e2e, stochastic}.
"""

from __future__ import annotations

import re

from ..models import Finding, SpecFile

# Loose REQ-ID match — strict format is the job of rule req-id-format.
_REQ_ID_LOOSE = re.compile(r"^REQ-[A-Za-z0-9_]+-\d+$")
_CHG_ID = re.compile(r"^CHG-\d{4}$")
_PHASE_ID = re.compile(r"^PHASE-\d+$")

_STATUS_VALUES = {"draft", "tests-red", "tests-green", "reviewed", "merged", "deprecated"}
_TIER_VALUES = {"unit", "integration", "e2e", "stochastic"}

_REQUIRED_KEYS = (
    "id",
    "revision",
    "status",
    "introduced",
    "supersedes",
    "phase",
    "tier",
    "references",
)
_REQUIRED_REFERENCES_KEYS = ("epic", "story", "adrs")


class SpecFrontmatterValid:
    id = "spec-frontmatter-valid"
    description = "REQ frontmatter has required keys with valid values (ADR-0004 §5)"

    def check(self, spec_file: SpecFile) -> list[Finding]:
        out: list[Finding] = []
        for r in spec_file.requirements:
            if r.frontmatter is None:
                out.append(self._finding(r, "REQ block has no frontmatter or frontmatter failed to parse"))
                continue
            fm = r.frontmatter

            for key in _REQUIRED_KEYS:
                if key not in fm:
                    out.append(self._finding(r, f"Frontmatter missing required key: {key}"))

            if "id" in fm and fm["id"] != r.heading_id:
                out.append(
                    self._finding(
                        r,
                        f"Frontmatter id '{fm['id']}' does not match heading id '{r.heading_id}'",
                    )
                )

            if "revision" in fm and (not isinstance(fm["revision"], int) or fm["revision"] < 1):
                out.append(self._finding(r, f"revision must be a positive int, got {fm['revision']!r}"))

            if "status" in fm and fm["status"] not in _STATUS_VALUES:
                out.append(
                    self._finding(
                        r, f"status '{fm['status']}' not in {sorted(_STATUS_VALUES)}"
                    )
                )

            if "tier" in fm and fm["tier"] not in _TIER_VALUES:
                out.append(
                    self._finding(r, f"tier '{fm['tier']}' not in {sorted(_TIER_VALUES)}")
                )

            if "introduced" in fm and (
                not isinstance(fm["introduced"], str) or not _CHG_ID.match(fm["introduced"])
            ):
                out.append(
                    self._finding(r, f"introduced '{fm['introduced']}' is not a valid CHG-NNNN")
                )

            if "phase" in fm and (
                not isinstance(fm["phase"], str) or not _PHASE_ID.match(fm["phase"])
            ):
                out.append(self._finding(r, f"phase '{fm['phase']}' is not a valid PHASE-N"))

            if "supersedes" in fm and fm["supersedes"] is not None:
                if not isinstance(fm["supersedes"], str) or not _REQ_ID_LOOSE.match(fm["supersedes"]):
                    out.append(
                        self._finding(
                            r,
                            f"supersedes must be null or REQ-<DOMAIN>-<NNNN>, got {fm['supersedes']!r}",
                        )
                    )

            if "references" in fm:
                refs = fm["references"]
                if not isinstance(refs, dict):
                    out.append(
                        self._finding(
                            r, f"references must be a mapping, got {type(refs).__name__}"
                        )
                    )
                else:
                    for key in _REQUIRED_REFERENCES_KEYS:
                        if key not in refs:
                            out.append(self._finding(r, f"references missing key: {key}"))
                    if "adrs" in refs and not isinstance(refs["adrs"], list):
                        out.append(
                            self._finding(
                                r,
                                f"references.adrs must be a list, got {type(refs['adrs']).__name__}",
                            )
                        )

        return out

    def _finding(self, r, message: str) -> Finding:
        return Finding(
            rule_id=self.id,
            severity="error",
            file=r.file,
            req_id=r.heading_id,
            line=r.heading_line,
            message=message,
        )
