"""
Rule: anti-aliasing

Enforces ADR-0004 §4 — pairwise n-gram similarity across all REQ
Description+Acceptance bodies in the corpus; pairs above a configurable
threshold are flagged. These are the paper's δ-convex lures: distinct
specifications occupying near-identical positions in any retrieval space.

Configuration: ``tools/spec_lint/config.yaml`` under ``anti_aliasing``.
Constructor accepts an override dict for tests.
"""

from __future__ import annotations

import pathlib

import yaml

from .._sections import extract_section
from ..models import Finding, SpecFile

_CONFIG_PATH = pathlib.Path(__file__).resolve().parent.parent / "config.yaml"
_DEFAULT_CONFIG = {"ngram_size": 4, "ngram_type": "char", "threshold": 0.7}


class AntiAliasing:
    id = "anti-aliasing"
    description = (
        "Pairs of REQs with high n-gram similarity in Description+Acceptance "
        "(ADR-0004 §4, paper-derived)"
    )

    def __init__(self, config: dict | None = None):
        cfg = config if config is not None else self._load_config()
        self.ngram_size: int = int(cfg["ngram_size"])
        self.ngram_type: str = str(cfg["ngram_type"])
        self.threshold: float = float(cfg["threshold"])

    @staticmethod
    def _load_config() -> dict:
        try:
            data = yaml.safe_load(_CONFIG_PATH.read_text())
            return data["anti_aliasing"]
        except (OSError, KeyError, TypeError):
            return dict(_DEFAULT_CONFIG)

    def check_corpus(self, spec_files: list[SpecFile]) -> list[Finding]:
        entries: list[tuple[str, str, int, frozenset[str]]] = []
        for sf in spec_files:
            for r in sf.requirements:
                desc = extract_section(r.body, "### Description")
                acc = extract_section(r.body, "### Acceptance")
                body_text = (desc + "\n" + acc).strip()
                if not body_text:
                    continue
                ngrams = self._ngrams(body_text)
                if ngrams:
                    entries.append(
                        (r.heading_id, r.file, r.heading_line, ngrams)
                    )

        out: list[Finding] = []
        n = len(entries)
        for i in range(n):
            id1, file1, line1, set1 = entries[i]
            for j in range(i + 1, n):
                id2, file2, line2, set2 = entries[j]
                sim = self._jaccard(set1, set2)
                if sim >= self.threshold:
                    out.append(
                        Finding(
                            rule_id=self.id,
                            severity="error",
                            file=file1,
                            req_id=id1,
                            line=line1,
                            message=(
                                f"REQ {id1} body has Jaccard similarity "
                                f"{sim:.2f} with REQ {id2} @ {file2}:{line2} "
                                f"(threshold {self.threshold:.2f}). "
                                f"ADR-0004 §4: near-duplicates are the paper's "
                                f"δ-convex lures — split, merge, or distinguish."
                            ),
                        )
                    )
        return out

    @staticmethod
    def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    def _ngrams(self, text: str) -> frozenset[str]:
        text = text.lower().strip()
        if self.ngram_type == "char":
            if len(text) < self.ngram_size:
                return frozenset()
            return frozenset(
                text[i : i + self.ngram_size]
                for i in range(len(text) - self.ngram_size + 1)
            )
        # word mode
        words = text.split()
        if len(words) < self.ngram_size:
            return frozenset()
        return frozenset(
            " ".join(words[i : i + self.ngram_size])
            for i in range(len(words) - self.ngram_size + 1)
        )
