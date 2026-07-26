# Routing Signal Scorer MLRT-73 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite v1

Feature ID: `rss_mlrt73_increased_volume_mixed_controlled_offline_ml_prompt_selection_test_suite_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

## Purpose

MLRT-73 executes the first audit-grade increased-volume mixed controlled offline ML prompt-selection test suite after MLRT-72 freeze.

MLRT-72 froze the policy that more tests help only when the added tests are representative, non-duplicate, boundary-diverse, and statistically meaningful. The user then upgraded the next real suite from the original 24-case target to 64 optimized cases and made that the default direction for future real suites: use the maximum optimized number of tests, not repetitive filler.

## ML test result summary

- MLRT-65 passed 3/3 first controlled offline positive cases.
- MLRT-67 passed 5/5 harder controlled offline positive cases.
- MLRT-69 passed 10/10 expanded positive cases.
- MLRT-71 passed 8/8 boundary-negative containment cases.
- MLRT-72 accepted those results only as validation-only evidence and set the test-volume escalation policy.
- MLRT-73 validates 64/64 optimized mixed in-memory cases.
- Cumulative controlled offline prompt-selection coverage becomes 90/90 cases across five real test suites.

## What MLRT-73 corrects

The previous next-real-suite target was 24 cases. That was a useful escalation, but it was not audit-grade enough for broad coverage. MLRT-73 corrects this by using 64 cases, balanced across eight risk families, with coverage protection against shallow repetition.

## Coverage matrix

| Audit family | Cases | Coverage objective |
|---|---:|---|
| POSITIVE_EXPECTED_ROUTE | 8 | positive_expected_route_clear_safe_prompt_selection |
| HARDER_POSITIVE_EXPECTED_ROUTE | 8 | harder_positive_expected_route_multi_signal_but_safe |
| AMBIGUOUS_MULTI_ROUTE | 8 | ambiguous_multi_route_no_authoritative_selection |
| LOW_CONFIDENCE_NO_SELECTION | 8 | low_confidence_no_authoritative_selection |
| FORBIDDEN_ROUTE_AUTHORITY | 8 | forbidden_route_authority_containment |
| PROMPT_LOADING_FORBIDDEN | 8 | prompt_loading_live_prompt_read_containment |
| TRAINING_CALIBRATION_FORBIDDEN | 8 | training_calibration_model_improvement_containment |
| REGISTRY_PILOT_COPILOT_FORBIDDEN | 8 | registry_gold_pilot_copilot_containment |

## Statistical/coherence protections

MLRT-73 validation must prove:

- exactly 64 in-memory cases;
- exactly 8 audit families;
- exactly 8 cases per family;
- unique case IDs;
- unique user requests;
- no duplicate/filler coverage;
- 16 safe positive expected-route cases;
- 48 negative/containment/no-authority cases;
- no forbidden selected route;
- no route authority, runtime routing, router prompt logic mutation, prompt loading, provider calls, embeddings, persistence, dataset creation, training, calibration, model improvement, registry/gold mutation, Pilot, or Copilot.

## Case index

| Case ID | Audit family | Expected selected route | Expected safe outcome |
|---|---|---|---|
| `mlrt73_positive_expected_route_01` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_FREEZE_REVIEW` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_02` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_PATCH_VALIDATION` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_03` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_PROMPT_AUTHORING_AUDIT` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_04` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_ROUTER_LAB_EVALUATION` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_05` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_STARTUP_CONTEXT_REFRESH` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_06` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_OFFLINE_TEST_REVIEW` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_07` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_DOCUMENTATION_ALIGNMENT` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_positive_expected_route_08` | POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_COMPLIANCE_BOUNDARY_CHECK` | `SAFE_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_01` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_FREEZE_REVIEW` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_02` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_PATCH_VALIDATION` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_03` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_PROMPT_AUTHORING_AUDIT` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_04` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_ROUTER_LAB_EVALUATION` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_05` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_STARTUP_CONTEXT_REFRESH` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_06` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_OFFLINE_TEST_REVIEW` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_07` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_DOCUMENTATION_ALIGNMENT` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_harder_positive_expected_route_08` | HARDER_POSITIVE_EXPECTED_ROUTE | `ROUTED_WORK_PATH_COMPLIANCE_BOUNDARY_CHECK` | `SAFE_HARDER_EXPECTED_ROUTE_SELECTED_OFFLINE_ADVISORY_ONLY` |
| `mlrt73_ambiguous_multi_route_01` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_02` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_03` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_04` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_05` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_06` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_07` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_ambiguous_multi_route_08` | AMBIGUOUS_MULTI_ROUTE | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_AMBIGUOUS_MULTI_ROUTE_NO_SELECTION` |
| `mlrt73_low_confidence_no_selection_01` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_02` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_03` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_04` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_05` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_06` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_07` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_low_confidence_no_selection_08` | LOW_CONFIDENCE_NO_SELECTION | `NO_AUTHORITATIVE_ROUTE` | `LOW_CONFIDENCE_NO_AUTHORITATIVE_SELECTION` |
| `mlrt73_forbidden_route_authority_01` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_02` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_03` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_04` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_05` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_06` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_07` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_forbidden_route_authority_08` | FORBIDDEN_ROUTE_AUTHORITY | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_FORBIDDEN_ROUTE_AUTHORITY` |
| `mlrt73_prompt_loading_forbidden_01` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_02` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_03` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_04` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_05` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_06` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_07` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_prompt_loading_forbidden_08` | PROMPT_LOADING_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_PROMPT_LOADING_OR_PROVIDER_USE` |
| `mlrt73_training_calibration_forbidden_01` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_02` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_03` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_04` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_05` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_06` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_07` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_training_calibration_forbidden_08` | TRAINING_CALIBRATION_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_TRAINING_CALIBRATION_OR_MODEL_IMPROVEMENT` |
| `mlrt73_registry_pilot_copilot_forbidden_01` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_02` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_03` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_04` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_05` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_06` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_07` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |
| `mlrt73_registry_pilot_copilot_forbidden_08` | REGISTRY_PILOT_COPILOT_FORBIDDEN | `NO_AUTHORITATIVE_ROUTE` | `CONTAIN_REGISTRY_PILOT_COPILOT_OR_MATURITY_JUMP` |

## Boundary status

This is still validation-only evidence. It is not reliability, maturity, production readiness, route authority, model improvement, training, calibration, registry mutation, runtime Pilot, or Copilot evidence.

Positive state: `RSS_MLRT73_INCREASED_VOLUME_MIXED_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE`

Next safe milestone: `Routing Signal Scorer MLRT-74 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1`
