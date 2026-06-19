# Architecture Hardening Triage Template

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
Status: Reusable architecture-hardening protocol
Use: Load for architecture hardening, warning cleanup, shadow conflicts, layer-boundary safety, or state-safety campaigns.

## Purpose

Audit, classify, triage, and safely harden architecture without broad rewrites or unrelated source edits.


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

## Core Workflow

```text
audit -> classify -> add or tune checkers if needed -> triage findings -> separate hard failures from transitional debt -> patch smallest owner box -> validate -> wait for user validation -> freeze or handoff
```

## Finding Classes

Hard failure: must be fixed before gate can pass.
Transitional debt: real issue that cannot be safely fixed in this pass.
Warning or observation: worth tracking but not blocking.

## Hardening Targets

- public facade and symbol ownership safety
- layer-boundary safety
- runtime state and lifecycle safety
- duplicate normalizer and responsibility overlap safety
- non-canonical folder contamination
- stale generated artifact handling

## Allowlist Rule

Allowlist only transitional debt. Do not weaken checker rules globally. New unallowlisted findings must remain visible.

## Final Rule

Hardening is not rewriting. Patch one risk class at a time and preserve working behavior.
