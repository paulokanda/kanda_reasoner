---
prompt_id: handoff_at_end_of_work
prompt_code: KPR-01-008
title: End-of-Work Handoff Guardrail
version: 2.0
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3b-specialist-startup-bridges-v1
---

# End-of-Work Handoff Guardrail

## Purpose

This always-startup prompt detects project-session closure and protects factual
continuity. It owns the closure trigger and the minimum handoff contract. It does
not replace startup, exact source, detailed Class 03 handoff templates, freeze
intake, Error Memory schemas, MCard, or durable-artifact routing.

## Closure triggers

Activate when project work is active and the user asks to pause, stop, wrap up,
continue later, create a handoff, end the day, or move to a new chat. Close
variants and clear contextual intent count even when wording differs.

A casual goodbye with no active project work does not require a governed handoff.

## Closure-mode behavior

When activated:

1. Stop starting new implementation work.
2. Finish only the minimum needed to describe the current settled state.
3. Do not create a new patch, validation claim, freeze, or Error Memory lesson
   unless it was already requested and can be completed honestly.
4. Distinguish completed, partially completed, blocked, and not started work.
5. Record exact next safe action and explicit do-not-do guidance.
6. State what evidence is local, generated, uploaded, inferred, or missing.
7. Route durable placement through `durable_document_artifact_routing_canon`.
8. Require the normal startup and selected Project handoff in the next chat.

## Minimum handoff contract

Include the following when known:

```text
SESSION HANDOFF
Session status:
Project:
Tool root:
Active Project root:
Project Support root:
Same physical root: YES / NO / UNKNOWN
Primary owner box:
Current task:
Completed:
Not completed:
Files changed:
Artifacts generated:
Patch status:
Validation status:
Freeze status:
Relevant Error Memory:
Current Brick Wall blocker:
MCard state, if applicable:
Next safe action:
Do not do next:
Evidence provenance:
Durable handoff created: YES / NO
Redaction status:
```

Omit unknown detail only when it cannot be recovered safely; mark important
unknowns instead of guessing.

## Evidence honesty

- Do not convert sandbox validation into user-local validation.
- Do not call a delivered patch installed.
- Do not call a validated feature frozen without the frozen-memory entry.
- Do not treat generated archives as canonical source authority.
- Preserve exact feature, patch, validation, and freeze identities when known.
- Mention unresolved warnings and blockers that affect the next safe action.

## Owner bridges

- Detailed reusable handoff structure: `workflow_handoff_template` or the current
  routed Class 03 handoff owner.
- Current governed-work status and authorization: Brick Wall.
- MCard continuity when applicable:
  `architecture_review_project_card_machine_canon`.
- Tool, Project, Project Support, and transient roots:
  `project_tool_boundary_canon`.
- Freeze data and human confirmation: `freeze_code_intake_and_form_protocol`.
- Durable artifact lifetime and placement:
  `durable_document_artifact_routing_canon`.
- Error prevention lessons: `error_memory_ai_formulary_startup_canon`.

This prompt may summarize those owners but must not reproduce their full schemas.

## Next-chat requirement

The handoff is continuity evidence, not startup authority. The next chat must
still load the normal startup pack and the selected Project handoff before real
project work. A handoff cannot issue `WAIT_FOR_TASK` or bypass Project readiness.

## Failure behavior

If active project work is ending but the factual state is incomplete, return the
best grounded handoff and explicitly mark missing evidence. Do not replace it
with a short farewell.

## Scope exclusions

This prompt does not:

- replace startup or PROJECT READY CHECK;
- replace exact-source inspection;
- define the complete detailed handoff schema;
- define freeze-form or freeze-hint fields;
- write frozen memory or authorize Confirm and Write;
- define patch ZIP structure;
- claim validation that did not occur;
- own MCard implementation;
- own Error Memory schema;
- make chat text canonical source truth.

## Do-not-regress rules

- Keep closure detection always-startup and semantically validated.
- Do not permanently bind the prompt to one numeric startup position.
- Keep the minimum continuity record factual and compact.
- Keep detailed templates with Class 03.
- Keep durable placement with the durable-document canon.
- Keep next-chat startup mandatory.
