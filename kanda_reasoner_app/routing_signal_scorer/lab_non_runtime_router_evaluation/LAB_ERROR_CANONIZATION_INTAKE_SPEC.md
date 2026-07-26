# LAB-12 - Error Canonization Intake Spec v1

Feature ID: `routing_signal_scorer_v3_ml_lab_error_canonization_intake_spec_v1`

Feature title: `Routing Signal Scorer v3 ML LAB Error Canonization Intake Spec v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation`

Schema version: `lab-12-error-canonization-intake-spec`

Status: governed documentation-only error canonization intake specification.

## Purpose

LAB-12 defines how future observed ML LAB failures may become reviewed regression candidates.
It is not an error library implementation. It is not automatic canonization. It does not modify any corpus, fixture, prompt library, router canon, freeze memory, gold registry, startup pack, approval state, activation state, runtime decision log, or persistent ML decision store.

The purpose is to protect the future learning loop:

```text
future lab failure observed
-> failure classified using LAB-2 taxonomy
-> hard/critical/LAB_INVALID handling checked using LAB-3 scoring doctrine
-> candidate intake draft prepared as non-authoritative proposal only
-> human review required
-> separate governed patch required before any corpus/regression/canon update
-> freeze required before the new regression becomes protected behavior
```

## LAB-12 scope

LAB-12 may define:

- error intake purpose
- error intake eligibility
- non-authoritative intake record fields
- human review requirements
- blocked automatic mutation rules
- regression candidate lifecycle states
- relationship to LAB-11 static corpus expansion
- relationship to LAB-13 closure/readiness review
- critical-boundary stop conditions

LAB-12 does not create Python lab modules, schema code, validators, fixture files, corpus files, runner execution, scoring execution, report generation, candidate evaluation execution, provider adapters, prompt loaders, persistent ML decision stores, activation keys, field-test flags, runtime Pilot behavior, or Copilot behavior.

## Future intake record doctrine

A future error intake record may exist only as a non-authoritative proposal. It must not mutate anything by itself.

Required future fields:

- `intake_id`
- `intake_version`
- `schema_version`
- `source_lab_run_id`
- `source_report_reference`
- `source_case_id`
- `source_corpus_version`
- `source_candidate_id`
- `source_candidate_version`
- `observed_outcome`
- `failure_codes`
- `critical_boundary_flag`
- `lab_invalid_flag`
- `evidence_excerpt`
- `reproduction_steps_reference`
- `expected_behavior_reference`
- `actual_behavior_summary`
- `proposed_regression_category`
- `proposed_future_case_title`
- `proposed_fixture_requirement`
- `proposed_canon_rule_reference`
- `human_review_required`
- `human_review_status`
- `mutation_allowed_by_this_record`
- `requires_separate_governed_patch`
- `requires_freeze_after_patch`

The required value for `mutation_allowed_by_this_record` is always `false`.

## Intake eligibility

Future intake may be proposed for:

- repeated false fast-path decisions
- missed Routed Work Path decisions
- missing prompt/group recall
- forbidden prompt loading attempts
- route authority attempts
- stale-context acceptance
- missing-context failures
- box boundary leakage
- prompt-injection bypass
- insecure output to downstream systems
- match-before-disagree violations
- false reliability claims
- candidate output that attempts to become authoritative
- fixture or manifest integrity failures
- human review bypass attempts

Future intake must not be used to silently update canon, corpus, or gold expectations.

## Required future lifecycle states

A future error intake candidate should use lifecycle states like:

- `PROPOSED`
- `NEEDS_HUMAN_REVIEW`
- `REJECTED`
- `ACCEPTED_FOR_GOVERNED_PATCH`
- `PATCH_CREATED`
- `VALIDATED`
- `FROZEN_AS_REGRESSION`

Only `FROZEN_AS_REGRESSION` may become protected behavior, and only after a separate governed patch, validation, and freeze.

## Explicit non-actions

LAB-12 does not create an error library.
LAB-12 does not write regression cases.
LAB-12 does not mutate LAB-11 corpus files.
LAB-12 does not execute test cases.
LAB-12 does not evaluate candidates.
LAB-12 does not compare routes.
LAB-12 does not grant route authority.
LAB-12 does not load prompts.

LAB-12 does not:

- create an error library
- create automatic error canonization
- write regression cases
- mutate LAB-11 corpus files
- mutate alpha corpus files
- mutate fixture manifests
- mutate router canon
- mutate prompt library files
- mutate freeze memory
- mutate gold registry
- generate reports
- persist reports
- execute test cases
- score test cases
- evaluate candidates
- compare routes
- grant route authority
- load prompts
- read live prompt-library content
- read live freeze memory
- read live router canon
- import runtime router modules
- call providers
- call embedding models
- use network
- use subprocess
- use async/background/batch execution
- persist ML decisions
- activate Pilot
- activate Copilot
- enable field testing
- implement runtime Pilot behavior
- implement Copilot behavior

## Critical boundary rules

Critical boundary error budget remains `0`.

Any future attempt to use an error intake record as an automatic update, route decision, prompt-loading instruction, freeze authorization, human approval, readiness approval, activation signal, field-test signal, runtime Pilot command, or Copilot instruction is a critical boundary violation.

Any future automatic mutation of corpus, canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, runtime decision logs, or persistent ML decision storage from error intake is a critical boundary violation.

## Relationship to LAB-11

LAB-11 expanded static corpus coverage to 60 combined static cases. LAB-12 does not modify that corpus. LAB-12 only defines how future failures may be proposed for later governed regression updates.

## Relationship to LAB-13

LAB-13 - Lab Closure / Next-Phase Readiness Review is the next safe milestone after LAB-12 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed.

LAB-13 should review whether the LAB has enough boundary, corpus, self-validation, harness, observability, and intake discipline to begin controlled ML/router candidate reliability testing. LAB-13 must still not continue ML implementation directly.

## Reliability and ML implementation lock

LAB-12 provides no ML/router reliability evidence.

The ML implementation continuation lock remains:

```text
LAB/test fulfills its mission
-> LAB self-validation passes
-> ML router prompt logic reliability is tested
-> zero critical boundary violations are demonstrated
-> human review and freeze confirm reliability evidence
-> only then continue ML logic implementation
```
