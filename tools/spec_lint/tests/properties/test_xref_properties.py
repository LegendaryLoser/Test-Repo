"""
Property-based tests for tools.spec_lint.rules.xref_resolves.

PHASE-1 / CHG-0007. Red in TASK-0012, green in TASK-0013.
"""

from __future__ import annotations

import pathlib

from hypothesis import HealthCheck, given, settings, strategies as st

from tools.spec_lint.rules.xref_resolves import XrefResolves
from tools.spec_lint.tests.xref_helpers import write_doc

# Filenames safe across platforms; non-empty; no path separators.
_FNAME = st.from_regex(r"\A[a-z][a-z0-9_]{0,15}\Z", fullmatch=True)


@settings(max_examples=20, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(name=_FNAME)
def test_links_to_existing_files_never_flagged(tmp_path: pathlib.Path, name: str) -> None:
    """
    @test-id TEST-SPEC-0075
    """
    target_name = f"{name}.md"
    write_doc(tmp_path, target_name, "# target\n")
    src = write_doc(tmp_path, "doc.md", f"See [target]({target_name}).\n")
    findings = [
        f
        for f in XrefResolves().check_files([(src, src.read_text())])
        if f.rule_id == "xref-resolves"
    ]
    assert findings == [], f"Expected no findings; got {findings}"


@settings(max_examples=20, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(name=_FNAME)
def test_links_to_missing_files_always_flagged(tmp_path: pathlib.Path, name: str) -> None:
    """
    @test-id TEST-SPEC-0076

    We pick a guaranteed-missing target by using a unique prefix that
    cannot collide with anything created by the helper.
    """
    target = f"NONEXISTENT_{name}.md"
    src = write_doc(tmp_path, "doc.md", f"See [missing]({target}).\n")
    findings = [
        f
        for f in XrefResolves().check_files([(src, src.read_text())])
        if f.rule_id == "xref-resolves"
    ]
    assert findings, f"Expected ≥1 finding for missing target {target!r}"
    assert any(target in f.message for f in findings)


@settings(max_examples=30, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    scheme=st.sampled_from(["http", "https", "ftp", "ftps"]),
    host=st.from_regex(r"\A[a-z]{3,10}\.[a-z]{2,5}\Z", fullmatch=True),
    path=st.from_regex(r"\A[a-z0-9/_-]{0,20}\Z", fullmatch=True),
)
def test_http_links_are_always_skipped(
    tmp_path: pathlib.Path, scheme: str, host: str, path: str
) -> None:
    """
    @test-id TEST-SPEC-0077
    """
    url = f"{scheme}://{host}/{path}"
    src = write_doc(tmp_path, "doc.md", f"[external]({url})\n")
    findings = [
        f
        for f in XrefResolves().check_files([(src, src.read_text())])
        if f.rule_id == "xref-resolves"
    ]
    assert findings == [], f"Expected no findings for {url!r}; got {findings}"
