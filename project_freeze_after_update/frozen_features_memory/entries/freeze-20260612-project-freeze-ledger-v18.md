---
freeze_id: "freeze-20260612-project-freeze-ledger-v18"
box: "project_freeze_ledger"
status: "frozen"
date: "2026-06-12"
entry: "project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v18.md"
protected_paths:
  - "project_freeze_ledger/readme_project_freeze_ledger.md"
  - "project_freeze_ledger/project_frozen_implemented_steps.md"
  - "project_freeze_ledger/send_to_ai_when_freezing_feature.md"
  - "project_freeze_ledger/USER_READ_THIS_TO_UNDERSTAND_HOW_TO_FREEZE_FEATURE.md"
  - "project_freeze_ledger/entries/"
do_not_touch_summary:
  - "Do not reintroduce hardcoded local absolute paths."
  - "Keep human guide and AI helper separate."
  - "Keep Markdown canonical until generated index tooling is implemented."
superseded_by: null
---
# freeze-20260612-project-freeze-ledger-v18

## freeze identity

```text
freeze id: freeze-20260612-project-freeze-ledger-v18
date: 2026-06-12
project box: project_freeze_ledger
freeze tier: tier 1 governance / baseline freeze
status: frozen after validation and user acceptance
```

## frozen version

```text
project_freeze_ledger v1.8 dynamic-path validation baseline
```

## summary

The `project_freeze_ledger` box is frozen as the project-wide Markdown freeze ledger with dynamic-path-compatible human and AI workflows.

This freeze supersedes the earlier `freeze-20260612-project-freeze-ledger-v1` baseline as the active project freeze ledger baseline, while keeping the v1 entry as historical evidence.

## what was implemented

The project freeze ledger now includes and separates these roles:

```text
project_freeze_ledger/readme_project_freeze_ledger.md
= governance explanation and freeze protocol

project_freeze_ledger/project_frozen_implemented_steps.md
= master dashboard of frozen implemented project baselines

project_freeze_ledger/send_to_ai_when_freezing_feature.md
= reusable AI-facing helper to freeze a completed feature

project_freeze_ledger/USER_READ_THIS_TO_UNDERSTAND_HOW_TO_FREEZE_FEATURE.md
= human-facing manual

project_freeze_ledger/entries/
= detailed freeze entries
```

The freeze guide and validation workflow were repaired so they use dynamic project-root logic rather than hardcoded local absolute paths.

The user also clarified the normal freeze input rule:

```text
When freezing a feature, send AI:
1. project_freeze_ledger/readme_project_freeze_ledger.md
2. project_freeze_ledger/project_frozen_implemented_steps.md
3. project_freeze_ledger/send_to_ai_when_freezing_feature.md

If touching an already frozen box, also send the relevant entry from:
project_freeze_ledger/entries/
```

## files and folders affected

Frozen box:

```text
project_freeze_ledger/
```

Frozen files in this baseline:

```text
project_freeze_ledger/readme_project_freeze_ledger.md
project_freeze_ledger/project_frozen_implemented_steps.md
project_freeze_ledger/send_to_ai_when_freezing_feature.md
project_freeze_ledger/USER_READ_THIS_TO_UNDERSTAND_HOW_TO_FREEZE_FEATURE.md
project_freeze_ledger/entries/
project_freeze_ledger/entries/freeze-20260612-phase7a-v24.md
project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v1.md
project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v18.md
```

Patch files used to install/validate this freeze:

```text
install_project_freeze_ledger_v18_freeze_box.ps1
validate_project_freeze_ledger_v18_freeze_box.ps1
```

## validation evidence summary

The user ran the dynamic-path freeze system validation and it passed.

Validated facts:

```text
1. project root was detected dynamically
2. required freeze ledger files existed
3. USER_READ guide used dynamic <project_root> paths
4. practical AI freeze helper was usable
5. master ledger referenced frozen entries and helper
6. no known broken old scripts were found in the project root
```

Validation result:

```text
VALIDATION OK
Freeze feature guide and project_freeze_ledger are readable, linked, and dynamic-path ready.
```

This freeze patch also includes a dedicated validation script for the v1.8 freeze-box baseline.

## behavioral tests

Not applicable as a runtime behavior test.

This is a governance/documentation/workflow freeze. The relevant evidence is file presence, link consistency, dynamic-path compatibility, and user acceptance.

## what is explicitly not included

This freeze does not include:

```text
runtime application logic changes
UI changes
startup delivery generator changes
prompt-routing algorithm changes
JSON mirror generation
compiled build output
item 15 implementation
```

This freeze does not make the ledger immutable forever. It only prevents casual or accidental changes without a new freeze/break-glass path.

## do-not-touch boundaries

Do not casually change:

```text
project_freeze_ledger/readme_project_freeze_ledger.md
project_freeze_ledger/project_frozen_implemented_steps.md
project_freeze_ledger/send_to_ai_when_freezing_feature.md
project_freeze_ledger/USER_READ_THIS_TO_UNDERSTAND_HOW_TO_FREEZE_FEATURE.md
project_freeze_ledger/entries/
```

Do not reintroduce:

```text
hardcoded local absolute paths in freeze docs
broken v1.2 PowerShell here-string scripts
broken v1.7 PowerShell scripts with param placed after executable statements
manual JSON mirror
duplicate freeze IDs
```

Keep this invariant:

```text
USER_READ_THIS_TO_UNDERSTAND_HOW_TO_FREEZE_FEATURE.md
= human guide

send_to_ai_when_freezing_feature.md
= AI-facing reusable freeze helper
```

## downstream dependencies

Future freeze tasks depend on this box to know:

```text
what files to send to AI
where freeze entries live
how to avoid changing frozen boxes casually
how to validate freeze-ledger consistency
how to preserve dynamic-path compatibility for future compilation
```

The startup delivery system freeze entry remains independently frozen:

```text
freeze-20260612-phase7a-v24
```

## exposure classification

```text
safe_for_targeted_ai_upload
```

Rationale:

```text
This freeze entry describes project governance, file roles, and validation rules.
It does not include full project source code, private keys, credentials, patient data, or proprietary implementation internals beyond file/folder names and workflow rules.
```

## external AI sharing rule

Safe to share with an external AI only for targeted work involving:

```text
freeze ledger updates
project governance
implementation baseline tracking
validation workflow repair
handoff/workflow explanation
```

Do not share full project ZIPs or unrelated source code unless specifically required and reviewed separately.

## rollback / break-glass protocol

To change this frozen baseline:

```text
1. read this freeze entry first
2. state exactly what must change and why
3. preserve the human-guide vs AI-helper separation
4. preserve dynamic <project_root> or project-root-relative paths
5. avoid hardcoded local absolute paths
6. implement the smallest possible patch
7. validate with a dynamic-path validation script
8. create a new freeze entry if the change is accepted
```

If the project freeze ledger becomes broken, restore from the most recent backup under:

```text
project_freeze_ledger/_backups/
```

or recover the last known freeze ZIP patch.

## next allowed step

The next allowed step is:

```text
use the three-file freeze input set for future feature freezes
```

The three-file freeze input set is:

```text
project_freeze_ledger/readme_project_freeze_ledger.md
project_freeze_ledger/project_frozen_implemented_steps.md
project_freeze_ledger/send_to_ai_when_freezing_feature.md
```

If the future task touches an already frozen box, also include the relevant entry from:

```text
project_freeze_ledger/entries/
```

Do not implement any new project feature from this freeze task alone.
