# MLRT-18 Candidate First Non-Runtime Dry-Run Harness Stub Source Surface Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_source_surface_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only first non-runtime dry-run harness stub source-surface planning milestone.

## Purpose

MLRT-18 defines the future source-surface plan for a non-runtime harness stub after MLRT-17 Candidate First Non-Runtime Dry-Run Harness Stub Implementation Plan has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This is roadmap progress toward a future first non-runtime dry-run harness stub source surface, but it is still not source code and not a harness implementation. MLRT-18 does not create Python source files, does not create a source surface, does not create harness code, does not create runner code, does not create harness stub files, does not create implementation modules, does not create executable validators, does not create schema code, does not create contract schema files, does not implement a static interface, does not implement a boundary checker, does not execute a dry run, does not execute a candidate, does not create candidate outputs, does not execute cases, does not score cases, does not compare routes, does not generate reports, does not validate candidate reliability, and does not unlock ML implementation.

## Roadmap position

MLRT-18 is not a loop. It narrows the next blocker after MLRT-17:

```text
MLRT-13 - first non-runtime dry-run execution planning
MLRT-14 - future harness skeleton planning
MLRT-15 - future harness contract planning
MLRT-16 - future harness implementation boundary planning
MLRT-17 - future harness stub implementation planning
MLRT-18 - future harness stub source-surface planning
```

The purpose of this step is to define what a future source surface may be allowed to expose before any static interface contract milestone is considered.

## Hard boundary

MLRT-18 is documentation-only. It does not create a source file. It does not create a source surface. It does not create a harness. It does not create a runner. It does not create harness stub files. It does not create implementation modules. It does not create executable validators. It does not create schema code. It does not create a harness contract file. It does not implement a static interface. It does not implement a harness boundary checker. It does not execute a dry run. It does not execute a candidate. It does not create dry-run execution records. It does not create candidate outputs. It does not run cases. It does not score cases. It does not compare routes. It does not generate reports. It does not validate candidate reliability. It does not unlock ML implementation.

MLRT-18 must not:

- create Python source files
- create source-surface files
- create source-surface directories
- create harness code
- create runner code
- create harness stub files
- create implementation modules
- create executable validators
- create schema code
- create contract schema files
- create static interface implementation files
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

## Planned source-surface identity

A future source surface, if later authorized by a separate governed milestone, must be named and shaped as a standard-library-only, import-isolated, deterministic, in-memory-only, non-runtime adapter boundary. It must not be a router, not a runner, not a prompt loader, not a provider adapter, not an embedding adapter, not a persistence writer, not an approval writer, not an activation mechanism, not a Pilot mechanism, and not a Copilot mechanism.

A future source surface plan may describe only:

- the future source file identity
- the future module import policy
- the future public function names
- the future typed input boundary
- the future typed output envelope boundary
- the future abort label vocabulary
- the future no-live-read doctrine
- the future no-authority doctrine
- the future no-execution doctrine
- the future no-reliability-claim doctrine

MLRT-18 does not create these future files, modules, functions, types, or envelopes as code. It only defines that any future static interface must be planned before any code is written.

## Planned source-surface allowed shape

A future source-surface milestone may plan only a minimal static interface surface that accepts caller-supplied, in-memory, already-sanitized static data. The surface must return deterministic dictionaries or frozen data envelopes that state planning status and abort status only. It must not run cases, must not run a candidate, must not score outputs, must not compare routes, and must not write reports.

The future source surface may include only planned names for:

- static input bundle descriptor
- static candidate descriptor
- static freeze-reference descriptor
- static contract-reference descriptor
- abort label enumeration
- non-authoritative planning envelope
- human-review-required flag
- no-dry-run-executed flag
- no-candidate-output-created flag
- no-reliability-claim flag

These are future planned names only. MLRT-18 does not implement them.

## Planned import policy

A future source surface must be standard-library-only and import-isolated. It may not import project runtime router modules, prompt-library modules, freeze-memory readers, provider libraries, embedding libraries, vector-store clients, network clients, subprocess helpers, persistence writers, GUI modules, approval writers, activation modules, Pilot modules, or Copilot modules.

The future source surface must operate only on caller-supplied in-memory data. It must not read live project files. It must not inspect live prompt-library files. It must not inspect live freeze memory. It must not inspect live router canon. It must not inspect the gold registry. It must not inspect candidate package files. It must not reach outside the provided input bundle.

## Planned output envelope doctrine

A future source surface may only plan non-authoritative output envelopes. The planned envelope must state that it is advisory, static, and in-memory only. It must state that no dry run has executed, no candidate has executed, no candidate output exists, no case has run, no score exists, no route comparison exists, no reliability claim is made, and human review remains required.

The planned output envelope must not contain route decisions, prompt loading instructions, execution commands, install commands, freeze writes, approval writes, readiness approvals, reliability approvals, activation signals, field-test signals, runtime Pilot instructions, or Copilot instructions.

## Planned abort doctrine

A future source surface must abort before returning any non-abort planning envelope if it detects:

- missing MLRT-17 freeze reference
- missing MLRT-16 freeze reference
- missing MLRT-15 freeze reference
- missing MLRT-14 freeze reference
- missing MLRT-13 freeze reference
- missing static candidate descriptor
- missing static input bundle
- missing static contract reference
- hash mismatch
- unexpected live project read
- unexpected runtime import
- unexpected provider, embedding, network, subprocess, batch, persistence, activation, Pilot, or Copilot field
- any route-authority field
- any prompt-loading field
- any approval-write field
- any reliability-claim field
- any execution-command field
- any report-persistence field

Abort labels remain non-authoritative and must not become route decisions, readiness approvals, reliability approvals, freeze writes, activation signals, Pilot instructions, or Copilot instructions.

## No implementation doctrine

MLRT-18 must not be interpreted as authorization to implement the source surface. It only defines the future harness stub source-surface plan. A later governed milestone must explicitly define the static interface contract before any code is written. A later code milestone, if ever approved, must remain non-runtime and non-authoritative.

## No reliability claim doctrine

MLRT-18 is not candidate reliability evidence. It does not show that a source surface exists, that a stub exists, that a harness exists, that a candidate can run, that output can be captured, that contracts pass, that cases can be scored, or that routing is safe. Candidate reliability remains unvalidated and ML implementation remains locked.

## Positive label doctrine

The only positive MLRT-18 label is:

```text
MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_SOURCE_SURFACE_PLAN_READY_FOR_STATIC_INTERFACE_CONTRACT_PLANNING_ONLY
```

This label means only that future harness stub source-surface planning is documented and ready to proceed to a future static-interface-contract planning milestone after local validation and freeze. It does not mean source files exist. It does not mean a source surface exists. It does not mean a static interface exists. It does not mean a harness exists. It does not mean runner code exists. It does not mean harness stub files exist. It does not mean implementation modules exist. It does not mean a boundary checker exists. It does not mean a contract schema exists. It does not mean a dry run has executed. It does not mean candidate outputs exist. It does not mean cases were executed. It does not mean scores exist. It does not mean reports exist. It does not mean candidate reliability is validated. It does not mean ML implementation is unlocked.

## Forbidden authority fields

Future source-surface planning must continue to reject these authority fields:

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

After MLRT-18 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
MLRT-19 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Contract Plan
```

That next step must remain a separate governed non-runtime documentation-only milestone. It must not create source code unless and until a later explicitly governed code milestone is approved.
