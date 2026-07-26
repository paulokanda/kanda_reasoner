# Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Contract v1

Feature ID: `rss_ml_adv_phase11_read_only_advisory_panel_host_binding_contract_v1`

Prerequisite handoff: `rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_completion_handoff_v1`

## Purpose

This patch creates the Phase 11 read-only advisory panel host binding contract. It defines the safe future conditions for attaching the Phase 10 renderer/mount descriptor to an application host boundary.

This is a host-binding contract only. It does not perform actual host binding, does not make the panel visible in the runtime app host, does not mutate UI, does not wire runtime telemetry surfaces, and does not grant route authority.

## Accepted contract shape

A future host-binding implementation may be considered only when all of these remain true:

- input is the Phase 10 renderer/mount descriptor lineage only;
- host binding is feature-flagged and default-off;
- disabled behavior is no-op;
- missing descriptor behavior is fail-open;
- unsafe descriptor behavior is blocked and fail-open;
- host input and host output are bounded;
- host binding remains removable/no-op;
- route selection remains invariant;
- router final selection remains invisible to the panel;
- feedback remains non-training;
- the panel remains read-only and non-authoritative.

## Explicit non-scope

This contract does not add or approve any of the following:

- actual host binding;
- host binding activation;
- runtime app-host visibility;
- mounted runtime panel;
- host event subscription;
- host callback registration;
- runtime UI mutation;
- runtime telemetry surface wiring;
- route influence;
- route authority;
- router calls;
- advisor calls;
- adapter execution;
- provider calls;
- persistence;
- prompt loading;
- prompt registry mutation;
- prompt library read;
- freeze-memory read or write;
- router-canon read;
- prompt-selection hook;
- final-selection hook;
- route override button;
- Use ML route button;
- best-route claim;
- prompt ranking;
- free-text route advice;
- runtime Pilot behavior;
- runtime Copilot decision behavior;
- autonomous ML router;
- MLRT-113.

## Next safe step

`Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Contract Result Review Gate v1`

The next step must review this contract before any host-binding implementation is attempted.
