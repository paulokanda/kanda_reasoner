# Phase 8 Read-Only Advisory Panel UI Implementation Boundary Model v1

Feature ID: rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1

## Boundary summary

This is a renderer-neutral view-model implementation. It is not a renderer, not
a runtime panel activation, and not runtime UI wiring.

The implementation sits after Phase 7 surface envelope construction:

Canonical router final result -> Phase 7 read-only surface envelope -> Phase 8
read-only advisory panel view model.

The canonical router final result remains unchanged.

## Input boundary

The only accepted live input is the Phase 7 read-only advisory surface envelope, implemented as a Phase 7 `ReadOnlyAdvisorySurfaceWiringEnvelope`.
Missing or invalid input fails open to a no-op view model.

## Output boundary

The output is a bounded immutable `ReadOnlyAdvisoryPanelViewModel` with typed
sections only. The output has no actions, no route override controls, no prompt
rankings, and no free-text route advice.

## Runtime boundary

The implementation does not attach to app screens or runtime UI. It does not
perform rendering. It does not mutate UI state. It does not write persistence.

## Authority boundary

No field in the view model may select, rank, override, veto, modify, or recommend
routes or prompts. Confidence bands are advisory status only and not correctness
proof.
