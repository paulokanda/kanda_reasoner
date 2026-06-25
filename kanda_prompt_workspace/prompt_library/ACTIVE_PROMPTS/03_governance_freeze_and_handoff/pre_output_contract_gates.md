---
prompt_id: pre_output_contract_gates
title: Pre-Output Contract Gates
version: 1.1
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
- Patch install delivery error-register checks.
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


### INSTALL_ERROR fail-safe wrapper

Every install PowerShell block must wrap the install body in `try { ... } catch { ... }` or use a text-equivalent checked wrapper so that install errors cannot bypass terminal cleanup.

If installation succeeds, the script must show `INSTALL OK. Terminal will clear in 5 seconds...`, wait 5 seconds, run `Clear-Host`, and keep the terminal open with no `Read-Host`.

If installation fails at any point before success, the `catch` block must show `INSTALL ERROR`, show the error message, wait for Enter, run `Clear-Host`, wait for Enter again, run `Clear-Host` again, keep the terminal open, and must not call `exit`, `Stop-Process`, `Restart-Computer`, or any command that closes the terminal.

The installer must not rely on an uncaught `throw` for install failures because an uncaught error can skip the diagnostic cleanup footer.

<!-- PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_START -->
## Canonical freeze-ready patch delivery sequence

For every freezeable KANDA/PyArchitect patch, the delivery order is mandatory and must not be inverted, skipped, or diluted:

1. **Send the patch ZIP only after contract validation.** The ZIP must contain only the changed project files plus a root-level `KANDA_FREEZE_HINT.json` sidecar. If the ZIP contract cannot be verified, block delivery with `CONTRACT NOT MET - PATCH DELIVERY BLOCKED`.
2. **Send the install PowerShell after the ZIP.** The install block must stage the ZIP from `<drive>:\PATCH_NAME.zip` into `<drive>:\<project_name>_delete_after_daily_work\`, delete the root-drive ZIP copy after successful staging, extract only from the staged ZIP, and install only changed project files.
3. **Do not install the freeze sidecar into the project root.** `KANDA_FREEZE_HINT.json` is freeze-intake delivery metadata. It may be scanned or consumed from the staged ZIP / daily-work intake location, but it must not be copied as a normal project source file.
4. **Send the validation PowerShell after the install block.** Validation must be a separate local action after install and must emit recognizable evidence, including `VALIDATION OK: <feature_id>`. When startup delivery, generated evidence, or sync state is validated, it must also emit `STATUS: IN_SYNC`.
5. **Freeze only after local validation passes.** The Freeze Feature After Update flow must use the feature-specific `KANDA_FREEZE_HINT.json` / freeze-intake data plus current validation evidence, then require Preview and explicit human Confirm and Write.
6. **Refresh AI exposure after freeze.** A successful local freeze write must refresh AI-send exposure and startup freeze context so the next startup pack knows the frozen behavior.

Short form:

```text
patch ZIP with root KANDA_FREEZE_HINT.json
-> install changed files only, keeping KANDA_FREEZE_HINT.json out of project root
-> run local validation with VALIDATION OK and STATUS: IN_SYNC when applicable
-> freeze through Preview + Confirm and Write
-> refresh AI-send and startup freeze context
```

Install success is not validation. A freeze hint is not validation evidence. Old feature validation must not be reused for the current feature.
<!-- PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_END -->

## PATCH_DELIVERY_CONTRACT

Apply before delivering any patch ZIP or install instructions.

Before writing the installer or validation wrapper, also apply `patch_install_delivery_error_register`. The register is startup-loaded and append-only so known install-wrapper regressions are blocked before output.

Patch ZIP delivery is a governed release event, not generic code output. The AI must treat this as `PATCH_DELIVERY_RELEASE` and must fail closed if the release contract cannot be verified.

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
13. The ZIP must pass `python scripts/validate_patch_zip.py <zip_path>` before the download link is emitted. If this script fails or cannot be run, block the ZIP link and report the failure.
14. The PowerShell install block must be generated from the canonical root-drive staging template or be text-equivalent to it. It must not use Downloads/Desktop search fallbacks.
15. The PowerShell validation block must not emit long freeze evidence as one giant quoted `Write-Host` line; use a here-string or short statements.
15. The same canonical freeze payload must feed both root-level `KANDA_FREEZE_HINT.json` and any user-facing freeze-form JSON so `validated_files`, `validation_evidence_summary`, and feature identity cannot diverge.

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

Mandatory release checklist before any ZIP link:

```text
PATCH DELIVERY PRE-FLIGHT VERIFICATION:
[PASS] ZIP basename is compact and Windows-safe.
[PASS] Root-level KANDA_FREEZE_HINT.json is present unless explicitly non-freezeable.
[PASS] KANDA_FREEZE_HINT.json has all mandatory fields with no placeholders.
[PASS] validated_files and validation_evidence_summary are non-empty.
[PASS] KANDA_FREEZE_HINT.json is not duplicated inside the install payload folder.
[PASS] ZIP contract validator result: PASS.
[PASS] Installer stages from the project drive root into <drive>:\<project>_delete_after_daily_work.
[PASS] Installer deletes the root-drive ZIP copy after successful staging.
[PASS] Installer uses no Downloads/Desktop fallback.
[PASS] patch_install_delivery_error_register was applied before output.
[PASS] Long validation evidence uses a here-string or short statements, not one giant quoted Write-Host line.
[PASS] Install success uses 5-second Clear-Host and no Enter prompts.
[PASS] Install errors use Enter, Clear-Host, Enter, Clear-Host and keep the terminal open.
[PASS] Freeze-form JSON is emitted from the same payload source, or the response explicitly states why it is withheld until user-local validation.
```

If any line cannot truthfully be marked PASS, the AI must respond with:

```text
CONTRACT NOT MET - PATCH DELIVERY BLOCKED
```

and must not provide the ZIP link.

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
