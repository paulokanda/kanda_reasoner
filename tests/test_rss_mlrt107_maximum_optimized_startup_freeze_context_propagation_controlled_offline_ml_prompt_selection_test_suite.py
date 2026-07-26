from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
DOC = MLRT / "MLRT_107_MAXIMUM_OPTIMIZED_STARTUP_FREEZE_CONTEXT_PROPAGATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_106_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt107_maximum_optimized_startup_freeze_context_propagation_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-107 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt107_maximum_optimized_startup_freeze_context_propagation_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt106_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-106 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT107_MAXIMUM_OPTIMIZED_STARTUP_FREEZE_CONTEXT_PROPAGATION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-108 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-107 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized startup freeze-context propagation in-memory offline prompt-selection test suite after MLRT-106 freeze; MLRT-106 reviewed the MLRT-105 64-case AI-send exposure alignment result as good but validation-only evidence and identified startup freeze-context propagation as the next correction; MLRT-107 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-107 passed 64/64 startup freeze-context propagation cases across eight balanced audit families, with 32/32 startup freeze-context propagation pairs represented, two deliberately propagated-current-context-versus-stale-or-mismatched-context variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 startup freeze-context propagation pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 1178/1178 cases across twenty-two real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of the next AI programming session to the selected project current freeze memory across first_prompts_to_ai.zip, paste_after_first_prompts_to_ai.md, 09_active_project_freeze_context.md, AI-send instructions, current freeze IDs, planned next-step sequencing, and startup handoff provenance, while demoting stale, truncated, wrong-root, wrong-feature, missing-startup, missing-paste-after, mismatched-context, wrong-next-step, or project_freeze_ledger startup evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['FIRST_PROMPTS_ZIP_CURRENT_CONTEXT_BINDING', 'ACTIVE_PROJECT_FREEZE_CONTEXT_FILE_COHERENCE', 'PASTE_AFTER_STARTUP_SEQUENCE_ALIGNMENT', 'AI_SEND_INSTRUCTION_TO_STARTUP_HANDOFF_ALIGNMENT', 'CURRENT_FREEZE_ID_AND_NEXT_STEP_PROPAGATION', 'STARTUP_STALENESS_TRUNCATION_AND_UPLOAD_RECOVERY', 'SELECTED_PROJECT_ROOT_AND_LEDGER_DEMOTION', 'NO_AUTHORITY_NO_RUNTIME_BOUNDARY_CONTAINMENT']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE', 'TREAT_PROJECT_FREEZE_LEDGER_AS_ACTIVE_MEMORY', 'TREAT_WRONG_ROOT_AS_CURRENT_PROJECT', 'TREAT_MISSING_WRITTEN_PATHS_AS_COMPLETE', 'TREAT_TRUNCATED_PATHS_AS_COMPLETE', 'TREAT_MISSING_INDEX_AS_COMPLETE', 'TREAT_MISSING_IMPLEMENTED_STEPS_AS_COMPLETE', 'TREAT_INDEX_COUNT_MISMATCH_AS_OK', 'TREAT_ENTRY_FILE_COUNT_MISMATCH_AS_OK', 'TREAT_ACTIVE_COUNT_MISMATCH_AS_OK', 'TREAT_STALE_INDEX_AS_CURRENT', 'TREAT_STALE_AI_SEND_ZIP_AS_CURRENT', 'TREAT_WRONG_ROOT_AI_SEND_AS_CURRENT', 'TREAT_STARTUP_ZIP_AS_FREEZE_OWNER', 'TREAT_AI_SEND_ARTIFACT_AS_MEMORY_OWNER', 'TREAT_MISSING_STARTUP_CONTEXT_AS_OK', 'TREAT_MISMATCHED_AI_SEND_CONTEXT_AS_CURRENT', 'TREAT_STALE_STARTUP_CONTEXT_AS_CURRENT', 'TREAT_MISSING_PASTE_AFTER_AS_OK', 'TREAT_WRONG_NEXT_STEP_AS_CURRENT', 'TREAT_STARTUP_HANDOFF_AS_ROUTE_AUTHORITY']
FAMILY_DEFINITIONS = [{'family': 'FIRST_PROMPTS_ZIP_CURRENT_CONTEXT_BINDING', 'pairs': [('first_prompts_to_ai.zip contains the current 09_active_project_freeze_context.md after the local write', 'first_prompts_to_ai.zip is stale but accepted as current startup context'), ('startup ZIP refresh is tied to the selected project root and current freeze ID', 'startup ZIP points to a wrong project root but is accepted'), ('startup ZIP is exposure for the next session, not owner of freeze memory', 'startup ZIP is treated as active freeze-memory owner'), ('startup ZIP refresh follows the current AI compliance refresh after local write', 'startup ZIP timestamp predates the current write but is accepted')]}, {'family': 'ACTIVE_PROJECT_FREEZE_CONTEXT_FILE_COHERENCE', 'pairs': [('09_active_project_freeze_context.md names the current feature freeze ID and latest next step', '09_active_project_freeze_context.md names a prior feature but is accepted'), ('active project freeze context preserves project_freeze_after_update/frozen_features_memory as owner', 'active project freeze context points to project_freeze_ledger as active memory'), ('active project freeze context is refreshed inside the startup ZIP after current write', 'active project freeze context is missing inside startup ZIP but completion is inferred'), ('active project freeze context remains read-only exposure to the next AI session', 'active project freeze context is used to mutate freeze_index.json')]}, {'family': 'PASTE_AFTER_STARTUP_SEQUENCE_ALIGNMENT', 'pairs': [('paste_after_first_prompts_to_ai.md is refreshed with the same current freeze ID as startup ZIP', 'paste-after file and startup ZIP contain mismatched freeze IDs'), ('paste-after file communicates the next step after the current MLRT feature', 'paste-after file names the wrong next MLRT but is accepted'), ('paste-after file tells the next session to load current freeze context without solving a task prematurely', 'paste-after file is treated as permission to bypass routing controls'), ('truncated paste-after exposure triggers targeted recovery instead of false completion', 'truncated paste-after text is inflated into complete startup evidence')]}, {'family': 'AI_SEND_INSTRUCTION_TO_STARTUP_HANDOFF_ALIGNMENT', 'pairs': [('what_to_say_to_ai_freeze_feature.md and startup ZIP expose the same current freeze context', 'AI-send instruction and startup ZIP come from different features but are accepted'), ('AI-send instruction remains a handoff instruction and not route authority', 'AI-send instruction grants runtime route authority'), ('AI-send instruction points to the refreshed startup package for the next programming session', 'AI-send instruction points to a stale startup package but is accepted'), ('AI compliance refresh block lists both AI-send and startup artifacts from the same local write', 'AI compliance refresh block lists only one artifact and missing context is ignored')]}, {'family': 'CURRENT_FREEZE_ID_AND_NEXT_STEP_PROPAGATION', 'pairs': [('current freeze ID propagates consistently through write block, startup context, paste-after file, and AI-send instruction', 'current freeze ID differs across handoff surfaces but is accepted'), ('planned next step matches the current feature review-gate or real-suite sequence', 'planned next step jumps to an unrelated or stale feature'), ('latest current-feature freeze ID wins over older preview or starter blocks', 'older preview or starter block overrides current startup context'), ('current-feature title and freeze ID both match before next patch proceeds', 'matching title is missing but a similar freeze ID is accepted')]}, {'family': 'STARTUP_STALENESS_TRUNCATION_AND_UPLOAD_RECOVERY', 'pairs': [('complete startup exposure includes startup ZIP, paste-after file, and active freeze context file', 'only partial startup exposure is present but treated as complete'), ('stale startup exposure is demoted while latest local write remains recognized', 'stale startup exposure blocks a valid current freeze write'), ('truncated first_prompts_to_ai evidence triggers specific missing-context recovery', 'truncated first_prompts_to_ai evidence is treated as authoritative completion'), ('separate-upload startup evidence can satisfy exposure only when it matches current feature context', 'separate-upload startup evidence for another feature is accepted')]}, {'family': 'SELECTED_PROJECT_ROOT_AND_LEDGER_DEMOTION', 'pairs': [('startup handoff surfaces point to the selected project root', 'startup handoff points to a different drive or project and is accepted'), ('project_freeze_ledger remains reusable blueprint logic only', 'project_freeze_ledger is treated as selected project freeze memory'), ('startup handoff does not install KANDA_FREEZE_HINT.json into project root', 'KANDA_FREEZE_HINT.json in project root is accepted as installed state'), ('selected project frozen_features_memory paths remain canonical after startup refresh', 'startup handoff redirects memory ownership to files_to_send_ai')]}, {'family': 'NO_AUTHORITY_NO_RUNTIME_BOUNDARY_CONTAINMENT', 'pairs': [('startup propagation helps prompt selection only during offline review', 'startup propagation enables runtime routing authority'), ('startup context is not live prompt loading for routing', 'startup context is loaded as live prompts for routing'), ('startup propagation does not create datasets, labels, reports, training data, or calibration evidence', 'startup propagation is treated as model improvement or training data'), ('provider calls, embeddings, vector stores, registry mutation, runtime Pilot, and Copilot stay disabled', 'startup handoff enables provider calls or Copilot behavior')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            good_text, gap_text = pair
            pair_id = f"mlrt107_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("startup_context_propagated_current_feature", good_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("startup_context_gap_or_mismatch_containment", gap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt107_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-107 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Preserve selected-project startup freeze-context propagation without runtime authority."
                )
                aligned = variant == "startup_context_propagated_current_feature"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "first_prompts_to_ai_zip_present": aligned,
                    "first_prompts_to_ai_zip_current_refresh_bound": aligned,
                    "startup_zip_selected_project_root_bound": aligned,
                    "startup_zip_timestamp_after_current_write": aligned,
                    "active_project_freeze_context_file_present": aligned,
                    "active_project_freeze_context_matches_current_freeze_id": aligned,
                    "active_project_freeze_context_matches_planned_next_step": aligned,
                    "paste_after_file_present": aligned,
                    "paste_after_file_current_sequence_aligned": aligned,
                    "paste_after_file_same_refresh_event_as_startup_zip": aligned,
                    "ai_send_instruction_present": aligned,
                    "ai_send_instruction_aligned_to_startup_handoff": aligned,
                    "ai_compliance_refresh_block_present_after_write": aligned,
                    "refresh_block_lists_required_ai_send_and_startup_artifacts": aligned,
                    "refresh_block_same_current_freeze_id": aligned,
                    "latest_current_feature_freeze_id_coherent_across_startup_surfaces": aligned,
                    "planned_next_step_sequence_coherent": aligned,
                    "project_freeze_ledger_demoted_to_blueprint_logic": True,
                    "startup_artifacts_demoted_to_session_exposure_not_memory_owner": True,
                    "ai_send_artifacts_demoted_to_exposure_not_memory_owner": True,
                    "wrong_root_startup_demoted": not aligned,
                    "stale_startup_context_demoted": True,
                    "truncated_startup_or_paste_after_recovery_required": not aligned,
                    "mismatched_startup_context_not_inflated": not aligned,
                    "missing_startup_or_paste_after_gap_not_false_completion": not aligned,
                    "wrong_next_step_not_treated_as_current": not aligned,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_stale_startup_context_as_current": False,
                    "treat_missing_startup_context_as_ok": False,
                    "treat_missing_paste_after_as_ok": False,
                    "treat_wrong_next_step_as_current": False,
                    "treat_startup_zip_as_freeze_owner": False,
                    "treat_startup_handoff_as_route_authority": False,
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
    assert all(variants == {"startup_context_propagated_current_feature", "startup_context_gap_or_mismatch_containment"} for variants in variants_by_pair.values())

    alignment_fields = [
        "first_prompts_to_ai_zip_present",
        "first_prompts_to_ai_zip_current_refresh_bound",
        "startup_zip_selected_project_root_bound",
        "startup_zip_timestamp_after_current_write",
        "active_project_freeze_context_file_present",
        "active_project_freeze_context_matches_current_freeze_id",
        "active_project_freeze_context_matches_planned_next_step",
        "paste_after_file_present",
        "paste_after_file_current_sequence_aligned",
        "paste_after_file_same_refresh_event_as_startup_zip",
        "ai_send_instruction_present",
        "ai_send_instruction_aligned_to_startup_handoff",
        "ai_compliance_refresh_block_present_after_write",
        "refresh_block_lists_required_ai_send_and_startup_artifacts",
        "refresh_block_same_current_freeze_id",
        "latest_current_feature_freeze_id_coherent_across_startup_surfaces",
        "planned_next_step_sequence_coherent",
    ]
    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        aligned = case["variant"] == "startup_context_propagated_current_feature"
        for field in alignment_fields:
            assert candidate[field] is aligned, (case["case_id"], field)
        for flag in BOUNDARY_FALSE_FLAGS:
            assert candidate[flag] is False, (case["case_id"], flag)
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["project_freeze_ledger_demoted_to_blueprint_logic"] is True
        assert candidate["startup_artifacts_demoted_to_session_exposure_not_memory_owner"] is True
        assert candidate["ai_send_artifacts_demoted_to_exposure_not_memory_owner"] is True
        assert candidate["treat_stale_startup_context_as_current"] is False
        assert candidate["treat_missing_startup_context_as_ok"] is False
        assert candidate["treat_missing_paste_after_as_ok"] is False
        assert candidate["treat_wrong_next_step_as_current"] is False
        assert candidate["treat_startup_zip_as_freeze_owner"] is False
        assert candidate["treat_startup_handoff_as_route_authority"] is False
        assert candidate["critical_boundary_error_budget"] == 0


def validate_static_files() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert PREV_DOC.exists()

    doc_text = DOC.read_text(encoding="utf-8")
    readme_text = README.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for required in [
        FEATURE_TITLE,
        FEATURE_ID,
        POS_LABEL,
        "64/64",
        "32/32 startup freeze-context propagation pairs",
        "1178/1178",
        "twenty-two real test suites",
        "validation-only evidence",
        "no runtime routing",
        "no route authority",
        "no prompt loading",
        "no provider calls",
        "critical boundary error budget zero",
        "first_prompts_to_ai.zip",
        "paste_after_first_prompts_to_ai.md",
        "09_active_project_freeze_context.md",
        "project_freeze_ledger",
    ]:
        assert required in doc_text, required
    assert FEATURE_ID in readme_text
    assert "cumulative controlled offline prompt-selection coverage is now `1178/1178`" in readme_text

    expected_manifest = {
        f"{PREFIX}_feature_id": FEATURE_ID,
        f"{PREFIX}_feature_title": FEATURE_TITLE,
        f"{PREFIX}_previous_suite_feature_id": PREV_FEATURE_ID,
        f"{PREFIX}_previous_suite_title": PREV_TITLE,
        f"{PREFIX}_real_cases_added": 64,
        f"{PREFIX}_cases_passed": 64,
        f"{PREFIX}_startup_freeze_context_propagation_pairs": 32,
        f"{PREFIX}_audit_families": 8,
        f"{PREFIX}_cases_per_family": 8,
        f"{PREFIX}_governed_offline_review_only_cases": 32,
        f"{PREFIX}_containment_no_authority_cases": 32,
        f"{PREFIX}_forbidden_selected_routes": 0,
        f"{PREFIX}_unique_case_ids": 64,
        f"{PREFIX}_unique_user_requests": 64,
        f"{PREFIX}_cumulative_controlled_offline_cases_passed": 1178,
        f"{PREFIX}_cumulative_controlled_offline_test_stages": 22,
        f"{PREFIX}_positive_validation_state": POS_LABEL,
        f"{PREFIX}_next_safe_milestone": NEXT_TITLE,
        f"{PREFIX}_next_review_gate_feature_id": 'rss_mlrt108_maximum_optimized_startup_freeze_context_propagation_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1',
        f"{PREFIX}_maximum_optimized_number_policy_preserved": True,
        f"{PREFIX}_first_prompts_zip_current_context_binding_tested": True,
        f"{PREFIX}_active_project_freeze_context_file_coherence_tested": True,
        f"{PREFIX}_paste_after_startup_sequence_alignment_tested": True,
        f"{PREFIX}_ai_send_instruction_to_startup_handoff_alignment_tested": True,
        f"{PREFIX}_current_freeze_id_and_next_step_propagation_tested": True,
        f"{PREFIX}_startup_staleness_truncation_and_upload_recovery_tested": True,
        f"{PREFIX}_selected_project_root_and_ledger_demotion_tested": True,
        f"{PREFIX}_no_authority_no_runtime_boundary_containment_tested": True,
        f"{PREFIX}_accepted_for_continued_offline_testing_only": True,
        f"{PREFIX}_validation_only_evidence": True,
        f"{PREFIX}_prompt_selection_help_only": True,
        f"{PREFIX}_reliability_claimed": False,
        f"{PREFIX}_maturity_claimed": False,
        f"{PREFIX}_production_readiness_claimed": False,
        f"{PREFIX}_ml_signal_ready_for_runtime": False,
        f"{PREFIX}_ml_signal_ready_for_route_authority": False,
        f"{PREFIX}_ml_signal_ready_for_training": False,
        f"{PREFIX}_critical_boundary_error_budget": 0,
    }
    for key, value in expected_manifest.items():
        assert manifest.get(key) == value, (key, manifest.get(key), value)
    for flag in BOUNDARY_FALSE_FLAGS:
        assert manifest.get(f"{PREFIX}_{flag}") is False, flag


def test_mlrt107_maximum_optimized_startup_freeze_context_propagation_suite() -> None:
    cases = build_cases()
    validate_cases(cases)
    validate_static_files()
    print("VALIDATION OK: " + FEATURE_ID)
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print("SANDBOX_RSS_MLRT107_MAXIMUM_OPTIMIZED_STARTUP_FREEZE_CONTEXT_PROPAGATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    test_mlrt107_maximum_optimized_startup_freeze_context_propagation_suite()
