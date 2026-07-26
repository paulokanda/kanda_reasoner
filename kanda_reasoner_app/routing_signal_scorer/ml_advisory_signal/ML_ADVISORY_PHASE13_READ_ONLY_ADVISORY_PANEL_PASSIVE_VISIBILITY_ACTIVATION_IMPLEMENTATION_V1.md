# Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation v1

Feature ID: `rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1`

This patch implements the Phase 13 passive visibility activation implementation as a feature-flagged, default-off, in-memory read-only descriptor builder. It consumes only the Phase 12 runtime app-host visibility descriptor lineage and copies bounded runtime-visible sections into bounded passive visibility slot descriptors.

The implementation remains passive descriptor metadata only. It does not perform actual passive visibility activation, register or mutate passive visibility slots in a host, activate runtime app-host visibility, mount a runtime panel, mutate runtime UI, wire telemetry surfaces, subscribe to host events, register host callbacks, call router/advisor/provider logic, persist data, read prompt libraries, read freeze memory, read router canon, influence route selection, grant route authority, or create runtime Copilot decision behavior.

## Accepted behaviors

- Feature flag exists and defaults off.
- Disabled/default-off execution returns `DISABLED_NOOP`.
- Missing or invalid Phase 12 visibility descriptor returns `FAIL_OPEN_NO_DESCRIPTOR`.
- Unsafe Phase 12 descriptor returns `BLOCKED_UNSAFE_DESCRIPTOR`.
- Safe Phase 12 descriptor returns a bounded read-only passive visibility activation descriptor.
- Output is in-memory only, bounded, removable/no-op, route-invariant, final-selection-invisible, and non-authoritative.

## Explicitly blocked

- Actual passive visibility activation.
- Passive visibility slot registration or mutation.
- Actual runtime app-host visibility activation.
- Mounted runtime panel side effects.
- Runtime UI mutation.
- Runtime telemetry surface wiring.
- Host event subscription or callback registration.
- Route influence, route authority, router calls, advisor calls, provider calls, persistence, runtime Copilot decision behavior, autonomous ML routing, and MLRT-113.

## Planned next step

Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation Result Review Gate v1
