# Phase 10 Read-Only Advisory Panel Renderer Mount Implementation Boundary Model v1

Feature ID: `rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1`

## Boundary

This patch stays inside `routing_signal_scorer/ml_advisory_signal` and creates a
pure in-memory read-only mount descriptor builder. It does not import GUI
frameworks and does not mutate runtime UI.

## Input boundary

Allowed input:

- a caller-supplied Phase 9 `ReadOnlyAdvisoryPanelRuntimeActivationEnvelope`.

Forbidden input acquisition:

- router calls;
- advisor calls;
- adapter execution;
- provider calls;
- prompt library reads;
- freeze-memory reads;
- router-canon reads;
- persistence reads.

## Output boundary

Allowed output:

- immutable `ReadOnlyAdvisoryPanelRendererMountDescriptor`;
- immutable bounded rendered sections copied from Phase 8 panel sections;
- disabled/no-op state;
- fail-open state;
- blocked-unsafe-envelope state;
- ready read-only descriptor state.

Forbidden output:

- route influence;
- route authority;
- final-selection hook;
- prompt-selection hook;
- route override button;
- Use ML route button;
- best-route claim;
- prompt ranking;
- advisory ranking;
- free-text route advice;
- runtime UI mutation;
- runtime telemetry surface wiring;
- persistence.

## Safety conclusion

Phase 10 implementation may expose a visible-read-only descriptor under an
explicit feature flag, but the governed router remains final selector and ML
Advisory Signal remains telemetry only.
