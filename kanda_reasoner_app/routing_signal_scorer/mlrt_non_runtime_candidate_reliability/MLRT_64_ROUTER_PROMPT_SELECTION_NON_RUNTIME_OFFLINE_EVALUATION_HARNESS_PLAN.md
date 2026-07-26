# Routing Signal Scorer MLRT-64 Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan v1

Feature ID: `rss_mlrt64_router_prompt_selection_non_runtime_offline_evaluation_harness_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation/test patch for a future **router prompt-selection non-runtime offline evaluation harness plan**.

## Purpose

MLRT-64 stays on the direct path to the final goal: **ML must be tested for helping prompt selection in router prompt logic**. This milestone defines the future non-runtime offline evaluation harness plan for router prompt-selection cases. It does **not** implement the harness. It does **not** create a runner. It does **not** create fixed cases. It does **not** create labels. It does **not** execute a candidate. It does **not** score cases. It does **not** compare routes. It does **not** generate reports. It does **not** train, calibrate, learn, persist, mutate registries, grant route authority, load prompts, enable Pilot, or enable Copilot behavior.

The purpose is narrow: define what the next controlled offline test must be allowed to do, and what it must still never do, so the first real prompt-selection test can be scoped without drifting into runtime router authority.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-64 may begin only because MLRT-63 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-64 router prompt-selection non-runtime offline evaluation harness plan.

After MLRT-64 is frozen, the count is: **0 remaining planning steps to the testing-harness gate, 1 step to the first real controlled ML prompt-selection test**.

## Focused path to testing

```text
MLRT-64 -> non-runtime offline evaluation harness plan/gate only
MLRT-65 -> first controlled offline ML prompt-selection test
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-64 must not modify these source files and must not add new Python implementation files.

## Future non-runtime offline evaluation harness plan

A future harness, if later approved, must be **non-runtime, read-only, explicit-input, and non-authoritative**. It may only operate on fixed prompt-selection cases that a future approved milestone explicitly provides. It may only compare a bounded candidate prompt-selection output against expected prompt-route labels that are explicitly supplied by the approved fixed case set. It must not load live project prompts. It must not call providers. It must not use embeddings. It must not discover cases. It must not create labels. It must not mutate gold or registry records. It must not train, calibrate, improve, persist, or route live user requests.

The future harness plan must include these gates:

```text
harness_identity_gate: confirms harness id, version, scope, and non-runtime status.
fixed_case_set_gate: accepts only a separately approved fixed prompt-selection case set; no discovery and no generation.
candidate_output_envelope_gate: accepts only explicit candidate output envelopes supplied to the harness; no candidate execution by default.
expected_route_label_gate: compares against human-reviewed expected prompt-route labels only.
accepted_alternate_route_gate: handles explicitly reviewed alternates without creating new labels.
forbidden_route_gate: treats forbidden route hits as critical failures.
boundary_failure_gate: critical boundary failures override soft prompt-selection accuracy.
read_only_result_gate: result is in-memory/read-only unless a later milestone explicitly allows report creation.
no_learning_gate: result is not training data, calibration data, model improvement data, or gold mutation input.
no_authority_gate: result cannot make live route decisions or change router prompt logic.
human_review_gate: first controlled test result must be reviewed before any later maturity claim.
```

These are **planned gates only**. MLRT-64 creates no harness file, no runner, no result object, no JSON, no YAML, no CSV, no Python harness, no case content, no labels, no candidate output, no score, no route comparison, no report, no registry record, and no training data.

## Current allowed state

```text
router_prompt_selection_non_runtime_offline_evaluation_harness_planned = true
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
testing_harness_gate_planned = true
remaining_planning_steps_to_testing_harness_gate = 0
remaining_steps_to_first_real_ml_prompt_selection_test = 1
offline_evaluation_harness_created = false
offline_evaluation_harness_source_created = false
offline_evaluation_runner_created = false
offline_evaluation_run_enabled = false
offline_evaluation_run_executed = false
fixed_case_set_created = false
fixed_case_set_file_created = false
prompt_selection_cases_created = false
prompt_selection_labels_created = false
candidate_output_envelope_created = false
candidate_execution_enabled = false
candidate_output_created = false
expected_route_comparison_enabled = false
prompt_selection_scoring_enabled = false
case_execution_enabled = false
case_scoring_enabled = false
route_comparison_enabled = false
report_generation_enabled = false
result_persistence_enabled = false
reliability_claim_enabled = false
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

MLRT-64 must not create offline evaluation harness source, runner source, case set files, JSON/YAML/CSV case artifacts, Python case objects, prompt-selection cases, labels, expected-route records, gold records, registry writers, mutation proposals, candidate outputs, scoring functions, route comparison logic, report generators, training datasets, calibration datasets, learning inputs, learning outputs, data loaders, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, prompt loading, or route authority.

MLRT-64 must not claim that a harness exists, an offline evaluation ran, prompt-selection testing started, prompt-selection accuracy was measured, model reliability was validated, candidate reliability was validated, router prompt logic improved, production readiness exists, or runtime routing is allowed.

## Explicit non-harness and non-test status

The current project may contain MLRT-61 schema planning text, MLRT-62 fixed case set format planning text, MLRT-63 static validation planning text, prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, learning sandbox plan text, controlled learning experiment plan text, and freeze memory. None of these are a non-runtime offline evaluation harness. None are fixed prompt-selection cases. None are labels. None are candidate outputs. None are offline evaluation results. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-64.

## Future governed milestone

MLRT-64 only authorizes the next narrow milestone:

```text
MLRT-65 -> First Controlled Offline ML Prompt-Selection Test
```

A practical count after MLRT-64 freeze:

```text
0 remaining planning steps to the testing-harness gate
1 step to the first real controlled ML prompt-selection test: MLRT-65
```

MLRT-65 must still remain non-runtime, offline, controlled, and non-authoritative unless a later governed scope explicitly changes that. MLRT-64 does not pre-authorize runtime route authority, prompt loading, provider calls, training, calibration, persistence, Pilot, or Copilot.

## Positive label

The only positive MLRT-64 label is:

```text
RSS_MLRT64_PROMPT_SELECTION_OFFLINE_EVALUATION_HARNESS_PLANNED_NO_HARNESS_NO_EXECUTION
```

This label means the future non-runtime offline evaluation harness boundary for router prompt selection is planned while all harness implementation, runner implementation, fixed case set creation, case creation, label creation, candidate output creation, scoring, route comparison, evaluation execution, report generation, persistence, model learning, model training, model calibration, model improvement, gold mutation, route authority, prompt loading, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-64 validation must confirm:

```text
VALIDATION OK: rss_mlrt64_router_prompt_selection_non_runtime_offline_evaluation_harness_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-64, the project must locally freeze:

```text
Routing Signal Scorer MLRT-64 Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-65 First Controlled Offline ML Prompt-Selection Test v1`.
