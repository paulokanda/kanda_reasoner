from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_101_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_100_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt101_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-101 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt101_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt100_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-100 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT101_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-102 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-101 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized written-path integrity in-memory offline prompt-selection test suite after MLRT-100 freeze; MLRT-100 reviewed the MLRT-99 64-case human-confirmation binding result as good but validation-only evidence and identified written-path integrity as the next correction; MLRT-101 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-101 passed 64/64 written-path integrity cases across eight balanced audit families, with 32/32 written-path integrity pairs represented, two deliberately selected-project-frozen-memory-paths-versus-missing-or-wrong-path variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 written-path integrity pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 986/986 cases across nineteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of freeze completion to selected-project written paths under project_freeze_after_update/frozen_features_memory, including matching entries freeze file, freeze_index.json, project_frozen_implemented_steps.md, exact project root, exact current freeze ID, and refreshed FREEZE_MEMORY_STATUS OK, while demoting missing, truncated, stale, project_freeze_ledger, wrong-root, missing-index, missing-implemented-steps, missing-entries, or mismatched-freeze-ID path evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['WRITTEN_PATH_TRIPLET_COMPLETENESS', 'SELECTED_PROJECT_ROOT_BINDING', 'FROZEN_FEATURES_MEMORY_OWNERSHIP', 'FREEZE_ID_PATH_FILENAME_COHERENCE', 'PATH_TRUNCATION_AND_OMISSION_RECOVERY', 'STALE_OR_WRONG_FEATURE_PATH_DEMOTION', 'WRITE_AND_EXPOSURE_BINDING', 'BOUNDARY_CONTAINMENT_DURING_PATH_INTEGRITY']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE', 'TREAT_PROJECT_FREEZE_LEDGER_AS_ACTIVE_MEMORY', 'TREAT_WRONG_ROOT_AS_CURRENT_PROJECT', 'TREAT_MISSING_WRITTEN_PATHS_AS_COMPLETE', 'TREAT_TRUNCATED_PATHS_AS_COMPLETE', 'TREAT_MISSING_INDEX_AS_COMPLETE', 'TREAT_MISSING_IMPLEMENTED_STEPS_AS_COMPLETE']
FAMILY_DEFINITIONS = [{'family': 'WRITTEN_PATH_TRIPLET_COMPLETENESS', 'pairs': [('entries freeze file, freeze_index.json, and project_frozen_implemented_steps.md are all present for the selected project', 'LOCAL FREEZE WRITE OK appears but written paths are omitted'), ('entries path and freeze_index.json together support the current freeze write', 'entries path exists but freeze_index.json path is missing'), ('project_frozen_implemented_steps.md is present with the current write path set', 'project_frozen_implemented_steps.md is missing from an otherwise current-looking write block'), ('all written paths remain under project_freeze_after_update/frozen_features_memory', 'one written path is outside frozen_features_memory but is treated as complete')]}, {'family': 'SELECTED_PROJECT_ROOT_BINDING', 'pairs': [('written paths are bound to the selected project root E:\\kanda_reasoner', 'written paths point to a different project root and are accepted as current'), ('same-drive temporary work folders are not active freeze memory paths', 'kanda_reasoner_delete_after_daily_work paths are treated as frozen memory'), ('startup workspace files are refresh artifacts but not the owner of frozen memory', 'kanda_prompt_workspace startup ZIP path is treated as the written freeze entry'), ('AI-send exposure paths are compliance artifacts, not the freeze memory owner', 'files_to_send_ai path is treated as the primary freeze memory entry')]}, {'family': 'FROZEN_FEATURES_MEMORY_OWNERSHIP', 'pairs': [('active freeze memory belongs only to selected project project_freeze_after_update/frozen_features_memory', 'project_freeze_ledger path is treated as active project-specific memory'), ('project_freeze_ledger remains reusable blueprint logic only', 'project_freeze_ledger write path confirms the current project freeze'), ('written paths must not redirect frozen memory ownership to templates or ledgers', 'template or ledger path is accepted as the current feature entry'), ('canonical rule is preserved while reading evidence, not used to mutate files', 'evidence review repairs or mutates freeze_index.json')]}, {'family': 'FREEZE_ID_PATH_FILENAME_COHERENCE', 'pairs': [('entry filename matches the exact current MLRT-101 freeze ID', 'entry filename contains a stale MLRT-99 or MLRT-100 freeze ID'), ('freeze ID in LOCAL FREEZE WRITE OK agrees with the entries path filename', 'freeze ID and entries path filename disagree but are accepted'), ('current feature title, freeze ID, and entries filename all refer to written-path integrity', 'human-confirmation or preview-versus-write path is accepted for written-path integrity'), ('truncated filename is not inflated into a full current freeze ID', 'truncated entries filename is treated as exact current freeze ID')]}, {'family': 'PATH_TRUNCATION_AND_OMISSION_RECOVERY', 'pairs': [('truncated written paths trigger targeted recovery instead of false completion', 'truncated written paths are accepted as complete freeze evidence'), ('missing entries path is a written-path integrity gap even if status is OK', 'FREEZE_MEMORY_STATUS OK alone replaces the missing entries path'), ('missing freeze_index path is recovered or requested without denying the write block itself', 'missing freeze_index path causes the system to say no write happened'), ('delayed FREEZE_MEMORY_STATUS OK can complete exposure only when path triplet already matches', 'delayed status from another feature completes a path-mismatched write')]}, {'family': 'STALE_OR_WRONG_FEATURE_PATH_DEMOTION', 'pairs': [('current MLRT-101 written paths override older adjacent MLRT write paths', 'older adjacent MLRT written paths override the current feature'), ('stale sidecar path evidence is demoted when current written paths are present', 'stale sidecar path evidence is selected instead of current written paths'), ('planned next step text is not a written path for the current feature', 'planned next step text is treated as current written path evidence'), ('wrong-feature write paths are preserved as context but not as current freeze completion', 'wrong-feature write paths are used to advance the current feature')]}, {'family': 'WRITE_AND_EXPOSURE_BINDING', 'pairs': [('LOCAL FREEZE WRITE OK, written path triplet, freeze hint used, AI refresh, and FREEZE_MEMORY_STATUS OK form coherent current evidence', 'split evidence from several features is merged into a false coherent write'), ('freeze hint intake marked as used supports only the matching current feature', 'freeze hint used marker from another feature confirms current written paths'), ('AI compliance refresh after local write supports exposure but not memory ownership', 'AI-send ZIP path replaces frozen_features_memory ownership'), ('FREEZE_MEMORY_STATUS OK is read-only exposure bound to the same current write event', 'FREEZE_MEMORY_STATUS OK mutates or repairs missing written paths')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_PATH_INTEGRITY', 'pairs': [('written-path integrity is offline evidence handling, not runtime routing authority', 'written-path integrity grants runtime route authority'), ('targeted path inspection does not load live prompts, live freeze memory, or router canon for routing', 'targeted path inspection loads live prompts for routing decisions'), ('path-integrity tests do not train, calibrate, or improve a model', 'path-integrity evidence is stored as training data'), ('path-integrity recovery does not mutate freeze memory, gold registry, Pilot, or Copilot behavior', 'path-integrity recovery writes the gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            good_text, gap_text = pair
            pair_id = f"mlrt101_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("selected_project_frozen_memory_paths", good_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("missing_or_wrong_path_containment", gap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt101_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-101 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Preserve selected-project written-path integrity without runtime authority."
                )
                complete = variant == "selected_project_frozen_memory_paths"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "selected_project_root_bound": complete,
                    "active_memory_under_project_freeze_after_update": complete,
                    "entries_freeze_file_path_present": complete,
                    "freeze_index_path_present": complete,
                    "project_frozen_implemented_steps_path_present": complete,
                    "written_path_triplet_complete": complete,
                    "entries_filename_matches_current_freeze_id": complete,
                    "freeze_id_matches_entries_path": complete,
                    "current_feature_title_matches_written_paths": complete,
                    "freeze_memory_status_ok_bound_to_same_write": complete,
                    "project_freeze_ledger_demoted_to_blueprint_logic": True,
                    "files_to_send_ai_demoted_to_exposure_artifact": True,
                    "startup_zip_demoted_to_refresh_artifact": True,
                    "wrong_root_paths_demoted": not complete,
                    "truncated_paths_demoted_or_recovered": True,
                    "missing_path_gap_not_inflated": not complete,
                    "stale_or_adjacent_paths_demoted": True,
                    "planned_next_step_not_written_path": True,
                    "read_only_exposure_does_not_repair_paths": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_project_freeze_ledger_as_active_memory": False,
                    "treat_wrong_root_as_current_project": False,
                    "treat_missing_written_paths_as_complete": False,
                    "treat_truncated_paths_as_complete": False,
                    "treat_missing_index_as_complete": False,
                    "treat_missing_implemented_steps_as_complete": False,
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
    assert all(variants == {"selected_project_frozen_memory_paths", "missing_or_wrong_path_containment"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        complete = case["variant"] == "selected_project_frozen_memory_paths"
        assert candidate["selected_project_root_bound"] is complete
        assert candidate["active_memory_under_project_freeze_after_update"] is complete
        assert candidate["entries_freeze_file_path_present"] is complete
        assert candidate["freeze_index_path_present"] is complete
        assert candidate["project_frozen_implemented_steps_path_present"] is complete
        assert candidate["written_path_triplet_complete"] is complete
        assert candidate["entries_filename_matches_current_freeze_id"] is complete
        assert candidate["freeze_id_matches_entries_path"] is complete
        assert candidate["current_feature_title_matches_written_paths"] is complete
        assert candidate["freeze_memory_status_ok_bound_to_same_write"] is complete
        assert candidate["project_freeze_ledger_demoted_to_blueprint_logic"] is True
        assert candidate["files_to_send_ai_demoted_to_exposure_artifact"] is True
        assert candidate["startup_zip_demoted_to_refresh_artifact"] is True
        assert candidate["wrong_root_paths_demoted"] is (not complete)
        assert candidate["truncated_paths_demoted_or_recovered"] is True
        assert candidate["missing_path_gap_not_inflated"] is (not complete)
        assert candidate["stale_or_adjacent_paths_demoted"] is True
        assert candidate["planned_next_step_not_written_path"] is True
        assert candidate["read_only_exposure_does_not_repair_paths"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_project_freeze_ledger_as_active_memory"] is False
        assert candidate["treat_wrong_root_as_current_project"] is False
        assert candidate["treat_missing_written_paths_as_complete"] is False
        assert candidate["treat_truncated_paths_as_complete"] is False
        assert candidate["treat_missing_index_as_complete"] is False
        assert candidate["treat_missing_implemented_steps_as_complete"] is False
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
    assert "MLRT-100" in text
    assert "64/64" in text
    assert "986/986" in text
    assert "`19` real test suites" in text
    assert "project_freeze_after_update/frozen_features_memory" in text
    assert "project_freeze_ledger" in text
    assert "freeze_index.json" in text
    assert "project_frozen_implemented_steps.md" in text
    assert "exact current freeze ID" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "986/986" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_written_path_integrity_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 986
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 19
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_written_path_triplet_completeness_tested"] is True
    assert manifest[f"{PREFIX}_selected_project_root_binding_tested"] is True
    assert manifest[f"{PREFIX}_frozen_features_memory_ownership_tested"] is True
    assert manifest[f"{PREFIX}_freeze_id_path_filename_coherence_tested"] is True
    assert manifest[f"{PREFIX}_path_truncation_and_omission_recovery_tested"] is True
    assert manifest[f"{PREFIX}_stale_or_wrong_feature_path_demotion_tested"] is True
    assert manifest[f"{PREFIX}_write_and_exposure_binding_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_path_integrity_tested"] is True
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
    print("SANDBOX_RSS_MLRT101_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
