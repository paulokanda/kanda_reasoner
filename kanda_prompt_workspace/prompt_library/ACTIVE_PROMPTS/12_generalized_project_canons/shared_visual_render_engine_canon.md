# Shared Visual Render Engine Canon

Version: 1.0
Status: Active special prompt candidate
Use: Load when multiple GUI tools render the same conceptual object, scene, chart, graph, map, table, or preview and must remain visually consistent without sharing business logic.


## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


## Generalization Rule

This prompt was generalized from EEG/KANDA project materials. Do not copy EEG-specific nouns, paths, labels, channel names, montage rules, electrode coordinates, or clinical assumptions into KANDA Reasoner unless the current project explicitly needs them. Preserve only the transferable engineering pattern.


## Purpose

Generalize the source project's shared-render-engine canon. The reusable pattern is: one shared scene/model/theme/rendering contract, many controllers.

## Rule

If two tools display the same conceptual object, they must share a rendering engine or rendering contract. They may layer different interactions on top, but they must not fork the visual model.

## Separation

The shared visual engine owns:

- scene model;
- geometry/layout model;
- theme/style model;
- rendering contract;
- visual modes;
- export/render helpers.

The tool/controller owns:

- business workflow;
- user actions;
- current selection;
- validation rules;
- data meaning;
- persistence decisions.

## Freeze Rule

When changing a shared visual engine, do not change business logic unless explicitly scoped. Visual polish must not silently alter selection semantics, event semantics, data meaning, saved definitions, or runtime state.

## Visual Mode Pattern

A visual engine may expose modes such as:

- simple/native mode;
- premium/polished mode;
- diagnostic/debug mode;
- export/report mode.

A visual-mode toggle must change rendering only, not business truth.

## Validation Checklist

- Both consuming tools still render the same object consistently.
- Selection/click behavior remains unchanged unless explicitly scoped.
- Controller-to-renderer contract is stable.
- Renderer does not import private controller internals.
- Visual-mode toggle does not mutate domain state.
- The shared renderer has focused tests or snapshot/golden checks where possible.
