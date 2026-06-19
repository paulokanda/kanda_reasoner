# KANDA Human Project Action Menu Appendix

Purpose: this file is a human-facing helper. It tells the human partner what kinds of project actions can be requested from AI, how to phrase them, and what prompt stack or project evidence should usually be provided.

This is not an active AI behavior canon. It is a reading/reference appendix for the human.

Status: updated to match the KANDA Context Routing Layer manual-use box.

---

## Core rule

You do not need to know the exact technical prompt name. You can speak naturally. The AI should route your request to the correct prompt stack.

However, when a task is risky, architectural, cross-box, data-related, prompt-audit-related, validation-related, or intended to become official, you should expect AI to ask for the correct supporting prompts/files before implementing.

The normal pattern is:

```text
Human asks naturally
-> AI classifies the task
-> AI identifies required prompt groups
-> AI asks for folder cards and specialist prompts
-> Human loads only what is needed
-> AI proceeds only inside the loaded context
```

---

## 1. Starting the day / starting a new session

You can say:

- "Start the day."
- "We will continue KANDA Reasoner."
- "Load the project working context."
- "Continue from the latest handoff."
- "Use the Context Routing Layer manually."

Core Tier 0 routing files/prompts to provide:

- `start_of_day_master_stack`
- `session_start_upload_checklist`
- `ai_prompt_request_canon`
- `prompt_navigation_index`
- `GROUP_ASSIMILATION_INDEX`

Useful optional files/prompts to provide:

- `FOLDER_ASSIMILATION_CARDS_INDEX`
- latest workflow handoff
- latest validation/freeze status
- active project overlay, if working inside a concrete project
- project tree or relevant file list if implementation will happen

AI should establish:

- current task
- task intent
- active box
- current baseline/freeze status
- whether work is planning, audit, implementation, validation, freeze, or handoff
- required prompt groups
- optional prompt groups
- folder cards to load
- specialist prompts to load
- missing behavior: `HARD_STOP`, `STEP_PAUSE`, or `DEGRADED_WARNING`

AI should not implement until required prompts are loaded or the human explicitly redirects the task.

---

## 2. Creating a new folder, box, subsystem, or database area

You can say:

- "We will create a new folder for the database."
- "Create a new data storage box."
- "Add a database layer."
- "Create a new subsystem for persistence."

AI should request/load:

1. `session_start_upload_checklist`
2. `ai_prompt_request_canon`
3. `prompt_navigation_index`
4. `GROUP_ASSIMILATION_INDEX`
5. selected folder assimilation card(s)
6. `box_architecture_canon`
7. `project_folder_organization_canon`
8. `python_database_design_optimisation`
9. `python_validation_serialisation_type_safety`
10. `python_security_threat_prevention`
11. `implementation_roadmap_builder`
12. `bundle_gated_development_workflow`

You should be ready to provide:

- intended folder path
- database type: SQLite, JSON, CSV, PostgreSQL, etc.
- owner box
- files allowed to change
- files explicitly out of scope
- validation command or expected manual test
- whether this is prototype, production, or reference-only

Expected missing behavior:

```text
HARD_STOP before implementation if architecture, database, or ownership prompts are missing.
```

---

## 3. Refactoring a large module

You can say:

- "This module is too big."
- "Split this file."
- "Refactor this module without changing behavior."
- "Extract helpers/classes but preserve logic."

AI should request/load:

- `large_module_refactor_protocol`
- `box_architecture_canon`
- `bundle_gated_development_workflow`
- `python_refactoring`
- `architecture_hardening_triage_protocol` if architecture issues are involved
- current file/module and related tests/validators

You should define:

- primary file/module
- current line count, if known
- allowed extraction locations
- public API that cannot change
- tests/validation commands
- maximum safe scope for one patch

Expected missing behavior:

```text
HARD_STOP before modifying the file.
```

---

## 4. Fixing bugs or validation errors

You can say:

- "Fix this error."
- "Tab 1 failed."
- "Tab 2 validator fails."
- "This patch broke something."
- "This import error appeared."

AI should request/load:

- exact validation logs or traceback
- changed-file context
- `bundle_gated_development_workflow`
- `evidence_freshness_gate`
- `patch_registry_validation_freeze`
- relevant domain prompt based on the error type
- relevant Python engineering prompt if code will be changed

You should provide:

- exact error message/log
- file where failure occurred
- command run
- expected behavior
- what changed immediately before failure
- whether the failure is new, old, intermittent, or environment-specific

Expected missing behavior:

```text
STEP_PAUSE until logs/source evidence are available.
HARD_STOP before code modification if delivery/validation protocol is missing.
```

---

## 5. UI/layout-only changes

You can say:

- "Move this button only."
- "Do not change logic, just aesthetics."
- "Keep columns symmetrical."
- "Change label text only."

AI should request/load:

- `box_architecture_canon`
- `bundle_gated_development_workflow`
- current GUI file
- screenshot or description of current layout
- relevant UI/layout prompt if available

AI should preserve:

- existing callbacks
- existing object names used by logic
- worker paths
- validation flow
- hidden state variables
- layout symmetry constraints explicitly stated by the human

Expected missing behavior:

```text
STEP_PAUSE before editing GUI code.
HARD_STOP if the requested visual change risks changing logic callbacks or hidden state.
```

---

## 6. Creating, updating, or auditing prompts

You can say:

- "Create a new prompt."
- "Generalize this prompt from another project."
- "Audit these prompts."
- "Rename prompts to intuitive names."
- "Update the navigation index."
- "Compare these two prompts."
- "Decide if this prompt is deprecated."

AI should request/load:

- `prompt_navigation_index`
- `GROUP_ASSIMILATION_INDEX`
- selected folder card for prompt authoring/audit
- `prompt_audit_canon`
- `project_specific_prompt_generalization`
- `prompt_canon_reconciliation_protocol`
- `prompt_substitution_map`
- target prompt folder
- source prompt files

AI should classify each prompt as:

- active
- audited candidate
- optional
- reference-only
- deprecated
- retired
- duplicate
- needs generalization
- needs split
- integration candidate needed
- blocked by conflict

Critical audit rule:

```text
The index tells AI where to look.
The actual prompt file proves what is inside.
No related prompt file means no final overlap decision.
```

If the AI suspects that a rule, paragraph, workflow, command, or feature already exists in a previously audited prompt, it must request the actual related prompt file before making a final duplicate / newer / older / conflicting / superseded decision.

If a useful snippet belongs to a different prompt responsibility, AI should extract it into an integration candidate, not silently insert it into another prompt during the same audit.

Recommended integration candidate filename pattern:

```text
TO_BE_INSERTED_IN_PROMPT_<TARGET_ID>__FROM_<SOURCE_ID>__IC###.md
```

Expected missing behavior:

```text
STEP_PAUSE until related prompt files are available for comparison.
HARD_STOP before canon conflict resolution without human decision.
```

Note:

`prompt_router` may be useful as an optional or advanced routing artifact when explicit routing logic is being audited. It should not replace the manual routing kernel unless the human explicitly asks for router-level analysis.

---

## 7. Creating an implementation bundle

You can say:

- "Create the patch ZIP."
- "Make an installable bundle."
- "Send code to implement this."
- "Create the install and validation scripts."

AI should request/load:

- `implementation_and_delivery_protocol`
- `bundle_gated_development_workflow`
- `universal_delivery_protocol`
- `patch_registry_validation_freeze`
- active box prompts
- relevant engineering prompt
- source files and evidence needed for the patch

AI should deliver:

- focused patch bundle
- changed file manifest
- backup/rollback logic when needed
- Windows install script
- Windows validation script
- expected validation output
- known risks
- files touched / files not touched

Current terminal behavior canon:

```text
Install script:
- if install succeeds, print result/manifest/backup information, wait 5 seconds, then clear terminal;
- if install fails, do not clear terminal;
- do not use PowerShell finally blocks.

Validation script:
- print all validation output;
- do not clear automatically;
- clear only after the user presses Enter twice;
- if validation fails, leave output visible.
```

Important distinction:

```text
Install success is not validation.
Validation output must be copied back to AI.
AI reviews validation output before classifying the step as validated, repair-needed, failed, or frozen.
```

---

## 8. Freezing / making work official

You can say:

- "Ok freeze."
- "Make this official."
- "Canonize this."
- "Update governance."
- "Validation passed, review and freeze."

AI should request/load:

- `active_governance_freeze_update`
- `evidence_freshness_gate`
- `patch_registry_validation_freeze`
- latest validation output
- latest handoff/status report
- relevant governance/freeze folder card

AI should not freeze if:

- validation is stale
- validation output was not reviewed
- changed files are unknown
- errors remain unexplained
- manual GUI smoke is required but not done
- source evidence does not match generated artifacts
- a canon conflict requires human decision
- warnings are unresolved and not classified

Routine step-freeze rule:

If the user provides complete validation output and all required gates are clean, AI is authorized to freeze that routine implementation step.

Human decision is still required for:

- canon changes
- governance policy changes
- unresolved warning acceptance
- failed gate override
- known-risk exception
- prompt conflict decision
- broad architecture decision

---

## 9. Creating a handoff

You can say:

- "Create a handoff."
- "Write what next AI should know."
- "Summarize what is frozen and what is next."
- "Prepare next session."

AI should request/load:

- `current_workflow_handoff_template`
- latest task history
- current freeze status
- installed patches
- known failures / open questions
- relevant project paths and artifact names

The handoff should include:

- what was done
- what is frozen
- what is not frozen
- next recommended step
- files and paths involved
- validation status
- open risks
- important user preferences/canon decisions
- what prompts should be loaded next time

Expected missing behavior:

```text
STEP_PAUSE if current freeze status or validation status is unknown.
```

---

## 10. Testing the routing box manually

You can say:

- "Test if the routing logic works."
- "Do not solve the task; only classify routing."
- "Run routing test mode."

Use this format:

```text
ROUTING_TEST_MODE

Do not solve the task.
Only classify routing.

For the task below, return:

task_intent:
fast_path_allowed:
required_groups:
optional_groups:
folder_cards_to_load:
specialist_prompts_needed:
minimum_viable_context:
missing_behavior:
should_AI_stop_before_implementation:
NEED_message_to_human:
confidence:

Task:
<task here>
```

A routing test passes if AI:

- does not solve during routing test mode
- classifies the task correctly
- requests only relevant groups/cards/prompts
- uses fast path for simple explanation
- uses `HARD_STOP` before unsafe implementation
- requests validation evidence before freeze
- requests actual related prompt files before final prompt-audit overlap decisions

A routing test fails if AI:

- starts implementation before routing
- asks for all prompts by default
- treats folder cards as full protocols
- freezes without validation evidence
- marks unaudited prompts as active routes
- edits unrelated prompt logic during audit

---

## 11. One-sentence habit

When asking for a task, the cleanest human format is:

```text
Goal: <what I want>
Box: <where it belongs, if known>
Scope: <files allowed / files forbidden>
Evidence: <logs, screenshots, current files>
Validation: <how we know it worked>
```

Example:

```text
Goal: create a new SQLite database folder for prompt metadata.
Box: prompt_library.
Scope: only new database folder and docs, no GUI changes.
Evidence: current prompt library structure uploaded.
Validation: py_compile + catalog loading test + no broken group IDs.
```

If you do not know the box, say:

```text
Box: unknown; AI should classify before action.
```

---

## 12. Minimal daily command

If you want the shortest safe command, say:

```text
Use the KANDA Context Routing Layer manually.
Route my task before doing it.
Tell me required groups, folder cards, specialist prompts, missing behavior, and whether you must stop before implementation.

Task:
<my task>
```
