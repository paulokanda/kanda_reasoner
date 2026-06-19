---
prompt_id: pre_output_contract_gates
title: Pre-Output Contract Gates
version: 1.0
status: active_candidate
load_type: on_request
owner_group: 03_governance_freeze_and_handoff
created_by_patch: pre_output_contract_gates_v1
---

# Pre-Output Contract Gates

## Purpose

Use this prompt immediately before the AI emits any high-risk operational artifact.

The router decides what context is required. This prompt decides whether the final artifact is allowed to be emitted in its current form.

This prompt exists because KANDA failures can happen after correct routing. The AI can classify a task correctly, then switch into code, JSON, or patch-delivery generation and fall back to generic habits. These gates force the AI to apply the KANDA canon at output time.

## Required triggers

Request or apply this prompt before producing any of these artifacts:

- PowerShell or terminal install block.
- PowerShell or terminal validation block.
- Diagnostic terminal block.
- Error-handling terminal block.
- Patch ZIP delivery instructions.
- Freeze-ready patch ZIP instructions.
- `KANDA_FREEZE_FORM_JSON_BEGIN` / `KANDA_FREEZE_FORM_JSON_END` output.
- `validation_evidence_summary` intended for a freeze entry.
- `KANDA_FREEZE_HINT.json` metadata.
- Any path decision for `project_freeze_after_update/freeze_hint_intake` or `project_freeze_after_update/frozen_features_memory`.

Do not use this prompt for simple explanation-only Fast Path tasks unless the answer includes one of the artifact types above.

## Output-time rule

Before emitting a triggered artifact, the AI must classify the artifact type and apply the matching contract below.

This classification may be silent during normal user work. For routing tests, it may be shown when the test asks for evidence.

Do not rely on memory. Do not use generic code-generation habits. Do not guess if the contract is unclear.

## TERMINAL_OUTPUT_CONTRACT

Apply before any PowerShell or terminal block.

First classify the terminal artifact as one of:

- `INSTALL_SUCCESS`
- `INSTALL_ERROR`
- `VALIDATION`
- `DIAGNOSTIC`
- `OTHER_TERMINAL`

### INSTALL_SUCCESS contract

Use only after an install command completes successfully.

Required footer behavior:

- Show a success message.
- Wait 5 seconds.
- Clear the terminal.
- Keep the terminal open.
- Do not ask for Enter.
- Do not close the terminal.

PowerShell shape:

```powershell
Write-Host ""
Write-Host "INSTALL OK. Terminal will clear in 5 seconds..."
Start-Sleep -Seconds 5
Clear-Host
```

### VALIDATION, DIAGNOSTIC, INSTALL_ERROR, VALIDATION_ERROR, and OTHER_TERMINAL contract

Use this cleanup behavior for validation blocks, diagnostic blocks, install failures, validation failures, and any terminal block that is not a successful install.

Required footer behavior:

- Keep the terminal open.
- Wait for Enter.
- Clear the terminal.
- Wait for Enter again.
- Clear the terminal again.
- Do not close the terminal.

PowerShell shape:

```powershell
Write-Host ""
Read-Host "Press Enter to clear terminal"
Clear-Host

Read-Host "Press Enter again to finish"
Clear-Host
```

### Terminal forbidden patterns

Never mix the install-success 5-second footer with the Enter Enter cleanup footer.
Never use the old generic footer that waits 5 seconds and then asks for Enter twice.
Never close the terminal from install, validation, diagnostic, or error blocks.
Never ask for Enter after a successful install unless the user explicitly asked to keep the log visible.
Never auto-clear validation or diagnostic output after 5 seconds.

## PATCH_DELIVERY_CONTRACT

Apply before delivering any patch ZIP or install instructions.

Required behavior:

1. The patch ZIP contains only updated installable files and required delivery metadata.
2. The human downloads the ZIP to the root of the same drive as the active project, for example `<drive>:\PATCH_NAME.zip`.
3. The installer creates `<drive>:\<project_in_use_name>_delete_after_daily_work\` if missing.
4. The installer moves the ZIP from the drive root into the delete-after-daily-work staging folder before extraction.
5. The installer installs only from the staged ZIP path.
6. The installer removes any old extraction folder before extracting.
7. The installer freshly extracts on every run.
8. The installer must not assume yesterday's extracted folder exists.
9. Install and validation commands must be separate terminal blocks.
10. Temporary install helpers, validation helpers, README patch files, extracted files, and backups must not be placed in the active project root.
11. Freeze-ready patch ZIPs must include root-level `KANDA_FREEZE_HINT.json` unless intentionally non-freezeable and the reason is stated.
12. `KANDA_FREEZE_HINT.json` is delivery metadata and must not be installed into the project root as a source file unless a separate governed app contract explicitly requires that.

Required failure when ZIP is missing from root and staging:

```text
zip is not in root of drive:\ where project is
```

Patch delivery forbidden patterns:

- Do not package the whole project.
- Do not include caches, `__pycache__`, `.git`, backup folders, temporary validation folders, or unrelated unchanged files.
- Do not assume an extracted folder already exists.
- Do not ask the user to manually move the ZIP into staging when the installer can do it.
- Do not omit `KANDA_FREEZE_HINT.json` from a freeze-ready patch ZIP.

## FREEZE_FORM_JSON_CONTRACT

Apply before returning a freeze-form JSON block to the KANDA app.

The entire answer must be exactly:

```text
KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_title":"...","primary_box":"...","box_type":"...","validated_files":"...","generated_files":"...","protected_paths":"...","do_not_regress_rules":"...","validation_evidence_summary":"...","known_warnings":"...","planned_next_step":"...","notes":"..."}
KANDA_FREEZE_FORM_JSON_END
```

Required fields:

- `feature_title`
- `primary_box`
- `box_type`
- `validated_files`
- `generated_files`
- `protected_paths`
- `do_not_regress_rules`
- `validation_evidence_summary`
- `known_warnings`
- `planned_next_step`
- `notes`

Strict output rules:

- Use valid JSON.
- Use double quotes for all JSON keys and string values.
- Escape line breaks inside string values as `
`.
- Avoid raw Windows backslashes inside JSON strings unless they are escaped. Forward slashes are safer inside evidence strings.
- Prefer compact one-object JSON when the receiver is strict.
- Do not include markdown fences.
- Do not include comments.
- Do not include bullets.
- Do not include trailing commas.
- Do not place prose between the markers.
- Do not add text before or after the markers when strict receiver mode is requested.
- Do not invent validation evidence.

If required validation evidence is missing, do not output freeze-form JSON.

## VALIDATION_EVIDENCE_CONTRACT

Apply before producing freeze-ready metadata, freeze-form JSON, or a freeze approval answer.

If local validation passed, `validation_evidence_summary` must include the exact recognizer-friendly marker:

```text
VALIDATION OK: <feature_id>
```

If startup delivery sync was validated, include the exact marker:

```text
STATUS: IN_SYNC
```

Optional supporting markers may include:

```text
CONTRACT_TEST_OK: ...
SANDBOX_..._VALIDATION_OK
INSTALL OK: ...
```

If `VALIDATION OK: <feature_id>` is absent, the AI must not produce freeze-ready JSON. It must return:

```text
FREEZE BLOCKED - validation evidence marker missing.
```

Validation evidence forbidden patterns:

- Do not treat generic text such as "sandbox passed" as sufficient local validation evidence.
- Do not reuse validation evidence from another feature.
- Do not reuse stale validation lists from older freeze forms.
- Do not claim user-local validation before the user provides it or a local validation command produced it.
- Do not write `STATUS IN_SYNC`; the exact startup marker is `STATUS: IN_SYNC`.

## FREEZE_HINT_SIDECAR_CONTRACT

Apply before delivering a freeze-ready patch ZIP or preparing `KANDA_FREEZE_HINT.json`.

A freeze-ready patch ZIP must include root-level `KANDA_FREEZE_HINT.json` with these keys:

- `schema_version`
- `kind`
- `patch_name`
- `feature_id`
- `feature_title`
- `primary_box`
- `box_type`
- `validated_files`
- `generated_files`
- `protected_paths`
- `do_not_regress_rules`
- `validation_evidence_summary`
- `known_warnings`
- `planned_next_step`
- `notes`

Recommended keys:

- `freeze_readiness`
- `requires_user_validation`
- `source_patch_zip`

Allowed `freeze_readiness` values:

- `pre_validation_hint`
- `locally_validated`
- `frozen`

Rules:

- The sidecar describes the current patch feature, not an older heuristic feature.
- The sidecar remains delivery metadata unless a separate governed app contract says otherwise.
- Chat memory must not override sidecar identity.
- If sidecar identity and chat memory disagree, sidecar identity wins.
- If no sidecar exists for a freeze-ready patch, block delivery or explicitly mark the patch non-freezeable and explain why.

## FREEZE_HINT_INTAKE_MONOTONIC_CONTRACT

Apply when freeze-intake state is saved, rescanned, or used for New Local Freeze Entry.

If a saved freeze hint already contains recognizer-friendly local validation evidence such as `VALIDATION OK: <feature_id>`, a same-feature or same-source staged ZIP rescan must not downgrade that evidence to a pending-local-validation note.

Validated local evidence is stronger than pre-validation sidecar evidence.

Do not overwrite stronger saved evidence with weaker sidecar evidence.

## MULTI_PROJECT_ROOT_CONTRACT

Apply before any path decision involving freeze-intake or frozen memory.

The selected active project root owns project-specific state.

State paths must be relative to the selected active project root:

```text
<active_project_root>/project_freeze_after_update/freeze_hint_intake
<active_project_root>/project_freeze_after_update/frozen_features_memory
```

If KANDA Reasoner itself is the active project, these paths are inside KANDA Reasoner.

If KANDA Reasoner is analyzing another project, these paths are inside that other selected project.

Forbidden:

- Do not store active project freeze-intake state inside `project_freeze_ledger`.
- Do not store active project frozen memory inside `project_freeze_ledger`.
- Do not hardcode `E:\kanda_reasoner` as the active project root for all projects.
- Do not write another project's freeze state under KANDA Reasoner merely because KANDA is the tool.

## Fast Path protection

Do not over-route simple tasks.

If the user asks only for a simple explanation, brainstorming, or non-binding discussion and no high-risk artifact will be emitted, Fast Path remains allowed. Do not load this prompt just because the topic is technical.

Use this prompt only when output-time contracts matter.

## Final rule

A prompt rule that controls a machine-consumed artifact must be treated as a contract, not as advice.

If the artifact cannot satisfy the relevant contract, block the artifact and state the missing contract requirement.
