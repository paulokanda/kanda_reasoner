# MLRT-5 - Candidate Static Review Outcome Gate Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_static_review_outcome_gate_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-5 Candidate Static Review Outcome Gate Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-5-candidate-static-review-outcome-gate-plan`

Status: governed documentation-only MLRT static-review outcome-gate planning milestone.

## Purpose

MLRT-5 defines the planned outcome gate for a future candidate static review.

MLRT-5 does not perform static review. It does not create static review outcome records. It does not read evidence envelopes as live evidence. It does not approve a candidate package. It does not create, accept, install, import, execute, validate, score, compare, or evaluate a candidate package. It does not create candidate outputs, reliability reports, persistent reports, persistent ML decisions, route decisions, human approvals, readiness approvals, activation signals, field-test signals, runtime Pilot commands, or Copilot instructions.

MLRT-5 only defines doctrine for how a future static review outcome gate could classify static review evidence before any later non-runtime dry-run readiness planning may exist.

There is no candidate reliability validation in MLRT-5 and there is no ML implementation unlock.

## Precondition inherited from MLRT-4

MLRT-5 may begin only after MLRT-4 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-4 established that the next safe step after candidate static review evidence-envelope planning is static review outcome gate planning only.

## Contract scope

MLRT-5 defines planned outcome-gate groups for a future static review. These groups are doctrine only:

1. Outcome gate identity and traceability.
2. Required evidence-envelope reference doctrine.
3. Critical boundary blocker doctrine.
4. Static review pass candidate doctrine.
5. Static review rejection doctrine.
6. Static review human-escalation doctrine.
7. Dry-run readiness planning label doctrine.
8. Outcome-gate non-authority doctrine.
9. Outcome-gate forbidden field doctrine.
10. Outcome-gate next-milestone doctrine.

MLRT-5 does not create executable validators. MLRT-5 does not read, scan, import, execute, or review candidate files. MLRT-5 does not write outcome records.

## Outcome gate identity and traceability doctrine

A future static review outcome gate record must declare at least:

- `static_review_outcome_gate_id`
- `static_review_outcome_gate_version`
- `schema_version`
- `mlrt_phase_reference`
- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `candidate_package_intake_record_id`
- `static_review_checklist_version`
- `static_review_evidence_envelope_id`
- `static_review_evidence_envelope_hash`
- `outcome_gate_requested_by_human`
- `outcome_gate_performed_by_human_or_tooling`
- `outcome_gate_timestamp`
- `outcome_gate_scope`
- `non_runtime_only`
- `non_authoritative_only`
- `critical_boundary_error_budget`
- `outcome_gate_hash_algorithm`
- `outcome_gate_canonicalization_method`

A future outcome gate record with missing package traceability, missing evidence-envelope reference, missing evidence hash, missing outcome scope, missing non-runtime declaration, missing non-authoritative declaration, missing hash algorithm, or missing canonicalization method must not progress.

## Required evidence-envelope reference doctrine

A future outcome gate may only reason over a governed static review evidence envelope from the future MLRT-4-derived evidence-envelope phase.

The planned future outcome gate must require evidence for at least:

- package identity and traceability
- candidate package reference evidence
- static review checklist reference evidence
- manifest and hash evidence
- dependency and import boundary evidence
- side-effect and persistence boundary evidence
- prompt-loading and route-authority boundary evidence
- provider, embedding, network, subprocess, and batch-mode evidence
- Pilot, Copilot, activation, and field-test boundary evidence
- human review escalation evidence
- rejection evidence when applicable
- evidence-envelope outcome label

A missing evidence-envelope reference, missing evidence hash, or missing checklist reference must produce `MLRT_STATIC_REVIEW_OUTCOME_INCOMPLETE` or a stricter rejection label.

## Critical boundary blocker doctrine

A future outcome gate must treat critical boundary violations as hard blockers.

The following planned future conditions must always block progression:

- any route authority claim
- any prompt loading claim
- any provider call capability
- any embedding or vector-store capability
- any network call capability
- any subprocess call capability
- any batch-mode capability
- any persistence of ML decisions
- any report persistence outside approved future non-runtime evidence area
- any freeze memory mutation
- any prompt library mutation
- any router canon mutation
- any gold registry mutation
- any startup pack mutation
- any approval state mutation
- any activation state mutation
- any field-test state mutation
- any runtime decision log mutation
- any activation key creation
- any Pilot enablement
- any Copilot enablement
- any automatic maturity jump
- any candidate attempt to produce route decisions
- any candidate attempt to issue runtime commands

A critical boundary blocker cannot be overridden by usefulness, confidence, convenience, aggregate scores, human preference, or a candidate's claimed safety.

## Static review pass candidate doctrine

A future outcome gate may define a non-authoritative planning-only pass candidate label, but that label must not mean the candidate package is accepted, installed, imported, executed, reliable, routable, activated, field-tested, usable by Pilot, or usable by Copilot.

A future pass-candidate path may exist only when all of these are true:

- evidence-envelope identity and traceability are complete
- manifest and hash evidence are complete
- dependency and import boundary evidence has no critical blocker
- side-effect and persistence boundary evidence has no critical blocker
- prompt-loading and route-authority evidence has no critical blocker
- provider, embedding, network, subprocess, and batch-mode evidence has no critical blocker
- Pilot, Copilot, activation, and field-test evidence has no critical blocker
- evidence labels are internally consistent
- human review escalation is not unresolved
- rejection evidence is absent or resolved as non-critical under a later governed review rule

Even then, the only allowed positive label remains planning-only and non-authoritative.

## Static review rejection doctrine

Allowed future rejection labels include:

- `MLRT_STATIC_REVIEW_OUTCOME_INCOMPLETE`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_MISSING_EVIDENCE`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_HASH_OR_MANIFEST_RISK`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_FORBIDDEN_RUNTIME_BOUNDARY`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_FORBIDDEN_IMPORT_OR_DEPENDENCY`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_PERSISTENCE_OR_AUTHORITY_RISK`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_PROMPT_OR_ROUTE_AUTHORITY_RISK`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_PROVIDER_EMBEDDING_NETWORK_SUBPROCESS_OR_BATCH_RISK`
- `MLRT_STATIC_REVIEW_OUTCOME_REJECTED_BY_PILOT_COPILOT_ACTIVATION_OR_FIELD_TEST_RISK`
- `MLRT_STATIC_REVIEW_OUTCOME_NEEDS_HUMAN_REVIEW`

A rejection label must not be converted into a soft score and must not be used as evidence of candidate reliability.

## Static review human-escalation doctrine

A future outcome gate may record that human review is required, but it must not record human approval.

A future outcome gate may include:

- `needs_human_review`
- `human_review_reason_codes`
- `human_review_requested_scope`
- `human_review_required_before_progression`
- `reviewer_notes_non_authoritative`

A future outcome gate must not include:

- `record_human_approval`
- `approve_readiness`
- `approve_reliability`
- `approve_activation`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`
- `write_startup_pack`

Human escalation may stop or defer a future review, but it cannot authorize execution, routing, activation, field testing, Pilot, Copilot, or ML implementation.

## Dry-run readiness planning label doctrine

The only positive MLRT-5 planning label is:

```text
MLRT_STATIC_REVIEW_OUTCOME_READY_FOR_NON_RUNTIME_DRY_RUN_READINESS_PLANNING_ONLY
```

This label means the outcome-gate doctrine is ready for a later governed non-runtime dry-run readiness planning milestone.

It does not mean that static review has been performed. It does not mean outcome records exist. It does not mean a candidate is reliable. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Outcome-gate non-authority doctrine

A future outcome gate must remain non-authoritative.

A future outcome gate must not become:

- a route decision
- a prompt loading instruction
- an install command
- an import command
- an execution command
- a scoring command
- a report generation command
- a report persistence command
- a freeze write
- a human approval record
- a readiness approval record
- a reliability approval record
- an activation signal
- a field-test signal
- a runtime Pilot command
- a Copilot instruction
- an ML implementation unlock

## Outcome-gate forbidden authority fields

A future outcome gate must reject these fields or equivalent behavior anywhere in package metadata, package manifest, checklist status, evidence envelope, outcome gate, or reviewer note:

- `route_decision`
- `load_prompt`
- `execute_route`
- `approve_readiness`
- `approve_reliability`
- `record_human_approval`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`
- `write_startup_pack`
- `activate_pilot`
- `activate_copilot`
- `enable_field_test`
- `call_provider`
- `call_embedding_model`
- `network_call`
- `subprocess_call`
- `start_batch_mode`
- `persist_ml_decision`
- `runtime_command`
- `pilot_instruction`
- `copilot_instruction`

These fields are critical boundary violations in MLRT-5 planning and cannot be softened by aggregate metrics, review convenience, or future candidate claims.

## Preserved boundary

The critical boundary error budget remains `0`.

MLRT-5 must preserve:

- no route authority
- no prompt loading
- no persistence
- no provider calls
- no embeddings/vector stores
- no network calls
- no subprocess calls
- no batch mode
- no activation
- no field testing
- no runtime Pilot behavior
- no Copilot behavior
- no candidate execution
- no case execution
- no case scoring
- no route comparison
- no report generation
- no report persistence
- no static review performed
- no static review outcome record created
- no candidate reliability claim
- no ML implementation unlock

Neither MLRT-4 nor MLRT-5 validates candidate reliability.

## Next safe milestone

After MLRT-5 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-6 - Candidate Non-Runtime Dry-Run Readiness Gate Plan
```

MLRT-6 must remain governed and non-runtime. It may only plan readiness for a later non-runtime dry-run and must not execute candidates unless a later explicit governed scope authorizes that after all prior gates are validated and frozen.
