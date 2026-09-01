# KANDA Prompt Navigation Index

Version: v3 intent-routing compatibility report

Authority notice: this expanded report is compatibility documentation. Current routing authority is `ROUTING/prompt_navigation_index.json` together with the canonical active `prompt_navigation_index.md`. `prompt_router` is deprecated pending consumer migration in Wave 2B and must not be selected for new routing work. Historical entries below do not override current route status.

This file maps natural human requests to the correct clean prompt ID and companion prompt stack. The human does not need to know exact filenames. The AI should infer intent from trigger phrases, examples, aliases, and context.

## Routing Rules

- Match the user request against trigger phrases, user intent examples, aliases, and category context.
- If multiple prompts match, prefer the lower numeric `priority` value, then load required companion prompts.
- For implementation, refactor, prompt update, governance update, or bundle creation, include `box_architecture_canon` unless the selected prompt already is the box canon.
- For patch or delivery work, select the smallest current Class 05 owner set and include the active PIR index before emitting patch-related output.
- For freeze/governance, do not freeze unless validation/evidence has already passed.
- For prompt import/generalization/reconciliation, use prompt-authoring/audit prompts, not Python source-code prompts.
- For shielding requests, meaningful box milestones, stronger ML preparation, or authority-boundary protection, load `kanda_box_shielding_canon` with `box_architecture_canon` and the owning box context. Do not continue stronger work until the shield is validated and frozen.
- If intent remains ambiguous, use `ai_prompt_request_canon` with the canonical `prompt_navigation_index`, then ask one focused clarification. Do not select deprecated `prompt_router` for new work.

## Prompt Routes
## Session Start And Navigation (`01_session_start_and_navigation`)

Current direct routes:

- `KPR-01-001 start_of_day_master_stack` - compact startup governance bridge.
- `KPR-01-002 session_start_upload_checklist` - two-stage startup and Project readiness.
- `KPR-01-003 prompt_router_reasoner_startup_check` - on-request readiness assessment.
- `KPR-01-004 ai_human_partnership_session_start` - optional collaboration overlay.
- `KPR-01-005 daily_startup_loader_template` - startup-loader authoring template.
- `KPR-01-006 project_startup_canon_template` - Project startup-profile authoring template.
- `KPR-01-007 daily_patch_delivery_guardrails` - compact patch-delivery bridge to Class 05.
- `KPR-01-008 handoff_at_end_of_work` - session closure and minimum continuity guardrail.
- `KPR-01-012 error_memory_ai_formulary_startup_canon` - Error Memory admission and workflow owner.
- `KPR-01-013 durable_document_artifact_routing_canon` - durable documentary-artifact routing owner.
- `KPR-01-014 ai_prompt_request_canon` - request admission.

`patch_install_delivery_error_register` moved to Class 05 as `KPR-05-001` and is
conditionally required before patch-related output. It is not always-startup.

Deprecated compatibility records are not active routes: `daily_reasoner_startup_loader`, `daily_session_start_prompt`, `general_prompt_stack_load_order`, and `reasoner_startup_canon`.

## Prompt Routing And Indexing (`02_prompt_routing_and_indexing`)


### `kanda_routing_system_canon` — KANDA Routing System Canon

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md`
- **Priority:** `3`
- **Trigger phrases:** `routing system canon`; `KANDA Routing System Canon`; `canonize routing system`; `routing logic canon`; `context selection operating system`; `Prompt-Call Accuracy`; `Context Package Manifest`; `Prompt Registration v2`; `register prompt as routable context asset`; `prompt-call accuracy`; `routing-system update`; `startup routing behavior`; `prompt insertion rule`; `similarity advisory routing`; `freeze-aware routing`; `routing canon registration`
- **User intent examples:** `Canonize the routing system itself.`; `Update the way prompts are registered into the routing system.`; `Define the Context Package Manifest before routing automation.`
- **Aliases:** `kanda_routing_system_canon`; `kanda_routing_system_canon.md`; `routing canon`; `routing system canon`; `prompt-call canon`; `context package manifest canon`
- **When to load:** When routing-system behavior, prompt-call accuracy, context package manifests, prompt registration, startup routing, or routing indexes are being audited, changed, canonized, or frozen.
- **When not to load:** Do not load for simple Fast Path explanations, ordinary code patches with an already-clear route, or as a substitute for specialist prompts after routing is decided.
- **Required companion prompts:** `ai_prompt_request_canon`; `prompt_navigation_index`; `GROUP_ASSIMILATION_INDEX`

### `routing_signal_scorer_v3_semantic_readiness_canon` — Routing Signal Scorer v3 Semantic Readiness Canon

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_semantic_readiness_canon.md`
- **Priority:** `2`
- **Trigger phrases:** `semantic readiness canon`; `routing_signal_scorer v3`; `embedding readiness`; `semantic evidence layer`; `semantic scorer`; `semantic retrieval`; `machine learning architecture`; `embeddings`; `vector index`; `FAISS`; `Qdrant`; `Chroma`; `sentence-transformers`; `Metadata Vector Manifest`; `retrieval evaluation`; `stale corpus`; `index poisoning`; `ML safety boundary`
- **User intent examples:** `Before implementing embeddings, canonize the semantic readiness plan.`; `Design routing_signal_scorer v3 with semantic evidence but no ML implementation yet.`; `Can we use sentence-transformers or FAISS in KANDA Reasoner?`
- **Aliases:** `routing_signal_scorer_v3_semantic_readiness_canon`; `routing_signal_scorer_v3_semantic_readiness_canon.md`; `semantic readiness canon`; `semantic evidence canon`; `embedding readiness canon`; `routing_signal_scorer v3 canon`; `Metadata Vector Manifest canon`
- **When to load:** When KANDA work involves ML, embeddings, semantic retrieval/search, vector indexes/databases, semantic scorer work, routing_signal_scorer v3, Metadata Vector Manifest, corpus generation, retrieval evaluation, or ML/retrieval library adoption.
- **When not to load:** Do not load for ordinary lexical routing-scorer patches, simple Fast Path explanations, non-routing ML discussion unrelated to KANDA, or as a substitute for source/freeze context during implementation.
- **Required companion prompts:** `kanda_routing_system_canon`; `kanda_box_shielding_canon`; `prompt_navigation_index`; `GROUP_ASSIMILATION_INDEX`

### `project_overlay_selector` — Project Overlay Selector

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/project_overlay_selector.md`
- **Priority:** `10`
- **Trigger phrases:** `which overlay`; `project overlay`; `use project-specific rules`; `select overlay`; `generalize to project`
- **User intent examples:** `Which project overlay applies to this task?`
- **Aliases:** `index`; `navigator`; `overlay`; `project`; `project overlay selector`; `project_overlay_selector`; `project_overlay_selector.md`; `router`; `selector`
- **When to load:** When choosing whether project-specific or general prompts should govern a task.
- **When not to load:** Do not load when the active project and prompt stack are already clear.
- **Required companion prompts:** `general_prompt_stack_load_order`; `prompt_substitution_map`

### `prompt_navigation_index` — Prompt Navigation Index

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- **Priority:** `10`
- **Trigger phrases:** `what prompt should I use`; `navigation index`; `route this request`; `prompt map`; `find correct prompt`
- **User intent examples:** `I say “module too big”; which prompt should that trigger?`
- **Aliases:** `index`; `navigation`; `navigator`; `prompt navigation index`; `prompt_navigation_index`; `prompt_navigation_index.md`; `router`
- **When to load:** When translating messy human intent into prompt routes.
- **When not to load:** Do not load as a substitute for the actual specialist prompt after routing is decided.
- **Required companion prompts:** `general_prompt_stack_load_order`; `prompt_substitution_map`

### `prompt_substitution_map` — Prompt Substitution Map

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md`
- **Priority:** `10`
- **Trigger phrases:** `substitute prompt`; `replace prompt`; `old prompt new prompt`; `prompt substitution`; `rename prompt reference`
- **User intent examples:** `Update references from an old prompt name to the new clean name.`
- **Aliases:** `index`; `navigator`; `prompt substitution map`; `prompt_substitution_map`; `prompt_substitution_map.md`; `router`; `substitution`
- **When to load:** When resolving renamed/replaced prompts or substituting old prompt references.
- **When not to load:** Do not load if no prompt name migration or substitution is involved.
- **Required companion prompts:** `general_prompt_stack_load_order`

## Governance Freeze And Handoff (`03_governance_freeze_and_handoff`)

### `brick_wall_comprehensive_quality_gate` - Brick Wall - Comprehensive Quality Gate

- **Prompt code:** `KPR-03-001`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md`
- **Priority:** `40`
- **Trigger phrases:** `brick wall`; `show brick wall`; `brick wall check`; `update brick wall`; `where are we on brick wall`; `run the quality wall`
- **User intent examples:** `Brick wall.`; `Show Brick Wall and tell me where this implementation stands.`; `Update the Brick Wall checklist after validation.`
- **Aliases:** `KPR-03-001`; `brick wall`; `brick wall quality gate`; `brick_wall_comprehensive_quality_gate`; `brick_wall_comprehensive_quality_gate.md`; `comprehensive quality gate`; `Q01-Q40 checklist`
- **When to load:** Whenever the user says Brick Wall or requests the live Q01-Q40 governed implementation status for KANDA Reasoner work.
- **When not to load:** Do not load for unrelated medical, writing, or general-information tasks, and do not use it as a substitute for exact source or specialist owner prompts.
- **Required companion prompts:** `project_tool_boundary_canon`; `box_architecture_canon`; `kanda_box_shielding_canon`

### `cooperative_implementation_methodology` - Cooperative Implementation Methodology

- **Prompt code:** `KPR-03-002`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/cooperative_implementation_methodology.md`
- **Priority:** `25`
- **Trigger phrases:** `cooperative implementation`; `proposal before code`; `compare implementation options`
- **User intent examples:** `Compare consequential implementation options before governed admission.`
- **Aliases:** `KPR-03-002`; `cooperative_implementation_methodology`; `cooperative_implementation_methodology.md`; `cooperative implementation methodology`
- **When to load:** Compare consequential implementation options before governed admission.
- **When not to load:** Do not use as implementation authorization or as a substitute for the exact specialist owner.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `freeze_code_intake_and_form_protocol` - Freeze Hint and Form Intake Protocol

- **Prompt code:** `KPR-03-003`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md`
- **Priority:** `30`
- **Trigger phrases:** `freeze hint intake`; `freeze form`; `new local freeze entry`; `freeze blueprint`; `Get Blueprint Freeze`
- **User intent examples:** `Carry one validated feature identity into project-owned freeze intake.`
- **Aliases:** `KPR-03-003`; `freeze_code_intake_and_form_protocol`; `freeze_code_intake_and_form_protocol.md`; `freeze hint and form intake protocol`
- **When to load:** When the current validated feature needs project-owned freeze intake, a manual Freeze GUI form, or the canonical generic receive-ready blueprint; preserve Preview read-only and explicit human Confirm and Write.
- **When not to load:** Do not use as implementation authorization or as a substitute for the exact specialist owner.
- **Required companion prompts:** `brick_wall_comprehensive_quality_gate`; `pre_output_contract_gates`

### `pre_output_contract_gates` - Pre-Output Artifact Contract Gate

- **Prompt code:** `KPR-03-004`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md`
- **Priority:** `35`
- **Trigger phrases:** `pre-output contract`; `before terminal code`; `before zip delivery`
- **User intent examples:** `Dispatch an outgoing operational artifact to its exact current owner before emission.`
- **Aliases:** `KPR-03-004`; `pre_output_contract_gates`; `pre_output_contract_gates.md`; `pre-output artifact contract gate`
- **When to load:** Dispatch an outgoing operational artifact to its exact current owner before emission.
- **When not to load:** Do not use as implementation authorization or as a substitute for the exact specialist owner.
- **Required companion prompts:** `brick_wall_comprehensive_quality_gate`

### `professional_engineering_governance_template` - Professional Engineering Governance Profile Template

- **Prompt code:** `KPR-03-005`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/professional_engineering_governance_template.md`
- **Priority:** `25`
- **Trigger phrases:** `governance profile template`; `draft project governance`
- **User intent examples:** `Draft a Project-specific governance profile without creating a parallel authority.`
- **Aliases:** `KPR-03-005`; `professional_engineering_governance_template`; `professional_engineering_governance_template.md`; `professional engineering governance profile template`
- **When to load:** Draft a Project-specific governance profile without creating a parallel authority.
- **When not to load:** Do not use as implementation authorization or as a substitute for the exact specialist owner.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `workflow_handoff_template` - Generic Workflow Handoff Profile Template

- **Prompt code:** `KPR-03-006`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/workflow_handoff_template.md`
- **Priority:** `25`
- **Trigger phrases:** `generic workflow handoff template`; `draft handoff profile`
- **User intent examples:** `Draft a generic factual handoff only when no current generated owner exists.`
- **Aliases:** `KPR-03-006`; `workflow_handoff_template`; `workflow_handoff_template.md`; `generic workflow handoff profile template`
- **When to load:** Draft a generic factual handoff only when no current generated owner exists.
- **When not to load:** Do not use as implementation authorization or as a substitute for the exact specialist owner.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `self_contained_freeze_entry_intake_zip` - Self-Contained Freeze Entry Intake ZIP

- **Prompt code:** `KPR-03-007`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/self_contained_freeze_entry_intake_zip.md`
- **Priority:** `27`
- **When to load:** When the user requests one self-contained ZIP that loads the currently validated feature into Freeze Feature After Update -> New Local Freeze Entry for the currently selected Project.
- **When not to load:** Do not load for ordinary source patch installation, direct frozen-memory writes, unvalidated features, or freeze-form text only.
- **Required companion prompts:** `freeze_code_intake_and_form_protocol`; `freeze_candidate_pre_output_audit`; `pre_output_contract_gates`; `implementation_and_delivery_protocol`

### `freeze_candidate_pre_output_audit` - Freeze Candidate Pre-Output Audit Protocol

- **Prompt code:** `KPR-03-008`
- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_candidate_pre_output_audit.md`
- **Priority:** `36`
- **Trigger phrases:** `freeze candidate`; `freeze form correction`; `review freeze candidate`; `before freeze JSON`; `freeze blueprint`; `Get Blueprint Freeze`
- **User intent examples:** `Audit an AI-authored local freeze candidate from evidence before emitting it to the Freeze GUI receiver.`
- **Aliases:** `KPR-03-008`; `freeze_candidate_pre_output_audit`; `freeze candidate pre-output audit`
- **When to load:** Immediately before an AI emits, approves, corrects, regenerates, or supplies the generic blueprint for a local Freeze GUI candidate/form; audit receiver schema, path owner roots, evidence, complete post-write planned-next-step semantics, and KPR-03-003/button blueprint parity.
- **When not to load:** Do not use as patch-sidecar schema owner, local freeze writer authority, or substitute for freeze intake and human confirmation.
- **Required companion prompts:** `freeze_code_intake_and_form_protocol`; `pre_output_contract_gates`; `brick_wall_comprehensive_quality_gate`

## Class 04 - Box Architecture and Boundaries

### KPR-04-001 - Box Architecture Canon

- Path: `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md`
- Use for bounded ownership, public/private contract law, authoritative state,
  dependencies, lifecycle vocabulary, and the Box Boundary Audit.

### KPR-04-006 - Boundary-First Repair Protocol

- Path: `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/boundary_first_repair_protocol.md`
- Use when the visible symptom may not belong to the true repair owner.

### KPR-04-002 - KANDA Box Shielding Canon

- Path: `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md`
- Use only after a risk-based shield applicability decision proves unique value.

### KPR-04-003 - Project Folder Organization Canon

- Path: `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/project_folder_organization_canon.md`
- Use for artifact classification, canonical placement, root/owner conflicts, and
  folder migration obligations.

### KPR-04-004 - Stateful Control Regression Canon

- Path: `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/stateful_control_regression_canon.md`
- Use for GUI option identity, persistence, hydration, fallback, caption, and
  sizing regressions.

### Retired Class 04 identities

- `closed_box_delivery_canon` -> `KPR-04-001 box_architecture_canon`.
- `KPR-04-007 governed_architecture_companion_handoff` -> current canonical
  owner dispatch. The compact file is a deprecated redirect with no route.
## Patch Delivery And Validation (`05_patch_delivery_and_validation`)

### `bundle_gated_development_workflow` - Bundle-Gated Development Workflow

- **Code:** `KPR-05-002`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/bundle_gated_development_workflow.md`
- **Status / load:** `active` / `routed`
- **When to load:** When an authorized change requires an installable or distributable release unit.
- **When not to load:** Do not load for read-only audit, explanation-only work, or an edit that will not be packaged.
- **Triggers:** `installable release`; `bundle gated release`; `package this change`; `release lifecycle`; `build a patch bundle`
- **Aliases:** `KPR-05-002`; `bundle_gated_development_workflow`; `bundle gated development workflow`; `installable release lifecycle`; `kanda_bundle_gated_development_workflow`
- **Required companion prompts:** `brick_wall_comprehensive_quality_gate`; `patch_install_delivery_error_register`
- **Optional companion prompts:** `project_tool_boundary_canon`; `box_architecture_canon`; `implementation_and_delivery_protocol`; `pre_output_contract_gates`

### `implementation_and_delivery_protocol` - Implementation and Delivery Protocol

- **Code:** `KPR-05-003`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md`
- **Status / load:** `active` / `routed`
- **When to load:** After implementation authorization when an installable release needs payload and installer construction.
- **When not to load:** Do not load for analysis-only work or before release admission.
- **Triggers:** `construct patch payload`; `prepare installer`; `surgical delivery`; `baseline hash allowlist`; `rollback package`
- **Aliases:** `KPR-05-003`; `implementation_and_delivery_protocol`; `implementation and delivery protocol`; `surgical patch construction`; `installer preparation`
- **Required companion prompts:** `brick_wall_comprehensive_quality_gate`; `bundle_gated_development_workflow`; `patch_install_delivery_error_register`
- **Optional companion prompts:** `project_tool_boundary_canon`; `pre_output_contract_gates`; `terminal_cleanup_contract`

### `implementation_roadmap_builder` - Implementation Roadmap Builder - Draft Template

- **Code:** `KPR-05-004`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_roadmap_builder.md`
- **Status / load:** `active` / `on_request`
- **When to load:** Only when the user explicitly requests a roadmap, checklist, or progress-tracking draft.
- **When not to load:** Do not auto-load for normal KANDA implementation or treat the tracker as execution evidence.
- **Triggers:** `draft an implementation roadmap`; `roadmap template`; `make a progress tracker`; `conceptual implementation plan`
- **Aliases:** `KPR-05-004`; `implementation_roadmap_builder`; `implementation roadmap draft`; `roadmap template`; `progress tracker template`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.
- **Optional companion prompts:** `brick_wall_comprehensive_quality_gate`; `cooperative_implementation_methodology`; `workflow_handoff_template`

### `patch_validate_freeze_error_memory_routine_blueprint` - Answer Validate Freeze Memorize Error Routine Blueprint

- **Code:** `KPR-05-005`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_validate_freeze_error_memory_routine_blueprint.md`
- **Status / load:** `active` / `on_request`
- **When to load:** When the user presses the Show Project to AI routine button or asks to continue current source or compact evidence through one update ZIP, one fail-closed Install -> Enter x2 -> Validate paste unit, human-gated Freeze, and final Error Memory disposition.
- **When not to load:** Do not load for explanation-only work with no release, validation, Freeze, or Error Memory continuation.
- **Triggers:** `Answer, Validate, Freeze, Memorize Error`; `one zip install enter enter validate freeze error memory`; `compact update release`; `finish release phases`; `copy recovery routine`
- **Aliases:** `KPR-05-005`; `patch_validate_freeze_error_memory_routine_blueprint`; `Show Project to AI recovery blueprint`; `Answer Validate Freeze Memorize Error`; `recovery routine owner dispatch`
- **Required companion prompts:** `project_tool_boundary_canon`; `brick_wall_comprehensive_quality_gate`; `durable_document_artifact_routing_canon`
- **Optional companion prompts:** `bundle_gated_development_workflow`; `implementation_and_delivery_protocol`; `pre_output_contract_gates`; `patch_install_delivery_error_register`; `terminal_cleanup_contract`; `freeze_code_intake_and_form_protocol`; `self_contained_freeze_entry_intake_zip`; `error_memory_ai_formulary_startup_canon`; `self_contained_error_memory_lesson_intake_zip`

### `patch_install_delivery_error_register` - Patch Install Delivery Active Regression Index

- **Prompt code:** `KPR-05-001`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_install_delivery_error_register.md`
- **Priority:** `11`
- **Trigger phrases:** `patch install error`; `delivery regression`; `isolated ZIP`; `root-drive staging`; `validation evidence failure`
- **User intent examples:** `Check current delivery regression classes before releasing a patch.`
- **Aliases:** `KPR-05-001`; `patch_install_delivery_error_register`; `patch regression index`
- **When to load:** Conditionally required before patch-related output and delivery-regression repair.
- **When not to load:** Do not load at every startup and do not use as an append-only traceback log.
- **Required companion prompts:** `daily_patch_delivery_guardrails`; `implementation_and_delivery_protocol`; `terminal_cleanup_contract`


### `terminal_cleanup_contract` - Terminal Cleanup Contract

- **Code:** `KPR-05-007`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/terminal_cleanup_contract.md`
- **Status / load:** `active` / `always_startup`
- **When to load:** Startup bridge is always visible; load the full prompt when emitting or auditing PowerShell terminal behavior.
- **When not to load:** Do not load the full prompt for tasks with no terminal output.
- **Triggers:** `terminal cleanup`; `Clear-Host`; `install success footer`; `PowerShell block`; `Press Enter to clear terminal`; `PowerShell shows >>`
- **Aliases:** `KPR-05-007`; `terminal_cleanup_contract`; `terminal cleanup contract`; `PowerShell cleanup`; `clean PowerShell prompt`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.
- **Optional companion prompts:** `pre_output_contract_gates`; `implementation_and_delivery_protocol`; `patch_install_delivery_error_register`

### `self_contained_error_memory_lesson_intake_zip` - Self-Contained Error Memory Lesson Intake ZIP

- **Code:** `KPR-05-008`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/self_contained_error_memory_lesson_intake_zip.md`
- **Status / load:** `active` / `on_request`
- **When to load:** When the user requests one self-contained ZIP that stages one or more validated lessons as `pending` transport in the Error Memory lesson library; GUI admission normalizes the working lesson to `draft`.
- **When not to load:** Do not load for direct active memorization, ordinary patch delivery, or when no reusable lesson candidate exists.
- **Triggers:** `Send Zip Errors`; `create error lesson loader ZIP`; `self-contained Error Memory ZIP`; `stage Error Memory lessons for approval`; `pending error lesson intake`
- **Aliases:** `KPR-05-008`; `self_contained_error_memory_lesson_intake_zip`; `Send Zip Errors`; `send zip errors`; `self-contained Error Memory ZIP`; `Error Memory lesson intake loader`
- **Required companion prompts:** `error_memory_ai_formulary_startup_canon`; `bundle_gated_development_workflow`; `implementation_and_delivery_protocol`; `pre_output_contract_gates`
- **Optional companion prompts:** `terminal_cleanup_contract`; `patch_install_delivery_error_register`; `patch_validate_freeze_error_memory_routine_blueprint`; `self_contained_freeze_entry_intake_zip`

### `router_bridge_user_detected_correction` - User-Detected Correction Incident Dispatcher

- **Code:** `KPR-05-006`
- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_user_detected_correction.md`
- **Status / load:** `active` / `routed`
- **When to load:** Only when a real prior-answer, source, path, install, validation, delivery, startup, freeze, or Error Memory defect is identified.
- **When not to load:** Do not load for ordinary feature work, speculative planning, or explanation without a demonstrated incident.
- **Triggers:** `you made a mistake`; `validation failed`; `install failed`; `wrong path`; `wrong file`; `coded from memory`; `missing STATUS: IN_SYNC`; `freeze blocked`; `AI detected an implementation error`
- **Aliases:** `KPR-05-006`; `router_bridge_user_detected_correction`; `user detected correction`; `correction incident`; `AI mistake correction`
- **Required companion prompts:** `patch_install_delivery_error_register`
- **Optional companion prompts:** `brick_wall_comprehensive_quality_gate`; `pre_output_contract_gates`; `terminal_cleanup_contract`; `freeze_code_intake_and_form_protocol`; `error_memory_ai_formulary_startup_canon`; `project_tool_boundary_canon`

## Refactor And Architecture Hardening (`06_refactor_and_architecture_hardening`)

### `architecture_hardening_triage_protocol` — Architecture Hardening Triage Protocol

- **Prompt code:** `KPR-06-005`
- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/architecture_hardening_triage_protocol.md`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** Current evidence demonstrates an architecture risk requiring owner and protection-gap triage.
- **When not to load:** Broad cleanup ideas, isolated local edits, or implementation authorization.
- **Required companion prompts:** `box_architecture_canon`; `boundary_first_repair_protocol`; `kanda_box_shielding_canon`

### `architecture_hardening_triage_template` — Architecture Hardening Triage Record Template

- **Prompt code:** `KPR-06-006`
- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/architecture_hardening_triage_template.md`
- **Status:** `draft_template`
- **Load type:** `explicit_on_request`
- **When to load:** A fillable architecture-hardening triage record is explicitly requested.
- **When not to load:** Actual hardening triage or any mutation authorization.
- **Required companion prompts:** `architecture_hardening_triage_protocol`

### `large_module_refactor_protocol` — Large Module Creation and Refactor Protocol

- **Prompt code:** `KPR-06-007`
- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** A new or touched module exceeds or would exceed 500 physical lines, or current evidence proves material cohesion or dependency problems.
- **When not to load:** Small local edits that remain within the size and cohesion contract.
- **Required companion prompts:** `box_architecture_canon`; `large_module_refactor_template`

### `large_module_refactor_template` — Large Module Refactor Planning Record Template

- **Prompt code:** `KPR-06-008`
- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_template.md`
- **Status:** `draft_template`
- **Load type:** `explicit_on_request`
- **When to load:** A fillable large-module assessment or planning record is explicitly requested.
- **When not to load:** Actual refactoring or any mutation authorization.
- **Required companion prompts:** `large_module_refactor_protocol`

### `prompt_insertion_and_router_registration_protocol` - Prompt Insertion and Router Registration Protocol

- **File:** `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_insertion_and_router_registration_protocol.md`
- **Priority:** `36`
- **Trigger phrases:** `insert a new prompt`; `add a new prompt`; `create a new prompt`; `register a prompt in the router`; `make the router call this prompt`; `activate a prompt in router logic`; `connect a prompt to the router`; `bridge a prompt to prompt router logic`; `add prompt to ACTIVE_PROMPTS`; `prompt insertion protocol`; `prompt router registration`
- **User intent examples:** `Create a new prompt and connect it to the router.`; `Bridge this prompt to prompt router logic without making it always-startup.`; `Add this prompt to ACTIVE_PROMPTS with metadata and routing validation.`
- **Aliases:** `prompt insertion and router registration protocol`; `prompt_insertion_and_router_registration_protocol`; `prompt bridge insertion protocol`; `prompt router registration`
- **When to load:** When the task asks to create, insert, update, route, bridge, register, or make available a prompt in the KANDA prompt workspace.
- **When not to load:** Do not load for ordinary implementation tasks that do not change prompt-library files or routing awareness.
- **Required companion prompts:** `prompt_canon_reconciliation_protocol`; `prompt_audit_canon`; `project_specific_prompt_generalization`; `prompt_identity_code_registry_canon`; `prompt_navigation_index`; `prompt_router`

### `project_specific_prompt_generalization` — Project-Specific Prompt Generalization

- **File:** `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/project_specific_prompt_generalization.md`
- **Priority:** `35`
- **Trigger phrases:** `generalize prompts`; `project-specific prompts`; `remove EEG specificity`; `make project agnostic`; `generalization`
- **User intent examples:** `Generalize these EEG project prompts for KANDA Reasoner.`
- **Aliases:** `canon`; `generalization`; `project`; `project-specific prompt generalization`; `project_specific_prompt_generalization`; `project_specific_prompt_generalization.md`; `prompt audit`; `prompt authoring`; `specific`
- **When to load:** When importing prompts/canons from another project and making them reusable.
- **When not to load:** Do not load when preserving a project-specific prompt unchanged.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`; `prompt_substitution_map`

### `prompt_audit_canon` — Prompt Audit Canon

- **File:** `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_audit_canon.md`
- **Priority:** `35`
- **Trigger phrases:** `audit prompts`; `prompt batch audit`; `review prompt files`; `prompt canon audit`; `prompt quality`
- **User intent examples:** `Audit this batch of prompts and decide keep/update/deprecate.`
- **Aliases:** `audit`; `canon`; `prompt audit`; `prompt audit canon`; `prompt authoring`; `prompt_audit_canon`; `prompt_audit_canon.md`
- **When to load:** When reviewing prompt files for quality, duplication, status, or integration.
- **When not to load:** Do not load for normal code refactor.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`; `prompt_substitution_map`

### `prompt_canon_reconciliation_protocol` — Prompt Canon Reconciliation Protocol

- **File:** `ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_canon_reconciliation_protocol.md`
- **Priority:** `35`
- **Trigger phrases:** `reconcile prompts`; `deduplicate prompts`; `clean prompt folder`; `rename prompts`; `prompt canon reconciliation`
- **User intent examples:** `Mechanically reconcile 84 staged prompt files into clean active prompts.`
- **Aliases:** `canon`; `prompt audit`; `prompt authoring`; `prompt canon reconciliation protocol`; `prompt_canon_reconciliation_protocol`; `prompt_canon_reconciliation_protocol.md`; `reconciliation`
- **When to load:** When deduplicating, renaming, promoting, or cleaning prompt-canon folders.
- **When not to load:** Do not load for writing a new single prompt from scratch.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`; `prompt_substitution_map`

## Python Engineering Core (`08_python_engineering_core`)

### `python_clean_architecture` — Python Clean Architecture

- **Code:** `KPR-08-001`
- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_clean_architecture.md`
- **Priority:** `50`
- **Trigger phrases:** `dependency direction`; `framework isolation`; `ports and adapters`; `composition root`; `clean architecture python`
- **User intent examples:** `Review whether this Python system needs ports, adapters, or a clearer composition boundary.`
- **Aliases:** `KPR-08-001`; `python clean architecture`; `python dependency direction`; `python_clean_architecture`
- **When to load:** When dependency direction, framework isolation, ports/adapters, or a composition boundary is materially involved.
- **When not to load:** Do not load for local readability, simple scripts, KANDA box ownership, or generic architecture discussion without Python dependency evidence.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_clean_code` — Python Clean Code

- **Code:** `KPR-08-002`
- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_clean_code.md`
- **Priority:** `50`
- **Trigger phrases:** `python readability`; `function clarity`; `naming review`; `local code cohesion`; `python documentation clarity`
- **User intent examples:** `Review this Python module for local readability and maintainability without changing its architecture.`
- **Aliases:** `KPR-08-002`; `python clean code`; `clean_code_python`; `python_clean_code`
- **When to load:** When local naming, readability, documentation, function clarity, or class cohesion is central.
- **When not to load:** Do not load as architecture, refactoring, testing, typing, security, or resilience authority.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_design_patterns` — Python Design Patterns

- **Code:** `KPR-08-003`
- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_design_patterns.md`
- **Priority:** `50`
- **Trigger phrases:** `pattern selection`; `strategy or function`; `adapter pattern python`; `observer lifecycle`; `factory tradeoff`
- **User intent examples:** `Decide whether this recurring Python design problem needs a named pattern or a simpler language feature.`
- **Aliases:** `KPR-08-003`; `python design patterns`; `python pattern selection`; `python_design_patterns`
- **When to load:** When a demonstrated structural or behavioral variation requires an explicit pattern-selection decision.
- **When not to load:** Do not load for simple direct code, DDD, enterprise persistence patterns, GUI lifecycle, or async/distributed design owned elsewhere.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_domain_driven_design` — Python Domain-Driven Design

- **Code:** `KPR-08-004`
- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_domain_driven_design.md`
- **Priority:** `50`
- **Trigger phrases:** `ubiquitous language`; `bounded context`; `domain invariants`; `aggregate boundary`; `domain event semantics`
- **User intent examples:** `Determine whether domain complexity justifies DDD and define the smallest evidence-grounded model.`
- **Aliases:** `KPR-08-004`; `python domain driven design`; `python DDD`; `python_domain_driven_design`
- **When to load:** When domain language, invariants, subdomains, or bounded contexts materially drive the design.
- **When not to load:** Do not load for simple CRUD, utility scripts, generic dependency direction, persistence implementation, or messaging delivery mechanics.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_enterprise_architecture` - Python Enterprise Application Patterns

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_enterprise_architecture.md`
- **Code:** `KPR-08-005`
- **Category:** `08_python_engineering_core`
- **Load type:** `on_request`
- **When to load:** When enterprise persistence patterns, application services, transactions, object identity, or concurrency-control patterns are the central concern.
- **When not to load:** Do not load for small scripts, simple CRUD, generic dependency architecture, DDD modeling, database tuning, or unmeasured performance work.
- **Aliases:** `KPR-08-005`; `python enterprise application patterns`; `python enterprise architecture`; `python_enterprise_architecture`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_high_performance` - Python Performance Evidence and Optimization

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_high_performance.md`
- **Code:** `KPR-08-006`
- **Category:** `08_python_engineering_core`
- **Load type:** `on_request`
- **When to load:** When runtime, latency, throughput, memory, I/O, profiling, or benchmark evidence is a primary requirement.
- **When not to load:** Do not load when no named performance objective or suspected material bottleneck exists.
- **Aliases:** `KPR-08-006`; `python performance evidence`; `python high performance`; `python_high_performance`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_legacy_code_workflow` - Python Legacy Code Stabilization Workflow

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_legacy_code_workflow.md`
- **Code:** `KPR-08-007`
- **Category:** `08_python_engineering_core`
- **Load type:** `on_request`
- **When to load:** When existing Python code is risky, poorly understood, weakly protected, side-effectful, or historically brittle.
- **When not to load:** Do not load for a well-understood greenfield module or as a substitute for the refactoring or testing owners.
- **Aliases:** `KPR-08-007`; `A022`; `python legacy code stabilization`; `python legacy code workflow`; `python_legacy_code_workflow`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_pragmatic_programmer` - Python Pragmatic Trade-off and Reversible Progress

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_pragmatic_programmer.md`
- **Code:** `KPR-08-008`
- **Category:** `08_python_engineering_core`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When pragmatic trade-off, reversibility, or proportional automation is the central concern.
- **When not to load:** Do not load as a replacement for a technical specialist.
- **Aliases:** `KPR-08-008`; `pragmatic trade-off`; `python_pragmatic_programmer`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_refactoring` - Python Behavior-Preserving Refactoring

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_refactoring.md`
- **Code:** `KPR-08-009`
- **Category:** `08_python_engineering_core`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When bounded Python structure must improve without intended behavior change.
- **When not to load:** Do not load for legacy stabilization, large-module decomposition, or feature behavior changes.
- **Aliases:** `KPR-08-009`; `python refactoring`; `python_refactoring`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `software_engineering_books_master` - Software Engineering Books Synthesis Map

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/software_engineering_books_master.md`
- **Code:** `KPR-08-010`
- **Category:** `08_python_engineering_core`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When an explicit cross-book principle comparison or educational specialist map is needed.
- **When not to load:** Do not load as a master governance or implementation prompt.
- **Aliases:** `KPR-08-010`; `software engineering books synthesis`; `software_engineering_books_master`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_documentation_developer_experience` - Python Documentation and Developer Experience

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_documentation_developer_experience.md`
- **Code:** `KPR-09-011`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When documentation architecture, onboarding, examples, docstrings, or DX is central.
- **When not to load:** Do not load for local naming only or project-specific help styling.
- **Aliases:** `KPR-09-011`; `python documentation`; `python_documentation_developer_experience`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_observability_logging_metrics_tracing` - Python Observability: Logging, Metrics, and Tracing

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_observability_logging_metrics_tracing.md`
- **Code:** `KPR-09-012`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When runtime telemetry and diagnosis are central.
- **When not to load:** Do not load when no telemetry change is needed.
- **Aliases:** `KPR-09-012`; `python observability`; `python_observability_logging_metrics_tracing`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_resilience_error_handling` - Python Failure Semantics and Resilience

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_resilience_error_handling.md`
- **Code:** `KPR-09-013`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When failure, deadline, retry, idempotency, degradation, or recovery semantics are central.
- **When not to load:** Do not load for exception formatting alone.
- **Aliases:** `KPR-09-013`; `python resilience`; `python_resilience_error_handling`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_security_threat_prevention` - Python Security and Threat Prevention

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_security_threat_prevention.md`
- **Code:** `KPR-09-014`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When trust boundaries, threats, authorization, secrets, archives, or hostile input are central.
- **When not to load:** Do not load as a generic quality checklist.
- **Aliases:** `KPR-09-014`; `python security`; `python_security_threat_prevention`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_testing_pytest` - Python Testing and Pytest Strategy

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_testing_pytest.md`
- **Code:** `KPR-09-015`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When testing strategy, pytest, regression protection, or result interpretation is central.
- **When not to load:** Do not impose universal coverage or mutation quotas.
- **Aliases:** `KPR-09-015`; `python testing`; `python_testing_pytest`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_validation_serialisation_type_safety` - Python Boundary Validation, Serialization, and Type Safety

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_validation_serialisation_type_safety.md`
- **Code:** `KPR-09-016`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When invalid or ambiguous data crossing a boundary is the principal risk.
- **When not to load:** Do not use for domain authorization or API protocol semantics.
- **Aliases:** `KPR-09-016`; `python validation`; `python_validation_serialisation_type_safety`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `tab4_docstring_quality_roadmap` - Tab 4 Docstring Quality Roadmap - Deprecated Global Route

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/tab4_docstring_quality_roadmap.md`
- **Code:** `KPR-09-017`
- **Category:** `09_python_quality_security_observability`
- **Status:** `deprecated`
- **Load type:** `never`
- **When to load:** Never load as a global active route; this is a deprecated compatibility tombstone.
- **When not to load:** Use KPR-09-011 for generic documentation and inspect current project source for Tab 4 status.
- **Aliases:** `KPR-09-017`; `tab4_docstring_quality_roadmap`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `python_api_design` - Python API and External Interface Contracts

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_api_design.md`
- **Code:** `KPR-10-001`
- **Category:** `10_python_api_data_async_config`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When an API or external interface contract is central.
- **When not to load:** Do not load for internal function structure or persistence implementation.
- **Aliases:** `KPR-10-001`; `python API design`; `python_api_design`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_async_parallel_distributed` - Python Concurrency, Parallel, and Distributed Execution

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_async_parallel_distributed.md`
- **Code:** `KPR-10-002`
- **Category:** `10_python_api_data_async_config`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When concurrency model, task lifecycle, cancellation, backpressure, or distributed execution is central.
- **When not to load:** Do not load for simple synchronous work or unmeasured performance assumptions.
- **Aliases:** `KPR-10-002`; `python concurrency`; `python_async_parallel_distributed`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_configuration_feature_flags` - Python Configuration and Feature-Flag Lifecycle

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_configuration_feature_flags.md`
- **Code:** `KPR-10-003`
- **Category:** `10_python_api_data_async_config`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When configuration schema, precedence, secret references, reload, or flag lifecycle is central.
- **When not to load:** Do not load for constants, entitlements, or deployment injection alone.
- **Aliases:** `KPR-10-003`; `python configuration`; `python_configuration_feature_flags`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_database_design_optimisation` - Python Database Design, Queries, and Migrations

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_database_design_optimisation.md`
- **Code:** `KPR-10-004`
- **Category:** `10_python_api_data_async_config`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When database schema, queries, migrations, transactions, or engine behavior is central.
- **When not to load:** Do not load for application Repository design or work with no persistence.
- **Aliases:** `KPR-10-004`; `python database design`; `python_database_design_optimisation`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `kubernetes_deployment_operations` - Kubernetes Deployment and Operations

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/kubernetes_deployment_operations.md`
- **Code:** `KPR-11-001`
- **Category:** `11_productization_and_release_readiness`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When an actual container or Kubernetes workload needs deployment and operational design.
- **When not to load:** Do not load for speculative Kubernetes adoption or as a universal production checklist.
- **Aliases:** `KPR-11-001`; `kubernetes deployment`; `kubernetes_deployment_operations`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `productization_readiness_roadmap` - Productization Readiness Roadmap

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/productization_readiness_roadmap.md`
- **Code:** `KPR-11-002`
- **Category:** `11_productization_and_release_readiness`
- **Status:** `deprecated`
- **Load type:** `never`
- **When to load:** Never load globally; this is a deprecated historical project-specific roadmap tombstone.
- **When not to load:** Use current project capability evidence and active Class 11 specialists.
- **Aliases:** `KPR-11-002`; `productization_readiness_roadmap`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `professional_ai_assisted_engineering_framework` - AI-Assisted Engineering Operating Model Overview

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/professional_ai_assisted_engineering_framework.md`
- **Code:** `KPR-11-003`
- **Category:** `11_productization_and_release_readiness`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When a concise non-authoritative human/AI role and work-state overview is needed.
- **When not to load:** Do not load as a master implementation, validation, or freeze authority.
- **Aliases:** `KPR-11-003`; `AI-assisted engineering operating model`; `professional_ai_assisted_engineering_framework`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `professional_infrastructure_roadmap` - Professional Infrastructure Roadmap

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/professional_infrastructure_roadmap.md`
- **Code:** `KPR-11-004`
- **Category:** `11_productization_and_release_readiness`
- **Status:** `deprecated`
- **Load type:** `never`
- **When to load:** Never load globally; this is a deprecated historical missing-infrastructure tombstone.
- **When not to load:** Inspect current source and use a source-bound project capability-status matrix.
- **Aliases:** `KPR-11-004`; `professional_infrastructure_roadmap`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `python_lifecycle_versioning_deprecation` - Python Lifecycle, Versioning, Deprecation, and End-of-Life

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/python_lifecycle_versioning_deprecation.md`
- **Code:** `KPR-11-005`
- **Category:** `11_productization_and_release_readiness`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When version policy, compatibility, deprecation, support or EOL is central.
- **When not to load:** Do not load for legacy refactoring, database migration mechanics or packaging installation.
- **Aliases:** `KPR-11-005`; `python lifecycle versioning`; `python_lifecycle_versioning_deprecation`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `python_site_reliability_engineering` - Python Service Reliability Engineering

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/python_site_reliability_engineering.md`
- **Code:** `KPR-11-006`
- **Category:** `11_productization_and_release_readiness`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When an operationally owned production service needs SLI/SLO, incident, toil or capacity governance.
- **When not to load:** Do not load for local tools or as a universal Google SRE checklist.
- **Aliases:** `KPR-11-006`; `python SRE`; `python_site_reliability_engineering`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `error_memory_active_ready_correction_blueprint` - Error Memory Active-Ready Correction Blueprint

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_correction_blueprint.md`
- **Code:** `KPR-12-002`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** When a real Error Memory draft must be corrected or evaluated for active readiness.
- **When not to load:** Do not load for ordinary code changes or to invent validation evidence.
- **Aliases:** `KPR-12-002`; `Error Memory correction blueprint`; `error_memory_active_ready_correction_blueprint`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `project_tool_boundary_canon` - Project Tool Boundary Canon

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md`
- **Prompt code:** `KPR-12-001`
- **Priority:** `5`
- **Load type:** `always_startup`
- **Trigger phrases:** `project versus tool`; `project vs tool`; `tool identity`; `active project identity`; `project in use`; `selected project root`; `active project root`; `target project`; `my_project`; `PROJECT_ROOT`; `do not hardcode kanda_reasoner`; `freeze paths active project`; `handoff path active project`; `patch staging active project`; `forbidden nested support root`; `support root inside project source`; `E:/kanda_reasoner/kanda_reasoner_show_project_to_AI`; `canonical external sibling support root`
- **User intent examples:** `Keep KANDA Reasoner separate from the active project in every coding task.`; `Make sure freeze paths use the project in use, not always kanda_reasoner.`; `Canonize the distinction between the tool and <my_project>.`
- **Aliases:** `project tool boundary`; `project_tool_boundary_canon`; `tool target boundary`; `active project boundary`; `selected project boundary`
- **When to load:** Always at startup. Apply to every coding, patching, validation, freeze, staging, handoff, Workbench, source-inspection, or project-root task.
- **When not to load:** The canon remains loaded as a boundary invariant; simple non-project writing tasks normally require no additional action from it.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`

### `data_transform_pipeline_invariants` - Data Transform Pipeline Invariants

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/data_transform_pipeline_invariants.md`
- **Code:** `KPR-12-009`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When source-to-derived lineage, transform provenance or rebuild correctness is central.
- **When not to load:** Do not load for transform selection resolution without pipeline lineage concerns.
- **Aliases:** `KPR-12-009`; `data transform pipeline invariants`; `data_transform_pipeline_invariants`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `desktop_help_document_layout_canon` - KANDA Desktop Help Document Layout Profile

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/desktop_help_document_layout_canon.md`
- **Code:** `KPR-12-010`
- **Category:** `12_generalized_project_canons`
- **Status:** `active_project_overlay`
- **Load type:** `on_request`
- **When to load:** When the KANDA help system or an explicitly adopted equivalent profile is being authored or reviewed.
- **When not to load:** Do not load as a universal documentation or runtime visual-engine canon.
- **Aliases:** `KPR-12-010`; `KANDA desktop help layout`; `desktop_help_document_layout_canon`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `domain_decision_table_template` - Versioned Domain Decision Table Template

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/domain_decision_table_template.md`
- **Code:** `KPR-12-011`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When multiple discrete domain rules need a versioned, testable matrix.
- **When not to load:** Do not load for continuous/probabilistic decisions or undefined domain policy.
- **Aliases:** `KPR-12-011`; `domain decision table`; `domain_decision_table_template`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `plugin_package_import_canon` - Plugin Package Import and Trust Canon

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/plugin_package_import_canon.md`
- **Code:** `KPR-12-012`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When user-importable package trust, permissions and lifecycle are central.
- **When not to load:** Do not load for ordinary patch ZIPs or to invent a universal plugin engine.
- **Aliases:** `KPR-12-012`; `plugin package import`; `plugin_package_import_canon`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `shared_visual_render_engine_canon` - Shared Visual Semantic Contract

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/shared_visual_render_engine_canon.md`
- **Code:** `KPR-12-013`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When multiple consumers represent the same conceptual visual object or scene.
- **When not to load:** Do not load for static editorial artwork or generic UI styling.
- **Aliases:** `KPR-12-013`; `shared visual semantics`; `shared_visual_render_engine_canon`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `transform_resolver_architecture_contract` - Transform Resolver Architecture Contract

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/transform_resolver_architecture_contract.md`
- **Code:** `KPR-12-014`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When stable identities and selectable transforms must resolve into controlled operations.
- **When not to load:** Do not load for pipeline lineage/rebuild or direct operation execution.
- **Aliases:** `KPR-12-014`; `transform resolver contract`; `transform_resolver_architecture_contract`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `web_ai_large_module_refactor_exchange_protocol`

- Prompt code: `KPR-06-001`
- Load when: an exact Planner package needs bounded external architecture review.
- Do not load for: target-specific AST repair, direct source implementation, delivery mechanics, or freeze writing.
- Companions: `large_module_refactor_protocol`, `web_ai_planning_response_bundle_blueprint`, `brick_wall_comprehensive_quality_gate`.

### `web_ai_planning_response_bundle_blueprint`

- Prompt code: `KPR-06-002`
- Load when: an already-reasoned planning payload must be packaged for Imported Web AI Version intake.
- Do not load for: architecture reasoning, direct source implementation, or final freeze authority.
- Companions: `web_ai_large_module_refactor_exchange_protocol`, current Class 05 delivery owners.

### `web_ai_ast_split_risk_repair_protocol`

- Prompt code: `KPR-06-003`
- Load when: exact target source and current AST evidence require target-specific repair or a SAFE structural split.
- Do not load for: generic Planner review, universal module-size law, or final freeze writing.
- Companions: `large_module_refactor_protocol`, `python_refactoring`, `project_tool_boundary_canon`.

## Wave 8A Class 12 human-process and handbook specialists

### `peopleware_team_boundary` — Peopleware Team Boundary

- **Prompt code:** `KPR-12-007`
- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/peopleware_team_boundary.md`
- **Load when:** a software-delivery problem may be primarily human, organizational, workload, communication, or collaboration related.
- **Do not load for:** solo code mechanics, medical diagnosis, covert monitoring, personnel ranking, or implementation authorization.
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `practical_field_handbook_template` — Practical Field Handbook Template

- **Prompt code:** `KPR-12-008`
- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/practical_field_handbook_template.md`
- **Load when:** a supplied or reliably identified source must become a practical audience-specific handbook.
- **Do not load for:** invented source-faithful detail, substitute reproduction of a copyrighted work, or direct source implementation.
- **Companions:** `prompt_navigation_index`; current evidence sources when current claims require verification.

### `anti_hallucination_independent_ai_audit_full` - Independent Adversarial Engineering Audit - Full

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_independent_ai_audit_full.md`
- **Code:** `KPR-09-003`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When a consequential plan needs adversarial review and claim/assumption separation.
- **When not to load:** Do not label same-context self-review as independent.
- **Aliases:** `KPR-09-003`; `independent adversarial audit`; `anti_hallucination_independent_ai_audit_full`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `anti_hallucination_web_evidence_audit_full` - Current Web Evidence and Disconfirmation Audit - Full

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_web_evidence_audit_full.md`
- **Code:** `KPR-09-004`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When time-sensitive external claims require current primary-source verification.
- **When not to load:** Do not expose private project data or fabricate web access.
- **Aliases:** `KPR-09-004`; `web evidence audit`; `anti_hallucination_web_evidence_audit_full`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `anti_hallucination_book_literature_audit_full` - Verified Literature Architecture Audit - Full

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_book_literature_audit_full.md`
- **Code:** `KPR-09-005`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** When inspected literature can resolve a material architecture uncertainty.
- **When not to load:** Do not attribute claims to uninspected books or force a source count.
- **Aliases:** `KPR-09-005`; `verified literature audit`; `anti_hallucination_book_literature_audit_full`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `anti_hallucination_master_protocol_full` - Evidence Synthesis and Truthful Status Protocol - Full

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_master_protocol_full.md`
- **Code:** `KPR-09-006`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** As the final synthesis stage after evidence records exist.
- **When not to load:** Do not load as a mega-canon or implementation authority.
- **Aliases:** `KPR-09-006`; `evidence synthesis`; `anti_hallucination_master_protocol_full`
- **Required companion prompts:** none; dispatch supporting concerns only when current Project evidence requires them.

### `anti_hallucination_independent_ai_audit_short` - Independent Adversarial Audit - Short

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_independent_ai_audit_short.md`
- **Code:** `KPR-09-007`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** For bounded routine adversarial screening.
- **When not to load:** Escalate to KPR-09-003 when material risk or uncertainty appears.
- **Aliases:** `KPR-09-007`; `anti_hallucination_independent_ai_audit_short`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `anti_hallucination_web_evidence_audit_short` - Current Web Evidence Audit - Short

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_web_evidence_audit_short.md`
- **Code:** `KPR-09-008`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** For bounded current-source verification.
- **When not to load:** Escalate to KPR-09-004 when sources conflict or risk is material.
- **Aliases:** `KPR-09-008`; `anti_hallucination_web_evidence_audit_short`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `anti_hallucination_book_literature_audit_short` - Verified Literature Audit - Short

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_book_literature_audit_short.md`
- **Code:** `KPR-09-009`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** For a bounded verified literature check.
- **When not to load:** Escalate to KPR-09-005 when comparison or provenance is complex.
- **Aliases:** `KPR-09-009`; `anti_hallucination_book_literature_audit_short`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `anti_hallucination_protocol_short` - Evidence Synthesis Protocol - Short

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_protocol_short.md`
- **Code:** `KPR-09-010`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `on_request`
- **When to load:** For routine synthesis of bounded evidence records.
- **When not to load:** Escalate to KPR-09-006 when evidence conflicts or risk is material.
- **Aliases:** `KPR-09-010`; `anti_hallucination_protocol_short`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `anti_hallucination_full_group` - Evidence Verification Train - Full

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_full_group.md`
- **Code:** `KPR-09-001`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** When consequential work requires the full staged evidence-verification train.
- **When not to load:** Do not load for routine low-risk work or as implementation authority.
- **Aliases:** `KPR-09-001`; `anti_hallucination_full_group`; `full evidence train`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `anti_hallucination_short_group` - Evidence Verification Train - Short

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_short_group.md`
- **Code:** `KPR-09-002`
- **Category:** `09_python_quality_security_observability`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** When routine governed work needs a compact staged evidence review.
- **When not to load:** Escalate to KPR-09-001 for high-risk, conflicting, or uncertain work.
- **Aliases:** `KPR-09-002`; `anti_hallucination_short_group`; `short evidence train`
- **Required companions:** none; dispatch supporting concerns to current owners.

### `error_memory_active_ready_json_template` - Error Memory Marker-Wrapped JSON Output Envelope

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_json_template.md`
- **Code:** `KPR-12-003`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** Before emitting, approving, correcting, or regenerating the exact marker-wrapped final Error Memory lesson output envelope, or when Error Memory reports `MCARD_FORMATTED_LESSON_JSON_REQUIRED`.
- **When not to load:** Do not use as field-schema authority or before readiness evidence exists.
- **Aliases:** `KPR-12-003`; `Error Memory JSON envelope`; `error_memory_active_ready_json_template`
- **Exact output gate:** literal `KANDA_ERROR_LESSON_JSON_BEGIN` -> exactly one raw JSON object -> literal `KANDA_ERROR_LESSON_JSON_END`; no Markdown fence, escaped markers, writing block, citations, or prose.
- **Required companions:** none; dispatch supporting concerns to current owners.

### `error_memory_model_template` - Error Memory Human-Readable Lesson Model

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_model_template.md`
- **Code:** `KPR-12-004`
- **Category:** `12_generalized_project_canons`
- **Status:** `active`
- **Load type:** `routed`
- **When to load:** When a human-readable Error Memory lesson model verified against current application schema is needed.
- **When not to load:** Do not treat the template as stronger than current application schema/models.
- **Aliases:** `KPR-12-004`; `Error Memory model`; `error_memory_model_template`
- **Required companions:** none; dispatch supporting concerns to current owners.


### `kanda_desktop_help_exact_layout_blueprint` - KANDA Desktop Help Exact Layout Blueprint

- **Code:** `KPR-12-015`
- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/kanda_desktop_help_exact_layout_blueprint.md`
- **Category:** `12_generalized_project_canons`
- **Load type:** `companion_on_request`
- **When to load:** When a KANDA help page must reproduce the established book-style layout and design model exactly.
- **Required companion:** `desktop_help_document_layout_canon`
- **Aliases:** `KPR-12-015`; `KANDA help exact layout`; `kanda_desktop_help_exact_layout_blueprint`

## Self-contained Freeze/Error intake bridge

`KPR-05-005 patch_validate_freeze_error_memory_routine_blueprint` is the lifecycle bridge between:

- `KPR-03-007 self_contained_freeze_entry_intake_zip`; and
- `KPR-05-008 self_contained_error_memory_lesson_intake_zip`.

They remain separate specialist ZIP owners. Route shared selected-Project identity, feature identity, patch identity, focused validator, and current validation evidence through KPR-05-005. Never merge artifacts or human approval gates.
