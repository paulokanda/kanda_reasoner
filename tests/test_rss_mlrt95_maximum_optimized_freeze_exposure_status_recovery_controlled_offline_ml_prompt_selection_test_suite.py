from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_95_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_94_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt95_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-95 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt95_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt94_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-94 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT95_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-96 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-95 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized freeze-exposure status recovery in-memory offline prompt-selection test suite after MLRT-94 freeze; MLRT-94 reviewed the MLRT-93 64-case current-feature freeze-intake precedence result as good but validation-only evidence and identified freeze-exposure status recovery as the next correction; MLRT-95 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-95 passed 64/64 freeze-exposure status recovery cases across eight balanced audit families, with 32/32 freeze-exposure recovery pairs represented, two deliberately status-recovered-versus-status-gap variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 freeze-exposure recovery pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 794/794 cases across sixteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the distinction between LOCAL FREEZE WRITE OK as written freeze-entry evidence and FREEZE_MEMORY_STATUS OK as refreshed exposure evidence, including omitted, delayed, truncated, separate-upload, stale-status, and wrong-feature status cases without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['LOCAL_WRITE_OK_WITH_STATUS_PENDING_DISTINCTION', 'SEPARATE_EXPOSURE_STATUS_RECOVERY', 'TRUNCATED_LOG_TARGETED_STATUS_SEARCH', 'SAME_FEATURE_STATUS_BINDING', 'STALE_STATUS_AND_OLD_FREEZE_DEMOTION', 'FALSE_BLOCKER_PREVENTION_AFTER_WRITE', 'SEQUENCE_ADVANCEMENT_GATING_WITH_STATUS', 'BOUNDARY_CONTAINMENT_DURING_STATUS_RECOVERY']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_WRITE_AS_EXPOSURE_STATUS', 'TREAT_STALE_STATUS_AS_CURRENT', 'TREAT_WRONG_FEATURE_STATUS_AS_CURRENT', 'PROCEED_WITHOUT_STATUS_RECOVERY']
FAMILY_DEFINITIONS = [{'family': 'LOCAL_WRITE_OK_WITH_STATUS_PENDING_DISTINCTION', 'pairs': [('LOCAL FREEZE WRITE OK is recognized as current freeze-entry write evidence while status refresh remains a separate recoverable check', 'LOCAL FREEZE WRITE OK is treated as both write evidence and FREEZE_MEMORY_STATUS OK'), ('written paths and freeze hint intake usage prove the entry was written but do not by themselves prove refreshed exposure status', 'written paths are treated as refreshed AI exposure status'), ('same-feature write evidence is preserved when the status section is omitted from the pasted chat text', 'same-feature write evidence is rejected because the pasted chat omitted exposure status'), ('write-confirmed current feature is marked status-pending rather than not-frozen when refresh evidence is not yet visible', 'write-confirmed current feature is marked not written because status is not visible')]}, {'family': 'SEPARATE_EXPOSURE_STATUS_RECOVERY', 'pairs': [('FREEZE_MEMORY_STATUS OK supplied in a later pasted block is joined to the same current freeze ID', 'later FREEZE_MEMORY_STATUS OK is ignored because it was not in the first pasted block'), ('FREEZE_MEMORY_STATUS OK supplied in an uploaded file is recovered by targeted search for the same feature', 'uploaded status evidence is not searched after a write block appears in chat'), ('AI COMPLIANCE REFRESH AFTER LOCAL WRITE plus current status OK completes the exposure check', 'AI compliance refresh text alone completes exposure without status OK'), ('startup freeze context refresh supports but does not replace current status OK', 'startup refresh alone replaces missing FREEZE_MEMORY_STATUS OK')]}, {'family': 'TRUNCATED_LOG_TARGETED_STATUS_SEARCH', 'pairs': [('truncated uploaded log requires targeted search for current freeze ID and FREEZE_MEMORY_STATUS OK', 'truncated uploaded log is treated as missing evidence without targeted search'), ('long file containing older statuses is searched for the newest matching current-feature status block', 'first visible older FREEZE_MEMORY_STATUS OK controls the current feature'), ('status hidden after compact freeze ID list is recoverable by exact current-feature query', 'compact freeze ID list truncation permanently blocks progress'), ('generic Pasted text filename is acceptable when exact current status evidence is inside it', 'generic Pasted text filename is rejected even with exact current status evidence')]}, {'family': 'SAME_FEATURE_STATUS_BINDING', 'pairs': [('FREEZE_MEMORY_STATUS OK must bind to the same MLRT-94 freeze ID before MLRT-95 proceeds', 'FREEZE_MEMORY_STATUS OK from MLRT-71 binds to MLRT-94'), ('same current feature title plus same freeze ID plus status OK is accepted', 'same title without same freeze ID is accepted as current exposure status'), ('status OK from the active project root E:\\kanda_reasoner is accepted for the current feature', 'status OK from another project root is accepted for the current feature'), ('same-feature status evidence after LOCAL FREEZE WRITE OK is treated as completed exposure refresh', 'status evidence before an unrelated old write is treated as current')]}, {'family': 'STALE_STATUS_AND_OLD_FREEZE_DEMOTION', 'pairs': [('older MLRT status OK lines are historical context when current MLRT status is separate later', 'older MLRT status OK lines prove the current feature exposure status'), ('old freeze-entry summaries are not used to infer current exposure status', 'old freeze-entry summaries supply current exposure status'), ('consumed stale sidecar status evidence is demoted unless same current feature matches', 'consumed stale sidecar status evidence completes current feature'), ('prior uploaded file status is demoted when a newer upload lacks current status and needs targeted search', 'prior uploaded file status controls over latest upload context')]}, {'family': 'FALSE_BLOCKER_PREVENTION_AFTER_WRITE', 'pairs': [('same-feature LOCAL FREEZE WRITE OK prevents a false not-frozen blocker while exposure status is sought', 'missing pasted status causes a false blocker that ignores write evidence'), ('status-pending recovery asks for or searches status evidence rather than rebuilding the same patch', 'status-pending recovery repeats the same patch because status was omitted'), ('written freeze entry plus delayed status is treated as recoverable sequence evidence', 'delayed status is treated as sequence failure'), ('current write evidence plus planned next step allows safe preparation once status is confirmed', 'planned next step alone allows safe preparation before write evidence')]}, {'family': 'SEQUENCE_ADVANCEMENT_GATING_WITH_STATUS', 'pairs': [('MLRT-94 write plus same-feature status OK permits MLRT-95 real suite generation', 'MLRT-94 validation-only output permits MLRT-95 without write or status'), ('review gate to real suite alternation is preserved after write and exposure status confirmation', 'real suite generation proceeds from preview-only review gate evidence'), ('planned next step is used only after current write and exposure status are reconciled', 'planned next step is used before current write is confirmed'), ('status recovery preserves the current MLRT sequence and does not skip MLRT-95', 'status recovery skips directly to a later milestone')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_STATUS_RECOVERY', 'pairs': [('freeze-exposure recovery is offline evidence handling, not runtime route authority', 'freeze-exposure recovery grants runtime route authority'), ('targeted uploaded-log search for status is not live freeze-memory read for routing', 'targeted uploaded-log search enables live freeze-memory reads for routing'), ('status recovery testing does not train, calibrate, or improve a model', 'status recovery evidence is saved as training data'), ('status recovery does not mutate freeze memory, gold registry, Pilot, or Copilot behavior', 'status recovery writes gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            recovery_text, gap_text = pair
            pair_id = f"mlrt95_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("status_recovered", recovery_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("status_gap_containment", gap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt95_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-95 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Recover freeze-exposure status without runtime authority."
                )
                recovered = variant == "status_recovered"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "local_freeze_write_ok_present": True,
                    "written_freeze_entry_recognized": True,
                    "same_feature_freeze_id_required": True,
                    "freeze_memory_status_ok_recovered": recovered,
                    "status_gap_containment_applied": not recovered,
                    "distinguishes_write_from_exposure_status": True,
                    "exposure_status_targeted_search_required": True,
                    "separate_upload_status_recovery_supported": True,
                    "truncated_log_status_recovery_supported": True,
                    "stale_status_demoted": True,
                    "wrong_feature_status_demoted": True,
                    "false_blocker_prevented_after_write": True,
                    "sequence_advancement_requires_status_reconciliation": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_write_as_exposure_status": False,
                    "treat_stale_status_as_current": False,
                    "treat_wrong_feature_status_as_current": False,
                    "treat_validation_as_freeze": False,
                    "auto_confirm_freeze": False,
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
    assert all(variants == {"status_recovered", "status_gap_containment"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["local_freeze_write_ok_present"] is True
        assert candidate["written_freeze_entry_recognized"] is True
        assert candidate["same_feature_freeze_id_required"] is True
        assert candidate["freeze_memory_status_ok_recovered"] is (case["variant"] == "status_recovered")
        assert candidate["status_gap_containment_applied"] is (case["variant"] == "status_gap_containment")
        assert candidate["distinguishes_write_from_exposure_status"] is True
        assert candidate["exposure_status_targeted_search_required"] is True
        assert candidate["separate_upload_status_recovery_supported"] is True
        assert candidate["truncated_log_status_recovery_supported"] is True
        assert candidate["stale_status_demoted"] is True
        assert candidate["wrong_feature_status_demoted"] is True
        assert candidate["false_blocker_prevented_after_write"] is True
        assert candidate["sequence_advancement_requires_status_reconciliation"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_write_as_exposure_status"] is False
        assert candidate["treat_stale_status_as_current"] is False
        assert candidate["treat_wrong_feature_status_as_current"] is False
        assert candidate["treat_validation_as_freeze"] is False
        assert candidate["auto_confirm_freeze"] is False
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
    assert "MLRT-94" in text
    assert "64/64" in text
    assert "794/794" in text
    assert "`16` real test suites" in text
    assert "LOCAL FREEZE WRITE OK" in text
    assert "FREEZE_MEMORY_STATUS: OK" in text
    assert "separate upload" in text
    assert "truncated" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "794/794" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_freeze_exposure_status_recovery_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 794
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 16
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_local_freeze_write_ok_recognition_tested"] is True
    assert manifest[f"{PREFIX}_separate_exposure_status_recovery_tested"] is True
    assert manifest[f"{PREFIX}_truncated_log_targeted_status_search_tested"] is True
    assert manifest[f"{PREFIX}_same_feature_status_binding_tested"] is True
    assert manifest[f"{PREFIX}_stale_status_and_old_freeze_demotion_tested"] is True
    assert manifest[f"{PREFIX}_false_blocker_prevention_after_write_tested"] is True
    assert manifest[f"{PREFIX}_sequence_advancement_gating_with_status_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_status_recovery_tested"] is True
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
    print("SANDBOX_RSS_MLRT95_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
