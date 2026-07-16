# Tab 9 Prompt Asset Placement Rules

Version: 1.3.0
Status: active
Category: prompt_library_teaching

## Purpose

Define where prompt-library assets belong when an AI creates or updates Tab 9 content.

## Correct Locations

Template foundation:

```text
kanda_reasoner_app\templates\prompt_library_templates
```

Prompt library assets:

```text
kanda_reasoner_app\prompt_library
```

Common subfolders:

```text
active
metadata
stacks
profiles
overlays
packs
qa
release
groups
teaching
```

Bundle manifests for prompt-library bundles:

```text
workbench\bundle_manifest
```

## Incorrect Locations

Do not use these for Tab 9 package-owned prompt assets:

```text
.project_reference
_project_reference
```

Do not use this legacy bundle-manifest folder for new bundles:

```text
workbench\_bundle_temp
workbench\BUNDLE_MANIFEST
```

## Group Box Updates

Dashboard group boxes are controlled by:

```text
kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json
```

Add a new group only when the user asks for a new visible dashboard box.

Add a prompt_id to an existing group when the prompt belongs to an existing dashboard box.

## Prompt Router Contract

Each new prompt-library asset must define how it is routed.

Routing can be any one of these:

```text
listed in PROMPT_GROUPS.json
recommended by KANDA_PROMPT_ROUTER.md
referenced by a parent methodology prompt
referenced by an authoring guide
included in a named prompt stack
marked archive/reference-only in metadata
```

If none apply, the prompt is marooned and should not be considered complete.

Do not solve marooning by adding every prompt to Daily Start. Use the router to recommend specialized groups only when needed.

## Dashboard Visibility Contract

Tab 9 dashboard group boxes are controlled by:

```text
kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json
```

A prompt appears under a dashboard group only if the group prompt_id can be matched by at least one stable prompt-library identifier.

Reliable matching should use:

```text
metadata.prompt_id
```

Acceptable fallback identifiers include:

```text
display_name
file stem
relative path
```

Rules:

1. metadata.prompt_id should match the value placed in PROMPT_GROUPS.json.
2. If a prompt is created but not added to a group, it may exist in the library but not appear in the dashboard group.
3. Do not create a new dashboard group unless the user asks for a new visible group/spinning box.
4. Do not add a prompt to unrelated groups only to make it visible.
5. Prefer one primary group and optional router references over broad duplication.

## Bundle Manifest Placement Contract

Every installable prompt-library bundle should include a bundle manifest under:

```text
workbench\bundle_manifest\BUNDLE_MANIFEST_<task_slug>.txt
```

The manifest is a generated workbench artifact. It is not a prompt asset and should not live inside the prompt_library tree.

The manifest should identify:

```text
bundle_id
active_box
bundle_type
changed_files
forbidden_files
validation_commands
rollback_notes
freeze_status
```

## Safety Boundaries

Prompt asset placement rules do not authorize source-code changes.

Do not modify:

```text
Python runtime source
GUI source
architecture/workflow validators
active governance files
AI bridge internals
runtime collectors
Tabs 1 through 8
```

unless the user explicitly requests a separate code/governance gate.

## Change Log

- v1.3.0: Added lowercase workbench\bundle_manifest contract and stricter dashboard visibility rules.
- v1.2.0: Added prompt router contract for Tab 9 assets.
- v1.1.0: Added dashboard visibility contract and prompt_id matching rules.
- v1.0.0: Initial placement rules for Tab 9 prompt-library assets.
