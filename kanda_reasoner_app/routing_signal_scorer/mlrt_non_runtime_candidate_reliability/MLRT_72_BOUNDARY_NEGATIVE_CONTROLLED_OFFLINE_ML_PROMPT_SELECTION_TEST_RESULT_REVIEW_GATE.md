# Routing Signal Scorer MLRT-72 Boundary-Negative Controlled Offline ML Prompt-Selection Test Result Review Gate v1

Feature ID: `rss_mlrt72_boundary_negative_controlled_offline_ml_prompt_selection_test_result_review_gate_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Box type: `post-source Item 5 boundary-negative result review gate plus web-informed test-volume escalation policy box`

Status: review-gate and policy implementation after MLRT-71 freeze with `FREEZE_MEMORY_STATUS: OK`.

## ML test result summary

Status: good direction, stronger than before, but still not runtime-ready.

- MLRT-65 first controlled offline test: 3/3 positive cases passed.
- MLRT-67 second controlled offline test: 5/5 harder positive cases passed.
- MLRT-69 expanded controlled offline test suite: 10/10 expanded positive cases passed.
- MLRT-71 boundary-negative controlled offline test suite: 8/8 boundary-negative containment cases passed.
- Cumulative controlled offline prompt-selection coverage: 26/26 cases passed across four tests.

Interpretation: this is useful validation-only evidence for continued offline testing, but it is not a reliability claim, maturity claim, production-readiness claim, training approval, model-improvement claim, or runtime-route-authority claim.

## Web-informed test-volume decision

A web check of reliable ML/MLOps testing sources supports increasing the number of test cases only when the new cases increase meaningful coverage. The decision is conditional:

- More cases can improve confidence when they are large enough, representative, non-duplicate, and closer to real expected usage.
- More cases can improve robustness when they cover different failure modes, boundary conditions, and repeated/alternative evaluation splits.
- Repeating similar easy positive cases does not materially improve reliability and may overstate confidence.
- Test sets can wear out when repeatedly used to make decisions, so future suites must add fresh cases rather than reusing only the same cases.

## Implemented policy

MLRT-72 implements the following policy for future ML prompt-selection test-suite ZIPs:

- Future real ML prompt-selection test-suite ZIPs should increase case count when moving beyond review gates.
- Minimum future real test-suite size: 16 in-memory cases unless a governed exception explains why a smaller suite is safer.
- Next real test-suite target: 24 in-memory cases.
- Future suites must include mixed positive, boundary-negative, ambiguous, low-confidence, duplicate/leakage-guard, drift/representativeness, forbidden-route, and containment cases.
- Added cases must be test-local and in-memory only.
- Added cases must not create datasets, persistent case files, labels, gold records, registry writes, reports, prompt loading, provider calls, embeddings, route authority, training, calibration, runtime Pilot, or Copilot behavior.

## What this corrects

MLRT-70 identified that earlier tests were good but still limited because many cases were positive/static expected-route matches. MLRT-71 corrected that with boundary-negative containment coverage. MLRT-72 further corrects the testing strategy by preventing the next test stages from staying too small.

## Guardrails preserved

- `runtime_route_authority_enabled = false`
- `router_prompt_logic_modified = false`
- `prompt_loading_enabled = false`
- `provider_calls_enabled = false`
- `embeddings_enabled = false`
- `result_persistence_enabled = false`
- `training_data_intake_enabled = false`
- `dataset_creation_enabled = false`
- `model_training_started = false`
- `model_calibration_started = false`
- `model_improvement_started = false`
- `gold_registry_write_enabled = false`
- `registry_mutation_enabled = false`
- `runtime_pilot_enabled = false`
- `copilot_enabled = false`
- `critical_boundary_error_budget = 0`

Positive label: `RSS_MLRT72_BOUNDARY_NEGATIVE_RESULT_REVIEW_ACCEPTED_AND_TEST_VOLUME_ESCALATION_POLICY_SET_NON_RUNTIME_NON_AUTHORITATIVE`

Next safe milestone: `Routing Signal Scorer MLRT-73 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite v1`
