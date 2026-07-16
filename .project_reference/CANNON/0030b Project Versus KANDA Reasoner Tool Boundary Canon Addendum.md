# Project Versus KANDA Reasoner Tool Boundary Canon Addendum

Status: canonical boundary clarification
Scope: all KANDA Reasoner coding, patching, validation, handoff, freeze, Error Memory, and Show Project to AI workflows

## Core rule

KANDA Reasoner as a tool and the selected project in use are separate logic boxes.

They may point to the same folder only when the user explicitly selects KANDA Reasoner itself as the active project. Even then, implementation must preserve the distinction so the same logic works for any other project later.

## Required identities

Use these identities separately:

```text
tool_project_slug = kanda_reasoner
tool_source_root = the KANDA Reasoner application source root

active_project_slug = selected project in use
active_project_root = selected project source root
active_project_support_root = <project_drive>\<active_project_slug>_show_project_to_AI
active_project_daily_work_root = <project_drive>\<active_project_slug>_delete_after_daily_work
```

## Selected project output folders

The following folders belong to the selected project in use:

```text
<project_drive>\<active_project_slug>_show_project_to_AI\first_prompt_files
<project_drive>\<active_project_slug>_show_project_to_AI\second_prompt_files
<project_drive>\<active_project_slug>_show_project_to_AI\project_error_memory
<project_drive>\<active_project_slug>_show_project_to_AI\project_freeze_after_update
<project_drive>\<active_project_slug>_delete_after_daily_work
```

These folders are not KANDA Reasoner tool folders unless the selected project is KANDA Reasoner itself.

## Editable source root

The editable source root is:

```text
active_project_root
```

It is not:

```text
<active_project_slug>_show_project_to_AI
<active_project_slug>_show_project_to_AI\second_prompt_files
<active_project_slug>_delete_after_daily_work
```

## Second prompt files rule

`second_prompt_files` is generated project handoff output for the selected project.

It may contain different package families depending on the selected project:

```text
<project_slug>__ai_handoff_upload*.zip
<project_slug>__source_archive_partXX_of_YY.zip
<project_slug>__png_assets_partXX_of_YY.zip
<project_slug>__error_memory_full.zip
<project_slug>__ai_handoff_all_in_one*.zip
```

PNG asset parts are optional and appear only when that selected project has PNG assets needed for exact reconstruction.

## Mutation rule

Before mutation, always ask:

```text
Am I modifying the reusable KANDA Reasoner tool?
Or am I using KANDA Reasoner to operate on the selected active project?
```

If modifying reusable KANDA Reasoner source code, patch files under the KANDA Reasoner source root.

If operating on another selected project, do not write reusable KANDA Reasoner code into that project.

If writing project-specific state, write under that selected project's external support root, not into the project source root.

## Freeze rule

Project-specific freeze intake and frozen memory belong under:

```text
<project_drive>\<active_project_slug>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake
<project_drive>\<active_project_slug>_show_project_to_AI\project_freeze_after_update\frozen_features_memory
```

They do not belong under:

```text
project_freeze_ledger
<active_project_root>\project_freeze_after_update
```

`project_freeze_ledger` is reusable KANDA Reasoner tool logic, not active project memory.

## Error Memory rule

Project-specific Error Memory belongs under:

```text
<project_drive>\<active_project_slug>_show_project_to_AI\project_error_memory
```

It does not belong in the KANDA Reasoner tool root unless KANDA Reasoner is the selected active project.

## Patch staging rule

Patch ZIPs and transient install artifacts must be staged under:

```text
<project_drive>\<active_project_slug>_delete_after_daily_work
```

They must not be placed in:

```text
active_project_root
active_project_root\tests
active_project_root\validation
active_project_root\kanda_reasoner_app
```

except for real source files intentionally installed by a validated patch.

## Validation rule

Boundary validation must prove that:

```text
KANDA Reasoner tool identity is separate from selected project identity.
_show_project_to_AI folders are generated support/output folders.
second_prompt_files belongs to the selected project handoff, not the tool.
freeze memory is external under the selected project's support root.
Error Memory is external under the selected project's support root.
daily work is external under the selected project's daily-work root.
validators do not hardcode kanda_reasoner as the selected project.
```

Successful validation must print:

```text
VALIDATION OK: project-tool-boundary-canon-v1
STATUS: IN_SYNC
```
"kanda_reasoner project" can be a project worked in "kanda_reasoner tool". CAsually we are using kanda_reasoner tool to
implement kanda_reasoner project  (the tool is building itself), but project could be <project>_other_project, so this division project tool must
be well undesrtood by the AI 