# UI COMPONENT DO-NOT-REGRESS OVERLAY TEMPLATE

Version: 1.0.0
Status: Template
Use: Copy this overlay when a project needs frozen UI component behavior preserved during GUI work.

## Prompt Identity

Prompt name: <PROJECT_NAME> UI Component Do-Not-Regress Overlay
Prompt type: conditional domain overlay
Project: <PROJECT_NAME>
Project root: <PROJECT_ROOT>
UI framework: <GUI_FRAMEWORK>
Component family: <UI_COMPONENT_FAMILY>

## Purpose

Use this overlay to preserve a resolved UI component behavior while allowing focused maintenance.

It is for components such as dropdowns, panels, grids, editors, toolbars, windows, or navigation controls.

## Project-Agnostic Contract

This overlay must not assume a specific GUI framework.

Use:

- <GUI_FRAMEWORK> for the UI toolkit;
- <UI_COMPONENT_FAMILY> for the component group;
- <CANONICAL_UI_HELPERS> for owner helpers;
- <PROJECT_ROOT> for project root.

## Adaptation Variables

<PROJECT_ROOT> =
<PROJECT_NAME> =
<GUI_FRAMEWORK> =
<UI_COMPONENT_FAMILY> =
<CANONICAL_UI_HELPERS> =
<TASK_DESCRIPTION> =
<VALIDATION_COMMANDS> =

## Trigger Conditions

Use this overlay when the task touches:

- component sizing;
- component state hydration;
- focus behavior;
- popup behavior;
- layout regression;
- scroll behavior;
- caption or label rendering;
- visual do-not-regress rules.

## Non-Trigger Conditions

Do not use this overlay for:

- non-GUI source changes;
- signal, data, or domain math;
- governance updates;
- broad style redesign without user approval.

## Required Inputs

Ask for:

- relevant UI source files;
- screenshots or GUI observations;
- expected behavior;
- current wrong behavior;
- validation commands or launch command;
- current prompt stack and delivery protocol.

## Output Contract

The AI must produce:

- current component owner;
- frozen behavior to preserve;
- regression risks;
- minimal patch plan;
- manual GUI validation checklist.

## File Creation Contract

This overlay creates no files by itself.

## Safety Boundaries

Do not:

- solve visual bugs by changing domain logic;
- patch unrelated UI systems;
- rebuild persistent widgets unnecessarily;
- steal focus from active editors;
- introduce fixed sizes where responsive layout is required;
- declare GUI validation complete without user-run GUI checks unless actually run.

## Validation Requirements

Minimum:

- compile touched UI files;
- import smoke if safe;
- manual GUI checklist;
- screenshot comparison when available.

## User-Facing Help Metadata

Explain: UI do-not-regress overlay for preserving resolved GUI behavior.
How it works: Defines canonical component behavior, forbidden regressions, and manual GUI checks.
Files created: None by this overlay.
Safe usage: Use only for GUI component tasks.

## Prompt Body

Act as a GUI component regression auditor.

Identify whether the requested change affects layout, state hydration, focus, sizing, or rendering. Preserve the current frozen component contract unless the user explicitly asks to redesign it.

Before implementation, produce a manual GUI checklist that can prove the regression is fixed and the frozen behavior is preserved.

## Example Usage

Task: Fix a dropdown width regression without changing unrelated panel layout.
Adapt <UI_COMPONENT_FAMILY> to dropdowns and list the canonical sizing helper.

## Change Log

- v1.0.0: Initial UI component do-not-regress overlay template.
