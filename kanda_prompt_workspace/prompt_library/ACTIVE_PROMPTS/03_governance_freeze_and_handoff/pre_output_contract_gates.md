---
prompt_id: pre_output_contract_gates
title: Pre-Output Contract Gates
version: 1.3
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

Terminal cleanup behavior is owned by `terminal_cleanup_contract.md`.

Before emitting any PowerShell or terminal block, apply `terminal_cleanup_contract.md` to classify the block and audit the exact footer text.

This pre-output gate must not duplicate terminal footer implementation details. It must fail closed if the terminal block conflicts with the canonical contract.

Additional pre-output constraints still apply:

- Install blocks must include a fail-safe `try` / `catch` or equivalent checked error path.
- Freeze-prep, freeze-hint merge, validation-evidence merge, repair, or other KANDA operational PowerShell blocks must not use inline `python -c`; use a temporary UTF-8 `.py` helper under `_delete_after_daily_work`.
- Terminal blocks must never close the visible terminal session.




<!-- RECEIVER_DELIVERY_OUTPUT_GATE_V1_START -->
## RECEIVER_DELIVERY_OUTPUT_GATE - v1

Apply this gate before emitting any artifact that mentions or contains `KANDA_FREEZE_HINT.json`, `KANDA_FREEZE_FORM_JSON_BEGIN`, `KANDA_ERROR_LESSON_JSON_BEGIN`, governance intake bundle, manual receiver bundle, Error Memory intake ZIP, or freeze form ZIP.

Classify the receiver before writing the response:

```text
SOURCE_PATCH
FREEZE_HINT_INTAKE
MANUAL_FREEZE_FORM_RECEIVER
ERROR_MEMORY_AI_ASSISTED_INTAKE
STORAGE_ONLY_MANUAL_HELPER
```

### Source patch receiver

A source patch installs changed project files only. A root-level `KANDA_FREEZE_HINT.json` is a sidecar, not a source file, and must not be installed into the active project root.

### Freeze hint intake receiver

A freeze-hint delivery is valid only when the install or validation flow stages or updates feature-specific freeze intake under `<project_drive>\<project_name>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake`. After local validation, `validation_evidence_summary` must contain recognizable local evidence such as `VALIDATION OK: <feature_id>`, `STATUS: IN_SYNC`, and `ZIP CONTRACT: PASS`. Sandbox-only text or pending-validation wording is not acceptable for Confirm and Write.

### Manual freeze form receiver

Use this only when the latest freeze hint is stale, consumed, or unavailable. The receiver-ready text must be exactly:

```text
KANDA_FREEZE_FORM_JSON_BEGIN
{ one valid freeze form JSON object }
KANDA_FREEZE_FORM_JSON_END
```

The JSON object must include `feature_title`, `primary_box`, `box_type`, `validated_files`, `generated_files`, `protected_paths`, `do_not_regress_rules`, `validation_evidence_summary`, `known_warnings`, `planned_next_step`, and `notes`.

If the text is packaged in a ZIP but not imported automatically by the app, label it `STORAGE_ONLY_MANUAL_HELPER` and state that manual paste into the Freeze Feature receiver is required. Do not call it installed freeze intake.

### Error Memory AI-assisted intake receiver

For text output, the receiver-ready lesson must be exactly:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ active-ready JSON object }
KANDA_ERROR_LESSON_JSON_END
```

Do not wrap the markers in markdown code fences. Do not output plain JSON only. Do not use writing blocks. Active-ready lessons require the current Error Memory blueprint fields including `redaction`, where `redaction.applied` and `redaction.export_safe` are true and `redaction.rules` is a non-empty list.

For ZIP delivery, the install block must stage the active-ready lesson into `<project_drive>\<project_name>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake`. A ZIP that only stores the lesson in daily-work is storage/manual helper only.

### Fail-closed rule

If the response cannot prove the actual receiver path or manual receiver action, block the artifact and output:

```text
CONTRACT NOT MET - RECEIVER DELIVERY BLOCKED
```
<!-- RECEIVER_DELIVERY_OUTPUT_GATE_V1_END -->

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


<!-- NO_ISOLATED_ZIP_RESPONSE_CONTRACT_V1_START -->
## NO_ISOLATED_ZIP_RESPONSE_CONTRACT

Apply before any response that contains a patch ZIP link, including sandbox links, local file links, or download links ending in `.zip`.

A patch ZIP link is forbidden unless the response includes this visible gate before the link:

```text
PATCH DELIVERY GATE
ZIP purpose:
ZIP placement path:
What this ZIP is:
What this ZIP is not:
Install code present: YES
Validation code present: YES
Expected validation markers:
Changed files:
Allowed write paths:
Forbidden write paths:
Freeze/freeze-intake:
Error Memory payload:
Post-validation steps:
What not to do:
Beginner-safe: YES
GATE STATUS: PASS
```

The response must also include:

1. A complete install PowerShell block.
2. A complete validation PowerShell block.
3. Expected markers, including `VALIDATION OK: <feature_id>` and `STATUS: IN_SYNC` when startup sync was touched.
4. Freeze/freeze-intake instructions for freezeable patches.
5. Error Memory intake or staging instructions when the patch corrects a user-detected AI mistake.

If any required item is missing, uncertain, or contradicted by the ZIP contract, output exactly:

```text
CONTRACT NOT MET - PATCH DELIVERY BLOCKED
```

and do not provide the ZIP link.
<!-- NO_ISOLATED_ZIP_RESPONSE_CONTRACT_V1_END -->

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
[PASS] Install success uses 2-second Clear-Host and no Enter prompts.
[PASS] Install errors use Enter, Enter, one final Clear-Host and keep the terminal open.
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
<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake
<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/frozen_features_memory
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

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_PARADIGM_V1_BEGIN -->

## Mandatory validation evidence merge gate

Before emitting any validation command for a freeze-capable patch ZIP, include a
post-validation merge step unless the patch is explicitly non-freezeable.

The validation command must:

1. Run the ZIP contract validator.
2. Run the feature-specific validators.
3. Store the recognizer-friendly local validation evidence in a small evidence
   text file or here-string.
4. Run `python scripts\merge_freeze_validation_evidence.py` with the active
   project root, the same feature ID as `KANDA_FREEZE_HINT.json`, the feature
   title, and the evidence file.
5. Treat a missing `FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>` line as a
   validation failure for freeze-readiness.

The merge step prevents New Local Freeze Entry from showing the old
pre-validation sidecar text after validation has passed.

Do not output a freeze-ready answer if the user-local validation passed but the
freeze form still shows only sandbox evidence or a local-validation-pending note.
The correct action is to refresh or merge validation evidence, then preview and
Confirm and Write.

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_PARADIGM_V1_END -->

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_BY_PATCH_ZIP_V2_BEGIN -->

## Patch ZIP keyed validation evidence merge - v2

When a validation block merges local validation evidence into freeze hint intake,
it must not assume `latest_freeze_hint.json` already belongs to the feature that
was just validated. A previous patch can leave a stale latest hint for another
feature.

For every freeze-capable patch validation block:

1. Capture local validation markers after the validator passes.
2. Call `scripts/merge_freeze_validation_evidence.py` with `--patch-zip` pointing
   to the staged patch ZIP and with the current `--feature-id`.
3. Require the merge helper to load the matching root-level `KANDA_FREEZE_HINT.json`
   from that patch ZIP before merging evidence if the current latest hint is for
   another feature.
4. Treat a feature-id mismatch without a matching `--patch-zip` as a validation
   failure, not as a reason to merge evidence into the wrong freeze form.
5. Freeze-ready evidence must include `VALIDATION OK: <feature_id>` and
   `FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>`.

This prevents stale freeze-intake data from causing `FREEZE BLOCKED - no
recognizable validation evidence found` after local validation already passed.

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_BY_PATCH_ZIP_V2_END -->

<!-- ERROR_MEMORY_LESSON_BLOCK_SCHEMA_GATE_V1_BEGIN -->

## Error Memory lesson block schema gate - v1

Any ZIP, patch, direct Error Lesson ZIP, or clipboard receive block that carries
`KANDA_ERROR_LESSON_JSON` must be schema-valid before delivery.

Machine gate:

```text
python scripts\validate_patch_zip.py <staged_patch_zip>
```

must inspect every packaged `KANDA_ERROR_LESSON_JSON_*.txt` file and block the
ZIP if the lesson JSON lacks `schema_version`, `project_slug`, required active
lesson fields, `redaction`, `exception`, `fingerprint`, `prevention_triggers`,
or `validation_evidence` when `status` is `active`.

Required minimum for every packaged lesson block:

```text
schema_version: "1.0"
project_slug: non-empty selected project slug
lesson_id: present
status: draft, active, deprecated, or superseded
redaction.applied: true
redaction.export_safe: true
```

Do not answer with only a corrected manual JSON block when an Error Memory
lesson was generated with missing schema fields. Correct the creation/validation
path so the next generated package is blocked before release.

<!-- ERROR_MEMORY_LESSON_BLOCK_SCHEMA_GATE_V1_END -->


<!-- PRE_OUTPUT_ERROR_MEMORY_ACTIVE_READY_OUTPUT_GATE_V21_BEGIN -->

## Error Memory active-ready output gate - v21

Apply this gate before outputting any artifact that contains or stages
`KANDA_ERROR_LESSON_JSON`.

The gate checks the exact outgoing JSON object, not a summary. If `status` is
`active`, the object must include `raw_error_text`,
`raw_error_snapshot_scrubbed`, `redaction`, `exception`, `fingerprint`,
`prevention_triggers`, `regression_check`, `validation_command_summary`,
`validation_evidence`, `install_command_summary`, and `notes`, with meaningful
values. `redaction.applied` and `redaction.export_safe` must be true and
`redaction.rules` must be a non-empty list.

If the exact outgoing active lesson would trigger the GUI message `This lesson is
not active-ready`, block the output and repair the prompt/package before showing
the ZIP link, terminal command, direct lesson ZIP, or marker-wrapped block.

<!-- PRE_OUTPUT_ERROR_MEMORY_ACTIVE_READY_OUTPUT_GATE_V21_END -->

<!-- PRE_OUTPUT_ERROR_MEMORY_JSON_FORWARD_SLASH_GATE_V22_BEGIN -->

## Error Memory JSON forward-slash pre-output gate - v22

Apply this before outputting anything that contains or stages
`KANDA_ERROR_LESSON_JSON`.

The exact outgoing active lesson must parse as JSON, include the full
active-ready schema, include `redaction.rules`, and have a slash-only
`regression_check.command`. Backslashes and control characters in that command
are release blockers.

If sandbox/tool validation is available, validate the exact JSON before showing
it, linking a ZIP, or providing install commands. If validation cannot be done,
do not emit an active lesson block.

<!-- PRE_OUTPUT_ERROR_MEMORY_JSON_FORWARD_SLASH_GATE_V22_END -->

<!-- RECEIVER_DELIVERY_OUTPUT_GATE_V2_START -->

## Receiver delivery output gate - v2

Before outputting any freeze, Error Memory, governance intake, manual receiver,
or patch ZIP artifact, the response must prove the real receiver chain:

```text
artifact -> declared receiver -> install or manual action -> validation proof
```

Do not treat a file stored under `<project>_delete_after_daily_work` as consumed
by the app. Daily-work storage is transient staging only.

Required visible block when receiver-bearing ZIPs are mentioned:

```text
RECEIVER DELIVERY CHECK
Receiver classification:
Actual receiver path or action:
Installer stages to receiver: YES / NO
Manual paste required: YES / NO
Storage-only helper: YES / NO
Receiver proof:
RECEIVER STATUS: PASS / FAIL
```

Hard blocks:

- If `ERROR_MEMORY_AI_ASSISTED_INTAKE` is claimed, the install block must copy
  the lesson into `project_error_memory\pending_ai_assisted_error_lesson_intake`.
- If `FREEZE_HINT_INTAKE` is claimed, the install or validation block must copy
  or merge the current feature's `KANDA_FREEZE_HINT.json` into
  `project_freeze_after_update\freeze_hint_intake`.
- If only marker-wrapped text is provided for manual paste, the receiver must be
  `MANUAL_FREEZE_FORM_RECEIVER` or `STORAGE_ONLY_MANUAL_HELPER`; do not call it
  installed intake.
- If Error Memory text is output, it must use `KANDA_ERROR_LESSON_JSON_BEGIN` /
  `KANDA_ERROR_LESSON_JSON_END` and must be active-ready JSON, not code-fenced
  plain JSON.
- If manual freeze form text is output, it must use `KANDA_FREEZE_FORM_JSON_BEGIN`
  / `KANDA_FREEZE_FORM_JSON_END` and must include current local validation
  evidence markers.

Install blocks that extract ZIPs must validate ZIP member names before
`Expand-Archive` and reject traversal paths.

<!-- RECEIVER_DELIVERY_OUTPUT_GATE_V2_END -->

## Receiver delivery package marker gate - v3

When a patch ZIP includes any Error Memory lesson archive member whose basename starts with `KANDA_ERROR_LESSON_JSON_`, the archive member content must be receiver-block text, not raw JSON only.

Required package-time shape:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ one active-ready JSON object }
KANDA_ERROR_LESSON_JSON_END
```

This applies even when the archive member suffix is `.json`. The suffix is not permission to omit the markers. `scripts/validate_patch_zip.py` is the source-of-truth ZIP contract check and must pass before delivery.

