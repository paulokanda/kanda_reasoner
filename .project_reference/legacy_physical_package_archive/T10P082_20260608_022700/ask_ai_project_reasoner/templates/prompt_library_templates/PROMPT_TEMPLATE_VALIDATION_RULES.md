# Prompt Template Validation Rules

Version: 1.0.0
Status: Text-only validation rules for Tab 9 prompt-library templates

## Purpose

These rules define how a prompt-library template or prompt metadata file should
be reviewed before it is treated as reusable.

This document is a text-only rulebook. It does not execute validation and does
not modify source code, runtime files, or governance files.

## Severity Levels

- ERROR: The prompt or metadata is not reusable until fixed.
- WARNING: The prompt can be read or copied, but should not be promoted.
- INFO: Helpful note only.

## Structural Rules

T01 ERROR: Markdown template file must be readable as UTF-8 without BOM.

T02 ERROR: Metadata sidecar JSON must parse as valid JSON.

T03 ERROR: schema_version must use semantic versioning.

T04 ERROR: prompt_id must be present and unique inside the prompt library.

T05 ERROR: version in metadata must match the prompt header version.

T06 ERROR: The prompt must contain all required blueprint sections.

T07 ERROR: Prompt body must be non-empty.

T08 WARNING: Change log should contain at least one entry.

T09 ERROR: Trigger conditions section must be present.

T10 ERROR: Non-trigger conditions section must be present.

T11 ERROR: Output contract section must be present.

T12 ERROR: Safety boundaries section must be present.

## Project-Agnostic Rules

A01 ERROR: Reusable prompts must not require one fixed project.

A02 ERROR: Project paths must use <PROJECT_ROOT> or another declared placeholder.

A03 ERROR: Product/package names must use <PRODUCT_PACKAGE> unless inside Example Usage.

A04 ERROR: Task-specific content must use <TASK_DESCRIPTION>.

A05 WARNING: Project-specific examples must be clearly labeled as examples.

A06 ERROR: The prompt must include an Adaptation Variables section.

A07 ERROR: The prompt must include instructions for how to use it in another project.

## File Creation Rules

F01 ERROR: If creates_files is true, files_created must contain at least one path and purpose.

F02 ERROR: Created paths must be project-relative or use <PROJECT_ROOT>.

F03 ERROR: A text-only Tab 9 prompt must not declare source-code patching as its direct action.

F04 ERROR: A text-only Tab 9 prompt must not declare active governance writes as its direct action.

F05 WARNING: Prompt-library output should default to _project_reference when it creates reference artifacts.

## Governance Safety Rules

G01 ERROR: governance_linked prompts must not use edit_policy direct editing.

G02 ERROR: modifies_governance true requires explicit user approval wording.

G03 ERROR: Governance update prompts must not be mixed with source/runtime bundle output.

G04 WARNING: Governance-related prompts should explain the difference between handoff and official canon update.

## Dependency Rules

D01 ERROR: depends_on entries must point to known prompt_id values when a registry exists.

D02 ERROR: required_before entries must point to known prompt_id values when a registry exists.

D03 WARNING: Load-order prompts should define precedence rules.

D04 WARNING: Special-use prompts should define trigger and non-trigger conditions.

## Help Metadata Rules

H01 ERROR: explainer must be present and non-empty.

H02 ERROR: how_it_works must be present and non-empty.

H03 WARNING: risks and mitigations should be paired.

H04 WARNING: safe_usage should explain when the prompt should be copied or presented to an AI.

H05 WARNING: files_created should explain file purpose, not only paths.

## Text-Only Tab 9 Rules

X01 ERROR: Tab 9 templates must not execute code.

X02 ERROR: Tab 9 templates must not patch source files.

X03 ERROR: Tab 9 templates must not change runtime behavior.

X04 ERROR: Tab 9 templates must not update active governance.

X05 ERROR: Tab 9 templates must not modify Tabs 1-8 behavior.

X06 INFO: Tab 9 templates may create or organize prompt text, metadata, schema, archive, and export artifacts.

## Recommended Review Flow

1. Check metadata JSON parses.
2. Check the Markdown file is readable.
3. Check the required sections exist.
4. Check project-agnostic placeholders.
5. Check file creation contract.
6. Check safety boundaries.
7. Check help metadata.
8. Check dependencies if a registry exists.
9. Check change log.
10. Mark as reusable only if no ERROR remains.

## Final Rule

A reusable prompt is not only good wording. It is a documented, project-agnostic,
text-only artifact with clear triggers, limits, file effects, validation rules,
and safe usage instructions.
