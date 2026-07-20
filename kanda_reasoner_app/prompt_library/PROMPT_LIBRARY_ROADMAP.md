# Prompt Library Roadmap

Version: 1.0.2
Status: active text-only roadmap
Scope: Tab 9 Prompt Engineering Library

## Purpose

This roadmap defines the safe evolution of the text-only Prompt Library without letting it become a source-code editor, runtime controller, governance bypass, or automatic prompt runner.

## Frozen Scope

Tab 9 is an isolated text-library box.

It stores and organizes project-agnostic prompts for the user to copy and present to an AI.

Tab 9 does not change project source code, runtime behavior, active governance, or Tabs 1 through 8.

## Current Naming State

```text
Project root: E:\kanda_reasoner
Canonical package facade: kanda_reasoner_app
Current physical prompt-library path: kanda_reasoner_app\prompt_library
Canonical reference-only folder: project_freeze_ledger
Canonical bundle-manifest folder: workbench\bundle_manifest
```

## Completed Steps

### T9T001 - Template foundation

Status: installed.

### T9T002 - Prompt library structure

Status: installed.

### T9T003 - General project prompt pack

Status: installed.

### T9T004 - Package relocation

Status: installed and validated.

### T9T005 - Project profile templates

Status: installed.

### T9T006 - Domain overlay templates

Status: installed.

### T9T007 - Prompt pack export/import templates

Status: installed.

### T9T008 - Master index

Status: installed.

### T9T012 - Kanda Bundle-Gated Development Workflow

Status: installed.

Creates the named parent methodology prompt for:

```text
plan -> bundle -> install -> validate -> repair/continue -> freeze
```

### T9T013 - Teach AI Prompt Authoring Complete Lifecycle

Status: historical application entry; current owner is KPR-05-002.

Updates Teach AI Prompt Authoring so future AIs do the complete prompt-library job when asked to create or update a prompt.

Adds:

```text
existing asset inspection
create vs update vs link vs no-op decision
complete prompt asset lifecycle
cross-prompt awareness rules with negative examples
dashboard visibility contract
bundle manifest minimum fields
workbench\bundle_manifest output path
PowerShell validation expectations
text-only safety boundaries
```

Registers `bundle_gated_development_workflow` in:

```text
teach_ai_prompt_authoring
```

The prompt also remains available through high-risk engineering workflows where already registered.

## Next Text-Only Steps

### T9T009 - First Kanda Reasoner project profile instance

Create a project profile instance under:

```text
kanda_reasoner_app\prompt_library\profiles\kanda_reasoner\
```

Expected files:

```text
PROJECT_PROFILE.md
PROJECT_ADAPTATION_VARIABLES.json
PROJECT_PROMPT_STACK_PROFILE.json
README.md
```

No Python, no GUI, no governance changes.

### T9T010 - Prompt stack examples

Create example prompt stacks for common workflows:

1. General source patch.
2. Complex roadmap-first task.
3. Large-module refactor.
4. Architecture-hardening audit.
5. Governance update request.

No Python, no GUI, no governance changes.

### T9T011 - Prompt-library usage guide

Create a plain-language usage guide:

1. How to select a prompt.
2. How to adapt placeholders.
3. How to copy a stack.
4. How to avoid hardcoded project paths.
5. How to archive deprecated prompts.

No Python, no GUI, no governance changes.

## Future Optional Code Steps

These require explicit approval later.

### T9C001 - Headless text validator

A small Python validator could check prompt metadata, required sections, ASCII, UTF-8, group resolution, and hardcoded path rules.

This is not part of the current text-only phase.

### T9G001 - Read-only GUI viewer improvements

A future GUI phase could improve display, filtering, and copy behavior for the text library.

It must be read-only by default and must not edit code or governance.

## Never-Do List

Do not add automatic source patching to Tab 9.
Do not add active governance editing to Tab 9.
Do not make Tab 9 load prompts into Tabs 1 through 8 automatically.
Do not hardcode one project root into reusable prompts.
Do not treat examples as universal rules.
