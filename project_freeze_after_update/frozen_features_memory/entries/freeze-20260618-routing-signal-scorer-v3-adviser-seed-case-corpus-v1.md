---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-seed-case-corpus-v1"
feature_title: "Routing Signal Scorer v3 Adviser Seed Case Corpus v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-seed-case-corpus-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Adviser M7 remains seed input case corpus only."
  - "M7 seed cases are not gold cases and must remain human_review_status seed_unreviewed."
  - "M7 must not add teacher answers, candidate outputs, reviewed gold sets, scratch reports, or registry files."
  - "M7 must not execute a candidate scorer or create candidate outputs."
  - "No ML execution, runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, or router authority are added by this milestone."
  - "Seed cases must not be loaded by runtime router code."
  - "Runtime router code must not import adviser_offline."
  - "adviser_offline test_data must not import runtime router code."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-seed-case-corpus-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-seed-case-corpus-v1`

Feature title: `Routing Signal Scorer v3 Adviser Seed Case Corpus v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_seed_case_corpus_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M7 adds seed input cases only. It does not create gold cases, teacher answers, candidate outputs, or any runtime behavior. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_seed_case_corpus_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/seed_case_corpus_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/seed_cases_v1.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/adversarial_bypass_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/ambiguous_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/box_boundary_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/false_positive_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/freeze_workflow_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/out_of_scope_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/patch_delivery_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/prompt_library_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/routing_signal_scorer_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/startup_delivery_cases.jsonl`
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

- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/seed_case_corpus_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/seed_cases_v1.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/adversarial_bypass_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/ambiguous_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/box_boundary_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/false_positive_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/freeze_workflow_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/out_of_scope_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/patch_delivery_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/prompt_library_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/routing_signal_scorer_cases.jsonl`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/input_cases/startup_delivery_cases.jsonl`
- `tests/test_routing_signal_scorer_v3_adviser_seed_case_corpus.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Adviser M7 remains seed input case corpus only.`
- `M7 seed cases are not gold cases and must remain human_review_status seed_unreviewed.`
- `M7 must not add teacher answers, candidate outputs, reviewed gold sets, scratch reports, or registry files.`
- `M7 must not execute a candidate scorer or create candidate outputs.`
- `No ML execution, runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, or router authority are added by this milestone.`
- `Seed cases must not be loaded by runtime router code.`
- `Runtime router code must not import adviser_offline.`
- `adviser_offline test_data must not import runtime router code.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_seed_case_corpus_v1
CONTRACT_TEST_OK: adviser seed case corpus, 50 synthetic seed input cases only, no gold set, no teacher answers, no candidate outputs, no candidate scorer, no ML execution, no runtime import/export, no prompt auto-loading, no artifact IO, no embeddings, no providers, M0/M1/M2/M3/M4/M5/M6 adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_SEED_CASE_CORPUS_V1_VALIDATION_OK
```

## known warnings

['Seed corpus milestone only.', 'Cases are synthetic seed input cases and remain seed_unreviewed, not gold.', 'No teacher answers were added.', 'No candidate outputs or candidate scorer were added.', 'No gold set, scratch writer, registry writer, runtime integration, ML execution, embeddings, providers, prompt auto-loading, artifact IO, source scanning, or router authority were added.', 'M0/M1/M2/M3/M4/M5/M6 tests were updated only to allow the new M7 test_data/input_cases seed corpus while preserving no-candidate/no-runtime/no-gold restrictions.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Seed Case Corpus v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M8: Routing Signal Scorer v3 Adviser Human Review Record and Draft Teacher Answers v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T12:50:55Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
