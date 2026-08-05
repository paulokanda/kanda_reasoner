MASTER PROMPT - CREATE A SELF-CONTAINED ERROR MEMORY LESSON INTAKE ZIP FOR THE CURRENT PROJECT

You are working inside KANDA Reasoner with a currently selected active Project.

Your task is to review the completed work, identify reusable Error Memory lessons, and create one self-contained ZIP that stages those lessons in the selected Project's Error Memory pending-intake area for human review.

This prompt must work with any Project registered and selected in KANDA Reasoner.

Do not assume the Project is KANDA Reasoner.

Do not assume the Project is EEG Kanda.

Do not assume the Project root, support root, transient root, drive letter, Project slug, owner identity, Error Memory root, or validator paths.

Discover all Project-specific values from the current selected-Project context.

CORE RESULT

Create exactly one self-contained ZIP containing:

* all Error Memory lesson records;
* all validation code;
* all pending-intake staging code;
* all required PowerShell scripts;
* the package manifest;
* the captured evidence summary;
* one packaged execution entry point named RUN_INSTALL.ps1.

Do not create separate lesson ZIPs.

Do not require a separate downloadable runner.

After creating the ZIP, provide:

1. One download link to the ZIP.
2. The exact filename.
3. The final SHA-256.
4. One complete PowerShell installation block.
5. The expected success markers.
6. The human approval workflow inside Error Memory.

The loader must stage lessons for approval only.

It must never:

* write directly into canonical Error Memory lessons;
* invoke or simulate Memorize Error;
* modify Project source code;
* modify Freeze Memory;
* modify Project selection;
* modify the Tool registry;
* build the Project;
* run unrelated Project operations.

CURRENT PROJECT DISCOVERY

Before creating any artifact, discover the currently selected Project through the available KANDA Reasoner context.

Use the current handoff, selected-Project registry state, Project owner manifests, source archive, user-provided paths, or current Project evidence.

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

PROJECT_ROOT: <parent><project_name>

PROJECT_SUPPORT_ROOT: <parent><project_name>_show_project_to_AI

PROJECT_DAILY_WORK_ROOT: <parent><project_name>_delete_after_daily_work

PROJECT_ERROR_MEMORY_ROOT:
<PROJECT_SUPPORT_ROOT>\project_error_memory

PROJECT_ERROR_MEMORY_OWNER_MANIFEST:
<PROJECT_ERROR_MEMORY_ROOT>\owner_manifest.json

PENDING_INTAKE_ROOT:
<PROJECT_ERROR_MEMORY_ROOT>\pending_ai_assisted_error_lesson_intake

CANONICAL_LESSONS_ROOT:
<PROJECT_ERROR_MEMORY_ROOT>\lessons

These are expected patterns only.

Validate the actual paths and ownership before using them.

Do not construct paths only by string convention when canonical registry or owner-manifest evidence is available.

CURRENT PROJECT OWNERSHIP

The currently selected active Project is the owner of the new Error Memory lessons.

All lesson records must use:

project_slug:
the actual current Project slug

owner identity:
the current Project Error Memory owner

pending intake:
the current Project's pending-intake directory

canonical lesson checks:
the current Project's canonical Error Memory lessons directory

Another Project may appear in validation evidence only when it was genuinely used as an external fixture, integration target, or ownership-reuse test.

An external fixture must never become:

* the lesson owner;
* the Project slug;
* the Error Memory root;
* the pending-intake root;
* the canonical lessons root;
* the owner manifest;
* the Project source owner;
* the primary Box owner.

ANTI-CROSS-PROJECT RULE

Before staging anything, verify that:

1. PROJECT_ROOT belongs to the selected Project.
2. PROJECT_SUPPORT_ROOT belongs to the selected Project.
3. PROJECT_ERROR_MEMORY_ROOT belongs to the selected Project.
4. owner_manifest.json identifies the selected Project.
5. every lesson project_slug matches the selected Project.
6. no pending lesson is written under another Project's support root.
7. no canonical lesson from another Project is inspected as the selected Project's canonical lesson.

Fail closed when Project ownership is ambiguous or inconsistent.

LESSON SELECTION

Create one lesson for each distinct demonstrated and reusable failure class.

A lesson is appropriate when the completed work reveals a reusable prevention rule involving:

* a wrong assumption;
* a missing validation gate;
* an ownership violation;
* a lifecycle misunderstanding;
* a packaging or manifest error;
* a stale authority source;
* a false-positive validation result;
* an unsafe fallback;
* a rollback deficiency;
* an import or execution-context defect;
* a repeatable source of regression.

Do not create a lesson merely because a command failed.

Do not create lessons for:

* user typing mistakes;
* cancelled operations;
* temporary network failures unrelated to the implementation;
* errors already fully covered by an existing current lesson;
* speculative risks without demonstrated evidence;
* failures caused only by an intentionally unsupported environment.

Before creating lessons:

1. Read Compact Error Memory for the selected Project.
2. Open Full Error Memory only when repeated-error debugging, conflict resolution, or insufficient compact context requires it.
3. Search existing active, draft, deprecated, and superseded lessons.
4. Compare root cause, wrong assumption, fingerprint, prevention rule, affected Box, and regression obligation.
5. Decide whether the issue requires:

   * a new lesson;
   * an update to an existing draft;
   * reinterpretation of an existing current lesson;
   * no new lesson.

Do not create duplicate lessons under different names.

LESSON SEPARATION

Create separate lessons when failures differ materially in:

* root cause;
* wrong assumption;
* operational phase;
* affected Box;
* canonical owner;
* required correction;
* long-term prevention;
* regression validator;
* rejection condition.

Combine multiple symptoms into one lesson when they came from the same underlying defect and require the same prevention rule.

REAL EVIDENCE ONLY

Every lesson must be derived from real current evidence.

Acceptable evidence includes:

* tracebacks;
* exception messages;
* validator output;
* rejected validation markers;
* successful validation markers;
* source inspection;
* manifest inspection;
* Project ownership records;
* package-member inspection;
* transactional rollback output;
* final build or runtime evidence;
* GUI smoke evidence;
* exact function names;
* exact Project-relative file paths;
* exact validator paths;
* exact feature IDs;
* exact artifact hashes.

Do not invent:

* root causes;
* source filenames;
* function names;
* validator names;
* success markers;
* rejection markers;
* feature IDs;
* artifact hashes;
* Project identities;
* freeze IDs;
* timestamps;
* completed corrections.

When a detail cannot be verified, mark it unresolved or omit it where the schema permits.

LESSON TRANSPORT FORMAT

Create one lesson file for every lesson.

Filename:

KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt

Each lesson file must have this exact structure:

KANDA_ERROR_LESSON_JSON_BEGIN

{
"schema_version": "1.0"
}

KANDA_ERROR_LESSON_JSON_END

Requirements:

* The beginning marker appears exactly once.
* The ending marker appears exactly once.
* The beginning marker is the first non-whitespace content.
* The ending marker is the last non-whitespace content.
* The content between markers is valid JSON.
* No Markdown fences.
* No prose outside the markers.
* UTF-8 without BOM.
* Standard LF newlines.
* Double-quoted JSON strings.
* No comments.
* No trailing commas.
* Prefer ASCII-escaped JSON output.

REQUIRED LESSON FIELDS

Each completed lesson must contain:

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
the actual selected Project slug

prevention_triggers:
a non-empty JSON array of strings

validation_evidence:
a non-empty JSON array of strings

Do not encode arrays as multiline strings.

LESSON ID

Use:

lesson-<specific-reusable-failure-class>-v1

A lesson ID must describe the reusable defect, not only the feature, ticket, patch, or date.

Examples:

lesson-validator-project-package-import-bootstrap-v1
lesson-private-settings-duplicate-project-authority-v1
lesson-generated-artifact-treated-as-source-authority-v1
lesson-runtime-manifest-membership-assumption-v1
lesson-gui-smoke-false-positive-runtime-report-gap-v1

Lesson IDs must be:

* unique inside the package;
* stable;
* descriptive;
* independent of transient timestamps;
* specific enough to avoid collisions.

EXCEPTION OBJECT

The exception object must include:

type
phase
relative_file_path
function_or_test_name
message_normalized
stacktrace_scrubbed

Use Project-relative paths when the affected file belongs to the selected Project.

Absolute paths may be retained only inside scrubbed evidence when required to understand the failure, and must not expose secrets or unrelated personal profile information.

FINGERPRINT OBJECT

The fingerprint object must contain:

strategy
components
fingerprint_hash

Required:

strategy:
"v1_structural_conservative"

components:
a non-empty array of stable structural characteristics

fingerprint_hash:
a deterministic SHA-256 generated from normalized fingerprint components

The fingerprint must describe the failure class, not the machine, timestamp, temporary folder, or user account.

REGRESSION CHECK

The regression_check object must contain:

type
command
expected_marker
required_before_freeze

Use the actual focused validator when one exists.

When no regression validator exists, use an explicit unavailable representation rather than inventing a command.

Do not use a historical validation marker as proof of current validation.

REDACTION

The redaction object must contain:

applied
export_safe
rules

Required:

applied:
true

export_safe:
true

rules:
a JSON array

Remove or scrub:

* API keys;
* access tokens;
* credentials;
* private provider settings;
* unrelated personal profile paths;
* secrets;
* sensitive unrelated content.

Do not remove technical facts needed to understand the failure.

SELF-CONTAINED ZIP STRUCTURE

The ZIP must contain all files directly at the archive root.

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

Dynamic lesson members:

KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt

Do not include an enclosing parent directory.

Do not include:

* Project source payloads;
* source patches;
* nested ZIPs;
* Freeze hints;
* canonical lesson files copied from Error Memory;
* owner manifests copied from Project Support;
* backups;
* cache files;
* `.pyc`;
* `__pycache__`;
* temporary extraction files;
* a separate external runner.

PACKAGE NAME

Use:

<project_slug>_<feature_or_workflow_slug>_error_memory_intake_loader_v1.zip

Corrected loader revisions must increment the loader version:

v1r1
v2
v3

Do not silently replace an earlier ZIP while advertising its old SHA-256.

PACKAGE_MANIFEST.JSON

The manifest must contain:

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

lesson_ids:
every packaged lesson ID exactly once

exact_members:
the exact final ZIP member set

member_sha256:
hashes of every archive member except PACKAGE_MANIFEST.json itself

Do not recursively hash the manifest into itself.

VALIDATE_PACKAGE.PY

Create an internal validator for the finished ZIP.

It must validate:

1. ZIP filename matches package_name.
2. Exact archive-member set.
3. No duplicate members.
4. No directory members.
5. No enclosing parent directory.
6. No absolute archive paths.
7. No drive-letter archive paths.
8. No UNC paths.
9. No leading slash or backslash.
10. No `..` traversal components.
11. PACKAGE_MANIFEST.json parses.
12. Manifest kind is correct.
13. Manifest Project slug matches the package.
14. Manifest lesson IDs exactly match lesson files.
15. Manifest exact_members exactly match the ZIP.
16. Every declared member SHA-256 matches.
17. Every lesson marker contract is exact.
18. Every lesson payload parses as JSON.
19. Every lesson has all required top-level fields.
20. Every lesson status is active.
21. Every lesson Project slug matches the package Project slug.
22. Lesson IDs are unique.
23. prevention_triggers is a non-empty array.
24. validation_evidence is a non-empty array.
25. redaction.applied is true.
26. redaction.export_safe is true.
27. No source-code payload exists.
28. No canonical Error Memory lesson path exists.
29. No script invokes or simulates Memorize Error.
30. RUN_INSTALL.ps1 exists at the archive root.

Print on success:

SELF-CONTAINED RUNNER MEMBER: PASS
ERROR MEMORY LOADER EXACT MEMBER SET: PASS
ERROR MEMORY LESSON ACTIVE-READY SCHEMA: PASS
ERROR MEMORY CANONICAL WRITE PATH: ABSENT
ERROR MEMORY HUMAN MEMORIZE GATE: PASS
ERROR MEMORY LOADER VALIDATION: PASS

ERROR_MEMORY_LOADER.PY

The loader must support:

validation-only mode

and:

--stage

Required arguments:

--project-root
--package-root
--package-zip

Optional flag:

--stage

PROJECT OWNERSHIP PREFLIGHT

Resolve and validate:

* selected Project root;
* Project slug;
* Project support root;
* Project Error Memory root;
* Project Error Memory owner manifest;
* pending-intake root;
* canonical lessons root.

Require that owner_manifest.json belongs to the selected Project.

Fail on:

* missing owner manifest;
* malformed owner manifest;
* Project slug mismatch;
* owner ID mismatch;
* Project root mismatch;
* support-root mismatch;
* another Project's Error Memory root;
* unresolved selected Project identity.

VALIDATION-ONLY MODE

Validation-only mode must:

1. Verify current Project ownership.
2. Validate every lesson.
3. Confirm every lesson belongs to the selected Project.
4. Confirm the pending-intake path.
5. Confirm canonical lessons will not be written.
6. Confirm Memorize Error will not be executed.
7. Confirm source files will not be modified.

Print:

ERROR MEMORY OWNER IDENTITY: PASS
ERROR MEMORY PROJECT SUPPORT ROOT: <actual path>
ERROR MEMORY DAILY WORK ROOT: <actual path>
ERROR MEMORY ACTIVE-READY LESSON COUNT: <count>
ERROR MEMORY CANONICAL LESSON WRITE: NO
MEMORIZE ERROR EXECUTED: NO
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY LOADER PROJECT PREFLIGHT: PASS

STAGING MODE

Stage lessons only under:

<PROJECT_ERROR_MEMORY_ROOT>\pending_ai_assisted_error_lesson_intake

For each lesson:

1. Determine the canonical path:

<CANONICAL_LESSONS_ROOT><lesson_id>.json

2. If the canonical lesson exists:

   * validate its internal lesson ID;
   * do not overwrite it;
   * do not restage it;
   * print:

LESSON ALREADY MEMORIZED - NOT RESTAGED: <lesson_id>

3. Determine the pending path:

<PENDING_INTAKE_ROOT><lesson_id>.json

4. If the pending file exists and is byte-identical:

   * do not rewrite it;
   * print:

LESSON ALREADY STAGED FOR APPROVAL: <lesson_id>

5. If the pending filename exists with different content:

   * preserve it as:

<filename>.replaced_<UTC timestamp>.invalid_do_not_scan

* atomically write the corrected lesson.

6. For new lessons:

   * write to a temporary file first;
   * use UTF-8 without BOM;
   * use LF newlines;
   * atomically replace the final pending file;
   * print:

LESSON STAGED FOR APPROVAL: <lesson_id>

Never write into the canonical lessons folder.

Never call the canonical lesson writer.

Never invoke Memorize Error.

Never modify Project source.

Never alter the Project registry.

INTAKE RECEIPT

Write an execution receipt under:

<PROJECT_DAILY_WORK_ROOT>\error_memory_intake_loader<UTC timestamp>\intake_receipt.json

The receipt must contain:

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

Each lesson receipt must contain:

lesson_id
action
pending_path
canonical_path

Allowed actions:

staged
already_staged
replaced_stale_pending
already_memorized

Required values:

canonical_lessons_written:
0

memorize_error_executed:
false

project_source_files_modified:
0

FINAL STAGING MARKERS

Print:

ERROR MEMORY OWNER IDENTITY: PASS
ERROR MEMORY PENDING INTAKE ROOT: <actual path>
ERROR MEMORY LESSONS AVAILABLE FOR APPROVAL: <count>
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY INTAKE RECEIPT: <actual path>
ERROR MEMORY TAB APPROVAL READY: PASS

VALIDATE.PS1

Accept:

-ProjectRoot
-PackageZip

It must:

1. Validate ProjectRoot.
2. Validate PackageZip.
3. Resolve Python in this order:

   * `<PROJECT_ROOT>\.venv\Scripts\python.exe`
   * `<PROJECT_ROOT>\venv\Scripts\python.exe`
   * `python.exe`
   * `py.exe -3`
4. Store the executable and optional prefix arguments separately.
5. Execute VALIDATE_PACKAGE.py.
6. Locate the KANDA governed ZIP validator applicable to the current Project.
7. Require:

ZIP CONTRACT: PASS

8. Execute ERROR_MEMORY_LOADER.py in validation-only mode.
9. Stop on any nonzero result.
10. Print:

ZIP CONTRACT: PASS
ERROR MEMORY INTAKE VALIDATION: PASS

Do not use inline `python -c`.

PREPARE_ERROR_MEMORY.PS1

Accept:

-ProjectRoot
-PackageZip

It must:

1. Execute VALIDATE.ps1.
2. Capture and display full validation output.
3. Stop if validation fails.
4. Require:

ZIP CONTRACT: PASS
ERROR MEMORY LOADER VALIDATION: PASS
ERROR MEMORY INTAKE VALIDATION: PASS

5. Resolve Python consistently.
6. Execute ERROR_MEMORY_LOADER.py with --stage.
7. Stop on failure.
8. Print:

ERROR MEMORY LOADER SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
ERROR MEMORY LESSON INTAKE PREPARATION COMPLETE

INSTALL.PS1

Accept:

-ProjectRoot
-PackageZip

It must invoke PREPARE_ERROR_MEMORY.ps1.

It must not:

* install source;
* modify source;
* run a Project build;
* run Freeze preparation;
* write canonical lessons.

On success, print:

ERROR MEMORY LOADER INSTALLATION OK: <feature_id>

RUN_INSTALL.PS1

This is the only packaged execution entry point.

Accept:

-ProjectRoot
-PackageZip

It must:

1. Validate ProjectRoot.
2. Validate PackageZip.
3. Invoke INSTALL.ps1.
4. Stop on any nonzero exit.
5. Print:

ERROR MEMORY LESSON LOADER: PASS
PROJECT SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO
OPEN ERROR MEMORY FOR HUMAN APPROVAL

README.TXT

Explain:

* the selected Project;
* the included lessons;
* the evidence behind each lesson;
* that lessons are staged only for review;
* that Project source is not modified;
* that canonical Error Memory is not written;
* that Memorize Error is human-only;
* where pending intake is stored;
* how to review each lesson in Error Memory.

CAPTURED_ERROR_MEMORY_EVIDENCE.TXT

Include a concise, scrubbed evidence summary:

* demonstrated failures;
* wrong assumptions;
* corrections;
* rollback evidence;
* focused validator evidence;
* final validation or runtime evidence;
* source files involved;
* current Project identity.

Do not include unnecessary full logs.

Do not include secrets.

SELF-CONTAINED DELIVERY

The user must receive only:

1. One self-contained ZIP.
2. One installation PowerShell block.

Do not provide:

* separate lesson ZIPs;
* a separate runner file;
* raw lesson JSON without the loader;
* instructions requiring manual file placement inside pending intake.

EXTERNAL INSTALLATION BLOCK

Provide one complete PowerShell block that:

1. Uses the actual current PROJECT_ROOT.
2. Derives the drive root.
3. Expects the downloaded ZIP at the drive root.
4. Verifies the final SHA-256.
5. Creates a UTC-stamped staging directory under PROJECT_DAILY_WORK_ROOT.
6. Copies the ZIP to staging.
7. Verifies the staged SHA-256.
8. Deletes the drive-root ZIP only after verified staging.
9. Extracts only from the staged ZIP.
10. Locates RUN_INSTALL.ps1 inside the extracted package.
11. Executes it with ProjectRoot and the staged PackageZip.
12. Stops on nonzero exit.
13. Prints on success:

ERROR MEMORY INTAKE INSTALLATION: PASS
PROJECT SOURCE FILES MODIFIED: 0
CANONICAL LESSONS WRITTEN: 0
MEMORIZE ERROR EXECUTED: NO

14. On success:

* wait approximately two seconds;
* execute Clear-Host;
* do not request Enter.

15. On error:

* show the error;
* request Enter;
* request Enter again;
* execute one final Clear-Host;
* keep the terminal open.

Avoid fragile PowerShell continuation syntax.

IDEMPOTENCE

The loader must be safely repeatable.

On repeated execution:

* memorized lessons are not overwritten;
* identical pending lessons are not rewritten;
* differing stale pending records are preserved with `.invalid_do_not_scan`;
* duplicate lesson IDs are rejected;
* canonical lesson writes remain zero;
* Memorize Error remains unexecuted;
* a new receipt is written for each run.

FINAL VALIDATION BEFORE DELIVERY

Before delivering the ZIP:

1. Rebuild the final archive.
2. Reopen it.
3. Confirm exact members.
4. Confirm no duplicate members.
5. Confirm no enclosing directory.
6. Confirm no traversal or absolute paths.
7. Parse PACKAGE_MANIFEST.json.
8. Validate member hashes.
9. Parse every lesson file.
10. Confirm exact markers.
11. Confirm every lesson is active-ready.
12. Confirm every lesson belongs to the current Project.
13. Confirm unique lesson IDs.
14. Confirm non-empty prevention triggers.
15. Confirm non-empty validation evidence.
16. Confirm redaction is applied and export-safe.
17. Confirm no source payload.
18. Confirm no canonical lesson writes.
19. Confirm no Memorize Error invocation.
20. Confirm RUN_INSTALL.ps1 is present.
21. Run the official ZIP contract validator.
22. Run a fixture staging test.
23. Confirm pending lesson creation.
24. Confirm canonical lesson count remains zero.
25. Run an idempotent second fixture execution.
26. Confirm already-staged behavior.
27. Calculate final SHA-256 only after the last rebuild.

REQUIRED PACKAGE MARKERS

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

FINAL RESPONSE FORMAT

Return:

1. Download link to the one ZIP.
2. Exact ZIP filename.
3. Final SHA-256.
4. Included lesson IDs and short descriptions.
5. Confirmation that source files are not modified.
6. Confirmation that canonical lessons are not written.
7. Confirmation that Memorize Error remains human-only.
8. One complete PowerShell installation block.
9. Expected final markers.
10. Human approval steps:

KANDA Reasoner
-> select the Project that owns the lessons
-> Error Memory
-> review the automatically loaded pending lesson
-> click Memorize Error only after approval
-> repeat for every remaining pending lesson

Do not provide separate lesson packages.

Do not create a separate runner download.

Do not hardcode KANDA Reasoner as the Project.

Create the complete self-contained ZIP in the current response.
