# Teach AI Tab 9 Prompt Authoring Guide

Version: 1.4.0
Status: active
Category: prompt_library_teaching

## Purpose

Teach an AI how to create or update Tab 9 prompt-library assets safely and completely.

Tab 9 is a read-only prompt engineering library and visual dashboard. It stores project-agnostic prompt text, metadata, groups, stacks, profiles, overlays, pack templates, QA checklists, and release notes.

Tab 9 helps the user find, understand, copy, and assemble prompts to present to an AI. Tab 9 does not execute prompts automatically and does not apply prompt text to the codebase.

## Core Tab 9 Rules

1. Tab 9 is an isolated prompt-library box.
2. Tab 9 prompt assets are text and JSON reference assets.
3. Tab 9 does not edit source code.
4. Tab 9 does not edit active governance.
5. Tab 9 does not change Tabs 1 through 8.
6. Tab 9 does not run prompts automatically.
7. Prompt assets must be project-agnostic by default.
8. Project-specific content must be isolated inside examples or project profiles.
9. Paths inside reusable prompt assets must use placeholders such as <PROJECT_ROOT>.
10. The current physical package path may still be kanda_reasoner_app while kanda_reasoner_app is used as the canonical facade.

## Correct Package-Owned Locations

Use these package-owned locations for prompt-library assets:

```text
kanda_reasoner_app\templates\prompt_library_templates
kanda_reasoner_app\prompt_library
kanda_reasoner_app\prompt_library\active
kanda_reasoner_app\prompt_library\metadata
kanda_reasoner_app\prompt_library\stacks
kanda_reasoner_app\prompt_library\profiles
kanda_reasoner_app\prompt_library\overlays
kanda_reasoner_app\prompt_library\packs
kanda_reasoner_app\prompt_library\qa
kanda_reasoner_app\prompt_library\release
kanda_reasoner_app\prompt_library\groups
kanda_reasoner_app\prompt_library\teaching
```

Do not place Tab 9 prompt-library assets under:

```text
project_freeze_ledger
_project_reference
```

Reason: reference folders are non-source/reference-only areas and may be excluded from project scanning. Tab 9 assets are package-owned prompt-library assets and should remain discoverable by the Tab 9 GUI.

## Prompt Asset Types

### Active prompts

Folder:

```text
kanda_reasoner_app\prompt_library\active
```

Use for reusable prompts that users can copy into a work chat.

### Metadata

Folder:

```text
kanda_reasoner_app\prompt_library\metadata
```

or adjacent to the prompt file as:

```text
<file_stem>.meta.json
```

Metadata powers display name, explanation, grouping, validation expectations, and copy behavior.

### Stacks

Folder:

```text
kanda_reasoner_app\prompt_library\stacks
```

Use for ordered prompt stacks such as daily-start stacks.

### Profiles

Folder:

```text
kanda_reasoner_app\prompt_library\profiles
```

Use for adapting the generic prompt system to a specific project.

### Overlays

Folder:

```text
kanda_reasoner_app\prompt_library\overlays
```

Use for conditional project/domain prompts such as architecture hardening, domain decision tables, UI do-not-regress rules, and Python clean-code rules.

### Packs

Folder:

```text
kanda_reasoner_app\prompt_library\packs
```

Use for export/import templates and prompt pack manifests.

### QA

Folder:

```text
kanda_reasoner_app\prompt_library\qa
```

Use for human-readable review checklists.

### Release

Folder:

```text
kanda_reasoner_app\prompt_library\release
```

Use for state summaries, scope freezes, and release handoffs.

### Groups

Folder:

```text
kanda_reasoner_app\prompt_library\groups
```

Use for dynamic dashboard group definitions in PROMPT_GROUPS.json.

### Teaching

Folder:

```text
kanda_reasoner_app\prompt_library\teaching
```

Use for assets that teach an AI how to create or update prompt-library content.

## Required Prompt Structure

Every reusable prompt should follow this common structure when practical:

```text
1. Prompt Identity
2. Purpose
3. Project-Agnostic Contract
4. Adaptation Variables
5. Trigger Conditions
6. Non-Trigger Conditions
7. Required Inputs
8. Output Contract
9. File Creation Contract
10. Safety Boundaries
11. Validation Requirements
12. User-Facing Help Metadata
13. Prompt Body
14. Example Usage
15. Change Log
```

If a prompt is intentionally simple, keep the headings and write NONE where a section does not apply.

## Project-Agnostic Contract

Reusable prompt-library assets must use placeholders instead of fixed project paths.

Preferred placeholders:

```text
<PROJECT_ROOT>
<PROJECT_NAME>
<PRODUCT_PACKAGE>
<TASK_DESCRIPTION>
<TASK_SLUG>
<GOVERNANCE_FOLDER>
<VALIDATION_COMMANDS>
<OUTPUT_FOLDER>
<SOURCE_FILES>
<LOG_FILES>
```

Do not hardcode one user's project root inside reusable prompt text.

Project-specific examples are allowed only in clearly marked Example sections.

## Complete Prompt Asset Lifecycle

When asked to create or update a prompt, the AI must complete this lifecycle:

1. Inspect the existing prompt library first.
2. Search for related prompts, overlays, stacks, guides, groups, and metadata.
3. Decide create vs update vs link vs no-op.
4. Identify the active box as tab_9_prompt_engineering_text_library.
5. Identify the target folder.
6. Identify whether the asset needs metadata.
7. Identify whether the asset should appear in a Tab 9 group/spinning box.
8. Create or update the .md prompt asset.
9. Create or update the .meta.json sidecar or metadata record.
10. Register the prompt_id in PROMPT_GROUPS.json when dashboard visibility is required.
11. Update only the related prompts that directly route to, teach, load, recommend, or depend on the new or updated prompt.
12. Update PROMPT_LIBRARY_MASTER_INDEX.md, PROMPT_LIBRARY_CURRENT_STATE.md, and PROMPT_LIBRARY_ROADMAP.md when the library state changes.
13. Create a bundle manifest under workbench\bundle_manifest.
14. Deliver a project-relative ZIP with install and validation commands.
15. State that the bundle is not frozen until local validation passes and the user approves freeze.

## Create vs Update vs Link Decision

Use this decision order:

```text
1. Update an existing prompt if it already covers the same purpose but needs better instructions.
2. Link or recommend an existing prompt if it already covers the purpose and no content change is needed.
3. Create a new prompt only when no existing prompt or overlay clearly owns the task.
4. Use no-op when the request is already fully satisfied and no registration/index update is needed.
```

The AI must state this decision before writing files.

## Cross-Prompt Awareness Rules

Cross-prompt awareness means that related prompts know when to recommend, load, or defer to the new or updated prompt.

Update another prompt only when one of these is true:

```text
1. It is the parent methodology prompt for the task.
2. It is the teaching guide for the same asset type.
3. It is the router that decides which prompt group to load.
4. It is an overlay that should be linked rather than duplicated.
5. It is the index/current-state/roadmap that records prompt-library state.
```

Do not update unrelated prompts just because they mention a similar word.

Do not solve discoverability by adding every prompt to Daily Start.

Do not duplicate full rule sets across many prompts. Prefer short references and stable prompt_ids.

## Dashboard Visibility Contract

Tab 9 dashboard group boxes are controlled by:

```text
kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json
```

A prompt is reliably visible in a group when:

```text
PROMPT_GROUPS.json prompt_ids contains the prompt_id
metadata.prompt_id contains the same prompt_id
```

Fallback matching may use display name, file stem, or relative path, but stable prompt_id matching is the preferred contract.

Do not create a new group unless the user explicitly asks for a new visible dashboard group/spinning box.

## Full Bundle Output Contract

A prompt-library bundle should include only project-relative files.

The bundle response must include:

```text
1. Patch summary
2. Download link
3. Complete install script with backup/restore
4. Complete validation script
5. Expected output
6. GUI smoke checklist when group visibility changes
7. Freeze instruction
```

The bundle manifest belongs under:

```text
workbench\bundle_manifest\BUNDLE_MANIFEST_<task_slug>.txt
```

The manifest should include:

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

Prompt-library authoring is text-library work only.

Do not edit:

```text
Python runtime source
GUI code
architecture/workflow validators
active governance files
AI bridge internals
runtime collectors
Tabs 1 through 8
```

unless the user explicitly requests a separate owner box and the AI declares the cross-box gate.

## Validation Requirements

For text-only prompt-library bundles, validate:

```text
PROMPT_GROUPS.json parses as JSON
changed .meta.json files parse as JSON
changed prompt files are UTF-8 text
changed prompt files are ASCII unless the project explicitly allows otherwise
metadata.prompt_id matches group prompt_ids
no duplicate group prompt_ids are introduced
bundle manifest is under workbench\bundle_manifest
workflow validation passes
architecture validation passes
Tab 9 GUI smoke passes when group visibility changed
```

## Example Usage

```text
Create a new prompt that teaches future AIs how to update Tab 9 prompts safely.
```

Expected AI behavior:

```text
1. Inspect existing teaching prompts.
2. Decide whether to update TEACH_AI_TAB9_PROMPT_AUTHORING_GUIDE.md or create a new prompt.
3. Update metadata and group registration.
4. Update related prompt awareness.
5. Update index/current-state/roadmap.
6. Create a bundle manifest under workbench\bundle_manifest.
7. Provide install and validation commands.
```

## Change Log

- v1.4.0: Added complete lifecycle, create/update/link/no-op decision, cross-prompt awareness, dashboard visibility, bundle output, and lowercase workbench\bundle_manifest contract.
- v1.3.0: Added prompt routing requirement for new Tab 9 assets.
- v1.2.0: Added Python Clean Code overlay awareness.
- v1.1.0: Added lifecycle, validation scope, and rollback notes.
- v1.0.0: Initial Tab 9 prompt-authoring teaching guide.
