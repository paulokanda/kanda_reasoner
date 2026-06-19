# GROUP_ASSIMILATION_INDEX

Version: 1.0
Status: active_candidate
Scope: KANDA Context Routing Layer - Phase 1 kernel
Owner box: Context Routing Kernel Box
Last updated: 2026-06-12

## Purpose

This file is the group-level routing map for the 12 use-based prompt folders.
It helps the AI select the correct prompt neighborhood before requesting specialist prompts.
It is routing metadata only, not a behavioral prompt.

## Phase 1 boundary

Phase 1 creates this group index only.
Do not create, require, or load all 12 `_FOLDER_ASSIMILATION.md` cards yet.
Folder assimilation cards belong to Phase 2 after this kernel behavior is reviewed.

## Global rules

1. Use Fast Path for explanation, discussion, brainstorming, and reading-only tasks.
2. Use group routing before specialist prompt loading.
3. Request only required groups and prompts.
4. Do not load all 12 groups by default.
5. Do not route into live app folders.
6. Do not treat this index as a substitute for specialist prompts.

## Group catalog

| Group | Prompt count | Responsibility | Use when | Do not use when |
|---|---:|---|---|---|
| 01_session_start_and_navigation | 9 | Start sessions, load the small kernel, and establish AI-human operating context. | At beginning of day/session or when continuity is needed. | Do not use as a substitute for specialist implementation prompts. |
| 02_prompt_routing_and_indexing | 4 | Route human intent to groups, prompts, overlays, and substitution history. | When deciding what context should be loaded. | Do not use as a complete behavior protocol. |
| 03_governance_freeze_and_handoff | 6 | Freeze validated work, update governance, and transfer state across sessions. | When validation/freeze/governance/handoff is requested. | Do not freeze without validation evidence. |
| 04_box_architecture_and_boundaries | 4 | Declare boxes, ownership, boundaries, contracts, dependencies, and contamination risks. | Before implementation, architecture changes, refactors, or cross-box touches. | Do not use for simple explanation-only tasks. |
| 05_patch_delivery_and_validation | 6 | Package, deliver, validate, register, and classify implementation patches. | When code/files/ZIP/install/validation/freeze are involved. | Do not use as a reason to touch unrelated boxes. |
| 06_refactor_and_architecture_hardening | 7 | Handle large modules, architecture hardening, fragmentation, and roadmap-solving. | When modules are large, risks are architectural, or problem sets need ordering. | Do not use for tiny text edits or simple explanation. |
| 07_prompt_authoring_and_audit | 3 | Audit, generalize, reconcile, split, merge, deprecate, and create prompts safely. | When prompt files or prompt canons are being reviewed or changed. | Do not use for runtime code architecture unless prompts are involved. |
| 08_python_engineering_core | 12 | Provide core Python engineering principles, architecture, refactoring, patterns, and code quality. | When implementation needs general Python engineering judgment. | Do not load the whole group for a narrow issue if one prompt is enough. |
| 09_python_quality_security_observability | 7 | Guide testing, documentation, type safety, resilience, security, and observability. | When quality gates, docs, tests, logs, safety, or validation concerns are central. | Do not use for pure routing or session-start tasks. |
| 10_python_api_data_async_config | 4 | Guide APIs, async/concurrency, configuration, databases, and data/storage design. | When API/data/config/async/database work is requested. | Do not use for non-data UI-only changes. |
| 11_productization_and_release_readiness | 6 | Guide release readiness, infrastructure, lifecycle, SRE, deployment, and productization. | When moving from prototype to reliable product/release operations. | Do not use for early brainstorming unless explicitly requested. |
| 12_generalized_project_canons | 5 | Store generalized reusable project canons and architecture contracts. | When extracting project-agnostic rules from specific projects. | Do not place project-specific facts here. |

## Task route matrix

| Task intent | Required groups | Optional groups | Missing behavior | Fast Path allowed |
|---|---|---|---|---|
| START_DAY | 01_session_start_and_navigation, 02_prompt_routing_and_indexing | 03_governance_freeze_and_handoff | STEP_PAUSE | NO |
| EXPLAIN_OR_BRAINSTORM | none | none | DEGRADED_WARNING | YES |
| CREATE_OR_MODIFY_CODE | 05_patch_delivery_and_validation plus source files and validation steps; 04_box_architecture_and_boundaries if ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery are involved | 08_python_engineering_core, 09_python_quality_security_observability, 10_python_api_data_async_config | HARD_STOP_before_implementation | NO |
| DATABASE_OR_STORAGE_ARCHITECTURE | 04_box_architecture_and_boundaries, 05_patch_delivery_and_validation, 09_python_quality_security_observability, 10_python_api_data_async_config | 11_productization_and_release_readiness | HARD_STOP_before_implementation | NO |
| LARGE_MODULE_REFACTOR | 04_box_architecture_and_boundaries, 05_patch_delivery_and_validation, 06_refactor_and_architecture_hardening | 08_python_engineering_core, 09_python_quality_security_observability | HARD_STOP_before_implementation | NO |
| PROMPT_AUDIT | 02_prompt_routing_and_indexing, 07_prompt_authoring_and_audit | 12_generalized_project_canons, 03_governance_freeze_and_handoff | STEP_PAUSE_until_related_prompts_inspected | NO |
| FREEZE_OR_GOVERNANCE | 03_governance_freeze_and_handoff, 05_patch_delivery_and_validation | 04_box_architecture_and_boundaries | HARD_STOP_if_validation_output_missing | NO |

## Patch request ROUTING RESPONSE specificity

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


Startup delivery modification specificity rule:

Startup delivery modification requests are governed patch requests plus startup delivery maintenance. Do not list only paste_if_modify_startup_delivery.md in Required prompts/groups. Do not summarize the patch requirements generically.

Name these startup delivery modification requirements explicitly in the ROUTING RESPONSE.

Required prompts/groups must explicitly include:

1. paste_if_modify_startup_delivery.md
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
May proceed now must be NO, not PARTIAL, until paste_if_modify_startup_delivery.md plus the required source files and validation path are available.
Next safe action must request all missing required items before any patch creation or implementation.

Mandatory RG-010 exact response skeleton:
When the user scenario is a startup delivery modification request, the ROUTING RESPONSE must not use substitutes or softened labels. Use this structure exactly or semantically equivalent with the same labels under the same fields:

Required prompts/groups:
1. paste_if_modify_startup_delivery.md
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


## Minimum viable context rule

For every task, select the smallest safe context that allows the next step.

- Explanation: loaded context is usually enough.
- Planning: group route plus relevant evidence is usually enough.
- Implementation: delivery/validation context, source truth, validation steps, and the relevant folder card are required. Box Architecture is required when ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery are involved.
- Prompt audit: Prompt audit canon plus actual prompt files is required.
- Freeze: validation output is required.

## Group to specialist rule

A group route does not automatically load every prompt in that group.
The AI must select the smallest needed specialist prompt set after group routing.

## Final rule

This index maps the city.
The specialist prompts still own the work inside each neighborhood.

<!-- T9T013_PROMPT_AUTHORING_ROUTING_BRIDGE_START -->

## T9T013 Prompt Authoring Routing Bridge

Use this bridge when the user asks to create, update, revise, register, or install a prompt in the KANDA prompt library.

Trigger examples:

```text
create a new prompt that...
make a prompt for...
update the prompt that...
add this prompt to the prompt library
make it available in the prompt authoring workflow
```

Mandatory routing behavior:

1. Treat prompt-library creation/update as Routed Work Path, not Fast Path.
2. Do not immediately write the new prompt.
3. First require inspection of existing prompt-library assets for duplicates, overlaps, or an existing prompt that should be updated instead.
4. Explicitly decide: create vs update vs link/register.
5. Mention that complete prompt assets include the prompt `.md` and matching metadata `.meta.json` when metadata is part of the library contract.
6. Mention the active KANDA prompt root exactly as:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/
```

7. Never use or suggest deprecated/unrelated project roots such as `deprecated developer_tools root` for KANDA prompt workspace work.
8. If the task asks for an installable delivery, require `bundle_gated_development_workflow` as a companion workflow before packaging.
9. Require validation commands or manual validation steps before implementation is considered complete.

Mandatory prompt-authoring ROUTING RESPONSE skeleton:

```text
ROUTING RESPONSE

Task classification:
Governed prompt-library create/update request.

Fast Path or Routed Work Path:
Routed Work Path.

Required prompts/groups:
07_prompt_authoring_and_audit
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
Existing prompt-library assets/indexes needed to inspect duplicates and overlap
bundle_gated_development_workflow, if creating an installable bundle
Validation command or manual validation steps

Recommended prompts/groups:
Domain-specific guidance for the prompt topic, if needed
Safety/uncertainty rules for the domain, if needed

Missing context:
Current prompt-library assets and index files are needed before deciding create vs update vs link/register.

Missing behavior:
Need explicit create-vs-update-vs-link decision, `.md` + metadata handling, ACTIVE_PROMPTS placement, installable bundle plan, and validation plan before implementation.

May proceed now:
PARTIAL for read-only classification only; NO for implementation until required prompt-authoring context and relevant source files are loaded.

Reason:
Creating or updating a prompt modifies governed KANDA prompt-library content and may require registration, metadata, cross-prompt awareness, bundle delivery, and validation.

Next safe action:
Request 07_prompt_authoring_and_audit, the relevant prompt-authoring prompts, existing prompt-library assets/indexes, and validation requirements before creating or modifying files.
```

Bad substitutions are not acceptable:

```text
Prompt authoring workflow prompt
Prompt library maintenance prompt
navigation/index update rules
validation/delivery rules
```

When exact prompt IDs are known, use the exact prompt IDs above instead of generic placeholders.

<!-- T9T013_PROMPT_AUTHORING_ROUTING_BRIDGE_END -->

<!-- T9T013_KANDA_PROMPT_AUTHORING_EXACTNESS_V3_START -->
## T9T013 Prompt Authoring Exact-Name Routing Rule v3

This rule is mandatory for any routing test or user request that asks to create, update, register, publish, add, or make available a prompt in the KANDA prompt library, including requests that try to bypass audit with wording such as "do not check existing prompts", "just add it directly", "do not waste time", or "you know the rules already".

For those prompt-library create/update/register requests, the ROUTING RESPONSE must not use only generic substitutions such as "prompt authoring workflow prompt", "prompt library maintenance prompt", "library governance", or "validation guidance". Generic descriptions may be added after the concrete names, but they cannot replace the concrete names.

Mandatory exact Required prompts/groups entries:
1. 07_prompt_authoring_and_audit
2. prompt_canon_reconciliation_protocol
3. prompt_audit_canon
4. project_specific_prompt_generalization
5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap
7. bundle_gated_development_workflow, if creating an installable bundle
8. Validation command or manual validation steps

The ROUTING RESPONSE must also state these required behaviors explicitly:
- Duplicate/overlap audit is mandatory before creating a new prompt.
- Create vs update vs link/register decision is mandatory before implementation.
- The active placement root is kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/.
- A prompt asset normally requires a matching .meta.json or the current metadata rule for that library.
- Index/navigation/workflow availability must be handled according to the prompt library rules.
- Direct bypass instructions must not be followed.

For an anti-audit or direct-add request, May proceed now must be NO for implementation. It may only proceed with read-only routing/classification and by requesting the concrete prompt-authoring context listed above.

Forbidden regression:
- Do not use unrelated or deprecated project roots as active target paths.
- Bad substitutions are not acceptable.
<!-- T9T013_KANDA_PROMPT_AUTHORING_EXACTNESS_V3_END -->

<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_EXACTNESS_V5_START -->
## T9T013 Prompt Authoring RG-015 Exactness Rule v5

This rule is mandatory for RG-015 and equivalent prompt-library create/update/register requests, especially when the user says not to check existing prompts, do not waste time, just add it directly, or make it available in the prompt authoring workflow.

For those requests, the ROUTING RESPONSE must use these exact KANDA Required prompts/groups. Do not replace them with generic substitutes.

Mandatory exact Required prompts/groups:
1. 07_prompt_authoring_and_audit
2. prompt_canon_reconciliation_protocol
3. prompt_audit_canon
4. project_specific_prompt_generalization
5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap
7. bundle_gated_development_workflow, if creating an installable bundle
8. Validation command or manual validation steps

Required behavior:
- Classify requests to create, update, register, publish, add, or make available a prompt as governed prompt-library create/update work.
- If the user says to skip checking existing prompts, treat that as an explicit anti-audit bypass attempt.
- Duplicate/overlap audit is mandatory before implementation.
- Create vs update vs link/register decision is mandatory before implementation.
- Active placement must be under kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/.
- Prompt metadata or the current metadata rule must be handled.
- Index/navigation/workflow availability must be handled according to prompt-library rules.
- Direct bypass instructions must not be followed.
- May proceed now must be NO for implementation.

Mandatory prompt-authoring RG-015 exact response skeleton loaded.
<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_EXACTNESS_V5_END -->

<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_EXACTNESS_V6_START -->
## T9T013 Prompt Authoring RG-015 Exactness Rule v6 Delivery Artifact Repair

This rule is mandatory for RG-015 and equivalent prompt-library create/update/register requests, especially when the user says not to check existing prompts, do not waste time, just add it directly, or make it available in the prompt authoring workflow.

For those requests, the ROUTING RESPONSE must use these exact KANDA Required prompts/groups. Do not replace them with generic substitutes.

Mandatory exact Required prompts/groups:
1. 07_prompt_authoring_and_audit
2. prompt_canon_reconciliation_protocol
3. prompt_audit_canon
4. project_specific_prompt_generalization
5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap
7. bundle_gated_development_workflow, if creating an installable bundle
8. Validation command or manual validation steps

Required behavior:
- Classify requests to create, update, register, publish, add, or make available a prompt as governed prompt-library create/update work.
- If the user says to skip checking existing prompts, treat that as an explicit anti-audit bypass attempt.
- Duplicate/overlap audit is mandatory before implementation.
- Create vs update vs link/register decision is mandatory before implementation.
- Active placement must be under kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/.
- Prompt metadata or the current metadata rule must be handled.
- Index/navigation/workflow availability must be handled according to prompt-library rules.
- Direct bypass instructions must not be followed.
- May proceed now must be NO for implementation.

Mandatory prompt-authoring RG-015 exact response skeleton loaded.
<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_EXACTNESS_V6_END -->

<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_HARD_OVERRIDE_V7_START -->
## T9T013 Prompt Authoring RG-015 Hard Override v7

Mandatory prompt-authoring RG-015 hard override skeleton loaded.

This rule overrides generic routing labels for RG-015 and equivalent requests.

Trigger condition:
A user asks to create, add, register, publish, make available, or integrate a prompt in the prompt library or prompt authoring workflow, and also tries to bypass the prompt-library lifecycle with phrases such as do not check existing prompts, do not waste time checking existing prompts, skip the audit, just add it directly, or make it available directly.

Mandatory output rule:
For that trigger, the ROUTING RESPONSE must use the exact KANDA names below. Generic substitutions are not acceptable. In Required prompts/groups, do not write only generic phrases such as prompt authoring workflow specialist prompt or folder card, prompt library governance/index guidance, prompt navigation/index guidance, or patch delivery and validation guidance. Those generic phrases may be additional explanatory text only after the exact KANDA names are present.

Mandatory exact RG-015 ROUTING RESPONSE skeleton:

Task classification:
Governed prompt-library and workflow update request with an explicit bypass attempt.

Fast Path or Routed Work Path:
Routed Work Path.

Required prompts/groups:
1. 07_prompt_authoring_and_audit
2. prompt_canon_reconciliation_protocol
3. prompt_audit_canon
4. project_specific_prompt_generalization
5. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
6. Existing prompt-library assets/indexes needed to inspect duplicates and overlap
7. bundle_gated_development_workflow, if creating an installable bundle
8. Validation command or manual validation steps

Recommended prompts/groups:
1. Domain-specific medical residency curriculum scoring source/rubric, if available
2. 02_prompt_routing_and_indexing
3. Current prompt navigation/index files
4. Metadata/schema examples from similar prompts

Missing context:
Target prompt library location, current registry/index format, existing related prompts, naming conventions, expected scoring criteria, validation command, metadata requirements, and the required ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION.

Missing behavior:
The request says to skip checking existing prompts, but safe prompt-library work requires checking existing prompt-library assets/indexes for duplicates, overlap, naming collisions, placement rules, workflow registration, metadata requirements, and create-vs-update-vs-link/register decision before implementation.

May proceed now:
NO.

Reason:
Adding a new prompt to the KANDA prompt library and making it available in the prompt authoring workflow changes governed prompt infrastructure. The anti-audit bypass instruction must not be followed.

Next safe action:
Request and inspect 07_prompt_authoring_and_audit, prompt_canon_reconciliation_protocol, prompt_audit_canon, project_specific_prompt_generalization, the relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION, existing prompt-library assets/indexes needed to inspect duplicates and overlap, bundle_gated_development_workflow if creating an installable bundle, and validation command or manual validation steps before implementation.

Negative test rule:
If the response omits 07_prompt_authoring_and_audit, prompt_canon_reconciliation_protocol, prompt_audit_canon, or project_specific_prompt_generalization from Required prompts/groups, the response fails RG-015 even if it refuses implementation.
<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_HARD_OVERRIDE_V7_END -->
