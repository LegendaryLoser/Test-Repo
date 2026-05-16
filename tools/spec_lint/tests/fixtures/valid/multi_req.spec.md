# Search feature

Multi-REQ valid spec used as a positive test fixture for spec_lint.

## REQ-SEARCH-0001
---
id: REQ-SEARCH-0001
revision: 1
status: tests-green
introduced: CHG-0042
supersedes: null
phase: PHASE-5
tier: integration
references:
  epic: EPIC-0010
  story: STORY-0033
  adrs: [ADR-0003, ADR-0006]
---

### Description
The search endpoint returns documents matching a free-text query.

### Acceptance
- Given a populated index, when query "foo" is sent, then results contain documents with "foo" in title or body.

## REQ-SEARCH-0002
---
id: REQ-SEARCH-0002
revision: 2
status: reviewed
introduced: CHG-0043
supersedes: REQ-SEARCH-0001
phase: PHASE-5
tier: e2e
references:
  epic: EPIC-0010
  story: STORY-0034
  adrs: []
---

### Description
The search endpoint applies caller-scoped permissions before returning hits.

### Acceptance
- Given a user without read access, when they query, then their results exclude the unauthorized documents.
