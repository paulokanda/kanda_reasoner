# PROMPT TEMPLATE BLUEPRINT

Version: 1.0.0
Status: Project-agnostic reusable prompt blueprint
Box: tab_9_prompt_engineering_text_library
Use: Create structured prompts that can be stored in Tab 9 and reused for any project.

## 1. Prompt Identity

Prompt name:
- <PROMPT_NAME>

Prompt ID:
- <PROMPT_ID>

Version:
- <PROMPT_VERSION>

Status:
- template | active | draft | archived | deprecated

Category:
- <PROMPT_CATEGORY>

Load type:
- always | always_first | on_request | conditional | special_use

## 2. Purpose

Describe what this prompt is for in plain language.

Required:
- What problem the prompt solves.
- When the user should use it.
- Who should use it.
- Whether it is daily, special-use, refactor-only, governance-only, handoff-only, or template-only.

## 3. Project-Agnostic Contract

This prompt must work across projects.

Required:
- Use <PROJECT_ROOT> instead of absolute paths.
- Use <PROJECT_NAME> instead of a fixed project name.
- Use <PRODUCT_PACKAGE> instead of a fixed package name.
- Use <TASK_DESCRIPTION> for the user task.
- Use <GOVERNANCE_FOLDER> as a configurable variable.
- Place project-specific examples only under the Example Usage section.
- Do not require one fixed repository unless the prompt is explicitly marked example-only.

## 4. Adaptation Variables

Before using this prompt, define these variables:

<PROJECT_ROOT> =
<PROJECT_NAME> =
<PRODUCT_PACKAGE> =
<GOVERNANCE_FOLDER> =
<VALIDATION_COMMANDS> =
<TASK_DESCRIPTION> =
<TASK_SLUG> =
<OUTPUT_FOLDER> =
<SOURCE_FILES> =
<LOG_FILES> =

## 5. Trigger Conditions

Use this prompt when:

- <TRIGGER_CONDITION_1>
- <TRIGGER_CONDITION_2>

## 6. Non-Trigger Conditions

Do not use this prompt when:

- <NON_TRIGGER_CONDITION_1>
- <NON_TRIGGER_CONDITION_2>

## 7. Required Inputs

Before using this prompt, collect:

- Current task description.
- Current source files or source ZIP when implementation depends on source truth.
- Runtime logs, validation output, screenshots, or observations when relevant.
- Current governance or project profile files when the task depends on frozen rules.
- Any special domain prompt required by the task.

## 8. Output Contract

This prompt may produce:

- Roadmap text.
- Audit text.
- Handoff text.
- Prompt text.
- Prompt stack text.
- File plan.
- Validation plan.
- A project-relative ZIP only when the prompt explicitly allows file creation.

The output must state whether it is a proposal, a draft, a validated result, or an official freeze candidate.

## 9. File Creation Contract

State whether this prompt creates or modifies files.

If it creates files, define:

- Folder.
- File names.
- Whether paths are project-relative.
- Whether files are source, runtime, governance, reference, prompt, or draft artifacts.
- Whether files are safe to overwrite.
- Whether validation is required before promotion.

Default safe folder for prompt-library artifacts:

<PROJECT_ROOT>\<PRODUCT_PACKAGE>\prompt_library\

## 10. Safety Boundaries

This prompt must not:

- Silently edit source code.
- Silently update active governance.
- Hardcode one project root.
- Rewrite source from memory.
- Weaken tests or validation gates.
- Promote proposals into frozen canon.
- Touch unrelated boxes.
- Claim exhaustive testing without evidence.

## 11. Validation Requirements

Before treating this prompt as ready, check:

- Required sections are present.
- Metadata sidecar exists.
- Version in metadata matches this prompt header.
- Project paths use placeholders.
- File creation contract is explicit.
- Safety boundaries are explicit.
- Dependencies are declared.
- Prompt is UTF-8 without BOM.
- Prompt is readable as plain text.

## 12. User-Facing Help Metadata

This section powers Tab 9 help buttons.

### Explain

<PLAIN_LANGUAGE_EXPLANATION>

### How It Works

<STEP_BY_STEP_BEHAVIOR>

### Files Created

<FILES_CREATED_AND_PURPOSES>

### Risks

<RISKS>

### Mitigations

<MITIGATIONS>

### Safe Usage

<SAFE_USAGE>

### Copy Label

<COPY_BUTTON_LABEL>

### Edit Policy

read_only | draft_only | manual_only

### Promotion Policy

none | manual_only | validate_then_explicit_approve

## 13. Prompt Body

Write the actual prompt text here.

Rules:
- Use clear sections.
- Keep project-specific examples separate from generic instructions.
- Use <PROJECT_ROOT> and other variables instead of fixed paths.
- Tell the AI when to stop, ask for files, create a roadmap, validate, or deliver.

## 14. Example Usage

Example usage is optional.

If examples include project-specific names or paths, mark them as examples only
and do not make them required behavior.

## 15. Change Log

- 1.0.0: Initial prompt created from the Tab 9 project-agnostic blueprint.
