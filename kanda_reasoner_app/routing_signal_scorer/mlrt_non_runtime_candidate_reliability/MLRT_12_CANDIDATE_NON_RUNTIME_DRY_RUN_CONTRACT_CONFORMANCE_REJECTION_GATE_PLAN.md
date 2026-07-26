# MLRT-12 Candidate Non-Runtime Dry-Run Contract-Conformance Rejection Gate Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_contract_conformance_rejection_gate_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only planning milestone.

## Purpose

MLRT-12 defines a future non-runtime dry-run contract-conformance rejection gate plan after MLRT-11 output-capture contract-conformance planning has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This milestone exists to describe how a future candidate output would be rejected or escalated when it fails the declared non-runtime dry-run output-capture contract-conformance doctrine. It is the last planned gate before the project may safely plan the first non-runtime dry-run execution milestone. It defines gate doctrine only. It does not run a rejection gate, does not run a conformance check, does not create rejection records, does not create conformance records, does not create output records, does not execute a dry run, does not execute a candidate, does not execute cases, does not score cases, does not compare routes, does not validate candidate reliability, and does not unlock ML implementation.

## Roadmap position

This is roadmap progress, not a loop. The MLRT chain has moved through distinct blocking layers:

```text
MLRT-7  - future dry-run protocol planning
MLRT-8  - future dry-run input-set planning
MLRT-9  - future dry-run output-capture planning
MLRT-10 - future output-capture rejection-gate planning
MLRT-11 - future output-capture contract-conformance planning
MLRT-12 - future contract-conformance rejection-gate planning
```

Each layer narrows the conditions under which a future non-runtime candidate dry run could exist without allowing runtime authority, prompt loading, persistence, provider calls, route decisions, field testing, Pilot, or Copilot behavior.

## Hard boundary

MLRT-12 is documentation-only. It does not create contract-conformance rejection records and does not run a contract-conformance rejection gate. It does not run a conformance check. It does not create conformance records, conformance evidence, output records, output manifests, output capture envelopes, output capture rejection records, output rejection gate records, dry-run input records, dry-run output records, candidate outputs, case outputs, reports, or reliability evidence. It does not:

- run a contract-conformance rejection gate
- create contract-conformance rejection records
- create contract-conformance records
- create contract-conformance evidence
- run a contract-conformance check
- create dry-run output records
- create dry-run output manifests
- create output capture envelopes
- create output capture rejection records
- create output rejection gate records
- run an output rejection gate
- create dry-run input records
- create dry-run input manifests
- execute a dry run
- execute a candidate
- create candidate outputs
- execute cases
- score cases
- compare routes
- generate reports
- persist reports
- validate candidate reliability
- unlock ML implementation
- create or accept a candidate package
- install a candidate package
- import a candidate package
- perform static review
- create static review records
- create static review evidence records
- create evidence envelopes
- create static review outcome records
- create outcome gate records
- perform dry-run readiness review
- create dry-run readiness records
- create dry-run protocol records
- create dry-run protocol execution records
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
- mutate corpus, fixtures, router canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage
- create activation keys
- enable field-test mode
- create runtime Pilot behavior
- create Copilot behavior

The critical boundary error budget remains `0`.

Neither MLRT-11 nor MLRT-12 validates candidate reliability.

## Rejection-gate identity doctrine

A future contract-conformance rejection gate record, if later approved by a separate governed milestone, must identify:

- rejection gate record identity
- MLRT phase reference
- MLRT-7 dry-run protocol reference
- MLRT-8 dry-run input-set reference
- MLRT-9 output-capture plan reference
- MLRT-10 output-capture rejection gate reference
- MLRT-11 contract-conformance plan reference
- candidate package reference
- candidate output capture envelope reference
- output contract version reference
- conformance rule-set version reference
- rejection-family classification
- mandatory rejection reason
- human-review escalation status
- non-authoritative-only status

MLRT-12 does not create these records. It defines only that such identity would be mandatory later.

## Mandatory rejection families

Future contract-conformance rejection-gate handling must reject or escalate candidate outputs that fall into any of these non-runtime families:

- missing required output field
- invalid required field type
- invalid required field value domain
- invalid required field cardinality
- invalid field canonicalization
- missing candidate package identity
- mismatched candidate package identity
- missing input-to-output correlation
- mismatched input-to-output correlation
- missing dry-run protocol reference
- mismatched dry-run protocol reference
- malformed rejection envelope
- malformed non-authoritative label
- unknown field present
- forbidden authority field present
- forbidden mutation field present
- forbidden prompt-loading field present
- forbidden route-decision field present
- forbidden runtime-command field present
- forbidden provider, embedding, network, subprocess, or batch-mode field present
- forbidden persistence or ML-decision storage field present
- forbidden activation, field-test, Pilot, or Copilot field present
- ambiguous or unverifiable output shape
- boundary-risking output that requires human review

These are planning families only. MLRT-12 does not run a validator, conformance checker, parser, classifier, rejection gate, dry run, candidate, scorer, or report generator.

## Rejection outcome-label doctrine

Future contract-conformance rejection-gate planning may use labels such as:

- contract_conformance_rejection_gate_not_run
- contract_conformance_rejected_missing_required_field
- contract_conformance_rejected_invalid_field_type
- contract_conformance_rejected_invalid_field_value
- contract_conformance_rejected_invalid_cardinality
- contract_conformance_rejected_invalid_canonicalization
- contract_conformance_rejected_identity_mismatch
- contract_conformance_rejected_correlation_mismatch
- contract_conformance_rejected_malformed_rejection_envelope
- contract_conformance_rejected_unknown_field
- contract_conformance_rejected_forbidden_authority_field
- contract_conformance_rejected_forbidden_mutation_field
- contract_conformance_rejected_prompt_loading_attempt
- contract_conformance_rejected_route_authority_attempt
- contract_conformance_rejected_runtime_command_attempt
- contract_conformance_rejected_provider_embedding_network_subprocess_or_batch_attempt
- contract_conformance_rejected_persistence_or_ml_decision_storage_attempt
- contract_conformance_rejected_activation_field_test_pilot_or_copilot_attempt
- contract_conformance_requires_human_review
- contract_conformance_rejection_gate_ready_for_first_non_runtime_dry_run_execution_planning_only

These labels must remain non-authoritative. They must not validate candidate reliability, score a case, approve a candidate, approve a dry run, authorize execution, or unlock ML implementation.

## No pass-to-execution doctrine

A future output that is not rejected by this gate must not automatically pass to execution. A future gate result may only support the next governed planning step. It must not mean:

- the candidate is reliable
- the candidate is safe
- the candidate can route
- the candidate can load prompts
- the candidate can replace current routing logic
- the candidate can be used in Pilot
- the candidate can be used in Copilot
- the candidate can be field-tested
- the candidate can run at runtime
- ML implementation is unlocked

The first future non-runtime dry-run execution plan may be planned only after MLRT-12 is validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

## Human-review escalation doctrine

Future contract-conformance rejection-gate planning must escalate ambiguous, malformed, unknown-field, identity-mismatch, correlation-mismatch, authority-field, mutation-field, persistence-seeking, activation-seeking, or boundary-risking outputs to human review.

Human review escalation must not equal approval. It must not write freeze memory, approve readiness, approve reliability, unlock ML implementation, grant route authority, activate a candidate, enable field testing, create runtime Pilot behavior, or create Copilot behavior.

## No silent waiver doctrine

Future rejection-gate handling must not silently waive failures. A candidate output that triggers a rejection family must remain rejected or escalated. Future gate handling must not downgrade a critical boundary violation into a warning.

## No silent coercion doctrine

Future rejection-gate handling must not repair, normalize into safety, rewrite, reinterpret, or coerce a candidate output into a passing contract shape. A malformed, ambiguous, unknown-field, authority-seeking, route-seeking, prompt-loading, persistence-seeking, activation-seeking, Pilot-seeking, or Copilot-seeking output must remain rejected or escalated.

## No-live-read doctrine

Future rejection-gate handling must not read live prompt-library files, live freeze memory, live router canon, runtime router modules, current project state, provider endpoints, embedding stores, vector stores, or network sources to decide, repair, waive, or reinterpret candidate output.

Any future rejection gate must use only predeclared static input references, declared output contracts, and candidate output material supplied under the governed dry-run protocol.

## No mutation doctrine

Future rejection-gate handling must not mutate:

- corpus
- fixtures
- router canon
- prompt library
- freeze memory
- gold registry
- startup pack
- approval state
- activation state
- field-test state
- runtime logs
- persistent ML decision storage

MLRT-12 creates no mutating code and no mutating records.

## Forbidden authority fields

Future dry-run contract-conformance rejection-gate envelopes must not contain active authority fields. Forbidden fields include:

```text
route_decision
load_prompt
execute_route
execute_dry_run
approve_readiness
approve_reliability
approve_dry_run_execution
record_human_approval
write_freeze_memory
write_gold_registry
write_prompt_library
write_router_canon
write_startup_pack
activate_pilot
activate_copilot
enable_field_test
call_provider
call_embedding_model
network_call
subprocess_call
start_batch_mode
persist_ml_decision
runtime_command
pilot_instruction
copilot_instruction
```

If a future candidate output contains these fields, contract-conformance rejection-gate planning must treat that as rejection or human escalation under a later governed milestone.

## Positive label

The only positive MLRT-12 label is:

```text
MLRT_CONTRACT_CONFORMANCE_REJECTION_GATE_READY_FOR_FIRST_NON_RUNTIME_DRY_RUN_EXECUTION_PLANNING_ONLY
```

This label means only that the documentation-only contract-conformance rejection-gate plan is ready for the next planning milestone after local validation and freeze.

It does not mean that rejection records exist. It does not mean a rejection gate has run. It does not mean a conformance check has run. It does not mean output records exist. It does not mean output capture envelopes exist. It does not mean a dry run executed. It does not mean candidate outputs exist. It does not mean contract conformance can validate reliability. It does not mean contract conformance can score cases. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Next safe milestone

After MLRT-12 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-13 Candidate First Non-Runtime Dry-Run Execution Plan
```

The next milestone must remain governed and non-runtime. It may only plan the first non-runtime dry-run execution. It must not yet execute a dry run, create candidate outputs, score cases, validate reliability, authorize routing, activate Pilot, activate Copilot, or unlock runtime ML implementation.
