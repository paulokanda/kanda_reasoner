# Routing Signal Scorer MLRT-52 Lab Reliability Test Against Fixed Cases v1

Feature ID: `rss_mlrt52_lab_reliability_fixed_cases_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed post-source LAB reliability test after MLRT-51 harness self-test.

## Purpose

MLRT-52 performs the first lab reliability test against fixed in-memory cases.

This milestone checks that the already-created non-runtime LAB interfaces behave deterministically across a small fixed case matrix:

```text
fixed_safe_metadata_case -> NOT_EVALUATED
fixed_forbidden_authority_case -> HARNESS_INTERFACE_REJECTED
fixed_self_validation_pass_case -> LAB_SELF_VALIDATION_PASS
fixed_self_validation_fail_case -> LAB_INVALID
```

This is a LAB reliability boundary test, not a candidate reliability claim. It confirms deterministic behavior of existing non-runtime interfaces against fixed cases supplied inside the validation test.

MLRT-52 does **not** execute a candidate, does **not** execute a dry run, does **not** execute project cases, does **not** score candidate quality, does **not** compare routes, does **not** generate reports, does **not** persist outputs, does **not** train or calibrate a model, and does **not** start Item 5 governance.

The critical boundary error budget remains `0`.

## Existing source surfaces under reliability test

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
```

## Fixed in-memory cases

MLRT-52 may only use fixed validation-owned in-memory cases:

```text
case_01_safe_metadata_not_evaluated
case_02_forbidden_authority_metadata_rejected
case_03_self_validation_all_controls_true_pass
case_04_self_validation_one_control_false_lab_invalid
```

These cases are not training data, not gold-registry mutations, not live corpus discovery, and not runtime project inputs. They are deterministic validation fixtures embedded in the test file only.

## Allowed test actions

MLRT-52 may only perform these actions:

```text
import_existing_mlrt_stub
import_existing_lab_candidate_harness_interface
import_existing_lab_self_validation_gate
call_get_stub_contract
call_assert_static_non_runtime_boundary
build_fixed_safe_not_evaluated_envelope_in_memory
build_fixed_forbidden_authority_rejected_envelope_in_memory
evaluate_fixed_all_controls_true_self_validation_in_memory
evaluate_fixed_one_false_control_self_validation_in_memory
repeat_fixed_cases_to_confirm_determinism
confirm_all_outputs_are_non_authoritative
confirm_no_candidate_execution
confirm_no_dry_run_execution
confirm_no_case_execution
confirm_no_case_scoring
confirm_no_route_comparison
confirm_no_route_authority
confirm_no_prompt_loading
confirm_no_provider_calls
confirm_no_embeddings
confirm_no_persistence
confirm_no_report_generation
confirm_no_training_data_use
confirm_no_item5_start
confirm_exactly_one_mlrt_python_source_file_exists
confirm_lab_python_surface_still_exactly_three_files
```

## Forbidden actions

MLRT-52 must not modify the MLRT source file, modify the LAB source files, add a harness engine, add a runner, add dry-run input loading, execute candidates, execute cases, score cases, compare routes, generate reports, persist outputs, read prompt libraries at runtime, read freeze memory at runtime, read router canon at runtime, call providers, use embeddings/vector stores, open network connections, spawn subprocesses, use batch mode, activate Pilot, activate Copilot, or start Item 5 training/learning governance.

MLRT-52 must not claim validated candidate reliability. It only confirms LAB interface determinism and boundary safety against fixed in-memory cases.

## Positive label

The only positive MLRT-52 label is:

```text
RSS_MLRT52_LAB_RELIABILITY_FIXED_CASES_PASSED_NON_RUNTIME
```

This label means the LAB reliability fixed-case test passed while remaining non-runtime, non-authoritative, non-evaluating, and non-persistent. It does not mean candidate reliability exists, dry-run behavior exists, training exists, or routing authority exists.

## Validation standard

MLRT-52 validation must confirm:

```text
VALIDATION OK: rss_mlrt52_lab_reliability_fixed_cases_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-52, the project must locally freeze:

```text
Routing Signal Scorer MLRT-52 Lab Reliability Test Against Fixed Cases v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-53 Training Learning Governance Plan v1`.
