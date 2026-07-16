# Prompt Library Templates

Status: Text-only template foundation
Box: tab_9_prompt_engineering_text_library
Scope: Project-agnostic prompt storage and retrieval

## Purpose

This folder stores reusable prompt-library templates for Tab 9.

Tab 9 is an isolated text-only box. It helps the user store, organize,
explain, validate, copy, and export project-agnostic prompts that can be
presented to any AI for any project.

Tab 9 does not change source code. Tab 9 does not change runtime behavior.
Tab 9 does not edit active governance. Tab 9 does not touch Tabs 1-8.

## Folder role

This folder is for template definitions only:

- PROMPT_TEMPLATE_BLUEPRINT.md defines the reusable structure used by all prompts.
- PROMPT_TEMPLATE_BLUEPRINT.meta.json describes the blueprint as a prompt-library item.
- PROMPT_METADATA_SCHEMA.json defines the required metadata contract.
- PROMPT_TEMPLATE_VALIDATION_RULES.md defines text-only validation rules.

Actual user prompts may later live under:

<PROJECT_ROOT>\<PRODUCT_PACKAGE>\prompt_library\

## Project-agnostic rule

Templates in this folder must work for any project. They must use placeholders
instead of fixed project paths or package names.

Required placeholders include:

- <PROJECT_ROOT>
- <PROJECT_NAME>
- <PRODUCT_PACKAGE>
- <TASK_DESCRIPTION>
- <TASK_SLUG>
- <GOVERNANCE_FOLDER>
- <VALIDATION_COMMANDS>
- <OUTPUT_FOLDER>
- <SOURCE_FILES>
- <LOG_FILES>

Project-specific examples are allowed only inside an Example Usage section and
must be clearly labeled as examples.

## Allowed content

Allowed:

- Markdown templates
- Text templates
- JSON metadata
- JSON schema files
- Readme files

Forbidden in this text-only foundation:

- Python code
- Runtime scripts
- Source patchers
- Governance writers
- Automatic prompt runners
- AI bridge integration

## Safe use

Use this folder to create or inspect reusable prompt structures. Do not treat it
as active project source. Do not use it to update official governance files.

## Change log

- 1.0.0: Initial text-only Tab 9 prompt-library template foundation.
