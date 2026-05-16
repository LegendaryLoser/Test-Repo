"""
Per-corpus loaders.

PHASE-1 / CHG-0009 / TASK-0017 — RED stubs. TASK-0018 implements.
"""

from __future__ import annotations

import pathlib

from ..models import SpecFile


def load_openspec_docs(corpus_dir: pathlib.Path) -> list[tuple[pathlib.Path, str]]:
    """Return (path, text) for every `*.md` file in the OpenSpec corpus
    directory.

    MANIFEST.md and LICENSE are excluded — they are not user-authored
    documentation content for the spec_lint rules to scan.
    """
    raise NotImplementedError(
        "load_openspec_docs: TASK-0017 RED stub — implemented in TASK-0018"
    )


def load_promise_arff(arff_path: pathlib.Path) -> list[SpecFile]:
    """Parse the PROMISE_exp ARFF file; return one synthetic SpecFile per
    requirement.

    Each requirement becomes a SpecFile with a single ReqBlock:
    - heading_id = ``REQ-PRMS-<NNNN>`` (synthetic; PROMISE has no IDs).
    - Description = the original requirement text, verbatim.
    - Acceptance = the original requirement text (so anti-aliasing has a
      single body to compare; the duplication is documented at the loader
      boundary, not in the data).
    - frontmatter populated with synthetic-but-valid values so spec
      structure is well-formed for rules that inspect it.
    """
    raise NotImplementedError(
        "load_promise_arff: TASK-0017 RED stub — implemented in TASK-0018"
    )
