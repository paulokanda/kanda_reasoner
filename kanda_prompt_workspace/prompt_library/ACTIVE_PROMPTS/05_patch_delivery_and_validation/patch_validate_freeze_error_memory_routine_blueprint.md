---
prompt_id: patch_validate_freeze_error_memory_routine_blueprint
prompt_code: KPR-05-005
title: Answer Validate Freeze Memorize Error Routine Blueprint
version: 2.0
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: prompt-audit-wave5a-patch-lifecycle-core-v1
---

# Answer, Validate, Freeze, Memorize Error Routine Blueprint

## Purpose

This prompt is a thin wrapper copied by the Show Project to AI
`Answer, Validate, Freeze, Memorize Error` button or loaded for equivalent user
intent. It classifies the incident, selects current owners, and states the safe
high-level sequence. Downstream owner prompts define all exact fields, commands,
markers, schemas, and terminal behavior.

## Incident classification

Select one primary incident:

- `STARTUP_DELIVERY_FAILURE`: first-prompt files, startup ZIP, source map, or
  generator failure;
- `PROJECT_HANDOFF_FAILURE`: Show Project to AI collector, JSON handoff, source
  archive, or second-prompt export failure;
- `PATCH_BUILD_OR_DELIVERY_FAILURE`: release packaging, ZIP contract, staging,
  installer, or receiver failure;
- `VALIDATION_FAILURE`: local or packaged validator failure, stale evidence, or
  missing success marker;
- `FREEZE_INTAKE_FAILURE`: freeze-hint merge, Preview, Confirm and Write, or
  startup freeze-context refresh failure;
- `ERROR_MEMORY_INTAKE_FAILURE`: lesson construction, validation, staging, or
  persistence failure.

Do not combine unrelated incidents into one correction release.

## Required identity

Resolve and report:

```text
RECOVERY ROUTINE IDENTITY
Project slug:
Tool root:
Active project root:
Same physical root: YES / NO
Project Support root:
Project-linked transient root:
Selected incident:
Exact failing artifact or command:
Current source or artifact fingerprint:
Last reliable marker:
May modify source: YES / NO
```

The transient work location is derived from the selected project as
`<project_drive>/<project_name>_delete_after_daily_work`; it never owns durable
truth. Exact staging and cleanup commands belong to the current delivery owner.

## Owner dispatch

- Startup delivery: load the startup-maintenance guard, generator source map,
  generator, current delivery artifacts, and startup validation owner.
- Project handoff/export: load exact collector/export source, manifest, current
  handoff evidence, `project_tool_boundary_canon`, and relevant validator.
- Patch delivery: load Brick Wall, `bundle_gated_development_workflow`,
  `implementation_and_delivery_protocol`,
  `pre_output_contract_gates`, `pre_output_contract_gates`, and
  `patch_install_delivery_error_register`.
- Terminal output: load `terminal_cleanup_contract`.
- Freeze: load `freeze_code_intake_and_form_protocol` and current active freeze
  context. Preview remains read-only; writing requires explicit human Confirm
  and Write after successful local validation.
- Error Memory: load the current Error Memory intake owner and templates only
  when a verified recurring error is being admitted.

## Safe sequence

```text
diagnose exact failure
-> verify current source and relevant Error Memory
-> obtain Brick Wall and specialist authorization
-> repair the smallest owner
-> build or regenerate through the canonical owner
-> validate the exact final artifact contract
-> deliver with receiver and terminal contracts
-> install in the user's live project when required
-> execute current local validation
-> conditionally prepare freeze intake
-> conditionally prepare Error Memory intake
```

Each arrow is conditional. Do not invent validation evidence, combine a failed
phase with a later success marker, auto-freeze, or auto-memorize an error.

## Fail-closed response

```text
RECOVERY ROUTINE BLOCKED
Incident:
Missing exact source or artifact:
Missing owner or validator:
Unresolved fingerprint or identity:
Last reliable evidence:
May build patch: NO
May claim validation: NO
May freeze: NO
May stage Error Memory: NO
Next safe action:
```

## Button integration

The GUI owns button placement, label, clipboard behavior, and user feedback. The
button copies this canonical file from the selected project root. This prompt
does not define GUI code.

## Non-authorization statement

This wrapper does not authorize implementation, patch release, validation,
freeze, or Error Memory persistence.

## Version history

- 2.0: converted to a true incident-classification and owner-dispatch wrapper;
  removed copied PowerShell, freeze-form, and Error Memory schema doctrine.
- 1.x: historical combined answer/install/validate/freeze/memorize routine.
