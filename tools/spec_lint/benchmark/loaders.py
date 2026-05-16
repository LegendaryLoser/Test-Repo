"""Per-corpus loaders."""

from __future__ import annotations

import pathlib
import re

from ..models import SpecFile
from ..parser import parse_spec_file_text

_PROMISE_DATA_RE = re.compile(r"^(\d+),'(.*)',([A-Z]+)\s*$")
_OPENSPEC_SKIP = {"MANIFEST.md", "LICENSE"}


def load_openspec_docs(corpus_dir: pathlib.Path) -> list[tuple[pathlib.Path, str]]:
    """Return (path, text) for every `*.md` file in the OpenSpec corpus
    directory, excluding MANIFEST and LICENSE."""
    out: list[tuple[pathlib.Path, str]] = []
    for p in sorted(corpus_dir.iterdir()):
        if not p.is_file():
            continue
        if p.name in _OPENSPEC_SKIP:
            continue
        if p.suffix.lower() != ".md":
            continue
        out.append((p, p.read_text()))
    return out


def load_promise_arff(arff_path: pathlib.Path) -> list[SpecFile]:
    """Parse PROMISE_exp ARFF; return one synthetic SpecFile per requirement.

    Each ARFF data row becomes a synthetic REQ block with the original
    requirement text in Description AND Acceptance. The wrapping is
    deliberate: anti-aliasing operates over Description+Acceptance; doubling
    the body preserves text fidelity without weighting one section. The
    original text is never modified.
    """
    text = arff_path.read_text()
    in_data = False
    specs: list[SpecFile] = []
    idx = 0
    for raw in text.splitlines():
        if not in_data:
            if raw.strip().upper().startswith("@DATA"):
                in_data = True
            continue
        line = raw.rstrip()
        if not line or line.startswith("%"):
            continue
        m = _PROMISE_DATA_RE.match(line)
        if not m:
            continue
        idx += 1
        project_id, req_text, label = m.group(1), m.group(2), m.group(3)
        req_id = f"REQ-PRMS-{idx:04d}"
        synthetic = (
            f"# PROMISE requirement (project {project_id}, label {label})\n"
            f"\n"
            f"## {req_id}\n"
            f"---\n"
            f"id: {req_id}\n"
            f"revision: 1\n"
            f"status: draft\n"
            f"introduced: CHG-0009\n"
            f"supersedes: null\n"
            f"phase: PHASE-1\n"
            f"tier: unit\n"
            f"references:\n"
            f"  epic: EPIC-0001\n"
            f"  story: STORY-0001\n"
            f"  adrs: []\n"
            f"---\n"
            f"\n"
            f"### Description\n"
            f"{req_text}\n"
            f"\n"
            f"### Acceptance\n"
            f"{req_text}\n"
        )
        specs.append(parse_spec_file_text(synthetic, f"{arff_path}::req-{idx:04d}"))
    return specs
