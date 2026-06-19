---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-seed-gold-set-assembly-v1"
feature_title: "Routing Signal Scorer v3 Adviser Seed Gold Set Assembly v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-seed-gold-set-assembly-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "M9C creates static offline seed gold cases only from M9B human-reviewed records."
  - "M9C must not create candidate outputs or a candidate scorer."
  - "M9C must not execute ML, install dependencies, call providers, create embeddings, create vector indexes, scan source trees, auto-load prompts, or integrate with runtime routing."
  - "Seed gold cases are expected answers for future offline evaluation, not router authority."
  - "Runtime router code must not import adviser_offline or seed gold data."
  - "The M9B cross-cutting governance-path note remains preserved and must not be converted into a fake ninth case-level override."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-seed-gold-set-assembly-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-seed-gold-set-assembly-v1`

Feature title: `Routing Signal Scorer v3 Adviser Seed Gold Set Assembly v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_static_seed_gold_set_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M9C assembles a static offline seed gold set from M9B human-reviewed approval/override records. It creates 50 seed gold cases and a manifest only; no candidate scorer, ML execution, runtime integration, prompt auto-loading, artifact IO, embeddings, providers, or router authority. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_seed_gold_set_assembly_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_set_assembly_notes.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_set_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_manifest_m6_compatible.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_cases_v1.jsonl`
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

- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/README.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_set_assembly_notes.md`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_set_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_manifest_m6_compatible.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/test_data/gold_set/seed_gold_set_v1/seed_gold_cases_v1.jsonl`
- `tests/test_routing_signal_scorer_v3_adviser_seed_gold_set_assembly.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `M9C creates static offline seed gold cases only from M9B human-reviewed records.`
- `M9C must not create candidate outputs or a candidate scorer.`
- `M9C must not execute ML, install dependencies, call providers, create embeddings, create vector indexes, scan source trees, auto-load prompts, or integrate with runtime routing.`
- `Seed gold cases are expected answers for future offline evaluation, not router authority.`
- `Runtime router code must not import adviser_offline or seed gold data.`
- `The M9B cross-cutting governance-path note remains preserved and must not be converted into a fake ninth case-level override.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_seed_gold_set_assembly_v1
CONTRACT_TEST_OK: adviser seed gold set assembly, 50 static offline seed gold cases assembled from M9B human-reviewed records, 42 approved case-level records, 8 overridden case-level records, 1 cross-cutting governance-path note preserved, 0 rejected, no candidate outputs, no candidate scorer, no ML execution, no runtime import/export, no prompt auto-loading, no artifact IO, no embeddings, no providers, M0/M1/M2/M3/M4/M5/M6/M7/M8/M9/M9B adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_SEED_GOLD_SET_ASSEMBLY_V1_VALIDATION_OK
```

## known warnings

['M9C creates a static seed gold set, but does not evaluate a candidate.', 'No candidate scorer or candidate outputs were added.', 'No runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, scratch writer, registry writer, or router authority were added.', 'Future candidate design remains a separate governed milestone.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Seed Gold Set Assembly v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M10: Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer Design v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T14:11:13Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
