# Routing Signal Scorer MLRT-75 Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite v1

Feature ID: `rss_mlrt75_maximum_optimized_adversarial_controlled_offline_ml_prompt_selection_test_suite_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Box type: `post-source Item 5 maximum-optimized adversarial controlled offline ML prompt-selection testing suite box`

## Purpose

MLRT-75 implements the next real ML prompt-selection test suite after MLRT-74 freeze.

It follows the user's standing rule that future real ML prompt-selection test-suite patches use the **maximum optimized number of coherent, non-duplicate tests** rather than small fixed targets or repetitive filler.

MLRT-75 adds **64/64 adversarial and edge-case in-memory tests**. The suite is intentionally harder than MLRT-73: every case is a containment/no-authority case, not a friendly expected-route selection.

## Prior ML test result summary

- MLRT-65: `3/3` first positive offline cases passed.
- MLRT-67: `5/5` harder positive offline cases passed.
- MLRT-69: `10/10` expanded positive offline cases passed.
- MLRT-71: `8/8` boundary-negative containment cases passed.
- MLRT-73: `64/64` optimized mixed in-memory cases passed.
- Before MLRT-75: cumulative controlled offline prompt-selection coverage was `90/90` cases across five real test suites.

## MLRT-75 result summary

- MLRT-75 adds exactly `64` adversarial/edge cases.
- MLRT-75 passes `64/64` cases.
- Cumulative controlled offline prompt-selection coverage becomes `154/154` cases across six real test suites.

This is a stronger offline signal for continued testing, but it is **not** a reliability claim, maturity claim, production-readiness claim, route-authority claim, training claim, calibration claim, or model-improvement claim.

## Coverage protection

MLRT-75 enforces:

- exactly `64` unique case IDs;
- exactly `64` unique user requests;
- exactly `8` adversarial audit families;
- exactly `8` cases per family;
- exactly `0` positive selected-route cases;
- exactly `64` containment/no-authority cases;
- no duplicate filler coverage;
- no forbidden selected routes;
- no persistent case files, dataset files, labels, gold records, reports, or registry writes.

Adversarial audit families:

- `PROMPT_INJECTION_OVERRIDE` — 8 adversarial/edge cases.
- `STALE_OR_POISONED_FREEZE_CONTEXT` — 8 adversarial/edge cases.
- `ROUTE_AUTHORITY_ESCALATION` — 8 adversarial/edge cases.
- `RUNTIME_ACTIVATION_PRESSURE` — 8 adversarial/edge cases.
- `PROMPT_LOADING_OR_EXFILTRATION` — 8 adversarial/edge cases.
- `TRAINING_OR_CALIBRATION_PRESSURE` — 8 adversarial/edge cases.
- `REGISTRY_OR_GOLD_MUTATION_PRESSURE` — 8 adversarial/edge cases.
- `AMBIGUOUS_EDGE_COLLISION` — 8 adversarial/edge cases.

## Expected-answer comparison doctrine

Each test case has a known expected answer:

- expected selected route: `NO_AUTHORITATIVE_ROUTE`;
- expected safe outcome: family-specific containment outcome;
- expected boundary flags: all forbidden runtime/training/persistence/registry/Pilot/Copilot flags remain false.

The static candidate ML prompt-selection output is compared against the expected answer key. This validates only the candidate's behavior on these fixed, in-memory cases. It does not prove behavior on all unseen future cases.

## Boundary preservation

MLRT-75 remains:

- offline;
- non-runtime;
- in-memory;
- test-local;
- validation-only;
- non-authoritative;
- human-review-gated.

MLRT-75 does not enable route authority, runtime routing, router prompt logic modification, prompt loading, live prompt-library reads, provider calls, embeddings, vector stores, persistence, batch mode, training-data intake, dataset creation, model training, model calibration, model improvement, gold registry writes, registry mutation, runtime Pilot, Copilot behavior, activation key, or field-test mode.

Critical boundary error budget: `0`.

## Positive state

`RSS_MLRT75_MAXIMUM_OPTIMIZED_ADVERSARIAL_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE`

## Next safe milestone

Routing Signal Scorer MLRT-76 Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1
