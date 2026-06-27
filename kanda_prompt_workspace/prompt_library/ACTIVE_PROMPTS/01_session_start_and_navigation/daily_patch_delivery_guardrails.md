# Daily Patch Delivery Guardrails

Version: 2.2
Status: startup guardrail
Prompt ID: daily_patch_delivery_guardrails
Load mode: always_startup
Scope: daily startup, patch delivery safety, root-to-staging ZIP movement, sandbox pre-delivery validation, root cleanliness, terminal hygiene
Do not use as: full patch implementation protocol, full bundle workflow, or freeze ledger

## Purpose

This file is loaded at every startup so the AI remembers the safe delivery rules before creating any patch ZIP, install command, validation command, or delivery bundle.

The full patch workflow still belongs to the Patch Delivery and Validation prompt group. This file is a short daily guardrail that prevents repeated delivery mistakes.

## Daily guardrail

When creating or delivering any install ZIP, patch bundle, installer, validator, or delivery README:

1. Do not place temporary install scripts, validation helpers, README files, extracted patch files, or one-use delivery files directly in the active project root.
2. The user downloads each install ZIP to the root of the same drive as the project, for example:

```text
<drive>:\PATCH_NAME.zip
```

The installer must then move the ZIP into:

```text
<drive>:\<project_in_use_name>_delete_after_daily_work\
```

before extracting or installing anything.

3. The ZIP must contain only files that are intended to be installed or updated.
4. Install commands and validation commands must be sent as separate copy-paste terminal blocks.
5. Terminal commands must target Windows 11 and the PyCharm terminal.
6. Install and validation blocks must use the KANDA terminal cleanup behavior unless the user explicitly asks to keep the log visible. Successful install commands use the install-success cleanup footer. Validation commands, validation failures, install errors, and diagnostic/error cases use the diagnostic cleanup footer.
7. Successful install cleanup means: show the install success message, wait 5 seconds, clear the terminal, keep the terminal open, and do not ask for Enter Enter.
8. Validation, install-error, validation-error, and diagnostic cleanup means: keep the terminal open, wait for Enter, clear the terminal, wait for Enter again, and clear the terminal again.
9. Install failure and validation failure must show the log/error before cleanup so the user can copy or send the output if needed.
10. Do not close the terminal from any install, validation, error, or diagnostic block. Do not replace this behavior with the old generic footer that always waits 5 seconds and then asks for Enter twice.
11. If the AI forgets the terminal cleanup rule, it must not guess. It must return to this guardrail and the router canon first, then ask the human if still uncertain.
12. Install blocks must contain a fail-safe error cleanup path. A successful install uses 5 seconds then `Clear-Host`; any install error must show the error, wait for Enter, `Clear-Host`, wait for Enter again, and `Clear-Host` again. The terminal must never be closed.
13. Remind the user to use Freeze Feature After Update only at meaningful regression-risk checkpoints, not after every small update.



## Pre-output contract gate hook

Before the AI emits any PowerShell block, terminal command, patch ZIP delivery instruction, validation command, freeze-form JSON, validation evidence summary intended for freezing, or `KANDA_FREEZE_HINT.json`, it must apply the output-time contract gate.

For detailed rules, request or apply `pre_output_contract_gates` from `03_governance_freeze_and_handoff`.

Minimum startup hook:

1. Terminal output must be classified as install success, validation, diagnostic, install error, validation error, or other terminal before writing the footer.
2. Install success uses the 5-second Clear-Host footer and no Enter prompts.
3. Validation, diagnostic, install-error, validation-error, and other non-install-success terminal blocks use Enter, Clear-Host, Enter, Clear-Host.
4. Patch ZIP delivery must detect `DRIVE_ROOT` from `$PROJECT_ROOT`, look first at `<drive>:\PATCH_NAME.zip`, stage the ZIP into `<project>_delete_after_daily_work`, delete the root-drive ZIP copy after successful staging, extract only from staging, and must freshly extract.
5. Freeze-form JSON must use exact markers and valid JSON only.
6. Freeze-ready validation evidence must include `VALIDATION OK: <feature_id>` after local validation passes.
7. Freeze-ready patch ZIPs must include root-level `KANDA_FREEZE_HINT.json` unless intentionally non-freezeable.
8. Any patch ZIP link must be blocked unless the ZIP passes `python scripts/validate_patch_zip.py <zip_path>` in the sandbox or local release pipeline.
9. The root sidecar and the freeze-form JSON must be rendered from the same freeze payload source. Do not hand-type them separately.
10. Freeze-intake and frozen memory paths must use the selected active project root.

This hook is output-time compliance. It does not replace the router and must not over-route simple Fast Path explanation-only tasks.


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

## Startup-loaded install error register hook

The startup pack must also load `patch_install_delivery_error_register`.

Before emitting a patch ZIP link, install block, validation block, or freeze-ready patch metadata, the AI must apply both:

1. `daily_patch_delivery_guardrails`
2. `patch_install_delivery_error_register`

This exists because PIR-001 showed that correct feature implementation can still fail at the final delivery wrapper.

Hard rule from PIR-001:

- User saves the patch ZIP at `<drive>:\PATCH_NAME.zip`.
- Installer stages it into `<drive>:\<project_name>_delete_after_daily_work\`.
- Installer deletes the root-drive ZIP copy after successful staging.
- Installer extracts only from the staged ZIP.
- Installer must not use a Downloads/Desktop-first search fallback.
- Installer must not require the user to manually place the ZIP directly in `_delete_after_daily_work`.

If a future install delivery error occurs, pause feature implementation and append a new PIR entry to `patch_install_delivery_error_register.md` before continuing.

## Required KANDA terminal cleanup behavior

Terminal cleanup behavior must distinguish successful install commands from validation, error, and diagnostic commands.

Use the successful install footer only after an install command completes successfully.

Successful install behavior:

* Show the install success message.
* Wait 5 seconds.
* Clear the terminal.
* Keep the terminal open.
* Do not ask for Enter Enter.

Successful install footer:

```powershell
Write-Host ""
Write-Host "INSTALL OK. Terminal will clear in 5 seconds..."
Start-Sleep -Seconds 5
Clear-Host
```

Use the diagnostic cleanup footer after validation commands, validation failures, install errors, or any other diagnostic/error case.

Validation, install-error, validation-error, and diagnostic behavior:

* Keep the terminal open.
* Wait for Enter.
* Clear the terminal.
* Wait for Enter again.
* Clear the terminal again.

Validation, install-error, validation-error, and diagnostic footer:

```powershell
Write-Host ""
Read-Host "Press Enter to clear terminal"
Clear-Host

Read-Host "Press Enter again to finish"
Clear-Host
```

Do not close the terminal from any install, validation, error, or diagnostic block.
Do not substitute the old generic footer that always waits 5 seconds and then asks for Enter twice.




<!-- TERMINAL_FOOTER_SELF_AUDIT_V15_START -->

## Terminal footer self-audit - v15

Before emitting any KANDA/PyArchitect PowerShell or terminal block, the AI must
perform a footer self-audit on the exact command text it is about to show. This
is an output-time gate, not a reminder.

First classify the command as one of:

```text
INSTALL
VALIDATION
DIAGNOSTIC
INSTALL_ERROR_PATH
VALIDATION_ERROR_PATH
OTHER_TERMINAL
```

Hard fail-closed rules:

1. Never deliver a KANDA install block without the 5-second success clear footer.
2. A successful install block must end its success path with the exact behavior:
   show `INSTALL OK. Terminal will clear in 5 seconds...`, run
   `Start-Sleep -Seconds 5`, then run `Clear-Host`, with no success-path
   `Read-Host` prompt.
3. Every install block must also include an error path that shows the install
   error, waits for Enter, runs `Clear-Host`, waits for Enter again, and runs
   `Clear-Host` again.
4. Every validation command, validation-error command, diagnostic command,
   staging check, repair check, freeze/evidence-merge command, and all other
   non-install-success terminal code must use the Enter, `Clear-Host`, Enter,
   `Clear-Host` footer.
5. If the command cannot be confidently classified as successful install output,
   classify it as `OTHER_TERMINAL` and use Enter, `Clear-Host`, Enter,
   `Clear-Host`.
6. If the generated block is missing the required footer, mixes the install
   success footer with Enter Enter cleanup, or auto-clears validation output
   after 5 seconds, the answer must be blocked and repaired before the command
   is shown.

Required exact install-success footer:

```powershell
if (-not $InstallFailed) {
    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 5 seconds..."
    Start-Sleep -Seconds 5
    Clear-Host
}
```

Required exact non-install-success footer:

```powershell
Write-Host ""
Read-Host "Press Enter to clear terminal"
Clear-Host
Read-Host "Press Enter again to finish"
Clear-Host
```

This rule applies to install/validation blocks shown in ChatGPT answers even if
the patch code itself is correct. A correct feature patch with a wrong terminal
footer is still a delivery regression.

<!-- TERMINAL_FOOTER_SELF_AUDIT_V15_END -->

## Mandatory sandbox pre-delivery validation rule

Before the AI gives the user any download link, install block, validation block, or patch ZIP as final delivery, it must test the deliverable in its own sandbox first.

Required sandbox checks before delivery:

1. Build the patch ZIP in the sandbox.
2. Re-open or extract the ZIP in the sandbox and verify it contains only the intended updated/installable files.
3. Verify no installer script, validation helper, README, temporary file, `__pycache__`, `.git`, backup folder, or scratch artifact is accidentally included.
4. Run `python -m py_compile` on every changed Python file and every Python validation/helper file generated for the user, when Python files exist.
5. Run focused sandbox tests or text checks that can be executed safely without the user's machine.
6. If the patch changes prompts, startup files, or generated delivery artifacts, run exact-text checks for the new guardrail phrases and run the relevant generator/checker in sandbox when available.
7. Inspect the install block itself before delivery and confirm it implements the root-to-staging ZIP movement rule below.
8. Report sandbox validation honestly as sandbox validation only. Never claim user-local validation until the user provides local output.

If the AI cannot run a sandbox check, it must say which check could not be run and why, then reduce the claim accordingly.


## PATCH_DELIVERY_RELEASE fail-closed contract

Patch ZIP delivery is an output-time release event. Before the AI provides any patch ZIP download link, install block, validation block, or freeze metadata, it must run the governed release gate:

1. Build the ZIP in the sandbox.
2. Confirm `KANDA_FREEZE_HINT.json` is at ZIP root, not inside the payload folder.
3. Confirm every mandatory freeze-hint field is present, non-empty, and not placeholder text.
4. Run or simulate the checked-in validator:

```text
python scripts/validate_patch_zip.py <zip_path>
```

5. Confirm the install block follows the root-drive staging template and contains no Downloads/Desktop fallback.
6. If any check fails, do not emit the ZIP link. Return `CONTRACT NOT MET - PATCH DELIVERY BLOCKED` with the failed check.

This rule exists because prior failures occurred after correct routing, during final ZIP/link/PowerShell output. Treat it as a hard gate, not a reminder.

## Installer ZIP staging rule

When the AI creates terminal install code for any KANDA/PyArchitect patch ZIP, the install code must implement the strict root-drive-to-staging flow before installation. This replaces and forbids the old generic installer search template.

Required installer behavior, in this exact priority order:

1. Detect the active project root from the current PyCharm terminal location or from the explicit `$PROJECT_ROOT`.
2. Detect `DRIVE_ROOT` dynamically from `$PROJECT_ROOT`. Do not hardcode `E:\`, `C:\`, or any other fixed drive.
3. Look first for the downloaded patch ZIP at the project drive root:

```text
<drive>:\PATCH_NAME.zip
```

4. Create this staging folder if it does not exist:

```text
<drive>:\<project_in_use_name>_delete_after_daily_work\
```

5. If the expected ZIP exists at the drive root, move or copy-stage it into the staging folder before extraction or installation. The installer must literally implement this behavior, not merely mention it.
6. After successful staging, delete the temporary downloaded ZIP copy from the drive root so no duplicate root copy remains.
7. If the ZIP is already in the staging folder and no root copy exists, use the staged ZIP.
8. Install and extract only from the ZIP path inside the delete-after-daily-work staging folder.
9. If the expected ZIP is neither in the drive root nor already in the staging folder, stop and show exactly:

```text
zip is not in root of drive:\ where project is
```

10. Do not ask the user to manually move the ZIP into the staging folder. The installer must perform the root-drive staging operation.
11. Only after the ZIP is confirmed inside the staging folder should the install code extract and copy project files.

Forbidden installer behavior for this situation:

- Do not search `Downloads` or `Desktop` before the project drive root.
- Do not use a generic candidate search where `Downloads` or `Desktop` can beat `<drive>:\PATCH_NAME.zip`.
- Do not leave the root-drive downloaded ZIP copy behind after successful staging.
- Do not extract from the project root or from the drive root.
- Do not install from an extracted folder created in an earlier run.
- Do not rely on a vague newest-ZIP search when the patch filename is known.

Canonical installer opening pattern:

```powershell
$PROJECT_ROOT = "<PROJECT_ROOT>"
$PATCH_NAME = "PATCH_NAME"
$PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
$ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT ($PATCH_NAME + ".zip")
$WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")

if (-not (Test-Path $WORK_DIR)) {
    New-Item -ItemType Directory -Path $WORK_DIR -Force | Out-Null
}

if (Test-Path $ROOT_PATCH_ZIP) {
    Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force
    if (Test-Path $WORK_PATCH_ZIP) {
        Remove-Item -Path $ROOT_PATCH_ZIP -Force
    }
}

if (-not (Test-Path $WORK_PATCH_ZIP)) {
    throw "zip is not in root of drive:\ where project is"
}
```

The words `Downloads` and `Desktop` must not appear in KANDA patch install blocks unless the user explicitly asks for a one-off diagnostic search outside the governed installer flow.

## Validation phrase rule

Installer guidance must include the exact phrase "move the ZIP" so validation can confirm that ZIP staging is explicitly described.

## Root cleanliness rule

Do not pollute the active project root with files such as:

```text
install_*.ps1
README_*_PATCH.md
*_install.py
*_validate.py
STARTUP_DELIVERY_*_README.md
```

Temporary patch files belong in the delete-after-daily-work staging folder or another clearly temporary patch staging folder.

The active project root should receive only real project files that belong to the project.

## Box ownership rule

Patch delivery must respect the active box:

```text
prompt_library/      = canonical prompt source
prompt_tools/        = generators and source maps
first_prompt_files/    = generated human-facing startup delivery artifacts
delete_after_daily_work folder = temporary patch ZIPs and extracted patch helpers
```

Do not treat generated delivery files as canonical source.

Do not manually edit generated startup ZIP contents as the durable fix.

If a generated startup delivery artifact is wrong, update the canonical source, source map, or generator, then regenerate.

## Required behavior before creating patch ZIPs

Before delivering a patch ZIP, the AI should verify:

```text
Patch target box:
Files to install:
Files not to touch:
ZIP staging location:
Install command:
Validation command:
Root cleanliness check:
Drive-root ZIP move implemented: yes/no
Sandbox pre-delivery validation completed: yes/no
Freeze checkpoint needed: yes/no
```

If the task changes startup delivery generation, request the startup delivery maintenance prompt before implementation.

## Final rule

This daily guardrail is mandatory at startup.

If it conflicts with a loose or ad hoc delivery habit, this guardrail wins.

For complex patch delivery, request the full Patch Delivery and Validation prompt group before creating the final bundle.

## Freeze hint sidecar for patch ZIPs

Version: 1.0
Status: required delivery metadata for governed patch ZIPs
Purpose: prevent KANDA Reasoner from guessing the wrong feature when the human later opens New Local Freeze Entry.

When delivering a governed patch ZIP, include a root-level metadata sidecar named:

`KANDA_FREEZE_HINT.json`

This sidecar is delivery metadata for the app and for the human. It is not frozen memory, not a source file, and not project-specific memory. It may remain inside the staged patch ZIP under the delete-after-daily-work folder. Do not install it into the project root unless a separate governed app contract explicitly requires that.

The sidecar must describe the feature that the patch implements, not the older feature that the local heuristic might infer from nearby files.

Minimum required JSON keys:

`schema_version`
`kind`
`patch_name`
`feature_id`
`feature_title`
`primary_box`
`box_type`
`validated_files`
`generated_files`
`protected_paths`
`do_not_regress_rules`
`validation_evidence_summary`
`known_warnings`
`planned_next_step`
`notes`

Use the same text conventions as the Freeze Feature After Update form: project-relative paths, one path per line encoded with `\n` inside JSON strings, and validation evidence only when it is actually known.

If the patch is delivered before the user's local validation has run, do not invent local validation. In `validation_evidence_summary`, record only sandbox validation and clearly state that local validation evidence must be filled from the user's validation output after validation passes.

When the user later provides local validation output, the AI must correct the freeze form using that validation output and the sidecar feature identity. Do not reuse stale heuristic feature titles or validation lists from older freezes.

`KANDA_FREEZE_HINT.json` must never instruct the app to bypass Preview or Confirm and Write. It only pre-fills freeze entry fields. Human review and confirmation remain mandatory.

The sidecar must preserve these boundaries:

- project-specific frozen memory belongs under `<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory`.
- project-specific frozen memory must not be stored inside `project_freeze_ledger`.
- generated startup artifacts are not source of truth.
- external AI review remains advanced/fallback and not the normal freeze path.
- local freeze write must refresh AI startup freeze context after success.

Patch-answer requirement:

When giving a patch ZIP to the user, explicitly mention whether the ZIP includes `KANDA_FREEZE_HINT.json`. Do not count the sidecar as an installed source file. If listing payload files, separate installed payload files from delivery metadata files.

Validation requirement:

Before delivery, the AI must inspect the ZIP and confirm that `KANDA_FREEZE_HINT.json` exists, is valid JSON, includes the required keys, and names the same feature as the patch being delivered. If the patch is intentionally non-freezeable, the AI must say why no freeze hint is included.


## Install error fail-safe footer

Every install block must protect the install body with a `try { ... } catch { ... }` or text-equivalent wrapper. This prevents install failures from bypassing cleanup.

Install error behavior:

* Show `INSTALL ERROR` and the error message.
* Wait for Enter.
* Clear the terminal.
* Wait for Enter again.
* Clear the terminal again.
* Keep the terminal open.
* Do not use `exit`, `Stop-Process`, or any command that closes the terminal.

Install error footer:

```powershell
Write-Host ""
Write-Host "INSTALL ERROR. Review the error below before clearing the terminal."
Write-Host $_.Exception.Message
Write-Host ""
Read-Host "Press Enter to clear terminal"
Clear-Host

Read-Host "Press Enter again to finish"
Clear-Host
$global:LASTEXITCODE = 1
return
```

<!-- KANDA_GUARDRAIL:error_event_owner_canon_pointer:v2 -->
## Error Memory owner-canon pointer for corrected-error patch delivery

If a patch corrects a reported or detected error, do not treat code validation alone as closure. Apply `error_memory_ai_formulary_startup_canon` as the owner of the Error Memory intake track. The patch must include/stage a pending lesson through the dynamic `<drive>:\<project>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake` path, or clearly state the Error Memory track is still pending human review. Do not write directly into Lessons.

---
<!-- KANDA_ADDENDUM:daily_guardrail_error_memory_active_ready_packaging:v1 -->

## Error Memory packaged lesson active-ready gate

When a patch ZIP, installer, validator, or delivery bundle includes
`payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_*.txt`, the AI must
validate each packaged lesson before delivery.

Block delivery and repair the package when an active lesson is missing any of:

```text
schema_version
lesson_id
status
operation_phase
symptom
root_cause
correct_fix
long_term_prevention
do_not_repeat_rule
exception
fingerprint
prevention_triggers
regression_check
validation_evidence
redaction
raw_error_snapshot_scrubbed
```

`redaction.applied` and `redaction.export_safe` must both be true for active
lessons. Missing redaction metadata is a packaging error, not something the user
should fix manually after install.

<!-- PATCH_VALIDATION_EVIDENCE_MERGE_PARADIGM_V1_BEGIN -->

## Patch validation evidence merge paradigm

For every freeze-capable patch ZIP delivery, validation is not complete until the
local validation evidence is also merged into the project-local freeze hint
intake record.

Required validation command shape after all validators pass:

```text
run ZIP contract validation
run feature validators
capture the passed local validation output in a short evidence file or here-string
run scripts\merge_freeze_validation_evidence.py with --project-root, --feature-id,
--feature-title, and --evidence-file
require FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>
```

This is mandatory when the ZIP includes root-level `KANDA_FREEZE_HINT.json` and
is intended to be frozen through Freeze Feature After Update.

Do not rely on the pre-validation sidecar to populate `validation_evidence_summary`.
`KANDA_FREEZE_HINT.json` is delivered before local validation and may contain
sandbox evidence or a local-validation-pending note. The saved freeze-intake
record must be upgraded after validation passes so New Local Freeze Entry loads
recognizer-friendly evidence.

A freeze-ready validation log should include:

```text
ZIP CONTRACT: PASS
VALIDATION OK: <feature_id>
FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>
VALIDATION COMMAND COMPLETE
```

If startup sync is part of the validation, keep the exact marker:

```text
STATUS: IN_SYNC
```

If the merge helper is unavailable or fails, do not tell the user to freeze from
the stale preview. Provide the validation evidence text and instruct the user to
merge or paste it into the freeze form before Confirm and Write.

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


<!-- DAILY_ERROR_MEMORY_ACTIVE_READY_OUTPUT_GATE_V21_BEGIN -->

## Daily Error Memory active-ready output gate - v21

Before emitting any ZIP link, patch package, Direct Error Lesson ZIP,
marker-wrapped `KANDA_ERROR_LESSON_JSON`, or terminal instructions that stage an
Error Memory lesson, the AI must apply the Error Memory active-ready output gate
from `error_memory_ai_formulary_startup_canon`.

Block and repair the answer before delivery if an active lesson is missing any
of these high-risk fields:

```text
raw_error_text
raw_error_snapshot_scrubbed
redaction
exception
fingerprint
prevention_triggers
regression_check
validation_command_summary
validation_evidence
install_command_summary
notes
```

The exact regression phrase to catch is:

```text
This lesson is not active-ready. Required fields, prevention triggers, and redaction metadata must be present before saving as active.
```

Do not emit a corrected manual JSON block alone when the prompt/guardrail path is
what allowed AI to generate the malformed lesson.

<!-- DAILY_ERROR_MEMORY_ACTIVE_READY_OUTPUT_GATE_V21_END -->

<!-- DAILY_ERROR_MEMORY_JSON_FORWARD_SLASH_GATE_V22_BEGIN -->

## Daily Error Memory JSON forward-slash gate - v22

Before emitting any patch ZIP, Direct Error Lesson ZIP, pending intake file,
validation evidence, or marker-wrapped `KANDA_ERROR_LESSON_JSON`, apply the v22
Error Memory JSON forward-slash active-ready gate.

Block delivery if an active lesson has `regression_check.command` with any
backslash or control character. Use slash-only commands such as:

```text
python validation/test_name.py
```

Do not correct only the final pasted text. Correct the generation prompt/package
and validate the exact outgoing JSON before delivery.

<!-- DAILY_ERROR_MEMORY_JSON_FORWARD_SLASH_GATE_V22_END -->
