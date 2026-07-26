# Phase 6 Guarded Runtime Advisory Display Implementation Boundary Model v1

Feature ID: `rss_ml_adv_phase6_guarded_runtime_advisory_display_implementation_v1`

## Allowed

- In-memory payload construction from caller-supplied advisory output.
- Bounded canned flags and reason codes.
- Read-only telemetry payloads.
- Route-invariant and final-selection-invisible behavior.
- Fail-open removable behavior.

## Forbidden

- Real ML execution.
- Adapter or candidate execution.
- Provider, network, API-key, embedding, or vector-store access.
- File persistence or report persistence.
- Prompt loading, prompt-library read, prompt-registry mutation.
- Freeze-memory read or write.
- Router-canon read.
- Runtime shadow-mode enablement.
- Runtime advisory panel creation.
- Runtime UI mutation.
- Router prompt logic modification.
- Router final-selection modification.
- Route authority.
- Advisory ranking.
- Free-text advisory explanation.
- Training, calibration, or model improvement.

## Safety shape

The display implementation is limited to immutable dataclasses and
standard-library-only in-memory values. It must remain removable without
changing router outcomes.
