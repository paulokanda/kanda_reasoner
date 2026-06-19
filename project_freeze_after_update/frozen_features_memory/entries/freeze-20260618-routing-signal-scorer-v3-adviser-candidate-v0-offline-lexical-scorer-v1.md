---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-v1"
feature_title: "Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "M11 candidate remains adviser-offline only and must not be imported/exported by runtime routing modules."
  - "M11 candidate must remain standard-library-only and pure over caller-supplied primitive input."
  - "M11 candidate must not perform file IO, source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration."
  - "M11 candidate must not persist candidate outputs, create scratch writers, create registry writers, or mutate gold sets."
  - "M11 candidate output remains advisory evidence only and must never grant router authority or final-route decisions."
  - "M11 candidate must never emit unsafe proceed values such as YES, YES_UNCONDITIONAL, PROCEED, or AUTO_PROCEED."
  - "Ambiguous short commands such as continue/go/ok/next must abstain unless separately governed context proves the next safe milestone."
  - "Critical bypass, authority-promotion, prompt-auto-loading, startup-bypass, prompt-library-bypass, freeze-bypass, and box-invasion patterns must recommend NO/ABSTAIN/UNKNOWN, never action."
  - "Candidate outputs must continue to pass M3 contract/output guard and M4 resource/severity checks before any future offline comparison trust."
  - "M10 remains design-only history"
  - "M11 is the separate governed milestone that allows the exact offline candidate module while still forbidding runtime behavior and candidate output persistence."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-v1`

Feature title: `Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_candidate_v0_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M11 implements the first offline deterministic lexical Adviser Candidate v0. It is standard-library-only and pure over caller-supplied primitive input. It returns advisory candidate-answer dictionaries for offline comparison only and adds no candidate output persistence, file IO, source scanning, prompt auto-loading, artifact IO, embeddings, providers, ML execution, runtime integration, or router authority. The patch also updates earlier regression tests so frozen design-only milestones can coexist with this separately governed M11 implementation while preserving their no-runtime/no-output boundaries. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/offline_lexical_scorer.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_gold_set_gate.py`
- `tests/test_routing_signal_scorer_v3_adviser_human_reviewed_approval_records.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_case_corpus.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_human_review_draft_teacher_answers.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_gold_set_assembly.py`
- `tests/test_routing_signal_scorer_v3_adviser_gold_manifest_run_registry.py`
- `tests/test_routing_signal_scorer_v3_adviser_pure_comparison_harness.py`
- `tests/test_routing_signal_scorer_v3_adviser_severity_resource_limits.py`
- `tests/test_routing_signal_scorer_v3_adviser_contract_validator_output_guard.py`
- `tests/test_routing_signal_scorer_v3_generator_candidate_human_decision_recording_patch_boundary_design.py`
- `tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py`
- `tests/test_freeze_hint_autofill_state_machine.py`

## generated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/offline_lexical_scorer.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_gold_set_gate.py`
- `tests/test_routing_signal_scorer_v3_adviser_human_reviewed_approval_records.py`
- `tests/test_routing_signal_scorer_v3_adviser_seed_case_corpus.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_human_review_draft_teacher_answers.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `M11 candidate remains adviser-offline only and must not be imported/exported by runtime routing modules.`
- `M11 candidate must remain standard-library-only and pure over caller-supplied primitive input.`
- `M11 candidate must not perform file IO, source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration.`
- `M11 candidate must not persist candidate outputs, create scratch writers, create registry writers, or mutate gold sets.`
- `M11 candidate output remains advisory evidence only and must never grant router authority or final-route decisions.`
- `M11 candidate must never emit unsafe proceed values such as YES, YES_UNCONDITIONAL, PROCEED, or AUTO_PROCEED.`
- `Ambiguous short commands such as continue/go/ok/next must abstain unless separately governed context proves the next safe milestone.`
- `Critical bypass, authority-promotion, prompt-auto-loading, startup-bypass, prompt-library-bypass, freeze-bypass, and box-invasion patterns must recommend NO/ABSTAIN/UNKNOWN, never action.`
- `Candidate outputs must continue to pass M3 contract/output guard and M4 resource/severity checks before any future offline comparison trust.`
- `M10 remains design-only history`
- `M11 is the separate governed milestone that allows the exact offline candidate module while still forbidding runtime behavior and candidate output persistence.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_v1
CONTRACT_TEST_OK: adviser candidate v0 offline lexical scorer, standard-library-only pure lexical baseline, no file IO, no source scanning, no prompt auto-loading, no candidate output persistence, no scratch writer, no registry writer, no ML execution, no embeddings, no providers, no runtime import/export, no router authority, candidate outputs pass M3/M4 contract guard resource checks in tests, M0/M1/M2/M3/M4/M5/M6/M7/M8/M9/M9B/M9C/M10 adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_CANDIDATE_V0_OFFLINE_LEXICAL_SCORER_V1_VALIDATION_OK
```

## known warnings

['First candidate implementation milestone; still deterministic lexical baseline, not ML/provider-based scoring.', 'No evaluation runner, candidate registry writer, active review queue, promotion gate, shadow mode, Assistant behavior, or Copilot behavior is added.', 'Earlier regression tests were updated only to allow the exact M11 candidate module and to repair stale syntax/false-positive assertions while preserving no-output/no-runtime boundaries.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M12: Routing Signal Scorer v3 Adviser Candidate v0 Evaluation Runner v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T16:13:58Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
