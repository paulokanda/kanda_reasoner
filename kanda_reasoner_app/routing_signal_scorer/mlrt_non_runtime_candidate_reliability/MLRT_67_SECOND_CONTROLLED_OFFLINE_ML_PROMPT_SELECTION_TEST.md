# Routing Signal Scorer MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1

Feature ID: `rss_mlrt67_second_controlled_offline_ml_prompt_selection_test_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed second controlled offline prompt-selection test. This is active testing, but it remains non-runtime, in-memory, validation-only, and non-authoritative.

## Purpose

MLRT-67 continues the practical testing track for the real goal: **ML must be tested for helping prompt selection in router prompt logic**.

MLRT-65 started testing. MLRT-66 reviewed that first test as acceptable evidence to continue offline testing. MLRT-67 now executes a second controlled offline comparison with five harder in-memory cases and static candidate ML prompt-selection outputs.

**Count after MLRT-67 freeze:** testing has already started. There are **0 steps to start testing**.

## What MLRT-67 allows

MLRT-67 allows only this narrow test-local behavior:

```text
five harder fixed in-memory prompt-selection cases: allowed inside tests only
static candidate ML prompt-selection outputs: allowed inside tests only
offline expected-route comparison: allowed inside tests only
offline prompt-selection score: allowed inside tests only
in-memory validation summary: allowed inside tests only
```

The comparison is not route authority. It is not runtime routing. It is not prompt loading. It is not a model call. It is not provider usage. It is not training. It is not calibration. It is not a persistent report. It is not a gold-registry write.

## Second test cases used by validation

The MLRT-67 validation test defines five harder prompt-selection cases in memory:

```text
mlrt67_freeze_with_validation_and_handoff_case -> expected route: 03_governance_freeze_and_handoff
mlrt67_prompt_authoring_bypass_case -> expected route: 07_prompt_authoring_and_audit
mlrt67_startup_after_freeze_context_case -> expected route: 01_session_start_and_navigation
mlrt67_prompt_router_index_update_case -> expected route: 02_prompt_routing_and_indexing
mlrt67_ml_router_reliability_case -> expected route: 052_routing_signal_scorer_v3_mlrt_world
```

These cases are harder than MLRT-65 because they include distractor signals, explicit bypass attempts, freeze/startup overlap, routing-index updates, and MLRT-specific router reliability language. A pass requires every static candidate output to avoid forbidden routes, avoid critical boundary flags, remain non-authoritative, and match either the expected primary route or an explicitly accepted alternate route.

These cases are not persisted as a dataset, corpus, gold registry, training data, calibration data, or runtime prompt-selection memory. They exist only as in-memory validation fixtures inside `tests/test_rss_mlrt67_second_controlled_offline_ml_prompt_selection_test.py`.

## Current result scope

A successful MLRT-67 validation means only:

```text
second_controlled_offline_prompt_selection_test_executed = true
second_controlled_offline_prompt_selection_test_passed = true
prompt_selection_cases_evaluated_in_memory = 5
prompt_selection_cases_passed = 5
cumulative_controlled_offline_tests_passed = 2
steps_to_start_testing = 0
```

It does not mean runtime ML is ready. It does not mean model reliability is validated. It does not mean the router prompt logic may use candidate outputs. It does not mean Pilot or Copilot may start. It does not permit training, calibration, data intake, prompt loading, provider calls, embeddings, persistence, or registry mutation.

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-67 does not modify these source files and does not add new Python implementation files under the MLRT box. The test file is a validation artifact under `tests/` only.

## Current allowed state

```text
second_controlled_offline_ml_prompt_selection_test_defined = true
second_controlled_offline_ml_prompt_selection_test_executed_by_validation = true
second_controlled_offline_ml_prompt_selection_test_passed_in_sandbox = true
testing_started = true
steps_to_start_testing = 0
cumulative_controlled_offline_tests_passed = 2
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
fixed_prompt_selection_cases_in_test_only = true
static_candidate_ml_outputs_in_test_only = true
offline_expected_route_comparison_in_test_only = true
offline_prompt_selection_score_in_test_only = true
in_memory_validation_summary_only = true
persistent_case_files_created = false
persistent_dataset_created = false
persistent_labels_created = false
gold_registry_created = false
gold_records_created = false
gold_registry_write_enabled = false
registry_mutation_enabled = false
report_file_created = false
result_persistence_enabled = false
runtime_route_authority_enabled = false
router_prompt_logic_modified = false
prompt_loading_enabled = false
live_prompt_library_read_enabled = false
provider_calls_enabled = false
embeddings_enabled = false
vector_store_enabled = false
training_data_intake_enabled = false
training_data_use_enabled = false
model_training_started = false
model_calibration_started = false
model_improvement_started = false
runtime_pilot_enabled = false
copilot_enabled = false
```

## Forbidden actions

MLRT-67 must not load prompt files, read live prompt libraries, read live router canon, call providers, call embeddings, create vector stores, create persistent cases, create datasets, create labels, create gold records, write registries, mutate registries, train, calibrate, improve a model, persist results, generate report files, alter router prompt logic, grant route authority, enable runtime Pilot, or enable Copilot.

MLRT-67 must not claim production readiness, runtime maturity, automatic route authority, training-data approval, gold-registry approval, or model improvement. MLRT-67 may only claim that the second controlled offline prompt-selection comparison passed in the validation harness.

## Next governed milestone

After MLRT-67 is frozen, the next safe milestone is:

```text
Routing Signal Scorer MLRT-68 Second Controlled Offline ML Prompt-Selection Test Result Review Gate v1
```

MLRT-68 should review the second test result and decide whether the second controlled offline test evidence is acceptable before expanding to a larger fixed suite, calibration-only dry-run, learning experiment, or router-integration planning.

## Positive label

```text
RSS_MLRT67_SECOND_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_PASSED_NON_RUNTIME_NON_AUTHORITATIVE
```

## Validation standard

MLRT-67 validation must print:

```text
VALIDATION OK: rss_mlrt67_second_controlled_offline_ml_prompt_selection_test_v1
CONTRACT_TEST_OK: MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1, executed the second controlled in-memory offline prompt-selection comparison using five harder fixed test cases and static candidate ML prompt-selection outputs after MLRT-66 freeze; preserved that testing has already started with 0 steps remaining to start testing; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; second controlled offline prompt-selection test passed; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.
SANDBOX_RSS_MLRT67_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_V1_VALIDATION_OK
```

## Freeze requirement

Before continuing beyond MLRT-67, the project must locally freeze:

```text
Routing Signal Scorer MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1
```

Required freeze output:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```
