<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_FIRST_POSITION_OVERRIDE_V8_START -->
## RG-015 FIRST-POSITION EXACT OVERRIDE

Mandatory prompt-authoring RG-015 first-position hard override loaded.

WHEN THE USER SCENARIO ASKS TO CREATE/ADD/REGISTER A NEW PROMPT AND ALSO SAYS TO SKIP CHECKING EXISTING PROMPTS, DO NOT USE GENERIC ROUTING LABELS.

OUTPUT THIS EXACT ROUTING RESPONSE SHAPE FIRST:

ROUTING RESPONSE

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

FAIL CONDITIONS FOR RG-015:
- FAIL if Required prompts/groups uses only generic labels such as prompt authoring workflow specialist prompt or folder card.
- FAIL if Required prompts/groups omits 07_prompt_authoring_and_audit.
- FAIL if Required prompts/groups omits prompt_canon_reconciliation_protocol.
- FAIL if Required prompts/groups omits prompt_audit_canon.
- FAIL if Required prompts/groups omits project_specific_prompt_generalization.
<!-- T9T013_KANDA_PROMPT_AUTHORING_RG015_FIRST_POSITION_OVERRIDE_V8_END -->

# GROUP_ASSIMILATION_INDEX

Version: 1.1
Status: active_candidate
Scope: KANDA Context Routing Layer - Phase 1 kernel
Owner box: Context Routing Kernel Box
Last updated: 2026-06-15

## Purpose

This file is the group-level routing map for the 12 use-based prompt folders.
It helps the AI select the correct prompt neighborhood before requesting specialist prompts.
It is routing metadata only, not a behavioral prompt.

## Phase boundary and current use

This file remains the group-level router.
Folder assimilation cards now exist as selected-when-needed Phase 2 support files.
Do not load all folder cards at startup.
Use folder cards only after group routing narrows the task to one or more relevant groups.

## Global rules

1. Use Fast Path for explanation, discussion, brainstorming, and reading-only tasks.
2. Use group routing before specialist prompt loading.
3. Request only required groups and prompts.
4. Do not load all 12 groups by default.
5. Do not route into live app folders.
6. Do not treat this index as a substitute for specialist prompts.

## Retired routing identity rule

`prompt_router`, RG-PILOT-000, and RG-LAB-000 are not active group routes. Resolve them through KPR-02-005. Current semantic, Pilot, Copilot, LAB, MLRT, provider, or ML-routing proposals use KPR-02-006 plus KPR-02-002 and Brick Wall admission.

## Routing-index escalation discipline

Use the three routing indexes in a deliberate escalation order.

1. Start here, with `GROUP_ASSIMILATION_INDEX.md`, to identify the broad prompt group or groups required by the task.
2. Escalate to `FOLDER_ASSIMILATION_CARDS_INDEX.md` only when the broad group is known but the exact folder card, sub-area, or group-specific context is ambiguous.
3. Escalate to `prompt_navigation_index.md` only when the exact prompt file, prompt ID, route, companion prompt, or current path must be selected or verified.
4. Do not read or request all three indexes by default for every task. Use the smallest index set that makes the route safe and current.
5. If the indexes disagree, stop and flag `ROUTING_INDEX_CONFLICT` instead of guessing.
6. For Fast Path tasks, do not escalate beyond the loaded startup kernel unless the answer would otherwise rely on stale or missing project-specific context.

## Group catalog

| Group | Prompt count | Responsibility | Use when | Do not use when |
|---|---:|---|---|---|
| 01_session_start_and_navigation | 11 | Compact startup, two-stage readiness, closure, Error Memory admission, durable-artifact routing, overlays, and templates. | At startup, continuation, upload review, closure, Error Memory admission, durable routing, or startup authoring. | Do not use as implementation, patch-registry, or freeze authority. |
| 02_prompt_routing_and_indexing | 6 | Select current routing owners, exact prompt paths, Project overlays, historical substitutions, and semantic/ML adoption safety. | When deciding what context should be loaded, resolving an old prompt identity, or evaluating a current KANDA semantic/ML proposal. | Do not use as a complete behavior protocol. |
| 03_governance_freeze_and_handoff | 8 | Own Brick Wall status, cooperative decisions, freeze intake, strict AI freeze-candidate pre-output audit, self-contained freeze intake, final artifact dispatch, and draft-only governance or handoff profiles. | Use for governed implementation status, freeze intake, AI freeze-candidate audit, self-contained freeze intake, consequential option discussion, final operational artifact checks, or explicit generic profile drafting. | Do not use as a substitute for specialist implementation, delivery, validation, Box, Tool/Project, Error Memory, or normal KANDA handoff owners. |
| 04_box_architecture_and_boundaries | 6 | Declare boxes, ownership, boundaries, contracts, dependencies, contamination risks, KBSC shield requirements, and route the governed architecture companion on demand. | Before implementation, architecture changes, refactors, cross-box touches, meaningful milestone shielding, or stronger ML preparation. | Do not use for simple explanation-only tasks. |
| 05_patch_delivery_and_validation | 8 | Coordinate release lifecycle, surgical delivery, active PIR routing, correction incidents, terminal behavior, recovery dispatch, and self-contained Error Memory intake. | When packaging, installing, validating, correcting, emitting terminal output, or preparing the governed Error Memory intake ZIP. | Do not use as implementation, Freeze, or Architecture Review MCard authority. |
| 06_refactor_and_architecture_hardening | 8 | Current architecture/refactor owners plus bounded Web-AI planning, bundle, AST-repair, and Safe Refactor specialist routes. | When current structural evidence requires a Class 06 owner or specialist. | Do not let specialist prompts replace KPR-06-007, Class 05, Brick Wall, or human-confirmed freeze. |
| 07_prompt_authoring_and_audit | 3 | Audit, generalize, reconcile, split, merge, deprecate, and create prompts safely. | When prompt files or prompt canons are being reviewed or changed. | Do not use for runtime code architecture unless prompts are involved. |
| 08_python_engineering_core | 10 | Python-specific architecture, refactoring, patterns, performance, legacy-code, and maintainability specialists. | When Python source or Python-system design needs one selected specialist. | Do not use for team-process advice or source-grounded handbook generation; use Class 12. |
| 09_python_quality_security_observability | 17 | Guide testing, documentation, type safety, resilience, security, observability, and evidence-first anti-hallucination review. | When quality gates, docs, tests, logs, safety, validation, unsupported AI assumptions, or evidence verification concerns are central. | Do not use for pure routing or session-start tasks. |
| 10_python_api_data_async_config | 4 | Guide APIs, async/concurrency, configuration, databases, and data/storage design. | When API/data/config/async/database work is requested. | Do not use for non-data UI-only changes. |
| 11_productization_and_release_readiness | 6 | Guide release readiness, infrastructure, lifecycle, SRE, deployment, and productization. | When moving from prototype to reliable product/release operations. | Do not use for early brainstorming unless explicitly requested. |
| 12_generalized_project_canons | 14 | Reusable generalized canons and templates, including Tool/Project identity, MCard lifecycle, Error Memory models, human-process guidance, and source-grounded handbook generation. | When one selected generalized canon or template is required. | Do not use as generic implementation, personnel-action, medical-diagnosis, surveillance, package, or freeze authority. |





## KANDA Routing System Canon route

Use `kanda_routing_system_canon` from `02_prompt_routing_and_indexing` when routing-system behavior itself is being changed, canonized, audited, or frozen; when Context Package Manifest or Prompt Registration v2 rules are being defined; when prompt insertion must be corrected to prompt registration; or when advisory similarity output must be kept separate from final routing authority.

The routing canon is on-request and must not become an always-loaded startup prompt. Pair it with current routing indexes, `ai_prompt_request_canon`, validation steps, and KBSC when shielding or authority-boundary protection is involved.

## KANDA Box Shielding Canon route

Use `kanda_box_shielding_canon` from `04_box_architecture_and_boundaries` when the user asks to create, improve, canonize, audit, or implement shielding logic; when a meaningful box milestone must be protected before continuing; when stronger ML/probabilistic behavior is being considered; or when advisory output may creep into routing authority.

KBSC is an on-request shielding canon. It must not be loaded for simple Fast Path explanation-only tasks. It must be paired with the owning box context, validation path, and patch-delivery rules when implementation is requested.

## Task route matrix

| Task intent | Required groups | Optional groups | Missing behavior | Fast Path allowed |
|---|---|---|---|---|
| START_DAY | 01_session_start_and_navigation, 02_prompt_routing_and_indexing | 03_governance_freeze_and_handoff | STEP_PAUSE | NO |
| EXPLAIN_OR_BRAINSTORM | none | none | DEGRADED_WARNING | YES |
| CREATE_OR_MODIFY_CODE | 05_patch_delivery_and_validation plus source files and validation steps; 04_box_architecture_and_boundaries if ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery are involved | 08_python_engineering_core, 09_python_quality_security_observability, 10_python_api_data_async_config | HARD_STOP_before_implementation | NO |
| GOVERNED_ARCHITECTURE_COMPANION | governed_architecture_companion_handoff, brick_wall_comprehensive_quality_gate, brick_wall_comprehensive_quality_gate, project_tool_boundary_canon, box_architecture_canon | kanda_box_shielding_canon and architecture_review_project_card_machine_canon only when triggered | HARD_STOP_before_implementation_if_canonical_owners_or_Brick_Wall_authorization_are_incomplete | NO |
| DATABASE_OR_STORAGE_ARCHITECTURE | 04_box_architecture_and_boundaries, 05_patch_delivery_and_validation, 09_python_quality_security_observability, 10_python_api_data_async_config | 11_productization_and_release_readiness | HARD_STOP_before_implementation | NO |
| LARGE_MODULE_REFACTOR | 04_box_architecture_and_boundaries, 05_patch_delivery_and_validation, 06_refactor_and_architecture_hardening | 08_python_engineering_core, 09_python_quality_security_observability | HARD_STOP_before_implementation | NO |
| PILOT_COPILOT_PHASE0_POST_M35 | 02_prompt_routing_and_indexing, routing_signal_scorer_v3_pilot_copilot_phase0_router_canon, kanda_routing_system_canon, kanda_box_shielding_canon; 05 plus current project files and validation steps if patching | 04_box_architecture_and_boundaries, 03_governance_freeze_and_handoff, 08_python_engineering_core, 09_python_quality_security_observability | HARD_STOP_before_implementation; PARTIAL_for_read_only_review; P0 only until frozen | NO |
| POST_P12_LAB_PHASE_ENTRY_OR_ML_ROUTER_RELIABILITY | 02_prompt_routing_and_indexing, routing_signal_scorer_v3_lab_phase_entry_router_canon, routing_signal_scorer_v3_pilot_copilot_phase0_router_canon, kanda_routing_system_canon, kanda_box_shielding_canon; 05 plus current project files and validation steps if patching | 04_box_architecture_and_boundaries, 03_governance_freeze_and_handoff, 08_python_engineering_core, 09_python_quality_security_observability | HARD_STOP_before_ML_implementation; PARTIAL_for_RG_LAB_000_review; LAB-0 only after RG-LAB-000 freeze | NO |
| ROUTING_SYSTEM_CANON_OR_CONTEXT_PACKAGE_MANIFEST | 02_prompt_routing_and_indexing, kanda_routing_system_canon, ai_prompt_request_canon, current routing indexes, 07_prompt_authoring_and_audit if prompt assets are updated, validation command or manual validation steps | 04_box_architecture_and_boundaries, kanda_box_shielding_canon, 03_governance_freeze_and_handoff | HARD_STOP_before_implementation; PARTIAL_for_read_only_review | NO |
| BOX_SHIELDING_OR_STRONGER_ML_PREP | 04_box_architecture_and_boundaries, kanda_box_shielding_canon, 05_patch_delivery_and_validation if patching, relevant owning-box source files/tests, validation command or manual validation steps | 03_governance_freeze_and_handoff, 08_python_engineering_core, 09_python_quality_security_observability | HARD_STOP_before_implementation; PARTIAL_for_architecture_discussion_only | NO |
| PROMPT_AUDIT | 02_prompt_routing_and_indexing, 07_prompt_authoring_and_audit | 12_generalized_project_canons, 03_governance_freeze_and_handoff | STEP_PAUSE_until_related_prompts_inspected | NO |
| BRICK_WALL_STATUS_CHECK | brick_wall_comprehensive_quality_gate, 03_governance_freeze_and_handoff | project_tool_boundary_canon, box_architecture_canon, kanda_box_shielding_canon; other companions only when applicable | HARD_STOP_before_coding_if_mandatory_pre_code_items_incomplete | NO |
| FREEZE_OR_GOVERNANCE | 03_governance_freeze_and_handoff, 05_patch_delivery_and_validation | 04_box_architecture_and_boundaries | HARD_STOP_if_validation_output_missing | NO |
| FREEZE_CODE_AFTER_PATCH | freeze_code_intake_and_form_protocol, freeze_candidate_pre_output_audit, 03_governance_freeze_and_handoff, 05_patch_delivery_and_validation | 04_box_architecture_and_boundaries, cooperative_implementation_methodology | HARD_STOP_if_validation_output_missing_or_freeze_hint_data_is_stale | NO |
| PRE_OUTPUT_ARTIFACT_CONTRACT | pre_output_contract_gates, 03_governance_freeze_and_handoff, 05_patch_delivery_and_validation | freeze_code_intake_and_form_protocol, freeze_candidate_pre_output_audit, 09_python_quality_security_observability | HARD_STOP_if_artifact_contract_missing_or_output_would_violate_canon | NO |
| FREEZE_FEATURE_GUI_OR_LOCAL_WRITER_CHANGE | 09_active_project_freeze_context, 04_box_architecture_and_boundaries, cooperative_implementation_methodology, 05_patch_delivery_and_validation, relevant freeze_after_update source files, validation command or manual validation steps | 08_python_engineering_core and 09_python_quality_security_observability when source/validation/safety code may be modified | HARD_STOP_before_implementation; NO if human confirmation bypass is requested | NO |


## Pre-output contract gates routing hook


## Brick Wall Q01-Q40 status route

Use `brick_wall_comprehensive_quality_gate` when the user says `brick wall` or requests the live governed implementation status. The prompt is routed and must display the current evidence-backed status plus the Q01-Q40 ledger before any implementation code. It coordinates but does not replace Tool/Project, Box, shielding, MCard, delivery, freeze, or Error Memory owner prompts.

When the task will produce PowerShell or terminal code, patch ZIP delivery instructions, validation commands, freeze-form JSON, validation evidence intended for freezing, `KANDA_FREEZE_HINT.json`, or multi-project freeze path decisions, request or apply `pre_output_contract_gates` from `03_governance_freeze_and_handoff` immediately before emitting the artifact.

This hook is output-time compliance, not a router replacement. Do not load it for simple Fast Path explanation-only tasks.

## Freeze code intake and form protocol routing hook

When the task involves freezing code, preparing a freeze form, reviewing a freeze formulary, delivering a freeze-ready patch ZIP, or using `KANDA_FREEZE_HINT.json`, request `freeze_code_intake_and_form_protocol` from `03_governance_freeze_and_handoff`. Before the AI emits, approves, corrects, or regenerates a local Freeze GUI candidate/form, also request `KPR-03-008 freeze_candidate_pre_output_audit`.

This prompt is required because the AI chat knows the current feature title, validation evidence, protected paths, and do-not-regress rules, while the local app can otherwise fall back to stale heuristics.

Do not proceed with freeze form approval if the feature title or validation evidence belongs to an older feature. For multi-project work, verify that freeze-intake state and frozen memory are under the selected active project root, not a global KANDA Reasoner root.

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


## Minimum viable context rule

For every task, select the smallest safe context that allows the next step.

- Explanation: loaded context is usually enough.
- Planning: group route plus relevant evidence is usually enough.
- Implementation: delivery/validation context, source truth, validation steps, and the relevant folder card are required. Box Architecture is required when ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery are involved.
- Prompt audit: Prompt audit canon plus actual prompt files is required.
- Freeze: validation output is required.

- Freeze Feature After Update GUI/local-writer changes: exact prompt-call package is required. Request 09_active_project_freeze_context, 04_box_architecture_and_boundaries, cooperative_implementation_methodology, 05_patch_delivery_and_validation, relevant freeze_after_update source files, and validation steps. Add 08_python_engineering_core and 09_python_quality_security_observability when source, validation, safety, or write behavior may change. Do not proceed if the request bypasses explicit human confirmation for freeze writes.

- RG-028 complete-pass rule: `rg028_freeze_workflow_context_package_v1` is a route/checkpoint label, not a replacement for the Required prompts/groups list. A complete response must expand and name the actual package: 09_active_project_freeze_context; 04_box_architecture_and_boundaries; cooperative_implementation_methodology; 05_patch_delivery_and_validation; 08_python_engineering_core; 09_python_quality_security_observability; relevant freeze_after_update GUI/app/contract/local-writer source files; and validation command/manual validation steps. For a Confirm-and-Write bypass request, Estimated context load must be large and May proceed now must be NO.

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

7. Never use or suggest deprecated/unrelated legacy project roots for KANDA prompt workspace work.
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

<!-- ERROR_MEMORY_ACTIVE_READY_CORRECTION_GROUP_ROUTE_V1_START -->
## Error Memory active-ready correction group route

Use `error_memory_active_ready_correction_blueprint` from `12_generalized_project_canons` when a task asks to convert, correct, promote, or validate a `KANDA_ERROR_LESSON_JSON` draft so it can become active-ready or active.

This route is a routed bridge. It must not become an always-loaded startup prompt. Pair it with `prompt_navigation_index` and `prompt_router`. If the task also changes prompt-library assets, also use `07_prompt_authoring_and_audit` and the prompt insertion/router registration protocol.

Do not use this route for Error Memory GUI implementation patches unless the task also involves lesson JSON draft-to-active correction.
<!-- ERROR_MEMORY_ACTIVE_READY_CORRECTION_GROUP_ROUTE_V1_END -->

<!-- GOVERNED_ARCHITECTURE_COMPANION_GROUP_ROUTE_V1_START -->

Use `governed_architecture_companion_handoff` from `04_box_architecture_and_boundaries` only on demand. The startup bridge keeps the compact rules visible, while the full companion is loaded for architecture-sensitive, self-hosting, cross-box, lifecycle-heavy, or authority-sensitive work. Brick Wall remains the final coding-authorization owner.

<!-- GOVERNED_ARCHITECTURE_COMPANION_GROUP_ROUTE_V1_END -->


## 04_box_architecture_and_boundaries

Responsibility: bounded ownership and focused boundary specialists.

Active owners:
- box_architecture_canon.md
- boundary_first_repair_protocol.md
- kanda_box_shielding_canon.md
- project_folder_organization_canon.md
- stateful_control_regression_canon.md

Prompt count: 5

Retired: closed_box_delivery_canon; governed_architecture_companion_handoff is a deprecated redirect only.
