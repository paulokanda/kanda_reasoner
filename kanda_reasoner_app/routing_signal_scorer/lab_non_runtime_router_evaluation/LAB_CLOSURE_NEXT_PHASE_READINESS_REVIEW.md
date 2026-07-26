# LAB-13 - Lab Closure / Next-Phase Readiness Review v1

Feature ID: `routing_signal_scorer_v3_ml_lab_closure_next_phase_readiness_review_v1`

Feature title: `Routing Signal Scorer v3 ML LAB Closure / Next-Phase Readiness Review v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation`

Schema version: `lab-13-closure-next-phase-readiness-review`

Status: governed documentation-only LAB closure and next-phase readiness review.

## Purpose

LAB-13 closes the first governed ML LAB construction sequence and defines the readiness review required before moving into controlled non-runtime ML/router candidate reliability testing.

LAB-13 is a readiness review milestone, not a candidate evaluation milestone. It does not run cases, score cases, evaluate a candidate, compare routes, generate reports, persist reports, load prompts, call providers, call embeddings, activate Pilot, activate Copilot, enable field testing, or grant route authority.

The review asks whether the LAB infrastructure is mature enough to begin a separate governed next phase:

```text
controlled non-runtime ML/router candidate reliability testing planning
```

It does not unlock direct ML implementation.

## Closure review scope

LAB-13 reviews whether the LAB phase now has these governed building blocks:

- RG-LAB-000 LAB phase entry canonization
- LAB-0 Phase Boundary + Lab Charter / Entry Gate
- LAB-0A Success Criteria Matrix
- LAB-0B Risk-Control Matrix
- LAB-0C SLO / Critical Error Budget Declaration
- LAB-1 Box Boundary + Shielding Manifest
- LAB-2 Failure Taxonomy + Critical Violation Model
- LAB-3 Scoring Model + Hard Gates
- LAB-4 Test Case Schema + Candidate Output Contract
- LAB-5 Frozen Canon Fixture Format + Hash Manifest
- LAB-6 Deterministic Runner Skeleton
- LAB-7 Lab Self-Validation Gate
- LAB-8 Alpha Corpus Seed
- LAB-9 Offline Observability + Experiment Report
- LAB-10 Candidate Evaluation Harness Interface
- LAB-11 Corpus V1 Expansion
- LAB-12 Error Canonization Intake Spec

LAB-13 does not change those artifacts. It creates no new LAB Python module.

## Readiness questions

A future closure/readiness review must be able to answer all of these questions before any controlled candidate reliability testing begins:

1. Is the LAB box isolated from production/runtime code?
2. Do production/runtime modules avoid importing the LAB box?
3. Are the only allowed LAB Python source files still exactly:
   - `candidate_evaluation_harness_interface.py`
   - `deterministic_runner_skeleton.py`
   - `lab_self_validation_gate.py`
4. Are static corpus and fixture-like assets versioned and hash-checked where applicable?
5. Does the LAB self-validation gate require all mandatory controls before later candidate evaluation?
6. Are hard gates evaluated before soft scores?
7. Is the critical boundary error budget still `0`?
8. Do any candidate outputs have a path to runtime route authority?
9. Can a candidate output load prompts, execute routes, approve readiness, write freeze memory, write canon, write prompt library files, write gold registry records, activate Pilot, activate Copilot, enable field testing, call providers, call embeddings, start batch mode, persist ML decisions, or act as a Copilot instruction?
10. Are corpus growth and error canonization still governed by human review, separate patch, validation, and freeze?
11. Are reports reproducible from static, versioned, non-live inputs only?
12. Does the next phase remain non-runtime and governed?

If any answer indicates a critical boundary leak, the result is not ready.

## Readiness labels

LAB-13 defines readiness labels only. These labels do not grant route authority or runtime permissions.

Allowed labels:

- `NOT_READY_FOR_CANDIDATE_RELIABILITY_TESTING`
- `READY_FOR_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLANNING_ONLY`
- `BLOCKED_BY_LAB_INVALID`
- `BLOCKED_BY_CRITICAL_BOUNDARY_RISK`
- `BLOCKED_BY_MISSING_FREEZE_OR_STARTUP_REFRESH`
- `NEEDS_HUMAN_REVIEW_BEFORE_NEXT_PHASE`

The only positive label allowed by LAB-13 is:

```text
READY_FOR_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLANNING_ONLY
```

This label means the next separate governed scope may plan controlled non-runtime candidate reliability tests. It does not mean the ML/router candidate is reliable. It does not mean ML implementation is allowed to continue directly.

## Mandatory closure preconditions

Before claiming the LAB is ready for controlled candidate reliability test planning, future review evidence must include:

- local validation evidence for LAB-13
- prior LAB validation chain evidence or startup freeze context showing `FREEZE_MEMORY_STATUS: OK`
- all current LAB tests passing
- no unauthorized LAB Python files
- no route authority
- no prompt loading
- no provider calls
- no embedding/vector calls
- no report persistence
- no persistent ML decision storage
- no activation key
- no field-test mode
- no runtime Pilot behavior
- no Copilot behavior
- no automatic corpus, fixture, canon, prompt-library, freeze-memory, gold-registry, or startup-pack mutation
- no candidate output path to runtime
- no critical boundary violations

## Explicit non-actions

LAB-13 does not:

- continue ML implementation
- create an ML/router candidate
- run a candidate
- evaluate candidate output
- execute test cases
- score test cases
- compare routes
- select routes
- execute routes
- grant route authority
- load prompts
- read live prompt-library files
- read live freeze memory
- read live router canon
- import runtime router modules
- create actual fixture snapshots
- mutate Corpus V1
- mutate alpha corpus
- mutate fixture manifests
- mutate router canon
- mutate prompt library files
- mutate freeze memory
- mutate gold registry
- create an error library
- create automatic error canonization
- generate reports
- persist reports
- call providers
- call embedding models
- use network calls
- use subprocess calls
- start batch mode
- persist ML decisions
- create an activation key
- create field-test mode
- create runtime Pilot behavior
- create Copilot behavior

## Critical boundary closure rule

Critical boundary error budget remains `0`.

If candidate output can reach runtime, the LAB closure fails.

If candidate output can write freeze memory, canon, prompt library, gold registry, startup pack, approval state, activation state, field-test state, runtime decision logs, or persistent ML decision storage, the LAB closure fails.

If candidate output can become a route decision, prompt-loading command, install command, readiness approval, human approval, activation signal, field-test signal, runtime Pilot command, or Copilot instruction, the LAB closure fails.

## Relationship to LAB-12

LAB-12 defined the future non-authoritative human-reviewed error intake proposal doctrine. LAB-13 verifies that this intake path remains governed and cannot mutate corpus, fixtures, canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, runtime logs, or persistent ML decisions by itself.

## Next safe milestone after LAB-13

After LAB-13 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-0 - Controlled Non-Runtime ML/Router Candidate Reliability Test Plan
```

MLRT-0 must be a separate governed scope. It may plan how to test a future ML/router candidate against the LAB, but it still must not activate runtime route authority, prompt loading, provider calls, embeddings, persistent ML decisions, batch mode, activation, field testing, runtime Pilot, or Copilot behavior.

## Reliability and ML implementation lock

LAB-13 is not ML/router reliability evidence.

The ML implementation continuation lock remains:

```text
LAB closure/readiness review frozen
-> controlled non-runtime candidate reliability test plan
-> candidate reliability testing under LAB controls
-> zero critical boundary violations
-> human review
-> freeze of reliability evidence
-> only then consider continuing ML logic implementation
```

Until that happens, ML implementation remains blocked.
