# PROJECT PROFILE USAGE GUIDE

Version: 1.0.0
Status: Text-only guide
Use: Explain how project profiles work in the prompt library.

## Purpose

Project profiles adapt the general prompt library to a specific project without
changing the reusable prompts themselves.

The profile is a text and JSON reference layer. It helps the user assemble a
prompt stack to present to an AI. It does not execute prompts automatically.

## Files

PROJECT_PROFILE_TEMPLATE.md
- Human-readable template for one project profile.

PROJECT_PROFILE_TEMPLATE.meta.json
- Metadata describing the project profile template.

PROJECT_ADAPTATION_VARIABLES_TEMPLATE.json
- Machine-readable placeholder values for one project.

PROJECT_PROMPT_STACK_PROFILE_TEMPLATE.json
- Machine-readable prompt stack selection and routing profile.

## Workflow

1. Copy PROJECT_PROFILE_TEMPLATE.md.
2. Rename the copy for the project.
3. Fill in project identity, source scope, validation commands, and special rules.
4. Copy PROJECT_ADAPTATION_VARIABLES_TEMPLATE.json.
5. Fill in project variables.
6. Copy PROJECT_PROMPT_STACK_PROFILE_TEMPLATE.json.
7. Select which prompt IDs belong to the project stack.
8. Use the stack profile to copy prompts to an AI session.

## Boundaries

Allowed:
- Store project-specific prompt variables.
- Store prompt stack selections.
- Store text guidance for how to use prompts in a project.

Forbidden:
- Do not change source code.
- Do not change runtime behavior.
- Do not edit active governance.
- Do not modify Tabs 1 through 8.
- Do not treat profile text as higher truth than current source files or logs.

## Final Rule

Profiles adapt prompts to a project. They do not make code changes.
