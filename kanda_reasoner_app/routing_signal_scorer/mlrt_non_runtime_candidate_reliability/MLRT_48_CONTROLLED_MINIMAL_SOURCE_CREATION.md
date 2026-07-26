# Routing Signal Scorer MLRT-48 Controlled Minimal Source Creation v1

Feature ID: `rss_mlrt48_controlled_minimal_source_creation_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed controlled minimal source creation milestone.

## Purpose

MLRT-48 is the first controlled source-creation milestone after MLRT-47 was validated, frozen, exposed, and synchronized with `FREEZE_MEMORY_STATUS: OK`.

MLRT-48 intentionally ends the plan-only chain. It creates exactly one inert non-runtime Python source file at the planned path:

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
```

This is source creation only. It is not harness testing, not dry-run execution, not candidate execution, not case scoring, not report generation, not reliability validation, not training, not Item 5 governance, and not runtime activation.

The critical boundary error budget remains `0`.

## What MLRT-48 creates

MLRT-48 creates exactly this Python source file:

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
```

The source file is a static inert source surface. It exposes only static contract data and a boundary assertion helper. It does not read files, write files, create folders after install, open network connections, call subprocesses, load prompts, call providers, use embeddings, create vector stores, persist decisions, start batch mode, activate field testing, route anything, execute candidates, run dry runs, score cases, generate reports, claim reliability, start training-data use, create runtime Pilot behavior, or create Copilot behavior.

## Boundary transition from MLRT-47

MLRT-47 was the final documentation-only go/no-go gate. MLRT-48 supersedes the earlier temporary zero-Python-implementation rule inside the MLRT non-runtime candidate reliability box by exactly one permitted file:

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
```

No other Python implementation file is allowed under the MLRT box after MLRT-48. Historical MLRT-42 through MLRT-47 tests that asserted zero Python implementation files represented the pre-source state and must not be reused as post-MLRT-48 regression tests. MLRT-48 supplies the new boundary test for the post-source state.

## Hard boundary

MLRT-48 does not create route authority, prompt loading, provider calls, embeddings, vector stores, persistence, batch mode, activation keys, field-test mode, runtime Pilot behavior, Copilot behavior, dry-run execution, candidate execution, case scoring, route comparison, report generation, reliability validation, training-data use, model training, model calibration, model improvement, gold/registry mutation, or automatic maturity jumps.

MLRT-48 does not start Item 5. Item 5 remains blocked until the minimal source surface is created and later static/harness/lab tests prove the non-runtime box is safe.

## Static source contract

The created source file must expose:

```text
FEATURE_ID
SOURCE_STATUS
CRITICAL_BOUNDARY_ERROR_BUDGET
MinimalNonRuntimeHarnessStubContract
get_stub_contract
assert_static_non_runtime_boundary
```

The source file must be import-safe and all forbidden capability flags must remain `False`.

The only positive MLRT-48 label is:

```text
RSS_MLRT48_MINIMAL_NON_RUNTIME_SOURCE_CREATED_STATIC_ONLY
```

This label means exactly one inert source file exists. It does not mean testing started, training started, reliability was proven, or routing authority exists.

## Validation standard

MLRT-48 validation must confirm:

```text
source_file_exists_at_exact_path
only_one_python_file_under_mlrt_box
source_import_is_safe
source_contract_flags_are_static
critical_boundary_error_budget_zero
lab_python_surface_still_exactly_three_files
no_prompt_loading
no_provider_calls
no_embeddings
no_persistence
no_route_authority
no_dry_run_execution
no_candidate_execution
no_training_data_use
no_runtime_pilot
no_copilot
```

## Freeze requirement

Before continuing beyond MLRT-48, the project must locally freeze:

```text
Routing Signal Scorer MLRT-48 Controlled Minimal Source Creation v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-49 Static Boundary Test v1`.
