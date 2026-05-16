"""Dry-run runner."""

from __future__ import annotations

import pathlib
import time
from dataclasses import dataclass, field

from ..models import Finding
from ..rules.anti_aliasing import AntiAliasing
from ..rules.compound_requirement_detector import CompoundRequirementDetector
from ..rules.prose_xref_banned import ProseXrefBanned
from ..rules.xref_resolves import XrefResolves
from .loaders import load_openspec_docs, load_promise_arff


@dataclass
class CorpusResult:
    name: str
    items_loaded: int
    findings_by_rule: dict[str, list[Finding]] = field(default_factory=dict)
    uncertain_by_rule: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class DryRunResult:
    corpora: list[CorpusResult] = field(default_factory=list)
    runtime_seconds: float = 0.0


def run_dry_run(corpora_root: pathlib.Path) -> DryRunResult:
    """Execute the full dry-run across all vendored corpora."""
    t0 = time.time()
    result = DryRunResult()

    openspec_dir = corpora_root / "openspec_docs"
    if openspec_dir.is_dir():
        pairs = load_openspec_docs(openspec_dir)
        c = CorpusResult(name="openspec_docs", items_loaded=len(pairs))
        c.findings_by_rule["prose-xref-banned"] = ProseXrefBanned().check_files(pairs)
        c.findings_by_rule["xref-resolves"] = XrefResolves().check_files(pairs)
        c.uncertain_by_rule["prose-xref-banned"] = []
        c.uncertain_by_rule["xref-resolves"] = []
        result.corpora.append(c)

    promise_path = corpora_root / "promise_nfr" / "PROMISE_exp.arff"
    if promise_path.is_file():
        specs = load_promise_arff(promise_path)
        c = CorpusResult(name="promise_nfr", items_loaded=len(specs))
        c.findings_by_rule["anti-aliasing"] = AntiAliasing().check_corpus(specs)
        compound_findings: list[Finding] = []
        compound_rule = CompoundRequirementDetector()
        for s in specs:
            compound_findings.extend(compound_rule.check(s))
        c.findings_by_rule["compound-requirement-detector"] = compound_findings
        c.uncertain_by_rule["anti-aliasing"] = []
        c.uncertain_by_rule["compound-requirement-detector"] = []
        result.corpora.append(c)

    result.runtime_seconds = time.time() - t0
    return result
