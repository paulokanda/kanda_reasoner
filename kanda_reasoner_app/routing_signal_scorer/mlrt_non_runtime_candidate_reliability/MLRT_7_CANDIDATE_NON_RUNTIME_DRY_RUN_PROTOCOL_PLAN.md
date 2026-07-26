# MLRT-7 - Candidate Non-Runtime Dry-Run Protocol Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_protocol_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-7 Candidate Non-Runtime Dry-Run Protocol Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-7-candidate-non-runtime-dry-run-protocol-plan`

Status: governed documentation-only MLRT non-runtime dry-run protocol planning milestone.

## Purpose

MLRT-7 defines the planned protocol doctrine for a future candidate non-runtime dry run.

MLRT-7 does not execute a dry run. It does not create dry-run protocol records. It does not create dry-run protocol execution records. It does not create dry-run inputs. It does not create dry-run outputs. It does not read dry-run readiness gates as live evidence. It does not approve a candidate package for dry-run execution. It does not create, accept, install, import, execute, validate, score, compare, or evaluate a candidate package. It does not create candidate outputs, reliability reports, persistent reports, persistent ML decisions, route decisions, human approvals, readiness approvals, activation signals, field-test signals, runtime Pilot commands, or Copilot instructions.

MLRT-7 only defines doctrine for how a future non-runtime dry-run protocol could be specified under a later governed milestone.

There is no candidate reliability validation in MLRT-7 and there is no ML implementation unlock.

## Precondition inherited from MLRT-6

MLRT-7 may begin only after MLRT-6 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-6 established that the next safe step after dry-run readiness gate planning is non-runtime dry-run protocol planning only.

## Contract scope

MLRT-7 defines planned protocol groups for a future non-runtime dry run. These groups are doctrine only:

1. Dry-run protocol identity and traceability.
2. Required dry-run readiness gate reference doctrine.
3. Non-runtime execution boundary doctrine.
4. Candidate package reference doctrine.
5. Static input set planning doctrine.
6. Candidate invocation envelope planning doctrine.
7. Output capture envelope planning doctrine.
8. Failure and rejection envelope planning doctrine.
9. Critical boundary blocker doctrine.
10. Human-escalation doctrine.
11. Protocol planning label doctrine.
12. Dry-run protocol non-authority doctrine.
13. Dry-run protocol forbidden authority field doctrine.
14. Dry-run protocol next-milestone doctrine.

MLRT-7 does not create executable validators. MLRT-7 does not read, scan, import, execute, or review candidate files. MLRT-7 does not write dry-run protocol records. MLRT-7 does not execute a dry run.

## Dry-run protocol identity and traceability doctrine

A future dry-run protocol record must declare at least:

- `dry_run_protocol_id`
- `dry_run_protocol_version`
- `schema_version`
- `mlrt_phase_reference`
- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `candidate_package_intake_record_id`
- `static_review_outcome_gate_id`
- `dry_run_readiness_gate_id`
- `dry_run_readiness_gate_hash`
- `dry_run_readiness_label`
- `dry_run_protocol_requested_by_human`
- `dry_run_protocol_authored_by_human_or_tooling`
- `dry_run_protocol_timestamp`
- `dry_run_protocol_scope`
- `non_runtime_only`
- `non_authoritative_only`
- `no_route_authority`
- `no_prompt_loading`
- `critical_boundary_error_budget`
- `protocol_hash_algorithm`
- `protocol_canonicalization_method`

A future dry-run protocol record with missing candidate traceability, missing readiness-gate reference, missing readiness-gate hash, missing protocol scope, missing non-runtime declaration, missing non-authoritative declaration, missing no-route-authority declaration, missing no-prompt-loading declaration, missing hash algorithm, or missing canonicalization method must not progress.

## Required dry-run readiness gate reference doctrine

A future dry-run protocol may only reason over a governed dry-run readiness gate from the future MLRT-6-derived readiness-gate phase.

The planned future protocol must require evidence for at least:

- package identity and traceability
- static review outcome-gate reference
- dry-run readiness gate reference
- dry-run readiness gate hash
- readiness label
- candidate package eligibility label
- critical boundary blocker status
- human review escalation status
- non-runtime declaration
- non-authoritative declaration
- no-route-authority declaration
- no-prompt-loading declaration
- no-provider-call declaration
- no-embedding-call declaration
- no-network-call declaration
- no-subprocess-call declaration
- no-batch-mode declaration
- no-persistence declaration
- no-Pilot declaration
- no-Copilot declaration
- no-activation declaration
- no-field-test declaration

A missing readiness gate reference, missing readiness gate hash, unresolved human escalation, unresolved rejection label, or any critical boundary blocker must produce `MLRT_DRY_RUN_PROTOCOL_INCOMPLETE` or a stricter rejection label.

## Non-runtime execution boundary doctrine

A future non-runtime dry-run protocol, if later authored under a separate governed milestone, must be isolated from runtime and authority surfaces.

A future non-runtime dry-run protocol may only plan:

- static input-set references
- static candidate package references
- static candidate invocation envelope references
- static expected-output contract references
- in-memory non-authoritative dry-run output envelope shape
- in-memory non-authoritative dry-run rejection envelope shape
- non-authoritative failure classification
- non-authoritative human review notes
- no-route-authority enforcement
- no-prompt-loading enforcement
- no-persistence enforcement
- zero critical boundary error doctrine

A future non-runtime dry-run protocol must not be a runtime Pilot, Copilot, activation, field test, production run, batch mode, route selector, prompt loader, provider caller, embedding caller, network caller, subprocess caller, or persistent ML decision writer.

## Candidate package reference doctrine

A future protocol may reference only a candidate package that already passed the earlier planning gates in doctrine:

- package intake planning
- static review checklist planning
- static review evidence-envelope planning
- static review outcome-gate planning
- dry-run readiness-gate planning

MLRT-7 does not create, accept, install, import, or validate a candidate package. A protocol reference must not become an install command, import command, execution command, approval, reliability claim, route decision, or activation signal.

## Static input set planning doctrine

A future dry-run protocol may define only the plan for a later static input set. It must not create that input set in MLRT-7.

A future input set plan may describe:

- input case identifiers
- static input envelope references
- expected non-authoritative output envelope references
- expected rejection envelope references
- critical boundary trigger cases
- human review trigger cases
- deterministic ordering doctrine
- no-live-data doctrine
- no-live-prompt-library-read doctrine
- no-live-freeze-memory-read doctrine
- no-live-router-canon-read doctrine

MLRT-7 does not create dry-run inputs and does not execute cases.

## Candidate invocation envelope planning doctrine

A future dry-run protocol may plan a candidate invocation envelope only as doctrine. It must not define executable invocation code.

A future invocation envelope must preserve:

- caller-supplied static input only
- no prompt loading
- no route authority
- no provider calls
- no embedding calls
- no network calls
- no subprocess calls
- no batch mode
- no persistence
- no write access to corpus, fixtures, canon, prompt library, freeze memory, gold registry, startup pack, activation state, field-test state, runtime logs, or persistent ML decision storage

The invocation envelope must be non-authoritative and must not become a runtime command.

## Output capture envelope planning doctrine

A future dry-run protocol may plan output capture only as a non-authoritative envelope.

A future dry-run output capture envelope may include:

- `dry_run_output_record_id`
- `dry_run_protocol_id`
- `candidate_package_id`
- `input_case_id`
- `candidate_output_payload`
- `candidate_rejection_payload`
- `contract_compliance_status`
- `critical_boundary_status`
- `human_review_required`
- `non_authoritative_only`
- `no_route_authority`
- `no_prompt_loading`

A future output capture envelope must not include route decisions, prompt loading instructions, install commands, freeze writes, human approvals, readiness approvals, activation signals, field-test signals, runtime Pilot commands, or Copilot instructions.

## Failure and rejection envelope planning doctrine

A future dry-run protocol must be able to fail closed.

A future rejection envelope may include:

- `missing_readiness_gate_reference`
- `readiness_gate_hash_mismatch`
- `missing_candidate_package_reference`
- `missing_static_input_reference`
- `candidate_invocation_boundary_risk`
- `output_capture_boundary_risk`
- `critical_boundary_blocker_present`
- `human_review_required`
- `protocol_scope_invalid`
- `runtime_or_authority_surface_detected`

A future protocol rejection must not become an approval or a runtime instruction.

## Critical boundary blocker doctrine

The critical boundary error budget remains `0`.

Any future protocol design that permits route authority, prompt loading, provider calls, embedding calls, network calls, subprocess calls, batch mode, persistence, report persistence, freeze-memory writes, prompt-library writes, router-canon writes, gold-registry writes, startup-pack writes, activation, field testing, runtime Pilot behavior, or Copilot behavior must be blocked.

Critical boundary incidents must not be hidden by aggregate soft metrics.

Neither MLRT-6 nor MLRT-7 validates candidate reliability.

## Human-escalation doctrine

A future protocol may declare human escalation as required, but that declaration must not approve execution.

A future human-escalation status may include:

- `MLRT_DRY_RUN_PROTOCOL_HUMAN_REVIEW_NOT_REQUIRED`
- `MLRT_DRY_RUN_PROTOCOL_HUMAN_REVIEW_REQUIRED`
- `MLRT_DRY_RUN_PROTOCOL_HUMAN_REVIEW_BLOCKING`

Human review notes must remain non-authoritative until a later governed scope explicitly authorizes a concrete action. MLRT-7 creates no human approvals.

## Protocol planning label doctrine

The only positive MLRT-7 label is:

```text
MLRT_DRY_RUN_PROTOCOL_READY_FOR_INPUT_SET_PLANNING_ONLY
```

This label only means that the dry-run protocol planning document is ready to support a later dry-run input-set planning milestone after local validation, freeze, startup context refresh, and `FREEZE_MEMORY_STATUS: OK`.

It does not mean that a protocol record exists. It does not mean dry-run inputs exist. It does not mean a dry run can execute. It does not mean candidate outputs exist. It does not mean a candidate is reliable. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

Allowed future planning labels may include only:

- `MLRT_DRY_RUN_PROTOCOL_NOT_READY`
- `MLRT_DRY_RUN_PROTOCOL_INCOMPLETE`
- `MLRT_DRY_RUN_PROTOCOL_BLOCKED_BY_MISSING_READINESS_GATE`
- `MLRT_DRY_RUN_PROTOCOL_BLOCKED_BY_HASH_OR_TRACEABILITY_MISMATCH`
- `MLRT_DRY_RUN_PROTOCOL_BLOCKED_BY_CRITICAL_BOUNDARY_RISK`
- `MLRT_DRY_RUN_PROTOCOL_NEEDS_HUMAN_REVIEW`
- `MLRT_DRY_RUN_PROTOCOL_READY_FOR_INPUT_SET_PLANNING_ONLY`

## Dry-run protocol non-authority doctrine

A future dry-run protocol must remain non-authoritative. It must not decide routes, rank routes for use, load prompts, approve reliability, approve readiness, approve dry-run execution, create install commands, create runtime commands, write freeze memory, write the prompt library, write router canon, write the gold registry, write startup packs, call providers, call embedding models, perform network calls, perform subprocess calls, start batch mode, persist ML decisions, activate Pilot, activate Copilot, enable field tests, or instruct runtime Pilot or Copilot behavior.

## Dry-run protocol forbidden authority fields

Future dry-run protocol envelopes must reject fields named:

- `route_decision`
- `load_prompt`
- `execute_route`
- `execute_dry_run`
- `approve_readiness`
- `approve_reliability`
- `approve_dry_run_execution`
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

## Explicit non-actions

MLRT-7 does not:

- create an ML/router candidate
- create or accept a real candidate package
- install a candidate package
- import a candidate package
- execute a candidate
- create candidate outputs
- perform static review
- create static review records
- create static review evidence records
- create static review outcome records
- create outcome gate records
- perform dry-run readiness review
- create dry-run readiness records
- create dry-run protocol records
- create dry-run protocol execution records
- execute a dry run
- create dry-run inputs
- create dry-run outputs
- execute LAB cases
- score cases
- compare live routes
- grant route authority
- load prompts
- read live prompt-library files
- read live freeze memory
- read live router canon
- import runtime router modules
- call providers
- call embedding models
- use vector stores
- use network calls
- use subprocess calls
- start batch mode
- persist ML decisions or create persistent ML decisions
- create or persist reports
- mutate corpus, fixtures, canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage
- create activation keys
- enable field-test mode
- create runtime Pilot behavior
- create Copilot behavior
- unlock ML implementation

## Next safe milestone

After MLRT-7 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-8 - Candidate Non-Runtime Dry-Run Input Set Plan
```

MLRT-8 must remain governed and non-runtime. It may only plan the dry-run input set. It must not create dry-run inputs, execute a dry run, score cases, validate candidate reliability, or unlock ML implementation.
