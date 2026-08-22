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
source changes, delivery, validation claims, or snapshot/freeze writes.

Use `KPR-06-005 architecture_hardening_triage_protocol` for the governing
triage method.

## Project-agnostic operating rule

This prompt defines standalone Project engineering logic. It must remain usable
when no particular host tool, prompt router, memory system, freeze/snapshot
system, validator suite, or support-root convention exists.

- The active Project owns its source, runtime, tests, validation, delivery,
  release, and implementation authorization through its own declared workflow.
- Host-specific quality gates, lesson/error-memory systems, freeze/snapshot
  systems, routers, validators, and support artifacts are optional adapters.
  Their absence must not block this prompt's technical reasoning.
- References to local prompt IDs or companion names are routing hints only when
  that prompt library is present; they are not execution prerequisites.
- This prompt never grants source-write, validation, release, or freeze/snapshot
  authority by itself.

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
Relevant Project error/lesson records, if available:
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
Snapshot/freeze impact, if applicable:
Current blockers:
```

## Authorization

```text
Project implementation authorization: NOT GRANTED / GRANTED SEPARATELY
May write source: NO / YES BY SEPARATE AUTHORITY
May build a patch: NO / YES BY SEPARATE AUTHORITY
May claim validation: NO / YES FROM EXECUTED EVIDENCE
May write snapshot/freeze state: NO / YES ONLY THROUGH THE PROJECT OR HOST-SPECIFIC CONFIRMATION CONTRACT
Next safe action:
```

Completing this record does not itself authorize any mutation.
