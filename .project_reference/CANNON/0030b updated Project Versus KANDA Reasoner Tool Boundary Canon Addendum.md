# Project Tool Boundary Canon

Version: 1.2
Status: Active prompt-library canon
Prompt ID: project_tool_boundary_canon
Prompt code: KPR-12-001
Owner group: 12_generalized_project_canons
Load type: routed

## Purpose

Preserve the canonical separation between the tool that performs AI-assisted work and the active project being worked on.

This canon exists because KANDA Reasoner can be both:

- the tool/runtime used to inspect, route, patch, validate, freeze, and hand off work;
- the active target project when the selected project is KANDA Reasoner itself.

Even when both names are the same in a given session, implementation logic must keep the two identities separate.

## Core rule

Never collapse tool identity into target project identity.

KANDA Reasoner is the reusable tool/runtime. The selected project in use is the active target project. The active target project may be KANDA Reasoner itself only when the human explicitly selects KANDA Reasoner as the project being worked on. Even in that self-hosting case, implementation logic must keep the two identities separate so the same code works for any other project later.

Tool/app logic remains in the KANDA Reasoner tool source. Project-specific support data lives under the active project's external support root. Do not copy reusable source files, prompt-library machinery, GUI code, validators, patch installers, or tool engines into project-specific support folders. Those folders contain handoff, freeze, Error Memory, or transient support data for one selected project only.

Use this model for implementation reasoning:

```text
tool_project_slug = kanda_reasoner
tool_source_root = KANDA Reasoner application source root
active_project_slug = selected project in use
active_project_root = selected project source root
active_project_support_root = <project_drive>/<active_project_slug>_show_project_to_AI
active_project_daily_work_root = <project_drive>/<active_project_slug>_delete_after_daily_work
```

KANDA Reasoner may contain the code that performs the behavior, but the behavior must target the active project in use unless the human explicitly selected KANDA Reasoner itself as the active project.

## Required implementation question

Before coding, patching, validating, freezing, or generating a handoff, ask:

```text
Am I modifying the KANDA Reasoner tool itself?
Or am I using the KANDA Reasoner tool to operate on the active target project?
```

If the answer is unclear, stop before mutation and resolve the active project root and active project slug.


## No-Leak tool/project rule

NO_LEAK_LOGIC_V1 applies to this canon whenever KANDA Reasoner is both the
reusable tool and the active project under work.

The rule is:

```text
Reusable tool engines, GUI tabs, analyzers, planners, validators, prompt
routing, patch delivery, startup delivery, freeze tooling, and source maps are
tool-owned. Concrete generated or refactored files for the selected active
project are project-owned.
```

Before any mutation, classify the target as tool-owned logic, active-project
source, project-specific support state, generated evidence, temporary
daily-work artifact, external dependency, or out-of-scope file.

Block the patch when reusable tool code would be installed into active-project
output/support paths, or when selected-project output would be installed into
reusable tool-source paths.

## Canonical identities

### Tool identity

The tool identity describes the reusable KANDA Reasoner runtime and its prompt/workflow infrastructure.

Examples:

```text
kanda_reasoner
kanda_prompt_workspace
project_freeze_ledger
Prompt Router Reasoner
Show Project to AI
patch delivery machinery
startup delivery machinery
```

Tool identity is allowed to own reusable engines, source maps, validators, GUI tabs, router logic, prompt library machinery, and reusable freeze tooling.

### Target project identity

The target project identity describes the selected project that the tool is currently helping with.

Examples:

```text
<my_project>
<active_project_root>
<active_project_slug>
<PROJECT_ROOT>
```

Target project identity owns project-specific source files, project-specific evidence, project-specific freeze intake, project-specific frozen memory, and project-specific handoff output.

## Required path rules

Use dynamic active-project paths for project-specific support state.

The following paths identify support-data locations for the selected active project, not reusable KANDA Reasoner source-code locations. The logic that creates, reads, validates, and migrates this content remains in the KANDA Reasoner tool.

```text
<project_drive>/<active_project_slug>_show_project_to_AI/first_prompt_files
<project_drive>/<active_project_slug>_show_project_to_AI/second_prompt_files
<project_drive>/<active_project_slug>_show_project_to_AI/project_error_memory
<project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake
<project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update/frozen_features_memory
<project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update/files_to_send_ai
<project_drive>/<active_project_slug>_show_project_to_AI/large_file_refactor_workbench
<project_drive>/<active_project_slug>_show_project_to_AI/large_file_refactor_workbench/preview/<preview_id>
<project_drive>/<active_project_slug>_delete_after_daily_work
<project_drive>/<active_project_slug>_delete_after_daily_work/large_file_refactor_shadow/<shadow_id>
```

Do not hardcode these paths to KANDA Reasoner unless KANDA Reasoner is explicitly the selected active project.

`second_prompt_files` is generated handoff output for the selected project in use. It is not automatically KANDA Reasoner tool state. Some selected projects may have PNG asset parts, while pure Python projects may not.

`active_project_root` is the editable source root for the selected project. It is not the same as `<active_project_slug>_show_project_to_AI`, `second_prompt_files`, or `<active_project_slug>_delete_after_daily_work`.

## Large File Refactor Workbench ownership

The Large File Refactor Workbench is implemented by reusable KANDA Reasoner tool code, but its project-specific durable workflow state belongs to the selected active project's external support root.

Canonical ownership:

```text
Tool-owned implementation:
<tool_source_root>/kanda_reasoner_app/manage_architecture/large_file_refactor_planner/...

Active-project source truth:
<active_project_root>/...

Durable Workbench project-support state:
<project_drive>/<active_project_slug>_show_project_to_AI/large_file_refactor_workbench/...

Canonical Preview runs:
<project_drive>/<active_project_slug>_show_project_to_AI/large_file_refactor_workbench/preview/<preview_id>/...

Disposable Shadow runs:
<project_drive>/<active_project_slug>_delete_after_daily_work/large_file_refactor_shadow/<shadow_id>/...
```

Preview and Shadow are not interchangeable.

- Preview is project-specific durable Workbench support state used for governed review and validation evidence. It is not active project source truth, but it must survive ordinary cleanup and must not live under daily-work.
- Shadow is a disposable execution/testing workspace. It may live under daily-work because it is regenerable garbage rather than canonical project support state.
- Structural validation reports, preflight readiness evidence, backup/recovery evidence associated with a Preview transaction, and final Workbench validation evidence belong under the selected project's Workbench support state unless a narrower owner canon explicitly assigns another durable project-support child.
- Patch ZIP staging, extraction, temporary installer backups, temporary helpers, temporary validation-evidence assembly, disposable Shadow workspaces, and other regenerable garbage belong under the selected project's daily-work root.

Daily-work is garbage-only. Never use `<active_project_daily_work_root>` as the authority for Preview truth, durable Workbench workflow state, canonical freeze memory, canonical Error Memory, or project source.

NO_LEAK_LOGIC_V1 must block wrong-root writes, Tool/Project leakage, cross-project support leakage, Preview-to-daily-work leakage, Shadow-to-durable-support promotion, private reach-in, hidden mutable state, public API ownership leakage, generated-artifact-as-source leakage, and validation/freeze evidence leakage.

## Common failure pattern

This is wrong:

```text
active project = kanda_reasoner
therefore every project freeze path, staging path, handoff path, validation path, and metadata path can be hardcoded to kanda_reasoner
```

This is correct:

```text
tool_project_slug remains kanda_reasoner
active_project_slug is resolved from the selected project
active_project_root is resolved from the selected project
durable project-specific support writes use active_project_support_root; disposable staging, Shadow workspaces, temporary validation assembly, and regenerable garbage only use active_project_daily_work_root
selected project source edits use active_project_root only when the task intentionally edits the selected project source
reusable tool writes use the owning KANDA Reasoner tool source path
```

## Required routing behavior

Load or apply this canon for any coding, patch, freeze, handoff, source-inspection, project-root, staging-path, or validation task where the implementation could confuse:

```text
KANDA Reasoner as the tool
KANDA Reasoner as the selected target project
another <my_project> as the selected target project
```

For ordinary implementation tasks, this canon is a boundary invariant and should be paired with the relevant implementation, box, patch, validation, or freeze prompt. It is not a replacement for those prompts.

## When to use

Use when the task involves:

- coding or patching behavior that uses a project root;
- freeze-intake or frozen-memory paths;
- patch staging or install folders;
- Show Project to AI handoff output;
- startup or router logic that mentions active project state;
- validation evidence tied to a project;
- Large File Refactor Workbench Preview, Shadow, preflight backup/readiness, rollback evidence, or final validation state;
- any question about whether Workbench state belongs in project support or daily-work;
- source inspection in a selected project;
- any change that might accidentally treat the tool project as every target project.

## When not to use

Do not load this canon for:

- simple explanations with no project mutation;
- medical writing or ordinary non-code drafting;
- UI color/style discussions without project-root, freeze, patch, handoff, or routing consequences;
- cases where another specialist prompt already covers the issue and no tool-vs-target ambiguity exists.

## Do-not-regress rules

- The selected active project root is the authority for project source. The selected active project support root is the authority for project-specific generated support state.
- The KANDA Reasoner tool root is not automatically the active target project root.
- Examples using `E:/kanda_reasoner` are examples only unless that project is selected.
- `project_freeze_ledger` remains reusable engine logic and must not store active project frozen memory.
- Freeze intake and frozen memory belong under `<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/`.
- Patch staging uses the active project drive and active project slug under the external daily-work root.
- Large File Refactor Workbench Preview runs belong under `<active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>`.
- Disposable Workbench Shadow runs belong under `<active_project_daily_work_root>/large_file_refactor_shadow/<shadow_id>`.
- Daily-work is garbage-only and must never own durable Preview truth or durable Workbench project-support state.
- Handoff output names, second_prompt_files, Error Memory, freeze memory, and evidence paths use the active project slug.
- Generated artifacts are not source truth for either the tool or the active project.
- Router decisions must preserve the distinction even when the tool and target project have the same slug.

## Merge-forbidden rule

Merging the KANDA Reasoner tool box with the selected project box is forbidden.

A patch may modify reusable KANDA Reasoner source only when the task is explicitly to change the KANDA Reasoner tool. A patch may modify another selected project's source only when the task is explicitly to change that selected project. Project-specific support files must stay in that selected project's external support folders.

The fact that KANDA Reasoner is currently being used to implement KANDA Reasoner does not remove this boundary. It is a self-hosting case, not a reason to hardcode KANDA Reasoner as every future project.

## Validation questions

- Did the implementation resolve `active_project_root` instead of assuming KANDA Reasoner?
- Did the implementation distinguish reusable tool paths from project-specific paths?
- Are freeze, handoff, staging, and validation outputs written under the active project context?
- Is Workbench Preview under project support while Shadow and regenerable garbage remain under daily-work?
- Does any durable Workbench state incorrectly depend on a daily-work path that routine cleanup can delete?
- Does any new prompt, script, help text, or installer imply that `kanda_reasoner` is always the selected project?
- If KANDA Reasoner is the selected project, does the code still work when a different project is selected later?
