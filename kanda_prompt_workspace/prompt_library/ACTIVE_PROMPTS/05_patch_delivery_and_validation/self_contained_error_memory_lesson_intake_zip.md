---
prompt_code: KPR-05-008
prompt_id: self_contained_error_memory_lesson_intake_zip
title: Self-Contained Error Memory Lesson Intake ZIP
version: 1.2
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: freeze-error-intake-bridge-v1
---

# MASTER PROMPT - CREATE A SELF-CONTAINED ERROR MEMORY LESSON INTAKE ZIP FOR THE CURRENT PROJECT

You are working with the currently selected active Project in KANDA Reasoner.

Your task is to identify the real lessons from the current work, create complete Error Memory lesson records, and package them into one self-contained ZIP that stages the lessons inside the Error Memory pending-intake tab for human review.

Do not create separate lesson ZIPs.

Do not provide only lesson JSON.

Do not create a separate external runner file.

Create one ZIP containing:

- all lesson records;
- all Python code;
- all PowerShell code;
- package validation;
- intake validation;
- the packaged installation entry point.

After creating the ZIP, provide one complete PowerShell installation block that verifies, stages, extracts, and executes the packaged `RUN_INSTALL.ps1`.

The loader must make the lessons available in Error Memory for approval.

It must never press or imitate `Memorize Error`.

It must never write directly into canonical Error Memory lessons.

## CURRENT-PROJECT DISCOVERY

Before creating anything, determine the actual selected Project identity from the current handoff, registry state, source archive, owner manifests, or user-provided paths.

Resolve:

PROJECT_ROOT
PROJECT_NAME
PROJECT_SLUG
PROJECT_DISPLAY_NAME
PROJECT_PARENT_ROOT
PROJECT_DRIVE_ROOT
PROJECT_SUPPORT_ROOT
PROJECT_DAILY_WORK_ROOT
PROJECT_ERROR_MEMORY_ROOT
PROJECT_ERROR_MEMORY_OWNER_MANIFEST
PENDING_INTAKE_ROOT
CANONICAL_LESSONS_ROOT

Expected relationships commonly follow:

PROJECT_ROOT:
<parent>\<project_name>

PROJECT_SUPPORT_ROOT:
<parent>\<project_name>_show_project_to_AI

PROJECT_DAILY_WORK_ROOT:
<parent>\<project_name>_delete_after_daily_work

PROJECT_ERROR_MEMORY_ROOT:
<PROJECT_SUPPORT_ROOT>\project_error_memory

PROJECT_ERROR_MEMORY_OWNER_MANIFEST:
<PROJECT_ERROR_MEMORY_ROOT>\owner_manifest.json

PENDING_INTAKE_ROOT:
<PROJECT_ERROR_MEMORY_ROOT>\pending_ai_assisted_error_lesson_intake

CANONICAL_LESSONS_ROOT:
<PROJECT_ERROR_MEMORY_ROOT>\lessons

Do not assume the Project is `kanda_reasoner`.

Do not assume the drive is `E:`.

These are expected naming patterns only. Validate actual paths and ownership before using them. Prefer canonical selected-Project registry and owner-manifest evidence over paths constructed only from naming conventions.

Do not use paths, identities, owner manifests, lesson IDs, or evidence from another Project except when another Project was genuinely used as an external validation fixture.

External fixtures may be mentioned in validation evidence, but they must never become the owner of the lesson.

## CURRENT PROJECT OWNERSHIP

The currently selected active Project is the only owner of the new Error Memory lessons.

All lesson records must use:

project_slug:
the actual selected Project slug

owner identity:
the selected Project Error Memory owner

pending intake:
the selected Project pending-intake directory

canonical lesson checks:
the selected Project canonical Error Memory lessons directory

Another Project may appear in validation evidence only when it was genuinely used as an external fixture, integration target, or ownership-reuse test.

An external fixture must never become:

- the lesson owner;
- the Project slug;
- the Error Memory root;
- the pending-intake root;
- the canonical lessons root;
- the owner manifest;
- the Project source owner;
- the primary Box owner.

## ANTI-CROSS-PROJECT RULE

Before staging anything, verify that:

1. PROJECT_ROOT belongs to the selected Project.
2. PROJECT_SUPPORT_ROOT belongs to the selected Project.
3. PROJECT_ERROR_MEMORY_ROOT belongs to the selected Project.
4. owner_manifest.json identifies the selected Project.
5. every lesson project_slug matches the selected Project.
6. no pending lesson is written under another Project support root.
7. no canonical lesson from another Project is inspected as the selected Project canonical lesson.

Fail closed when Project ownership is ambiguous or inconsistent.

## EXACT OBJECTIVE

The final self-contained ZIP must:

1. Contain every new lesson identified from the current work.
2. Contain complete active-ready Error Memory lesson records.
3. Validate the exact archive-member set.
4. Validate every lesson schema and identity.
5. Validate the selected Project Error Memory owner manifest.
6. Stage lessons only under the current Project's pending-intake folder.
7. Make the lessons appear in Error Memory for human review.
8. Avoid writing directly into canonical `project_error_memory\lessons`.
9. Avoid executing `Memorize Error`.
10. Avoid modifying Project source code.
11. Avoid modifying Freeze Memory.
12. Avoid modifying Project selection or Project registry state.
13. Avoid overwriting an already memorized lesson.
14. Support safe idempotent re-execution.
15. Produce a durable intake receipt under the Project daily-work root.
16. Include one packaged execution entry point named `RUN_INSTALL.ps1`.
17. Require only one externally supplied ZIP and one external terminal installation block.

## LESSON SELECTION

Create one lesson for each distinct demonstrated failure class.

Do not combine unrelated root causes into one broad lesson.

Create separate lessons when failures differ in any of these ways:

- different root cause;
- different wrong assumption;
- different affected Box;
- different prevention rule;
- different validator or regression obligation;
- different operational phase.

Do not create duplicate lessons for multiple symptoms caused by the same root defect.

Before creating a lesson:

1. Inspect the real failure output.
2. Inspect the exact affected source.
3. Inspect relevant Compact Error Memory.
4. Open Full Error Memory when repeated-error debugging or conflict checking requires it.
5. Search for an existing lesson with the same fingerprint or prevention rule.
6. Decide whether to:
   - create a new lesson;
   - update an existing draft;
   - treat the issue as already covered;
   - create no lesson.

Do not create a lesson merely because a command failed.

Create a lesson only when the failure provides a reusable prevention rule.

## REAL EVIDENCE ONLY

Every lesson must be grounded in actual evidence from the current work.

Valid evidence may include:

- traceback text;
- validator output;
- transactional rollback output;
- source inspection;
- package-member inspection;
- manifest inspection;
- successful correction markers;
- successful production validation;
- successful GUI smoke results;
- exact file paths;
- exact function or symbol names;
- exact feature IDs;
- exact validator names;
- final artifact hashes.

Do not invent:

- validation markers;
- root causes;
- affected files;
- function names;
- regression commands;
- successful corrections;
- freeze IDs;
- Project identities;
- timestamps.

If a fact cannot be established, mark it clearly as unresolved or omit it when the schema permits.

## LESSON FILE TRANSPORT FORMAT

Create one lesson file for each lesson.

Filename format:

KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt

Each lesson file must use this exact marker-wrapped transport:

KANDA_ERROR_LESSON_JSON_BEGIN

{
  "...": "..."
}

KANDA_ERROR_LESSON_JSON_END

Rules:

- The beginning marker must appear exactly once.
- The ending marker must appear exactly once.
- The beginning marker must be the first non-whitespace content.
- The ending marker must be the last non-whitespace content.
- The content between the markers must be valid JSON.
- Do not include Markdown fences.
- Do not place prose outside the markers.
- Use double quotes.
- Do not use comments.
- Do not use trailing commas.
- Save as UTF-8 without BOM.
- Prefer JSON generated with ASCII escaping enabled.

## REQUIRED LESSON TOP-LEVEL FIELDS

Each completed active-ready lesson must contain all of these fields:

schema_version
lesson_id
status
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

Required values:

schema_version:
"1.0"

status:
"active"

project_slug:
the real current Project slug

`prevention_triggers` must be a non-empty JSON array of strings.

`validation_evidence` must be a non-empty JSON array of strings.

Do not serialize arrays as strings that merely look like lists.

## LESSON ID

Use a stable, descriptive lesson ID:

lesson-<specific-failure-class>-v1

Examples of acceptable structure:

lesson-validator-project-package-import-bootstrap-v1
lesson-portable-source-manifest-membership-assumption-v1
lesson-tool-portable-private-settings-project-authority-v1

The lesson ID must describe the reusable failure class, not merely the patch filename.

All lesson IDs inside the package must be unique.

## EXCEPTION OBJECT

The `exception` object must contain:

type
phase
relative_file_path
function_or_test_name
message_normalized
stacktrace_scrubbed

Use Project-relative file paths where possible.

Do not include secrets, personal profile paths, tokens, credentials, or unrelated absolute user paths.

## FINGERPRINT OBJECT

The `fingerprint` object must contain:

strategy
components
fingerprint_hash

Requirements:

strategy:
"v1_structural_conservative"

components:
a non-empty JSON array of stable structural characteristics

fingerprint_hash:
a deterministic SHA-256 derived from the normalized fingerprint components

The fingerprint should capture the reusable failure pattern, not a transient timestamp.

## REGRESSION_CHECK OBJECT

The `regression_check` object must contain:

type
command
expected_marker
required_before_freeze

Use the actual focused validator or regression command when one exists.

Do not claim a regression command exists when none was created.

When no command exists, use an explicit non-available representation rather than inventing one.

## REDACTION OBJECT

The `redaction` object must contain:

applied
export_safe
rules

Required:

applied:
true

export_safe:
true

rules:
a JSON array explaining any applied redaction or an empty array when no redaction was needed

Do not include credentials, API keys, personal tokens, private user profile details, or unrelated secrets.

## PACKAGE STRUCTURE

The ZIP must contain files directly at the archive root.

Do not include an enclosing parent directory.

Mandatory fixed members:

CAPTURED_ERROR_MEMORY_EVIDENCE.txt
ERROR_MEMORY_LOADER.py
INSTALL.ps1
PACKAGE_MANIFEST.json
PREPARE_ERROR_MEMORY.ps1
README.txt
RUN_INSTALL.ps1
VALIDATE.ps1
VALIDATE_PACKAGE.py

Also include one lesson file for every lesson:

KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt

Therefore, the exact archive-member set is dynamic only with respect to the lesson files.

No other members are permitted.

Do not include:

- source-code payloads;
- backups;
- cache files;
- `__pycache__`;
- `.pyc` files;
- temporary files;
- extracted folders;
- nested ZIPs;
- Freeze hints;
- canonical Error Memory files;
- owner manifests copied from the Project;
- external runner scripts.

## PACKAGE NAMING

Use:

<project_slug>_<feature_or_workflow_slug>_error_memory_intake_loader_v1.zip

For a corrected loader, increment only the loader version:

v1r1
v2
v3

Do not overwrite an older package while continuing to advertise its previous SHA-256.

Calculate the final SHA-256 only after the last archive rebuild.

## PACKAGE_MANIFEST.JSON

`PACKAGE_MANIFEST.json` must contain at least:

schema_version
kind
feature_id
package_name
project_slug
lesson_ids
exact_members
member_sha256
pending_intake_contract
self_contained_runner
source_files_modified
canonical_lessons_written
human_memorize_required

Required values:

schema_version:
"1.0"

kind:
"kanda_error_memory_intake_loader"

pending_intake_contract:
"project_error_memory/pending_ai_assisted_error_lesson_intake"

self_contained_runner:
"RUN_INSTALL.ps1"

source_files_modified:
false

canonical_lessons_written:
false

human_memorize_required:
true

`lesson_ids` must contain every packaged lesson ID exactly once.

`exact_members` must match the complete ZIP member set exactly.

`member_sha256` must contain SHA-256 values for every archive member except `PACKAGE_MANIFEST.json` itself, avoiding recursive self-hashing.

## VALIDATE_PACKAGE.PY

Create an internal package validator that validates the final ZIP itself.

It must check:

1. The ZIP filename matches `package_name`.
2. The archive contains the exact expected member set.
3. No member is duplicated.
4. No member uses an absolute path.
5. No member uses a drive path.
6. No member uses a UNC path.
7. No member begins with `/` or `\`.
8. No member contains a `..` traversal component.
9. No member is a directory.
10. No unexpected nested path exists.
11. `PACKAGE_MANIFEST.json` parses as valid JSON.
12. Manifest kind is correct.
13. Manifest Project slug is correct.
14. Manifest lesson IDs exactly match the lesson files.
15. Manifest exact-members list matches the ZIP.
16. Every declared member hash matches.
17. Every lesson file uses the exact marker contract.
18. Every lesson payload parses as valid JSON.
19. Every lesson contains all required top-level keys.
20. Every lesson status is `active`.
21. Every lesson Project slug matches the current package Project slug.
22. Every lesson ID is unique.
23. `prevention_triggers` is a non-empty array.
24. `validation_evidence` is a non-empty array.
25. Redaction is applied and export-safe.
26. No source payload exists.
27. No canonical Error Memory lesson file is included.
28. `RUN_INSTALL.ps1` exists at the archive root.

On success, print markers including:

ERROR MEMORY LOADER EXACT MEMBER SET: PASS
ERROR MEMORY LESSON ACTIVE-READY SCHEMA: PASS
ERROR MEMORY HUMAN MEMORIZE GATE: PASS
ERROR MEMORY CANONICAL WRITE PATH: ABSENT
ERROR MEMORY LOADER VALIDATION: PASS

## ERROR_MEMORY_LOADER.PY

Create the actual pending-intake loader.

It must support two modes:

1. Validation-only mode.
2. `--stage` mode.

Required command-line arguments:

--project-root
--package-root
--package-zip

Optional flag:

--stage

### PROJECT PATH RESOLUTION

Resolve the real Project root.

Derive or verify:

project_support_root
project_daily_work_root
project_error_memory_root
pending_intake_root
canonical_lessons_root

Use the actual selected Project identity.

Validate:

<project_error_memory_root>\owner_manifest.json

Require the owner manifest to belong to the current Project.

Fail closed on:

- missing owner manifest;
- malformed owner manifest;
- Project slug mismatch;
- owner root mismatch;
- ownership conflict;
- another Project's Error Memory root.

### VALIDATION-ONLY MODE

Validation-only mode must:

1. Verify the owner manifest.
2. Validate every packaged lesson file.
3. Confirm all lesson IDs and Project identity.
4. Confirm the pending-intake owner path.
5. Confirm no canonical write will occur.
6. Confirm `Memorize Error` will not execute.

Print:

ERROR MEMORY OWNER IDENTITY: PASS
ERROR MEMORY PROJECT SUPPORT ROOT: <actual path>
ERROR MEMORY DAILY WORK ROOT: <actual path>
ERROR MEMORY ACTIVE-READY LESSON COUNT: <count>
ERROR MEMORY CANONICAL LESSON WRITE: NO
MEMORIZE ERROR EXECUTED: NO
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY LOADER PROJECT PREFLIGHT: PASS

### STAGING MODE

Staging mode must use:

<PROJECT_ERROR_MEMORY_ROOT>\pending_ai_assisted_error_lesson_intake

For each lesson:

1. Determine the canonical target:
   <CANONICAL_LESSONS_ROOT>\<lesson_id>.json

2. If the canonical lesson already exists:
   - validate that its internal lesson ID matches;
   - do not overwrite it;
   - do not restage it;
   - print:

LESSON ALREADY MEMORIZED - NOT RESTAGED: <lesson_id>

3. If the pending lesson already exists and is byte-identical:
   - leave it unchanged;
   - print:

LESSON ALREADY STAGED FOR APPROVAL: <lesson_id>

4. If a pending file with the same filename exists but differs:
   - rename it to:

<filename>.replaced_<UTC timestamp>.invalid_do_not_scan

   - do not delete it silently;
   - atomically write the corrected pending lesson.

5. For a new lesson:
   - write first to a temporary file;
   - use UTF-8 without BOM;
   - use newline `\n`;
   - atomically replace the final pending file;
   - print:

LESSON STAGED FOR APPROVAL: <lesson_id>

Do not write into:

<PROJECT_ERROR_MEMORY_ROOT>\lessons

Do not invoke any canonical lesson writer.

Do not call or simulate `Memorize Error`.

Do not alter the GUI.

Do not edit Project source.

### INTAKE RECEIPT

Create a durable execution receipt under:

<PROJECT_DAILY_WORK_ROOT>\error_memory_intake_loader\<UTC timestamp>\intake_receipt.json

The receipt must include:

artifact_type
schema_version
project_slug
project_root
project_support_root
error_memory_root
pending_intake_root
package_zip
owner_id
created_at_utc
lessons
canonical_lessons_written
memorize_error_executed
project_source_files_modified

Each lesson receipt entry must include:

lesson_id
action
pending_path
canonical_path

Possible actions:

staged
already_staged
replaced_stale_pending
already_memorized

Required receipt values:

canonical_lessons_written:
0

memorize_error_executed:
false

project_source_files_modified:
0

### FINAL STAGING MARKERS

Print:

ERROR MEMORY OWNER IDENTITY: PASS
ERROR MEMORY PENDING INTAKE ROOT: <actual path>
ERROR MEMORY LESSONS AVAILABLE FOR APPROVAL: <count>
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY INTAKE RECEIPT: <actual receipt path>
ERROR MEMORY TAB APPROVAL READY: PASS

## VALIDATE.PS1

`VALIDATE.ps1` must accept:

-ProjectRoot
-PackageZip

It must:

1. Confirm ProjectRoot exists.
2. Confirm PackageZip exists.
3. Resolve a Python interpreter in this order:
   - `<PROJECT_ROOT>\.venv\Scripts\python.exe`
   - `<PROJECT_ROOT>\venv\Scripts\python.exe`
   - `python.exe`
   - `py.exe -3`
4. Treat the Python executable and optional prefix arguments separately.
5. Run `VALIDATE_PACKAGE.py`.
6. Locate the official Project ZIP validator:

<PROJECT_ROOT>\scripts\validate_patch_zip.py

7. Run the official validator using the loader's non-freezeable classification.
8. Require:

ZIP CONTRACT: PASS

9. Run `ERROR_MEMORY_LOADER.py` in validation-only mode.
10. Fail immediately when any command returns nonzero.
11. Print:

ZIP CONTRACT: PASS
ERROR MEMORY INTAKE VALIDATION: PASS

Do not use an improvised inline `python -c`.

## PREPARE_ERROR_MEMORY.PS1

`PREPARE_ERROR_MEMORY.ps1` must accept:

-ProjectRoot
-PackageZip

It must:

1. Run `VALIDATE.ps1`.
2. Capture and display its complete output.
3. Stop when validation fails.
4. Require these exact markers:

ZIP CONTRACT: PASS
ERROR MEMORY LOADER VALIDATION: PASS
ERROR MEMORY INTAKE VALIDATION: PASS

5. Resolve Python using the same interpreter logic.
6. Run:

ERROR_MEMORY_LOADER.py --project-root <root> --package-root <package root> --package-zip <staged ZIP> --stage

7. Stop when staging fails.
8. Print:

ERROR MEMORY LOADER SOURCE FILES MODIFIED: 0
PROJECT SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
ERROR MEMORY LESSON INTAKE PREPARATION COMPLETE

## INSTALL.PS1

`INSTALL.ps1` must:

1. Accept ProjectRoot and PackageZip.
2. Invoke `PREPARE_ERROR_MEMORY.ps1`.
3. Stop on failure.
4. Print:

ERROR MEMORY LOADER INSTALLATION OK: <feature_id>

It must not install source code.

It must not copy files into canonical Error Memory Lessons.

It must not execute a Project build.

It must not execute Freeze preparation.

## RUN_INSTALL.PS1

`RUN_INSTALL.ps1` is the only packaged execution entry point.

It must accept:

-ProjectRoot
-PackageZip

It must:

1. Confirm ProjectRoot exists.
2. Confirm the staged PackageZip exists.
3. Invoke packaged `INSTALL.ps1`.
4. Stop on nonzero exit.
5. Print:

ERROR MEMORY LESSON LOADER: PASS
PROJECT SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
OPEN ERROR MEMORY FOR HUMAN APPROVAL

## README.TXT

Explain:

- what lessons are contained;
- why each lesson exists;
- that the ZIP stages lessons only for approval;
- that no source code is modified;
- that no canonical lesson is written;
- that `Memorize Error` remains human-only;
- how to review the lessons in Error Memory;
- where the pending intake is located.

## CAPTURED_ERROR_MEMORY_EVIDENCE.TXT

Include a concise evidence record containing:

- the relevant actual failures;
- the corrected behavior;
- validator success markers;
- rollback evidence when applicable;
- final successful feature or production evidence;
- source of each lesson;
- Project identity.

Do not paste unnecessary full logs.

Do not include secrets.

## SELF-CONTAINED ZIP RULE

The final user receives only:

1. One self-contained ZIP.
2. One installation PowerShell block in the response.

Do not require the user to download a second runner file.

Do not depend on files outside the ZIP except:

- the real Project root;
- its Python environment;
- its official ZIP validator;
- its Error Memory owner manifest and folders.

## EXTERNAL INSTALLATION BLOCK

After building the ZIP, provide one complete PowerShell block.

The block must:

1. Use the real ProjectRoot.
2. Derive the drive root from ProjectRoot.
3. Expect the downloaded ZIP at the drive root.
4. Verify the final SHA-256.
5. Create a UTC-stamped staging folder under the Project daily-work root.
6. Copy the ZIP into that folder.
7. Verify the staged copy's SHA-256.
8. Delete the root-drive ZIP copy only after successful staging and hash verification.
9. Extract only from the staged ZIP.
10. Locate the packaged `RUN_INSTALL.ps1`.
11. Execute it with:
    -ProjectRoot
    -PackageZip
12. Stop on any nonzero exit.
13. On success, print:

ERROR MEMORY INTAKE INSTALLATION: PASS
PROJECT SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO

14. On successful installation:
    - wait approximately two seconds;
    - run `Clear-Host`;
    - do not prompt for Enter.

15. On error:
    - show the error;
    - request Enter;
    - request Enter again;
    - run one final `Clear-Host`;
    - keep the terminal open.

Avoid fragile multiline escaping and excessive PowerShell backticks.

The block must be safe to copy and paste without leaving PowerShell in continuation mode.

## IDEMPOTENCE

Re-running the loader must be safe.

Required behavior:

- already memorized lessons are not overwritten;
- identical pending lessons are not rewritten;
- stale differing pending lessons are preserved with `.invalid_do_not_scan`;
- no duplicate canonical lesson is created;
- no duplicate lesson ID is admitted;
- the loader always writes a new execution receipt;
- canonical lesson write count remains zero.

## FREEZE COMPANION BRIDGE

The canonical lifecycle bridge is `KPR-05-005 patch_validate_freeze_error_memory_routine_blueprint`.
The companion Freeze loader owner is `KPR-03-007 self_contained_freeze_entry_intake_zip`.

This prompt owns only the Error Memory lesson intake ZIP. It must never add Freeze files, write Freeze intake, execute Preview, or execute Confirm and Write.

After Error Memory disposition is resolved, report exactly one:

- `ERROR MEMORY DISPOSITION: STAGED_FOR_HUMAN_APPROVAL`
- `ERROR MEMORY DISPOSITION: ALREADY_COMPLETE`
- `ERROR MEMORY DISPOSITION: NOT_REQUIRED`
- `ERROR MEMORY DISPOSITION: BLOCKED`

Also report exactly one companion state:

- `FREEZE COMPANION DISPOSITION: REQUIRED`
- `FREEZE COMPANION DISPOSITION: ALREADY_COMPLETE`
- `FREEZE COMPANION DISPOSITION: NOT_ELIGIBLE`
- `FREEZE COMPANION DISPOSITION: BLOCKED`

When the current feature is locally validated, synchronized, and eligible for Freeze but Freeze intake is not complete, the next exact owner is `KPR-03-007`. Pass the same selected-Project identity, Tool root, feature identity, exact patch identity, focused validator, and current validation evidence. Do not make the user re-enter those values.

Do not merge the Error Memory ZIP and Freeze ZIP. They remain separate artifacts, separate pending intakes, separate owner Boxes, and separate human approval actions.

## FINAL PACKAGE VALIDATION

Before delivering:

1. Rebuild the final ZIP.
2. Reopen it.
3. Verify the exact archive-member set.
4. Verify no duplicate members.
5. Verify no parent directory.
6. Verify no traversal or absolute members.
7. Parse `PACKAGE_MANIFEST.json`.
8. Validate every declared member hash.
9. Parse every lesson file.
10. Confirm exact markers.
11. Confirm every lesson is active-ready.
12. Confirm every lesson belongs to the current Project.
13. Confirm every lesson ID is unique.
14. Confirm prevention triggers and validation evidence are non-empty arrays.
15. Confirm redaction is applied and export-safe.
16. Confirm no source payload exists.
17. Confirm no canonical Error Memory path is written by any script.
18. Confirm no script calls `Memorize Error`.
19. Confirm `RUN_INSTALL.ps1` is present at the archive root.
20. Confirm the package is accepted by the official ZIP validator.
21. Perform a safe fixture or sandbox staging test.
22. Confirm the fixture produces pending lessons and zero canonical lessons.
23. Perform an idempotent second run.
24. Confirm identical lessons are reported as already staged.
25. Calculate SHA-256 only after the final ZIP is complete.

## REQUIRED SUCCESS MARKERS

The validated package should produce markers including:

ZIP CONTRACT: PASS
SELF-CONTAINED RUNNER MEMBER: PASS
ERROR MEMORY LOADER EXACT MEMBER SET: PASS
ERROR MEMORY LESSON ACTIVE-READY SCHEMA: PASS
ERROR MEMORY CANONICAL WRITE PATH: ABSENT
ERROR MEMORY HUMAN MEMORIZE GATE: PASS
ERROR MEMORY LOADER VALIDATION: PASS
ERROR MEMORY INTAKE VALIDATION: PASS
ERROR MEMORY OWNER IDENTITY: PASS
ERROR MEMORY TAB APPROVAL READY: PASS
PROJECT SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
ERROR MEMORY LESSON LOADER: PASS

## REQUIRED FINAL RESPONSE

Return:

1. A download link to the single ZIP.
2. The exact ZIP filename.
3. The final SHA-256.
4. A concise explanation of the included lessons.
5. Confirmation that Project source files are not modified.
6. Confirmation that canonical Error Memory Lessons are not written.
7. Confirmation that Memorize Error remains human-only.
8. One complete PowerShell installation block.
9. The expected final markers.
10. The Error Memory disposition and Freeze companion disposition.
11. The human approval workflow:

KANDA Reasoner
-> select the correct Project
-> Error Memory
-> review the automatically loaded pending lesson
-> click Memorize Error only after approval
-> repeat for the remaining pending lessons

Do not provide separate lesson ZIPs.

Do not provide a separate runner download.

Do not provide only JSON.

Create the functional, self-contained ZIP in the current response.
