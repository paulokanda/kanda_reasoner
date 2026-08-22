---
prompt_id: implementation_roadmap_builder
prompt_code: KPR-05-004
title: Implementation Roadmap Builder - Draft Template
version: 2.0
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: prompt-audit-wave5a-patch-lifecycle-core-v1
---

# Implementation Roadmap Builder - Draft Template

## Purpose

Create a non-authoritative roadmap draft when the human explicitly asks for a
roadmap, checklist, or progress-tracking template. This prompt does not own the
Project implementation plan, implementation-authority status, durable handoff, release
lifecycle, validation evidence, or source-write authorization.

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

## Use when

- a conceptual sequence would help compare or communicate work;
- current source has been inspected and the user wants a source-grounded draft;
- an already authorized release needs a presentation-oriented task list;
- the user wants an optional human-managed tracker.

Do not auto-load for normal implementation. Do not use when the active Project's implementation authority, a
specialist plan, or a current handoff already provides the required state.

## Evidence first

Use evidence already supplied in the current task before asking questions.
Record missing facts and assumptions explicitly. Ask only when a material
ambiguity cannot be resolved from available source or context.

Roadmap types:

- `CONCEPTUAL`: no exact source or execution claim;
- `SOURCE_GROUNDED`: exact current files and owners inspected;
- `RELEASE_READY_DRAFT`: current authorization, package boundaries, and
  validators identified, but execution remains separate.

## Adaptive roadmap format

```text
IMPLEMENTATION ROADMAP DRAFT
Roadmap type:
Requested outcome:
Verified current state:
Evidence inspected:
Assumptions:
Primary owner:
Supporting owners:
Dependencies:
Risks:

STEP
Step ID:
Outcome:
Owner:
Exact files or artifacts:
Preconditions:
Action:
Validation or review evidence:
Rollback or rejection condition:
Check-in suggested: YES / NO
Status: NOT_STARTED / IN_PROGRESS / BLOCKED / EVIDENCED

Unresolved decisions:
Next safe action:
Authority source:
Freshness timestamp or source fingerprint:
```

Use as many or as few phases as the task requires. Do not force a seven-phase
model, branch, production merge, fixed item count, or two-step response limit.

## Optional tracker

A tracker is a human convenience, not execution truth. Checkboxes, percentages,
and self-reported completion do not prove source changes, tests, validation, or
snapshot/freeze state. Bind the tracker to a source fingerprint or evidence date and mark it
stale when project, source, operation, validator, or requirements change.

## Boundaries

- The active Project's declared implementation owner owns current implementation authority and gate status.
- Cooperative Implementation Methodology owns consequential option comparison.
- Specialist prompts own technical plans.
- Current handoff owners own durable continuation state.
- Bundle-Gated Workflow owns installable-release lifecycle when applicable.
- Validation owners own actual PASS/FAIL evidence.

Do not include secrets, personal data, credentials, or unredacted production
records in a roadmap.

## Non-authorization statement

This template cannot authorize source writes, release delivery, validation
claims, or snapshot/freeze writes.

## Version history

- 2.0: reclassified as an explicit draft-only template with adaptive structure
  and freshness-bound optional tracking.
- 1.x: historical prescriptive implementation tracker.
