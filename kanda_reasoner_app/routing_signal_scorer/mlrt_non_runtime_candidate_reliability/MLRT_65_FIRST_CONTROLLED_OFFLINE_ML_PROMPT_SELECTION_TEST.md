# Routing Signal Scorer MLRT-65 First Controlled Offline ML Prompt-Selection Test v1

Feature ID: `rss_mlrt65_first_controlled_offline_ml_prompt_selection_test_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed first controlled offline prompt-selection test. This is the first real controlled offline test in this chain. It is still non-runtime, in-memory, explicit, and non-authoritative.

## Purpose

MLRT-65 starts the practical testing track for the real goal: **ML must be tested for helping prompt selection in router prompt logic**.

This milestone executes a small controlled offline comparison in the validation test only. It uses fixed in-memory router prompt-selection cases and static candidate ML prompt-selection outputs. It checks whether the candidate-selected prompt route matches the expected prompt route while preserving all runtime, training, persistence, prompt-loading, provider, registry, Pilot, and Copilot locks.

**Count after MLRT-65 freeze:** testing has started. There are **0 steps to start testing**. The first controlled offline ML prompt-selection test has passed if validation prints the MLRT-65 validation markers.

## What MLRT-65 allows

MLRT-65 allows only this narrow test-local behavior:

```text
fixed in-memory prompt-selection cases: allowed inside tests only
static candidate ML prompt-selection outputs: allowed inside tests only
offline expected-route comparison: allowed inside tests only
offline prompt-selection score: allowed inside tests only
in-memory validation summary: allowed inside tests only
```

The allowed comparison is not route authority. It is not runtime routing. It is not prompt loading. It is not a model call. It is not provider usage. It is not training. It is not calibration. It is not a persistent report. It is not a gold-registry write.

## Fixed test cases used by validation

The MLRT-65 validation test defines three fixed prompt-selection cases in memory:

```text
mlrt65_freeze_workflow_case -> expected route: 03_governance_freeze_and_handoff
mlrt65_prompt_routing_case -> expected route: 02_prompt_routing_and_indexing
mlrt65_startup_context_case -> expected route: 01_session_start_and_navigation
```

Each case has accepted alternates and forbidden routes. The test also defines a matching static candidate output envelope for each case. A pass requires every candidate output to avoid forbidden routes, avoid critical boundary flags, and match either the expected primary route or an explicitly accepted alternate route.

These cases are not persisted as a dataset, corpus, gold registry, training data, calibration data, or runtime prompt-selection memory. They exist only as in-memory validation fixtures inside `tests/test_rss_mlrt65_first_controlled_offline_ml_prompt_selection_test.py`.

## Current result scope

MLRT-65 validation produces an in-memory test result only. The result is printed through the validation command and then disappears. It is not written to a report file, registry, dataset, gold store, vector store, cache, or prompt library.

A successful MLRT-65 validation means only:

```text
first_controlled_offline_prompt_selection_test_executed = true
first_controlled_offline_prompt_selection_test_passed = true
prompt_selection_cases_evaluated_in_memory = 3
prompt_selection_cases_passed = 3
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

MLRT-65 does not modify these source files and does not add new Python implementation files under the MLRT box. The test file is a validation artifact under `tests/` only.

## Current allowed state

```text
first_controlled_offline_ml_prompt_selection_test_defined = true
first_controlled_offline_ml_prompt_selection_test_executed_by_validation = true
first_controlled_offline_ml_prompt_selection_test_passed_in_sandbox = true
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
steps_to_start_testing = 0
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

MLRT-65 must not load prompt files, read live prompt libraries, read live router canon, call providers, call embeddings, create vector stores, create persistent cases, create datasets, create labels, create gold records, write registries, mutate registries, train, calibrate, improve a model, persist results, generate report files, alter router prompt logic, grant route authority, enable runtime Pilot, or enable Copilot.

MLRT-65 must not claim production readiness, runtime maturity, automatic route authority, training-data approval, gold-registry approval, or model improvement. MLRT-65 may only claim that the first controlled offline prompt-selection comparison passed in the validation harness.

## Next governed milestone

After MLRT-65 is frozen, the next safe milestone is:

```text
Routing Signal Scorer MLRT-66 Controlled Offline ML Prompt-Selection Test Result Review Gate v1
```

MLRT-66 should review the test result and decide whether the first controlled offline test evidence is acceptable before any expansion to more cases, harder cases, calibration, learning, or router integration planning.

## Positive label

```text
RSS_MLRT65_FIRST_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_PASSED_NON_RUNTIME_NON_AUTHORITATIVE
```

## Validation standard

MLRT-65 validation must print:

```text
VALIDATION OK: rss_mlrt65_first_controlled_offline_ml_prompt_selection_test_v1
CONTRACT_TEST_OK: MLRT-65 First Controlled Offline ML Prompt-Selection Test v1, executed the first controlled in-memory offline prompt-selection comparison using fixed test cases and static candidate ML prompt-selection outputs after MLRT-64 freeze; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; testing has now started with 0 steps remaining to start testing; first controlled offline prompt-selection test passed; no runtime routing, no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.
SANDBOX_RSS_MLRT65_FIRST_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_V1_VALIDATION_OK
```

## Freeze requirement

Before continuing beyond MLRT-65, the project must locally freeze:

```text
Routing Signal Scorer MLRT-65 First Controlled Offline ML Prompt-Selection Test v1
```

Required freeze output:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```
