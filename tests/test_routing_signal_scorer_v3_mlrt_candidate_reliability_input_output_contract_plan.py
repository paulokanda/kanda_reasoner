from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"

FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_reliability_input_output_contract_plan_v1"
DOC = MLRT / "MLRT_1_CANDIDATE_RELIABILITY_INPUT_OUTPUT_CONTRACT_PLAN.md"
README = MLRT / "README.md"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}
FORBIDDEN_DOC_TERMS = [
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
FORBIDDEN_OUTPUT_FIELDS = [
    "route_decision",
    "load_prompt",
    "execute_route",
    "approve_readiness",
    "write_freeze_memory",
    "write_prompt_library",
    "write_router_canon",
    "activate_pilot",
    "activate_copilot",
    "call_provider",
    "call_embedding_model",
    "persist_ml_decision",
    "runtime_command",
    "copilot_instruction",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt1_docs_exist() -> None:
    assert README.exists()
    assert DOC.exists()


def test_mlrt1_is_contract_planning_only_and_not_algorithm_testing() -> None:
    text = read(DOC)
    assert FEATURE_ID in text
    assert "does not test the ML/router algorithm" in text
    assert "does not execute a candidate" in text
    assert "does not execute cases" in text
    assert "does not score cases" in text
    assert "does not unlock ML implementation" in text
    assert "MLRT-2 - Candidate Package Intake Contract Plan" in text


def test_mlrt1_defines_future_input_output_and_rejection_envelopes() -> None:
    text = read(DOC)
    assert "Candidate reliability input envelope doctrine" in text
    assert "Candidate reliability output envelope doctrine" in text
    assert "Rejection envelope doctrine" in text
    assert "non_authoritative_candidate_reliability_output_record" in text
    assert "input_envelope_id" in text
    assert "output_record_id" in text
    assert "rejection_record_id" in text
    assert "pass_1_canon_match" in text
    assert "pass_2_disagreement_or_improvement" in text
    assert "yield_to_canon" in text


def test_mlrt1_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    for term in FORBIDDEN_DOC_TERMS:
        assert term in text
    for field in FORBIDDEN_OUTPUT_FIELDS:
        assert field in text
    assert "The critical boundary error budget remains `0`." in text
    assert "Candidate output remains non-authoritative." in text


def test_mlrt1_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt1_does_not_create_forbidden_implementation_paths() -> None:
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
        "schemas",
        "validators",
        "runner",
        "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_box_manifest_records_mlrt1_boundary() -> None:
    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_reliability_input_output_contract_plan"
    assert data[f"{prefix}_feature_id"] == FEATURE_ID
    assert data[f"{prefix}_doc"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_1_CANDIDATE_RELIABILITY_INPUT_OUTPUT_CONTRACT_PLAN.md"
    assert data[f"{prefix}_readme"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
    assert data[f"{prefix}_test"] == "tests/test_routing_signal_scorer_v3_mlrt_candidate_reliability_input_output_contract_plan.py"
    assert data[f"{prefix}_documentation_only"] is True
    assert data[f"{prefix}_contract_planning_only"] is True
    assert data[f"{prefix}_candidate_executed"] is False
    assert data[f"{prefix}_cases_executed"] is False
    assert data[f"{prefix}_cases_scored"] is False
    assert data[f"{prefix}_candidate_outputs_created"] is False
    assert data[f"{prefix}_route_authority"] is False
    assert data[f"{prefix}_prompt_loading"] is False
    assert data[f"{prefix}_provider_calls"] is False
    assert data[f"{prefix}_embeddings"] is False
    assert data[f"{prefix}_persistence"] is False
    assert data[f"{prefix}_activation_key"] is False
    assert data[f"{prefix}_field_test_mode"] is False
    assert data[f"{prefix}_runtime_pilot_behavior"] is False
    assert data[f"{prefix}_copilot_behavior"] is False
    assert data[f"{prefix}_candidate_reliability_validated"] is False
    assert data[f"{prefix}_ml_implementation_unlocked"] is False
    assert data[f"{prefix}_critical_boundary_error_budget"] == 0
    assert data[f"{prefix}_positive_label"] == "MLRT_IO_CONTRACT_READY_FOR_CANDIDATE_PACKAGE_INTAKE_PLANNING_ONLY"
    assert data[f"{prefix}_next_safe_milestone"] == "MLRT-2 Candidate Package Intake Contract Plan after MLRT-1 freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_mlrt1_docs_exist()
    test_mlrt1_is_contract_planning_only_and_not_algorithm_testing()
    test_mlrt1_defines_future_input_output_and_rejection_envelopes()
    test_mlrt1_preserves_forbidden_boundaries()
    test_mlrt1_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt1_does_not_create_forbidden_implementation_paths()
    test_box_manifest_records_mlrt1_boundary()
    print(
        "CONTRACT_TEST_OK: MLRT-1 Candidate Reliability Input/Output Contract Plan v1, "
        "immutable governed documentation-only input/output contract planning after MLRT-0 freeze with FREEZE_MEMORY_STATUS OK, "
        "defines future non-authoritative candidate reliability input envelope, output envelope, and rejection envelope doctrine only, "
        "candidate reliability not validated, ML implementation not unlocked, no executable validators, no schema code, no candidate implementation, "
        "no candidate execution, no candidate outputs created, no case execution, no case scoring, no route comparison, no route authority, "
        "no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, "
        "no corpus mutation, no fixture mutation, no router-canon mutation, no prompt-library mutation, no freeze-memory mutation, "
        "no gold-registry mutation, no report generation, no report persistence, no provider calls, no embeddings, no network calls, "
        "no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, "
        "no Copilot behavior, critical boundary error budget zero, candidate output remains non-authoritative, "
        "next safe milestone is MLRT-2 Candidate Package Intake Contract Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_RELIABILITY_INPUT_OUTPUT_CONTRACT_PLAN_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
