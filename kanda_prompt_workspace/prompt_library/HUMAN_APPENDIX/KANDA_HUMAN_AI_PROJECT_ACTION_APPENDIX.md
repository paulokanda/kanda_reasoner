# KANDA Human ↔ AI Project Action Appendix

This appendix is the human-facing counterpart to the Prompt Navigation Index.

It answers two practical questions:

1. **What can the human ask the AI to do in the project?**
2. **What should the AI ask the human to provide when the correct prompt stack is missing?**

This file is not a replacement for the route table. It is a daily operational guide for using the prompt system safely.

---

## 1. Core Principle

The human should not need to remember exact prompt filenames.

The human can describe the work naturally, for example:

```text
start the day
this module is too big
create a patch bundle
ok freeze
create handoff
review these prompts
make this project-specific prompt generic
```

The AI must translate that request into the correct prompt stack using:

```text
ROUTING/PROMPT_NAVIGATION_INDEX.md
ROUTING/prompt_navigation_index.json
ROUTING/prompt_route_coverage_table.csv
```

If the needed prompt stack was not provided in the current chat, the AI should ask for it explicitly or tell the human which files to upload.

---

## 2. Human Quick Commands

Use these simple phrases when working with AI.

| Human says | AI should understand as | Prompt family to load/request |
|---|---|---|
| “Start the day” | Begin a structured project session | session start + prompt stack load order + project checklist |
| “Continue from last time” | Resume from previous context | current workflow handoff + daily startup loader |
| “What should I upload?” | Ask for session input package | session start upload checklist |
| “This module is too big” | Large module refactor | large module refactor + box architecture + bundle workflow |
| “Refactor this safely” | Surgical refactor with validation | refactor protocol + box boundaries + tests/validation |
| “Fix this error” | Evidence-first repair | implementation roadmap + patch delivery + validation |
| “Create patch bundle” | Generate installable change bundle | bundle-gated workflow + implementation delivery |
| “Create install code” | Produce PowerShell installer | code implementation and send-to-user protocol |
| “Do not break other tabs” | Require cross-box protection | box architecture + stateful control regression canon |
| “Check if evidence is stale” | Validate generated artifacts/source timestamps | evidence freshness gate |
| “Validate before freeze” | Run validation gates before canonization | patch registry validation freeze + evidence freshness |
| “Ok freeze” | Governance/canon update after validation | active governance freeze update |
| “Create handoff” | Prepare next-session or next-AI handoff | workflow handoff template |
| “Audit this prompt batch” | Review prompts for integration/deprecation/update | prompt audit + prompt lifecycle |
| “Generalize this project prompt” | Remove project-specific assumptions | project-specific canon generalization protocol |
| “Create a new prompt” | Build a reusable prompt asset | prompt authoring lifecycle roadmap |
| “Rebuild prompt library” | Prepare prompts for Tab Prompt Library | prompt routing/indexing + metadata/group logic |
| “Make it professional” | Add missing engineering infrastructure | professional AI-assisted engineering framework |
| “Prepare for release” | Productization readiness | productization + lifecycle + SRE prompts |

---

## 3. What To Deliver To AI By Situation

### 3.1 Starting the day

Human instruction:

```text
Start the day for KANDA Reasoner.
Use the current prompt system and tell me what files you need.
```

Deliver or ask AI to request:

```text
- ai_human_partnership_session_start.md
- daily_reasoner_startup_loader.md
- general_prompt_stack_load_order.md
- session_start_upload_checklist.md
- prompt_navigation_index.md
- workflow_handoff_template.md, if continuing prior work
```

AI should ask for:

```text
- current project ZIP or changed files
- last handoff, if available
- validation output, if work continues from a previous patch
- active goal for this session
```

---

### 3.2 Continuing previous work

Human instruction:

```text
Continue from the last handoff.
```

Deliver or ask AI to request:

```text
- workflow_handoff_template.md
- freeze_code_intake_and_form_protocol.md, if prior work was frozen
- prompt_navigation_index.md
- latest project ZIP or changed files
```

AI should ask:

```text
Which part is frozen?
Which patch was installed?
What validation passed or failed?
What is the next intended task?
```

---

### 3.3 Refactoring a large module

Human instruction:

```text
This module is too big. Refactor it safely.
```

Deliver or ask AI to request:

```text
- large_module_refactor_protocol.md
- box_architecture_canon.md
- bundle_gated_development_workflow.md
- python_refactoring.md
- python_testing_pytest.md
- current relevant source files
```

AI must ask for Box Logic if not provided:

```text
What is the active box?
What files belong to this box?
Which public API must be preserved?
Which files are explicitly out of scope?
What validation should prove the refactor is safe?
```

---

### 3.4 Fixing an error or failed validation

Human instruction:

```text
Fix this error without changing unrelated logic.
```

Deliver or ask AI to request:

```text
- implementation_roadmap_builder.md
- bundle_gated_development_workflow.md
- error log or validation output
- exact files touched by the failing patch
```

AI should ask:

```text
Is the error from source code, generated artifact, stale evidence, installer, import path, GUI state, or validation script?
Can you provide the full terminal output without clearing it?
Which previous patch introduced the issue?
```

---

### 3.5 Creating an installable patch bundle

Human instruction:

```text
Create a ZIP patch bundle for this change.
```

Deliver or ask AI to request:

```text
- code_implementation_delivery_protocol.md
- bundle_gated_development_workflow.md
- box_architecture_canon.md
- target source files
```

AI should output:

```text
- ZIP bundle
- install PowerShell script
- backup/rollback instructions
- files changed list
- validation checklist
- no terminal clear commands
```

AI must not say the work is frozen until human validation passes.

---

### 3.6 UI change, aesthetic change, or tab layout change

Human instruction:

```text
Change only the visual layout. Do not change logic.
```

Deliver or ask AI to request:

```text
- box_architecture_canon.md
- stateful_control_dropdown_regression_canon.md
- bundle_gated_development_workflow.md
- relevant GUI file(s)
- screenshot or exact visual target, if available
```

AI should ask:

```text
Which widgets are logic-bound and must not be renamed/removed?
Which hidden fields must remain for existing logic?
Which tab/box owns the layout?
What manual smoke test confirms no regression?
```

---

### 3.7 Prompt audit, prompt update, or prompt generalization

Human instruction:

```text
Audit these prompts and generalize useful ones for KANDA Reasoner.
```

Deliver or ask AI to request:

```text
- prompt_authoring_lifecycle_roadmap.md
- project_specific_canon_generalization_protocol.md
- prompt_navigation_index.md
- prompt_substitution_map.md
- source prompt ZIP(s)
```

AI should classify each prompt as:

```text
- keep active
- update existing active prompt
- create new generalized prompt
- reference-only
- deprecated/discarded
```

AI should not promote domain-specific assumptions as general KANDA Reasoner rules.

---

### 3.8 Renaming prompts or rebuilding prompt folder structure

Human instruction:

```text
Rename prompts to intuitive names and rebuild the clean prompt folder.
```

Deliver or ask AI to request:

```text
- prompt_navigation_index.md
- prompt_route_coverage_table.csv
- prompt metadata files, if available
- current prompt_library folder or ZIP
```

AI should produce:

```text
- clean use-based folder structure
- intuitive filenames
- updated metadata
- updated route table
- verification report
- no active old-name alias map unless live code depends on old names
```

---

### 3.9 Freezing/canonizing validated work

Human instruction:

```text
Ok freeze this.
```

Deliver or ask AI to request:

```text
- freeze_code_intake_and_form_protocol.md
- workflow_handoff_template.md
- validation results
```

AI must ask before freezing:

```text
Which exact files are validated?
Which tests passed?
Was the GUI manually smoke-tested, if applicable?
Is any generated evidence stale?
What is the new frozen baseline identifier?
```

AI must not freeze based only on its own confidence.

---

### 3.10 Creating an end-of-session handoff

Human instruction:

```text
Create a handoff for next AI.
```

Deliver or ask AI to request:

```text
- workflow_handoff_template.md
- freeze_code_intake_and_form_protocol.md, if anything was frozen
- validation outputs
- list of installed patches
- remaining issues
```

AI should write:

```text
- what was done
- what is frozen
- what is not frozen
- what files changed
- what validations passed/failed
- exact next step
- warnings for next AI
```

---

## 4. When To Remember Box Logic

Box Logic is required whenever the task may touch code, architecture, GUI state, prompt library structure, or generated artifacts.

Human reminders:

```text
Remember Box Logic.
State the active box first.
Declare what files are allowed to change.
Do not touch other boxes.
If you must touch another box, declare it first.
```

AI must apply Box Logic for:

```text
- implementation
- refactor
- architecture repair
- GUI changes
- prompt library rebuild
- validation framework changes
- generated artifact pipelines
- installer/patch bundle creation
- cross-file or cross-folder cleanup
```

AI may not need full Box Logic for:

```text
- pure explanation
- conceptual planning without file changes
- simple status summary
- non-project conversation
```

Minimum Box Logic statement:

```text
Active box:
Owner paths:
Allowed files:
Out-of-scope files:
Cross-box touches:
Public contracts to preserve:
Validation required:
```

---

## 5. AI-Side Obligation: Ask For The Correct Prompts

If the human asks for an action but the relevant prompt stack is not available, the AI should not improvise silently.

AI should say:

```text
To do this safely, please provide or confirm these prompt files:
- [prompt A]
- [prompt B]
- [prompt C]
```

Or, if the prompt library is already available:

```text
I will route this request through:
- [prompt A]
- [prompt B]
- [prompt C]
```

The AI should especially ask for correct prompts when the task involves:

```text
- code changes
- large module refactor
- architecture validation
- prompt migration/import
- governance freeze
- generated artifact validation
- cross-box change
- release/productization work
```

---

## 6. AI-Side Obligation: Ask For Missing Evidence

The AI should request evidence, not guess, when evidence is missing.

Examples:

```text
Please provide the current project ZIP.
Please provide the exact file you want changed.
Please provide the terminal output without clearing it.
Please provide the failing validation report.
Please provide the latest handoff.
Please provide the active prompt folder ZIP.
Please provide the previous patch bundle, if this is a repair.
```

If evidence is stale or incomplete, the AI should mark the answer as provisional and avoid freeze/canonization.

---

## 7. Human-Side Minimal Session Start Message

Use this when opening a new chat:

```text
We are working on KANDA Reasoner.
Use the prompt navigation system.
First identify the active task and required prompt stack.
If a needed prompt or evidence file is missing, ask me for it before implementing.
Always apply Box Logic for code, architecture, prompt-library, or patch-bundle changes.
Do not freeze anything unless I confirm validation passed.
```

---

## 8. Human-Side Minimal Refactor Message

```text
Refactor this safely.
First state the active box, owner paths, allowed files, out-of-scope files, public contracts, and validation plan.
Use the large module/refactor prompt stack.
Create a patch bundle only after the plan is clear.
Do not change unrelated logic.
```

---

## 9. Human-Side Minimal Freeze Message

```text
Ok freeze this.
Before updating governance, ask me for the validation evidence you need.
List exactly what is being frozen and what is not frozen.
Do not infer validation from your own confidence.
```

---

## 10. Human-Side Minimal Prompt-Audit Message

```text
Audit these prompts for KANDA Reasoner.
Generalize useful logic, update existing prompts if duplicated, deprecate/discard what is already covered, and produce a clean insertable ZIP.
Do not import project-specific assumptions as active general rules.
```

---

## 11. Final Operating Rule

The human can speak naturally.

The AI must route professionally.

```text
Human messy request
→ AI detects intent
→ AI identifies required prompt stack
→ AI asks for missing prompts/evidence
→ AI applies Box Logic when needed
→ AI produces a controlled deliverable
→ Human validates
→ Only then freeze/canonize
```
