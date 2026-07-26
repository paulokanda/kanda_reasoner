---
prompt_id: router_bridge_patch_delivery_contract
title: Router Bridge Patch Delivery Contract
version: 5.0
status: deprecated
load_type: never
active_route: false
owner_group: 05_patch_delivery_and_validation
created_by_patch: kanda-router-bridge-no-isolated-zip-gate-v1
---
# DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE

This file is not an active KANDA owner and must never be loaded for current
work. Current authority is `pre_output_contract_gates`. Trigger aliases are preserved in
`prompt_substitution_map.md` and current routing indexes.

The historical contract below remains only because frozen validators and old
release provenance still inspect exact compatibility markers. It cannot
authorize implementation, delivery, validation, freeze, Error Memory, or any
source write.

---

# Router Bridge Patch Delivery Contract

## Purpose

Use this routed bridge whenever the next response may deliver, mention, or link an installable patch ZIP, installer block, validation block, patch release instructions, `KANDA_FREEZE_HINT.json`, Error Memory intake for a delivered correction, implementation-time error correction, or a freeze-ready patch.

This bridge closes the isolated-ZIP failure mode. A ZIP is only the payload. Patch delivery is complete only when the user receives the payload plus placement, install, validation, expected markers, freeze/Error Memory handling, and beginner-safe warnings in the same response.

## Implementation-time Error Memory companion rule

If the patch corrects an error that occurred while the AI was implementing code, editing prompts, building a ZIP, validating, installing, preparing freeze evidence, or repairing a delivery mistake, Error Memory handling is not optional. The delivery must classify the Error Memory receiver and prove that the installer stages the receive-ready lesson into the Error Memory tab pending intake folder:

```text
<project_drive>:\<project_name>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
```

The lesson file must be marker-wrapped with `KANDA_ERROR_LESSON_JSON_BEGIN` and `KANDA_ERROR_LESSON_JSON_END`, must validate as active-ready or draft according to available evidence, and must not be written directly into Lessons. The Error Memory tab review and `Memorize Error` click remain human-controlled.

If no durable lesson is appropriate, the response must say `Error Memory payload: N/A` and give a specific reason. A generic omission is a bridge failure.

## First hard gate: dynamic daily-work containment

When this bridge is active, the AI must remember this before drafting any patch, installer, validation, correction, freeze-intake, or Error Memory delivery text:

```text
All transient delivery artifacts must be created, staged, extracted, corrected, updated, or consumed only under:

<drive>:\<project_name>_delete_after_daily_work\

This includes patch ZIP staging copies, extracted patch folders, install helpers, temporary files, correction files, validation helper files, patch helper files, transient manifests, one-use README files, and temporary copies of freeze or Error Memory payloads.

The active project root may receive only real intended project files that belong in the project. Governed persistent freeze-intake and Error Memory intake files must use their canonical project-specific intake folders, not the active project root.
```

This is a bridge-level enforcement of existing canon, not a new prompt canon. If an answer would place transient install, temp, correction, patch, validation-helper, or one-use delivery files in the active project root, the bridge must fail closed and the answer must be repaired before any ZIP link, install block, validation block, or freeze metadata is emitted.




<!-- RECEIVER_DELIVERY_BRIDGE_ENFORCEMENT_V1_START -->
## Receiver delivery bridge enforcement - v1

This bridge already enforces ZIP delivery, dynamic daily-work staging, freeze
handling, and Error Memory handling. The receiver bridge adds the missing
output-time proof: the artifact must reach the actual KANDA receiver that will
consume it.

Before emitting any ZIP, freeze form, Error Memory lesson, governance intake
bundle, or receiver-ready text, classify the receiver as exactly one of:

```text
SOURCE_PATCH
FREEZE_HINT_INTAKE
MANUAL_FREEZE_FORM_RECEIVER
ERROR_MEMORY_AI_ASSISTED_INTAKE
STORAGE_ONLY_MANUAL_HELPER
```

Add a visible block when a ZIP or governance intake artifact contains freeze or
Error Memory payloads:

```text
RECEIVER DELIVERY CHECK
Receiver classification:
Actual receiver path or action:
Installer stages to receiver: YES / NO / MANUAL
Manual paste required: YES / NO
Storage-only helper: YES / NO
Receiver proof:
RECEIVER STATUS: PASS / FAIL
```

Hard rules:

1. A ZIP that only extracts receiver-ready text under `<drive>:\<project>_delete_after_daily_work\...` is not an installed freeze or Error Memory intake. It is `STORAGE_ONLY_MANUAL_HELPER` unless the install block copies the payload into a real KANDA intake folder.
2. An Error Memory ZIP is operational only when the installer stages an active-ready lesson into `<project_drive>\<project_name>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake`. If it does not, label it manual/storage-only and do not call it Error Memory intake installation.
3. A freeze form ZIP is operational only when it updates a real freeze-hint intake record or the response explicitly says the user must paste the marker-wrapped form into the Freeze Feature manual receiver. A file sitting in daily-work is not proof that New Local Freeze Entry consumed it.
4. A freezeable source patch must keep using the normal root-level `KANDA_FREEZE_HINT.json` sidecar route and must stage the sidecar under `<project_drive>\<project_name>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake`.
5. Do not validate a receiver bundle only by checking that JSON files exist in the ZIP. Validation must check either the real receiver staging path or the explicit `STORAGE_ONLY_MANUAL_HELPER` / manual-paste classification.

Failure text:

```text
CONTRACT NOT MET - RECEIVER DELIVERY BLOCKED
```

Use this failure when the response cannot prove which receiver will consume the artifact.
<!-- RECEIVER_DELIVERY_BRIDGE_ENFORCEMENT_V1_END -->

## Trigger phrases

Route here for requests or situations containing any of the following:

```text
patch ZIP
send zip
deliver zip
download patch
install patch
validation code
PowerShell install
KANDA_FREEZE_HINT.json
freeze-ready patch
Error Memory intake
user says the AI forgot install code
user says the AI delivered an isolated ZIP
implementation error while coding
AI detected an implementation error
patch validation failed during implementation
install failed during implementation
```

## Required companion prompts

Load or apply the smallest complete set:

```text
implementation_and_delivery_protocol
pre_output_contract_gates
freeze_code_intake_and_form_protocol, when the patch can be frozen later
patch_install_delivery_error_register
error_memory_active_ready_correction_blueprint, when the delivery includes or corrects Error Memory lesson intake
error_memory_active_ready_json_template, when the delivery includes text for the Error Memory tab AI-assisted intake receiver
error_memory_model_template, after error_memory_active_ready_json_template for field-by-field lesson construction
project_tool_boundary_canon, when project root or tool/project identity matters
```

Do not load the entire prompt library. Do not use this bridge for simple explanation-only responses that do not emit a patch artifact or terminal instructions.

## Mandatory Patch Delivery Gate

Before a ZIP link appears, the answer must include this visible gate with truthful values:

```text
PATCH DELIVERY GATE
ZIP purpose:
ZIP placement path:
What this ZIP is:
What this ZIP is not:
Install code present: YES / NO
Validation code present: YES / NO
Expected validation markers:
Changed files:
Allowed write paths:
Forbidden write paths:
Freeze/freeze-intake:
Error Memory payload:
Post-validation steps:
What not to do:
Beginner-safe: YES / NO
GATE STATUS: PASS / FAIL
```

Hard rule:

```text
No ZIP link may appear unless GATE STATUS is PASS.
```

If any required item is unknown, missing, not yet validated, or unsafe, output:

```text
CONTRACT NOT MET - PATCH DELIVERY BLOCKED
```

and do not show the ZIP link.

## Install and validation requirements

The same response as the ZIP link must include user-facing terminal code:

1. Install PowerShell code.
2. Validation PowerShell code.
3. Expected validation markers.
4. What to paste back if validation fails.

Install code must follow the project root-to-staging rule:

```text
<drive>:\PATCH_NAME.zip -> <drive>:\<project>_delete_after_daily_work\PATCH_NAME.zip -> extract staged ZIP -> install changed files only
```

The install block must dynamically compute the daily-work folder from the active project root and create it if missing. All transient helper files, extracted files, correction files, patch helper files, and validation helper files must remain inside that daily-work folder. Do not put these files in the active project root.

Do not use Downloads/Desktop search fallbacks.

## Freeze and Error Memory handling

For freezeable patches, include a root-level `KANDA_FREEZE_HINT.json` in the ZIP and explain that the freeze entry is written only after local validation and explicit human confirmation.

For user-detected AI mistakes, include or stage an Error Memory intake payload. Do not end with apology-only text when the mistake requires a governed correction.

When the response asks AI to create or correct Error Memory lesson text for the **Error Memory tab -> AI-assisted error lesson intake** receiver, the bridge must route to and include the active-ready intake templates in this order:

```text
error_memory_active_ready_json_template
error_memory_model_template
```

The copied/requested AI payload must tell AI to return exactly one marker-wrapped `KANDA_ERROR_LESSON_JSON_BEGIN` / `KANDA_ERROR_LESSON_JSON_END` block, replace every placeholder with concrete evidence, and avoid invented validation evidence.

## Beginner-safe rendering rule

Assume the user can copy and paste terminal blocks but should not have to guess what a ZIP is, where to place it, whether to unzip manually, or how to validate the result. Say what the ZIP is not, what not to do, and what success markers to look for.

## Do-not-repeat rules

```text
Do not deliver a patch ZIP as an isolated artifact.
Do not put the ZIP link before the Patch Delivery Gate.
Do not omit install code.
Do not omit validation code.
Do not claim local validation from sandbox validation.
Do not install root-level KANDA_FREEZE_HINT.json as source code.
Do not skip Error Memory intake for user-detected AI mistakes.
Do not write transient install, temp, correction, patch, validation-helper, one-use delivery, or staging files into the active project root.
```

<!-- RECEIVER_DELIVERY_BRIDGE_ENFORCEMENT_V2_START -->

## Receiver delivery bridge enforcement - v3 hardening

Apply this before any ZIP, freeze form, governance intake bundle, manual receiver
bundle, or Error Memory lesson is shown.

V2 keeps the existing receiver classifications and adds hard proof requirements:

```text
SOURCE_PATCH
FREEZE_HINT_INTAKE
MANUAL_FREEZE_FORM_RECEIVER
ERROR_MEMORY_AI_ASSISTED_INTAKE
STORAGE_ONLY_MANUAL_HELPER
```

### Hard receiver proof rules

- `ERROR_MEMORY_AI_ASSISTED_INTAKE` is valid only when the install block copies
  the active-ready lesson JSON into
  `<project_drive>\<project_name>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake`.
  Mentioning the path in prose is not enough.
- `FREEZE_HINT_INTAKE` is valid only when the install block copies root-level
  `KANDA_FREEZE_HINT.json` into
  `<project_drive>\<project_name>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake`
  or the validation block calls the approved merge helper for the current patch
  ZIP and feature ID.
- `MANUAL_FREEZE_FORM_RECEIVER` must set manual paste YES, installer stages NO,
  and must include the exact `KANDA_FREEZE_FORM_JSON_BEGIN` /
  `KANDA_FREEZE_FORM_JSON_END` receiver text.
- `STORAGE_ONLY_MANUAL_HELPER` must set storage-only YES, manual paste YES, and
  installer stages NO. It must not be described as installed intake.

### Schema proof rules

- Error Memory marker blocks must parse as JSON and satisfy the active-ready
  lesson schema, including `redaction` as an object, `redaction.applied: true`,
  `redaction.export_safe: true`, non-empty `redaction.rules`, and
  `regression_check.type: validation_command`.
- Manual freeze forms must parse as JSON and include `feature_title`,
  `primary_box`, `box_type`, `validated_files`, `generated_files`,
  `protected_paths`, `do_not_regress_rules`, `validation_evidence_summary`,
  `known_warnings`, `planned_next_step`, and `notes`.
- Manual freeze form `validation_evidence_summary` must include recognizable
  local validation markers: `VALIDATION OK: <feature_id>` and `STATUS: IN_SYNC`
  when local validation has completed.

### ZIP extraction safety rule

Install blocks that use `Expand-Archive` must validate ZIP member names before
extracting. Reject absolute paths, drive-prefixed names, empty names, null
characters, and `..` traversal segments. Use `System.IO.Compression.ZipFile` to
inspect entries before extraction.

If receiver proof, schema proof, or ZIP member safety proof is missing, output:

```text
CONTRACT NOT MET - RECEIVER DELIVERY BLOCKED
```

Do not show the ZIP link.

<!-- RECEIVER_DELIVERY_BRIDGE_ENFORCEMENT_V2_END -->

### Error Memory lesson archive-member rule - v3

For any delivered ZIP containing `project_error_memory/pending_ai_assisted_error_lesson_intake/KANDA_ERROR_LESSON_JSON_*`, the lesson file must contain complete `KANDA_ERROR_LESSON_JSON_BEGIN` and `KANDA_ERROR_LESSON_JSON_END` markers around the active-ready JSON object. Do not package raw JSON only. Validate the final ZIP with `scripts/validate_patch_zip.py` before sending the link.
