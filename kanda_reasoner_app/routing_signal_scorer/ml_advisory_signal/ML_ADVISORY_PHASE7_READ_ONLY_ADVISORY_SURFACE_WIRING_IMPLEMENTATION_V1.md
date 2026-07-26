# ML Advisory Signal Phase 7 Read-Only Advisory Surface Wiring Implementation v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation v1
Feature ID: rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1

## Purpose

This feature implements the narrow read-only surface wiring step permitted by the
Phase 7 surface wiring contract result review gate. It adds an in-memory envelope
builder that can attach an already-built guarded advisory display payload to a
separate telemetry surface envelope after canonical router completion.

## Implemented behavior

The implementation adds:

- `CanonicalDispatchSnapshot` for caller-supplied canonical output metadata;
- `ReadOnlyAdvisorySurfaceWiringPolicy` for the wiring policy;
- `ReadOnlyAdvisorySurfaceWiringEnvelope` for the immutable output envelope;
- `build_read_only_advisory_surface_wiring_envelope` for construction;
- `build_phase7_read_only_surface_wiring_probe` for tests.

The builder copies the canonical snapshot unchanged into `before` and `after`
positions. The advisory display payload is attached only as a separate telemetry
surface field. Disabled, missing, invalid, or rejected advisory data fails open
without changing the canonical snapshot.

## Non-activation boundary

This implementation does not wire itself into the runtime app, UI, or router. It
creates no advisory panel and no runtime telemetry surface. It is a callable,
bounded, in-memory utility only.

## Forbidden scope

No real ML, adapter execution, provider calls, network calls, API keys,
embeddings, vector store, persistence, report persistence, prompt loading,
prompt registry mutation, prompt-library read, freeze-memory read or write,
router-canon read, runtime shadow mode, runtime advisory panel, runtime UI
mutation, runtime telemetry surface wiring, router prompt logic modification,
router final selection modification, route authority, advisory rankings,
free-text route advice, free-text advisory explanations, training, calibration,
model improvement, runtime Pilot behavior, runtime Copilot decision behavior, or
MLRT-113.
