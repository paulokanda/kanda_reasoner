# Stateful Control Regression Canon

Version: 1.0
Status: Active special prompt candidate
Use: Load when working on dropdowns, comboboxes, option panels, captions, persisted selections, control hydration, sizing, option registries, or UI state regressions.


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

Generalize the EEG dropdown canon into a project-agnostic rule for any stateful UI control: controls must have one sizing policy, one state owner, one hydration source, and one renderer/adapter contract.

## Canonical Control-State Rule

A dropdown/control must separate:

- option registry;
- selected value;
- user-visible caption;
- internal stable identifier;
- sizing/rendering policy;
- hydration/loading logic;
- runtime effect triggered by selection.

Do not let one widget own all of these.

## Single Sizing Authority

For any repeated control family, there must be one canonical sizing helper. Wrappers may call it, but must not create competing width/height calculators.

Sizing must consider:

- visible caption text;
- popup option text;
- placeholder text;
- formatted adapter text;
- longest possible loaded state;
- compact/expanded layout mode.

## Stable Identifier Rule

Never use display text as the only truth if the option has domain or workflow meaning. Use:

```text
stable_id -> display_label -> adapter_caption -> runtime_payload
```

## Hydration Rule

Control options must be hydrated from the owning registry or state model. A random GUI module must not hand-build the same option list.

## Do-Not-Regress Checklist

Before freezing a control-state patch, test:

- initial load;
- reload/refresh;
- saved preference restore;
- missing old selection fallback;
- long label sizing;
- placeholder behavior;
- manual selection behavior;
- disabled/unavailable option behavior;
- stable_id preserved even if visible caption changes;
- no duplicate option ownership.

## Forbidden Patterns

- multiple independent dropdown-width calculators;
- display label used as persistent ID;
- GUI control directly mutates data truth;
- hard-coded option list duplicated across boxes;
- reset on refresh without clear reason;
- stale selection silently mapped to wrong option;
- UI caption adapter changing runtime meaning.
