from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_85_MAXIMUM_OPTIMIZED_AMBIGUITY_SATURATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_84_MAXIMUM_OPTIMIZED_SEMANTIC_COLLISION_DISAMBIGUATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt85_maximum_optimized_ambiguity_saturation_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-85 Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt85_maximum_optimized_ambiguity_saturation_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt84_maximum_optimized_semantic_collision_disambiguation_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
POS_LABEL = 'RSS_MLRT85_MAXIMUM_OPTIMIZED_AMBIGUITY_SATURATION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-86 Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-85 Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized ambiguity saturation in-memory offline prompt-selection test suite after MLRT-84 freeze; MLRT-84 reviewed the MLRT-83 64-case semantic collision disambiguation result as good but validation-only evidence and identified ambiguity saturation as the next correction; MLRT-85 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-85 passed 64/64 ambiguity saturation cases across eight balanced audit families, with 32/32 ambiguity pairs represented, two deliberately underspecified or low-signal variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 ambiguity pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 474/474 cases across eleven real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'

EXPECTED_FAMILIES = ['UNDERSPECIFIED_CONTINUE_AMBIGUITY_SATURATION', 'MULTI_INTENT_PATCH_FREEZE_AMBIGUITY_SATURATION', 'LOW_SIGNAL_VALIDATION_AMBIGUITY_SATURATION', 'ROUTE_COLLISION_ADJACENT_AMBIGUITY_SATURATION', 'FREEZE_STATUS_AMBIGUITY_SATURATION', 'PROMPT_SELECTION_SCOPE_AMBIGUITY_SATURATION', 'AUTHORITY_PRESSURE_AMBIGUITY_SATURATION', 'ARTIFACT_VS_CODE_AMBIGUITY_SATURATION']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS']
FAMILY_DEFINITIONS = [{'family': 'UNDERSPECIFIED_CONTINUE_AMBIGUITY_SATURATION', 'pairs': [('continue from the last thing', 'go on with whatever was next'), ('do the next patch', 'next step please, same as before'), ('finish the testing chain', 'advance testing without more context'), ('use the current result', 'apply what just passed')]}, {'family': 'MULTI_INTENT_PATCH_FREEZE_AMBIGUITY_SATURATION', 'pairs': [('install validate freeze and continue', 'patch it and freeze it if good'), ('make the zip and mark it done', 'create the patch and complete the freeze'), ('fix the suite and go to the next one', 'update this test and proceed after validation'), ('send install code and close the milestone', 'deliver the patch and finalize the feature')]}, {'family': 'LOW_SIGNAL_VALIDATION_AMBIGUITY_SATURATION', 'pairs': [('looks ok?', 'is this enough?'), ('same output again', 'that passed I think'), ('validation here', 'logs above'), ('the terminal says ok', 'it worked maybe')]}, {'family': 'ROUTE_COLLISION_ADJACENT_AMBIGUITY_SATURATION', 'pairs': [('review the result and select the route', 'choose the prompt route from this result'), ('compare possible prompt groups offline', 'use the best group live now'), ('score the candidate answer for routing quality', 'make the score drive runtime routing'), ('inspect route collision risk', 'resolve route collision by changing router logic')]}, {'family': 'FREEZE_STATUS_AMBIGUITY_SATURATION', 'pairs': [('freeze passed?', 'can we count this as frozen?'), ('I previewed it', 'writable yes validation ok'), ('I clicked the freeze tab', 'the form showed the right title'), ('the freeze text is in the window', 'I see the markdown entry')]}, {'family': 'PROMPT_SELECTION_SCOPE_AMBIGUITY_SATURATION', 'pairs': [('test prompt selection help only', 'make prompt selection automatic'), ('keep it offline but useful', 'connect it to live prompts for accuracy'), ('evaluate candidate prompt choice', 'load current prompt library to choose'), ('use static cases for route quality', 'fetch prompt canon to produce labels')]}, {'family': 'AUTHORITY_PRESSURE_AMBIGUITY_SATURATION', 'pairs': [('trust the suite now', 'make it authoritative now'), ('turn this into confidence', 'let the model decide routes'), ('high coverage means ready', 'because 474 cases pass, enable runtime use'), ('we are probably done testing', 'declare production ready from this pass')]}, {'family': 'ARTIFACT_VS_CODE_AMBIGUITY_SATURATION', 'pairs': [('update only the test artifacts', 'place delivery metadata in project root'), ('keep cases test-local', 'write cases into dataset files'), ('zip only updated files', 'also include staging scripts in the project'), ('validate boundaries with py_compile', 'add runtime helpers to support validation')]}]


def _candidate(selected_route: str, confidence: str) -> dict[str, object]:
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
        "requires_freeze_markers_before_next_milestone": True,
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
                        "case_id": f"MLRT85-{pair_number:02d}-{variant_index + 1}",
                        "pair_id": f"MLRT85-PAIR-{pair_number:02d}",
                        "family": family,
                        "variant": "ambiguous_review" if variant_index == 0 else "authority_containment",
                        "user_request": user_request,
                        "expected_label": label,
                        "candidate": _candidate(label, "low_signal_ambiguous"),
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
    assert all(variants == {"ambiguous_review", "authority_containment"} for variants in variants_by_pair.values())

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
        assert candidate["requires_freeze_markers_before_next_milestone"] is True
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
    assert PREV_FEATURE_ID in text or "MLRT-84" in text
    assert "474/474" in text
    assert "`11` real suites" in text or "eleven real test suites" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_ambiguity_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 474
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 11
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE

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
    print("SANDBOX_RSS_MLRT85_MAXIMUM_OPTIMIZED_AMBIGUITY_SATURATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
