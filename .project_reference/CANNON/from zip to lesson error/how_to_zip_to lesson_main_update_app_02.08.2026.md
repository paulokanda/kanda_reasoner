# UNIVERSAL KANDA REASONER PATCH, INSTALL, VALIDATE, FREEZE, AND ERROR MEMORY MASTER PROMPT

You are working through KANDA Reasoner on a currently selected software Project.

The selected Project may be any Python application, library, desktop program, service, tool, website, automation, or mixed-code repository loaded into KANDA Reasoner.

Do not assume that the selected Project is KANDA Reasoner itself.

Your responsibility is to complete the entire governed development and release lifecycle:

1. Load and verify the selected Project identity.
2. Inspect its current exact source.
3. Review supplied handoffs, compact updates, validation evidence, Freeze memory, and Error Memory.
4. Identify the smallest canonical owner for the requested change.
5. Implement the change without creating duplicate responsibilities.
6. Validate the changed source.
7. Build exactly one self-contained update ZIP.
8. Package installation, validation, rollback, Freeze preparation, and required helpers inside that ZIP.
9. Stage all transient release artifacts under the selected Project’s own `<project_name>_delete_after_daily_work` folder.
10. Create that folder automatically when it does not exist.
11. Provide independent terminal commands for:

    * TERMINAL 1 — INSTALL
    * TERMINAL 2 — VALIDATE
    * TERMINAL 3 — FREEZE
    * TERMINAL 4 — ERROR MEMORY
12. Preserve human approval for Freeze and Error Memory.
13. Continue from the last reliable marker when repairing an interrupted release.

Do not merely explain what should be done. Perform the work in the current response, create the required artifact, validate it as far as the available environment permits, and provide the complete governed delivery procedure.

---

# 1. LOAD THE SELECTED PROJECT IDENTITY

Resolve the following values from the current KANDA Reasoner Project selection, startup handoff, Project Ready Check, uploaded source archive, current validation output, or canonical Project registry:

```text
Selected Project slug:
Selected Project name:
Selected Project source root:
Selected Project drive root:
Selected Project Support root:
Selected Project daily-work root:
KANDA Reasoner Tool root:
Same physical root: YES / NO
Project interpreter:
Interpreter-resolution owner:
Canonical release prompt:
Current source fingerprint:
Current Project status:
```

Do not invent these values.

Do not silently use the KANDA Reasoner Tool root as the selected Project root.

The selected Project and KANDA Reasoner may:

* Have different physical roots.
* Share the same physical root.
* Be on different drives.
* Use different Python interpreters.
* Have different Project Support and transient folders.

Even when they share the same physical directory, maintain their logical ownership boundaries.

---

# 2. UNIVERSAL PATH DERIVATION

Derive the selected Project’s paths from its exact source root.

Given:

```text
PROJECT_ROOT = exact selected Project source root
```

Derive:

```text
PROJECT_NAME = final directory name of PROJECT_ROOT
PROJECT_DRIVE = drive root containing PROJECT_ROOT
```

Then derive:

```text
PROJECT_DAILY_WORK_ROOT =
<PROJECT_DRIVE>\<PROJECT_NAME>_delete_after_daily_work
```

And, unless the current Project handoff provides a different canonical owner:

```text
PROJECT_SUPPORT_ROOT =
<PROJECT_DRIVE>\<PROJECT_NAME>_show_project_to_AI
```

Example for a Project located at:

```text
D:\medical_app
```

Derived paths:

```text
PROJECT_NAME:
medical_app

PROJECT_DRIVE:
D:\

PROJECT_DAILY_WORK_ROOT:
D:\medical_app_delete_after_daily_work

PROJECT_SUPPORT_ROOT:
D:\medical_app_show_project_to_AI
```

Example for a Project located at:

```text
E:\projects\invoice_system
```

Derived paths:

```text
PROJECT_NAME:
invoice_system

PROJECT_DRIVE:
E:\

PROJECT_DAILY_WORK_ROOT:
E:\invoice_system_delete_after_daily_work

PROJECT_SUPPORT_ROOT:
E:\invoice_system_show_project_to_AI
```

The daily-work and Project Support folders are siblings of the selected Project’s top-level folder on the same drive. They are not placed inside the Project source unless the current Project’s canonical routing explicitly says otherwise.

---

# 3. CREATE THE PROJECT DAILY-WORK FOLDER

Before staging ZIPs, extracting files, writing validation evidence, creating backup receipts, preparing Freeze intake, or staging Error Memory intake, verify:

```text
<PROJECT_DAILY_WORK_ROOT>
```

If it does not exist, create it.

The packaged release scripts must perform equivalent logic to:

```powershell
if (-not (Test-Path -LiteralPath $ProjectDailyWorkRoot)) {
    New-Item `
        -ItemType Directory `
        -Path $ProjectDailyWorkRoot `
        -Force | Out-Null
}

if (-not (Test-Path -LiteralPath $ProjectDailyWorkRoot)) {
    throw "The selected Project daily-work folder could not be created."
}
```

Do not use these as automatic substitutes:

* Downloads
* Desktop
* The current shell directory
* The operating-system temporary folder
* The KANDA Reasoner Tool’s daily-work folder
* Another Project’s daily-work folder
* A generic `C:\Temp`
* An unverified fallback directory

All temporary release materials must belong to the selected Project.

---

# 4. TOOL-VERSUS-PROJECT OWNERSHIP

## KANDA Reasoner Tool owns

* Governance prompts.
* Prompt routing.
* Project selection infrastructure.
* Generic release contracts.
* Generic Freeze and Error Memory engines.
* Governance UI.
* Cross-Project Tool capabilities.
* Tool-specific validators.

## The selected Project owns

* Its source payload.
* Its installation target.
* Its live runtime validation.
* Its Project-specific configuration.
* Its Project Support evidence.
* Its Project-specific Freeze memory.
* Its Project-specific Error Memory.
* Its transient daily-work files.
* Its patch identity and release evidence.
* Its source backups and rollback receipts.

Do not patch KANDA Reasoner because an external selected Project failed unless a separate KANDA Reasoner Tool defect is demonstrated.

Do not write Project-specific Freeze or Error Memory into a generic KANDA Tool store.

Do not transfer one Project’s authority, paths, memory, or validation evidence to another Project.

Generated handoffs and archives are evidence, not automatic editing authority. Current exact source and canonical Project ownership remain authoritative.

---

# 5. ROUTINE CLASSIFICATION

Choose exactly one principal routine class:

```text
ROUTINE_POST_IMPLEMENTATION_COMPLETION
STARTUP_DELIVERY_FAILURE
PROJECT_HANDOFF_FAILURE
PATCH_BUILD_OR_DELIVERY_FAILURE
INSTALLATION_FAILURE
VALIDATION_FAILURE
FREEZE_INTAKE_FAILURE
ERROR_MEMORY_INTAKE_FAILURE
```

Do not combine unrelated failures in the same patch.

Before implementation or delivery, resolve:

```text
ANSWER VALIDATE FREEZE MEMORIZE ROUTINE IDENTITY

Selected routine class:
Selected Project slug:
Selected Project name:
Selected Project source root:
Selected Project drive:
Selected Project Support root:
Selected Project daily-work root:
KANDA Reasoner Tool root:
Same physical root: YES / NO
Feature ID:
Feature title:
Patch ZIP name:
Patch ZIP version:
Project interpreter:
Interpreter-resolution owner:
Current Project source fingerprint:
Last reliable marker:
Already completed phases:
Current active or failed phase:
Next required phase:
May modify selected Project source: YES / NO
May modify KANDA Reasoner Tool source: YES / NO
```

Blank, stale, ambiguous, or conflicting identities block implementation and delivery.

---

# 6. CONTINUATION RULES

Maintain this state:

```text
ROUTINE CONTINUATION STATE

Selected Project:
Feature ID:
Exact ZIP or artifact identity:
Completed phases:
Last reliable marker:
Current blocked or active phase:
Next exact action:
User execution required: YES / NO
Need new training prompt: NO
```

Resume from the last trustworthy marker.

Examples:

* INSTALL passed and VALIDATE failed:

  * Do not reinstall the feature unless the validation repair requires a source change.
  * Create the smallest validation correction.
* VALIDATE passed and FREEZE preparation failed:

  * Do not reinstall or revalidate unnecessarily.
  * Correct only Freeze preparation.
* A preliminary frozen entry was written with incomplete evidence:

  * Do not edit it directly.
  * Create a newer corrective Freeze entry.
* ERROR MEMORY staging failed:

  * Do not alter feature source.
  * Correct only Error Memory intake.
* A correction changes ZIP contents:

  * Give it a new exact ZIP identity.
  * Do not reuse the previous ZIP filename or hash.

Do not ask the user to repeat evidence already supplied in the conversation or uploaded files.

---

# 7. SOURCE AUTHORITY AND INSPECTION

Before coding:

1. Resolve the exact current Project root.
2. Inspect current source files.
3. Inspect applicable Project handoffs.
4. Inspect relevant Freeze memory.
5. Inspect compact Error Memory.
6. Inspect current validators.
7. Inspect exact manifest membership when Portable or packaging behavior may be affected.
8. Identify the canonical owner of the requested behavior.
9. Identify protected paths.
10. Record baseline hashes.

Do not edit:

* An old source archive when newer source exists.
* A generated handoff as though it were current source.
* A Project Support export instead of the actual Project.
* A stale patch extraction folder.
* Another Project with a similar name.
* KANDA Reasoner when the defect belongs to the selected external Project.

---

# 8. VERIFIED PROBLEM RECORD

Before implementation, produce:

```text
VERIFIED PROBLEM RECORD

Selected Project:
Change type:
Concrete observed problem:
Evidence:
Existing capability inspected:
Canonical owner:
Smallest adequate intervention:
Files expected to change:
Files expected to be generated:
Protected paths:
Cross-box touches:
Duplication risk:
Portable or package impact:
Admission decision:
```

Valid change types include:

```text
ADD
REPAIR
CONSOLIDATE
REMOVE
VALIDATION_CORRECTION
DELIVERY_CORRECTION
FREEZE_CORRECTION
ERROR_MEMORY_CORRECTION
```

Do not add a feature merely because it sounds useful. It must solve a demonstrated gap.

---

# 9. BOX BOUNDARY AUDIT

Resolve:

```text
BOX BOUNDARY AUDIT

Selected Project:
Primary box:
Canonical owner paths:
Supporting paths:
Public contracts:
Allowed state:
Forbidden state:
Read authority:
Write authority:
Human confirmation boundaries:
Protected paths:
Portable manifests in scope: YES / NO
Project-selection authority in scope: YES / NO
May begin coding: YES / NO
```

Rules:

* One canonical owner per responsibility.
* No duplicate configuration stores.
* No duplicate clipboard owner.
* No duplicate Project authority.
* No duplicate provider runtime.
* No silent cross-Project state.
* No hidden fallback to a paid provider.
* No bypass of human approval.
* No mutation outside the declared payload.

---

# 10. ERROR MEMORY PREFLIGHT

Before implementation, inspect the selected Project’s compact Error Memory.

Open the full Error Memory archive only when:

* This is repeated-error debugging.
* A compact lesson indicates more context is required.
* The proposed solution could conflict with an existing lesson.
* Compact memory is insufficient.
* The user explicitly requests a full audit.

Resolve:

```text
ERROR MEMORY CHECK

Selected Project:
Compact export identity:
Compact export freshness:
Relevant lesson IDs:
Confidence per match:
Applicable avoidance rules:
Regression obligations:
Full Error Memory required: YES / NO
Reason:
Duplicate lesson risk:
May begin coding: YES / NO
Next safe action:
```

Do not create a duplicate Error Memory lesson for an already-covered failure.

---

# 11. IMPLEMENTATION STANDARDS

All generated Python must be:

* Compatible with the selected Project’s verified Python version.
* Windows-compatible when the Project supports Windows.
* PEP 8 compliant.
* ASCII-only when the Project requires ASCII source.
* Cohesive and maintainable.
* Properly type-checked when practical.
* Protected by focused validation.

For each changed Python module:

* Compile or parse its AST.
* Check its physical line count.
* Keep it at or below 500 physical lines.
* Prefer approximately 400 lines or fewer.
* Do not compress code merely to avoid the limit.
* Split cohesive responsibilities into smaller modules.

For JSON, TOML, YAML, XML, Markdown, HTML, and other artifacts:

* Parse or structurally validate them.
* Verify source and rendered help consistency where applicable.
* Reject malformed generated output.

---

# 12. BASELINE AND INSTALLED HASHES

For each payload path, record:

```text
Path:
Action: ADD / REPLACE / DELETE
Baseline exists: YES / NO
Expected baseline SHA-256:
Expected installed SHA-256:
Backup required: YES / NO
Rollback action:
```

The installer must fail closed before mutation when a required baseline does not match.

It must distinguish:

* Exact expected baseline.
* Exact already-installed payload.
* Unknown or conflicting state.

Safe behavior:

```text
Expected baseline:
Proceed with installation.

Exact expected installed hash:
Treat as safe repeated installation or idempotent state.

Any other hash:
Stop before mutation.
```

Do not overwrite unknown source.

---

# 13. TRANSACTIONAL INSTALLATION

The packaged installer must:

1. Verify the selected Project root.
2. Verify the Project identity.
3. Verify the package root.
4. Load the install manifest.
5. Verify every baseline hash before writing.
6. Stop before mutation on mismatch.
7. Create backups for replaced files.
8. Record newly added paths.
9. Write only manifest-approved destinations.
10. Verify installed hashes.
11. Roll back all replacements if installation fails.
12. Remove all newly added files if installation fails.
13. Verify rollback restoration.
14. Preserve unrelated files.
15. Support safe repeated installation.
16. Output a single install success marker.

Expected marker:

```text
INSTALL PHASE COMPLETE: <FEATURE_ID>
```

Installation must not run live validation.

---

# 14. EXACTLY ONE SELF-CONTAINED UPDATE ZIP

Create exactly one primary update or correction ZIP.

Suggested filename:

```text
<project_slug>_<feature_slug>_<version>_patch.zip
```

Examples:

```text
medical_app_invoice_export_v1_patch.zip
inventory_service_api_timeout_fix_v1r1_patch.zip
desktop_tool_validation_correction_v1r2_patch.zip
```

The ZIP must contain, as applicable:

```text
RUN_INSTALL.ps1
INSTALL.ps1
INSTALL_PATCH.py
RUN_VALIDATE.ps1
VALIDATE.ps1
NATIVE_PROCESS.ps1
PREPARE_FREEZE.ps1
INSTALL_MANIFEST.json
DELIVERY_MANIFEST.json
PATCH_TRACE.json
README.md
KANDA_FREEZE_HINT.json
payload/
tools/
scripts/
```

Do not require separate downloads for:

* Installer
* Validator
* Runner
* Manifest
* Validation report
* Freeze helper
* Disposable evidence file

One primary feature release uses one primary self-contained ZIP.

A separate Freeze intake ZIP or Error Memory intake ZIP is allowed only when required by its distinct canonical schema. Such a ZIP must not reinstall feature source.

---

# 15. ROOT-LEVEL FREEZE HINT

A freezeable update ZIP must contain exactly one root-level:

```text
KANDA_FREEZE_HINT.json
```

It must:

* Describe the exact current feature.
* Use the exact current ZIP identity.
* List validated and generated files.
* List protected paths.
* List do-not-regress rules.
* State known warnings.
* State required validation markers.
* State that Preview is read-only.
* State that Confirm and Write is human-only.
* Use the same canonical feature identity used by Freeze preparation.

It must not:

* Be installed into Project source.
* Contain stale data from a previous patch.
* Claim live validation that has not occurred.
* Claim Freeze completion before human confirmation.
* Write canonical Freeze memory automatically.

---

# 16. ZIP CONTRACT

Before showing the ZIP link, verify:

```text
ZIP CONTRACT CHECK

Selected Project:
Feature ID:
Feature title:
ZIP filename:
ZIP path:
ZIP SHA-256:
Receiver classification:
Declared payload members:
Actual payload members:
Total ZIP members:
Install manifest present:
Packaged installer present:
Packaged validator present:
Freeze preparation present:
Root Freeze hint present:
Provenance manifest present:
Payload hashes reconciled:
Patch provenance contract:
ZIP member contract:
ZIP CONTRACT: PASS / FAIL
```

If it does not pass, do not show the ZIP link.

Output:

```text
CONTRACT NOT MET - PATCH DELIVERY BLOCKED
```

---

# 17. PROJECT-SPECIFIC TRANSIENT ROUTING

The release must use:

```text
PROJECT_DAILY_WORK_ROOT =
<PROJECT_DRIVE>\<PROJECT_NAME>_delete_after_daily_work
```

The expected workflow is:

```text
downloaded ZIP at Project drive root
-> verify root ZIP hash
-> create Project daily-work root if absent
-> stage ZIP into Project daily-work root
-> verify staged ZIP hash
-> delete drive-root ZIP after verified staging
-> extract staged ZIP into Project daily-work root
-> run packaged installer from extraction folder
-> store temporary validation evidence in Project daily-work root
-> prepare Freeze or Error Memory intake from validated evidence
```

Expected paths:

```text
Root-drive download:
<PROJECT_DRIVE>\<PATCH_NAME>.zip

Staged ZIP:
<PROJECT_DAILY_WORK_ROOT>\<PATCH_NAME>.zip

Extraction folder:
<PROJECT_DAILY_WORK_ROOT>\<PATCH_NAME>_extract

Validation evidence folder:
<PROJECT_DAILY_WORK_ROOT>\<PATCH_NAME>

Validation evidence:
<PROJECT_DAILY_WORK_ROOT>\<PATCH_NAME>\validation_evidence.txt
```

The drive-root ZIP may be deleted only after:

1. It passed SHA-256 verification.
2. The staged copy exists.
3. The staged copy passed SHA-256 verification.

Do not extract directly over the Project.

Do not install directly from the drive-root ZIP.

---

# 18. PROJECT INTERPRETER RESOLUTION

Do not default to a generic system `python`.

Resolve the selected Project interpreter from:

* Current Project handoff.
* Project virtual environment.
* Existing validator owner.
* Project interpreter manifest.
* Canonical Project interpreter resolver.
* Previously validated Project execution command.

Possible examples include:

```text
<PROJECT_ROOT>\.venv\Scripts\python.exe
<PROJECT_ROOT>\venv\Scripts\python.exe
py -3.10
py -3.11
py -3.12
a governed executable plus prefix arguments
```

An executable and its prefix arguments must be handled separately.

When a validator dynamically imports Project packages:

* Add the selected Project root to `sys.path`.
* Set `PYTHONPATH` when required.
* Do not rely solely on the current working directory.

Require:

```text
VALIDATOR PROJECT ROOT IMPORT PATH: PASS
```

or the Project’s equivalent canonical marker.

---

# 19. POWERSHELL PATH SAFETY

Construct paths component by component.

Correct:

```powershell
$ToolsRoot = Join-Path $ProjectPath "tools"
$Validator = Join-Path $ToolsRoot "validate_feature.py"

$ScriptsRoot = Join-Path $ProjectPath "scripts"
$ZipValidator = Join-Path $ScriptsRoot "validate_patch_zip.py"
```

Avoid generating ordinary host-language strings such as:

```text
tools\validate_feature.py
```

when the host language could interpret `\v` as a vertical-tab escape.

Before delivery, inspect all packaged PowerShell files as raw bytes.

Reject every C0 control byte except:

* Tab
* Carriage return
* Line feed

Require markers:

```text
POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS
VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS
VERTICAL TAB BYTE ABSENT: PASS
CONCATENATED TOOLSVALIDATE PATH ABSENT: PASS
ESCAPE-SENSITIVE PATH ABSENT: PASS
```

Never deliver a PowerShell script containing a literal hidden vertical-tab byte.

---

# 20. PASTE-SAFE POWERSHELL

Every user-facing PowerShell block must be one independent paste unit.

Do not emit:

* Detached `else`
* Detached `catch`
* Detached `finally`
* `elseif`
* Control flow split across multiple fences
* Unsupported shell syntax
* Hidden control characters
* Paths copied from a different Project
* Stale ZIP names
* Stale SHA-256 values

Prefer invoking the packaged script directly.

Use Windows PowerShell 5.1-compatible APIs unless a newer shell is explicitly verified.

---

# 21. NATIVE STDERR HANDLING

Native stderr is not automatically a failure.

A Python, Qt, compiler, package manager, or external executable may write warnings to stderr and still exit successfully.

The native-process owner must use:

* Native process exit code.
* Required success markers.
* Structured captured output.

It must not allow a benign stderr warning to become a false PowerShell validation failure.

Require a probe such as:

```text
NATIVE_STDERR_PROBE_WARNING
NATIVE_STDERR_PROBE_OK
NATIVE_STDERR_ZERO_EXIT_USES_EXIT_CODE_AUTHORITY: PASS
```

Validation fails when:

* Exit code is nonzero.
* A required success marker is absent.
* An explicit rejection marker appears.
* Output is structurally invalid.

A warning alone is not sufficient to fail validation when exit code and required markers indicate success.

---

# 22. FORWARD-COMPATIBLE REGRESSION VALIDATORS

Prior-stage validators must assert their own durable capabilities.

Do not pin the exact hash of a predecessor validator when a later release may legitimately improve that validator.

Do not pin the exact hash of a GUI file if later releases are expected to extend it while preserving the original capability.

Use exact hashes for protected authority and product files that must remain byte-identical.

Use capability checks for extensible owners.

Examples:

```text
PRIOR-STAGE VALIDATOR FORWARD COMPATIBILITY: PASS
CUMULATIVE VALIDATOR CAPABILITY CHAIN: PASS
ORIGINAL FEATURE CAPABILITIES PRESERVED: PASS
```

A later update must not be rejected merely because it added a legitimate button, status panel, help section, or compatible validation improvement.

---

# 23. USER-FACING RELEASE FORMAT

The final response must use these exact principal headings:

# ARTIFACT — ONE UPDATE ZIP

# TERMINAL 1 — INSTALL

# TERMINAL 2 — VALIDATE

# TERMINAL 3 — FREEZE

# TERMINAL 4 — ERROR MEMORY

Do not merge these phases.

---

# ARTIFACT — ONE UPDATE ZIP

Provide:

```text
Selected Project:
Feature ID:
Feature title:
ZIP filename:
ZIP SHA-256:
Payload file count:
ZIP member count:
ZIP CONTRACT: PASS
```

Provide exactly one primary ZIP link.

Explain what the ZIP changes and what it explicitly does not change.

---

# TERMINAL 1 — INSTALL

The INSTALL phase may:

* Resolve the selected Project root.
* Derive Project name and drive.
* Create the Project daily-work folder when absent.
* Locate the drive-root ZIP.
* Verify its SHA-256.
* Stage it into the Project daily-work folder.
* Verify the staged ZIP.
* Delete the root-drive ZIP after verified staging.
* Remove stale extraction folders.
* Extract the staged ZIP.
* Invoke the packaged installer.
* Verify baseline hashes.
* Create backups.
* Install payload files.
* Verify installed hashes.
* Roll back after failure.

INSTALL must not:

* Run live validation.
* Prepare Freeze.
* Write Freeze memory.
* Stage Error Memory.
* Memorize an error.

Expected marker:

```text
INSTALL PHASE COMPLETE: <FEATURE_ID>
```

After successful installation:

1. Show the marker.
2. Pause briefly.
3. Run `Clear-Host`.
4. Keep the terminal open.

On failure, show:

```text
PHASE: INSTALL
ERROR TYPE:
ERROR MESSAGE:
INVOCATION:
LAST SUCCESSFUL MARKER:
PROJECT ROOT:
PACKAGE ROOT:
```

Then:

1. Require Enter.
2. Require Enter again.
3. Run one final `Clear-Host`.
4. Keep the terminal open.

---

# TERMINAL 2 — VALIDATE

VALIDATE may:

* Verify installed hashes.
* Run focused validators.
* Run applicable regression validators.
* Run GUI functional smoke tests.
* Run no-Project tests when relevant.
* Run package and Portable checks when relevant.
* Verify startup synchronization.
* Write named transient evidence under the selected Project daily-work folder.
* Write durable evidence through the selected Project’s canonical Project Support owner when required.

VALIDATE must not:

* Install source.
* Prepare Freeze.
* Write Freeze memory.
* Stage Error Memory.
* Memorize an error.

Require:

```text
VALIDATION OK: <FEATURE_ID>
ZIP CONTRACT: PASS
STATUS: IN_SYNC
VALIDATION PHASE COMPLETE: <FEATURE_ID>
```

Also require feature-specific markers.

Do not claim that delivery-time simulation equals real local validation.

When GUI validation could not run in the artifact-building environment, explicitly require it to run in the selected Project’s local environment during Terminal 2.

Remember:

```text
INSTALL IS NOT VALIDATION
```

---

# TERMINAL 3 — FREEZE

FREEZE may run only after:

```text
VALIDATION OK: <FEATURE_ID>
ZIP CONTRACT: PASS
STATUS: IN_SYNC
```

FREEZE may:

* Verify the selected Project identity.
* Verify the exact ZIP identity.
* Read current validation evidence.
* Merge validation evidence into the canonical Freeze intake.
* Load or prepare a New Local Freeze Entry.

FREEZE must not:

* Install source.
* Re-run installation.
* Write canonical frozen memory automatically.
* Execute Preview automatically.
* Execute Confirm and Write automatically.
* Bypass human confirmation.
* Edit an existing frozen entry directly.

Expected preparation marker:

```text
FREEZE DISPOSITION: PREPARED_FOR_HUMAN_CONFIRMATION
```

Then instruct:

```text
Freeze Feature After Update
-> New Local Freeze Entry
-> Preview Freeze Entry
-> review identity, files, rules, and evidence
-> Confirm and Write
```

Preview is read-only.

Confirm and Write is human-only.

For a correction, create a newer corrective Freeze entry. Never directly edit an existing frozen entry.

Project-specific Freeze memory belongs under the selected Project Support root, normally:

```text
<PROJECT_SUPPORT_ROOT>\project_freeze_after_update\frozen_features_memory
```

After human confirmation, refresh the selected Project’s startup Freeze context.

---

# TERMINAL 4 — ERROR MEMORY

Evaluate Error Memory only from actual failures.

For each observed failure:

1. Preserve exact output.
2. Record the last successful marker.
3. Identify the root cause.
4. Search compact Error Memory.
5. Open full Error Memory when necessary.
6. Check duplicate lessons.
7. Check overlapping lessons.
8. Check supersession.
9. Determine whether the failure is reusable across future work.
10. Create a lesson only when it is verified and not already covered.

If no new reusable lesson is justified, output:

```text
ERROR MEMORY DISPOSITION: NOT_REQUIRED
```

Do not generate an empty intake ZIP.

When a reusable lesson is justified:

* Create a separate Error Memory intake ZIP.
* Do not include feature source in that intake ZIP.
* Stage it under the selected Project’s daily-work root.
* Load pending lessons for review.
* Do not execute Memorize Error.

Then instruct:

```text
KANDA Reasoner
-> select the correct Project
-> Error Memory
-> review each pending lesson
-> Memorize Error only after explicit human approval
```

---

# 24. STRICT PHASE ISOLATION

The following rules are absolute:

```text
INSTALL cannot run VALIDATE.
INSTALL cannot run FREEZE.
INSTALL cannot run ERROR MEMORY.

VALIDATE cannot run INSTALL.
VALIDATE cannot run FREEZE.
VALIDATE cannot run ERROR MEMORY.

FREEZE cannot install source.
FREEZE cannot run validation as a substitute for current evidence.
FREEZE cannot write automatically.
FREEZE cannot stage Error Memory.

ERROR MEMORY cannot install source.
ERROR MEMORY cannot validate source.
ERROR MEMORY cannot write Freeze memory.
ERROR MEMORY cannot execute Memorize Error.
```

Never provide an all-in-one release command.

---

# 25. TERMINAL CLEANUP CONTRACT

Each terminal phase is independent.

After a successful phase:

1. Display the final success marker.
2. Keep it visible long enough to read.
3. Pause briefly when appropriate.
4. Clear the terminal once.
5. Keep the terminal window open.

After a failed phase:

1. Display:

   * Phase
   * Error type
   * Error message
   * Invocation
   * Last successful marker
   * Evidence path
2. Require Enter.
3. Require Enter again.
4. Run one final `Clear-Host`.
5. Keep the terminal open.

Do not close the terminal automatically.

---

# 26. NO-ORPHAN-REPORT RULE

Do not generate or deliver files such as:

```text
*_VALIDATION_REPORT.txt
standalone runner
standalone installer
standalone validator
duplicate manifest
disposable summary
empty Error Memory loader
```

unless the file has:

* A named future consumer.
* A canonical owner.
* A retention path.
* A documented reuse purpose.

Temporary validation evidence may be stored at:

```text
<PROJECT_DAILY_WORK_ROOT>\<PATCH_NAME>\validation_evidence.txt
```

This is allowed when Freeze preparation is its named future consumer.

Durable evidence belongs under the selected Project Support root through its canonical owner.

---

# 27. REQUIRED PRE-DELIVERY TESTS

Before releasing the ZIP, run every applicable test supported by the current environment:

```text
Current source inspected: PASS
Project identity resolved: PASS
Canonical owner resolved: PASS
Error Memory preflight: PASS
Python AST or compile: PASS
JSON parse: PASS
Help consistency: PASS
Module size <=500: PASS
Baseline hashes recorded: PASS
Installed hashes recorded: PASS
Exact payload manifest: PASS
ZIP member contract: PASS
Patch provenance contract: PASS
Freeze hint contract: PASS
Hidden PowerShell control bytes: 0
Structural Join-Path contract: PASS
Native stderr zero-exit probe: PASS
Baseline mismatch rejection: PASS
No writes after baseline rejection: PASS
Transactional installation simulation: PASS
Installed-hash verification: PASS
Repeated installation: PASS
Forced-failure rollback: PASS
Rollback restoration: PASS
Protected paths unchanged: PASS
Cross-Project authority absent: PASS
Project-selection authority unchanged: PASS
Portable manifests unchanged or exact change justified: PASS
GUI functional smoke: PASS or deferred to local validation
No-Project GUI state: PASS when applicable
```

Do not claim a test passed when it was not executed.

---

# 28. PATCH DELIVERY GATE

Before final delivery, output:

```text
PATCH DELIVERY GATE

Selected Project:
ZIP purpose:
ZIP placement path:
Feature ID:
What this ZIP is:
What this ZIP is not:
Install code present: YES / NO
Validation code present: YES / NO
Expected validation markers:
Changed files:
Generated files:
Allowed write paths:
Protected paths:
Forbidden write paths:
Rollback behavior:
Daily-work folder:
Daily-work folder created if absent: YES / NO
Root Freeze hint present: YES / NO
Freeze remains human-only: YES / NO
Error Memory payload:
Post-validation steps:
What not to do:
Beginner-safe: YES / NO
GATE STATUS: PASS / FAIL
```

---

# 29. RECEIVER DELIVERY CHECK

Also output:

```text
RECEIVER DELIVERY CHECK

Selected Project:
Receiver classification:
Actual receiver path:
Selected Project daily-work path:
Installer stages ZIP: YES / NO
Daily-work folder created if absent: YES / NO
Root ZIP hash verified: YES / NO
Staged ZIP hash verified: YES / NO
Root ZIP removed only after staging verification: YES / NO
Extraction occurs only from staged ZIP: YES / NO
Manual source paste required: YES / NO
Storage-only helper: YES / NO
Receiver proof:
RECEIVER STATUS: PASS / FAIL
```

---

# 30. FAIL-CLOSED RESPONSE

When Project identity, current source, owner, interpreter, baseline, ZIP contract, or validation authority cannot be resolved, do not improvise.

Output:

```text
ANSWER VALIDATE FREEZE MEMORIZE ROUTINE BLOCKED

Routine class:
Selected Project identity problem:
Missing exact source or artifact:
Missing owner or validator:
Unresolved source fingerprint:
Unresolved interpreter:
Unresolved ZIP identity:
Last reliable marker:
May build patch: NO
May show ZIP link: NO
May claim live validation: NO
May freeze: NO
May stage Error Memory: NO
Next safe action:
```

---

# 31. UNIVERSAL SAFE SEQUENCE

Follow this exact sequence:

```text
load selected Project identity
-> distinguish KANDA Reasoner Tool from selected Project
-> derive Project name, drive, Support root, and daily-work root
-> create daily-work root if absent
-> inspect current exact source
-> inspect handoff, Freeze memory, and Error Memory
-> identify the smallest canonical owner
-> record protected paths and boundaries
-> implement the smallest safe change
-> compile and statically validate
-> create one self-contained update ZIP
-> package INSTALL, VALIDATE, FREEZE preparation, manifests, and helpers
-> scan PowerShell raw bytes
-> validate structural paths
-> validate ZIP contract
-> simulate transactional installation
-> simulate rollback
-> test repeated installation
-> deliver one ZIP link and SHA-256
-> provide TERMINAL 1 — INSTALL
-> require INSTALL PHASE COMPLETE
-> provide TERMINAL 2 — VALIDATE
-> require VALIDATION OK, ZIP CONTRACT: PASS, and STATUS: IN_SYNC
-> provide TERMINAL 3 — FREEZE
-> prepare intake only
-> human Preview
-> human Confirm and Write
-> refresh Project startup Freeze context
-> evaluate observed failures
-> provide TERMINAL 4 — ERROR MEMORY only when justified
-> human review
-> human Memorize Error only after approval
```

---

# 32. FINAL RESPONSE STYLE

Use these exact prominent headings:

```text
# ARTIFACT — ONE UPDATE ZIP

# TERMINAL 1 — INSTALL

# TERMINAL 2 — VALIDATE

# TERMINAL 3 — FREEZE

# TERMINAL 4 — ERROR MEMORY
```

For each terminal phase:

* Give exactly one independent PowerShell paste block.
* State when it may run.
* State what it does.
* State what it cannot do.
* Show expected markers.
* Show exact paths.
* Explain relevant nonfatal warnings.
* Keep phases separate.

The final response must be complete enough for a beginner to:

1. Download the ZIP.
2. Put it in the correct drive-root location.
3. Install it.
4. Validate it.
5. Prepare and confirm Freeze.
6. Handle Error Memory when justified.

---

# 33. CURRENT SELECTED PROJECT

Resolve these values from KANDA Reasoner. Do not assume them:

```text
SELECTED PROJECT SLUG:
<RESOLVE_FROM_CURRENT_KANDA_PROJECT>

SELECTED PROJECT NAME:
<DERIVE_FROM_SELECTED_PROJECT_ROOT>

SELECTED PROJECT ROOT:
<RESOLVE_FROM_CURRENT_KANDA_PROJECT>

SELECTED PROJECT DRIVE:
<DERIVE_FROM_SELECTED_PROJECT_ROOT>

SELECTED PROJECT SUPPORT ROOT:
<RESOLVE_OR_DERIVE_FROM_SELECTED_PROJECT>

SELECTED PROJECT DAILY-WORK ROOT:
<SELECTED_PROJECT_DRIVE>\<SELECTED_PROJECT_NAME>_delete_after_daily_work

KANDA REASONER TOOL ROOT:
<RESOLVE_FROM_CURRENT_KANDA_INSTALLATION>

SAME PHYSICAL ROOT:
<YES_OR_NO>

PROJECT INTERPRETER:
<RESOLVE_FROM_CURRENT_PROJECT_HANDOFF_OR_VALIDATOR_OWNER>
```

Never replace these placeholders with KANDA Reasoner’s own paths unless KANDA Reasoner itself is the currently selected Project.

---

# 34. CURRENT TASK

Complete this task for the currently selected Project:

```text
<PASTE THE FEATURE REQUEST, BUG REPORT, VALIDATION FAILURE, INSTALLATION FAILURE, FREEZE FAILURE, OR ERROR MEMORY REQUEST HERE>
```

Treat all currently uploaded files, exact source archives, validation outputs, Freeze snippets, compact updates, patch identities, and current Project handoffs as one continuation context.

Do not ask the user to repeat evidence already supplied.

Resume from the last reliable marker.

Perform the work now.
