# Prompt Groups

This folder stores the package compatibility fallback for Prompt Library group definitions.

The current canonical group source is:

```text
kanda_prompt_workspace/prompt_library/GROUPS/PROMPT_GROUPS_DRAFT.json
```

The Prompt Library tab reads the canonical workspace when it is available and falls back to `PROMPT_GROUPS.json` only when the workspace is missing.

A group is a read-only navigation cube. It does not run prompts, edit prompts, change source code, or update governance.

Group catalog rules:

- Keep one cube for every current `ACTIVE_PROMPTS` folder group.
- Use stable `group_id` values matching the canonical folder name.
- Use metadata `prompt_id` values in `prompt_ids`.
- Exclude prompts whose metadata status is deprecated, retired, inactive, archived, or superseded.
- Exclude prompts whose metadata `load_type` is `never`.
- Keep the package fallback catalog synchronized with the canonical group catalog.
- Missing current prompt IDs are discovered from the canonical folder and appended by the GUI loader.
- Stale group IDs are pruned when no current prompt resolves to them.
