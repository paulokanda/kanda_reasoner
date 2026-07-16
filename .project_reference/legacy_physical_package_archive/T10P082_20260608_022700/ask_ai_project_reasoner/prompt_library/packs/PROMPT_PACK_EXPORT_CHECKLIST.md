# Prompt Pack Export Checklist

Use this checklist before exporting a prompt pack from Tab 9 or from the prompt library folder.

## 1. Pack Identity

- Pack ID: <PROMPT_PACK_ID>
- Display name: <PROMPT_PACK_DISPLAY_NAME>
- Version: <VERSION>
- Status: draft | reviewed | released | archived
- Intended target projects: any project | <PROJECT_TYPE>

## 2. Required Files

Confirm the pack contains:

- Prompt markdown files.
- Matching .meta.json sidecars.
- PROMPT_PACK_MANIFEST.json.
- Optional stack worksheet.
- Optional validation report.
- Optional release notes.

## 3. Project-Agnostic Check

Confirm:

- No hardcoded absolute Windows paths.
- No hardcoded Unix paths.
- No fixed project root.
- No fixed product package unless inside examples.
- <PROJECT_ROOT> is used for project paths.
- <PROJECT_NAME> is used for project names.
- <PRODUCT_PACKAGE> is used for package names.
- <TASK_DESCRIPTION> is used for user task text.

## 4. Metadata Check

For every prompt:

- prompt_id is present.
- display_name is present.
- version is present.
- project_agnostic is true unless intentionally project-specific.
- safe_to_copy is true or a reason is documented.
- edit_policy is defined.
- validation_requirements are defined.
- files_created is present when creates_files is true.

## 5. Governance Safety Check

Confirm:

- The pack does not update active governance.
- The pack does not include accepted_warning_baseline.json unless it is a governance-only pack.
- The pack does not contain source-code patches.
- The pack does not include runtime artifacts.
- Governance-linked prompts are clearly marked as draft-only or read-only.

## 6. Export Decision

Export only when:

- All required files are present.
- All metadata parses.
- Hardcoded path scan is clean or warnings are explicitly accepted.
- The user understands the pack is prompt text, not an automatic code change.

## 7. Export Output

Suggested export name:

<PROMPT_PACK_ID>_v<VERSION>.zip

Suggested output folder:

<PROJECT_ROOT>sk_ai_project_reasoner\prompt_library\exports