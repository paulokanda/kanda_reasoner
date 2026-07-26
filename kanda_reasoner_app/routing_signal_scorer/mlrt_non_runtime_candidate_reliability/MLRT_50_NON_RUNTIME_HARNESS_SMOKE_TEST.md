# Routing Signal Scorer MLRT-50 Non-Runtime Harness Smoke Test v1

Feature ID: `rss_mlrt50_non_runtime_harness_smoke_test_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed non-runtime smoke-test milestone after MLRT-49 static boundary test.

## Purpose

MLRT-50 is the first non-runtime smoke test of the controlled minimal MLRT source surface created by MLRT-48 and statically checked by MLRT-49.

This milestone confirms that the inert harness stub can be imported and its allowed public contract functions can be called without side effects. It tests that the stub is present, import-safe, deterministic, and still declares every forbidden ML/router capability as disabled.

MLRT-50 is a **smoke test of the inert stub contract only**. It is not a dry run, not candidate execution, not case scoring, not route comparison, not report generation, not reliability validation, not Item 5 training/learning governance, and not runtime behavior.

The critical boundary error budget remains `0`.

## Source under smoke test

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
```

## Allowed smoke-test actions

MLRT-50 may only perform these actions:

```text
import_the_existing_stub_module
call_get_stub_contract
call_assert_static_non_runtime_boundary
confirm_contract_is_deterministic
confirm_no_files_created_or_modified_by_import_or_calls
confirm_all_forbidden_capability_flags_are_false
confirm_exactly_one_mlrt_python_source_file_exists
confirm_lab_python_surface_still_exactly_three_files
confirm_no_dry_run_execution
confirm_no_candidate_execution
confirm_no_case_scoring
confirm_no_report_generation
confirm_no_route_authority
confirm_no_prompt_loading
confirm_no_provider_calls
confirm_no_embeddings
confirm_no_persistence
confirm_no_training_data_use
confirm_no_item5_start
confirm_no_runtime_pilot
confirm_no_copilot
```

## Forbidden actions

MLRT-50 must not modify the source file, add a runner, add a harness engine, add dry-run input loading, execute candidates, execute cases, score cases, compare routes, generate reports, persist outputs, read prompt libraries at runtime, read freeze memory at runtime, call providers, use embeddings/vector stores, open network connections, spawn subprocesses, use batch mode, activate Pilot, activate Copilot, or start Item 5 training/learning governance.

MLRT-50 must not claim validated candidate reliability. It only confirms that the minimal non-runtime source surface can survive a smoke test while remaining inert.

## Positive label

The only positive MLRT-50 label is:

```text
RSS_MLRT50_NON_RUNTIME_HARNESS_SMOKE_TEST_PASSED_STUB_STILL_INERT
```

This label means the inert stub survived import and contract-call smoke testing. It does not mean dry-run behavior exists, candidate evaluation exists, validated reliability exists, training exists, or routing authority exists.

## Validation standard

MLRT-50 validation must confirm:

```text
VALIDATION OK: rss_mlrt50_non_runtime_harness_smoke_test_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-50, the project must locally freeze:

```text
Routing Signal Scorer MLRT-50 Non-Runtime Harness Smoke Test v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-51 Candidate Evaluation Harness Self-Test v1`.
