# KANDA Reasoner Handoff - Programmatic Dynamic Artifact Staging Enforcement

## Objective

Update **KANDA Reasoner only** so transient artifact delivery/staging is enforced programmatically instead of depending primarily on AI prompt compliance.

Do not modify EEG Kanda or any other observed Project.

Release owner classification:

`KANDA_TOOL_RELEASE`

The selected external Project remains observer-only.

## Problem demonstrated

A delivered helper file was incorrectly assumed to already exist at:

`E:\eeg_kanda_delete_after_daily_work\R7A_FREEZE_CORRECTION.ps1`

The actual workflow is:

1. Delivered/imported artifact initially appears at the root of the active Project's drive.
2. KANDA workflow derives the active Project dynamically.
3. Artifact is staged into `<project>_delete_after_daily_work`.
4. Integrity is verified.
5. Only after successful staging is the drive-root copy removed.
6. Work proceeds from the staged copy.
7. Everything remaining under `<project>_delete_after_daily_work` is disposable at end of work/day.

The Project name and drive must never be hardcoded.

Examples:

```text
Project root:
E:\eeg_kanda

Derived drive root:
E:\

Derived transient root:
E:\eeg_kanda_delete_after_daily_work
```

```text
Project root:
D:\my_project

Derived drive root:
D:\

Derived transient root:
D:\my_project_delete_after_daily_work
```

## Architectural decision

Do not implement this as a fuzzy heuristic.

Implement a deterministic central policy.

Heuristics may be used only for optional artifact discovery when a filename is unknown.

Path ownership and staging destination must always be deterministic from the active Project root.

Canonical conceptual API:

```text
Active Project root
        |
        v
ProjectArtifactStagingPolicy
        |
        +-- project_root
        +-- drive_root
        +-- project_name
        +-- root_inbox
        +-- transient_root
        |
        v
validated staging operation
```

## Python implementation basis

Use only Python 3.10-compatible standard-library APIs.

Preferred path derivation:

```python
project_root = Path(project_root).resolve(strict=True)

drive_root = Path(project_root.anchor)
project_name = project_root.name

transient_root = (
    drive_root /
    f"{project_name}_delete_after_daily_work"
)
```

Do not derive the transient folder from:

* KANDA Tool root;
* current working directory;
* Downloads;
* Desktop;
* a previously selected Project;
* a cached project name;
* a hardcoded drive;
* a hardcoded project slug.

The active Project root is the sole path-derivation input.

## Proposed canonical Tool component

First inspect current KANDA Reasoner source and Box ownership.

If no existing canonical owner already provides this responsibility, add one small cohesive module under the correct KANDA Tool Box, conceptually:

```text
kanda_reasoner_app/
    project_artifact_staging.py
```

Do not create this exact file blindly if an existing staging/path-policy owner already exists.

Prefer extending the existing canonical owner over creating duplicate infrastructure.

Suggested public concepts:

```text
ProjectArtifactStagingPlan
derive_project_artifact_staging_plan(...)
stage_root_artifact(...)
validate_staging_plan(...)
```

Avoid Project-specific names such as:

```text
stage_eeg_kanda_artifact
eeg_kanda_daily_work_root
```

## Staging plan object

The central API should return an immutable object containing at least:

```text
project_root
drive_root
project_name
root_inbox
transient_root
source_artifact
staged_artifact
```

Example:

```text
project_root:
E:\eeg_kanda

drive_root:
E:\

project_name:
eeg_kanda

root_inbox:
E:\

transient_root:
E:\eeg_kanda_delete_after_daily_work

source_artifact:
E:\R7A_FREEZE_CORRECTION.ps1

staged_artifact:
E:\eeg_kanda_delete_after_daily_work\R7A_FREEZE_CORRECTION.ps1
```

## Fail-closed path rules

Reject staging if any of the following occurs:

```text
project root missing
project root not absolute
project root cannot be resolved
project name empty
drive/anchor missing
artifact name contains parent traversal
artifact is not directly under the derived drive root
artifact is a directory when a file is required
artifact is an unsafe link/reparse target when policy forbids it
source and destination resolve unexpectedly
destination escapes transient root
active Project changes during operation
```

Never silently fall back to:

```text
Downloads
Desktop
current working directory
KANDA Reasoner root
another Project's transient folder
```

Failure result should clearly report:

```text
ARTIFACT STAGING BLOCKED
Project root:
Derived drive root:
Derived transient root:
Expected root artifact:
Reason:
```

## Safe staging algorithm

Preserve the existing governance requirement:

```text
copy
verify
remove source
```

Do not simply delete or move the source without verification.

Recommended algorithm:

```text
1. Resolve active Project root.

2. Derive:
   drive_root
   project_name
   transient_root

3. Require incoming artifact at:
   drive_root / artifact_filename

4. Create transient_root when needed.

5. Copy source to a temporary file located inside transient_root.

6. Compute SHA-256 of:
   original drive-root file
   temporary staged copy

7. Require exact hash equality.

8. Promote the verified temporary copy to:
   transient_root / artifact_filename

9. Only after successful verification/promotion:
   delete the original drive-root file.

10. Return the final staged path.
```

Because KANDA Reasoner supports Python 3.10, implement file hashing with a normal chunked `hashlib.sha256()` loop.

Do not use `hashlib.file_digest()`, because that helper was added after Python 3.10.

A temporary destination should be used so a partial copy is never mistaken for a successfully staged artifact.

Within the same filesystem, `os.replace()` may be used to promote the completely verified temporary file to the final staged filename.

## Important behavioral invariant

After success:

```text
ROOT ARTIFACT PRESENT: NO
STAGED ARTIFACT PRESENT: YES
SHA256 VERIFIED: YES
STAGED ROOT MATCHES ACTIVE PROJECT: YES
```

On failure:

```text
ROOT ARTIFACT DELETED: NO
PARTIAL STAGED ARTIFACT ACCEPTED: NO
WRONG PROJECT TRANSIENT ROOT USED: NO
```

The root source must remain intact if staging verification fails.

## Dynamic Project-switch protection

The selected Project can change.

Therefore staging must not rely on a stale global/cached value.

At operation start capture the current Project observation/selection token already owned by KANDA Reasoner.

Immediately before the destructive final step - deletion of the root copy - verify that the selected Project observation still represents the same Project.

Use current KANDA Reasoner terminology:

`selection_ticket`

Do not introduce `selection_epoch`.

If Project identity changed during staging:

```text
PROJECT SWITCH DURING STAGING: BLOCKED
ROOT SOURCE PRESERVED: YES
```

The temporary staged copy may be discarded.

## Tool/Project boundary

This feature belongs entirely to KANDA Reasoner workflow/governance.

It must not:

* modify EEG Kanda source;
* install code into EEG Kanda merely to implement the staging policy;
* require an EEG Kanda Python module;
* copy KANDA Reasoner runtime source into the selected Project;
* make the selected Project depend on KANDA Reasoner at application runtime;
* use Fire Shield as permission for normal external-Project development.

KANDA Reasoner computes and communicates workflow paths.

The external Project remains independent.

## Integrate with handoff generation

Do not create a new standalone manifest/schema unless necessary.

Prefer extending an existing current handoff structure such as the appropriate:

```text
patch_safety_routes
routing_manifest
ai_briefing
```

with a machine-generated staging contract.

Suggested conceptual fields:

```text
artifact_staging:
    project_root
    drive_root
    project_name
    root_inbox
    transient_root
    source_location_rule
    staging_required
    verify_before_source_delete
    cleanup_semantics
```

Example generated values for EEG Kanda:

```text
project_root:
E:\eeg_kanda

drive_root:
E:\

root_inbox:
E:\

transient_root:
E:\eeg_kanda_delete_after_daily_work
```

The values must be generated from the selected Project.

They must not be copied from a static EEG-specific template.

## Integrate with startup delivery

The current startup rule is already explicit for patch ZIP delivery.

Generalize it from "patch ZIP" to all externally delivered transient work artifacts.

Desired canonical behavior:

```text
All externally delivered transient work artifacts initially arrive
at the root of the active Project's drive.

Before use, derive the current Project drive and Project name
programmatically from PROJECT_ROOT and stage the artifact into:

<project_drive>\<project_name>_delete_after_daily_work

Verify successful staging before removing the drive-root source.

Never ask the user to pre-place a delivered artifact directly inside
_delete_after_daily_work.

Never hardcode the Project name or drive.

When the selected Project changes, derive the paths again.
```

Because this changes startup-delivery source behavior, implementation must load and obey:

```text
zz_read_only_if_modifying_startup_delivery.md
sync_startup_routing_kernel_pack.py
STARTUP_ROUTING_KERNEL_SOURCES.json
current first_prompt_files artifacts
```

Do not directly patch generated startup ZIP contents as the canonical source.

Regenerate startup delivery through its existing generator.

## Generated-command enforcement

Add a KANDA Tool validator that inspects generated patch/install/validation/freeze command templates and rejects known bad patterns.

At minimum detect:

```text
Downloads-first artifact lookup
Desktop-first artifact lookup
hardcoded E:\eeg_kanda_delete_after_daily_work
hardcoded E:\kanda_reasoner_delete_after_daily_work
hardcoded external Project drive
instructions telling the user to manually place a delivered file
inside <project>_delete_after_daily_work before staging
```

Do not reject the literal suffix:

```text
_delete_after_daily_work
```

because the suffix itself is canonical.

Reject cases where the full owner path is statically bound rather than derived from the current Project root.

## Prefer generated expressions

PowerShell emitted by KANDA's governance templates should follow the conceptual form:

```text
$ProjectRoot
    -> GetFullPath
    -> drive root

Split-Path $ProjectRoot -Leaf
    -> project name

drive root + project name + "_delete_after_daily_work"
    -> transient root
```

Never generate:

```text
$DailyWorkRoot = "E:\eeg_kanda_delete_after_daily_work"
```

for reusable Project-agnostic instructions.

## Validator requirements

Create focused regression tests around the central Python policy.

Mandatory cases:

### Dynamic drive/name

```text
E:\eeg_kanda
-> E:\
-> eeg_kanda
-> E:\eeg_kanda_delete_after_daily_work
PASS
```

```text
D:\other_project
-> D:\
-> other_project
-> D:\other_project_delete_after_daily_work
PASS
```

### No Tool contamination

External Project:

```text
project_root = E:\eeg_kanda
```

must never derive:

```text
E:\kanda_reasoner_delete_after_daily_work
```

### No stale-project reuse

Switch:

```text
project_A -> project_B
```

Then stage another artifact.

Expected:

```text
PROJECT_B TRANSIENT ROOT USED: YES
PROJECT_A TRANSIENT ROOT REUSED: NO
```

### Root location

Given:

```text
E:\patch.zip
```

and:

```text
PROJECT_ROOT = E:\eeg_kanda
```

expected source:

```text
E:\patch.zip
```

not:

```text
Downloads\patch.zip
Desktop\patch.zip
E:\eeg_kanda_delete_after_daily_work\patch.zip
```

before staging.

### Integrity

Test:

```text
copy succeeds
hash matches
destination promoted
root source removed
```

and:

```text
copy corrupted/hash mismatch
destination not accepted
root source remains
```

### Project-switch race

Simulate Project selection changing before destructive cleanup.

Expected:

```text
SOURCE DELETE BLOCKED
```

### Path traversal

Reject:

```text
..\artifact.zip
subfolder\artifact.zip
absolute path belonging to another drive
```

when the API contract expects a drive-root artifact filename.

## Static source guards

Search KANDA Reasoner source for stale delivery assumptions.

Classify every occurrence of:

```text
Downloads
Desktop
_delete_after_daily_work
DRIVE_ROOT
ProjectRoot
patch ZIP staging
artifact staging
```

Do not mass-replace legitimate historical evidence or test fixtures.

Repair only live runtime/generator/prompt owners.

## Startup bridge validation

After regeneration verify:

```text
DYNAMIC ACTIVE PROJECT DRIVE DERIVATION: PASS
DYNAMIC PROJECT NAME DERIVATION: PASS
ROOT-FIRST ARTIFACT INTAKE: PASS
STAGE-BEFORE-USE: PASS
VERIFY-BEFORE-ROOT-DELETE: PASS
DOWNLOADS FALLBACK: ABSENT
DESKTOP FALLBACK: ABSENT
HARDCODED PROJECT DAILY-WORK ROOT: ABSENT
PROJECT SWITCH RE-DERIVES STAGING ROOT: PASS
```

## Architecture constraints

Preserve:

```text
KANDA Reasoner = Tool
selected external Project = observer-only Project
```

Do not add another general path framework if one already exists.

Do not create a service locator.

Do not create global mutable staging state.

Do not cache the transient root across Project switches.

Do not weaken existing Tool/Project boundaries.

Keep each new/touched Python module <=500 physical lines after normal formatting.

Prefer a small pure derivation function plus a bounded staging executor.

## Required prompts/context before implementation

Because this is a KANDA Tool release and also affects startup delivery, load the smallest current owner set including:

```text
01_ai_prompt_request_canon
07_daily_patch_delivery_guardrails
14_project_tool_boundary_canon
pre_output_contract_gates
patch_install_delivery_error_register
04_box_architecture_and_boundaries
05_patch_delivery_and_validation
08_python_engineering_core
09_python_quality_security_observability
zz_read_only_if_modifying_startup_delivery.md
```

Also inspect:

```text
sync_startup_routing_kernel_pack.py
STARTUP_ROUTING_KERNEL_SOURCES.json
current staging/delivery helper owners
current Show Project to AI handoff generator
current patch_safety_routes generator
current tests/validators for transient workspace routing
```

Use the current source to identify exact canonical owner files before editing.

## Release boundary

Classification:

`KANDA_TOOL_RELEASE`

Do not request or modify EEG Kanda source for this change.

EEG Kanda may be used only as an external Project test fixture/context demonstrating dynamic path derivation.

Expected release write set:

```text
KANDA Reasoner Tool source
KANDA Reasoner Tool tests/validators
KANDA prompt/startup canonical sources if bridge wording changes
generated startup artifacts through canonical regeneration
```

Expected EEG Kanda production-source write set:

```text
ZERO
```

## Suggested feature identity

Suggested feature ID:

```text
kanda-project-artifact-dynamic-staging-enforcement-v1
```

Suggested title:

```text
Dynamic Active-Project Artifact Staging Enforcement
```

## Acceptance markers

Final validation should include equivalent markers:

```text
PROJECT ARTIFACT STAGING OWNER: KANDA TOOL
EXTERNAL PROJECT SOURCE MODIFIED: NO

PROJECT ROOT DYNAMIC: PASS
PROJECT DRIVE DYNAMIC: PASS
PROJECT NAME DYNAMIC: PASS
TRANSIENT ROOT DYNAMIC: PASS

ROOT-FIRST ARTIFACT INTAKE: PASS
STAGING COPY: PASS
SHA256 VERIFICATION: PASS
ROOT COPY REMOVED ONLY AFTER VERIFICATION: PASS
FAILED STAGING PRESERVES ROOT SOURCE: PASS

PROJECT SWITCH RE-DERIVES PATHS: PASS
STALE PROJECT TRANSIENT ROOT REUSE: ABSENT

DOWNLOADS-FIRST FALLBACK: ABSENT
DESKTOP-FIRST FALLBACK: ABSENT
HARDCODED PROJECT DRIVE: ABSENT
HARDCODED PROJECT DAILY-WORK ROOT: ABSENT

EXTERNAL PROJECT KANDA RUNTIME DEPENDENCY ADDED: NO
EXTERNAL PROJECT SOURCE WRITE ADDED: NO

STARTUP DELIVERY REGENERATED: PASS
STARTUP DELIVERY STATUS: IN_SYNC

VALIDATION OK: kanda-project-artifact-dynamic-staging-enforcement-v1
STATUS: IN_SYNC
```

## Freeze requirements

If implementation and validation pass:

1. Preserve successful validation evidence outside any `_delete_after_daily_work` folder.
2. Prepare KANDA Reasoner's Tool-owned freeze intake.
3. Preview remains read-only.
4. Confirm and Write remains explicit human action.
5. Refresh startup freeze context after successful write.

## Do-not-regress rules

* Never hardcode the active Project drive.
* Never hardcode the active Project name.
* Never assume EEG Kanda is the selected Project.
* Never assume KANDA Reasoner is the selected Project.
* Never ask the user to manually place an incoming file in `_delete_after_daily_work`.
* Incoming transient artifacts start at the active Project drive root.
* Stage before use.
* Verify before deleting the root copy.
* Derive the transient root again whenever the selected Project changes.
* `_delete_after_daily_work` is disposable.
* Durable evidence must leave `_delete_after_daily_work` before cleanup.
* KANDA Reasoner remains observer/support tooling for external Projects.
* External Projects must not require KANDA Tool source/runtime to operate or validate themselves.

## Resume instruction for next AI

Do not modify EEG Kanda.

Open the current KANDA Reasoner source and locate the existing canonical owners for:

```text
Project root/selection observation
transient workspace derivation
patch/artifact staging
Show Project to AI handoff generation
startup delivery generation
patch-safety command generation
```

Then implement the smallest centralized dynamic staging policy that removes hardcoded Project paths and converts the current prompt-level staging rule into executable KANDA Tool behavior plus regression validation.

Do not create duplicate path/staging infrastructure if a canonical owner already exists.
