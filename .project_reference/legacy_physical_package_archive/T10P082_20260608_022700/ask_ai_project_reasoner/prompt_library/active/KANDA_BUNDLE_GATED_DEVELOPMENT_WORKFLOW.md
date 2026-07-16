# KANDA BUNDLE-GATED DEVELOPMENT WORKFLOW

Version: 1.0.3
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

The user installs the ZIP into the real project root.

Standard Windows install pattern:

```powershell
$root = "<PROJECT_ROOT>"
$zipPath = "E:\BUNDLE_NAME.zip"
Expand-Archive -Path $zipPath -DestinationPath $root -Force
Write-Host "Bundle installed."
```

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

python ".project_reference\ACTIVE_PROJECT_GOVERNANCE\check_reasoner_project_canon.py" --project-root <PROJECT_ROOT>
python ".project_reference\ACTIVE_PROJECT_GOVERNANCE\test_reasoner_project_canon.py"

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
