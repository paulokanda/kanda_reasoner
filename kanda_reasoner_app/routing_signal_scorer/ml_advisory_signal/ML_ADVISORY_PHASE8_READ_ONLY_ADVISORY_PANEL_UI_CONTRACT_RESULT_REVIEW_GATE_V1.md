# Phase 8 Read-Only Advisory Panel UI Contract Result Review Gate v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract Result Review Gate v1
Feature ID: rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1

## Reviewed feature

Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract v1

This review gate accepts the Phase 8 UI contract as safe only for continued
governed implementation of a future read-only advisory panel. The reviewed
contract begins the visible Copilot/advisory panel track, but it remains a
contract only and does not activate a panel.

## Review decision

The reviewed contract is accepted only because it requires a future panel to be
read-only, telemetry-only, route-invariant, final-selection-invisible,
fail-open, removable/no-op, bounded, and non-authoritative.

It accepts only bounded UI sections such as advisory role label, canonical route
unchanged label, advisory status, boundary status, confidence band, bounded
reason codes, guardrail state, disabled/no-op state, and a non-training feedback
slot.

It requires explicit labels that the governed router remains the final selector,
the canonical route is unchanged, ML Advisory Signal has no route authority, and
confidence/status values are not route correctness proof.

## Not accepted

This review gate does not accept:

- runtime panel activation;
- runtime UI mutation;
- runtime telemetry surface wiring;
- route influence;
- route authority;
- router calls;
- advisor calls;
- adapter execution;
- provider calls;
- persistence writes;
- prompt ranking;
- route override buttons;
- use-ML-route buttons;
- best-route claims;
- free-text route advice;
- free-text advisory explanations;
- final-selection hooks;
- prompt-selection hooks;
- runtime Pilot behavior;
- runtime Copilot decision behavior.

## Safe next step

Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation v1

The next implementation may only build a renderer-neutral, bounded in-memory
panel view model from the already-governed Phase 7 surface envelope or already-built
guarded advisory display payload. It must not render a real UI, mutate screens,
wire runtime telemetry, call ML, call the router, call an advisor, execute an
adapter, call a provider, persist data, or affect routing.
