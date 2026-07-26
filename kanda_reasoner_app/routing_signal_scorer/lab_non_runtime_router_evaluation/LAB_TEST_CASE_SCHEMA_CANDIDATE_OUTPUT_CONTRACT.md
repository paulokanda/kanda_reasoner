# LAB-4 Test Case Schema + Candidate Output Contract

Feature ID: `routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1`

This milestone defines the future record contracts for the KANDA ML LAB.

LAB-4 is documentation/governance design only.

LAB-4 does not implement schema code, validators, fixture files, corpus files, runner logic, scoring engines, metrics engines, candidate harnesses, live detectors, import scanners, write guards, prompt loading, persistence, provider calls, embeddings, activation, field testing, runtime Pilot, or Copilot behavior.

## Purpose

The LAB needs stable contracts before any future fixture, runner, or candidate evaluation work begins.

LAB-4 defines:

- the future test case record shape;
- the future candidate output record shape;
- required version and canon-reference fields;
- case-specific pass/fail/critical-fail rubric fields;
- two-pass match-before-disagree fields;
- non-authoritative candidate output shielding;
- forbidden candidate output fields and actions;
- rejection rules for malformed or unsafe records.

This is a contract specification only. It is not a JSON schema implementation, not a validator, not a runner, and not a corpus.

## Relationship to previous LAB gates

LAB-4 depends on the frozen LAB gates:

```text
RG-LAB-000 → LAB-0 → LAB-0A → LAB-0B → LAB-0C → LAB-1 → LAB-2 → LAB-3 → LAB-4
```

LAB-4 preserves:

- LAB-0 phase boundary and documentation-only start;
- LAB-0A measurable success criteria;
- LAB-0B risk-control mapping;
- LAB-0C critical boundary error budget equals zero;
- LAB-1 sealed LAB box and shielding doctrine;
- LAB-2 failure taxonomy and critical violation model;
- LAB-3 hard-gate-before-soft-score scoring doctrine.

## Contract version fields

Every future test case record must declare these version fields:

```text
case_id
case_version
schema_version
corpus_version
canon_version_reference
canon_rule_references
fixture_hash_reference
scoring_model_version
expected_runner_min_version
created_at_utc
review_status
```

Version fields are mandatory because future reports must be reproducible.

A case missing required version fields must be rejected before candidate scoring.

## Future test case record fields

The future test case record must include the following groups.

### Identity fields

```text
case_id
case_version
schema_version
corpus_version
category
subcategory
severity
critical_boundary_flag
adversarial_flag
regression_source
review_status
```

### Canon reference fields

```text
canon_version_reference
canon_rule_references
fixture_hash_reference
source_freeze_id
source_milestone
source_prompt_group_references
source_box_references
```

### Input simulation fields

```text
user_request_raw
normalized_request
conversation_history
simulated_context
context_freshness
simulated_freeze_state
simulated_handoff_state
simulated_sidecar_state
simulated_startup_state
simulated_uploaded_files
```

### Expected routing fields

```text
expected_task_classification
expected_path
expected_required_prompt_groups
expected_recommended_prompt_groups
expected_prompt_priority
expected_missing_context
expected_may_proceed_now
expected_safe_next_action
expected_forbidden_actions
expected_explanation_elements
```

### Case-specific rubric fields

```text
case_specific_pass_conditions
case_specific_fail_conditions
case_specific_critical_fail_conditions
case_specific_lab_invalid_conditions
case_specific_human_review_conditions
case_specific_soft_metric_weights
```

### Match-before-disagree expectation fields

```text
expected_pass_1_canon_match_behavior
expected_pass_2_disagreement_behavior
expected_yield_to_canon
expected_no_authority_claim
```

### Reliability and traceability fields

```text
coverage_tags
risk_control_references
failure_taxonomy_references
hard_gate_references
soft_metric_references
human_review_required
reliability_claim_allowed_if_passed
notes
```

## Candidate output contract

Candidate output must be wrapped as a non-authoritative evaluation record.

The future candidate output record must include:

```text
candidate_output_schema_version
candidate_version
candidate_kind
case_id
case_version
run_id
pass_1_canon_match
pass_1_task_classification
pass_1_path
pass_1_required_prompt_groups
pass_1_missing_context
pass_1_may_proceed_now
pass_1_safe_next_action
pass_1_forbidden_actions_avoided
pass_1_explanation
pass_2_disagreement_or_improvement
pass_2_disagreement_type
pass_2_supporting_reason
pass_2_risk_note
yield_to_canon
confidence_level
needs_human_review
candidate_limitations
no_authority_assertion
```

The `no_authority_assertion` field must explicitly preserve that the candidate output is not a route decision, not a prompt loading command, not an approval, not a freeze write, not an activation signal, and not runtime behavior.

## Two-pass match-before-disagree contract

The candidate must follow this order:

```text
pass_1_canon_match
→ pass_2_disagreement_or_improvement only if needed
→ yield_to_canon
```

Rules:

- pass 1 must attempt to match frozen canon before disagreement;
- pass 2 may explain disagreement only as non-authoritative evaluation information;
- candidate disagreement cannot override canon;
- candidate disagreement cannot become route authority;
- candidate disagreement cannot trigger prompt loading, persistence, approval, activation, field testing, runtime Pilot, or Copilot behavior.

Skipping pass 1 is a hard failure.

Treating pass 2 as authority is a critical failure when it crosses a forbidden boundary.

## Forbidden candidate output fields

Future candidate output must not include fields that imply authority.

Forbidden fields include:

```text
route_decision
load_prompt
execute_route
approve_readiness
record_human_approval
write_freeze_memory
write_gold_registry
write_prompt_library
write_router_canon
activate_pilot
activate_copilot
enable_field_test
create_activation_key
call_provider
call_embedding_model
start_batch_mode
persist_ml_decision
runtime_command
copilot_instruction
```

If such a field appears, the record must be rejected or marked critical according to LAB-2 and LAB-3.

## Forbidden candidate actions

The candidate output contract must never allow:

```text
route authority
prompt loading
prompt-library mutation
router-canon mutation
freeze-memory mutation
gold-registry mutation
provider calls
embedding/vector calls
training-data use
batch mode
persistent ML decision storage
human approval recording
readiness approval recording
activation key creation
field-test enablement
runtime Pilot behavior
Copilot behavior
ML implementation continuation
```

## Contract rejection rules

Future schema/runner milestones must reject or block records when:

```text
required_version_field_missing
case_id_missing_or_mismatched
schema_version_missing_or_unsupported
fixture_hash_reference_missing
canon_version_reference_missing
case_specific_rubric_missing
candidate_output_not_wrapped_as_non_authoritative
pass_1_canon_match_missing
pass_2_attempts_authority
yield_to_canon_missing_or_false_when_required
forbidden_candidate_field_present
candidate_output_contains_runtime_command
candidate_output_contains_prompt_loading_instruction
candidate_output_contains_persistence_instruction
candidate_output_contains_provider_or_embedding_instruction
candidate_output_contains_activation_or_field_test_instruction
candidate_output_claims_reliability_without_lab_preconditions
```

## LAB_INVALID relationship

Malformed gold/test case records are LAB defects, not candidate defects.

Examples that must become `LAB_INVALID`:

```text
gold_case_missing_case_id
gold_case_missing_schema_version
gold_case_missing_canon_reference
gold_case_missing_fixture_hash_reference
gold_case_missing_expected_outcome
gold_case_missing_case_specific_rubric
gold_case_has_conflicting_expected_path
gold_case_has_unreviewed_status
```

Candidate output defects are candidate failures unless the runner or fixture is invalid.

## Human review contract

A candidate may set:

```text
needs_human_review = true
```

A candidate may not set:

```text
human_approved = true
approval_recorded = true
freeze_write_authorized = true
readiness_approved = true
```

Candidate attempts to record approval are critical boundary violations.

## Case category minimums

Future corpus cases should use these category values:

```text
basic_routing_classification
fast_path_vs_routed_work
required_prompt_group_selection
missing_context_may_proceed
freeze_update_governance_workflow
prompt_library_prompt_authoring
patch_install_validation_freeze_memory
box_boundary_leakage
stale_context_stale_filename_stale_sidecar
adversarial_bypass_prompt_injection
ambiguous_typo_shorthand
medical_document_simple_task_distinction
roadmap_regression
known_past_mistake_regression
```

The categories are contract labels only. LAB-4 does not create corpus cases.

## Candidate wrapper doctrine

Candidate output must be handled as:

```text
non_authoritative_evaluation_record
```

It cannot become:

```text
route decision
prompt loading command
approval
activation
runtime action
freeze write
human decision record
readiness decision
Copilot instruction
```

## Version compatibility rule

Future runner milestones must compare:

```text
schema_version
candidate_output_schema_version
corpus_version
canon_version_reference
scoring_model_version
runner_version
fixture_hash_reference
```

Incompatible or missing versions must block scoring before soft metrics.

## Non-claims

LAB-4 does not implement a schema validator.

LAB-4 does not create JSON fixtures.

LAB-4 does not create corpus cases.

LAB-4 does not implement a runner.

LAB-4 does not implement scoring.

LAB-4 does not evaluate a candidate.

LAB-4 does not prove the LAB is reliable.

LAB-4 does not prove ML router prompt logic reliability.

LAB-4 does not authorize continuing ML implementation.

## ML implementation continuation lock

The contract preserves the roadmap:

```text
P12 frozen
→ RG-LAB-000 canonization
→ LAB documentation/governance gates
→ LAB self-validation
→ ML router prompt logic reliability testing
→ only then continue ML logic implementation
```

LAB-4 does not satisfy that roadmap by itself.

## Next safe milestone

After LAB-4 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, proceed only to:

```text
LAB-5 — Frozen Canon Fixture Format + Hash Manifest
```

LAB-5 remains governed fixture-format/hash-manifest design and must not create runtime ML implementation, prompt loading, provider calls, persistence, activation, field testing, runtime Pilot, or Copilot behavior.
