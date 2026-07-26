"""Contract tests for LAB-0 ML LAB Phase Boundary / Charter Entry Gate v1.

These tests intentionally validate documentation-only behavior. They must not
import a LAB implementation module because LAB-0 is not allowed to create one.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1"

REQUIRED_DOCS = (
    "README.md",
    "LAB_PHASE_BOUNDARY.md",
    "LAB_CHARTER.md",
    "LAB_FORBIDDEN_BEHAVIORS.md",
    "LAB_STOP_CONDITIONS.md",
    "LAB_ALLOWED_ARTIFACTS.md",
)

FORBIDDEN_TERMS_THAT_MUST_BE_DENIED = (
    "schema code",
    "fixture",
    "corpus",
    "runner",
    "candidate harness",
    "prompt loading",
    "persistence",
    "provider calls",
    "embeddings",
    "batch mode",
    "activation key",
    "field-test",
    "runtime Pilot",
    "Copilot behavior",
)


def _doc_text(name: str) -> str:
    return (LAB_BOX / name).read_text(encoding="utf-8")



def _assert_lab_python_files_are_allowed_for_current_milestone() -> None:
    """Allow only governed LAB Python files introduced up to LAB-7."""
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    allowed_after_lab6 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"]
    allowed_after_lab7 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py", "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"]
    allowed_after_lab10 = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
    assert python_files in ([], allowed_after_lab6, allowed_after_lab7, allowed_after_lab10)

def test_lab0_documentation_files_exist() -> None:
    for name in REQUIRED_DOCS:
        assert (LAB_BOX / name).is_file(), name


def test_lab0_box_contains_no_python_implementation_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab0_charter_preserves_required_flow_before_ml_implementation() -> None:
    combined = "\n".join(_doc_text(name) for name in REQUIRED_DOCS)
    assert "P12 frozen" in combined
    assert "RG-LAB-000" in combined
    assert "LAB-0" in combined
    assert "LAB/test reliability" in combined
    assert "ML router prompt logic reliability" in combined
    assert "only then continue ML logic implementation" in combined or "only then continue ML implementation" in combined


def test_lab0_denies_runtime_and_lab_implementation_behaviors() -> None:
    combined = "\n".join(_doc_text(name) for name in REQUIRED_DOCS)
    for term in FORBIDDEN_TERMS_THAT_MUST_BE_DENIED:
        assert term in combined, term
    assert "LAB-0 is documentation-only" in combined
    assert "Critical boundary error budget: zero" in combined


def test_lab0_next_safe_milestone_is_success_criteria_matrix_only() -> None:
    readme = _doc_text("README.md")
    boundary = _doc_text("LAB_PHASE_BOUNDARY.md")
    allowed = _doc_text("LAB_ALLOWED_ARTIFACTS.md")
    combined = "\n".join((readme, boundary, allowed))
    assert "LAB-0A" in combined
    assert "Success Criteria Matrix" in combined
    assert "No later step may be skipped" in combined
    assert "success-criteria documentation only" in combined


def test_box_manifest_registers_lab0_as_documentation_only() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_lab0_documentation_only"] is True
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_lab_python_modules"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_schema_code"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_fixtures"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_corpus"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_runner"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_candidate_harness"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_runtime_pilot"] is False
    assert manifest["ml_lab_phase_boundary_charter_entry_gate_contains_copilot_behavior"] is False


def test_rg_lab_000_router_canon_file_is_present_as_precondition_reference() -> None:
    rg_lab_canon = (
        PROJECT_ROOT
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / "02_prompt_routing_and_indexing"
        / "routing_signal_scorer_v3_lab_phase_entry_router_canon.md"
    )
    text = rg_lab_canon.read_text(encoding="utf-8")
    assert "RG-LAB-000" in text
    assert "LAB-0" in text
    assert "documentation-only" in text
