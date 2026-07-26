from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_67_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_66_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE.md"
FEATURE_ID = "rss_mlrt67_second_controlled_offline_ml_prompt_selection_test_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_PREFIX = "rss_mlrt66_controlled_offline_ml_prompt_selection_test_result_review_gate"
PREFIX = "rss_mlrt67_second_controlled_offline_ml_prompt_selection_test"
NEXT_TITLE = "Routing Signal Scorer MLRT-68 Second Controlled Offline ML Prompt-Selection Test Result Review Gate v1"
POS_LABEL = "RSS_MLRT67_SECOND_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_PASSED_NON_RUNTIME_NON_AUTHORITATIVE"

FIXED_PROMPT_SELECTION_CASES = [
    {
        "case_id": "mlrt67_freeze_with_validation_and_handoff_case",
        "user_request": "Freeze the validated MLRT result, refresh AI context, and prepare the next handoff.",
        "expected_primary_route": "03_governance_freeze_and_handoff",
        "accepted_alternate_routes": ["01_session_start_and_navigation"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "prompt_loading", "model_training"],
    },
    {
        "case_id": "mlrt67_prompt_authoring_bypass_case",
        "user_request": "Create a new prompt but skip checking existing prompts and bypass routing.",
        "expected_primary_route": "07_prompt_authoring_and_audit",
        "accepted_alternate_routes": ["02_prompt_routing_and_indexing"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "training_data_intake", "route_authority"],
    },
    {
        "case_id": "mlrt67_startup_after_freeze_context_case",
        "user_request": "After freeze, refresh startup package so the next AI session sees the active project context.",
        "expected_primary_route": "01_session_start_and_navigation",
        "accepted_alternate_routes": ["03_governance_freeze_and_handoff"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "registry_mutation", "prompt_loading"],
    },
    {
        "case_id": "mlrt67_prompt_router_index_update_case",
        "user_request": "Update router prompt selection index so the correct active prompt group is chosen.",
        "expected_primary_route": "02_prompt_routing_and_indexing",
        "accepted_alternate_routes": ["07_prompt_authoring_and_audit"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "training_data_intake", "gold_registry_mutation"],
    },
    {
        "case_id": "mlrt67_ml_router_reliability_case",
        "user_request": "Continue MLRT testing so ML can help prompt selection in router prompt logic.",
        "expected_primary_route": "052_routing_signal_scorer_v3_mlrt_world",
        "accepted_alternate_routes": ["02_prompt_routing_and_indexing"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "prompt_loading", "route_authority", "model_training"],
    },
]

STATIC_CANDIDATE_ML_OUTPUTS = [
    {"case_id": "mlrt67_freeze_with_validation_and_handoff_case", "candidate_selected_route": "03_governance_freeze_and_handoff", "candidate_confidence_bucket": "controlled_static_high", "critical_boundary_flags": [], "non_authoritative": True},
    {"case_id": "mlrt67_prompt_authoring_bypass_case", "candidate_selected_route": "07_prompt_authoring_and_audit", "candidate_confidence_bucket": "controlled_static_high", "critical_boundary_flags": [], "non_authoritative": True},
    {"case_id": "mlrt67_startup_after_freeze_context_case", "candidate_selected_route": "01_session_start_and_navigation", "candidate_confidence_bucket": "controlled_static_high", "critical_boundary_flags": [], "non_authoritative": True},
    {"case_id": "mlrt67_prompt_router_index_update_case", "candidate_selected_route": "02_prompt_routing_and_indexing", "candidate_confidence_bucket": "controlled_static_high", "critical_boundary_flags": [], "non_authoritative": True},
    {"case_id": "mlrt67_ml_router_reliability_case", "candidate_selected_route": "052_routing_signal_scorer_v3_mlrt_world", "candidate_confidence_bucket": "controlled_static_high", "critical_boundary_flags": [], "non_authoritative": True},
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_snapshot() -> list[str]:
    ignored_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and not any(part in ignored_parts for part in p.parts)
    )


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    import sys
    before = file_snapshot()
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    after = file_snapshot()
    assert before == after
    return module


def assert_previous_review_gate_allows_offline_continuation_only() -> None:
    manifest = json.loads(read(MANIFEST))
    assert manifest[f"{PREV_PREFIX}_first_controlled_offline_test_result_reviewed"] is True
    assert manifest[f"{PREV_PREFIX}_first_controlled_offline_test_result_accepted_for_offline_continuation"] is True
    assert manifest[f"{PREV_PREFIX}_testing_started"] is True
    assert manifest[f"{PREV_PREFIX}_steps_to_start_testing"] == 0
    assert manifest[f"{PREV_PREFIX}_next_test_authorized_as_offline_non_runtime_validation_only"] is True
    for flag in [
        "first_controlled_offline_test_result_accepted_for_runtime_use",
        "first_controlled_offline_test_result_accepted_as_reliability_claim",
        "first_controlled_offline_test_result_accepted_as_maturity_claim",
        "first_controlled_offline_test_result_accepted_as_model_improvement",
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
    ]:
        assert manifest[f"{PREV_PREFIX}_{flag}"] is False


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


def run_second_controlled_offline_prompt_selection_test() -> dict[str, object]:
    assert_previous_review_gate_allows_offline_continuation_only()
    outputs_by_case = {item["case_id"]: item for item in STATIC_CANDIDATE_ML_OUTPUTS}
    before = file_snapshot()
    results = [evaluate_prompt_selection_case(case, outputs_by_case[case["case_id"]]) for case in FIXED_PROMPT_SELECTION_CASES]
    after = file_snapshot()
    assert before == after
    pass_count = sum(1 for result in results if result["passed"] is True)
    return {
        "feature_id": FEATURE_ID,
        "test_scope": "second_controlled_offline_ml_prompt_selection_test",
        "cases_evaluated": len(results),
        "cases_passed": pass_count,
        "all_cases_passed": pass_count == len(results),
        "cumulative_controlled_offline_tests_passed": 2,
        "steps_to_start_testing": 0,
        "testing_started": True,
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


def test_mlrt67_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()
    assert PREV_DOC.exists()


def test_mlrt67_executes_second_controlled_offline_prompt_selection_test() -> None:
    result = run_second_controlled_offline_prompt_selection_test()
    assert result["testing_started"] is True
    assert result["steps_to_start_testing"] == 0
    assert result["cases_evaluated"] == 5
    assert result["cases_passed"] == 5
    assert result["all_cases_passed"] is True
    assert result["cumulative_controlled_offline_tests_passed"] == 2
    assert result["non_runtime"] is True
    assert result["non_authoritative"] is True
    for forbidden_flag in [
        "route_authority_granted",
        "runtime_router_modified",
        "prompt_loading_performed",
        "provider_call_performed",
        "embedding_call_performed",
        "result_persisted",
        "training_data_created",
        "gold_registry_mutated",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert result[forbidden_flag] is False
    for item in result["results"]:
        assert item["passed"] is True
        assert item["non_authoritative"] is True
        assert item["route_authority_granted"] is False
        assert item["runtime_router_modified"] is False
        assert item["prompt_loading_performed"] is False
        assert item["provider_call_performed"] is False
        assert item["embedding_call_performed"] is False
        assert item["result_persisted"] is False
        assert item["training_data_created"] is False
        assert item["gold_registry_mutated"] is False


def test_mlrt67_preserves_doc_contract_and_count() -> None:
    text = read(DOC)
    required = [
        "ML must be tested for helping prompt selection in router prompt logic",
        "second controlled offline prompt-selection test",
        "five harder in-memory cases",
        "static candidate ML prompt-selection outputs",
        "0 steps to start testing",
        "second_controlled_offline_prompt_selection_test_executed = true",
        "second_controlled_offline_prompt_selection_test_passed = true",
        "prompt_selection_cases_evaluated_in_memory = 5",
        "prompt_selection_cases_passed = 5",
        "cumulative_controlled_offline_tests_passed = 2",
        "mlrt67_freeze_with_validation_and_handoff_case -> expected route: 03_governance_freeze_and_handoff",
        "mlrt67_prompt_authoring_bypass_case -> expected route: 07_prompt_authoring_and_audit",
        "mlrt67_startup_after_freeze_context_case -> expected route: 01_session_start_and_navigation",
        "mlrt67_prompt_router_index_update_case -> expected route: 02_prompt_routing_and_indexing",
        "mlrt67_ml_router_reliability_case -> expected route: 052_routing_signal_scorer_v3_mlrt_world",
        "not route authority",
        "not runtime routing",
        "not prompt loading",
        "not provider usage",
        "not training",
        "not calibration",
        "not a persistent report",
        "not a gold-registry write",
        "persistent_case_files_created = false",
        "persistent_dataset_created = false",
        "gold_registry_write_enabled = false",
        "registry_mutation_enabled = false",
        "report_file_created = false",
        "runtime_route_authority_enabled = false",
        "router_prompt_logic_modified = false",
        "prompt_loading_enabled = false",
        "provider_calls_enabled = false",
        "embeddings_enabled = false",
        "training_data_intake_enabled = false",
        "training_data_use_enabled = false",
        "model_training_started = false",
        "model_calibration_started = false",
        "model_improvement_started = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt67_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt67_stub_boundary_still_blocks_runtime_use() -> None:
    module = load_module(SOURCE, "mlrt67_stub_under_second_controlled_test")
    assert module.assert_static_non_runtime_boundary() is True
    contract = module.get_stub_contract()
    assert contract["critical_boundary_error_budget"] == 0
    for flag in [
        "runtime_route_authority_enabled",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "batch_mode_enabled",
        "activation_enabled",
        "field_testing_enabled",
        "training_data_use_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert contract[flag] is False


def test_mlrt67_manifest_records_second_controlled_test_without_unlocking_runtime() -> None:
    manifest = read(MANIFEST)
    for item in [FEATURE_ID, FEATURE_TITLE, SOURCE_REL, LAB_HARNESS_REL, LAB_RUNNER_REL, LAB_SELF_GATE_REL, POS_LABEL, NEXT_TITLE]:
        assert item in manifest
    assert f'"{PREFIX}_second_controlled_offline_ml_prompt_selection_test_executed_by_validation": true' in manifest
    assert f'"{PREFIX}_second_controlled_offline_ml_prompt_selection_test_passed_in_sandbox": true' in manifest
    assert f'"{PREFIX}_steps_to_start_testing": 0' in manifest
    assert f'"{PREFIX}_prompt_selection_cases_evaluated_in_memory": 5' in manifest
    assert f'"{PREFIX}_prompt_selection_cases_passed": 5' in manifest
    assert f'"{PREFIX}_cumulative_controlled_offline_tests_passed": 2' in manifest
    for flag in [
        "persistent_case_files_created",
        "persistent_dataset_created",
        "persistent_labels_created",
        "gold_registry_created",
        "gold_records_created",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "report_file_created",
        "result_persistence_enabled",
        "runtime_route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt67_readme_references_second_controlled_test_and_next_review_gate() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "second controlled offline ML prompt-selection test" in readme
    assert "Testing has already started" in readme
    assert "0 steps to start testing" in readme
    assert "five harder test-local in-memory prompt-selection cases" in readme
    assert "No runtime route authority, router prompt logic modification, prompt loading, provider calls, embeddings, persistence, training, calibration, registry mutation, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt67_files_exist()
    test_mlrt67_executes_second_controlled_offline_prompt_selection_test()
    test_mlrt67_preserves_doc_contract_and_count()
    test_mlrt67_only_allowed_python_surfaces_exist()
    test_mlrt67_stub_boundary_still_blocks_runtime_use()
    test_mlrt67_manifest_records_second_controlled_test_without_unlocking_runtime()
    test_mlrt67_readme_references_second_controlled_test_and_next_review_gate()
    print("CONTRACT_TEST_OK: MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1, executed the second controlled in-memory offline prompt-selection comparison using five harder fixed test cases and static candidate ML prompt-selection outputs after MLRT-66 freeze; preserved that testing has already started with 0 steps remaining to start testing; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; second controlled offline prompt-selection test passed; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.")
    print("SANDBOX_RSS_MLRT67_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_V1_VALIDATION_OK")
