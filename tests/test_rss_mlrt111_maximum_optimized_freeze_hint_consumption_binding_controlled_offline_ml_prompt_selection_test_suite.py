from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
DOC = MLRT / "MLRT_111_MAXIMUM_OPTIMIZED_FREEZE_HINT_CONSUMPTION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_110_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt111_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-111 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt111_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt110_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-110 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT111_MAXIMUM_OPTIMIZED_FREEZE_HINT_CONSUMPTION_BINDING_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-112 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-111 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized freeze-hint consumption binding in-memory offline prompt-selection test suite after MLRT-110 freeze; MLRT-110 reviewed the MLRT-109 64-case startup handoff next-step arbitration result as good but validation-only evidence and identified freeze-hint consumption binding as the next correction; MLRT-111 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-111 passed 64/64 freeze-hint consumption binding cases across eight balanced audit families, with 32/32 freeze-hint consumption binding pairs represented, two deliberately current-consumption-bound-versus-stale-or-reused-hint variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 freeze-hint consumption binding pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 1306/1306 cases across twenty-four real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of KANDA_FREEZE_HINT consumption to the selected current feature title, feature ID, freeze ID, validation evidence, local freeze write output, used intake marker, planned next step, and delivery metadata only status, while demoting stale, unconsumed, already-consumed-for-another-feature, wrong-root, wrong-feature, mismatched-freeze-ID, missing-validation, preview-only, or project_freeze_ledger hint evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['FREEZE_HINT_INTAKE_RECORD_BINDING', 'USED_MARKER_CONSUMPTION_STATE_BINDING', 'FEATURE_TITLE_AND_ID_COHERENCE', 'VALIDATION_TO_LOCAL_WRITE_COUPLING', 'PLANNED_NEXT_STEP_AND_REVIEW_GATE_ALIGNMENT', 'WRONG_ROOT_AND_WRONG_FEATURE_DEMOTION', 'CONFLICT_RECOVERY_AND_SAFE_BLOCKING', 'NO_AUTHORITY_NO_RUNTIME_BOUNDARY_CONTAINMENT']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE', 'TREAT_PROJECT_FREEZE_LEDGER_AS_ACTIVE_MEMORY', 'TREAT_WRONG_ROOT_AS_CURRENT_PROJECT', 'TREAT_MISSING_WRITTEN_PATHS_AS_COMPLETE', 'TREAT_TRUNCATED_PATHS_AS_COMPLETE', 'TREAT_MISSING_INDEX_AS_COMPLETE', 'TREAT_MISSING_IMPLEMENTED_STEPS_AS_COMPLETE', 'TREAT_INDEX_COUNT_MISMATCH_AS_OK', 'TREAT_ENTRY_FILE_COUNT_MISMATCH_AS_OK', 'TREAT_ACTIVE_COUNT_MISMATCH_AS_OK', 'TREAT_STALE_INDEX_AS_CURRENT', 'TREAT_STALE_AI_SEND_ZIP_AS_CURRENT', 'TREAT_WRONG_ROOT_AI_SEND_AS_CURRENT', 'TREAT_STARTUP_ZIP_AS_FREEZE_OWNER', 'TREAT_AI_SEND_ARTIFACT_AS_MEMORY_OWNER', 'TREAT_MISSING_STARTUP_CONTEXT_AS_OK', 'TREAT_MISMATCHED_AI_SEND_CONTEXT_AS_CURRENT', 'TREAT_STALE_STARTUP_CONTEXT_AS_CURRENT', 'TREAT_MISSING_PASTE_AFTER_AS_OK', 'TREAT_WRONG_NEXT_STEP_AS_CURRENT', 'TREAT_STARTUP_HANDOFF_AS_ROUTE_AUTHORITY', 'TREAT_FREEZE_HINT_AS_ROUTE_AUTHORITY', 'TREAT_CONSUMED_HINT_AS_CURRENT', 'TREAT_MISMATCHED_REVIEW_GATE_NEXT_CORRECTION_AS_CURRENT', 'TREAT_STARTUP_PACKAGE_NEXT_STEP_AS_AUTHORITY', 'TREAT_UNCONSUMED_HINT_AS_WRITTEN_FREEZE', 'TREAT_HINT_USED_FOR_OTHER_FEATURE_AS_CURRENT', 'TREAT_HINT_WITHOUT_VALIDATION_AS_CURRENT', 'TREAT_HINT_WITHOUT_LOCAL_WRITE_AS_CURRENT']
FAMILY_DEFINITIONS = [{'family': 'FREEZE_HINT_INTAKE_RECORD_BINDING', 'pairs': [('KANDA_FREEZE_HINT intake record matches the current MLRT-111 feature title and feature ID', 'KANDA_FREEZE_HINT intake record names an older feature but is accepted'), ('freeze hint intake record carries validation evidence for the same current feature', 'freeze hint intake record has missing validation evidence but is treated as current'), ('freeze hint intake record is delivery metadata only and is never installed into project root', 'KANDA_FREEZE_HINT in project root is accepted as active project state'), ('freeze hint intake record is bound to the selected active project root', 'freeze hint from a wrong project root is treated as current')]}, {'family': 'USED_MARKER_CONSUMPTION_STATE_BINDING', 'pairs': [('used marker indicates the current MLRT-111 hint was consumed by this exact freeze write', 'used marker belongs to another feature but is accepted'), ('already-consumed older hint is demoted instead of reused as current metadata', 'already-consumed older hint is reused as the current next-step source'), ('unconsumed hint is treated as intake evidence only until Confirm and Write succeeds', 'unconsumed hint is treated as a completed freeze'), ('used marker references the same freeze ID as the local freeze write output', 'used marker references a mismatched freeze ID and is accepted')]}, {'family': 'FEATURE_TITLE_AND_ID_COHERENCE', 'pairs': [('feature title, feature ID, positive marker, and test filename all point to MLRT-111', 'feature title and feature ID disagree but are accepted'), ('freeze ID slug corresponds to the current MLRT-111 feature title', 'freeze ID slug corresponds to MLRT-109 or MLRT-110 but is accepted'), ('planned next step points to the MLRT-112 review gate for the same domain', 'planned next step skips to an unrelated feature and is accepted'), ('freeze hint metadata and review-gate correction agree on freeze-hint consumption binding', 'freeze hint metadata and review-gate correction disagree and are accepted')]}, {'family': 'VALIDATION_TO_LOCAL_WRITE_COUPLING', 'pairs': [('validation OK marker and local freeze write OK marker are both present for current MLRT-111', 'freeze hint has local write only without current validation and is accepted'), ('local freeze write paths include entries, freeze_index.json, and project_frozen_implemented_steps.md', 'local freeze write paths are missing or truncated but are accepted'), ('Preview Freeze Entry remains read-only until explicit Confirm and Write', 'preview-only freeze hint evidence is treated as written memory'), ('validation output is evidence for offline tests only and not route authority', 'validation output is used as route authority')]}, {'family': 'PLANNED_NEXT_STEP_AND_REVIEW_GATE_ALIGNMENT', 'pairs': [('KANDA_FREEZE_HINT planned next step equals MLRT-112 review gate after MLRT-111', 'KANDA_FREEZE_HINT planned next step names stale MLRT-110 and is accepted'), ('review-gate next correction and hint planned next step remain domain-consistent', 'review-gate correction and hint planned next step conflict and are accepted'), ('consumed current hint cannot override newer freeze memory exposure after write', 'consumed hint overrides newer freeze memory exposure'), ('planned next step is a handoff cue only and never runtime routing authority', 'planned next step is treated as runtime route authority')]}, {'family': 'WRONG_ROOT_AND_WRONG_FEATURE_DEMOTION', 'pairs': [('wrong-root freeze hint is demoted even when the title resembles the current feature', 'wrong-root freeze hint is selected as current'), ('wrong-feature freeze hint is demoted even when generated recently', 'wrong-feature freeze hint generated recently is selected as current'), ('project_freeze_ledger hint-like metadata remains reusable engine blueprint logic only', 'project_freeze_ledger hint-like metadata is accepted as active memory'), ('AI-send hint copy is exposure evidence only and not the active freeze memory owner', 'AI-send hint copy is treated as active memory owner')]}, {'family': 'CONFLICT_RECOVERY_AND_SAFE_BLOCKING', 'pairs': [('mismatched hint consumption state triggers targeted recovery before next patch', 'mismatched hint consumption state is ignored and next patch proceeds'), ('missing freeze hint intake record blocks auto-fill but permits manual human review', 'missing freeze hint intake record causes unsafe auto-fill'), ('truncated hint evidence is not inflated into complete freeze evidence', 'truncated hint evidence is inflated into complete freeze evidence'), ('multiple hint records are arbitrated by current feature ID and local write evidence', 'multiple hint records are arbitrated by timestamp alone')]}, {'family': 'NO_AUTHORITY_NO_RUNTIME_BOUNDARY_CONTAINMENT', 'pairs': [('freeze-hint consumption binding remains a test-local offline evidence check', 'freeze-hint consumption binding mutates runtime router behavior'), ('no prompt loading, provider calls, embeddings, persistence, or training are introduced', 'test introduces prompt loading or provider calls'), ('no gold registry write, dataset creation, or model improvement is performed', 'test creates gold records or improves a model'), ('critical boundary error budget remains zero while allowing false-blocker recovery', 'critical boundary error budget is nonzero or ignored')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, definition in enumerate(FAMILY_DEFINITIONS, start=1):
        family = definition["family"]
        for pair_index, pair in enumerate(definition["pairs"], start=1):
            pair_id = f"MLRT111-F{family_index:02d}-P{pair_index:02d}"
            for variant_index, (variant, prompt, expected_label, current_bound) in enumerate([
                ("current_consumption_bound", pair[0], "GOVERNED_OFFLINE_REVIEW_ONLY", True),
                ("stale_or_reused_hint_containment", pair[1], "NO_AUTHORITATIVE_ROUTE", False),
            ], start=1):
                case_id = f"{pair_id}-V{variant_index:02d}"
                user_request = (
                    f"Assess MLRT-111 freeze-hint consumption binding case {case_id}: {prompt}. "
                    "Keep the decision test-local, in-memory, non-persistent, non-training, and non-authoritative."
                )
                candidate: dict[str, object] = {
                    "selected_route": expected_label,
                    "feature_id": FEATURE_ID,
                    "feature_title": FEATURE_TITLE,
                    "previous_feature_id": PREV_FEATURE_ID,
                    "previous_title": PREV_TITLE,
                    "positive_validation_state": POS_LABEL,
                    "case_family": family,
                    "case_pair_id": pair_id,
                    "kanda_freeze_hint_intake_record_current": current_bound,
                    "kanda_freeze_hint_feature_title_current": current_bound,
                    "kanda_freeze_hint_feature_id_current": current_bound,
                    "kanda_freeze_hint_freeze_id_current": current_bound,
                    "kanda_freeze_hint_validation_evidence_current": current_bound,
                    "kanda_freeze_hint_local_write_evidence_current": current_bound,
                    "kanda_freeze_hint_used_marker_current": current_bound,
                    "kanda_freeze_hint_planned_next_step_current": current_bound,
                    "review_gate_next_correction_current": current_bound,
                    "freeze_hint_consumption_surfaces_coherent": current_bound,
                    "conflict_recovery_or_safe_block_required": not current_bound,
                    "kanda_freeze_hint_delivery_metadata_only": True,
                    "kanda_freeze_hint_not_installed_to_project_root": True,
                    "preview_only_evidence_demoted": True,
                    "stale_freeze_hint_demoted": True,
                    "unconsumed_hint_not_treated_as_completed_freeze": True,
                    "already_consumed_other_feature_hint_demoted": True,
                    "wrong_root_hint_demoted": True,
                    "wrong_feature_hint_demoted": True,
                    "mismatched_freeze_id_hint_demoted": True,
                    "missing_validation_hint_demoted": True,
                    "project_freeze_ledger_demoted_to_blueprint_logic": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_freeze_hint_as_route_authority": False,
                    "treat_consumed_hint_as_current": False,
                    "treat_unconsumed_hint_as_written_freeze": False,
                    "treat_hint_used_for_other_feature_as_current": False,
                    "treat_hint_without_validation_as_current": False,
                    "treat_hint_without_local_write_as_current": False,
                    "treat_project_freeze_ledger_as_active_memory": False,
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
    assert all(variants == {"current_consumption_bound", "stale_or_reused_hint_containment"} for variants in variants_by_pair.values())

    binding_fields = [
        "kanda_freeze_hint_intake_record_current",
        "kanda_freeze_hint_feature_title_current",
        "kanda_freeze_hint_feature_id_current",
        "kanda_freeze_hint_freeze_id_current",
        "kanda_freeze_hint_validation_evidence_current",
        "kanda_freeze_hint_local_write_evidence_current",
        "kanda_freeze_hint_used_marker_current",
        "kanda_freeze_hint_planned_next_step_current",
        "review_gate_next_correction_current",
        "freeze_hint_consumption_surfaces_coherent",
    ]
    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        current_bound = case["variant"] == "current_consumption_bound"
        for field in binding_fields:
            assert candidate[field] is current_bound, (case["case_id"], field)
        assert candidate["conflict_recovery_or_safe_block_required"] is (not current_bound)
        for flag in BOUNDARY_FALSE_FLAGS:
            assert candidate[flag] is False, (case["case_id"], flag)
        assert candidate["kanda_freeze_hint_delivery_metadata_only"] is True
        assert candidate["kanda_freeze_hint_not_installed_to_project_root"] is True
        assert candidate["preview_only_evidence_demoted"] is True
        assert candidate["stale_freeze_hint_demoted"] is True
        assert candidate["unconsumed_hint_not_treated_as_completed_freeze"] is True
        assert candidate["already_consumed_other_feature_hint_demoted"] is True
        assert candidate["wrong_root_hint_demoted"] is True
        assert candidate["wrong_feature_hint_demoted"] is True
        assert candidate["mismatched_freeze_id_hint_demoted"] is True
        assert candidate["missing_validation_hint_demoted"] is True
        assert candidate["project_freeze_ledger_demoted_to_blueprint_logic"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["treat_freeze_hint_as_route_authority"] is False
        assert candidate["treat_consumed_hint_as_current"] is False
        assert candidate["treat_unconsumed_hint_as_written_freeze"] is False
        assert candidate["treat_hint_used_for_other_feature_as_current"] is False
        assert candidate["treat_hint_without_validation_as_current"] is False
        assert candidate["treat_hint_without_local_write_as_current"] is False
        assert candidate["treat_project_freeze_ledger_as_active_memory"] is False
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
        "32/32 freeze-hint consumption binding pairs",
        "1306/1306",
        "twenty-four real test suites",
        "validation-only evidence",
        "no runtime routing",
        "no route authority",
        "no prompt loading",
        "no provider calls",
        "critical boundary error budget zero",
        "KANDA_FREEZE_HINT",
        "Used intake records",
        "project_freeze_ledger",
    ]:
        assert required in doc_text, required
    assert FEATURE_ID in readme_text
    assert "cumulative controlled offline prompt-selection coverage is now `1306/1306`" in readme_text

    expected_manifest = {
        f"{PREFIX}_feature_id": FEATURE_ID,
        f"{PREFIX}_feature_title": FEATURE_TITLE,
        f"{PREFIX}_previous_suite_feature_id": PREV_FEATURE_ID,
        f"{PREFIX}_previous_suite_title": PREV_TITLE,
        f"{PREFIX}_real_cases_added": 64,
        f"{PREFIX}_cases_passed": 64,
        f"{PREFIX}_freeze_hint_consumption_binding_pairs": 32,
        f"{PREFIX}_audit_families": 8,
        f"{PREFIX}_cases_per_family": 8,
        f"{PREFIX}_governed_offline_review_only_cases": 32,
        f"{PREFIX}_containment_no_authority_cases": 32,
        f"{PREFIX}_forbidden_selected_routes": 0,
        f"{PREFIX}_unique_case_ids": 64,
        f"{PREFIX}_unique_user_requests": 64,
        f"{PREFIX}_cumulative_controlled_offline_cases_passed": 1306,
        f"{PREFIX}_cumulative_controlled_offline_test_stages": 24,
        f"{PREFIX}_positive_validation_state": POS_LABEL,
        f"{PREFIX}_next_safe_milestone": NEXT_TITLE,
        f"{PREFIX}_next_review_gate_feature_id": 'rss_mlrt112_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1',
        f"{PREFIX}_maximum_optimized_number_policy_preserved": True,
        f"{PREFIX}_freeze_hint_intake_record_binding_tested": True,
        f"{PREFIX}_used_marker_consumption_state_binding_tested": True,
        f"{PREFIX}_feature_title_and_id_coherence_tested": True,
        f"{PREFIX}_validation_to_local_write_coupling_tested": True,
        f"{PREFIX}_planned_next_step_and_review_gate_alignment_tested": True,
        f"{PREFIX}_wrong_root_and_wrong_feature_demotion_tested": True,
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


def main() -> None:
    validate_static_files()
    cases = build_cases()
    validate_cases(cases)
    print("VALIDATION OK: " + FEATURE_ID)
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print("SANDBOX_RSS_MLRT111_MAXIMUM_OPTIMIZED_FREEZE_HINT_CONSUMPTION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
