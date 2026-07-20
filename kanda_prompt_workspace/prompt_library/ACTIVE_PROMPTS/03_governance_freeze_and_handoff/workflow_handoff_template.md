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

Use this Project-agnostic draft template only when a new or external Project has
no current generated handoff owner. Normal KANDA session closure remains owned
by `handoff_at_end_of_work` and the current Project handoff exporter.

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
Freeze state:
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
7. Do not claim install, validation, freeze, or Error Memory completion without
   the corresponding current evidence.
8. Keep the next action bounded and executable.
9. Redact secrets and unnecessary personal data.
10. Route any permanent handoff schema or exporter change through its current
    source owner and Class 07 insertion governance.

## Authority boundary

This template drafts text. It does not write source, generate the official KANDA
handoff package, update governance, authorize implementation, merge evidence, or
write freeze memory.
