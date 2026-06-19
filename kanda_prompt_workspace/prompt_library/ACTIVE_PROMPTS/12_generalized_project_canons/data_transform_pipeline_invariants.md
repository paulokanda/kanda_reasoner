# Data Transform Pipeline Invariants

Version: 1.0
Status: Active prompt-library candidate
Use: Load when implementing data import, normalization, transformations, filters, derived outputs, previews, analysis artifacts, or any pipeline where user interaction can change runtime output.


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


## Generalized Pipeline Model

The transferable architecture from the source project is:

```text
SourceTruth -> CanonicalWorkingBase -> DerivedRuntimeProduct
```

## Definitions

### SourceTruth

The immutable imported or acquired truth. It is preserved for provenance and recovery. It must not be filtered, transformed, patched, reinterpreted, or used as a scratch object.

### CanonicalWorkingBase

A normalized, validated working base derived from SourceTruth. It may contain safe normalization, metadata repair, identity resolution, and compatibility fields. After creation, it should be treated as stable input for runtime rebuilds.

### DerivedRuntimeProduct

A disposable output created from CanonicalWorkingBase plus current transform state. It can be rebuilt whenever signal-affecting or data-affecting state changes. It must not become the new SourceTruth.

## Non-Negotiable Invariants

- The visible/output product must never become the next source of truth.
- Applying a new transform on top of an already transformed output is forbidden unless the transform is explicitly cumulative by design and validated as such.
- Same final active state must yield the same derived output regardless of user-click order.
- View-only controls must not rebuild or mutate data truth.
- Data-affecting controls rebuild DerivedRuntimeProduct from CanonicalWorkingBase.
- Runtime previews are disposable and must be regenerable.
- Generated analysis artifacts must record which source/canonical/transform state produced them.

## Control Classes

| Class | Meaning | Examples | Allowed action |
|---|---|---|---|
| View-only control | Display state only | zoom, theme, scroll, font, visibility | update view state only |
| Derived-output control | affects runtime output | filters, reference transforms, derived selections | rebuild derived output |
| Source/canonical control | affects identity/provenance | import metadata, normalization, registry | requires explicit owner box and validation |
| Analysis control | creates secondary artifacts | reports, maps, tables, summaries | consume derived/canonical state, do not mutate truth |

## Validation Questions

- Can this change mutate SourceTruth? If yes, reject.
- Can this change make DerivedRuntimeProduct become the next source? If yes, reject.
- Can user-click order change final output for same active state? If yes, redesign.
- Is the state class view-only, derived-output, source/canonical, or analysis?
- Which box owns the transform state?
- Which tests prove deterministic rebuild from canonical base?
