# MLRT-10 Candidate Non-Runtime Dry-Run Output Capture Rejection Gate Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_output_capture_rejection_gate_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only planning milestone.

## Purpose

MLRT-10 defines a future non-runtime dry-run output-capture rejection gate plan after MLRT-9 output-capture planning has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This milestone exists to describe how future captured candidate outputs would be rejected, blocked, or escalated when they are malformed, unsafe, ambiguous, authority-seeking, or outside the declared dry-run contract. It does not create output records, create rejection records, capture candidate outputs, execute candidates, execute cases, score cases, compare routes, validate reliability, or unlock ML implementation.

## Hard boundary

MLRT-10 is documentation-only. It does not create rejection records and does not run a rejection gate. It does not create dry-run output records, does not create output capture rejection records, does not execute a dry run, does not execute a candidate, does not execute cases, does not score cases, does not validate candidate reliability, and does not unlock ML implementation. It does not:

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

Neither MLRT-9 nor MLRT-10 validates candidate reliability.

## Rejection gate identity doctrine

A future output-capture rejection gate record, if later approved by a separate governed milestone, must identify:

- rejection gate record identity
- MLRT phase reference
- MLRT-7 dry-run protocol reference
- MLRT-8 dry-run input-set reference
- MLRT-9 output-capture plan reference
- candidate package reference
- candidate output capture envelope reference
- input-to-output correlation reference
- output contract version reference
- rejection contract version reference
- human-review escalation status
- non-authoritative-only status

MLRT-10 does not create these records. It defines only that such identity would be mandatory later.

## Mandatory rejection families

Future output-capture rejection gating must be able to classify candidate output problems into non-authoritative rejection families, including:

- missing output
- duplicate output
- uncorrelated output
- malformed output
- unparsable output
- contract-incomplete output
- forbidden field output
- route-authority seeking output
- prompt-loading seeking output
- runtime-command seeking output
- provider-call seeking output
- embedding-call seeking output
- network-call seeking output
- subprocess-call seeking output
- batch-mode seeking output
- persistence seeking output
- freeze-write seeking output
- gold-registry-write seeking output
- prompt-library-write seeking output
- router-canon-write seeking output
- startup-pack-write seeking output
- activation seeking output
- field-test seeking output
- runtime Pilot seeking output
- Copilot seeking output
- human-review required output

These are planning categories only. MLRT-10 does not run any classifier, validator, or rejection gate.

## Critical-boundary blocker doctrine

Future rejection gating must block or escalate every captured output that contains or implies a critical boundary violation. Critical boundary blockers include:

- route decisions
- live prompt loading
- runtime command execution
- dry-run execution approval
- provider calls
- embedding calls
- network calls
- subprocess calls
- batch mode
- persistent ML decisions
- file persistence outside a separately approved non-runtime evidence plan
- freeze memory writes
- gold registry writes
- prompt-library writes
- router-canon writes
- startup-pack writes
- activation keys
- field-test enablement
- runtime Pilot behavior
- Copilot behavior

A future blocker must never become a pass, score, reliability claim, approval, activation signal, or runtime signal.

## Rejection outcome labels doctrine

Future rejection-gate planning may use labels such as:

- output_rejected_missing
- output_rejected_duplicate
- output_rejected_uncorrelated
- output_rejected_unparsable
- output_rejected_contract_incomplete
- output_rejected_forbidden_authority_field
- output_rejected_critical_boundary_violation
- output_rejected_persistence_or_mutation_attempt
- output_rejected_provider_embedding_network_or_subprocess_attempt
- output_rejected_activation_field_test_pilot_or_copilot_attempt
- output_requires_human_review
- output_capture_ready_for_later_contract_conformance_planning_only

These labels must remain non-authoritative. They must not validate candidate reliability, score a case, approve a candidate, or authorize execution.

## Human-review escalation doctrine

Future rejection gating must escalate ambiguous, malformed, authority-seeking, persistence-seeking, or boundary-risk candidate outputs to human review.

Human review escalation must not equal approval. It must not write freeze memory, approve readiness, approve reliability, unlock ML implementation, grant route authority, activate a candidate, enable field testing, create runtime Pilot behavior, or create Copilot behavior.

## No silent coercion doctrine

Future rejection gating must not repair, normalize into safety, rewrite, reinterpret, or coerce unsafe candidate output into a passing shape. A captured output that is malformed, ambiguous, or authority-seeking must remain rejected or escalated.

## No-live-read doctrine

Future rejection gating must not read live prompt-library files, live freeze memory, live router canon, runtime router modules, current project state, provider endpoints, embedding stores, vector stores, or network sources to decide, repair, or reinterpret candidate output.

Any future rejection gate must use only predeclared static input references and candidate output material supplied under the governed dry-run protocol.

## No mutation doctrine

Future rejection gating must not mutate:

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

MLRT-10 creates no mutating code and no mutating records.

## Forbidden authority fields

Future dry-run output-capture rejection gate envelopes must not contain active authority fields. Forbidden fields include:

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

If a future candidate output contains these fields, the output-capture rejection gate plan must treat that as rejection or human escalation under a later governed milestone.

## Positive label

The only positive MLRT-10 label is:

```text
MLRT_OUTPUT_CAPTURE_REJECTION_GATE_READY_FOR_NON_RUNTIME_CAPTURE_CONFORMANCE_PLANNING_ONLY
```

This label means only that the documentation-only output-capture rejection gate plan is ready for the next planning milestone after local validation and freeze.

It does not mean that output capture records exist. It does not mean rejection gate records exist. It does not mean a rejection gate has run. It does not mean a dry run executed. It does not mean candidate outputs exist. It does not mean output capture can validate reliability. It does not mean output capture can score cases. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Next safe milestone

After MLRT-10 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-11 Candidate Non-Runtime Dry-Run Output Capture Contract-Conformance Plan
```

The next milestone must remain governed and non-runtime. It may only plan output-capture contract-conformance handling. It must not execute a dry run, create output records, score cases, validate reliability, or unlock ML implementation.
