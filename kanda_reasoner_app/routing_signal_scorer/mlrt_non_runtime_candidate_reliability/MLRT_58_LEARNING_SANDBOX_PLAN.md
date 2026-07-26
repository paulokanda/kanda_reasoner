# Routing Signal Scorer MLRT-58 Learning Sandbox Plan v1

Feature ID: `rss_mlrt58_learning_sandbox_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed Item 5 learning-sandbox planning after MLRT-57 freeze.

## Purpose

MLRT-58 defines the **learning sandbox plan** for future governed work.

MLRT-58 does **not** create a learning sandbox implementation. It does **not** create a sandbox workspace. It does **not** create a sandbox runner. It does **not** run a learning experiment. It does **not** create learning inputs. It does **not** create learning outputs. It does **not** create learning records or persist learning results. It does **not** start training-data intake, dataset creation, label creation, model training, model calibration, model improvement, offline evaluation execution, case execution, case scoring, route comparison, report generation, gold registry mutation, route authority, Pilot, or Copilot behavior.

The purpose is to define the minimum future proof required before any later patch may introduce an isolated, non-runtime, non-authoritative learning sandbox. A future learning sandbox, if ever approved, must be unable to change model behavior, route behavior, prompts, registries, gold records, training data, thresholds, weights, or runtime decisions.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-58 may begin only because MLRT-57 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-58 learning sandbox plan.

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
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-58 must not modify these source files and must not add new Python implementation files.

## Learning sandbox definitions

MLRT-58 fixes the following terms for later governed work:

```text
Learning sandbox plan: a documented future procedure for designing an isolated non-runtime learning rehearsal environment without implementing it.
Learning sandbox environment: a future isolated non-runtime, non-authoritative workspace; forbidden in MLRT-58.
Learning sandbox runner: a future non-runtime runner that could rehearse a learning experiment; forbidden in MLRT-58.
Learning experiment: a future controlled rehearsal that must remain non-authoritative and non-runtime until separately governed; forbidden in MLRT-58.
Learning input: a future non-training, non-gold, non-runtime input admitted only after a separate governed schema milestone; forbidden in MLRT-58.
Learning output: a future non-authoritative observation from a learning sandbox experiment; forbidden in MLRT-58.
Learning record: a future record of sandbox-only observations; forbidden in MLRT-58.
Model learning: any operation that changes model behavior, route behavior, thresholds, weights, heuristics, confidence mapping, prompts, registry data, or gold data; forbidden in MLRT-58.
```

## Required future learning sandbox gate

A later patch may not create or run any learning sandbox unless a separate governed milestone proves all of the following first:

```text
1. MLRT-58 is frozen with FREEZE_MEMORY_STATUS: OK.
2. A learning sandbox input schema exists and is frozen.
3. A learning sandbox output boundary exists and is frozen.
4. Learning inputs are explicitly non-training, non-gold, non-runtime, and non-authoritative.
5. Learning outputs are explicitly non-training, non-gold, non-runtime, and non-authoritative.
6. No learning output can update thresholds, weights, route behavior, registries, gold records, training data, prompts, or models.
7. Candidate execution remains unavailable until a later explicit execution milestone.
8. Case scoring remains unavailable until a later explicit scoring milestone.
9. Route comparison remains unavailable until a later explicit comparison milestone.
10. Validation proves the sandbox preview cannot write results, persist records, mutate data, train, calibrate, learn, or grant route authority.
```

## Current allowed state

MLRT-58 may only document and test the learning sandbox planning boundary. It may update the MLRT README, MLRT governance document, manifest metadata, and validation test.

Every actual learning, sandbox, training, calibration, evaluation, gold, registry, and runtime capability remains false:

```text
learning_sandbox_plan_defined = true
learning_sandbox_enabled = false
learning_sandbox_created = false
learning_sandbox_runner_created = false
learning_sandbox_workspace_created = false
learning_sandbox_executed = false
learning_experiment_enabled = false
learning_experiment_started = false
learning_inputs_created = false
learning_outputs_created = false
learning_records_created = false
learning_results_persisted = false
learning_metrics_applied = false
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

MLRT-58 must not create learning sandbox workspaces, sandbox runners, learning engines, learning input schemas, learning output schemas, learning inputs, learning outputs, learning records, learning result stores, learning metrics, score transforms, confidence transforms, thresholds, weights, parameters, candidate execution logic, case execution logic, case scoring, route comparison logic, report generators, data loaders, gold records, gold registries, registry mutation proposals, registry diffs, registry writes, labels, datasets, truth records, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, or route authority.

MLRT-58 must not claim learning sandbox readiness for execution, controlled learning experiment readiness, model learning readiness, model training readiness, calibration readiness, score readiness, threshold readiness, route readiness, registry readiness, production readiness, candidate reliability, model reliability, learned reliability, or dry-run execution readiness.

## Explicit non-learning status

The current project may contain prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, calibration-only dry-run plan text, and freeze memory. None of these are learning inputs. None are learning outputs. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-58.

## Future governed milestones

MLRT-58 only authorizes the following roadmap labels. Each requires a separate future patch, validation, and freeze:

```text
MLRT-59 -> First Controlled Learning Experiment Plan
MLRT-60 -> Gold Registry Schema Proposal Plan
MLRT-61 -> Offline Evaluation Case Schema Plan
MLRT-62 -> Calibration Input Schema Plan
MLRT-63 -> Learning Sandbox Input Boundary Plan
```

None of these future steps may be treated as already approved by MLRT-58.

## Positive label

The only positive MLRT-58 label is:

```text
RSS_MLRT58_LEARNING_SANDBOX_PLAN_DEFINED_NO_LEARNING
```

This label means the learning sandbox planning boundary is documented and tested while all sandbox implementation, sandbox workspace creation, sandbox runner creation, learning experiment execution, learning inputs, learning outputs, learning records, learning persistence, model learning, model training, model calibration, model improvement, offline evaluation execution, case execution, scoring, route comparison, report generation, gold mutation, route authority, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-58 validation must confirm:

```text
VALIDATION OK: rss_mlrt58_learning_sandbox_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-58, the project must locally freeze:

```text
Routing Signal Scorer MLRT-58 Learning Sandbox Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-59 First Controlled Learning Experiment Plan v1`.
