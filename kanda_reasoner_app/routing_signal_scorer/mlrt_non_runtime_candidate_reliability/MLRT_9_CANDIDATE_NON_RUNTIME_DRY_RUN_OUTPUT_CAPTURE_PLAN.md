# MLRT-9 Candidate Non-Runtime Dry-Run Output Capture Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_output_capture_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only planning milestone.

## Purpose

MLRT-9 defines a future non-runtime dry-run output capture plan after MLRT-8 input-set planning has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This milestone exists to describe how future non-authoritative dry-run output capture would be planned. It does not create output records, capture candidate outputs, execute candidates, execute cases, score cases, compare routes, validate reliability, or unlock ML implementation.

## Hard boundary

MLRT-9 is documentation-only. It does not:

- create dry-run output records
- create dry-run output manifests
- create output capture envelopes
- create output capture rejection records
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

Neither MLRT-8 nor MLRT-9 validates candidate reliability.


MLRT-9 does not create dry-run output records, does not create dry-run output manifests, does not create output capture envelopes, and does not create output capture rejection records. It does not create dry-run input records, does not execute a dry run, does not execute a candidate, does not execute cases, does not score cases, does not validate candidate reliability, and does not unlock ML implementation.

## Output capture identity and traceability doctrine

A future dry-run output capture record, if later approved by a separate governed milestone, must be traceable to:

- the MLRT phase reference
- the MLRT-7 dry-run protocol plan reference
- the MLRT-8 dry-run input-set plan reference
- the candidate package reference
- the static case reference
- the dry-run input envelope reference
- the candidate interface version reference
- the output contract version reference
- the rejection contract version reference
- the frozen canon or fixture reference declared by the input set

MLRT-9 does not create those records. It only defines that traceability would be mandatory later.

## Required input-to-output correlation doctrine

Future output capture must correlate every captured output to exactly one future input-set item. The correlation must not be inferred from live project reads, live prompt-library files, live freeze memory, or live router canon.

The future capture plan must reject ambiguous, duplicated, missing, or untraceable output correlation. MLRT-9 does not perform that rejection.

## Candidate raw output containment doctrine

Future output capture must keep candidate raw output non-authoritative. Candidate raw output must not become:

- route decisions
- prompt loading instructions
- install commands
- dry-run execution commands
- case scoring commands
- freeze writes
- human approvals
- readiness approvals
- reliability approvals
- activation signals
- field-test signals
- runtime Pilot commands
- Copilot instructions

## Normalized output envelope doctrine

A future normalized output capture envelope, if separately approved later, must be non-authoritative and must preserve:

- output capture identity
- input envelope reference
- candidate package reference
- candidate version reference
- dry-run protocol reference
- dry-run input-set reference
- raw candidate output reference or hash
- normalized candidate output fields
- parse status
- contract-conformance status
- rejection status
- boundary-risk flags
- critical-boundary flags
- human-review-required flag
- non-authoritative-only flag
- no-route-authority flag
- no-prompt-loading flag
- no-persistence flag
- no-provider-call flag
- no-embedding-call flag
- no-network-call flag
- no-subprocess-call flag
- no-batch-mode flag
- no-activation flag
- no-field-test flag
- no-runtime-pilot flag
- no-copilot flag

MLRT-9 does not define executable schemas or validators for this envelope.

## Parse and contract-conformance status doctrine

Future capture planning may distinguish statuses such as:

- output absent
- output present but unparsable
- output parseable but contract-incomplete
- output parseable and contract-shaped
- output rejected by boundary flags
- output needs human review
- output ready for later non-runtime comparison planning only

These labels must remain planning labels. They must not validate reliability or authorize execution.

## Capture failure and rejection doctrine

Future output capture must be able to represent failures without creating route decisions or runtime effects. Rejection must be mandatory for any captured output that contains or implies:

- route authority
- prompt loading
- runtime command execution
- dry-run execution approval
- provider calls
- embedding calls
- network calls
- subprocess calls
- batch mode
- persistence
- freeze writes
- gold registry writes
- prompt-library writes
- router-canon writes
- startup-pack writes
- activation keys
- field-test enablement
- runtime Pilot behavior
- Copilot behavior

MLRT-9 plans the doctrine only. It creates no rejection records.

## Boundary-risk flag doctrine

Future output capture must preserve boundary-risk flags in a non-authoritative wrapper. Boundary flags must be visible to human review and must never silently coerce an output into a pass.

Critical boundary violations remain zero-tolerance. A future candidate output containing critical boundary risk must be rejected or escalated by later governed logic, not accepted.

## No-live-read doctrine

Future output capture must not read live prompt-library files, live freeze memory, live router canon, runtime router modules, current project state, provider endpoints, embedding stores, vector stores, or network sources to improve, repair, or reinterpret candidate output.

Any future capture must use only predeclared static input references and candidate output material supplied under the governed dry-run protocol.

## Capture hash and canonicalization doctrine

Future output capture must have a deterministic canonicalization and hash plan for captured output material. The hash plan must distinguish:

- raw candidate output hash
- normalized wrapper hash
- input envelope hash reference
- candidate package hash reference
- static case hash reference
- dry-run protocol hash reference

MLRT-9 does not create hashes and does not create output files.

## Human-review escalation doctrine

Future output capture must escalate to human review when output is ambiguous, malformed, boundary-risk flagged, authority-seeking, persistence-seeking, or incompatible with the declared contract.

Human review escalation must not equal approval. It must not write freeze memory, approve readiness, approve reliability, unlock ML implementation, or authorize runtime behavior.

## Forbidden authority fields

Future dry-run output capture envelopes must not contain active authority fields. Forbidden fields include:

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

If a future candidate output contains these fields, the output capture plan must treat that as rejection or human escalation under a later governed milestone.

## Positive label

The only positive MLRT-9 label is:

```text
MLRT_DRY_RUN_OUTPUT_CAPTURE_READY_FOR_CAPTURE_REJECTION_GATE_PLANNING_ONLY
```

This label means only that the documentation-only output capture plan is ready for the next planning milestone after local validation and freeze.

It does not mean that output capture records exist. It does not mean a dry run executed. It does not mean candidate outputs exist. It does not mean output capture can validate reliability. It does not mean output capture can score cases. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Next safe milestone

After MLRT-9 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-10 - Candidate Non-Runtime Dry-Run Output Capture Rejection Gate Plan
```

The next milestone must remain governed and non-runtime. It may only plan output-capture rejection gating. It must not execute a dry run, create output records, score cases, validate reliability, or unlock ML implementation.
