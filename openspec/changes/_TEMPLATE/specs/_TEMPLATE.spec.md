# Spec delta — TEMPLATE

> Each change folder may carry a `specs/` directory containing the spec
> deltas it introduces. On merge, deltas are applied to
> `openspec/specs/<domain>/<feature>.spec.md` and removed from the change
> folder. Format of each REQ block is fixed by
> [`ADR-0004` §5](../../../architecture/decisions/ADR-0004-spec-storage-discipline.md).

## REQ-DOMAIN-NNNN
---
id: REQ-DOMAIN-NNNN
revision: 1
status: draft
introduced: CHG-NNNN
supersedes: null
phase: PHASE-<N>
tier: unit            # unit | integration | e2e | stochastic
references:
  epic: EPIC-NNNN
  story: STORY-NNNN
  adrs: []
---

### Description
<single assertion>

### Acceptance
- Given <state>, when <event>, then <observable outcome>

### Non-acceptance
- ...

### Notes
- ...
