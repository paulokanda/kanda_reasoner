"""Contract tests for LAB-0B ML LAB Risk-Control Matrix v1.

These tests validate a documentation-only risk-control milestone. They must
not import a LAB implementation module because LAB-0B is still not allowed to
create schema code, fixtures, corpus, runner, metrics engine, candidate harness,
live risk detectors, provider adapters, or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1"
RISK_DOC = LAB_BOX / "LAB_RISK_CONTROL_MATRIX.md"

REQUIRED_RISKS = tuple(f"RC-{index:02d}" for index in range(1, 21))

REQUIRED_RISK_FAMILIES = (
    "Prompt injection / bypass",
    "Insecure output to downstream",
    "Route authority overreach",
    "Prompt loading overreach",
    "Persistence overreach",
    "Provider / embedding overreach",
    "Box leakage",
    "Fixture contamination",
    "Live canon coupling",
    "Stale context acceptance",
    "Missing-context failure",
    "False confidence / metric gaming",
    "Match-before-disagree violation",
    "Human review bypass",
    "Activation drift",
    "Training-data drift",
    "Batch / async drift",
    "Sensitive information leakage",
    "Supply-chain / dependency drift",
    "LAB self-validation failure",
)

FORBIDDEN_IMPLEMENTATION_TERMS = (
    "schema code",
    "fixtures",
    "corpus",
    "runner",
    "scoring engine",
    "candidate harness",
    "live risk detectors",
    "prompt loaders",
    "persistence",
    "provider adapters",
    "activation",
    "field testing",
    "runtime Pilot",
    "Copilot behavior",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_lab_python_files_are_allowed_for_current_milestone() -> None:
    """Allow only governed LAB Python files introduced up to LAB-7."""
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    allowed_after_lab6 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"]
    allowed_after_lab7 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py", "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"]
    allowed_after_lab10 = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
    assert python_files in ([], allowed_after_lab6, allowed_after_lab7, allowed_after_lab10)

def test_lab0b_risk_control_document_exists() -> None:
    assert RISK_DOC.is_file()


def test_lab0b_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab0b_defines_required_risk_control_matrix() -> None:
    text = _read(RISK_DOC)
    assert FEATURE_ID in text
    assert "Risk-control matrix" in text
    assert "Critical boundary risks have zero acceptable failures" in text
    for risk_id in REQUIRED_RISKS:
        assert risk_id in text, risk_id
    for family in REQUIRED_RISK_FAMILIES:
        assert family in text, family


def test_lab0b_controls_include_forbidden_authority_and_box_leakage() -> None:
    text = _read(RISK_DOC)
    for phrase in (
        "Candidate output remains non-authoritative",
        "Canon and router governance remain authoritative",
        "Candidate becomes route authority",
        "Prompt loading attempt or prompt-library read attempt",
        "Unauthorized write or persistent decision storage",
        "Provider call, network call, embedding/vector-store use",
        "LAB-production coupling or forbidden import",
        "Fixture hash mismatch or mutable expected output",
        "Candidate advances milestone using stale evidence",
        "Any critical failure is marked acceptable because score is high",
        "Candidate skips canon match or overrides canon",
        "Any activation or field-test artifact appears",
        "Candidate evaluation runs before self-validation",
    ):
        assert phrase in text, phrase


def test_lab0b_denies_implementation_and_reliability_claims() -> None:
    text = _read(RISK_DOC)
    for term in FORBIDDEN_IMPLEMENTATION_TERMS:
        assert term in text, term
    assert "LAB-0B does not claim that any control is implemented" in text
    assert "LAB-0B does not claim that risks are detected automatically" in text
    assert "LAB-0B does not claim that the LAB is reliable" in text
    assert "LAB-0B does not claim that ML router prompt logic reliability has been tested" in text
    assert "LAB-0B does not authorize continuing ML implementation" in text


def test_lab0b_next_safe_milestone_is_lab0c_slo_only() -> None:
    text = "\n".join(
        _read(path)
        for path in (
            RISK_DOC,
            LAB_BOX / "README.md",
            LAB_BOX / "LAB_PHASE_BOUNDARY.md",
            LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "LAB-0C" in text
    assert "LAB SLO / Critical Error Budget Declaration" in text
    assert "documentation/governance only" in text
    assert "LAB SLO / Critical Error Budget Declaration documentation only" in text


def test_box_manifest_registers_lab0b_as_documentation_only() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_risk_control_matrix_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_risk_control_matrix_documentation_only"] is True
    assert manifest["ml_lab_risk_control_matrix_contains_lab_python_modules"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_schema_code"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_fixtures"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_corpus"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_runner"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_metrics_engine"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_candidate_harness"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_live_risk_detectors"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_runtime_pilot"] is False
    assert manifest["ml_lab_risk_control_matrix_contains_copilot_behavior"] is False
    assert manifest["ml_lab_risk_control_matrix_critical_boundary_error_budget"] == "zero"
    assert manifest["ml_lab_risk_control_matrix_hard_controls_override_soft_performance"] is True


def test_lab0b_preserves_lab0_and_lab0a_boundaries() -> None:
    combined = "\n".join(
        _read(LAB_BOX / name)
        for name in (
            "README.md",
            "LAB_PHASE_BOUNDARY.md",
            "LAB_CHARTER.md",
            "LAB_FORBIDDEN_BEHAVIORS.md",
            "LAB_STOP_CONDITIONS.md",
            "LAB_ALLOWED_ARTIFACTS.md",
            "LAB_SUCCESS_CRITERIA_MATRIX.md",
            "LAB_RISK_CONTROL_MATRIX.md",
        )
    )
    assert "LAB-0 is documentation-only" in combined
    assert "LAB-0A adds a success criteria matrix only" in combined
    assert "Hard gates override soft scores" in combined
    assert "P12 frozen" in combined
    assert "RG-LAB-000" in combined
    assert "only then continue ML logic implementation" in combined or "only then continue ML implementation" in combined
