# LARGE MODULE OVERLAY PROFILE TEMPLATE

Version: 1.0.0
Status: Template
Use: Copy this overlay when a project needs staged large-module audit or helper decomposition guidance.

## Prompt Identity

Prompt name: <PROJECT_NAME> Large Module Overlay Profile
Prompt type: conditional domain overlay
Project: <PROJECT_NAME>
Project root: <PROJECT_ROOT>
Target module: <TARGET_MODULE>

## Purpose

Use this overlay to adapt the general large-module refactor protocol to a specific project without hardcoding that project into the protocol.

## Project-Agnostic Contract

This overlay must keep project values in adaptation variables.

Use:

- <TARGET_MODULE> for the file being audited;
- <HELPER_FOLDER> for proposed helper location;
- <PUBLIC_API_EXPECTATIONS> for public symbols that must remain stable;
- <VALIDATION_COMMANDS> for project checks.

## Adaptation Variables

<PROJECT_ROOT> =
<PROJECT_NAME> =
<TARGET_MODULE> =
<HELPER_FOLDER> =
<PUBLIC_API_EXPECTATIONS> =
<VALIDATION_COMMANDS> =
<TASK_DESCRIPTION> =

## Trigger Conditions

Use this overlay when:

- a file is above the project's line limit;
- helper split is requested;
- a refactor is intentionally opened;
- the file is approaching the line limit and will grow;
- public API preservation is required during decomposition.

## Non-Trigger Conditions

Do not use this overlay for:

- simple one-line fixes;
- documentation-only edits;
- prompt-library text-only changes;
- governance-only updates.

## Required Inputs

Ask for:

- current target module content;
- current line count;
- public symbol expectations;
- import paths;
- relevant tests;
- desired refactor goal.

## Output Contract

The AI must follow staged gates:

1. audit only;
2. roadmap only;
3. implementation only after approval.

## File Creation Contract

This overlay creates no files by itself.

Implementation later may create helper files, but only after approval through the large-module protocol.

## Safety Boundaries

Do not:

- split without approval;
- change public API accidentally;
- create catch-all helper files;
- mix unrelated behavior changes into refactor;
- claim behavior validation from compile-only checks.

## Validation Requirements

At minimum:

- compile touched files;
- import smoke for public entry point;
- focused tests when available;
- line-count report;
- public API preservation check.

## User-Facing Help Metadata

Explain: Project overlay for adapting large-module refactor protocol.
How it works: Defines target module, public API expectations, helper folder, and project validation commands.
Files created: None by this overlay.
Safe usage: Use with the large-module protocol only after current source is available.

## Prompt Body

Act as a large-module refactor auditor.

Do not implement immediately. Produce Task 0 audit first, including line count, public symbols, responsibilities, risks, available tests, missing evidence, and candidate helper boundaries.

Stop for user approval before roadmap or implementation.

## Example Usage

Task: Split <TARGET_MODULE> into <HELPER_FOLDER> while preserving <PUBLIC_API_EXPECTATIONS>.

## Change Log

- v1.0.0: Initial large module overlay profile template.
