---
prompt_code: KPR-03-007
prompt_id: self_contained_freeze_entry_intake_zip
title: Self-Contained Freeze Entry Intake ZIP
version: 1.3
status: active
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: prompt-freeze-error-memory-lifecycle-alignment-v1
---

## Freeze-loader semantic boundary

This ZIP is a transport/intake artifact for one exact already validated feature
state. It must never turn Freeze into implementation, validation, patch execution,
or cumulative state synthesis.

`KANDA_FREEZE_HINT.json` is mandatory inside this Freeze-loader because this
artifact's purpose is Freeze intake. That requirement does not make Freeze Hint
mandatory for unrelated ordinary source-patch validity.

A loader must represent one exact effective feature/revision. Do not combine
multiple source patches or historical revisions into one cumulative Freeze loader
unless the human explicitly requested and approved a distinct cumulative/baseline
Freeze operation before package construction.

MASTER PROMPT — CREATE A ZIP THAT LOADS THE CURRENT FEATURE INTO “NEW LOCAL FREEZE ENTRY”

You are working with the currently selected active project in KANDA Reasoner.

Your task is to create a real, functional ZIP that loads the currently validated feature into:

Freeze Feature After Update
→ New Local Freeze Entry

Do not provide only the freeze-form text.

You must generate the actual ZIP, make it available for download, provide its final SHA-256, and provide one complete, robust PowerShell block to execute it.

CURRENT-PROJECT DISCOVERY

Before creating anything, determine the exact current project identity from the available project context, source files, handoff, selected-project state, or user-provided paths.

Resolve these values:

* PROJECT_ROOT
* PROJECT_NAME or PROJECT_SLUG
* PROJECT_SUPPORT_ROOT
* PROJECT_DAILY_WORK_ROOT
* FEATURE_ID
* FEATURE_TITLE
* PRIMARY_BOX
* FOCUSED_VALIDATOR
* FOCUSED_VALIDATOR_ROOT_ARGUMENT
* KANDA_REASONER_TOOL_ROOT, when Tool-owned helper fallback is required
* OFFICIAL_ZIP_VALIDATOR
* OFFICIAL_ZIP_VALIDATOR_OWNER
* FREEZE_EVIDENCE_MERGE_HELPER
* FREEZE_EVIDENCE_MERGE_HELPER_OWNER

OFFICIAL HELPER OWNERSHIP RESOLUTION

First resolve the official ZIP validator and freeze-evidence merge helper from the selected Project. If they are not Project-owned, resolve the canonical Tool-owned implementations from the KANDA Reasoner Tool root. Never copy, recreate, or assume these helpers under the Project root.

For each helper, record:

* exact resolved path;
* owner type: PROJECT or TOOL;
* owner root;
* source SHA-256;
* accepted command-line or import contract.

Fail closed if the canonical owner cannot be proven.

The selected Project remains the owner of the freeze entry even when a Tool-owned validator or merge helper performs governance work. Tool-owned helper execution must never transfer freeze ownership to the Tool.

Expected path relationships usually follow:

PROJECT_ROOT: <parent>/<project_name>

PROJECT_SUPPORT_ROOT: <parent>/<project_name>_show_project_to_AI

PROJECT_DAILY_WORK_ROOT: <parent>/<project_name>_delete_after_daily_work

Do not assume the project name is `kanda_reasoner`.

Do not assume the project root is `E:\kanda_reasoner`.

Do not reuse project-specific values from examples, previous chats, fixtures, test projects, or unrelated freeze entries.

Use the actual currently selected project.

EXACT OBJECTIVE

The ZIP must:

1. Represent only the feature that is currently validated.
2. Belong only to the currently selected active project.
3. Prepare the persistent intake used by New Local Freeze Entry.
4. Make the form appear correctly auto-filled.
5. Keep Preview Freeze Entry read-only.
6. Keep Confirm and Write as an explicit human action.
7. Never write the final frozen entry directly.
8. Never modify project source code.
9. Never use another project’s paths, identity, manifests, support roots, or ownership data in the current freeze.
10. Preserve real validation evidence without confusing external test fixtures with freeze ownership.

PROJECT OWNERSHIP RULES

The currently selected active project is the only owner of the freeze.

The project’s source files, generated files, protected paths, ownership identity, and memory destination must all correspond to that project.

Previous projects or examples may be used only to understand the freeze-loading mechanism.

They are never the source of freeze data for the current feature.

For the current project:

* validated_files must belong to the current project;
* generated_files must belong to the current project;
* protected_paths must belong to the current project;
* primary_box must belong to the current project;
* feature ownership must identify the current project;
* no path from another project may appear in path-bearing freeze fields.

MANDATORY PROJECT-RELATIVE PATHS

The following fields must contain only paths relative to PROJECT_ROOT:

* validated_files
* generated_files
* protected_paths
* primary_box, when it represents a file or module

Valid examples:

src/package/module.py
tools/validate_current_feature.py
portable
project_freeze_after_update/frozen_features_memory

Invalid examples:

E:/current_project/src/package/module.py
E:/another_project_show_project_to_AI/project_error_memory/owner_manifest.json
../another_project/file.py
/project/file.py
\server\share\file.py

Do not convert a path from another project into a fake relative path.

When a file does not belong to the project being frozen, it must not appear in:

* validated_files;
* generated_files;
* protected_paths;
* primary_box.

EXTERNAL FIXTURE EVIDENCE

Validation evidence may legitimately mention another project used as a smoke-test fixture, integration fixture, external-project test, or ownership-reuse test.

Examples:

EXTERNAL PROJECT STABLE ID REUSE: PASS
EXTERNAL PROJECT OWNER IDENTITY EXACT MATCH: PASS

Such lines may remain in validation_evidence_summary when they are real validation output.

However, names, roots, support roots, manifests, or files belonging to an external fixture must never become:

* protected_paths;
* validated_files;
* generated_files;
* primary_box;
* owner paths;
* freeze ownership;
* memory ownership.

Do not reject a freeze merely because validation evidence mentions an external fixture.

Validate external-project contamination precisely in path-bearing fields only.

MANDATORY ZIP STRUCTURE

The ZIP must contain these files directly at the archive root, with no enclosing parent directory:

CAPTURED_LOCAL_VALIDATION_EVIDENCE.txt
FREEZE.ps1
INSTALL.ps1
KANDA_FREEZE_FORM.txt
KANDA_FREEZE_HINT.json
PACKAGE_MANIFEST.json
PREPARE_FREEZE.ps1
README.txt
VALIDATE.ps1
VALIDATE_PACKAGE.py

Do not include a source-code payload.

This ZIP is a freeze loader, not a source-installation patch.

PACKAGE NAMING

Use a project- and feature-specific filename such as:

<project_slug>_<feature_slug>_freeze_loader_v1.zip

When correcting a defective loader, increment the loader version:

v2
v3
v4

Do not overwrite an earlier package while continuing to advertise its old SHA-256.

KANDA_FREEZE_HINT.JSON

KANDA_FREEZE_HINT.json must exist at the archive root and contain, at minimum:

```json
{
  "schema_version": "1.0",
  "kind": "kanda_freeze_hint",
  "patch_name": "<exact final ZIP filename>",
  "feature_id": "<real current feature ID>",
  "feature_title": "<exact current feature title>",
  "primary_box": "<project-relative owning box>",
  "box_type": "<box type>",
  "summary": "<short current-feature summary>",
  "validated_files": [],
  "generated_files": [],
  "protected_paths": [],
  "do_not_regress_rules": [],
  "validation_evidence_summary": [],
  "known_warnings": "<real warnings or n/a>",
  "planned_next_step": "<ONLY ACTION THAT REMAINS PENDING AFTER THE COMPLETE CURRENT CONFIRM AND WRITE TRANSACTION RETURNS>",
  "notes": "<current-project provenance and relevant notes>",
  "freeze_readiness": "locally_validated",
  "requires_user_validation": false,
  "preview_read_only": true,
  "confirm_and_write_human_required": true,
  "patch_provenance_required": false
}
```

The following fields must be real JSON arrays of strings:

* validated_files
* generated_files
* protected_paths
* do_not_regress_rules
* validation_evidence_summary

Never store those fields as one string that merely looks like a list.

Use double quotes.

Do not use comments.

Do not use trailing commas.

Do not include placeholders in the finished package.

KANDA_FREEZE_FORM.TXT

Before emitting or packaging the AI-authored local Freeze candidate/form, load and
apply `KPR-03-008 freeze_candidate_pre_output_audit`. The exact candidate must
pass its current-store duplicate/predecessor/supersession audit, exact feature and
revision evidence audit, release-owner provenance audit, path-owner/root audit,
strict 11-field JSON audit, complete Confirm and Write transaction simulation, and
second independent audit. If any mandatory gate is unresolved, fail closed with
`FREEZE CANDIDATE NOT READY`; do not package a partial candidate.

`planned_next_step` must remain genuinely pending after the complete current
Confirm and Write transaction has returned. It must not repeat Preview, Confirm
and Write, automatic hint consumption, startup/compliance refresh, indexing, or
another writer/GUI-owned action already completed by that transaction. If no
immediate human action remains, use a future durable trigger.

Also include one receive-ready Freeze form as exactly one canonical raw JSON object:

```json
{
  "feature_title": "...",
  "primary_box": "...",
  "box_type": "...",
  "validated_files": [],
  "generated_files": [],
  "protected_paths": [],
  "do_not_regress_rules": [],
  "validation_evidence_summary": [],
  "known_warnings": "...",
  "planned_next_step": "...",
  "notes": "..."
}
```

The form must match KANDA_FREEZE_HINT.json. The JSON object is the transport;
BEGIN/END markers and Markdown fences are not part of the receiver contract.
KANDA_FREEZE_FORM.txt must contain only the raw JSON object, with no prose.

VALIDATION_EVIDENCE_SUMMARY

Use only real markers obtained from local validation.

Do not invent:

STATUS: IN_SYNC
ZIP CONTRACT: PASS
VALIDATION OK

The completed local validation must produce, at minimum:

VALIDATION OK: <feature_id>
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Preserve other relevant validation lines in their original order.

Do not remove real evidence merely because it mentions an external smoke fixture.

If the required local evidence does not exist, stop and state that the freeze loader cannot yet be completed.

Do not fabricate markers.

VALIDATE_PACKAGE.PY

Create an internal package validator that checks:

1. The exact ZIP member set.
2. No duplicate archive members.
3. No path traversal.
4. No absolute archive-member paths.
5. KANDA_FREEZE_HINT.json exists at the archive root.
6. kind equals kanda_freeze_hint.
7. feature_id matches the current feature.
8. Required arrays exist and are not empty.
9. Every validated_files, generated_files, and protected_paths item is project-relative.
10. No item in those path fields contains:

* an absolute drive path;
* a path beginning with `/` or `\`;
* a UNC path;
* a `..` path component.

11. Real validation evidence contains:

* VALIDATION OK: <feature_id>
* STATUS: IN_SYNC
* ZIP CONTRACT: PASS

12. No source payload exists.
13. KANDA_FREEZE_FORM.txt follows the exact receive-ready transport contract.
14. The JSON inside KANDA_FREEZE_FORM.txt is valid.
15. The form arrays match the corresponding hint arrays.
16. patch_name matches the final ZIP filename.

Do not reject external-fixture names found only in validation evidence.

VALIDATE.PS1

VALIDATE.ps1 must:

1. Confirm PROJECT_ROOT exists.
2. Confirm PackageZip exists.
3. Execute VALIDATE_PACKAGE.py.
4. Resolve the official ZIP validator through OFFICIAL HELPER OWNERSHIP RESOLUTION.

When it is Project-owned, execute the exact Project-owned validator.

When it is not Project-owned, execute the canonical Tool-owned validator from KANDA_REASONER_TOOL_ROOT.

Never copy, recreate, or assume validate_patch_zip.py under PROJECT_ROOT.

Record the validator owner and exact resolved path in the validation evidence.

5. Require:

ZIP CONTRACT: PASS

6. Confirm every validated_files path exists under PROJECT_ROOT.
7. Locate and execute the real focused validator for the current feature.
8. Inspect the focused validator’s actual command-line interface before calling it.

Do not assume the parameter is:

--project-root

Inspect argparse or run:

python <focused_validator> --help

Possible accepted arguments may include:

--project-root
--tool-root
--root
--source-root

Use exactly the argument accepted by the actual validator.

Do not infer the argument from another project or another validator.

9. Capture the complete focused-validation output.
10. Require:

VALIDATION OK: <feature_id>

11. Add:

STATUS: IN_SYNC

only after every real validation gate passes.

12. Write validation evidence as UTF-8 without BOM under PROJECT_DAILY_WORK_ROOT.
13. Do not modify source code.
14. Do not execute a build unless the current feature validation explicitly requires it.
15. Do not turn historical or expected markers into claimed current evidence.

TEMPORARY DAILY-WORK ROOT

PROJECT_DAILY_WORK_ROOT may contain temporary material such as:

* extracted package files;
* temporary validation evidence;
* temporary Python helpers;
* temporary receipts;
* temporary backups.

It is not the persistent freeze-memory location.

Nothing required for future freeze loading should depend exclusively on this folder remaining available.

PREPARE_FREEZE.PS1 AND FREEZE.PS1

PREPARE_FREEZE.ps1 must:

1. Execute VALIDATE.ps1.
2. Stop immediately when validation fails.
3. Require these markers in the captured output:

VALIDATION OK: <feature_id>
STATUS: IN_SYNC
ZIP CONTRACT: PASS
FREEZE LOADER VALIDATION: PASS

4. Write complete evidence as UTF-8 without BOM.
5. Resolve the official freeze-evidence merge helper through OFFICIAL HELPER OWNERSHIP RESOLUTION, then create a temporary Python helper to invoke that exact canonical implementation.

Do not use:

python -c

The temporary helper must:

* add the resolved helper owner root to sys.path;
* use PROJECT_ROOT as the selected freeze owner argument even when the helper is Tool-owned;
* import the canonical merge helper only from the resolved owner root;
* never copy or recreate the helper under PROJECT_ROOT;
* import:

scripts.merge_freeze_validation_evidence.main

* call it with named arguments:

--project-root
--feature-id
--feature-title
--patch-zip
--evidence-file

Conceptual example:

```python
from pathlib import Path
import sys

helper_owner_root = Path(sys.argv[1]).resolve(strict=True)
project_root = Path(sys.argv[2]).resolve(strict=True)
sys.path.insert(0, str(helper_owner_root))

from scripts.merge_freeze_validation_evidence import main

raise SystemExit(
    main(
        [
            "--project-root",
            str(project_root),
            "--feature-id",
            sys.argv[3],
            "--feature-title",
            sys.argv[4],
            "--patch-zip",
            sys.argv[5],
            "--evidence-file",
            sys.argv[6],
        ]
    )
)
```

6. Require:

FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>

CORRECT PERSISTENT INTAKE

After the merge, validate:

<PROJECT_SUPPORT_ROOT>/project_freeze_after_update/freeze_hint_intake/latest_freeze_hint.json

Do not assume the merge helper creates a feature-ID subdirectory.

Do not block the process merely because this path does not exist:

freeze_hint_intake/<feature_id>/

The proven persistent intake contract is:

latest_freeze_hint.json

PROJECT_SUPPORT_ROOT must be derived from the currently selected project.

Do not use another project’s support root.

POST-MERGE PATH-FIELD REPAIR

The merge helper may preserve stale fields from an earlier intake.

After the merge, open latest_freeze_hint.json and replace only these fields using the clean KANDA_FREEZE_HINT.json from the current package:

* validated_files
* generated_files
* protected_paths

Apply this replacement in both:

latest["hint"]

and:

latest["form_inputs"]

Preserve all other data, especially:

* validation_evidence_summary;
* feature identity;
* timestamps;
* provenance;
* merge metadata;
* warnings;
* notes.

A field inside form_inputs may be stored as:

* a JSON array;
* one multiline string.

Preserve the receiver’s existing representation:

* when it is an array, write an array;
* when it is a string, write newline-separated values.

After repairing the fields, validate each path again.

Do not scan the entire JSON for the name of another project.

Validation evidence may legitimately name an external fixture.

Only validate fields that actually contain project paths.

FINAL INTAKE VALIDATION

After merge and path-field repair, require:

1. latest_freeze_hint.json exists.
2. latest.hint.feature_id matches the current feature.
3. The intake belongs to the current selected project.
4. validation_evidence_summary contains:

   * VALIDATION OK: <feature_id>
   * STATUS: IN_SYNC
   * ZIP CONTRACT: PASS
5. validated_files preserves every current validated file.
6. protected_paths contains only paths relative to PROJECT_ROOT.
7. No absolute path remains in path-bearing freeze fields.
8. No path from another project remains in path-bearing freeze fields.
9. The final intake does not replace current feature data with stale legacy feature data.

Print:

LATEST FREEZE PATH FIELDS REPLACED FROM CLEAN PACKAGE: PASS
LATEST FREEZE PROJECT-RELATIVE PATHS: PASS
LATEST FREEZE STALE EXTERNAL PROTECTED PATH REMOVED: PASS
FREEZE HINT PROJECT PATHS ONLY: PASS
LATEST FREEZE HINT IDENTITY: PASS
LATEST FREEZE FORM VALIDATION EVIDENCE: PASS
NEW LOCAL FREEZE ENTRY AUTOFILL READY: PASS
PREVIEW FREEZE ENTRY EXECUTED: NO
CONFIRM AND WRITE EXECUTED: NO

INSTALL.PS1

INSTALL.ps1 must not install source code.

It must only invoke PREPARE_FREEZE.ps1.

On success, print:

FREEZE LOADER SOURCE FILES MODIFIED: 0
FREEZE LOADER INSTALLATION OK: <feature_id>

OLDER DEFECTIVE PACKAGES

When precisely identified older defective freeze-loader ZIPs for the same project and feature exist under:

* the drive root;
* PROJECT_DAILY_WORK_ROOT;

prevent them from being scanned again.

Rename them to a non-ZIP extension, for example:

package.zip.invalid_do_not_scan

Do this only for exact earlier loader filenames for the same feature.

Do not use broad wildcards that could quarantine unrelated packages.

Do not delete evidence unnecessarily.

TERMINAL CODE

After generating the ZIP, provide one complete, robust PowerShell block.

That block must:

1. Use the real current PROJECT_ROOT.
2. Use clear, direct paths.
3. Verify the final SHA-256.
4. Copy the ZIP to PROJECT_DAILY_WORK_ROOT.
5. Verify the SHA-256 again after copying.
6. Extract the ZIP.
7. Execute PREPARE_FREEZE.ps1.
8. Check LASTEXITCODE.
9. End automatically.

Do not use Read-Host.

Do not leave the terminal waiting for Enter.

Avoid fragile code with excessive PowerShell backticks.

Avoid unnecessarily complex nested loops.

Prefer complete commands on single lines when practical.

The code must be safe to copy and paste without leaving PowerShell in continuation mode.

The execution block must not assume drive `E:` unless that is the current project’s actual drive.

NO FINAL-WRITE CONTRACT

The loader must never:

* click Preview;
* execute Preview programmatically;
* execute Confirm and Write;
* write directly into frozen_features_memory;
* write into project_freeze_ledger;
* edit an already frozen entry;
* imitate human confirmation.

The final human workflow remains:

Freeze Feature After Update
→ New Local Freeze Entry
→ Preview Freeze Entry
→ human review
→ Confirm and Write exactly once

FINAL STORAGE

The final entry belongs to the currently selected project and must be stored under:

<PROJECT_SUPPORT_ROOT>/project_freeze_after_update/frozen_features_memory

Do not use:

project_freeze_ledger

project_freeze_ledger is reusable blueprint logic.

It is not the owner of project-specific freeze memory.

ERROR MEMORY COMPANION BRIDGE

The canonical lifecycle bridge is `KPR-05-005 patch_validate_freeze_error_memory_routine_blueprint`.
The companion Error Memory loader owner is `KPR-05-008 self_contained_error_memory_lesson_intake_zip`.

This prompt owns only the Freeze intake ZIP. It must never add Error Memory lesson records, write pending Error Memory intake, or execute Memorize Error.

Before declaring the post-update lifecycle complete, report exactly one:

* `FREEZE DISPOSITION: PREPARED_FOR_HUMAN_CONFIRMATION`
* `FREEZE DISPOSITION: ALREADY_COMPLETE`
* `FREEZE DISPOSITION: NOT_ELIGIBLE`
* `FREEZE DISPOSITION: BLOCKED`

Also report exactly one companion state:

* `ERROR MEMORY COMPANION DISPOSITION: REQUIRED`
* `ERROR MEMORY COMPANION DISPOSITION: ALREADY_COMPLETE`
* `ERROR MEMORY COMPANION DISPOSITION: NOT_REQUIRED`
* `ERROR MEMORY COMPANION DISPOSITION: BLOCKED`

When a verified, reusable failure lesson is justified and Error Memory intake is not complete, the next exact owner is `KPR-05-008`. Pass Tool root, feature identity, exact patch identity, focused validator, current validation evidence, demonstrated failure evidence, and selected-Project relevance context only when it is directly useful evidence. Selected Project identity is context, not Error Memory ownership, and must not determine reusable lesson storage. Do not make the user re-enter evidence already available.

Do not merge the Freeze ZIP and Error Memory ZIP. They remain separate artifacts, separate pending/transport intakes, separate owner Boxes, and separate human approval actions. Error Memory admission into its review surface normalizes to `draft`; human `Memorize Error` is the only draft-to-active promotion gate.

FINAL ZIP VALIDATION BEFORE DELIVERY

Before delivering the ZIP:

1. Reopen the finished ZIP.
2. Confirm the exact archive-member set.
3. Parse KANDA_FREEZE_HINT.json.
4. Parse the JSON inside KANDA_FREEZE_FORM.txt.
5. Confirm all required arrays are real JSON arrays.
6. Confirm every path is relative to PROJECT_ROOT.
7. Confirm no path-bearing field contains another project’s path.
8. Confirm patch_name matches the final ZIP filename exactly.
9. Confirm VALIDATE.ps1 uses the focused validator’s actual CLI.
10. Confirm PREPARE_FREEZE.ps1 does not require a feature-specific intake directory.
11. Confirm post-merge validation checks path-bearing fields only.
12. Confirm no Read-Host exists.
13. Confirm no source payload exists.
14. Confirm the ZIP contains no accidental parent directory.
15. Calculate the final SHA-256 only after the last modification and final ZIP rebuild.

Never reuse a SHA-256 calculated before the final modification.

REQUIRED RESPONSE FORMAT

Your final response must include:

1. A download link to the ZIP.
2. The exact ZIP filename.
3. The final SHA-256.
4. A concise explanation of what the package does.
5. Confirmation that it does not modify project source code.
6. One complete PowerShell block without Read-Host.
7. The expected final markers.
8. The Freeze disposition and Error Memory companion disposition.
9. This final instruction:

Freeze Feature After Update
→ New Local Freeze Entry
→ Preview Freeze Entry
→ Confirm and Write

Do not provide only a suggestion, JSON, or partial script.

Create the functional ZIP in the current response.
