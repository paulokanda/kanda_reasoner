from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_52_LAB_RELIABILITY_TEST_AGAINST_FIXED_CASES.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt52_lab_reliability_fixed_cases_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-52 Lab Reliability Test Against Fixed Cases v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-53 Training Learning Governance Plan v1"
POS_LABEL = "RSS_MLRT52_LAB_RELIABILITY_FIXED_CASES_PASSED_NON_RUNTIME"
PREFIX = "rss_mlrt52_lab_reliability_fixed_cases"


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


def load_mlrt_stub():
    return load_module(SOURCE, "mlrt52_stub_under_fixed_case_test")


def load_lab_harness():
    return load_module(LAB_HARNESS, "mlrt52_lab_harness_under_fixed_case_test")


def load_self_validation_gate():
    return load_module(LAB_SELF_GATE, "mlrt52_lab_self_validation_gate_under_fixed_case_test")


def assert_envelope_has_no_runtime_effects(envelope) -> None:
    assert envelope.non_authoritative is True
    assert envelope.candidate_evaluation_executed is False
    assert envelope.candidate_evaluation_allowed_by_this_interface is False
    assert envelope.case_execution_performed is False
    assert envelope.case_scoring_performed is False
    assert envelope.route_comparison_performed is False
    assert envelope.route_authority_granted is False
    assert envelope.prompt_loading_performed is False
    assert envelope.provider_call_performed is False
    assert envelope.embedding_call_performed is False
    assert envelope.persistence_performed is False
    assert envelope.report_generated is False
    assert envelope.report_persisted is False
    assert envelope.activation_performed is False
    assert envelope.field_test_performed is False
    assert envelope.runtime_pilot_behavior_performed is False
    assert envelope.copilot_behavior_performed is False


def assert_self_validation_has_no_runtime_effects(result) -> None:
    assert result.candidate_evaluation_executed is False
    assert result.candidate_evaluation_allowed_by_this_gate is False
    assert result.route_authority_granted is False
    assert result.prompt_loading_performed is False
    assert result.provider_call_performed is False
    assert result.embedding_call_performed is False
    assert result.persistence_performed is False
    assert result.activation_performed is False
    assert result.field_test_performed is False
    assert result.runtime_pilot_behavior_performed is False
    assert result.copilot_behavior_performed is False


def fixed_safe_metadata_case(module):
    return module.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="mlrt52-fixed-safe-case",
        candidate_id="candidate-placeholder",
        candidate_version="0.0.0-non-runtime",
        candidate_output_reference="in-memory-fixed-safe-output-only",
        candidate_output_metadata={
            "output_kind": "non_authoritative_evaluation_record",
            "fixed_case_id": "case_01_safe_metadata_not_evaluated",
            "candidate_claim": "placeholder only",
        },
        test_case_reference="case_01_safe_metadata_not_evaluated",
        corpus_version="mlrt52-fixed-validation-cases-not-training-data",
        fixture_manifest_hash="2" * 64,
        self_validation_status="caller_supplied_pass_reference_only",
    )


def fixed_forbidden_authority_case(module):
    return module.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="mlrt52-fixed-forbidden-authority-case",
        candidate_id="candidate-placeholder",
        candidate_version="0.0.0-non-runtime",
        candidate_output_reference="in-memory-fixed-forbidden-output-only",
        candidate_output_metadata={
            "output_kind": "non_authoritative_evaluation_record",
            "fixed_case_id": "case_02_forbidden_authority_metadata_rejected",
            "route_decision": "FORBIDDEN_AUTHORITY_FIELD",
            "activate_copilot": True,
            "call_provider": True,
        },
        test_case_reference="case_02_forbidden_authority_metadata_rejected",
        corpus_version="mlrt52-fixed-validation-cases-not-training-data",
        fixture_manifest_hash="3" * 64,
        self_validation_status="caller_supplied_pass_reference_only",
    )


def fixed_self_validation_pass_case(gate_module):
    return gate_module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="case_03_self_validation_all_controls_true_pass",
        control_results=gate_module.build_all_controls_true(),
    )


def fixed_self_validation_fail_case(gate_module):
    controls = dict(gate_module.build_all_controls_true())
    controls["zero_critical_boundary_error_budget_enforced"] = False
    return gate_module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="case_04_self_validation_one_control_false_lab_invalid",
        control_results=controls,
    )


def test_mlrt52_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt52_documents_lab_reliability_fixed_cases_without_unlocking_candidate_reliability() -> None:
    text = read(DOC)
    required = [
        "first lab reliability test against fixed in-memory cases",
        "fixed_safe_metadata_case -> NOT_EVALUATED",
        "fixed_forbidden_authority_case -> HARNESS_INTERFACE_REJECTED",
        "fixed_self_validation_pass_case -> LAB_SELF_VALIDATION_PASS",
        "fixed_self_validation_fail_case -> LAB_INVALID",
        "not a candidate reliability claim",
        "does **not** execute a candidate",
        "does **not** execute a dry run",
        "does **not** score candidate quality",
        "does **not** start Item 5 governance",
        "The critical boundary error budget remains `0`",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt52_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt52_stub_boundary_still_inert() -> None:
    module = load_mlrt_stub()
    assert module.assert_static_non_runtime_boundary() is True
    contract = module.get_stub_contract()
    assert contract["critical_boundary_error_budget"] == 0
    forbidden_flags = [
        "runtime_route_authority_enabled",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "batch_mode_enabled",
        "activation_enabled",
        "field_testing_enabled",
        "dry_run_execution_enabled",
        "candidate_execution_enabled",
        "case_scoring_enabled",
        "report_generation_enabled",
        "reliability_claim_enabled",
        "training_data_use_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in forbidden_flags:
        assert contract[flag] is False


def test_mlrt52_fixed_candidate_harness_cases_are_deterministic_and_non_authoritative() -> None:
    module = load_lab_harness()
    before = file_snapshot()
    safe_one = fixed_safe_metadata_case(module)
    safe_two = fixed_safe_metadata_case(module)
    rejected_one = fixed_forbidden_authority_case(module)
    rejected_two = fixed_forbidden_authority_case(module)
    after = file_snapshot()
    assert before == after

    assert safe_one == safe_two
    assert rejected_one == rejected_two
    assert safe_one.outcome == module.OUTCOME_NOT_EVALUATED
    assert safe_one.forbidden_authority_fields_present == ()
    assert rejected_one.outcome == module.OUTCOME_INTERFACE_REJECTED
    assert rejected_one.forbidden_authority_fields_present == ("route_decision", "activate_copilot", "call_provider")
    assert_envelope_has_no_runtime_effects(safe_one)
    assert_envelope_has_no_runtime_effects(rejected_one)


def test_mlrt52_fixed_self_validation_cases_are_deterministic_and_non_authoritative() -> None:
    gate = load_self_validation_gate()
    before = file_snapshot()
    pass_one = fixed_self_validation_pass_case(gate)
    pass_two = fixed_self_validation_pass_case(gate)
    fail_one = fixed_self_validation_fail_case(gate)
    fail_two = fixed_self_validation_fail_case(gate)
    after = file_snapshot()
    assert before == after

    assert pass_one == pass_two
    assert fail_one == fail_two
    assert pass_one.outcome == gate.OUTCOME_PASS
    assert pass_one.gate_passed is True
    assert fail_one.outcome == gate.OUTCOME_LAB_INVALID
    assert fail_one.gate_passed is False
    assert fail_one.false_controls == ("zero_critical_boundary_error_budget_enforced",)
    assert_self_validation_has_no_runtime_effects(pass_one)
    assert_self_validation_has_no_runtime_effects(fail_one)


def test_mlrt52_does_not_start_training_item5_or_runtime_authority() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "candidate execution is enabled",
        "dry run is executed",
        "case scoring is enabled",
        "route authority is granted",
        "Item 5 has started",
        "training is started",
        "candidate reliability is validated",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not claim validated candidate reliability",
        "not a candidate reliability claim",
        "does **not** execute a candidate",
        "does **not** execute a dry run",
        "does **not** start Item 5 governance",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt52_manifest_records_lab_reliability_without_unlocking_runtime_or_item5() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_SELF_GATE_REL,
        "lab_reliability_fixed_cases_test",
        "fixed_case_matrix_executed",
        "candidate_reliability_validated",
        "dry_run_executed",
        "candidate_executed",
        "item5_training_governance_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_fixed_case_matrix_executed": true' in manifest
    assert f'"{PREFIX}_lab_reliability_fixed_cases_test": true' in manifest
    assert f'"{PREFIX}_candidate_reliability_validated": false' in manifest
    assert f'"{PREFIX}_dry_run_executed": false' in manifest
    assert f'"{PREFIX}_candidate_executed": false' in manifest
    assert f'"{PREFIX}_case_scoring_started": false' in manifest
    assert f'"{PREFIX}_route_authority_granted": false' in manifest
    assert f'"{PREFIX}_item5_training_governance_started": false' in manifest


def test_mlrt52_readme_references_lab_reliability_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert LAB_HARNESS_REL in readme
    assert LAB_SELF_GATE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "fixed in-memory case matrix" in readme
    assert "Item 5 remains blocked until MLRT-52 freezes" in readme


if __name__ == "__main__":
    test_mlrt52_files_exist()
    test_mlrt52_documents_lab_reliability_fixed_cases_without_unlocking_candidate_reliability()
    test_mlrt52_only_allowed_python_surfaces_exist()
    test_mlrt52_stub_boundary_still_inert()
    test_mlrt52_fixed_candidate_harness_cases_are_deterministic_and_non_authoritative()
    test_mlrt52_fixed_self_validation_cases_are_deterministic_and_non_authoritative()
    test_mlrt52_does_not_start_training_item5_or_runtime_authority()
    test_mlrt52_manifest_records_lab_reliability_without_unlocking_runtime_or_item5()
    test_mlrt52_readme_references_lab_reliability_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-52 Lab Reliability Test Against Fixed Cases v1, "
        "tested fixed in-memory LAB cases for deterministic NOT_EVALUATED, HARNESS_INTERFACE_REJECTED, "
        "LAB_SELF_VALIDATION_PASS, and LAB_INVALID outcomes; no source modification, no dry run, "
        "no candidate execution, no case execution, no candidate scoring, no route comparison, no report generation, "
        "no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no training-data use, "
        "no Item 5 start, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT52_LAB_RELIABILITY_FIXED_CASES_V1_VALIDATION_OK")
