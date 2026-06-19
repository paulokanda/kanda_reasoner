---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-design-v1"
feature_title: "Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer Design v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-design-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "M10 remains design-only for future Adviser Candidate v0 offline lexical scorer."
  - "M10 must not create candidate modules or candidate outputs."
  - "M10 must not execute candidate logic, ML, providers, embeddings, vector indexes, source scanning, prompt auto-loading, artifact IO, or runtime router integration."
  - "Future M11 candidate must be standard-library-only and pure over caller-supplied primitive inputs."
  - "Runtime router code must not import adviser_offline, candidate design, or seed gold data."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-design-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-design-v1`

Feature title: `Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer Design v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_candidate_design_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M10 defines the design-only boundary for a future Adviser Candidate v0 offline lexical scorer. It adds design/spec documentation and tests only; no candidate module, candidate outputs, candidate execution, ML, runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, or router authority. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design_v1_patch_FIXED_FREEZE_HINT.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/candidate_v0_offline_lexical_scorer/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/candidate_v0_offline_lexical_scorer/candidate_v0_offline_lexical_scorer_design.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/candidate_v0_offline_lexical_scorer/candidate_v0_offline_lexical_scorer_design_spec.json`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_gold_set_assembly.py`
- `tests/test_routing_signal_scorer_v3_adviser_human_reviewed_approval_records.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_gold_set_gate.py`
- `tests/test_routing_signal_scorer_v3_adviser_human_review_draft_teacher_answers.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_case_corpus.py`
- `tests/test_routing_signal_scorer_v3_adviser_gold_manifest_run_registry.py`
- `tests/test_routing_signal_scorer_v3_adviser_pure_comparison_harness.py`
- `tests/test_routing_signal_scorer_v3_adviser_severity_resource_limits.py`
- `tests/test_routing_signal_scorer_v3_adviser_contract_validator_output_guard.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_generator_candidate_human_decision_recording_patch_boundary_design.py`
- `tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py`
- `tests/test_freeze_hint_autofill_state_machine.py`

## generated files

- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/candidate_v0_offline_lexical_scorer/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/candidate_v0_offline_lexical_scorer/candidate_v0_offline_lexical_scorer_design.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/candidate_v0_offline_lexical_scorer/candidate_v0_offline_lexical_scorer_design_spec.json`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `M10 remains design-only for future Adviser Candidate v0 offline lexical scorer.`
- `M10 must not create candidate modules or candidate outputs.`
- `M10 must not execute candidate logic, ML, providers, embeddings, vector indexes, source scanning, prompt auto-loading, artifact IO, or runtime router integration.`
- `Future M11 candidate must be standard-library-only and pure over caller-supplied primitive inputs.`
- `Runtime router code must not import adviser_offline, candidate design, or seed gold data.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design_v1
CONTRACT_TEST_OK: adviser candidate v0 offline lexical scorer design, design-only lexical baseline boundary, no candidate module, no candidate outputs, no candidate execution, no ML execution, no runtime import/export, no prompt auto-loading, no artifact IO, no embeddings, no providers, no source scanning, no router authority, M0/M1/M2/M3/M4/M5/M6/M7/M8/M9/M9B/M9C adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_CANDIDATE_V0_OFFLINE_LEXICAL_SCORER_DESIGN_V1_VALIDATION_OK
```

## known warnings

['Design-only milestone.', 'No candidate scorer or candidate outputs were added.', 'No runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, scratch writer, registry writer, or router authority were added.', 'Future M11 implementation remains a separate governed milestone after M10 freeze.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer Design v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M11: Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T15:08:37Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
