# .claude/agents/

Thin wrappers that surface BMAD personas to Claude Code as subagents.
Populated in PHASE-1 per
[`ADR-0002`](../../openspec/architecture/decisions/ADR-0002-bmad-integration.md).

Each wrapper is one front-matter block plus a `Load:` directive pointing at a
file under `bmad/` by **path**, never by name.
