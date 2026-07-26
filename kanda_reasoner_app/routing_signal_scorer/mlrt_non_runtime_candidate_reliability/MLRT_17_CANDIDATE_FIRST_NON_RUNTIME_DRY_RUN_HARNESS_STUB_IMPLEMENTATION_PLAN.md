# MLRT-17 Candidate First Non-Runtime Dry-Run Harness Stub Implementation Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_implementation_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only first non-runtime dry-run harness stub implementation planning milestone.

## Purpose

MLRT-17 defines the future harness stub implementation plan after MLRT-16 Candidate First Non-Runtime Dry-Run Harness Implementation Boundary Plan has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This is roadmap progress toward a future first non-runtime dry-run harness stub, but it is still not stub code and not a harness implementation. MLRT-17 does not create harness code, does not create runner code, does not create harness stub files, does not create module files, does not create executable validators, does not create schema code, does not create contract schema files, does not implement a boundary checker, does not execute a dry run, does not execute a candidate, does not create candidate outputs, does not execute cases, does not score cases, does not compare routes, does not generate reports, does not validate candidate reliability, and does not unlock ML implementation.

## Roadmap position

MLRT-17 is not a loop. It narrows the next blocker after MLRT-16:

```text
MLRT-13 - first non-runtime dry-run execution planning
MLRT-14 - future harness skeleton planning
MLRT-15 - future harness contract planning
MLRT-16 - future harness implementation boundary planning
MLRT-17 - future harness stub implementation planning
```

The purpose of this step is to define what a future stub implementation may be allowed to contain before any source-surface milestone is considered.

## Hard boundary

MLRT-17 is documentation-only. It does not create a harness. It does not create a runner. It does not create harness stub files. It does not create implementation modules. It does not create executable validators. It does not create schema code. It does not create a harness contract file. It does not implement a harness boundary checker. It does not execute a dry run. It does not execute a candidate. It does not create dry-run execution records. It does not create candidate outputs. It does not run cases. It does not score cases. It does not compare routes. It does not generate reports. It does not validate candidate reliability. It does not unlock ML implementation.

MLRT-17 must not:

- create harness code
- create runner code
- create harness stub files
- create implementation modules
- create executable validators
- create schema code
- create contract schema files
- create harness contract implementation files
- create boundary checker implementation files
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

## Planned stub implementation identity

A future harness stub, if later authorized by a separate governed milestone, must be named and shaped as a non-runtime, non-authoritative, deterministic adapter boundary. It must not be a router, not a runner, not a prompt loader, not a provider adapter, not an embedding adapter, not a persistence writer, not an approval writer, not an activation mechanism, not a Pilot mechanism, and not a Copilot mechanism.

A future stub implementation plan may describe only:

- the future stub purpose
- the future stub file identity
- the future stub public surface
- the future stub input bundle boundary
- the future stub output envelope boundary
- the future stub abort behavior
- the future stub no-live-read doctrine
- the future stub no-authority doctrine
- the future stub no-execution doctrine
- the future stub no-reliability-claim doctrine

MLRT-17 does not create these future files or surfaces as code. It only defines that any future stub must be preceded by a source-surface planning milestone.

## Planned stub source-surface constraints

A future source-surface milestone may plan a stub source file only if it remains standard-library-only, import-isolated, deterministic, and in-memory-only. It must not import runtime router modules. It must not import prompt-library files. It must not import freeze-memory files. It must not import provider libraries. It must not import embedding libraries. It must not perform network calls. It must not perform subprocess calls. It must not write persistent files. It must not create live execution records.

The future source surface may only plan non-authoritative functions that return planning envelopes or abort labels from caller-supplied static data. The future source surface must not run candidates, must not run cases, must not score outputs, must not compare routes, and must not generate persisted reports.

## Planned allowed stub behaviors

A future stub implementation plan may allow only these non-runtime behaviors to be planned:

- accept caller-supplied in-memory static input bundle
- accept caller-supplied in-memory static candidate descriptor
- check that required in-memory fields are present
- return deterministic abort labels when required fields are absent
- return deterministic non-authoritative planning envelope metadata
- declare that no dry run has executed
- declare that no candidate has executed
- declare that no candidate output exists
- declare that no reliability claim is made
- declare that human review remains required

These are future planned behaviors only. MLRT-17 does not implement them.

## Planned prohibited stub behaviors

A future stub must prohibit and abort on:

- live prompt-library read
- live freeze-memory read
- live router-canon read
- runtime router import
- candidate package import
- candidate execution command
- dry-run execution command
- case execution command
- scoring command
- route comparison command
- report persistence command
- approval write command
- freeze write command
- gold registry write command
- startup pack write command
- provider call command
- embedding call command
- vector-store call command
- network call command
- subprocess call command
- batch-mode command
- persistent ML decision command
- activation command
- field-test command
- runtime Pilot command
- Copilot instruction command

## Stub abort doctrine

A future stub implementation plan must require abort before any candidate-facing, dry-run-facing, or output-facing operation if it detects:

- missing MLRT-16 freeze reference
- missing MLRT-15 freeze reference
- missing MLRT-14 freeze reference
- missing MLRT-13 freeze reference
- missing static candidate descriptor
- missing static input bundle
- hash mismatch
- unexpected live project read
- unexpected runtime import
- unexpected provider, embedding, network, subprocess, batch, persistence, activation, Pilot, or Copilot field
- any route-authority field
- any prompt-loading field
- any approval-write field
- any reliability-claim field

Abort labels remain non-authoritative and must not become route decisions, readiness approvals, reliability approvals, freeze writes, activation signals, Pilot instructions, or Copilot instructions.

## No implementation doctrine

MLRT-17 must not be interpreted as authorization to implement the stub. It only defines the future harness stub implementation plan. A later governed milestone must explicitly define a source surface before any code is written. A later code milestone, if ever approved, must remain non-runtime and non-authoritative.

## No reliability claim doctrine

MLRT-17 is not candidate reliability evidence. It does not show that a stub exists, that a harness exists, that a candidate can run, that output can be captured, that contracts pass, that cases can be scored, or that routing is safe. Candidate reliability remains unvalidated and ML implementation remains locked.

## Positive label doctrine

The only positive MLRT-17 label is:

```text
MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_IMPLEMENTATION_PLAN_READY_FOR_STUB_SOURCE_SURFACE_PLANNING_ONLY
```

This label means only that future harness stub implementation planning is documented and ready to proceed to a future source-surface planning milestone after local validation, freeze, startup context refresh, and `FREEZE_MEMORY_STATUS: OK`.

It does not mean a harness exists. It does not mean runner code exists. It does not mean harness stub files exist. It does not mean implementation modules exist. It does not mean a boundary checker exists. It does not mean a contract schema exists. It does not mean a dry run has executed. It does not mean candidate outputs exist. It does not mean cases were executed. It does not mean scores exist. It does not mean reports exist. It does not mean candidate reliability is validated. It does not mean ML implementation is unlocked.

## Forbidden authority fields

Future stub implementation plans, source-surface plans, stub implementations, harness contracts, harness invocations, output capture, result handling, or contract conformance must reject or escalate any presence of:

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

After MLRT-17 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-18 Candidate First Non-Runtime Dry-Run Harness Stub Source Surface Plan
```

The next milestone must remain governed and non-runtime. It may only plan the future source surface for a harness stub inside the MLRT-16 boundary and MLRT-17 stub plan. It must not yet create code, execute a dry run, create candidate outputs, score cases, validate reliability, authorize routing, activate Pilot, activate Copilot, or unlock runtime ML implementation.
