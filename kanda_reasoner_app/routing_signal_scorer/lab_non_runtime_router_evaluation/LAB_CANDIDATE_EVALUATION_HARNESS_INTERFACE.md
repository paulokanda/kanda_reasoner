# LAB-10 — Candidate Evaluation Harness Interface v1

Feature ID: `routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1`

Feature title: `Routing Signal Scorer v3 ML LAB Candidate Evaluation Harness Interface v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation`

Schema version: `lab-10-candidate-evaluation-harness-interface`

Status: governed non-runtime candidate evaluation harness interface only.

## Purpose

LAB-10 defines the first in-memory interface envelope that a future candidate evaluation harness will use.
It is not the harness itself. It does not evaluate candidates, execute cases, score cases, compare routes, generate reports, persist reports, or authorize reliability claims.

The interface exists so future LAB milestones have a controlled boundary for candidate inputs before any evaluation machinery is introduced.

## Added Python interface file

LAB-10 adds exactly one new allowed LAB Python source file:

- `candidate_evaluation_harness_interface.py`

The file SHA-256 in the sandbox patch build is:

`4379b920d8af248e28ff1a7376c29c5c3431ec378f1ee5013ef515e89c5c4c8f`

After LAB-10, the only allowed LAB Python source files are:

- `candidate_evaluation_harness_interface.py`
- `deterministic_runner_skeleton.py`
- `lab_self_validation_gate.py`

No other LAB Python source file is allowed by LAB-10.

## Interface behavior

The interface may:

- accept caller-supplied candidate metadata
- accept caller-supplied candidate identity/version/reference
- accept caller-supplied test case reference
- accept caller-supplied corpus version
- accept caller-supplied fixture manifest hash
- accept caller-supplied self-validation status
- canonicalize caller-supplied candidate metadata
- compute SHA-256 for caller-supplied candidate metadata
- return an immutable, read-only, non-authoritative interface envelope
- mark output as `NOT_EVALUATED`
- reject envelopes that contain forbidden authority fields as `HARNESS_INTERFACE_REJECTED`

The interface must not read live project state or files. It does not execute any case or candidate.

## Required interface inputs

Future use of this interface requires caller-supplied values for:

- `lab_run_id`
- `candidate_id`
- `candidate_version`
- `candidate_output_reference`
- `candidate_output_metadata`
- `test_case_reference`
- `corpus_version`
- `fixture_manifest_hash`
- `self_validation_status`

Missing or malformed future inputs must become `LAB_INVALID` in a later governed evaluator. LAB-10 does not implement that evaluator.

## Non-authoritative candidate wrapper

A LAB-10 envelope is only a non-authoritative carrier. It is not any of the following:

- route decision
- prompt loading command
- route execution command
- score
- report
- freeze write
- human approval
- readiness approval
- reliability claim
- activation signal
- field-test signal
- runtime Pilot command
- Copilot instruction

## Forbidden authority fields

Candidate metadata must not include these authority fields:

- `route_decision`
- `load_prompt`
- `execute_route`
- `approve_readiness`
- `record_human_approval`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`
- `activate_pilot`
- `activate_copilot`
- `enable_field_test`
- `call_provider`
- `call_embedding_model`
- `start_batch_mode`
- `persist_ml_decision`
- `runtime_command`
- `copilot_instruction`

If any of those fields are present, LAB-10 may return `HARNESS_INTERFACE_REJECTED`. That is not candidate evaluation. It is an interface-boundary rejection.

## Explicit non-actions

LAB-10 does not:

- evaluate candidates
- execute test cases
- score test cases
- compare routes
- select routes
- execute routes
- load prompts
- read live prompt-library content
- read live freeze memory
- read live router canon
- import runtime router modules
- read fixture files from disk
- create actual fixture snapshots
- create hash manifest data files
- create corpus cases
- generate reports
- persist reports
- persist ML decisions
- call providers
- call embedding models
- use network
- use subprocess
- use async/background/batch execution
- activate Pilot
- activate Copilot
- enable field testing
- implement runtime Pilot behavior
- implement Copilot behavior

## Relationship to LAB-9

LAB-9 defined the offline observability and experiment-report contract. LAB-10 only defines the future candidate-evaluation input envelope.

LAB-10 does not produce a LAB-9 report and does not populate report data.

## Relationship to future LAB-11

LAB-11 — Corpus V1 Expansion is the next safe milestone.

LAB-11 may expand static corpus coverage, but it must still not evaluate candidates unless a later governed milestone explicitly introduces candidate evaluation machinery after all required boundaries are frozen.

## Reliability and ML implementation lock

LAB-10 provides no reliability evidence.

The ML implementation continuation lock remains:

`LAB/test fulfills its mission → LAB self-validation passes → ML router prompt logic reliability is tested → zero critical boundary violations are demonstrated → human review and freeze confirm reliability evidence → only then continue ML logic implementation`

## Zero critical-boundary doctrine

The critical boundary error budget remains `0`.

Any future attempt to use this interface as route authority, prompt loading authority, report persistence authority, reliability authority, activation authority, field-test authority, runtime Pilot behavior, or Copilot behavior is a critical boundary violation.
