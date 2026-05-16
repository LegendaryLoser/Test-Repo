"""
Rule: xref-resolves

Enforces ADR-0004 §2 — every relative markdown link and every
``REQ-X-NNNN @ relative/path.spec.md`` reference must resolve. For REQ
references, the cited spec file must contain a ``## REQ-X-NNNN`` heading.

Resolution semantics:
- Markdown link ``[text](path)``: **src-relative** (standard markdown).
- ``REQ-X-NNNN @ path``: tries **src-relative** first, then walks up
  ancestor directories trying each as a notional repo root. The
  ADR-0004 §2 example uses repo-relative paths
  (``REQ-AUTH-0007 @ openspec/specs/auth/login.spec.md``); walk-up makes
  that convention work without the rule needing an explicit root.
"""

from __future__ import annotations

import pathlib
import re

from ..models import Finding

_MD_LINK_RE = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)")
_REQ_AT_PATH_RE = re.compile(
    r"\b(?P<id>REQ-[A-Z0-9_]+-\d+)\s+@\s+(?P<path>[\w./_-]+\.spec\.md)\b"
)
_REQ_HEADING_RE = re.compile(r"^## (REQ-\S+)\s*$", re.MULTILINE)
_SKIP_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "ftps://")


def _strip_fragment(target: str) -> str:
    return target.split("#", 1)[0]


class XrefResolves:
    id = "xref-resolves"
    description = "Markdown link targets and REQ-ID@path references resolve (ADR-0004 §2)"

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        findings: list[Finding] = []
        for path, text in files:
            findings.extend(self._check_md_links(path, text))
            findings.extend(self._check_req_at_path(path, text))
        return findings

    def _check_md_links(
        self, path: pathlib.Path, text: str
    ) -> list[Finding]:
        out: list[Finding] = []
        for line_no, line in enumerate(text.splitlines(), start=1):
            for m in _MD_LINK_RE.finditer(line):
                raw = m.group("target").strip()
                if raw.startswith(_SKIP_SCHEMES):
                    continue
                target = _strip_fragment(raw)
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    out.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=str(path),
                            line=line_no,
                            message=(
                                f"Broken markdown link: {raw!r} "
                                f"(resolved to {resolved})"
                            ),
                        )
                    )
        return out

    def _check_req_at_path(
        self, path: pathlib.Path, text: str
    ) -> list[Finding]:
        out: list[Finding] = []
        for line_no, line in enumerate(text.splitlines(), start=1):
            for m in _REQ_AT_PATH_RE.finditer(line):
                req_id = m.group("id")
                target = m.group("path")
                resolved = self._resolve_req_path(path, target)
                if resolved is None:
                    out.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=str(path),
                            line=line_no,
                            req_id=req_id,
                            message=(
                                f"REQ-ID reference target missing: "
                                f"{target!r} ({req_id} @ {target})"
                            ),
                        )
                    )
                    continue
                if not self._contains_req(resolved, req_id):
                    out.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=str(path),
                            line=line_no,
                            req_id=req_id,
                            message=(
                                f"REQ-ID {req_id} not found in {target!r} "
                                f"(resolved to {resolved})"
                            ),
                        )
                    )
        return out

    @staticmethod
    def _resolve_req_path(
        src: pathlib.Path, target: str
    ) -> pathlib.Path | None:
        """src-relative first, then walk-up across ancestor directories."""
        primary = (src.parent / target).resolve()
        if primary.exists():
            return primary
        p = src.resolve().parent
        while p != p.parent:
            candidate = (p / target).resolve()
            if candidate.exists():
                return candidate
            p = p.parent
        return None

    @staticmethod
    def _contains_req(spec_path: pathlib.Path, req_id: str) -> bool:
        try:
            text = spec_path.read_text()
        except OSError:
            return False
        return any(
            m.group(1) == req_id for m in _REQ_HEADING_RE.finditer(text)
        )
