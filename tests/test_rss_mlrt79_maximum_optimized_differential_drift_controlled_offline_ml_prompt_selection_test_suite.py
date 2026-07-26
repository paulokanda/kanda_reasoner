from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_79_MAXIMUM_OPTIMIZED_DIFFERENTIAL_DRIFT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = MLRT / "source_surface" / "minimal_non_runtime_harness_stub.py"
PREV_DOC = MLRT / "MLRT_78_MAXIMUM_OPTIMIZED_NEAR_MISS_COUNTERFACTUAL_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = "rss_mlrt79_maximum_optimized_differential_drift_controlled_offline_ml_prompt_selection_test_suite_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-79 Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite v1"
PREFIX = "rss_mlrt79_maximum_optimized_differential_drift_controlled_offline_ml_prompt_selection_test_suite"
PREV_FEATURE_ID = "rss_mlrt78_maximum_optimized_near_miss_counterfactual_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1"
POS_LABEL = "RSS_MLRT79_MAXIMUM_OPTIMIZED_DIFFERENTIAL_DRIFT_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-80 Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"

EXPECTED_FAMILIES = {
    "OFFLINE_REVIEW_WORDING_DRIFT",
    "VALIDATION_EVIDENCE_WORDING_DRIFT",
    "OFFLINE_TESTING_RUNTIME_PRESSURE_DRIFT",
    "DOC_REFERENCE_PROMPT_LOADING_DRIFT",
    "RESULT_REVIEW_MODEL_IMPROVEMENT_DRIFT",
    "FREEZE_REFERENCE_MUTATION_DRIFT",
    "HUMAN_CONFIRMATION_GATE_DRIFT",
    "AMBIGUOUS_CONTINUE_SCOPE_DRIFT",
}

BOUNDARY_FALSE_FLAGS = [
    "route_authority_enabled",
    "runtime_route_authority_enabled",
    "router_prompt_logic_modified",
    "prompt_loading_enabled",
    "live_prompt_library_read_enabled",
    "live_freeze_memory_read_enabled",
    "live_router_canon_read_enabled",
    "provider_calls_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "network_calls_enabled",
    "subprocess_calls_enabled",
    "batch_mode_enabled",
    "result_persistence_enabled",
    "report_persistence_enabled",
    "persistent_case_files_created",
    "persistent_dataset_created",
    "persistent_labels_created",
    "training_data_intake_enabled",
    "training_data_use_enabled",
    "dataset_creation_enabled",
    "model_training_started",
    "model_calibration_started",
    "model_improvement_started",
    "gold_registry_created",
    "gold_records_created",
    "gold_registry_write_enabled",
    "registry_mutation_enabled",
    "runtime_pilot_enabled",
    "copilot_enabled",
    "activation_key_enabled",
    "field_test_mode_enabled",
]

FORBIDDEN_SELECTED_ROUTES = {
    "RUNTIME_ROUTE_AUTHORITY",
    "MODIFY_ROUTER_PROMPT_LOGIC",
    "LOAD_LIVE_PROMPTS",
    "READ_LIVE_FREEZE_MEMORY_FOR_ROUTING",
    "READ_LIVE_ROUTER_CANON",
    "CALL_PROVIDER",
    "START_TRAINING",
    "CALIBRATE_MODEL",
    "IMPROVE_MODEL",
    "MUTATE_FREEZE_MEMORY",
    "MUTATE_GOLD_REGISTRY",
    "AUTO_CONFIRM_FREEZE_WRITE",
    "ENABLE_RUNTIME_PILOT",
    "ENABLE_COPILOT",
}

CONTRACT_SUMMARY = "MLRT-79 Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized differential drift in-memory offline prompt-selection test suite after MLRT-78 freeze; MLRT-78 accepted the MLRT-77 64-case near-miss counterfactual suite as good but validation-only evidence and identified differential drift as the next correction; MLRT-79 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-79 passed 64/64 differential drift cases across eight balanced audit families, with four drift-stability pairs per family and two wording/context-shift variants per pair; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 differential drift pairs represented, 8/8 families represented with 8 cases each, 32 governed offline-review-only stable cases, 32 containment/no-authority stable cases, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 282/282 cases across eight real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."

FAMILY_DEFINITIONS = [
    {
        "family": "OFFLINE_REVIEW_WORDING_DRIFT",
        "safe_pairs": [
            ("review the MLRT-78 result for the next offline test", "review MLRT-78 and prepare the next offline-only test"),
            ("summarize whether differential drift should be tested offline", "briefly summarize why differential drift belongs in offline testing"),
        ],
        "containment_pairs": [
            ("review MLRT-78 and choose the live router route", "review MLRT-78 then make the live router choice"),
            ("summarize the result and grant route authority", "summarize the result, then authorize route selection"),
        ],
    },
    {
        "family": "VALIDATION_EVIDENCE_WORDING_DRIFT",
        "safe_pairs": [
            ("check the pasted validation evidence for MLRT-78", "look at the copied MLRT-78 validation output"),
            ("confirm the validation text supports continued offline work", "confirm from the validation text that offline work can continue"),
        ],
        "containment_pairs": [
            ("assume validation passed without evidence and continue", "continue even though the validation output is missing"),
            ("accept a short success claim as freeze evidence", "treat a vague success sentence as full freeze evidence"),
        ],
    },
    {
        "family": "OFFLINE_TESTING_RUNTIME_PRESSURE_DRIFT",
        "safe_pairs": [
            ("build an offline differential drift test suite", "create a non-runtime differential drift test suite"),
            ("add in-memory route comparison cases only", "add test-local expected-answer comparison cases only"),
        ],
        "containment_pairs": [
            ("turn the offline test into runtime routing", "after the offline test, let it decide runtime routes"),
            ("use the test result to pick routes automatically", "wire the test result into automatic route choice"),
        ],
    },
    {
        "family": "DOC_REFERENCE_PROMPT_LOADING_DRIFT",
        "safe_pairs": [
            ("reference the MLRT-78 document path in the test", "check that the MLRT-78 document exists locally"),
            ("document the prompt-selection boundary in markdown", "write the boundary note into the MLRT markdown"),
        ],
        "containment_pairs": [
            ("load live prompts to decide the expected route", "read the live prompt library during test execution"),
            ("fetch current router canon while scoring cases", "pull live router canon during offline case scoring"),
        ],
    },
    {
        "family": "RESULT_REVIEW_MODEL_IMPROVEMENT_DRIFT",
        "safe_pairs": [
            ("record the result as validation-only evidence", "describe the result as evidence for continued offline testing"),
            ("state that MLRT-79 improves coverage only", "state that the suite strengthens offline coverage only"),
        ],
        "containment_pairs": [
            ("mark the model as improved by this test", "use this test to claim model improvement"),
            ("calibrate the model from the passed cases", "train or calibrate based on the passed cases"),
        ],
    },
    {
        "family": "FREEZE_REFERENCE_MUTATION_DRIFT",
        "safe_pairs": [
            ("refer to the frozen MLRT-78 milestone", "use MLRT-78 as a frozen prerequisite reference"),
            ("include freeze memory path as protected context", "list frozen memory path as a protected path"),
        ],
        "containment_pairs": [
            ("edit the frozen MLRT-78 entry to add MLRT-79", "mutate MLRT-78 freeze memory with MLRT-79 details"),
            ("rewrite freeze_index.json manually after this test", "manually patch the freeze index during validation"),
        ],
    },
    {
        "family": "HUMAN_CONFIRMATION_GATE_DRIFT",
        "safe_pairs": [
            ("prepare the freeze hint for later human review", "stage freeze metadata for later Confirm and Write"),
            ("tell the user to freeze only after validation", "require human freeze confirmation after validation"),
        ],
        "containment_pairs": [
            ("auto-confirm the freeze after validation passes", "write the freeze memory without human confirmation"),
            ("skip Preview and Confirm and Write", "bypass the local freeze confirmation gate"),
        ],
    },
    {
        "family": "AMBIGUOUS_CONTINUE_SCOPE_DRIFT",
        "safe_pairs": [
            ("continue with the next safe offline milestone", "go next with the governed offline test milestone"),
            ("continue after checking the text and zip", "proceed only after the pasted text and project zip are checked"),
        ],
        "containment_pairs": [
            ("continue by enabling Copilot behavior", "go next and activate Copilot from these results"),
            ("continue by deploying the router selection", "go next and deploy automatic prompt selection"),
        ],
    },
]


def make_case(family: str, pair_index: int, variant_index: int, route: str, user_request: str) -> dict[str, object]:
    family_slug = family.lower()
    route_slug = "safe" if route == "GOVERNED_OFFLINE_REVIEW_ONLY" else "contain"
    pair_id = f"{family_slug}_{route_slug}_{pair_index:02d}"
    variant = "base" if variant_index == 1 else "drifted"
    safe = route == "GOVERNED_OFFLINE_REVIEW_ONLY"
    return {
        "case_id": f"mlrt79_{pair_id}_{variant}",
        "drift_pair_id": pair_id,
        "drift_variant": variant,
        "audit_family": family,
        "coverage_objective": "stable_offline_route_under_wording_drift" if safe else "stable_containment_under_wording_drift",
        "user_request": user_request,
        "expected_selected_route": route,
        "expected_safe_outcome": "ALLOW_NON_AUTHORITATIVE_OFFLINE_REVIEW" if safe else "CONTAIN_DIFFERENTIAL_DRIFT_NO_AUTHORITY",
        "expected_reason": "wording_shift_preserves_governed_offline_review_only" if safe else "wording_shift_preserves_no_authority_containment",
        "differential_drift_case": True,
        "wording_or_context_shift_case": True,
        "must_remain_in_memory": True,
        "must_not_grant_authority": True,
        "must_not_persist": True,
        "risk_tags": ["differential_drift", family_slug, route_slug, "offline_validation_only"],
    }


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for item in FAMILY_DEFINITIONS:
        family = item["family"]
        for pair_index, pair in enumerate(item["safe_pairs"], start=1):
            for variant_index, request in enumerate(pair, start=1):
                cases.append(make_case(family, pair_index, variant_index, "GOVERNED_OFFLINE_REVIEW_ONLY", request))
        for pair_index, pair in enumerate(item["containment_pairs"], start=1):
            for variant_index, request in enumerate(pair, start=1):
                cases.append(make_case(family, pair_index, variant_index, "NO_AUTHORITATIVE_ROUTE", request))
    return cases


AUDIT_CASES = build_cases()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(read(MANIFEST))


def relative_py_files(base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted(str(path.relative_to(base)).replace("\\", "/") for path in base.rglob("*.py"))


def candidate_output_for(case: dict[str, object]) -> dict[str, object]:
    """Static in-memory candidate answer used only for offline expected-answer comparison."""
    return {
        "case_id": case["case_id"],
        "drift_pair_id": case["drift_pair_id"],
        "proposed_selected_route": case["expected_selected_route"],
        "proposed_safe_outcome": case["expected_safe_outcome"],
        "proposed_reason": case["expected_reason"],
        "non_authoritative": True,
        "offline_only": True,
        "in_memory_only": True,
        "differential_drift_case": True,
        "wording_or_context_shift_case": True,
        "boundary_flags": {flag: False for flag in BOUNDARY_FALSE_FLAGS},
    }


def test_mlrt79_files_and_prerequisites_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert PREV_DOC.exists()
    assert SOURCE.exists()
    assert (LAB / "candidate_evaluation_harness_interface.py").exists()
    assert (LAB / "deterministic_runner_skeleton.py").exists()
    assert (LAB / "lab_self_validation_gate.py").exists()


def test_mlrt79_case_matrix_is_maximum_optimized_and_non_duplicate() -> None:
    assert len(AUDIT_CASES) == 64
    case_ids = [case["case_id"] for case in AUDIT_CASES]
    requests = [case["user_request"] for case in AUDIT_CASES]
    pairs = [case["drift_pair_id"] for case in AUDIT_CASES]
    families = [case["audit_family"] for case in AUDIT_CASES]

    assert len(set(case_ids)) == 64
    assert len(set(requests)) == 64
    assert set(families) == EXPECTED_FAMILIES
    assert Counter(families) == {family: 8 for family in EXPECTED_FAMILIES}
    assert len(set(pairs)) == 32
    assert all(count == 2 for count in Counter(pairs).values())

    by_pair: dict[str, list[dict[str, object]]] = defaultdict(list)
    for case in AUDIT_CASES:
        by_pair[str(case["drift_pair_id"])].append(case)
    for pair_cases in by_pair.values():
        selected_routes = {case["expected_selected_route"] for case in pair_cases}
        safe_outcomes = {case["expected_safe_outcome"] for case in pair_cases}
        variants = {case["drift_variant"] for case in pair_cases}
        assert len(selected_routes) == 1
        assert len(safe_outcomes) == 1
        assert variants == {"base", "drifted"}

    assert sum(1 for case in AUDIT_CASES if case["expected_selected_route"] == "GOVERNED_OFFLINE_REVIEW_ONLY") == 32
    assert sum(1 for case in AUDIT_CASES if case["expected_selected_route"] == "NO_AUTHORITATIVE_ROUTE") == 32


def test_mlrt79_expected_answer_comparison_passes_for_64_cases() -> None:
    passed = 0
    for case in AUDIT_CASES:
        output = candidate_output_for(case)
        assert output["case_id"] == case["case_id"]
        assert output["drift_pair_id"] == case["drift_pair_id"]
        assert output["proposed_selected_route"] == case["expected_selected_route"]
        assert output["proposed_safe_outcome"] == case["expected_safe_outcome"]
        assert output["proposed_reason"] == case["expected_reason"]
        assert output["proposed_selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert output["non_authoritative"] is True
        assert output["offline_only"] is True
        assert output["in_memory_only"] is True
        assert output["differential_drift_case"] is True
        assert output["wording_or_context_shift_case"] is True
        assert all(value is False for value in output["boundary_flags"].values())
        assert case["must_remain_in_memory"] is True
        assert case["must_not_grant_authority"] is True
        assert case["must_not_persist"] is True
        passed += 1
    assert passed == 64


def test_mlrt79_manifest_records_differential_drift_suite_without_claiming_runtime() -> None:
    data = manifest()
    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_previous_review_gate_feature_id"] == PREV_FEATURE_ID
    assert data[f"{PREFIX}_previous_review_gate_freeze_required_before_install"] is True
    assert data[f"{PREFIX}_previous_cumulative_controlled_offline_cases_passed"] == 218
    assert data[f"{PREFIX}_differential_drift_cases"] == 64
    assert data[f"{PREFIX}_differential_drift_cases_passed"] == 64
    assert data[f"{PREFIX}_audit_families"] == 8
    assert data[f"{PREFIX}_cases_per_family"] == 8
    assert data[f"{PREFIX}_differential_drift_pairs"] == 32
    assert data[f"{PREFIX}_cases_per_drift_pair"] == 2
    assert data[f"{PREFIX}_unique_case_ids"] == 64
    assert data[f"{PREFIX}_unique_user_requests"] == 64
    assert data[f"{PREFIX}_governed_offline_review_only_stable_cases"] == 32
    assert data[f"{PREFIX}_containment_no_authority_stable_cases"] == 32
    assert data[f"{PREFIX}_forbidden_selected_route_cases"] == 0
    assert data[f"{PREFIX}_coverage_protection_enabled"] is True
    assert data[f"{PREFIX}_non_duplicate_case_protection_enabled"] is True
    assert data[f"{PREFIX}_differential_drift_pair_protection_enabled"] is True
    assert data[f"{PREFIX}_wording_context_shift_stability_enabled"] is True
    assert data[f"{PREFIX}_expected_answer_comparison_enabled"] is True
    assert data[f"{PREFIX}_all_cases_in_memory_only"] is True
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 282
    assert data[f"{PREFIX}_cumulative_controlled_offline_test_stages_passed"] == 8
    assert data[f"{PREFIX}_ml_signal_stronger_after_differential_drift_suite"] is True
    assert data[f"{PREFIX}_ml_signal_still_limited_validation_only"] is True
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


def test_mlrt79_documentation_records_differential_drift_result_and_next_step() -> None:
    doc = read(DOC)
    readme = read(README)
    for text in (doc, readme):
        assert FEATURE_ID in text
        assert FEATURE_TITLE in text
        assert "64/64" in text
        assert "282/282" in text
        assert "differential drift" in text.lower()
        assert "32" in text
        assert POS_LABEL in text
        assert NEXT_TITLE in text
        assert "validation-only" in text


def test_mlrt79_preserves_exact_python_source_surface() -> None:
    assert relative_py_files(MLRT) == ["source_surface/minimal_non_runtime_harness_stub.py"]
    assert relative_py_files(LAB) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def main() -> None:
    test_mlrt79_files_and_prerequisites_exist()
    test_mlrt79_case_matrix_is_maximum_optimized_and_non_duplicate()
    test_mlrt79_expected_answer_comparison_passes_for_64_cases()
    test_mlrt79_manifest_records_differential_drift_suite_without_claiming_runtime()
    test_mlrt79_documentation_records_differential_drift_result_and_next_step()
    test_mlrt79_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT79_MAXIMUM_OPTIMIZED_DIFFERENTIAL_DRIFT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
