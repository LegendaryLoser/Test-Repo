# Login feature

Single-REQ valid spec used as a positive test fixture for spec_lint.

## REQ-AUTH-0001
---
id: REQ-AUTH-0001
revision: 1
status: draft
introduced: CHG-0001
supersedes: null
phase: PHASE-1
tier: unit
references:
  epic: EPIC-0001
  story: STORY-0001
  adrs: [ADR-0003]
---

### Description
The user must be able to log in with a valid email-password pair.

### Acceptance
- Given valid credentials, when login is invoked, then a session token is returned.

### Non-acceptance
- Password reset flow.

### Notes
- N/A.
