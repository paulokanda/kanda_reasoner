# MLRT-14 Candidate First Non-Runtime Dry-Run Harness Skeleton Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_skeleton_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only first non-runtime dry-run harness skeleton planning milestone.

## Purpose

MLRT-14 defines the future harness skeleton plan after MLRT-13 Candidate First Non-Runtime Dry-Run Execution Plan has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This is roadmap progress toward a first non-runtime dry-run harness, but it is still not a harness implementation. MLRT-14 does not create harness code, does not create runner code, does not create executable validators, does not create schemas, dry-run execution records, candidate outputs, case outputs, scores, comparisons, reports, reliability evidence, route decisions, prompt loading, provider calls, persistence, activation, Pilot behavior, or Copilot behavior. It does not execute a candidate and does not execute a dry run.

## Roadmap position

MLRT-14 is not a loop. It narrows the next blocker after MLRT-13:

```text
MLRT-13 - first non-runtime dry-run execution planning
MLRT-14 - future harness skeleton planning
```

The purpose of this step is to define what a future non-runtime harness skeleton may be allowed to contain before any code is created in a later governed milestone.

## Hard boundary

MLRT-14 is documentation-only. It does not create a harness. It does not create a runner. It does not create executable validators. It does not create schema code. It does not execute a dry run. It does not execute a candidate. It does not create dry-run execution records. It does not create candidate outputs. It does not run cases. It does not score cases. It does not compare routes. It does not generate reports. It does not validate candidate reliability. It does not unlock ML implementation.

MLRT-14 must not:

- create harness code
- create runner code
- create executable validators
- create schema code
- create dry-run execution records
- run a dry run
- execute a candidate
- create candidate outputs
- run cases
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
- create dry-run input records
- create dry-run input manifests
- create dry-run output records
- create dry-run output manifests
- create output capture envelopes
- create output capture rejection records
- create output rejection gate records
- run an output rejection gate
- create contract-conformance records
- create contract-conformance evidence
- run a contract-conformance check
- create contract-conformance rejection records
- run a contract-conformance rejection gate
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

## Planned harness skeleton identity

A future harness skeleton, if later allowed by a separate governed implementation milestone, must identify itself as a non-runtime, non-authoritative, isolated test scaffold. It must include only static references to already-governed inputs and must not discover or mutate project state.

A future harness skeleton identity may require:

- harness skeleton identity
- MLRT phase reference
- MLRT-13 execution-plan reference
- MLRT-12 contract-conformance rejection-gate reference
- dry-run protocol reference
- dry-run input-set reference
- candidate package reference
- candidate static-review outcome reference
- no-live-read declaration
- no-route-authority declaration
- no-provider-call declaration
- no-persistence declaration
- no-activation declaration
- no-Pilot declaration
- no-Copilot declaration

MLRT-14 does not create this identity record. It only defines that the identity will be mandatory for any later harness skeleton.

## Planned harness skeleton allowed shape

A future harness skeleton may only be planned as a minimal non-runtime scaffold. It may define names for later, still-disabled surfaces such as:

- static input reference acceptance
- candidate reference acceptance
- preflight boundary checks
- abort-condition routing to non-authoritative labels
- invocation envelope placeholder
- output-capture envelope placeholder
- rejection-gate placeholder
- contract-conformance placeholder
- human-review escalation placeholder
- final no-authority return object placeholder

These are placeholders only. In this milestone they are not implemented as code, not executed, and not connected to any candidate, router, prompt loader, provider, persistence layer, Pilot, or Copilot.

## Planned harness skeleton forbidden shape

A future harness skeleton must not contain any direct or indirect runtime authority surface. It must not contain:

- prompt loader integrations
- provider integrations
- embedding integrations
- vector-store integrations
- network integrations
- subprocess integrations
- batch-mode integrations
- runtime router imports
- route-decision emitters
- report writers
- persistent ML-decision writers
- approval writers
- activation writers
- field-test toggles
- Pilot command emitters
- Copilot instruction emitters

## Planned harness skeleton abort doctrine

A future harness skeleton must abort before any candidate-facing operation if it detects:

- missing MLRT-13 freeze reference
- missing MLRT-12 freeze reference
- missing static candidate reference
- missing static dry-run input reference
- hash mismatch
- unexpected live project read
- unexpected runtime import
- unexpected provider, embedding, network, subprocess, batch, persistence, activation, Pilot, or Copilot field
- ambiguous human-review state
- any route-authority field
- any prompt-loading field

Abort labels remain non-authoritative and must not become route decisions, readiness approvals, reliability approvals, freeze writes, activation signals, Pilot instructions, or Copilot instructions.

## No execution doctrine

MLRT-14 must not be interpreted as authorization to create or run the harness. It only defines the future harness skeleton plan. A later governed milestone must explicitly authorize any skeleton implementation, and even that implementation must remain non-runtime and non-authoritative.

## No reliability claim doctrine

MLRT-14 is not candidate reliability evidence. It does not show that a candidate can run, that output can be captured, that contracts pass, that cases can be scored, or that routing is safe. Candidate reliability remains unvalidated and ML implementation remains locked.

## Positive label doctrine

The only positive MLRT-14 label is:

```text
MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_SKELETON_PLAN_READY_FOR_HARNESS_CONTRACT_PLANNING_ONLY
```

This label means only that future harness skeleton planning is documented and ready to proceed to a future harness contract planning milestone after local validation, freeze, startup context refresh, and `FREEZE_MEMORY_STATUS: OK`.

It does not mean a harness exists. It does not mean runner code exists. It does not mean a dry run has executed. It does not mean candidate outputs exist. It does not mean cases were executed. It does not mean scores exist. It does not mean reports exist. It does not mean candidate reliability is validated. It does not mean ML implementation is unlocked.

## Forbidden authority fields

Future harness planning, skeleton implementation, invocation, output capture, or result handling must reject or escalate any presence of:

```text
route_decision
load_prompt
execute_route
execute_dry_run
execute_candidate
run_case
score_case
compare_route
create_report
persist_report
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

## Next safe milestone

After MLRT-14 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-15 Candidate First Non-Runtime Dry-Run Harness Contract Plan
```

The next milestone must remain governed and non-runtime. It may only define the future harness contract. It must not yet execute a dry run, create candidate outputs, score cases, validate reliability, authorize routing, activate Pilot, activate Copilot, or unlock runtime ML implementation.
