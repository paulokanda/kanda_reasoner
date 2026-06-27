# Bundle-Gated Development Workflow

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.5
Status: Reusable engineering methodology prompt
Prompt ID: kanda_bundle_gated_development_workflow
Prompt type: parent implementation protocol
Scope: AI-assisted software development with local validation gates

## Purpose

Use this prompt as the parent methodology for implementation, refactor, repair,
handoff, and freeze work.

The method keeps AI-assisted development safe by forcing each change through a
small installable bundle, local validation, and an explicit decision before the
change becomes baseline.

## Short name

Kanda Bundle-Gated Development.

## Full name

Kanda Bundle-Gated Development and Validate-Before-Freeze Workflow.

## Core rule

Nothing becomes baseline until it is installed locally and validated.

## Standard cycle

```text
plan -> bundle -> install -> validate -> repair/continue -> freeze
```

## When to use this prompt

Use this methodology when the AI is asked to:

- implement code;
- refactor code;
- repair validation failures;
- update prompt-library assets;
- prepare a handoff;
- prepare a governance freeze;
- create installable bundles;
- protect a clean validation baseline.

## When not to use this prompt

Do not use this methodology to justify:

- direct unreviewed source mutation;
- hidden cross-box edits;
- governance updates without explicit user approval;
- accepting sandbox-only validation as final local validation;
- bundling unrelated changes together.

## Box logic

Before changing anything, identify the active box.

A box is one isolated responsibility area. Examples include:

```text
architecture governance
workflow governance
Tab 3 docstring tooling
Tab 9 prompt library
runtime collection
GUI layer
engineering safety
```

Modify only the active box by default.

Cross-box changes are allowed only when necessary. The AI must declare:

```text
current box
external box
why external touch is required
exact files touched
validation for current box
validation for external box
```

A cross-box change is allowed only when:

- another box blocks the current box from working;
- another box invades the current box;
- the current box invades another box;
- shared canonical infrastructure must be updated.


## Prompt-Library Authoring Rule

When the bundle creates or updates Tab 9 prompt-library assets, load and follow:

```text
TEACH_AI_TAB9_PROMPT_AUTHORING_GUIDE.md
TEACH_AI_CREATE_OR_UPDATE_PROMPT_REQUEST.md
TAB9_PROMPT_ASSET_PLACEMENT_RULES.md
```

For prompt-library work, the AI must decide whether the correct action is create, update, link, or no-op before writing files.

If the prompt should be visible in Tab 9, the bundle must update:

```text
kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json
```

The bundle must also update related prompts only when they should genuinely recommend, depend on, or load the new prompt.


## Step 1 - Plan

Before generating files, state:

```text
Bundle ID:
Active box:
Goal:
Files expected to change:
Files explicitly out of scope:
Risk level:
Focused tests or text checks:
Architecture validation command:
Workflow validation command:
Manual validation needed:
Governance update needed:
```

The plan must be narrow. One bundle should solve one concern.

## Step 1.5 - Sandbox pre-delivery validation

Before delivering a bundle ZIP or final install/validation commands to the user, the AI must validate the deliverable in its own sandbox/environment.

Minimum sandbox validation:

```text
create ZIP in sandbox
extract or inspect ZIP in sandbox
verify ZIP contains only intended changed/new files
verify no cache/temp/backup/readme clutter is included
py_compile changed Python files and generated Python helpers when present
run focused sandbox tests or exact-text checks that are safe to run
inspect install PowerShell for root-to-staging ZIP movement
state sandbox validation results honestly
```

Sandbox validation is not user-local validation. The AI must still wait for the user's local validation output before claiming the bundle is locally validated or freezeable.

## Step 2 - Bundle

Create an installable ZIP bundle.

The bundle should include only the files needed for the current step.

Code bundles should include:

- modified source files;
- focused tests;
- bundle manifest;
- optional status documentation.

Text-only bundles should include:

- prompt-library or documentation files;
- metadata files when applicable;
- bundle manifest;
- local Test-Path or text-check commands.

Governance-only bundles must include only active governance files.

## Step 3 - Install

The user installs the ZIP into the real project root using the canonical root-to-staging ZIP flow.

The user downloads the patch ZIP to the root of the same drive as the project:

```text
<drive>:\BUNDLE_NAME.zip
```

The installer must move the ZIP into:

```text
<drive>:\<project_name>_delete_after_daily_work\BUNDLE_NAME.zip
```

before extracting or installing anything.

Required Windows install pattern:

```powershell
$PROJECT_ROOT = "<PROJECT_ROOT>"
$PATCH_NAME = "BUNDLE_NAME"
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

This is mandatory for every KANDA/PyArchitect patch installer: detect `DRIVE_ROOT` from `$PROJECT_ROOT`, check the project drive root first, stage into `<project_name>_delete_after_daily_work`, delete the root-drive ZIP copy after successful staging, and then extract only from `$WORK_PATCH_ZIP` into a temporary extraction folder under `$WORK_DIR`. Do not search `Downloads` or `Desktop` before the project drive root and do not use the old generic installer search template for governed patch installs.

Then back up exact overwritten files and copy only the bundle files into the project.

Important Windows limitation:

```text
Expand-Archive -Force overwrites files but does not delete files absent from the ZIP.
```

If deletion is required, provide explicit Remove-Item commands or overwrite stale
files with tested relocation markers.

## Step 4 - Validate

Run focused validation first.

Example:

```powershell
python tests\FOCUSED_TEST_NAME.py
```

Then run architecture validation:

```powershell
python kanda_reasoner_app\manage_architecture\manage_architecture.py --root <PROJECT_ROOT> --validate
```

Then run workflow validation:

```powershell
python kanda_reasoner_app\manage_workflows\manage_workflows.py --root <PROJECT_ROOT> --validate
```

Expected Kanda Reasoner clean baseline:

```text
Architecture: No validation issues
Workflow: pass=8 fail=0 warn=0 skip=3
```

For GUI work, manual GUI validation is also required.

For governance work, run the governance checker and governance regression test.

## Step 5 - Repair or continue

If focused validation fails, repair before adding features.

If architecture or workflow validation fails, repair before continuing.

If validation passes, continue to the next focused bundle.

The AI must not claim local success unless the user provides local validation
output or the response clearly says validation was sandbox-only.

## Step 6 - Freeze

Freeze only after:

- focused validation passed;
- architecture validation passed;
- workflow validation passed;
- manual validation passed when applicable;
- the user explicitly approved the freeze.

A handoff is not a governance freeze.

A governance freeze must use the official governance update protocol.

## Bundle types

### Feature bundle

Adds one feature or one small capability.

### Repair bundle

Fixes a failed validation state. It should not add new features.

### Refactor bundle

Changes structure without changing behavior. It must preserve public imports and
validate architecture/workflow gates.

### Text-only prompt-library bundle

Adds or updates prompt-library assets. It must not change runtime behavior,
active governance, or unrelated tabs.

### Governance bundle

Updates official canon. It requires explicit user approval and must contain only
the active governance files.

### Handoff note

Records continuity evidence. It does not freeze canon.

## Bundle manifest

Every bundle should include a manifest under:

```text
workbench\bundle_manifest\
```

The manifest should state:

```text
bundle name
scope
files changed
behavior added
behavior preserved
validation performed
install instructions
local validation commands
known limitations
```


## Prompt router relationship

The beginning-of-day prompt router may recommend this workflow when a task
requires implementation, refactor, repair, prompt-library bundle creation, or
other bundle-gated delivery.

When this workflow is loaded because of the router, obey the router's selected
scope and do not load unrelated prompt groups.

## Python code-quality overlay

For Python code bundles, also load:

```text
PYTHON_CLEAN_CODE_OVERLAY.md
```

Use it when the bundle creates, refactors, or repairs Python source code.

Do not require it for text-only, governance-only, handoff-only, or prompt-library
documentation bundles unless Python source code is changed.

The clean-code overlay is subordinate to this workflow:

```text
Bundle-Gated Development controls delivery and validation.
Python Clean Code Overlay controls Python code quality.
```

## AI behavior contract

The AI must:

- give a short plan before complex work;
- create focused bundles;
- include focused tests or text checks;
- avoid unrelated edits;
- provide install commands;
- provide local validation commands;
- wait for user validation output before claiming final local success;
- repair failed validation before expanding scope.

The AI must not:

- claim local validation without local output;
- hide failed tests;
- bundle unrelated changes;
- silently update governance;
- treat handoff notes as canon;
- delete accepted-warning history without explicit pruning approval;
- change box ownership without declaring it.

## Human validation contract

The user should:

- install the ZIP locally;
- run the focused validation commands;
- run architecture validation;
- run workflow validation;
- paste terminal output back;
- confirm manual GUI behavior when applicable;
- explicitly approve governance freezes.

## Accepted-warning rule

Accepted-warning baselines are governed ledgers.

Rules:

- preserve historical entries;
- append only with explicit approval;
- do not hide new unaccepted warnings;
- do not use the baseline as a trash bin;
- each accepted warning needs classification, rationale, path, code, and a stable matcher.

If a warning is later fixed, the historical entry can remain unless the user
approves a pruning task.

## Standard code-bundle validation block

```powershell
$root = "<PROJECT_ROOT>"
$zipPath = "E:\BUNDLE_NAME.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force
Write-Host "Bundle installed."

cd <PROJECT_ROOT>

python tests\FOCUSED_TEST_NAME.py

python kanda_reasoner_app\manage_architecture\manage_architecture.py --root <PROJECT_ROOT> --validate
python kanda_reasoner_app\manage_workflows\manage_workflows.py --root <PROJECT_ROOT> --validate
```

## Standard governance validation block

```powershell
$root = "<PROJECT_ROOT>"
$zipPath = "E:\GOVERNANCE_BUNDLE.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force
Write-Host "Governance bundle installed."

cd <PROJECT_ROOT>

python "project_freeze_ledger\check_reasoner_project_canon.py" --project-root <PROJECT_ROOT>
python "project_freeze_ledger\test_reasoner_project_canon.py"

python kanda_reasoner_app\manage_architecture\manage_architecture.py --root <PROJECT_ROOT> --validate
python kanda_reasoner_app\manage_workflows\manage_workflows.py --root <PROJECT_ROOT> --validate
```

## Final definition

Kanda Bundle-Gated Development is a validate-before-freeze workflow for
AI-assisted engineering. Each change is delivered as a narrow installable bundle
with focused tests or text checks. The user installs it locally, runs focused and
global validators, reports the real result, and only then is the change accepted,
repaired, continued, or frozen into governance. The method protects box
boundaries, preserves working behavior, prevents silent regressions, and makes
AI-generated work auditable.

## Motto

```text
Bundle first.
Validate locally.
Repair before expanding.
Freeze only with evidence.
```


## Change Log

- v1.0.3: Updated validation examples to prefer kanda_reasoner_app canonical CLI entrypoints.
- v1.0.2: Updated examples and bundle manifest folder to workbench\bundle_manifest.


---

## v1.0.4 Canon Reconciliation Addendum - Anti-Vibe-Coding and Staged Safety

This addendum incorporates the Kanda Reasoner canon notes that distinguish this
workflow from vibe coding and strengthen non-trivial change handling.

### Anti-vibe-coding identity

Kanda Reasoner work is not "vibe coding". The discipline is:

```text
Human architects -> AI implements -> Human validates -> Human governs
```

A change drifts toward vibe coding when any of these happen:

- generated code is accepted without reading or validation;
- validation commands are skipped;
- governance files are modified without explicit user approval;
- the AI guesses from memory instead of current source/log evidence;
- broad rewrites are accepted because they "look good".

This workflow exists to prevent those failures. The AI may generate and package,
but the project validators and the human decide whether the result becomes the
next baseline.

### Mandatory staged protocol for non-trivial changes

For architecture-affecting edits, warning cleanup, refactors, module splits,
public API changes, generated artifact repairs, helper-manifest repairs,
validator changes, GUI/runtime/workflow changes, or any change that can affect
Tab 1 or Tab 2 validation, use this staged protocol:

```text
Task 0 audit -> Task 1 roadmap -> Task 2 implementation runner -> dry run -> apply -> rollback on failure -> Tab 1 validation -> Tab 2 validation -> freeze only if clean
```

#### Task 0 audit

- inspect current source, logs, and validation output;
- identify exact target files, owner box, warning/error class, and risk;
- make no source changes;
- generate no patch ZIP unless explicitly asked;
- state the frozen baseline and what must not be touched;
- wait for user approval.

#### Task 1 roadmap

- propose the exact correction strategy;
- define files to touch and files not to touch;
- define validation gates and rollback conditions;
- make no source changes;
- wait for user approval.

#### Task 2 implementation runner

- produce a focused bundle or runner;
- support dry-run mode for risky work;
- back up every touched file/folder before writing when using a runner;
- restore backup automatically on failure;
- print explicit pass/fail markers;
- avoid quick one-shot destructive edits.

#### Dry run and apply

The dry run must show intended file changes, strategy, line counts when useful,
and validation plan without modifying source. The apply step can run only after
the dry run is clean.

#### Rollback on failure

Any focused validation, compile, import smoke, manifest validation, Tab 1
architecture validation, Tab 2 workflow validation, or unexpected exception can
block freeze. If a runner applied files and then fails, it must restore the prior
baseline and print a clear rollback marker.

### Freeze condition

A non-trivial pass is not frozen unless all relevant gates are clean:

```text
Focused validation: PASS
Tab 1 architecture: Errors 0
Tab 2 workflow: fail 0
Unexpected runtime/import/manifest failures: 0
Human freeze approval: YES
```

Py-compile alone is never enough for a non-trivial Project Reasoner pass.

### Terminal log preservation

Install, audit, validation, diagnosis, and repair scripts must not clear the
terminal. Do not emit or suggest `Clear-Host`, `cls`, `clear`, transcript
deletion, log deletion, output truncation, or terminal reset commands. Terminal
output is audit evidence.

### Change log

- v1.0.5: Added mandatory sandbox pre-delivery validation and canonical root-to-staging ZIP movement before install.
- v1.0.4: Added anti-vibe-coding identity, mandatory Task 0/1/2 staged protocol,
  dry-run/apply/rollback rule, Tab 1/Tab 2 freeze gates, and terminal log
  preservation rule.

---

## Professional AI-assisted engineering extension

### v1.0.4 professional AI-assisted engineering update

This workflow now incorporates the professional AI + human engineering partnership
rules from the v2.0 partnership framework.

Core upgrade:

```text
technical lead human -> AI pair programmer -> automated validation gate -> human freeze
```

The human owns direction, priorities, acceptance, GUI smoke validation, override
decisions, and freeze decisions. The AI owns code generation, patch design,
focused tests, validation scripts, triage, and handoffs. The AI must not decide
what ships.

Mandatory validation chain for non-trivial patches:

```text
py_compile
hallucination detector, when available
focused unit tests
focused integration tests
regression tests
performance benchmark, when required
workflow validation
architecture validation
manual GUI checklist, when visual behavior changed
freeze gate
```

A patch is not frozen unless all applicable gates pass and the user explicitly
approves freeze.

Additional professional gates:

1. Evidence freshness gate: generated evidence must match current source and may
   warn when older than the configured staleness threshold.
2. Patch registry: created, installed, focused_validated, fully_validated,
   frozen, failed, restored, and abandoned states must be tracked.
3. Unified validation runner: one command should run the validation chain and
   write both raw log and structured JSON results.
4. GUI smoke checklist: GUI patches require explicit human confirmation.
5. Freeze governance: no patch may be marked frozen when workflow fails,
   architecture fails, evidence is stale, or GUI confirmation is missing.
6. Git checkpoint gate: recommend a checkpoint before risky installs but never
   auto-commit unless explicitly requested.
7. Patch install manifest indexer: install manifests outside project root should
   be discoverable from project evidence.
8. Failure triage classifier: classify failures as patch-caused,
   existing-unrelated, generated-evidence-stale, environmental,
   missing-dependency, manual-GUI-needed, or unknown.
9. Prompt and protocol enforcement: important workflow prompts must be routable
   and loaded intentionally.
10. End-of-session handoff generator: every significant session should leave a
   structured continuation record.
11. State-based testing sandbox: patches touching persistent settings or session
   state should be tested in a disposable environment when possible.
12. Human-in-the-loop override log: rare gate overrides must be recorded with a
   reason and reviewed later.

Terminal log rule:

```text
Never clear, hide, truncate, overwrite, delete, or reduce terminal logs.
Never use Clear-Host, cls, clear, Reset-Host, or equivalent terminal reset commands.
Install, audit, validation, traceback, and diagnostic output are audit evidence.
```

Performance rule:

Patches touching imports, startup paths, event loops, large data structures, or
I/O paths should run non-regression performance benchmarks before freeze.

Documentation synchronization rule:

If a patch changes user-visible behavior, related help text, README, tooltips,
or user guidance should be updated in the same patch or explicitly marked as a
separate documentation follow-up.

Dependency compatibility rule:

If generated code relies on third-party APIs, the patch must respect the locked
or documented dependency versions. Dependency-version mismatch is a validation
failure class, not a mystery runtime failure.

AI hallucination guard:

Generated code should be scanned for common hallucination patterns: undefined
imports, references to non-existent helpers, unresolved TODO markers,
placeholder pass in non-abstract functions, and fake module paths.


## Imported Domain-Canon Generalization Rule

When a bundle is created from another project's prompts or canon, the bundle must be treated as a prompt-library/generalization bundle, not as direct governance. The AI must:

- classify source files as generalizable, reference-only, duplicate, deprecated, or rejected;
- remove source-project roots and domain-specific assumptions;
- create new generalized prompt files only for reusable engineering patterns;
- preserve the source inventory;
- avoid declaring the imported material frozen for KANDA Reasoner;
- produce an index-update candidate showing how the new prompts are routed;
- include install code but not official governance freeze.

This is subordinate to the normal bundle-gated workflow: no direct source mutation, validate-before-freeze, and one concern per bundle.

---
<!-- KANDA_ADDENDUM:error_driven_repair_bundle_to_error_memory:v1 -->

## Error-Driven Repair Bundle to Error Memory Bridge

When a user pastes an error from a terminal, app error window, GUI popup, validation run, install run, traceback, or chat-reported AI mistake, keep this workflow as the owner of the repair bundle and call the Error Memory AI formulary as the companion output.

Do not jump directly to a patch. First classify the error source and Operation phase, extract the useful evidence, inspect the exact source files, and test the narrow correction in sandbox when possible.

Before delivery, the repair ZIP must install only the corrected code and must not include unrelated files. After delivery, include install and validation commands. If the patch corrected an error, also include a receive-ready Error Memory lesson block using error_memory_ai_formulary_startup_canon.

Use real evidence only. Separate sandbox validation from user-local validation. If local validation has not been run by the user, say local validation is pending. If the correction is not fully proven, mark the Error Memory lesson as draft. Never freeze automatically.

---
<!-- KANDA_ADDENDUM:corrected_error_two_track_closure:v2 -->

## Corrected-Error Two-Track Closure Contract

When the user pastes an error and the AI corrects code, the AI must close the task in two linked tracks.

Track A is the code correction.

Track B is the Error Memory lesson that teaches the system what happened, how the code was corrected, and how not to repeat the same mistake.

The AI must not deliver only the code patch. It must also prepare the Error Memory intake material.

For every corrected-error patch, final delivery must include:

1. Code correction summary.
2. Changed files and reason for each change.
3. Installable repair ZIP or exact install instructions.
4. Code validation command and result.
5. Error Memory intake block for the AI-assisted Error lesson intake group.
6. Error Memory validation command or manual validation steps.
7. Freeze-ready summary for the code correction.
8. Freeze-ready summary for the Error Memory lesson.
9. Clear statement that local freeze is not automatic and still requires human Preview and Confirm and Write.

The Error Memory intake block must explicitly connect the error to the code correction.

It must include raw error summary, operation phase, symptom, root cause, wrong assumption, corrected code files, corrected functions or workflow areas, patch ZIP name when available, install command summary, validation command summary, validation evidence, do-not-repeat rule, prevention triggers, regression check, and freeze-readiness status.

The AI must not invent validation evidence.

If sandbox validation passed but local validation has not been run, the AI must say: Sandbox validation passed. Local validation is still pending.

If the Error Memory lesson has not yet been accepted or written through the Error Memory tab, the AI must say: Error Memory intake is prepared, but Error Memory write is still pending human review.

If freeze is not complete, the AI must say: Freeze-ready material is prepared, but freeze is not complete until Preview and Confirm and Write are performed by the user.

A corrected-error task is not complete unless both tracks are addressed:

Track A: code correction installed and validated or pending local validation.

Track B: Error Memory intake prepared and validated or pending local Error Memory validation.

Never automatically freeze.

Never claim that Error Memory was written unless the user provides local write evidence or the app reports LOCAL FREEZE WRITE OK / Error Memory write success.

Never claim the startup freeze context refreshed unless the local freeze writer output shows it.

---
<!-- KANDA_ADDENDUM:error_memory_default_autoload_patch_delivery:v2 -->

## Error Memory default insertion package delivery

When delivering the default Error Memory insertion workflow, use the normal guarded ZIP delivery pattern. In plain trigger language, this is the zip install validate routine:

```text
ZIP at project drive root -> installer stages ZIP in <project>_delete_after_daily_work -> install/update needed files and stage pending lesson -> validation -> full app restart/open Error Memory tab
```

Default Error Memory insertion package responsibilities:

```text
1. Include a formatted KANDA_ERROR_LESSON_JSON pending lesson file.
2. Stage that file under:
   <drive>:\<project>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
3. If source support is missing or stale, update error_memory_tab.py and lazy_tabs.py so the pending-intake loader is called after the tab is embedded and after project-root propagation.
4. validation must check py_compile, the staged dynamic pending file, and the source contract that loads the pending lesson into AI-assisted error lesson intake and Error Editor.
5. State that Lessons is not changed until the human clicks Memorize Error.
```

This default mode is different from Direct Error Lesson ZIP. Direct Error Lesson ZIP is manual import only. The default mode is the correct response when the user asks for `zip, install, validate, error appear in AI-assisted error lesson intake`.

---
<!-- KANDA_ADDENDUM:bundle_error_memory_packaged_lesson_gate:v1 -->

## Bundle gate for packaged Error Memory lessons

When the bundle corrects an error or includes Error Memory receive blocks, the
bundle is not ready for release until each packaged active Error Memory lesson
passes the active-ready contract in `error_memory_ai_formulary_startup_canon`.

The bundle validator or manual preflight must inspect:

```text
payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_*.txt
```

and confirm parseable marker-wrapped JSON, required active fields, meaningful
prevention triggers, real validation evidence, regression check, exception
metadata, fingerprint metadata, and redaction metadata.

Do not shift this cleanup to the user. If the lesson is not active-ready, fix the
package before emitting the ZIP link.

<!-- BUNDLE_ERROR_MEMORY_ACTIVE_READY_OUTPUT_GATE_V21_BEGIN -->

## Bundle Error Memory active-ready output gate - v21

Any bundle that corrects an error or carries Error Memory intake material must
validate the exact packaged `KANDA_ERROR_LESSON_JSON` block before release.

A bundle is not ready if an active lesson is missing `raw_error_text`,
`raw_error_snapshot_scrubbed`, `redaction`, `exception`, `fingerprint`,
`prevention_triggers`, `regression_check`, `validation_command_summary`,
`validation_evidence`, `install_command_summary`, or `notes`.

When this gate fails, fix the lesson-generation prompt/package first. Do not ask
the user to repair malformed active-ready metadata in the GUI.

<!-- BUNDLE_ERROR_MEMORY_ACTIVE_READY_OUTPUT_GATE_V21_END -->

<!-- BUNDLE_ERROR_MEMORY_JSON_FORWARD_SLASH_GATE_V22_BEGIN -->

## Bundle Error Memory JSON forward-slash gate - v22

Any bundle that contains Error Memory lesson material must validate the exact
packaged `KANDA_ERROR_LESSON_JSON` blocks before release.

An active packaged lesson is invalid when `regression_check.command` contains a
backslash or control character. Use forward slashes in commands and paths inside
Error Memory JSON. A bundle that fails this check must not be delivered.

<!-- BUNDLE_ERROR_MEMORY_JSON_FORWARD_SLASH_GATE_V22_END -->
