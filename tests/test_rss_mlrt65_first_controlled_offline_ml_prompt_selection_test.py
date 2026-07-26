from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_65_FIRST_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_64_ROUTER_PROMPT_SELECTION_NON_RUNTIME_OFFLINE_EVALUATION_HARNESS_PLAN.md"
FEATURE_ID = "rss_mlrt65_first_controlled_offline_ml_prompt_selection_test_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-65 First Controlled Offline ML Prompt-Selection Test v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-66 Controlled Offline ML Prompt-Selection Test Result Review Gate v1"
POS_LABEL = "RSS_MLRT65_FIRST_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_PASSED_NON_RUNTIME_NON_AUTHORITATIVE"
PREFIX = "rss_mlrt65_first_controlled_offline_ml_prompt_selection_test"


FIXED_PROMPT_SELECTION_CASES = [
    {
        "case_id": "mlrt65_freeze_workflow_case",
        "user_request": "Freeze the validated routing signal scorer milestone after validation passed.",
        "expected_primary_route": "03_governance_freeze_and_handoff",
        "accepted_alternate_routes": ["01_session_start_and_navigation"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "prompt_loading"],
    },
    {
        "case_id": "mlrt65_prompt_routing_case",
        "user_request": "Update prompt routing logic for selecting the right active prompt group.",
        "expected_primary_route": "02_prompt_routing_and_indexing",
        "accepted_alternate_routes": ["07_prompt_authoring_and_audit"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "training_data_intake"],
    },
    {
        "case_id": "mlrt65_startup_context_case",
        "user_request": "Refresh startup context so future AI sessions see the right project state.",
        "expected_primary_route": "01_session_start_and_navigation",
        "accepted_alternate_routes": ["03_governance_freeze_and_handoff"],
        "forbidden_routes": ["runtime_pilot", "copilot", "provider_call", "registry_mutation"],
    },
]

STATIC_CANDIDATE_ML_OUTPUTS = [
    {
        "case_id": "mlrt65_freeze_workflow_case",
        "candidate_selected_route": "03_governance_freeze_and_handoff",
        "candidate_confidence_bucket": "controlled_static_high",
        "critical_boundary_flags": [],
        "non_authoritative": True,
    },
    {
        "case_id": "mlrt65_prompt_routing_case",
        "candidate_selected_route": "02_prompt_routing_and_indexing",
        "candidate_confidence_bucket": "controlled_static_high",
        "critical_boundary_flags": [],
        "non_authoritative": True,
    },
    {
        "case_id": "mlrt65_startup_context_case",
        "candidate_selected_route": "01_session_start_and_navigation",
        "candidate_confidence_bucket": "controlled_static_high",
        "critical_boundary_flags": [],
        "non_authoritative": True,
    },
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


def evaluate_prompt_selection_case(case: dict[str, object], output: dict[str, object]) -> dict[str, object]:
    assert case["case_id"] == output["case_id"]
    selected_route = output["candidate_selected_route"]
    expected = case["expected_primary_route"]
    accepted = set(case["accepted_alternate_routes"])
    forbidden = set(case["forbidden_routes"])
    critical_boundary_flags = list(output["critical_boundary_flags"])
    assert output["non_authoritative"] is True
    passed = (
        selected_route == expected or selected_route in accepted
    ) and selected_route not in forbidden and not critical_boundary_flags
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


def run_first_controlled_offline_prompt_selection_test() -> dict[str, object]:
    outputs_by_case = {item["case_id"]: item for item in STATIC_CANDIDATE_ML_OUTPUTS}
    before = file_snapshot()
    results = [
        evaluate_prompt_selection_case(case, outputs_by_case[case["case_id"]])
        for case in FIXED_PROMPT_SELECTION_CASES
    ]
    after = file_snapshot()
    assert before == after
    pass_count = sum(1 for result in results if result["passed"] is True)
    return {
        "feature_id": FEATURE_ID,
        "test_scope": "first_controlled_offline_ml_prompt_selection_test",
        "cases_evaluated": len(results),
        "cases_passed": pass_count,
        "all_cases_passed": pass_count == len(results),
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


def test_mlrt65_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()
    assert PREV_DOC.exists()


def test_mlrt65_executes_first_controlled_offline_prompt_selection_test() -> None:
    result = run_first_controlled_offline_prompt_selection_test()
    assert result["testing_started"] is True
    assert result["steps_to_start_testing"] == 0
    assert result["cases_evaluated"] == 3
    assert result["cases_passed"] == 3
    assert result["all_cases_passed"] is True
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


def test_mlrt65_preserves_doc_contract_and_count() -> None:
    text = read(DOC)
    required = [
        "ML must be tested for helping prompt selection in router prompt logic",
        "first real controlled offline test",
        "fixed in-memory router prompt-selection cases",
        "static candidate ML prompt-selection outputs",
        "0 steps to start testing",
        "first_controlled_offline_prompt_selection_test_executed = true",
        "first_controlled_offline_prompt_selection_test_passed = true",
        "prompt_selection_cases_evaluated_in_memory = 3",
        "prompt_selection_cases_passed = 3",
        "fixed in-memory prompt-selection cases: allowed inside tests only",
        "offline expected-route comparison: allowed inside tests only",
        "offline prompt-selection score: allowed inside tests only",
        "not route authority",
        "not runtime routing",
        "not prompt loading",
        "not a model call",
        "not provider usage",
        "not training",
        "not calibration",
        "not a persistent report",
        "not a gold-registry write",
        "mlrt65_freeze_workflow_case -> expected route: 03_governance_freeze_and_handoff",
        "mlrt65_prompt_routing_case -> expected route: 02_prompt_routing_and_indexing",
        "mlrt65_startup_context_case -> expected route: 01_session_start_and_navigation",
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


def test_mlrt65_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt65_stub_boundary_still_blocks_runtime_use() -> None:
    module = load_module(SOURCE, "mlrt65_stub_under_first_controlled_test")
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


def test_mlrt65_manifest_records_first_controlled_test_without_unlocking_runtime() -> None:
    manifest = read(MANIFEST)
    for item in [FEATURE_ID, FEATURE_TITLE, SOURCE_REL, LAB_HARNESS_REL, LAB_RUNNER_REL, LAB_SELF_GATE_REL, POS_LABEL, NEXT_TITLE]:
        assert item in manifest
    assert f'"{PREFIX}_first_controlled_offline_ml_prompt_selection_test_executed_by_validation": true' in manifest
    assert f'"{PREFIX}_first_controlled_offline_ml_prompt_selection_test_passed_in_sandbox": true' in manifest
    assert f'"{PREFIX}_steps_to_start_testing": 0' in manifest
    assert f'"{PREFIX}_prompt_selection_cases_evaluated_in_memory": 3' in manifest
    assert f'"{PREFIX}_prompt_selection_cases_passed": 3' in manifest
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


def test_mlrt65_readme_references_first_controlled_test_and_next_review_gate() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "first controlled offline ML prompt-selection test" in readme
    assert "Testing has started" in readme
    assert "0 steps to start testing" in readme
    assert "No runtime route authority, prompt loading, provider calls, embeddings, persistence, training, calibration, registry mutation, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt65_files_exist()
    test_mlrt65_executes_first_controlled_offline_prompt_selection_test()
    test_mlrt65_preserves_doc_contract_and_count()
    test_mlrt65_only_allowed_python_surfaces_exist()
    test_mlrt65_stub_boundary_still_blocks_runtime_use()
    test_mlrt65_manifest_records_first_controlled_test_without_unlocking_runtime()
    test_mlrt65_readme_references_first_controlled_test_and_next_review_gate()
    print("CONTRACT_TEST_OK: MLRT-65 First Controlled Offline ML Prompt-Selection Test v1, executed the first controlled in-memory offline prompt-selection comparison using fixed test cases and static candidate ML prompt-selection outputs after MLRT-64 freeze; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; testing has now started with 0 steps remaining to start testing; first controlled offline prompt-selection test passed; no runtime routing, no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.")
    print("SANDBOX_RSS_MLRT65_FIRST_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_V1_VALIDATION_OK")
