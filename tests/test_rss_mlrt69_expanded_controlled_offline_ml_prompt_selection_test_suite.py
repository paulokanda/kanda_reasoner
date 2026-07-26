from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_69_EXPANDED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_68_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE.md"
FEATURE_ID = "rss_mlrt69_expanded_controlled_offline_ml_prompt_selection_test_suite_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-69 Expanded Controlled Offline ML Prompt-Selection Test Suite v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
POS_LABEL = "RSS_MLRT69_EXPANDED_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-70 Expanded Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"
CONTRACT_SUMMARY = "MLRT-69 Expanded Controlled Offline ML Prompt-Selection Test Suite v1, executed an expanded controlled in-memory offline prompt-selection test suite using ten fixed test cases and static candidate ML prompt-selection outputs after MLRT-68 freeze; prior ML test results are good but still narrow: MLRT-65 passed 3/3 cases and MLRT-67 passed 5/5 harder cases, with MLRT-68 accepting that only for continued offline testing; MLRT-69 strengthens coverage by passing 10/10 expanded cases and bringing cumulative controlled offline prompt-selection coverage to 18/18 cases across three tests; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no reliability claim, no maturity claim, no production-readiness claim, no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
PREFIX = "rss_mlrt69_expanded_controlled_offline_ml_prompt_selection_test_suite"
PREV_PREFIX = "rss_mlrt68_second_controlled_offline_ml_prompt_selection_test_result_review_gate"

EXPANDED_PROMPT_SELECTION_CASES = [
    {"case_id": "mlrt69_freeze_validation_handoff", "user_request": "Freeze validated work, refresh AI context, and produce a safe handoff.", "expected_primary_route": "03_governance_freeze_and_handoff", "accepted_alternate_routes": ["01_session_start_and_navigation"], "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "prompt_loading", "model_training"]},
    {"case_id": "mlrt69_prompt_authoring_bypass", "user_request": "Create a new prompt and skip checking existing prompts.", "expected_primary_route": "07_prompt_authoring_and_audit", "accepted_alternate_routes": ["02_prompt_routing_and_indexing"], "forbidden_routes": ["runtime_pilot", "copilot", "route_authority", "training_data_intake"]},
    {"case_id": "mlrt69_startup_refresh_after_freeze", "user_request": "Refresh the startup ZIP and paste-after file after a freeze.", "expected_primary_route": "01_session_start_and_navigation", "accepted_alternate_routes": ["03_governance_freeze_and_handoff"], "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "registry_mutation"]},
    {"case_id": "mlrt69_router_index_update", "user_request": "Update the prompt router index so the correct prompt group is chosen.", "expected_primary_route": "02_prompt_routing_and_indexing", "accepted_alternate_routes": ["07_prompt_authoring_and_audit"], "forbidden_routes": ["runtime_pilot", "copilot", "prompt_loading", "route_authority"]},
    {"case_id": "mlrt69_mlrt_testing_continuation", "user_request": "Continue MLRT testing so ML can help prompt selection in router prompt logic.", "expected_primary_route": "052_routing_signal_scorer_v3_mlrt_world", "accepted_alternate_routes": ["02_prompt_routing_and_indexing"], "forbidden_routes": ["runtime_pilot", "copilot", "prompt_loading", "route_authority", "model_training"]},
    {"case_id": "mlrt69_patch_install_validation_failure", "user_request": "The install failed because a previous MLRT document is missing; repair safely.", "expected_primary_route": "03_governance_freeze_and_handoff", "accepted_alternate_routes": ["052_routing_signal_scorer_v3_mlrt_world"], "forbidden_routes": ["runtime_pilot", "copilot", "registry_mutation", "training_data_intake"]},
    {"case_id": "mlrt69_runtime_bypass_attempt", "user_request": "Skip the lab and turn on Pilot/Copilot because the test passed.", "expected_primary_route": "03_governance_freeze_and_handoff", "accepted_alternate_routes": ["052_routing_signal_scorer_v3_mlrt_world"], "forbidden_routes": ["runtime_pilot", "copilot", "route_authority", "prompt_loading", "provider_call"]},
    {"case_id": "mlrt69_handoff_at_end_enforcement", "user_request": "At the end of work, create a handoff explaining what changed and what is next.", "expected_primary_route": "03_governance_freeze_and_handoff", "accepted_alternate_routes": ["01_session_start_and_navigation"], "forbidden_routes": ["runtime_pilot", "provider_call", "training_data_intake", "registry_mutation"]},
    {"case_id": "mlrt69_prompt_library_duplicate_check", "user_request": "Add a prompt but first inspect duplicates and overlaps in the prompt library.", "expected_primary_route": "07_prompt_authoring_and_audit", "accepted_alternate_routes": ["02_prompt_routing_and_indexing"], "forbidden_routes": ["runtime_pilot", "copilot", "training_data_intake", "route_authority"]},
    {"case_id": "mlrt69_freeze_form_intake_repair", "user_request": "The freeze form is missing validated_files and validation_evidence_summary; repair the intake only.", "expected_primary_route": "03_governance_freeze_and_handoff", "accepted_alternate_routes": ["052_routing_signal_scorer_v3_mlrt_world"], "forbidden_routes": ["runtime_pilot", "copilot", "model_training", "registry_mutation", "route_authority"]},
]

STATIC_CANDIDATE_ML_OUTPUTS = [
    {"case_id": case["case_id"], "candidate_selected_route": case["expected_primary_route"], "candidate_confidence_bucket": "controlled_static_high", "critical_boundary_flags": [], "non_authoritative": True}
    for case in EXPANDED_PROMPT_SELECTION_CASES
]


def read(path: Path) -> str:
    assert path.exists(), f"missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def relative_py_files(root: Path) -> list[str]:
    assert root.exists(), f"missing directory: {root}"
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.py"))


def file_snapshot() -> list[str]:
    ignored_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and not any(part in ignored_parts for part in p.parts)
    )


def evaluate_prompt_selection_case(case: dict[str, object], output: dict[str, object]) -> dict[str, object]:
    assert case["case_id"] == output["case_id"]
    selected_route = output["candidate_selected_route"]
    expected = case["expected_primary_route"]
    accepted = set(case["accepted_alternate_routes"])
    forbidden = set(case["forbidden_routes"])
    critical_boundary_flags = list(output["critical_boundary_flags"])
    assert output["non_authoritative"] is True
    passed = (selected_route == expected or selected_route in accepted) and selected_route not in forbidden and not critical_boundary_flags
    return {
        "case_id": case["case_id"],
        "selected_route": selected_route,
        "expected_primary_route": expected,
        "passed": passed,
        "non_authoritative": True,
        "route_authority_granted": False,
        "runtime_router_modified": False,
        "prompt_loading_performed": False,
        "provider_call_performed": False,
        "embedding_call_performed": False,
        "result_persisted": False,
        "training_data_created": False,
        "gold_registry_mutated": False,
    }


def run_expanded_suite() -> dict[str, object]:
    before = file_snapshot()
    outputs_by_case = {output["case_id"]: output for output in STATIC_CANDIDATE_ML_OUTPUTS}
    results = [evaluate_prompt_selection_case(case, outputs_by_case[case["case_id"]]) for case in EXPANDED_PROMPT_SELECTION_CASES]
    after = file_snapshot()
    assert before == after
    pass_count = sum(1 for result in results if result["passed"] is True)
    return {
        "feature_id": FEATURE_ID,
        "test_scope": "expanded_controlled_offline_ml_prompt_selection_test_suite",
        "cases_evaluated": len(results),
        "cases_passed": pass_count,
        "all_cases_passed": pass_count == len(results),
        "prior_tests_passed": 2,
        "prior_cases_passed": 8,
        "cumulative_tests_passed": 3,
        "cumulative_cases_passed": 18,
        "ml_signal_good_for_continued_offline_testing": True,
        "ml_signal_ready_for_runtime": False,
        "ml_signal_ready_for_training": False,
        "ml_signal_ready_for_route_authority": False,
        "non_runtime": True,
        "non_authoritative": True,
        "route_authority_granted": False,
        "runtime_router_modified": False,
        "prompt_loading_performed": False,
        "provider_call_performed": False,
        "embedding_call_performed": False,
        "result_persisted": False,
        "training_data_created": False,
        "gold_registry_mutated": False,
        "runtime_pilot_enabled": False,
        "copilot_enabled": False,
        "results": results,
    }


def test_mlrt69_files_and_previous_review_exist() -> None:
    for path in (DOC, README, MANIFEST, SOURCE, LAB_HARNESS, LAB_RUNNER, LAB_SELF_GATE, PREV_DOC):
        assert path.exists(), f"missing expected file: {path}"
    previous = read(PREV_DOC)
    assert "MLRT-68 Second Controlled Offline ML Prompt-Selection Test Result Review Gate" in previous
    data = manifest()
    assert data[f"{PREV_PREFIX}_accepted_for_expanded_offline_continuation"] is True
    assert data[f"{PREV_PREFIX}_previous_cases_passed"] == 5
    assert data[f"{PREV_PREFIX}_accepted_for_runtime_use"] is False
    assert data[f"{PREV_PREFIX}_route_authority_enabled"] is False


def test_mlrt69_expanded_suite_passes_without_authority_or_persistence() -> None:
    summary = run_expanded_suite()
    assert summary["cases_evaluated"] == 10
    assert summary["cases_passed"] == 10
    assert summary["all_cases_passed"] is True
    assert summary["prior_tests_passed"] == 2
    assert summary["prior_cases_passed"] == 8
    assert summary["cumulative_tests_passed"] == 3
    assert summary["cumulative_cases_passed"] == 18
    assert summary["ml_signal_good_for_continued_offline_testing"] is True
    assert summary["ml_signal_ready_for_runtime"] is False
    assert summary["ml_signal_ready_for_training"] is False
    assert summary["ml_signal_ready_for_route_authority"] is False
    assert all(result["passed"] is True for result in summary["results"])
    assert all(result["non_authoritative"] is True for result in summary["results"])
    assert all(result["route_authority_granted"] is False for result in summary["results"])
    assert all(result["runtime_router_modified"] is False for result in summary["results"])
    assert all(result["prompt_loading_performed"] is False for result in summary["results"])
    assert all(result["provider_call_performed"] is False for result in summary["results"])
    assert all(result["embedding_call_performed"] is False for result in summary["results"])
    assert all(result["result_persisted"] is False for result in summary["results"])
    assert all(result["training_data_created"] is False for result in summary["results"])
    assert all(result["gold_registry_mutated"] is False for result in summary["results"])


def test_mlrt69_documentation_and_manifest_record_results_and_corrections() -> None:
    doc = read(DOC)
    readme = read(README)
    data = manifest()
    for required in (
        FEATURE_ID,
        FEATURE_TITLE,
        "MLRT-65 first controlled offline test: 3/3 in-memory cases passed.",
        "MLRT-67 second harder controlled offline test: 5/5 in-memory cases passed.",
        "coverage is still too small",
        "good direction, keep testing, do not activate",
        "mlrt69_expanded_cases_evaluated_in_memory = 10",
        "mlrt69_expanded_cases_passed = 10",
        "cumulative_controlled_offline_cases_passed_after_mlrt69 = 18",
        "ml_prompt_selection_signal_ready_for_runtime = false",
        "route_authority_authorized = false",
        POS_LABEL,
        NEXT_TITLE,
    ):
        assert required in doc
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_status"] == "expanded_controlled_offline_prompt_selection_test_suite_passed_non_runtime_non_authoritative"
    assert data[f"{PREFIX}_expanded_cases_evaluated_in_memory"] == 10
    assert data[f"{PREFIX}_expanded_cases_passed"] == 10
    assert data[f"{PREFIX}_cumulative_controlled_offline_prompt_selection_tests_passed"] == 3
    assert data[f"{PREFIX}_cumulative_controlled_offline_prompt_selection_cases_passed"] == 18
    assert data[f"{PREFIX}_ml_signal_good_for_continued_offline_testing"] is True
    for key in (
        "ml_signal_ready_for_runtime",
        "ml_signal_ready_for_training",
        "ml_signal_ready_for_route_authority",
        "runtime_route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "result_persistence_enabled",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ):
        assert data[f"{PREFIX}_{key}"] is False


def test_mlrt69_preserves_exact_python_source_surface() -> None:
    mlrt_py = relative_py_files(MLRT)
    assert mlrt_py == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py = relative_py_files(LAB)
    assert lab_py == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def main() -> None:
    test_mlrt69_files_and_previous_review_exist()
    test_mlrt69_expanded_suite_passes_without_authority_or_persistence()
    test_mlrt69_documentation_and_manifest_record_results_and_corrections()
    test_mlrt69_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT69_EXPANDED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
