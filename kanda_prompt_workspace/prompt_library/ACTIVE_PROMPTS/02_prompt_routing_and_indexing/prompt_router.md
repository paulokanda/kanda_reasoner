# Prompt Router

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.2
Status: Reusable beginning-of-day prompt router
Prompt ID: kanda_prompt_router
Prompt type: conditional prompt router
Scope: Route a user request to the correct Tab 9 prompt groups, prompts, and overlays

## Purpose

Use this prompt at the beginning of a Kanda Reasoner work session.

The router helps the AI decide which prompt-library group or overlay should be
loaded for the current task.

It does not replace the specialized prompts. It points to them.

## Core rule

Every new prompt injected into Tab 9 must be routable.

A new prompt is routable when at least one of these is true:

```text
it is included in a relevant PROMPT_GROUPS.json group
it is referenced by a parent methodology prompt
it is referenced by an authoring guide as a known reusable prompt
it is part of a named stack used at the beginning or end of a chat
it is deliberately marked as archive/reference-only
```

If none of these is true, the prompt is marooned.

## Beginning-of-day behavior

At the start of a work session:

1. Read the user's task.
2. Classify the task type.
3. Select the smallest useful prompt stack.
4. Do not load every prompt.
5. Load specialized overlays only when their trigger condition is met.
6. If the task is ambiguous, ask for the minimal missing information or choose
   the safest read-only planning route.

## Forgotten-rule recovery rule

If the AI forgets, doubts, or cannot verify a KANDA rule, it must not assume, guess, or hallucinate a substitute rule.

Recovery order:

1. Go back to the router logic and active startup canon.
2. Load or request the smallest relevant prompt group, folder card, source map, or guardrail needed to recover the rule.
3. If the rule is still unclear, ask the human for the canon decision before acting.

The human is the project partner. Asking a clarifying rule question is preferred over inventing terminal behavior, patch-delivery behavior, freeze behavior, prompt-routing behavior, or validation behavior.

## Router table

### General engineering implementation

Trigger:

```text
implement code
repair code
refactor code
create a bundle
modify source files
```

Load or recommend:

```text
kanda_bundle_gated_development_workflow
```

If Python source code is changed, also load:

```text
python_clean_code_overlay
```

Group to open in Tab 9:

```text
high_risk_engineering
```

### Python implementation, repair, or tests

Trigger:

```text
Python module
Python function
Python class
test file
validator
report writer
runtime helper
```

Load or recommend:

```text
kanda_bundle_gated_development_workflow
python_clean_code_overlay
```

Group to open in Tab 9:

```text
high_risk_engineering
```

### Large module refactor

Trigger:

```text
large file
module split
class too large
mixed responsibility
extract helper
preserve public imports
```

Load or recommend:

```text
kanda_bundle_gated_development_workflow
python_clean_code_overlay
large_module_overlay_profile_template
0000_5_5_large_module_refactor_protocol_template
```

Group to open in Tab 9:

```text
large_module_refactor
```

### Architecture warning cleanup

Trigger:

```text
architecture warning
mixed responsibility
cross-box collision
dead code
generated artifact contract
validation issue
```

Load or recommend:

```text
architecture_hardening_overlay_template
0000_8_1_architecture_hardening_triage_protocol_template
kanda_bundle_gated_development_workflow
```

Group to open in Tab 9:

```text
architecture_hardening
```

### Governed patch ZIP release

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


Trigger:

```text
patch ZIP
install ZIP
create zip
deliver zip
PowerShell install block
validation block
KANDA_FREEZE_HINT.json
freeze-form JSON
release gate
patch delivery
```

Load or recommend:

```text
05_patch_delivery_and_validation
pre_output_contract_gates
freeze_code_intake_and_form_protocol
```

Group to open in Tab 9:

```text
05_patch_delivery_and_validation
03_governance_freeze_and_handoff
```

Rule:

Classify as `PATCH_DELIVERY_RELEASE`. This is a governed output-time release event. The AI must not emit a ZIP download link, install block, validation block, `KANDA_FREEZE_HINT.json`, or freeze-form JSON until the ZIP contract validator has passed or the patch is explicitly declared non-freezeable. If the contract is not verified, output `CONTRACT NOT MET - PATCH DELIVERY BLOCKED` and state the missing requirement.



<!-- CHATGPT_KANDA_ROUTING_CHOICE_OUTPUT_PROTOCOL_V1_START -->
### Manual Prompt Router Reasoner capture / KANDA_ROUTING_CHOICE output

Trigger:

```text
KANDA_ROUTING_CHOICE
manual router capture
Prompt Router Reasoner paste block
which prompt should I use
route this task
select the prompt
send this to Prompt Router Reasoner
```

Load or apply:

```text
chatgpt_kanda_routing_choice_output_protocol
prompt_navigation_index
prompt_router
prompt_identity_code_registry_canon, when prompt_code assignment or prompt creation is involved
```

Required behavior:

```text
Emit a valid advisory KANDA_ROUTING_CHOICE_START / KANDA_ROUTING_CHOICE_END JSON block when the user asks for routing-choice output that will be pasted into Prompt Router Reasoner.
```

Boundary:

```text
Browser ChatGPT is advisory only. The block must not claim final local authority, write files, apply patches, write freeze memory, activate ML, or bypass validation. Local KANDA remains responsible for validating prompt addresses and loading canonical ACTIVE_PROMPTS text.
```
<!-- CHATGPT_KANDA_ROUTING_CHOICE_OUTPUT_PROTOCOL_V1_END -->

### Prompt creation or prompt update

Trigger:

```text
create a new prompt
update a prompt
add an overlay
make a prompt visible in Tab 9
register a prompt group
```

Load or recommend:

```text
prompt_insertion_and_router_registration_protocol
prompt_identity_code_registry_canon
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
kanda_bundle_gated_development_workflow, if creating an installable bundle
```

If the new prompt involves Python code generation or Python refactor, also
recommend:

```text
python_clean_code_overlay
```

Group to open in Tab 9:

```text
teach_ai_prompt_authoring
```




<!-- PROMPT_INSERTION_ROUTER_REGISTRATION_PROTOCOL_V1_START -->
### Prompt insertion and router registration

Trigger:

```text
insert a new prompt
add a new prompt to ACTIVE_PROMPTS
register this prompt in the router
connect this prompt to router logic
make the router call this prompt when necessary
activate a prompt in router prompt logic
```

Load or recommend:

```text
prompt_insertion_and_router_registration_protocol
prompt_identity_code_registry_canon
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
bundle_gated_development_workflow, if creating an installable bundle
```

Group to open:

```text
07_prompt_authoring_and_audit
02_prompt_routing_and_indexing, if router/navigation files must be changed
```

Rule:
The protocol is routed, not always_startup. The AI must inspect the target folder assimilation, metadata, existing prompts, and router/navigation indexes before deciding create vs update vs link/register. The exact ACTIVE_PROMPTS folder depends on the type of prompt.
<!-- PROMPT_INSERTION_ROUTER_REGISTRATION_PROTOCOL_V1_END -->

<!-- PROMPT_IDENTITY_CODE_REGISTRY_CANON_V1_START -->
### Prompt identity, prompt_code, and copy/paste prompt address

Trigger:

```text
prompt code
prompt identifier
prompt registry
assign code to prompt
make prompt copy/paste addressable
ChatGPT should display selected prompt code
new prompt needs a code
KPR code
```

Load or recommend:

```text
prompt_identity_code_registry_canon
prompt_insertion_and_router_registration_protocol, if creating or registering a prompt
prompt_canon_reconciliation_protocol
prompt_audit_canon
```

Group to open:

```text
07_prompt_authoring_and_audit
02_prompt_routing_and_indexing, if router/navigation files must be changed
```

Rule:
Every new routed prompt must receive a stable `prompt_code` using `KPR-<folder_number>-<sequence>` before router registration is considered complete. ChatGPT router-choice blocks must display prompt_code and prompt_id when available, and KANDA Reasoner must resolve the code locally.
<!-- PROMPT_IDENTITY_CODE_REGISTRY_CANON_V1_END -->


### Pilot/Copilot Phase 0 router canon after M35

Trigger:

```text
start Pilot
start Copilot
continue after M35
Pilot/Copilot Phase 0
create P0
Pilot scope charter
Pilot projection
Pilot simulation
Pilot disagreement taxonomy
Pilot implementation gate
Pilot router reproduction
Limited Shadow Runtime after M35
```

Load or recommend:

```text
routing_signal_scorer_v3_pilot_copilot_phase0_router_canon
kanda_routing_system_canon
kanda_box_shielding_canon
prompt_navigation_index
GROUP_ASSIMILATION_INDEX
```

Group to open in Tab 9:

```text
02_prompt_routing_and_indexing
```

Rule:

If P0 is not yet validated and frozen, the only safe implementation milestone is P0. Do not implement Pilot, Copilot, prompt loading, persistence, runtime integration, training-data use, batch mode, or Limited Shadow Runtime.



### RG-LAB-000 post-P12 ML LAB phase entry

Trigger:

```text
canonize LAB phase
start LAB after P12
continue after P12
go next after P12
LAB-0
lab charter
ML lab/test
router prompt logic lab
test ML router prompt logic
prompt choosing reliability
continue ML implementation after lab
```

Load or recommend:

```text
routing_signal_scorer_v3_lab_phase_entry_router_canon
routing_signal_scorer_v3_pilot_copilot_phase0_router_canon
kanda_routing_system_canon
kanda_box_shielding_canon
prompt_navigation_index
GROUP_ASSIMILATION_INDEX
```

Group to open in Tab 9:

```text
02_prompt_routing_and_indexing
```

Rule:

After P12, "next" does not mean direct ML implementation. First canonize LAB entry, then route to LAB-0 only. LAB-0 is documentation-only. Do not create LAB code, schema, fixtures, corpus, runner, candidate harness, prompt loading, persistence, provider calls, embeddings, activation, field-test mode, runtime Pilot, or Copilot behavior.

### Governance or canon update

Trigger:

```text
freeze
canon
governance
accepted warning baseline
official project truth
```

Load or recommend:

```text
0000_4_0_end_of_chat_governance_update_template
governance_update_overlay_notes_template
```

Group to open in Tab 9:

```text
governance_freeze
```

Do not perform governance updates unless validated work occurred and the user
explicitly approved the freeze.

### Handoff or session closure

Trigger:

```text
handoff
end of chat
continue next time
session summary
next AI should know
```

Load or recommend:

```text
0000_6_0_workflow_handoff_template
text_library_freeze_handoff
prompt_library_current_state
prompt_library_roadmap
```

Group to open in Tab 9:

```text
end_of_day_handoff
```

### Domain-specific overlays

Trigger:

```text
do-not-regress rule
domain decision table
UI component boundary
special overlay
```

Load or recommend:

```text
domain_decision_table_overlay_template
ui_component_do_not_regress_overlay_template
```

Group to open in Tab 9:

```text
domain_special_overlays
```

### Prompt library maintenance

Trigger:

```text
prompt pack
prompt import
prompt export
prompt validation
prompt metadata checklist
prompt library QA
```

Load or recommend:

```text
prompt_template_blueprint
prompt_pack_manifest_template
prompt_pack_export_checklist
prompt_pack_import_checklist
prompt_validation_report_template
prompt_library_qa_checklist
prompt_library_release_checklist
prompt_library_master_index
```

Group to open in Tab 9:

```text
prompt_library_tools
```

## Marooned prompt audit rule

When adding or updating a prompt, check whether it is marooned.

A prompt is probably marooned if:

```text
it has a prompt_id but appears in no group
it is not referenced by any stack or parent prompt
it has no metadata
it has a metadata prompt_id that does not match any group prompt_id
it is important but only discoverable by manual file browsing
```

If a prompt is marooned, fix exactly one of these:

```text
add it to the correct existing group
reference it from the correct parent prompt
reference it from the correct authoring guide
mark it as archive/reference-only in metadata
```

Do not add a new group or spinning box unless the user explicitly asks for it.

## New prompt routing requirement

Every new prompt-library bundle must answer:

```text
Where is this prompt routed?
Which group contains it?
Which parent prompt, guide, or stack knows it exists?
Is it intended for beginning-of-day use?
Is it intended only as an optional overlay?
Is it archive/reference-only?
```

If the answer is unclear, the bundle is incomplete.

## Negative examples

Do not update unrelated prompts just to make them aware of a new asset.

Examples:

```text
Do not update a governance-freeze prompt to reference a Python formatting overlay
unless governance output directly depends on that overlay.

Do not update Tab 1 through Tab 8 prompts to reference Tab 9 prompt-authoring
assets.

Do not add every new prompt to Daily Start. Daily Start should contain routing
logic, not the entire library.
```

## Output expectation

After routing, tell the user:

```text
recommended group to open
prompts or overlays to load
whether the task is code, text-only, governance, handoff, or planning
whether bundle-gated validation is required
whether manual Tab 9 visibility validation is required
```


### Canon reconciliation or prompt-stack update from uploaded canon notes

Trigger:

```text
uploaded canon notes
compare canon to prompts
add useful canon ideas to prompts
update prompt library from handoff/canon
not sure if this belongs in an existing prompt
```

Load or recommend:

```text
kanda_prompt_canon_reconciliation_protocol
kanda_bundle_gated_development_workflow
kanda_prompt_router
prompt_library_master_index
prompt_library_current_state
prompt_library_roadmap
```

Group to open in Tab 9:

```text
teach_ai_prompt_authoring
```

Rule:

Do not blindly paste the canon into every prompt. Classify each idea as:

```text
already present
update existing prompt
create new prompt
reference-only / archive
requires official governance freeze
reject or defer
```

### Tab 1 and Tab 2 detector taxonomy planning

Trigger:

```text
architecture detector roadmap
workflow detector roadmap
First step check correct architecture
Second step check correct workflow
Tab 1 errors taxonomy
Tab 2 workflow taxonomy
```

Load or recommend:

```text
kanda_tab1_tab2_audit_taxonomy
kanda_bundle_gated_development_workflow
0000_8_0_reasoner_architecture_hardening_triage_protocol
```

Group to open in Tab 9:

```text
architecture_hardening
```

### Tab 4 docstring quality roadmap

Trigger:

```text
insert missing docstring quality
AI docstring generation
heuristic docstring generation
structured docstring rendering
Tab 4 docstring roadmap
```

Load or recommend:

```text
kanda_tab4_docstring_quality_roadmap
kanda_bundle_gated_development_workflow
python_clean_code_overlay
```

Group to open in Tab 9:

```text
high_risk_engineering
```

### Productization readiness roadmap

Trigger:

```text
professional app readiness
commercial SaaS readiness
make Kanda Reasoner professional
release-grade product
polished developer tool
```

Load or recommend:

```text
kanda_productization_readiness_roadmap
kanda_bundle_gated_development_workflow
sre_python
peopleware_python
secure_python_app_security
```

Group to open in Tab 9:

```text
prompt_library_tools
```

### GUI visual prototype or WebEngine experiment

Trigger:

```text
3D cube prototype
PySide6 cube
visual dashboard idea
WebEngine Three.js experiment
```

Load or recommend:

```text
reference_only_visual_prototype_notes
```

Group to open in Tab 9:

```text
domain_special_overlays
```

Rule:

Treat prototype snippets as reference-only unless the user opens a dedicated GUI
box implementation task with current source files and validation gates.

## Final reminder

The router should reduce prompt clutter.

It should make the correct specialized prompt easier to find, not load the whole
library by default.


## Change Log

- v1.0.2: Added forgotten-rule recovery rule: do not guess from memory; return to router/startup canon first, then ask the human if still uncertain.
- v1.0.1: Added routes for canon reconciliation, Tab 1/Tab 2 detector planning, Tab 4 docstring quality, productization readiness, and visual prototype reference material.

---

## Professional engineering infrastructure routing update

### Professional engineering infrastructure routing

Use this routing block when the user asks about professionalizing the Kanda
Reasoner workflow, making AI-assisted development auditable, tracking patches,
freezing validated work, preventing stale evidence, or preserving terminal logs.

Trigger phrases:

```text
professional AI-assisted engineering
missing implementations to become professional
patch registry
validation runner
evidence freshness
freeze governance
GUI smoke checklist
terminal log preservation
AI-human partnership
complex Python apps with AI
```

Load or recommend:

```text
professional_ai_assisted_engineering_framework.md
professional_infrastructure_roadmap.md
evidence_freshness_gate.md
patch_registry_validation_freeze.md
bundle_gated_development_workflow.md
```

Task type:

```text
planning, governance, validation infrastructure, or professional workflow hardening
```

Default behavior:

1. Do not implement all infrastructure modules at once.
2. Start with Task 0 audit.
3. Build one narrow box at a time.
4. Prefer read-only detectors before mutating source.
5. Never mark a patch frozen until patch registry, validation runner, workflow,
   architecture, evidence freshness, and GUI checklist gates are satisfied where applicable.

Recommended implementation order:

```text
Evidence Freshness Gate
Patch Registry
Unified Validation Runner
GUI Smoke Checklist System
Freeze Governance Workflow
Git Checkpoint Gate
Patch Install Manifest Indexer
Failure Triage Classifier
Prompt and Protocol Enforcement
End-of-Session Handoff Generator
State-Based Testing Sandbox
Human Override Log
```

Do not confuse reference documents with app source. If a prompt asset should be
active, it must be routed through Tab 9 groups or referenced by a parent prompt.


## EEG Project Generalization Routes — Added from CANON.zip and PROMPTS.zip

Use these routes when the user brings prompts or canon from a domain-specific project and asks to generalize them for KANDA Reasoner.

### Project-specific canon generalization

Trigger phrases:
- generalize prompts from another project
- import useful canon from old project
- convert EEG Kanda canon to KANDA Reasoner
- batch correct and add if useful
- remove domain-specific assumptions

Route to:
- project_specific_prompt_generalization.md

### Closed-box product delivery

Trigger phrases:
- each module needs its own box
- isolated boxes
- feature boxes should not mix
- UI box is owning logic it should not own
- box delivers only final product

Route to:
- closed_box_delivery_canon.md
- box_architecture_canon.md

### Data transform pipeline invariants

Trigger phrases:
- immutable source truth
- canonical working base
- derived runtime output
- rebuild from canonical
- do not stack transforms
- view-only state vs signal/data state

Route to:
- data_transform_pipeline_invariants.md

### Stateful controls and dropdowns

Trigger phrases:
- dropdown state
- combobox sizing
- options disappear
- selected value changes after refresh
- caption adapter
- control hydration
- stable id vs display label

Route to:
- stateful_control_regression_canon.md

### Plugin packages / importable extensions

Trigger phrases:
- plugin package
- import plugin
- extension file
- package manifest
- portable artifact
- user imports a custom package

Route to:
- plugin_package_import_canon.md

### Shared visual/render engine

Trigger phrases:
- two tools render same thing
- shared renderer
- visual engine
- premium visual mode
- rendering should change only visuals
- same chart/scene in multiple tabs

Route to:
- shared_visual_render_engine_canon.md

### Domain decision tables

Trigger phrases:
- label normalization
- alias mapping
- role classification
- manual override
- contradiction handling
- uncertainty notice
- registry integrity

Route to:
- domain_decision_table_template.md

### Transform resolver architecture

Trigger phrases:
- source identity versus active transform
- base identity
- resolver table
- invalid combination
- selected transform maps to runtime operation

Route to:
- transform_resolver_architecture_contract.md


## Terminal cleanup canon

For any response that emits a terminal block, classify the terminal output before writing the footer. Successful install blocks must use the 5-second `Clear-Host` success footer and must not ask for Enter. Install errors, validation, validation errors, diagnostics, and any other terminal output must use the Enter/Clear-Host/Enter/Clear-Host cleanup footer. The terminal must be cleaned, not closed. Install blocks must include a fail-safe `try/catch` or text-equivalent wrapper so an install error cannot bypass cleanup.
