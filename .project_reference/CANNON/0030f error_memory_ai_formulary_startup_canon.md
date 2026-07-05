# Error Memory AI Formulary Startup Canon

Version: 1.4
Status: always_startup
Owner box: Error Memory / AI Formulary Intake
Scope: KANDA Reasoner and selected-project AI-assisted implementation sessions

## Canonical authority declaration

This file is the canonical owner prompt for the Error Memory AI-assisted intake workflow. It owns **when** Error Memory intake is required, **where and how** AI-produced lesson material is staged, **how** the running Error Memory GUI should discover and load pending intake, and **which human gate** completes canonical memorization.

Schema authority is delegated to these active prompts and must not be redefined inconsistently here:

```text
error_memory_active_ready_json_template
error_memory_model_template
error_memory_active_ready_correction_blueprint
```

Router, navigation, patch-delivery, validation, and correction prompts may bridge to this canon, but they must not create a parallel Error Memory intake doctrine. When this file conflicts with older copied guidance about Error Memory delivery or routine GUI refresh, this v1.4 canon controls the Error Memory intake workflow, while the active schema/model templates control the exact lesson schema.

## Purpose

This startup canon tells the AI how to cooperate with the KANDA Reasoner Error Memory tab.

The Error Memory tab has a **Receive Formulary from AI** workflow. When an error, failed install, failed validation, GUI crash, startup failure, or AI implementation mistake is corrected or meaningfully analyzed, the AI must provide a strict JSON receive block that KANDA can paste into the tab and save as a project-specific lesson.

This is separate from `KANDA_FREEZE_HINT.json`. The freeze hint records implemented feature freeze data. The Error Memory formulary records the mistake, correction, and prevention rule so future AI sessions do not repeat the same error.

## When this canon applies

Apply this canon when any of these are true:

1. The user reports an error, traceback, validation failure, install failure, startup failure, GUI crash, ZIP contract failure, or AI implementation mistake.
2. The AI delivers a correction patch after any failure.
3. The AI explains how an error was corrected.
4. The user asks to save an error, add to Error Memory, fill the Error Memory tab, or prepare data for **Receive Formulary from AI**.
5. A validation/repair loop reveals a repeatable prevention lesson.

Do not emit an Error Memory JSON block for ordinary discussion, planning-only work, or a clean feature patch that did not involve an error/correction lesson.

## Required behavior after correction patches

When delivering or discussing a patch that corrects an error, include a copy-paste-ready Error Memory receive block after the patch/install/validation instructions or after the error analysis.

The block must describe:

- what failed;
- the root cause;
- the wrong assumption;
- the correction;
- the long-term prevention rule;
- the do-not-repeat rule;
- prevention triggers;
- real validation evidence only;
- patch ZIP name, install summary, and validation summary when available.

If the error is not corrected yet or the root cause is uncertain, set `status` to `draft` and clearly state what is missing.

## Receive block format

Return one valid JSON object between these exact markers. The object must use the
same active-ready shape that the Error Memory tab can memorize without asking the
GUI to invent missing fields:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{
  "schema_version": "1.0",
  "project_slug": "kanda_reasoner",
  "lesson_id": "lesson-<stable-slug>-v1",
  "status": "active",
  "superseded_by": "",
  "operation_phase": "patch-delivery|validation|freeze|runtime|prompt-sync|startup-sync|unknown",
  "created_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "updated_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "source_patch_zip": "<patch zip or empty>",
  "raw_error_text": "short scrubbed error/context snapshot",
  "raw_error_snapshot_scrubbed": "scrubbed raw error/context snapshot or clear no-raw-error explanation",
  "symptom": "what failed",
  "root_cause": "why it failed, only if proven",
  "wrong_assumption": "the assumption or missing safeguard that caused the mistake",
  "correct_fix": "how it was corrected or should be corrected",
  "do_not_repeat_rule": "single clear prevention rule",
  "long_term_prevention": "future workflow/test/architecture rule that prevents recurrence",
  "exception": {
    "type": "<error type or domain error>",
    "phase": "<phase>",
    "relative_file_path": "<relative path or empty>",
    "function_or_test_name": "<function/test/workflow or empty>",
    "message_normalized": "<normalized error message>",
    "stacktrace_scrubbed": "<scrubbed trace or explicit no-traceback note>"
  },
  "fingerprint": {
    "strategy": "v1_structural_conservative",
    "components": ["<type>", "<relative path>", "<workflow/function>", "<phase>", "<normalized trigger>"],
    "fingerprint_hash": "<stable sha256>"
  },
  "prevention_triggers": ["trigger phrase 1", "trigger phrase 2"],
  "redaction": {
    "applied": true,
    "export_safe": true,
    "rules": [
      "No secrets or credentials present.",
      "No patient data present.",
      "Project identifiers are intentional technical context."
    ]
  },
  "regression_check": {
    "type": "validation_command",
    "command": "python validation/<test_name>.py",
    "expected_marker": "VALIDATION OK: <feature-id>",
    "required_before_freeze": true
  },
  "validation_command_summary": "what validation proves",
  "validation_evidence": ["real evidence item 1"],
  "install_command_summary": "what the installer stages or changes",
  "notes": "short blameless notes"
}
KANDA_ERROR_LESSON_JSON_END
```

## Strict output rules

- Use valid JSON only between the markers.
- Use double quotes for every key and string value.
- Do not use markdown fences around the receive block when the user needs to paste it into KANDA.
- Do not include comments or trailing commas.
- Escape Windows path backslashes as `\` inside JSON strings.
- Do not invent validation evidence, traceback content, file paths, or root cause.
- If no traceback exists, say that no traceback was provided in `stacktrace_scrubbed` instead of inventing a stack trace.
- Do not include secrets, private tokens, emails, IPs, or unsanitized user paths.
- Keep language factual and blameless. Prefer `wrong_assumption` over blame language.
- `status` may be `active` only when every active-ready field above is present and evidence-backed.
- Use `status: draft` when the correction, evidence, redaction safety, root cause, or regression check is not known yet.


<!-- KANDA_CANON:error_event_owner_box_intake_gate:v2 -->
## Mandatory Error Event Intake Gate

This prompt is the owner canon for turning an error event into Error Memory intake. Router, navigation, bundle, install, validation, and startup prompts may point here, but they must not create a parallel Error Memory doctrine.

Trigger this gate whenever the user reports, or the AI detects, any traceback, validation error, install error, startup failure, GUI crash, ZIP contract failure, wrong patch, prompt-routing mistake, freeze-intake mistake, or repeated AI implementation mistake.

Box logic:

```text
- The active repair box owns source inspection, root-cause analysis, and code/prompt correction.
- The Error Memory box owns prevention capture and AI-assisted error lesson intake.
- Installers may stage a pending lesson for human review.
- Installers must not write directly into Lessons.
- Lessons remain unchanged until the human opens Error Memory, reviews the intake/Error Editor, and clicks Memorize Error.
```

Mandatory sequence for every error-triggered repair:

```text
1. Pause and classify the error event and operation_phase.
2. Capture a scrubbed raw error summary.
3. Read compact Error Memory when available and decide whether full Error Memory is needed.
4. Inspect exact source or prompt files before editing.
5. Correct or meaningfully analyze the error without claiming success for the failed step.
6. Prepare Error Memory lesson material from the same evidence used for the correction.
7. If a correction patch is delivered, include Error Memory intake material in that same patch ZIP unless the user explicitly asks for a Direct Error Lesson ZIP.
8. Stage the formatted lesson into the dynamic pending intake folder during install.
9. Validate both the correction track and the staged Error Memory intake track, or clearly state which track remains pending local validation.
```

Default package path for corrected-error patches:

```text
<drive_where_project_is>:\<project_name>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake\KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
```

The patch payload must include:

```text
payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_<lesson_slug>.txt
```

Closure rule:

```text
A task that began with an error event is not closed by code validation alone. It is closed only when the correction track is addressed and the Error Memory intake track is prepared, staged, validated, or explicitly marked pending human review.
```

Use `status: draft` when the root cause, fix, or validation evidence is incomplete. Use `status: active` only when the lesson is active-ready and supported by evidence. Do not claim the error was remembered in Lessons unless the app or user confirms Memorize Error succeeded.

## Relationship with Error Memory exports

If the uploaded second-prompt files contain compact Error Memory files, read them before coding:

- `*_error_memory_ai_prompt.md`
- `*_error_lessons_compact.json`
- `*_error_memory_manifest.json`

A separate `*_error_memory_full.zip` may also be uploaded. Do not open the full Error Memory ZIP by default. Open it only when the compact files are insufficient, the task is specifically about repeated errors, or the user asks for a deeper Error Memory audit.

## Mandatory check before implementation after an error

When a task follows a reported error or failed validation, begin the implementation reasoning with this internal check and expose a concise summary when useful:

```text
ERROR MEMORY FORMULARY CHECK
Error/correction present: YES / NO
Existing compact lessons relevant: YES / NO / NOT PROVIDED
Will emit receive-ready JSON after correction: YES / NO
Reason:
```

## Final canon

For any correction patch or validated repair, the AI should not only deliver code. It should also give KANDA a structured Error Memory lesson so the corrected mistake can be saved through **Receive Formulary from AI** and avoided in future work.

---
<!-- KANDA_ADDENDUM:error_memory_companion_to_bundle_gated_repair:v1 -->

## Companion Bridge to Bundle-Gated Error Repairs

When kanda_bundle_gated_development_workflow delivers a patch that corrects an error, failed validation, install failure, GUI crash, traceback, or AI implementation mistake, this canon becomes the required companion output.

Prepare a receive-ready Error Memory lesson from the same evidence used for the repair: raw error evidence, Operation phase, symptom, root cause, wrong assumption, correct fix, long-term prevention, do-not-repeat rule, prevention triggers, validation evidence, regression check, patch ZIP name when available, install summary, and validation summary.

Do not invent root cause, fix, or validation evidence. If sandbox validation passed but user-local validation has not run, state that local validation is pending. If the correction is not fully proven, use status draft.

---
<!-- KANDA_ADDENDUM:error_memory_intake_code_fix_reference:v2 -->

## Error Memory Intake Must Reference the Code Correction

When an Error Memory lesson is prepared after a code repair, the lesson must explicitly reference how the code correction fixed the error.

The AI-assisted Error lesson intake material must include:

1. The original error or scrubbed error summary.
2. The Operation phase.
3. The symptom.
4. The root cause, if proven.
5. The wrong assumption or missing safeguard.
6. The corrected source files.
7. The corrected functions, classes, tab, workflow, or validation area.
8. The patch ZIP name, when available.
9. The install command summary.
10. The validation command summary.
11. The validation evidence.
12. The do-not-repeat rule.
13. The prevention triggers.
14. The regression check.
15. The freeze-readiness status.

If the code correction is validated but the Error Memory lesson has not been written locally, state that Error Memory write is pending human review.

If the Error Memory lesson is written locally, include the local write evidence supplied by the app or user.

Do not claim Error Memory write success without local evidence.

Do not claim freeze completion unless Preview and Confirm and Write were performed and the local freeze writer output confirms success.

For corrected-error patches, validation and freeze-readiness must cover both the code correction and the Error Memory lesson.

---
<!-- KANDA_ADDENDUM:prompt_error_lesson_zip_direct_import_canon:v1 -->

## Direct Error Lesson ZIP Canon

Default routine remains unchanged: when the AI delivers code, prompt, GUI, validation, or project-source corrections, it must deliver a normal patch ZIP with install and validation commands, and freeze-ready evidence when applicable.

Direct Error Lesson ZIP is a separate explicit option. Use it only when the user asks for an Error Lesson ZIP, direct import ZIP, formatted Error Memory lesson ZIP, or a ZIP to import into the Error Memory tab.

A Direct Error Lesson ZIP must not be treated as a code patch, app patch, prompt patch, freeze patch, or project-source installer. It must not include source code changes, app files, prompt-library files, generated startup files, or direct writes into Error Memory.

The required Direct Error Lesson ZIP structure is:

```text
bundle_manifest.json
payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_<lesson_slug>.txt
```

The formatted lesson file must contain exactly one receive-ready block:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ valid JSON lesson object }
KANDA_ERROR_LESSON_JSON_END
```

The raw evidence file preserves the copied terminal error, validation failure, traceback, install failure, app error, GUI error, or chat-reported mistake.

The lesson JSON must include the Error Memory metadata needed by the current tab workflow, including `status`, `operation_phase`, `symptom`, `root_cause`, `wrong_assumption`, `correct_fix`, `long_term_prevention`, `do_not_repeat_rule`, `prevention_triggers`, `validation_evidence`, and `regression_check`.

Use `status: active` only when the lesson is active-ready: the symptom, root cause, correct fix, do-not-repeat rule, prevention triggers, and validation evidence are meaningful and supported by evidence. Use `status: draft` when the fix or evidence is incomplete.

The Direct Error Lesson ZIP workflow is:

```text
Error Memory tab
-> Import Error Lesson ZIP
-> AI-assisted error lesson intake is populated
-> Error Editor is populated
-> human may edit Error Editor
-> Memorize Error
-> lesson is saved into Lessons
```

Do not add install or validation PowerShell for a Direct Error Lesson ZIP unless the user explicitly asks for package self-validation. ZIP package validation is enough: verify `bundle_manifest.json`, both payload files, receive markers, parseable JSON, expected `operation_phase`, and active-ready fields when `status` is `active`.

If the user says only `send/gimme Error Lesson ZIP`, deliver the Direct Error Lesson ZIP download link and short GUI import steps. Do not wrap it in the normal code-patch install/validate routine.

If the user asks for the default routine, or the task modifies any project file, source file, GUI file, prompt file, startup file, validation file, or freeze behavior, use the normal patch ZIP -> install -> validate flow instead.

---
<!-- KANDA_ADDENDUM:error_memory_default_autoload_insertion:v2 -->

## Error Memory insertion modes and default autoload workflow

This canon controls how AI delivers a new Error Memory lesson into the KANDA Error Memory tab.

There are three supported modes.

### Mode 1 - Default: ZIP -> install -> validate -> populate Error Memory tab

Use this by default when the user asks to add an error to Error Memory, send an error to the EM tab, create a zipped error with install and validation, or make the error appear in `AI-assisted error lesson intake`.

The default package is a normal patch-style/staging ZIP with install and validation commands. It must not require the user to click `Import Error Lesson ZIP`. The installer must stage the formatted lesson into the dynamic project Error Memory folder derived from the active project root:

```text
<drive_where_project_is>:\<project_name>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake\KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
```

For example, for project root `E:\kanda_reasoner`, the canonical pending folder is:

```text
E:\kanda_reasoner_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
```

The installer must derive this path from `$PROJECT_ROOT`; it must not hardcode `E:\kanda_reasoner` as the universal project root.

Expected GUI behavior after install/staging while the live-refresh feature is active:

```text
KANDA may remain open.
Error Memory may remain the visible tab.
A newly created or genuinely changed valid pending intake file is detected by the Error Memory-owned live-refresh bridge.
AI-assisted error lesson intake = populated through the existing trusted loader.
Error Editor = synchronized by the existing trusted loader when appropriate.
Lessons = unchanged until the human clicks Memorize Error.
```

The runtime refresh contract is owned inside the Error Memory box. The intended ownership is:

```text
kanda_reasoner_app/error_memory_gui/error_memory_tab.py
kanda_reasoner_app/error_memory_gui/_pending_live_refresh.py
kanda_reasoner_app/error_memory_gui/_pending_loader.py
kanda_reasoner_app/error_memory_gui/_pending_rows.py
kanda_reasoner_app/error_memory_gui/_pending_sources.py
```

The live-refresh bridge must detect pending candidate-set changes and invoke the existing trusted refresh/load path. It must not become a second parser, classifier, or canonical writer. `Memorize Error` remains the only human-controlled canonical lesson write action.

A one-time app restart is required only after installing new Python source that adds or changes the live-refresh implementation, because the running Python process must load the new code. After that activation restart, routine terminal staging of new valid pending lessons must not require closing and reopening the app.

## Canonical terminal staging and live-refresh contract - v1

This is the canonical delivery recipe for AI-generated Error Memory lesson material that must appear in `Error Memory tab -> AI-assisted error lesson intake`.

### Safe project-drive derivation

Given a selected project root such as:

```text
E:\kanda_reasoner
```

derive the drive root without trimming the trailing separator:

```powershell
$PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
$PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Do not use:

```powershell
[System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
```

because `E:\` becomes `E:`, and `E:` is drive-relative in Windows PowerShell.

Build the canonical pending intake path with absolute-root-safe joins:

```powershell
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
```

For `E:\kanda_reasoner`, the canonical receiver is:

```text
E:\kanda_reasoner_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
```

### Exact staged-file contract

The staged file must:

1. contain exactly one lesson;
2. begin with `KANDA_ERROR_LESSON_JSON_BEGIN`;
3. end with `KANDA_ERROR_LESSON_JSON_END`;
4. contain no conversational prose outside the markers;
5. use the active-ready schema/model templates;
6. use UTF-8 without BOM;
7. use only canonical phase values;
8. include real validation evidence only;
9. use forward slashes in `regression_check.command`;
10. be written into the canonical pending intake directory, never directly into Lessons.

Recommended PowerShell write method:

```powershell
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
```

The timestamp update is only a change signal for the live-refresh bridge. It does not bypass parsing, classification, duplicate detection, human review, or `Memorize Error`.

### Canonical phase enum

`operation_phase` and `exception.phase` must use only:

```text
patch-delivery
validation
freeze
runtime
prompt-sync
startup-sync
unknown
```

Do not invent alternate values unless a newer active schema canon explicitly changes the enum.

### Real KANDA validation chain

When tooling is available, validate the exact staged candidate through the real KANDA contracts:

```text
text_is_formatted_error_lesson_payload = True
lesson_from_formatted_text = PASS
active_ready = True
pending row kind = pending_review
auto-load eligible = YES
```

Interpretation:

```text
pending_review    = normal new valid lesson ready for human review
pending_edit      = candidate exists but is not review-ready
pending_duplicate = lesson_id already exists in canonical Lessons
```

Do not change the transport format when the exact staged file already passes parser, active-ready, scanner, and `pending_review` classification. In that case, investigate the running GUI refresh path.

### Live-refresh behavior

With the live-refresh implementation active, the normal runtime sequence is:

```text
KANDA remains open
-> Error Memory may remain open
-> PowerShell writes a new or genuinely changed valid pending lesson
-> Error Memory-owned live-refresh bridge detects the candidate-set change
-> existing pending rows refresh
-> existing parser/classifier/loader path runs
-> AI-assisted error lesson intake is populated
-> human reviews
-> human clicks Memorize Error
```

The bridge must not directly write Lessons, maintain a competing parser, or overwrite an Error Memory lesson currently being reviewed. If the work surface is occupied, the new candidate may remain deferred until it is safe to display.

### Staging is not memorization

Do not claim `Error Memory written successfully` merely because the pending file exists or the intake window is populated.

Use:

```text
Error Memory intake is prepared, but Error Memory write is still pending human review.
```

Only claim permanent memorization after governed write evidence or user confirmation that `Memorize Error` succeeded.

---

### Mode 2 - Explicit Direct Error Lesson ZIP

Use this only when the user explicitly asks for an `Error Lesson ZIP`, `direct import ZIP`, `formatted Error Memory lesson ZIP`, or a ZIP to import manually through the Error Memory tab.

This direct package uses this structure:

```text
bundle_manifest.json
payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_<lesson_slug>.txt
```

Direct Error Lesson ZIP workflow:

```text
Error Memory tab -> Import Error Lesson ZIP -> review/edit Error Editor -> Memorize Error
```

Do not use this direct manual-import mode when the user asks for `zip, install, validate, error appears in AI-assisted error lesson intake`. That request means Mode 1.

### Mode 3 - Clipboard/formatted-text loop through AI

Use this when the user uses the GUI buttons:

```text
Copy error/draft to AI
Paste error formatted from AI
```

`Copy error/draft to AI` copies only the current Error Editor content. AI must return a marker-wrapped formatted lesson block:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ valid JSON lesson object }
KANDA_ERROR_LESSON_JSON_END
```

The human pastes that result into `Paste error formatted from AI`, reviews/edits it in Error Editor, and clicks `Memorize Error`.

### Required lesson JSON fields

Every formatted active lesson must include the same active-ready fields that
`Memorize Error` and the ZIP validator require:

```text
schema_version
project_slug
lesson_id
status
operation_phase
created_at_utc
updated_at_utc
source_patch_zip
raw_error_text
raw_error_snapshot_scrubbed
symptom
root_cause
wrong_assumption
correct_fix
do_not_repeat_rule
long_term_prevention
exception
fingerprint
prevention_triggers
redaction
regression_check
validation_command_summary
validation_evidence
install_command_summary
notes
```

Use `status: active` only when the lesson is active-ready and supported by
evidence. Otherwise use `status: draft` and state what is missing in `notes`.


### Do-not-repeat rules

```text
- Do not confuse the default autoload path with manual Import Error Lesson ZIP.
- Do not validate only the staged file; validate the GUI load path and lazy-host trigger when code support is involved.
- Do not hardcode the KANDA Reasoner path; derive <drive> and <project_name> from active PROJECT_ROOT.
- Do not write directly into Lessons without human review; Lessons stays unchanged until Memorize Error.
- Do not clear or overwrite unrelated Error Memory lessons.
```

---
<!-- KANDA_ADDENDUM:active_ready_error_memory_packaged_lesson_contract:v1 -->

## Active-ready packaged Error Memory lesson contract

This section is the owner contract for AI-created packaged Error Memory lessons.
It applies to every normal patch ZIP, direct Error Lesson ZIP, or clipboard
formatted block that contains `KANDA_ERROR_LESSON_JSON`.

### Mandatory packaging rule

Before the AI delivers any package that stages, imports, or asks the user to
memorize an Error Memory lesson, the AI must verify the lesson block against
this active-ready schema. A package must be blocked and repaired before delivery
when `status` is `active` but any required field is missing, empty, unsupported
by evidence, or not export safe.

For normal patch ZIP delivery, this check happens before the ZIP link is emitted.
For Direct Error Lesson ZIP delivery, this check happens before the direct ZIP is
emitted. For clipboard/formatted-text mode, this check happens before the AI
prints the marker-wrapped block.

### Active-ready lesson JSON shape

When `status` is `active`, the marker-wrapped JSON object must include all of
these keys with meaningful values:

```text
schema_version
lesson_id
status
superseded_by
project_slug
operation_phase
created_at_utc
updated_at_utc
source_patch_zip
raw_error_text
symptom
root_cause
wrong_assumption
correct_fix
long_term_prevention
do_not_repeat_rule
exception
fingerprint
prevention_triggers
regression_check
validation_command_summary
validation_evidence
redaction
raw_error_snapshot_scrubbed
install_command_summary
notes
```

The `exception` object must include:

```text
type
phase
relative_file_path
function_or_test_name
message_normalized
stacktrace_scrubbed
```

The `fingerprint` object must include:

```text
strategy
components
fingerprint_hash
```

The `regression_check` object must include:

```text
type
command
expected_marker
required_before_freeze
```

The `redaction` object is mandatory for active lessons and must include:

```text
applied
export_safe
rules
```

`redaction.applied` must be true. `redaction.export_safe` must be true. The
`rules` list must state what was scrubbed or why the lesson is safe to export.

### Active-ready minimum evidence rules

Use `status: active` only when all of these are true:

1. `symptom`, `root_cause`, `correct_fix`, `do_not_repeat_rule`, and
   `long_term_prevention` are specific and non-empty.
2. `prevention_triggers` is a non-empty list of concrete trigger phrases.
3. `validation_evidence` is a non-empty list of real evidence from the current
   chat, terminal output, user report, validation output, or inspected artifact.
4. `regression_check.command` and `regression_check.expected_marker` identify
   the check that should prevent recurrence, unless the lesson is explicitly a
   non-code/manual lesson and explains that in `regression_check.type`.
5. `redaction.applied` and `redaction.export_safe` are true.
6. `raw_error_snapshot_scrubbed` contains scrubbed error context or a clear
   explanation that the raw error was unavailable.

If any of these are not true, use `status: draft` and state what is missing.

### Active-ready template

Use this template as the canonical structure for packaged lessons:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{
  "schema_version": "1.0",
  "lesson_id": "lesson-<stable-slug>-v1",
  "status": "active",
  "superseded_by": "",
  "project_slug": "<project_slug>",
  "operation_phase": "patch-delivery|validation|freeze|runtime|prompt-sync|startup-sync|unknown",
  "created_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "updated_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "source_patch_zip": "<patch zip or empty>",
  "raw_error_text": "short scrubbed error/context snapshot",
  "symptom": "what failed",
  "root_cause": "why it failed",
  "wrong_assumption": "the assumption or missing safeguard that caused the mistake",
  "correct_fix": "how it was corrected or should be corrected",
  "long_term_prevention": "future workflow/test/architecture rule that prevents recurrence",
  "do_not_repeat_rule": "single clear prevention rule",
  "exception": {
    "type": "<error type or domain error>",
    "phase": "<phase>",
    "relative_file_path": "<relative path or empty>",
    "function_or_test_name": "<function/test/workflow or empty>",
    "message_normalized": "<normalized message>",
    "stacktrace_scrubbed": "<scrubbed trace or empty>"
  },
  "fingerprint": {
    "strategy": "v1_structural_conservative",
    "components": [
      "<type>",
      "<relative path>",
      "<function/test/workflow>",
      "<phase>",
      "<normalized trigger>"
    ],
    "fingerprint_hash": "<stable sha256 or clearly derived placeholder only for draft>"
  },
  "prevention_triggers": [
    "<trigger phrase 1>",
    "<trigger phrase 2>"
  ],
  "regression_check": {
    "type": "validation_command",
    "command": "python validation/<test_name>.py",
    "expected_marker": "VALIDATION OK: <feature-id>",
    "required_before_freeze": true
  },
  "validation_command_summary": "what validation proves",
  "validation_evidence": [
    "real evidence item 1",
    "real evidence item 2"
  ],
  "redaction": {
    "applied": true,
    "export_safe": true,
    "rules": [
      "No secrets or credentials present.",
      "Raw paths or private details were scrubbed or are intentional project context."
    ]
  },
  "raw_error_snapshot_scrubbed": "scrubbed raw error/context snapshot",
  "install_command_summary": "what the installer stages or changes",
  "notes": "short blameless notes"
}
KANDA_ERROR_LESSON_JSON_END
```

### Packaged lesson files

A package that carries Error Memory lessons must place each lesson at:

```text
payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_<lesson_slug>.txt
```

For the default autoload workflow, the installer must stage the formatted lesson
into the dynamic pending intake folder derived from `$PROJECT_ROOT`:

```text
<drive>:\<project>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
```

The installer must not write directly into saved Lessons. Human review and
`Memorize Error` remain required.

### Do-not-repeat checks for AI

Before any patch ZIP is released, the AI must inspect every packaged
`KANDA_ERROR_LESSON_JSON_*.txt` file and block release if an active lesson lacks
`redaction`, `exception`, `fingerprint`, `prevention_triggers`, or
`validation_evidence`.

Do not answer with only a corrected JSON block when the failure is a recurring
packaging logic problem. Patch the canon/guardrail so the next AI creates the
packaged lesson correctly the first time.

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



---
<!-- KANDA_ADDENDUM:error_memory_active_ready_creation_contract:v2 -->

## Error Memory active-ready creation contract - v2

This section resolves the observed failure where AI returned marker-wrapped JSON
that looked conceptually correct but was not memorization-ready because it missed
active lesson metadata such as `raw_error_text`, `raw_error_snapshot_scrubbed`,
`redaction`, `exception`, and `fingerprint`.

Creation path rule:

```text
Any text that AI creates for the AI-assisted error lesson intake window must be
created from the active-ready template, not from the older minimal template.
```

Hard output gate before printing or packaging a lesson:

```text
1. Parse the exact JSON object that will be sent to AI-assisted error lesson intake.
2. If status is active, verify that all active-ready fields are present.
3. Verify `raw_error_text` and `raw_error_snapshot_scrubbed` contain scrubbed,
   evidence-backed context.
4. Verify `redaction.applied` and `redaction.export_safe` are true and
   `redaction.rules` is non-empty.
5. Verify `exception`, `fingerprint`, `prevention_triggers`,
   `regression_check`, and `validation_evidence` are present and meaningful.
6. If a field cannot be supported by the provided evidence, do not guess; change
   `status` to `draft` and explain the missing evidence in `notes`.
```

Do not repair this recurring problem by manually correcting one JSON block only.
Correct the generation prompt, parser/builder, and package validation gate so the
next AI-created Error Memory lesson is active-ready before it reaches the intake
window.

<!-- KANDA_ADDENDUM:error_memory_active_ready_creation_contract:v2_END -->

<!-- ERROR_MEMORY_ACTIVE_READY_OUTPUT_HARD_GATE_V21_BEGIN -->

## Error Memory active-ready output hard gate - v21

This is a hard output gate for every `KANDA_ERROR_LESSON_JSON` block that AI
prints, packages, stages, or asks the user to paste into the AI-assisted error
lesson intake window.

Observed regression blocked by this gate:

```text
This lesson is not active-ready. Required fields, prevention triggers, and
redaction metadata must be present before saving as active.
```

The failed class is an active lesson that looks conceptually complete but misses
active-ready metadata such as `raw_error_text`, `raw_error_snapshot_scrubbed`, or
`redaction`. This must be blocked before the text reaches the Error Memory tab.

### Mandatory output gate

Before emitting any marker-wrapped lesson, ZIP package, pending intake file, or
clipboard/formatted-text response, inspect the exact outgoing JSON object. Do not
inspect a plan, summary, partial draft, or earlier version.

If `status` is `active`, the exact outgoing JSON object must include all fields
below:

```text
schema_version
lesson_id
status
superseded_by
project_slug
operation_phase
created_at_utc
updated_at_utc
source_patch_zip
raw_error_text
raw_error_snapshot_scrubbed
symptom
root_cause
wrong_assumption
correct_fix
long_term_prevention
do_not_repeat_rule
prevention_triggers
exception
fingerprint
regression_check
validation_command_summary
validation_evidence
redaction
install_command_summary
notes
```

The nested objects must also be complete:

```text
exception.type
exception.phase
exception.relative_file_path
exception.function_or_test_name
exception.message_normalized
exception.stacktrace_scrubbed
fingerprint.strategy
fingerprint.components
fingerprint.fingerprint_hash
regression_check.type
regression_check.command
regression_check.expected_marker
regression_check.required_before_freeze
redaction.applied
redaction.export_safe
redaction.rules
```

Active-ready meaning checks:

```text
raw_error_text: non-empty scrubbed error or context evidence
raw_error_snapshot_scrubbed: non-empty scrubbed evidence or explicit no-raw-error explanation
prevention_triggers: non-empty list of concrete trigger phrases
validation_evidence: non-empty list of real evidence
redaction.applied: true
redaction.export_safe: true
redaction.rules: non-empty list
```

Fail-closed rule:

```text
If any required active-ready field is missing, empty, unsupported by evidence, or
not export safe, do not emit status active. Either repair the exact JSON before
output or change status to draft and state what evidence is missing in notes.
```

Do not rely on older minimal lesson shapes. A lesson that has `schema_version`,
`lesson_id`, `exception`, `fingerprint`, `prevention_triggers`, and
`validation_evidence` but lacks `raw_error_text`, `raw_error_snapshot_scrubbed`,
or `redaction` is invalid when `status` is `active`.

Do not answer by only correcting one malformed pasted block when the failure is
that AI is generating malformed active lessons. Correct or apply this prompt gate
first, then prepare any corrected lesson material from the same active-ready
contract.

<!-- ERROR_MEMORY_ACTIVE_READY_OUTPUT_HARD_GATE_V21_END -->

<!-- ERROR_MEMORY_JSON_FORWARD_SLASH_ACTIVE_READY_GATE_V22_BEGIN -->

## Error Memory JSON forward-slash active-ready gate - v22

This gate applies to every `KANDA_ERROR_LESSON_JSON` block, Direct Error Lesson
ZIP, pending AI-assisted Error Memory intake file, and prompt-generated Error
Memory lesson.

The failure class is not one bad final text. The failed box is the Error Memory
lesson creation contract. AI must not emit visually plausible JSON that later
parses with path corruption or fails active-ready validation.

### Slash-only command rule

Inside Error Memory JSON, every validation command and machine-ingested path must
use forward slashes `/`. Do not use Windows backslashes in `regression_check.command`.

Correct:

```json
"command": "python validation/test_error_memory_memorize_clears_intake_only_v2.py"
```

Blocked:

```json
"command": "python validation\test_error_memory_memorize_clears_intake_only_v2.py"
"command": "python validation	est_error_memory_memorize_clears_intake_only_v2.py"
```

Reason: the single-backslash form can parse as control characters such as tab.
The double-backslash form is valid JSON, but it keeps future AI and users in the
same failure mode. Error Memory JSON uses slash-only commands.

### Required exact-output validation before delivery

Before AI emits any active `KANDA_ERROR_LESSON_JSON`, it must check the exact
outgoing text, not a plan or earlier draft:

```text
1. Marker wrapper is exactly KANDA_ERROR_LESSON_JSON_BEGIN / END.
2. The text between markers is one valid JSON object.
3. status active has the full active-ready field set.
4. redaction.applied is true.
5. redaction.export_safe is true.
6. redaction.rules is a non-empty list.
7. prevention_triggers is a non-empty list.
8. validation_evidence is a non-empty list.
9. regression_check.command uses forward slashes and contains no backslash.
10. regression_check.command contains no tab, newline, carriage return,
    backspace, form-feed, or vertical-tab control characters.
```

If tool/sandbox validation is available, run that validation before delivering
the patch, ZIP, or receive-ready block. If validation is not available, do not
emit `status: active`; use draft and explain the missing validation in `notes`.

Fail closed. Do not ask the user to fix one block manually when the generation
path is creating malformed active lessons.

<!-- ERROR_MEMORY_JSON_FORWARD_SLASH_ACTIVE_READY_GATE_V22_END -->
