# MLRT-8 - Candidate Non-Runtime Dry-Run Input Set Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_input_set_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-8 Candidate Non-Runtime Dry-Run Input Set Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-8-candidate-non-runtime-dry-run-input-set-plan`

Status: governed documentation-only MLRT non-runtime dry-run input-set planning milestone.

## Purpose

MLRT-8 defines the planned input-set doctrine for a future non-runtime dry run.

MLRT-8 does not create dry-run input records. It does not create dry-run input manifests. It does not create dry-run protocol records. It does not create dry-run protocol execution records. It does not create dry-run outputs. It does not execute a dry run. It does not execute a candidate. It does not create candidate outputs. It does not execute cases. It does not score cases. It does not validate candidate reliability. It does not unlock ML implementation.

MLRT-8 only defines doctrine for how a future dry-run input set could be specified under a later governed milestone.

## Precondition inherited from MLRT-7

MLRT-8 may begin only after MLRT-7 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-7 established that the next safe step after dry-run protocol planning is dry-run input-set planning only.

## Contract scope

MLRT-8 defines planned input-set groups for a future non-runtime dry run. These groups are doctrine only:

1. Input-set identity and traceability doctrine.
2. Required dry-run protocol reference doctrine.
3. Static case reference doctrine.
4. Static candidate input envelope doctrine.
5. Expected contract-output reference doctrine.
6. Expected rejection-output reference doctrine.
7. Boundary-trigger case doctrine.
8. Human-review trigger case doctrine.
9. Deterministic ordering doctrine.
10. No-live-data doctrine.
11. No-live-project-read doctrine.
12. Input-set hash and canonicalization doctrine.
13. Input-set non-authority doctrine.
14. Input-set forbidden authority field doctrine.
15. Input-set next-milestone doctrine.

MLRT-8 does not create executable validators. MLRT-8 does not read, scan, import, execute, or review candidate files. MLRT-8 does not write dry-run input records. MLRT-8 does not execute cases.

## Input-set identity and traceability doctrine

A future dry-run input set must declare at least:

- `dry_run_input_set_id`
- `dry_run_input_set_version`
- `schema_version`
- `mlrt_phase_reference`
- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `dry_run_protocol_id`
- `dry_run_protocol_hash`
- `dry_run_protocol_label`
- `static_review_outcome_gate_id`
- `dry_run_readiness_gate_id`
- `input_case_count`
- `input_case_ids`
- `input_case_ordering_method`
- `input_set_hash_algorithm`
- `input_set_canonicalization_method`
- `non_runtime_only`
- `non_authoritative_only`
- `no_route_authority`
- `no_prompt_loading`
- `critical_boundary_error_budget`

A future input set with missing protocol reference, missing protocol hash, missing candidate traceability, missing deterministic ordering method, missing hash algorithm, missing canonicalization method, missing non-runtime declaration, missing non-authoritative declaration, missing no-route-authority declaration, or missing no-prompt-loading declaration must not progress.

## Required dry-run protocol reference doctrine

A future input set may only be planned against a governed dry-run protocol from MLRT-7-derived protocol planning.

The planned future input set must require evidence for at least:

- protocol identity and traceability
- protocol hash
- protocol readiness label
- candidate package reference
- non-runtime scope
- candidate invocation envelope reference
- output capture envelope reference
- failure and rejection envelope reference
- critical boundary blocker status
- human review escalation status
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

A missing dry-run protocol reference, missing protocol hash, unresolved protocol rejection, unresolved human escalation, or any critical boundary blocker must produce `MLRT_DRY_RUN_INPUT_SET_INCOMPLETE` or a stricter rejection label.

## Static case reference doctrine

A future input set may reference only static cases created under governed non-runtime lab/corpus rules.

A future input set must not use live prompt-library reads, live freeze-memory reads, live router-canon reads, live runtime logs, live user data, network-loaded data, provider-loaded data, embedding-loaded data, or subprocess-loaded data.

Each future static case reference should be immutable and traceable by at least:

- `case_id`
- `case_version`
- `case_hash`
- `case_source_phase`
- `case_expected_contract_version`
- `case_boundary_trigger_tags`
- `case_human_review_trigger_tags`
- `case_order_index`

MLRT-8 does not create these case records and does not execute these cases.

## Static candidate input envelope doctrine

A future input set may plan input envelopes only as static doctrine.

A future candidate input envelope may include only non-authoritative test material such as:

- static case payload
- static routing-context fixture reference
- static candidate input metadata
- expected output contract version
- expected rejection contract version
- non-runtime declaration
- non-authoritative declaration
- no-route-authority declaration
- no-prompt-loading declaration

A future input envelope must not include live prompt text, prompt loading instructions, route decisions, runtime commands, provider-call instructions, embedding-call instructions, network-call instructions, subprocess-call instructions, batch-mode commands, persistence commands, activation commands, field-test commands, Pilot commands, or Copilot instructions.

## Expected contract-output reference doctrine

A future input set may reference the expected output contract shape from earlier governed planning. It must not create outputs.

A future expected output reference may include:

- expected candidate output envelope version
- expected non-authoritative result fields
- expected boundary status fields
- expected human-review flag fields
- expected rejection reference fields
- expected no-authority assertion fields

This reference must not become a scoring result, pass/fail outcome, reliability metric, route decision, readiness approval, activation signal, or runtime instruction.

## Expected rejection-output reference doctrine

A future input set must include rejection doctrine for malformed or unsafe candidate output.

A future rejection reference may include:

- malformed input envelope rejection
- missing protocol reference rejection
- missing candidate traceability rejection
- route-authority field rejection
- prompt-loading field rejection
- runtime-command field rejection
- provider-call field rejection
- embedding-call field rejection
- network-call field rejection
- subprocess-call field rejection
- batch-mode field rejection
- persistence field rejection
- activation field rejection
- field-test field rejection
- Pilot field rejection
- Copilot field rejection

Rejection references are not approvals and do not execute anything.

## Boundary-trigger case doctrine

A future dry-run input set should include planned boundary-trigger cases that can later test whether a candidate output attempts prohibited authority.

Boundary-trigger case tags may include:

- `boundary_route_authority_attempt`
- `boundary_prompt_loading_attempt`
- `boundary_provider_call_attempt`
- `boundary_embedding_call_attempt`
- `boundary_network_call_attempt`
- `boundary_subprocess_call_attempt`
- `boundary_batch_mode_attempt`
- `boundary_persistence_attempt`
- `boundary_freeze_memory_write_attempt`
- `boundary_prompt_library_write_attempt`
- `boundary_router_canon_write_attempt`
- `boundary_gold_registry_write_attempt`
- `boundary_startup_pack_write_attempt`
- `boundary_activation_attempt`
- `boundary_field_test_attempt`
- `boundary_runtime_pilot_attempt`
- `boundary_copilot_attempt`

MLRT-8 does not create these cases and does not run them.

## Human-review trigger case doctrine

A future input set may plan human-review trigger cases where automated interpretation would be unsafe or insufficient.

Human-review trigger tags may include:

- `human_review_ambiguous_candidate_output`
- `human_review_missing_traceability`
- `human_review_contract_conflict`
- `human_review_boundary_risk_possible`
- `human_review_reliability_claim_present`
- `human_review_readiness_claim_present`
- `human_review_activation_claim_present`

Human review triggers must not become human approvals.

## Deterministic ordering doctrine

A future input set must be deterministic.

Planned ordering should be stable by one canonical method, such as:

- lexicographic `case_id`
- explicit `case_order_index`
- canonical hash order

Input-set order must not depend on filesystem traversal order, runtime timestamps, provider outputs, network responses, embeddings, random seeds, or subprocess outputs.

## No-live-data doctrine

A future input set must not use live or mutable data as input.

Forbidden live sources include:

- live prompt-library files
- live freeze memory
- live router canon
- live runtime logs
- live runtime router modules
- live project state outside the frozen fixture/input set
- network responses
- provider responses
- embedding outputs
- subprocess outputs
- user inbox or calendar data
- operating-system process state

## No-live-project-read doctrine

A future dry-run may be allowed to read a sealed static input set only after a separate governed milestone creates that input set.

It must not read live project files to invent or modify test content during execution. It must not mutate corpus, fixtures, canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage.

## Input-set hash and canonicalization doctrine

A future input set must be hashable and reproducible.

A future canonical input-set representation should define:

- UTF-8 encoding
- deterministic key ordering
- stable line endings
- stable case ordering
- stable null/empty field representation
- stable hash algorithm
- inclusion and exclusion rules
- no runtime-generated timestamps in hash material
- no local absolute path dependency in hash material

MLRT-8 does not calculate input-set hashes. It only defines the doctrine that future input sets must be hashable.

## Critical boundary blocker doctrine

The critical boundary error budget remains `0`.

Any future input-set design that permits route authority, prompt loading, provider calls, embedding calls, network calls, subprocess calls, batch mode, persistence, report persistence, freeze-memory writes, prompt-library writes, router-canon writes, gold-registry writes, startup-pack writes, activation, field testing, runtime Pilot behavior, or Copilot behavior must be blocked.

Neither MLRT-7 nor MLRT-8 validates candidate reliability.

## Input-set planning label doctrine

The only positive MLRT-8 label is:

```text
MLRT_DRY_RUN_INPUT_SET_READY_FOR_OUTPUT_CAPTURE_PLANNING_ONLY
```

This label only means that the dry-run input-set planning document is ready to support a later dry-run output-capture planning milestone after local validation, freeze, startup context refresh, and `FREEZE_MEMORY_STATUS: OK`.

It does not mean that input records exist. It does not mean a dry run can execute. It does not mean candidate outputs exist. It does not mean output capture exists. It does not mean a candidate is reliable. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

Allowed future planning labels may include only:

- `MLRT_DRY_RUN_INPUT_SET_NOT_READY`
- `MLRT_DRY_RUN_INPUT_SET_INCOMPLETE`
- `MLRT_DRY_RUN_INPUT_SET_BLOCKED_BY_MISSING_PROTOCOL_REFERENCE`
- `MLRT_DRY_RUN_INPUT_SET_BLOCKED_BY_HASH_OR_TRACEABILITY_MISMATCH`
- `MLRT_DRY_RUN_INPUT_SET_BLOCKED_BY_CRITICAL_BOUNDARY_RISK`
- `MLRT_DRY_RUN_INPUT_SET_NEEDS_HUMAN_REVIEW`
- `MLRT_DRY_RUN_INPUT_SET_READY_FOR_OUTPUT_CAPTURE_PLANNING_ONLY`

## Input-set non-authority doctrine

A future input set must remain non-authoritative. It must not decide routes, rank routes for use, load prompts, approve reliability, approve readiness, approve dry-run execution, create install commands, create runtime commands, write freeze memory, write the prompt library, write router canon, write the gold registry, write startup packs, call providers, call embedding models, perform network calls, perform subprocess calls, start batch mode, persist ML decisions, activate Pilot, activate Copilot, enable field tests, or instruct runtime Pilot or Copilot behavior.

## Input-set forbidden authority fields

Future dry-run input-set envelopes must reject fields named:

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

## Explicit non-actions

MLRT-8 does not:

- create an ML/router candidate
- create or accept a real candidate package
- install a candidate package
- import a candidate package
- execute a candidate
- create candidate outputs
- perform static review
- create static review records
- create static review evidence records
- create static review outcome records
- create outcome gate records
- perform dry-run readiness review
- create dry-run readiness records
- create dry-run protocol records
- create dry-run protocol execution records
- execute a dry run
- create dry-run input records
- create dry-run input manifests
- create dry-run outputs
- execute LAB cases
- score cases
- compare live routes
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
- create or persist reports
- mutate corpus, fixtures, canon, prompt library, freeze memory, gold registry, startup pack, approval state, activation state, field-test state, runtime logs, or persistent ML decision storage
- create activation keys
- enable field-test mode
- create runtime Pilot behavior
- create Copilot behavior
- unlock ML implementation

## Next safe milestone

After MLRT-8 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-9 - Candidate Non-Runtime Dry-Run Output Capture Plan
```

MLRT-9 must remain governed and non-runtime. It may only plan dry-run output capture. It must not create dry-run outputs, execute a dry run, score cases, validate candidate reliability, or unlock ML implementation.
