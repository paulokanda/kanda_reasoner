# PROJECT PROFILE TEMPLATE

Version: 1.0.0
Status: Text-only project profile template
Use: Copy this file when adapting the general prompt library to a specific project.

## 1. Purpose

This template describes one project profile for the Prompt Engineering Library.

A project profile explains how reusable project-agnostic prompts should be adapted
for a specific codebase without hardcoding that codebase into the prompt library.

This file is text-only. It does not change source code, runtime behavior,
active governance, or any other tab.

## 2. Project Identity

Project name:
- <PROJECT_NAME>

Project root:
- <PROJECT_ROOT>

Product package or main source folder:
- <PRODUCT_PACKAGE>

Primary runtime entry point, if any:
- <RUNTIME_ENTRY_POINT>

Primary validation commands:
- <VALIDATION_COMMANDS>

## 3. Project-Agnostic Contract

This profile must preserve the reusable prompt library.

Rules:
- Keep prompts reusable by default.
- Use placeholders instead of hardcoded paths.
- Put project-specific facts in this profile, not inside generic prompt bodies.
- Do not turn this profile into source code.
- Do not use this profile to edit active governance.
- Do not let this profile change Tabs 1 through 8 behavior.

## 4. Adaptation Variables

Define these variables before using a prompt stack with this project.

<PROJECT_NAME> =
<PROJECT_ROOT> =
<PRODUCT_PACKAGE> =
<SOURCE_ROOTS> =
<NON_CANONICAL_FOLDERS> =
<GOVERNANCE_FOLDER> =
<VALIDATION_COMMANDS> =
<RUNTIME_ENTRY_POINT> =
<TASK_DESCRIPTION> =
<TASK_SLUG> =
<OUTPUT_FOLDER> =

## 5. Source Scope

Canonical source folders:
- <SOURCE_ROOTS>

Non-canonical folders:
- <NON_CANONICAL_FOLDERS>

Generated or reference folders:
- <REFERENCE_OR_GENERATED_FOLDERS>

Rule:
- The prompt library may store text references, but project source truth comes from
  current source files, runtime logs, validation output, and explicit user instructions.

## 6. Prompt Stack Profile

Daily prompt stack for this project:
1. <PROMPT_ID_LOAD_ORDER>
2. <PROMPT_ID_DELIVERY_PROTOCOL>
3. <PROMPT_ID_PROJECT_STARTUP_CANON>
4. <PROMPT_ID_DAILY_LOADER>
5. <ACTIVE_GOVERNANCE_FILES_OR_ZIP>
6. <LATEST_HANDOFF>
7. <CURRENT_TASK_DESCRIPTION>
8. <RELEVANT_SOURCE_ZIP_LOGS_OR_VALIDATION>

Special prompts:
- <SPECIAL_PROMPT_ID>: use when <TRIGGER_CONDITION>.

## 7. Domain Safety Rules

Project-specific domain safety rules:
- <DOMAIN_SAFETY_RULE_1>
- <DOMAIN_SAFETY_RULE_2>

If the project has no special domain safety rules, write NONE.

## 8. Box Map

Known boxes for this project:

| Box name | Owner path | Responsibility | Forbidden responsibilities |
|---|---|---|---|
| <BOX_NAME> | <OWNER_PATH> | <RESPONSIBILITY> | <FORBIDDEN_RESPONSIBILITIES> |

Rule:
- Patch the owner box, not the symptom.

## 9. Governance Handling

Governance folder:
- <GOVERNANCE_FOLDER>

Governance file set:
- <GOVERNANCE_FILE_1>
- <GOVERNANCE_FILE_2>
- <GOVERNANCE_FILE_3>
- <GOVERNANCE_FILE_4>
- <GOVERNANCE_FILE_5>

Rules:
- This profile does not update governance.
- Governance changes require explicit user approval and the project governance workflow.
- If the project uses a five-file governance model, preserve accepted warning baseline files.

## 10. Validation Commands

Use project-specific validation commands here.

```powershell
cd <PROJECT_ROOT>
<VALIDATION_COMMANDS>
```

## 11. How to Use This Profile

1. Copy this template into a project-specific profile file.
2. Replace placeholders with project facts.
3. Keep project facts in the profile, not in reusable prompts.
4. Select the prompt stack profile for the project.
5. Copy the generated prompt stack to the AI session.
6. Treat current source files and logs as higher truth than profile text.

## 12. Change Log

- v1.0.0: Initial text-only project profile template.
