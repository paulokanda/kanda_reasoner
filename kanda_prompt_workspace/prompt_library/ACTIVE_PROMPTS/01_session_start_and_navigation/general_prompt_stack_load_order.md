---
audit_id: P001
canonical_id: pyarchitect_general_prompt_stack_load_order
name: PyArchitect General Prompt Stack Load Order
version: 1.1
status: audited_candidate
project_agnostic: true
type: prompt_router
group: core
load_mode: always_on
tokenizer: cl100k_base
description: Project-agnostic prompt router that defines load order, prompt request behavior, precedence, and human-supervised validation workflow.
replaces: []
created_from:
  - 0000 0.1 PYARCHITECT GENERAL PROMPT STACK LOAD ORDER v1.0.md
  - audited useful generic rules from 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
---

# General Prompt Stack Load Order

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Status: Project-agnostic audited candidate  
Use: Send first when starting a PyArchitect session for any software project.

## Purpose

Define which prompt files should be loaded, in which order, which prompt wins when rules conflict, and which specialized prompt should be requested before implementation.

This prompt must not contain hardcoded project facts. Project-specific facts belong in a project overlay.

## Beginning-of-Chat User Warning

As soon as possible at the beginning of a work chat, show this warning to the user before implementation:

```text
WARNING - end-of-chat closure reminder

When you are ready to pause or stop this work session, please state one of these clearly:
- LETS TAKE A BREAK
- LETS STOP NOW

When you say this, I will help you close the session safely by asking for the correct closing materials:
1. If validated work should become official governance, load the current active governance files or governance ZIP.
2. If validated work should become official governance, load the end-of-chat active governance update prompt.
3. Always load or use the workflow handoff prompt to create the final handoff for the next AI/chat.

Governance update is only for validated work with explicit canon/governance approval.
If work is unfinished, uncertain, or only discussed, create a handoff instead so the next AI knows exactly how to continue.
```

Required AI behavior:
- Do not wait until the user forgets to close the session. Show this warning near the start of the chat.
- When the user says LETS TAKE A BREAK or LETS STOP NOW, stop normal implementation flow and start the closing workflow.
- Invite the user to provide active governance files only when validated work may need official governance update.
- Invite the user to provide the governance update prompt only when governance update is appropriate.
- Invite the user to use the workflow handoff prompt every time the chat is ending or pausing.
- Do not create or update governance files for proposals, unfinished work, or unvalidated behavior.

## Project-Agnostic Contract

This prompt must work for any software project. Replace variables before use.

Required variables:

```text
<PROJECT_ROOT>
<PROJECT_NAME>
<PRODUCT_PACKAGE>
<TASK_DESCRIPTION>
<TASK_SLUG>
<GOVERNANCE_FOLDER>
<PROMPT_LIBRARY_FOLDER>
<AUDITED_PROMPT_FOLDER>
<VALIDATION_COMMANDS>
<OUTPUT_FOLDER>
<SOURCE_FILES>
<LOG_FILES>
```

Rules:
- Do not hardcode one project root.
- Do not assume one product package.
- Do not treat examples as active project truth.
- Use current source files, logs, screenshots, validation output, and observed behavior as evidence.
- If evidence is missing, request the exact missing files before implementation.

## Mandatory Load Order

1. general_prompt_stack_load_order.md
2. Current project overlay, if one exists.
3. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL or equivalent delivery prompt.
4. Project startup canon template or active project startup canon.
5. Daily startup loader template or active project daily loader.
6. Current active governance files or governance ZIP, if the project uses governance.
7. Latest workflow handoff output, if any.
8. Current task description.
9. Relevant source ZIP, logs, screenshots, validation output, or observed behavior.

## Special Prompt Routing

Request the professional governance layer for:
- runtime behavior;
- schema changes;
- persistence;
- GUI lifecycle;
- public API changes;
- safety or security risk;
- multi-box work;
- high-risk architecture work.

Request the large module protocol when:
- a relevant Python file is above the project maximum line count;
- the user explicitly opens a large-module refactor;
- the change requires splitting a module or moving responsibilities.

Request the architecture hardening protocol when:
- layer-boundary cleanup is needed;
- duplicate ownership exists;
- stale generated artifacts may affect truth;
- shadow files or deprecated folders may confuse source truth;
- broad architecture warnings must be triaged.

Request the prompt audit protocol when:
- prompt-library files are being audited;
- prompts may be merged, split, deprecated, or rewritten;
- project-specific rules must be separated from agnostic canon;
- a prompt conflict requires human canon decision.

Request the end-of-chat governance update protocol only after:
- validation output was reviewed;
- work is ready for governance update;
- the required governance baseline files are available;
- a human canon/governance decision exists when required.

## Prompt Request Rule

Before implementation, say:

```text
For this task I need these prompt files before implementation:
- <prompt file 1>
- <prompt file 2>
Please upload them or confirm they are already loaded.
```

If a required prompt is missing and the task depends on it, do not implement yet.

## Precedence Order

1. Current user instruction, if safe and explicit.
2. Actual source files, runtime logs, GUI observations, screenshots, and validation output.
3. Current active governance files.
4. Latest workflow handoff.
5. Current project overlay.
6. Project startup canon/profile.
7. Universal delivery protocol for delivery mechanics.
8. Special prompts requested for this task.
9. Older prompts and historical examples.
10. AI memory, lowest priority.

## Human-Supervised Install and Validation Workflow

Install success is not validation.

Validation success is not automatic freeze.

The user may authorize the AI to freeze a routine implementation step after the AI reviews complete clean validation output.

### Install terminal behavior

- The AI provides a Windows CMD or PowerShell install script when the delivery workflow requires it.
- The install script installs or extracts the patch ZIP into the project.
- The install script prints install result, manifest path, backup path, and installed file list when applicable.
- If install succeeds, the install terminal content may be cleaned automatically because install output is not the main validation evidence.
- If install fails, do not clean the terminal. Leave the error visible.

### Validation terminal behavior

- A separate Windows CMD or PowerShell validation script is mandatory after install for code changes.
- The validation script must print all validation output.
- The user must copy the validation output and paste it back to the AI.
- The validation output is audit evidence for validation and freeze decisions.
- The validation script must not clean the terminal before the user has time to copy the output.
- After validation finishes, the validation script may ask the user to press Enter twice before cleaning the terminal.
- If validation fails, do not clean the terminal automatically. Leave the failure visible unless the user confirms cleanup.

### AI step-freeze authority

The AI is authorized to freeze the current routine implementation step only when all of the following are true:

1. The expected validation commands were run.
2. The pasted output is complete enough to audit.
3. All required exit codes are clean.
4. Focused tests passed.
5. Relevant regression tests passed or were explicitly not applicable.
6. Compile or syntax checks passed for touched files.
7. Workflow validation passed when applicable.
8. Architecture validation passed when applicable.
9. Manual GUI validation passed when GUI behavior changed.
10. No new unexplained warning, traceback, import error, failed assertion, or red gate appears.
11. The AI can explain why the result is clean.

If these conditions are met, the AI may state:

```text
Validation reviewed. All required gates passed. This step is frozen.
```

Human approval is still required for:
- canon changes;
- governance updates;
- accepting unresolved warnings;
- overriding failed gates;
- freezing known-risk exceptions;
- resolving prompt conflicts;
- broad architectural direction decisions.

## Prompt Audit Boundary Rule

During prompt audit, audit only the prompt currently under review.

If the audit discovers a rule, feature, command, workflow, paragraph, or implementation instruction that belongs to another prompt, do not edit the other prompt immediately.

Instead, isolate the extracted material into an integration candidate file for later review.

No integration candidate becomes canon automatically.

If the target prompt was already audited or frozen, the candidate requires a later integration pass, version bump, validation, and human approval before entering the target prompt.

## Safety Boundaries

- Do not implement from memory when current source files are needed.
- Do not update governance without the required governance workflow.
- Do not flatten project paths in delivery ZIPs.
- Do not use examples as active source truth.
- Do not silently decide prompt conflicts. Present options and ask the human which option becomes canon.
- Do not merge project-specific facts into project-agnostic prompts.

## How to Use in Another Project

1. Load this prompt first.
2. Load the current project overlay.
3. Resolve project variables from the overlay.
4. Request missing specialized prompts before implementation.
5. Validate all code before step-freeze.
