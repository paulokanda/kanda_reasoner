# Project-Specific Prompt Generalization

Version: 1.0
Status: Active prompt-library candidate
Use: Load when importing prompts, canons, handoffs, roadmaps, or domain rules from another project into KANDA Reasoner.


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

Convert useful project-specific canon into reusable KANDA Reasoner prompt assets without contaminating the prompt stack with another project's domain assumptions.

## Core Rule

A source canon from another project is not inserted directly. It must pass through four gates:

1. **Extract the engineering pattern.** Identify the reusable architecture idea, validation discipline, UI-state rule, pipeline invariant, packaging rule, or workflow law.
2. **Remove project-specific payload.** Strip fixed project roots, domain names, clinical labels, source-file names, hard-coded UI labels, coordinates, and any data model that belongs only to the source project.
3. **Rename into project-agnostic language.** Replace domain words with generic owner-box terms such as source truth, canonical working base, derived runtime product, control-state registry, resolver, plugin package, visual render engine, and decision table.
4. **Route it in KANDA Reasoner.** Mark whether it becomes an active prompt, optional special prompt, reference-only file, deprecated source, or index candidate.

## Import Decision Table

| Source material type | Action | Example generalized output |
|---|---|---|
| Domain-specific clinical/math rule | Reference-only unless KANDA Reasoner needs that domain | Keep as source inventory only |
| Architecture invariant | Generalize and add prompt | immutable source -> derived product |
| GUI/dropdown/control-state safety | Generalize and add prompt | control-state do-not-regress canon |
| Plugin package format | Generalize and add prompt | extension package import canon |
| Visual rendering contract | Generalize and add prompt | shared render engine canon |
| Prompt stack/load order from old project | Use only as router idea; do not replace active KANDA Reasoner stack | update router addendum |
| Handoff from old project | Extract unresolved risks only; do not make canon | report/reference only |

## Contamination Checks

Reject or quarantine imported text if it contains:

- hard-coded source project root;
- domain labels not used by KANDA Reasoner;
- coordinate tables or clinical identities;
- instructions that override KANDA Reasoner governance;
- statements like "frozen" that were frozen only in the source project;
- source project folder names as active truth;
- unverified claims that implementation already exists in KANDA Reasoner.

## Required Output When Generalizing

Every batch generalization should output:

- source inventory;
- accepted generalized ideas;
- rejected/reference-only ideas;
- updated prompt files;
- new prompt files;
- index-update candidate;
- sandbox review/self-check;
- install/extract command that preserves terminal logs.

<!-- T9T013_KANDA_DEPRECATED_ROOT_GUARD_START -->

## T9T013 Deprecated Root Regression Guard

When generalizing prompt-library work, never preserve obsolete local roots as active truth.

For this workspace, prompt assets are expected under:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/
kanda_prompt_workspace/prompt_library/METADATA/
```

If a handoff, roadmap, install block, validation block, or generated bundle refers to an unrelated project root as the active project root, classify that as a regression unless the user explicitly says they are working in that project.

Generalize path rules into owner boxes and active workspace-relative paths. Do not turn deprecated local paths into active instructions.

<!-- T9T013_KANDA_DEPRECATED_ROOT_GUARD_END -->

