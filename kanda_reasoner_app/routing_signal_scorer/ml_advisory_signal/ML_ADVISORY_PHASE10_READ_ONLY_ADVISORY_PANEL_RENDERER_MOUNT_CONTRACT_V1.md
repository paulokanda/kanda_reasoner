# Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Contract v1

Feature ID: `rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1`

This patch starts Phase 10 as a **renderer/mount contract only**. It defines the
safety requirements for a future visible read-only advisory panel renderer and
mount point, but it does not activate a renderer, mount a panel, mutate UI, or
wire runtime telemetry.

Source prerequisite:
`Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Completion Handoff v1`.

## What this contract permits later

A future governed implementation may request a visible read-only panel
renderer/mount path only if all of these remain true:

- the future renderer consumes only the Phase 9 activation envelope lineage;
- the path is explicit, feature-flagged, default-off, removable, and fail-open;
- the renderer input is bounded;
- the renderer output is bounded;
- the mounted surface remains read-only, telemetry-only, route-invariant, and
  final-selection-invisible;
- the panel shows advisory role, canonical route unchanged, no route authority,
  confidence-not-correctness, and non-training feedback labels;
- final route selection remains governed by the deterministic router;
- actual renderer activation and UI mounting remain separate later governed
  implementation work.

## What this contract does not do

This patch does not activate a renderer, mount a panel, render UI, mutate runtime
screens, wire a runtime telemetry surface, call the router, call an advisor,
execute adapters, call providers, persist data, read prompt libraries, read
freeze memory, read router canon, influence routes, or grant route authority.

## Forbidden runtime capabilities

The contract blocks route override button, use-ML-route button, best-route claim,
prompt ranking, advisory ranking, free-text route advice, free-text advisory
explanations, final-selection hook, prompt-selection hook, router call, advisor
call, adapter execution, provider call, persistence write, prompt loading, prompt
registry mutation, prompt library read, freeze-memory read/write, router-canon
read, route influence, route authority, actual runtime panel activation,
actual renderer mount, renderer activation, mounted panel behavior, runtime UI
mutation, runtime telemetry surface wiring, and runtime Copilot decision behavior.

## Next safe step

After validation and freeze, the next safe step is:
`Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Contract Result Review Gate v1`.
