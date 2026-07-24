# Prompt Library Compatibility Assets

Status: read-only compatibility and teaching assets
Scope: package fallback for the Prompt Library tab

The current canonical prompt source is:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS
```

The current canonical group registry is:

```text
kanda_prompt_workspace/prompt_library/GROUPS/PROMPT_GROUPS_DRAFT.json
```

The Prompt Library tab reads those workspace owners when available. This package folder remains a compatibility fallback and stores teaching, profiles, overlays, checklists, release notes, and fallback group definitions.

The tab is read-only. It may inspect, group, preview, copy, and open prompt files. It must not execute prompts, edit source code, mutate active governance, write Error Memory, or write Freeze memory.

Current catalog policy:

- one cube per current `ACTIVE_PROMPTS` folder group;
- current prompt identity comes from metadata and canonical source;
- deprecated, retired, inactive, archived, superseded, and `load_type=never` prompts are hidden;
- package fallback groups mirror the canonical group registry;
- prompts remain project-agnostic unless explicitly classified otherwise.
