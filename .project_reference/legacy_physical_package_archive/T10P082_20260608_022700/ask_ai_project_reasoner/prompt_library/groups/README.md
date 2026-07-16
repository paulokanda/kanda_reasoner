# Prompt Groups

This folder stores read-only group definitions for the Prompt Engineering Library dashboard.

The main catalog is `PROMPT_GROUPS.json`.

A group is a friendly navigation box in Tab 9. It does not run prompts, edit prompts, change source code, or update governance. It only defines which existing prompt-library text files should be shown together in a filtered floating library window.

Group catalog rules:

- Use stable `group_id` values.
- Use metadata `prompt_id` values in `prompt_ids` whenever possible.
- Keep groups project-agnostic.
- Do not include absolute project paths.
- Missing prompt IDs should be treated as non-fatal warnings by GUI code.
