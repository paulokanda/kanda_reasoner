# ML Advisory Signal Phase 6 Guarded Runtime Advisory Display Contract v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract v1
Feature ID: rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_v1

## Prerequisite

This feature is allowed only after the frozen prerequisite:

Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Result Review Gate v1

## Scope

This patch defines a guarded runtime advisory display contract only. It does not
implement a runtime advisory panel, does not show advisory data, does not enable
runtime shadow mode, does not execute a real adapter, does not execute a
candidate adapter, and does not call providers.

The contract exists so a future runtime surface can be evaluated before any
actual display implementation is allowed. This phase is therefore contract-only,
read-only, telemetry-only, route-invariant, final-selection-invisible,
non-authoritative, and removable as a no-op.

## Allowed contract surface

The contract may describe only these bounded concepts:

- advisory status labels;
- abstention reason-code labels;
- boundary status labels;
- unavailable/advisor-abstained/boundary-rejected failure states;
- removal/no-op guarantee;
- route-invariance guarantee;
- final-selector invisibility guarantee.

## Forbidden scope

This phase forbids:

- real ML;
- adapter execution;
- candidate execution;
- provider calls;
- network calls;
- API keys;
- embeddings;
- vector store;
- persistence;
- report persistence;
- prompt loading;
- prompt registry mutation;
- prompt library read;
- freeze-memory read or write;
- router-canon read;
- runtime shadow mode;
- runtime display implementation;
- runtime advisory panel;
- runtime telemetry surface;
- runtime UI mutation;
- router prompt logic modification;
- router final selection modification;
- route authority;
- advisory rankings;
- free-text advisory explanations;
- training;
- calibration;
- model improvement;
- runtime Pilot behavior;
- runtime Copilot behavior;
- MLRT-113.

## Acceptance condition

The contract is accepted only when all required guards are true and every
forbidden capability is false. Any missing guard or enabled forbidden capability
must produce a rejected decision.

## Next safe feature

Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract Result Review Gate v1
