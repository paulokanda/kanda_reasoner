# ML Advisory Signal Phase 7 Read-Only Advisory Surface Wiring Boundary Model v1

## Safe data flow

```text
canonical router already completed
        ↓
caller supplies immutable CanonicalDispatchSnapshot
        ↓
caller supplies already-built GuardedRuntimeAdvisoryDisplayPayload
        ↓
build_read_only_advisory_surface_wiring_envelope(...)
        ↓
immutable read-only telemetry envelope
```

## Boundary rules

1. The builder does not call the router.
2. The builder does not call advisors, models, adapters, providers, network, or
   storage.
3. The builder does not mutate canonical data.
4. Advisory data is separate from canonical data.
5. Disabled mode returns a no-op envelope.
6. Invalid advisory data fails open.
7. The implementation has no UI or panel side effects.
8. It cannot select prompts or influence final selection.

## Useful finality

This stage makes later visible advisory UI safer because the app can consume a
single typed envelope instead of raw advisory output. The envelope already
contains state codes, a separate advisory payload section, and immutable canonical
snapshot copies.
