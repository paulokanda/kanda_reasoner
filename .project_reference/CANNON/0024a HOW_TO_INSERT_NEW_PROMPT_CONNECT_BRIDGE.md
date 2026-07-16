# Handoff: How to create a prompt and connect it to KANDA prompt-router logic using a short bridge

## Purpose

This handoff explains how to add a new prompt to the KANDA prompt library and make the AI aware of it through router logic without loading the entire prompt during startup.

The target pattern is:

```text
Full prompt = routed prompt, loaded only when needed.
Router bridge = short pointer/hook that tells AI when to request/load the full prompt.
Startup = should not contain the full prompt unless the prompt is truly always-startup.
```

Use this when adding prompts such as:

```text
error_memory_active_ready_correction_blueprint
freeze_intake_review_blueprint
patch_zip_validation_blueprint
specialized audit prompts
domain-specific correction prompts
```

The goal is to avoid bloating startup while still ensuring that future AI sessions discover the prompt when the user task requires it.

---

## Core principle

Do not make every important prompt an always-startup prompt.

A prompt can be important but still routed.

The AI becomes aware through three layers:

```text
1. Metadata
   prompt_library/METADATA/<prompt_id>.meta.json

2. Folder assimilation
   ACTIVE_PROMPTS/<target_folder>/_FOLDER_ASSIMILATION.md

3. Router/navigation bridge
   ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
   and/or prompt_router.md
   and/or kanda_routing_system_canon.md
```

This is the bridge model:

```text
The full prompt lives in the correct ACTIVE_PROMPTS folder.

The router has a short bridge that says:
"When task X appears, require prompt Y."

The startup/session load does not need to include full prompt Y.
It only needs enough routing awareness to know prompt Y exists and when to request it.
```

---

## Canonical source locations

Canonical source:

```text
E:\kanda_reasoner\kanda_prompt_workspace\prompt_library
```

Active prompt folders:

```text
E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS
```

Prompt metadata:

```text
E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\METADATA
```

Router/navigation folder:

```text
E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing
```

Generated startup artifacts:

```text
E:\kanda_reasoner\kanda_prompt_workspace\first_AI_deliver
```

Do not directly edit generated startup files as canonical source:

```text
first_prompts_to_ai.zip
paste_after_first_prompts_to_ai.md
tell_AI_read_before_all.md
first_AI_deliver/*
```

Generated files are outputs. Change canonical prompt source and generator/source-map inputs, then regenerate when needed.

---

## Prompt type decision

Before adding a prompt, classify it.

### 1. Always-startup prompt

Use only when the prompt must be loaded every serious AI session.

Examples:

```text
startup read order
first response shape
session upload checklist
global startup safety rule
```

Load mode:

```text
always_startup
```

Usually placed in:

```text
ACTIVE_PROMPTS/01_session_start_and_navigation
```

Requires startup source-map/generator sync.

### 2. Normal routed prompt

Use when the prompt should be called only when task signals match.

Examples:

```text
error_memory_active_ready_correction_blueprint
python testing prompt
patch delivery prompt
schema audit prompt
domain-specific correction prompt
```

Load mode:

```text
routed
```

Requires metadata, folder assimilation, and router/navigation bridge.

### 3. On-request specialist prompt

Use when the prompt should be available but only loaded if explicitly requested or selected by a routed workflow.

Load mode:

```text
on_request
```

Register in folder assimilation and navigation index. Do not auto-load.

### 4. Maintenance-only prompt

Use only for prompt tools, startup delivery, generated artifacts, or governance machinery.

Load mode:

```text
maintenance_only
```

Do not load in normal startup unless a governed maintenance workflow explicitly requires it.

---

## Correct folder selection

Choose the folder based on prompt purpose.

Common examples:

```text
Startup/session prompt:
ACTIVE_PROMPTS/01_session_start_and_navigation

Prompt router/navigation prompt:
ACTIVE_PROMPTS/02_prompt_routing_and_indexing

Freeze/governance prompt:
ACTIVE_PROMPTS/03_governance_freeze_and_handoff

Box architecture prompt:
ACTIVE_PROMPTS/04_box_architecture_and_boundaries

Patch delivery/validation prompt:
ACTIVE_PROMPTS/05_patch_delivery_and_validation

Prompt-authoring/audit prompt:
ACTIVE_PROMPTS/07_prompt_authoring_and_audit

Testing/observability prompt:
ACTIVE_PROMPTS/09_python_quality_security_observability

Reusable project canon:
ACTIVE_PROMPTS/12_generalized_project_canons
```

For the Error Memory active-ready correction blueprint, preferred placement is:

```text
ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_correction_blueprint.md
```

Reason:

```text
It is a reusable project canon/state-machine and schema contract.
It is not a startup prompt.
It is not only a patch delivery prompt.
It is not generic Python engineering.
It should be routed when Error Memory draft-to-active correction is requested.
```

---

## Required files for a routed prompt

For a routed prompt, create/update these:

```text
1. Full prompt file
   ACTIVE_PROMPTS/<target_folder>/<prompt_id>.md

2. Metadata
   METADATA/<prompt_id>.meta.json

3. Folder assimilation
   ACTIVE_PROMPTS/<target_folder>/_FOLDER_ASSIMILATION.md

4. Router/navigation bridge
   ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
   and/or ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md
   and/or ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md

5. Tests / validation script
   validation/test_<prompt_id>_routing.py
   or equivalent prompt-library validation file
```

Do not update startup source map unless the prompt is truly always-startup.

---

## Full prompt file structure

Create a stable lowercase file:

```text
error_memory_active_ready_correction_blueprint.md
```

Recommended structure:

```text
# Error Memory Active-Ready Correction Blueprint

## Purpose

## When to use

## When not to use

## Required context

## Required behavior

## Draft-to-active rules

## Active-ready schema checklist

## Evidence rules

## Output shape

## Safety and governance rules

## Validation expectations

## Do-not-regress rules
```

For this specific blueprint, it should say:

```text
- Do not output status: active unless the active-ready checklist passes.
- Do not invent validation evidence.
- If source_patch_zip, install_command_summary, validation_command_summary, regression_check.command, regression_check.expected_marker, raw_error_text, or redaction.rules are missing, keep the lesson draft/needs_ai_review.
- regression_check.type must be validation_command for active-ready lessons.
- regression_check.command must use forward slashes.
- Do not use Heuristic Correction to promote a draft.
- If evidence is incomplete, say what is missing and ask for the correction patch/validation evidence.
```

---

## Metadata file

Create:

```text
kanda_prompt_workspace/prompt_library/METADATA/error_memory_active_ready_correction_blueprint.meta.json
```

Example:

```json
{
  "prompt_id": "error_memory_active_ready_correction_blueprint",
  "title": "Error Memory Active-Ready Correction Blueprint",
  "folder": "ACTIVE_PROMPTS/12_generalized_project_canons",
  "path": "ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_correction_blueprint.md",
  "load_mode": "routed",
  "status": "active",
  "owner": "prompt_library",
  "created_for": "Convert Error Memory draft lessons into valid active-ready lessons only when evidence is complete.",
  "routing_intents": [
    "error memory draft correction",
    "KANDA_ERROR_LESSON_JSON active-ready conversion",
    "Memorize Error missing active-ready fields",
    "convert draft Error Memory lesson to active",
    "validation_command_summary source_patch_zip regression_check missing"
  ],
  "requires": [
    "ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md",
    "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
    "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md"
  ],
  "do_not_regress": [
    "Do not make this prompt always_startup without explicit approval.",
    "Do not output active Error Memory lessons without full active-ready evidence.",
    "Do not use Windows backslashes in regression_check.command.",
    "Do not treat draft normalization as active correction."
  ]
}
```

---

## Folder assimilation update

Update:

```text
ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md
```

Add a compact entry:

```text
## error_memory_active_ready_correction_blueprint

Purpose:
Defines the active-ready Error Memory draft-to-active correction contract.

When to use:
Use when the task involves correcting, promoting, validating, or converting a KANDA_ERROR_LESSON_JSON draft into an active-ready or active lesson.

When not to use:
Do not use for ordinary code patches, generic Error Memory review, or GUI behavior patches unless the task specifically involves Error Memory lesson schema/promotion.

Routing notes:
This is a routed prompt. It must not be always-startup. Router/navigation should request it when draft-to-active Error Memory conversion is requested.

Dependencies:
- Error Memory active-ready validator behavior.
- Prompt routing/navigation bridge.
- Project patch validation and freeze evidence when active status is requested.

Do-not-regress:
- Do not output status active unless active-ready evidence is complete.
- Do not invent validation evidence.
- Do not use backslashes in regression_check.command.
```

The folder assimilation entry helps future AI identify the prompt’s role without opening every prompt in the folder.

---

## Router/navigation bridge

The bridge is a short routing entry, not the full prompt.

It belongs in the current router/navigation files, usually one or more of:

```text
ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md
ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md
ACTIVE_PROMPTS/02_prompt_routing_and_indexing/_FOLDER_ASSIMILATION.md
```

Do not guess which file is authoritative. Inspect the current project router format first.

A good bridge entry is:

```text
## Error Memory active-ready correction bridge

When the task involves converting, correcting, promoting, or validating a KANDA_ERROR_LESSON_JSON draft so it can become active, do not rely on memory or heuristic correction.

Task classification:
Governed Error Memory draft-to-active correction request.

Required routed prompt:
- error_memory_active_ready_correction_blueprint

Trigger examples:
- "correct this Error Memory draft"
- "make this lesson active-ready"
- "Memorize Error says missing active-ready fields"
- "validation_command_summary/source_patch_zip/regression_check missing"
- "convert draft to active lesson"
- "KANDA_ERROR_LESSON_JSON_BEGIN ... status draft"
- "This lesson is not ready for active status"
- "regression_check.type must be validation_command"
- "regression_check.command is empty"
- "source_patch_zip is empty"
- "install_command_summary is empty"

Behavior:
- Load or request error_memory_active_ready_correction_blueprint before producing active JSON.
- If validation evidence is missing, keep the lesson draft/needs_ai_review.
- Do not output status active unless the full active-ready checklist passes.
- Do not invent source_patch_zip, validation_evidence, regression_check.command, or expected_marker.
- Use forward slashes in regression_check.command.
- If the user only provided a failed draft and no successful correction evidence, return a corrected draft or request the missing evidence instead of marking active.

Missing context behavior:
If the source patch ZIP, validation command, expected marker, or successful validation evidence is not available, say exactly which active-ready fields are missing and do not produce an active lesson.

Anti-bypass behavior:
If the user asks to "just make it active" while required evidence is missing, refuse promotion and route to draft/needs_ai_review.
```

This bridge tells the router when to load the full blueprint, without putting the full blueprint into startup.

---

## Why use a bridge instead of startup-loading the full prompt?

Use the bridge because:

```text
- The full blueprint is useful only for a specific task class.
- Loading it every startup adds noise.
- A routed bridge keeps startup small.
- The router can still discover the prompt when the task requires it.
- The full prompt can evolve independently while the bridge stays compact.
```

Startup should contain the minimum routing awareness required to request the prompt, not the full prompt body.

---

## How future AI should use the bridge

When a user asks:

```text
Here is a KANDA_ERROR_LESSON_JSON draft. Make it active.
```

The router should answer internally:

```text
Task classification:
Governed Error Memory draft-to-active correction request.

Required prompt:
error_memory_active_ready_correction_blueprint

Next action:
Load/request the blueprint before producing active JSON.
```

Then the AI should inspect the lesson and classify it:

```text
active-ready: all evidence present
draft-only: structurally valid but missing evidence
needs_ai_review: incomplete and cannot be safely completed without AI/manual evidence
invalid: not even draft-saveable
```

Only `active-ready` may be output with:

```text
status: active
```

---

## Validation requirements

A routed prompt bridge is valid only when tests prove all of this:

```text
prompt file exists in the correct ACTIVE_PROMPTS folder
metadata exists and matches prompt_id/path/load_mode
load_mode is routed, not always_startup
folder assimilation references the prompt
router/navigation bridge references the prompt
router/navigation can discover the prompt from matching trigger text
non-matching tasks do not route to the prompt
startup source map does not include the full prompt as always-startup
generated startup ZIP does not include the full blueprint as a startup file
no generated artifact is treated as canonical source
no stale validation\<test_name>.py examples remain
all regression_check.command examples use forward slashes
```

Example routing tests:

```text
Input:
"Correct this KANDA_ERROR_LESSON_JSON draft. Memorize Error says source_patch_zip is empty."

Expected:
Routes to error_memory_active_ready_correction_blueprint.

Input:
"Create a patch for a GUI button layout issue."

Expected:
Does not route to error_memory_active_ready_correction_blueprint unless Error Memory draft-to-active conversion is also requested.

Input:
"Make this Error Memory lesson active even though validation evidence is missing."

Expected:
Routes to blueprint and blocks active output; returns missing active-ready fields.
```

---

## Patch packaging requirements

If this is delivered as a patch ZIP, include:

```text
KANDA_FREEZE_HINT.json at ZIP root
new full prompt file
metadata file
updated target folder _FOLDER_ASSIMILATION.md
updated router/navigation bridge file(s)
validation script
bundle_manifest.json
optional Error Memory lesson receive block for this prompt/canon update
```

Do not place `KANDA_FREEZE_HINT.json` in the project root during install. It is ZIP delivery metadata.

---

## Freeze requirements

After installation and validation pass:

```text
1. Use Freeze Feature After Update.
2. Preview the freeze entry.
3. Confirm and Write only after validation evidence is present.
4. Store project-specific freeze memory under:
   project_freeze_after_update/frozen_features_memory
5. Do not store project-specific freeze memory under:
   project_freeze_ledger
6. Refresh startup freeze context after freeze.
```

---

## Common mistakes to avoid

```text
Mistake:
Putting the full prompt in startup because it is important.

Fix:
Make it routed. Add a short router bridge.

Mistake:
Editing first_prompts_to_ai.zip directly.

Fix:
Edit canonical source in prompt_library and regenerate generated artifacts only if needed.

Mistake:
Creating the prompt file but no metadata.

Fix:
Add METADATA/<prompt_id>.meta.json.

Mistake:
Creating metadata but no folder assimilation.

Fix:
Update _FOLDER_ASSIMILATION.md so future AI can discover intent.

Mistake:
Adding bridge text to the wrong folder only.

Fix:
Router bridge belongs in routing/navigation files under 02_prompt_routing_and_indexing.

Mistake:
Router bridge is too broad.

Fix:
Use trigger examples and when-not-to-use behavior to avoid over-calling.

Mistake:
Making a routed prompt always_startup.

Fix:
Use load_mode routed unless the prompt must load every session.

Mistake:
No validation.

Fix:
Test both positive routing and negative routing.

Mistake:
Prompt says active lessons can use incomplete evidence.

Fix:
Active-ready correction prompts must block active output unless evidence is complete.
```

---

## Minimal checklist for future AI

Before implementing a prompt bridge, complete this checklist:

```text
[ ] Classify the prompt type.
[ ] Choose the correct ACTIVE_PROMPTS folder.
[ ] Search for duplicate/overlapping prompts.
[ ] Inspect target folder _FOLDER_ASSIMILATION.md.
[ ] Inspect current router/navigation files.
[ ] Create or update the full prompt file.
[ ] Create or update metadata.
[ ] Update folder assimilation.
[ ] Add a short router/navigation bridge.
[ ] Do not add full prompt to startup unless explicitly always-startup.
[ ] Validate positive routing.
[ ] Validate negative routing.
[ ] Validate startup ZIP does not include routed prompt as always-startup.
[ ] Validate no generated artifact is treated as source.
[ ] Package patch with KANDA_FREEZE_HINT.json.
[ ] Freeze after validation passes.
[ ] Refresh startup freeze context after freeze.
```

---

## Example: Error Memory active-ready correction blueprint

Full prompt:

```text
ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_correction_blueprint.md
```

Metadata:

```text
METADATA/error_memory_active_ready_correction_blueprint.meta.json
```

Folder assimilation:

```text
ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md
```

Router bridge:

```text
ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
and/or prompt_router.md
and/or kanda_routing_system_canon.md
```

Load mode:

```text
routed
```

Do not add to:

```text
STARTUP_ROUTING_KERNEL_SOURCES.json
```

unless a separate governed startup decision says the full prompt must always load.

Bridge text:

```text
## Error Memory active-ready correction bridge

When the task involves converting, correcting, promoting, or validating a KANDA_ERROR_LESSON_JSON draft so it can become active, do not rely on memory or heuristic correction.

Required routed prompt:
- error_memory_active_ready_correction_blueprint

Trigger examples:
- "correct this Error Memory draft"
- "make this lesson active-ready"
- "Memorize Error says missing active-ready fields"
- "validation_command_summary/source_patch_zip/regression_check missing"
- "convert draft to active lesson"
- "KANDA_ERROR_LESSON_JSON_BEGIN ... status draft"

Behavior:
- Load or request the blueprint before producing active JSON.
- If validation evidence is missing, keep the lesson draft/needs_ai_review.
- Do not output status active unless the full active-ready checklist passes.
```

Expected validation:

```text
VALIDATION OK: error-memory-active-ready-correction-blueprint-v31
STATUS: IN_SYNC
```

Final invariant:

```text
Full blueprint: routed prompt.
Startup/router awareness: small bridge only.
Generated artifacts: updated only through sync, never edited as source.
```
