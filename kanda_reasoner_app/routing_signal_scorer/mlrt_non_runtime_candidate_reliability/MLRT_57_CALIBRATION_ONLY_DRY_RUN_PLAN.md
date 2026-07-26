# Routing Signal Scorer MLRT-57 Calibration-Only Dry-Run Plan v1

Feature ID: `rss_mlrt57_calibration_only_dry_run_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed Item 5 calibration-only dry-run planning after MLRT-56 freeze.

## Purpose

MLRT-57 defines the **calibration-only dry-run plan** for future governed work.

MLRT-57 does **not** run a calibration dry-run. It does **not** create calibration inputs. It does **not** create calibration outputs. It does **not** create thresholds, parameters, weights, metrics, score transforms, or calibration records. It does **not** start model calibration, model training, model improvement, learning, registry mutation, offline evaluation execution, case execution, case scoring, route comparison, report generation, route authority, Pilot, or Copilot behavior.

The purpose is to define the minimum future proof required before any later patch may introduce a controlled calibration-only dry-run. A future calibration-only dry-run, if ever approved, must remain non-runtime, non-authoritative, non-training, non-gold-mutating, and unable to change route behavior.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-57 may begin only because MLRT-56 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-57 calibration-only dry-run plan.

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
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-57 must not modify these source files and must not add new Python implementation files.

## Calibration-only dry-run definitions

MLRT-57 fixes the following terms for later governed work:

```text
Calibration-only dry-run plan: a documented future procedure for rehearsing calibration boundary checks without calibrating any model.
Calibration dry-run: a future non-authoritative rehearsal that may only be introduced by a separate governed patch; forbidden in MLRT-57.
Calibration input: a future non-training, non-gold, non-runtime input used only after a separate governed input-schema milestone; forbidden in MLRT-57.
Calibration output: a future non-authoritative observation from a calibration dry-run; forbidden in MLRT-57.
Calibration threshold: a future proposed threshold value; forbidden in MLRT-57.
Calibration parameter: a future proposed parameter or weight; forbidden in MLRT-57.
Calibration record: a future record of calibration-only rehearsal evidence; forbidden in MLRT-57.
Model calibration: any operation that changes model behavior, route behavior, thresholds, weights, heuristics, or confidence mapping; forbidden in MLRT-57.
```

## Required future calibration-only dry-run gate

A later patch may not run any calibration-only dry-run unless a separate governed milestone proves all of the following first:

```text
1. MLRT-57 is frozen with FREEZE_MEMORY_STATUS: OK.
2. A calibration input schema exists and is frozen.
3. A calibration-output boundary exists and is frozen.
4. Calibration inputs are explicitly non-training, non-gold, non-runtime, and non-authoritative.
5. Calibration outputs are explicitly non-training, non-gold, non-runtime, and non-authoritative.
6. No calibration output can update thresholds, weights, route behavior, registries, gold records, training data, or prompts.
7. Candidate execution remains unavailable until a later explicit execution milestone.
8. Case scoring remains unavailable until a later explicit scoring milestone.
9. Route comparison remains unavailable until a later explicit comparison milestone.
10. Validation proves the dry-run preview cannot write results, mutate data, calibrate a model, or grant route authority.
```

## Current allowed state

MLRT-57 may only document and test the calibration-only dry-run planning boundary. It may update the MLRT README, MLRT governance document, manifest metadata, and validation test.

Every actual calibration and dry-run capability remains false:

```text
calibration_only_dry_run_plan_defined = true
calibration_only_dry_run_enabled = false
calibration_only_dry_run_executed = false
calibration_dry_run_runner_created = false
calibration_inputs_created = false
calibration_outputs_created = false
calibration_thresholds_created = false
calibration_parameters_created = false
calibration_records_created = false
calibration_results_persisted = false
calibration_metrics_applied = false
model_calibration_started = false
model_calibrated = false
model_training_started = false
model_improvement_started = false
offline_evaluation_run_enabled = false
offline_evaluation_run_executed = false
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

MLRT-57 must not create calibration input schemas, calibration output schemas, calibration inputs, calibration outputs, calibration records, calibration result stores, calibration runners, dry-run engines, thresholds, weights, parameters, metrics, score transforms, confidence transforms, candidate execution logic, case execution logic, case scoring, route comparison logic, report generators, data loaders, gold records, gold registries, registry mutation proposals, registry diffs, registry writes, labels, datasets, truth records, provider calls, embedding calls, vector stores, persistence, batch mode, Pilot activation, Copilot activation, or route authority.

MLRT-57 must not claim model calibration readiness, calibration readiness for execution, score readiness, threshold readiness, route readiness, registry readiness, production readiness, candidate reliability, model reliability, learned reliability, or dry-run execution readiness.

## Explicit non-calibrating status

The current project may contain prior documentation, validation logs, README text, source comments, fixed LAB cases, candidate metadata envelopes, offline evaluation protocol text, and freeze memory. None of these are calibration inputs. None are calibration outputs. None may be scored. None may be treated as accepted truth. None may be used as training data or gold data by MLRT-57.

## Future governed milestones

MLRT-57 only authorizes the following roadmap labels. Each requires a separate future patch, validation, and freeze:

```text
MLRT-58 -> Learning Sandbox Plan
MLRT-59 -> First Controlled Learning Experiment Plan
MLRT-60 -> Gold Registry Schema Proposal Plan
MLRT-61 -> Offline Evaluation Case Schema Plan
MLRT-62 -> Calibration Input Schema Plan
```

None of these future steps may be treated as already approved by MLRT-57.

## Positive label

The only positive MLRT-57 label is:

```text
RSS_MLRT57_CALIBRATION_ONLY_DRY_RUN_PLAN_DEFINED_NO_CALIBRATION
```

This label means the calibration-only dry-run planning boundary is documented and tested while all dry-run execution, calibration inputs, calibration outputs, thresholds, parameters, model calibration, training-data use, datasets, labels, model training, model improvement, offline evaluation execution, case execution, scoring, route comparison, report generation, gold mutation, route authority, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-57 validation must confirm:

```text
VALIDATION OK: rss_mlrt57_calibration_only_dry_run_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-57, the project must locally freeze:

```text
Routing Signal Scorer MLRT-57 Calibration-Only Dry-Run Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-58 Learning Sandbox Plan v1`.
