# MLRT-2 - Candidate Package Intake Contract Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_package_intake_contract_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-2 Candidate Package Intake Contract Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-2-candidate-package-intake-contract-plan`

Status: governed documentation-only MLRT package-intake contract-planning milestone.

## Purpose

MLRT-2 defines the planned contract for a future candidate package intake step.

MLRT-2 does not create a candidate package. It does not accept a real package into the project. It does not install, import, execute, validate, score, compare, or evaluate a candidate. It does not generate reports, persist reports, validate candidate reliability, and does not unlock ML implementation.

MLRT-2 only defines doctrine for what a future package-intake record would need before a later static review milestone may exist.

## Precondition inherited from MLRT-1

MLRT-2 may begin only after MLRT-1 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-1 established that the next safe step after input/output contract planning is package intake contract planning only.

## Contract scope

MLRT-2 defines the planned contract for four future non-runtime objects:

1. Candidate package metadata envelope.
2. Candidate package contents manifest.
3. Candidate package intake decision envelope.
4. Candidate package rejection envelope.

MLRT-2 does not create executable validators. MLRT-2 does not create an actual candidate package. MLRT-2 does not write package data or intake records.

## Candidate package metadata envelope doctrine

A future candidate package metadata envelope must be static, non-runtime, and human-submitted for governed intake.

The planned future metadata envelope must include at least these fields:

- `candidate_package_id`
- `candidate_package_version`
- `candidate_package_schema_version`
- `candidate_id`
- `candidate_version`
- `candidate_kind`
- `candidate_interface_version`
- `candidate_origin`
- `candidate_author`
- `candidate_submission_date`
- `target_mlrt_phase`
- `requires_static_review`
- `requires_human_review`
- `declared_files`
- `declared_entrypoints`
- `declared_dependencies`
- `declared_runtime_permissions`
- `declared_write_targets`
- `declared_network_use`
- `declared_provider_use`
- `declared_embedding_use`
- `declared_persistence_use`
- `declared_batch_mode_use`
- `declared_activation_use`
- `declared_field_test_use`
- `declared_pilot_use`
- `declared_copilot_use`
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

A future package metadata envelope must not contain executable instructions that install, import, execute, activate, field-test, persist, or route through the candidate.

## Candidate package contents manifest doctrine

A future candidate package contents manifest must list candidate package contents without executing or importing them.

The planned future contents manifest must include at least:

- `contents_manifest_id`
- `contents_manifest_version`
- `candidate_package_id`
- `candidate_package_version`
- `file_entries`
- `file_path`
- `file_kind`
- `file_sha256`
- `file_size_bytes`
- `declared_purpose`
- `static_review_required`
- `executable_flag`
- `entrypoint_flag`
- `dependency_flag`
- `forbidden_runtime_boundary_flag`
- `hash_algorithm`
- `hash_input_canonicalization`

The manifest may describe files for future review. It must not copy candidate files into runtime boxes. It must not install dependencies. It must not load candidate modules. It must not run import checks that import candidate code.

## Candidate package intake decision envelope doctrine

A future intake decision envelope may only decide whether the package is ready for a later static review plan.

Allowed future intake labels are:

- `MLRT_PACKAGE_INTAKE_NOT_READY`
- `MLRT_PACKAGE_INTAKE_READY_FOR_STATIC_REVIEW_PLANNING_ONLY`
- `MLRT_PACKAGE_INTAKE_BLOCKED_BY_MISSING_METADATA`
- `MLRT_PACKAGE_INTAKE_BLOCKED_BY_FORBIDDEN_RUNTIME_BOUNDARY`
- `MLRT_PACKAGE_INTAKE_BLOCKED_BY_UNDECLARED_DEPENDENCY`
- `MLRT_PACKAGE_INTAKE_BLOCKED_BY_HASH_OR_MANIFEST_MISMATCH`
- `MLRT_PACKAGE_INTAKE_NEEDS_HUMAN_REVIEW`

The only positive MLRT-2 label is:

```text
MLRT_PACKAGE_INTAKE_READY_FOR_STATIC_REVIEW_PLANNING_ONLY
```

This label does not mean a package is safe. It does not mean a candidate is reliable. It does not mean a candidate can be installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Candidate package rejection envelope doctrine

A future rejection envelope must be non-authoritative and must identify package-intake contract failures without fixing, importing, installing, or executing the candidate.

The planned future rejection envelope must include at least:

- `rejection_record_id`
- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `rejection_code`
- `rejection_family`
- `rejection_severity`
- `contract_field_path`
- `manifest_field_path`
- `critical_boundary_flag`
- `lab_invalid_flag`
- `human_review_required`
- `non_authoritative_only`

A rejection envelope must not write to freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage.

## Forbidden candidate package intake behaviors

A future package intake contract must reject any package that attempts or requests:

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

Any future package that requests these behaviors must be blocked before static review and must not be converted into a softer failure by aggregate metrics.

## Intake storage doctrine

MLRT-2 does not create intake storage.

A future intake storage design, if ever approved, must remain outside runtime authority and must not become persistent ML decision storage, human approval storage, readiness approval storage, activation storage, field-test storage, or runtime routing storage.

No actual intake records are created by MLRT-2.

## Static review boundary

MLRT-2 may only lead to a future static review checklist plan. It does not perform static review.

Static review is not execution. Static review is not reliability evidence. Static review is not route authority.

## Critical boundary rule

The critical boundary error budget remains `0`.

If a future package intake contract gives a candidate package any path to runtime authority, MLRT is invalid.

If a future package intake contract gives a candidate package any write path to freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime decision logs, or persistent ML decision storage, MLRT is invalid.

If a future package intake contract allows prompt loading, provider calls, embeddings, persistence, batch mode, activation, field testing, runtime Pilot, or Copilot behavior, MLRT is invalid unless a later explicit governed scope changes that boundary after reliability has been proven and frozen.

## Relationship to MLRT-1

MLRT-1 defined the future input/output/rejection envelope for candidate reliability outputs.

MLRT-2 defines the future package metadata and contents-manifest contract that would precede static review of a candidate package.

Neither MLRT-1 nor MLRT-2 validates candidate reliability.

## Next safe milestone after MLRT-2

After MLRT-2 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-3 - Candidate Static Review Checklist Plan
```

MLRT-3 must remain governed and non-runtime. It may define a future static review checklist, but it must not implement a candidate, install a package, import a package, execute candidates, score cases, compare routes, grant route authority, load prompts, call providers, use embeddings, persist ML decisions or create persistent ML decisions, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

## ML implementation continuation lock

ML implementation remains blocked.

The continuation lock is:

```text
LAB closure/readiness review frozen
-> MLRT-0 controlled non-runtime candidate reliability test plan
-> MLRT-1 candidate reliability input/output contract plan
-> MLRT-2 candidate package intake contract plan
-> MLRT-3 candidate static review checklist plan
-> future governed candidate reliability execution under LAB controls
-> zero critical boundary violations
-> human review
-> freeze of reliability evidence
-> only then consider continuing ML logic implementation
```

Until that full chain is completed, real ML implementation remains blocked.
