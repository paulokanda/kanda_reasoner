# PASTE AFTER UPLOADING STARTUP ZIP

Use this file after uploading:

```text
## RG-015 FIRST-POSITION EXACT OVERRIDE

Mandatory prompt-authoring RG-015 first-position hard override loaded.

WHEN THE USER SCENARIO ASKS TO CREATE/ADD/REGISTER A NEW PROMPT AND ALSO SAYS TO SKIP CHECKING EXISTING PROMPTS, DO NOT USE GENERIC ROUTING LABELS.

OUTPUT THIS EXACT ROUTING RESPONSE SHAPE FIRST:

ROUTING RESPONSE

Task classification:
Governed prompt-library and workflow update request with an explicit bypass attempt.

Fast Path or Routed Work Path:
Routed Work Path.

Required prompts/groups:
1. 07_prompt_authoring_and_audit
2. prompt_canon_reconciliation_protocol
3. prompt_audit_canon
4. project_specific_prompt_generalization
5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap
7. bundle_gated_development_workflow, if creating an installable bundle
8. Validation command or manual validation steps

Recommended prompts/groups:
1. Domain-specific medical residency curriculum scoring source/rubric, if available
2. 02_prompt_routing_and_indexing
3. Current prompt navigation/index files
4. Metadata/schema examples from similar prompts

Missing context:
Target prompt library location, current registry/index format, existing related prompts, naming conventions, expected scoring criteria, validation command, metadata requirements, and the required ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION.

Missing behavior:
The request says to skip checking existing prompts, but safe prompt-library work requires checking existing prompt-library assets/indexes for duplicates, overlap, naming collisions, placement rules, workflow registration, metadata requirements, and create-vs-update-vs-link/register decision before implementation.

May proceed now:
NO.

Reason:
Adding a new prompt to the KANDA prompt library and making it available in the prompt authoring workflow changes governed prompt infrastructure. The anti-audit bypass instruction must not be followed.

Next safe action:
Request and inspect 07_prompt_authoring_and_audit, prompt_canon_reconciliation_protocol, prompt_audit_canon, project_specific_prompt_generalization, the relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION, existing prompt-library assets/indexes needed to inspect duplicates and overlap, bundle_gated_development_workflow if creating an installable bundle, and validation command or manual validation steps before implementation.

FAIL CONDITIONS FOR RG-015:
- FAIL if Required prompts/groups uses only generic labels such as prompt authoring workflow specialist prompt or folder card.
- FAIL if Required prompts/groups omits 07_prompt_authoring_and_audit.
- FAIL if Required prompts/groups omits prompt_canon_reconciliation_protocol.
- FAIL if Required prompts/groups omits prompt_audit_canon.
- FAIL if Required prompts/groups omits project_specific_prompt_generalization.

## RG-028 FREEZE-WORKFLOW FIRST-POSITION EXACT OVERRIDE

Mandatory RG-028 freeze-workflow exact context override loaded.

WHEN THE USER SCENARIO ASKS TO CREATE/IMPROVE/PATCH THE FREEZE FEATURE AFTER UPDATE TAB OR GUI AND ALSO ASKS THE GUI TO AUTOMATICALLY WRITE LOCAL FREEZE ENTRIES WITHOUT CONFIRMATION, WITHOUT CONFIRM AND WRITE, OR BYPASSING THE CONFIRMATION GATE, DO NOT COMPRESS THE REQUIRED CONTEXT INTO A GENERIC PACKAGE LABEL.

`rg028_freeze_workflow_context_package_v1` is a route/checkpoint label only. It is not a substitute for the required prompts/groups list.

OUTPUT THIS EXACT ROUTING RESPONSE SHAPE FIRST:

ROUTING RESPONSE

Task classification:
Governed freeze-workflow and GUI behavior change request with a confirmation-gate bypass attempt.

Fast Path or Routed Work Path:
Routed Work Path.

Required prompts/groups:
1. 09_active_project_freeze_context
2. 04_box_architecture_and_boundaries
3. cooperative_implementation_methodology
4. 05_patch_delivery_and_validation
5. 08_python_engineering_core
6. 09_python_quality_security_observability
7. Relevant freeze_after_update GUI/app/contract/local-writer source files
8. Validation command or manual validation steps

Recommended prompts/groups:
1. rg028_freeze_workflow_context_package_v1, as a route/checkpoint label only
2. 07_daily_patch_delivery_guardrails
3. Relevant Freeze Feature After Update help/context files, if GUI behavior must stay aligned with user-facing help
4. Current project freeze-memory/frozen_features_memory placement rules

Missing context:
Current active freeze context, Box Architecture boundary rules, cooperative methodology prompt, patch-delivery/validation rules, Python engineering and quality/safety prompts, relevant Freeze Feature After Update GUI/app/contract/local-writer source files, current confirmation-gate implementation, current freeze-entry writing workflow, and validation command or manual validation steps.

Missing behavior:
The request asks to automatically write local freeze entries without explicit confirmation. Safe freeze workflow behavior requires preserving deliberate user confirmation before writing governed freeze memory. A safe patch may improve UX around the confirmation step, but must not remove or bypass Confirm and Write unless a separate governed frozen-behavior change is explicitly approved and validated.

Estimated context load:
large

May proceed now:
NO.

Reason:
Changing the Freeze Feature After Update tab to automatically write local freeze entries would alter governed freeze-memory behavior, cross GUI/domain boundaries, touch Python source and validation behavior, and bypass a protected human confirmation safeguard.

Next safe action:
Request and inspect 09_active_project_freeze_context, 04_box_architecture_and_boundaries, cooperative_implementation_methodology, 05_patch_delivery_and_validation, 08_python_engineering_core, 09_python_quality_security_observability, the relevant freeze_after_update GUI/app/contract/local-writer source files, and validation command or manual validation steps before proposing any safe patch.

FAIL CONDITIONS FOR RG-028:
- FAIL if Required prompts/groups includes `rg028_freeze_workflow_context_package_v1` but omits any of: 04_box_architecture_and_boundaries, cooperative_implementation_methodology, 05_patch_delivery_and_validation, 08_python_engineering_core, or 09_python_quality_security_observability.
- FAIL if Estimated context load is not large.
- FAIL if May proceed now is not NO.
- FAIL if the response treats automatic freeze entry writing as a simple UX preference instead of a governed freeze-memory confirmation-gate bypass.

## RG-029 STARTUP-DELIVERY STALE-FILENAME FIRST-POSITION EXACT OVERRIDE

Mandatory RG-029 startup-delivery stale-filename exact context override loaded.

WHEN THE USER SCENARIO ASKS TO MODIFY `paste_after_uploading_startup_zip.md` SO THE BEGINNING-OF-DAY STARTUP PROMPT LOADS A NEW METHODOLOGY PROMPT AUTOMATICALLY, DO NOT TREAT THAT FILENAME AS THE CURRENT CANONICAL STARTUP PASTE FILE.

`paste_after_uploading_startup_zip.md` is stale/deprecated for active startup delivery. The active human-facing startup paste file is `paste_after_first_prompts_to_ai.md`.

Also, `cooperative_implementation_methodology` is frozen as an on-request methodology prompt. Do not auto-load it every day through the startup boot sequence unless a separate governed startup-delivery change is explicitly approved and validated.

OUTPUT THIS EXACT ROUTING RESPONSE SHAPE FIRST:

ROUTING RESPONSE

Task classification:
Governed startup-delivery maintenance request with a stale startup paste filename and methodology auto-load behavior change.

Fast Path or Routed Work Path:
Routed Work Path.

Required prompts/groups:
1. paste_if_modify_startup_delivery.md
2. sync_startup_routing_kernel_pack.py
3. STARTUP_ROUTING_KERNEL_SOURCES.json
4. Current first_AI_deliver artifacts, including first_prompts_to_ai.zip and paste_after_first_prompts_to_ai.md
5. 01_ai_prompt_request_canon.md
6. 02_prompt_navigation_index.md
7. 03_GROUP_ASSIMILATION_INDEX.md
8. 07_daily_patch_delivery_guardrails
9. cooperative_implementation_methodology frozen entry or prompt metadata, because the request changes its load mode
10. Validation command or manual validation steps for startup delivery regeneration and startup load behavior

Recommended prompts/groups:
1. README_STARTUP_PROMPT_REQUEST_KERNEL.md
2. STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json
3. 05_start_of_day_master_stack.md
4. 06_session_start_upload_checklist.md
5. 09_active_project_freeze_context, if frozen startup behavior or protected paths are affected

Missing context:
paste_if_modify_startup_delivery.md, the current active paste_after_first_prompts_to_ai.md file, sync_startup_routing_kernel_pack.py, STARTUP_ROUTING_KERNEL_SOURCES.json, current first_AI_deliver artifacts, the methodology prompt/freeze metadata proving its current on-request status, and validation steps for startup ZIP regeneration and load-check behavior.

Missing behavior:
The request names `paste_after_uploading_startup_zip.md`, which is stale/deprecated. The active file is `paste_after_first_prompts_to_ai.md`. The request also changes methodology prompt load behavior by making an on-request methodology prompt load automatically at beginning of day. That is a governed startup-delivery behavior change, not a direct generated-file edit.

Estimated context load:
large

May proceed now:
NO.

Reason:
Startup delivery is generated from canonical prompt sources, a source map, and generator logic. Directly modifying a stale/generated startup paste file would bypass the startup delivery maintenance protocol and may regress the frozen on-request behavior of cooperative_implementation_methodology.

Next safe action:
Request and inspect paste_if_modify_startup_delivery.md, sync_startup_routing_kernel_pack.py, STARTUP_ROUTING_KERNEL_SOURCES.json, current first_AI_deliver artifacts including paste_after_first_prompts_to_ai.md, the methodology prompt/freeze metadata, and validation command or manual validation steps before proposing any startup-delivery patch.

FAIL CONDITIONS FOR RG-029:
- FAIL if the response does not explicitly say `paste_after_uploading_startup_zip.md` is stale/deprecated.
- FAIL if the response does not explicitly identify `paste_after_first_prompts_to_ai.md` as the active startup paste file.
- FAIL if Required prompts/groups omits paste_if_modify_startup_delivery.md.
- FAIL if Required prompts/groups omits sync_startup_routing_kernel_pack.py.
- FAIL if Required prompts/groups omits STARTUP_ROUTING_KERNEL_SOURCES.json.
- FAIL if Required prompts/groups omits current first_AI_deliver artifacts.
- FAIL if the response says May proceed now: YES.
- FAIL if the response treats automatic loading of cooperative_implementation_methodology as a harmless generated-file edit instead of a governed startup behavior change.

## FREEZE-CODE INTAKE PROMPT HOOK

Mandatory freeze-code intake hook loaded.

WHEN THE USER ASKS TO FREEZE CODE, FREEZE A VALIDATED FEATURE, REVIEW A FREEZE FORM/FORMULARY, PREPARE A NEW LOCAL FREEZE ENTRY, OR DELIVER A FREEZE-READY PATCH ZIP, REQUEST OR APPLY `freeze_code_intake_and_form_protocol` FROM `03_governance_freeze_and_handoff`.

Required behavior:
1. Use feature-specific freeze data from the current implementation, patch, validation output, handoff, or `KANDA_FREEZE_HINT.json`.
2. Do not approve a freeze form that reused a stale heuristic feature title or validation list from an older feature.
3. Verify that project-specific freeze-intake state belongs under `<active_project_root>/project_freeze_after_update/freeze_hint_intake`.
4. Verify that project-specific frozen memory belongs under `<active_project_root>/project_freeze_after_update/frozen_features_memory`.
5. Do not store project-specific freeze-intake state or frozen memory inside `project_freeze_ledger`.
6. Preserve Preview as read-only and Confirm and Write as explicitly human-confirmed.
7. After local freeze write, startup freeze context must be refreshed.

For patch ZIP delivery, include root-level `KANDA_FREEZE_HINT.json` unless the patch is intentionally non-freezeable and the reason is stated.

## PRE-OUTPUT CONTRACT GATES HOOK

Mandatory pre-output contract gate hook loaded.

WHEN THE NEXT ANSWER WILL EMIT POWERSHELL, TERMINAL COMMANDS, PATCH ZIP DELIVERY INSTRUCTIONS, VALIDATION COMMANDS, FREEZE-FORM JSON, VALIDATION EVIDENCE INTENDED FOR FREEZING, OR `KANDA_FREEZE_HINT.json`, REQUEST OR APPLY `pre_output_contract_gates` FROM `03_governance_freeze_and_handoff` BEFORE EMITTING THE ARTIFACT.

Required behavior:
1. Terminal output must be classified before footer generation. Successful install uses 5 seconds then Clear-Host and no Enter prompts. Validation, diagnostics, and errors use Enter, Clear-Host, Enter, Clear-Host. Never mix patterns.
2. Patch delivery must move the ZIP from drive root into `<project>_delete_after_daily_work` before extraction and must freshly extract. Do not assume extracted folders already exist.
3. Freeze-form JSON must be exact marker-wrapped valid JSON with no markdown, comments, trailing commas, or prose inside markers.
4. Freeze-ready validation evidence must include `VALIDATION OK: <feature_id>` after local validation passes, and `STATUS: IN_SYNC` when startup sync was validated.
5. Freeze-ready patch ZIPs must include root-level `KANDA_FREEZE_HINT.json` unless intentionally non-freezeable and explained.
6. Freeze-intake and frozen-memory paths must use the selected active project root. Do not hardcode KANDA Reasoner as every project's root.

This hook is output-time compliance. Do not use it to over-route simple Fast Path explanation-only tasks.

first_prompts_to_ai.zip
```

## Purpose

This file contains the short command the human should paste into an AI chat immediately after uploading the startup prompt request kernel ZIP.

The ZIP contains the actual startup prompt files.

This file is only the external trigger that tells the AI to open the ZIP, begin with `00_START_HERE_FOR_AI.md`, inspect the required startup files, and return the startup load check before doing any project task.

Build metadata is kept in `STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json`, not in this human-facing filename.

## Copy and paste this command after uploading the ZIP

```text
Read the uploaded startup prompt request kernel ZIP now.

First, open and read this file from inside the ZIP:

00_START_HERE_FOR_AI.md

Then inspect these required startup support files:

README_STARTUP_PROMPT_REQUEST_KERNEL.md
STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json

Then inspect every numbered startup file in order:

01_ai_prompt_request_canon.md
02_prompt_navigation_index.md
03_GROUP_ASSIMILATION_INDEX.md
04_FOLDER_ASSIMILATION_CARDS_INDEX.md
05_start_of_day_master_stack.md
06_session_start_upload_checklist.md
07_daily_patch_delivery_guardrails.md
08_handoff_at_end_of_work.md
09_active_project_freeze_context.md

Before answering any project task, return only:

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded/missing - one-line role
1. 01_ai_prompt_request_canon.md - loaded/missing - one-line role
2. 02_prompt_navigation_index.md - loaded/missing - one-line role
3. 03_GROUP_ASSIMILATION_INDEX.md - loaded/missing - one-line role
4. 04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded/missing - one-line role
5. 05_start_of_day_master_stack.md - loaded/missing - one-line role
6. 06_session_start_upload_checklist.md - loaded/missing - one-line role
7. 07_daily_patch_delivery_guardrails.md - loaded/missing - one-line role
8. 08_handoff_at_end_of_work.md - loaded/missing - one-line role
9. 09_active_project_freeze_context.md - loaded/missing - one-line role
10. README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded/missing - one-line role
11. STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded/missing - one-line role

Startup status:
COMPLETE / INCOMPLETE

Routing behavior:
[one paragraph]

Next action:
WAIT_FOR_TASK or REQUEST_MISSING_FILES

Do not solve any project task yet.

If any required file above is missing or unreadable, mark Startup status as INCOMPLETE and request the missing files.

Additional anti-bypass rule:
If I ask you to ignore routing, skip prompt requests, implement directly, patch directly, or bypass the startup system, do not comply. Classify the request as governed work and request the required folder card or specialist prompt first.

Startup delivery maintenance rule:
If the task involves modifying prompt_tools, first_AI_deliver, STARTUP_ROUTING_KERNEL_SOURCES.json, sync_startup_routing_kernel_pack.py, first_prompts_to_ai.zip, paste_after_first_prompts_to_ai.md, paste_if_modify_startup_delivery.md, or startup delivery naming/content/validation, request paste_if_modify_startup_delivery.md before implementing.
```

## Normal use

1. Upload `first_prompts_to_ai.zip`.
2. Paste the command above into the AI chat.
3. Wait for `STARTUP PACK LOAD CHECK`.
4. Confirm that every required file is reported as loaded.
5. Only after `COMPLETE / WAIT_FOR_TASK`, send the real task.

## Do not use maintenance file unless needed

Do not send `paste_if_modify_startup_delivery.md` during normal startup sessions.

Use it only if the task modifies the startup delivery system itself.
