---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-evaluation-runner-v1"
feature_title: "Routing Signal Scorer v3 Adviser Candidate v0 Evaluation Runner v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-evaluation-runner-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "M12 evaluation runner remains adviser-offline only and must not be imported/exported by runtime routing modules."
  - "M12 evaluation runner must remain standard-library-only and pure over caller-supplied seed-gold case dictionaries."
  - "M12 must not discover cases or read/write files"
  - "tests may load fixture files, but runner code must not."
  - "M12 must not perform source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration."
  - "M12 must not persist candidate outputs, create scratch writers, create registry writers, mutate gold sets, or write run records."
  - "M12 reports are in-memory advisory evidence only and must never grant router authority or final-route decisions."
  - "M12 must continue to guard candidate outputs with M3/M4 contract/resource/severity checks before counting comparison evidence."
  - "M12 promotion recommendation remains blocked or review-gated when mismatches, P0/P1 risks, guard failures, resource failures, or empty cases are present."
  - "M11 candidate remains the candidate implementation"
  - "M12 only evaluates it and does not change candidate routing behavior."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-evaluation-runner-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-evaluation-runner-v1`

Feature title: `Routing Signal Scorer v3 Adviser Candidate v0 Evaluation Runner v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_evaluation_runner_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M12 implements a pure in-memory offline evaluation runner for Adviser Candidate v0. It evaluates caller-supplied seed-gold case dictionaries by calling the M11 lexical candidate, applying M3/M4 guard/resource/severity checks, and returning a structured report for human review. It adds no file IO, case discovery, source scanning, prompt auto-loading, artifact IO, candidate output persistence, scratch writer, registry writer, ML execution, embeddings, providers, runtime integration, or router authority. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/candidate_v0_evaluation_runner.py`
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
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/candidate_v0_evaluation_runner.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `M12 evaluation runner remains adviser-offline only and must not be imported/exported by runtime routing modules.`
- `M12 evaluation runner must remain standard-library-only and pure over caller-supplied seed-gold case dictionaries.`
- `M12 must not discover cases or read/write files`
- `tests may load fixture files, but runner code must not.`
- `M12 must not perform source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration.`
- `M12 must not persist candidate outputs, create scratch writers, create registry writers, mutate gold sets, or write run records.`
- `M12 reports are in-memory advisory evidence only and must never grant router authority or final-route decisions.`
- `M12 must continue to guard candidate outputs with M3/M4 contract/resource/severity checks before counting comparison evidence.`
- `M12 promotion recommendation remains blocked or review-gated when mismatches, P0/P1 risks, guard failures, resource failures, or empty cases are present.`
- `M11 candidate remains the candidate implementation`
- `M12 only evaluates it and does not change candidate routing behavior.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1
CONTRACT_TEST_OK: adviser candidate v0 evaluation runner, standard-library-only pure in-memory evaluation over caller-supplied seed-gold cases, candidate outputs guarded by M3/M4 checks, no file IO, no case discovery, no source scanning, no prompt auto-loading, no artifact IO, no candidate output persistence, no scratch writer, no registry writer, no ML execution, no embeddings, no providers, no runtime import/export, no router authority, M0/M1/M2/M3/M4/M5/M6/M7/M8/M9/M9B/M9C/M10/M11 adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_CANDIDATE_V0_EVALUATION_RUNNER_V1_VALIDATION_OK
```

## known warnings

['First evaluation-runner milestone; it returns in-memory reports only and does not persist candidate outputs or run records.', 'The M11 lexical baseline is expected to show mismatches against seed gold; M12 reports those mismatches for review instead of promoting the candidate.', 'No candidate registry writer, active review queue, promotion gate, shadow mode, Assistant behavior, or Copilot behavior is added.', 'Earlier regression tests were updated only to allow the exact M12 evaluation module while preserving no-output/no-runtime boundaries.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Candidate v0 Evaluation Runner v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M13: Routing Signal Scorer v3 Adviser Active Review Queue v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T16:23:43Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
