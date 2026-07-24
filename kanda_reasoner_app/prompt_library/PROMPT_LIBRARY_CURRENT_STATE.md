# Prompt Library Current State

Version: 1.0.2
Status: active
Scope: Kanda Reasoner Prompt Library

## Current Project Context

Current KANDA Tool root:

```text
E:\kanda_reasoner
```

Current canonical Prompt Library source:

```text
kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS
```

Current canonical group registry:

```text
kanda_prompt_workspace\prompt_library\GROUPS\PROMPT_GROUPS_DRAFT.json
```

Package compatibility fallback:

```text
kanda_reasoner_app\prompt_library
```

The Prompt Library tab must prefer the canonical workspace, create one cube for each current active folder group, and hide deprecated or retired prompt identities. The package folder remains a read-only compatibility and teaching facade.

## Current Non-Source Reference Folder

Canonical reference-only folder:

```text
project_freeze_ledger
```

Legacy reference-only folder:

```text
_project_reference
```

Neither folder is part of the project source tree. Do not place Tab 9 prompt-library assets there.

## Current Generated Workbench Folder

Canonical bundle-manifest folder:

```text
workbench\bundle_manifest
```

Do not create new bundle manifests under:

```text
workbench\_bundle_temp
workbench\BUNDLE_MANIFEST
workbench\bundle_manifest
_project_reference\BUNDLE_MANIFEST
```

## Current Methodology Parent Prompt

The prompt library includes:

```text
kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\05_patch_delivery_and_validation\bundle_gated_development_workflow.md
```

This prompt formalizes the implementation cycle:

```text
plan -> bundle -> install -> validate -> repair/continue -> freeze
```

Use it as the parent protocol for implementation, refactor, repair, handoff, prompt-library authoring, and governance-freeze work.

## Current Teach AI Prompt Authoring Lifecycle

Teach AI Prompt Authoring now requires future AIs to perform the complete prompt-library job when asked to create or update a prompt:

```text
inspect existing prompt assets
choose create vs update vs link vs no-op
create or update the prompt .md
create or update metadata
register dashboard group prompt_id when needed
update related prompt awareness only when directly relevant
update master index/current state/roadmap when state changes
create bundle manifest under workbench\bundle_manifest
provide install and validation commands
avoid source/governance/runtime changes unless explicitly requested
```

The relevant files are:

```text
kanda_reasoner_app\prompt_library\teaching\TEACH_AI_CREATE_OR_UPDATE_PROMPT_REQUEST.md
kanda_reasoner_app\prompt_library\teaching\TEACH_AI_TAB9_PROMPT_AUTHORING_GUIDE.md
kanda_reasoner_app\prompt_library\teaching\TAB9_PROMPT_ASSET_PLACEMENT_RULES.md
kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json
```

## Current Tab 9 Group Registration

The Teach AI Prompt Authoring group contains:

```text
teach_ai_tab9_prompt_authoring_guide
teach_ai_create_or_update_prompt_request
tab9_prompt_asset_placement_rules
bundle_gated_development_workflow
```

## Current Recommended Next Step

After T9T013 validation and freeze, the next safe prompt-library step is to create or update a project profile instance for the renamed project root:

```text
kanda_reasoner_app\prompt_library\profiles\kanda_reasoner\
```

This should remain a text-only Tab 9 bundle unless the user explicitly requests code or GUI changes.

## Manual Checks

Run these checks from PowerShell after replacing <PROJECT_ROOT> with the project root:

```text
Test-Path "<PROJECT_ROOT>\kanda_reasoner_app\prompt_library\PROMPT_LIBRARY_MASTER_INDEX.md"
Test-Path "<PROJECT_ROOT>\kanda_reasoner_app\prompt_library\PROMPT_LIBRARY_ROADMAP.md"
Test-Path "<PROJECT_ROOT>\kanda_reasoner_app\prompt_library\PROMPT_LIBRARY_CURRENT_STATE.md"
Test-Path "<PROJECT_ROOT>\workbench\bundle_manifest"
```

Expected result for each check:

```text
True
```
