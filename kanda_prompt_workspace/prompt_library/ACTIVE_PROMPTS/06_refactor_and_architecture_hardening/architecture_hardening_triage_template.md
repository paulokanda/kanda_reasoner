# Architecture Hardening Triage Record Template

Prompt code: `KPR-06-006`
Prompt id: `architecture_hardening_triage_template`
Version: 2.0.0
Status: `draft_template`
Load type: `explicit_on_request`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this draft-only template to record one source-grounded architecture
hardening triage. It is not an active hardening protocol and does not authorize
source changes, delivery, validation claims, or freeze writes.

Use `KPR-06-005 architecture_hardening_triage_protocol` for the governing
triage method.

## Required identity

```text
Record type: CONCEPTUAL / SOURCE_GROUNDED / IMPLEMENTATION_CANDIDATE
Project root:
Project name:
Selected target:
Target relative path:
Source SHA-256 or current fingerprint:
Source byte length when relevant:
Operation identity:
Lifecycle generation:
Evidence timestamp:
```

## Ownership and boundary record

```text
Primary box:
Canonical owner:
Allowed files:
Out-of-scope files:
Supporting touches:
Public contracts:
Private boundaries:
Tool root:
Project source root:
Project Support root:
Transient root:
```

## Evidence record

```text
Current architecture finding:
Exact source locations:
Runtime or test evidence:
Architecture-validator evidence:
Relevant frozen behavior:
Relevant Error Memory lessons:
Current validators and coverage:
Generated-artifact provenance:
Disconfirming evidence searched:
Unknown evidence:
```

## Classification

Choose one:

```text
HARD_FAILURE
PROTECTION_GAP
TRANSITIONAL_DEBT
WARNING
NOT_APPLICABLE
```

Classification reason:

## Response comparison

```text
No-change option:
Current-validator repair:
Owner-local repair:
Boundary or facade repair:
Narrow shielding option:
Bounded refactor option:
Deferred-debt option:
Selected smallest response:
Rejected broader responses:
```

## Validation and continuity

```text
Required focused validators:
Required regression validators:
Rollback obligation:
Durable evidence destination:
Freeze impact:
Current blockers:
```

## Authorization

```text
Brick Wall implementation authorization: NOT GRANTED / GRANTED SEPARATELY
May write source: NO / YES BY SEPARATE AUTHORITY
May build a patch: NO / YES BY SEPARATE AUTHORITY
May claim validation: NO / YES FROM EXECUTED EVIDENCE
May freeze: NO / YES AFTER HUMAN CONFIRMATION
Next safe action:
```

Completing this record does not itself authorize any mutation.
