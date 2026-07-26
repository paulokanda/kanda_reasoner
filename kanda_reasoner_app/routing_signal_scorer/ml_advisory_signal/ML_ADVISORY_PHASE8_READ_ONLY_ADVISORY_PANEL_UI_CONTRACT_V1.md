# ML Advisory Signal Phase 8 Read-Only Advisory Panel UI Contract v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract v1
Feature ID: rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_v1

## Frozen prerequisite

This contract follows the frozen feature:

Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Completion Handoff v1

The previous completion handoff closed Phase 7 as a dormant bounded in-memory
read-only telemetry surface envelope foundation. Phase 8 begins the visible
panel track, but this feature is still only a UI contract.

## Purpose

Define what a future visible Copilot/advisory panel may display and what it must
never do.

The useful target is a visible safety/advisory layer that can show bounded
telemetry such as advisory status, boundary status, confidence band, guardrail
state, disabled/no-op state, and a label that the canonical route is unchanged.

This contract does not render a panel, does not activate a panel, wire a runtime UI, attach to app screens,
create a runtime telemetry surface, call ML, call the router, call an advisor,
or influence route choice.

## Allowed future panel sections

A future implementation may only use bounded typed sections equivalent to:

- advisory role label;
- canonical route unchanged label;
- advisory status;
- boundary status;
- confidence band;
- bounded reason codes;
- guardrail state;
- disabled/no-op state;
- non-training feedback slot.

These sections must be derived only from the Phase 7 read-only advisory surface
envelope and already-built guarded display payloads. A panel must not call the
router, call the advisor, execute an adapter, or call a provider to produce its
own content.

## Required labels

Any future panel must clearly communicate:

- advisory data is telemetry only;
- the governed router remains the final selector;
- the canonical route is unchanged;
- ML Advisory Signal has no route authority;
- confidence/status values are advisory status, not route correctness proof;
- user feedback is non-training feedback unless a separate future governed
  training contract exists.

## Forbidden panel capabilities

The panel contract forbids:

- route override button;
- use-ML-route button;
- best-route claim;
- prompt ranking;
- free-text route advice;
- free-text advisory explanation;
- final-selection hook;
- prompt-selection hook;
- router call;
- advisor call;
- adapter execution;
- provider call;
- persistence write;
- runtime UI mutation;
- runtime panel activation in this contract;
- runtime telemetry surface wiring in this contract;
- route influence;
- route authority.

## Authority model

The governed router remains the final selector. The advisory panel is not an ML
router and not a Copilot decision engine.

ML Advisory Signal remains telemetry only.

Governed Prompt Intake remains the only safe door for future prompts.

Manual Prompt Code Hint remains classification help only.

## Safe result of this patch

This patch may add docs, manifest gates, tests, and a non-runtime contract module
that evaluates whether a requested panel specification stays within the safe UI
contract. It must not activate any runtime UI.

## Next safe step

Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract Result Review Gate v1
