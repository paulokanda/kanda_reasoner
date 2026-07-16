# Project-Agnostic Prompt Review Checklist

Version: 1.0.0
Status: Text-only manual project-agnostic review checklist
Use: Confirm that prompts can be reused across projects.

## Purpose

This checklist verifies that a prompt can be adapted to any project through
explicit variables and does not depend on one fixed repository.

## Required Adaptation Variables

Confirm the prompt defines or supports:

- [ ] <PROJECT_ROOT>
- [ ] <PROJECT_NAME>
- [ ] <PRODUCT_PACKAGE>
- [ ] <TASK_DESCRIPTION>
- [ ] <TASK_SLUG>
- [ ] <SOURCE_FILES>
- [ ] <LOG_FILES>
- [ ] <VALIDATION_COMMANDS>
- [ ] <OUTPUT_FOLDER>
- [ ] <GOVERNANCE_FOLDER> when governance is relevant.

## Hardcoded Path Checks

- [ ] No absolute Windows path appears outside examples.
- [ ] No Unix absolute path appears outside examples.
- [ ] No fixed project name appears in an instruction section.
- [ ] No fixed package name appears in an instruction section.
- [ ] Examples are clearly labeled as examples.
- [ ] Examples do not become required behavior.

## Generalization Checks

- [ ] Domain-specific terms are isolated in an overlay or example.
- [ ] Project-specific safety rules are variables or profile fields.
- [ ] Validation commands are placeholders or templates.
- [ ] Governance folder is configurable.
- [ ] Prompt does not assume a GUI unless declared.
- [ ] Prompt does not assume Python unless declared.
- [ ] Prompt does not assume a single operating system unless declared.

## AI Use Checks

- [ ] The prompt tells the AI what to ask before implementation.
- [ ] The prompt tells the AI to avoid stale or missing evidence.
- [ ] The prompt has a safe stop condition.
- [ ] The prompt separates proposals from frozen decisions.
- [ ] The prompt does not claim runtime facts without evidence.

## Result

- [ ] PASS - Project-agnostic.
- [ ] FAIL - Project-specific content must be converted.
- [ ] PARTIAL - Use only as a project-specific prompt.

## Notes

<PROJECT_AGNOSTIC_REVIEW_NOTES>
