# Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Contract v1

Feature ID: `rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_v1`

This patch starts the runtime-visible panel track as a **contract only**.
It defines the safety requirements for a future read-only advisory panel runtime activation, but it does not activate a runtime panel.

Source prerequisite:
`Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Completion Handoff v1`.

## What this contract permits later

A future governed implementation may request a visible panel only if all of these remain true:

- The panel consumes only the Phase 8 renderer-neutral panel view-model or Phase 7 read-only surface envelope lineage.
- Runtime activation must be explicit, feature-flagged, default-off, removable, and fail-open.
- The mounted surface must remain read-only, telemetry-only, route-invariant, and final-selection-invisible.
- The panel must show advisory role, canonical route unchanged, no route authority, confidence-not-correctness, and non-training feedback labels.
- Renderer adapter work must remain a separate future governed contract.

## What this contract does not do

This patch does not activate a panel, render UI, mount UI, mutate runtime screens, wire a runtime telemetry surface, call the router, call an advisor, execute adapters, call providers, persist data, read prompt libraries, read freeze memory, read router canon, influence routes, or grant route authority.

## Forbidden runtime capabilities

The contract blocks route override button, use-ML-route button, best-route claim, prompt ranking, advisory ranking, free-text route advice, free-text advisory explanations, final-selection hook, prompt-selection hook, router call, advisor call, adapter execution, provider call, persistence write, prompt loading, prompt registry mutation, prompt library read, freeze-memory read/write, router-canon read, route influence, route authority, and runtime Copilot decision behavior.

## Next safe step

After validation and freeze, the next safe step is:
`Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Contract Result Review Gate v1`.
