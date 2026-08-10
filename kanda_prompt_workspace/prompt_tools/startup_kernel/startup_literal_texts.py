"""Long startup literal text constants for startup kernel generation."""

from __future__ import annotations



__all__ = [
    "T9T013_RG015_FIRST_POSITION_OVERRIDE_RULE_V8",
    "RG028_FREEZE_WORKFLOW_FIRST_POSITION_OVERRIDE_RULE_V3",
    "RG029_STARTUP_STALE_FILENAME_FIRST_POSITION_OVERRIDE_RULE_V1",
    "T9T013_RG015_HARD_OVERRIDE_RULE_V7",
    "T9T013_RG015_BOOT_EXACTNESS_RULE_V6",
    "T9T013_RG015_BOOT_EXACTNESS_RULE",
    "FREEZE_CODE_INTAKE_FIRST_POSITION_OVERRIDE_RULE_V1",
    "PRE_OUTPUT_CONTRACT_GATES_FIRST_POSITION_HOOK_V1",
    "BOOT_COMMAND_TEXT",
]

T9T013_RG015_FIRST_POSITION_OVERRIDE_RULE_V8 = '## RG-015 FIRST-POSITION EXACT OVERRIDE\n\nMandatory prompt-authoring RG-015 first-position hard override loaded.\n\nWHEN THE USER SCENARIO ASKS TO CREATE/ADD/REGISTER A NEW PROMPT AND ALSO SAYS TO SKIP CHECKING EXISTING PROMPTS, DO NOT USE GENERIC ROUTING LABELS.\n\nOUTPUT THIS EXACT ROUTING RESPONSE SHAPE FIRST:\n\nROUTING RESPONSE\n\nTask classification:\nGoverned prompt-library and workflow update request with an explicit bypass attempt.\n\nFast Path or Routed Work Path:\nRouted Work Path.\n\nRequired prompts/groups:\n1. 07_prompt_authoring_and_audit\n2. prompt_canon_reconciliation_protocol\n3. prompt_audit_canon\n4. project_specific_prompt_generalization\n5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder\n6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap\n7. bundle_gated_development_workflow, if creating an installable bundle\n8. Validation command or manual validation steps\n\nRecommended prompts/groups:\n1. Domain-specific medical residency curriculum scoring source/rubric, if available\n2. 02_prompt_routing_and_indexing\n3. Current prompt navigation/index files\n4. Metadata/schema examples from similar prompts\n\nMissing context:\nTarget prompt library location, current registry/index format, existing related prompts, naming conventions, expected scoring criteria, validation command, metadata requirements, and the required ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION.\n\nMissing behavior:\nThe request says to skip checking existing prompts, but safe prompt-library work requires checking existing prompt-library assets/indexes for duplicates, overlap, naming collisions, placement rules, workflow registration, metadata requirements, and create-vs-update-vs-link/register decision before implementation.\n\nMay proceed now:\nNO.\n\nReason:\nAdding a new prompt to the KANDA prompt library and making it available in the prompt authoring workflow changes governed prompt infrastructure. The anti-audit bypass instruction must not be followed.\n\nNext safe action:\nRequest and inspect 07_prompt_authoring_and_audit, prompt_canon_reconciliation_protocol, prompt_audit_canon, project_specific_prompt_generalization, the relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION, existing prompt-library assets/indexes needed to inspect duplicates and overlap, bundle_gated_development_workflow if creating an installable bundle, and validation command or manual validation steps before implementation.\n\nFAIL CONDITIONS FOR RG-015:\n- FAIL if Required prompts/groups uses only generic labels such as prompt authoring workflow specialist prompt or folder card.\n- FAIL if Required prompts/groups omits 07_prompt_authoring_and_audit.\n- FAIL if Required prompts/groups omits prompt_canon_reconciliation_protocol.\n- FAIL if Required prompts/groups omits prompt_audit_canon.\n- FAIL if Required prompts/groups omits project_specific_prompt_generalization.\n'

RG028_FREEZE_WORKFLOW_FIRST_POSITION_OVERRIDE_RULE_V3 = """## RG-028 FREEZE-WORKFLOW FIRST-POSITION EXACT OVERRIDE

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
"""


RG029_STARTUP_STALE_FILENAME_FIRST_POSITION_OVERRIDE_RULE_V1 = """## RG-029 STARTUP-DELIVERY STALE-FILENAME FIRST-POSITION EXACT OVERRIDE

Mandatory RG-029 startup-delivery stale-filename exact context override loaded.

WHEN THE USER SCENARIO ASKS TO MODIFY `paste_after_uploading_startup_zip.md` SO THE BEGINNING-OF-DAY STARTUP PROMPT LOADS A NEW METHODOLOGY PROMPT AUTOMATICALLY, DO NOT TREAT THAT FILENAME AS THE CURRENT CANONICAL STARTUP PASTE FILE.

`paste_after_uploading_startup_zip.md` is stale/deprecated for active startup delivery. The active human-facing startup paste file is `tell_AI_read_before_all.md`.

Also, `cooperative_implementation_methodology` is frozen as an on-request methodology prompt. Do not auto-load it every day through the startup boot sequence unless a separate governed startup-delivery change is explicitly approved and validated.

OUTPUT THIS EXACT ROUTING RESPONSE SHAPE FIRST:

ROUTING RESPONSE

Task classification:
Governed startup-delivery maintenance request with a stale startup paste filename and methodology auto-load behavior change.

Fast Path or Routed Work Path:
Routed Work Path.

Required prompts/groups:
1. zz_read_only_if_modifying_startup_delivery.md
2. sync_startup_routing_kernel_pack.py
3. STARTUP_ROUTING_KERNEL_SOURCES.json
4. Current first_prompt_files artifacts, including first_prompts_to_ai.zip and tell_AI_read_before_all.md
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
zz_read_only_if_modifying_startup_delivery.md, the current active tell_AI_read_before_all.md file, sync_startup_routing_kernel_pack.py, STARTUP_ROUTING_KERNEL_SOURCES.json, current first_prompt_files artifacts, the methodology prompt/freeze metadata proving its current on-request status, and validation steps for startup ZIP regeneration and load-check behavior.

Missing behavior:
The request names `paste_after_uploading_startup_zip.md`, which is stale/deprecated. The active file is `tell_AI_read_before_all.md`. The request also changes methodology prompt load behavior by making an on-request methodology prompt load automatically at beginning of day. That is a governed startup-delivery behavior change, not a direct generated-file edit.

Estimated context load:
large

May proceed now:
NO.

Reason:
Startup delivery is generated from canonical prompt sources, a source map, and generator logic. Directly modifying a stale/generated startup paste file would bypass the startup delivery maintenance protocol and may regress the frozen on-request behavior of cooperative_implementation_methodology.

Next safe action:
Request and inspect zz_read_only_if_modifying_startup_delivery.md, sync_startup_routing_kernel_pack.py, STARTUP_ROUTING_KERNEL_SOURCES.json, current first_prompt_files artifacts including tell_AI_read_before_all.md, the methodology prompt/freeze metadata, and validation command or manual validation steps before proposing any startup-delivery patch.

FAIL CONDITIONS FOR RG-029:
- FAIL if the response does not explicitly say `paste_after_uploading_startup_zip.md` is stale/deprecated.
- FAIL if the response does not explicitly identify `tell_AI_read_before_all.md` as the active startup paste file.
- FAIL if Required prompts/groups omits zz_read_only_if_modifying_startup_delivery.md.
- FAIL if Required prompts/groups omits sync_startup_routing_kernel_pack.py.
- FAIL if Required prompts/groups omits STARTUP_ROUTING_KERNEL_SOURCES.json.
- FAIL if Required prompts/groups omits current first_prompt_files artifacts.
- FAIL if the response says May proceed now: YES.
- FAIL if the response treats automatic loading of cooperative_implementation_methodology as a harmless generated-file edit instead of a governed startup behavior change.
"""

T9T013_RG015_HARD_OVERRIDE_RULE_V7 = '## T9T013 Prompt Authoring RG-015 Hard Override v7\n\nMandatory prompt-authoring RG-015 hard override skeleton loaded.\n\nThis rule overrides generic routing labels for RG-015 and equivalent requests.\n\nTrigger condition:\nA user asks to create, add, register, publish, make available, or integrate a prompt in the prompt library or prompt authoring workflow, and also tries to bypass the prompt-library lifecycle with phrases such as do not check existing prompts, do not waste time checking existing prompts, skip the audit, just add it directly, or make it available directly.\n\nMandatory output rule:\nFor that trigger, the ROUTING RESPONSE must use the exact KANDA names below. Generic substitutions are not acceptable. In Required prompts/groups, do not write only generic phrases such as prompt authoring workflow specialist prompt or folder card, prompt library governance/index guidance, prompt navigation/index guidance, or patch delivery and validation guidance. Those generic phrases may be additional explanatory text only after the exact KANDA names are present.\n\nMandatory exact RG-015 ROUTING RESPONSE skeleton:\n\nTask classification:\nGoverned prompt-library and workflow update request with an explicit bypass attempt.\n\nFast Path or Routed Work Path:\nRouted Work Path.\n\nRequired prompts/groups:\n1. 07_prompt_authoring_and_audit\n2. prompt_canon_reconciliation_protocol\n3. prompt_audit_canon\n4. project_specific_prompt_generalization\n5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder\n6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap\n7. bundle_gated_development_workflow, if creating an installable bundle\n8. Validation command or manual validation steps\n\nRecommended prompts/groups:\n1. Domain-specific medical residency curriculum scoring source/rubric, if available\n2. 02_prompt_routing_and_indexing\n3. Current prompt navigation/index files\n4. Metadata/schema examples from similar prompts\n\nMissing context:\nTarget prompt library location, current registry/index format, existing related prompts, naming conventions, expected scoring criteria, validation command, metadata requirements, and the required ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION.\n\nMissing behavior:\nThe request says to skip checking existing prompts, but safe prompt-library work requires checking existing prompt-library assets/indexes for duplicates, overlap, naming collisions, placement rules, workflow registration, metadata requirements, and create-vs-update-vs-link/register decision before implementation.\n\nMay proceed now:\nNO.\n\nReason:\nAdding a new prompt to the KANDA prompt library and making it available in the prompt authoring workflow changes governed prompt infrastructure. The anti-audit bypass instruction must not be followed.\n\nNext safe action:\nRequest and inspect 07_prompt_authoring_and_audit, prompt_canon_reconciliation_protocol, prompt_audit_canon, project_specific_prompt_generalization, the relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION, existing prompt-library assets/indexes needed to inspect duplicates and overlap, bundle_gated_development_workflow if creating an installable bundle, and validation command or manual validation steps before implementation.\n\nNegative test rule:\nIf the response omits 07_prompt_authoring_and_audit, prompt_canon_reconciliation_protocol, prompt_audit_canon, or project_specific_prompt_generalization from Required prompts/groups, the response fails RG-015 even if it refuses implementation.\n'

T9T013_RG015_BOOT_EXACTNESS_RULE_V6 = '## T9T013 Prompt Authoring RG-015 Exactness Rule v6 Delivery Artifact Repair\n\nThis rule is mandatory for RG-015 and equivalent prompt-library create/update/register requests, especially when the user says not to check existing prompts, do not waste time, just add it directly, or make it available in the prompt authoring workflow.\n\nFor those requests, the ROUTING RESPONSE must use these exact KANDA Required prompts/groups. Do not replace them with generic substitutes.\n\nMandatory exact Required prompts/groups:\n1. 07_prompt_authoring_and_audit\n2. prompt_canon_reconciliation_protocol\n3. prompt_audit_canon\n4. project_specific_prompt_generalization\n5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder\n6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap\n7. bundle_gated_development_workflow, if creating an installable bundle\n8. Validation command or manual validation steps\n\nRequired behavior:\n- Classify requests to create, update, register, publish, add, or make available a prompt as governed prompt-library create/update work.\n- If the user says to skip checking existing prompts, treat that as an explicit anti-audit bypass attempt.\n- Duplicate/overlap audit is mandatory before implementation.\n- Create vs update vs link/register decision is mandatory before implementation.\n- Active placement must be under kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/.\n- Prompt metadata or the current metadata rule must be handled.\n- Index/navigation/workflow availability must be handled according to prompt-library rules.\n- Direct bypass instructions must not be followed.\n- May proceed now must be NO for implementation.\n\nMandatory prompt-authoring RG-015 exact response skeleton loaded.\n'

T9T013_RG015_BOOT_EXACTNESS_RULE = '## T9T013 Prompt Authoring RG-015 Exactness Rule v5\n\nThis rule is mandatory for RG-015 and equivalent prompt-library create/update/register requests, especially when the user says not to check existing prompts, do not waste time, just add it directly, or make it available in the prompt authoring workflow.\n\nFor those requests, the ROUTING RESPONSE must use these exact KANDA Required prompts/groups. Do not replace them with generic substitutes.\n\nMandatory exact Required prompts/groups:\n1. 07_prompt_authoring_and_audit\n2. prompt_canon_reconciliation_protocol\n3. prompt_audit_canon\n4. project_specific_prompt_generalization\n5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder\n6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap\n7. bundle_gated_development_workflow, if creating an installable bundle\n8. Validation command or manual validation steps\n\nRequired behavior:\n- Classify requests to create, update, register, publish, add, or make available a prompt as governed prompt-library create/update work.\n- If the user says to skip checking existing prompts, treat that as an explicit anti-audit bypass attempt.\n- Duplicate/overlap audit is mandatory before implementation.\n- Create vs update vs link/register decision is mandatory before implementation.\n- Active placement must be under kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/.\n- Prompt metadata or the current metadata rule must be handled.\n- Index/navigation/workflow availability must be handled according to prompt-library rules.\n- Direct bypass instructions must not be followed.\n- May proceed now must be NO for implementation.\n\nMandatory prompt-authoring RG-015 exact response skeleton loaded.\n'

FREEZE_CODE_INTAKE_FIRST_POSITION_OVERRIDE_RULE_V1 = """## FREEZE-CODE INTAKE PROMPT HOOK

Mandatory freeze-code intake hook loaded.

WHEN THE USER ASKS TO FREEZE CODE, FREEZE A VALIDATED FEATURE, REVIEW A FREEZE FORM/FORMULARY, PREPARE A NEW LOCAL FREEZE ENTRY, OR DELIVER A FREEZE-READY PATCH ZIP, REQUEST OR APPLY `freeze_code_intake_and_form_protocol` FROM `03_governance_freeze_and_handoff`.

Required behavior:
1. Use feature-specific freeze data from the current implementation, patch, validation output, handoff, or `KANDA_FREEZE_HINT.json`.
2. Do not approve a freeze form that reused a stale heuristic feature title or validation list from an older feature.
3. Verify that project-specific freeze-intake state belongs under `<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake`.
4. Verify that project-specific frozen memory belongs under `<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/frozen_features_memory`.
5. Do not store project-specific freeze-intake state or frozen memory inside `project_freeze_ledger`.
6. Preserve Preview as read-only and Confirm and Write as explicitly human-confirmed.
7. After local freeze write, startup freeze context must be refreshed.

For patch ZIP delivery, include root-level `KANDA_FREEZE_HINT.json` unless the patch is intentionally non-freezeable and the reason is stated.
"""


PRE_OUTPUT_CONTRACT_GATES_FIRST_POSITION_HOOK_V1 = """## PRE-OUTPUT CONTRACT GATES HOOK

Mandatory pre-output contract gate hook loaded.

WHEN THE NEXT ANSWER WILL EMIT POWERSHELL, TERMINAL COMMANDS, PATCH ZIP DELIVERY INSTRUCTIONS, VALIDATION COMMANDS, FREEZE-FORM JSON, VALIDATION EVIDENCE INTENDED FOR FREEZING, OR `KANDA_FREEZE_HINT.json`, REQUEST OR APPLY `pre_output_contract_gates` FROM `03_governance_freeze_and_handoff` BEFORE EMITTING THE ARTIFACT.

Required behavior:
1. Terminal output must be classified before footer generation. Successful install uses about 2 seconds then Clear-Host and no Enter prompts. Install errors, validation, freeze, diagnostics, validation errors, freeze errors, and all non-install-success terminal blocks use Enter, Enter, Clear-Host. Never mix patterns and never close the terminal. Freeze-prep and validation-evidence merge commands must not use inline `python -c`; write a temporary UTF-8 `.py` helper under `_delete_after_daily_work`, set `$env:PYTHONPATH = $PROJECT_ROOT`, insert `project_root` into `sys.path` in the helper before importing `kanda_reasoner_app`, and run that file.
2. Patch delivery must detect `DRIVE_ROOT` from `$PROJECT_ROOT`, look first for the ZIP at the project drive root, stage it into `<project>_delete_after_daily_work`, delete the root-drive ZIP copy after successful staging, and extract only from the staged ZIP. Do not use the old generic Downloads/Desktop-first installer search template. Install blocks must include a fail-safe try/catch or text-equivalent wrapper so install errors use Enter, Enter, Clear-Host instead of bypassing cleanup.
3. Before emitting patch ZIP delivery, install, validation, or freeze-ready metadata, apply `patch_install_delivery_error_register` and block known PIR regressions, especially Downloads/Desktop fallback installers, daily-work-only installers, and giant single-line validation evidence.
4. Patch ZIP delivery is `PATCH_DELIVERY_RELEASE`, a governed release event. Do not emit a ZIP link unless the ZIP contract validator has passed or the patch is explicitly declared non-freezeable. If the contract cannot be verified, output `CONTRACT NOT MET - PATCH DELIVERY BLOCKED`.
4. Patch ZIPs that can be frozen must include root-level `KANDA_FREEZE_HINT.json`. The sidecar must not be duplicated inside the install payload folder.
5. Root-level `KANDA_FREEZE_HINT.json` and any freeze-form JSON must be generated from the same freeze payload source. Do not hand-type separate divergent copies.
6. Freeze-form JSON must be exact marker-wrapped valid JSON with no markdown, comments, trailing commas, or prose inside markers.
7. Freeze-ready validation evidence must include `VALIDATION OK: <feature_id>` after local validation passes, and `STATUS: IN_SYNC` when startup sync was validated.
8. Freeze-intake and frozen-memory paths must use the selected active project root. Do not hardcode KANDA Reasoner as every project's root.

This hook is output-time compliance. Do not use it to over-route simple Fast Path explanation-only tasks.
"""

BOOT_COMMAND_TEXT = """This file is the first startup instruction. Read this instruction before opening ZIP contents.

After this instruction, read the uploaded startup prompt request kernel ZIP.

Also note that the user should have uploaded `{PROMPT_LIBRARY_ZIP_NAME}` in the same chat. That ZIP is the on-demand canonical prompt source. Do not read every prompt in it at startup. Open it later only when a specific prompt is needed and the needed prompt is not already present in `{DEFAULT_ZIP_NAME}`.

First, open and read this file from inside the startup ZIP:

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
8. README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded/missing - one-line role
9. STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded/missing - one-line role

Startup status:
COMPLETE / INCOMPLETE

Routing behavior:
[one paragraph]

Next action:
Waiting for all files (Project Files) from second_prompt_files folder or REQUEST_MISSING_FILES

Do not solve any project task yet.

If any required file above is missing or unreadable, mark Startup status as INCOMPLETE and request the missing files.

If all startup files are complete, do not answer the project task yet. Wait for all files from the second_prompt_files folder. After the second upload group is read, return PROJECT READY CHECK and end with Next action:, then PROJECT IN USE: <ACTIVE PROJECT DISPLAY NAME>, then WAIT_FOR_TASK. Derive the display name from the selected active Project, not the KANDA Tool; replace underscores with spaces and convert it to uppercase.
"""

