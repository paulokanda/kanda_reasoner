# Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Contract v1

## status

Contract-only Phase 12 boundary after the frozen Phase 11 host-binding completion handoff.

## purpose

This contract defines the safe future conditions for runtime app-host visibility of the read-only ML Advisory panel. It consumes only the Phase 11 host-binding descriptor lineage and prepares a later governed implementation review path.

## allowed future shape

A later implementation may only build a feature-flagged, default-off, fail-open, removable/no-op, in-memory, read-only runtime app-host visibility descriptor from the Phase 11 host-binding descriptor. The descriptor may describe how bounded host-bound advisory sections could be shown by the app host, but this contract does not show them.

## hard boundaries

This contract adds no actual runtime app-host visibility, no visibility activation, no mounted runtime panel, no runtime panel mount side effects, no runtime UI mutation, no runtime telemetry surface wiring, no host event subscription, no host callback registration, no router calls, no advisor calls, no provider calls, no persistence, no prompt loading, no prompt registry mutation, no prompt library read, no freeze-memory read or write, no router-canon read, no route influence, no route authority, no route override button, no Use ML route button, no best-route claim, no prompt ranking, no free-text route advice, no runtime Pilot behavior, no runtime Copilot decision behavior, no autonomous ML router, and no MLRT-113.

## required safety properties

- Phase 11 host-binding descriptor lineage only.
- Explicit feature flag required.
- Feature flag default-off.
- Disabled/no-op behavior required.
- Fail-open missing-descriptor behavior required.
- Block unsafe descriptor behavior required.
- Runtime visibility input bounded.
- Runtime visibility output bounded.
- Removable/no-op visibility behavior required.
- Route-invariant behavior required.
- Final-selection-invisible behavior required.
- Non-training feedback slot only.
- Non-authoritative status.
- Critical boundary error budget zero.

## completion meaning

Passing this contract means Phase 12 may proceed to a contract result review gate. It does not mean ML is visible in the app host yet and does not complete runtime ML integration.

## planned next step

Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Contract Result Review Gate v1
