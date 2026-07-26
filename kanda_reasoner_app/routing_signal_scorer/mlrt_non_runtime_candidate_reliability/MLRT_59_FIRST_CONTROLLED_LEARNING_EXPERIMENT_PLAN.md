# Routing Signal Scorer MLRT-59 First Controlled Learning Experiment Plan v1

Feature ID: `rss_mlrt59_first_controlled_learning_experiment_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed Item 5 first controlled learning experiment planning after MLRT-58 freeze.

## Purpose

MLRT-59 defines the **first controlled learning experiment plan** for a future governed milestone.

MLRT-59 does **not** create a controlled learning experiment implementation. It does **not** create an experiment runner. It does **not** create a sandbox workspace. It does **not** start or run a learning experiment. It does **not** create learning inputs. It does **not** create learning outputs. It does **not** create learning records or persist learning results. It does **not** start training-data intake, dataset creation, label creation, model training, model calibration, model improvement, offline evaluation execution, case execution, case scoring, route comparison, report generation, gold registry mutation, route authority, Pilot, or Copilot behavior.

The purpose is to define the minimum future proof required before any later patch may describe a controlled learning experiment envelope. A future experiment, if ever approved, must remain isolated, non-runtime, non-authoritative, non-training, non-gold, non-routing, non-persistent, and unable to change model behavior, route behavior, prompts, registries, gold records, training data, thresholds, weights, or runtime decisions.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-59 may begin only because MLRT-58 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-59 first controlled learning experiment plan.

The safe sequence is:

```text
MLRT-48 -> controlled minimal inert source creation
MLRT-49 -> static boundary test
MLRT-50 -> non-runtime harness smoke test
MLRT-51 -> candidate evaluation harness self-test
MLRT-52 -> LAB reliability fixed-case test
MLRT-53 -> Item 5 training/learning governance planning only
MLRT-54 -> training-data boundary planning only
MLRT-55 -> gold registry mutation gate planning only
MLRT-56 -> offline evaluation protocol planning only
MLRT-57 -> calibration-only dry-run planning only
MLRT-58 -> learning sandbox planning only
MLRT-59 -> first controlled learning experiment planning only
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-59 must not modify these source files and must not add new Python implementation files.

## Controlled learning experiment definitions

MLRT-59 fixes the following terms for later governed work:

```text
First controlled learning experiment plan: a documented future procedure for designing a single isolated non-runtime learning experiment without implementing it.
Controlled learning experiment: a future non-runtime, non-authoritative rehearsal; forbidden in MLRT-59.
Experiment runner: a future runner that could rehearse a controlled experiment; forbidden in MLRT-59.
Experiment envelope: a future static description of admitted inputs, expected observations, boundary locks, and non-authoritative outcome fields; forbidden in MLRT-59.
Experiment input: a future non-training, non-gold, non-runtime, non-authoritative input admitted only after separate governed schema approval; forbidden in MLRT-59.
Experiment output: a future non-authoritative observation that cannot update thresholds, weights, models, prompts, registries, routes, gold records, or training data; forbidden in MLRT-59.
Learning result: a future sandbox-only observation with no authority, no persistence, no training use, and no route effect; forbidden in MLRT-59.
Model learning: any operation that changes model behavior, route behavior, thresholds, weights, heuristics, confidence mapping, prompts, registry data, or gold data; forbidden in MLRT-59.
```

## Required future controlled experiment gate

A later patch may not create or run any controlled learning experiment unless a separate governed milestone proves all of the following first:

```text
1. MLRT-59 is frozen with FREEZE_MEMORY_STATUS: OK.
2. A controlled experiment input schema exists and is frozen.
3. A controlled experiment output boundary exists and is frozen.
4. Experiment inputs are explicitly non-training, non-gold, non-runtime, non-authoritative, and non-persistent.
5. Experiment outputs are explicitly non-training, non-gold, non-runtime, non-authoritative, and non-persistent.
6. No experiment output can update thresholds, weights, route behavior, prompts, registries, gold records, training data, or models.
7. Candidate execution remains unavailable until a later explicit execution milestone.
8. Case scoring remains unavailable until a later explicit scoring milestone.
9. Route comparison remains unavailable until a later explicit comparison milestone.
10. Validation proves a future experiment preview cannot write results, persist records, mutate data, train, calibrate, learn, score, compare routes, generate reports, or grant route authority.
```

## Current allowed state

MLRT-59 may only document and test the first controlled learning experiment planning boundary. It may update the MLRT README, MLRT governance document, manifest metadata, and validation test.

Every actual learning, experiment, sandbox, training, calibration, evaluation, gold, registry, and runtime capability remains false:

```text
first_controlled_learning_experiment_plan_defined = true
controlled_learning_experiment_enabled = false
controlled_learning_experiment_created = false
controlled_learning_experiment_started = false
controlled_learning_experiment_executed = false
experiment_runner_created = false
experiment_envelope_created = false
experiment_inputs_created = false
experiment_outputs_created = false
experiment_records_created = false
experiment_results_persisted = false
experiment_metrics_applied = false
learning_sandbox_enabled = false
learning_sandbox_created = false
learning_sandbox_runner_created = false
learning_sandbox_workspace_created = false
learning_sandbox_executed = false
learning_inputs_created = false
learning_outputs_created = false
learning_records_created = false
learning_results_persisted = false
model_learning_started = false
model_training_started = false
model_calibration_started = false
model_improvement_started = false
offline_evaluation_run_enabled = false
case_execution_enabled = false
case_scoring_enabled = false
route_comparison_enabled = false
report_generation_enabled = false
gold_registry_mutation_enabled = false
training_data_use_enabled = false
route_authority_enabled = false
runtime_pilot_enabled = false
copilot_enabled = false
```

## Forbidden actions

MLRT-59 must not create controlled learning experiment workspaces, experiment runners, experiment envelopes, learning engines, experiment input schemas, experiment output schemas, experiment inputs, experiment outputs, experiment records, experiment result stores, experiment metrics, score transforms, confidence transforms, thresholds, weights, parameters, candidate execution logic, case execution logic, case scoring, route comparison logic, report generators, data loaders, gold records, gold registries, registry mutation proposals, registry diffs, registry writes, labels, datasets, truth records, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, or route authority.

MLRT-59 must not claim controlled learning experiment readiness, experiment execution readiness, learning sandbox readiness for execution, model learning readiness, model training readiness, calibration readiness, score readiness, threshold readiness, route readiness, registry readiness, production readiness, candidate reliability, model reliability, learned reliability, or dry-run execution readiness.

## Explicit non-experiment status

The current project may contain prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, learning sandbox plan text, and freeze memory. None of these are experiment inputs. None are experiment outputs. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-59.

## Future governed milestones

MLRT-59 only authorizes the following roadmap labels. Each requires a separate future patch, validation, and freeze:

```text
MLRT-60 -> Gold Registry Schema Proposal Plan
MLRT-61 -> Offline Evaluation Case Schema Plan
MLRT-62 -> Calibration Input Schema Plan
MLRT-63 -> Learning Sandbox Input Boundary Plan
MLRT-64 -> Controlled Learning Experiment Input Boundary Plan
```

None of these future steps may be treated as already approved by MLRT-59.

## Positive label

The only positive MLRT-59 label is:

```text
RSS_MLRT59_FIRST_CONTROLLED_LEARNING_EXPERIMENT_PLAN_DEFINED_NO_EXPERIMENT
```

This label means the first controlled learning experiment planning boundary is documented and tested while all experiment implementation, experiment runner creation, sandbox workspace creation, experiment execution, experiment inputs, experiment outputs, experiment records, experiment persistence, model learning, model training, model calibration, model improvement, offline evaluation execution, case execution, scoring, route comparison, report generation, gold mutation, route authority, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-59 validation must confirm:

```text
VALIDATION OK: rss_mlrt59_first_controlled_learning_experiment_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-59, the project must locally freeze:

```text
Routing Signal Scorer MLRT-59 First Controlled Learning Experiment Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-60 Gold Registry Schema Proposal Plan v1`.
