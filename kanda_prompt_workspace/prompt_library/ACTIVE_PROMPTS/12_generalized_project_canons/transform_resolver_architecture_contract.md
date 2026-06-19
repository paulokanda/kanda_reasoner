# Transform Resolver Architecture Contract

Version: 1.0
Status: Active prompt-library candidate
Use: Load when a project separates source identity from active runtime transforms, avoids invalid combinations, or needs a resolver that maps user selections into concrete runtime operations.


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

Generalize the source project's reference architecture contract. The reusable idea is a two-layer architecture:

```text
Base Identity + Active Transform -> Concrete Runtime Operation
```

## Layer 1: Base Identity

The base identity answers:

```text
What is the trusted source/canonical identity of the current data or object?
```

It is owned by import, diagnostic, registry, or session identity boxes.

## Layer 2: Active Transform

The active transform answers:

```text
What operation should the runtime output use now?
```

It is owned by the runtime transform/control-state box.

## Resolver Rule

A single resolver maps:

```text
Base Identity + Active Transform -> Concrete Runtime Operation
```

Do not scatter this mapping across GUI dropdowns, validators, plugins, and runtime code.

## Invalid Combination Rule

Some transforms may be blocked depending on base identity. The resolver must return structured results:

- allowed / blocked;
- concrete operation;
- reason;
- user-facing message;
- validation code;
- fallback if available.

## Runtime Rebuild Rule

If the transform changes runtime output, discard and rebuild the derived runtime product from the canonical base. Do not apply a new transform on top of an already transformed output unless explicitly cumulative and validated.

## Tests

At minimum, test:

- each base identity;
- each active transform;
- blocked combinations;
- unknown identity;
- migration of legacy values;
- display labels do not control runtime meaning.
