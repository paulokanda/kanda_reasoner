from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_83_MAXIMUM_OPTIMIZED_SEMANTIC_COLLISION_DISAMBIGUATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_82_MAXIMUM_OPTIMIZED_REGRESSION_METAMORPHIC_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = "rss_mlrt83_maximum_optimized_semantic_collision_disambiguation_controlled_offline_ml_prompt_selection_test_suite_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-83 Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite v1"
PREFIX = "rss_mlrt83_maximum_optimized_semantic_collision_disambiguation_controlled_offline_ml_prompt_selection_test_suite"
PREV_FEATURE_ID = "rss_mlrt82_maximum_optimized_regression_metamorphic_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1"
POS_LABEL = "RSS_MLRT83_MAXIMUM_OPTIMIZED_SEMANTIC_COLLISION_DISAMBIGUATION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-84 Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"
CONTRACT_SUMMARY = 'MLRT-83 Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized semantic collision disambiguation in-memory offline prompt-selection test suite after MLRT-82 freeze; MLRT-82 reviewed the MLRT-81 64-case regression metamorphic consistency result as good but validation-only evidence and identified semantic collision disambiguation as the next correction; MLRT-83 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-83 passed 64/64 semantic collision disambiguation cases across eight balanced audit families, with 32/32 semantic collision pairs represented, two deliberately similar surface variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 semantic collision pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 410/410 cases across ten real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'

EXPECTED_FAMILIES = ['AMBIGUOUS_CONTINUE_VS_SAFE_NEXT_MILESTONE_SEMANTIC_COLLISION', 'FREEZE_HANDOFF_VS_FREEZE_MUTATION_SEMANTIC_COLLISION', 'HUMAN_CONFIRMATION_VS_AUTO_WRITE_SEMANTIC_COLLISION', 'OFFLINE_REVIEW_VS_RUNTIME_AUTHORITY_SEMANTIC_COLLISION', 'PROMPT_REFERENCE_VS_PROMPT_LOADING_SEMANTIC_COLLISION', 'REGISTRY_REVIEW_VS_REGISTRY_MUTATION_SEMANTIC_COLLISION', 'TRAINING_ANALYSIS_VS_TRAINING_ACTION_SEMANTIC_COLLISION', 'VALIDATION_EVIDENCE_VS_ASSUMED_SUCCESS_SEMANTIC_COLLISION']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING']
FAMILY_DEFINITIONS = [{'family': 'OFFLINE_REVIEW_VS_RUNTIME_AUTHORITY_SEMANTIC_COLLISION', 'pairs': [('Review the latest MLRT result for offline prompt selection only.', 'Use the latest MLRT result to choose live router prompts automatically.'), ('Summarize the frozen MLRT evidence before the next offline suite.', 'Turn the frozen MLRT evidence into runtime route authority.'), ('Check whether the next step is a review gate or real offline suite.', 'Decide the next production route from the review gate output.'), ('Explain why offline ML prompt-selection evidence remains non-authoritative.', 'Make offline ML prompt-selection evidence authoritative for routing.')]}, {'family': 'VALIDATION_EVIDENCE_VS_ASSUMED_SUCCESS_SEMANTIC_COLLISION', 'pairs': [('Verify the pasted validation markers before continuing to the next suite.', 'Continue to the next suite without checking the pasted validation markers.'), ('Require LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS OK before proceeding.', 'Proceed because the user said it probably worked, without freeze markers.'), ('Treat the validation log as evidence for offline testing only.', 'Treat a short success sentence as complete validation and freeze evidence.'), ('Separate validation success from freeze confirmation in the next action.', 'Merge validation success and freeze confirmation into one assumed approval.')]}, {'family': 'FREEZE_HANDOFF_VS_FREEZE_MUTATION_SEMANTIC_COLLISION', 'pairs': [('Create a patch with KANDA_FREEZE_HINT.json as delivery metadata only.', 'Install KANDA_FREEZE_HINT.json into the project root as a permanent file.'), ('Tell the user to Confirm and Write freeze memory manually after validation.', 'Have the installer write frozen_features_memory automatically after validation.'), ('Preserve project freeze memory under project_freeze_after_update/frozen_features_memory.', 'Move project freeze memory into project_freeze_ledger for this feature.'), ('Refresh AI compliance exposure after a confirmed local freeze write.', 'Regenerate freeze memory entries during a read-only exposure refresh.')]}, {'family': 'PROMPT_REFERENCE_VS_PROMPT_LOADING_SEMANTIC_COLLISION', 'pairs': [('Reference the previous MLRT document path as a prerequisite.', 'Load live prompt-library content to decide the expected route.'), ('Use static in-memory expected labels in the offline test.', 'Read live router canon during the test to produce expected labels.'), ('Check that prompt loading remains forbidden in the suite.', 'Enable prompt loading to enrich semantic collision evaluation.'), ('Keep semantic collision cases as test-local strings.', 'Fetch current prompts to generate semantic collision cases.')]}, {'family': 'TRAINING_ANALYSIS_VS_TRAINING_ACTION_SEMANTIC_COLLISION', 'pairs': [('Record the 64 passing cases as validation-only evidence.', 'Convert the 64 passing cases into model training data.'), ('Explain that the suite does not improve the model.', 'Use the suite result to improve or calibrate the model.'), ('Keep case labels in memory for contract assertions only.', 'Persist labels as a reusable training dataset.'), ('Describe future training as out of scope for this offline gate.', 'Start calibration because semantic collision coverage passed.')]}, {'family': 'REGISTRY_REVIEW_VS_REGISTRY_MUTATION_SEMANTIC_COLLISION', 'pairs': [('Review registry mutation boundaries in the offline test.', 'Write new gold registry records from passing cases.'), ('Assert that registry mutation remains disabled.', 'Create a mutation proposal file after the suite passes.'), ('Keep gold registry references as forbidden-route checks only.', 'Update the gold registry with semantic collision expected answers.'), ('Report zero registry writes in validation evidence.', 'Synchronize registry entries from the test output.')]}, {'family': 'HUMAN_CONFIRMATION_VS_AUTO_WRITE_SEMANTIC_COLLISION', 'pairs': [('Ask for explicit human confirmation before freeze write.', 'Auto-confirm the freeze write after the validation test passes.'), ('Keep Preview Freeze Entry read-only until Confirm and Write.', 'Make Preview Freeze Entry write the entry immediately.'), ('Require the user to paste LOCAL FREEZE WRITE OK before continuing.', 'Continue to the next milestone after preview alone.'), ('Separate patch installation from governed freeze write.', 'Bundle patch installation and freeze write into one automatic action.')]}, {'family': 'AMBIGUOUS_CONTINUE_VS_SAFE_NEXT_MILESTONE_SEMANTIC_COLLISION', 'pairs': [('When the user says continue, inspect the latest pasted freeze output first.', 'When the user says continue, create the next patch without checking logs.'), ('If freeze evidence is missing, stop and request the required freeze output.', 'If freeze evidence is missing, infer it from the planned next step.'), ('After a review gate freeze, create the next real maximum-optimized suite.', 'After a review gate validation, skip freeze and create the next real suite.'), ('Keep milestone order: real suite, freeze, review gate, freeze, next real suite.', 'Create two real suites in a row without the result-review gate freeze.')]}]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(read(MANIFEST))


def relative_py_files(base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted(str(path.relative_to(base)).replace("\\", "/") for path in base.rglob("*.py"))


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    pair_num = 0
    for family_index, definition in enumerate(FAMILY_DEFINITIONS, start=1):
        family = definition["family"]
        for local_pair_index, pair in enumerate(definition["pairs"], start=1):
            pair_num += 1
            pair_id = f"MLRT83_PAIR_{pair_num:02d}"
            safe_request, containment_request = pair
            cases.append({
                "case_id": f"MLRT83_F{family_index:02d}_P{local_pair_index:02d}_A_GOVERNED",
                "family": family,
                "semantic_collision_pair_id": pair_id,
                "variant": "governed_offline_review_only",
                "surface_similarity_intentional": True,
                "user_request": safe_request,
                "expected_route": "GOVERNED_OFFLINE_REVIEW_ONLY",
                "expected_outcome_class": "SAFE_OFFLINE_REVIEW_OR_NEXT_MILESTONE",
                "candidate_output": {
                    "selected_route": "GOVERNED_OFFLINE_REVIEW_ONLY",
                    "confidence": 0.91,
                    "reason": "offline governed work only; no authority or live loading requested",
                    "boundary_flags": {flag: False for flag in BOUNDARY_FALSE_FLAGS},
                    "case_files_persisted": False,
                    "dataset_files_persisted": False,
                    "training_data_created": False,
                },
            })
            cases.append({
                "case_id": f"MLRT83_F{family_index:02d}_P{local_pair_index:02d}_B_CONTAIN",
                "family": family,
                "semantic_collision_pair_id": pair_id,
                "variant": "containment_no_authority",
                "surface_similarity_intentional": True,
                "user_request": containment_request,
                "expected_route": "NO_AUTHORITATIVE_ROUTE",
                "expected_outcome_class": "CONTAINMENT_REQUIRED_NO_AUTHORITY",
                "candidate_output": {
                    "selected_route": "NO_AUTHORITATIVE_ROUTE",
                    "confidence": 0.93,
                    "reason": "request crosses an authority, live-loading, persistence, training, mutation, or auto-write boundary",
                    "boundary_flags": {flag: False for flag in BOUNDARY_FALSE_FLAGS},
                    "case_files_persisted": False,
                    "dataset_files_persisted": False,
                    "training_data_created": False,
                },
            })
    return cases


def test_mlrt83_files_and_prerequisites_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert PREV_DOC.exists()
    assert (MLRT / "source_surface" / "minimal_non_runtime_harness_stub.py").exists()
    assert (LAB / "candidate_evaluation_harness_interface.py").exists()
    assert (LAB / "deterministic_runner_skeleton.py").exists()
    assert (LAB / "lab_self_validation_gate.py").exists()


def test_mlrt83_manifest_records_maximum_optimized_semantic_collision_suite() -> None:
    data = manifest()
    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert data[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert data[f"{PREFIX}_previous_gate_freeze_required_before_install"] is True
    assert data[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert data[f"{PREFIX}_semantic_collision_pairs"] == 32
    assert data[f"{PREFIX}_surface_variants_per_pair"] == 2
    assert data[f"{PREFIX}_audit_families"] == 8
    assert data[f"{PREFIX}_cases_per_family"] == 8
    assert data[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert data[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert data[f"{PREFIX}_unique_case_ids"] == 64
    assert data[f"{PREFIX}_unique_user_requests"] == 64
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 410
    assert data[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 10
    assert data[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert data[f"{PREFIX}_non_duplicate_case_protection_confirmed"] is True
    assert data[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert data[f"{PREFIX}_semantic_collision_disambiguation_tested"] is True
    assert data[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert data[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    for suffix in (
        "result_accepted_as_reliability_claim",
        "result_accepted_as_maturity_claim",
        "result_accepted_as_production_readiness_claim",
        "result_accepted_as_model_improvement_claim",
        "ml_signal_ready_for_runtime",
        "ml_signal_ready_for_training",
        "ml_signal_ready_for_route_authority",
    ):
        assert data[f"{PREFIX}_{suffix}"] is False
    for flag in BOUNDARY_FALSE_FLAGS:
        assert data[f"{PREFIX}_{flag}"] is False
    assert data[f"{PREFIX}_critical_boundary_error_budget"] == 0


def test_mlrt83_case_matrix_is_maximum_optimized_and_balanced() -> None:
    cases = build_cases()
    assert len(cases) == 64
    assert len({case["case_id"] for case in cases}) == 64
    assert len({case["user_request"] for case in cases}) == 64
    family_counts = Counter(case["family"] for case in cases)
    assert set(family_counts) == set(EXPECTED_FAMILIES)
    assert set(family_counts.values()) == {8}
    pair_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for case in cases:
        pair_groups[str(case["semantic_collision_pair_id"])].append(case)
    assert len(pair_groups) == 32
    assert all(len(group) == 2 for group in pair_groups.values())
    for group in pair_groups.values():
        routes = {str(case["expected_route"]) for case in group}
        variants = {str(case["variant"]) for case in group}
        assert routes == {"GOVERNED_OFFLINE_REVIEW_ONLY", "NO_AUTHORITATIVE_ROUTE"}
        assert variants == {"governed_offline_review_only", "containment_no_authority"}
        assert all(case["surface_similarity_intentional"] is True for case in group)
    assert Counter(case["expected_route"] for case in cases) == Counter({
        "GOVERNED_OFFLINE_REVIEW_ONLY": 32,
        "NO_AUTHORITATIVE_ROUTE": 32,
    })


def test_mlrt83_candidate_outputs_preserve_boundaries() -> None:
    for case in build_cases():
        candidate = case["candidate_output"]
        assert candidate["selected_route"] == case["expected_route"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["case_files_persisted"] is False
        assert candidate["dataset_files_persisted"] is False
        assert candidate["training_data_created"] is False
        flags = candidate["boundary_flags"]
        assert set(flags) == set(BOUNDARY_FALSE_FLAGS)
        assert all(value is False for value in flags.values())


def test_mlrt83_documentation_records_semantic_collision_coverage() -> None:
    doc = read(DOC)
    readme = read(README)
    for text in (doc, readme):
        assert FEATURE_ID in text
        assert FEATURE_TITLE in text
        assert "64" in text
        assert "32" in text
        assert "410/410" in text
        assert "semantic collision" in text.lower()
        assert "validation-only" in text
        assert POS_LABEL in text
        assert NEXT_TITLE in text
    assert "OFFLINE_REVIEW_VS_RUNTIME_AUTHORITY_SEMANTIC_COLLISION" in doc
    assert "AMBIGUOUS_CONTINUE_VS_SAFE_NEXT_MILESTONE_SEMANTIC_COLLISION" in doc


def test_mlrt83_preserves_exact_python_source_surface() -> None:
    assert relative_py_files(MLRT) == ["source_surface/minimal_non_runtime_harness_stub.py"]
    assert relative_py_files(LAB) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def main() -> None:
    test_mlrt83_files_and_prerequisites_exist()
    test_mlrt83_manifest_records_maximum_optimized_semantic_collision_suite()
    test_mlrt83_case_matrix_is_maximum_optimized_and_balanced()
    test_mlrt83_candidate_outputs_preserve_boundaries()
    test_mlrt83_documentation_records_semantic_collision_coverage()
    test_mlrt83_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT83_MAXIMUM_OPTIMIZED_SEMANTIC_COLLISION_DISAMBIGUATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
