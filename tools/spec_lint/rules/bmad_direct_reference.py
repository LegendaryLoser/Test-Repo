"""
Rule: bmad-direct-reference

Enforces [ADR-0002](../../../openspec/architecture/decisions/ADR-0002-bmad-integration.md)
§6 + Compliance — no file under ``tools/``, ``packages/``, or
``projects/`` may import from or execute ``_bmad/``, except authorized
integration points (``tools/tea/`` when it exists).

Detection is narrow (imports + executable paths only) so docstrings,
comments, and string constants describing the rule do not self-flag:

- Python: ``^\\s*(?:import|from)\\s+_bmad\\b``,
  ``(?:__import__|importlib\\.import_module)\\(["']_bmad``.
- Subprocess: ``subprocess\\.\\w+\\(\\s*\\[\\s*["']_bmad/``.
- TS / JS: ``import .* from ["']..._bmad/...``,
  ``require\\(["']..._bmad/...``.
- Shell: any ``_bmad/`` path component.

Allow path: ``tools/tea/`` (per ADR-0002 §6). Inline allow marker:
``<!-- spec-lint: allow bmad-direct-reference -->`` on same line.
Rule's own implementation + test files are structurally exempt.
"""

from __future__ import annotations

import pathlib
import re

from ..models import Finding


_PY_IMPORT_BMAD = re.compile(r"^\s*(?:import|from)\s+_bmad\b")
_PY_DYNAMIC_BMAD = re.compile(
    r"(?:__import__|importlib\.import_module)\s*\(\s*[\"']_bmad"
)
_PY_SUBPROCESS_BMAD = re.compile(
    r"subprocess\.\w+\s*\(\s*\[\s*[\"']_bmad/"
)
_TS_IMPORT_BMAD = re.compile(
    r"""(?:import|from)\s+["'][^"']*_bmad/"""
)
_TS_REQUIRE_BMAD = re.compile(
    r"""require\s*\(\s*["'][^"']*_bmad/"""
)
_SH_BMAD_PATH = re.compile(r"(?:^|[/\s])_bmad/")

_ALLOW_MARKER = "spec-lint: allow bmad-direct-reference"

_ALLOWED_PATH_PREFIXES = ("tools/tea/",)

_OWN_FILE_SUFFIXES = (
    "tools/spec_lint/rules/bmad_direct_reference.py",
    "tools/spec_lint/tests/test_bmad_direct_reference.py",
)


def _posix(path: pathlib.Path) -> str:
    return path.as_posix()


class BmadDirectReference:
    id = "bmad-direct-reference"
    description = (
        "No file under tools/, packages/, projects/ may import or execute "
        "_bmad/ paths except tools/tea/ (ADR-0002 §6)"
    )

    def check_files(
        self, files: list[tuple[pathlib.Path, str]]
    ) -> list[Finding]:
        findings: list[Finding] = []
        for path, text in files:
            findings.extend(self._check_one(path, text))
        return findings

    def _check_one(
        self, path: pathlib.Path, text: str
    ) -> list[Finding]:
        path_str = _posix(path)
        if any(path_str.endswith(s) for s in _OWN_FILE_SUFFIXES):
            return []
        if any(path_str.startswith(p) or f"/{p}" in path_str for p in _ALLOWED_PATH_PREFIXES):
            return []

        suffix = path.suffix
        if suffix == ".py":
            patterns = ((_PY_IMPORT_BMAD, "import"), (_PY_DYNAMIC_BMAD, "dynamic import"), (_PY_SUBPROCESS_BMAD, "subprocess path"))
        elif suffix in (".ts", ".tsx", ".js", ".jsx"):
            patterns = ((_TS_IMPORT_BMAD, "import"), (_TS_REQUIRE_BMAD, "require"))
        elif suffix == ".sh":
            patterns = ((_SH_BMAD_PATH, "path"),)
        else:
            return []

        out: list[Finding] = []
        for i, line in enumerate(text.splitlines(), start=1):
            if _ALLOW_MARKER in line:
                continue
            for pattern, what in patterns:
                if pattern.search(line):
                    out.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=path_str,
                            line=i,
                            message=(
                                f"Direct reference to _bmad/ via {what}; "
                                f"ADR-0002 §6 forbids this outside tools/tea/. "
                                f"Add `<!-- {_ALLOW_MARKER} -->` only if you "
                                f"are an authorized integration point."
                            ),
                        )
                    )
                    break
        return out
