# Prompt Pack Import Checklist

Use this checklist before importing a prompt pack into another project.

## 1. Import Context

- Target project root: <PROJECT_ROOT>
- Target project name: <PROJECT_NAME>
- Product package: <PRODUCT_PACKAGE>
- Import purpose: <TASK_DESCRIPTION>

## 2. Pack Inspection

Before copying files, inspect:

- PROMPT_PACK_MANIFEST.json.
- Prompt markdown files.
- .meta.json sidecars.
- Stack files.
- Release notes.
- Validation report.

## 3. Safety Checks

Reject or quarantine the pack if:

- It contains Python source patches.
- It writes active governance unexpectedly.
- It contains hardcoded source project paths outside examples.
- It contains runtime artifacts.
- Prompt metadata is missing for active prompts.
- The pack manifest is absent.

## 4. Placeholder Substitution

Before using imported prompts, define:

- <PROJECT_ROOT> =
- <PROJECT_NAME> =
- <PRODUCT_PACKAGE> =
- <GOVERNANCE_FOLDER> =
- <VALIDATION_COMMANDS> =
- <TASK_DESCRIPTION> =

Do not globally replace placeholders inside the library copy unless you intentionally create a project-specific draft.

## 5. Import Target

Recommended import target:

<PROJECT_ROOT>sk_ai_project_reasoner\prompt_library\imports\<PROMPT_PACK_ID>
Imported packs should be reviewed before copying prompts into active.

## 6. Activation Policy

A prompt imported from another project should become active only after:

- Metadata parses.
- Project-agnostic check passes.
- Required placeholders are documented.
- The user reviews the prompt.
- The prompt is copied or promoted manually.

## 7. Final Import Note

Importing a prompt pack does not execute prompts and does not change source code. It only makes prompt text available for the user to inspect, copy, and present to an AI.
