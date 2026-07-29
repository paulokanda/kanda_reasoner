---
prompt_id: patch_validate_freeze_error_memory_routine_blueprint
prompt_code: KPR-05-005
title: Answer Validate Freeze Memorize Error Routine Blueprint
version: 3.1
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: powershell-paste-safe-operational-output-v1
---

# Answer, Validate, Freeze, Memorize Error Routine Blueprint

## Purpose

This is the canonical continuation wrapper copied by the Show Project to AI
`Answer, Validate, Freeze, Memorize Error` button. It restores the complete
project release cycle after an AI stops at an answer, patch, install, validation,
Freeze, or Error Memory phase. It is also used when a prior phase failed.

This wrapper selects owners and enforces phase order. Exact PowerShell bodies,
ZIP schemas, Freeze fields, and Error Memory fields remain with their current
canonical owners.

## Button context envelope

The button must place a `KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT` envelope
before this prompt. Treat the envelope as current interaction identity and copy
its values into the routine record.

The envelope must identify:

```text
Selected project slug
Selected project source root
KANDA Reasoner tool root
Same physical root: YES / NO
Selected Project Support root
Selected project-linked transient root
Canonical prompt source
```

When the envelope is unavailable, resolve the same fields from the current
`PROJECT READY CHECK`, exact handoff, and `project_tool_boundary_canon` before
any source mutation or operational output.

## Hard Tool-versus-Project boundary

- The selected Project owns its source patch, install destination, live
  validation, Project Support, Freeze memory, and Error Memory.
- KANDA Reasoner owns the reusable prompt source and governance UI. It is not
  the selected Project merely because it created the handoff or receives Freeze
  and Error Memory intake.
- Do not patch KANDA Reasoner to repair an external Project release unless exact
  source proves a separate Tool defect and the Tool operation is independently
  authorized.
- If Tool and Project are the same physical root, keep their logical roles
  separate.
- Generated handoffs and source archives are evidence, not editing authority.

## Primary routine classification

Select one primary class:

- `ROUTINE_POST_IMPLEMENTATION_COMPLETION`: implementation or analysis exists,
  but ZIP delivery, install instructions, validation, synchronization, Freeze,
  Error Memory disposition, or final reporting is incomplete;
- `STARTUP_DELIVERY_FAILURE`;
- `PROJECT_HANDOFF_FAILURE`;
- `PATCH_BUILD_OR_DELIVERY_FAILURE`;
- `INSTALLATION_FAILURE`;
- `VALIDATION_FAILURE`;
- `FREEZE_INTAKE_FAILURE`;
- `ERROR_MEMORY_INTAKE_FAILURE`.

Do not combine unrelated defects into one correction release.

## Required routine identity

```text
ANSWER VALIDATE FREEZE MEMORIZE ROUTINE IDENTITY
Project slug:
Selected project source root:
KANDA Reasoner tool root:
Same physical root: YES / NO
Project Support root:
Project-linked transient root:
Canonical prompt source:
Selected routine class:
Feature ID:
Patch ZIP identity:
Project interpreter or interpreter-resolution owner:
Current source fingerprint:
Last reliable marker:
Already completed phases:
Next required phase:
May modify selected Project source: YES / NO
May modify KANDA Reasoner Tool source: YES / NO
```

A blank, stale, ambiguous, or conflicting identity blocks mutation and artifact
output.

## Mandatory owner dispatch

Apply the smallest current owner set needed for the remaining phases:

- identity: `project_tool_boundary_canon`;
- implementation admission: Brick Wall and the exact Box owner;
- release lifecycle: `bundle_gated_development_workflow`;
- payload, baseline, install transaction, and rollback:
  `implementation_and_delivery_protocol`;
- output-time release gate: `pre_output_contract_gates`;
- known delivery regressions: `patch_install_delivery_error_register`;
- terminal blocks: `terminal_cleanup_contract`;
- Freeze: `freeze_code_intake_and_form_protocol` and current active Freeze
  context;
- Error Memory admission: `error_memory_ai_formulary_startup_canon` and, when a
  candidate is justified, `error_memory_active_ready_correction_blueprint`,
  `error_memory_active_ready_json_template`, and `error_memory_model_template`.

Never load or depend on deprecated `router_bridge_patch_delivery_contract`.

## Continuation contract

Continue from the last reliable marker. Do not make the user retrain the AI or
repeat phases that already passed for the same exact feature and ZIP.

For every response, return:

```text
ROUTINE CONTINUATION STATE
Feature ID:
Exact ZIP or artifact identity:
Completed phases:
Last reliable marker:
Current blocked or active phase:
Next exact action:
User execution required: YES / NO
Need new training prompt: NO
```

If current evidence changes the feature, ZIP, source fingerprint, interpreter,
or Project identity, invalidate only the affected later phases.

## Paste-safe PowerShell hard gate

Every user-facing PowerShell code fence is one independent paste unit that must
start safely at a clean primary `PS ...>` prompt. Prefer a direct invocation of
a packaged `.ps1` script over an inline control-flow wrapper.

For interactive user-facing output:

- never emit `elseif`, `else`, or `finally`;
- never emit a standalone or separately pasted `catch`;
- never split `if/elseif/else` or `try/catch/finally` across code fences or
  console submissions;
- never tell the user to paste the remainder of a control-flow chain later;
- when a preflight is needed, use complete independent `if` checks or place the
  guarded logic inside the packaged script;
- require Windows PowerShell 5.1-compatible APIs unless PowerShell 7 or a newer
  runtime has been explicitly verified;
- use the exact artifact path produced by the current workflow instead of an
  assumed destination or placeholder path.

Before emitting a terminal block, scan the final visible code for detached
control-flow tokens and unsupported runtime APIs. If the block is not one safe
paste unit, repair it before output.

Existing Error Memory owners include
`lesson-powershell-detached-else-interactive-paste-footer-v1` and
`lesson-powershell-validation-wrapper-marker-and-finally-v1`; do not create
duplicate lessons for those failure classes.

## Safe end-to-end sequence

```text
answer the requested task from exact current source
-> obtain implementation authorization when source changes
-> repair the smallest selected-Project owner
-> build one self-contained patch ZIP
-> validate the exact final ZIP contract before showing its link
-> deliver the ZIP with SHA-256, placement, separate install code, separate
   validation code, expected markers, rollback, Freeze handling, and Error
   Memory disposition in the same response
-> user installs into the selected Project from project-linked transient staging
-> verify installed hashes and receipt identity
-> execute current local validation with the selected Project interpreter
-> distinguish native warnings from process exit-code failure
-> regenerate or validate Show Project synchronization when source, prompts,
   Freeze context, or Error Memory changed
-> require `VALIDATION OK: <feature_id>` and `STATUS: IN_SYNC`
-> merge current local validation evidence into the selected Project Freeze Hint
-> prepare read-only Preview; human performs explicit Confirm and Write
-> evaluate Error Memory eligibility and duplicates
-> prepare exactly one marker-wrapped lesson candidate only when justified;
   human validates and explicitly uses Memorize Error
-> return the completed user-facing answer and remaining next action
```

`INSTALL IS NOT VALIDATION`. Sandbox or package validation is not proof of the
user's live installation.

## Release delivery requirements

No ZIP link may be emitted alone. The same response must include truthful
release identity and all operational instructions required to continue.

A freezeable ZIP must contain one root-level `KANDA_FREEZE_HINT.json`, must not
install that sidecar as source, and must pass the current ZIP contract. Transient
ZIPs, extraction folders, helpers, receipts, and evidence belong under:

```text
<project_drive>/<project_name>_delete_after_daily_work
```

Install and validation commands must derive paths from the selected Project.
Do not use Downloads/Desktop fallback searches. Do not default to generic
`python` when the handoff or current Project defines a governed interpreter.

## Freeze rules

Freeze is eligible only after current local validation and synchronization.
Installation alone must not create completed Freeze evidence. Validation must
merge current markers into the current selected-Project Freeze intake record.
Preview remains read-only. Confirm and Write remains an explicit human action.
After writing, regenerate startup Freeze context.

## Error Memory rules

Create or correct a lesson only for a verified failure with durable, repeatable
prevention value after duplicate, overlap, supersession, and current-schema
checks.

Do not create a new lesson merely for a user selecting the wrong Project, a
skipped prerequisite, a correct fail-closed safeguard, a transient external
failure, or an incident already owned by an active lesson.

When an intake block is justified, use exactly one:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ one current-schema lesson object }
KANDA_ERROR_LESSON_JSON_END
```

Do not wrap it in a markdown fence. Do not invent validation evidence. Do not
write directly into canonical Lessons. Human validation and Memorize Error are
required.

## Fail-closed response

```text
ANSWER VALIDATE FREEZE MEMORIZE ROUTINE BLOCKED
Routine class:
Selected Project identity problem:
Missing exact source or artifact:
Missing owner or validator:
Unresolved fingerprint, interpreter, or ZIP identity:
Last reliable marker:
May build patch: NO
May show ZIP link: NO
May claim live validation: NO
May freeze: NO
May stage Error Memory: NO
Next safe action:
```

## Button integration

The GUI owns the resolved identity envelope, clipboard behavior, label, tooltip,
and user feedback. The canonical prompt is read from the KANDA Reasoner Tool
root; the selected external Project does not become prompt-library authority.

## Non-authorization statement

This wrapper does not itself authorize implementation, release, validation
claims, Freeze writes, or Error Memory persistence.

## Version history

- 3.1: added a paste-safe PowerShell hard gate, Windows PowerShell 5.1 compatibility, exact artifact-path use, and existing Error Memory owner enforcement.
- 3.0: added cross-project identity envelope, post-implementation completion,
  no-retraining continuation state, complete ZIP/install/validate/sync/Freeze/
  Error Memory sequence, and EEG Kanda regression protections.
- 2.0: converted the historical mega-prompt to an owner-dispatch wrapper.
- 1.x: historical combined routine.
