# Prompt Pack Templates

Purpose:
This folder stores text-only templates for exporting, importing, validating, and assembling prompt packs.

Scope:
- These files are part of the Tab 9 prompt-library text assets.
- They help users package prompts for reuse across projects.
- They do not execute prompts.
- They do not change source code.
- They do not update active governance.
- They do not modify Tabs 1 through 8.

Core rule:
Prompt packs must remain project-agnostic by default. Use placeholders such as <PROJECT_ROOT>, <PROJECT_NAME>, <PRODUCT_PACKAGE>, and <TASK_DESCRIPTION> instead of hardcoded project paths or fixed project names.

Recommended pack contents:
1. Prompt markdown files.
2. Matching .meta.json sidecar files.
3. A prompt pack manifest.
4. Optional stack assembly worksheet.
5. Optional validation report.
6. Optional release notes.

Install note:
These are templates only. Copy a template to a project-specific prompt pack folder and fill in the placeholders before export.
