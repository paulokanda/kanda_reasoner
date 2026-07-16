# Prompt Library Master Index

Version: 1.0.2
Status: active
Scope: Kanda Reasoner prompt-library assets

## Purpose

This index describes the Tab 9 Prompt Engineering Library and the current package-owned prompt assets.

Tab 9 is a prompt storage and retrieval library. It helps the user find, understand, copy, and assemble prompts to present to an AI.

Tab 9 is not a code editor, runtime controller, governance editor, or automatic AI prompt runner.

## Current Physical Locations

Prompt-library assets currently live under:

```text
kanda_reasoner_app\prompt_library\
```

The canonical package facade is:

```text
kanda_reasoner_app
```

The physical implementation package has not yet been renamed from kanda_reasoner_app.

## Main Prompt Library Folders

```text
active\
metadata\
stacks\
profiles\
overlays\
packs\
qa\
release\
groups\
teaching\
```

## Non-Source Reference Folders

Do not place package-owned Tab 9 prompt assets under:

```text
.project_reference\
_project_reference\
```

These folders are reference-only/non-source boundaries.

## Generated Workbench Folder

Prompt-library bundle manifests now belong under:

```text
workbench\bundle_manifest\
```

## Installed Text Bundles

### T9T001 - Template foundation

Created the reusable prompt-template foundation.

### T9T002 - Prompt library structure

Created package-owned prompt-library folders and README files.

### T9T003 - General project prompt pack

Created reusable project-agnostic prompts and metadata.

### T9T004 - Package relocation

Moved prompt assets from reference-only folders into package-owned folders.

### T9T005 - Project profile templates

Created project-profile templates and adaptation-variable templates.

### T9T006 - Domain overlay templates

Created reusable overlay templates for domain-specific special prompts.

### T9T007 - Prompt pack export/import templates

Created prompt-pack, export, import, validation-report, and release-note templates.

### T9T008 - Master index

Created this master index, current-state note, roadmap, and quick start files.

### T9T012 - Kanda Bundle-Gated Development Workflow

Path:

```text
kanda_reasoner_app\prompt_library\active\KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW.md
```

Purpose:

```text
Parent methodology for plan -> bundle -> install -> validate -> repair/continue -> freeze.
```

### T9T013 - Teach AI Prompt Authoring Complete Lifecycle

Updated Teach AI Prompt Authoring so future AIs do the complete prompt-library lifecycle when asked to create or update a prompt.

Core lifecycle:

```text
inspect existing prompts
choose create vs update vs link vs no-op
edit prompt .md and metadata
register in PROMPT_GROUPS.json when needed
update related prompt awareness only when directly relevant
update index/current-state/roadmap when state changes
create bundle manifest under workbench\bundle_manifest
provide install and validation commands
respect text-only boundaries
```

Key files:

```text
kanda_reasoner_app\prompt_library\teaching\TEACH_AI_CREATE_OR_UPDATE_PROMPT_REQUEST.md
kanda_reasoner_app\prompt_library\teaching\TEACH_AI_TAB9_PROMPT_AUTHORING_GUIDE.md
kanda_reasoner_app\prompt_library\teaching\TAB9_PROMPT_ASSET_PLACEMENT_RULES.md
kanda_reasoner_app\prompt_library\groups\PROMPT_GROUPS.json
```

## Main User Flow

1. Choose a project profile.
2. Choose a prompt or prompt stack.
3. Review Explain, How It Works, and Files Created metadata.
4. Replace adaptation variables.
5. Copy the prompt or stack.
6. Paste it into an AI session.
7. Use bundle-gated delivery and local validation for implementation work.

## Safety Rules

1. Tab 9 text assets may be edited as text.
2. Tab 9 must not change Python source files by itself.
3. Tab 9 must not update active governance files.
4. Tab 9 must not modify Tabs 1 through 8 behavior.
5. Tab 9 prompts must be project-agnostic by default.
6. Reusable prompts should use placeholders such as <PROJECT_ROOT> and <PROJECT_NAME>.
7. No prompt should require one fixed project unless it is explicitly marked project-specific.
