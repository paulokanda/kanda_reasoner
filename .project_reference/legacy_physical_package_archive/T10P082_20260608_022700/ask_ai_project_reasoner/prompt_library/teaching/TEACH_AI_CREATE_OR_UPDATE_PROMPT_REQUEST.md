# Teach AI Create Or Update Prompt Request

Version: 1.4.0
Status: active
Category: prompt_library_teaching

## Purpose

Use this as the copyable request when asking an AI to create or update a Tab 9 prompt-library asset.

This prompt is intentionally operational. It tells the AI to complete the whole prompt-library lifecycle, not only draft prompt text.

The full method is defined by:

```text
TEACH_AI_TAB9_PROMPT_AUTHORING_GUIDE.md
TAB9_PROMPT_ASSET_PLACEMENT_RULES.md
KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW.md
```

## Copyable Request

```text
You are updating the Tab 9 Prompt Engineering Library for <PROJECT_NAME>.

Task:
<TASK_DESCRIPTION>

Use the surgical prompt-library authoring model.

Mandatory pre-flight:
1. Inspect existing prompt-library assets before creating anything.
2. Check whether an existing prompt, overlay, stack, guide, group, or router entry already covers the request.
3. Decide whether the correct action is create, update, link, or no-op.
4. State the target folder and whether the prompt should appear in an existing Tab 9 group.
5. State which related prompts genuinely need awareness of the new or updated prompt.
6. State validation checks before creating the bundle.
7. State safety boundaries.

Mandatory lifecycle:
1. Create or update the prompt .md file.
2. Create or update the matching .meta.json file.
3. Ensure metadata.prompt_id is stable and matches any PROMPT_GROUPS.json reference.
4. Register the prompt_id in kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json when the prompt belongs in a Tab 9 dashboard group.
5. Do not create a new group unless I explicitly ask for a new visible Tab 9 group/spinning box.
6. Update related prompts only when they directly route to, teach, load, recommend, or depend on the new or updated prompt.
7. Update PROMPT_LIBRARY_MASTER_INDEX.md, PROMPT_LIBRARY_CURRENT_STATE.md, and PROMPT_LIBRARY_ROADMAP.md when the library state changes.
8. Create a bundle manifest under workbench\bundle_manifest.
9. Deliver a project-relative ZIP.
10. Provide complete install and validation commands.

Safety boundaries:
- Tab 9 prompt-library authoring is text-library work only.
- Do not edit Python source, GUI code, runtime collectors, AI bridge internals, validators, active governance, or Tabs 1 through 8 unless I explicitly request a separate code/governance gate.
- Do not place prompt-library assets under .project_reference or _project_reference.
- Do not hardcode one local project root in reusable prompts.
- Use placeholders such as <PROJECT_ROOT>, <PROJECT_NAME>, <PRODUCT_PACKAGE>, <TASK_DESCRIPTION>, and <TASK_SLUG>.
- Keep project-specific examples under clearly marked Example sections.
- If the request involves Python code generation or refactor, link or recommend python_clean_code_overlay instead of duplicating its rules.

Before implementation, show:
1. existing prompt assets inspected;
2. create/update/link/no-op decision;
3. target folder;
4. files to create or update;
5. group membership, if any;
6. related prompts that must be made aware, if any;
7. validation plan;
8. safety boundaries.

Then create the ZIP with only the required prompt-library text/JSON assets.
```

## Minimum Validation

The implementation response should include validation commands for:

```text
PROMPT_GROUPS.json JSON parse
metadata JSON parse for changed .meta.json files
prompt_id resolution for every changed group entry
ASCII / UTF-8 sanity for changed prompt assets
workflow validation
architecture validation
Tab 9 GUI smoke if group visibility changed
```

## Change Log

- v1.4.0: Added complete lifecycle checklist, lowercase workbench\bundle_manifest path, and strict text-only boundaries.
- v1.3.0: Added routing preflight for created or updated prompts.
- v1.2.0: Added Python Clean Code overlay awareness.
- v1.1.0: Added lean pre-flight, create/update/link decision, bundle-gated delivery reference, and related-prompt awareness requirement.
- v1.0.0: Initial copyable AI request for Tab 9 prompt creation or update.
