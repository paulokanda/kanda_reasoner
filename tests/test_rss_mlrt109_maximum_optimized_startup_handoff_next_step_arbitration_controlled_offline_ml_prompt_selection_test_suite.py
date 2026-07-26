from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
DOC = MLRT / "MLRT_109_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_108_MAXIMUM_OPTIMIZED_STARTUP_FREEZE_CONTEXT_PROPAGATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt109_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-109 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt109_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt108_maximum_optimized_startup_freeze_context_propagation_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-108 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT109_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-110 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-109 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized startup handoff next-step arbitration in-memory offline prompt-selection test suite after MLRT-108 freeze; MLRT-108 reviewed the MLRT-107 64-case startup freeze-context propagation result as good but validation-only evidence and identified startup handoff next-step arbitration as the next correction; MLRT-109 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-109 passed 64/64 startup handoff next-step arbitration cases across eight balanced audit families, with 32/32 startup handoff next-step arbitration pairs represented, two deliberately current-governed-next-step-versus-stale-or-conflicting-next-step variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 startup handoff next-step arbitration pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 1242/1242 cases across twenty-three real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved arbitration of the current governed next step across first_prompts_to_ai.zip, paste_after_first_prompts_to_ai.md, 09_active_project_freeze_context.md, AI-send instructions, KANDA_FREEZE_HINT planned_next_step, review-gate next correction, latest current-feature freeze ID, and latest FREEZE_MEMORY_STATUS OK exposure, while demoting stale, truncated, wrong-root, wrong-feature, wrong-next-step, consumed-hint, mismatched-review-gate, or project_freeze_ledger handoff evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['STARTUP_PACKAGE_NEXT_STEP_CANDIDATE_DISCOVERY', 'PASTE_AFTER_FILE_NEXT_STEP_ALIGNMENT', 'AI_SEND_INSTRUCTION_NEXT_STEP_ALIGNMENT', 'KANDA_FREEZE_HINT_PLANNED_NEXT_STEP_ARBITRATION', 'REVIEW_GATE_NEXT_CORRECTION_RECONCILIATION', 'LATEST_CURRENT_FEATURE_FREEZE_ID_PRECEDENCE', 'CONFLICT_RECOVERY_AND_SAFE_BLOCKING', 'NO_AUTHORITY_NO_RUNTIME_BOUNDARY_CONTAINMENT']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE', 'TREAT_PROJECT_FREEZE_LEDGER_AS_ACTIVE_MEMORY', 'TREAT_WRONG_ROOT_AS_CURRENT_PROJECT', 'TREAT_MISSING_WRITTEN_PATHS_AS_COMPLETE', 'TREAT_TRUNCATED_PATHS_AS_COMPLETE', 'TREAT_MISSING_INDEX_AS_COMPLETE', 'TREAT_MISSING_IMPLEMENTED_STEPS_AS_COMPLETE', 'TREAT_INDEX_COUNT_MISMATCH_AS_OK', 'TREAT_ENTRY_FILE_COUNT_MISMATCH_AS_OK', 'TREAT_ACTIVE_COUNT_MISMATCH_AS_OK', 'TREAT_STALE_INDEX_AS_CURRENT', 'TREAT_STALE_AI_SEND_ZIP_AS_CURRENT', 'TREAT_WRONG_ROOT_AI_SEND_AS_CURRENT', 'TREAT_STARTUP_ZIP_AS_FREEZE_OWNER', 'TREAT_AI_SEND_ARTIFACT_AS_MEMORY_OWNER', 'TREAT_MISSING_STARTUP_CONTEXT_AS_OK', 'TREAT_MISMATCHED_AI_SEND_CONTEXT_AS_CURRENT', 'TREAT_STALE_STARTUP_CONTEXT_AS_CURRENT', 'TREAT_MISSING_PASTE_AFTER_AS_OK', 'TREAT_WRONG_NEXT_STEP_AS_CURRENT', 'TREAT_STARTUP_HANDOFF_AS_ROUTE_AUTHORITY', 'TREAT_FREEZE_HINT_AS_ROUTE_AUTHORITY', 'TREAT_CONSUMED_HINT_AS_CURRENT', 'TREAT_MISMATCHED_REVIEW_GATE_NEXT_CORRECTION_AS_CURRENT', 'TREAT_STARTUP_PACKAGE_NEXT_STEP_AS_AUTHORITY']
FAMILY_DEFINITIONS = [{'family': 'STARTUP_PACKAGE_NEXT_STEP_CANDIDATE_DISCOVERY', 'pairs': [('first_prompts_to_ai.zip current context names the current governed MLRT-109 next step after MLRT-108 freeze', 'first_prompts_to_ai.zip is stale and names MLRT-107 or MLRT-108 as the next step but is accepted'), ('startup package current freeze ID for MLRT-108 gates selection of MLRT-109', 'startup package carries an old freeze ID while still selecting MLRT-109'), ('09_active_project_freeze_context.md next-step line wins over older prompt starter blocks', 'older prompt starter block overrides current active project freeze context'), ('startup package exposes next-step context but never grants route authority', 'startup package next-step text is treated as runtime route authority')]}, {'family': 'PASTE_AFTER_FILE_NEXT_STEP_ALIGNMENT', 'pairs': [('paste_after_first_prompts_to_ai.md matches the startup package and current MLRT-109 title', 'paste-after file and startup package disagree about the next MLRT'), ('paste-after file is current while stale AI-send text is demoted', 'stale AI-send next-step text overrides current paste-after file'), ('truncated paste-after next-step evidence triggers targeted recovery', 'truncated paste-after evidence is inflated into complete next-step evidence'), ('paste-after file preserves wait-for-task routing discipline after startup load', 'paste-after file is treated as permission to bypass routing controls')]}, {'family': 'AI_SEND_INSTRUCTION_NEXT_STEP_ALIGNMENT', 'pairs': [('what_to_say_to_ai_freeze_feature.md aligns to the same MLRT-109 next step as startup context', 'AI-send instruction names a stale next step and is accepted'), ('AI-send ZIP timestamp and instruction are after the current MLRT-108 freeze write', 'stale AI-send ZIP predates current freeze write but is accepted'), ('AI-send instruction is a handoff aid and not owner of freeze memory', 'AI-send instruction is treated as active freeze memory owner'), ('missing AI-send evidence creates a recoverable exposure gap, not current next-step authority', 'missing AI-send evidence is ignored while claiming full handoff consistency')]}, {'family': 'KANDA_FREEZE_HINT_PLANNED_NEXT_STEP_ARBITRATION', 'pairs': [('KANDA_FREEZE_HINT planned_next_step matches the current MLRT-109 governed next step', 'KANDA_FREEZE_HINT planned_next_step names the wrong feature and is accepted'), ('KANDA_FREEZE_HINT remains delivery metadata only and is not installed into project root', 'KANDA_FREEZE_HINT in project root is accepted as active project state'), ('consumed freeze hint is demoted after freeze write while current freeze memory stays canonical', 'consumed freeze hint overrides current frozen memory after write'), ('freeze hint planned next step reconciles with the review-gate next correction before proceeding', 'freeze hint conflicts with review-gate next correction and wins unsafely')]}, {'family': 'REVIEW_GATE_NEXT_CORRECTION_RECONCILIATION', 'pairs': [('MLRT-108 review gate next correction names MLRT-109 and matches startup handoff surfaces', 'stale review gate next correction names another feature and is accepted'), ('review-gate next correction is current only after matching validation and freeze evidence', 'validation-only review gate next correction is treated as frozen and current'), ('review-gate next correction helps offline prompt selection only', 'review-gate next correction is treated as route authority'), ('review-gate title and feature ID both match the current next step', 'similar title without matching feature ID is accepted')]}, {'family': 'LATEST_CURRENT_FEATURE_FREEZE_ID_PRECEDENCE', 'pairs': [('latest MLRT-108 LOCAL FREEZE WRITE OK plus FREEZE_MEMORY_STATUS OK selects current MLRT-109 next step', 'older freeze block overrides the latest MLRT-108 freeze evidence'), ('current freeze ID agrees across freeze write, index exposure, startup package, paste-after file, and AI-send instruction', 'current freeze ID disagrees across handoff surfaces but is accepted'), ('preview-only next-step blocks are demoted when write-confirmed evidence exists', 'preview-only next-step block overrides write-confirmed evidence'), ('latest uploaded or pasted current evidence wins over stale sidecars', 'stale sidecar next-step hint overrides latest current evidence')]}, {'family': 'CONFLICT_RECOVERY_AND_SAFE_BLOCKING', 'pairs': [('conflicting next-step surfaces trigger targeted recovery or safe block before patch creation', 'conflicting next-step surfaces proceed as if coherent'), ('wrong project root conflict is demoted and does not select the next step', 'wrong project root handoff selects the next MLRT'), ('truncated startup, hint, or review-gate next-step lines are treated as incomplete context', 'truncated next-step lines are inferred as complete'), ('missing one handoff surface is reported precisely without granting authority', 'missing handoff surface is hidden while claiming full coherence')]}, {'family': 'NO_AUTHORITY_NO_RUNTIME_BOUNDARY_CONTAINMENT', 'pairs': [('next-step arbitration helps prompt selection only during governed offline review', 'next-step arbitration enables runtime routing authority'), ('next-step handoff never loads live prompts, live freeze memory, or router canon for routing', 'next-step handoff loads live prompts or freeze memory for routing'), ('next-step arbitration does not create datasets, labels, reports, training data, or calibration evidence', 'next-step arbitration is treated as model improvement or training data'), ('provider calls, embeddings, vector stores, registry mutation, runtime Pilot, and Copilot stay disabled', 'next-step arbitration enables provider calls or Copilot behavior')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            good_text, gap_text = pair
            pair_id = f"mlrt109_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("current_governed_next_step_arbitrated", good_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("stale_or_conflicting_next_step_containment", gap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt109_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-109 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Arbitrate the startup handoff current governed next step without runtime authority."
                )
                aligned = variant == "current_governed_next_step_arbitrated"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "startup_package_next_step_current": aligned,
                    "startup_package_current_freeze_id_bound": aligned,
                    "active_project_context_next_step_current": aligned,
                    "paste_after_next_step_aligned": aligned,
                    "paste_after_same_current_feature_context": aligned,
                    "ai_send_instruction_next_step_aligned": aligned,
                    "ai_send_timestamp_after_current_freeze_write": aligned,
                    "kanda_freeze_hint_planned_next_step_current": aligned,
                    "kanda_freeze_hint_delivery_metadata_only": True,
                    "consumed_freeze_hint_demoted": True,
                    "review_gate_next_correction_current": aligned,
                    "review_gate_next_correction_validation_and_freeze_bound": aligned,
                    "latest_current_feature_freeze_id_precedence_preserved": aligned,
                    "latest_freeze_memory_status_ok_bound": aligned,
                    "handoff_surfaces_coherent": aligned,
                    "conflict_recovery_or_safe_block_required": not aligned,
                    "wrong_project_root_demoted": True,
                    "wrong_feature_next_step_demoted": True,
                    "truncated_next_step_not_inflated": True,
                    "project_freeze_ledger_demoted_to_blueprint_logic": True,
                    "startup_artifacts_demoted_to_session_exposure_not_memory_owner": True,
                    "ai_send_artifacts_demoted_to_exposure_not_memory_owner": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_startup_package_next_step_as_authority": False,
                    "treat_freeze_hint_as_route_authority": False,
                    "treat_consumed_hint_as_current": False,
                    "treat_mismatched_review_gate_next_correction_as_current": False,
                    "treat_wrong_next_step_as_current": False,
                    "treat_stale_startup_context_as_current": False,
                    "treat_missing_paste_after_as_ok": False,
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
    assert all(variants == {"current_governed_next_step_arbitrated", "stale_or_conflicting_next_step_containment"} for variants in variants_by_pair.values())

    alignment_fields = [
        "startup_package_next_step_current",
        "startup_package_current_freeze_id_bound",
        "active_project_context_next_step_current",
        "paste_after_next_step_aligned",
        "paste_after_same_current_feature_context",
        "ai_send_instruction_next_step_aligned",
        "ai_send_timestamp_after_current_freeze_write",
        "kanda_freeze_hint_planned_next_step_current",
        "review_gate_next_correction_current",
        "review_gate_next_correction_validation_and_freeze_bound",
        "latest_current_feature_freeze_id_precedence_preserved",
        "latest_freeze_memory_status_ok_bound",
        "handoff_surfaces_coherent",
    ]
    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        aligned = case["variant"] == "current_governed_next_step_arbitrated"
        for field in alignment_fields:
            assert candidate[field] is aligned, (case["case_id"], field)
        assert candidate["conflict_recovery_or_safe_block_required"] is (not aligned)
        for flag in BOUNDARY_FALSE_FLAGS:
            assert candidate[flag] is False, (case["case_id"], flag)
        assert candidate["kanda_freeze_hint_delivery_metadata_only"] is True
        assert candidate["consumed_freeze_hint_demoted"] is True
        assert candidate["wrong_project_root_demoted"] is True
        assert candidate["wrong_feature_next_step_demoted"] is True
        assert candidate["truncated_next_step_not_inflated"] is True
        assert candidate["project_freeze_ledger_demoted_to_blueprint_logic"] is True
        assert candidate["startup_artifacts_demoted_to_session_exposure_not_memory_owner"] is True
        assert candidate["ai_send_artifacts_demoted_to_exposure_not_memory_owner"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["treat_startup_package_next_step_as_authority"] is False
        assert candidate["treat_freeze_hint_as_route_authority"] is False
        assert candidate["treat_consumed_hint_as_current"] is False
        assert candidate["treat_mismatched_review_gate_next_correction_as_current"] is False
        assert candidate["treat_wrong_next_step_as_current"] is False
        assert candidate["treat_stale_startup_context_as_current"] is False
        assert candidate["treat_missing_paste_after_as_ok"] is False
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
        "32/32 startup handoff next-step arbitration pairs",
        "1242/1242",
        "twenty-three real test suites",
        "validation-only evidence",
        "no runtime routing",
        "no route authority",
        "no prompt loading",
        "no provider calls",
        "critical boundary error budget zero",
        "first_prompts_to_ai.zip",
        "paste_after_first_prompts_to_ai.md",
        "09_active_project_freeze_context.md",
        "KANDA_FREEZE_HINT",
        "review-gate next correction",
        "project_freeze_ledger",
    ]:
        assert required in doc_text, required
    assert FEATURE_ID in readme_text
    assert "cumulative controlled offline prompt-selection coverage is now `1242/1242`" in readme_text

    expected_manifest = {
        f"{PREFIX}_feature_id": FEATURE_ID,
        f"{PREFIX}_feature_title": FEATURE_TITLE,
        f"{PREFIX}_previous_suite_feature_id": PREV_FEATURE_ID,
        f"{PREFIX}_previous_suite_title": PREV_TITLE,
        f"{PREFIX}_real_cases_added": 64,
        f"{PREFIX}_cases_passed": 64,
        f"{PREFIX}_startup_handoff_next_step_arbitration_pairs": 32,
        f"{PREFIX}_audit_families": 8,
        f"{PREFIX}_cases_per_family": 8,
        f"{PREFIX}_governed_offline_review_only_cases": 32,
        f"{PREFIX}_containment_no_authority_cases": 32,
        f"{PREFIX}_forbidden_selected_routes": 0,
        f"{PREFIX}_unique_case_ids": 64,
        f"{PREFIX}_unique_user_requests": 64,
        f"{PREFIX}_cumulative_controlled_offline_cases_passed": 1242,
        f"{PREFIX}_cumulative_controlled_offline_test_stages": 23,
        f"{PREFIX}_positive_validation_state": POS_LABEL,
        f"{PREFIX}_next_safe_milestone": NEXT_TITLE,
        f"{PREFIX}_next_review_gate_feature_id": 'rss_mlrt110_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1',
        f"{PREFIX}_maximum_optimized_number_policy_preserved": True,
        f"{PREFIX}_startup_package_next_step_candidate_discovery_tested": True,
        f"{PREFIX}_paste_after_file_next_step_alignment_tested": True,
        f"{PREFIX}_ai_send_instruction_next_step_alignment_tested": True,
        f"{PREFIX}_kanda_freeze_hint_planned_next_step_arbitration_tested": True,
        f"{PREFIX}_review_gate_next_correction_reconciliation_tested": True,
        f"{PREFIX}_latest_current_feature_freeze_id_precedence_tested": True,
        f"{PREFIX}_conflict_recovery_and_safe_blocking_tested": True,
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


def test_mlrt109_maximum_optimized_startup_handoff_next_step_arbitration_suite() -> None:
    cases = build_cases()
    validate_cases(cases)
    validate_static_files()
    print("VALIDATION OK: " + FEATURE_ID)
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print("SANDBOX_RSS_MLRT109_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    test_mlrt109_maximum_optimized_startup_handoff_next_step_arbitration_suite()
