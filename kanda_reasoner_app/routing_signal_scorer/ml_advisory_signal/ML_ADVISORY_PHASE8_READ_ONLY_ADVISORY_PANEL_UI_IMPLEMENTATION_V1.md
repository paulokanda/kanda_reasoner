# ML Advisory Signal Phase 8 Read-Only Advisory Panel UI Implementation v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation v1
Feature ID: rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1

## Frozen prerequisite

This implementation follows the frozen feature:

Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract Result Review Gate v1

The review gate accepted the Phase 8 UI contract only for continued governed
implementation. This patch implements a renderer-neutral panel view-model
builder, not a runtime UI panel.

## Purpose

Build a bounded in-memory view model that a future UI renderer could display as
a read-only advisory panel. The view model is created only from the Phase 7
read-only advisory surface envelope or its already-built guarded advisory display
payload.

This is the first concrete implementation step toward a visible Copilot/advisory
panel, but it is still not runtime panel activation. This implementation does not render UI.

## What the implementation may do

The implementation may build immutable renderer-neutral sections such as:

- advisory role label;
- canonical route unchanged label;
- no route authority label;
- advisory status;
- boundary status;
- confidence band;
- confidence is not correctness proof label;
- bounded reason codes;
- guardrail state;
- disabled/no-op state;
- non-training feedback slot.

## What the implementation must not do

This implementation must not:

- render UI or mutate runtime UI;
- activate a runtime panel;
- wire a runtime telemetry surface;
- call the router;
- call an advisor;
- execute adapters;
- call providers or network;
- persist panel output;
- read prompt library, freeze memory, or router canon;
- rank prompts or routes;
- emit free-text route advice or free-text advisory explanations;
- provide route override or use-ML-route actions;
- influence route choice;
- grant route authority;
- behave as runtime Copilot decision logic.

## Authority model

The governed router remains the final selector. The panel view model is a
read-only telemetry artifact only. It is not a router, not a prompt selector, and
not evidence of prompt-selection correctness.

## Safe result of this patch

After this patch, the codebase can construct an in-memory renderer-neutral
read-only panel view model from a safe surface envelope. A separate future patch
must still review, safety-gate, and explicitly wire any runtime UI renderer.

## Next safe step

Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation Result Review Gate v1
