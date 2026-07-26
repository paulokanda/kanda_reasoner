# MLRT-3 - Candidate Static Review Checklist Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_static_review_checklist_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-3 Candidate Static Review Checklist Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-3-candidate-static-review-checklist-plan`

Status: governed documentation-only MLRT static-review checklist-planning milestone.

## Purpose

MLRT-3 defines the planned checklist for a future static review of a candidate package.

MLRT-3 does not perform static review. It does not accept, install, import, execute, validate, score, compare, or evaluate a candidate package. It does not create static review records, candidate outputs, reliability reports, persistent reports, or persistent ML decisions. It does not validate candidate reliability and does not unlock ML implementation.

MLRT-3 only defines doctrine for what a future static review checklist would need before any later non-runtime dry-run or candidate evaluation planning may exist.

## Precondition inherited from MLRT-2

MLRT-3 may begin only after MLRT-2 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-2 established that the next safe step after candidate package intake contract planning is static review checklist planning only.

## Contract scope

MLRT-3 defines planned checklist groups for future static review. These checklist groups are doctrine only:

1. Package identity and traceability checklist.
2. File manifest and hash checklist.
3. Candidate interface declaration checklist.
4. Dependency and import boundary checklist.
5. Runtime and side-effect boundary checklist.
6. Prompt-loading and route-authority boundary checklist.
7. Provider, embedding, network, subprocess, and batch-mode boundary checklist.
8. Persistence, report, and ML-decision-storage boundary checklist.
9. Pilot, Copilot, activation, and field-test boundary checklist.
10. Human review escalation checklist.
11. Rejection checklist.
12. Static review outcome checklist.

MLRT-3 does not create executable validators. MLRT-3 does not scan or import candidate files. MLRT-3 does not perform static analysis. MLRT-3 does not create candidate package review records.

## Package identity and traceability checklist doctrine

A future static review checklist must require a reviewed candidate package to declare at least:

- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `candidate_kind`
- `candidate_origin`
- `candidate_author`
- `candidate_submission_date`
- `candidate_package_intake_record_id`
- `candidate_package_intake_label`
- `source_mlrt_phase`
- `target_review_phase`
- `review_requested_by_human`
- `non_runtime_only`
- `non_authoritative_only`

A future checklist must reject missing identity, missing package version, missing intake label, missing human-review request, or any attempt to bypass package intake.

## File manifest and hash checklist doctrine

A future static review checklist must require static file metadata without importing or executing any file.

The planned future checklist must include at least:

- all declared files are listed in the package contents manifest
- every listed file has a declared purpose
- every listed file has a SHA-256 hash
- every listed file has a size record
- every listed file has a path confined to the future candidate package review area
- every executable candidate file is marked for future review
- every entrypoint-like file is marked as non-runtime and non-authoritative
- no file is copied into a runtime box
- no file is copied into the LAB box as executable LAB source
- no file is copied into the prompt library, router canon, freeze memory, gold registry, startup pack, activation state, field-test state, runtime logs, or persistent ML decision storage

Missing hashes, path traversal, unlisted files, undeclared entrypoints, or mismatch between package metadata and contents manifest must block future review progression.

## Candidate interface declaration checklist doctrine

A future static review checklist must verify that the package declares the planned non-runtime candidate interface before later review can continue.

The planned future interface checklist must include at least:

- declared input envelope compatibility with MLRT-1
- declared output envelope compatibility with MLRT-1
- declared rejection envelope compatibility with MLRT-1
- declared package metadata compatibility with MLRT-2
- declared contents manifest compatibility with MLRT-2
- declared candidate output wrapper `non_authoritative_candidate_reliability_output_record`
- declared no-route-authority behavior
- declared no-prompt-loading behavior
- declared no-persistence behavior
- declared no-provider-call behavior
- declared no-embedding-call behavior
- declared no-activation behavior
- declared no-field-test behavior
- declared no-runtime-Pilot behavior
- declared no-Copilot behavior

A missing or ambiguous interface declaration must lead to a future rejection or human review request. It must not be interpreted as permission to execute the candidate.

## Dependency and import boundary checklist doctrine

A future static review checklist must require dependency declarations but must not install dependencies and must not import candidate code.

The planned future dependency checklist must require at least:

- declared standard-library dependencies
- declared third-party dependencies
- declared local project dependencies
- declared forbidden dependencies
- declared import targets
- declared import side-effect risk
- declared isolation requirement
- declared no-runtime-router-import
- declared no-prompt-loader-import
- declared no-provider-adapter-import
- declared no-embedding-adapter-import
- declared no-freeze-writer-import
- declared no-gold-registry-mutation-import
- declared no-activation-state-import
- declared no-field-test-state-import

A future package that requires imports from runtime router modules, prompt loaders, provider adapters, embedding adapters, freeze writers, gold-registry mutation utilities, activation state, field-test state, runtime decision logs, or persistent ML decision storage must be blocked.

## Runtime and side-effect boundary checklist doctrine

A future static review checklist must verify that the candidate package declares no runtime side effects.

The planned future side-effect checklist must reject any candidate package that requests or exposes:

- route authority
- prompt loading
- route selection
- runtime command execution
- install commands
- file writes outside an explicitly approved future non-runtime review area
- freeze memory mutation
- prompt library mutation
- router canon mutation
- gold registry mutation
- startup pack mutation
- approval state mutation
- activation state mutation
- field-test state mutation
- runtime decision log mutation
- persistent ML decision storage mutation
- provider calls
- embedding calls
- network calls
- subprocess calls
- batch mode
- runtime Pilot behavior
- Copilot behavior

Any such request is a critical boundary violation and must not be converted into a soft failure by aggregate metrics.

## Prompt-loading and route-authority boundary checklist doctrine

A future static review checklist must explicitly confirm that the candidate cannot load prompts and cannot decide routes.

The planned future checklist must reject these fields or equivalent behavior:

- `route_decision`
- `select_route`
- `execute_route`
- `load_prompt`
- `prompt_loading_instruction`
- `prompt_selection_instruction`
- `route_authority_override`
- `runtime_router_import`
- `router_canon_write`
- `routing_registry_write`

Candidate output remains non-authoritative even if later review approves a package for a later controlled non-runtime dry-run plan.


## Forbidden static review authority fields

A future static review checklist must reject these fields or equivalent behavior anywhere in a candidate package, metadata envelope, manifest, declared output, or review request:

- `route_decision`
- `load_prompt`
- `execute_route`
- `approve_readiness`
- `write_freeze_memory`
- `write_prompt_library`
- `write_router_canon`
- `activate_pilot`
- `activate_copilot`
- `call_provider`
- `call_embedding_model`
- `persist_ml_decision`
- `runtime_command`
- `copilot_instruction`

These fields are critical boundary violations in MLRT-3 planning and cannot be softened by review convenience, aggregate metrics, or future candidate claims.

## Provider, embedding, network, subprocess, and batch-mode boundary checklist doctrine

A future static review checklist must require explicit rejection of external execution mechanisms.

The planned future checklist must reject:

- `call_provider`
- `call_embedding_model`
- `network_call`
- `subprocess_call`
- `start_batch_mode`
- `background_job`
- `scheduler_job`
- `training_data_use`
- `vector_store_write`
- `vector_store_read`

MLRT-3 does not create adapters or allow such adapters. Any later change would require a separate governed scope after reliability evidence and freeze evidence.

## Persistence, report, and ML-decision-storage boundary checklist doctrine

MLRT-3 does not create persistent reports, persistent ML decisions, or static review records.

A future static review checklist must reject any package that tries to persist:

- candidate outputs
- route decisions
- prompt selections
- human approvals
- readiness approvals
- reliability approvals
- freeze writes
- runtime logs
- activation state
- field-test state
- Pilot state
- Copilot state
- persistent ML decisions

A future report or evidence envelope, if ever approved, must be non-authoritative and governed separately. It must not become a route decision, human approval, readiness approval, activation signal, field-test signal, runtime Pilot command, or Copilot instruction.

## Pilot, Copilot, activation, and field-test boundary checklist doctrine

A future static review checklist must reject any package that exposes or requests:

- `activate_pilot`
- `activate_copilot`
- `enable_field_test`
- `pilot_instruction`
- `copilot_instruction`
- `runtime_pilot_command`
- `copilot_runtime_action`
- `activation_key`
- `maturity_jump`
- `automatic_maturity_jump`

The future Pilot/Copilot activation boundary remains locked. MLRT-3 does not add an activation key, maturity state, field-test state, runtime Pilot, or Copilot behavior.

## Human review escalation checklist doctrine

A future static review checklist may define reasons to request human review.

Human review escalation may be requested for:

- ambiguous package identity
- unclear candidate purpose
- ambiguous dependency risk
- ambiguous import boundary risk
- unclear interface compatibility
- unclear side-effect declarations
- missing static evidence
- possible critical boundary violation
- mismatch between package metadata and contents manifest
- uncertainty about whether a package is a candidate or a prompt-library/governance patch

Human review escalation is not approval. A candidate package may request human review, but it must not record human approval, readiness approval, freeze authorization, activation authorization, field-test authorization, runtime Pilot authorization, or Copilot authorization.

## Rejection checklist doctrine

A future static review checklist must reject candidate packages for at least these classes:

- missing candidate package identity
- missing package intake traceability
- missing contents manifest
- missing SHA-256 file hashes
- unlisted files
- undeclared dependencies
- undeclared entrypoints
- path traversal or review-area escape
- runtime import request
- prompt-loader import request
- provider or embedding call request
- network, subprocess, scheduler, or batch-mode request
- persistence request
- route-authority request
- prompt-loading request
- freeze-memory, prompt-library, router-canon, gold-registry, startup-pack, approval-state, activation-state, field-test-state, runtime-log, or persistent-ML-decision mutation request
- Pilot, Copilot, activation, or field-test request
- unreliable or missing non-authoritative output wrapper declaration
- contradiction between metadata and manifest
- request to skip static review or bypass human review

Rejection remains non-authoritative and must not mutate project state beyond a later explicitly approved non-runtime record mechanism.

## Static review outcome checklist doctrine

Allowed future MLRT-3 static review planning labels are:

- `MLRT_STATIC_REVIEW_NOT_READY`
- `MLRT_STATIC_REVIEW_READY_FOR_EVIDENCE_ENVELOPE_PLANNING_ONLY`
- `MLRT_STATIC_REVIEW_BLOCKED_BY_MISSING_PACKAGE_TRACEABILITY`
- `MLRT_STATIC_REVIEW_BLOCKED_BY_MANIFEST_OR_HASH_RISK`
- `MLRT_STATIC_REVIEW_BLOCKED_BY_FORBIDDEN_RUNTIME_BOUNDARY`
- `MLRT_STATIC_REVIEW_BLOCKED_BY_FORBIDDEN_IMPORT_OR_DEPENDENCY`
- `MLRT_STATIC_REVIEW_BLOCKED_BY_PERSISTENCE_OR_AUTHORITY_RISK`
- `MLRT_STATIC_REVIEW_NEEDS_HUMAN_REVIEW`

The only positive MLRT-3 label is:

```text
MLRT_STATIC_REVIEW_READY_FOR_EVIDENCE_ENVELOPE_PLANNING_ONLY
```

This label does not mean that static review has been performed. It does not mean a package is safe. It does not mean a candidate is reliable. It does not mean a candidate can be installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Static review storage doctrine

MLRT-3 does not create static review storage.

A future static review evidence design, if ever approved, must remain non-runtime and non-authoritative. It must not become persistent ML decision storage, human approval storage, readiness approval storage, activation storage, field-test storage, runtime routing storage, or Copilot instruction storage.

No actual static review records are created by MLRT-3.

## Critical boundary rule

The critical boundary error budget remains `0`.

If a future static review checklist gives a candidate package any path to runtime authority, MLRT is invalid.

If a future static review checklist gives a candidate package any write path to freeze memory, prompt library, router canon, gold registry, startup pack, approval state, activation state, field-test state, runtime decision logs, or persistent ML decision storage, MLRT is invalid.

If a future static review checklist allows prompt loading, provider calls, embeddings, network calls, subprocess calls, persistence, batch mode, activation, field testing, runtime Pilot, or Copilot behavior, MLRT is invalid unless a later explicit governed scope changes that boundary after reliability has been proven and frozen.

## Relationship to MLRT-2

MLRT-2 defined the future package metadata and contents-manifest contract that would precede static review of a candidate package.

MLRT-3 defines the future static review checklist plan that would assess those package declarations without installing, importing, executing, or scoring the candidate.

Neither MLRT-2 nor MLRT-3 validates candidate reliability.

## Next safe milestone after MLRT-3

After MLRT-3 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-4 - Candidate Static Review Evidence Envelope Plan
```

MLRT-4 must remain governed and non-runtime. It may define a future evidence envelope for a static review result, but it must not perform static review, create static review records, implement a candidate, install a package, import a package, execute candidates, score cases, compare routes, grant route authority, load prompts, call providers, use embeddings, persist ML decisions or create persistent ML decisions, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

## ML implementation continuation lock

ML implementation remains blocked.

The continuation lock is:

```text
LAB closure/readiness review frozen
-> MLRT-0 controlled non-runtime candidate reliability test plan
-> MLRT-1 candidate reliability input/output contract plan
-> MLRT-2 candidate package intake contract plan
-> MLRT-3 candidate static review checklist plan
-> MLRT-4 candidate static review evidence envelope plan
```

No ML/router implementation continuation may proceed from MLRT-3.
