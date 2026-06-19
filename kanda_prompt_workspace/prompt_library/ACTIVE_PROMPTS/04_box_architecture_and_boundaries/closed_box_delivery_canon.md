# Closed-Box Delivery Canon

Version: 1.0
Status: Active prompt-library candidate
Use: Load when a feature has multiple subdomains, UI controls, runtime outputs, generated artifacts, or competing ownership risks.


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


## Core Analogy

Each feature box is an isolated ingredient box. One box delivers peas. Another delivers oranges. Another delivers cocoa. A box may consume another box's public product, but it must not open another box and start mixing its internals.

## Rule

Every box must deliver one final product through an explicit public contract. It must not own another box's state, mutate another box's truth, or duplicate another box's resolver logic.

## Required Box Declaration

Before implementation, declare:

- box name;
- final product delivered;
- owner paths;
- public API / interface;
- allowed dependencies;
- forbidden dependencies;
- state owned by this box;
- state not owned by this box;
- validation gate for this box;
- cross-box contracts consumed or produced.

## Closed-Box Anti-Patterns

Do not allow:

- UI boxes owning domain truth;
- runtime boxes owning dropdown state;
- validators mutating production outputs;
- duplicate resolvers in two feature boxes;
- helper modules importing private internals of sibling boxes;
- source-truth objects being mutated by derived-product boxes;
- two boxes producing the same final product without an owner decision.

## Cross-Box Touch Rule

A cross-box edit is allowed only if:

1. another box blocks the current box from working;
2. another box invades the current box;
3. the current box invades another box and must be repaired;
4. shared canonical infrastructure must be updated.

When this happens, the patch must declare both boxes and validate both.
