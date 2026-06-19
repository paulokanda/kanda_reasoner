---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-active-review-queue-v1"
feature_title: "Routing Signal Scorer v3 Adviser Active Review Queue v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-active-review-queue-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "M13 active review queue remains adviser-offline only and must not be imported/exported by runtime routing modules."
  - "M13 active review queue must remain standard-library-only and pure over caller-supplied evaluation report dictionaries."
  - "M13 must not discover cases or read/write files"
  - "tests may load fixtures, but queue code must not."
  - "M13 must not perform source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration."
  - "M13 must not persist queue items, candidate outputs, create scratch writers, create registry writers, mutate gold sets, or write run records."
  - "M13 queues are in-memory advisory evidence only and must never grant router authority, candidate promotion, or final-route decisions."
  - "M13 must keep every queue item human-review queued, promotion-blocked, and non-mutating until a later governed review decision milestone."
  - "M12 remains the evaluation runner"
  - "M13 only queues its supplied report and does not change candidate or evaluation behavior."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-active-review-queue-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-active-review-queue-v1`

Feature title: `Routing Signal Scorer v3 Adviser Active Review Queue v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_active_review_queue_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M13 implements a pure in-memory active review queue builder for M12 evaluation reports. It prioritizes caller-supplied evaluation results for human review and returns queue dictionaries only. It adds no file IO, case discovery, source scanning, prompt auto-loading, artifact IO, queue persistence, candidate output persistence, scratch writer, registry writer, gold mutation, ML execution, embeddings, providers, runtime integration, or router authority. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_active_review_queue_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/active_review_queue.py`
- `tests/test_routing_signal_scorer_v3_adviser_active_review_queue.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer.py`
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

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/active_review_queue.py`
- `tests/test_routing_signal_scorer_v3_adviser_active_review_queue.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `M13 active review queue remains adviser-offline only and must not be imported/exported by runtime routing modules.`
- `M13 active review queue must remain standard-library-only and pure over caller-supplied evaluation report dictionaries.`
- `M13 must not discover cases or read/write files`
- `tests may load fixtures, but queue code must not.`
- `M13 must not perform source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration.`
- `M13 must not persist queue items, candidate outputs, create scratch writers, create registry writers, mutate gold sets, or write run records.`
- `M13 queues are in-memory advisory evidence only and must never grant router authority, candidate promotion, or final-route decisions.`
- `M13 must keep every queue item human-review queued, promotion-blocked, and non-mutating until a later governed review decision milestone.`
- `M12 remains the evaluation runner`
- `M13 only queues its supplied report and does not change candidate or evaluation behavior.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_active_review_queue_v1
CONTRACT_TEST_OK: adviser active review queue, standard-library-only pure in-memory queue over caller-supplied evaluation reports, queue items remain human-review queued and promotion-blocked, no file IO, no case discovery, no source scanning, no prompt auto-loading, no artifact IO, no queue persistence, no candidate output persistence, no scratch writer, no registry writer, no gold mutation, no ML execution, no embeddings, no providers, no runtime import/export, no router authority, M0/M1/M2/M3/M4/M5/M6/M7/M8/M9/M9B/M9C/M10/M11/M12 adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_ACTIVE_REVIEW_QUEUE_V1_VALIDATION_OK
```

## known warnings

['First active review queue milestone; it returns in-memory queue dictionaries only and does not persist queue items or run records.', 'The queue does not approve, override, reject, promote, or mutate gold/candidate data; it only prioritizes review evidence for later human decision records.', 'No candidate registry writer, promotion gate, shadow mode, Assistant behavior, or Copilot behavior is added.', 'Earlier regression tests were updated only to allow the exact M13 review queue module while preserving no-output/no-runtime boundaries.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Active Review Queue v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M14: Routing Signal Scorer v3 Adviser Candidate Registry v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T16:28:36Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
