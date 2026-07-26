# Routing Signal Scorer MLRT-54 Training Data Boundary Plan v1

Feature ID: `rss_mlrt54_training_data_boundary_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed Item 5 training-data boundary planning after MLRT-53 freeze.

## Purpose

MLRT-54 defines the **training-data boundary** for future governed work.

MLRT-54 does **not** create a dataset. It does **not** read prompts as training data. It does **not** read freeze memory as training data. It does **not** read user logs as training data. It does **not** label examples. It does **not** create gold records. It does **not** train, calibrate, score, or improve a model.

The purpose is to define what future work must prove before any later patch may introduce a controlled training-data intake, offline evaluation corpus, calibration corpus, or learning experiment.

The critical boundary error budget remains `0`.

## Entry evidence

MLRT-54 may begin only because MLRT-53 froze with `FREEZE_MEMORY_STATUS: OK` and preserved the next safe milestone as this MLRT-54 training-data boundary plan.

The safe sequence is:

```text
MLRT-48 -> controlled minimal inert source creation
MLRT-49 -> static boundary test
MLRT-50 -> non-runtime harness smoke test
MLRT-51 -> candidate evaluation harness self-test
MLRT-52 -> LAB reliability fixed-case test
MLRT-53 -> Item 5 training/learning governance planning only
MLRT-54 -> training-data boundary planning only
```

## Existing source surfaces remain unchanged

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

MLRT-54 must not modify these source files and must not add new Python implementation files.

## Boundary definitions

MLRT-54 fixes the following terms for later governed work:

```text
Candidate output metadata: caller-supplied non-authoritative in-memory metadata used only by existing LAB interface self-tests.
Fixed LAB case: hardcoded in-memory validation case used to check deterministic boundary outcomes.
Training data: any example, record, prompt, freeze entry, user log, routing decision, expected answer, score, label, correction, or gold truth that could change model behavior.
Training-data intake: any process that collects, normalizes, stores, labels, hashes, indexes, embeds, or prepares training data.
Gold data: canonical expected answers, expected routes, expected prompts, or scoring truth records.
Evaluation corpus: approved static cases for measurement only, not for changing model behavior.
Calibration corpus: approved static cases for changing thresholds or weights, only after separate calibration governance.
Runtime data: live project state, live prompts, live freeze memory, user sessions, logs, active router decisions, or runtime decisions.
```

## Explicitly non-training data in current MLRT state

The following current surfaces are not training data and must not be treated as training data by MLRT-54:

```text
- MLRT-48 inert source contract
- MLRT-49 static boundary tests
- MLRT-50 smoke-test contract calls
- MLRT-51 in-memory harness self-test envelopes
- MLRT-52 fixed in-memory LAB reliability cases
- MLRT-53 Item 5 governance document
```

They may be used only to verify that boundaries remain closed.

## Forbidden data sources

MLRT-54 forbids treating any of the following as training data:

```text
project_freeze_after_update/frozen_features_memory
project_freeze_after_update/files_to_send_ai
kanda_prompt_workspace/prompt_library
kanda_prompt_workspace/first_AI_deliver
runtime prompts
user conversation logs
manual freeze logs
validation terminal logs
project source comments
docstrings
README files
routing decisions
candidate outputs
candidate output metadata
LAB fixed cases
```

These sources may be inspected by governed validation only to verify boundaries, but they may not be ingested, labeled, embedded, indexed, persisted, scored as training examples, or used to change model behavior.

## Current allowed state

MLRT-54 may only document and test the training-data boundary. It may update the MLRT README, MLRT governance document, manifest metadata, and validation test.

Every actual data capability remains false:

```text
training_data_boundary_defined = true
training_data_intake_enabled = false
training_data_use_enabled = false
training_dataset_created = false
training_labels_created = false
gold_data_created = false
gold_registry_mutation_enabled = false
prompt_library_training_ingestion_enabled = false
freeze_memory_training_ingestion_enabled = false
user_log_training_ingestion_enabled = false
embedding_training_index_enabled = false
model_training_started = false
model_calibration_started = false
model_improvement_started = false
route_authority_enabled = false
runtime_pilot_enabled = false
copilot_enabled = false
```

## Future governed milestones

MLRT-54 only authorizes the following roadmap labels. Each requires a separate future patch, validation, and freeze:

```text
MLRT-55 -> Gold Registry Mutation Gate Plan
MLRT-56 -> Offline Evaluation Protocol Plan
MLRT-57 -> Calibration-Only Dry-Run Plan
MLRT-58 -> Learning Sandbox Plan
MLRT-59 -> First Controlled Learning Experiment Plan
```

None of these future steps may be treated as already approved by MLRT-54.

## Forbidden actions

MLRT-54 must not create data loaders, read prompts as training data, read freeze memory as training data, read user logs as training data, create datasets, create labels, create gold records, mutate gold registries, change scoring weights, change thresholds, train a model, fine-tune a model, call providers, call embedding systems, create vector stores, open network connections, persist evaluation outputs, persist training records, spawn subprocesses as runtime behavior, add batch mode, activate Pilot, activate Copilot, or grant route authority.

MLRT-54 must not claim candidate reliability, model reliability, learned reliability, data readiness, training readiness, or production readiness.

## Positive label

The only positive MLRT-54 label is:

```text
RSS_MLRT54_TRAINING_DATA_BOUNDARY_DEFINED_NO_DATA_USE
```

This label means the training-data boundary is documented and tested while all training-data use, data intake, datasets, labels, gold mutation, training, calibration, model improvement, runtime authority, Pilot, and Copilot remain blocked.

## Validation standard

MLRT-54 validation must confirm:

```text
VALIDATION OK: rss_mlrt54_training_data_boundary_plan_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-54, the project must locally freeze:

```text
Routing Signal Scorer MLRT-54 Training Data Boundary Plan v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-55 Gold Registry Mutation Gate Plan v1`.
