# MLRT-11 Candidate Non-Runtime Dry-Run Output Capture Contract-Conformance Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_output_capture_contract_conformance_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only planning milestone.

## Purpose

MLRT-11 defines a future non-runtime dry-run output-capture contract-conformance plan after MLRT-10 output-capture rejection-gate planning has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This milestone exists to describe how future captured candidate outputs would be checked against a declared non-runtime dry-run output contract. It defines planning doctrine only. It does not create conformance records, run a conformance check, capture outputs, execute dry runs, execute candidates, execute cases, score cases, compare routes, validate reliability, or unlock ML implementation.

## Hard boundary

MLRT-11 is documentation-only. It does not create contract-conformance records and does not run a contract-conformance check and does not run a conformance check. It does not create output records, does not create output manifests, does not create output capture envelopes, does not create output capture rejection records, does not create conformance evidence, does not execute a dry run, does not execute a candidate, does not execute cases, does not score cases, does not validate candidate reliability, and does not unlock ML implementation. It does not:

- create dry-run output records
- create dry-run output manifests
- create output capture envelopes
- create output capture rejection records
- create output rejection gate records
- run an output rejection gate
- create contract-conformance records
- create contract-conformance evidence
- run a contract-conformance check
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

Neither MLRT-10 nor MLRT-11 validates candidate reliability.

## Contract-conformance identity doctrine

A future contract-conformance record, if later approved by a separate governed milestone, must identify:

- conformance record identity
- MLRT phase reference
- MLRT-7 dry-run protocol reference
- MLRT-8 dry-run input-set reference
- MLRT-9 output-capture plan reference
- MLRT-10 output-capture rejection gate reference
- candidate package reference
- candidate output capture envelope reference
- input-to-output correlation reference
- output contract version reference
- output field contract reference
- rejection contract version reference
- conformance rule-set version reference
- human-review escalation status
- non-authoritative-only status

MLRT-11 does not create these records. It defines only that such identity would be mandatory later.

## Contract-conformance families

Future contract-conformance checking must be able to classify captured candidate output against non-authoritative conformance families, including:

- required field presence
- required field type
- required field value domain
- required field cardinality
- required field canonicalization
- required rejection envelope shape
- required non-authoritative label domain
- input-to-output correlation consistency
- candidate package identity consistency
- dry-run protocol reference consistency
- static case reference consistency
- missing optional-field tolerance
- unknown field rejection
- forbidden authority-field rejection
- forbidden mutation-field rejection
- forbidden runtime-command rejection
- forbidden provider embedding network subprocess or batch-mode rejection
- forbidden activation field-test Pilot or Copilot rejection
- human-review escalation trigger

These are planning categories only. MLRT-11 does not run any validator, conformance checker, parser, classifier, or rejection gate.

## Mandatory conformance questions

Future contract-conformance planning must be able to ask, without performing the check in MLRT-11:

- Does the captured output contain every required non-authoritative output field?
- Does the captured output omit every forbidden authority field?
- Does the captured output preserve input-to-output correlation?
- Does the captured output stay inside the declared output contract version?
- Does the captured output avoid prompt-loading, routing, activation, runtime, provider, embedding, network, subprocess, batch-mode, persistence, and freeze-write behavior?
- Does the captured output require human review because it is ambiguous, malformed, or boundary-risking?
- Does the captured output remain non-authoritative even if it appears structurally conformant?

MLRT-11 answers none of these questions for a real candidate output. It only defines that the questions would be mandatory later.

## Conformance outcome-label doctrine

Future contract-conformance planning may use labels such as:

- output_contract_conformance_not_checked
- output_contract_conformance_blocked_missing_output
- output_contract_conformance_rejected_missing_required_field
- output_contract_conformance_rejected_invalid_field_type
- output_contract_conformance_rejected_invalid_field_value
- output_contract_conformance_rejected_unknown_field
- output_contract_conformance_rejected_forbidden_authority_field
- output_contract_conformance_rejected_forbidden_mutation_field
- output_contract_conformance_rejected_runtime_or_provider_attempt
- output_contract_conformance_rejected_activation_field_test_pilot_or_copilot_attempt
- output_contract_conformance_requires_human_review
- output_capture_contract_conformance_ready_for_later_rejection_gate_planning_only

These labels must remain non-authoritative. They must not validate candidate reliability, score a case, approve a candidate, approve a dry run, or authorize execution.

## No pass-to-reliability doctrine

A future structurally conformant output must not become a reliability claim. Passing contract-conformance, if later implemented under separate governance, would only mean that a captured non-runtime output appears to match the declared envelope shape. It must not mean:

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

## Human-review escalation doctrine

Future contract-conformance planning must escalate ambiguous, malformed, unknown-field, authority-field, mutation-field, persistence-seeking, or boundary-risking candidate outputs to human review.

Human review escalation must not equal approval. It must not write freeze memory, approve readiness, approve reliability, unlock ML implementation, grant route authority, activate a candidate, enable field testing, create runtime Pilot behavior, or create Copilot behavior.

## No silent coercion doctrine

Future contract-conformance handling must not repair, normalize into safety, rewrite, reinterpret, or coerce a candidate output into a passing contract shape. A captured output that is malformed, ambiguous, unknown-field, or authority-seeking must remain rejected or escalated.

## No-live-read doctrine

Future contract-conformance handling must not read live prompt-library files, live freeze memory, live router canon, runtime router modules, current project state, provider endpoints, embedding stores, vector stores, or network sources to decide, repair, or reinterpret candidate output.

Any future conformance check must use only predeclared static input references, declared output contracts, and candidate output material supplied under the governed dry-run protocol.

## No mutation doctrine

Future contract-conformance handling must not mutate:

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

MLRT-11 creates no mutating code and no mutating records.

## Forbidden authority fields

Future dry-run output-capture contract-conformance envelopes must not contain active authority fields. Forbidden fields include:

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

If a future candidate output contains these fields, contract-conformance planning must treat that as rejection or human escalation under a later governed milestone.

## Positive label

The only positive MLRT-11 label is:

```text
MLRT_OUTPUT_CAPTURE_CONTRACT_CONFORMANCE_READY_FOR_CONFORMANCE_REJECTION_GATE_PLANNING_ONLY
```

This label means only that the documentation-only contract-conformance plan is ready for the next planning milestone after local validation and freeze.

It does not mean that conformance records exist. It does not mean a conformance check has run. It does not mean output records exist. It does not mean output capture envelopes exist. It does not mean output rejection gates have run. It does not mean a dry run executed. It does not mean candidate outputs exist. It does not mean contract conformance can validate reliability. It does not mean contract conformance can score cases. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Next safe milestone

After MLRT-11 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-12 Candidate Non-Runtime Dry-Run Contract-Conformance Rejection Gate Plan
```

The next milestone must remain governed and non-runtime. It may only plan contract-conformance rejection-gate handling. It must not execute a dry run, create output records, run conformance checks, score cases, validate reliability, or unlock ML implementation.
