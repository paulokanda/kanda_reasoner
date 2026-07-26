"""Contract tests for LAB-1 ML LAB Box Boundary + Shielding Manifest v1.

These tests validate a documentation-only boundary/shielding milestone.
They must not import LAB implementation code because LAB-1 is not allowed to
create schema code, fixtures, corpus, runner, scoring engine, candidate harness,
live risk detectors, import scanners, write guards, provider adapters, or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1"
SHIELD_DOC = LAB_BOX / "LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md"

FORBIDDEN_IMPORT_TERMS = (
    "runtime router modules",
    "prompt loading modules",
    "prompt-library active prompt readers",
    "provider/model API modules",
    "embedding or vector-store modules",
    "PySide6, Qt, or UI controller modules",
    "freeze-memory writer modules",
    "gold-registry mutation modules",
    "activation-gate modules",
    "field-test modules",
    "runtime Pilot modules",
    "Copilot modules",
    "background, async, scheduler, or batch execution modules",
)

FORBIDDEN_WRITE_TERMS = (
    "prompt library",
    "router canon",
    "freeze memory",
    "gold registry",
    "routing registry",
    "project source outside the LAB box",
    "startup routing pack",
    "activation state",
    "human review approval state",
    "runtime decision logs",
    "persistent ML decision storage",
)

NON_CLAIMS = (
    "LAB-1 does not enforce the shield automatically",
    "LAB-1 does not create import guards",
    "LAB-1 does not create write guards",
    "LAB-1 does not create fixture snapshots",
    "LAB-1 does not create a runner",
    "LAB-1 does not evaluate a candidate",
    "LAB-1 does not prove the LAB is reliable",
    "LAB-1 does not prove ML router prompt logic reliability",
    "LAB-1 does not authorize continuing ML implementation",
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

def test_lab1_shielding_manifest_exists() -> None:
    assert SHIELD_DOC.is_file()


def test_lab1_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab1_declares_primary_box_and_public_surface_only() -> None:
    text = _read(SHIELD_DOC)
    assert FEATURE_ID in text
    assert "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation" in text
    assert "LAB-1 is documentation/governance only" in text
    assert "LAB-1 exposes only Markdown documentation" in text
    assert "no Python package" in text
    assert "no callable API" in text
    assert "no importable LAB module" in text
    assert "no route evaluator" in text
    assert "no prompt selector" in text
    assert "no candidate runner" in text
    assert "no activation flag" in text
    assert "no persistent state writer" in text


def test_lab1_declares_forbidden_identity_drift() -> None:
    text = _read(SHIELD_DOC)
    for phrase in (
        "a runtime router",
        "a prompt loader",
        "a prompt-library reader",
        "a freeze-memory writer",
        "a gold-registry writer",
        "a provider adapter",
        "an embedding/vector adapter",
        "a UI controller",
        "an activation gate",
        "a field-test mode",
        "a runtime Pilot",
        "a Copilot",
    ):
        assert phrase in text, phrase


def test_lab1_declares_one_way_dependency_rule_and_static_fixture_read_model() -> None:
    text = _read(SHIELD_DOC)
    for phrase in (
        "Production/runtime code must not import the LAB box",
        "static, copied, versioned fixtures",
        "frozen canon reference → copied fixture snapshot → fixture hash manifest → deterministic evaluator",
        "live prompt library → evaluator",
        "live freeze memory → evaluator",
        "live router canon → evaluator",
        "runtime router object → evaluator",
        "must not reach into live protected boxes during evaluation",
    ):
        assert phrase in text, phrase


def test_lab1_declares_forbidden_imports_and_forbidden_writes() -> None:
    text = _read(SHIELD_DOC)
    for term in FORBIDDEN_IMPORT_TERMS:
        assert term in text, term
    for term in FORBIDDEN_WRITE_TERMS:
        assert term in text, term
    assert "LAB-1 creates no code that performs this enforcement" in text
    assert "Any future write target must be explicitly authorized by a later governed milestone" in text


def test_lab1_candidate_output_is_non_authoritative() -> None:
    text = _read(SHIELD_DOC)
    for phrase in (
        "non-authoritative evaluation record",
        "a route decision",
        "a prompt loading instruction",
        "an install command",
        "a freeze write",
        "a human approval",
        "a readiness approval",
        "an activation signal",
        "a field-test signal",
        "a runtime Pilot command",
        "a Copilot instruction",
    ):
        assert phrase in text, phrase


def test_lab1_preserves_fixture_human_review_and_reliability_shielding() -> None:
    text = _read(SHIELD_DOC)
    for phrase in (
        "Fixtures must not be confused with active prompt canon",
        "Human review remains outside candidate authority",
        "The LAB self-validation gate passes",
        "Fixture integrity passes",
        "Critical boundary failures equal zero",
        "Human review confirms the result",
        "Freeze memory records the validation evidence",
        "critical_boundary_error_budget = 0",
    ):
        assert phrase in text, phrase


def test_lab1_non_claims_and_ml_implementation_lock_are_explicit() -> None:
    text = _read(SHIELD_DOC)
    for phrase in NON_CLAIMS:
        assert phrase in text, phrase
    for phrase in (
        "LAB/test fulfills its mission",
        "LAB self-validation passes",
        "ML router prompt logic reliability is tested",
        "zero critical boundary violations are demonstrated",
        "only then continue ML logic implementation",
    ):
        assert phrase in text, phrase


def test_lab1_next_safe_milestone_is_failure_taxonomy() -> None:
    combined = "\n".join(
        _read(path)
        for path in (
            SHIELD_DOC,
            LAB_BOX / "README.md",
            LAB_BOX / "LAB_PHASE_BOUNDARY.md",
            LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "LAB-2" in combined
    assert "Failure Taxonomy + Critical Violation Model" in combined
    assert "later lab implementation only after documentation, shielding, taxonomy, scoring, and schema gates are frozen" in combined


def test_box_manifest_registers_lab1_as_documentation_only_and_shielded() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_box_boundary_shielding_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_box_boundary_shielding_documentation_only"] is True
    assert manifest["ml_lab_box_boundary_shielding_contains_lab_python_modules"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_schema_code"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_fixtures"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_corpus"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_runner"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_scoring_engine"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_metrics_engine"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_candidate_harness"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_live_risk_detectors"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_import_scanner"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_write_guard"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_runtime_pilot"] is False
    assert manifest["ml_lab_box_boundary_shielding_contains_copilot_behavior"] is False
    assert manifest["ml_lab_box_boundary_shielding_production_imports_lab_allowed"] is False
    assert manifest["ml_lab_box_boundary_shielding_lab_imports_runtime_router_allowed"] is False
    assert manifest["ml_lab_box_boundary_shielding_lab_imports_prompt_loader_allowed"] is False
    assert manifest["ml_lab_box_boundary_shielding_lab_imports_provider_or_embedding_allowed"] is False
    assert manifest["ml_lab_box_boundary_shielding_lab_writes_outside_lab_allowed"] is False
    assert manifest["ml_lab_box_boundary_shielding_candidate_output_authoritative_allowed"] is False
    assert manifest["ml_lab_box_boundary_shielding_critical_boundary_error_budget"] == 0
    assert manifest["ml_lab_box_boundary_shielding_ml_implementation_blocked_until_lab_and_router_reliability_validated"] is True


def test_lab1_preserves_prior_lab_documentation_gates() -> None:
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
            "LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md",
        )
    )
    assert "LAB-0 is documentation-only" in combined
    assert "LAB-0A adds a success criteria matrix only" in combined
    assert "LAB-0B adds a risk-control matrix only" in combined
    assert "LAB-0C adds a LAB SLO / Critical Error Budget Declaration only" in combined
    assert "critical_boundary_error_budget = 0" in combined
    assert "RG-LAB-000" in combined
    assert "only then continue ML logic implementation" in combined or "only then continue ML implementation" in combined
