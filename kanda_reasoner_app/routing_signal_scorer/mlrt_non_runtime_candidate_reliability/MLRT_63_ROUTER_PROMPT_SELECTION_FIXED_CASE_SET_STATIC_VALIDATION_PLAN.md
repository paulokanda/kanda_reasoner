# Routing Signal Scorer MLRT-63 Router Prompt Selection Fixed Case Set Static Validation Plan v1

Feature ID: `rss_mlrt63_router_prompt_selection_fixed_case_set_static_validation_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation/test patch for a future **router prompt-selection fixed case set static validation plan**.

## Purpose

MLRT-63 stays on the direct path to the final goal: **ML must be tested for helping prompt selection in router prompt logic**. This milestone defines the future static validation plan for a fixed router prompt-selection case set. It does **not** create a fixed case set. It does **not** create case files. It does **not** implement a validator. It does **not** run static validation. It does **not** execute cases. It does **not** score candidate output. It does **not** compare routes. It does **not** generate reports. It does **not** train, calibrate, learn, persist, mutate registries, grant route authority, load prompts, enable Pilot, or enable Copilot behavior.

The purpose is narrow: define what a future static validator must check before any fixed prompt-selection case set can be used by a later non-runtime offline evaluation harness.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-63 may begin only because MLRT-62 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-63 router prompt-selection fixed case set static validation plan.

After MLRT-63 is frozen, the count is: **1 step to the testing harness, 2 steps to the first real ML prompt-selection test**.

## Focused path to testing

```text
MLRT-63 -> fixed case set static validation plan only
MLRT-64 -> non-runtime offline evaluation harness plan/source gate
MLRT-65 -> first controlled offline prompt-selection test
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-63 must not modify these source files and must not add new Python implementation files.

## Future static validation plan

A future static validator, if later approved and implemented, must inspect only an approved fixed prompt-selection case set artifact. It must not execute the ML candidate. It must not call providers. It must not load live prompts. It must not compare candidate outputs. It must not score cases. It must not produce reliability claims. It must not mutate gold or registry records. It must not write training records.

The future static validation plan should require these validation groups:

```text
manifest_identity_check: confirms case_set_id, case_set_version, case_schema_version, purpose, and freeze reference are present.
schema_compatibility_check: confirms the set claims the MLRT-61 prompt-selection case schema version.
case_index_shape_check: confirms each future case reference has stable id, scenario text reference, expected route labels, boundary expectations, and review state.
expected_route_label_check: confirms expected primary prompt group labels are explicit and not generated from candidate outputs.
accepted_alternate_route_check: confirms alternates are explicit and reviewed.
forbidden_route_check: confirms routes that must be rejected are explicit.
boundary_expectation_check: confirms no prompt loading, no provider calls, no embeddings, no persistence, no route authority, no Pilot, and no Copilot.
critical_failure_check: confirms critical boundary failures override soft accuracy.
provenance_check: confirms the case set is human-reviewed and not automatically derived from project prompts, freeze memory, user logs, validation logs, comments, docstrings, candidate outputs, or LAB fixed cases.
checksum_freeze_check: confirms checksum/freeze references are present before use by a future harness.
static_validation_output_check: future validator output must be pass/fail only, not score, report, reliability result, training record, or registry mutation.
```

These are **planned validation groups only**. MLRT-63 creates no validator file, no validation output, no JSON, no YAML, no CSV, no Python validator, no case content, no labels, no candidate output, no score, no route comparison, no report, no registry record, and no training data.

## Current allowed state

```text
router_prompt_selection_fixed_case_set_static_validation_planned = true
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
static_validator_created = false
static_validation_run_enabled = false
static_validation_output_created = false
fixed_case_set_created = false
fixed_case_set_file_created = false
fixed_prompt_selection_case_set_created = false
prompt_selection_cases_created = false
prompt_selection_labels_created = false
prompt_selection_gold_cases_created = false
prompt_selection_candidate_outputs_created = false
prompt_selection_scoring_enabled = false
route_comparison_enabled = false
offline_evaluation_run_enabled = false
case_execution_enabled = false
case_scoring_enabled = false
report_generation_enabled = false
training_data_use_enabled = false
training_data_intake_enabled = false
training_dataset_created = false
model_learning_started = false
model_training_started = false
model_calibration_started = false
model_improvement_started = false
controlled_learning_experiment_started = false
learning_sandbox_enabled = false
persistence_enabled = false
route_authority_enabled = false
prompt_loading_enabled = false
provider_calls_enabled = false
embeddings_enabled = false
runtime_pilot_enabled = false
copilot_enabled = false
```

## Forbidden actions

MLRT-63 must not create static validators, validator output records, fixed case set files, JSON/YAML/CSV case artifacts, Python case objects, prompt-selection cases, labels, expected-route records, gold records, registry writers, mutation proposals, candidate outputs, scoring functions, route comparison logic, report generators, training datasets, calibration datasets, learning inputs, learning outputs, data loaders, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, prompt loading, or route authority.

MLRT-63 must not claim static validation passed, fixed-case readiness, fixed-case-set implementation readiness, evaluation readiness, scoring readiness, prompt-selection reliability, model reliability, candidate reliability, route readiness, production readiness, or runtime readiness.

## Explicit non-case and non-validator status

The current project may contain MLRT-61 schema planning text, MLRT-62 fixed case set format planning text, prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, learning sandbox plan text, controlled learning experiment plan text, and freeze memory. None of these are fixed prompt-selection cases. None are labels. None are static validation outputs. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-63.

## Future governed milestones

MLRT-63 only authorizes the next narrow planning milestone:

```text
MLRT-64 -> Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan
```

A practical count after MLRT-63 freeze:

```text
1 step to the testing harness: MLRT-64
2 steps to the first real ML prompt-selection test: MLRT-64, MLRT-65
```

None of these future steps may be treated as already approved by MLRT-63.

## Positive label

The only positive MLRT-63 label is:

```text
RSS_MLRT63_PROMPT_SELECTION_FIXED_CASE_SET_STATIC_VALIDATION_PLANNED_NO_VALIDATOR_NO_CASE_SET
```

This label means the future static validation boundary for router prompt-selection fixed case sets is documented and tested while all static validator implementation, validator output creation, case set creation, case creation, label creation, candidate output creation, scoring, route comparison, evaluation execution, report generation, persistence, model learning, model training, model calibration, model improvement, gold mutation, route authority, prompt loading, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-63 validation must confirm:

```text
VALIDATION OK: rss_mlrt63_router_prompt_selection_fixed_case_set_static_validation_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-63, the project must locally freeze:

```text
Routing Signal Scorer MLRT-63 Router Prompt Selection Fixed Case Set Static Validation Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-64 Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan v1`.
