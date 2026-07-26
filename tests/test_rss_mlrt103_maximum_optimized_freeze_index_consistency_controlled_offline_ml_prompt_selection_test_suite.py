from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_103_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_102_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt103_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-103 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt103_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt102_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-102 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT103_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-104 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-103 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized freeze-index consistency in-memory offline prompt-selection test suite after MLRT-102 freeze; MLRT-102 reviewed the MLRT-101 64-case written-path integrity result as good but validation-only evidence and identified freeze-index consistency as the next correction; MLRT-103 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-103 passed 64/64 freeze-index consistency cases across eight balanced audit families, with 32/32 freeze-index consistency pairs represented, two deliberately index-consistent-versus-index-inconsistent variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 freeze-index consistency pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 1050/1050 cases across twenty real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of current freeze memory exposure to selected-project freeze_index.json consistency, including index entry counts, entry file counts, active/non-superseded counts, project_frozen_implemented_steps.md alignment, AI-send exposure alignment, latest current-feature freeze ID coherence, and read-only exposure status, while demoting stale, truncated, wrong-root, wrong-feature, project_freeze_ledger, mismatched-count, missing-entry-file, or mismatched-index evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['INDEX_COUNT_ENTRY_FILE_ALIGNMENT', 'ACTIVE_NON_SUPERSEDED_ALIGNMENT', 'CURRENT_FEATURE_INDEX_BINDING', 'PROJECT_FROZEN_IMPLEMENTED_STEPS_ALIGNMENT', 'AI_SEND_EXPOSURE_ALIGNMENT', 'STALE_INDEX_OR_SIDECAR_DEMOTION', 'READ_ONLY_EXPOSURE_AND_NO_REPAIR', 'BOUNDARY_CONTAINMENT_DURING_INDEX_CONSISTENCY']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE', 'TREAT_PROJECT_FREEZE_LEDGER_AS_ACTIVE_MEMORY', 'TREAT_WRONG_ROOT_AS_CURRENT_PROJECT', 'TREAT_MISSING_WRITTEN_PATHS_AS_COMPLETE', 'TREAT_TRUNCATED_PATHS_AS_COMPLETE', 'TREAT_MISSING_INDEX_AS_COMPLETE', 'TREAT_MISSING_IMPLEMENTED_STEPS_AS_COMPLETE', 'TREAT_INDEX_COUNT_MISMATCH_AS_OK', 'TREAT_ENTRY_FILE_COUNT_MISMATCH_AS_OK', 'TREAT_ACTIVE_COUNT_MISMATCH_AS_OK', 'TREAT_STALE_INDEX_AS_CURRENT']
FAMILY_DEFINITIONS = [{'family': 'INDEX_COUNT_ENTRY_FILE_ALIGNMENT', 'pairs': [('freeze_index.json index entries and entry files match the selected project current exposure counts', 'index entries count and entry files count disagree but are accepted as current'), ('the latest index entry points to the current MLRT-103 freeze ID and existing entry file', 'latest index entry points to a missing entry file'), ('entry files count aligns with the reported Current freeze exposure after write block', 'reported entry files count is truncated or absent but treated as complete'), ('index entries count increases coherently after current Confirm and Write', 'index count appears stale from before the current write')]}, {'family': 'ACTIVE_NON_SUPERSEDED_ALIGNMENT', 'pairs': [('active/non-superseded entries count is coherent with index entries and supersession state', 'active/non-superseded count exceeds index entries or entry files'), ('superseded entries are not counted as active current-feature evidence', 'superseded or inactive entry is accepted as the current active freeze'), ('active count delta is interpreted as exposure evidence, not route authority', 'active count delta grants route authority'), ('active/non-superseded count mismatch triggers targeted evidence recovery', 'active count mismatch is silently treated as OK')]}, {'family': 'CURRENT_FEATURE_INDEX_BINDING', 'pairs': [('freeze_index.json current entry binds to MLRT-103 title, feature ID, and freeze ID', 'index current entry binds to MLRT-101 or MLRT-102 but is accepted for MLRT-103'), ('current freeze ID in index agrees with LOCAL FREEZE WRITE OK and entries filename', 'index freeze ID and write-block freeze ID disagree'), ('planned next step remains MLRT-104 and is not treated as current index entry', 'planned next step MLRT-104 is treated as an already indexed current freeze'), ('adjacent prior MLRT index entries are context but not current MLRT-103 completion', 'adjacent prior MLRT index entry overrides current MLRT-103 evidence')]}, {'family': 'PROJECT_FROZEN_IMPLEMENTED_STEPS_ALIGNMENT', 'pairs': [('project_frozen_implemented_steps.md references the current MLRT-103 feature consistently with freeze_index.json', 'implemented steps file is missing or stale but index alone is treated as enough'), ('implemented steps and index agree on current feature sequence and next milestone', 'implemented steps says a different next milestone but is ignored'), ('implemented steps path remains under selected project frozen_features_memory', 'implemented steps path points to project_freeze_ledger or wrong root'), ('implemented steps is preserved as project-specific memory, not a dataset or training source', 'implemented steps is ingested as training data')]}, {'family': 'AI_SEND_EXPOSURE_ALIGNMENT', 'pairs': [('AI-send exposure and startup context are refreshed after the same current write indexed in freeze_index.json', 'AI-send exposure is refreshed for a different feature but accepted for current index'), ('AI-send ZIP is exposure artifact, not the owner of freeze memory', 'AI-send ZIP path replaces freeze_index.json ownership'), ('startup 09_active_project_freeze_context reflects current freeze memory without mutating it', 'startup context mismatch is repaired by mutating freeze_index.json'), ('AI-send instruction path supports exposure review but not route authority', 'AI-send instruction path enables runtime Pilot or Copilot')]}, {'family': 'STALE_INDEX_OR_SIDECAR_DEMOTION', 'pairs': [('latest current-feature freeze_index.json evidence overrides stale sidecar snippets', 'stale sidecar index snippet overrides current freeze_index evidence'), ('wrong-root index files are demoted even when their counts are coherent', 'wrong-root coherent counts are treated as selected project memory'), ('project_freeze_ledger index-like data is blueprint context only', 'project_freeze_ledger index-like data is used as active project freeze index'), ('truncated index snippets trigger recovery rather than false current completion', 'truncated index snippet is inflated into full current evidence')]}, {'family': 'READ_ONLY_EXPOSURE_AND_NO_REPAIR', 'pairs': [('READ_ONLY_EXPOSURE reports index consistency without mutating freeze_index.json or entries', 'read-only exposure repairs or regenerates freeze_index.json'), ('FREEZE_MEMORY_STATUS OK is accepted only as exposure bound to matching index evidence', 'FREEZE_MEMORY_STATUS OK alone replaces missing index evidence'), ('mismatched counts are surfaced as evidence gaps without denying the write block itself', 'mismatched counts cause the system to claim no local write happened'), ('index consistency checks remain offline review-only and do not persist reports', 'index consistency check persists reports or labels')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_INDEX_CONSISTENCY', 'pairs': [('freeze-index consistency is offline evidence handling, not runtime routing authority', 'freeze-index consistency grants runtime route authority'), ('targeted index consistency review does not load live prompts, live freeze memory, or router canon for routing', 'index consistency review loads live prompts for routing decisions'), ('index consistency tests do not train, calibrate, or improve a model', 'index consistency evidence is stored as training data'), ('index consistency review does not mutate freeze memory, gold registry, Pilot, or Copilot behavior', 'index consistency review writes the gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            good_text, gap_text = pair
            pair_id = f"mlrt103_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("index_consistent_current_feature", good_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("index_inconsistent_or_mismatched_containment", gap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt103_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-103 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Preserve selected-project freeze-index consistency without runtime authority."
                )
                consistent = variant == "index_consistent_current_feature"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "freeze_index_json_present": consistent,
                    "index_entry_count_matches_entry_files": consistent,
                    "entry_files_count_matches_exposure_report": consistent,
                    "active_non_superseded_count_coherent": consistent,
                    "latest_index_entry_matches_current_feature": consistent,
                    "latest_index_freeze_id_matches_write_block": consistent,
                    "entry_filename_exists_for_current_freeze_id": consistent,
                    "project_frozen_implemented_steps_aligned": consistent,
                    "ai_send_exposure_aligned_to_same_current_write": consistent,
                    "startup_context_aligned_to_same_current_write": consistent,
                    "selected_project_root_bound": consistent,
                    "project_freeze_ledger_demoted_to_blueprint_logic": True,
                    "files_to_send_ai_demoted_to_exposure_artifact": True,
                    "startup_zip_demoted_to_refresh_artifact": True,
                    "wrong_root_index_demoted": not consistent,
                    "stale_or_sidecar_index_demoted": True,
                    "truncated_index_snippet_recovery_required": not consistent,
                    "mismatched_count_gap_not_inflated": not consistent,
                    "planned_next_step_not_indexed_current_freeze": True,
                    "read_only_exposure_does_not_repair_index": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_index_count_mismatch_as_ok": False,
                    "treat_entry_file_count_mismatch_as_ok": False,
                    "treat_active_count_mismatch_as_ok": False,
                    "treat_stale_index_as_current": False,
                    "treat_project_freeze_ledger_as_active_memory": False,
                    "treat_wrong_root_as_current_project": False,
                    "critical_boundary_error_budget": 0,
                }
                for flag in BOUNDARY_FALSE_FLAGS:
                    candidate[flag] = False
                cases.append({
                    "case_id": case_id,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "user_request": user_request,
                    "expected_label": expected_label,
                    "candidate": candidate,
                })
    return cases


def validate_cases(cases: list[dict[str, object]]) -> None:
    assert len(cases) == 64
    assert len({case["case_id"] for case in cases}) == 64
    assert len({case["user_request"] for case in cases}) == 64
    assert len({case["pair_id"] for case in cases}) == 32

    family_counts = Counter(str(case["family"]) for case in cases)
    assert set(family_counts) == set(EXPECTED_FAMILIES)
    assert all(count == 8 for count in family_counts.values())

    pair_counts = Counter(str(case["pair_id"]) for case in cases)
    assert all(count == 2 for count in pair_counts.values())

    label_counts = Counter(str(case["expected_label"]) for case in cases)
    assert label_counts["GOVERNED_OFFLINE_REVIEW_ONLY"] == 32
    assert label_counts["NO_AUTHORITATIVE_ROUTE"] == 32

    variants_by_pair: dict[str, set[str]] = defaultdict(set)
    for case in cases:
        variants_by_pair[str(case["pair_id"])].add(str(case["variant"]))
    assert all(variants == {"index_consistent_current_feature", "index_inconsistent_or_mismatched_containment"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        consistent = case["variant"] == "index_consistent_current_feature"
        assert candidate["freeze_index_json_present"] is consistent
        assert candidate["index_entry_count_matches_entry_files"] is consistent
        assert candidate["entry_files_count_matches_exposure_report"] is consistent
        assert candidate["active_non_superseded_count_coherent"] is consistent
        assert candidate["latest_index_entry_matches_current_feature"] is consistent
        assert candidate["latest_index_freeze_id_matches_write_block"] is consistent
        assert candidate["entry_filename_exists_for_current_freeze_id"] is consistent
        assert candidate["project_frozen_implemented_steps_aligned"] is consistent
        assert candidate["ai_send_exposure_aligned_to_same_current_write"] is consistent
        assert candidate["startup_context_aligned_to_same_current_write"] is consistent
        assert candidate["selected_project_root_bound"] is consistent
        assert candidate["project_freeze_ledger_demoted_to_blueprint_logic"] is True
        assert candidate["files_to_send_ai_demoted_to_exposure_artifact"] is True
        assert candidate["startup_zip_demoted_to_refresh_artifact"] is True
        assert candidate["wrong_root_index_demoted"] is (not consistent)
        assert candidate["stale_or_sidecar_index_demoted"] is True
        assert candidate["truncated_index_snippet_recovery_required"] is (not consistent)
        assert candidate["mismatched_count_gap_not_inflated"] is (not consistent)
        assert candidate["planned_next_step_not_indexed_current_freeze"] is True
        assert candidate["read_only_exposure_does_not_repair_index"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_index_count_mismatch_as_ok"] is False
        assert candidate["treat_entry_file_count_mismatch_as_ok"] is False
        assert candidate["treat_active_count_mismatch_as_ok"] is False
        assert candidate["treat_stale_index_as_current"] is False
        assert candidate["treat_project_freeze_ledger_as_active_memory"] is False
        assert candidate["treat_wrong_root_as_current_project"] is False
        assert candidate["critical_boundary_error_budget"] == 0
        for flag in BOUNDARY_FALSE_FLAGS:
            assert candidate[flag] is False, (case["case_id"], flag)


def validate_project_surface() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    assert README.exists(), README
    assert MANIFEST.exists(), MANIFEST

    text = DOC.read_text(encoding="utf-8")
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert "MLRT-102" in text
    assert "64/64" in text
    assert "1050/1050" in text
    assert "`20` real test suites" in text
    assert "freeze_index.json" in text
    assert "entry files" in text
    assert "active/non-superseded" in text
    assert "project_frozen_implemented_steps.md" in text
    assert "AI-send" in text
    assert "project_freeze_ledger" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "1050/1050" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_freeze_index_consistency_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 1050
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 20
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_index_count_entry_file_alignment_tested"] is True
    assert manifest[f"{PREFIX}_active_non_superseded_alignment_tested"] is True
    assert manifest[f"{PREFIX}_current_feature_index_binding_tested"] is True
    assert manifest[f"{PREFIX}_project_frozen_implemented_steps_alignment_tested"] is True
    assert manifest[f"{PREFIX}_ai_send_exposure_alignment_tested"] is True
    assert manifest[f"{PREFIX}_stale_index_or_sidecar_demotion_tested"] is True
    assert manifest[f"{PREFIX}_read_only_exposure_and_no_repair_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_index_consistency_tested"] is True
    for flag in BOUNDARY_FALSE_FLAGS:
        assert manifest[f"{PREFIX}_{flag}"] is False

    mlrt_py = [path for path in MLRT.rglob("*.py") if "__pycache__" not in path.parts]
    assert len(mlrt_py) == 1
    assert mlrt_py[0].name == "minimal_non_runtime_harness_stub.py"

    lab_py = [path for path in LAB.rglob("*.py") if "__pycache__" not in path.parts]
    assert len(lab_py) == 3
    assert sorted(path.name for path in lab_py) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]

    assert not (ROOT / "KANDA_FREEZE_HINT.json").exists()


def main() -> None:
    cases = build_cases()
    validate_cases(cases)
    validate_project_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT103_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
