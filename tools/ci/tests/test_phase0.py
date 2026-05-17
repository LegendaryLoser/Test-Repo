"""
PHASE-0 verification tests.

Each test corresponds to one REQ-ARCH-NNNN clause in
openspec/architecture/ARCHITECTURE.md §10. These assertions land in TASK-0002
(red→green); the same tests were RED in the TASK-0001 commit immediately
preceding this one (P4 — red-first).

Annotations below are parsed by tools/trace (PHASE-2). For now they are
documentary.

Each test is intentionally self-contained — it only reads files and uses
the standard library plus pyyaml. No fixture chain beyond `repo_root`.
"""

from __future__ import annotations

import json
import pathlib
import re

import pytest
import yaml


# ---------------------------------------------------------------------------
# Pinned constants — keep aligned with ARCHITECTURE.md §3 and ADR-0005 §6.
# A drift between this file and the architecture is itself a defect (CI for
# this fact lands in PHASE-2 via tools/trace cross-doc consistency).
# ---------------------------------------------------------------------------

# Top-level layout constants now live in `tools.spec_lint._top_level_allowlist`
# and are exercised via the `top-level-allowlist` rule from CHG-0011. This
# file no longer carries its own copies; the rule is the single source.

EXPECTED_ADRS = [f"ADR-{n:04d}" for n in range(1, 9)]
EXPECTED_PHASES = [f"PHASE-{n}" for n in range(0, 6)]

EXPECTED_HOOK_EVENTS = {"SessionStart", "PreToolUse", "PostToolUse", "Stop", "SessionEnd"}

PRODUCT_TEMPLATE_PATHS = [
    "openspec/vision.md",
    "openspec/briefs/_TEMPLATE.md",
    "openspec/prd/_TEMPLATE.md",
    "openspec/epics/_TEMPLATE.md",
    "openspec/stories/_TEMPLATE.md",
]

NON_TEMPLATE_DIRS_MUST_BE_EMPTY = [
    "openspec/briefs",
    "openspec/prd",
    "openspec/epics",
    "openspec/stories",
]

# File extensions that count as "executable code" for REQ-ARCH-0006.
EXECUTABLE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".sh", ".bash"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_principles(text: str) -> list[str]:
    """Extract the five numbered, bold-prefixed principle bullets, joining continuation lines."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines) and len(out) < 5:
        m = re.match(r"^(\d)\.\s+(\*\*[^*]+\*\*.*)$", lines[i])
        if m and 1 <= int(m.group(1)) <= 5:
            buf = [m.group(2)]
            j = i + 1
            while j < len(lines) and lines[j].startswith("   "):
                buf.append(lines[j].strip())
                j += 1
            out.append(" ".join(buf))
            i = j
        else:
            i += 1
    return out


def _walk_markdown_links(text: str) -> list[str]:
    """Yield the target portion of every [text](target) link, stripped of #fragment."""
    pattern = re.compile(r"\[[^\]]+\]\((?P<target>[^)#]+)(?:#[^)]*)?\)")
    return [m.group("target").strip() for m in pattern.finditer(text)]


def _frontmatter(text: str) -> dict | None:
    """Parse a leading `---\\n...\\n---` YAML frontmatter block, if present."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    body = text[4:end]
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_arch_0001_top_level_layout(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0001
    @covers REQ-ARCH-0001

    Delegates to the runnable lint rule introduced in CHG-0011 so the
    invariant test and the gate cannot diverge.
    """
    from tools.spec_lint.rules.top_level_allowlist import TopLevelAllowlist

    findings = TopLevelAllowlist().check_repo(repo_root)
    assert findings == [], (
        "top-level-allowlist findings on real repo: "
        + "; ".join(f.message for f in findings)
    )


def test_arch_0002_architecture_artifacts_present(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0002
    @covers REQ-ARCH-0002
    """
    arch = repo_root / "openspec" / "architecture" / "ARCHITECTURE.md"
    assert arch.is_file(), "ARCHITECTURE.md missing"

    adr_dir = repo_root / "openspec" / "architecture" / "decisions"
    adr_files = sorted(adr_dir.glob("ADR-*.md"))
    adr_ids = []
    for f in adr_files:
        fm = _frontmatter(f.read_text())
        assert fm is not None, f"ADR has no frontmatter: {f.name}"
        assert "id" in fm, f"ADR missing id in frontmatter: {f.name}"
        adr_ids.append(fm["id"])
    assert adr_ids == EXPECTED_ADRS, f"ADR IDs mismatch: {adr_ids} != {EXPECTED_ADRS}"

    phase_dir = repo_root / "openspec" / "architecture" / "phases"
    phase_files = sorted(phase_dir.glob("PHASE-*.md"))
    phase_ids = []
    for f in phase_files:
        fm = _frontmatter(f.read_text())
        assert fm is not None, f"PHASE has no frontmatter: {f.name}"
        assert "id" in fm, f"PHASE missing id in frontmatter: {f.name}"
        phase_ids.append(fm["id"])
    assert phase_ids == EXPECTED_PHASES, f"PHASE IDs mismatch: {phase_ids} != {EXPECTED_PHASES}"


def test_arch_0003_empty_product_templates(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0003
    @covers REQ-ARCH-0003
    """
    for rel in PRODUCT_TEMPLATE_PATHS:
        assert (repo_root / rel).is_file(), f"Product template missing: {rel}"

    for rel in NON_TEMPLATE_DIRS_MUST_BE_EMPTY:
        d = repo_root / rel
        assert d.is_dir(), f"Product directory missing: {rel}"
        non_templates = [
            p.name for p in d.iterdir() if p.is_file() and not p.name.startswith("_TEMPLATE")
        ]
        assert not non_templates, (
            f"{rel} contains non-template product content: {sorted(non_templates)}"
        )


def test_arch_0004_specs_index_parses(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0004
    @covers REQ-ARCH-0004
    """
    index_path = repo_root / "openspec" / "specs" / "INDEX.yaml"
    assert index_path.is_file(), "openspec/specs/INDEX.yaml missing"
    data = yaml.safe_load(index_path.read_text())
    assert isinstance(data, dict), "INDEX.yaml top level is not a mapping"
    for key in ("version", "generated_at", "requirements"):
        assert key in data, f"INDEX.yaml missing key: {key}"
    assert isinstance(data["requirements"], list), "INDEX.yaml `requirements` must be a list"
    # Empty at PHASE-0 is explicitly permitted.
    assert data["requirements"] == [] or all(isinstance(r, dict) for r in data["requirements"])


def test_arch_0005_architecture_xrefs_resolve(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0005
    @covers REQ-ARCH-0005
    """
    arch_dir = repo_root / "openspec" / "architecture"
    broken: list[tuple[str, str]] = []
    for md in arch_dir.rglob("*.md"):
        for target in _walk_markdown_links(md.read_text()):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                broken.append((str(md.relative_to(repo_root)), target))
    assert not broken, "Broken cross-references in openspec/architecture/:\n" + "\n".join(
        f"  {src} -> {tgt}" for src, tgt in broken
    )


def test_arch_0006_no_executable_code_in_architecture(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0006
    @covers REQ-ARCH-0006
    """
    arch_dir = repo_root / "openspec" / "architecture"
    offenders: list[str] = []
    for f in arch_dir.rglob("*"):
        if not f.is_file():
            continue
        if f.suffix.lower() in EXECUTABLE_EXTENSIONS:
            offenders.append(str(f.relative_to(repo_root)))
            continue
        # Shebang scan for extensionless executables
        try:
            head = f.read_bytes()[:64]
        except OSError:
            continue
        if head.startswith(b"#!"):
            offenders.append(str(f.relative_to(repo_root)))
    assert not offenders, f"Executable code found under openspec/architecture/: {offenders}"


def test_arch_0007_claude_md_principles_verbatim(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0007
    @covers REQ-ARCH-0007
    """
    arch_principles = _extract_principles(
        (repo_root / "openspec" / "architecture" / "ARCHITECTURE.md").read_text()
    )
    claude_principles = _extract_principles((repo_root / "CLAUDE.md").read_text())

    assert len(arch_principles) == 5, f"ARCHITECTURE.md §1 must list 5 principles, got {len(arch_principles)}"
    assert len(claude_principles) == 5, f"CLAUDE.md must list 5 principles, got {len(claude_principles)}"
    for i, (a, c) in enumerate(zip(arch_principles, claude_principles), start=1):
        assert a == c, (
            f"Principle {i} drift between ARCHITECTURE.md and CLAUDE.md:\n"
            f"  arch:   {a}\n"
            f"  claude: {c}"
        )


def test_arch_0008_settings_declares_all_hooks(repo_root: pathlib.Path) -> None:
    """
    @test-id TEST-ARCH-0008
    @covers REQ-ARCH-0008
    """
    settings_path = repo_root / ".claude" / "settings.json"
    assert settings_path.is_file(), ".claude/settings.json missing"
    data = json.loads(settings_path.read_text())
    hooks = data.get("hooks", {})
    declared = set(hooks.keys())
    missing = EXPECTED_HOOK_EVENTS - declared
    assert not missing, f"Hook events missing from settings.json: {sorted(missing)}"
    # Every declared event must have at least one hooks entry.
    for event in EXPECTED_HOOK_EVENTS:
        entries = hooks.get(event, [])
        assert entries, f"Hook event `{event}` declared but has no hooks entries"
        for entry in entries:
            inner = entry.get("hooks", [])
            assert inner, f"Hook event `{event}` matcher has empty hooks list"
            for h in inner:
                assert h.get("type") == "command", (
                    f"Hook entry for `{event}` is not of type command: {h}"
                )
                assert h.get("command"), f"Hook entry for `{event}` missing command string"
