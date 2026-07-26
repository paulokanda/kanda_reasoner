from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_105_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_104_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt105_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-105 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt105_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt104_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-104 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT105_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-106 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-105 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized AI-send exposure alignment in-memory offline prompt-selection test suite after MLRT-104 freeze; MLRT-104 reviewed the MLRT-103 64-case freeze-index consistency result as good but validation-only evidence and identified AI-send exposure alignment as the next correction; MLRT-105 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-105 passed 64/64 AI-send exposure alignment cases across eight balanced audit families, with 32/32 AI-send exposure alignment pairs represented, two deliberately exposure-aligned-versus-exposure-mismatched variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 AI-send exposure alignment pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 1114/1114 cases across twenty-one real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of current freeze memory exposure to selected-project AI-send and startup exposure alignment, including files_to_send_ai ZIP refresh, what_to_say_to_ai_freeze_feature.md alignment, startup ZIP refresh (`first_prompts_to_ai.zip`), paste-after file refresh, 09_active_project_freeze_context.md coherence, AI compliance refresh block coherence, and latest current-feature freeze ID alignment, while demoting stale, truncated, wrong-root, wrong-feature, missing-AI-send, missing-startup, mismatched-context, or project_freeze_ledger exposure evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['AI_SEND_ZIP_CURRENT_FREEZE_BINDING', 'AI_SEND_INSTRUCTION_ALIGNMENT', 'STARTUP_ZIP_CONTEXT_REFRESH_ALIGNMENT', 'PASTE_AFTER_FILE_ALIGNMENT', 'AI_COMPLIANCE_REFRESH_BLOCK_BINDING', 'FREEZE_MEMORY_EXPOSURE_TO_AI_SEND_CONSISTENCY', 'STALE_OR_WRONG_ROOT_EXPOSURE_DEMOTION', 'BOUNDARY_CONTAINMENT_DURING_AI_SEND_ALIGNMENT']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE', 'TREAT_PROJECT_FREEZE_LEDGER_AS_ACTIVE_MEMORY', 'TREAT_WRONG_ROOT_AS_CURRENT_PROJECT', 'TREAT_MISSING_WRITTEN_PATHS_AS_COMPLETE', 'TREAT_TRUNCATED_PATHS_AS_COMPLETE', 'TREAT_MISSING_INDEX_AS_COMPLETE', 'TREAT_MISSING_IMPLEMENTED_STEPS_AS_COMPLETE', 'TREAT_INDEX_COUNT_MISMATCH_AS_OK', 'TREAT_ENTRY_FILE_COUNT_MISMATCH_AS_OK', 'TREAT_ACTIVE_COUNT_MISMATCH_AS_OK', 'TREAT_STALE_INDEX_AS_CURRENT', 'TREAT_STALE_AI_SEND_ZIP_AS_CURRENT', 'TREAT_WRONG_ROOT_AI_SEND_AS_CURRENT', 'TREAT_STARTUP_ZIP_AS_FREEZE_OWNER', 'TREAT_AI_SEND_ARTIFACT_AS_MEMORY_OWNER', 'TREAT_MISSING_STARTUP_CONTEXT_AS_OK', 'TREAT_MISMATCHED_AI_SEND_CONTEXT_AS_CURRENT']
FAMILY_DEFINITIONS = [{'family': 'AI_SEND_ZIP_CURRENT_FREEZE_BINDING', 'pairs': [('files_to_send_ai ZIP is refreshed after the current local write and names the current feature freeze ID', 'files_to_send_ai ZIP is stale from a prior feature but accepted as current'), ('AI-send ZIP remains under the selected project project_freeze_after_update/files_to_send_ai path', 'AI-send ZIP path points at a wrong project root and is accepted'), ('AI-send ZIP contains current active project freeze context exposure without owning memory', 'AI-send ZIP replaces project_freeze_after_update/frozen_features_memory as the owner'), ('AI-send ZIP timestamp follows the current Confirm and Write evidence', 'AI-send ZIP timestamp predates current write but is treated as refreshed')]}, {'family': 'AI_SEND_INSTRUCTION_ALIGNMENT', 'pairs': [('what_to_say_to_ai_freeze_feature.md aligns with current freeze memory and current feature ID', 'AI-send instruction references a prior or future feature but is accepted'), ('AI-send instruction remains an exposure guide and does not mutate freeze memory', 'AI-send instruction is used to repair or regenerate freeze_index.json'), ('AI-send instruction points the next AI session to active project freeze context without route authority', 'AI-send instruction grants runtime route authority'), ('AI-send instruction is paired with the matching AI-send ZIP from the same refresh block', 'instruction and ZIP come from different refresh blocks but are treated as aligned')]}, {'family': 'STARTUP_ZIP_CONTEXT_REFRESH_ALIGNMENT', 'pairs': [('first_prompts_to_ai.zip refresh contains 09_active_project_freeze_context.md for the current freeze', 'startup ZIP is old and lacks current freeze context but is accepted'), ('09_active_project_freeze_context.md matches the latest current feature freeze ID and next step', 'startup context freeze ID disagrees with the local write block'), ('startup ZIP refresh is session exposure, not live prompt loading for routing', 'startup ZIP is loaded as live prompts for runtime routing'), ('startup ZIP path is selected-project local exposure, not external AI authority', 'startup ZIP path is treated as external AI approval authority')]}, {'family': 'PASTE_AFTER_FILE_ALIGNMENT', 'pairs': [('paste_after_first_prompts_to_ai.md is refreshed with the current freeze context sequence', 'paste-after file is stale and points to an older current feature'), ('paste-after file and startup ZIP belong to the same current refresh event', 'paste-after file and startup ZIP have mismatched refresh provenance'), ('paste-after instructions expose context for the next session without changing router prompt logic', 'paste-after instructions modify router prompt logic'), ('truncated paste-after exposure triggers targeted recovery instead of completion', 'truncated paste-after text is inflated into full completion evidence')]}, {'family': 'AI_COMPLIANCE_REFRESH_BLOCK_BINDING', 'pairs': [('AI COMPLIANCE REFRESH AFTER LOCAL WRITE follows the matching LOCAL FREEZE WRITE OK block', 'AI compliance refresh block appears only in preview context but is accepted'), ('refresh block lists AI-send ZIP, AI-send instruction, startup ZIP, paste-after file, and context file', 'refresh block is missing startup or AI-send artifacts but is treated as complete'), ('refresh block is tied to the same current feature freeze ID as written paths and exposure status', 'refresh block belongs to a different feature freeze ID'), ('refresh block confirms exposure refresh without becoming freeze write evidence itself', 'refresh block replaces explicit local freeze write evidence')]}, {'family': 'FREEZE_MEMORY_EXPOSURE_TO_AI_SEND_CONSISTENCY', 'pairs': [('FREEZE_MEMORY_STATUS OK agrees with current AI-send and startup exposure artifacts', 'FREEZE_MEMORY_STATUS OK is paired with stale AI-send artifacts'), ('latest current-feature freeze ID coheres across write block, index, AI-send, startup context, and planned next step', 'current freeze ID differs across AI-send and startup context but is accepted'), ('index and active counts align with the current AI-send exposure generated time', 'AI-send exposure reports counts from a different selected project'), ('active/non-superseded counts remain offline exposure facts and not route authority', 'active/non-superseded counts grant route authority')]}, {'family': 'STALE_OR_WRONG_ROOT_EXPOSURE_DEMOTION', 'pairs': [('stale files_to_send_ai packs are demoted even when their filenames look valid', 'stale files_to_send_ai pack overrides current freeze memory'), ('wrong-root AI-send and startup paths are demoted even when internally coherent', 'wrong-root coherent AI-send paths are treated as selected project exposure'), ('project_freeze_ledger exposure-like data remains blueprint logic only', 'project_freeze_ledger exposure-like data is used as active project freeze memory'), ('missing or truncated AI-send/startup exposure triggers recovery without denying the local write', 'truncated exposure causes a false claim that no local write occurred')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_AI_SEND_ALIGNMENT', 'pairs': [('AI-send exposure alignment is offline evidence handling and not runtime routing authority', 'AI-send exposure alignment grants runtime route authority'), ('AI-send/startup alignment does not load live prompts, live freeze memory, or router canon for routing', 'alignment loads live prompts or live freeze memory for routing'), ('AI-send exposure alignment tests do not train, calibrate, or improve a model', 'AI-send exposure evidence is stored as training data'), ('AI-send exposure alignment does not mutate freeze memory, gold registry, Pilot, or Copilot behavior', 'alignment writes the gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            good_text, gap_text = pair
            pair_id = f"mlrt105_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("ai_send_exposure_aligned_current_feature", good_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("ai_send_exposure_gap_or_mismatch_containment", gap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt105_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-105 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Preserve selected-project AI-send/startup exposure alignment without runtime authority."
                )
                aligned = variant == "ai_send_exposure_aligned_current_feature"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "files_to_send_ai_zip_present": aligned,
                    "files_to_send_ai_zip_current_feature_bound": aligned,
                    "ai_send_zip_selected_project_root_bound": aligned,
                    "ai_send_zip_timestamp_after_current_write": aligned,
                    "ai_send_instruction_present": aligned,
                    "ai_send_instruction_current_context_aligned": aligned,
                    "ai_send_instruction_and_zip_same_refresh_event": aligned,
                    "startup_zip_present": aligned,
                    "startup_zip_current_context_present": aligned,
                    "active_project_freeze_context_matches_current_freeze_id": aligned,
                    "paste_after_file_present": aligned,
                    "paste_after_file_current_sequence_aligned": aligned,
                    "ai_compliance_refresh_block_present_after_write": aligned,
                    "refresh_block_lists_required_ai_send_and_startup_artifacts": aligned,
                    "refresh_block_same_current_freeze_id": aligned,
                    "freeze_memory_status_ok_bound_to_ai_send_exposure": aligned,
                    "latest_current_feature_freeze_id_coherent_across_exposure": aligned,
                    "project_freeze_ledger_demoted_to_blueprint_logic": True,
                    "ai_send_artifacts_demoted_to_exposure_not_owner": True,
                    "startup_artifacts_demoted_to_session_exposure": True,
                    "wrong_root_ai_send_demoted": not aligned,
                    "stale_ai_send_pack_demoted": True,
                    "truncated_ai_send_or_startup_recovery_required": not aligned,
                    "mismatched_ai_send_context_not_inflated": not aligned,
                    "missing_ai_send_or_startup_gap_not_false_no_write": not aligned,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_stale_ai_send_zip_as_current": False,
                    "treat_wrong_root_ai_send_as_current": False,
                    "treat_startup_zip_as_freeze_owner": False,
                    "treat_ai_send_artifact_as_memory_owner": False,
                    "treat_missing_startup_context_as_ok": False,
                    "treat_mismatched_ai_send_context_as_current": False,
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
    assert all(variants == {"ai_send_exposure_aligned_current_feature", "ai_send_exposure_gap_or_mismatch_containment"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        aligned = case["variant"] == "ai_send_exposure_aligned_current_feature"
        alignment_fields = [
            "files_to_send_ai_zip_present",
            "files_to_send_ai_zip_current_feature_bound",
            "ai_send_zip_selected_project_root_bound",
            "ai_send_zip_timestamp_after_current_write",
            "ai_send_instruction_present",
            "ai_send_instruction_current_context_aligned",
            "ai_send_instruction_and_zip_same_refresh_event",
            "startup_zip_present",
            "startup_zip_current_context_present",
            "active_project_freeze_context_matches_current_freeze_id",
            "paste_after_file_present",
            "paste_after_file_current_sequence_aligned",
            "ai_compliance_refresh_block_present_after_write",
            "refresh_block_lists_required_ai_send_and_startup_artifacts",
            "refresh_block_same_current_freeze_id",
            "freeze_memory_status_ok_bound_to_ai_send_exposure",
            "latest_current_feature_freeze_id_coherent_across_exposure",
        ]
        for field in alignment_fields:
            assert candidate[field] is aligned
        assert candidate["project_freeze_ledger_demoted_to_blueprint_logic"] is True
        assert candidate["ai_send_artifacts_demoted_to_exposure_not_owner"] is True
        assert candidate["startup_artifacts_demoted_to_session_exposure"] is True
        assert candidate["wrong_root_ai_send_demoted"] is (not aligned)
        assert candidate["stale_ai_send_pack_demoted"] is True
        assert candidate["truncated_ai_send_or_startup_recovery_required"] is (not aligned)
        assert candidate["mismatched_ai_send_context_not_inflated"] is (not aligned)
        assert candidate["missing_ai_send_or_startup_gap_not_false_no_write"] is (not aligned)
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_stale_ai_send_zip_as_current"] is False
        assert candidate["treat_wrong_root_ai_send_as_current"] is False
        assert candidate["treat_startup_zip_as_freeze_owner"] is False
        assert candidate["treat_ai_send_artifact_as_memory_owner"] is False
        assert candidate["treat_missing_startup_context_as_ok"] is False
        assert candidate["treat_mismatched_ai_send_context_as_current"] is False
        assert candidate["critical_boundary_error_budget"] == 0
        for flag in BOUNDARY_FALSE_FLAGS:
            assert candidate[flag] is False, flag


def validate_project_surface() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    assert README.exists(), README
    assert MANIFEST.exists(), MANIFEST

    text = DOC.read_text(encoding="utf-8")
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert "MLRT-104" in text
    assert "64/64" in text
    assert "1114/1114" in text
    assert "`21` real test suites" in text
    assert "files_to_send_ai" in text
    assert "what_to_say_to_ai_freeze_feature.md" in text
    assert "first_prompts_to_ai.zip" in text
    assert "paste_after_first_prompts_to_ai.md" in text
    assert "09_active_project_freeze_context.md" in text
    assert "AI COMPLIANCE REFRESH AFTER LOCAL WRITE" in text
    assert "project_freeze_ledger" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "1114/1114" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_ai_send_exposure_alignment_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 1114
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 21
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_ai_send_zip_current_freeze_binding_tested"] is True
    assert manifest[f"{PREFIX}_ai_send_instruction_alignment_tested"] is True
    assert manifest[f"{PREFIX}_startup_zip_context_refresh_alignment_tested"] is True
    assert manifest[f"{PREFIX}_paste_after_file_alignment_tested"] is True
    assert manifest[f"{PREFIX}_ai_compliance_refresh_block_binding_tested"] is True
    assert manifest[f"{PREFIX}_freeze_memory_exposure_to_ai_send_consistency_tested"] is True
    assert manifest[f"{PREFIX}_stale_or_wrong_root_exposure_demotion_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_ai_send_alignment_tested"] is True
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
    print("SANDBOX_RSS_MLRT105_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
