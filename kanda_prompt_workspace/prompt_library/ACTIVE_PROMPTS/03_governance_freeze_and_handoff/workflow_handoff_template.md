---
prompt_id: workflow_handoff_template
prompt_code: KPR-03-006
title: Generic Workflow Handoff Profile Template
version: 2.0
status: draft_template
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: prompt-audit-wave4a-governance-freeze-handoff-v1
---

# Generic Workflow Handoff Profile Template

## Purpose

Use this Project-agnostic draft template when a Project has no current generated handoff owner. If the host environment provides a dedicated session-closure or handoff exporter, that host-specific owner may supersede this draft template.

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

## Draft handoff profile

```text
WORKFLOW HANDOFF
Project:
Tool root:
Active Project root:
Project Support root:
Current task:
Requested outcome:
Verified completed work:
Changed source files:
Generated artifacts:
Validation actually executed:
Exact validation results:
Installation state:
Snapshot/freeze state, if applicable:
Known warnings or failures:
Unresolved decisions:
Protected paths and do-not-regress rules:
Next safe action:
Required next-session files or evidence:
Claims not yet proven:
```

## Rules

1. Report only observed or validated facts.
2. Separate completed, attempted, failed, pending, and not-applicable work.
3. Include exact source and artifact identities when they matter.
4. Preserve failure evidence and unresolved blockers.
5. Distinguish Tool, Active Project, Project Support, and transient paths.
6. Do not treat chat memory as durable evidence.
7. Do not claim install, validation, snapshot/freeze, or lesson-memory completion without
   the corresponding current evidence.
8. Keep the next action bounded and executable.
9. Redact secrets and unnecessary personal data.
10. Route any permanent handoff schema or exporter change through its current
    source owner and Class 07 insertion governance.

## Authority boundary

This template drafts text. It does not write source, generate an official host handoff package, update governance, authorize implementation, merge evidence, or write snapshot/freeze memory.
