# KANDA Prompt Navigation Index

Version: v3 intent-routing index

This file maps natural human requests to the correct clean prompt ID and companion prompt stack. The human does not need to know exact filenames. The AI should infer intent from trigger phrases, examples, aliases, and context.

## Routing Rules

- Match the user request against trigger phrases, user intent examples, aliases, and category context.
- If multiple prompts match, prefer the lower numeric `priority` value, then load required companion prompts.
- For implementation, refactor, prompt update, governance update, or bundle creation, include `box_architecture_canon` unless the selected prompt already is the box canon.
- For patch or delivery work, include `bundle_gated_development_workflow`, `evidence_freshness_gate`, and `implementation_and_delivery_protocol` when relevant.
- For freeze/governance, do not freeze unless validation/evidence has already passed.
- For prompt import/generalization/reconciliation, use prompt-authoring/audit prompts, not Python source-code prompts.
- For shielding requests, meaningful box milestones, stronger ML preparation, or authority-boundary protection, load `kanda_box_shielding_canon` with `box_architecture_canon` and the owning box context. Do not continue stronger work until the shield is validated and frozen.
- If intent remains ambiguous, load `prompt_router` plus this navigation index and ask one focused clarification.

## Prompt Routes
## Session Start And Navigation (`01_session_start_and_navigation`)

### `ai_human_partnership_session_start` — AI-Human Partnership Session Start

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/ai_human_partnership_session_start.md`
- **Priority:** `20`
- **Trigger phrases:** `AI human partnership`; `how should I ask you`; `roles in this session`; `human AI workflow`; `avoid vibe coding`
- **User intent examples:** `Set the roles: I lead, AI assists, validators decide.`
- **Aliases:** `ai-human partnership session start`; `ai_human_partnership_session_start`; `ai_human_partnership_session_start.md`; `boot`; `human`; `partnership`; `session`; `start`; `startup`
- **When to load:** When setting expectations for AI-human collaboration, discipline, and validation.
- **When not to load:** Do not load for small one-off questions that need no workflow.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `daily_reasoner_startup_loader` — Daily Reasoner Startup Loader

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/daily_reasoner_startup_loader.md`
- **Priority:** `20`
- **Trigger phrases:** `start reasoner session`; `daily reasoner start`; `load reasoner startup`; `begin KANDA reasoner work`; `what should I send today`
- **User intent examples:** `Start today's KANDA Reasoner session and load the working protocol.`
- **Aliases:** `boot`; `daily`; `daily reasoner startup loader`; `daily_reasoner_startup_loader`; `daily_reasoner_startup_loader.md`; `loader`; `reasoner`; `session`; `startup`
- **When to load:** At the beginning of a Reasoner-focused development or prompt-maintenance session.
- **When not to load:** Do not load for generic Python advice when no project context is needed.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `daily_session_start_prompt` — Daily Session Start Prompt

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/daily_session_start_prompt.md`
- **Priority:** `20`
- **Trigger phrases:** `start session`; `new session checklist`; `what should I upload`; `begin work today`; `session boot`
- **User intent examples:** `Tell me what to send before we work on the project.`
- **Aliases:** `boot`; `daily`; `daily session start prompt`; `daily_session_start_prompt`; `daily_session_start_prompt.md`; `session`; `start`; `startup`
- **When to load:** At the start of any project session to define context, files, and expected output.
- **When not to load:** Do not load after the active task and required files are already established.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `daily_startup_loader_template` — Daily Startup Loader Template

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/daily_startup_loader_template.md`
- **Priority:** `20`
- **Trigger phrases:** `create daily startup template`; `generic startup loader`; `new project daily loader`; `startup template`
- **User intent examples:** `Create a daily startup loader template for a new project.`
- **Aliases:** `boot`; `daily`; `daily startup loader template`; `daily_startup_loader_template`; `daily_startup_loader_template.md`; `loader`; `session`; `startup`
- **When to load:** When designing or adapting a reusable daily-startup prompt template.
- **When not to load:** Do not load for normal code implementation.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `general_prompt_stack_load_order` — General Prompt Stack Load Order

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/general_prompt_stack_load_order.md`
- **Priority:** `20`
- **Trigger phrases:** `load order`; `prompt stack order`; `which prompt first`; `startup stack`; `prompt precedence`
- **User intent examples:** `Which prompts should be loaded first for this task?`
- **Aliases:** `boot`; `general`; `general prompt stack load order`; `general_prompt_stack_load_order`; `general_prompt_stack_load_order.md`; `load`; `order`; `session`; `stack`; `startup`
- **When to load:** When deciding the order and priority of prompts/canons in a session.
- **When not to load:** Do not load when only a single isolated prompt is needed.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `project_startup_canon_template` — Project Startup Canon Template

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/project_startup_canon_template.md`
- **Priority:** `20`
- **Trigger phrases:** `project startup canon`; `new project canon`; `startup canon template`; `initialize project rules`
- **User intent examples:** `Make a startup canon for a new project.`
- **Aliases:** `boot`; `project`; `project startup canon template`; `project_startup_canon_template`; `project_startup_canon_template.md`; `session`; `startup`
- **When to load:** When creating a project-agnostic startup canon template.
- **When not to load:** Do not load for existing project sessions that already have a startup canon.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `reasoner_startup_canon` — Reasoner Startup Canon

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/reasoner_startup_canon.md`
- **Priority:** `20`
- **Trigger phrases:** `reasoner canon`; `load reasoner canon`; `KANDA reasoner startup`; `reasoner operating rules`
- **User intent examples:** `Start KANDA Reasoner with the official canon.`
- **Aliases:** `boot`; `reasoner`; `reasoner startup canon`; `reasoner_startup_canon`; `reasoner_startup_canon.md`; `session`; `startup`
- **When to load:** When the work specifically concerns KANDA Reasoner behavior, prompts, or app workflow.
- **When not to load:** Do not load for non-Reasoner projects unless adapting it as a template.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

### `session_start_upload_checklist` — Session Start Upload Checklist

- **File:** `ACTIVE_PROMPTS/01_session_start_and_navigation/session_start_upload_checklist.md`
- **Priority:** `20`
- **Trigger phrases:** `what files should I upload`; `upload checklist`; `session files`; `start checklist`; `what to send first`
- **User intent examples:** `Tell me exactly what files to upload before starting.`
- **Aliases:** `boot`; `checklist`; `session`; `session start upload checklist`; `session_start_upload_checklist`; `session_start_upload_checklist.md`; `start`; `startup`; `upload`
- **When to load:** Before a session when required project evidence/files are not yet known.
- **When not to load:** Do not load after all required files are already available.
- **Required companion prompts:** `prompt_navigation_index`; `prompt_router`

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

### `routing_signal_scorer_v3_pilot_copilot_phase0_router_canon` - RG-PILOT-000 Pilot/Copilot Phase 0 Router Canon

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md`
- **Priority:** `1`
- **Trigger phrases:** `Pilot/Copilot Phase 0`; `post-M35 continuation`; `start Pilot`; `start Copilot`; `create P0`; `Pilot scope charter`; `Pilot projection`; `Pilot simulation`; `Pilot disagreement taxonomy`; `Pilot implementation gate`; `Pilot router reproduction`; `reproduction-before-disagreement`; `Limited Shadow Runtime`; `human_review_mandatory`; `candidate_prompt_groups`; `simulated_required_prompt_groups`
- **User intent examples:** `Canonize Pilot/Copilot router logic after M35.`; `Create P0 for Pilot/Copilot Phase 0.`; `Can we implement Pilot projection now?`
- **Aliases:** `RG-PILOT-000`; `routing_signal_scorer_v3_pilot_copilot_phase0_router_canon`; `Pilot/Copilot router canon`; `post-M35 Pilot canon`; `P0 router canon`
- **When to load:** When KANDA work involves post-M35 Pilot/Copilot scope, P0, P-series milestones, Pilot projection/simulation, Copilot boundary, reproduction-before-disagreement, or any request that could grant Pilot/Copilot authority, prompt loading, persistence, training-data use, batch mode, or runtime shadow behavior.
- **When not to load:** Do not load for ordinary lexical routing-scorer patches unrelated to Pilot/Copilot, simple Fast Path explanation-only tasks, or as a substitute for current project files and freeze evidence during implementation.
- **Required companion prompts:** `kanda_routing_system_canon`; `kanda_box_shielding_canon`; `prompt_navigation_index`; `GROUP_ASSIMILATION_INDEX`


### `routing_signal_scorer_v3_lab_phase_entry_router_canon` - RG-LAB-000 ML LAB Phase Entry Router Canon

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_lab_phase_entry_router_canon.md`
- **Priority:** `1`
- **Trigger phrases:** `RG-LAB-000`; `LAB phase`; `ML LAB`; `ML lab/test`; `lab/test logic`; `start LAB after P12`; `continue after P12`; `go next after P12`; `LAB-0`; `lab charter`; `test lab charter`; `router prompt logic lab`; `test ML router prompt logic`; `prompt choosing reliability`; `prompt selection reliability`; `ML router prompt logic reliability`; `continue ML implementation after lab`; `canonize LAB phase`; `canonize lab/test logic`
- **User intent examples:** `Canonize the LAB phase entry before implementing lab tests.`; `After P12, what is the next safe step?`; `Start LAB-0 for the ML router prompt logic test lab.`; `Continue ML logic after the lab fulfills its mission.`
- **Aliases:** `RG-LAB-000`; `routing_signal_scorer_v3_lab_phase_entry_router_canon`; `LAB phase entry canon`; `ML LAB router canon`; `post-P12 LAB canon`; `LAB-0 router canon`
- **When to load:** When KANDA work involves post-P12 LAB/test phase entry, LAB-0, ML router prompt logic reliability testing, lab/test implementation planning, or any request to continue ML implementation after P12.
- **When not to load:** Do not load for ordinary Fast Path explanations, simple non-KANDA ML discussion, or as a substitute for current project files and freeze evidence during implementation.
- **Required companion prompts:** `routing_signal_scorer_v3_pilot_copilot_phase0_router_canon`; `kanda_routing_system_canon`; `kanda_box_shielding_canon`; `prompt_navigation_index`; `GROUP_ASSIMILATION_INDEX`

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

### `prompt_router` — Prompt Router

- **File:** `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md`
- **Priority:** `10`
- **Trigger phrases:** `route prompt`; `prompt router`; `intent router`; `messy request to prompt`; `which stack`
- **User intent examples:** `Route “ok freeze” to the correct governance prompt.`
- **Aliases:** `index`; `navigator`; `prompt router`; `prompt_router`; `prompt_router.md`; `router`
- **When to load:** When multiple prompts may match and the system must select the best route.
- **When not to load:** Do not load when the exact specialist prompt is already explicitly chosen.
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

### `active_governance_freeze_update` — Active Governance Freeze Update

- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/active_governance_freeze_update.md`
- **Priority:** `25`
- **Trigger phrases:** `ok freeze`; `freeze this`; `make official`; `canonize this`; `validated baseline`; `update governance`
- **User intent examples:** `Validation passed; freeze this as official.`
- **Aliases:** `active`; `active governance freeze update`; `active_governance_freeze_update`; `active_governance_freeze_update.md`; `freeze`; `governance`; `handoff`; `update`
- **When to load:** Only after validation evidence confirms a change can become active governance.
- **When not to load:** Do not load before validation or when work is still draft.
- **Required companion prompts:** `evidence_freshness_gate`; `patch_registry_validation_freeze`; `current_workflow_handoff_template`

### `current_workflow_handoff_template` — Current Workflow Handoff Template

- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/current_workflow_handoff_template.md`
- **Priority:** `25`
- **Trigger phrases:** `current workflow handoff`; `handoff current work`; `what next AI should know`; `continue next time`; `active workflow summary`
- **User intent examples:** `Write a handoff for the current implementation state.`
- **Aliases:** `current`; `current workflow handoff template`; `current_workflow_handoff_template`; `current_workflow_handoff_template.md`; `freeze`; `governance`; `handoff`; `workflow`
- **When to load:** When transferring unfinished current workflow to a later session or another AI.
- **When not to load:** Do not load for finalized governance freeze; use freeze prompt instead.
- **Required companion prompts:** `evidence_freshness_gate`; `patch_registry_validation_freeze`

### `end_of_chat_governance_update_template` — End-of-Chat Governance Update Template

- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/end_of_chat_governance_update_template.md`
- **Priority:** `25`
- **Trigger phrases:** `end of chat update`; `session governance update`; `write end summary`; `governance note`; `end of day`
- **User intent examples:** `Create an end-of-chat governance update template.`
- **Aliases:** `chat`; `end-of-chat governance update template`; `end_of_chat_governance_update_template`; `end_of_chat_governance_update_template.md`; `freeze`; `governance`; `handoff`; `update`
- **When to load:** At session close when producing structured governance notes.
- **When not to load:** Do not load for immediate implementation without closing the session.
- **Required companion prompts:** `evidence_freshness_gate`; `patch_registry_validation_freeze`; `current_workflow_handoff_template`

### `professional_engineering_governance_template` — Professional Engineering Governance Template

- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/professional_engineering_governance_template.md`
- **Priority:** `25`
- **Trigger phrases:** `engineering governance template`; `professional governance`; `quality rules template`; `project governance`
- **User intent examples:** `Create a professional engineering governance template for a project.`
- **Aliases:** `engineering`; `freeze`; `governance`; `handoff`; `professional`; `professional engineering governance template`; `professional_engineering_governance_template`; `professional_engineering_governance_template.md`
- **When to load:** When designing reusable engineering governance rules.
- **When not to load:** Do not load for task-level patch implementation.
- **Required companion prompts:** `evidence_freshness_gate`; `patch_registry_validation_freeze`; `current_workflow_handoff_template`

### `reasoner_professional_engineering_governance` — Reasoner Professional Engineering Governance

- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/reasoner_professional_engineering_governance.md`
- **Priority:** `25`
- **Trigger phrases:** `reasoner governance`; `professional reasoner workflow`; `KANDA engineering rules`; `non vibe coding rules`
- **User intent examples:** `Apply the KANDA Reasoner professional engineering governance.`
- **Aliases:** `engineering`; `freeze`; `governance`; `handoff`; `professional`; `reasoner`; `reasoner professional engineering governance`; `reasoner_professional_engineering_governance`; `reasoner_professional_engineering_governance.md`
- **When to load:** When the task touches KANDA Reasoner development methodology or validation gates.
- **When not to load:** Do not load for unrelated general writing tasks.
- **Required companion prompts:** `evidence_freshness_gate`; `patch_registry_validation_freeze`; `current_workflow_handoff_template`

### `workflow_handoff_template` — Workflow Handoff Template

- **File:** `ACTIVE_PROMPTS/03_governance_freeze_and_handoff/workflow_handoff_template.md`
- **Priority:** `25`
- **Trigger phrases:** `create handoff`; `write handoff`; `handoff template`; `next AI instructions`; `transfer context`
- **User intent examples:** `Create a clean handoff so another AI can continue.`
- **Aliases:** `freeze`; `governance`; `handoff`; `workflow`; `workflow handoff template`; `workflow_handoff_template`; `workflow_handoff_template.md`
- **When to load:** When a reusable handoff document is needed.
- **When not to load:** Do not load when only a short chat summary is requested.
- **Required companion prompts:** `evidence_freshness_gate`; `patch_registry_validation_freeze`

## Box Architecture And Boundaries (`04_box_architecture_and_boundaries`)

### `box_architecture_canon` — Box Architecture Canon

- **File:** `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md`
- **Priority:** `5`
- **Trigger phrases:** `active box`; `box logic`; `box architecture`; `box boundary audit`; `box boundary`; `owner paths`; `allowed files`; `forbidden files`; `cross box touch`; `public contract`; `private internals`; `private reach-in`
- **User intent examples:** `Before editing, identify the active box and out-of-scope files.`; `Create a Box Boundary Audit before implementing this feature.`; `Prevent private reach-in and God Box expansion while patching.`; `Add Brain Navigator without contaminating Tab Registry or tab internals.`
- **Aliases:** `architecture`; `boundaries`; `box`; `box architecture canon`; `box boundary audit`; `box logic canon`; `box_architecture_canon`; `box_architecture_canon.md`; `ownership`; `one primary box`; `private reach-in`; `god box`; `leaking registry`; `remember box`
- **When to load:** Before implementation, refactor, prompt update, governance update, bundle creation, GUI ownership change, cross-box communication, or architecture-boundary work.
- **When not to load:** Skip only for pure explanation or text-editing tasks with no implementation consequence.
- **Required companion prompts:** `bundle_gated_development_workflow`; `implementation_roadmap_builder`

### `closed_box_delivery_canon` — Closed-Box Delivery Canon

- **File:** `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/closed_box_delivery_canon.md`
- **Priority:** `5`
- **Trigger phrases:** `closed box delivery`; `ingredient box`; `deliver box`; `box package`; `sealed component`
- **User intent examples:** `Package this as a closed delivery box with clear boundaries.`
- **Aliases:** `boundaries`; `box`; `closed`; `closed-box delivery canon`; `closed_box_delivery_canon`; `closed_box_delivery_canon.md`; `delivery`; `ownership`
- **When to load:** When delivering or importing a component as a bounded unit.
- **When not to load:** Do not load for conceptual discussion without delivery artifact.
- **Required companion prompts:** `bundle_gated_development_workflow`; `implementation_roadmap_builder`

### `project_folder_organization_canon` — Project Folder Organization Canon

- **File:** `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/project_folder_organization_canon.md`
- **Priority:** `5`
- **Trigger phrases:** `organize folder`; `project folder structure`; `where should files go`; `folder canon`; `project layout`
- **User intent examples:** `Organize the project folder before implementation.`
- **Aliases:** `boundaries`; `box`; `folder`; `organization`; `ownership`; `project`; `project folder organization canon`; `project_folder_organization_canon`; `project_folder_organization_canon.md`
- **When to load:** When designing or cleaning project folder structure.
- **When not to load:** Do not load for code logic changes that do not affect layout.
- **Required companion prompts:** `bundle_gated_development_workflow`; `implementation_roadmap_builder`

### `stateful_control_regression_canon` — Stateful Control Regression Canon

- **File:** `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/stateful_control_regression_canon.md`
- **Priority:** `5`
- **Trigger phrases:** `dropdown broke`; `button state`; `stateful control`; `do not regress UI control`; `selection state`
- **User intent examples:** `Changing this UI must not break existing dropdown behavior.`
- **Aliases:** `boundaries`; `box`; `control`; `ownership`; `regression`; `stateful`; `stateful control regression canon`; `stateful_control_regression_canon`; `stateful_control_regression_canon.md`
- **When to load:** When working on GUI controls, state, dropdowns, buttons, or preserved selections.
- **When not to load:** Do not load for non-interactive backend code.
- **Required companion prompts:** `bundle_gated_development_workflow`; `implementation_roadmap_builder`

### `kanda_box_shielding_canon` — KANDA Box Shielding Canon

- **File:** `ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md`
- **Priority:** `4`
- **Trigger phrases:** `box shield`; `box shielding`; `shield logic`; `shielding method`; `KBSC`; `KANDA Box Shielding Canon`; `canonize shielding`; `architectural fitness function`; `bounded context shield`; `do not invade other box logic`; `authority creep`; `forbidden authority escalation`; `truth source priority ladder`; `dependency direction`; `no placeholder commitment`; `shield before stronger ML`; `routing signal scorer shield`; `similarity box shield`
- **User intent examples:** `Create the shield before continuing to stronger ML.`; `Canonize the shielding method and insert it into the routing system.`; `Audit this box for authority creep and no-invasion behavior before the next patch.`
- **Aliases:** `KBSC`; `box shield`; `box shielding canon`; `kanda box shielding canon`; `kanda_box_shielding_canon`; `kanda_box_shielding_canon.md`; `architectural fitness function`; `bounded context shield`; `shield before stronger ML`
- **When to load:** When a meaningful box milestone must be protected before stronger/cross-box work, when shielding logic is being created or updated, or when advisory output risks becoming authority.
- **When not to load:** Do not load for simple Fast Path explanations, small rewrites, or implementation tasks with no boundary, authority, or regression-shield risk.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`

## Patch Delivery And Validation (`05_patch_delivery_and_validation`)

### `bundle_gated_development_workflow` — Bundle-Gated Development Workflow

- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/bundle_gated_development_workflow.md`
- **Priority:** `15`
- **Trigger phrases:** `bundle gated`; `one patch one problem`; `safe patch`; `installable bundle`; `AI patch workflow`
- **User intent examples:** `Create a small patch bundle, not a broad file replacement.`
- **Aliases:** `bundle`; `bundle-gated development workflow`; `bundle_gated_development_workflow`; `bundle_gated_development_workflow.md`; `development`; `gated`; `patch`; `validation`; `workflow`
- **When to load:** Before creating any source-changing or prompt-changing patch bundle.
- **When not to load:** Do not load for read-only audits unless a patch will follow.
- **Required companion prompts:** `box_architecture_canon`; `evidence_freshness_gate`

### `evidence_freshness_gate` — Evidence Freshness Gate

- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/evidence_freshness_gate.md`
- **Priority:** `15`
- **Trigger phrases:** `stale evidence`; `fresh evidence`; `source hash mismatch`; `regenerate evidence`; `validation artifact`
- **User intent examples:** `The validation failed because generated evidence is stale.`
- **Aliases:** `bundle`; `evidence`; `evidence freshness gate`; `evidence_freshness_gate`; `evidence_freshness_gate.md`; `freshness`; `gate`; `patch`; `validation`
- **When to load:** When generated evidence, manifests, timestamps, or source hashes may be stale.
- **When not to load:** Do not load for tasks with no generated evidence or validation artifacts.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`

### `implementation_and_delivery_protocol` — Implementation and Delivery Protocol

- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md`
- **Priority:** `15`
- **Trigger phrases:** `implement and send`; `code and deliver`; `patch with install code`; `implementation protocol`; `send code to user`
- **User intent examples:** `Implement this as a ZIP and include safe install instructions.`
- **Aliases:** `bundle`; `delivery`; `implementation`; `implementation and delivery protocol`; `implementation_and_delivery_protocol`; `implementation_and_delivery_protocol.md`; `patch`; `validation`
- **When to load:** When the AI must implement a change and deliver it safely.
- **When not to load:** Do not load for analysis-only requests.
- **Required companion prompts:** `box_architecture_canon`; `evidence_freshness_gate`; `bundle_gated_development_workflow`

### `implementation_roadmap_builder` — Implementation Roadmap Builder

- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_roadmap_builder.md`
- **Priority:** `15`
- **Trigger phrases:** `roadmap implementation`; `implementation plan`; `before coding plan`; `task roadmap`; `plan patch`
- **User intent examples:** `Build a roadmap before writing code.`
- **Aliases:** `builder`; `bundle`; `implementation`; `implementation roadmap builder`; `implementation_roadmap_builder`; `implementation_roadmap_builder.md`; `patch`; `validation`
- **When to load:** Before non-trivial implementation to define tasks, boxes, files, validation, and risks.
- **When not to load:** Do not load for trivial edits under ten lines.
- **Required companion prompts:** `box_architecture_canon`; `evidence_freshness_gate`; `bundle_gated_development_workflow`

### `patch_registry_validation_freeze` — Patch Registry Validation and Freeze

- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_registry_validation_freeze.md`
- **Priority:** `15`
- **Trigger phrases:** `patch registry`; `patch status`; `freeze patch`; `validated patch`; `track patch`
- **User intent examples:** `Register this patch and decide if it can be frozen.`
- **Aliases:** `bundle`; `freeze`; `patch`; `patch registry validation and freeze`; `patch_registry_validation_freeze`; `patch_registry_validation_freeze.md`; `registry`; `validation`
- **When to load:** When tracking patch lifecycle from draft to installed/validated/frozen.
- **When not to load:** Do not load when no patch or versioned change exists.
- **Required companion prompts:** `box_architecture_canon`; `evidence_freshness_gate`; `bundle_gated_development_workflow`; `current_workflow_handoff_template`

### `universal_delivery_protocol` — Universal Delivery Protocol

- **File:** `ACTIVE_PROMPTS/05_patch_delivery_and_validation/universal_delivery_protocol.md`
- **Priority:** `15`
- **Trigger phrases:** `deliver zip`; `send implementation`; `package output`; `final delivery`; `artifact delivery`
- **User intent examples:** `Package the change in a safe installable ZIP.`
- **Aliases:** `bundle`; `delivery`; `patch`; `universal`; `universal delivery protocol`; `universal_delivery_protocol`; `universal_delivery_protocol.md`; `validation`
- **When to load:** When producing deliverables, ZIPs, install scripts, reports, or patches.
- **When not to load:** Do not load for brainstorming without deliverables.
- **Required companion prompts:** `box_architecture_canon`; `evidence_freshness_gate`; `bundle_gated_development_workflow`

## Refactor And Architecture Hardening (`06_refactor_and_architecture_hardening`)

### `architecture_hardening_triage_protocol` — Architecture Hardening Triage Protocol

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/architecture_hardening_triage_protocol.md`
- **Priority:** `30`
- **Trigger phrases:** `architecture hardening`; `triage architecture`; `architecture problem`; `hardening protocol`; `structural risk`
- **User intent examples:** `Audit architecture before deciding the repair path.`
- **Aliases:** `architecture`; `architecture hardening triage protocol`; `architecture_hardening_triage_protocol`; `architecture_hardening_triage_protocol.md`; `hardening`; `refactor`; `triage`
- **When to load:** When structural/architectural problems are suspected.
- **When not to load:** Do not load for isolated bug fixes with no architecture implications.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

### `architecture_hardening_triage_template` — Architecture Hardening Triage Template

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/architecture_hardening_triage_template.md`
- **Priority:** `30`
- **Trigger phrases:** `architecture triage template`; `hardening checklist`; `architecture audit template`
- **User intent examples:** `Create a reusable checklist for architecture hardening.`
- **Aliases:** `architecture`; `architecture hardening triage template`; `architecture_hardening_triage_template`; `architecture_hardening_triage_template.md`; `hardening`; `refactor`; `triage`
- **When to load:** When a reusable triage document/template is needed.
- **When not to load:** Do not load as the main protocol when actual hardening work is underway.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

### `large_module_refactor_protocol` — Large Module Refactor Protocol

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md`
- **Priority:** `30`
- **Trigger phrases:** `module too big`; `file too large`; `split module`; `refactor large file`; `reduce module size`
- **User intent examples:** `This file is too big; split it safely without breaking API.`
- **Aliases:** `architecture`; `hardening`; `large`; `large module refactor protocol`; `large_module_refactor_protocol`; `large_module_refactor_protocol.md`; `module`; `refactor`
- **When to load:** When a module/file is too large or has mixed responsibilities.
- **When not to load:** Do not load for small local edits.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

### `large_module_refactor_template` — Large Module Refactor Template

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_template.md`
- **Priority:** `30`
- **Trigger phrases:** `large module template`; `refactor template`; `split file template`
- **User intent examples:** `Create a template for large-module refactor tasks.`
- **Aliases:** `architecture`; `hardening`; `large`; `large module refactor template`; `large_module_refactor_template`; `large_module_refactor_template.md`; `module`; `refactor`
- **When to load:** When documenting or scaffolding a repeated large-module refactor workflow.
- **When not to load:** Do not load instead of the protocol for actual refactor.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

### `problem_set_roadmap_solver` — Problem-Set Roadmap Solver

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/problem_set_roadmap_solver.md`
- **Priority:** `30`
- **Trigger phrases:** `problem set roadmap`; `many problems`; `solve roadmap`; `batch issues`; `prioritize problems`
- **User intent examples:** `Turn these issues into a sequenced roadmap.`
- **Aliases:** `architecture`; `hardening`; `problem`; `problem-set roadmap solver`; `problem_set_roadmap_solver`; `problem_set_roadmap_solver.md`; `refactor`; `solver`
- **When to load:** When many problems must be grouped, prioritized, and sequenced.
- **When not to load:** Do not load for a single well-defined bug.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

### `refactor_fragmentation_audit_runner` — Refactor Fragmentation Audit Runner

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/refactor_fragmentation_audit_runner.md`
- **Priority:** `30`
- **Trigger phrases:** `fragmentation audit`; `too fragmented`; `refactor runner`; `fragmented modules`; `audit split`
- **User intent examples:** `Check whether previous refactors created fragmentation.`
- **Aliases:** `architecture`; `audit`; `fragmentation`; `hardening`; `refactor`; `refactor fragmentation audit runner`; `refactor_fragmentation_audit_runner`; `refactor_fragmentation_audit_runner.md`; `runner`
- **When to load:** When module splitting/refactoring may have produced too many fragments or unclear ownership.
- **When not to load:** Do not load before any fragmentation exists.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

### `tab1_tab2_audit_taxonomy` — Tab 1 and Tab 2 Audit Taxonomy

- **File:** `ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/tab1_tab2_audit_taxonomy.md`
- **Priority:** `30`
- **Trigger phrases:** `tab1 tab2 errors`; `architecture tab errors`; `workflow validation errors`; `audit taxonomy`; `tab validation`
- **User intent examples:** `Classify Tab 1 and Tab 2 failures into a roadmap.`
- **Aliases:** `architecture`; `audit`; `hardening`; `refactor`; `tab 1 and tab 2 audit taxonomy`; `tab1`; `tab1_tab2_audit_taxonomy`; `tab1_tab2_audit_taxonomy.md`; `tab2`; `taxonomy`
- **When to load:** When interpreting KANDA Reasoner Tab 1/Tab 2 audit/validation output.
- **When not to load:** Do not load for unrelated Python test failures.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_refactoring`

## Prompt Authoring And Audit (`07_prompt_authoring_and_audit`)

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

### `peopleware_team_boundary` — Peopleware Team Boundary

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/peopleware_team_boundary.md`
- **Priority:** `50`
- **Trigger phrases:** `team workflow`; `peopleware`; `handoff between humans`; `communication risk`; `developer coordination`
- **User intent examples:** `Improve human workflow and reduce coordination risk.`
- **Aliases:** `boundary`; `peopleware`; `peopleware team boundary`; `peopleware_team_boundary`; `peopleware_team_boundary.md`; `python engineering`; `software design`; `team`
- **When to load:** When the issue is team/process/communication rather than code mechanics.
- **When not to load:** Do not load for solo coding implementation details.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `practical_field_handbook_template` — Practical Field Handbook Template

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/practical_field_handbook_template.md`
- **Priority:** `50`
- **Trigger phrases:** `field handbook`; `practical guide`; `operator handbook`; `how to use system`; `runbook style guide`
- **User intent examples:** `Create a practical field handbook for using this tool.`
- **Aliases:** `field`; `handbook`; `practical`; `practical field handbook template`; `practical_field_handbook_template`; `practical_field_handbook_template.md`; `python engineering`; `software design`
- **When to load:** When producing user/operator guidance rather than source code.
- **When not to load:** Do not load for implementation internals only.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_clean_architecture` — Python Clean Architecture

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_clean_architecture.md`
- **Priority:** `50`
- **Trigger phrases:** `clean architecture`; `dependency rule`; `entities use cases adapters`; `architecture layers`; `decouple python`
- **User intent examples:** `Apply Clean Architecture to this Python app.`
- **Aliases:** `architecture`; `clean`; `python clean architecture`; `python engineering`; `python_clean_architecture`; `python_clean_architecture.md`; `software design`
- **When to load:** When Python architecture/layering/dependency direction is central.
- **When not to load:** Do not load for styling-only edits.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_clean_code` — Python Clean Code

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_clean_code.md`
- **Priority:** `50`
- **Trigger phrases:** `clean code`; `readable code`; `function naming`; `small functions`; `code clarity`
- **User intent examples:** `Make this Python module cleaner and easier to read.`
- **Aliases:** `clean`; `code`; `python clean code`; `python engineering`; `python_clean_code`; `python_clean_code.md`; `software design`
- **When to load:** When code readability, naming, functions, and maintainability are central.
- **When not to load:** Do not load for performance-only optimization unless readability is also at stake.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_design_patterns` — Python Design Patterns

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_design_patterns.md`
- **Priority:** `50`
- **Trigger phrases:** `design pattern`; `factory pattern`; `strategy pattern`; `observer`; `adapter pattern`
- **User intent examples:** `Which design pattern fits this Python problem?`
- **Aliases:** `design`; `patterns`; `python design patterns`; `python engineering`; `python_design_patterns`; `python_design_patterns.md`; `software design`
- **When to load:** When selecting or implementing reusable object/behavior patterns.
- **When not to load:** Do not load for simple procedural code.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_domain_driven_design` — Python Domain-Driven Design

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_domain_driven_design.md`
- **Priority:** `50`
- **Trigger phrases:** `domain driven design`; `DDD`; `bounded context`; `domain model`; `ubiquitous language`
- **User intent examples:** `Model this app around domain concepts and bounded contexts.`
- **Aliases:** `design`; `domain`; `driven`; `python domain-driven design`; `python engineering`; `python_domain_driven_design`; `python_domain_driven_design.md`; `software design`
- **When to load:** When domain concepts, boundaries, and business rules drive architecture.
- **When not to load:** Do not load for low-level utility scripts.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_enterprise_architecture` — Python Enterprise Architecture

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_enterprise_architecture.md`
- **Priority:** `50`
- **Trigger phrases:** `enterprise architecture`; `repository pattern`; `unit of work`; `service layer`; `application architecture`
- **User intent examples:** `Use enterprise application patterns for this Python app.`
- **Aliases:** `architecture`; `enterprise`; `python engineering`; `python enterprise architecture`; `python_enterprise_architecture`; `python_enterprise_architecture.md`; `software design`
- **When to load:** When application layers, transactions, repositories, services, or enterprise patterns matter.
- **When not to load:** Do not load for one-off small scripts.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_high_performance` — Python High Performance

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_high_performance.md`
- **Priority:** `50`
- **Trigger phrases:** `performance`; `optimize python`; `slow code`; `memory usage`; `profiling`
- **User intent examples:** `This Python code is slow; optimize without breaking behavior.`
- **Aliases:** `high`; `performance`; `python engineering`; `python high performance`; `python_high_performance`; `python_high_performance.md`; `software design`
- **When to load:** When runtime, memory, profiling, vectorization, or throughput is central.
- **When not to load:** Do not load if performance is irrelevant.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_legacy_code_workflow` — Python Legacy Code Workflow

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_legacy_code_workflow.md`
- **Priority:** `50`
- **Trigger phrases:** `legacy code`; `working effectively with legacy code`; `safe change legacy`; `characterization tests`; `hard to change`
- **User intent examples:** `Change legacy code safely without breaking behavior.`
- **Aliases:** `code`; `legacy`; `python engineering`; `python legacy code workflow`; `python_legacy_code_workflow`; `python_legacy_code_workflow.md`; `software design`; `workflow`
- **When to load:** When existing code is risky, poorly tested, or hard to understand.
- **When not to load:** Do not load for greenfield modules.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_pragmatic_programmer` — Python Pragmatic Programmer

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_pragmatic_programmer.md`
- **Priority:** `50`
- **Trigger phrases:** `pragmatic programmer`; `DRY`; `orthogonality`; `tracer bullets`; `pragmatic code`
- **User intent examples:** `Apply pragmatic programming principles to this project.`
- **Aliases:** `pragmatic`; `programmer`; `python engineering`; `python pragmatic programmer`; `python_pragmatic_programmer`; `python_pragmatic_programmer.md`; `software design`
- **When to load:** When broad engineering judgement, maintainability, and practical tradeoffs are needed.
- **When not to load:** Do not load as the only prompt for specialized security/performance issues.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_refactoring` — Python Refactoring

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/python_refactoring.md`
- **Priority:** `50`
- **Trigger phrases:** `refactor python`; `extract function`; `move method`; `code smell`; `safe refactoring`
- **User intent examples:** `Refactor this Python file while preserving behavior.`
- **Aliases:** `python engineering`; `python refactoring`; `python_refactoring`; `python_refactoring.md`; `refactoring`; `software design`
- **When to load:** When changing structure without intended behavior changes.
- **When not to load:** Do not load for feature additions where behavior must change significantly.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `software_engineering_books_master` — Software Engineering Books Master

- **File:** `ACTIVE_PROMPTS/08_python_engineering_core/software_engineering_books_master.md`
- **Priority:** `50`
- **Trigger phrases:** `which engineering book prompt`; `books master`; `combine software books`; `engineering principles overview`
- **User intent examples:** `Use the combined software-engineering book principles.`
- **Aliases:** `books`; `engineering`; `master`; `python engineering`; `software`; `software design`; `software engineering books master`; `software_engineering_books_master`; `software_engineering_books_master.md`
- **When to load:** When broad multi-source engineering guidance is needed.
- **When not to load:** Do not load when a more specific engineering prompt is enough.
- **Required companion prompts:** `box_architecture_canon`; `implementation_roadmap_builder`; `python_testing_pytest`; `implementation_and_delivery_protocol`

## Python Quality Security Observability (`09_python_quality_security_observability`)

### `python_documentation_developer_experience` — Python Documentation and Developer Experience

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_documentation_developer_experience.md`
- **Priority:** `45`
- **Trigger phrases:** `developer experience`; `onboarding docs`; `API docs`; `documentation`; `README quality`
- **User intent examples:** `Create better developer docs and onboarding.`
- **Aliases:** `developer`; `documentation`; `experience`; `observability`; `python documentation and developer experience`; `python_documentation_developer_experience`; `python_documentation_developer_experience.md`; `quality`; `security`
- **When to load:** When docs, onboarding, help files, or developer usability are central.
- **When not to load:** Do not load for runtime bug fixes.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_observability_logging_metrics_tracing` — Python Observability Logging Metrics and Tracing

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_observability_logging_metrics_tracing.md`
- **Priority:** `45`
- **Trigger phrases:** `logging`; `metrics`; `tracing`; `observability`; `debug logs`
- **User intent examples:** `Add structured logging and useful diagnostics.`
- **Aliases:** `logging`; `metrics`; `observability`; `python observability logging metrics and tracing`; `python_observability_logging_metrics_tracing`; `python_observability_logging_metrics_tracing.md`; `quality`; `security`; `tracing`
- **When to load:** When instrumentation, logs, metrics, traces, or diagnosis are central.
- **When not to load:** Do not load for UI layout-only tasks.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_resilience_error_handling` — Python Resilience and Error Handling

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_resilience_error_handling.md`
- **Priority:** `45`
- **Trigger phrases:** `error handling`; `retries`; `circuit breaker`; `resilience`; `failure recovery`
- **User intent examples:** `Make this workflow robust against transient failures.`
- **Aliases:** `error`; `handling`; `observability`; `python resilience and error handling`; `python_resilience_error_handling`; `python_resilience_error_handling.md`; `quality`; `resilience`; `security`
- **When to load:** When exception handling, retries, fallback, or resilience is central.
- **When not to load:** Do not load for purely cosmetic changes.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_security_threat_prevention` — Python Security and Threat Prevention

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_security_threat_prevention.md`
- **Priority:** `45`
- **Trigger phrases:** `security`; `threat prevention`; `secret handling`; `input sanitization`; `secure python`
- **User intent examples:** `Review this Python code for security risks.`
- **Aliases:** `observability`; `prevention`; `python security and threat prevention`; `python_security_threat_prevention`; `python_security_threat_prevention.md`; `quality`; `security`; `threat`
- **When to load:** When security, trust boundaries, secrets, validation, or malicious input matter.
- **When not to load:** Do not load for local-only toy code with no security surface, unless requested.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `python_testing_pytest` — Python Testing with Pytest

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_testing_pytest.md`
- **Priority:** `45`
- **Trigger phrases:** `pytest`; `unit tests`; `test coverage`; `write tests`; `regression test`
- **User intent examples:** `Add pytest tests for this patch.`
- **Aliases:** `observability`; `pytest`; `python testing with pytest`; `python_testing_pytest`; `python_testing_pytest.md`; `quality`; `security`; `testing`
- **When to load:** When creating or updating tests, regression tests, fixtures, or test strategy.
- **When not to load:** Do not load if no code/testing is involved.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `implementation_and_delivery_protocol`

### `python_validation_serialisation_type_safety` — Python Validation, Serialisation, and Type Safety

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/python_validation_serialisation_type_safety.md`
- **Priority:** `45`
- **Trigger phrases:** `pydantic`; `type safety`; `data validation`; `serialization`; `schema validation`
- **User intent examples:** `Validate inputs and outputs with type-safe schemas.`
- **Aliases:** `observability`; `python validation, serialisation, and type safety`; `python_validation_serialisation_type_safety`; `python_validation_serialisation_type_safety.md`; `quality`; `safety`; `security`; `serialisation`; `type`; `validation`
- **When to load:** When data models, schemas, serialization, or type validation are central.
- **When not to load:** Do not load for UI-only text changes.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_testing_pytest`; `implementation_and_delivery_protocol`

### `tab4_docstring_quality_roadmap` — Tab 4 Docstring Quality Roadmap

- **File:** `ACTIVE_PROMPTS/09_python_quality_security_observability/tab4_docstring_quality_roadmap.md`
- **Priority:** `45`
- **Trigger phrases:** `docstring quality`; `tab4 docstrings`; `missing docstrings`; `docstring roadmap`; `documentation strings`
- **User intent examples:** `Improve the missing-docstring handler quality.`
- **Aliases:** `docstring`; `observability`; `quality`; `security`; `tab 4 docstring quality roadmap`; `tab4`; `tab4_docstring_quality_roadmap`; `tab4_docstring_quality_roadmap.md`
- **When to load:** When Tab 4/docstring generation or documentation quality is central.
- **When not to load:** Do not load for user manual documentation unrelated to code docstrings.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`; `python_testing_pytest`; `implementation_and_delivery_protocol`

## Python Api Data Async Config (`10_python_api_data_async_config`)

### `python_api_design` — Python API Design

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_api_design.md`
- **Priority:** `50`
- **Trigger phrases:** `REST API`; `GraphQL`; `API design`; `endpoint design`; `interface contract`
- **User intent examples:** `Design a clean API boundary for this Python service.`
- **Aliases:** `api`; `async`; `config`; `data`; `design`; `python api design`; `python_api_design`; `python_api_design.md`
- **When to load:** When external/internal API contracts, endpoints, or service interfaces are central.
- **When not to load:** Do not load for non-API GUI-only changes.
- **Required companion prompts:** `box_architecture_canon`; `python_testing_pytest`; `python_validation_serialisation_type_safety`; `implementation_and_delivery_protocol`

### `python_async_parallel_distributed` — Python Async, Parallel, and Distributed Computing

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_async_parallel_distributed.md`
- **Priority:** `50`
- **Trigger phrases:** `async`; `parallel`; `distributed`; `concurrency`; `background task`
- **User intent examples:** `Make this workflow async-safe and concurrency-aware.`
- **Aliases:** `api`; `async`; `config`; `data`; `distributed`; `parallel`; `python async, parallel, and distributed computing`; `python_async_parallel_distributed`; `python_async_parallel_distributed.md`
- **When to load:** When concurrency, async, parallelism, queues, or distributed work are central.
- **When not to load:** Do not load for simple synchronous scripts.
- **Required companion prompts:** `box_architecture_canon`; `python_testing_pytest`; `python_validation_serialisation_type_safety`; `implementation_and_delivery_protocol`

### `python_configuration_feature_flags` — Python Configuration and Feature Flags

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_configuration_feature_flags.md`
- **Priority:** `50`
- **Trigger phrases:** `configuration`; `feature flags`; `settings`; `environment variables`; `config management`
- **User intent examples:** `Move hard-coded settings into configuration safely.`
- **Aliases:** `api`; `async`; `config`; `configuration`; `data`; `feature`; `flags`; `python configuration and feature flags`; `python_configuration_feature_flags`; `python_configuration_feature_flags.md`
- **When to load:** When config, feature flags, environment-specific behavior, or settings are central.
- **When not to load:** Do not load for logic-only changes.
- **Required companion prompts:** `box_architecture_canon`; `python_testing_pytest`; `python_validation_serialisation_type_safety`; `implementation_and_delivery_protocol`

### `python_database_design_optimisation` — Python Database Design and Optimisation

- **File:** `ACTIVE_PROMPTS/10_python_api_data_async_config/python_database_design_optimisation.md`
- **Priority:** `50`
- **Trigger phrases:** `database design`; `SQL optimization`; `schema design`; `query performance`; `migrations`
- **User intent examples:** `Improve database schema/query design.`
- **Aliases:** `api`; `async`; `config`; `data`; `database`; `design`; `optimisation`; `python database design and optimisation`; `python_database_design_optimisation`; `python_database_design_optimisation.md`
- **When to load:** When database schema, queries, migrations, persistence, or data access are central.
- **When not to load:** Do not load when no database or persistence is involved.
- **Required companion prompts:** `box_architecture_canon`; `python_testing_pytest`; `python_validation_serialisation_type_safety`; `implementation_and_delivery_protocol`

## Productization And Release Readiness (`11_productization_and_release_readiness`)

### `kubernetes_deployment_operations` — Kubernetes Deployment and Operations

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/kubernetes_deployment_operations.md`
- **Priority:** `55`
- **Trigger phrases:** `kubernetes`; `deploy to k8s`; `containers operations`; `cluster deployment`; `helm`
- **User intent examples:** `Think about deployment/operations for this Python app.`
- **Aliases:** `deployment`; `kubernetes`; `kubernetes deployment and operations`; `kubernetes_deployment_operations`; `kubernetes_deployment_operations.md`; `operations`; `product`; `release`
- **When to load:** When Kubernetes/container operations are relevant.
- **When not to load:** Do not load for local desktop-only workflows unless deployment is planned.
- **Required companion prompts:** `professional_ai_assisted_engineering_framework`; `evidence_freshness_gate`

### `productization_readiness_roadmap` — Productization Readiness Roadmap

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/productization_readiness_roadmap.md`
- **Priority:** `55`
- **Trigger phrases:** `productization`; `release readiness`; `make production ready`; `ship this app`; `professionalize app`
- **User intent examples:** `What must be done before this app is product-ready?`
- **Aliases:** `operations`; `product`; `productization`; `productization readiness roadmap`; `productization_readiness_roadmap`; `productization_readiness_roadmap.md`; `readiness`; `release`
- **When to load:** When assessing readiness for use, release, maintenance, or distribution.
- **When not to load:** Do not load for early exploratory prototypes unless productization is requested.
- **Required companion prompts:** `professional_ai_assisted_engineering_framework`; `evidence_freshness_gate`

### `professional_ai_assisted_engineering_framework` — Professional AI-Assisted Engineering Framework

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/professional_ai_assisted_engineering_framework.md`
- **Priority:** `55`
- **Trigger phrases:** `professional AI engineering`; `AI assisted engineering`; `avoid vibe coding`; `human lead AI assistant`; `professional workflow`
- **User intent examples:** `Define professional AI-assisted engineering rules for this project.`
- **Aliases:** `assisted`; `engineering`; `framework`; `operations`; `product`; `professional`; `professional ai-assisted engineering framework`; `professional_ai_assisted_engineering_framework`; `professional_ai_assisted_engineering_framework.md`; `release`
- **When to load:** When establishing or auditing the overall AI-human engineering method.
- **When not to load:** Do not load for small isolated code snippets.
- **Required companion prompts:** `evidence_freshness_gate`

### `professional_infrastructure_roadmap` — Professional Infrastructure Roadmap

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/professional_infrastructure_roadmap.md`
- **Priority:** `55`
- **Trigger phrases:** `missing professional infrastructure`; `infrastructure roadmap`; `what is missing to be professional`; `validation infrastructure`
- **User intent examples:** `List what infrastructure is missing to make the project professional.`
- **Aliases:** `infrastructure`; `operations`; `product`; `professional`; `professional infrastructure roadmap`; `professional_infrastructure_roadmap`; `professional_infrastructure_roadmap.md`; `release`
- **When to load:** When identifying missing gates, registries, validators, or operational support.
- **When not to load:** Do not load for one-off code formatting.
- **Required companion prompts:** `professional_ai_assisted_engineering_framework`; `evidence_freshness_gate`

### `python_lifecycle_versioning_deprecation` — Python Lifecycle, Versioning, and Deprecation

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/python_lifecycle_versioning_deprecation.md`
- **Priority:** `55`
- **Trigger phrases:** `versioning`; `deprecation`; `release lifecycle`; `legacy support`; `migration path`
- **User intent examples:** `Plan versioning and deprecation for this module.`
- **Aliases:** `deprecation`; `lifecycle`; `operations`; `product`; `python lifecycle, versioning, and deprecation`; `python_lifecycle_versioning_deprecation`; `python_lifecycle_versioning_deprecation.md`; `release`; `versioning`
- **When to load:** When lifecycle, backward compatibility, deprecation, or migrations are central.
- **When not to load:** Do not load for brand-new throwaway code.
- **Required companion prompts:** `professional_ai_assisted_engineering_framework`; `evidence_freshness_gate`

### `python_site_reliability_engineering` — Python Site Reliability Engineering

- **File:** `ACTIVE_PROMPTS/11_productization_and_release_readiness/python_site_reliability_engineering.md`
- **Priority:** `55`
- **Trigger phrases:** `SRE`; `reliability`; `SLI`; `SLO`; `incident response`; `operational readiness`
- **User intent examples:** `Apply SRE thinking to the app's reliability.`
- **Aliases:** `engineering`; `operations`; `product`; `python site reliability engineering`; `python_site_reliability_engineering`; `python_site_reliability_engineering.md`; `release`; `reliability`; `site`
- **When to load:** When reliability, operations, monitoring, service levels, or incident handling matter.
- **When not to load:** Do not load for non-operational prompt-only edits.
- **Required companion prompts:** `professional_ai_assisted_engineering_framework`; `evidence_freshness_gate`

## Generalized Project Canons (`12_generalized_project_canons`)

### `project_tool_boundary_canon` - Project Tool Boundary Canon

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md`
- **Prompt code:** `KPR-12-001`
- **Priority:** `35`
- **Trigger phrases:** `project versus tool`; `project vs tool`; `tool identity`; `active project identity`; `project in use`; `selected project root`; `active project root`; `target project`; `my_project`; `PROJECT_ROOT`; `do not hardcode kanda_reasoner`; `freeze paths active project`; `handoff path active project`; `patch staging active project`
- **User intent examples:** `Keep KANDA Reasoner separate from the active project in every coding task.`; `Make sure freeze paths use the project in use, not always kanda_reasoner.`; `Canonize the distinction between the tool and <my_project>.`
- **Aliases:** `project tool boundary`; `project_tool_boundary_canon`; `tool target boundary`; `active project boundary`; `selected project boundary`
- **When to load:** When coding, patching, validating, freezing, staging, handoff generation, or routing could confuse KANDA Reasoner as the tool with the selected active project as the target.
- **When not to load:** Do not load for simple explanation-only tasks or non-code drafting when no project-root, freeze, patch, handoff, or routing consequence exists.
- **Required companion prompts:** `box_architecture_canon`; `bundle_gated_development_workflow`

### `data_transform_pipeline_invariants` — Data Transform Pipeline Invariants

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/data_transform_pipeline_invariants.md`
- **Priority:** `40`
- **Trigger phrases:** `data transform pipeline`; `source to derived`; `pipeline invariants`; `derived artifact`; `canonical working base`
- **User intent examples:** `Preserve source-to-derived pipeline invariants.`
- **Aliases:** `architecture pattern`; `data`; `data transform pipeline invariants`; `data_transform_pipeline_invariants`; `data_transform_pipeline_invariants.md`; `generalized canon`; `invariants`; `pipeline`; `transform`
- **When to load:** When source data is transformed into derived artifacts and consistency must be protected.
- **When not to load:** Do not load for static documents without transforms.
- **Required companion prompts:** `box_architecture_canon`; `project_specific_prompt_generalization`

### `desktop_help_document_layout_canon` - Desktop Help Document Layout Canon

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/desktop_help_document_layout_canon.md`
- **Priority:** `40`
- **Trigger phrases:** `opener image below blue header`; `no-overflow help layout`; `help page width limit`; `code chain overflows help`; `table larger than page`; `cartoon larger than page`; `help image outside page`; `help text outside page`; `help content outside page`; `help table too wide`; `help table overflow`; `help page overflow`; `cartoon above how to use this`; `full width opener cartoon`; `full-width help cartoon`; `image note should not render`; `no visible image note`; `hide image note`; `hidden image metadata`; `desktop help layout`; `help document layout`; `book-style help`; `help file artwork`; `daily-life cartoon help`; `hand-made help illustration`; `hand-drawn help artwork`; `beautiful help artwork`; `raster help artwork`; `help artwork quality gate`; `box-shielded help docs`; `help optimization pass`; `technical-layer research`; `plain-English completeness`; `source rendered parity`; `stable help header`; `tab-name help header`; `no tab numbers in help`; `scalable help cartoons`; `QWebEngineView help`; `offline help HTML`; `help quick start`; `practical help quick start`; `how to use this help`; `non-technical help explanation`; `artifact explanation help`; `book-grounded help`; `scholarly help references`; `five-book grounding`; `book grounding map`; `full help rebuild`; `summary-linked cartoon`; `common user help`; `five book help grounding`; `five books per feature`; `totally new help file`; `summary linked cartoon`; `summary-linked help artwork`
- **User intent examples:** `Place the funny help cartoon full-width below the blue title section and above How To Use This.`; `Fix a desktop help page where a route chain, control table, or issue-family table extends outside the page.`; `Remove visible Opener Image Note text from the desktop help page.`; `Create a desktop help file with book-style layout and local characterful artwork.`; `Update help artwork so simple SVG sketches cannot pass as beautiful hand-made illustration.`; `Optimize an existing help page without rewriting accurate sections.`; `Make a large help file with enough cartoons for all major themes.`; `Update a desktop help page so the header uses only the stable tab name, not Tab 1 or Tab 2.`; `Add a short How To Use This block below the title and opener image before the dense help sections.`; `Update a desktop help page so a non-technical user understands each artifact before the technical details.`; `Use optional book grounding for a major help-document subject without replacing official docs or local code truth.`; `Create a totally new desktop help file with five verified books for each major feature area.`; `Replace the opener with a funny hand-made cartoon tied to the page summary metaphor.`; `Rebuild this help page from scratch instead of making a narrow optimization pass.`
- **Aliases:** `opener below blue header`; `full-width opener image`; `source-only image note`; `hidden help image metadata`; `help page width`; `help table fit`; `wide help table`; `no overflow help`; `desktop help`; `desktop help document layout canon`; `desktop_help_document_layout_canon`; `desktop_help_document_layout_canon.md`; `help artwork`; `help layout`; `offline help`; `QWebEngineView`; `help artwork quality gate`; `hand-made help art`; `help optimization`; `source rendered parity`; `technical help research`; `scalable help illustrations`; `stable help header`; `tab-name help header`; `no tab numbers in help`; `help quick start`; `practical quick-start block`; `how to use this`; `non technical help`; `common user help`; `artifact explanation help`; `book grounded help`; `scholarly help references`
- **When to load:** When creating or updating local desktop help documents, optimizing existing help source/rendered output, offline help HTML/CSS, stable tab-name help headers, practical quick-start blocks for common users, non-technical artifact explanations, help artwork, book-style help layout, page-boundary/no-overflow help layout, route-chain wrapping, dense table fitting or splitting, local-code-grounded dual-audience explanations, optional or mandatory five-book grounding, book grounding maps, summary-linked opener cartoons, scalable help illustration planning, or box-shielded help-art quality gates, hidden/source-only artwork metadata, no visible image-note sections, full-width opener cartoons below the blue title/summary section and above How To Use This.
- **When not to load:** Do not load for ordinary runtime UI rendering when no help/documentation asset is being created.
- **Required companion prompts:** `box_architecture_canon`; `kanda_box_shielding_canon`; `project_specific_prompt_generalization`; `shared_visual_render_engine_canon`

### `domain_decision_table_template` — Domain Decision Table Template

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/domain_decision_table_template.md`
- **Priority:** `40`
- **Trigger phrases:** `decision table`; `domain rules table`; `rule matrix`; `classification table`; `if then domain rules`
- **User intent examples:** `Use a decision table for these domain rules.`
- **Aliases:** `architecture pattern`; `decision`; `domain`; `domain decision table template`; `domain_decision_table_template`; `domain_decision_table_template.md`; `generalized canon`; `table`
- **When to load:** When complex domain choices should be made explicit as a table/matrix.
- **When not to load:** Do not load for simple linear instructions.
- **Required companion prompts:** `box_architecture_canon`; `project_specific_prompt_generalization`

### `plugin_package_import_canon` — Plugin Package Import Canon

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/plugin_package_import_canon.md`
- **Priority:** `40`
- **Trigger phrases:** `plugin package`; `import plugin`; `plugin manifest`; `package import`; `extension package`
- **User intent examples:** `Import this as a plugin package with manifest and payload.`
- **Aliases:** `architecture pattern`; `generalized canon`; `import`; `package`; `plugin`; `plugin package import canon`; `plugin_package_import_canon`; `plugin_package_import_canon.md`
- **When to load:** When adding/importing plugin-like packages or extension bundles.
- **When not to load:** Do not load for ordinary direct source edits.
- **Required companion prompts:** `box_architecture_canon`; `project_specific_prompt_generalization`

### `shared_visual_render_engine_canon` — Shared Visual Render Engine Canon

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/shared_visual_render_engine_canon.md`
- **Priority:** `40`
- **Trigger phrases:** `shared render engine`; `visual renderer`; `drawing engine`; `canvas rendering`; `render contract`
- **User intent examples:** `Keep all visual outputs using the shared render engine.`
- **Aliases:** `architecture pattern`; `engine`; `generalized canon`; `render`; `shared`; `shared visual render engine canon`; `shared_visual_render_engine_canon`; `shared_visual_render_engine_canon.md`; `visual`
- **When to load:** When rendering/drawing/visual output contracts or shared visual engines are central.
- **When not to load:** Do not load for non-visual backend logic.
- **Required companion prompts:** `box_architecture_canon`; `project_specific_prompt_generalization`

### `transform_resolver_architecture_contract` — Transform Resolver Architecture Contract

- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/transform_resolver_architecture_contract.md`
- **Priority:** `40`
- **Trigger phrases:** `transform resolver`; `base identity plus transform`; `resolver architecture`; `active transform`; `identity resolver`
- **User intent examples:** `Use base identity plus active transform resolver architecture.`
- **Aliases:** `architecture`; `architecture pattern`; `contract`; `generalized canon`; `resolver`; `transform`; `transform resolver architecture contract`; `transform_resolver_architecture_contract`; `transform_resolver_architecture_contract.md`
- **When to load:** When an entity has stable identity plus selectable transforms/views/states.
- **When not to load:** Do not load for simple one-state data models.
- **Required companion prompts:** `box_architecture_canon`; `project_specific_prompt_generalization`
