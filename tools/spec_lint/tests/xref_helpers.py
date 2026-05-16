"""Helpers for xref-resolves tests: lay out small file trees under tmp_path."""

from __future__ import annotations

import pathlib


def write_doc(root: pathlib.Path, rel: str, text: str) -> pathlib.Path:
    """Write ``text`` to ``root / rel``; create parent dirs as needed.
    Return the absolute path."""
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    return target
