"""
spec_lint CLI entry point.

Invocation:
  python -m tools.spec_lint validate [path]    # run all rules over openspec/
  python -m tools.spec_lint check-layout       # run top-level-allowlist over CWD

Skeleton — TASK-0022 RED. Subcommands exit 0 without doing anything so
that TASK-0022's subprocess tests fail by assertion (expected exit 1 +
specific finding output), not by ModuleNotFoundError. Real implementation
lands in TASK-0023.
"""

from __future__ import annotations

import argparse
import sys


def _cmd_validate(args: argparse.Namespace) -> int:
    del args
    return 0


def _cmd_check_layout(args: argparse.Namespace) -> int:
    del args
    return 0


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
