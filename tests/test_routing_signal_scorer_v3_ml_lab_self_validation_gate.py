"""Contract tests for LAB-7 Self-Validation Gate v1."""

from __future__ import annotations

from dataclasses import is_dataclass
import ast
import importlib.util
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MODULE_PATH = LAB_BOX / "lab_self_validation_gate.py"
CONTRACT_DOC = LAB_BOX / "LAB_SELF_VALIDATION_GATE.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_self_validation_gate_v1"
ALLOWED_LAB_PYTHON_FILES = [
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_module():
    spec = importlib.util.spec_from_file_location("lab7_self_validation_gate", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_lab7_files_exist_and_lab_python_surface_is_exactly_allowed() -> None:
    assert MODULE_PATH.is_file()
    assert CONTRACT_DOC.is_file()
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    assert python_files == ALLOWED_LAB_PYTHON_FILES


def test_lab7_doc_declares_self_validation_gate_scope() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    for phrase in (
        "governed non-runtime self-validation gate",
        "validates the LAB itself before any future candidate evaluation",
        "does not evaluate candidates",
        "does not create corpus cases",
        "LAB_SELF_VALIDATION_PASS",
        "LAB_INVALID",
        "LAB-8 — Alpha Corpus Seed",
    ):
        assert phrase in text, phrase


def test_lab7_module_imports_only_safe_standard_library_modules() -> None:
    tree = ast.parse(_read(MODULE_PATH))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    assert imports <= {"__future__", "dataclasses", "types", "typing"}
    forbidden = {
        "os", "sys", "pathlib", "subprocess", "socket", "requests", "urllib", "asyncio",
        "kanda_prompt_workspace", "project_freeze_ledger", "project_freeze_after_update", "PySide6",
    }
    assert imports.isdisjoint(forbidden)


def test_lab7_contract_record_is_immutable_non_runtime_and_zero_authority() -> None:
    module = _load_module()
    record = module.get_lab7_self_validation_gate_record()
    assert is_dataclass(record)
    assert record.feature_id == FEATURE_ID
    assert record.schema_version == "lab-7-self-validation-gate"
    assert record.design_kind == "non_runtime_in_memory_self_validation_gate_only"
    assert record.storage_status == "in_memory_only"
    assert record.routing_effect == "none"
    assert record.prompt_loading_effect == "none"
    assert record.runtime_effect == "none"
    assert record.activation_effect == "none"
    assert record.critical_boundary_error_budget == 0
    assert record.next_safe_milestone == "LAB-8 Alpha Corpus Seed"
    assert "evaluate_candidate_output" in record.forbidden_operations
    assert "route_decision" in record.forbidden_authority_fields
    try:
        record.feature_id = "mutated"  # type: ignore[misc]
        raise AssertionError("record should be frozen")
    except Exception as exc:
        assert exc.__class__.__name__ == "FrozenInstanceError"


def test_lab7_required_controls_are_complete_and_specific() -> None:
    module = _load_module()
    controls = module.REQUIRED_SELF_VALIDATION_CONTROLS
    assert len(controls) == 11
    for name in (
        "gold_vs_gold_control_passed",
        "wrong_route_control_failed_as_expected",
        "missing_prompt_control_failed_as_expected",
        "forbidden_action_control_critical_failed_as_expected",
        "fixture_hash_mismatch_control_lab_invalid_as_expected",
        "skipped_match_before_disagree_control_critical_failed_as_expected",
        "zero_critical_boundary_error_budget_enforced",
        "lab6_runner_outputs_not_evaluated_only",
        "no_live_project_reads_confirmed",
        "no_authority_fields_confirmed",
        "candidate_evaluation_blocked_until_self_validation_passed",
    ):
        assert name in controls


def test_lab7_gate_passes_only_when_all_controls_are_true() -> None:
    module = _load_module()
    result = module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="lab7-self-check-001",
        control_results={name: True for name in module.REQUIRED_SELF_VALIDATION_CONTROLS},
    )
    assert result.outcome == "LAB_SELF_VALIDATION_PASS"
    assert result.gate_passed is True
    assert result.missing_controls == ()
    assert result.false_controls == ()
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
    assert result.next_safe_milestone == "LAB-8 Alpha Corpus Seed"


def test_lab7_gate_is_lab_invalid_when_controls_are_missing_or_false() -> None:
    module = _load_module()
    partial = {name: True for name in module.REQUIRED_SELF_VALIDATION_CONTROLS[:-1]}
    missing_result = module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="lab7-self-check-missing",
        control_results=partial,
    )
    assert missing_result.outcome == "LAB_INVALID"
    assert missing_result.gate_passed is False
    assert missing_result.missing_controls == ("candidate_evaluation_blocked_until_self_validation_passed",)
    false_controls = {name: True for name in module.REQUIRED_SELF_VALIDATION_CONTROLS}
    false_controls["wrong_route_control_failed_as_expected"] = False
    false_result = module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="lab7-self-check-false",
        control_results=false_controls,
    )
    assert false_result.outcome == "LAB_INVALID"
    assert false_result.gate_passed is False
    assert false_result.false_controls == ("wrong_route_control_failed_as_expected",)
    assert false_result.candidate_evaluation_executed is False
    assert false_result.route_authority_granted is False


def test_lab7_read_only_helpers_are_in_memory_and_immutable() -> None:
    module = _load_module()
    controls = module.build_all_controls_true()
    assert all(controls[name] is True for name in module.REQUIRED_SELF_VALIDATION_CONTROLS)
    try:
        controls["gold_vs_gold_control_passed"] = False  # type: ignore[index]
        raise AssertionError("controls mapping should be read-only")
    except TypeError:
        pass
    result = module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="lab7-self-check-readonly",
        control_results=controls,
    )
    mapping = module.as_read_only_mapping(result)
    assert mapping["outcome"] == "LAB_SELF_VALIDATION_PASS"
    try:
        mapping["outcome"] = "mutated"  # type: ignore[index]
        raise AssertionError("mapping should be read-only")
    except TypeError:
        pass


def test_lab7_no_forbidden_authority_fields_are_exposed_by_result() -> None:
    module = _load_module()
    result = module.evaluate_lab_self_validation_gate(
        lab_self_validation_id="lab7-self-check-authority",
        control_results=module.build_all_controls_true(),
    )
    keys = set(result.__dict__)
    assert keys.isdisjoint(set(module.FORBIDDEN_AUTHORITY_FIELDS))


def test_lab7_manifest_metadata_declares_non_runtime_self_validation_boundary() -> None:
    data = json.loads(_read(MANIFEST))
    assert data["ml_lab_self_validation_gate_feature_id"] == FEATURE_ID
    assert data["ml_lab_self_validation_gate_schema_version"] == "lab-7-self-validation-gate"
    assert data["ml_lab_self_validation_gate_status"] == "non_runtime_in_memory_self_validation_gate_only"
    assert data["ml_lab_self_validation_gate_contains_lab_python_modules"] is True
    assert data["ml_lab_self_validation_gate_allowed_python_modules"] == ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py", "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"]
    assert data["ml_lab_self_validation_gate_contains_candidate_evaluation"] is False
    assert data["ml_lab_self_validation_gate_contains_route_comparison"] is False
    assert data["ml_lab_self_validation_gate_contains_route_authority"] is False
    assert data["ml_lab_self_validation_gate_contains_actual_fixtures"] is False
    assert data["ml_lab_self_validation_gate_contains_hash_manifest_data"] is False
    assert data["ml_lab_self_validation_gate_contains_corpus"] is False
    assert data["ml_lab_self_validation_gate_contains_executable_scoring_engine"] is False
    assert data["ml_lab_self_validation_gate_contains_candidate_harness"] is False
    assert data["ml_lab_self_validation_gate_contains_live_prompt_library_reads"] is False
    assert data["ml_lab_self_validation_gate_contains_live_freeze_memory_reads"] is False
    assert data["ml_lab_self_validation_gate_contains_live_router_canon_reads"] is False
    assert data["ml_lab_self_validation_gate_contains_runtime_router_imports"] is False
    assert data["ml_lab_self_validation_gate_contains_prompt_loading"] is False
    assert data["ml_lab_self_validation_gate_contains_persistence"] is False
    assert data["ml_lab_self_validation_gate_contains_provider_calls"] is False
    assert data["ml_lab_self_validation_gate_contains_embeddings"] is False
    assert data["ml_lab_self_validation_gate_contains_network_calls"] is False
    assert data["ml_lab_self_validation_gate_contains_subprocess_calls"] is False
    assert data["ml_lab_self_validation_gate_contains_batch_mode"] is False
    assert data["ml_lab_self_validation_gate_contains_activation_key"] is False
    assert data["ml_lab_self_validation_gate_contains_field_test_mode"] is False
    assert data["ml_lab_self_validation_gate_contains_runtime_pilot"] is False
    assert data["ml_lab_self_validation_gate_contains_copilot_behavior"] is False
    assert data["ml_lab_self_validation_gate_storage_status"] == "in_memory_only"
    assert data["ml_lab_self_validation_gate_candidate_evaluation_executed"] is False
    assert data["ml_lab_self_validation_gate_candidate_evaluation_allowed_by_this_gate"] is False
    assert data["ml_lab_self_validation_gate_critical_boundary_error_budget"] == 0
    assert "LAB-8 Alpha Corpus Seed" in data["ml_lab_self_validation_gate_next_safe_milestone"]


if __name__ == "__main__":
    test_lab7_files_exist_and_lab_python_surface_is_exactly_allowed()
    test_lab7_doc_declares_self_validation_gate_scope()
    test_lab7_module_imports_only_safe_standard_library_modules()
    test_lab7_contract_record_is_immutable_non_runtime_and_zero_authority()
    test_lab7_required_controls_are_complete_and_specific()
    test_lab7_gate_passes_only_when_all_controls_are_true()
    test_lab7_gate_is_lab_invalid_when_controls_are_missing_or_false()
    test_lab7_read_only_helpers_are_in_memory_and_immutable()
    test_lab7_no_forbidden_authority_fields_are_exposed_by_result()
    test_lab7_manifest_metadata_declares_non_runtime_self_validation_boundary()
    print(
        "CONTRACT_TEST_OK: LAB-7 ML LAB Self-Validation Gate v1, "
        "immutable governed non-runtime in-memory self-validation gate after LAB-6 freeze with FREEZE_MEMORY_STATUS OK, "
        "validates caller-supplied LAB control facts before future candidate evaluation, requires gold-vs-gold pass, wrong-route negative control, "
        "missing-prompt negative control, forbidden-action critical control, fixture-hash mismatch LAB_INVALID control, skipped match-before-disagree critical control, "
        "zero critical boundary budget enforcement, LAB-6 NOT_EVALUATED behavior, no live project reads, no authority fields, and candidate evaluation blocked until self-validation, "
        "returns LAB_SELF_VALIDATION_PASS or LAB_INVALID only, candidate evaluation remains not executed and not allowed by this gate, no route comparison, no route authority, "
        "no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixtures, "
        "no hash manifest data files, no corpus, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, "
        "no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, "
        "zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-8 Alpha Corpus Seed next"
    )
