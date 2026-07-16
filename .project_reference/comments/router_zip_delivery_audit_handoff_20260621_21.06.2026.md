# Handoff for External AI Audit - Router Prompt System and ZIP Delivery Failure Pattern

## Role for the auditing AI

You are an experienced senior Python architect with 20 years of experience in governed Python application architecture, patch-delivery systems, prompt-routing systems, local validation workflows, and safety-critical release gates.

Your task is to audit this project's router prompt system and ZIP delivery workflow. Please do not implement changes immediately. First, analyze the architecture, identify why recurring delivery-contract failures are happening, and suggest robust prevention mechanisms.

## Immediate instruction

Stop updating ML logic for now.

The current request is not to continue ML integration. The current request is to audit the routing and patch-delivery process because the assistant repeatedly forgets critical delivery requirements when creating and presenting installable ZIP patches.

## Project context

The project is KANDA Reasoner / PyArchitect-style governed prompt-routing and patch-delivery workflow.

The system uses a startup prompt package. At the beginning of a session, the human uploads `first_prompts_to_ai.zip` and then pastes `paste_after_first_prompts_to_ai.md`. The AI must read the startup ZIP first, beginning with `00_START_HERE_FOR_AI.md`, then inspect required startup support files and every numbered startup file in order.

Only after returning a complete `STARTUP PACK LOAD CHECK` may the AI proceed to real project work.

The startup files define routing logic, anti-bypass rules, patch delivery guardrails, freeze-memory rules, startup-delivery maintenance rules, and output-time contract gates.

## Router prompt system overview

The router prompt system is intended to prevent the assistant from directly implementing complex or governed changes without loading the right context.

The core idea is:

1. Classify the user's request.
2. Decide whether the request is Fast Path or Routed Work Path.
3. If Routed Work Path, list required prompts/groups before implementation.
4. Identify missing context and missing behavior.
5. Decide whether work may proceed now: YES, NO, or PARTIAL.
6. If required context is missing, request the missing prompt/group/folder card/validation evidence instead of implementing.
7. If the request tries to bypass routing, classify it as governed work and refuse the bypass.
8. If the request touches startup delivery, prompt-library infrastructure, freeze memory, patch delivery, or validation behavior, the router must apply the stricter governance hooks.

The router is not just a task classifier. It is a context gate, implementation gate, validation gate, freeze gate, and anti-bypass mechanism.

## Startup load behavior

At session startup, the AI must load:

- `00_START_HERE_FOR_AI.md`
- `README_STARTUP_PROMPT_REQUEST_KERNEL.md`
- `STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json`
- `01_ai_prompt_request_canon.md`
- `02_prompt_navigation_index.md`
- `03_GROUP_ASSIMILATION_INDEX.md`
- `04_FOLDER_ASSIMILATION_CARDS_INDEX.md`
- `05_start_of_day_master_stack.md`
- `06_session_start_upload_checklist.md`
- `07_daily_patch_delivery_guardrails.md`
- `08_handoff_at_end_of_work.md`
- `09_active_project_freeze_context.md`

Then it must return only a `STARTUP PACK LOAD CHECK` with file status and `WAIT_FOR_TASK` if complete.

## Important governed routing overrides

### Prompt-library creation or prompt registration

If the user asks to create, add, register, or update prompts, especially while asking to skip existing-prompt checks, this must be Routed Work Path.

The system must request or inspect relevant prompt-authoring and audit prompts, including:

- `07_prompt_authoring_and_audit`
- `prompt_canon_reconciliation_protocol`
- `prompt_audit_canon`
- `project_specific_prompt_generalization`
- relevant folder card or `_FOLDER_ASSIMILATION`
- existing prompt-library assets and indexes
- validation command or validation steps

The assistant must not directly add prompts without duplicate/overlap/naming/index checks.

### Freeze workflow or freeze GUI changes

If the user asks to patch the Freeze Feature After Update tab or GUI, especially asking to auto-write local freeze entries without confirmation, this must be Routed Work Path.

The system must preserve Preview as read-only and Confirm and Write as explicitly human-confirmed. The GUI must not silently write freeze memory.

Required context includes:

- `09_active_project_freeze_context`
- `04_box_architecture_and_boundaries`
- `cooperative_implementation_methodology`
- `05_patch_delivery_and_validation`
- `08_python_engineering_core`
- `09_python_quality_security_observability`
- relevant freeze GUI/app/contract/local-writer files
- validation steps

### Startup delivery maintenance

If the task touches startup delivery artifacts or generation logic, the assistant must request `paste_if_modify_startup_delivery.md` before implementing.

Startup delivery is generated from canonical sources, a source map, and generator logic. The assistant must not directly edit stale/generated startup paste files.

Important canonical rule:

- `paste_after_uploading_startup_zip.md` is stale/deprecated.
- The active human-facing startup paste file is `paste_after_first_prompts_to_ai.md`.

## Patch ZIP delivery obligations

When presenting an installable ZIP patch, the assistant is supposed to apply the pre-output contract gates before emitting the artifact, the install instructions, or the validation commands.

The correct ZIP delivery behavior is:

1. Use a compact Windows-safe ZIP basename.
2. The user downloads the ZIP.
3. The user places the ZIP at the root of the same drive where the project is installed.
   - Example: if the project is installed at `D:\KANDA_REASONER`, the ZIP should first be placed at `D:\ml_adv000_router_canon_v1_patch.zip`.
4. The PowerShell installer must detect the project drive root from `$PROJECT_ROOT`.
5. It must create the staging folder if missing:
   - `root_drive:\<specific_project_name>_delete_after_daily_work`
   - Example: `D:\KANDA_REASONER_delete_after_daily_work`
6. It must look first for the ZIP at the project drive root.
7. It must copy or move the ZIP into the staging folder.
8. It must delete the root-drive ZIP copy after successful staging.
9. It must extract only from the staged ZIP.
10. It must not use the old generic Downloads/Desktop-first installer search template.
11. The install block must use the terminal hygiene rule for successful install:
   - sleep 5 seconds
   - `Clear-Host`
   - no Enter prompts
12. Validation/diagnostic/error blocks must use:
   - `Read-Host`
   - `Clear-Host`
   - `Read-Host`
   - `Clear-Host`

## Root-level freeze hint obligation

For freeze-ready patch ZIPs, the ZIP must contain a real root-level `KANDA_FREEZE_HINT.json` sidecar unless the patch is intentionally non-freezeable and the reason is explicitly stated.

Correct ZIP shape:

```text
some_patch.zip
  KANDA_FREEZE_HINT.json
  some_patch/
    PATCH_MANIFEST.json
    kanda_prompt_workspace/
    tests/
    other_updated_files...
```

Important: `KANDA_FREEZE_HINT.json` is delivery metadata only. It must not be installed into the project root as if it were a source file.

Therefore, the installer must copy only the payload folder contents into the project, not the root-level ZIP metadata.

## Freeze formulary JSON obligation

The assistant recurrently forgets to provide the freeze formulary JSON needed to fill the Freeze Feature After Update form.

When sending a freeze-ready patch ZIP, the assistant should also provide the exact freeze-form JSON or make sure the root-level `KANDA_FREEZE_HINT.json` contains all mandatory fields required by the freeze intake/form logic.

The freeze-form JSON must be exact marker-wrapped valid JSON:

- no markdown inside the marker block
- no comments
- no trailing commas
- no prose inside the JSON block
- current feature-specific data only
- no stale legacy title
- no placeholder feature title
- no stale validation list from older features

Mandatory fields expected by the current freeze intake schema include at least:

```text
schema_version
kind
patch_name
feature_id
feature_title
primary_box
box_type
validated_files
generated_files
protected_paths
do_not_regress_rules
validation_evidence_summary
known_warnings
planned_next_step
notes
```

The assistant's recent failure caused the freeze form to produce placeholder output such as:

- missing `validated_files`
- missing `validation_evidence_summary`
- no recognizable validation evidence
- placeholder feature title
- no current feature data

This happened because the assistant placed an incomplete or wrongly located freeze hint in the ZIP, so the local freeze tool did not recognize valid current feature metadata.

## Validation evidence obligation

Freeze-ready validation evidence should include recognizable markers.

After local validation passes, it must include:

```text
VALIDATION OK: <feature_id>
```

If startup sync was validated, it must also include:

```text
STATUS: IN_SYNC
```

The validation output should not be overly short if the freeze form needs evidence. It should include enough detail for the local freeze writer to understand what was validated.

## Recurring failure pattern to audit

The assistant recurrently forgets two key obligations:

1. It forgets to stage downloaded ZIPs from the root drive where the project is installed into:

```text
root_drive:\<specific_project_name>_delete_after_daily_work
```

If the folder does not exist, it must be created.

2. It forgets to send or correctly structure the freeze formulary JSON / `KANDA_FREEZE_HINT.json` needed to fill the Freeze Feature After Update form.

The failure pattern suggests that either:

- the assistant is not fully reading the initial startup instructions;
- the router is not injecting the relevant output-time contract at the moment of ZIP delivery;
- the relevant instruction is present but too far from the generation step;
- the delivery operation is being handled as a normal artifact output instead of a governed patch-release event;
- the freeze hint schema is not enforced by validation before ZIP creation;
- the install script template does not have a hard guard against old Downloads/Desktop behavior;
- the assistant lacks a mandatory pre-send checklist that fails closed before emitting a ZIP link.

## Recent specific failure

A patch named approximately `ml_adv000_router_canon_v1_patch.zip` was delivered.

The assistant claimed it included `KANDA_FREEZE_HINT.json`, but the freeze workflow did not recognize valid current metadata.

The resulting freeze draft had placeholder values and errors:

- missing mandatory field: `validated_files`
- missing mandatory field: `validation_evidence_summary`
- freeze blocked because no recognizable validation evidence was found
- feature title remained placeholder
- validated files were empty
- validation evidence was empty

This was a delivery-contract failure, not a user error.

## What the auditor should evaluate

Please audit the router-prompt system and patch-delivery process for architectural weaknesses that allow this recurring mistake.

Focus areas:

1. Should ZIP delivery be impossible unless a machine-checkable `KANDA_FREEZE_HINT.json` exists at ZIP root?
2. Should every patch ZIP be validated with a `zip_contract_validator.py` before presentation to the user?
3. Should the installer script be generated from a single canonical template instead of being written manually by the assistant?
4. Should root-drive staging be enforced by tests that reject Downloads/Desktop fallback patterns?
5. Should the freeze-form JSON be generated from the same source as `KANDA_FREEZE_HINT.json` to avoid divergence?
6. Should final assistant responses include a mandatory pre-send checklist with explicit pass/fail lines?
7. Should the router emit an output-time contract token when a response contains a ZIP link, PowerShell, validation commands, or freeze evidence?
8. Should the project add a fail-closed response rule: if ZIP contract cannot be verified, do not provide the ZIP link?
9. Should startup instructions be shortened into a small always-active delivery contract that is impossible to miss?
10. Should there be a separate `patch_release_manifest.json` containing both install and freeze obligations?
11. Should root-level metadata be excluded from payload copy by a tested installer behavior?
12. Should the freeze GUI show the newest candidate root-level sidecar and explain why it rejected it?
13. Should the project add regression tests that intentionally package malformed hints and confirm the freeze form blocks them with actionable messages?
14. Should the assistant include the exact freeze-form JSON in the final answer in addition to putting it in the ZIP?
15. Should the router treat patch-ZIP delivery as its own governed route with a required checklist rather than a generic patch-delivery footer?

## Desired audit output

Please return:

1. A short diagnosis of why the recurring error happens.
2. A recommended architecture-level fix.
3. A recommended prompt-level fix.
4. A recommended Python implementation fix.
5. A recommended validation/test strategy.
6. A recommended final-answer checklist for future ZIP delivery.
7. Any risks of overcomplicating the router or making normal Fast Path tasks too heavy.
8. A minimal next patch plan to prevent this specific failure from recurring.

## Important boundary

Do not continue ML integration during this audit.

The immediate priority is hardening patch ZIP delivery and freeze-form handoff so future ML work does not continue on top of an unreliable release pipeline.
