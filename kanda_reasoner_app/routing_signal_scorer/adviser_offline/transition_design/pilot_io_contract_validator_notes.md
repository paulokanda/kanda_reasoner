# P2 - Pilot Input Output Contract and Validator Design v1

Feature ID: `routing_signal_scorer_v3_pilot_io_contract_validator_design_v1`

This note accompanies `pilot_io_contract_validator_design.py`.

P2 is design-only. It defines the future Pilot input/output field envelope and
fail-closed validator rules, but it does not implement a live validator and does
not process inputs or generate outputs.

P2 does not implement Pilot, does not implement Copilot, does not implement projection logic, does not load prompts, and does not grant runtime authority.

## Preconditions

P2 requires:

- M35 post-Adviser to Pilot/Copilot handoff closure frozen.
- RG-PILOT-000 Pilot/Copilot Phase 0 router canon frozen.
- P0 Pilot/Copilot scope charter and entry gate frozen.
- P1 Pilot boundary design frozen.
- Startup freeze context refreshed after P1.
- `FREEZE_MEMORY_STATUS: OK` after P1.

## Allowed future input fields

Allowed future input fields are primitive and caller supplied only:

- `case_id`
- `schema_version`
- `user_request_summary`
- `routing_context_public_summary`
- `task_classification_hints_summary`
- `current_router_outcome_summary`
- `frozen_canon_constraints_summary`
- `known_boundary_flags`
- `caller_generated_timestamp_utc`

The unsafe prompt-group field name is not allowed. The contract uses
`task_classification_hints_summary` instead.

## Allowed future output fields

Allowed future output fields are non-authoritative human-review support only:

- `pilot_record_kind`
- `case_id`
- `schema_version`
- `authority_notice`
- `projection_analysis_summary`
- `task_classification_projection_summary`
- `reasoning_summary_for_human_review`
- `boundary_flags_for_human_review`
- `divergence_summary_for_human_review`
- `divergence_type`
- `missing_information_summary`
- `human_review_mandatory`
- `advisory_review_priority`
- `routing_effect`
- `prompt_loading_effect`
- `runtime_effect`
- `activation_effect`
- `storage_status`

`human_review_mandatory` is a non-suppressible invariant. It must remain true in
any later implementation.

The effect fields must remain fixed module-level constants:

- `routing_effect = "none"`
- `prompt_loading_effect = "none"`
- `runtime_effect = "none"`
- `activation_effect = "none"`
- `storage_status = "in_memory_only"`

## Fail-closed validator design

A later validator must reject:

- unknown keys;
- missing required keys;
- blank required strings;
- non-string scalar values;
- non-tuple boundary flags;
- nested objects;
- callable values;
- file handles;
- runtime objects;
- prompt objects;
- registry objects;
- provider or model configuration;
- path, URL, network, or execution markers;
- prompt-loading instructions;
- route-execution or route-override instructions;
- gold or registry mutation instructions;
- persistence instructions;
- training-data-use instructions;
- batch-mode instructions;
- activation instructions.

## Forbidden field names

The design explicitly records names that future payloads must reject, including
unsafe prompt-group, route-authority, prompt-loading, promotion, persistence,
human-decision, false-precision, recommendation, and runtime-enable names.

These names appear only as banned names inside this design artifact. They must
not appear as allowed input or output field names.

## Non-goals

P2 does not:

- implement a live validator;
- process input payloads;
- generate output payloads;
- implement Pilot;
- implement Copilot;
- implement projection logic;
- execute route comparison;
- select, override, or execute routes;
- select or load prompts;
- scan prompt libraries;
- import or integrate the runtime router;
- write files;
- persist, cache, log, or serialize Pilot outputs;
- write reports or review queues;
- record human decisions;
- mutate gold or registry state;
- use Pilot output as training data;
- run batch mode;
- call providers or models;
- create embeddings or vector indexes;
- activate limited shadow runtime;
- promote candidates;
- grant runtime authority.

## Next allowed milestone

After P2 validation, freeze, startup freeze context refresh, and
`FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

P3 - Routing Signal Scorer v3 Pilot Disagreement Taxonomy Design v1.
