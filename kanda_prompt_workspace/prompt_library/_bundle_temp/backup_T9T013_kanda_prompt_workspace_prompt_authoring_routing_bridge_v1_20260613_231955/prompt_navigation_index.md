# Prompt Navigation Index

Version: 2.0
Status: active_candidate
Scope: KANDA Context Routing Layer - Phase 1 kernel
Owner box: Context Routing Kernel Box
Last updated: 2026-06-12

## Purpose

This index is the authoritative human-readable router for the KANDA prompt library.
It maps human intent to prompt groups and then to specialist prompts.
It routes context; it does not replace the real prompts.

## What this index does not do

- It does not contain the full specialist rules.
- It does not replace GROUP_ASSIMILATION_INDEX.md.
- It does not replace prompt_audit_canon.
- It does not replace box_architecture_canon.
- It does not create folder assimilation cards in Phase 1.
- It does not route to the live app or Tab Prompt Library GUI.

## Routing authority

This file is the primary readable router.

`prompt_router` may remain as a compatibility/helper prompt, but it must not become a second competing router.
If prompt_router conflicts with this index, this index wins until a human canon decision changes that.

Machine-readable routes are stored in:

```text
ROUTING/prompt_navigation_index.json
ROUTING/group_assimilation_index.json
```

## Required routing behavior

1. Read the human request as intent.
2. Decide whether Fast Path is enough.
3. If not Fast Path, identify required group route(s).
4. Use GROUP_ASSIMILATION_INDEX.md for group-level routing.
5. Request selected specialist prompts only when needed.
6. Use HARD STOP only when missing context blocks safe action.
7. Do not load all 12 folders at session start.

## Fast Path

Fast Path is allowed for:

- explanation
- discussion
- brainstorming
- reading-only review
- non-binding advice

Fast Path is not allowed for:

- code patches
- architecture changes
- prompt canon changes
- governance updates
- freeze decisions
- delivery ZIP generation
- validation classification

## Active prompt groups

| Group | Prompt count | Routing role |
|---|---:|---|
| 01_session_start_and_navigation | 9 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 02_prompt_routing_and_indexing | 4 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 03_governance_freeze_and_handoff | 6 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 04_box_architecture_and_boundaries | 4 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 05_patch_delivery_and_validation | 6 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 06_refactor_and_architecture_hardening | 7 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 07_prompt_authoring_and_audit | 3 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 08_python_engineering_core | 12 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 09_python_quality_security_observability | 7 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 10_python_api_data_async_config | 4 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 11_productization_and_release_readiness | 6 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 12_generalized_project_canons | 5 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |

## Task-to-group routing table

| Task trigger | Required groups | Optional groups | Missing behavior |
|---|---|---|---|
| start day / continue session | 01, 02 | 03 if continuing from handoff | STEP PAUSE if kernel missing |
| explain / discuss / brainstorm | none beyond loaded kernel | selected group only if needed | DEGRADED WARNING if evidence thin |
| create or modify code | 05 plus source files and validation steps; 04 if ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery are involved | 08, 09, 10 depending on task | HARD STOP before implementation |
| create a new folder with a databank | 04, 05, 09, 10 | 11 if production-ready storage | HARD STOP before implementation |
| large module / file over 500 lines | 04, 05, 06 | 08, 09 | HARD STOP before implementation |
| architecture decision | 04 | 06, 11, 12 | STEP PAUSE before canon/patch |
| prompt audit / prompt batch review | 02, 07 | 03 if deprecation/freeze, 12 if generalizing | STEP PAUSE until related prompts inspected |
| prompt conflict | 02, 07 | relevant groups containing both prompts | HARD STOP for canon decision |
| validation / freeze | 03, 05 | 04 if architecture touched | HARD STOP if validation output missing |
| handoff / checkpoint | 03 | 01, 02 | DEGRADED WARNING if work state missing |
| Python code quality / tests / logging | 05 plus source files and validation steps before patching | 08, 09, 11 depending on scope | STEP PAUSE before patch |
| API / async / config / database | 04, 05, 09, 10 | 11 | HARD STOP before implementation |
| release / productization / SRE | 05, 09, 11 | 10 | STEP PAUSE before patch |
| generalized project canon | 07, 12 | 02 | STEP PAUSE before canon update |


## Patch request required context

For patch, implementation, direct-fix, or bypass-patch requests, the AI must ask for the following before implementation:

Required prompts/groups:

1. 05_patch_delivery_and_validation - required because the user requested a patch.
2. Relevant project source files - required because implementation cannot proceed from memory.
3. Validation command or manual validation steps - required before any patch can be validated.
4. Relevant folder card or specialist prompt for the app area being patched.
5. 04_box_architecture_and_boundaries - required if the patch touches ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery.

Recommended prompts/groups:

1. 08_python_engineering_core.
2. 09_python_quality_security_observability.
3. box_architecture_canon if ownership or boundary decisions are involved.

ROUTING RESPONSE specificity rule for patch requests:

For patch requests, do not summarize these requirements generically. Name them explicitly in the ROUTING RESPONSE.

Required prompts/groups must explicitly include:

1. 05_patch_delivery_and_validation
2. Relevant project source files
3. Validation command or manual validation steps
4. Relevant folder card or specialist prompt for the app area being patched
5. 04_box_architecture_and_boundaries, when conditional boundary risk exists

Recommended prompts/groups must explicitly include:

1. 08_python_engineering_core
2. 09_python_quality_security_observability
3. box_architecture_canon if ownership or boundary decisions are involved

If the human explicitly asks to bypass routing, the bypass request does not reduce required context. The task remains Routed Work Path with HARD STOP before implementation.

## Required specialist prompts by condition

| Condition | Specialist prompt requirement |
|---|---|
| implementation, architecture, refactor, or ownership boundary | box_architecture_canon |
| code/file delivery, ZIP, install, validation, or freeze | bundle_gated_development_workflow or delivery/validation protocol |
| prompt audit, split, merge, deprecate, conflict, or generalization | prompt_audit_canon plus related prompt files |
| file above 500 lines | large_module_refactor_protocol |
| governance update | governance/freeze prompt plus validation evidence |
| continuation across sessions | current_workflow_handoff_template or latest handoff |

## Phase 1 rule

This Phase 1 kernel uses group-level routing only.
Do not require the 12 `_FOLDER_ASSIMILATION.md` cards until Phase 1 behavior is reviewed.
When Phase 2 begins, folder cards must remain routing metadata only.

## Missing prompt behavior

HARD STOP:
Use when missing context could cause unsafe implementation, wrong canon, invalid freeze, or architecture contamination.

STEP PAUSE:
Use when planning can proceed but implementation, freeze, or canon update must wait.

DEGRADED WARNING:
Use when discussion can proceed but evidence is incomplete.

## Standard NEED response

```text
This appears to be a <task type> task.
Routing decision: <Fast Path / Tier 1 group route / Tier 2 specialist payload>
Required groups:
- <group_id>: <reason>
Required prompts before action:
- <prompt_id>: <reason>
Missing-context level: <HARD STOP / STEP PAUSE / DEGRADED WARNING>
Next safe action: <proceed / roadmap / request files / wait>
```

## Final rule

The map is not the territory.
This index routes to prompts; the specialist prompts still own their detailed rules.



Startup delivery modification specificity rule:

Startup delivery modification requests are governed patch requests plus startup delivery maintenance. Do not list only zz_read_only_if_modifying_startup_delivery.md in Required prompts/groups. Do not summarize the patch requirements generically.

Name these startup delivery modification requirements explicitly in the ROUTING RESPONSE.

Required prompts/groups must explicitly include:

1. zz_read_only_if_modifying_startup_delivery.md
2. 05_patch_delivery_and_validation
3. Relevant project source files
4. Validation command or manual validation steps
5. Relevant folder card or specialist prompt for startup delivery
6. 04_box_architecture_and_boundaries, because startup delivery is boundary-sensitive

Recommended prompts/groups must explicitly include:

1. 08_python_engineering_core, if generator or Python code may be edited
2. 09_python_quality_security_observability
3. box_architecture_canon if ownership or boundary decisions are involved

For startup delivery modification requests, May proceed now must remain NO until the maintenance prompt, relevant source files, and validation path are provided.

Strict RG-010 output rule:
In the ROUTING RESPONSE for startup delivery modification requests, put all six startup delivery requirements under Required prompts/groups, not under Recommended prompts/groups.
Do not move 05_patch_delivery_and_validation, relevant project source files, validation command or manual validation steps, relevant folder card or specialist prompt for startup delivery, or 04_box_architecture_and_boundaries into Recommended prompts/groups.
May proceed now must be NO, not PARTIAL, until zz_read_only_if_modifying_startup_delivery.md plus the required source files and validation path are available.
Next safe action must request all missing required items before any patch creation or implementation.

Mandatory RG-010 exact response skeleton:
When the user scenario is a startup delivery modification request, the ROUTING RESPONSE must not use substitutes or softened labels. Use this structure exactly or semantically equivalent with the same labels under the same fields:

Required prompts/groups:
1. zz_read_only_if_modifying_startup_delivery.md
2. 05_patch_delivery_and_validation
3. Relevant project source files
4. Validation command or manual validation steps
5. Relevant folder card or specialist prompt for startup delivery
6. 04_box_architecture_and_boundaries, because startup delivery is boundary-sensitive

Recommended prompts/groups:
1. 08_python_engineering_core, if generator or Python code may be edited
2. 09_python_quality_security_observability
3. box_architecture_canon if ownership or boundary decisions are involved

May proceed now: NO

Do not answer May proceed now: PARTIAL for RG-010.
Do not place 05_patch_delivery_and_validation under Recommended prompts/groups.
Do not replace 05_patch_delivery_and_validation with generic wording such as Patch delivery and validation behavior.
Do not replace Relevant project source files with generic source context wording.
Do not replace 04_box_architecture_and_boundaries with generic boundary wording.
Do not count Startup delivery maintenance rule as a substitute for the six required items.
Missing context must explicitly mention the missing maintenance file, relevant project source files, validation command or manual validation steps, relevant startup delivery folder card or specialist prompt, and the boundary architecture prompt.

