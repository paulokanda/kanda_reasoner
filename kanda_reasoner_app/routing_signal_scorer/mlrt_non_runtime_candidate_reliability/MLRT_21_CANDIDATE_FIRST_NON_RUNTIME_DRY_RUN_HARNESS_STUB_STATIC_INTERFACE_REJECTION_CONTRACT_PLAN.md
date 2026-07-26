# MLRT-21 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Rejection Contract Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_rejection_contract_plan_v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Status: governed documentation-only first non-runtime dry-run harness stub static-interface rejection-contract planning milestone.

## Purpose

MLRT-21 defines the future rejection-contract planning doctrine for a non-runtime harness stub static interface after MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan has been locally validated, frozen, and exposed with `FREEZE_MEMORY_STATUS: OK`.

This is still not testing. It is also not source code, not executable rejection logic, not an executable rejection gate, not an executable abort gate, not a static interface, not a source surface, not a harness implementation, and not a dry-run runner. MLRT-21 exists to ensure that any future static-interface envelope that survives an abort boundary can still be rejected safely before any dry-run action, candidate execution, case execution, scoring, report generation, reliability claim, or runtime-facing behavior exists.

MLRT-21 does not create Python source files, does not create rejection-contract code, does not create abort-contract code, does not create executable rejection gates, does not create executable abort gates, does not create a static interface, does not create source-surface files, does not create static-interface files, does not create harness code, does not create runner code, does not create harness stub files, does not create implementation modules, does not create boundary-checker code, does not create executable validators, does not create schema code, does not create contract schema files, does not execute a dry run, does not execute a candidate, does not create candidate outputs, does not execute cases, does not score cases, does not compare routes, does not generate reports, does not validate candidate reliability, and does not unlock ML implementation.

## When tests start

Real candidate/dry-run tests must not start at MLRT-21.

Reference estimate, not a promise: if no new safety gap appears, testing likely starts only after roughly six more governed milestones: rejection-contract planning, test-start readiness-gate planning, implementation-boundary confirmation for any source surface, creation of a non-runtime static harness stub if later allowed, fixture/input-output binding, and a final first-dry-run execution gate. In practical roadmap terms, that means tests are not expected before approximately MLRT-26 or MLRT-27.

This estimate is deliberately conservative. Any new boundary gap, stale freeze reference, missing fixture contract, missing abort/rejection gate, unsafe source surface, or live-runtime coupling must add more gates before testing.

Until those later milestones exist and are frozen with `FREEZE_MEMORY_STATUS: OK`, every MLRT step remains planning only. Candidate reliability remains unvalidated.

## Roadmap position

MLRT-21 is not a loop. It narrows the next blocker after MLRT-20:

```text
MLRT-13 - first non-runtime dry-run execution planning
MLRT-14 - future harness skeleton planning
MLRT-15 - future harness contract planning
MLRT-16 - future harness implementation boundary planning
MLRT-17 - future harness stub implementation planning
MLRT-18 - future harness stub source-surface planning
MLRT-19 - future harness stub static-interface contract planning
MLRT-20 - future harness stub static-interface abort-contract planning
MLRT-21 - future harness stub static-interface rejection-contract planning
```

The purpose of this step is to define the future rejection contract before any test-start readiness gate, executable interface, harness stub, or non-runtime test execution can be considered.

## Hard boundary

MLRT-21 is documentation-only. It does not create a source file. It does not create Python source files. It does not create rejection-contract code. It does not create abort-contract code. It does not create executable rejection gates. It does not create executable abort gates. It does not create a static interface. It does not create static-interface files. It does not create a source surface. It does not create source-surface files. It does not create a harness. It does not create a runner. It does not create harness stub files. It does not create implementation modules. It does not create executable validators. It does not create schema code. It does not create contract schema files. It does not implement a boundary checker. It does not execute a dry run. It does not execute a candidate. It does not create dry-run execution records. It does not create candidate outputs. It does not run cases. It does not score cases. It does not compare routes. It does not generate reports. It does not validate candidate reliability. It does not unlock ML implementation.

MLRT-21 must not:

- create Python source files
- create rejection-contract code
- create abort-contract code
- create executable rejection gates
- create executable abort gates
- create source-surface files
- create source-surface directories
- create static interface files
- create static interface directories
- create harness code
- create runner code
- create harness stub files
- create implementation modules
- create boundary-checker code
- create executable validators
- create schema code
- create contract schema files
- create static interface implementation files
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

## Planned rejection-contract identity

A future rejection contract, if later authorized by a separate governed milestone, must be standard-library-only, import-isolated, deterministic, in-memory-only, non-runtime, and non-authoritative. It must classify a future static-interface envelope as rejected before any dry-run action, candidate execution, case execution, scoring, report generation, persistence, approval, activation, or reliability claim.

The future rejection contract must be a safety classifier, not a test engine. It must not execute candidates, load prompts, compare routes, write approvals, write freeze memory, persist reports, call providers, use embeddings, use vector stores, activate field testing, activate Pilot, or activate Copilot.

## Planned rejection categories

A future rejection contract must define rejection categories for at least:

- freeze-reference mismatch
- stale freeze reference
- missing MLRT feature lineage
- missing human-review marker
- missing no-authority declaration
- missing no-live-read declaration
- missing no-execution declaration
- missing no-persistence declaration
- missing no-reliability-claim declaration
- unexpected route-authority field
- unexpected prompt-loading field
- unexpected provider-call field
- unexpected embedding-call field
- unexpected vector-store field
- unexpected network-call field
- unexpected subprocess-call field
- unexpected persistence field
- unexpected approval-write field
- unexpected freeze-write field
- unexpected mutation field
- unexpected activation field
- unexpected field-test field
- unexpected Pilot field
- unexpected Copilot field
- unexpected dry-run execution field
- unexpected candidate execution field
- unexpected case execution field
- unexpected scoring field
- unexpected report generation field
- unexpected report persistence field
- unexpected reliability-claim field
- unknown authority-bearing field

MLRT-21 does not implement these rejection categories as code. It documents that any later implementation must reject before action.

## Planned rejection output doctrine

A future rejection contract may only return a non-authoritative rejection envelope. That envelope must state that processing stopped before any dry run, candidate execution, case execution, scoring, route comparison, report generation, report persistence, approval, activation, or reliability claim.

The planned rejection output must not contain route decisions, prompt loading instructions, execution commands, install commands, freeze writes, approval writes, readiness approvals, reliability approvals, activation signals, field-test signals, runtime Pilot instructions, or Copilot instructions.

## Planned abort-contract dependency

A future rejection contract depends on the abort-contract doctrine defined by MLRT-20. The rejection contract must never weaken the abort contract. Abort happens first for forbidden or malformed authority-bearing input. Rejection may only classify a future static envelope that is already known to be non-runtime and non-authoritative.

MLRT-21 does not implement abort-contract code and does not implement rejection-contract code.

## Planned test-start readiness dependency

A future test-start readiness gate is a separate later planning milestone. MLRT-21 only defines rejection-contract planning. A test-start readiness gate may later decide whether the non-runtime surfaces are mature enough to allow a first dry-run attempt, but it must not itself create route authority, prompt loading, provider calls, persistence, or reliability claims.

## Planned import policy

A future rejection contract, if later implemented, must use only Python standard library imports approved by a separate implementation-boundary milestone. It must not import runtime router modules, prompt loaders, provider clients, embedding clients, vector stores, GUI modules, freeze writers, startup-pack writers, or project mutation tools.

MLRT-21 does not add or authorize those imports.

## No implementation doctrine

MLRT-21 is the plan, not the implementation. It does not create source files, code modules, validators, schema files, test fixtures, execution records, or reports.

## No testing doctrine

MLRT-21 does not start tests. It does not run a candidate, run a case, run a dry run, score a result, compare a route, or generate a reliability report.

## No reliability claim doctrine

MLRT-21 does not validate ML/router reliability. Any future output from this planning milestone must remain a planning artifact only.

## Positive label doctrine

The only positive MLRT-21 label is:

```text
MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_REJECTION_CONTRACT_PLAN_READY_FOR_TEST_START_READINESS_GATE_PLANNING_ONLY
```

This label means MLRT-21 is ready for test-start readiness-gate planning only. It does not mean source files exist. It does not mean a rejection contract exists. It does not mean an abort contract exists. It does not mean executable rejection gates exist. It does not mean executable abort gates exist. It does not mean a source surface exists. It does not mean a static interface exists. It does not mean a harness exists. It does not mean a dry run has executed. It does not mean candidate reliability is validated. It does not mean ML implementation is unlocked.

## Forbidden authority fields

A future rejection contract must reject or escalate any field that would imply:

- route authority
- prompt loading
- prompt mutation
- router-canon mutation
- prompt-library mutation
- gold-registry mutation
- freeze-memory mutation
- approval writes
- readiness approval
- reliability approval
- candidate execution
- dry-run execution
- case execution
- scoring execution
- report generation
- report persistence
- provider calls
- embedding calls
- vector-store use
- network calls
- subprocess calls
- batch mode
- persistence
- activation
- field testing
- runtime Pilot behavior
- Copilot behavior

MLRT-21 does not implement this rejection logic.

## Next safe milestone

After MLRT-21 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-22 - Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Test-Start Readiness Gate Plan
```

Plain milestone name: MLRT-22 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Test-Start Readiness Gate Plan.

MLRT-22 must remain governed and non-runtime. It may only plan the test-start readiness gate. It must not yet create code, execute a dry run, create candidate outputs, score cases, validate reliability, authorize routing, activate Pilot, activate Copilot, or unlock runtime ML implementation.
