# Large Module Refactor Planning Record Template

Prompt code: `KPR-06-008`
Prompt id: `large_module_refactor_template`
Version: 4.0.0
Status: `draft_template`
Load type: `explicit_on_request`
Owner box: `06_refactor_and_architecture_hardening`
Aligned with: `KPR-06-007 large_module_refactor_protocol v9.0`

## Purpose

Use this draft-only template to record one source-grounded large-module
assessment and decomposition proposal. It does not define governing doctrine
and does not authorize source writes, delivery, validation claims, or freeze.

## Record identity

```text
Record type: CONCEPTUAL / SOURCE_GROUNDED / IMPLEMENTATION_CANDIDATE
Project root:
Project name:
Target relative path:
Source SHA-256:
Source byte length:
Current physical lines:
Operation identity:
Lifecycle generation:
Evidence timestamp:
```

## Ownership and contract

```text
Primary box:
Canonical owner:
Public facade:
Public names and aliases:
Known consumers:
Signatures and defaults:
Decorators and bases:
Serialized or CLI contracts:
GUI signals and lifecycle hooks:
Relevant frozen behavior:
Relevant Error Memory lessons:
```

## Verified trigger

```text
Above hard maximum:
Would exceed hard maximum after requested change:
Mixed responsibilities:
Dependency-direction defect:
Architecture or AST finding:
Other verified trigger:
Disconfirming evidence:
```

## Characterization

```text
Existing tests:
Missing characterization:
Semantic baseline cases:
Exception and message cases:
Side-effect cases:
Consumer import checks:
GUI real-widget requirements:
```

## Candidate responsibility islands

For each candidate:

```text
Candidate ID:
Responsibility:
Proposed owner path:
Reads:
Writes or mutable state:
Public-boundary effect:
Dependency direction:
Expected physical lines:
Focused validation:
Conflicts with other candidates:
```

## Architecture comparison

```text
Smallest in-place repair:
Facade plus one helper:
Facade plus multiple cohesive owners:
Package conversion option:
Defer option:
Selected architecture:
Rejected alternatives:
```

## Transformation and validation

```text
Ordered reversible steps:
Public API preservation plan:
Import compatibility plan:
Behavior-equivalence plan:
Touched-family line-count plan:
Box and No-Leak checks:
Focused validators:
Regression validators:
Rollback obligation:
Durable evidence destination:
```

## Authorization

```text
Brick Wall implementation authorization: NOT GRANTED / GRANTED SEPARATELY
May write source: NO / YES BY SEPARATE AUTHORITY
May build a patch: NO / YES BY SEPARATE AUTHORITY
May claim validation: NO / YES FROM EXECUTED EVIDENCE
May freeze: NO / YES AFTER HUMAN CONFIRMATION
Current blockers:
Next safe action:
```

Completing this record does not itself authorize implementation.
