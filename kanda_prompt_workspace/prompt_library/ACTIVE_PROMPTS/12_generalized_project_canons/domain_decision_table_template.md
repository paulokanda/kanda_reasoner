# Domain Decision Table Template

Version: 1.0
Status: Active prompt-library candidate
Use: Load when a project has domain decisions, label normalization, role classification, manual overrides, contradiction handling, or user-visible uncertainty notices.


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

Generalize the EEG decision-table canon into a project-agnostic pattern for any domain where labels, roles, metadata, or inferred identities must be resolved deterministically and auditable.

## When To Use

Use this prompt for:

- label normalization;
- role classification;
- registry integrity;
- alias handling;
- manual override;
- contradiction handling;
- confidence or uncertainty display;
- user-visible notices when inference is uncertain.

## Required Decision Table Fields

Each rule should declare:

- input signal / label / metadata;
- normalization step;
- canonical identity;
- aliases;
- role classification;
- confidence level;
- contradiction rule;
- manual override behavior;
- user-facing notice;
- validation examples;
- owner box.

## Frozen Rule Pattern

Once a decision table is accepted, ad hoc UI logic must not override it. New exceptions must be added to the decision table with tests.

## Manual Override Rule

Manual overrides must be explicit, logged, reversible where possible, and must not erase original evidence.

## Contradiction Rule

When two evidence sources disagree, the system must not silently choose one unless the priority rule is explicit. It must classify the contradiction and either resolve by a documented hierarchy or ask for manual confirmation.

## Validation Checklist

- Known labels resolve correctly.
- Aliases map to canonical identities.
- Unknowns remain unknown rather than hallucinated.
- Contradictions produce a visible warning or structured issue.
- Manual overrides do not destroy original evidence.
- Registry integrity check catches duplicate or impossible assignments.
