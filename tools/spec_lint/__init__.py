"""
tools.spec_lint — spec hygiene linter.

Implements rules from ADR-0004 (paper-derived spec storage discipline).
See openspec/architecture/decisions/ADR-0008-ci-gates-and-phase-exits.md for
the full gate inventory.

Public surface (PHASE-1, CHG-0003):
- models: SpecFile, ReqBlock, Finding
- parser: parse_spec_file(path) -> SpecFile
- rules.req_id_format.ReqIdFormat
- rules.spec_frontmatter_valid.SpecFrontmatterValid
"""
