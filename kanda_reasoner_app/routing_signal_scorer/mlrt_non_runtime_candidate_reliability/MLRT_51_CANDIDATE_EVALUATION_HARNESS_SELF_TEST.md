# Routing Signal Scorer MLRT-51 Candidate Evaluation Harness Self-Test v1

Feature ID: `rss_mlrt51_candidate_evaluation_harness_self_test_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed non-runtime candidate evaluation harness self-test after MLRT-50 smoke test.

## Purpose

MLRT-51 self-tests the existing LAB candidate evaluation harness interface using in-memory, caller-supplied metadata only.

This milestone proves that the harness interface can build deterministic non-authoritative envelopes for two controlled self-test cases:

```text
safe_metadata_case -> NOT_EVALUATED
forbidden_authority_metadata_case -> HARNESS_INTERFACE_REJECTED
```

The self-test checks the interface boundary. It does **not** execute a candidate, does **not** run a dry run, does **not** execute a case, does **not** score cases, does **not** compare routes, does **not** generate reports, does **not** validate candidate reliability, does **not** start Item 5 training/learning governance, and does **not** add runtime authority.

The critical boundary error budget remains `0`.

## Existing source surfaces under self-test

```text
kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
```

## Allowed self-test actions

MLRT-51 may only perform these actions:

```text
import_existing_mlrt_stub
import_existing_lab_candidate_harness_interface
call_get_stub_contract
call_assert_static_non_runtime_boundary
call_get_lab10_candidate_harness_interface_record
build_safe_not_evaluated_envelope_in_memory
build_forbidden_authority_rejected_envelope_in_memory
confirm_envelopes_are_non_authoritative
confirm_candidate_evaluation_executed_false
confirm_case_execution_false
confirm_case_scoring_false
confirm_route_comparison_false
confirm_route_authority_false
confirm_prompt_loading_false
confirm_provider_calls_false
confirm_embeddings_false
confirm_persistence_false
confirm_report_generation_false
confirm_training_data_use_still_blocked
confirm_item5_not_started
confirm_exactly_one_mlrt_python_source_file_exists
confirm_lab_python_surface_still_exactly_three_files
```

## Forbidden actions

MLRT-51 must not modify the MLRT source file, add a harness engine, add a runner, add dry-run input loading, execute candidates, execute cases, score cases, compare routes, generate reports, persist outputs, read prompt libraries at runtime, read freeze memory at runtime, read router canon at runtime, call providers, use embeddings/vector stores, open network connections, spawn subprocesses, use batch mode, activate Pilot, activate Copilot, or start Item 5 training/learning governance.

MLRT-51 must not claim validated candidate reliability. It only confirms that the existing candidate evaluation harness interface can reject authority fields and produce non-authoritative NOT_EVALUATED / HARNESS_INTERFACE_REJECTED envelopes in memory.

## Positive label

The only positive MLRT-51 label is:

```text
RSS_MLRT51_CANDIDATE_EVALUATION_HARNESS_SELF_TEST_PASSED_NON_EVALUATING
```

This label means the candidate evaluation harness interface self-test passed while remaining non-evaluating and non-authoritative. It does not mean candidate evaluation exists, dry-run behavior exists, validated reliability exists, training exists, or routing authority exists.

## Validation standard

MLRT-51 validation must confirm:

```text
VALIDATION OK: rss_mlrt51_candidate_evaluation_harness_self_test_v1
```

and must keep all forbidden capability flags false.

## Freeze requirement

Before continuing beyond MLRT-51, the project must locally freeze:

```text
Routing Signal Scorer MLRT-51 Candidate Evaluation Harness Self-Test v1
```

The required freeze output remains:

```text
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
```

Only after that may a separate governed request proceed to `Routing Signal Scorer MLRT-52 Lab Reliability Test Against Fixed Cases v1`.
