# MLRT-0 - Controlled Non-Runtime ML/Router Candidate Reliability Test Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_controlled_non_runtime_candidate_reliability_test_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-0 Controlled Non-Runtime ML/Router Candidate Reliability Test Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-0-controlled-non-runtime-candidate-reliability-test-plan`

Status: governed documentation-only MLRT planning milestone.

## Purpose

MLRT-0 begins the next phase after LAB-13 closure. Its purpose is to define a controlled plan for future non-runtime ML/router candidate reliability testing.

MLRT-0 does not test the ML/router algorithm yet. It does not execute a candidate, score outputs, execute cases, compare routes, generate reliability evidence, or unlock ML implementation.

MLRT-0 only defines the planning boundary for a later candidate reliability test phase. It does not execute cases. It does not score cases.

## Precondition inherited from LAB-13

MLRT-0 may begin only after LAB-13 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

LAB-13 established that the LAB closure/readiness review is not candidate reliability evidence and that the next safe milestone is controlled non-runtime ML/router candidate reliability test planning only.

## Scope

MLRT-0 defines these planning topics:

1. What a future ML/router candidate reliability test may evaluate.
2. Which LAB controls must remain mandatory before candidate testing.
3. Which candidate artifacts must be provided before any reliability run.
4. Which outputs are allowed and which outputs are forbidden.
5. Which evidence is required before any future reliability claim.
6. Which critical boundary failures immediately invalidate a run.
7. Which next milestones may follow under separate governed patches.

MLRT-0 does not create any candidate, runner, scorer, report writer, provider adapter, embedding adapter, prompt loader, activation key, Pilot behavior, or Copilot behavior.

## Candidate reliability test mission

The later candidate reliability test phase may only test whether a future non-authoritative candidate can reproduce and explain frozen routing-governance expectations inside the LAB boundary.

A future candidate may be tested on whether it can:

- classify governed versus simple tasks
- identify required prompt groups
- detect missing context
- detect stale or conflicting context
- reject bypass attempts
- preserve box boundaries
- preserve freeze-memory and prompt-library authority boundaries
- obey match-before-disagree doctrine
- explain disagreement without overriding canon
- produce a non-authoritative evaluation record
- preserve zero critical boundary error doctrine

A future candidate must not be treated as a route authority.

## Mandatory controls before future candidate reliability testing

Before any later candidate reliability test can begin, a governed milestone must verify all of the following:

- LAB self-validation gate passes
- LAB fixture and corpus integrity checks pass
- the allowed LAB Python source file set remains exactly:
  - `candidate_evaluation_harness_interface.py`
  - `deterministic_runner_skeleton.py`
  - `lab_self_validation_gate.py`
- no production/runtime module imports the LAB box
- no MLRT module imports runtime router modules
- no candidate output can reach runtime
- no candidate output can write freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime decision logs, or persistent ML decision storage
- no candidate output can become a route decision, prompt loading command, install command, readiness approval, human approval, activation signal, field-test signal, runtime Pilot command, or Copilot instruction
- all candidate outputs are wrapped as non-authoritative evaluation records
- all critical boundary violations produce immediate invalidation
- aggregate soft scores cannot compensate for hard or critical failures
- human review remains required before any reliability conclusion is frozen

## Required future candidate package before testing

A future candidate reliability test must not begin until a separate governed patch defines a candidate package contract.

That future package must be non-runtime and must include at least:

- candidate identifier
- candidate version
- candidate source type
- candidate interface version
- candidate output contract version
- declared input limits
- declared forbidden capabilities
- declared non-authoritative status
- declared no-route-authority status
- declared no-prompt-loading status
- declared no-persistence status
- declared no-provider-call status
- declared no-embedding-call status
- declared no-runtime-integration status
- declared no-activation status
- declared no-Copilot-behavior status

MLRT-0 does not create this package. It only records that the package must exist before candidate reliability testing starts.

## Required future evidence before reliability claims

A future reliability claim must require a separate governed evidence packet including:

- exact candidate version
- exact LAB version/freeze context
- exact corpus version
- exact fixture/hash manifest references where applicable
- full validation output
- per-case outcome records
- hard-gate results
- critical boundary failure count
- soft metrics only after hard gates pass
- human review record
- freeze evidence
- reproducibility notes

No reliability claim may be made from aggregate accuracy alone.

No reliability claim may be made if any critical boundary violation occurs.

No reliability claim may be made if LAB self-validation fails.

No reliability claim may be made if the candidate output can reach runtime.

## Allowed planning labels

MLRT-0 defines planning labels only. They do not grant route authority or runtime permissions.

Allowed labels:

- `MLRT_PLAN_NOT_READY`
- `MLRT_PLAN_READY_FOR_INPUT_OUTPUT_CONTRACT_PLANNING_ONLY`
- `MLRT_PLAN_BLOCKED_BY_LAB_INVALID`
- `MLRT_PLAN_BLOCKED_BY_CRITICAL_BOUNDARY_RISK`
- `MLRT_PLAN_BLOCKED_BY_MISSING_FREEZE_OR_STARTUP_REFRESH`
- `MLRT_PLAN_NEEDS_HUMAN_REVIEW`

The only positive label allowed by MLRT-0 is:

```text
MLRT_PLAN_READY_FOR_INPUT_OUTPUT_CONTRACT_PLANNING_ONLY
```

This label means the next governed milestone may design the candidate reliability input/output contract. It does not mean a candidate is reliable. It does not mean ML implementation may continue. MLRT-0 does not unlock ML implementation.

## Forbidden actions

MLRT-0 must not:

- implement ML logic
- implement a candidate
- execute a candidate
- execute cases
- score cases
- compare live routes
- select routes
- execute routes
- grant route authority
- load prompts
- read live prompt-library files
- read live freeze memory
- read live router canon
- import runtime router modules
- create actual candidate outputs
- generate reports
- persist reports
- call providers
- call embedding models
- use vector stores
- use network calls
- use subprocess calls
- start batch mode
- persist ML decisions or create persistent ML decisions
- create an activation key
- enable field-test mode
- create runtime Pilot behavior
- create Copilot behavior
- mutate corpus
- mutate fixtures
- mutate router canon
- mutate prompt library files
- mutate freeze memory
- mutate gold registry
- mutate startup pack
- mutate approval state
- mutate activation state
- mutate field-test state
- mutate runtime decision logs
- mutate persistent ML decision storage

## Critical boundary rule

The critical boundary error budget remains `0`.

If a future plan or candidate gives candidate output any path to runtime authority, MLRT is invalid.

If a future plan or candidate gives candidate output any write path to freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime decision logs, or persistent ML decision storage, MLRT is invalid.

If a future plan or candidate allows route authority, prompt loading, provider calls, embeddings, persistence, batch mode, activation, field testing, runtime Pilot, or Copilot behavior, MLRT is invalid unless a later explicit governed scope changes that boundary after reliability has been proven and frozen.

## Relationship to LAB

LAB built the non-runtime evaluation infrastructure.

MLRT defines the governed plan for testing a future candidate against that infrastructure.

The LAB remains non-authoritative. MLRT remains non-authoritative. Candidate output remains non-authoritative.

## Next safe milestone after MLRT-0

After MLRT-0 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-1 - Candidate Reliability Input/Output Contract Plan
```

MLRT-1 must still be governed and non-runtime. It may define the future input/output contract for candidate reliability testing, but it must not execute candidates, score cases, grant route authority, load prompts, call providers, use embeddings, persist ML decisions or create persistent ML decisions, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

## ML implementation continuation lock

ML implementation remains blocked.

The continuation lock is:

```text
LAB closure/readiness review frozen
-> MLRT-0 controlled non-runtime candidate reliability test plan
-> MLRT-1 candidate reliability input/output contract plan
-> future governed candidate reliability execution under LAB controls
-> zero critical boundary violations
-> human review
-> freeze of reliability evidence
-> only then consider continuing ML logic implementation
```

Until that full chain is completed, real ML implementation remains blocked.
