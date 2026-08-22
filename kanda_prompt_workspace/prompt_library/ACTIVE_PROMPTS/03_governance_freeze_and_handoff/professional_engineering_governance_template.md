---
prompt_id: professional_engineering_governance_template
prompt_code: KPR-03-005
title: Professional Engineering Governance Profile Template
version: 2.0
status: draft_template
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: prompt-audit-wave4a-governance-freeze-handoff-v1
---

# Professional Engineering Governance Profile Template

## Purpose

Use this draft-only template to design a Project-specific engineering governance
profile when no current profile exists. It records Project choices and routes to
existing engineering canons. It does not create a parallel implementation-quality gate, Box canon, root/ownership model, delivery protocol, or snapshot/freeze system.

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

## Draft profile

```text
PROJECT ENGINEERING GOVERNANCE PROFILE
Project name:
Project root:
Project Support root:
Project purpose:
Primary runtime or product surfaces:
Risk classes relevant to this Project:
Current global canons adopted:
Project-specific constraints:
Protected milestones or interfaces:
Required validation families:
Required human approvals:
Durable evidence owners:
Known exclusions:
Review date:
Profile status: DRAFT / REVIEWED / ACTIVE_BY_GOVERNED_INSERTION
```

## Authoring rules

1. Inspect current source, manifests, tests, and frozen Project memory first.
2. Reference global canons by stable prompt ID; do not copy their full rules.
3. Record only Project-specific choices that are not already globally owned.
4. Distinguish preference, constraint, verified invariant, and historical note.
5. Define measurable validation evidence for every Project-specific hard rule.
6. Preserve unknowns instead of inventing policy.
7. Route insertion and registration through Class 07 governance.
8. Require the active Project's declared implementation authorization before any profile-driven implementation.

## Prohibited content

Do not embed:

- a second Q01-Q40 checklist;
- generic Box, NO_LEAK, host/Project ownership, observed-target lifecycle, patch, terminal, or snapshot/freeze rules;
- machine path formulas owned elsewhere;
- claims that the profile authorizes coding;
- application-specific secrets or personal data.

## Output boundary

This prompt produces a draft profile only. The draft has no source mutation,
implementation, validation, delivery, or snapshot/freeze authority. A governed insertion
release must assign its final identity, metadata, location, routes, validators,
and lifecycle status.
