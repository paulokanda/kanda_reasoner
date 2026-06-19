---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-gold-set-expansion-plan-v1"
feature_title: "Routing Signal Scorer v3 Adviser Gold Set Expansion Plan v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-gold-set-expansion-plan-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "M15 gold set expansion plan remains adviser-offline only and must not be imported/exported by runtime routing modules."
  - "M15 expansion plan must remain standard-library-only and pure over caller-supplied current gold, evaluation, review queue, registry, and policy dictionaries."
  - "M15 must not discover cases or read/write files"
  - "tests may load fixtures, but expansion-plan code must not."
  - "M15 must not create gold cases, approve cases, mutate gold sets, or mark any item as gold-ready."
  - "M15 must not perform source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration."
  - "M15 must not persist plans, persist registry records, persist candidate outputs, create scratch writers, create registry writers, mutate gold sets, or write run records."
  - "M15 plans are in-memory advisory evidence only and must never grant router authority, candidate promotion, or final-route decisions."
  - "Every M15 plan item must remain planned-only, human-review-required, and future-governed-patch-required."
  - "M14 remains the candidate registry"
  - "M15 only plans future gold expansion and does not change candidate, evaluation, queue, registry, or gold behavior."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-gold-set-expansion-plan-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-gold-set-expansion-plan-v1`

Feature title: `Routing Signal Scorer v3 Adviser Gold Set Expansion Plan v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_gold_set_expansion_plan_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M15 implements a pure in-memory gold set expansion planning helper for the Adviser seed-gold workflow. It builds deterministic advisory expansion plans from caller-supplied current gold summaries, M12 evaluation summaries, M13 review queue summaries, and M14 candidate registry summaries. It adds no new gold cases, no gold mutation, no file IO, no case discovery, no source scanning, no prompt auto-loading, no artifact IO, no plan persistence, no registry writer, no candidate output persistence, no scratch writer, no ML execution, no embeddings, no providers, no runtime integration, and no router authority. All plan items require future human review and a separate governed gold patch. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_gold_set_expansion_plan_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/gold_set_expansion_plan.py`
- `tests/test_routing_signal_scorer_v3_adviser_gold_set_expansion_plan.py`
- `tests/test_routing_signal_scorer_v3_adviser_candidate_registry.py`
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
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/gold_set_expansion_plan.py`
- `tests/test_routing_signal_scorer_v3_adviser_gold_set_expansion_plan.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `M15 gold set expansion plan remains adviser-offline only and must not be imported/exported by runtime routing modules.`
- `M15 expansion plan must remain standard-library-only and pure over caller-supplied current gold, evaluation, review queue, registry, and policy dictionaries.`
- `M15 must not discover cases or read/write files`
- `tests may load fixtures, but expansion-plan code must not.`
- `M15 must not create gold cases, approve cases, mutate gold sets, or mark any item as gold-ready.`
- `M15 must not perform source scanning, prompt auto-loading, artifact IO, provider calls, embeddings, vector indexing, dependency installation, network calls, or runtime integration.`
- `M15 must not persist plans, persist registry records, persist candidate outputs, create scratch writers, create registry writers, mutate gold sets, or write run records.`
- `M15 plans are in-memory advisory evidence only and must never grant router authority, candidate promotion, or final-route decisions.`
- `Every M15 plan item must remain planned-only, human-review-required, and future-governed-patch-required.`
- `M14 remains the candidate registry`
- `M15 only plans future gold expansion and does not change candidate, evaluation, queue, registry, or gold behavior.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_gold_set_expansion_plan_v1
CONTRACT_TEST_OK: adviser gold set expansion plan, standard-library-only pure in-memory expansion plan over caller-supplied gold/evaluation/review queue/registry summaries, no new gold cases, no gold mutation, no file IO, no case discovery, no source scanning, no prompt auto-loading, no artifact IO, no plan persistence, no registry writer, no candidate output persistence, no scratch writer, no ML execution, no embeddings, no providers, no runtime import/export, no router authority, M0/M1/M2/M3/M4/M5/M6/M7/M8/M9/M9B/M9C/M10/M11/M12/M13/M14 adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_GOLD_SET_EXPANSION_PLAN_V1_VALIDATION_OK
```

## known warnings

['First gold expansion planning milestone; it returns in-memory plan dictionaries only and does not add gold cases or persist plans.', 'The plan does not approve, override, reject, promote, mutate gold/candidate data, or grant runtime authority.', 'No promotion gate, shadow mode, Assistant behavior, or Copilot behavior is added.', 'Earlier regression tests were updated only to allow the exact M15 gold expansion plan module while preserving no-output/no-runtime/no-gold-mutation boundaries.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Gold Set Expansion Plan v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M16: Routing Signal Scorer v3 Adviser Promotion Criteria Gate v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T17:04:31Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
