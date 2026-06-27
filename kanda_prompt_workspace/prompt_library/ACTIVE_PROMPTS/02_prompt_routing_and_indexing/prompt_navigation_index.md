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
2. prompt_insertion_and_router_registration_protocol
3. prompt_identity_code_registry_canon
4. prompt_canon_reconciliation_protocol
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

# Prompt Navigation Index

Version: 2.1
Status: active_candidate
Scope: KANDA Context Routing Layer - Phase 1 kernel
Owner box: Context Routing Kernel Box
Last updated: 2026-06-16

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

## Startup Box Logic bridge rule

The start-of-day kernel carries only the compact Box Logic Startup Bridge. It
must not load the full Box Architecture canon at session start. For any risky
implementation, repair, refactor, prompt update, governance update, bundle, GUI
ownership, public-contract, cross-box, or mutable-state task, route to
`box_architecture_canon.md` before the risky step.

## Routing authority

This file is the primary readable router for exact prompt selection and route verification.

`prompt_router` may remain as a compatibility/helper prompt, but it must not become a second competing router.
If prompt_router conflicts with this index, this index wins until a human canon decision changes that.

Machine-readable routes are stored in:

```text
ROUTING/prompt_navigation_index.json
ROUTING/group_assimilation_index.json
```

## Routing-index escalation discipline

Use the routing indexes in this order:

1. `GROUP_ASSIMILATION_INDEX.md` for broad group-level routing.
2. `FOLDER_ASSIMILATION_CARDS_INDEX.md` only when the group is known but folder-level boundaries, placement, or selected card context are still needed.
3. This `prompt_navigation_index.md` when the exact prompt file, prompt ID, companion prompt, path, or current route must be selected or verified.

Do not request all routing indexes as a ritual.
Request the smallest complete current routing context that keeps the task safe.
If the indexes disagree, stop and flag `ROUTING_INDEX_CONFLICT` instead of proceeding from memory.

## Rule recovery and no-guessing requirement

When the AI is unsure about a KANDA rule or realizes it may have forgotten a rule, it must not guess from memory.

Required recovery path:

1. Return to this routing index, the AI Prompt Request Canon, and the relevant startup guardrail/source of truth.
2. Request only the smallest relevant prompt/router context needed to recover the rule.
3. If the correct rule still cannot be verified, ask the human for the rule or decision before implementing, freezing, validating, or delivering code.
4. Treat asking the human as the safe teamwork behavior, not as a failure.

Use this rule for forgotten delivery footer behavior, prompt-routing rules, startup sync rules, freeze-memory placement, validation evidence, and protected workflow gates.

## Required routing behavior

1. Read the human request as intent.
2. Decide whether Fast Path is enough.
3. If not Fast Path, identify required group route(s) using `GROUP_ASSIMILATION_INDEX.md`.
4. Escalate to folder cards only when group-level routing is not specific enough.
5. Escalate to this navigation index only when exact prompt identity, path, companion prompt, or route verification is needed.
6. Request selected specialist prompts only when needed.
7. Use HARD STOP only when missing context blocks safe action.
8. Do not load all 12 folders at session start.
9. Do not use routing indexes as a substitute for the specialist prompts they point to.



<!-- PROMPT_INSERTION_ROUTER_REGISTRATION_PROTOCOL_V1_START -->
## Prompt Insertion and Router Registration Protocol route

When the user asks to insert, create, add, register, activate, or connect a prompt in `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS`, route through:

```text
prompt_insertion_and_router_registration_protocol
```

Required prompts/groups for this route:

```text
1. 07_prompt_authoring_and_audit
2. prompt_insertion_and_router_registration_protocol
3. prompt_identity_code_registry_canon
4. prompt_canon_reconciliation_protocol
4. prompt_audit_canon
5. project_specific_prompt_generalization
6. Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION for the target folder
7. Existing prompt-library assets/indexes needed to inspect duplicates and overlap
8. Current prompt navigation/router files needed to register the prompt
9. bundle_gated_development_workflow, if creating an installable bundle
10. Validation command or manual validation steps
```

The protocol is routed, not always_startup. It teaches the AI how to choose the correct ACTIVE_PROMPTS folder by prompt type, create metadata, update folder assimilation, connect startup/routed/on-request/maintenance logic, test, validate, and freeze the new prompt.

Do not insert a new prompt directly into generated `first_prompt_files` artifacts. Do not make a normal routed prompt `always_startup` unless a separate governed startup-delivery change is approved and validated.
<!-- PROMPT_INSERTION_ROUTER_REGISTRATION_PROTOCOL_V1_END -->

<!-- PROMPT_IDENTITY_CODE_REGISTRY_CANON_V1_START -->
## Prompt Identity Code Registry Canon route

When the user asks to create, insert, add, register, activate, name, code, or make copy/paste-addressable a prompt, route through:

```text
prompt_identity_code_registry_canon
```

Use it together with:

```text
prompt_insertion_and_router_registration_protocol
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
```

Required behavior:

```text
Every new prompt must receive prompt_code, prompt_id, title/display name, folder path, file path, metadata, and load_type before router registration is considered complete.
```

The canonical prompt code format is:

```text
KPR-<folder_number>-<sequence>
```

The folder number must match the target ACTIVE_PROMPTS folder family. Do not reuse retired codes. Do not register a routed prompt without prompt_code metadata.
<!-- PROMPT_IDENTITY_CODE_REGISTRY_CANON_V1_END -->



<!-- CHATGPT_KANDA_ROUTING_CHOICE_OUTPUT_PROTOCOL_V1_START -->
## ChatGPT KANDA Routing Choice Output Protocol route

When the user asks ChatGPT to route a task, select a KANDA prompt, identify which prompt/folder/group should be used, or prepare output for manual Prompt Router Reasoner capture, apply:

```text
chatgpt_kanda_routing_choice_output_protocol
```

Required output behavior:

```text
KANDA_ROUTING_CHOICE_START
{ valid JSON with event_type chatgpt_router_prompt_choice, selected_prompts, and advisory_only true }
KANDA_ROUTING_CHOICE_END
```

This block is advisory only. It must not include mutation authority, freeze-writing authority, patch application authority, or ML activation. Browser ChatGPT is not authoritative; local KANDA validates prompt_code, prompt_id, folder_path, and prompt_path before loading canonical prompt text from ACTIVE_PROMPTS.

Known stable prompt-code examples for routing-choice output:

```text
KPR-02-001 = chatgpt_kanda_routing_choice_output_protocol
KPR-07-002 = prompt_identity_code_registry_canon
```

If a legacy prompt lacks a known prompt_code, do not invent a code. Include prompt_id, folder_path, and prompt_path so the local manual capture validator can resolve the canonical ACTIVE_PROMPTS file safely.
<!-- CHATGPT_KANDA_ROUTING_CHOICE_OUTPUT_PROTOCOL_V1_END -->


<!-- PROJECT_TOOL_BOUNDARY_CANON_V1_START -->
## Project Tool Boundary Canon route

When a coding, patch, freeze, handoff, validation, source-inspection, project-root, or staging-path task could confuse KANDA Reasoner as the tool with `<my_project>` as the selected target project, load or recommend:

```text
project_tool_boundary_canon
```

Prompt identity:

```text
KPR-12-001 = project_tool_boundary_canon
ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md
```

Required behavior:

```text
tool_project_slug = kanda_reasoner
active_project_slug = selected project in use
active_project_root = selected project root
```

Do not hardcode `kanda_reasoner` as the active target project unless KANDA Reasoner is explicitly the selected active project. Project-specific writes use `<active_project_root>`. Reusable tool writes use the owning KANDA Reasoner tool path. This route is a boundary invariant and must be paired with the relevant implementation, box, patch, validation, freeze, or handoff prompt; it does not replace those prompts.
<!-- PROJECT_TOOL_BOUNDARY_CANON_V1_END -->

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
| 02_prompt_routing_and_indexing | 7 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 03_governance_freeze_and_handoff | 9 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 04_box_architecture_and_boundaries | 5 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 05_patch_delivery_and_validation | 6 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 06_refactor_and_architecture_hardening | 7 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 07_prompt_authoring_and_audit | 3 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 08_python_engineering_core | 12 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 09_python_quality_security_observability | 7 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 10_python_api_data_async_config | 4 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 11_productization_and_release_readiness | 6 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |
| 12_generalized_project_canons | 7 | See GROUP_ASSIMILATION_INDEX.md for responsibility and use cases. |


## Governed patch ZIP release hook

<!-- PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_START -->
## Canonical freeze-ready patch delivery sequence

For every freezeable KANDA/PyArchitect patch, the delivery order is mandatory and must not be inverted, skipped, or diluted:

1. **Send the patch ZIP only after contract validation.** The ZIP must contain only the changed project files plus a root-level `KANDA_FREEZE_HINT.json` sidecar. If the ZIP contract cannot be verified, block delivery with `CONTRACT NOT MET - PATCH DELIVERY BLOCKED`.
2. **Send the install PowerShell after the ZIP.** The install block must stage the ZIP from `<drive>:\PATCH_NAME.zip` into `<drive>:\<project_name>_delete_after_daily_work\`, delete the root-drive ZIP copy after successful staging, extract only from the staged ZIP, and install only changed project files.
3. **Do not install the freeze sidecar into the project root.** `KANDA_FREEZE_HINT.json` is freeze-intake delivery metadata. It may be scanned or consumed from the staged ZIP / daily-work intake location, but it must not be copied as a normal project source file.
4. **Send the validation PowerShell after the install block.** Validation must be a separate local action after install and must emit recognizable evidence, including `VALIDATION OK: <feature_id>`. When startup delivery, generated evidence, or sync state is validated, it must also emit `STATUS: IN_SYNC`.
5. **Freeze only after local validation passes.** The Freeze Feature After Update flow must use the feature-specific `KANDA_FREEZE_HINT.json` / freeze-intake data plus current validation evidence, then require Preview and explicit human Confirm and Write.
6. **Refresh AI exposure after freeze.** A successful local freeze write must refresh AI-send exposure and startup freeze context so the next startup pack knows the frozen behavior.

Short form:

```text
patch ZIP with root KANDA_FREEZE_HINT.json
-> install changed files only, keeping KANDA_FREEZE_HINT.json out of project root
-> run local validation with VALIDATION OK and STATUS: IN_SYNC when applicable
-> freeze through Preview + Confirm and Write
-> refresh AI-send and startup freeze context
```

Install success is not validation. A freeze hint is not validation evidence. Old feature validation must not be reused for the current feature.
<!-- PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_END -->






<!-- GOVERNED_IMPLEMENTATION_NAVIGATION_GATE_V1_START -->
### Governed implementation gate

When the next answer may create, edit, repair, refactor, validate, or package source, prompt-library, startup-delivery, GUI, Error Memory, freeze, or patch-governance files, classify the route as `GOVERNED_IMPLEMENTATION`.

Required prompts/groups:

1. router_bridge_governed_implementation
2. implementation_and_delivery_protocol
3. Relevant folder card or specialist prompt for the target box
4. box_architecture_canon when boundary risk exists
5. project_tool_boundary_canon when project/tool identity can be confused
6. pre_output_contract_gates when terminal, ZIP, freeze, or validation artifacts will be emitted

Mandatory behavior:

- Emit `IMPLEMENTATION GATE` before governed implementation begins.
- Do not code from memory.
- Inspect actual source files and list Source files inspected in the gate.
- Declare Generated-vs-canonical status before editing generated artifacts.
- Declare target box and forbidden boxes.
- If the gate cannot pass, stop before implementation and inspect or request missing context.
<!-- GOVERNED_IMPLEMENTATION_NAVIGATION_GATE_V1_END -->





When the next answer will emit an installable patch ZIP link, an install PowerShell block, a validation block for a patch, `KANDA_FREEZE_HINT.json`, or freeze-form JSON, classify the output route as `PATCH_DELIVERY_RELEASE`.

Required prompts/groups:

1. 05_patch_delivery_and_validation
2. router_bridge_patch_delivery_contract
3. pre_output_contract_gates from 03_governance_freeze_and_handoff
4. freeze_code_intake_and_form_protocol when the patch can be frozen later
5. Relevant source files and validation command

Mandatory behavior:

- Do not emit the ZIP link unless the ZIP contract validator passes.
- Do not use generic Downloads/Desktop installer search patterns.
- Do stage from `<drive>:\PATCH_NAME.zip` into `<drive>:\<project>_delete_after_daily_work\`.
- Do keep root-level `KANDA_FREEZE_HINT.json` outside the install payload folder.
- Do generate freeze sidecar and freeze-form JSON from the same payload source.
- If any of these checks cannot be verified, output `CONTRACT NOT MET - PATCH DELIVERY BLOCKED` and do not present the ZIP.

<!-- NO_ISOLATED_ZIP_NAVIGATION_GATE_V1_START -->
### No isolated ZIP delivery gate

For patch ZIP delivery, also route to:

```text
router_bridge_patch_delivery_contract
```

A ZIP link is forbidden unless the same response includes a visible `PATCH DELIVERY GATE` with `GATE STATUS: PASS`, user-facing install code, user-facing validation code, expected validation markers, changed files, freeze/freeze-intake handling when applicable, Error Memory handling for user-detected corrections, and beginner-safe do-not-do instructions.

If the gate is incomplete, output `CONTRACT NOT MET - PATCH DELIVERY BLOCKED` instead of a ZIP link.
<!-- NO_ISOLATED_ZIP_NAVIGATION_GATE_V1_END -->

<!-- USER_DETECTED_CORRECTION_NAVIGATION_GATE_V1_START -->
### User-detected correction gate

When the user reports a defect in the AI's previous work or delivery, route to:

```text
router_bridge_user_detected_correction
```

Required behavior:

- Emit `USER-DETECTED CORRECTION GATE` before corrective implementation or patch delivery.
- Audit the exact cause from real source, response text, validation output, ZIP contents, or freeze sidecar.
- If a patch is needed, route through `router_bridge_governed_implementation` and `router_bridge_patch_delivery_contract`.
- Include Error Memory intake for user-detected AI mistakes unless a specific N/A reason is stated.
- Include freeze/freeze-intake handling for freezeable corrections without bypassing Preview or Confirm and Write.
<!-- USER_DETECTED_CORRECTION_NAVIGATION_GATE_V1_END -->


- Before outputting any PowerShell or terminal block, apply `TERMINAL_FOOTER_SELF_AUDIT`: install blocks require the 5-second `INSTALL OK. Terminal will clear in 5 seconds...` footer; validation, diagnostic, staging-check, repair, freeze/evidence-merge, and all other terminal blocks require Enter, `Clear-Host`, Enter, `Clear-Host`.
- If terminal cleanup cannot be verified from the exact text being emitted, output `CONTRACT NOT MET - PATCH DELIVERY BLOCKED` and repair the command before showing it.


## Pre-output contract gates routing hook

Request `pre_output_contract_gates.md` from `03_governance_freeze_and_handoff` immediately before the AI emits terminal code, patch ZIP delivery instructions, validation commands, freeze-form JSON, validation evidence intended for freezing, `KANDA_FREEZE_HINT.json`, or multi-project freeze path decisions.

Use this prompt as an output-time contract gate. It must not replace the router, patch delivery protocol, or freeze-code intake protocol. Do not load it for simple explanation-only Fast Path tasks.

## Cooperative implementation methodology routing hook

Request `cooperative_implementation_methodology.md` from `03_governance_freeze_and_handoff` when the user asks how KANDA Reasoner should implement a consequential feature, how AI and human should divide responsibility, whether to use handoff/web/book research before coding, or how to improve the implementation methodology after repeated friction.

Do not load it for simple questions or as a replacement for Box Architecture, patch delivery, freeze memory, or prompt-authoring specialist prompts. It is a cooperation-method overlay only.



## KANDA Box Shielding Canon routing hook

Request `kanda_box_shielding_canon.md` from `04_box_architecture_and_boundaries` when the user asks to create, improve, canonize, audit, or implement shielding logic; when a meaningful box milestone has been reached; when stronger ML, embeddings, vector stores, self-learning, prompt auto-selection, or cross-box integration is being considered; or when a box has accumulated multiple interacting advisory layers that must be protected before continuing.

KBSC is on-request. Do not load it for simple explanation-only Fast Path tasks. Do not treat it as a substitute for the owning specialist prompt, patch-delivery protocol, validation evidence, or human-confirmed freeze workflow.

For implementation or canonization of shielding behavior, required context normally includes:

```text
1. kanda_box_shielding_canon
2. 04_box_architecture_and_boundaries
3. 05_patch_delivery_and_validation, if source files, patch ZIP, install, validation, or freeze-ready delivery are involved
4. 07_prompt_authoring_and_audit, if the KBSC prompt or routing registration is being created or updated
5. 02_prompt_routing_and_indexing, if routing indexes or prompt-call behavior are being updated
6. 03_governance_freeze_and_handoff, if freeze, handoff, validation evidence, or governance behavior is involved
7. Active project freeze context, if frozen behavior may be changed or shielded
8. Relevant owning-box source files and tests
9. Validation command or manual validation steps
```

May proceed now is NO for implementation until the relevant owning-box context and validation path are available. It may be PARTIAL for architecture-only discussion or draft planning.



## RG-PILOT-000 Pilot/Copilot Phase 0 routing hook

Request `routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md` from `02_prompt_routing_and_indexing` when the user asks to start Pilot, start Copilot, continue after M35, implement Pilot/Copilot Phase 0, create P0, canonize Pilot/Copilot router logic, add Pilot projection/simulation, add Pilot disagreement taxonomy, add Pilot implementation gates, add Pilot router reproduction, use Pilot outputs as training data, batch-generate Pilot outputs, persist Pilot outputs, or introduce Limited Shadow Runtime after M35.

This canon is on-request. Do not load it for simple Fast Path explanation-only tasks. Do not treat it as an implementation prompt, and do not use it to add Pilot runtime, Copilot runtime, prompt loading, persistence, training-data use, batch mode, route execution, router authority, or runtime shadow behavior.

For Pilot/Copilot Phase 0 work, required context normally includes:

```text
1. routing_signal_scorer_v3_pilot_copilot_phase0_router_canon
2. kanda_routing_system_canon
3. kanda_box_shielding_canon
4. 02_prompt_routing_and_indexing
5. 04_box_architecture_and_boundaries, if source boundaries or box manifest are touched
6. 05_patch_delivery_and_validation, if a patch ZIP, install block, validation block, or freeze-ready delivery is requested
7. Active project freeze context and M35 closure evidence
8. Current project files and validation command or manual validation steps
```

May proceed now is PARTIAL for read-only planning or audit. It is NO for implementation until current project files, M35 closure context, patch boundary, validation path, and freeze path are clear. If P0 is not yet validated and frozen, the next implementation milestone is P0 only.

Canonical RG-PILOT-000 rule:

```text
Pilot/Copilot Phase 0 begins only as a design-only, non-authoritative, opt-in, ephemeral, zero-critical-error scope charter that preserves M35 bridge closure, forbids runtime authority and prompt loading, requires Pilot to reproduce frozen router/canon outcomes before disagreement evidence is trusted, and defers Copilot and any runtime shadow mode to separately governed future scopes.
```



## RG-LAB-000 Post-P12 ML LAB phase entry routing hook

Request `routing_signal_scorer_v3_lab_phase_entry_router_canon.md` from `02_prompt_routing_and_indexing` when the user asks to canonize LAB phase entry, start LAB after P12, continue after P12, go next after P12, create LAB-0, create a lab charter, implement ML lab/test logic, test ML router prompt logic, test prompt choosing reliability, validate ML router prompt logic reliability, or continue ML implementation after lab reliability.

This canon is on-request. Do not load it for simple Fast Path explanation-only tasks. Do not treat it as an implementation prompt, and do not use it to add LAB code, schema, fixtures, runner, candidate harness, prompt loading, persistence, provider calls, embeddings, training-data use, batch mode, activation gates, field-test mode, runtime Pilot, or Copilot behavior.

For post-P12 LAB phase work, required context normally includes:

```text
1. routing_signal_scorer_v3_lab_phase_entry_router_canon
2. routing_signal_scorer_v3_pilot_copilot_phase0_router_canon
3. kanda_routing_system_canon
4. kanda_box_shielding_canon
5. 02_prompt_routing_and_indexing
6. active project freeze context and P12 freeze evidence when continuing after P12
7. 05_patch_delivery_and_validation plus current project files and validation steps if patching
8. 09_python_quality_security_observability if validation, safety gates, tests, metrics, or observability are involved
```

May proceed now is PARTIAL for read-only planning, audit, and RG-LAB-000 canon review. It is YES only for a governed RG-LAB-000 routing-canon patch when the routing assets, patch boundary, validation path, and freeze path are clear. It is NO for ML implementation, LAB coding, runner creation, schema creation, fixtures, corpus, candidate harness, prompt loading, persistence, provider calls, activation, field-test mode, or Copilot behavior until the correct earlier LAB milestone is frozen.

Canonical RG-LAB-000 rule:

```text
After P12, canonize LAB entry first; build and validate the LAB before testing ML router prompt logic; validate ML router prompt logic reliability before continuing ML implementation.
```

## Routing Signal Scorer v3 semantic-readiness routing hook

Request `routing_signal_scorer_v3_semantic_readiness_canon.md` from `02_prompt_routing_and_indexing` when the user asks to design, canonize, audit, or implement machine learning, embeddings, semantic retrieval, vector indexes, vector databases, semantic scorer behavior, `routing_signal_scorer` v3, Metadata Vector Manifest, semantic corpus generation, retrieval evaluation, or ML/retrieval library adoption.

This canon is on-request. Do not load it for simple explanation-only Fast Path tasks. Do not treat it as an implementation prompt and do not use it to add ML dependencies, provider code, vector indexes, corpus generators, external APIs, self-learning loops, prompt auto-loading, or router overrides.

For semantic-readiness work, required context normally includes:

```text
1. routing_signal_scorer_v3_semantic_readiness_canon
2. kanda_routing_system_canon
3. kanda_box_shielding_canon
4. 02_prompt_routing_and_indexing
5. 04_box_architecture_and_boundaries, if implementation, design patch, authority boundary, or box ownership may be affected
6. 05_patch_delivery_and_validation, if a patch ZIP, install block, validation block, or freeze-ready delivery is requested
7. Active project freeze context, if frozen routing_signal_scorer behavior may be changed or protected
8. Current routing_signal_scorer design/freeze context, if implementation or design patch is requested
9. Validation command or manual validation steps
```

May proceed now is PARTIAL for read-only architecture discussion or audit. It is NO for implementation until the semantic-readiness canon, KBSC boundary, routing-system canon, current routing_signal_scorer shield context, patch boundary, validation plan, and freeze path are clear.

Canonical semantic-readiness rule:

```text
The semantic layer is an untrusted evidence witness. It may provide evidence; it may never provide authority.
```

## Freeze Feature After Update GUI/source routing hook (RG-028)

When the task changes the Freeze Feature After Update tab, local freeze writer, freeze_after_update public contract, preview/write behavior, or any path that can write active freeze memory, use this exact context package before implementation:

```text
Required:
1. 09_active_project_freeze_context
2. 04_box_architecture_and_boundaries
3. cooperative_implementation_methodology
4. 05_patch_delivery_and_validation
5. Relevant freeze_after_update GUI/app/contract/local-writer source files
6. Validation command or manual validation steps

Conditional required:
7. 08_python_engineering_core - required IF Python source code, GUI code, contract code, local writer code, install logic, or validation code may be modified.
8. 09_python_quality_security_observability - required IF safety checks, validation behavior, write-safety, or regression protection may be modified.
```

If the user requests automatic freeze writes without explicit human confirmation, classify it as a protected freeze-workflow conflict and set `May proceed now: NO`.

Estimated context load should normally be `large` because this route combines frozen behavior, GUI/domain ownership, source code, write-safety, and validation evidence.

### RG-028 complete-pass enforcement

Do not treat `rg028_freeze_workflow_context_package_v1` as a required prompt that replaces the actual package. It is a routing-rule/checkpoint label only.

For a full PASS, the Required prompts/groups field must expand the package and explicitly include:

```text
1. 09_active_project_freeze_context
2. 04_box_architecture_and_boundaries
3. cooperative_implementation_methodology
4. 05_patch_delivery_and_validation
5. 08_python_engineering_core
6. 09_python_quality_security_observability
7. relevant freeze_after_update GUI/app/contract/local-writer source files
8. validation command or manual validation steps
```

When the user asks to remove, bypass, automate away, or weaken Confirm and Write, the answer must set:

```text
Estimated context load: large
May proceed now: NO
```

Do not downgrade the context load to medium/medium-high for this confirmation-bypass route.

## Task-to-group routing table

| Task trigger | Required groups | Optional groups | Missing behavior |
|---|---|---|---|
| start day / continue session | 01, 02 | 03 if continuing from handoff | STEP PAUSE if kernel missing |
| explain / discuss / brainstorm | none beyond loaded kernel | selected group only if needed | DEGRADED WARNING if evidence thin |
| create or modify code | 05 plus source files and validation steps; 04 if ownership boundaries, public contracts, app structure, cross-box behavior, GUI ownership, or startup delivery are involved | 08, 09, 10 depending on task | HARD STOP before implementation; new code modules must stay <=500 lines |
| create a new folder with a databank | 04, 05, 09, 10 | 11 if production-ready storage | HARD STOP before implementation |
| large code module / code file over 500 lines, or new code module expected to exceed 500 lines | 04, 05, 06 | 08, 09 | HARD STOP before implementation |
| architecture decision | 04 | 06, 11, 12 | STEP PAUSE before canon/patch |
| Pilot/Copilot Phase 0 / post-M35 / P0 / Pilot projection / Copilot boundary | 02_prompt_routing_and_indexing, routing_signal_scorer_v3_pilot_copilot_phase0_router_canon, kanda_routing_system_canon, kanda_box_shielding_canon; 05 plus source files and validation steps if patching | 04, 09, 08 depending on implementation/safety scope | HARD STOP before implementation; PARTIAL only for read-only planning; P0 only until frozen |
| semantic readiness / embeddings / ML retrieval / routing_signal_scorer v3 | 02_prompt_routing_and_indexing, routing_signal_scorer_v3_semantic_readiness_canon, kanda_routing_system_canon, kanda_box_shielding_canon; 05 plus source files and validation steps if patching | 04, 09, 08 depending on implementation/safety scope | HARD STOP before implementation; PARTIAL only for architecture discussion |
| box shielding / KBSC / shield before stronger ML | 04_box_architecture_and_boundaries, kanda_box_shielding_canon; 05 plus source files and validation steps if patching; 07 if registering or updating prompts/routing assets | 03 if freeze/governance, 08/09 if source/validation/safety code may be modified | HARD STOP before implementation; PARTIAL only for architecture discussion |
| prompt audit / prompt batch review | 02, 07 | 03 if deprecation/freeze, 12 if generalizing | STEP PAUSE until related prompts inspected |
| prompt conflict | 02, 07 | relevant groups containing both prompts | HARD STOP for canon decision |
| validation / freeze | 03, 05 | 04 if architecture touched | HARD STOP if validation output missing |
| Freeze Feature After Update GUI/source workflow change | 09_active_project_freeze_context, 04_box_architecture_and_boundaries, cooperative_implementation_methodology, 05_patch_delivery_and_validation, relevant freeze_after_update source files, validation command or manual validation steps | 08_python_engineering_core and 09_python_quality_security_observability when source/validation/safety code may be modified | HARD STOP before implementation; May proceed now: NO if human confirmation is bypassed |
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
| semantic retrieval, embeddings, vector indexes, corpus generation, routing_signal_scorer v3 | routing_signal_scorer_v3_semantic_readiness_canon plus kanda_routing_system_canon and kanda_box_shielding_canon |
| box shield, KBSC, meaningful milestone, stronger ML preparation, authority boundary protection | kanda_box_shielding_canon plus box_architecture_canon |
| code/file delivery, ZIP, install, validation, or freeze | bundle_gated_development_workflow or delivery/validation protocol |
| prompt audit, split, merge, deprecate, conflict, or generalization | prompt_audit_canon plus related prompt files |
| code file above 500 lines, or new code module expected to exceed 500 lines | large_module_refactor_protocol |
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

7. Never use or suggest deprecated/unrelated project roots such as `deprecated hardcoded project root` for KANDA prompt workspace work.
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
2. prompt_insertion_and_router_registration_protocol
3. prompt_identity_code_registry_canon
4. prompt_canon_reconciliation_protocol
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
2. prompt_insertion_and_router_registration_protocol
3. prompt_identity_code_registry_canon
4. prompt_canon_reconciliation_protocol
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
2. prompt_insertion_and_router_registration_protocol
3. prompt_identity_code_registry_canon
4. prompt_canon_reconciliation_protocol
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
2. prompt_insertion_and_router_registration_protocol
3. prompt_identity_code_registry_canon
4. prompt_canon_reconciliation_protocol
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


## Terminal cleanup canon route

When the next answer will emit any PowerShell or terminal block, the router must apply the terminal cleanup canon before output. Successful install blocks use `INSTALL_SUCCESS`: wait 5 seconds, `Clear-Host`, keep terminal open, and no Enter prompts. Install errors, validation, validation errors, diagnostics, and all other terminal blocks use `Enter`, `Clear-Host`, `Enter`, `Clear-Host`, and keep terminal open. Install blocks must include a fail-safe `try/catch` or text-equivalent error path so failures cannot skip cleanup.


<!-- KANDA_NAV:error_event_to_error_memory_owner_canon:v2 -->
## Error event companion route to Error Memory owner canon

When any implementation, install, validation, GUI, startup, prompt-routing, ZIP contract, freeze-intake, or patch-delivery error appears, route the Error Memory prevention track to:

```text
error_memory_ai_formulary_startup_canon
```

For a correction patch, keep the correction track in the normal repair/bundle route and require the Error Memory owner canon's default autoload path. Router/navigation prompts must point to this owner canon rather than creating a parallel Error Memory doctrine.

<!-- KANDA_NAV:error_memory_direct_error_lesson_zip:v1 -->
## Direct Error Lesson ZIP route

When the user asks for an Error Lesson ZIP, formatted Error Memory lesson ZIP, direct ZIP to import into Error Memory, or ZIP containing a new error and solution JSON, route to:

```text
error_memory_ai_formulary_startup_canon
```

Classification:

```text
Fast Path or Routed Work Path: Fast Path when only packaging the formatted Error Lesson ZIP from already-known error evidence and no project files are changed.
Routed Work Path when the request also changes GUI/source/prompt/router/freeze behavior.
```

Required output for Fast Path Direct Error Lesson ZIP:

```text
1. Download link to the Error Lesson ZIP.
2. Short GUI import steps.
3. State that this is not a code patch and does not use install/validation PowerShell.
```

Canonical ZIP structure:

```text
bundle_manifest.json
payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_<lesson_slug>.txt
payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_<lesson_slug>.txt
```

Default routine reminder:

```text
For code, GUI, prompt, startup, validation, freeze, or project-source changes, use the normal patch ZIP -> install -> validate workflow.
```

<!-- KANDA_NAV:error_memory_default_autoload_insertion:v2 -->
## Error Memory default insertion autoload route

When the user wants a new error inserted with the routine `ZIP -> install -> validate -> populate EM tab`, select:

```text
error_memory_ai_formulary_startup_canon
bundle_gated_development_workflow
```

The expected package stages a formatted pending lesson under:

```text
<drive>:\<project>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
```

It must make the error appear in:

```text
AI-assisted error lesson intake
Error Editor
```

and must not save it into Lessons until `Memorize Error` is clicked.

Use Direct Error Lesson ZIP only when the user asks for a manual import package. Use Copy/Paste formatted AI flow only when the user asks for or uses those GUI buttons.

## Prompt Authoring And Audit (`07_prompt_authoring_and_audit`)

### `prompt_insertion_and_router_registration_protocol` - Prompt Insertion and Router Registration Protocol

- **File:** `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_insertion_and_router_registration_protocol.md`
- **Priority:** `36`
- **Trigger phrases:** `insert a new prompt`; `add a new prompt`; `create a new prompt`; `register a prompt in the router`; `make the router call this prompt`; `activate a prompt in router logic`; `connect a prompt to the router`; `bridge a prompt to prompt router logic`; `add prompt to ACTIVE_PROMPTS`; `prompt insertion protocol`; `prompt router registration`
- **User intent examples:** `Create a new prompt and connect it to the router.`; `Bridge this prompt to prompt router logic without making it always-startup.`; `Add this prompt to ACTIVE_PROMPTS with metadata and routing validation.`
- **Aliases:** `prompt insertion and router registration protocol`; `prompt_insertion_and_router_registration_protocol`; `prompt bridge insertion protocol`; `prompt router registration`
- **When to load:** When the task asks to create, insert, update, route, bridge, register, or make available a prompt in the KANDA prompt workspace.
- **When not to load:** Do not load for ordinary implementation tasks that do not change prompt-library files or routing awareness.
- **Required companion prompts:** `prompt_canon_reconciliation_protocol`; `prompt_audit_canon`; `project_specific_prompt_generalization`; `prompt_identity_code_registry_canon`; `prompt_navigation_index`; `prompt_router`

## Generalized Project Canons (`12_generalized_project_canons`)

### `error_memory_active_ready_correction_blueprint` - Error Memory Active-Ready Correction Blueprint

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_correction_blueprint.md`
- **Prompt code:** `KPR-12-002`
- **Priority:** `32`
- **Trigger phrases:** `correct this Error Memory draft`; `make this lesson active-ready`; `convert draft to active lesson`; `KANDA_ERROR_LESSON_JSON status draft`; `This lesson is not ready for active status`; `Memorize Error says missing active-ready fields`; `validation_command_summary is empty`; `source_patch_zip is empty`; `install_command_summary is empty`; `regression_check.type must be validation_command`; `regression_check.command is empty`; `regression_check.expected_marker is empty`
- **User intent examples:** `Convert this KANDA_ERROR_LESSON_JSON draft into an active-ready lesson.`; `Memorize Error rejects this lesson because active-ready fields are missing; correct it safely.`; `Make this Error Memory draft active only if validation evidence is complete.`
- **Aliases:** `error memory active-ready correction blueprint`; `error_memory_active_ready_correction_blueprint`; `draft to active error memory blueprint`; `active-ready Error Memory schema`
- **When to load:** When a task asks to correct, promote, validate, or convert a `KANDA_ERROR_LESSON_JSON` draft into active-ready or active status.
- **When not to load:** Do not load for ordinary code patches, generic Error Memory GUI behavior, or non-Error-Memory tasks unless an Error Memory lesson is being corrected or promoted.
- **Required companion prompts:** `prompt_insertion_and_router_registration_protocol`; `prompt_navigation_index`; `prompt_router`
