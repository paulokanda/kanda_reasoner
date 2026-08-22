---
prompt_code: KPR-05-008
prompt_id: self_contained_error_memory_lesson_intake_zip
title: Self-Contained Error Memory Lesson Intake ZIP
version: 3.1
status: active
load_type: on_request
owner_box: 05_patch_delivery_and_validation
source_stage: error-memory-library-intake-v3
---

# MASTER PROMPT - CREATE A SELF-CONTAINED ERROR MEMORY LESSON INTAKE ZIP

## Purpose

Create one self-contained ZIP that stages one or more validated Error Memory
lessons as `pending` entries for human review in a source/IDE Tool environment
where an independent external Tool Python executable has been explicitly
verified.

This is an Error Memory lesson-library workflow. It is not the Architecture
Review Machine-Card/MCard lifecycle.

Never use `architecture_review_project_card_machine_canon` as the Error Memory
storage or lesson-lifecycle owner.

## Hard Portable/PyInstaller gate

This executable intake-ZIP workflow is not a Portable/FROZEN runtime contract.

A PyInstaller package may embed CPython and the KANDA modules without exposing a
standalone interpreter executable. Never infer Tool Python from `_internal` and
never search for or assume these paths:

```text
_internal/python.exe
_internal/.venv/Scripts/python.exe
_internal/venv/Scripts/python.exe
```

Before packaging or executing this workflow, determine the Tool runtime mode and
verify a real external Tool Python executable independently of the frozen app.

If the Tool is frozen/PyInstaller, or no independent external Tool Python can be
verified, stop this ZIP workflow and return:

```text
ERROR MEMORY EXECUTABLE ZIP INTAKE NOT AVAILABLE
Runtime mode: PORTABLE/FROZEN or external Tool Python unavailable
TOOL_PYTHON verified: NO
May create executable intake ZIP: NO
Corrected intake method:
marker-wrapped Error Memory lesson
-> existing Error Memory GUI intake
-> normalized to draft
-> human Memorize Error gate
Python required: NO
Direct Error Memory filesystem write: NO
Memorize Error automatically executed: NO
Next required phase: ERROR MEMORY GUI INTAKE
```

In that state, return the marker-wrapped lesson text needed by the native GUI
instead of a self-contained execution ZIP.

A passive lesson ZIP imported by the already-running Error Memory GUI is a
different in-app file-import path and does not authorize this executable loader
workflow.

## Semantic boundary

```text
Error Memory
= reusable library of failure-prevention lessons

MCard / Machine Card
= separate Tool/Project or Architecture Review lifecycle concern
```

KANDA self-hosting may make Tool and selected-Project roots physically equal,
but logical Tool/Project roles remain separate. That fact does not make an Error
Memory lesson into an MCard.

Historical source may expose names such as `error_memory_card` or `_mcard_*`.
Treat those as compatibility implementation names only. Do not require a
`card_id`, Project-card identity, CARD_INSERTED/CARD_EJECTED lifecycle, or KPR-12-005
to package Error Memory lessons.

## Exact objective

After the hard runtime gate passes, the final self-contained ZIP must:

1. contain every justified new lesson from the current work;
2. stage new candidates as `status: pending`;
3. use `intended_status: active` only when active-ready evidence exists;
4. use `intended_status: draft` when review is still needed;
5. validate lesson IDs, fingerprints, evidence, redaction, and current runtime
   compatibility;
6. preflight the current Error Memory lesson library before any staging write;
7. add only unique lessons;
8. skip exact or semantic duplicates;
9. fail closed on same-ID or incompatible fingerprint conflicts;
10. never overwrite existing active, pending, draft, or retired lessons;
11. never call, imitate, or press `Memorize Error`;
12. never create a new active lesson automatically;
13. never modify Active Project selection or Project registry state merely to
    stage Error Memory lessons;
14. never modify Project source;
15. never modify Freeze Memory;
16. support safe idempotent re-execution;
17. include one packaged execution entry point named `RUN_INSTALL.ps1`;
18. require only one externally supplied ZIP and one external PowerShell block.

## Runtime discovery

Before creating the ZIP, determine from current source or runtime evidence:

```text
TOOL_ROOT
TOOL_DRIVE_ROOT
TOOL_RUNTIME_MODE
TOOL_PYTHON
ERROR_MEMORY_LIBRARY_RUNTIME
ERROR_MEMORY_LIBRARY_LOCATION_OR_RESOLVER
PACKAGE_STAGING_ROOT
```

`TOOL_PYTHON` must be a real, independently executable interpreter owned by the
source/IDE Tool environment. It must not be synthesized from a frozen executable
layout, `sys._MEIPASS`, `_internal`, or guessed virtual-environment paths.

Do not invent a storage path or an interpreter path.

Use the current installed Error Memory public behavior as authority. If the
current implementation still exposes compatibility modules under
`kanda_reasoner_app.error_memory_card`, they may be used only as the installed
lesson-storage implementation. Their historical name does not authorize MCard
semantics and does not create a `card_id` admission requirement.

If current runtime compatibility or external Tool Python ownership cannot be
established, fail closed before packaging or staging and use the native
marker-wrapped GUI intake path instead.

## Lesson admission

Create one lesson for each distinct demonstrated reusable failure class.

Before packaging:

1. inspect the real failure output;
2. inspect exact affected current source or runtime evidence;
3. inspect relevant current Error Memory lessons when duplicate checking needs
   them;
4. compare stable lesson ID, fingerprint, symptom, root cause, correct fix, and
   prevention rule;
5. decide:
   - `NEW_PENDING_LESSON`;
   - `DUPLICATE_DO_NOT_CREATE`;
   - `CONFLICT_REQUIRES_HUMAN_REVIEW`;
   - `TRANSIENT_DO_NOT_MEMORIZE`;
   - explicitly authorized draft edit outside automatic new-lesson staging.

Do not package an automatic replacement for an existing lesson.

## Lesson lifecycle

Canonical lesson lifecycle states are:

```text
pending
active
draft
retired
```

A new active-ready candidate is transported as:

```json
{
  "status": "pending",
  "intended_status": "active"
}
```

An incomplete candidate is transported as:

```json
{
  "status": "pending",
  "intended_status": "draft"
}
```

Only explicit human `Memorize Error` may promote a pending lesson.

## Lesson transport format

Create one file per packaged lesson:

```text
KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
```

Each file contains exactly:

```text
KANDA_ERROR_LESSON_JSON_BEGIN

{
  "...": "..."
}

KANDA_ERROR_LESSON_JSON_END
```

Rules:

- markers each appear exactly once;
- begin marker is first non-whitespace content;
- end marker is last non-whitespace content;
- JSON between markers is valid;
- no Markdown fence or prose outside markers;
- UTF-8 without BOM;
- newline `\n`;
- no comments or trailing commas.

## Required lesson fields

Every packaged lesson contains:

```text
schema_version
lesson_id
status
intended_status
origin
applicability
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

Required:

```text
schema_version = "1.0"
status = "pending"
intended_status = "active" or "draft"
```

Do not invent lesson ownership fields solely from Tool/Project selection.

## Package structure

The ZIP has no enclosing parent directory.

Mandatory root members:

```text
CAPTURED_ERROR_MEMORY_EVIDENCE.txt
ERROR_MEMORY_LESSON_LIBRARY_LOADER.py
INSTALL.ps1
PACKAGE_MANIFEST.json
PREPARE_ERROR_MEMORY.ps1
README.txt
RUN_INSTALL.ps1
VALIDATE.ps1
VALIDATE_PACKAGE.py
```

Plus one lesson file per lesson:

```text
KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
```

No other members are permitted.

Do not include Tool/Project source payloads, backups, cache files, nested ZIPs,
Freeze hints, canonical Error Memory library data, owner manifests, or external
runner scripts.

## Package naming

Use:

```text
kanda_reasoner_<feature_or_workflow_slug>_error_memory_lesson_intake_v1.zip
```

For a corrected loader, increment only the loader revision.

## PACKAGE_MANIFEST.json

Required fields:

```text
schema_version
kind
feature_id
package_name
lesson_ids
exact_members
member_sha256
tool_authority
active_project_authority
lesson_write_mode
self_contained_runner
source_files_modified
project_source_files_modified
active_lessons_created
human_memorize_required
```

Required values:

```text
schema_version = "1.0"
kind = "kanda_error_memory_lesson_intake_loader"
tool_authority = true
active_project_authority = false
lesson_write_mode = "pending_unique_only"
self_contained_runner = "RUN_INSTALL.ps1"
source_files_modified = false
project_source_files_modified = false
active_lessons_created = false
human_memorize_required = true
```

## VALIDATE_PACKAGE.py

Validate the final ZIP itself. Require:

1. exact ZIP filename;
2. exact safe member set;
3. no duplicate, absolute, drive, UNC, traversal, directory, or nested ZIP member;
4. manifest kind and fields;
5. lesson IDs exactly match lesson files;
6. declared member hashes match;
7. exact marker contract and valid lesson JSON;
8. every new lesson is pending;
9. every intended status is active or draft;
10. unique lesson IDs;
11. non-empty prevention triggers and validation evidence;
12. redaction applied and export-safe;
13. active-ready core fields when intended active;
14. no Tool/Project source payload;
15. no canonical Error Memory library payload;
16. root `RUN_INSTALL.ps1`;
17. no script calls `Memorize Error` or `memorize_card_lesson`.

Success markers:

```text
ERROR MEMORY LESSON INTAKE EXACT MEMBER SET: PASS
ERROR MEMORY PENDING LESSON SCHEMA: PASS
ERROR MEMORY MACHINE-CARD SEMANTICS: ABSENT
ERROR MEMORY HUMAN MEMORIZE GATE: PASS
ERROR MEMORY CANONICAL LIBRARY PAYLOAD IN ZIP: ABSENT
ERROR MEMORY LESSON INTAKE PACKAGE VALIDATION: PASS
```

## ERROR_MEMORY_LESSON_LIBRARY_LOADER.py

Support validation-only mode and `--stage`.

Required arguments:

```text
--tool-root
--package-root
--package-zip
```

Optional:

```text
--stage
```

Use current installed Error Memory lesson interfaces. The loader must discover
and validate the runtime instead of assuming one historical module layout.

Compatibility rule:

- a current public API under `kanda_reasoner_app.error_memory` is preferred;
- if the installed version still exposes required lesson operations only through
  `kanda_reasoner_app.error_memory_card`, that backend may be used as a legacy
  compatibility implementation;
- regardless of module name, do not require `card_id` and do not treat Error
  Memory as MCard.

Required operations are the semantic equivalents of:

```text
read current lessons
normalize candidate lesson
find duplicate/conflict
save one pending lesson
re-read and verify lesson status
```

Validation-only mode must not modify canonical lesson data.

## Preflight before staging

For every candidate:

- same lesson ID with different material content -> conflict, fail closed;
- identical existing pending lesson -> `already_staged`;
- equivalent active lesson -> `already_memorized`;
- retired same-ID lesson -> conflict; never reactivate automatically;
- same prevention fingerprint and semantic contract -> duplicate, do not add;
- incompatible fingerprint reuse -> conflict;
- otherwise -> unique candidate.

If any true conflict exists, stage nothing in that execution.

## Staging mode

On `--stage`:

1. perform complete duplicate/conflict preflight;
2. add only unique candidates as `pending`;
3. never alter an existing lesson;
4. re-read current Error Memory lessons;
5. require every newly added lesson still pending;
6. require zero newly created active lessons;
7. never call `Memorize Error`.

Do not create or mutate Project source, Freeze Memory, or Active Project
selection.

## Intake receipt

Write under package-local receipts:

```text
<package_root>/receipts/<UTC timestamp>/intake_receipt.json
```

Include:

```text
artifact_type
schema_version
tool_root
library_runtime
package_zip
created_at_utc
active_project_authority_used
lessons
pending_lessons_staged
existing_lessons_modified
active_lessons_created
memorize_error_executed
project_source_files_modified
```

Required:

```text
active_project_authority_used = false
existing_lessons_modified = 0
active_lessons_created = 0
memorize_error_executed = false
project_source_files_modified = 0
```

## Final staging markers

Print:

```text
ERROR MEMORY LESSON LIBRARY RUNTIME: PASS
ERROR MEMORY MACHINE-CARD AUTHORITY: ABSENT
ERROR MEMORY PENDING LESSONS STAGED: <count>
ERROR MEMORY EXISTING LESSONS MODIFIED: 0
ERROR MEMORY ACTIVE LESSONS CREATED: 0
MEMORIZE ERROR EXECUTED: NO
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY INTAKE RECEIPT: <path>
ERROR MEMORY TAB APPROVAL READY: PASS
```

## VALIDATE.ps1

Accept `-ToolRoot` and `-PackageZip`.

Resolve Python through the Tool environment, keeping executable and prefix
arguments separate.

Run:

1. `VALIDATE_PACKAGE.py`;
2. official Tool ZIP validator `<TOOL_ROOT>/scripts/validate_patch_zip.py`;
3. require `ZIP CONTRACT: PASS`;
4. `ERROR_MEMORY_LESSON_LIBRARY_LOADER.py` in validation-only mode.

Fail on any nonzero command.

Do not use inline `python -c`.

## PREPARE_ERROR_MEMORY.ps1

Run `VALIDATE.ps1`, require all validation markers, then run the lesson-library
loader with `--stage`.

On success print:

```text
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY EXISTING LESSONS MODIFIED: 0
ERROR MEMORY ACTIVE LESSONS CREATED: 0
MEMORIZE ERROR EXECUTED: NO
ERROR MEMORY LESSON INTAKE PREPARATION COMPLETE
```

## INSTALL.ps1 and RUN_INSTALL.ps1

The package entry point is `RUN_INSTALL.ps1`.

It invokes the packaged preparation workflow only. It must not install
Tool/Project source, change Active Project, change Freeze Memory, or execute
`Memorize Error`.

Success markers:

```text
ERROR MEMORY LESSON INTAKE LOADER: PASS
PROJECT SOURCE FILES MODIFIED: 0
ERROR MEMORY EXISTING LESSONS MODIFIED: 0
ERROR MEMORY ACTIVE LESSONS CREATED: 0
MEMORIZE ERROR EXECUTED: NO
OPEN ERROR MEMORY FOR HUMAN APPROVAL
```

## Idempotence

Re-running is safe:

- identical pending lesson is not rewritten;
- equivalent active lesson is not restaged;
- retired same-ID lesson is not automatically reactivated;
- fingerprint duplicate is not added;
- conflicts fail before writes;
- no existing lesson is replaced;
- each execution may write a new receipt;
- zero active lessons are created automatically.

## Freeze separation

Error Memory intake and Freeze intake are separate workflows and separate human
approval actions.

This prompt never creates Freeze files, writes Freeze intake, executes Freeze
Preview, or executes Confirm and Write.

## Required final response

If the hard Portable/PyInstaller gate blocks executable ZIP intake, do not return
a ZIP or PowerShell runner. Return the marker-wrapped Error Memory lesson and the
native GUI approval route:

```text
KANDA Reasoner
-> Error Memory
-> Paste error formatted from AI
-> review Draft
-> click Memorize Error only after approval
```

If the hard runtime gate passes in source/IDE mode, return:

1. one ZIP download link;
2. exact ZIP filename and SHA-256;
3. concise lesson summary;
4. confirmation Project source is not modified;
5. confirmation existing lessons are not overwritten;
6. confirmation staged lessons remain pending;
7. confirmation Machine-Card/MCard semantics are not used;
8. confirmation `Memorize Error` remains human-only;
9. one complete PowerShell installation block;
10. expected final markers;
11. Error Memory disposition;
12. Freeze companion disposition;
13. human approval workflow:

```text
KANDA Reasoner
-> Error Memory
-> To memorize
-> review one pending lesson
-> click Memorize Error only after approval
```
