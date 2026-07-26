"""Contract tests for LAB-0C ML LAB SLO / Critical Error Budget Declaration v1.

These tests validate a documentation-only SLO/critical error-budget milestone.
They must not import a LAB implementation module because LAB-0C is still not
allowed to create schema code, fixtures, corpus, runner, metrics engine,
candidate harness, live risk detectors, provider adapters, or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1"
SLO_DOC = LAB_BOX / "LAB_SLO_CRITICAL_ERROR_BUDGET.md"

REQUIRED_SLOS = tuple(f"SLO-{index:02d}" for index in range(1, 19))

CRITICAL_CATEGORIES = (
    "Route authority",
    "Prompt loading",
    "Runtime action",
    "Persistence",
    "Provider / network / embedding",
    "Canon / prompt / freeze / gold mutation",
    "Box leakage",
    "Fixture integrity",
    "Human review bypass",
    "Activation drift",
    "Match-before-disagree violation",
    "Missing mandatory context",
    "Stale context acceptance",
    "Training-data drift",
    "Batch / async / background drift",
    "Sensitive or protected information leakage",
    "Insecure downstream output",
    "LAB self-validation bypass",
)

FORBIDDEN_IMPLEMENTATION_TERMS = (
    "schema code",
    "fixtures",
    "corpus",
    "runner",
    "scoring engine",
    "metrics engine",
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

def test_lab0c_slo_document_exists() -> None:
    assert SLO_DOC.is_file()


def test_lab0c_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab0c_declares_zero_critical_boundary_error_budget() -> None:
    text = _read(SLO_DOC)
    assert FEATURE_ID in text
    assert "critical_boundary_error_budget = 0" in text
    assert "Hard gates are evaluated before soft scores" in text
    assert "Aggregate accuracy cannot compensate for a critical violation" in text
    assert "Soft metrics are meaningful only when critical failures are zero" in text
    for slo_id in REQUIRED_SLOS:
        assert slo_id in text, slo_id
    for category in CRITICAL_CATEGORIES:
        assert category in text, category


def test_lab0c_defines_critical_failure_and_lab_invalid_handling() -> None:
    text = _read(SLO_DOC)
    for phrase in (
        "LAB_RUN_STATUS = CRITICAL_FAIL",
        "CANDIDATE_RELIABILITY_CLAIM = BLOCKED",
        "ML_IMPLEMENTATION_CONTINUATION = BLOCKED",
        "LAB_RUN_STATUS = LAB_INVALID",
        "CANDIDATE_EVALUATION = BLOCKED",
        "RELIABILITY_CLAIM = BLOCKED",
        "Mark candidate run as critical fail",
        "Mark LAB run invalid and stop candidate evaluation",
    ):
        assert phrase in text, phrase


def test_lab0c_reliability_claim_gate_requires_lab_self_validation_and_zero_critical_failures() -> None:
    text = _read(SLO_DOC)
    for phrase in (
        "The LAB self-validation gate passes",
        "Fixture integrity checks pass",
        "Critical boundary failures equal zero",
        "Human review confirms the result",
        "Freeze memory records the validation evidence",
        "LAB/test fulfills its mission",
        "ML router prompt logic reliability is tested",
        "zero critical boundary violations are demonstrated",
        "only then continue ML logic implementation",
    ):
        assert phrase in text, phrase


def test_lab0c_denies_implementation_and_reliability_claims() -> None:
    text = _read(SLO_DOC)
    for term in FORBIDDEN_IMPLEMENTATION_TERMS:
        assert term in text, term
    assert "LAB-0C does not claim that SLOs are enforced automatically" in text
    assert "LAB-0C does not create a metrics engine" in text
    assert "LAB-0C does not create a runner" in text
    assert "LAB-0C does not evaluate a candidate" in text
    assert "LAB-0C does not prove that the LAB is reliable" in text
    assert "LAB-0C does not prove ML router prompt logic reliability" in text
    assert "LAB-0C does not authorize continuing ML implementation" in text


def test_lab0c_next_safe_milestone_is_lab1_shielding_manifest() -> None:
    text = "\n".join(
        _read(path)
        for path in (
            SLO_DOC,
            LAB_BOX / "README.md",
            LAB_BOX / "LAB_PHASE_BOUNDARY.md",
            LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "LAB-1" in text
    assert "Lab Box Boundary + Shielding Manifest" in text
    assert "later lab implementation only after documentation and shielding gates are frozen" in text
    assert "runtime authority" in text
    assert "Copilot behavior" in text


def test_box_manifest_registers_lab0c_as_documentation_only() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_slo_critical_error_budget_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_slo_critical_error_budget_documentation_only"] is True
    assert manifest["ml_lab_slo_critical_error_budget_contains_lab_python_modules"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_schema_code"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_fixtures"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_corpus"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_runner"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_metrics_engine"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_candidate_harness"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_live_risk_detectors"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_runtime_pilot"] is False
    assert manifest["ml_lab_slo_critical_error_budget_contains_copilot_behavior"] is False
    assert manifest["ml_lab_slo_critical_error_budget_critical_boundary_error_budget"] == 0
    assert manifest["ml_lab_slo_critical_error_budget_soft_scores_cannot_override_hard_gates"] is True
    assert manifest["ml_lab_slo_critical_error_budget_candidate_reliability_claim_blocked_until_zero_critical_failures"] is True
    assert manifest["ml_lab_slo_critical_error_budget_ml_implementation_blocked_until_lab_and_router_reliability_validated"] is True


def test_lab0c_preserves_prior_lab_documentation_gates() -> None:
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
            "LAB_SLO_CRITICAL_ERROR_BUDGET.md",
        )
    )
    assert "LAB-0 is documentation-only" in combined
    assert "LAB-0A adds a success criteria matrix only" in combined
    assert "LAB-0B adds a risk-control matrix only" in combined
    assert "Hard gates override soft scores" in combined
    assert "P12 frozen" in combined
    assert "RG-LAB-000" in combined
    assert "only then continue ML logic implementation" in combined or "only then continue ML implementation" in combined
