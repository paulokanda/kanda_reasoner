# ML Advisory Signal - Phase 11 Host Binding Implementation Boundary Model v1

The implementation boundary is a pure in-memory descriptor transformation:

Phase 10 renderer/mount descriptor -> Phase 11 host-binding descriptor.

Allowed:

- Read the supplied Phase 10 renderer/mount descriptor object.
- Verify the descriptor is ready, bounded, read-only, telemetry-only, in-memory-only, removable/no-op, route-invariant, final-selection-invisible, and non-authoritative.
- Copy bounded rendered sections into bounded host-bound sections.
- Return disabled/no-op, fail-open, blocked, or ready descriptor states.

Forbidden:

- Actual host binding side effects.
- Host binding activation.
- Runtime app-host visibility side effects.
- Mounted runtime panel side effects.
- Host event subscriptions.
- Host callback registrations.
- Runtime UI mutation.
- Runtime telemetry surface wiring.
- Router/advisor/provider calls.
- Persistence.
- Prompt loading or prompt registry mutation.
- Prompt-library, freeze-memory, or router-canon reads.
- Route influence or route authority.
- Runtime Copilot decision behavior.
- MLRT-113.

Critical boundary error budget: zero.
