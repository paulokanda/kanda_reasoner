# ML Advisory Phase 6 Guarded Runtime Advisory Display Implementation v1

Feature ID: `rss_ml_adv_phase6_guarded_runtime_advisory_display_implementation_v1`

Feature title: `Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Implementation v1`

## Purpose

This patch adds the first implementation-shaped guarded display component:
an in-memory read-only advisory telemetry payload builder.

The implementation accepts an already computed `AdvisoryOutput` and returns
an immutable `GuardedRuntimeAdvisoryDisplayPayload` that can later be shown by
a caller-supplied display surface.

## What it may expose

Only bounded canned telemetry fields are exposed:

- advisory flags;
- advisory reason codes;
- boundary status;
- abstention state;
- non-authoritative confidence;
- display failure state codes.

## Hard boundaries

This implementation does not execute a model or adapter. It does not call
providers. It does not read prompt libraries, freeze memory, router canon, or
prompt files. It does not persist payloads. It does not mutate UI. It does
not modify router prompt logic or final route selection.

The governed router remains final selector. The display payload is
telemetry-only and final-selection-invisible.

## Not a full runtime copilot yet

This patch implements a payload builder only. It does not wire the payload
into an application panel, runtime UI, router flow, or shadow mode. A later
governed patch must decide whether and where this read-only payload may be
surfaced.
