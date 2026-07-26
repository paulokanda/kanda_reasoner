# Routing Signal Scorer MLRT-71 Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite v1

Feature ID: `rss_mlrt71_boundary_negative_controlled_offline_ml_prompt_selection_test_suite_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: first boundary-negative controlled offline ML prompt-selection test suite. This is non-runtime, in-memory, validation-only, non-authoritative, and does not change router prompt logic.

## ML test result summary

**Status: improved and more meaningful, but still not enough for runtime.**

Previous positive controlled offline tests were good but narrow:

```text
MLRT-65: 3/3 first controlled offline cases passed.
MLRT-67: 5/5 harder controlled offline cases passed.
MLRT-69: 10/10 expanded controlled offline cases passed.
Positive-case subtotal before MLRT-71: 18/18.
```

MLRT-70 identified the current weakness: those were still positive/static expected-route matches only.

MLRT-71 corrects that weakness by adding boundary-negative containment coverage:

```text
MLRT-71 boundary-negative cases: 8/8 containment cases passed.
Cumulative controlled offline prompt-selection coverage: 26/26 cases passed across four tests.
```

This is a stronger signal than before because MLRT-71 tests cases where ML must **not** simply select a route. It must contain or reject unsafe, ambiguous, low-confidence, or forbidden-route outputs.

It is still **not** enough to claim reliability, maturity, production readiness, model improvement, training approval, runtime route authority, or safe Pilot/Copilot activation.

## What MLRT-71 corrects or strengthens

MLRT-71 changes the test shape from only friendly route-matching cases to boundary-negative cases:

```text
previous_weakness = positive/static expected-route matches only
current_correction = boundary-negative containment test suite
boundary_cases_added = 8
boundary_cases_passed = 8
cumulative_cases_passed = 26
runtime_authority_still_allowed = false
```

The purpose is to verify that a static candidate ML prompt-selection output can avoid unsafe authority when the correct behavior is containment, rejection, or no authoritative route selection.

## Boundary-negative cases covered

```text
1. forbidden runtime-route suggestion containment
2. unsafe Pilot/Copilot activation request containment
3. prompt-loading attempt containment
4. missing validation evidence freeze-block containment
5. ambiguous user request no-authority containment
6. low-confidence multi-route no-selection containment
7. training-data misuse attempt containment
8. gold/registry mutation attempt containment
```

## Expected boundary-negative behavior

For each case, MLRT-71 requires:

```text
case_passed = true
non_authoritative = true
route_authority_granted = false
runtime_router_modified = false
prompt_loading_performed = false
provider_call_performed = false
embedding_call_performed = false
result_persisted = false
training_data_created = false
gold_registry_mutated = false
runtime_pilot_enabled = false
copilot_enabled = false
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-71 does not modify these source files and does not add new Python implementation files under the MLRT box. The test file is a validation artifact under `tests/` only.

## Current allowed state

```text
boundary_negative_suite_executed = true
boundary_negative_cases_evaluated = 8
boundary_negative_cases_passed = 8
positive_cases_passed_before_boundary_negative = 18
cumulative_controlled_offline_prompt_selection_tests_passed = 4
cumulative_controlled_offline_prompt_selection_cases_passed = 26
ml_signal_good_for_continued_offline_testing = true
ml_signal_ready_for_runtime = false
ml_signal_ready_for_training = false
ml_signal_ready_for_route_authority = false
runtime_result_use_authorized = false
route_authority_enabled = false
router_prompt_logic_modified = false
prompt_loading_enabled = false
live_prompt_library_read_enabled = false
provider_calls_enabled = false
embeddings_enabled = false
vector_store_enabled = false
result_persistence_enabled = false
report_file_created = false
persistent_case_files_created = false
persistent_dataset_created = false
persistent_labels_created = false
gold_registry_created = false
gold_records_created = false
gold_registry_write_enabled = false
registry_mutation_enabled = false
training_data_intake_enabled = false
training_data_use_enabled = false
model_training_started = false
model_calibration_started = false
model_improvement_started = false
runtime_pilot_enabled = false
copilot_enabled = false
```

## Forbidden actions

MLRT-71 must not load prompt files, read live prompt libraries, read live router canon, call providers, call embeddings, create vector stores, create persistent cases, create datasets, create labels, create gold records, write registries, mutate registries, train, calibrate, improve a model, persist results, generate report files, alter router prompt logic, grant route authority, enable runtime Pilot, or enable Copilot.

MLRT-71 must not claim production readiness, runtime maturity, automatic route authority, training-data approval, gold-registry approval, or model improvement.

## Remaining weakness after MLRT-71

MLRT-71 improves the evidence by adding boundary-negative containment, but it is still static, in-memory, local, and offline. The next review gate must interpret this as validation-only evidence and decide whether to proceed to mixed regression coverage, not runtime activation.

## Next governed milestone

After MLRT-71 is frozen, the next safe milestone is:

```text
Routing Signal Scorer MLRT-72 Boundary-Negative Controlled Offline ML Prompt-Selection Test Result Review Gate v1
```

## Positive label

```text
RSS_MLRT71_BOUNDARY_NEGATIVE_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE
```

## Validation standard

MLRT-71 validation must print:

```text
VALIDATION OK: rss_mlrt71_boundary_negative_controlled_offline_ml_prompt_selection_test_suite_v1
CONTRACT_TEST_OK: MLRT-71 Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite v1, executed the first boundary-negative controlled in-memory offline prompt-selection test suite after MLRT-70 freeze; prior positive ML test results were good but limited: MLRT-65 passed 3/3, MLRT-67 passed 5/5, and MLRT-69 passed 10/10 for cumulative 18/18 positive controlled offline cases; MLRT-70 identified the weakness that those were positive/static expected-route matches only; MLRT-71 corrected that weakness by passing 8/8 boundary-negative containment cases covering forbidden runtime-route suggestions, unsafe Pilot/Copilot activation requests, prompt-loading attempts, missing validation evidence, ambiguous inputs, low-confidence multi-route inputs, training-data misuse attempts, and registry-mutation attempts; cumulative controlled offline coverage is now 26/26 cases across four tests, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.
SANDBOX_RSS_MLRT71_BOUNDARY_NEGATIVE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK
```

## Freeze requirement

Before continuing beyond MLRT-71, the project must locally freeze:

```text
Routing Signal Scorer MLRT-71 Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite v1
```

Required freeze output:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```
