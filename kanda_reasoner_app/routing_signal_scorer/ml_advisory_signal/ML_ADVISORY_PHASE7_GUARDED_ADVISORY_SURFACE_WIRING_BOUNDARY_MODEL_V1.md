# Phase 7 Guarded Advisory Surface Wiring Boundary Model v1

## Boundary model

The safe boundary is:

```text
canonical router final selection
  -> copied unchanged route result
  -> already computed AdvisoryOutput
  -> guarded display payload
  -> future read-only surface envelope
  -> no final route mutation
```

## Contract-only state

This patch defines the boundary, types, and tests. It does not wire the
boundary into the router, app, UI, or panel runtime.

## Required future implementation tests

- Route result copied unchanged.
- Final selection invisible to advisory logic.
- Disable/no-op returns no surface.
- Typed payload only.
- No free-text route advice.
- No runtime panel without explicit implementation contract.
- No provider, network, persistence, prompt-library, freeze-memory, or router-canon reads.
- Kill-switch and rollback path available.
