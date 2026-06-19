---
audit_id: P002_OVERLAY
canonical_id: project_overlay_selector
name: Project Overlay - Reasoner
version: 1.0
status: audited_candidate
project_agnostic: false
type: project_overlay
group: project_overlay
load_mode: stack
requires:
  - general_prompt_stack_load_order.md
description: Project-specific overlay that resolves variables and Reasoner-specific prompt routing without contaminating the project-agnostic parent prompt.
created_from:
  - 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
---

# Project Overlay Selector

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Status: Project-specific audited candidate  
Use: Load after the project-agnostic prompt router when working on Kanda Reasoner / Project Reasoner.

## Purpose

Resolve project-specific values for Kanda Reasoner / Project Reasoner while keeping the general PyArchitect prompt router project-agnostic.

This overlay contains project facts. Do not merge this file into the project-agnostic load-order prompt.

## Current Project Identity

Project name:

```text
Kanda Reasoner / Project Reasoner
```

Current user-specified project root for this audit installation:

```text
E:\kanda_reasoner
```

Product package:

```text
E:\kanda_reasoner\kanda_reasoner_app
```

Prompt library source folder:

```text
E:\kanda_reasoner\kanda_reasoner_app\prompt_library
```

Audited prompt destination folder:

```text
E:\kanda_reasoner\project_freeze_ledger\KANDA_PROMPTS_AUDITED
```

Important note:
Older Reasoner prompts may mention <PROJECT_ROOT>. Treat that path as historical unless current user instruction, current source files, or current project evidence confirms it.

## Reasoner Daily Load Order

When working on Kanda Reasoner / Project Reasoner, load this order unless the human gives a narrower task:

1. general_prompt_stack_load_order.md
2. project_overlay_selector.md
3. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL or current equivalent.
4. Project startup canon or current Reasoner startup canon.
5. Daily startup loader or current Reasoner daily loader.
6. Current active governance files or governance ZIP, if needed for the task.
7. Latest workflow handoff output, if available.
8. Current task description.
9. Relevant source ZIP, logs, screenshots, validation output, or observed behavior.

## Reasoner Special Prompt Routing

Request the professional engineering governance layer when the task affects:

- architecture;
- schema;
- retrieval;
- prompt construction;
- AI bridge;
- runtime behavior;
- GUI lifecycle;
- persistence;
- multi-box work;
- public APIs.

Request the large module refactor protocol when:

- a relevant Python file is above the project line limit;
- the user opens a large-module refactor;
- a module must be split by responsibility.

Request the problem set roadmap solver when:

- the user gives multiple problems;
- the user asks for the best solving order;
- several problems may need bundling or separation.

Request the architecture hardening triage protocol when the task involves:

- layer-boundary cleanup;
- public facade ownership;
- duplicate public symbols;
- duplicate normalizers;
- project-root hardcoding;
- stale generated artifacts;
- prompt/retrieval/AI-bridge ownership drift.

Request the governance update prompt only when:

- work was validated;
- the relevant output was reviewed;
- official active governance must be updated;
- the required governance baseline files are available.

## Reasoner Prompt Audit Rule

When auditing Reasoner prompts:

1. Preserve raw prompt files until replacements are created.
2. Split project-specific facts into this overlay or a newer overlay.
3. Keep reusable engineering rules inside project-agnostic prompts.
4. Move misplaced rules into integration candidates.
5. Deprecate the old project-specific prompt only after replacements are validated.
6. Do not silently delete useful content.

## Reasoner Delivery Preference

For implementation bundles:

- ZIP files should preserve final project-relative paths.
- ZIP files should be saved by the user at the drive root used for this project when practical.
- Use Windows CMD or PowerShell install code when installation/extraction supervision is needed.
- Use separate validation terminal code after install.
- The user pastes validation output back to the AI.
- The AI may freeze a routine implementation step after reviewing complete clean validation output.

## Current Audited Prompt Installation Target

For the current prompt audit bundle, install into:

```text
E:\kanda_reasoner\project_freeze_ledger\KANDA_PROMPTS_AUDITED
```

This folder is an audited prompt destination. It is not the live prompt library unless the human later promotes it.

## Project-Specific Safety Boundaries

- Do not treat old <PROJECT_ROOT> paths as current active root unless the human confirms.
- Do not edit the live prompt library just because audited prompts exist.
- Do not update governance from this overlay alone.
- Do not promote audited prompt candidates into active canon without validation and the correct prompt/governance workflow.
