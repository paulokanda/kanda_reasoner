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
teach_ai_tab9_prompt_authoring_guide
teach_ai_create_or_update_prompt_request
tab9_prompt_asset_placement_rules
kanda_bundle_gated_development_workflow
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
