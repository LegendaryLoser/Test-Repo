"""
Mutation test driver.

PHASE-1 / CHG-0008. Red in TASK-0014, green in TASK-0015.

For each rule, parametrizes over its mutation corpus. must-catch mutations
gate CI as red errors when uncaught. known-limitation mutations are run
inside a separate test that asserts they are NOT caught (they document the
current rule's boundary); a flip in either direction is a real signal worth
investigating.
"""

from __future__ import annotations

import pathlib

import pytest

from tools.spec_lint.parser import parse_spec_file_text
from tools.spec_lint.rules.anti_aliasing import AntiAliasing
from tools.spec_lint.rules.compound_requirement_detector import (
    CompoundRequirementDetector,
)
from tools.spec_lint.rules.prose_xref_banned import ProseXrefBanned
from tools.spec_lint.rules.req_id_format import ReqIdFormat
from tools.spec_lint.rules.spec_frontmatter_valid import SpecFrontmatterValid
from tools.spec_lint.rules.xref_resolves import XrefResolves

from tools.spec_lint.tests.mutations import (
    anti_aliasing_mutations,
    compound_mutations,
    prose_xref_banned_mutations,
    req_id_format_mutations,
    spec_frontmatter_valid_mutations,
    xref_resolves_mutations,
)
from tools.spec_lint.tests.mutations._models import Mutation
from tools.spec_lint.tests.mutations._seeds import single_req_seed
from tools.spec_lint.tests.mutations.runner import assert_caught, run_mutation
from tools.spec_lint.tests.xref_helpers import write_doc
from tools.spec_lint.tests.history_helpers import req_block, spec_file_text

FAKE_PATH = "/fake/openspec/specs/test.spec.md"


# ---------------------------------------------------------------------------
# Per-rule check adapters: each takes the mutated input and returns findings.
# ---------------------------------------------------------------------------


def _check_req_id_format(text: str):
    spec = parse_spec_file_text(text, FAKE_PATH)
    return ReqIdFormat().check(spec)


def _check_spec_frontmatter_valid(text: str):
    spec = parse_spec_file_text(text, FAKE_PATH)
    return SpecFrontmatterValid().check(spec)


def _check_compound(text: str):
    spec = parse_spec_file_text(text, FAKE_PATH)
    return CompoundRequirementDetector().check(spec)


def _check_anti_aliasing(text: str):
    # The mutation produces a SECOND spec (REQ-AUTH-0002 with same/edited body).
    # Pair with the seed spec (REQ-AUTH-0001) and run check_corpus.
    seed = single_req_seed("REQ-AUTH-0001")
    s1 = parse_spec_file_text(seed, "/fake/a.spec.md")
    s2 = parse_spec_file_text(text, "/fake/b.spec.md")
    return AntiAliasing().check_corpus([s1, s2])


# ---------------------------------------------------------------------------
# Driver tests — single-text rules
# ---------------------------------------------------------------------------


def _ids(corpus: list[Mutation], category: str):
    return [m.id for m in corpus if m.category == category]


def _by_id(corpus: list[Mutation], mid: str) -> Mutation:
    return next(m for m in corpus if m.id == mid)


@pytest.mark.parametrize("mid", _ids(req_id_format_mutations.MUTATIONS, "must-catch"))
def test_req_id_format_must_catch(mid: str) -> None:
    """
    @test-id TEST-SPEC-MUT-REQID-NNN
    @covers REQ-SPEC-0004
    """
    mutation = _by_id(req_id_format_mutations.MUTATIONS, mid)
    seed = single_req_seed()
    _, findings = run_mutation(seed, mutation, _check_req_id_format)
    assert_caught(mutation, findings)


@pytest.mark.parametrize(
    "mid", _ids(spec_frontmatter_valid_mutations.MUTATIONS, "must-catch")
)
def test_spec_frontmatter_valid_must_catch(mid: str) -> None:
    """
    @test-id TEST-SPEC-MUT-FRONTMATTER-NNN
    @covers REQ-SPEC-0005
    """
    mutation = _by_id(spec_frontmatter_valid_mutations.MUTATIONS, mid)
    seed = single_req_seed()
    _, findings = run_mutation(seed, mutation, _check_spec_frontmatter_valid)
    assert_caught(mutation, findings)


@pytest.mark.parametrize("mid", _ids(compound_mutations.MUTATIONS, "must-catch"))
def test_compound_must_catch(mid: str) -> None:
    """
    @test-id TEST-SPEC-MUT-COMPOUND-NNN
    @covers REQ-SPEC-0006
    """
    mutation = _by_id(compound_mutations.MUTATIONS, mid)
    seed = single_req_seed()
    _, findings = run_mutation(seed, mutation, _check_compound)
    assert_caught(mutation, findings)


@pytest.mark.parametrize("mid", _ids(anti_aliasing_mutations.MUTATIONS, "must-catch"))
def test_anti_aliasing_must_catch(mid: str) -> None:
    """
    @test-id TEST-SPEC-MUT-ALIAS-NNN
    @covers REQ-SPEC-0009
    """
    mutation = _by_id(anti_aliasing_mutations.MUTATIONS, mid)
    seed = single_req_seed("REQ-AUTH-0001")
    _, findings = run_mutation(seed, mutation, _check_anti_aliasing)
    assert_caught(mutation, findings)


# ---------------------------------------------------------------------------
# Driver tests — (path, text) rules
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mid", _ids(prose_xref_banned_mutations.MUTATIONS, "must-catch"))
def test_prose_xref_banned_must_catch(mid: str, tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-MUT-PROSE-NNN
    @covers REQ-SPEC-0007
    """
    mutation = _by_id(prose_xref_banned_mutations.MUTATIONS, mid)
    src = write_doc(tmp_path, "doc.md", "clean text REQ-AUTH-0001\n")
    mutated_text = mutation.apply(src.read_text())
    src.write_text(mutated_text)
    findings = ProseXrefBanned().check_files([(src, mutated_text)])
    assert_caught(mutation, findings)


@pytest.mark.parametrize("mid", _ids(xref_resolves_mutations.MUTATIONS, "must-catch"))
def test_xref_resolves_must_catch(mid: str, tmp_path: pathlib.Path) -> None:
    """
    @test-id TEST-SPEC-MUT-XREF-NNN
    @covers REQ-SPEC-0008
    """
    mutation = _by_id(xref_resolves_mutations.MUTATIONS, mid)
    # Materialize a real spec file at the path that XREF-REQ-WRONG-ID
    # references, so resolution gets past the existence check.
    write_doc(
        tmp_path,
        "openspec/specs/auth/login.spec.md",
        spec_file_text(req_block("REQ-AUTH-0001")),
    )
    src = write_doc(tmp_path, "doc.md", "seed: clean\n")
    mutated_text = mutation.apply(src.read_text())
    src.write_text(mutated_text)
    findings = XrefResolves().check_files([(src, mutated_text)])
    assert_caught(mutation, findings)


# ---------------------------------------------------------------------------
# Known-limitation suite — informational, asserts current boundary
# ---------------------------------------------------------------------------


def _kl_runners():
    return [
        (compound_mutations.MUTATIONS, _check_compound, single_req_seed()),
        (anti_aliasing_mutations.MUTATIONS, _check_anti_aliasing, single_req_seed("REQ-AUTH-0001")),
    ]


def test_known_limitations_remain_uncaught() -> None:
    """
    @test-id TEST-SPEC-MUT-KL-0001
    @covers REQ-SPEC-0006, REQ-SPEC-0009

        Each known-limitation mutation documents the current deterministic
        boundary. If one of these starts being CAUGHT, that's a real signal:
        either the rule improved (great — promote to must-catch) or the
        mutation was mislabeled. Either way, manual review needed.
    """
    uncaught_count = 0
    surprises: list[str] = []
    for corpus, check_fn, seed in _kl_runners():
        for m in corpus:
            if m.category != "known-limitation":
                continue
            _, findings = run_mutation(seed, m, check_fn)
            caught = any(f.rule_id == m.expected_rule_id for f in findings)
            if caught:
                surprises.append(f"{m.id} ({m.description}) was caught — investigate")
            else:
                uncaught_count += 1
    # Surprises become test failures so they're visible. Uncaught is the
    # expected state.
    assert not surprises, "Known-limitation mutations caught (review):\n" + "\n".join(surprises)
    assert uncaught_count > 0, "no known-limitation mutations exercised — corpus drift"
