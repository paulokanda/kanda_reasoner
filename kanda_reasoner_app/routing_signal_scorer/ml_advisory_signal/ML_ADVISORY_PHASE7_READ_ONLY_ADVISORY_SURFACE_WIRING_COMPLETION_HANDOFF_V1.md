# ML Advisory Signal Phase 7 Read-Only Advisory Surface Wiring Completion Handoff v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Completion Handoff v1
Feature ID: rss_ml_adv_phase7_read_only_advisory_surface_wiring_completion_handoff_v1

## Frozen prerequisite

This completion handoff follows the frozen feature:

Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Final Safety Gate v1

The final safety gate locked the Phase 7 read-only advisory surface wiring path
as safe only for a dormant bounded in-memory read-only telemetry surface envelope foundation. The completed artifact remains a read-only telemetry envelope builder
foundation only.

## Completed safe state

The completed Phase 7 read-only advisory surface wiring state is:

- bounded;
- in-memory only;
- read-only;
- telemetry-only;
- fail-open;
- removable/no-op safe;
- final-selection-invisible;
- route-invariant;
- non-authoritative;
- not prompt-selection correctness evidence;
- not runtime Copilot decision behavior;
- not runtime Pilot behavior;
- not a visible panel;
- not runtime UI wiring;
- not runtime telemetry surface wiring.

The completed implementation-shaped artifact can wrap a canonical dispatch snapshot and an already-built guarded advisory display payload into a separate read-only telemetry surface envelope. It does not call the router, call an
advisor, execute an adapter, activate a panel, mutate UI, persist data, or
influence routing.

## Authority model

The governed router remains the final selector. The governed router must remain
the final selector.

ML Advisory Signal remains telemetry only.

Governed Prompt Intake remains the only safe door for future prompts.

Manual Prompt Code Hint remains classification help only.

No advisory surface field, envelope state, feedback slot, confidence value,
boundary status, reason code, or display payload may select, rank, override,
veto, modify, or influence a route.

## Locked prohibitions

This completion handoff preserves these prohibitions:

- no real ML;
- no adapter execution;
- no candidate execution;
- no provider calls;
- no network calls;
- no API keys;
- no embeddings;
- no vector store;
- no persistence;
- no report persistence;
- no prompt loading;
- no prompt registry mutation;
- no prompt library read;
- no freeze-memory read or write;
- no router-canon read;
- no runtime shadow mode;
- no runtime advisory panel activation;
- no runtime UI mutation;
- no runtime telemetry surface wiring;
- no router prompt logic modification;
- no router final selection modification;
- no route influence;
- no route authority;
- no advisory rankings;
- no free-text route advice;
- no free-text advisory explanations;
- no training;
- no calibration;
- no model improvement;
- no runtime Pilot behavior;
- no runtime Copilot decision behavior;
- no MLRT-113;
- adds 0 new real prompt-selection cases;
- critical boundary error budget zero.

## What future work must do

This handoff completes the Phase 7 read-only advisory surface wiring foundation.
It does not authorize a visible Copilot/advisory panel. A visible panel must
start as a separate governed UI contract.

The next safe feature, if requested, is:

Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract v1

That future UI contract must remain read-only, telemetry-only, route-invariant,
final-selection-invisible, removable, fail-open, bounded, non-authoritative, and
must preserve the governed router as final selector. It must include a clear
label that advisory data is telemetry and not route authority.

Any future advisory panel, user-visible runtime surface, provider adapter,
persistence layer, prompt-loading behavior, prompt-registry change,
prompt-library read, freeze-memory read, router-canon read, router prompt logic
change, route influence, or final route selection change must be separately
designed, validated, and frozen.

## Stop condition

Phase 7 read-only advisory surface wiring work is complete for the current safe
telemetry-envelope foundation. The safe default next action is to stop and keep
this as documentation and tests unless the user explicitly requests the separate
advisory-panel UI contract.
