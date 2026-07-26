# Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract v1

## status

Contract-only Phase 13 boundary after the frozen Phase 12 runtime app-host visibility completion handoff.

## purpose

This contract defines the safe future conditions for passive visibility activation of the read-only ML Advisory panel. It consumes only the Phase 12 runtime app-host visibility descriptor lineage and prepares a later governed implementation review path.

## allowed future shape

A later implementation may only create a feature-flagged, default-off, fail-open, removable/no-op, in-memory, read-only passive visibility activation descriptor from the Phase 12 runtime app-host visibility descriptor. The descriptor may describe a passive read-only app-host slot for bounded runtime-visible sections, but this contract does not register the slot, mutate UI, activate visibility, or mount a runtime panel.

## hard boundaries

This contract adds no actual passive visibility activation, no passive visibility slot registration, no passive visibility slot mutation, no actual runtime app-host visibility, no visibility activation, no mounted runtime panel, no runtime panel mount side effects, no runtime UI mutation, no runtime telemetry surface wiring, no host event subscription, no host callback registration, no router calls, no advisor calls, no provider calls, no persistence, no prompt loading, no prompt registry mutation, no prompt library read, no freeze-memory read or write, no router-canon read, no route influence, no route authority, no route override button, no Use ML route button, no best-route claim, no prompt ranking, no advisory ranking, no free-text route advice, no free-text explanations, no runtime Pilot behavior, no runtime Copilot decision behavior, no autonomous ML router, no visible ML integration completion, and no MLRT-113.

## required safety properties

- Phase 12 runtime app-host visibility descriptor lineage only.
- Explicit feature flag required.
- Feature flag default-off.
- Disabled/no-op behavior required.
- Fail-open missing-descriptor behavior required.
- Block unsafe descriptor behavior required.
- Passive visibility input bounded.
- Passive visibility output bounded.
- Read-only passive visibility slot required for the future path.
- Removable/no-op activation behavior required.
- Route-invariant behavior required.
- Final-selection-invisible behavior required.
- Non-training feedback slot only.
- Non-authoritative status.
- Critical boundary error budget zero.

## completion meaning

Passing this contract means Phase 13 may proceed to a contract result review gate. It does not mean ML is visible in the app host yet and does not complete runtime ML integration.

## planned next step

Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract Result Review Gate v1
