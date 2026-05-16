"""Mutations targeting the ``spec-frontmatter-valid`` rule.

Comprehensive over the YAML contract defined in ADR-0004 §5.
"""

from __future__ import annotations

import re

from ._models import Mutation

_RULE = "spec-frontmatter-valid"


def _drop_line_starting_with(text: str, prefix: str) -> str:
    out = []
    skip_block = False
    indent: int | None = None
    for line in text.splitlines():
        if skip_block:
            # Continue dropping while inside a more-indented block of the
            # previously dropped key.
            curr_indent = len(line) - len(line.lstrip())
            if line.strip() == "" or (indent is not None and curr_indent > indent):
                continue
            skip_block = False
        m = re.match(rf"^( *){re.escape(prefix)}", line)
        if m:
            indent = len(m.group(1))
            skip_block = True
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def _drop_key(key: str):
    return lambda text: _drop_line_starting_with(text, f"{key}:")


def _set_value(key: str, value: str):
    """Replace ``key: <anything>`` with ``key: <value>`` (single-line)."""
    pattern = re.compile(rf"^( *){re.escape(key)}\s*:.*$", re.MULTILINE)
    return lambda text: pattern.sub(rf"\1{key}: {value}", text, count=1)


def _drop_references_subkey(subkey: str):
    """Drop a sub-key under ``references:``."""

    def apply(text: str) -> str:
        out: list[str] = []
        in_refs = False
        for line in text.splitlines():
            if line.startswith("references:"):
                in_refs = True
                out.append(line)
                continue
            if in_refs:
                if line.startswith("  ") and line.lstrip().startswith(f"{subkey}:"):
                    continue
                if line and not line.startswith(" "):
                    in_refs = False
            out.append(line)
        return "\n".join(out) + ("\n" if text.endswith("\n") else "")

    return apply


_REQUIRED_KEYS = [
    "id",
    "revision",
    "status",
    "introduced",
    "supersedes",
    "phase",
    "tier",
    "references",
]

MUTATIONS: list[Mutation] = []

# --- Drop each required key ---
for k in _REQUIRED_KEYS:
    MUTATIONS.append(
        Mutation(
            id=f"FM-DROP-{k.upper()}",
            description=f"drop required key `{k}`",
            expected_rule_id=_RULE,
            apply=_drop_key(k),
        )
    )

# --- status enum ---
for bad_status in ("WIBBLE", "in-progress", "Done", "draft "):
    MUTATIONS.append(
        Mutation(
            id=f"FM-STATUS-{bad_status.strip().upper().replace(' ', '_').replace('-', '_')}",
            description=f"out-of-enum status `{bad_status}`",
            expected_rule_id=_RULE,
            apply=_set_value("status", bad_status),
        )
    )

# --- tier enum ---
for bad_tier in ("smoke", "Unit", "perf", "regression"):
    MUTATIONS.append(
        Mutation(
            id=f"FM-TIER-{bad_tier.strip().upper().replace(' ', '_')}",
            description=f"out-of-enum tier `{bad_tier}`",
            expected_rule_id=_RULE,
            apply=_set_value("tier", bad_tier),
        )
    )

# --- revision non-positive / non-int ---
for bad_rev in ("0", "-1"):
    MUTATIONS.append(
        Mutation(
            id=f"FM-REV-{bad_rev.replace('-', 'NEG')}",
            description=f"revision={bad_rev} (non-positive)",
            expected_rule_id=_RULE,
            apply=_set_value("revision", bad_rev),
        )
    )

# --- introduced / phase / supersedes ID formats ---
MUTATIONS.append(
    Mutation(
        id="FM-INTRO-NONE",
        description="introduced is not a CHG-NNNN",
        expected_rule_id=_RULE,
        apply=_set_value("introduced", "nope"),
    )
)
MUTATIONS.append(
    Mutation(
        id="FM-PHASE-NONE",
        description="phase is not PHASE-N",
        expected_rule_id=_RULE,
        apply=_set_value("phase", "P1"),
    )
)
MUTATIONS.append(
    Mutation(
        id="FM-SUPERS-NONE",
        description="supersedes is non-null and not a REQ-ID",
        expected_rule_id=_RULE,
        apply=_set_value("supersedes", "foo"),
    )
)

# --- references sub-keys ---
for sub in ("epic", "story", "adrs"):
    MUTATIONS.append(
        Mutation(
            id=f"FM-REFS-DROP-{sub.upper()}",
            description=f"references missing sub-key `{sub}`",
            expected_rule_id=_RULE,
            apply=_drop_references_subkey(sub),
        )
    )

# --- id-mismatch (heading vs frontmatter) ---
MUTATIONS.append(
    Mutation(
        id="FM-IDMISMATCH",
        description="frontmatter id != heading id",
        expected_rule_id=_RULE,
        apply=_set_value("id", "REQ-AUTH-0999"),
    )
)
