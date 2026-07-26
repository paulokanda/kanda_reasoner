from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"

FEATURE_ID = "routing_signal_scorer_v3_mlrt_controlled_non_runtime_candidate_reliability_test_plan_v1"
DOC = MLRT / "MLRT_0_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLAN.md"
README = MLRT / "README.md"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}
FORBIDDEN_TERMS = [
    "route authority",
    "prompt loading",
    "provider calls",
    "embedding",
    "persistent ML decisions",
    "activation",
    "field-test",
    "runtime Pilot",
    "Copilot behavior",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt0_docs_exist() -> None:
    assert README.exists()
    assert DOC.exists()


def test_mlrt0_is_planning_only_and_not_algorithm_testing() -> None:
    text = read(DOC)
    assert FEATURE_ID in text
    assert "does not test the ML/router algorithm yet" in text
    assert "does not execute a candidate" in text
    assert "does not execute cases" in text
    assert "does not score cases" in text
    assert "does not unlock ML implementation" in text
    assert "MLRT-1 - Candidate Reliability Input/Output Contract Plan" in text


def test_mlrt0_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    for term in FORBIDDEN_TERMS:
        assert term in text
    assert "The critical boundary error budget remains `0`." in text
    assert "Candidate output remains non-authoritative." in text


def test_mlrt0_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt0_does_not_create_forbidden_implementation_paths() -> None:
    forbidden_paths = [
        "candidate",
        "candidate_outputs",
        "candidate_results",
        "reliability_results",
        "runtime_activation",
        "provider_adapter",
        "embedding_adapter",
        "prompt_loader",
        "persistent_ml_decisions",
        "reports",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_box_manifest_records_mlrt0_boundary() -> None:
    data = json.loads(read(MANIFEST))
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_feature_id"] == FEATURE_ID
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_doc"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_0_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLAN.md"
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_readme"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_test"] == "tests/test_routing_signal_scorer_v3_mlrt_controlled_non_runtime_candidate_reliability_test_plan.py"
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_documentation_only"] is True
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_candidate_executed"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_cases_executed"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_cases_scored"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_route_authority"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_prompt_loading"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_provider_calls"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_embeddings"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_persistence"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_activation_key"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_field_test_mode"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_runtime_pilot_behavior"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_copilot_behavior"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_candidate_reliability_validated"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_ml_implementation_unlocked"] is False
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_critical_boundary_error_budget"] == 0
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_positive_label"] == "MLRT_PLAN_READY_FOR_INPUT_OUTPUT_CONTRACT_PLANNING_ONLY"
    assert data["mlrt_controlled_non_runtime_candidate_reliability_test_plan_next_safe_milestone"] == "MLRT-1 Candidate Reliability Input/Output Contract Plan after MLRT-0 freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_mlrt0_docs_exist()
    test_mlrt0_is_planning_only_and_not_algorithm_testing()
    test_mlrt0_preserves_forbidden_boundaries()
    test_mlrt0_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt0_does_not_create_forbidden_implementation_paths()
    test_box_manifest_records_mlrt0_boundary()
    print(
        "CONTRACT_TEST_OK: MLRT-0 Controlled Non-Runtime ML/Router Candidate Reliability Test Plan v1, "
        "immutable governed documentation-only reliability-test planning after LAB-13 freeze with FREEZE_MEMORY_STATUS OK, "
        "defines candidate reliability test planning boundaries and preconditions only, candidate reliability not validated, "
        "ML implementation not unlocked, no candidate implementation, no candidate execution, no case execution, no case scoring, "
        "no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, "
        "no live router-canon reads, no runtime router imports, no corpus mutation, no fixture mutation, no router-canon mutation, "
        "no prompt-library mutation, no freeze-memory mutation, no gold-registry mutation, no report generation, no report persistence, "
        "no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, "
        "no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, "
        "candidate output remains non-authoritative, next safe milestone is MLRT-1 Candidate Reliability Input/Output Contract Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLAN_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
