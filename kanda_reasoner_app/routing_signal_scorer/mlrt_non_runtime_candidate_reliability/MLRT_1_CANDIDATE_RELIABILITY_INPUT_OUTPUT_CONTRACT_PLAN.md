# MLRT-1 - Candidate Reliability Input/Output Contract Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_reliability_input_output_contract_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-1 Candidate Reliability Input/Output Contract Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-1-candidate-reliability-input-output-contract-plan`

Status: governed documentation-only MLRT contract-planning milestone.

## Purpose

MLRT-1 defines the planned input and output contract for a future controlled non-runtime ML/router candidate reliability test.

MLRT-1 does not test the ML/router algorithm. It does not execute a candidate, does not execute cases, does not score cases, does not compare routes, does not generate reports, does not persist reports, does not validate candidate reliability, and does not unlock ML implementation.

MLRT-1 only defines contract doctrine for a later candidate reliability test phase.

## Precondition inherited from MLRT-0

MLRT-1 may begin only after MLRT-0 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-0 established that the next safe step after the controlled non-runtime test plan is input/output contract planning only.

## Contract scope

MLRT-1 defines the planned contract for three future non-runtime objects:

1. Candidate reliability input envelope.
2. Candidate reliability output envelope.
3. Candidate reliability rejection envelope.

MLRT-1 does not create executable validators. MLRT-1 does not create actual candidate outputs. MLRT-1 does not create a candidate package.

## Candidate reliability input envelope doctrine

A future candidate reliability input envelope must be static, non-runtime, and caller-supplied by the governed test harness.

The planned future input envelope must include at least these fields:

- `input_envelope_id`
- `input_envelope_version`
- `schema_version`
- `mlrt_phase_reference`
- `lab_phase_reference`
- `candidate_id`
- `candidate_version`
- `candidate_interface_version`
- `case_id`
- `case_version`
- `corpus_version_reference`
- `fixture_manifest_reference`
- `canon_version_reference`
- `canon_rule_references`
- `expected_task_classification`
- `expected_path`
- `expected_required_prompt_groups`
- `expected_missing_context`
- `expected_forbidden_actions`
- `case_specific_pass_conditions`
- `case_specific_fail_conditions`
- `case_specific_critical_fail_conditions`
- `allowed_context_bundle`
- `forbidden_live_sources`
- `non_runtime_only`
- `non_authoritative_only`
- `no_route_authority`
- `no_prompt_loading`
- `no_persistence`
- `no_provider_calls`
- `no_embedding_calls`
- `no_activation`
- `no_field_test_mode`
- `no_runtime_pilot`
- `no_copilot_behavior`

The future input envelope must not contain live prompt-library text, live freeze-memory reads, live router-canon reads, runtime router objects, provider credentials, embedding/vector handles, activation state, field-test state, runtime decision logs, or persistent ML decision storage handles.

## Candidate reliability output envelope doctrine

A future candidate reliability output envelope must be wrapped as:

```text
non_authoritative_candidate_reliability_output_record
```

The planned future output envelope must include at least these fields:

- `output_record_id`
- `output_record_version`
- `schema_version`
- `candidate_id`
- `candidate_version`
- `input_envelope_id`
- `case_id`
- `case_version`
- `corpus_version_reference`
- `fixture_manifest_reference`
- `canon_version_reference`
- `pass_1_canon_match`
- `pass_1_observed_classification`
- `pass_1_observed_path`
- `pass_1_observed_required_prompt_groups`
- `pass_1_observed_missing_context`
- `pass_1_observed_forbidden_actions`
- `pass_2_disagreement_or_improvement`
- `pass_2_disagreement_reason`
- `yield_to_canon`
- `boundary_risk_flags`
- `critical_boundary_flags`
- `human_review_requested`
- `candidate_explanation`
- `candidate_confidence_label`
- `candidate_limitations`
- `non_authoritative_only`
- `no_route_authority`
- `no_prompt_loading`
- `no_persistence`
- `no_provider_calls`
- `no_embedding_calls`
- `no_activation`
- `no_field_test_mode`
- `no_runtime_pilot`
- `no_copilot_behavior`

The future output envelope may describe a candidate's observed classification and its disagreement rationale. It may not become a route decision.

## Two-pass match-before-disagree doctrine

A future candidate output must preserve the two-pass contract:

1. `pass_1_canon_match` attempts to match frozen canon expectations.
2. `pass_2_disagreement_or_improvement` may explain a concern only after canon matching is attempted.
3. `yield_to_canon` must remain true when canon and candidate disagree unless a separate human review process later changes canon.

Disagreement is not authority. Explanation is not authority. Confidence is not authority.

## Forbidden output fields

A future candidate reliability output must be rejected if it contains any authority or runtime fields, including:

- `route_decision`
- `load_prompt`
- `execute_route`
- `select_route`
- `approve_readiness`
- `record_human_approval`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`
- `write_startup_pack`
- `write_activation_state`
- `write_field_test_state`
- `write_runtime_decision_log`
- `persist_ml_decision`
- `activate_pilot`
- `activate_copilot`
- `enable_field_test`
- `call_provider`
- `call_embedding_model`
- `start_batch_mode`
- `runtime_command`
- `pilot_instruction`
- `copilot_instruction`

Any future output with these fields must be rejected before scoring and must not be converted into a softer failure by aggregate metrics.

## Rejection envelope doctrine

A future rejection envelope must be non-authoritative and must identify contract failure reasons without executing or correcting the candidate.

The planned future rejection envelope must include at least:

- `rejection_record_id`
- `input_envelope_id`
- `candidate_id`
- `candidate_version`
- `case_id`
- `rejection_code`
- `rejection_family`
- `rejection_severity`
- `contract_field_path`
- `critical_boundary_flag`
- `lab_invalid_flag`
- `human_review_required`
- `non_authoritative_only`

A rejection envelope must not write to freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage.

## Allowed planning labels

MLRT-1 defines planning labels only. They do not grant runtime permissions.

Allowed labels:

- `MLRT_IO_CONTRACT_NOT_READY`
- `MLRT_IO_CONTRACT_READY_FOR_CANDIDATE_PACKAGE_INTAKE_PLANNING_ONLY`
- `MLRT_IO_CONTRACT_BLOCKED_BY_LAB_INVALID`
- `MLRT_IO_CONTRACT_BLOCKED_BY_CRITICAL_BOUNDARY_RISK`
- `MLRT_IO_CONTRACT_NEEDS_HUMAN_REVIEW`

The only positive label allowed by MLRT-1 is:

```text
MLRT_IO_CONTRACT_READY_FOR_CANDIDATE_PACKAGE_INTAKE_PLANNING_ONLY
```

This label means the next governed milestone may design candidate package intake. It does not mean a candidate exists. It does not mean a candidate is reliable. It does not mean ML implementation may continue.

## Critical boundary rule

The critical boundary error budget remains `0`.

If a future input/output contract gives candidate output any path to runtime authority, MLRT is invalid.

If a future input/output contract gives candidate output any write path to freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime decision logs, or persistent ML decision storage, MLRT is invalid.

If a future input/output contract allows prompt loading, provider calls, embeddings, persistence, batch mode, activation, field testing, runtime Pilot, or Copilot behavior, MLRT is invalid unless a later explicit governed scope changes that boundary after reliability has been proven and frozen.

## Relationship to LAB and MLRT-0

LAB built the non-runtime evaluation infrastructure.

MLRT-0 defined the test-planning boundary.

MLRT-1 defines the future input/output contract for candidate reliability testing.

Neither LAB nor MLRT output is authoritative. Candidate output remains non-authoritative.

## Next safe milestone after MLRT-1

After MLRT-1 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-2 - Candidate Package Intake Contract Plan
```

MLRT-2 must remain governed and non-runtime. It may define the future candidate package intake contract, but it must not implement a candidate, execute candidates, score cases, compare routes, grant route authority, load prompts, call providers, use embeddings, persist ML decisions or create persistent ML decisions, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

## ML implementation continuation lock

ML implementation remains blocked.

The continuation lock is:

```text
LAB closure/readiness review frozen
-> MLRT-0 controlled non-runtime candidate reliability test plan
-> MLRT-1 candidate reliability input/output contract plan
-> MLRT-2 candidate package intake contract plan
-> future governed candidate reliability execution under LAB controls
-> zero critical boundary violations
-> human review
-> freeze of reliability evidence
-> only then consider continuing ML logic implementation
```

Until that full chain is completed, real ML implementation remains blocked.
