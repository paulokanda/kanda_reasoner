# MLRT-4 - Candidate Static Review Evidence Envelope Plan v1

Feature ID: `routing_signal_scorer_v3_mlrt_candidate_static_review_evidence_envelope_plan_v1`

Feature title: `Routing Signal Scorer v3 MLRT-4 Candidate Static Review Evidence Envelope Plan v1`

Primary box: `kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability`

Schema version: `mlrt-4-candidate-static-review-evidence-envelope-plan`

Status: governed documentation-only MLRT static-review evidence-envelope planning milestone.

## Purpose

MLRT-4 defines the planned evidence envelope for a future candidate static review.

MLRT-4 does not perform static review. It does not create static review evidence records. It does not create, accept, install, import, execute, validate, score, compare, or evaluate a candidate package. It does not create candidate outputs, reliability reports, persistent reports, persistent ML decisions, route decisions, human approvals, readiness approvals, activation signals, field-test signals, runtime Pilot commands, or Copilot instructions.

MLRT-4 only defines doctrine for what a future static review evidence envelope would need before any later static review outcome gate or non-runtime dry-run planning may exist.

## Precondition inherited from MLRT-3

MLRT-4 may begin only after MLRT-3 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

MLRT-3 established that the next safe step after candidate static review checklist planning is static review evidence envelope planning only.

## Contract scope

MLRT-4 defines planned evidence-envelope groups for a future static review. These groups are doctrine only:

1. Evidence envelope identity and traceability.
2. Candidate package reference evidence.
3. Static review checklist reference evidence.
4. Manifest and hash evidence.
5. Dependency and import boundary evidence.
6. Side-effect and persistence boundary evidence.
7. Prompt-loading and route-authority boundary evidence.
8. Provider, embedding, network, subprocess, and batch-mode evidence.
9. Pilot, Copilot, activation, and field-test boundary evidence.
10. Human review escalation evidence.
11. Rejection evidence.
12. Evidence-envelope outcome label doctrine.

MLRT-4 does not create executable validators. MLRT-4 does not scan, import, execute, or review candidate files. MLRT-4 does not write static review evidence records.

## Evidence envelope identity and traceability doctrine

A future static review evidence envelope must declare at least:

- `static_review_evidence_envelope_id`
- `static_review_evidence_envelope_version`
- `schema_version`
- `mlrt_phase_reference`
- `candidate_package_id`
- `candidate_package_version`
- `candidate_id`
- `candidate_version`
- `candidate_package_intake_record_id`
- `static_review_checklist_version`
- `static_review_requested_by_human`
- `static_review_performed_by_human_or_tooling`
- `review_timestamp`
- `review_scope`
- `non_runtime_only`
- `non_authoritative_only`
- `critical_boundary_error_budget`
- `evidence_hash_algorithm`
- `evidence_canonicalization_method`

A future evidence envelope with missing package traceability, missing checklist version, missing review scope, missing non-runtime declaration, missing non-authoritative declaration, missing hash algorithm, or missing canonicalization method must not progress.

## Candidate package reference evidence doctrine

A future evidence envelope must reference package-intake data from MLRT-2 without copying a real candidate package into runtime.

The planned future package-reference evidence must include at least:

- package metadata envelope reference
- package contents manifest reference
- package intake decision envelope reference
- package intake rejection envelope reference when applicable
- declared file list reference
- declared file hash list reference
- declared dependency list reference
- declared entrypoint list reference
- declared permission list reference
- declared forbidden-action list reference

The future evidence envelope must not be treated as acceptance, installation, import, execution, validation, or reliability approval for a candidate package.

## Static review checklist reference evidence doctrine

A future evidence envelope must reference the MLRT-3 checklist groups that were considered, without creating authority to execute the candidate.

The planned future checklist-reference evidence must include status for at least:

- package identity and traceability checklist
- file manifest and hash checklist
- candidate interface declaration checklist
- dependency and import boundary checklist
- runtime and side-effect boundary checklist
- prompt-loading and route-authority boundary checklist
- provider, embedding, network, subprocess, and batch-mode boundary checklist
- persistence, report, and ML-decision-storage boundary checklist
- Pilot, Copilot, activation, and field-test boundary checklist
- human review escalation checklist
- rejection checklist
- static review outcome checklist

A missing checklist-reference status must produce `MLRT_STATIC_REVIEW_EVIDENCE_INCOMPLETE` or a stricter rejection label.

## Manifest and hash evidence doctrine

A future evidence envelope must preserve manifest and hash evidence without mutating package files or project source.

The planned future evidence envelope must include:

- declared file paths
- declared file purposes
- declared SHA-256 hashes
- observed hash references when review is later performed under a separate governed scope
- hash comparison status
- path confinement status
- path traversal check status
- unlisted-file check status
- package-manifest consistency status
- evidence-envelope hash
- aggregate evidence hash

The planned hash doctrine remains SHA-256.

A hash mismatch, unlisted file, missing hash, path traversal attempt, path outside the future review area, or mismatch between package metadata and manifest must be a hard blocker and may be a critical boundary violation when runtime or protected project paths are implicated.

## Dependency and import boundary evidence doctrine

A future evidence envelope must capture dependency and import evidence without installing dependencies and without importing candidate code.

The planned future evidence envelope must include status for:

- declared standard-library dependencies
- declared third-party dependencies
- declared local project dependencies
- declared forbidden dependencies
- declared import targets
- declared import side-effect risk
- declared isolation requirement
- runtime router import risk
- prompt loader import risk
- provider adapter import risk
- embedding adapter import risk
- freeze writer import risk
- gold registry mutation import risk
- activation state import risk
- field-test state import risk
- runtime decision log import risk
- persistent ML decision storage import risk

A future evidence envelope must reject or escalate any dependency or import evidence that points to runtime router modules, prompt loaders, provider adapters, embedding adapters, freeze writers, gold-registry mutation utilities, activation state, field-test state, runtime decision logs, or persistent ML decision storage.

## Side-effect and persistence boundary evidence doctrine

A future evidence envelope must capture side-effect and persistence boundary evidence.

The planned future evidence envelope must explicitly record absence or rejection of:

- file writes outside approved future non-runtime review area
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
- report persistence
- candidate output persistence
- route decision persistence
- human approval persistence
- readiness approval persistence

MLRT-4 does not persist any such evidence. It only defines the future envelope doctrine.

## Prompt-loading and route-authority boundary evidence doctrine

A future evidence envelope must explicitly prove that static review found no prompt-loading or route-authority claims before any later planning milestone may continue.

The planned future evidence envelope must reject these fields or equivalent behavior:

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

Candidate static review evidence remains non-authoritative even when it later records no observed route-authority risk.

## Provider, embedding, network, subprocess, and batch-mode evidence doctrine

A future evidence envelope must explicitly record absence or rejection of external execution mechanisms.

The planned future evidence envelope must reject:

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

MLRT-4 does not call providers, does not call embedding models, does not use network, does not use subprocess, and does not start batch mode.

## Pilot, Copilot, activation, and field-test boundary evidence doctrine

A future evidence envelope must explicitly record absence or rejection of:

- activation key creation
- activation key use
- Pilot enablement
- Copilot enablement
- field-test enablement
- runtime Pilot behavior
- Copilot behavior
- automatic maturity jump
- readiness approval
- human approval recording

The presence of such requests must be a critical boundary violation and must not be softened by review convenience, aggregate scoring, or a candidate's claimed usefulness.

## Human review escalation evidence doctrine

A future evidence envelope may record that human review is required, but it must not record human approval.

A future evidence envelope may include:

- `needs_human_review`
- `human_review_reason_codes`
- `human_review_requested_scope`
- `human_review_required_before_progression`
- `reviewer_notes_non_authoritative`

A future evidence envelope must not include:

- `record_human_approval`
- `approve_readiness`
- `approve_reliability`
- `approve_activation`
- `write_freeze_memory`
- `write_gold_registry`
- `write_prompt_library`
- `write_router_canon`

## Rejection evidence doctrine

A future static review evidence envelope must support rejection evidence without granting authority.

Allowed future rejection labels include:

- `MLRT_STATIC_REVIEW_EVIDENCE_INCOMPLETE`
- `MLRT_STATIC_REVIEW_EVIDENCE_REJECTED_BY_MISSING_PACKAGE_TRACEABILITY`
- `MLRT_STATIC_REVIEW_EVIDENCE_REJECTED_BY_HASH_OR_MANIFEST_RISK`
- `MLRT_STATIC_REVIEW_EVIDENCE_REJECTED_BY_FORBIDDEN_RUNTIME_BOUNDARY`
- `MLRT_STATIC_REVIEW_EVIDENCE_REJECTED_BY_FORBIDDEN_IMPORT_OR_DEPENDENCY`
- `MLRT_STATIC_REVIEW_EVIDENCE_REJECTED_BY_PERSISTENCE_OR_AUTHORITY_RISK`
- `MLRT_STATIC_REVIEW_EVIDENCE_NEEDS_HUMAN_REVIEW`

A rejection label must not be converted into a soft score and must not be used as evidence of candidate reliability.

## Evidence-envelope outcome label doctrine

The only positive MLRT-4 planning label is:

```text
MLRT_STATIC_REVIEW_EVIDENCE_READY_FOR_OUTCOME_GATE_PLANNING_ONLY
```

This label means the evidence-envelope doctrine is ready for a later governed outcome-gate planning milestone.

It does not mean that static review has been performed. It does not mean evidence records exist. It does not mean a candidate is reliable. It does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot.

## Forbidden evidence-envelope authority fields

A future evidence envelope must reject these fields or equivalent behavior anywhere in package metadata, package manifest, checklist status, evidence envelope, or reviewer note:

- `route_decision`
- `load_prompt`
- `execute_route`
- `approve_readiness`
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
- `start_batch_mode`
- `persist_ml_decision`
- `runtime_command`
- `pilot_instruction`
- `copilot_instruction`

These fields are critical boundary violations in MLRT-4 planning and cannot be softened by aggregate metrics, review convenience, or future candidate claims.

## Preserved boundary

The critical boundary error budget remains `0`.

MLRT-4 must preserve:

- no route authority
- no prompt loading
- no persistence
- no provider calls
- no embeddings/vector stores
- no network calls
- no subprocess calls
- no batch mode
- no activation
- no field testing
- no runtime Pilot behavior
- no Copilot behavior
- no candidate execution
- no case execution
- no case scoring
- no route comparison
- no report generation
- no report persistence
- no candidate reliability claim
- no ML implementation unlock

Neither MLRT-3 nor MLRT-4 validates candidate reliability.

## Next safe milestone

After MLRT-4 is locally validated, frozen, startup context is refreshed, and `FREEZE_MEMORY_STATUS: OK` is confirmed, the next safe milestone is:

```text
MLRT-5 - Candidate Static Review Outcome Gate Plan
```

MLRT-5 must remain governed and non-runtime unless a later explicit scope changes that boundary after reliability is proven and frozen.
