---
audit_id: A028
audit_decision: UPDATE
audit_classification: QUICK_START_REFERENCE
audit_batch: prompt_audit_chunk_003
review_status: sandbox_checked
---

> Audit note: This file was reviewed in batch mode. The content below is the real updated file for this audit decision.

# Daily Session Start Prompt

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.1
Status: Updated quick-start checklist
Use: Human-facing reminder for what to upload at the start of a Project Reasoner / PyArchitect work chat.

## Daily minimum prompt stack

Send these at the beginning of a new Reasoner work chat:

1. `0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md`
2. `universal_delivery_protocol.md`
3. `reasoner_startup_canon.md`
4. `daily_reasoner_startup_loader.md`
5. Active governance ZIP or the five active governance files:
   - `_project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.md`
   - `_project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.json`
   - `_project_reference\ACTIVE_PROJECT_ GOVERNANCE\check_reasoner_project_canon.py`
   - `_project_reference\ACTIVE_PROJECT_ GOVERNANCE\test_reasoner_project_canon.py`
   - `_project_reference\ACTIVE_PROJECT_ GOVERNANCE\accepted_warning_baseline.json`
6. Latest `0000 6.0` handoff output from the previous session.
7. Current task description.
8. Relevant source ZIP, logs, validation output, screenshots, or error text.

## Special prompts to send only when needed

### High-risk architecture, schema, runtime, GUI, retrieval, prompt, or multi-box work

Send:

`reasoner_professional_engineering_governance.md`

Use when the task touches schema, collector output, index loader, retrieval, prompt builder, AI bridge, runtime collector, GUI lifecycle, thread/process behavior, project-root logic, or cross-box boundaries.

### Large module or refactor work

Send:

`large_module_refactor_protocol.md`

Use when a Python file is above 500 lines, approaching 500 lines and expected to grow, needs helper-folder split, may require source-preserving facade split, or must preserve public API during refactor.

### Architecture hardening / warning cleanup campaign

Send:

`architecture_hardening_triage_protocol.md`

Use for public facade warnings, `__init__.py` cleanup, layer-boundary violations, box-boundary violations, duplicate normalizers, session-state writes, project-root hardcoding, shadow paths, or architecture warning cleanup.

### Several problems at once

Send:

`problem_set_roadmap_solver.md`

Use when you paste several warnings, errors, or problems and want the AI to prioritize them.

### End of day / break / unfinished work

Use:

`current_workflow_handoff_template.md`

Purpose: create the next-chat handoff. This is an engineering shift note, not official governance.

### Official governance/canon update

Send only after a validated freeze:

`active_governance_freeze_update.md`

Purpose: update the official five active governance files. Do not use it for normal work, proposals, or unfinished tasks.

## AI behavior expected

The loaded stack should make the AI state which additional prompt files are needed before implementation. Example:

```text
For this task, I need these prompt files before implementation:
1. reasoner_professional_engineering_governance.md
2. large_module_refactor_protocol.md
Please upload them or confirm they are already loaded.
```

## Quick examples

- Large module warning -> request `large_module_refactor_protocol.md`.
- Retrieval / prompt / schema / GUI lifecycle change -> request `reasoner_professional_engineering_governance.md`.
- Official governance update after validation -> request `active_governance_freeze_update.md`.
- Work ending or being handed off -> use `current_workflow_handoff_template.md`.
## AI Prompt Request Canon Requirement

At the start of the session and before any non-trivial project action, load or enforce i_prompt_request_canon.

The AI must classify the user's request and, when the needed prompt stack or project evidence is missing, ask the human for the correct prompts/files before implementation, refactor, prompt-library modification, architecture change, database/storage work, validation, freeze, or handoff.

For example, if the human says "we will start creating a new folder with a databank," the AI must recognize a new architecture/data-storage task and request the relevant prompt stack: session start, AI prompt request canon, Box Logic, folder organization, database design, validation/type safety, security, implementation roadmap, and bundle-gated workflow.

