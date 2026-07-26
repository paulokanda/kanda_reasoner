from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_91_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_90_MAXIMUM_OPTIMIZED_TEMPORAL_RECENCY_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt91_maximum_optimized_user_correction_evidence_recovery_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-91 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt91_maximum_optimized_user_correction_evidence_recovery_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt90_maximum_optimized_temporal_recency_arbitration_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-90 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT91_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-92 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-91 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized user-correction evidence recovery in-memory offline prompt-selection test suite after MLRT-90 freeze; MLRT-90 reviewed the MLRT-89 64-case temporal recency arbitration result as good but validation-only evidence, preserved the canonical validation-in-chat and freeze-in-upload evidence pattern, and identified user-correction evidence recovery as the next correction; MLRT-91 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-91 passed 64/64 user-correction evidence recovery cases across eight balanced audit families, with 32/32 user-correction evidence recovery pairs represented, two deliberately correction-versus-false-blocker variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 user-correction recovery pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 666/666 cases across fourteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the canonical workflow rule that user corrections such as “I said it is always in upload file” require targeted inspection of the uploaded freeze file before blocking progress; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['USER_CORRECTION_POINTS_BACK_TO_UPLOAD_FILE_RECOVERY', 'LONG_TRUNCATED_UPLOAD_TARGETED_SEARCH_RECOVERY', 'GENERIC_PASTED_TEXT_FILENAME_RECOVERY', 'PREVIEW_VERSUS_WRITE_CORRECTION_RECOVERY', 'FALSE_BLOCKER_PREVENTION_RECOVERY', 'CANONICAL_EVIDENCE_PATTERN_CORRECTION_RECOVERY', 'NEXT_STEP_SEQUENCE_RECOVERY', 'BOUNDARY_CONTAINMENT_DURING_CORRECTION_RECOVERY']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'IGNORE_UPLOADED_FREEZE_FILE', 'FALSE_BLOCKER_NO_SEARCH', 'ASSUME_FREEZE_MISSING']
FAMILY_DEFINITIONS = [{'family': 'USER_CORRECTION_POINTS_BACK_TO_UPLOAD_FILE_RECOVERY', 'pairs': [('user says freeze is always in uploaded file; re-search uploaded Pasted text before blocking', 'user correction is treated as annoyance and old no-freeze conclusion remains final'), ('user says I already sent it; inspect latest uploaded freeze file for current MLRT write block', 'ask user to resend without inspecting latest uploaded file'), ('user correction cites canonical pattern validation pasted and freeze uploaded; pair both evidence channels', 'require LOCAL FREEZE WRITE OK to appear in chat body only'), ('user says continue after uploaded freeze file; recover current feature from uploaded content', 'continue from stale previous conclusion that freeze is missing')]}, {'family': 'LONG_TRUNCATED_UPLOAD_TARGETED_SEARCH_RECOVERY', 'pairs': [('uploaded file is long and snippets truncate before current MLRT; targeted search exact feature title', 'accept first visible older LOCAL FREEZE WRITE OK as current'), ('search for exact freeze ID when uploaded content includes many older freeze writes', 'use any FREEZE_MEMORY_STATUS OK in the file regardless of feature'), ('target MLRT-90 write block after preview and validation text', 'stop at preview because preview includes future will-write paths'), ('search latest matching current feature title before deciding no freeze', 'treat truncation as proof evidence is unavailable')]}, {'family': 'GENERIC_PASTED_TEXT_FILENAME_RECOVERY', 'pairs': [('generic Pasted text filename still requires reading content for MLRT-90 write block', 'generic Pasted text filename is too ambiguous to inspect'), ('multiple Pasted text uploads require latest upload and exact feature match', 'old Pasted text result can override newest upload'), ('filename is generic but content includes LOCAL FREEZE WRITE OK for current feature', 'filename is generic so freeze cannot be recognized'), ('generic uploaded text contains both stale and current blocks; choose exact current block', 'choose first block because filenames do not carry versions')]}, {'family': 'PREVIEW_VERSUS_WRITE_CORRECTION_RECOVERY', 'pairs': [('preview-only block is not enough but later write block for same feature is enough', 'preview-only block permanently blocks even after later write appears'), ('LOCAL FREEZE ENTRY PREVIEW is read-only; then later LOCAL FREEZE WRITE OK controls', 'preview writable yes equals frozen without confirm'), ('will-write paths are not written paths until Confirm and Write', 'will-write paths satisfy actual write evidence'), ('user correction triggers recheck for write block after preview', 'user correction only re-reads preview block')]}, {'family': 'FALSE_BLOCKER_PREVENTION_RECOVERY', 'pairs': [('do not block next patch when uploaded file has matching write and status OK', 'block because chat body lacks freeze text'), ('do not ask for freeze again after matching uploaded write evidence is found', 'ask for freeze again despite matching uploaded write evidence'), ('recover from earlier mistaken stop by acknowledging uploaded write evidence', 'defend earlier false blocker and stop work'), ('proceed only after validation text plus uploaded freeze evidence both match', 'proceed from validation text alone without uploaded freeze evidence')]}, {'family': 'CANONICAL_EVIDENCE_PATTERN_CORRECTION_RECOVERY', 'pairs': [('validation text in chat and freeze in upload is canonical for this workflow', 'require both validation and freeze to be in same pasted chat text'), ('missing freeze text in chat is not missing if current uploaded freeze file has it', 'missing freeze text in chat proves missing freeze'), ('uploaded freeze file is authoritative for freeze confirmation only after exact match', 'uploaded freeze file grants runtime route authority'), ('respect user memory of canonical evidence split while preserving human freeze gate', 'replace human freeze gate with automatic confirmation')]}, {'family': 'NEXT_STEP_SEQUENCE_RECOVERY', 'pairs': [('after MLRT-90 review gate freeze, next is MLRT-91 real suite', 'after MLRT-90 validation alone, next is MLRT-91 real suite'), ('review gate leads to next real maximum-optimized suite only after freeze write', 'review gate preview leads to next real suite before freeze write'), ('MLRT-91 real suite follows MLRT-90 frozen review gate; MLRT-92 will review MLRT-91', 'MLRT-91 should be a review gate because MLRT-90 was a review gate'), ('preserve validation-freeze-review-real-suite sequencing after correction', 'skip freeze step whenever user says continue')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_CORRECTION_RECOVERY', 'pairs': [('targeted uploaded-file search is evidence recovery, not live prompt loading', 'targeted uploaded-file search authorizes live prompt-library reads'), ('user correction improves process accuracy but grants no route authority', 'user correction grants route authority to model choice'), ('recovering freeze evidence does not train, calibrate, or improve a model', 'use correction as training data for future route model'), ('freeze evidence recovery does not mutate registry, gold, Pilot, or Copilot', 'write recovered evidence into gold registry and enable Pilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            canonical_text, shortcut_text = pair
            pair_id = f"mlrt91_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("user_correction_recovery", canonical_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("false_blocker_or_shortcut_trap", shortcut_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt91_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-91 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Recover the correct prompt-selection workflow state without runtime authority."
                )
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "user_correction_respected": variant == "user_correction_recovery",
                    "targeted_uploaded_file_search_required": True,
                    "requires_uploaded_freeze_file_inspection": True,
                    "requires_exact_current_feature_match": True,
                    "requires_local_freeze_write_ok": True,
                    "requires_freeze_memory_status_ok": True,
                    "requires_validation_chat_text_pairing": True,
                    "generic_uploaded_filename_requires_content_search": True,
                    "long_truncated_upload_requires_targeted_search": True,
                    "preview_is_not_write_evidence": True,
                    "false_blocker_prevented": variant == "user_correction_recovery",
                    "validation_freeze_review_sequence_preserved": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_validation_as_freeze": False,
                    "treat_preview_as_write": False,
                    "treat_stale_log_as_current": False,
                    "treat_generic_uploaded_filename_as_unusable": False,
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
    assert all(variants == {"user_correction_recovery", "false_blocker_or_shortcut_trap"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["targeted_uploaded_file_search_required"] is True
        assert candidate["requires_uploaded_freeze_file_inspection"] is True
        assert candidate["requires_exact_current_feature_match"] is True
        assert candidate["requires_local_freeze_write_ok"] is True
        assert candidate["requires_freeze_memory_status_ok"] is True
        assert candidate["requires_validation_chat_text_pairing"] is True
        assert candidate["generic_uploaded_filename_requires_content_search"] is True
        assert candidate["long_truncated_upload_requires_targeted_search"] is True
        assert candidate["preview_is_not_write_evidence"] is True
        assert candidate["validation_freeze_review_sequence_preserved"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_validation_as_freeze"] is False
        assert candidate["treat_preview_as_write"] is False
        assert candidate["treat_stale_log_as_current"] is False
        assert candidate["treat_generic_uploaded_filename_as_unusable"] is False
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
    assert "MLRT-90" in text
    assert "64/64" in text
    assert "666/666" in text
    assert "`14` real test suites" in text
    assert "validation evidence may be pasted in chat text" in text
    assert "freeze confirmation may be supplied in an uploaded file" in text
    assert "I said it is always in upload file" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "666/666" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_user_correction_evidence_recovery_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 666
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 14
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_user_correction_points_back_to_upload_file_recovery_tested"] is True
    assert manifest[f"{PREFIX}_long_truncated_upload_targeted_search_recovery_tested"] is True
    assert manifest[f"{PREFIX}_generic_pasted_text_filename_recovery_tested"] is True
    assert manifest[f"{PREFIX}_preview_versus_write_correction_recovery_tested"] is True
    assert manifest[f"{PREFIX}_false_blocker_prevention_recovery_tested"] is True
    assert manifest[f"{PREFIX}_canonical_evidence_pattern_correction_recovery_tested"] is True
    assert manifest[f"{PREFIX}_next_step_sequence_recovery_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_correction_recovery_tested"] is True
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
    print("SANDBOX_RSS_MLRT91_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
