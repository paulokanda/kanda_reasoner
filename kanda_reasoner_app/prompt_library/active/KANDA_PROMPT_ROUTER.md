# KANDA PROMPT ROUTER

Version: 1.0.0
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

## Final reminder

The router should reduce prompt clutter.

It should make the correct specialized prompt easier to find, not load the whole
library by default.
