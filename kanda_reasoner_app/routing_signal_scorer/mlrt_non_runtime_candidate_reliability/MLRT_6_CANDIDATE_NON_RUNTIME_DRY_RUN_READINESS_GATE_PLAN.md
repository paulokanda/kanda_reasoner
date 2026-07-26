# MLRT-6 - Candidate Non-Runtime Dry-Run Readiness Gate Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_readiness_gate_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-6 Candidate Non-Runtime Dry-Run Readiness Gate Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-6-candidate-non-runtime-dry-run-readiness-gate-plan`

Status: governed documentation-only MLRT non-runtime dry-run readiness gate planning milestone.

## Purpose

MLRT-6 defines the planned readiness gate for a future candidate non-runtime dry-run protocol.

MLRT-6 does not perform a dry run. It does not create dry-run readiness records. It does not create dry-run protocol records. It does not read static review outcome gates as live evidence. It does not approve a candidate package for dry-run execution. It does not create, accept, install, import, execute, validate, score, compare, or evaluate a candidate package. It does not create candidate outputs, reliability reports, persistent reports, persistent ML decisions, route decisions, human approvals, readiness approvals, activation signals, field-test signals, runtime Pilot commands, or Copilot instructions.

MLRT-6 only defines doctrine for how a future readiness gate could decide whether a later non-runtime dry-run protocol planning milestone may be designed.

There is no candidate reliability validation in MLRT-6 and there is no ML implementation unlock.

## Precondition inherited from MLRT-5

MLRT-6 may begin only after MLRT-5 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-5 established that the next safe step after candidate static review outcome-gate planning is non-runtime dry-run readiness gate planning only.

## Contract scope

MLRT-6 defines planned readiness-gate groups for a future non-runtime dry-run protocol. These groups are doctrine only:

1. Dry-run readiness gate identity and traceability.
2. Required static review outcome-gate reference doctrine.
3. Non-runtime dry-run scope doctrine.
4. Candidate package eligibility doctrine.
5. Dry-run protocol precondition doctrine.
6. Critical boundary blocker doctrine.
7. Human-escalation doctrine.
8. Dry-run protocol planning label doctrine.
9. Dry-run readiness non-authority doctrine.
10. Dry-run readiness forbidden field doctrine.
11. Dry-run readiness next-milestone doctrine.

MLRT-6 does not create executable validators. MLRT-6 does not read, scan, import, execute, or review candidate files. MLRT-6 does not write readiness records. MLRT-6 does not execute a dry run.

## Dry-run readiness gate identity and traceability doctrine

A future dry-run readiness gate record must declare at least:

- `dry_run_readiness_gate_id`
- `dry_run_readiness_gate_version`
- `schema_version`
- `mlrt_phase_reference`
- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `candidate_package_intake_record_id`
- `static_review_outcome_gate_id`
- `static_review_outcome_gate_hash`
- `static_review_outcome_label`
- `dry_run_readiness_requested_by_human`
- `dry_run_readiness_performed_by_human_or_tooling`
- `dry_run_readiness_timestamp`
- `dry_run_readiness_scope`
- `non_runtime_only`
- `non_authoritative_only`
- `no_route_authority`
- `no_prompt_loading`
- `critical_boundary_error_budget`
- `readiness_gate_hash_algorithm`
- `readiness_gate_canonicalization_method`

A future readiness gate record with missing candidate traceability, missing static review outcome-gate reference, missing outcome-gate hash, missing readiness scope, missing non-runtime declaration, missing non-authoritative declaration, missing no-route-authority declaration, missing no-prompt-loading declaration, missing hash algorithm, or missing canonicalization method must not progress.

## Required static review outcome-gate reference doctrine

A future dry-run readiness gate may only reason over a governed static review outcome gate from the future MLRT-5-derived outcome-gate phase.

The planned future readiness gate must require evidence for at least:

- package identity and traceability
- static review evidence-envelope reference
- static review outcome-gate reference
- static review outcome-gate hash
- critical boundary blocker status
- static review pass-candidate or rejection label
- human review escalation status
- non-runtime declaration
- non-authoritative declaration
- no-route-authority declaration
- no-prompt-loading declaration
- no-provider-call declaration
- no-embedding-call declaration
- no-network-call declaration
- no-subprocess-call declaration
- no-batch-mode declaration
- no-persistence declaration
- no-Pilot declaration
- no-Copilot declaration
- no-activation declaration
- no-field-test declaration

A missing outcome-gate reference, missing outcome-gate hash, unresolved human escalation, unresolved rejection label, or any critical boundary blocker must produce `MLRT_DRY_RUN_READINESS_INCOMPLETE` or a stricter rejection label.

## Non-runtime dry-run scope doctrine

A future non-runtime dry run, if later planned under a separate governed milestone, must be isolated from runtime and authority surfaces.

A future non-runtime dry-run scope may only include planning for:

- static case input references
- static candidate package references
- static contract references
- static expected-output references
- non-authoritative dry-run output records
- non-authoritative dry-run rejection records
- non-authoritative dry-run failure classification
- non-authoritative human review notes
- no-route-authority enforcement
- no-prompt-loading enforcement
- no-persistence enforcement
- zero critical boundary error doctrine

A future non-runtime dry run must not be a runtime Pilot, Copilot, activation, field test, production run, batch mode, route selector, prompt loader, provider caller, provider calls, embedding caller, or persistent ML decision writer.

## Candidate package eligibility doctrine

A future readiness gate may define a planning-only eligibility label, but that label must not mean a candidate is accepted, installed, imported, executed, reliable, routable, activated, field-tested, usable by Pilot, or usable by Copilot.

A future package may become eligible for dry-run protocol planning only when all of these are true:

- static review outcome-gate traceability is complete
- static review outcome-gate hash is present
- no critical boundary blocker exists
- no route authority claim exists
- no prompt loading claim exists
- no provider, embedding, network, subprocess, or batch-mode capability exists
- no persistence of ML decisions exists
- no activation, field-test, Pilot, or Copilot capability exists
- human escalation is absent or resolved as a blocker-free non-approval note
- the future dry-run scope remains non-runtime and non-authoritative

Even then, the only allowed positive label remains planning-only and non-authoritative.

## Dry-run protocol precondition doctrine

MLRT-6 may only lead to a future dry-run protocol planning milestone. It must not directly lead to dry-run execution.

A future dry-run protocol plan must still be defined separately before any future dry-run execution can be considered. That later protocol plan must define at least:

- static input source references
- candidate package reference rules
- input/output contract reference rules
- dry-run output envelope rules
- dry-run rejection envelope rules
- dry-run failure taxonomy references
- hard-gate handling rules
- critical boundary failure handling rules
- allowed non-authoritative evidence locations, if any
- report-generation boundaries, if any
- human review requirements
- freeze requirements

MLRT-6 does not create that protocol. It only defines readiness doctrine for designing it later.

## Critical boundary blocker doctrine

A future dry-run readiness gate must treat critical boundary violations as hard blockers.

The following planned future conditions must always block progression:

- any route authority claim
- any prompt loading claim
- any provider call capability
- any embedding or vector-store capability
- any network call capability
- any subprocess call capability
- any batch-mode capability
- any persistence of ML decisions
- any report persistence outside approved future non-runtime evidence area
- any freeze memory mutation
- any prompt library mutation
- any router canon mutation
- any gold registry mutation
- any startup pack mutation
- any approval state mutation
- any activation state mutation
- any field-test state mutation
- any runtime decision log mutation
- any activation key creation
- any Pilot enablement
- any Copilot enablement
- any automatic maturity jump
- any candidate attempt to produce route decisions
- any candidate attempt to issue runtime commands
- any candidate attempt to perform dry-run execution before a governed dry-run protocol exists

A critical boundary blocker cannot be overridden by usefulness, confidence, convenience, aggregate scores, human preference, or a candidate's claimed safety.

## Human-escalation doctrine

A future dry-run readiness gate may record that human review is required, but it must not record human approval.

A future dry-run readiness gate may include:

- `needs_human_review`
- `human_review_reason_codes`
- `human_review_requested_scope`
- `human_review_required_before_progression`
- `reviewer_notes_non_authoritative`

A future dry-run readiness gate must not include:

- `record_human_approval`
- `approve_readiness`
- `approve_reliability`
- `approve_dry_run_execution`
- `approve_activation`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`
- `write_startup_pack`

Human escalation may stop or defer a future readiness gate, but it cannot authorize dry-run execution, routing, activation, field testing, Pilot, Copilot, or ML implementation.

## Dry-run protocol planning label doctrine

The only positive MLRT-6 planning label is:

```text
MLRT_DRY_RUN_READINESS_READY_FOR_DRY_RUN_PROTOCOL_PLANNING_ONLY
```

This label means the readiness-gate doctrine is ready for a later governed non-runtime dry-run protocol planning milestone.

It does not mean that dry-run readiness has been performed. It does not mean readiness records exist. It does not mean a dry-run protocol exists. It does not mean a dry run can execute. It does not mean a candidate is reliable. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Dry-run readiness non-authority doctrine

A future dry-run readiness gate must remain non-authoritative.

A future dry-run readiness gate must not become:

- a route decision
- a prompt loading instruction
- an install command
- an import command
- an execution command
- a dry-run execution command
- a scoring command
- a report generation command
- a report persistence command
- a freeze write
- a human approval record
- a readiness approval record
- a reliability approval record
- a dry-run execution approval record
- an activation signal
- a field-test signal
- a runtime Pilot command
- a Copilot instruction
- an ML implementation unlock

## Dry-run readiness forbidden authority fields

A future dry-run readiness gate must reject these fields or equivalent behavior anywhere in package metadata, package manifest, checklist status, evidence envelope, outcome gate, dry-run readiness gate, or reviewer note:

- `route_decision`
- `load_prompt`
- `execute_route`
- `execute_dry_run`
- `approve_readiness`
- `approve_reliability`
- `approve_dry_run_execution`
- `record_human_approval`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`
- `write_startup_pack`
- `activate_pilot`
- `activate_copilot`
- `enable_field_test`
- `call_provider`
- `call_embedding_model`
- `network_call`
- `subprocess_call`
- `start_batch_mode`
- `persist_ml_decision`
- `runtime_command`
- `pilot_instruction`
- `copilot_instruction`

## Rejection labels

Allowed future rejection labels include:

- `MLRT_DRY_RUN_READINESS_INCOMPLETE`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_MISSING_OUTCOME_GATE`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_OUTCOME_GATE_HASH_RISK`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_UNRESOLVED_HUMAN_ESCALATION`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_FORBIDDEN_RUNTIME_BOUNDARY`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_FORBIDDEN_IMPORT_OR_DEPENDENCY`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_PERSISTENCE_OR_AUTHORITY_RISK`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_PROMPT_OR_ROUTE_AUTHORITY_RISK`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_PROVIDER_EMBEDDING_NETWORK_SUBPROCESS_OR_BATCH_RISK`
- `MLRT_DRY_RUN_READINESS_REJECTED_BY_PILOT_COPILOT_ACTIVATION_OR_FIELD_TEST_RISK`
- `MLRT_DRY_RUN_READINESS_NEEDS_HUMAN_REVIEW`

A rejection label must not be converted into a soft score and must not be used as evidence of candidate reliability.

## Critical boundary budget

The critical boundary error budget remains `0`.

Neither MLRT-5 nor MLRT-6 validates candidate reliability.

Any planned future dry-run readiness gate with a critical boundary error must be considered blocked, regardless of other soft metrics or human preference.

## Forbidden actions

MLRT-6 must not:

- implement ML logic
- implement a candidate
- create a candidate package
- accept a candidate package
- install a candidate package
- import a candidate package
- validate a candidate package
- execute a candidate
- perform static review
- create static review records
- create static review evidence records
- create static review outcome records
- create outcome gate records
- perform dry-run readiness review
- create dry-run readiness records
- create dry-run protocol records
- execute a dry run
- create dry-run outputs
- create candidate outputs
- execute LAB cases
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
- mutate corpus, fixtures, canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage
- unlock ML implementation

## Next safe milestone

After MLRT-6 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-7 - Candidate Non-Runtime Dry-Run Protocol Plan
```

MLRT-7 must remain governed and non-runtime. It may only plan the dry-run protocol. It must not execute a dry run, score cases, validate reliability, or unlock ML implementation.
