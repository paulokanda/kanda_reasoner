# ROADMAP - pre_output_contract_gates_v1

## Intent

Implement a compliance layer that makes AI follow the KANDA canon at the exact moment it produces high-risk outputs.

The goal is not to rewrite the router.

The goal is to prevent this failure pattern:

1. AI routes the task correctly.
2. AI understands the canon in general.
3. AI begins writing the final artifact.
4. AI falls back to generic habits.
5. AI violates a KANDA canonical rule in PowerShell, patch delivery, freeze JSON, validation evidence, or project-root placement.

The new feature should make KANDA behave like this:

1. Router selects the correct path and context.
2. Pre-output contract gate classifies the artifact about to be emitted.
3. The gate applies the exact KANDA canon for that artifact type.
4. The AI emits the artifact only if it satisfies the contract.
5. Validators and tests check the output.
6. Validated behavior is frozen.

Feature name:

pre_output_contract_gates_v1

Primary purpose:

Make the AI follow the canon, especially for terminal blocks, patch ZIP delivery, freeze-form JSON, validation evidence, freeze sidecars, and multi-project paths.

---

# 1. Define implementation scope

## 1.1 In scope

Implement a narrow prompt-routing and compliance feature:

1. Add a new on-request prompt:
   pre_output_contract_gates.md

2. Add metadata for the prompt.

3. Register the prompt in the relevant prompt-library indexes.

4. Add a small startup hook, not the full prompt.

5. Update daily patch delivery guardrails to reference the contract gates.

6. Update freeze-code intake protocol to reference the strict freeze-form and validation evidence gates.

7. Add tests RG-031 to RG-040.

8. Regenerate startup artifacts.

9. Deliver as a patch ZIP with KANDA_FREEZE_HINT.json.

10. Validate and freeze after installation.

## 1.2 Out of scope

Do not rewrite the router.

Do not load all prompts daily.

Do not make all 80 prompts always-startup.

Do not remove Confirm and Write.

Do not bypass local human confirmation.

Do not store active project freeze memory in project_freeze_ledger.

Do not hardcode E:\kanda_reasoner as the active project root for all projects.

Do not install KANDA_FREEZE_HINT.json into the project root as a source file.

Do not invent validation evidence.

---

# 2. Architectural design

## 2.1 Current architecture

Current flow:

1. Startup prompt package loads.
2. Router decides Fast Path or Routed Work Path.
3. AI requests or uses required context.
4. AI generates output.

Problem:

There is no mandatory final contract check between step 3 and step 4.

## 2.2 Target architecture

New flow:

1. Startup prompt package loads.
2. Router decides Fast Path or Routed Work Path.
3. AI requests or uses required context.
4. If output is high-risk, AI applies pre_output_contract_gates.
5. AI emits terminal block, patch delivery instructions, freeze JSON, or validation evidence.
6. Validator/test checks artifact.
7. Freeze only after validated behavior.

## 2.3 Design principle

Router-time rules are not enough.

Output-time contracts are required for machine-consumed artifacts.

The AI should not merely remember the canon. It must be forced to classify the artifact type and apply the corresponding contract before emission.

---

# 3. New prompt design

## 3.1 New prompt file

Create:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md

Rationale:

The feature mostly protects patch delivery, freeze forms, freeze-ready ZIPs, validation evidence, terminal hygiene, and freeze-intake behavior. These belong closest to governance, freeze, handoff, and delivery.

## 3.2 Prompt status

Load mode:

on_request

Reason:

The canon says startup prompts should remain lean. The full contract-gate prompt should not become a giant always-loaded startup prompt.

## 3.3 Prompt role

The prompt is invoked before emitting high-risk artifacts.

It is not a replacement for the router.

It is not a replacement for freeze_code_intake_and_form_protocol.

It is a final compliance layer.

---

# 4. Startup hook design

## 4.1 Add a tiny startup hook

Add a short hook into the startup delivery source that generates paste_after_first_prompts_to_ai.md.

Suggested hook:

PRE-OUTPUT CONTRACT GATES HOOK

When producing any of the following artifacts, request or apply pre_output_contract_gates from 03_governance_freeze_and_handoff before emitting the final output:

1. PowerShell or terminal install block.
2. PowerShell or terminal validation block.
3. Diagnostic or error terminal block.
4. Patch ZIP delivery instructions.
5. Freeze-ready patch ZIP instructions.
6. KANDA_FREEZE_FORM_JSON_BEGIN / KANDA_FREEZE_FORM_JSON_END output.
7. Validation evidence summary intended for freezing.
8. KANDA_FREEZE_HINT.json metadata.

Required behavior:

Do not rely on memory.
Do not use generic terminal footers.
Do not emit freeze JSON without exact validation markers.
Do not emit freeze-ready patch delivery without checking sidecar requirements.
Do not hardcode active project paths.

## 4.2 Do not paste the entire prompt into startup

Startup should only contain the hook.

The full prompt remains on-request.

---

# 5. Contract gate contents

## 5.1 Gate A - Terminal Output Contract

Triggered before any terminal or PowerShell block.

The AI must classify the terminal block as one of:

1. INSTALL_SUCCESS
2. INSTALL_ERROR
3. VALIDATION
4. DIAGNOSTIC
5. OTHER_TERMINAL

Contract:

INSTALL_SUCCESS must end with:

* success message
* Start-Sleep -Seconds 5
* Clear-Host
* no Read-Host success prompt
* no terminal close

VALIDATION, DIAGNOSTIC, INSTALL_ERROR, VALIDATION_ERROR, and OTHER_TERMINAL must end with:

* Read-Host
* Clear-Host
* Read-Host
* Clear-Host
* no terminal close

Forbidden:

* Do not mix install-success and validation cleanup.
* Do not use old generic footer.
* Do not ask for Enter after successful install.
* Do not auto-clear validation output after 5 seconds.
* Do not close the terminal.

## 5.2 Gate B - Patch Delivery Contract

Triggered before any patch ZIP delivery or install instructions.

Contract:

1. Patch ZIP contains only updated files plus required metadata.
2. User downloads the ZIP to the root of the same drive as the project.
3. Installer creates the delete-after-daily-work folder if missing.
4. Installer moves ZIP from drive root into staging folder.
5. Installer freshly extracts every time.
6. Installer does not assume any extracted folder already exists.
7. Installer does not put temporary scripts in project root.
8. Install and validation commands are separate.
9. Freeze-ready patch ZIPs include root-level KANDA_FREEZE_HINT.json.
10. KANDA_FREEZE_HINT.json is delivery metadata, not installed source.

Forbidden:

* Do not package the whole project.
* Do not include caches.
* Do not include backup folders.
* Do not include unrelated unchanged files.
* Do not rely on yesterday's extracted folder.
* Do not omit KANDA_FREEZE_HINT.json from freeze-ready patches unless explicitly non-freezeable.

## 5.3 Gate C - Freeze Form JSON Contract

Triggered before returning freeze-form JSON to the app.

Contract:

Output exactly:

KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_title":"...","primary_box":"...","box_type":"...","validated_files":"...","generated_files":"...","protected_paths":"...","do_not_regress_rules":"...","validation_evidence_summary":"...","known_warnings":"...","planned_next_step":"...","notes":"..."}
KANDA_FREEZE_FORM_JSON_END

Required fields:

1. feature_title
2. primary_box
3. box_type
4. validated_files
5. generated_files
6. protected_paths
7. do_not_regress_rules
8. validation_evidence_summary
9. known_warnings
10. planned_next_step
11. notes

Forbidden:

* No markdown fences.
* No bullets.
* No comments.
* No explanation.
* No trailing commas.
* No invalid backslash escapes.
* No prose between markers.
* No extra text before or after if strict receiver mode is requested.
* Do not invent validation evidence.

## 5.4 Gate D - Validation Evidence Contract

Triggered before any freeze-ready metadata or freeze-form JSON.

Contract:

If local validation passed, validation_evidence_summary must include:

VALIDATION OK: feature_id

If startup sync was validated, include:

STATUS: IN_SYNC

Optional evidence:

CONTRACT_TEST_OK: ...
SANDBOX_..._VALIDATION_OK
INSTALL OK: ...

If the exact validation marker is absent, do not produce freeze-ready JSON.

Required failure response:

FREEZE BLOCKED - validation evidence marker missing.

Forbidden:

* Do not treat "sandbox passed" alone as sufficient.
* Do not use validation from another feature.
* Do not reuse stale validation lists.
* Do not claim local validation before it happened.
* Do not convert STATUS: IN_SYNC into STATUS IN_SYNC.

## 5.5 Gate E - Freeze Hint Sidecar Contract

Triggered before freeze-ready patch delivery.

Contract:

KANDA_FREEZE_HINT.json must include:

1. schema_version
2. kind
3. patch_name
4. feature_id
5. feature_title
6. primary_box
7. box_type
8. validated_files
9. generated_files
10. protected_paths
11. do_not_regress_rules
12. validation_evidence_summary
13. known_warnings
14. planned_next_step
15. notes

Recommended new fields:

16. freeze_readiness
17. requires_user_validation
18. source_patch_zip

Allowed freeze_readiness values:

1. pre_validation_hint
2. locally_validated
3. frozen

Rules:

* Sidecar describes the current patch feature.
* Sidecar must not describe an older heuristic feature.
* Sidecar must not be installed into project root.
* Chat memory must not override sidecar identity.
* If sidecar and chat context disagree, sidecar wins.
* If no sidecar exists and the patch is freeze-ready, block or mark non-freezeable.

## 5.6 Gate F - Multi-project Root Contract

Triggered before freeze-intake or freeze-memory paths.

Contract:

Active project root owns project-specific state.

If active project is E:\kanda_reasoner:

E:\kanda_reasoner\project_freeze_after_update\freeze_hint_intake
E:\kanda_reasoner\project_freeze_after_update\frozen_features_memory

If active project is D:\any_project:

D:\any_project\project_freeze_after_update\freeze_hint_intake
D:\any_project\project_freeze_after_update\frozen_features_memory

Forbidden:

* Do not store active project freeze memory inside project_freeze_ledger.
* Do not assume KANDA Reasoner is always the active project.
* Do not write external project freeze state under E:\kanda_reasoner merely because KANDA is the tool.

---

# 6. Prompt-library registration roadmap

## 6.1 Add prompt file

Add:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md

## 6.2 Add metadata

Add:

kanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json

Metadata should include:

prompt_id: pre_output_contract_gates
category: 03_governance_freeze_and_handoff
load_type: on_request
purpose: output-time contract gate for terminal code, patch delivery, freeze JSON, validation evidence, freeze sidecars, and multi-project path compliance

## 6.3 Update folder assimilation

Update:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md

Add the new prompt to the folder card.

## 6.4 Update routing indexes

Update:

kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json

Add routes for:

1. terminal block generation
2. PowerShell install generation
3. validation block generation
4. patch ZIP delivery
5. freeze-ready patch delivery
6. freeze-form JSON output
7. validation evidence summary
8. KANDA_FREEZE_HINT.json delivery metadata
9. multi-project freeze path verification

## 6.5 Update startup delivery generator source map if required

If startup delivery is generated from a source map, update:

kanda_prompt_workspace/startup_routing_kernel/STARTUP_ROUTING_KERNEL_SOURCES.json

or the equivalent active source map.

Do not manually edit generated startup ZIP content as durable source.

---

# 7. Startup delivery update roadmap

## 7.1 Update startup hook source

Add only a small first-position hook to the source that generates paste_after_first_prompts_to_ai.md.

Hook purpose:

When the task will output terminal code, patch delivery instructions, validation commands, freeze-form JSON, freeze-ready patch ZIP metadata, or KANDA_FREEZE_HINT.json, apply pre_output_contract_gates before output.

## 7.2 Regenerate delivery artifacts

Run startup regeneration:

1. sync_startup_routing_kernel_pack.py --ensure-sync --yes
2. sync_startup_routing_kernel_pack.py --check

Expected:

STATUS: IN_SYNC

## 7.3 Confirm generated files updated

Expected generated files:

1. kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
2. kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md
3. kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md
4. STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json if generated in delivery output

---

# 8. Validator roadmap

## 8.1 Terminal validator

Create a validator or test helper that checks generated PowerShell blocks.

Install success block must contain:

1. Start-Sleep -Seconds 5
2. Clear-Host
3. no Read-Host in success footer

Validation or diagnostic block must contain:

1. at least two Read-Host prompts
2. at least two Clear-Host calls
3. no 5-second auto-clear as the only cleanup

## 8.2 Patch delivery validator

Check install script contains:

1. drive root ZIP path
2. delete-after-daily-work staging folder
3. New-Item for staging folder
4. Move-Item or Copy-Item from root ZIP to staging ZIP
5. Expand-Archive from staging ZIP
6. removal of old extract folder before extraction
7. no dependency on pre-existing extracted path
8. no project-root temporary install script

## 8.3 Freeze JSON validator

Check AI output:

1. begins with KANDA_FREEZE_FORM_JSON_BEGIN
2. ends with KANDA_FREEZE_FORM_JSON_END
3. contains one valid JSON object
4. has all required fields
5. has no markdown fences
6. has no trailing commas
7. has no unescaped invalid backslashes
8. validation_evidence_summary contains VALIDATION OK: feature_id when validated

## 8.4 Freeze hint sidecar validator

Check patch ZIP contains:

1. root-level KANDA_FREEZE_HINT.json
2. kind == kanda_freeze_hint
3. feature_id present
4. feature_title present
5. protected paths present
6. validation_evidence_summary present
7. project_freeze_after_update/frozen_features_memory present in protected_paths or do-not-regress rules
8. project_freeze_ledger boundary rule present
9. sidecar is not installed into project root

## 8.5 Multi-project path validator

Check:

1. active project root is passed into freeze-intake functions
2. freeze_hint_intake state goes under active_project_root/project_freeze_after_update/freeze_hint_intake
3. frozen memory goes under active_project_root/project_freeze_after_update/frozen_features_memory
4. project_freeze_ledger is not used as active project state owner

---

# 9. Regression test roadmap

Do not test all prompts one by one.

Test the behavior classes that previously failed.

## 9.1 RG-031 - Terminal install success contract

Scenario:

Ask AI to create a PowerShell install block for a patch.

Expected:

1. Uses install success cleanup.
2. Shows success message.
3. Waits 5 seconds.
4. Clears terminal.
5. Keeps terminal open.
6. Does not ask for Enter on success.

Fail if:

1. Uses Enter Enter on success.
2. Mixes 5-second cleanup with Enter prompts.
3. Closes terminal.

## 9.2 RG-032 - Terminal validation contract

Scenario:

Ask AI to create a validation block.

Expected:

1. Uses validation cleanup.
2. Read-Host.
3. Clear-Host.
4. Read-Host again.
5. Clear-Host again.
6. Keeps terminal open.

Fail if:

1. Uses install-success footer.
2. Auto-clears after 5 seconds.
3. Closes terminal.

## 9.3 RG-033 - Patch staging contract

Scenario:

Ask AI to provide patch install instructions.

Expected:

1. ZIP starts at drive root.
2. Installer creates staging folder.
3. Installer moves ZIP to staging.
4. Installer freshly extracts.
5. Installer copies only intended files.
6. Installer does not assume existing extracted folders.

Fail if:

1. Extracted path is assumed.
2. ZIP is not staged.
3. Temporary files are placed in project root.

## 9.4 RG-034 - Freeze JSON strict contract

Scenario:

Ask AI for freeze-form JSON.

Expected:

1. Exact markers.
2. One valid compact JSON object.
3. No markdown.
4. No comments.
5. All required fields.

Fail if:

1. Parser rejects output.
2. Extra text is inside markers.
3. JSON is malformed.

## 9.5 RG-035 - Missing validation marker block

Scenario:

Ask AI to produce freeze JSON from validation evidence that lacks VALIDATION OK: feature_id.

Expected:

AI returns:

FREEZE BLOCKED - validation evidence marker missing.

Fail if:

AI produces freeze JSON anyway.

## 9.6 RG-036 - Freeze-ready sidecar contract

Scenario:

Ask AI to deliver a freeze-ready patch ZIP.

Expected:

Patch ZIP includes root-level KANDA_FREEZE_HINT.json.

Fail if:

1. Sidecar is missing.
2. Sidecar is under docs.
3. Sidecar is installed as source.
4. Sidecar describes wrong feature.

## 9.7 RG-037 - Sidecar beats chat memory

Scenario:

Chat context implies old feature, but KANDA_FREEZE_HINT.json says current feature.

Expected:

AI uses sidecar feature identity.

Fail if:

AI uses stale chat context.

## 9.8 RG-038 - Monotonic freeze hint contract

Scenario:

Saved hint has VALIDATION OK: feature_id. Same staged ZIP is rescanned.

Expected:

Validation evidence remains.

Fail if:

Evidence downgrades to local validation pending.

## 9.9 RG-039 - External project root contract

Scenario:

KANDA Reasoner analyzes D:\any_project.

Expected:

Freeze-intake state:

D:\any_project\project_freeze_after_update\freeze_hint_intake

Frozen memory:

D:\any_project\project_freeze_after_update\frozen_features_memory

Fail if:

State is written under E:\kanda_reasoner by default.

## 9.10 RG-040 - Fast Path no-overrouting

Scenario:

Ask for simple explanation.

Expected:

Fast Path. No governed prompt loading.

Fail if:

AI requests unnecessary prompt packs.

---

# 10. Patch packaging roadmap

## 10.1 Patch name

pre_output_contract_gates_v1_patch.zip

## 10.2 ZIP contents

Include only changed files.

Expected files may include:

1. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md
2. kanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json
3. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md
4. kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
5. kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
6. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
7. kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json
8. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md
9. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md
10. kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py if generator hook requires update
11. kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
12. kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md
13. kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md
14. tests or validation scripts if project has test folders for prompt-routing behavior
15. KANDA_FREEZE_HINT.json at ZIP root

Do not include:

1. whole project
2. caches
3. backups
4. **pycache**
5. temporary validation folders
6. root installer scripts
7. old extracted patch folders

## 10.3 KANDA_FREEZE_HINT.json

Feature title:

Pre-Output Contract Gates v1

Feature ID:

pre_output_contract_gates_v1

primary_box:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + startup routing kernel + first_AI_deliver

box_type:

Prompt Routing / Output-Time Compliance / Artifact Contract Gate

validation_evidence_summary before local validation:

Local validation pending. Must be updated after validation with VALIDATION OK: pre_output_contract_gates_v1 and STATUS: IN_SYNC.

After validation, merge recognizer-friendly evidence into freeze hint intake.

---

# 11. Installation roadmap

## 11.1 Human download location

Human downloads patch ZIP to:

E:\pre_output_contract_gates_v1_patch.zip

or same drive root as active project.

## 11.2 Installer behavior

Installer must:

1. Set PROJECT_ROOT to E:\kanda_reasoner for this patch, because this patch modifies KANDA Reasoner itself.
2. Determine drive root from PROJECT_ROOT.
3. Create E:\kanda_reasoner_delete_after_daily_work if missing.
4. Move ZIP from drive root into staging folder.
5. Remove old extraction folder if present.
6. Extract fresh.
7. Confirm KANDA_FREEZE_HINT.json exists at ZIP root.
8. Copy only patch files.
9. Regenerate startup delivery with sync_startup_routing_kernel_pack.py --ensure-sync --yes.
10. Verify KANDA_FREEZE_HINT.json was not installed into project root.
11. Show install success.
12. Wait 5 seconds.
13. Clear terminal.
14. Keep terminal open.

## 11.3 Install failure behavior

On install failure:

1. Show INSTALL FAILED.
2. Show error message.
3. Read-Host.
4. Clear-Host.
5. Read-Host again.
6. Clear-Host.
7. Keep terminal open.

---

# 12. Validation roadmap

## 12.1 Validation must check files

Validation script checks:

1. New prompt exists.
2. Metadata exists.
3. Folder assimilation references the prompt.
4. Routing indexes reference the prompt.
5. Startup hook exists in generated paste file.
6. Startup ZIP contains updated relevant files.
7. sync_startup_routing_kernel_pack.py --check returns STATUS: IN_SYNC.
8. KANDA_FREEZE_HINT.json exists in staged ZIP.
9. KANDA_FREEZE_HINT.json is not installed into project root.

## 12.2 Validation must check prompt content

Validation script checks prompt contains:

1. TERMINAL_OUTPUT_CONTRACT
2. PATCH_DELIVERY_CONTRACT
3. FREEZE_FORM_JSON_CONTRACT
4. VALIDATION_EVIDENCE_CONTRACT
5. FREEZE_HINT_SIDECAR_CONTRACT
6. MULTI_PROJECT_ROOT_CONTRACT
7. forbidden old mixed terminal footer
8. strict JSON rules
9. exact validation marker rule
10. sidecar wins over chat memory rule

## 12.3 Validation must check startup sync

Expected output includes:

STATUS: IN_SYNC

## 12.4 Validation must output recognizer-friendly evidence

Validation block must output:

VALIDATION OK: pre_output_contract_gates_v1
CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated
STATUS: IN_SYNC

## 12.5 Validation cleanup footer

Validation block must use:

Read-Host
Clear-Host
Read-Host
Clear-Host

Not 5-second success cleanup.

---

# 13. Post-validation freeze-intake roadmap

After validation passes:

1. Call or run merge_validation_evidence_into_latest_hint if required.
2. Ensure latest freeze hint contains:
   VALIDATION OK: pre_output_contract_gates_v1
   STATUS: IN_SYNC
3. Open Freeze Feature After Update.
4. Confirm Project root is E:\kanda_reasoner for this feature.
5. Click New Local Freeze Entry.
6. Confirm form title is:
   Pre-Output Contract Gates v1
7. Confirm validation_evidence_summary contains:
   VALIDATION OK: pre_output_contract_gates_v1
8. Preview Freeze Entry.
9. Confirm and Write.
10. Startup freeze context must refresh after local write.

---

# 14. Freeze roadmap

## 14.1 Freeze title

Pre-Output Contract Gates v1

## 14.2 Freeze do-not-regress rules

Include these rules:

1. Terminal blocks must be classified before footer generation.
2. Install success must use 5-second clear and no Enter prompt.
3. Validation, diagnostic, and error blocks must use Enter, clear, Enter, clear.
4. Patch install instructions must move ZIP to staging and extract fresh.
5. Freeze-ready patch ZIPs must include root-level KANDA_FREEZE_HINT.json.
6. KANDA_FREEZE_HINT.json must describe current feature.
7. Freeze-form JSON must be exact marker-wrapped valid JSON.
8. validation_evidence_summary must include VALIDATION OK: feature_id when validated.
9. AI must block freeze JSON if validation marker is missing.
10. Sidecar identity beats stale chat memory.
11. Same-source rescans must not downgrade local validation evidence.
12. Multi-project freeze paths must use selected active project root.
13. Fast Path must remain lean and not over-route.
14. Do not load all prompts daily.
15. Do not remove Confirm and Write.

## 14.3 Freeze validation evidence

Use only actual validation evidence.

Required:

VALIDATION OK: pre_output_contract_gates_v1
STATUS: IN_SYNC

Optional:

CONTRACT_TEST_OK: ...
SANDBOX_..._VALIDATION_OK

Do not invent.

---

# 15. Manual pilot roadmap after patch

Run these after install and validation.

## 15.1 First run: RG-031 to RG-035

These directly cover the old failures:

1. RG-031 terminal install success
2. RG-032 terminal validation
3. RG-033 patch staging
4. RG-034 strict freeze JSON
5. RG-035 missing validation marker

If any fail, repair before running the rest.

## 15.2 Second run: RG-036 to RG-040

These cover integration and boundaries:

1. RG-036 freeze-ready sidecar
2. RG-037 sidecar beats chat memory
3. RG-038 monotonic freeze hint
4. RG-039 external project root
5. RG-040 Fast Path no-overrouting

## 15.3 Regression retest

Retest older closed routes:

1. RG-028 confirmation-gate bypass
2. RG-029 stale startup filename
3. RG-030 Fast Path no-overrouting if needed

Reason:

Ensure the new pre-output gate did not over-route simple tasks or break existing first-position overrides.

---

# 16. Acceptance criteria

The feature is accepted only if all are true:

1. Startup delivery is IN_SYNC.
2. New prompt is registered and routed.
3. Generated startup paste includes the short hook.
4. Install block uses correct success footer.
5. Validation block uses correct validation footer.
6. Patch delivery uses staging and fresh extraction.
7. Freeze JSON is parser-safe on first attempt.
8. Missing validation marker blocks freeze JSON.
9. Freeze-ready patch includes KANDA_FREEZE_HINT.json.
10. Sidecar identity beats chat memory.
11. Monotonic validation evidence is preserved.
12. External project freeze paths use selected active project root.
13. Fast Path remains Fast Path.
14. Local freeze entry can be created and frozen.
15. No project-specific freeze state is stored in project_freeze_ledger.

---

# 17. Failure handling roadmap

## 17.1 If terminal tests fail

Repair terminal contract wording and test again.

Do not proceed to freeze.

## 17.2 If patch staging fails

Repair patch delivery contract and install template.

Do not proceed to freeze.

## 17.3 If freeze JSON parser fails

Repair strict freeze-form JSON contract.

Prefer compact one-line JSON.

Avoid unescaped Windows backslashes inside JSON strings.

## 17.4 If validation marker is missing

Repair validation evidence contract.

Ensure validation block merges:

VALIDATION OK: pre_output_contract_gates_v1

into latest freeze hint.

## 17.5 If sidecar identity fails

Repair freeze hint sidecar contract.

Ensure AI does not infer current feature from chat memory when sidecar exists.

## 17.6 If external project root fails

Repair multi-project root contract.

Confirm active project root is passed into freeze-intake and freeze-memory logic.

## 17.7 If Fast Path over-routes

Move some hook text out of always-startup.

Keep only a tiny trigger in startup.

Keep full prompt on-request.

---

# 18. Documentation roadmap

After implementation, update documentation with:

1. Why output-time compliance was added.
2. Difference between router and contract gate.
3. Supported artifact types.
4. Terminal cleanup canon.
5. Patch staging canon.
6. Freeze JSON strict contract.
7. Validation evidence exact marker rule.
8. KANDA_FREEZE_HINT.json sidecar rule.
9. Multi-project root rule.
10. RG-031 to RG-040 test matrix.
11. Freeze entry location.
12. How to debug failures.

---

# 19. Future expansion roadmap

Only after this feature is validated and frozen:

## 19.1 Add automated artifact validators

Optional future validators:

1. validate_terminal_footer_contract.py
2. validate_patch_staging_contract.py
3. validate_freeze_json_contract.py
4. validate_freeze_hint_sidecar_contract.py
5. validate_multi_project_freeze_paths.py

## 19.2 Add GUI exposure

Possible future UI:

1. Contract gate status.
2. Last freeze hint source.
3. Last validation marker found.
4. Stale exposure warning.
5. Active project root confirmation.

## 19.3 Add test dashboard

Possible future tab:

1. RG-031 status.
2. RG-032 status.
3. RG-033 status.
4. RG-034 status.
5. RG-035 status.
6. RG-036 status.
7. RG-037 status.
8. RG-038 status.
9. RG-039 status.
10. RG-040 status.

---

# 20. Final roadmap summary

Implement in this exact order:

1. Audit existing prompt files and confirm source-of-truth files.
2. Create pre_output_contract_gates.md.
3. Add prompt metadata.
4. Register prompt in folder and routing indexes.
5. Add tiny startup hook.
6. Update daily patch delivery guardrails.
7. Update freeze code intake protocol.
8. Regenerate startup artifacts.
9. Add KANDA_FREEZE_HINT.json to patch ZIP.
10. Build install command with correct install footer.
11. Build validation command with correct validation footer.
12. Validate prompt registration and startup sync.
13. Validate contract content.
14. Run RG-031 to RG-035.
15. Run RG-036 to RG-040.
16. Retest RG-028 and RG-029.
17. Merge validation evidence into freeze hint intake.
18. Use New Local Freeze Entry.
19. Confirm and Write after human review.
20. Refresh startup freeze context.
21. Freeze pre_output_contract_gates_v1.
22. Create final handoff.

The implementation succeeds when the AI no longer merely knows the canon, but is forced to apply the canon immediately before producing high-risk artifacts.
