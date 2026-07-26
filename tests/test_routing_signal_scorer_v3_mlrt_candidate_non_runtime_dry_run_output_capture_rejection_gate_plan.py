from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_10_CANDIDATE_NON_RUNTIME_DRY_RUN_OUTPUT_CAPTURE_REJECTION_GATE_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_output_capture_rejection_gate_plan_v1"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}
FORBIDDEN_AUTHORITY_FIELDS = [
    "route_decision",
    "load_prompt",
    "execute_route",
    "execute_dry_run",
    "approve_readiness",
    "approve_reliability",
    "approve_dry_run_execution",
    "record_human_approval",
    "write_freeze_memory",
    "write_gold_registry",
    "write_prompt_library",
    "write_router_canon",
    "write_startup_pack",
    "activate_pilot",
    "activate_copilot",
    "enable_field_test",
    "call_provider",
    "call_embedding_model",
    "network_call",
    "subprocess_call",
    "start_batch_mode",
    "persist_ml_decision",
    "runtime_command",
    "pilot_instruction",
    "copilot_instruction",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt10_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()


def test_mlrt10_is_rejection_gate_planning_only() -> None:
    text = read(DOC)
    assert FEATURE_ID in text
    assert "does not create output records" in text
    assert "does not create rejection records" in text
    assert "does not run any classifier, validator, or rejection gate" in text
    assert "does not create dry-run output records" in text
    assert "does not create output capture rejection records" in text
    assert "does not execute a dry run" in text
    assert "does not execute a candidate" in text
    assert "does not execute cases" in text
    assert "does not score cases" in text
    assert "does not validate candidate reliability" in text
    assert "does not unlock ML implementation" in text
    assert "MLRT-11 Candidate Non-Runtime Dry-Run Output Capture Contract-Conformance Plan" in text


def test_mlrt10_defines_rejection_gate_groups() -> None:
    text = read(DOC)
    assert "Rejection gate identity doctrine" in text
    assert "Mandatory rejection families" in text
    assert "Critical-boundary blocker doctrine" in text
    assert "Rejection outcome labels doctrine" in text
    assert "Human-review escalation doctrine" in text
    assert "No silent coercion doctrine" in text
    assert "No-live-read doctrine" in text
    assert "No mutation doctrine" in text
    assert "Forbidden authority fields" in text


def test_mlrt10_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    assert "The critical boundary error budget remains `0`." in text
    assert "Neither MLRT-9 nor MLRT-10 validates candidate reliability." in text
    assert "live prompt-library files" in text
    assert "live freeze memory" in text
    assert "live router canon" in text
    assert "provider calls" in text
    assert "embedding calls" in text
    assert "network calls" in text
    assert "subprocess calls" in text
    assert "runtime Pilot behavior" in text
    assert "Copilot behavior" in text
    assert "must not repair, normalize into safety, rewrite, reinterpret, or coerce unsafe candidate output" in text
    for field in FORBIDDEN_AUTHORITY_FIELDS:
        assert field in text


def test_mlrt10_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_OUTPUT_CAPTURE_REJECTION_GATE_READY_FOR_NON_RUNTIME_CAPTURE_CONFORMANCE_PLANNING_ONLY" in text
    assert "does not mean that output capture records exist" in text
    assert "does not mean rejection gate records exist" in text
    assert "does not mean a rejection gate has run" in text
    assert "does not mean a dry run executed" in text
    assert "does not mean candidate outputs exist" in text
    assert "does not mean output capture can validate reliability" in text
    assert "does not mean output capture can score cases" in text
    assert "does not mean a candidate package can be accepted, installed, imported, executed, scored, compared, routed, activated, field-tested, used by Pilot, or used by Copilot" in text


def test_mlrt10_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt10_does_not_create_forbidden_implementation_paths() -> None:
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
        "dry_run_input_records",
        "dry_run_input_manifests",
        "dry_run_outputs",
        "dry_run_output_records",
        "dry_run_output_manifests",
        "output_capture",
        "output_capture_envelopes",
        "output_capture_records",
        "output_capture_rejection_records",
        "output_rejection_gate",
        "output_rejection_gate_records",
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


def test_box_manifest_records_mlrt10_boundary() -> None:
    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_non_runtime_dry_run_output_capture_rejection_gate_plan"
    assert data[f"{prefix}_feature_id"] == FEATURE_ID
    assert data[f"{prefix}_doc"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_10_CANDIDATE_NON_RUNTIME_DRY_RUN_OUTPUT_CAPTURE_REJECTION_GATE_PLAN.md"
    assert data[f"{prefix}_readme"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
    assert data[f"{prefix}_test"] == "tests/test_routing_signal_scorer_v3_mlrt_candidate_non_runtime_dry_run_output_capture_rejection_gate_plan.py"
    assert data[f"{prefix}_documentation_only"] is True
    assert data[f"{prefix}_output_capture_rejection_gate_planning_only"] is True
    assert data[f"{prefix}_rejection_gate_run"] is False
    assert data[f"{prefix}_dry_run_performed"] is False
    assert data[f"{prefix}_dry_run_output_records_created"] is False
    assert data[f"{prefix}_output_capture_envelopes_created"] is False
    assert data[f"{prefix}_output_capture_rejection_records_created"] is False
    assert data[f"{prefix}_output_rejection_gate_records_created"] is False
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
    assert data[f"{prefix}_activation_key"] is False
    assert data[f"{prefix}_field_test_mode"] is False
    assert data[f"{prefix}_runtime_pilot_behavior"] is False
    assert data[f"{prefix}_copilot_behavior"] is False
    assert data[f"{prefix}_candidate_reliability_validated"] is False
    assert data[f"{prefix}_ml_implementation_unlocked"] is False
    assert data[f"{prefix}_critical_boundary_error_budget"] == 0
    assert data[f"{prefix}_positive_label"] == "MLRT_OUTPUT_CAPTURE_REJECTION_GATE_READY_FOR_NON_RUNTIME_CAPTURE_CONFORMANCE_PLANNING_ONLY"
    assert data[f"{prefix}_next_safe_milestone"] == "MLRT-11 Candidate Non-Runtime Dry-Run Output Capture Contract-Conformance Plan after MLRT-10 freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_mlrt10_docs_exist()
    test_mlrt10_is_rejection_gate_planning_only()
    test_mlrt10_defines_rejection_gate_groups()
    test_mlrt10_preserves_forbidden_boundaries()
    test_mlrt10_positive_label_is_planning_only()
    test_mlrt10_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt10_does_not_create_forbidden_implementation_paths()
    test_box_manifest_records_mlrt10_boundary()
    print(
        "CONTRACT_TEST_OK: MLRT-10 Candidate Non-Runtime Dry-Run Output Capture Rejection Gate Plan v1, "
        "immutable governed documentation-only output-capture rejection gate planning after MLRT-9 freeze with FREEZE_MEMORY_STATUS OK, "
        "defines future non-authoritative dry-run output-capture rejection gate groups for identity, mandatory rejection families, "
        "critical-boundary blockers, rejection outcome labels, human-review escalation, no silent coercion, no-live-read doctrine, "
        "no mutation doctrine, non-authority doctrine, forbidden authority fields, and next-milestone doctrine only, "
        "candidate reliability not validated, ML implementation not unlocked, no executable validators, no schema code, "
        "no candidate package created, no candidate package accepted, no candidate package installed, no candidate package imported, "
        "no candidate implementation, no candidate execution, no candidate outputs created, no package intake records created, "
        "no static review performed, no static review records created, no static review evidence records created, no evidence envelopes created, "
        "no static review outcome records created, no outcome gate records created, no dry-run readiness review performed, "
        "no dry-run readiness records created, no dry-run protocol records created, no dry-run protocol execution records created, "
        "no dry-run input records created, no dry-run input manifests created, no dry-run output records created, "
        "no dry-run output manifests created, no output capture envelopes created, no output capture rejection records created, "
        "no output rejection gate records created, no output rejection gate run, no dry run executed, no dry-run outputs created, "
        "no case execution, no case scoring, no route comparison, no route authority, no prompt loading, no live prompt-library reads, "
        "no live freeze-memory reads, no live router-canon reads, no runtime router imports, no corpus mutation, no fixture mutation, "
        "no router-canon mutation, no prompt-library mutation, no freeze-memory mutation, no gold-registry mutation, "
        "no report generation, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, "
        "no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, "
        "critical boundary error budget zero, candidate output-capture rejection gate remains non-authoritative, "
        "next safe milestone is MLRT-11 Candidate Non-Runtime Dry-Run Output Capture Contract-Conformance Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_NON_RUNTIME_DRY_RUN_OUTPUT_CAPTURE_REJECTION_GATE_PLAN_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
