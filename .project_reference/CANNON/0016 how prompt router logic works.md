# 0016 - How Prompt Router Logic Works

Status: canonical project reference
Scope: KANDA Reasoner prompt routing, prompt-library updates, startup prompt delivery, and safe prompt installation
Audience: AI assistant working on KANDA Reasoner with Rafael Kanda

## Purpose

This file explains how the KANDA prompt router is supposed to work, especially when a human asks the AI to add, update, install, register, or freeze a prompt.

The main goal is simple:

The AI must ask for the correct prompt/context set for the task, not all prompts blindly, and not proceed from memory when governed prompt files are missing.

KANDA is a multi-prompt system. It is not one giant prompt. The router decides which prompt groups are needed for each task.

## Core rule

If the AI forgets a rule, is unsure how to route a task, or does not remember the correct install/update workflow, it must not assume, guess, or invent.

The AI must first go back to the router logic and the relevant prompt navigation/index files to recover the correct rule.

If the router/index context is still insufficient, the AI must ask the human for the missing rule, file, prompt group, folder card, or decision.

The human is the project partner. Asking is safer than hallucinating.

## Fast Path vs Routed Work Path

### Fast Path

Use Fast Path only for simple tasks that do not modify governed project state.

Examples:

- Explain a concept in simple terms.
- Rewrite a sentence.
- Summarize already-provided text.
- Interpret a status message when no code, prompt, startup, freeze, or file change is requested.

Fast Path usually means:

- No extra prompt groups required.
- Estimated context load is small.
- May proceed now is usually YES.
- No patch, no implementation, no source inspection, no file write.

### Routed Work Path

Use Routed Work Path for governed project work.

Examples:

- Create, add, install, register, or update a prompt.
- Modify prompt-library files or prompt indexes.
- Modify startup delivery, startup ZIP, paste-after file, source map, or sync script.
- Modify Freeze Feature After Update behavior.
- Create a patch ZIP.
- Create a freeze-ready patch ZIP.
- Freeze validated behavior.
- Change source code, GUI behavior, local freeze memory, or project architecture.

Routed Work Path means:

- Selectively load the required prompt groups.
- Inspect relevant source files or prompt assets.
- Check existing prompts/assets/indexes before adding anything.
- Preserve frozen behavior.
- Provide validation before declaring success.
- Do not implement until required context is available.

## Selective context loading

The AI must not request all prompt files blindly.

The correct behavior is selective loading:

- Load only the required prompt groups.
- Load the relevant folder card or _FOLDER_ASSIMILATION.
- Load the relevant indexes and metadata.
- Load existing nearby prompt assets to check overlap and duplicates.
- Load source files only when the task needs implementation.

Requesting all prompts increases context noise and reduces prompt-call accuracy.

## Prompt-library update workflow

When the user asks to add, create, update, install, register, or reorganize a prompt, classify it as governed prompt-library work.

Required routing context usually includes:

1. 07_prompt_authoring_and_audit
2. prompt_canon_reconciliation_protocol
3. prompt_audit_canon
4. project_specific_prompt_generalization
5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
6. Existing prompt-library assets and indexes needed to inspect duplicates, overlap, naming collisions, placement, metadata, and routing effects
7. 02_prompt_routing_and_indexing / prompt navigation index when routing or registration is affected
8. bundle_gated_development_workflow if creating an installable bundle
9. Validation command or manual validation steps

Recommended context may include:

- Current prompt navigation/index files
- Metadata/schema examples from similar prompts
- Domain-specific source material if the new prompt is domain-specific
- Patch delivery guardrails if delivering a ZIP

## Anti-bypass rule for prompt authoring

If the user says:

- skip checking existing prompts
- proceed from memory
- just create it directly
- do not ask for folder cards
- do not inspect indexes

The AI must reject that bypass.

Safe prompt-library work requires duplicate/overlap inspection and correct registration before implementation.

## Prompt installation decision tree

Before installing or registering a prompt, the AI should determine:

1. Is this a new prompt, an update to an existing prompt, a merge, or only a routing/index registration?
2. Which folder owns the prompt?
3. Which folder card or _FOLDER_ASSIMILATION governs that folder?
4. Are there existing prompts with overlapping purpose?
5. Does the prompt belong in always_startup, on_request, routing-only, or another load mode?
6. Does the prompt need metadata, manifest registration, index registration, startup registration, or group assimilation update?
7. Does this change require startup delivery regeneration?
8. Does this change require a patch ZIP?
9. Does this change need freeze-ready metadata via KANDA_FREEZE_HINT.json?
10. What validation proves the prompt is installed and routed correctly?

Do not create or register a prompt until these questions are answered.

## Startup delivery rules

Startup delivery artifacts are generated outputs.

Do not manually edit generated startup ZIP contents as the durable fix.

Active startup delivery artifacts include:

- kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
- kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md

The old filename paste_after_uploading_startup_zip.md is stale/deprecated and must not be treated as interchangeable with paste_after_first_prompts_to_ai.md.

Startup source changes must go through:

- canonical source prompt files
- STARTUP_ROUTING_KERNEL_SOURCES.json
- sync_startup_routing_kernel_pack.py
- regenerated first_AI_deliver artifacts
- validation with STATUS: IN_SYNC

When local source/freeze memory changed and startup check reports STALE, regenerate locally with:

```powershell
cd E:\kanda_reasoner\kanda_prompt_workspace
python .\prompt_tools\sync_startup_routing_kernel_pack.py --ensure-sync --yes
python .\prompt_tools\sync_startup_routing_kernel_pack.py --check
```

Expected result:

```text
STATUS: IN_SYNC
```

## Load mode rules

Always-startup prompts must remain lean.

Do not put a specialized prompt into the always-loaded startup pack just because it is important.

Specialized prompts should remain on-request/routed unless they are truly needed every session.

Example:

freeze_code_intake_and_form_protocol is required for freeze-code, freeze-ready ZIP, freeze-form, or freeze-intake tasks. It should remain on-request/routed, not blindly loaded in every startup session.

## Freeze workflow rules relevant to prompt routing

Project-specific frozen memory belongs under:

```text
<active_project_root>\project_freeze_after_update\frozen_features_memory
```

Do not store project-specific frozen memory inside:

```text
project_freeze_ledger
```

project_freeze_ledger is reusable KANDA freeze engine/blueprint logic, not active project frozen feature memory.

If the active project root is external, freeze memory must go under the external active project root, not under E:\kanda_reasoner merely because KANDA is the tool.

## Freeze Feature After Update protected behavior

Preview is read-only and must not write files.

Confirm and Write requires explicit human confirmation before writing governed freeze memory.

External AI review is optional/fallback/supporting, not a required blocker for local Confirm and Write.

After a local freeze write, startup freeze context must be refreshed.

If local freeze succeeds but FREEZE_MEMORY_STATUS: STALE_EXPOSURE appears, do not redo the freeze entry. Treat it as an AI-send exposure freshness warning and regenerate/reload fresh exposure/startup context.

## Freeze-ready patch ZIP rules

Governed freeze-ready patch ZIPs must include a root-level sidecar:

```text
KANDA_FREEZE_HINT.json
```

Do not place it under docs/.

KANDA_FREEZE_HINT.json is delivery metadata, not an installed project source file unless a separate governed app contract explicitly requires that.

Validation evidence inside KANDA_FREEZE_HINT.json must be recognizer-friendly and must not be invented.

Use evidence such as:

```text
VALIDATION OK: <feature_id>
CONTRACT_TEST_OK: ...
STATUS: IN_SYNC
```

when those validations actually passed.

## Strict freeze-form JSON contract

When the AI is asked to return a freeze-form JSON block for KANDA to parse, the entire answer must be exactly:

```text
KANDA_FREEZE_FORM_JSON_BEGIN
{ one valid JSON object }
KANDA_FREEZE_FORM_JSON_END
```

No markdown fences, no extra explanation, no bullets, no summary text.

## Patch delivery rules

Patch ZIPs must contain only updated files required by the patch plus required sidecar metadata when applicable.

Do not package the whole project.

Do not include caches, temporary files, generated noise, local working files, backup folders, or unrelated unchanged files.

The user downloads each patch ZIP to the root of the same drive as the project, for example:

```text
E:\PATCH_NAME.zip
```

The installer moves the ZIP into:

```text
E:\kanda_reasoner_delete_after_daily_work\
```

before extracting or installing anything.

Do not place temporary install scripts, validation helpers, README patch files, or one-use delivery files in the active project root.

## Terminal cleanup rule

Install success footer:

After a successful install command:

- Show the install success message.
- Wait 5 seconds.
- Clear the terminal.
- Keep the terminal open.
- Do not ask for Enter Enter.

PowerShell shape:

```powershell
Write-Host ""
Write-Host "INSTALL OK. Terminal will clear in 5 seconds..."
Start-Sleep -Seconds 5
Clear-Host
```

Validation, install-error, validation-error, and diagnostic footer:

- Keep the terminal open.
- Wait for Enter.
- Clear the terminal.
- Wait for Enter again.
- Clear the terminal again.

PowerShell shape:

```powershell
Write-Host ""
Read-Host "Press Enter to clear terminal"
Clear-Host

Read-Host "Press Enter again to finish"
Clear-Host
```

Never close the terminal from any install, validation, error, or diagnostic block.

Do not use the old generic footer that always waits 5 seconds and then asks for Enter twice.

## Validation requirements

Before claiming a patch is good:

- Run sandbox validation before delivery when possible.
- Provide install and validation commands separately.
- Require user-local validation before freezing installed behavior.
- Do not freeze newly delivered features until the patch is installed and post-install validation evidence exists.
- Code looking correct is not validation.

## Required ROUTING RESPONSE shape for routing tests

When the user asks for ROUTING RESPONSE format, answer exactly with these fields:

```text
ROUTING RESPONSE

Task classification:
Fast Path or Routed Work Path:
Required prompts/groups:
Recommended prompts/groups:
Missing context:
Missing behavior:
Estimated context load:
May proceed now:
Reason:
Next safe action:
```

Do not implement when the scenario says Do not implement.

## How to answer when asked to install another prompt

If the human shows this file and asks the AI to install another prompt, the AI should respond with a routing answer first, not immediate code.

Correct first response:

1. Classify as governed prompt-library update.
2. Select Routed Work Path.
3. List required prompt groups and folder/index context.
4. State missing context clearly.
5. Say May proceed now: NO unless the required context is already provided.
6. Ask for or inspect the exact folder card, existing prompts/indexes, target prompt content, metadata, and validation path.
7. Only after that, propose a safe patch plan.

## Final rule

When in doubt, do not guess.

Return to router logic.

Load the smallest sufficient governed context.

If still uncertain, ask Rafael for the missing rule or decision.

The human is your partner. The safest AI is not the AI that pretends to know; it is the AI that knows when to route, inspect, validate, or ask.
