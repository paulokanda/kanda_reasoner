# Routing Signal Scorer MLRT-62 Router Prompt Selection Fixed Case Set Format Plan v1

Feature ID: `rss_mlrt62_router_prompt_selection_fixed_case_set_format_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation/test patch for a future **router prompt-selection fixed case set format**.

## Purpose

MLRT-62 stays on the direct path to the final goal: **ML must be tested for helping prompt selection in router prompt logic**. This milestone defines the future fixed case set format plan for router prompt-selection offline evaluation cases. It does **not** create the fixed case set. It does **not** create case files. It does **not** create labels. It does **not** execute cases. It does **not** score candidate output. It does **not** compare routes. It does **not** generate reports. It does **not** train, calibrate, learn, persist, mutate registries, grant route authority, load prompts, enable Pilot, or enable Copilot behavior.

The purpose is narrow: define the container/format that a future fixed prompt-selection case set must use so later controlled testing can compare ML/candidate prompt-route selection against expected prompt route labels.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-62 may begin only because MLRT-61 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-62 router prompt-selection fixed case set format plan.

After MLRT-62 is frozen, the count is: **2 steps to the testing harness, 3 steps to the first real ML prompt-selection test**.

## Focused path to testing

```text
MLRT-62 -> fixed prompt-selection case set format plan only
MLRT-63 -> fixed case set static validation plan, no ML execution
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

MLRT-62 must not modify these source files and must not add new Python implementation files.

## Future fixed case set format plan

A future fixed case set, if later approved and implemented, must be a frozen, reviewed, non-training, non-runtime prompt-selection test artifact. It must not be loaded by runtime routing. It must not be treated as training data. It must not mutate any gold registry. It must not imply route authority.

The future fixed case set format should contain these proposed sections:

```text
case_set_id: stable future identifier for the fixed prompt-selection case set.
case_set_version: explicit version for the set.
case_schema_version: version of the MLRT-61 prompt-selection case schema the set conforms to.
case_set_purpose: router prompt-selection offline evaluation only.
case_count: number of future fixed cases.
case_index: ordered references to future cases, not case content created by MLRT-62.
expected_primary_prompt_groups_index: aggregate view of expected primary route labels.
accepted_alternate_prompt_groups_index: aggregate view of allowed alternates.
forbidden_prompt_groups_index: aggregate view of routes that must be rejected.
boundary_expectation_index: aggregate required locks for no prompt loading, no provider calls, no embeddings, no persistence, no route authority, no Pilot, and no Copilot.
critical_failure_index: explicit critical failures that override soft accuracy.
human_review_record: future explicit review status before a set can become fixed.
provenance_record: future approved origin record, without treating project logs, freeze memory, source comments, docstrings, or LAB fixed cases as automatic source material.
checksum_record: future immutable checksum/hash record after approved set creation.
freeze_record_reference: future freeze ID only after approved local freeze.
```

These are **planned format sections only**. MLRT-62 creates no fixed case set file, no JSON, no YAML, no CSV, no Python object, no case content, no labels, no candidate output, no score, no route comparison, no report, no registry record, and no training data.

## Current allowed state

```text
router_prompt_selection_fixed_case_set_format_planned = true
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
fixed_case_set_format_created = false
fixed_case_set_file_created = false
fixed_case_set_validator_created = false
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

MLRT-62 must not create fixed case set files, JSON/YAML/CSV case artifacts, Python case objects, validators, prompt-selection cases, labels, expected-route records, gold records, registry writers, mutation proposals, candidate outputs, scoring functions, route comparison logic, report generators, training datasets, calibration datasets, learning inputs, learning outputs, data loaders, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, prompt loading, or route authority.

MLRT-62 must not claim fixed-case readiness, fixed-case-set implementation readiness, validation readiness, evaluation readiness, scoring readiness, prompt-selection reliability, model reliability, candidate reliability, route readiness, production readiness, or runtime readiness.

## Explicit non-case status

The current project may contain MLRT-61 schema planning text, prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, learning sandbox plan text, controlled learning experiment plan text, and freeze memory. None of these are fixed prompt-selection cases. None are labels. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-62.

## Future governed milestones

MLRT-62 only authorizes the next narrow planning milestone:

```text
MLRT-63 -> Router Prompt Selection Fixed Case Set Static Validation Plan
```

A practical count after MLRT-62 freeze:

```text
2 steps to the testing harness: MLRT-63, MLRT-64
3 steps to the first real ML prompt-selection test: MLRT-63, MLRT-64, MLRT-65
```

None of these future steps may be treated as already approved by MLRT-62.

## Positive label

The only positive MLRT-62 label is:

```text
RSS_MLRT62_PROMPT_SELECTION_FIXED_CASE_SET_FORMAT_PLANNED_NO_CASE_SET_NO_EVALUATION
```

This label means the future fixed case set format boundary for router prompt selection is documented and tested while all case set creation, case creation, label creation, candidate output creation, scoring, route comparison, evaluation execution, report generation, persistence, model learning, model training, model calibration, model improvement, gold mutation, route authority, prompt loading, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-62 validation must confirm:

```text
VALIDATION OK: rss_mlrt62_router_prompt_selection_fixed_case_set_format_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-62, the project must locally freeze:

```text
Routing Signal Scorer MLRT-62 Router Prompt Selection Fixed Case Set Format Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-63 Router Prompt Selection Fixed Case Set Static Validation Plan v1`.
