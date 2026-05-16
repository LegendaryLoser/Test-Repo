"""
spec_lint CLI entry point.

Invocation:
  python -m tools.spec_lint validate [path]    # run all rules over openspec/
  python -m tools.spec_lint check-layout       # run top-level-allowlist over CWD

The CLI is the unit of behavior CI invokes. Tests exercise it via
subprocess (see ``tests/test_openspec_validate.py``).

Excluded paths (always):
- ``openspec/_bmad-output/`` — staging (per ADR-0002 §7); drafts are
  not bound by canonical lint rules.
- ``openspec/changes/_TEMPLATE/`` — template scaffold; intentionally
  illustrative rather than valid.

Historical rules (``ReqIdImmutable``, ``ReqAppendOnly``) are not run
here — they require git history access per file and are designed to run
at commit-time / pre-receive, not as a snapshot validator.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

from .parser import parse_spec_file
from .rules.anti_aliasing import AntiAliasing
from .rules.compound_requirement_detector import CompoundRequirementDetector
from .rules.prose_xref_banned import ProseXrefBanned
from .rules.req_id_format import ReqIdFormat
from .rules.spec_frontmatter_valid import SpecFrontmatterValid
from .rules.top_level_allowlist import TopLevelAllowlist
from .rules.xref_resolves import XrefResolves


_EXCLUDED_REL_PREFIXES = (
    "_bmad-output/",
    "changes/_TEMPLATE/",
)


def _is_excluded(rel_posix: str) -> bool:
    return any(rel_posix.startswith(p) for p in _EXCLUDED_REL_PREFIXES)


def _gather(root: pathlib.Path) -> tuple[list[tuple[pathlib.Path, str]], list]:
    md_files: list[tuple[pathlib.Path, str]] = []
    spec_files = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if _is_excluded(rel):
            continue
        text = path.read_text()
        md_files.append((path, text))
        if path.name.endswith(".spec.md"):
            spec_files.append(parse_spec_file(path))
    return md_files, spec_files


def _cmd_validate(args: argparse.Namespace) -> int:
    target = pathlib.Path(args.path).resolve()
    if not target.exists():
        print(f"spec_lint validate: path does not exist: {target}", file=sys.stderr)
        return 2

    md_files, spec_files = _gather(target)

    findings = []

    per_file_rules = (
        SpecFrontmatterValid(),
        CompoundRequirementDetector(),
        ReqIdFormat(),
    )
    for sf in spec_files:
        findings.extend(sf.parse_findings)
        for rule in per_file_rules:
            findings.extend(rule.check(sf))

    cross_file_rules = (
        ProseXrefBanned(),
        XrefResolves(),
    )
    for rule in cross_file_rules:
        findings.extend(rule.check_files(md_files))

    findings.extend(AntiAliasing().check_corpus(spec_files))

    for f in findings:
        print(str(f), file=sys.stderr)

    return 1 if findings else 0


def _cmd_check_layout(args: argparse.Namespace) -> int:
    del args
    findings = TopLevelAllowlist().check_repo(pathlib.Path.cwd())
    for f in findings:
        print(str(f), file=sys.stderr)
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="spec_lint")
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Run all spec_lint rules over a path")
    v.add_argument("path", nargs="?", default="openspec")
    v.set_defaults(func=_cmd_validate)

    c = sub.add_parser("check-layout", help="Run top-level-allowlist over CWD")
    c.set_defaults(func=_cmd_check_layout)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
