# Routing Signal Scorer MLRT-49 Static Boundary Test v1

Feature ID: `rss_mlrt49_static_boundary_test_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed static boundary testing milestone after MLRT-48 controlled minimal source creation.

## Purpose

MLRT-49 is the first post-source testing milestone. It verifies that the MLRT-48 source surface remains exactly what it was allowed to become: one inert, import-safe, static non-runtime file.

MLRT-49 is a **static boundary test**. It starts boundary testing, not candidate execution.

It does not execute a dry run, does not execute candidates, does not score cases, does not compare routes, does not generate reports, does not persist outputs, does not use training data, does not train, does not calibrate, does not improve a model, does not start Item 5 governance, does not grant route authority, and does not create runtime Pilot or Copilot behavior.

The critical boundary error budget remains `0`.

## Source under test

The only MLRT Python source file allowed after MLRT-48 is:

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
```

MLRT-49 validates this file statically and by import-safety checks only.

## What MLRT-49 may test

MLRT-49 may check:

```text
source_file_exists_at_exact_path
only_one_python_file_under_mlrt_box
source_text_has_no_banned_runtime_or_io_api
source_import_has_no_file_side_effects
source_contract_flags_are_false
critical_boundary_error_budget_zero
lab_python_surface_still_exactly_three_files
no_prompt_loading
no_provider_calls
no_embeddings
no_vector_store
no_persistence
no_batch_mode
no_activation
no_field_testing
no_dry_run_execution
no_candidate_execution
no_case_scoring
no_report_generation
no_reliability_claim
no_training_data_use
no_runtime_pilot
no_copilot
```

## What MLRT-49 must not do

MLRT-49 must not create or modify the MLRT source file. It must not create a harness implementation, runner, dry-run engine, candidate executor, scoring engine, report generator, persistence layer, prompt loader, provider integration, embedding/vector-store integration, activation switch, field-test mode, runtime Pilot, or Copilot behavior.

MLRT-49 must not run historical MLRT-42 through MLRT-47 zero-Python-file tests, because MLRT-48 intentionally changed the boundary to exactly one allowed inert source file.

## Positive label

The only positive MLRT-49 label is:

```text
RSS_MLRT49_STATIC_BOUNDARY_TEST_PASSED_SOURCE_STILL_INERT
```

This label means static boundary checks passed and the single MLRT source file remains inert. It does not mean the harness works, a dry run works, a candidate was executed, reliability was proven, Item 5 started, or routing authority exists.

## Validation standard

MLRT-49 validation must confirm:

```text
VALIDATION OK: rss_mlrt49_static_boundary_test_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-49, the project must locally freeze:

```text
Routing Signal Scorer MLRT-49 Static Boundary Test v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-50 Non-Runtime Harness Smoke Test v1`.
