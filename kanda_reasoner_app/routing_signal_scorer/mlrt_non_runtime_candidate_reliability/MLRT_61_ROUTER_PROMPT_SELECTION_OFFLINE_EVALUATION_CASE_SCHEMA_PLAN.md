# Routing Signal Scorer MLRT-61 Router Prompt Selection Offline Evaluation Case Schema Plan v1

Feature ID: `rss_mlrt61_router_prompt_selection_offline_evaluation_case_schema_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation/test patch for a future **router prompt-selection offline evaluation case schema**.

## Purpose

MLRT-61 keeps the work on the direct path to the final goal: **ML must be tested for helping prompt selection in router prompt logic**. This milestone defines the future offline evaluation case schema plan for prompt-selection cases only. It does **not** create the schema file. It does **not** create cases. It does **not** create labels. It does **not** execute cases. It does **not** score candidate output. It does **not** compare routes. It does **not** generate reports. It does **not** train, calibrate, learn, persist, mutate registries, grant route authority, load prompts, enable Pilot, or enable Copilot behavior.

The purpose is narrow: define what a future offline prompt-selection evaluation case must contain so a later governed harness can test whether ML/candidate logic helps choose the correct router prompt group.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-61 may begin only because MLRT-60 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-61 router prompt-selection offline evaluation case schema plan.

The path to first testing is now:

```text
MLRT-61 -> offline evaluation case schema plan only
MLRT-62 -> fixed prompt-selection case set format plan only
MLRT-63 -> fixed case validation plan, no ML execution
MLRT-64 -> non-runtime offline evaluation harness plan
MLRT-65 -> first controlled offline prompt-selection test plan/execution gate
```

After MLRT-61 is frozen, the count is: **3 steps to the testing harness, 4 steps to the first real ML prompt-selection test**.

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-61 must not modify these source files and must not add new Python implementation files.

## Future prompt-selection offline evaluation case schema plan

A future prompt-selection offline evaluation case, if later approved and implemented, must be about router prompt selection only. It must not be a training record, not a runtime decision, not a prompt-load instruction, and not a gold registry mutation.

The future case schema should contain these proposed field groups:

```text
case_id: stable future case identifier.
case_version: explicit future case version.
user_request_text: the user-facing request text to be routed, stored only in a future approved case corpus.
normalized_user_intent: concise intent label or description.
required_context_signals: non-authoritative context signals expected to matter for prompt selection.
forbidden_context_assumptions: assumptions the candidate must not invent.
expected_primary_prompt_group: the expected prompt group or route target.
accepted_alternate_prompt_groups: bounded acceptable alternatives when multiple routes are valid.
forbidden_prompt_groups: prompt groups that must not be selected.
expected_routing_reason: minimal explanation/evidence a candidate must preserve.
boundary_expectations: governance locks expected to remain false, including no prompt loading, no provider calls, no embeddings, no persistence, no route authority, no Pilot, and no Copilot.
critical_failure_conditions: failures that invalidate the candidate even if the prompt group appears superficially correct.
human_review_state: future human-review status before any case may become gold or fixed.
provenance_note: origin note for future approved case creation, without treating project freeze memory, logs, source comments, docstrings, or LAB fixed cases as automatic case material.
```

These are **planned field groups only**. MLRT-61 creates no JSON schema, Python schema, validator, case file, case corpus, gold record, label, candidate output, score, route comparison, or report.

## Current allowed state

```text
router_prompt_selection_offline_case_schema_planned = true
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
offline_evaluation_case_schema_created = false
offline_evaluation_case_schema_file_created = false
offline_evaluation_case_validator_created = false
offline_evaluation_cases_created = false
fixed_prompt_selection_case_set_created = false
prompt_selection_labels_created = false
prompt_selection_gold_cases_created = false
prompt_selection_gold_records_created = false
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

MLRT-61 must not create schema files, JSON schema artifacts, Python schema code, validators, prompt-selection cases, fixed case sets, labels, gold records, gold registries, registry writers, mutation proposals, evaluation cases, candidate outputs, scoring functions, route comparison logic, report generators, training datasets, calibration datasets, learning inputs, learning outputs, data loaders, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, prompt loading, or route authority.

MLRT-61 must not claim schema implementation readiness, case corpus readiness, fixed-case readiness, evaluation readiness, scoring readiness, prompt-selection reliability, model reliability, candidate reliability, route readiness, production readiness, or runtime readiness.

## Explicit non-case status

The current project may contain prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, learning sandbox plan text, controlled learning experiment plan text, and freeze memory. None of these are prompt-selection evaluation cases. None are labels. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-61.

## Future governed milestones

MLRT-61 only authorizes the next narrow planning milestone:

```text
MLRT-62 -> Router Prompt Selection Fixed Case Set Format Plan
```

A practical count after MLRT-61 freeze:

```text
3 steps to the testing harness: MLRT-62, MLRT-63, MLRT-64
4 steps to the first real ML prompt-selection test: MLRT-62, MLRT-63, MLRT-64, MLRT-65
```

None of these future steps may be treated as already approved by MLRT-61.

## Positive label

The only positive MLRT-61 label is:

```text
RSS_MLRT61_PROMPT_SELECTION_OFFLINE_CASE_SCHEMA_PLANNED_NO_CASES_NO_EVALUATION
```

This label means the future offline evaluation case schema boundary for router prompt selection is documented and tested while all schema file creation, case creation, fixed case-set creation, label creation, candidate output creation, scoring, route comparison, evaluation execution, report generation, persistence, model learning, model training, model calibration, model improvement, gold mutation, route authority, prompt loading, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-61 validation must confirm:

```text
VALIDATION OK: rss_mlrt61_router_prompt_selection_offline_evaluation_case_schema_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-61, the project must locally freeze:

```text
Routing Signal Scorer MLRT-61 Router Prompt Selection Offline Evaluation Case Schema Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-62 Router Prompt Selection Fixed Case Set Format Plan v1`.
