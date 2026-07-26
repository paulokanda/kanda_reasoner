# MLRT-13 Candidate First Non-Runtime Dry-Run Execution Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_execution_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only first dry-run execution planning milestone.

## Purpose

MLRT-13 defines the first governed non-runtime dry-run execution plan after MLRT-12 contract-conformance rejection-gate planning has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This is a roadmap transition point. Earlier MLRT milestones prepared protocol, input-set, output-capture, rejection, contract-conformance, and rejection-gate doctrine. MLRT-13 is the first milestone that names the future first non-runtime dry-run execution path. It still does not execute a dry run. It does not create dry-run records, candidate outputs, case outputs, scores, comparisons, reports, reliability evidence, route decisions, prompt loading, provider calls, persistence, activation, Pilot behavior, or Copilot behavior. It does not execute a candidate.

## Roadmap position

This is roadmap progress, not a loop. The MLRT chain has moved through distinct blocking layers:

```text
MLRT-7  - future dry-run protocol planning
MLRT-8  - future dry-run input-set planning
MLRT-9  - future dry-run output-capture planning
MLRT-10 - future output-capture rejection-gate planning
MLRT-11 - future output-capture contract-conformance planning
MLRT-12 - future contract-conformance rejection-gate planning
MLRT-13 - first non-runtime dry-run execution planning
```

MLRT-13 exists because MLRT-12 confirmed that the project may proceed to first dry-run execution planning only. It does not convert planning into execution.

## Hard boundary

MLRT-13 is documentation-only. It does not run a dry run. It does not create a harness. It does not create a runner. It does not create executable validators. It does not create schemas. It does not create dry-run execution records. It does not create candidate outputs. It does not run cases. It does not score cases. It does not compare routes. It does not generate reports. It does not validate reliability. It does not unlock ML implementation.

MLRT-13 must not:

- run a dry run
- create dry-run execution records
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
- create a harness
- create a runner
- create executable validators
- create schema code
- create candidate outputs
- execute a candidate
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

## Planned future first dry-run identity

A future first non-runtime dry-run execution record, if later allowed by a separate governed milestone, must identify:

- dry-run execution record identity
- MLRT phase reference
- MLRT-7 protocol reference
- MLRT-8 input-set reference
- MLRT-9 output-capture reference
- MLRT-10 output-capture rejection-gate reference
- MLRT-11 contract-conformance reference
- MLRT-12 contract-conformance rejection-gate reference
- candidate package reference
- candidate static-review outcome reference
- dry-run input-set hash reference
- dry-run execution harness reference
- output capture envelope reference
- abort condition set reference
- human-review escalation status
- non-authoritative-only status

MLRT-13 does not create these records. It only defines that such identity will be mandatory before any later execution can be allowed.

## Planned first dry-run phases

A future first non-runtime dry-run execution may only be planned as a staged, abortable, non-authoritative process:

1. verify frozen MLRT chain references
2. verify candidate package reference is static and caller-supplied
3. verify input-set reference is static and caller-supplied
4. verify no live prompt-library, live freeze-memory, or live router-canon reads
5. verify no provider, embedding, network, subprocess, batch, persistence, activation, Pilot, or Copilot surface
6. prepare isolated non-runtime invocation envelope
7. prepare output-capture envelope
8. prepare rejection and contract-conformance gates
9. prepare human-review escalation path
10. stop before any real execution unless a later governed milestone explicitly authorizes non-runtime dry-run execution

These are planning phases only. MLRT-13 does not execute phase 6 or any later phase.

## Planned abort conditions

A future first non-runtime dry-run execution plan must abort before invocation if any of these are present:

- missing frozen MLRT-7 through MLRT-12 references
- missing candidate package reference
- missing candidate static-review outcome reference
- missing dry-run input-set reference
- mismatched hash reference
- malformed candidate invocation envelope
- any live prompt-library read
- any live freeze-memory read
- any live router-canon read
- any runtime router import
- any route-authority field
- any prompt-loading field
- any provider call field
- any embedding/vector-store field
- any network field
- any subprocess field
- any batch-mode field
- any persistence or ML-decision-storage field
- any activation or field-test field
- any runtime Pilot field
- any Copilot field
- any ambiguity requiring human review

Abort labels remain non-authoritative and must not become route decisions, readiness approvals, reliability approvals, freeze writes, activation signals, Pilot instructions, or Copilot instructions.

## Planned non-runtime invocation envelope doctrine

A future invocation envelope must be static, caller-supplied, non-authoritative, and isolated. It may describe input and output expectations, but it must not:

- load prompts
- discover cases dynamically
- read live project state
- call a provider
- call an embedding model
- access a vector store
- access the network
- spawn subprocesses
- persist results
- mutate gold data
- mutate canon
- mutate prompt library
- mutate freeze memory
- write approvals
- trigger Pilot or Copilot behavior

MLRT-13 does not create an invocation envelope.

## Planned output handling doctrine

A future first dry-run output must be captured into a non-authoritative output-capture envelope and then passed through rejection and contract-conformance gates. The output must not be used as:

- a route decision
- a prompt-loading instruction
- an installation command
- an execution command
- a freeze-memory write
- a human approval
- a readiness approval
- a reliability approval
- an activation signal
- a field-test signal
- a runtime Pilot command
- a Copilot instruction

MLRT-13 does not create output capture envelopes and does not create candidate outputs.

## No reliability claim doctrine

MLRT-13 must not be interpreted as candidate reliability evidence. Even a future first dry run, once separately authorized and executed, would only create early non-runtime evidence that would still require later scoring, review, rejection analysis, repeatability checks, and reliability gates.

MLRT-13 does not say the candidate works. It does not say the candidate is safe. It does not say the candidate can route. It does not say the candidate can be used by Pilot or Copilot.

## Positive label doctrine

The only positive MLRT-13 label is:

```text
MLRT_FIRST_NON_RUNTIME_DRY_RUN_EXECUTION_PLAN_READY_FOR_HARNESS_SKELETON_PLANNING_ONLY
```

This label means only that first non-runtime dry-run execution planning is documented and ready to proceed to a future harness-skeleton planning milestone after local validation, freeze, startup context refresh, and `FREEZE_MEMORY_STATUS: OK`.

It does not mean a harness exists. It does not mean a dry run has executed. It does not mean candidate outputs exist. It does not mean cases were executed. It does not mean scores exist. It does not mean reports exist. It does not mean candidate reliability is validated. It does not mean ML implementation is unlocked.

## Forbidden authority fields

Future dry-run planning, invocation, output capture, or result handling must reject or escalate any presence of:

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

After MLRT-13 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-14 Candidate First Non-Runtime Dry-Run Harness Skeleton Plan
```

The next milestone must remain governed and non-runtime. It may only plan a future harness skeleton. It must not yet execute a dry run, create candidate outputs, score cases, validate reliability, authorize routing, activate Pilot, activate Copilot, or unlock runtime ML implementation.
