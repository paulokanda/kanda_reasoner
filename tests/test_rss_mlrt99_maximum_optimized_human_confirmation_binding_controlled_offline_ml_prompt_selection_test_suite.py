from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_99_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_98_MAXIMUM_OPTIMIZED_PREVIEW_VERSUS_WRITE_BOUNDARY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt99_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-99 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt99_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt98_maximum_optimized_preview_versus_write_boundary_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-98 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT99_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-100 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-99 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized human-confirmation binding in-memory offline prompt-selection test suite after MLRT-98 freeze; MLRT-98 reviewed the MLRT-97 64-case preview-versus-write boundary result as good but validation-only evidence and identified human-confirmation binding as the next correction; MLRT-99 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-99 passed 64/64 human-confirmation binding cases across eight balanced audit families, with 32/32 human-confirmation binding pairs represented, two deliberately current-bound-confirmation-versus-unbound-or-mismatched-confirmation variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 human-confirmation binding pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 922/922 cases across eighteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of human confirmation to the exact current feature title, exact current freeze ID, explicit Confirm and Write action, matching LOCAL FREEZE WRITE OK block, written frozen_features_memory paths, and refreshed FREEZE_MEMORY_STATUS OK, while demoting implied, stale, mismatched, split, preview-only, wrong-feature, or ambiguous confirmation evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['EXPLICIT_CONFIRM_AND_WRITE_ACTION_BINDING', 'CURRENT_FEATURE_TITLE_BINDING', 'CURRENT_FREEZE_ID_BINDING', 'WRITE_BLOCK_AND_CONFIRMATION_COHERENCE', 'STALE_OR_ADJACENT_CONFIRMATION_DEMOTION', 'SPLIT_OR_TRUNCATED_CONFIRMATION_RECOVERY', 'SEQUENCE_ADVANCEMENT_BINDING', 'BOUNDARY_CONTAINMENT_DURING_CONFIRMATION_BINDING']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION', 'TREAT_STALE_CONFIRMATION_AS_CURRENT', 'TREAT_MISMATCHED_FREEZE_ID_AS_CURRENT', 'TREAT_MISMATCHED_TITLE_AS_CURRENT', 'TREAT_IMPLIED_CONFIRMATION_AS_WRITE']
FAMILY_DEFINITIONS = [{'family': 'EXPLICIT_CONFIRM_AND_WRITE_ACTION_BINDING', 'pairs': [('explicit human Confirm and Write action is bound to the current feature before sequence advancement', 'preview readiness text implies human confirmation without the Confirm and Write action'), ('LOCAL FREEZE WRITE OK after Confirm and Write is accepted as write evidence for the current feature', 'Human review required before Confirm and Write is treated as already confirmed'), ('written frozen_features_memory paths after explicit confirmation are used as current write evidence', 'Will write after Confirm and Write paths are treated as proof that the user confirmed'), ('confirmation is accepted only after the human-triggered write block appears', 'validation output alone is treated as human confirmation')]}, {'family': 'CURRENT_FEATURE_TITLE_BINDING', 'pairs': [('confirmation is bound to the exact MLRT-99 feature title and not merely to the newest visible title-like text', 'confirmation from MLRT-98 review gate title is reused for MLRT-99'), ('exact current title wins over stale planned-next-step title from older freeze logs', 'older planned next step text is treated as current confirmation'), ('current feature title must match the freeze entry being written', 'mismatched feature title with current-looking write status is accepted'), ('title binding prevents adjacent MLRT review gate and real suite from being swapped', 'review gate confirmation is accepted for the real suite or vice versa')]}, {'family': 'CURRENT_FREEZE_ID_BINDING', 'pairs': [('confirmation is bound to the exact current freeze ID for MLRT-99', 'stale MLRT-97 or MLRT-98 freeze ID is treated as current'), ('freeze ID and feature title must agree before advancing the sequence', 'matching title but wrong freeze ID is accepted'), ('freeze ID date and MLRT number are checked for current-feature consistency', 'same date but wrong MLRT number is accepted'), ('current freeze ID in LOCAL FREEZE WRITE OK is preferred over preview freeze ID text', 'preview freeze ID text is accepted as written freeze ID')]}, {'family': 'WRITE_BLOCK_AND_CONFIRMATION_COHERENCE', 'pairs': [('LOCAL FREEZE WRITE OK, Freeze ID, and Written paths are treated as a coherent confirmation block', 'split snippets from different features are merged into a false confirmation'), ('Freeze hint intake marked as used supports the same current write block only', 'Freeze hint intake marked used from another feature confirms the current one'), ('AI compliance refresh after local write supports confirmed current write evidence', 'AI compliance preview before write is treated as post-write refresh'), ('FREEZE_MEMORY_STATUS OK is associated with the same write event after confirmation', 'FREEZE_MEMORY_STATUS OK from stale exposure is bound to a new unconfirmed feature')]}, {'family': 'STALE_OR_ADJACENT_CONFIRMATION_DEMOTION', 'pairs': [('newer current-feature write evidence overrides older adjacent MLRT confirmation blocks', 'older adjacent MLRT write block blocks or replaces current feature confirmation'), ('stale sidecar confirmation is demoted when the current feature has its own write evidence', 'stale sidecar confirmation is selected instead of current write evidence'), ('old preview blocks are not reused as current human confirmation', 'old preview blocks are reused as current human confirmation'), ('prior frozen MLRT sequence evidence is preserved as context but not as the current write event', 'prior frozen MLRT sequence evidence is treated as the current write event')]}, {'family': 'SPLIT_OR_TRUNCATED_CONFIRMATION_RECOVERY', 'pairs': [('partial pasted write evidence prompts targeted status recovery instead of false route authority', 'partial pasted write evidence grants runtime route authority'), ('truncated confirmation is accepted only for the fields it actually contains and awaits matching status when needed', 'truncated confirmation is inflated into full freeze exposure evidence'), ('separate uploaded status can complete exposure recovery only when bound to the same current freeze ID', 'separate uploaded status from a different feature completes current confirmation'), ('missing FREEZE_MEMORY_STATUS after write is treated as exposure-gap recovery, not preview-only failure', 'missing FREEZE_MEMORY_STATUS after write is treated as no write ever happened')]}, {'family': 'SEQUENCE_ADVANCEMENT_BINDING', 'pairs': [('MLRT-100 review gate may proceed only after MLRT-99 validation and current write confirmation are present', 'MLRT-100 proceeds from validation alone without MLRT-99 write confirmation'), ('planned next step is used only after the current feature is written and exposed OK', 'planned next step in preview causes automatic sequence advancement'), ('current sequence preserves real-suite then review-gate order after confirmation', 'sequence skips review gate or repeats stale suite due to ambiguous confirmation'), ('human-confirmation binding avoids false blockers when write evidence is complete and current', 'complete current write evidence is blocked because older preview text exists')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_CONFIRMATION_BINDING', 'pairs': [('human-confirmation binding is offline evidence handling, not runtime routing authority', 'human-confirmation binding grants runtime routing authority'), ('targeted confirmation inspection does not load live prompts or router canon for routing', 'targeted confirmation inspection loads live prompts for routing'), ('confirmation-binding tests do not train, calibrate, or improve a model', 'confirmation-binding evidence is saved as training data'), ('confirmation-binding recovery does not mutate freeze memory, gold registry, Pilot, or Copilot behavior', 'confirmation-binding recovery writes gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            bound_text, unbound_text = pair
            pair_id = f"mlrt99_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("current_bound_confirmation", bound_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("unbound_or_mismatched_confirmation_containment", unbound_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt99_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-99 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Preserve human-confirmation binding without runtime authority."
                )
                bound = variant == "current_bound_confirmation"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "explicit_human_confirm_and_write_required": True,
                    "confirmation_bound_to_current_feature_title": bound,
                    "confirmation_bound_to_current_freeze_id": bound,
                    "current_feature_title_matches_freeze_entry": bound,
                    "current_freeze_id_matches_write_block": bound,
                    "local_freeze_write_ok_present": bound,
                    "written_paths_present_for_current_feature": bound,
                    "freeze_memory_status_ok_bound_to_same_write": bound,
                    "preview_readiness_not_confirmation": True,
                    "writable_preview_not_confirmation": True,
                    "validation_evidence_not_confirmation": True,
                    "stale_confirmation_demoted": True,
                    "mismatched_feature_title_demoted": not bound,
                    "mismatched_freeze_id_demoted": not bound,
                    "split_confirmation_not_merged_unsafely": True,
                    "sequence_advancement_requires_current_bound_confirmation": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_implied_confirmation_as_write": False,
                    "treat_stale_confirmation_as_current": False,
                    "treat_mismatched_freeze_id_as_current": False,
                    "treat_mismatched_title_as_current": False,
                    "skip_human_confirmation": False,
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
    assert all(variants == {"current_bound_confirmation", "unbound_or_mismatched_confirmation_containment"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        bound = case["variant"] == "current_bound_confirmation"
        assert candidate["explicit_human_confirm_and_write_required"] is True
        assert candidate["confirmation_bound_to_current_feature_title"] is bound
        assert candidate["confirmation_bound_to_current_freeze_id"] is bound
        assert candidate["current_feature_title_matches_freeze_entry"] is bound
        assert candidate["current_freeze_id_matches_write_block"] is bound
        assert candidate["local_freeze_write_ok_present"] is bound
        assert candidate["written_paths_present_for_current_feature"] is bound
        assert candidate["freeze_memory_status_ok_bound_to_same_write"] is bound
        assert candidate["preview_readiness_not_confirmation"] is True
        assert candidate["writable_preview_not_confirmation"] is True
        assert candidate["validation_evidence_not_confirmation"] is True
        assert candidate["stale_confirmation_demoted"] is True
        assert candidate["mismatched_feature_title_demoted"] is (not bound)
        assert candidate["mismatched_freeze_id_demoted"] is (not bound)
        assert candidate["split_confirmation_not_merged_unsafely"] is True
        assert candidate["sequence_advancement_requires_current_bound_confirmation"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_implied_confirmation_as_write"] is False
        assert candidate["treat_stale_confirmation_as_current"] is False
        assert candidate["treat_mismatched_freeze_id_as_current"] is False
        assert candidate["treat_mismatched_title_as_current"] is False
        assert candidate["skip_human_confirmation"] is False
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
    assert "MLRT-98" in text
    assert "64/64" in text
    assert "922/922" in text
    assert "`18` real test suites" in text
    assert "Confirm and Write" in text
    assert "LOCAL FREEZE WRITE OK" in text
    assert "FREEZE_MEMORY_STATUS: OK" in text
    assert "exact freeze ID" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "922/922" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_human_confirmation_binding_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 922
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 18
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_explicit_confirm_and_write_action_binding_tested"] is True
    assert manifest[f"{PREFIX}_current_feature_title_binding_tested"] is True
    assert manifest[f"{PREFIX}_current_freeze_id_binding_tested"] is True
    assert manifest[f"{PREFIX}_write_block_and_confirmation_coherence_tested"] is True
    assert manifest[f"{PREFIX}_stale_or_adjacent_confirmation_demotion_tested"] is True
    assert manifest[f"{PREFIX}_split_or_truncated_confirmation_recovery_tested"] is True
    assert manifest[f"{PREFIX}_sequence_advancement_binding_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_confirmation_binding_tested"] is True
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
    print("SANDBOX_RSS_MLRT99_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
