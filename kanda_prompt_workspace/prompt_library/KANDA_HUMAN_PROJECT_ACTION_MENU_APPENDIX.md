# KANDA Human Project Action Menu Appendix

Purpose: this file is a human-facing helper. It tells the human partner what kinds of project actions can be requested from AI, how to phrase them, and what prompt stack or project evidence should usually be provided.

This is not an active AI behavior canon. It is a reading/reference appendix for the human.

---

## Core rule

You do not need to know the exact technical prompt name. You can speak naturally. The AI should route your request to the correct prompt stack.

However, when a task is risky, architectural, cross-box, data-related, or intended to become official, you should expect AI to ask for the correct supporting prompts/files before implementing.

---

## 1. Starting the day / starting a new session

You can say:

- "Start the day."
- "We will continue KANDA Reasoner."
- "Load the project working context."
- "Continue from the latest handoff."

Useful files/prompts to provide:

- `session_start_upload_checklist`
- `daily_session_start_prompt`
- `daily_reasoner_startup_loader`
- `reasoner_startup_canon`
- latest workflow handoff
- latest validation/freeze status
- project tree or relevant file list if implementation will happen

AI should establish:

- current task
- active box
- current baseline/freeze status
- whether work is planning, audit, implementation, validation, or handoff
- what prompt stack is missing before action

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
3. `box_architecture_canon`
4. `folder_organization_canon`
5. `python_database_design_optimisation`
6. `python_validation_serialisation_type_safety`
7. `python_security_threat_prevention`
8. `implementation_roadmap_builder`
9. `bundle_gated_development_workflow`

You should be ready to provide:

- intended folder path
- database type: SQLite, JSON, CSV, PostgreSQL, etc.
- owner box
- files allowed to change
- files explicitly out of scope
- validation command or expected manual test
- whether this is prototype, production, or reference-only

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
- allowed extraction locations
- public API that cannot change
- tests/validation commands
- maximum safe scope for one patch

---

## 4. Fixing bugs or validation errors

You can say:

- "Fix this error."
- "Tab 1 failed."
- "Tab 2 validator fails."
- "This patch broke something."

AI should request/load:

- relevant validation logs
- `bundle_gated_development_workflow`
- `evidence_freshness_gate`
- `patch_registry_validation_freeze`
- relevant domain prompt based on the error type

You should provide:

- exact error message/log
- file where failure occurred
- command run
- expected behavior
- what changed immediately before failure

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

AI should preserve:

- existing callbacks
- existing object names used by logic
- worker paths
- validation flow
- hidden state variables

---

## 6. Creating or updating prompts

You can say:

- "Create a new prompt."
- "Generalize this prompt from another project."
- "Audit these prompts."
- "Rename prompts to intuitive names."
- "Update the navigation index."

AI should request/load:

- `prompt_audit_canon`
- `project_specific_prompt_generalization`
- `prompt_canon_reconciliation_protocol`
- `prompt_navigation_index`
- `prompt_router`
- target prompt folder
- source prompt files

AI should classify each prompt as:

- active
- optional
- reference-only
- deprecated
- duplicate
- needs generalization

---

## 7. Creating an implementation bundle

You can say:

- "Create the patch ZIP."
- "Make an installable bundle."
- "Send code to implement this."

AI should request/load:

- `implementation_and_delivery_protocol`
- `bundle_gated_development_workflow`
- `universal_delivery_protocol`
- `patch_registry_validation_freeze`
- active box prompts
- relevant engineering prompt

AI should deliver:

- focused patch bundle
- backup/rollback logic
- install script without terminal-clearing commands
- validation commands
- changed file manifest
- known risks

---

## 8. Freezing / making work official

You can say:

- "Ok freeze."
- "Make this official."
- "Canonize this."
- "Update governance."

AI should request/load:

- `active_governance_freeze_update`
- `evidence_freshness_gate`
- `patch_registry_validation_freeze`
- latest validation output
- latest handoff/status report

AI should not freeze if:

- validation is stale
- changed files are unknown
- errors remain unexplained
- manual GUI smoke is required but not done
- source evidence does not match generated artifacts

---

## 9. Creating a handoff

You can say:

- "Create a handoff."
- "Write what next AI should know."
- "Summarize what is frozen and what is next."

AI should request/load:

- `current_workflow_handoff_template`
- latest task history
- current freeze status
- installed patches
- known failures / open questions

The handoff should include:

- what was done
- what is frozen
- what is not frozen
- next recommended step
- files and paths involved
- validation status

---

## 10. One-sentence habit

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
