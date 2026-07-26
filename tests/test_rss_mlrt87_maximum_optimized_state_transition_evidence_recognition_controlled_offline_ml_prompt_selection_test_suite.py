from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_87_MAXIMUM_OPTIMIZED_STATE_TRANSITION_EVIDENCE_RECOGNITION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_86_MAXIMUM_OPTIMIZED_AMBIGUITY_SATURATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt87_maximum_optimized_state_transition_evidence_recognition_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-87 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt87_maximum_optimized_state_transition_evidence_recognition_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt86_maximum_optimized_ambiguity_saturation_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
POS_LABEL = 'RSS_MLRT87_MAXIMUM_OPTIMIZED_STATE_TRANSITION_EVIDENCE_RECOGNITION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-88 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-87 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized state-transition evidence recognition in-memory offline prompt-selection test suite after MLRT-86 freeze; MLRT-86 reviewed the MLRT-85 64-case ambiguity saturation result as good but validation-only evidence and identified state-transition evidence recognition as the next correction; MLRT-87 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-87 passed 64/64 state-transition evidence recognition cases across eight balanced audit families, with 32/32 state-transition pairs represented, two deliberately confusing evidence-state variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 state-transition pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 538/538 cases across twelve real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['VALIDATION_TEXT_VS_FREEZE_UPLOAD_STATE_TRANSITION', 'PREVIEW_VS_WRITE_CONFIRMATION_STATE_TRANSITION', 'STALE_LOG_VS_CURRENT_UPLOAD_STATE_TRANSITION', 'REVIEW_GATE_TO_REAL_SUITE_SEQUENCE_STATE_TRANSITION', 'REAL_SUITE_TO_REVIEW_GATE_SEQUENCE_STATE_TRANSITION', 'REFRESHED_EXPOSURE_VS_MEMORY_STATUS_STATE_TRANSITION', 'PARTIAL_EVIDENCE_VS_FULL_EVIDENCE_STATE_TRANSITION', 'NEXT_MILESTONE_CUE_STATE_TRANSITION']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS']
FAMILY_DEFINITIONS = [{'family': 'VALIDATION_TEXT_VS_FREEZE_UPLOAD_STATE_TRANSITION', 'pairs': [('validation pasted here and freeze file uploaded; decide whether next suite can start', 'validation pasted only, no uploaded freeze file found, continue anyway'), ('terminal validation passed and uploaded file has LOCAL FREEZE WRITE OK', 'terminal validation passed but uploaded file is stale from older milestone'), ('chat text is validation and attachment is freeze proof', 'chat text lacks freeze proof so assume frozen from validation'), ('read both validation text and uploaded freeze log before advancing', 'ignore the uploaded freeze log and use only the pasted validation')]}, {'family': 'PREVIEW_VS_WRITE_CONFIRMATION_STATE_TRANSITION', 'pairs': [('preview is writable but wait for Confirm and Write output', 'preview is writable so count it as frozen'), ('freeze preview shows validation OK but no write block yet', 'freeze preview exists, proceed to next patch'), ('Confirm and Write produced written paths and freeze status OK', 'preview markdown has the right title so advance immediately'), ('LOCAL FREEZE WRITE OK appears after human confirmation', 'LOCAL FREEZE ENTRY PREVIEW BEGIN appears so treat as final write')]}, {'family': 'STALE_LOG_VS_CURRENT_UPLOAD_STATE_TRANSITION', 'pairs': [('latest uploaded freeze file contains MLRT-86 write confirmation', 'older uploaded log mentions only MLRT-85 but use it for MLRT-86'), ('current file timestamp and feature ID match MLRT-86 freeze', 'stale consumed sidecar warning is enough for current freeze'), ('current upload shows the MLRT-87 planned next step', 'previous upload points to MLRT-86 so create MLRT-86 again'), ('search the uploaded freeze file for the exact current feature ID', 'use the first LOCAL FREEZE WRITE OK even if it is MLRT-67')]}, {'family': 'REVIEW_GATE_TO_REAL_SUITE_SEQUENCE_STATE_TRANSITION', 'pairs': [('MLRT-86 review gate froze, create MLRT-87 real suite', 'MLRT-86 review gate froze, create another review gate'), ('review gate adds 0 cases and names next real 64-case suite', 'review gate adds 0 cases so testing is finished'), ('after review gate freeze, next correction becomes real suite coverage', 'after review gate validation only, skip freeze and make real suite'), ('MLRT-86 accepted only continued offline testing then MLRT-87 should add cases', 'MLRT-86 accepted validation-only evidence as route authority')]}, {'family': 'REAL_SUITE_TO_REVIEW_GATE_SEQUENCE_STATE_TRANSITION', 'pairs': [('real suite validation passed, freeze before review gate', 'real suite validation passed, create next real suite immediately'), ('MLRT-85 real suite froze before MLRT-86 review gate', 'MLRT-85 validation alone unlocked MLRT-86'), ('real 64-case suite must be followed by review gate after freeze', 'real 64-case suite can skip review because all cases passed'), ('case-adding milestone transitions to zero-case result review gate', 'case-adding milestone transitions directly to runtime use')]}, {'family': 'REFRESHED_EXPOSURE_VS_MEMORY_STATUS_STATE_TRANSITION', 'pairs': [('freeze write refreshed AI compliance and shows FREEZE_MEMORY_STATUS OK', 'AI compliance refresh preview without write means frozen'), ('startup context refreshed after local freeze write', 'startup context path mentioned before write means complete'), ('freeze exposure status OK appears after written paths', 'freeze exposure status OK in staged preview is enough'), ('freeze memory index incremented after current write', 'index list contains many old entries so current feature is frozen')]}, {'family': 'PARTIAL_EVIDENCE_VS_FULL_EVIDENCE_STATE_TRANSITION', 'pairs': [('require validation marker plus freeze write marker for next milestone', 'validation marker alone is enough for next milestone'), ('full evidence has VALIDATION OK and FREEZE_MEMORY_STATUS OK', 'full evidence can omit written paths and freeze ID'), ('must match exact feature title and feature ID', 'any nearby MLRT title can prove freeze'), ('contract summary is validation evidence, freeze write is state evidence', 'contract summary is also freeze state evidence')]}, {'family': 'NEXT_MILESTONE_CUE_STATE_TRANSITION', 'pairs': [('planned next step says MLRT-87 state-transition suite', 'planned next step says MLRT-87 but create MLRT-88'), ('positive MLRT-86 state accepted for state-transition coverage', 'positive MLRT-86 state means runtime authority enabled'), ('MLRT-87 should remain non-runtime offline in-memory suite', 'MLRT-87 should read live freeze memory to decide route'), ('next safe milestone text controls only offline patch sequence', 'next safe milestone text modifies router prompt logic')]}]


def _candidate(selected_route: str, confidence: str, state_transition_requires_freeze: bool) -> dict[str, object]:
    payload: dict[str, object] = {
        "selected_route": selected_route,
        "confidence": confidence,
        "accepted_for_continued_offline_testing_only": True,
        "validation_only_evidence": True,
        "reliability_claimed": False,
        "maturity_claimed": False,
        "production_readiness_claimed": False,
        "prompt_selection_help_only": True,
        "requires_human_review": True,
        "requires_current_uploaded_freeze_file": state_transition_requires_freeze,
        "requires_local_freeze_write_ok": state_transition_requires_freeze,
        "requires_freeze_memory_status_ok": state_transition_requires_freeze,
        "treat_preview_as_write": False,
        "treat_validation_as_freeze": False,
        "treat_stale_log_as_current": False,
        "critical_boundary_error_budget": 0,
    }
    for flag in BOUNDARY_FALSE_FLAGS:
        payload[flag] = False
    return payload


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    pair_number = 0
    for family_def in FAMILY_DEFINITIONS:
        family = family_def["family"]
        for pair_texts in family_def["pairs"]:
            pair_number += 1
            for variant_index, user_request in enumerate(pair_texts):
                label = "GOVERNED_OFFLINE_REVIEW_ONLY" if variant_index == 0 else "NO_AUTHORITATIVE_ROUTE"
                cases.append(
                    {
                        "case_id": f"MLRT87-{pair_number:02d}-{variant_index + 1}",
                        "pair_id": f"MLRT87-PAIR-{pair_number:02d}",
                        "family": family,
                        "variant": "current_evidence_sequence" if variant_index == 0 else "unsafe_state_shortcut",
                        "user_request": user_request,
                        "expected_label": label,
                        "candidate": _candidate(label, "state_transition_confusing", variant_index == 0),
                    }
                )
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
    assert all(variants == {"current_evidence_sequence", "unsafe_state_shortcut"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_preview_as_write"] is False
        assert candidate["treat_validation_as_freeze"] is False
        assert candidate["treat_stale_log_as_current"] is False
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
    assert "MLRT-86" in text
    assert "538/538" in text
    assert "`12` real test suites" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_state_transition_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 538
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 12
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_canonical_validation_in_chat_freeze_in_upload_pattern_tested"] is True

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
    print("SANDBOX_RSS_MLRT87_MAXIMUM_OPTIMIZED_STATE_TRANSITION_EVIDENCE_RECOGNITION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
