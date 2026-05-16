---
id: STORY-NNNN
title: <one line>
status: draft           # draft | tests-red | tests-green | reviewed | done | deprecated
date: YYYY-MM-DD
references:
  epic: EPIC-NNNN
  adrs: []
requirements: []        # REQ-IDs this Story produces
---

# STORY-NNNN — <title>

## User-visible behavior

<one paragraph>

## Behavior decomposition (TEA, Given/When/Then)

- Given <state>, when <event>, then <outcome>  → REQ-X-NNNN
- ...

Each row above must produce exactly one REQ. Compound rows are a defect
(see [ADR-0004 §3](../architecture/decisions/ADR-0004-spec-storage-discipline.md)).

## Acceptance for Story `done`

- All produced REQs `tests-green` at their declared tiers.
- TEA gate decision: pass.
