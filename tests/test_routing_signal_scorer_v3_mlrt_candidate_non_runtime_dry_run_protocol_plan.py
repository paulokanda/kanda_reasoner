from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"

FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_protocol_plan_v1"
DOC = MLRT / "MLRT_7_CANDIDATE_NON_RUNTIME_DRY_RUN_PROTOCOL_PLAN.md"
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
FORBIDDEN_PROTOCOL_FIELDS = [
    "route_decision",
    "load_prompt",
    "execute_route",
    "execute_dry_run",
    "approve_readiness",
    "approve_reliability",
    "approve_dry_run_execution",
    "record_human_approval",
    "write_freeze_memory",
    "write_prompt_library",
    "write_router_canon",
    "activate_pilot",
    "activate_copilot",
    "call_provider",
    "call_embedding_model",
    "network_call",
    "subprocess_call",
    "persist_ml_decision",
    "runtime_command",
    "copilot_instruction",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt7_docs_exist() -> None:
    assert README.exists()
    assert DOC.exists()


def test_mlrt7_is_dry_run_protocol_planning_only() -> None:
    text = read(DOC)
    assert FEATURE_ID in text
    assert "does not execute a dry run" in text
    assert "does not create dry-run protocol records" in text
    assert "does not create dry-run protocol execution records" in text
    assert "does not create dry-run inputs" in text
    assert "does not create dry-run outputs" in text
    assert "does not read dry-run readiness gates as live evidence" in text
    assert "does not approve a candidate package for dry-run execution" in text
    assert "does not create, accept, install, import, execute, validate, score, compare, or evaluate a candidate package" in text
    assert "There is no candidate reliability validation in MLRT-7 and there is no ML implementation unlock" in text
    assert "MLRT-8 - Candidate Non-Runtime Dry-Run Input Set Plan" in text


def test_mlrt7_defines_protocol_groups() -> None:
    text = read(DOC)
    assert "Dry-run protocol identity and traceability doctrine" in text
    assert "Required dry-run readiness gate reference doctrine" in text
    assert "Non-runtime execution boundary doctrine" in text
    assert "Candidate package reference doctrine" in text
    assert "Static input set planning doctrine" in text
    assert "Candidate invocation envelope planning doctrine" in text
    assert "Output capture envelope planning doctrine" in text
    assert "Failure and rejection envelope planning doctrine" in text
    assert "Critical boundary blocker doctrine" in text
    assert "Human-escalation doctrine" in text
    assert "Protocol planning label doctrine" in text
    assert "Dry-run protocol non-authority doctrine" in text
    assert "Dry-run protocol forbidden authority fields" in text


def test_mlrt7_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    for term in FORBIDDEN_DOC_TERMS:
        assert term in text
    for field in FORBIDDEN_PROTOCOL_FIELDS:
        assert field in text
    assert "The critical boundary error budget remains `0`." in text
    assert "Neither MLRT-6 nor MLRT-7 validates candidate reliability." in text


def test_mlrt7_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_DRY_RUN_PROTOCOL_READY_FOR_INPUT_SET_PLANNING_ONLY" in text
    assert "does not mean that a protocol record exists" in text
    assert "does not mean dry-run inputs exist" in text
    assert "does not mean a dry run can execute" in text
    assert "does not mean candidate outputs exist" in text
    assert "does not mean a candidate is reliable" in text
    assert "does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot" in text


def test_mlrt7_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt7_does_not_create_forbidden_implementation_paths() -> None:
    forbidden_paths = [
        "candidate",
        "candidate_package",
        "candidate_packages",
        "candidate_outputs",
        "candidate_results",
        "package_intake_records",
        "static_review",
        "static_review_records",
        "static_review_results",
        "static_review_evidence",
        "static_review_evidence_records",
        "static_review_outcome",
        "static_review_outcome_records",
        "outcome_gate",
        "outcome_gate_records",
        "dry_run",
        "dry_run_readiness",
        "dry_run_readiness_records",
        "dry_run_protocol",
        "dry_run_protocol_records",
        "dry_run_protocol_execution_records",
        "dry_run_inputs",
        "dry_run_outputs",
        "evidence_envelopes",
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


def test_box_manifest_records_mlrt7_boundary() -> None:
    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_non_runtime_dry_run_protocol_plan"
    assert data[f"{prefix}_feature_id"] == FEATURE_ID
    assert data[f"{prefix}_doc"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_7_CANDIDATE_NON_RUNTIME_DRY_RUN_PROTOCOL_PLAN.md"
    assert data[f"{prefix}_readme"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
    assert data[f"{prefix}_test"] == "tests/test_routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_protocol_plan.py"
    assert data[f"{prefix}_documentation_only"] is True
    assert data[f"{prefix}_dry_run_protocol_planning_only"] is True
    assert data[f"{prefix}_dry_run_performed"] is False
    assert data[f"{prefix}_dry_run_protocol_records_created"] is False
    assert data[f"{prefix}_dry_run_protocol_execution_records_created"] is False
    assert data[f"{prefix}_dry_run_inputs_created"] is False
    assert data[f"{prefix}_dry_run_outputs_created"] is False
    assert data[f"{prefix}_dry_run_readiness_review_performed"] is False
    assert data[f"{prefix}_dry_run_readiness_records_created"] is False
    assert data[f"{prefix}_static_review_performed"] is False
    assert data[f"{prefix}_static_review_outcome_records_created"] is False
    assert data[f"{prefix}_candidate_package_created"] is False
    assert data[f"{prefix}_candidate_package_accepted"] is False
    assert data[f"{prefix}_candidate_package_installed"] is False
    assert data[f"{prefix}_candidate_package_imported"] is False
    assert data[f"{prefix}_candidate_executed"] is False
    assert data[f"{prefix}_candidate_outputs_created"] is False
    assert data[f"{prefix}_cases_executed"] is False
    assert data[f"{prefix}_cases_scored"] is False
    assert data[f"{prefix}_route_authority"] is False
    assert data[f"{prefix}_prompt_loading"] is False
    assert data[f"{prefix}_provider_calls"] is False
    assert data[f"{prefix}_embeddings"] is False
    assert data[f"{prefix}_network_calls"] is False
    assert data[f"{prefix}_subprocess_calls"] is False
    assert data[f"{prefix}_batch_mode"] is False
    assert data[f"{prefix}_persistence"] is False
    assert data[f"{prefix}_report_generation"] is False
    assert data[f"{prefix}_report_persistence"] is False
    assert data[f"{prefix}_activation_key"] is False
    assert data[f"{prefix}_field_test_mode"] is False
    assert data[f"{prefix}_runtime_pilot_behavior"] is False
    assert data[f"{prefix}_copilot_behavior"] is False
    assert data[f"{prefix}_candidate_reliability_validated"] is False
    assert data[f"{prefix}_ml_implementation_unlocked"] is False
    assert data[f"{prefix}_critical_boundary_error_budget"] == 0
    assert data[f"{prefix}_positive_label"] == "MLRT_DRY_RUN_PROTOCOL_READY_FOR_INPUT_SET_PLANNING_ONLY"
    assert data[f"{prefix}_next_safe_milestone"] == "MLRT-8 Candidate Non-Runtime Dry-Run Input Set Plan after MLRT-7 freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_mlrt7_docs_exist()
    test_mlrt7_is_dry_run_protocol_planning_only()
    test_mlrt7_defines_protocol_groups()
    test_mlrt7_preserves_forbidden_boundaries()
    test_mlrt7_positive_label_is_planning_only()
    test_mlrt7_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt7_does_not_create_forbidden_implementation_paths()
    test_box_manifest_records_mlrt7_boundary()
    print(
        "CONTRACT_TEST_OK: MLRT-7 Candidate Non-Runtime Dry-Run Protocol Plan v1, "
        "immutable governed documentation-only dry-run protocol planning after MLRT-6 freeze with FREEZE_MEMORY_STATUS OK, "
        "defines future non-authoritative dry-run protocol groups for identity, readiness-gate references, non-runtime execution boundary, candidate package references, static input set planning, candidate invocation envelope, output capture envelope, failure and rejection envelope, critical boundary blockers, human escalation, protocol planning labels, non-authority doctrine, forbidden authority fields, and next-milestone doctrine only, "
        "candidate reliability not validated, ML implementation not unlocked, no executable validators, no schema code, no candidate package created, "
        "no candidate package accepted, no candidate package installed, no candidate package imported, no candidate implementation, no candidate execution, "
        "no candidate outputs created, no package intake records created, no static review performed, no static review records created, "
        "no static review evidence records created, no evidence envelopes created, no static review outcome records created, no outcome gate records created, "
        "no dry-run readiness review performed, no dry-run readiness records created, no dry-run protocol records created, no dry-run protocol execution records created, "
        "no dry run executed, no dry-run inputs created, no dry-run outputs created, no case execution, no case scoring, no route comparison, "
        "no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, "
        "no runtime router imports, no corpus mutation, no fixture mutation, no router-canon mutation, no prompt-library mutation, "
        "no freeze-memory mutation, no gold-registry mutation, no report generation, no report persistence, no provider calls, no embeddings, "
        "no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero, candidate dry-run protocol remains non-authoritative, "
        "next safe milestone is MLRT-8 Candidate Non-Runtime Dry-Run Input Set Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_NON_RUNTIME_DRY_RUN_PROTOCOL_PLAN_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
