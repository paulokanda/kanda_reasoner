# Workflow Handoff Template

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.0
Status: Reusable engineering handoff template
Use: Create a continuation note at the end of a work session, break, or unfinished task.

## Purpose

Create a precise, safe, evidence-grounded handoff for the next AI or next work session.


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
<VALIDATION_COMMANDS>
<OUTPUT_FOLDER>
<SOURCE_FILES>
<LOG_FILES>
```

Rules:
- Do not hardcode one project root.
- Do not assume one product package.
- Do not treat examples as active project truth.
- Use current source files, logs, and validation output as evidence.
- If evidence is missing, request it before implementation.

## Handoff Is Not Governance

This handoff is continuity evidence. It does not freeze official governance by itself. Use the governance update protocol only after validated work and explicit freeze approval.


## Bundle-Gated Development Status

When this handoff follows AI-assisted implementation work, include the Kanda
Bundle-Gated Development state:

```text
plan:
bundle:
installed locally:
focused validation:
architecture validation:
workflow validation:
manual validation:
repair or continue decision:
freeze status:
```

Use the rule:

```text
Handoff is continuity evidence only. It is not a freeze.
```

Do not claim baseline acceptance unless the user installed the bundle locally and
reported passing validation.

## Required Sections

- Date
- Project
- Project root
- Handoff type
- Current active box
- Owning paths
- Boxes out of scope
- Current task
- User target outcome
- Completed work
- User-validated work
- Delivered but pending validation
- Discussed but not implemented
- Open bugs
- Known risks
- Do-not-regress behavior
- Files modified or delivered
- Bundles delivered
- Bundle-gated cycle status
- Terminal validation status
- Manual validation status
- Source truth status
- Testing honesty statement
- Next safe step
- Files to request next
- Prompt files to request next

## Final Rule

Do not update canon from this handoff alone.
