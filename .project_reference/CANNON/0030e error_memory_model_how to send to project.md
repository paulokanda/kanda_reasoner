# HANDOFF TO AI — Correctly Send an Error Memory Lesson to the AI-Assisted Error Lesson Intake Window

## 1. Purpose

This handoff explains the exact workflow for sending an Error Memory lesson from an AI-assisted conversation or Windows PowerShell into:

KANDA Reasoner
→ Error Memory tab
→ AI-assisted error lesson intake

The purpose is to let a future AI reproduce the correct workflow without rediscovering the transport path, payload format, parser contract, GUI refresh behavior, or human-review gate.

The intended workflow is:

AI analyzes real error evidence
→ AI creates one active-ready Error Memory lesson
→ PowerShell stages the marker-wrapped lesson in the canonical pending intake directory
→ running KANDA detects the new or changed intake file
→ existing KANDA parser validates it
→ existing classifier marks it as `pending_review`
→ existing trusted pending loader fills the AI-assisted error lesson intake window
→ human reviews the lesson and Error Editor
→ human clicks Memorize Error
→ only then is canonical Error Memory written

Permanent rule:

AI creates the lesson.
PowerShell stages the lesson.
KANDA validates and displays the lesson.
The human decides whether to click Memorize Error.

Never collapse these responsibilities into one uncontrolled step.

---

# 2. Canonical lesson model authority

The actual Error Memory lesson content must follow:

`0030d error_memory_model_template.md`

and the active-ready Error Memory canon referenced by that template.

The delivery instructions in this handoff do not replace or modify the lesson schema.

The actual pending intake file must contain exactly one marker-wrapped lesson:

KANDA_ERROR_LESSON_JSON_BEGIN
{
...
}
KANDA_ERROR_LESSON_JSON_END

Rules:

1. Keep the marker lines exactly.
2. Include one complete lesson only.
3. Do not put conversational prose before the begin marker.
4. Do not put conversational prose after the end marker.
5. Use `status: active` only when the lesson is active-ready and evidence-backed.
6. Do not fabricate missing facts.
7. Do not invent validation evidence.
8. Do not claim installation, validation, Error Memory write, or freeze success without real evidence.

---

# 3. Canonical phase values

The following exact values are allowed for:

* `operation_phase`
* `exception.phase`

Allowed values:

* `patch-delivery`
* `validation`
* `freeze`
* `runtime`
* `prompt-sync`
* `startup-sync`
* `unknown`

Do not invent phase values such as:

* `gui`
* `implementation`
* `delivery`
* `freeze_validation_evidence_merge`

unless a newer active canon explicitly changes the enum.

Examples:

A PowerShell freeze wrapper failure:

`operation_phase = "freeze"`

A GUI button or runtime tab behavior regression:

`operation_phase = "runtime"`

A failed validation script:

`operation_phase = "validation"`

A bad patch ZIP or install instruction:

`operation_phase = "patch-delivery"`

---

# 4. Canonical project paths

For the project:

`E:\kanda_reasoner`

the canonical project Error Memory root is:

`E:\kanda_reasoner_show_project_to_AI\project_error_memory`

The canonical AI-assisted pending intake directory is:

`E:\kanda_reasoner_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake`

Externally prepared AI lessons waiting for human review belong there.

Do not write AI-generated lessons directly into canonical Lessons storage.

Do not accidentally use:

`E:\kanda_reasoner\project_error_memory\...`

unless a governed workflow explicitly owns that location.

Do not accidentally create:

`E:\kanda_reasoner\kanda_reasoner_show_project_to_AI\...`

That is a wrong nested path.

---

# 5. Critical Windows drive-root rule

Given:

```powershell
$PROJECT_ROOT = "E:\kanda_reasoner"
```

Correct:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Result:

`E:\`

Do not do this:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
```

because:

`E:\`

becomes:

`E:`

and `E:` is drive-relative in Windows PowerShell.

This can silently send the lesson to the wrong directory.

Preferred construction:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$SHOW_PROJECT_ROOT = [System.IO.Path]::Combine(
    $DRIVE_ROOT,
    $PROJECT_NAME + "_show_project_to_AI"
)
```

Use absolute-root-safe path handling.

---

# 6. Required active-ready lesson structure

The lesson must follow this field model:

* `schema_version`
* `project_slug`
* `lesson_id`
* `status`
* `superseded_by`
* `operation_phase`
* `created_at_utc`
* `updated_at_utc`
* `source_patch_zip`
* `raw_error_text`
* `raw_error_snapshot_scrubbed`
* `symptom`
* `root_cause`
* `wrong_assumption`
* `correct_fix`
* `do_not_repeat_rule`
* `long_term_prevention`
* `redaction`
* `exception`
* `fingerprint`
* `prevention_triggers`
* `regression_check`
* `validation_command_summary`
* `validation_evidence`
* `install_command_summary`
* `notes`

The lesson should use the exact canonical model, not an improvised reduced schema.

---

# 7. Lesson ID rules

The `lesson_id` must be:

* stable;
* lowercase;
* descriptive;
* prefixed with `lesson-`;
* versioned.

Example:

`lesson-freeze-powershell-stderr-nativecommanderror-qt-warning-v1`

A real revised or superseding lesson may become:

`lesson-freeze-powershell-stderr-nativecommanderror-qt-warning-v2`

Do not create random lesson IDs.

Do not create a new version merely to work around stale GUI refresh state.

A new version should represent a genuinely revised lesson identity or superseding correction.

---

# 8. Validation evidence rules

`validation_evidence` must contain only real observed evidence.

Valid evidence examples:

* actual terminal output;
* actual traceback;
* actual validation marker;
* actual patch contract result;
* actual user-observed GUI behavior;
* actual install result;
* actual local Error Memory write success.

Do not invent:

* sandbox validation that was not run;
* local validation that was not run;
* freeze evidence that was not produced;
* Error Memory write success before Memorize Error is clicked.

If sandbox validation passed but local validation did not yet run, write:

`Sandbox validation passed. Local validation is still pending.`

If intake is prepared but not memorized, write:

`Error Memory intake is prepared, but Error Memory write is still pending human review.`

If freeze-ready material exists but Preview and Confirm and Write are incomplete, write:

`Freeze-ready material is prepared, but freeze is not complete until Preview and Confirm and Write are performed by the user.`

---

# 9. Complete regression-marker rule

`regression_check.expected_marker` must contain the complete required marker set for the applicable feature contract.

Do not include only:

`VALIDATION OK: feature-id`

when the contract also requires:

`STATUS: IN_SYNC`

or:

`ZIP CONTRACT: PASS`

or other mandatory markers.

Example:

```json
"expected_marker": "VALIDATION OK: feature-id\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS"
```

Use every marker required by the actual project contract.

---

# 10. Canonical PowerShell staging recipe

The AI should replace all placeholders with real evidence-backed values before sending the command.

```powershell
$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"

    $LESSON_ID = "lesson-REPLACE-WITH-REAL-ERROR-SLUG-v1"

    $INTAKE_FILENAME = (
        "KANDA_ERROR_LESSON_JSON_" +
        "REPLACE_WITH_REAL_ERROR_SLUG_v1.txt"
    )

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT

    # Keep the complete drive root, for example E:\
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

    if (-not $DRIVE_ROOT) {
        throw "Could not determine drive root."
    }

    $SHOW_PROJECT_ROOT = [System.IO.Path]::Combine(
        $DRIVE_ROOT,
        $PROJECT_NAME + "_show_project_to_AI"
    )

    $ERROR_MEMORY_ROOT = [System.IO.Path]::Combine(
        $SHOW_PROJECT_ROOT,
        "project_error_memory"
    )

    $PENDING_INTAKE_DIR = [System.IO.Path]::Combine(
        $ERROR_MEMORY_ROOT,
        "pending_ai_assisted_error_lesson_intake"
    )

    $INTAKE_FILE = [System.IO.Path]::Combine(
        $PENDING_INTAKE_DIR,
        $INTAKE_FILENAME
    )

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    New-Item `
        -ItemType Directory `
        -Path $PENDING_INTAKE_DIR `
        -Force | Out-Null

    $Timestamp = (
        Get-Date
    ).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

    $Lesson = [ordered]@{
        schema_version = "1.0"

        project_slug = $PROJECT_NAME

        lesson_id = $LESSON_ID

        status = "active"

        superseded_by = ""

        # Allowed values only:
        # patch-delivery
        # validation
        # freeze
        # runtime
        # prompt-sync
        # startup-sync
        # unknown
        operation_phase = "REPLACE_WITH_CANONICAL_PHASE"

        created_at_utc = $Timestamp

        updated_at_utc = $Timestamp

        source_patch_zip = "REPLACE_WITH_REAL_PATCH_OR_ARTIFACT"

        raw_error_text = "REPLACE WITH CONCISE REAL ERROR TEXT"

        raw_error_snapshot_scrubbed = "REPLACE WITH REAL SCRUBBED ERROR CHRONOLOGY"

        symptom = "REPLACE WITH USER-OBSERVED FAILURE"

        root_cause = "REPLACE WITH PROVEN ROOT CAUSE OR unknown"

        wrong_assumption = "REPLACE WITH FALSE ASSUMPTION THAT CAUSED THE ERROR"

        correct_fix = "REPLACE WITH PROVEN CORRECTION"

        do_not_repeat_rule = "REPLACE WITH ONE DIRECT ENFORCEABLE RULE"

        long_term_prevention = "REPLACE WITH VALIDATOR, WORKFLOW, OR ARCHITECTURE PREVENTION"

        redaction = [ordered]@{
            applied = $true

            export_safe = $true

            rules = @(
                "No secrets, credentials, API keys, tokens, patient data, or private external service data are included.",
                "The lesson contains only project workflow, patch-delivery, validation, error, runtime, freeze, prompt-sync, startup-sync, or architecture context needed to prevent recurrence.",
                "Local absolute paths are avoided or normalized where possible; retain only technical project identifiers needed for KANDA Reasoner context."
            )
        }

        exception = [ordered]@{
            type = "REPLACE_WITH_NORMALIZED_EXCEPTION_OR_REGRESSION_TYPE"

            # Use the same canonical phase enum.
            phase = "REPLACE_WITH_CANONICAL_PHASE"

            relative_file_path = "REPLACE_WITH_REAL_FILE_UI_OR_COMMAND_SURFACE"

            function_or_test_name = "REPLACE_WITH_REAL_FUNCTION_TEST_OR_WORKFLOW"

            message_normalized = "REPLACE WITH NORMALIZED FAILURE MESSAGE"

            stacktrace_scrubbed = "REPLACE WITH SCRUBBED TRACEBACK OR EXPLICIT NO-TRACEBACK OPERATIONAL FAILURE SUMMARY"
        }

        fingerprint = [ordered]@{
            strategy = "v1_structural_conservative"

            components = @(
                "REPLACE COMPONENT 1",
                "REPLACE COMPONENT 2",
                "REPLACE COMPONENT 3",
                "REPLACE COMPONENT 4",
                "REPLACE COMPONENT 5"
            )

            fingerprint_hash = "replace_with_stable_lowercase_failure_slug"
        }

        prevention_triggers = @(
            "REPLACE TRIGGER 1",
            "REPLACE TRIGGER 2",
            "REPLACE TRIGGER 3",
            "REPLACE TRIGGER 4"
        )

        regression_check = [ordered]@{
            type = "validation_command"

            command = "REPLACE_WITH_REAL_VALIDATION_COMMAND_USING_FORWARD_SLASHES_WHEN_POSSIBLE"

            expected_marker = "REPLACE_WITH_COMPLETE_REQUIRED_MARKER_SET"

            required_before_freeze = $true
        }

        validation_command_summary = "REPLACE WITH REAL VALIDATION COMMAND SUMMARY AND EVERY REQUIRED MARKER"

        validation_evidence = @(
            "REPLACE WITH REAL OBSERVED EVIDENCE 1",
            "REPLACE WITH REAL OBSERVED EVIDENCE 2"
        )

        install_command_summary = "REPLACE WITH HOW THE CORRECTION WAS INSTALLED OR STATE THAT INSTALL WAS NOT THE FAILING STEP"

        notes = "REPLACE WITH IMPORTANT DO-NOT-CONFUSE GUIDANCE"
    }

    $JsonText = $Lesson | ConvertTo-Json -Depth 15

    # Validate outgoing JSON before staging.
    $Parsed = $JsonText | ConvertFrom-Json

    if ($Parsed.lesson_id -ne $LESSON_ID) {
        throw "Outgoing lesson_id validation failed."
    }

    if ($Parsed.status -ne "active") {
        throw "Outgoing status validation failed."
    }

    $AllowedPhases = @(
        "patch-delivery",
        "validation",
        "freeze",
        "runtime",
        "prompt-sync",
        "startup-sync",
        "unknown"
    )

    if ($AllowedPhases -notcontains $Parsed.operation_phase) {
        throw "Invalid operation_phase."
    }

    if ($AllowedPhases -notcontains $Parsed.exception.phase) {
        throw "Invalid exception.phase."
    }

    if (-not $Parsed.redaction.applied) {
        throw "redaction.applied must be true."
    }

    if (-not $Parsed.redaction.export_safe) {
        throw "redaction.export_safe must be true."
    }

    if ($Parsed.redaction.rules.Count -lt 1) {
        throw "redaction.rules must be non-empty."
    }

    if ($Parsed.prevention_triggers.Count -lt 1) {
        throw "prevention_triggers must be non-empty."
    }

    if ($Parsed.validation_evidence.Count -lt 1) {
        throw "validation_evidence must be non-empty."
    }

    if ($Parsed.regression_check.command -match "\\") {
        throw "regression_check.command should use forward slashes when possible."
    }

    $ReceiverText = (
        "KANDA_ERROR_LESSON_JSON_BEGIN" +
        [Environment]::NewLine +
        $JsonText +
        [Environment]::NewLine +
        "KANDA_ERROR_LESSON_JSON_END" +
        [Environment]::NewLine
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $INTAKE_FILE,
        $ReceiverText,
        $Utf8NoBom
    )

    [System.IO.File]::SetLastWriteTimeUtc(
        $INTAKE_FILE,
        [DateTime]::UtcNow
    )

    if (-not (Test-Path $INTAKE_FILE)) {
        throw "Pending intake file was not created."
    }

    $SavedText = [System.IO.File]::ReadAllText($INTAKE_FILE)

    if (
        -not $SavedText.StartsWith(
            "KANDA_ERROR_LESSON_JSON_BEGIN"
        )
    ) {
        throw "Begin marker validation failed."
    }

    if (
        -not $SavedText.TrimEnd().EndsWith(
            "KANDA_ERROR_LESSON_JSON_END"
        )
    ) {
        throw "End marker validation failed."
    }

    Write-Host ""
    Write-Host "ERROR MEMORY AI-ASSISTED INTAKE STAGED"
    Write-Host "========================================"
    Write-Host ""

    Write-Host "Lesson ID:"
    Write-Host $LESSON_ID

    Write-Host ""
    Write-Host "Canonical receiver:"
    Write-Host $INTAKE_FILE

    Write-Host ""
    Write-Host "NEXT ACTION:"
    Write-Host "Review AI-assisted error lesson intake."
    Write-Host "Review Error Editor."
    Write-Host "Click Memorize Error only after human review."
}
catch {
    Write-Host ""
    Write-Host "ERROR MEMORY INTAKE ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host
```

---

# 11. Real KANDA parser validation

Writing the file is not enough.

For high-confidence staging, validate the exact candidate with the real KANDA contracts:

* `text_is_formatted_error_lesson_payload`
* `lesson_from_formatted_text`
* `active_ready`
* `pending_lesson_rows_for_table`

Expected:

`text_is_formatted_error_lesson_payload: True`

`lesson_from_formatted_text: PASS`

`active_ready: True`

`kind: pending_review`

`AUTO_LOAD_ELIGIBLE: YES`

A new valid externally staged lesson should normally become:

`pending_review`

Possible alternative states:

`pending_edit`

means the candidate exists but is not accepted as review-ready.

`pending_duplicate`

means the `lesson_id` already exists in canonical Lessons.

Do not force-load or directly memorize a malformed candidate.

---

# 12. Runtime live-refresh contract

Feature:

`error-memory-gui-pending-intake-live-refresh-v1`

The live-refresh bridge belongs to:

`kanda_reasoner_app/error_memory_gui`

Responsibilities:

1. monitor the canonical pending-intake candidate set;
2. detect newly created or genuinely changed files;
3. debounce/recheck safely;
4. refresh pending Lessons rows;
5. use the existing KANDA parser;
6. use the existing pending-row classifier;
7. use the existing trusted pending loader;
8. never write directly into canonical Lessons;
9. preserve Memorize Error as the human-controlled write gate;
10. avoid overwriting a lesson currently being reviewed;
11. defer a new candidate until the current work surface is clear when necessary;
12. clear stale dismissed state only for the exact changed candidate when appropriate.

Critical architecture rule:

The live-refresh bridge must not become a second Error Memory parser.

It should detect:

`pending intake changed`

and then invoke the normal trusted refresh and load path.

---

# 13. One-time activation rule

When the live-refresh code patch itself is first installed:

Install patch
→ restart KANDA once
→ new runtime behavior becomes active

After that one activation restart, routine intake should work without app restart:

KANDA remains open
→ Error Memory may remain open
→ terminal stages valid lesson
→ live refresh detects it
→ AI-assisted intake window populates
→ human reviews
→ human clicks Memorize Error

Do not confuse:

restart needed to load newly installed Python source

with:

normal future Error Memory staging workflow

Routine staging should not require restart after live refresh is active.

---

# 14. Expected live behavior

After live refresh is active:

1. Keep KANDA open.
2. Open Error Memory.
3. Keep the tab open.
4. Stage a fresh valid Error Memory lesson from PowerShell.
5. Do not close the app.
6. Do not reopen the app.

Expected result:

Within approximately 0.5–1 second:

AI-assisted error lesson intake: populated

Error Editor: synchronized by existing trusted loader when appropriate

Canonical Lessons: unchanged

Memorize Error: still requires human action

If another lesson is currently being edited or reviewed, the new lesson must not overwrite current work.

It should remain deferred until safe to display.

---

# 15. Staging is not memorization

Never claim:

`Error Memory was written`

only because the terminal created a pending file.

Correct statement:

`Error Memory intake is prepared, but Error Memory write is still pending human review.`

Permanent write is complete only after:

* the human clicks Memorize Error;
* and the app reports governed Error Memory write success or the user provides equivalent evidence.

---

# 16. Corrected-error two-track closure

When an error led to a code correction, the work should close in two linked tracks.

Track A: code correction

Track B: Error Memory lesson

The Error Memory lesson should explicitly connect the error to the correction.

Include:

* raw error summary;
* operation phase;
* symptom;
* root cause;
* wrong assumption;
* corrected files;
* corrected functions or workflow areas;
* patch ZIP name when available;
* install summary;
* validation command summary;
* real validation evidence;
* do-not-repeat rule;
* prevention triggers;
* regression check;
* freeze-readiness state when relevant.

A corrected-error workflow should not end with only the code patch when the mistake is reusable enough to belong in Error Memory.

---

# 17. Known failure A — Wrong Windows root handling

Bad:

```powershell
[System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
```

Risk:

`E:\` becomes `E:`

Correct:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

---

# 18. Known failure B — Assuming file existence means GUI success

A file may exist and still not populate the intake window because:

* the payload is malformed;
* the payload is not active-ready;
* classifier returns `pending_edit`;
* classifier returns `pending_duplicate`;
* GUI state has stale dismissal state;
* live refresh is not installed;
* new live-refresh code is installed but the old process is still running;
* another active work item is intentionally protected from overwrite.

Correct diagnostic sequence:

file exists?
→ real parser accepts?
→ active-ready?
→ real scanner sees it?
→ classifier returns `pending_review`?
→ auto-load eligible?
→ live-refresh active in running GUI?

Do not change payload format when parser and classifier already pass.

---

# 19. Known failure C — Creating artificial v2/v3 lessons for GUI refresh

Do not routinely create:

v1 → v2 → v3

just to escape stale GUI state.

Version the lesson only when:

* content is meaningfully revised;
* the prior lesson is superseded;
* the correction itself changes materially.

Runtime refresh problems should be fixed in the runtime refresh path.

---

# 20. Known failure D — Direct write into canonical Lessons

Never bypass:

AI-assisted intake
→ human review
→ Memorize Error

The terminal stages.

KANDA validates.

The human decides.

Canonical storage remains owned by the governed Error Memory workflow.

---

# 21. Troubleshooting decision tree

## Case 1 — File not found

Check:

`E:\kanda_reasoner_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake`

Then verify drive-root handling.

---

## Case 2 — File exists but parser fails

Check:

* exact begin marker;
* exact end marker;
* valid JSON;
* required active-ready fields;
* canonical operation phase;
* canonical exception phase;
* redaction;
* prevention triggers;
* validation evidence;
* regression check;
* complete expected markers.

Expected:

`text_is_formatted_error_lesson_payload: True`

`lesson_from_formatted_text: PASS`

`active_ready: True`

---

## Case 3 — Parser passes but `pending_edit`

The lesson is not review-ready.

Compare it against the active-ready model template.

Do not force it into canonical Lessons.

---

## Case 4 — `pending_duplicate`

Check canonical Lessons for the same `lesson_id`.

Decide whether:

* the lesson is already correctly memorized;
* or a real superseding version is justified.

Do not create duplicate active lessons unnecessarily.

---

## Case 5 — `pending_review` and auto-load eligible, but GUI remains empty

Check:

1. Is live-refresh installed?
2. Was KANDA restarted once after installing the live-refresh code patch?
3. Is the running process using the current project source?
4. Is another Error Memory work item currently active?
5. Did the pending file genuinely change?
6. Is the live-refresh timer active?
7. Is the exact pending candidate still in a stale dismissed set?
8. Is the existing trusted loader being invoked?

Do not rewrite the payload when parser and classifier already prove it valid.

---

# 22. Compact recipe for future AI

When asked:

“Send this error to AI-assisted Error lesson intake.”

Do this:

1. Inspect the real error evidence.
2. Build one complete active-ready lesson.
3. Follow the canonical Error Memory template.
4. Use only canonical phase values.
5. Use exact begin/end markers.
6. Put no prose outside the marker block in the intake file.
7. Derive the Windows drive root safely.
8. Never convert `E:\` into `E:`.
9. Write UTF-8 no BOM to the canonical pending intake directory.
10. Touch/update the candidate timestamp after successful write.
11. Validate with KANDA parser when possible.
12. Require:

* formatted = True
* parse = PASS
* active_ready = True
* row kind = pending_review
* auto-load eligible = YES

13. Let live refresh populate the running GUI.
14. Never write canonical Lessons directly.
15. Tell the user to review the lesson.
16. The user clicks Memorize Error.
17. Only after real write evidence may the AI claim the lesson was memorized.

---

# 23. Final canonical principle

The correct sequence is:

AI creates the lesson.
PowerShell stages the lesson.
KANDA validates the lesson.
Live refresh displays the lesson.
The human reviews the lesson.
Memorize Error writes the lesson.

Never bypass the human gate.

Never invent evidence.

Never confuse pending intake with permanent memory.

END OF HANDOFF
