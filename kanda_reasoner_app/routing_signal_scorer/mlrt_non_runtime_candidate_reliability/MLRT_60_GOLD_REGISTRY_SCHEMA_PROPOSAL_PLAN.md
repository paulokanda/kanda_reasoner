# Routing Signal Scorer MLRT-60 Gold Registry Schema Proposal Plan v1

Feature ID: `rss_mlrt60_gold_registry_schema_proposal_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation/test patch for a future **router prompt-selection gold registry schema proposal**.

## Purpose

MLRT-60 keeps the work focused on the final goal: **ML must be tested to help prompt selection in router prompt logic**. This milestone defines a future gold registry schema proposal for prompt-selection evaluation records only. It does **not** create a gold registry implementation. It does **not** create a schema file. It does **not** create gold records. It does **not** create evaluation cases. It does **not** run evaluation. It does **not** score candidate prompt-selection decisions. It does **not** compare routes. It does **not** train, calibrate, learn, persist, mutate registries, grant route authority, load prompts, enable Pilot, or enable Copilot behavior.

The purpose is narrow: define the future fields that a later governed gold registry schema must include so ML/router candidate behavior can eventually be tested against expected prompt-selection outcomes without granting runtime authority.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-60 may begin only because MLRT-59 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-60 gold registry schema proposal plan.

The safe sequence remains focused:

```text
MLRT-52 -> LAB reliability fixed-case test
MLRT-53 -> Item 5 training/learning governance planning only
MLRT-54 -> training-data boundary planning only
MLRT-55 -> gold registry mutation gate planning only
MLRT-56 -> offline evaluation protocol planning only
MLRT-57 -> calibration-only dry-run planning only
MLRT-58 -> learning sandbox planning only
MLRT-59 -> first controlled learning experiment planning only
MLRT-60 -> prompt-selection gold registry schema proposal planning only
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-60 must not modify these source files and must not add new Python implementation files.

## Future prompt-selection gold schema proposal

MLRT-60 proposes that a later governed schema, if approved, must be scoped to router prompt-selection testing and include at minimum these future field groups:

```text
case_identity: stable future case identifier and version.
user_intent_summary: normalized description of the user request being routed.
routing_signal_summary: non-authoritative signals available to the router prompt logic.
expected_primary_prompt_group: the intended prompt group or route target.
accepted_alternate_prompt_groups: bounded acceptable prompt groups when more than one route is valid.
forbidden_prompt_groups: prompt groups that must not be selected for this case.
selection_rationale_requirements: evidence a candidate must preserve when explaining why a prompt group was selected.
boundary_expectations: expected safety/governance locks such as no provider calls, no prompt loading, no route authority, and no persistence.
critical_failure_conditions: conditions that invalidate a candidate even when soft prompt-selection accuracy appears high.
human_review_status: future human-review state required before any record can become gold.
provenance_summary: future origin metadata for the case, without treating project prompts, freeze memory, logs, source comments, or LAB fixed cases as gold by default.
```

These are **proposal fields only**. MLRT-60 creates no JSON schema, no Python schema, no registry file, no registry writer, no gold cases, and no truth labels.

## Current allowed state

MLRT-60 may only document and test the prompt-selection gold schema proposal boundary. It may update the MLRT README, MLRT governance document, manifest metadata, and validation test.

All actual schema, registry, gold, data, evaluation, learning, training, calibration, prompt-loading, and runtime capabilities remain false:

```text
gold_registry_schema_proposal_defined = true
prompt_selection_focus_preserved = true
ml_prompt_selection_testing_goal_preserved = true
gold_registry_schema_created = false
gold_registry_created = false
gold_records_created = false
gold_record_labels_created = false
gold_registry_writer_created = false
gold_registry_mutation_enabled = false
gold_registry_mutated = false
gold_schema_file_created = false
prompt_selection_gold_cases_created = false
prompt_selection_gold_labels_created = false
prompt_selection_evaluation_cases_created = false
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
training_labels_created = false
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

MLRT-60 must not create schema files, JSON schema artifacts, Python schema code, validators, gold registries, gold records, gold labels, prompt-selection cases, prompt-selection labels, registry writers, mutation proposals, mutation diffs, rollback records, evaluation cases, candidate outputs, scoring functions, route comparison logic, report generators, training datasets, calibration datasets, learning inputs, learning outputs, data loaders, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, prompt loading, or route authority.

MLRT-60 must not claim schema readiness, gold registry readiness, evaluation readiness, scoring readiness, prompt-selection reliability, model reliability, candidate reliability, learned reliability, route readiness, production readiness, or runtime readiness.

## Explicit non-gold status

The current project may contain prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, learning sandbox plan text, controlled learning experiment plan text, and freeze memory. None of these are gold records. None are prompt-selection gold cases. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-60.

## Future governed milestones

MLRT-60 only authorizes the following roadmap labels. Each requires a separate future patch, validation, and freeze:

```text
MLRT-61 -> Router Prompt Selection Offline Evaluation Case Schema Plan
MLRT-62 -> Prompt Selection Expected Outcome Boundary Plan
MLRT-63 -> Prompt Selection Candidate Output Envelope Plan
MLRT-64 -> Prompt Selection Scoring Boundary Plan
MLRT-65 -> Prompt Selection Non-Runtime Test Harness Plan
```

None of these future steps may be treated as already approved by MLRT-60.

## Positive label

The only positive MLRT-60 label is:

```text
RSS_MLRT60_PROMPT_SELECTION_GOLD_SCHEMA_PROPOSAL_DEFINED_NO_SCHEMA_NO_GOLD
```

This label means the future prompt-selection gold schema proposal boundary is documented and tested while all schema creation, registry creation, gold record creation, prompt-selection case creation, scoring, route comparison, evaluation execution, report generation, persistence, model learning, model training, model calibration, model improvement, gold mutation, route authority, prompt loading, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-60 validation must confirm:

```text
VALIDATION OK: rss_mlrt60_gold_registry_schema_proposal_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-60, the project must locally freeze:

```text
Routing Signal Scorer MLRT-60 Gold Registry Schema Proposal Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-61 Router Prompt Selection Offline Evaluation Case Schema Plan v1`.
