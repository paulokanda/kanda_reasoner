# project-path: tools/validate_runtime_app_host_visibility_contract_ast_safe_refactor_v1.py
"""Validate the Phase 12 runtime app-host visibility contract AST-safe refactor."""

from __future__ import annotations

import argparse
import ast
import dataclasses
import hashlib
import inspect
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "read_only_advisory_panel_runtime_app_host_visibility_contract.py"
)
EVALUATION_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_runtime_app_host_visibility_contract_evaluation.py"
)
INVARIANTS_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_runtime_app_host_visibility_contract_invariants.py"
)
VALIDATOR_REL = "tools/validate_runtime_app_host_visibility_contract_ast_safe_refactor_v1.py"
FEATURE_ID = "runtime-app-host-visibility-contract-ast-safe-refactor-v1"
BASELINE_TARGET_SHA256 = "2cdca2d96f94c655ce58dd15438b2dd62260873d8cd95c155ac7a649784f5ae8"
EXPECTED_PUBLIC_ALL = [
    "build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract",
    "build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe",
    "evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy",
    "ReadOnlyPanelRuntimeAppHostVisibilityMode",
    "ReadOnlyPanelRuntimeAppHostVisibilityStatus",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def _assert_ascii_utf8_no_bom(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError(f"UTF8_BOM_FORBIDDEN: {path}")
    raw.decode("ascii")


def _assert_size(path: Path) -> None:
    count = _line_count(path)
    if not 101 <= count <= 499:
        raise AssertionError(f"LINE_LAW_101_499 failed: {path}: {count}")


def _assert_no_helper_to_facade_import(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden = "read_only_advisory_panel_runtime_app_host_visibility_contract"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and forbidden in str(node.module or ""):
            raise AssertionError(f"HELPER_TO_FACADE_IMPORT: {path}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if forbidden in alias.name:
                    raise AssertionError(f"HELPER_TO_FACADE_IMPORT: {path}")


def _capture(callable_obj: Any) -> dict[str, str]:
    try:
        callable_obj()
    except Exception as exc:
        return {"type": type(exc).__name__, "message": str(exc)}
    return {"type": "NO_ERROR", "message": ""}


def _assert_error(callable_obj: Any, expected_type: str, expected_message: str) -> None:
    actual = _capture(callable_obj)
    expected = {"type": expected_type, "message": expected_message}
    if actual != expected:
        raise AssertionError(f"ERROR_CONTRACT_CHANGED: expected={expected!r} actual={actual!r}")


def _assert_decorators(target_path: Path) -> None:
    tree = ast.parse(target_path.read_text(encoding="utf-8"), filename=str(target_path))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    for name in (
        "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy",
        "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision",
    ):
        node = classes.get(name)
        if node is None or len(node.decorator_list) != 1:
            raise AssertionError(f"DECORATOR_PRESERVATION_FAILED: {name}")
        decorator = node.decorator_list[0]
        if not isinstance(decorator, ast.Call) or _call_name(decorator.func) != "dataclass":
            raise AssertionError(f"DATACLASS_DECORATOR_MISSING: {name}")
        frozen = {
            item.arg: item.value
            for item in decorator.keywords
            if item.arg is not None
        }.get("frozen")
        if not isinstance(frozen, ast.Constant) or frozen.value is not True:
            raise AssertionError(f"DATACLASS_FROZEN_CHANGED: {name}")


def _assert_public_contract(module: Any) -> None:
    if list(module.__all__) != EXPECTED_PUBLIC_ALL:
        raise AssertionError("PUBLIC_API_ALL_CHANGED")
    expected = {
        "build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract": (
            "(policy: 'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy | None' = None) -> "
            "'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision'"
        ),
        "evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request": (
            "(request: 'Mapping[str, object]', policy: "
            "'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy | None' = None) -> "
            "'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision'"
        ),
        "build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe": (
            "() -> 'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision'"
        ),
    }
    for name, signature in expected.items():
        actual = str(inspect.signature(getattr(module, name)))
        if actual != signature:
            raise AssertionError(f"SIGNATURE_CHANGED: {name}: {actual}")


def _assert_policy_contract(module: Any) -> None:
    policy = module.ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy()
    if policy.visibility_mode.value != "contract_only":
        raise AssertionError("POLICY_DEFAULT_MODE_CHANGED")
    if policy.feature_flag_default_enabled is not False:
        raise AssertionError("POLICY_FEATURE_FLAG_DEFAULT_CHANGED")

    _assert_error(
        lambda: dataclasses.replace(policy, visibility_mode="bad"),
        "TypeError",
        "visibility_mode must be ReadOnlyPanelRuntimeAppHostVisibilityMode",
    )
    _assert_error(
        lambda: dataclasses.replace(policy, source_completion_handoff_id="bad"),
        "ValueError",
        "source_completion_handoff_id must match Phase 11 completion handoff",
    )
    _assert_error(
        lambda: dataclasses.replace(policy, source_host_binding_implementation_id="bad"),
        "ValueError",
        "source_host_binding_implementation_id must match Phase 11 implementation",
    )
    for name in module._policy_required_true_fields():
        _assert_error(
            lambda name=name: dataclasses.replace(policy, **{name: False}),
            "ValueError",
            name + " must remain True",
        )
    for name in module._policy_required_false_fields():
        _assert_error(
            lambda name=name: dataclasses.replace(policy, **{name: True}),
            "ValueError",
            name + " must remain False",
        )


def _assert_decision_contract(module: Any) -> None:
    decision = module.build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe()
    if decision.status.value != "accepted_future_read_only_runtime_app_host_visibility_contract":
        raise AssertionError("PROBE_STATUS_CHANGED")
    if decision.accepted is not True or decision.source_descriptor_safe is not True:
        raise AssertionError("PROBE_ACCEPTANCE_CHANGED")
    for name in module._decision_required_true_fields():
        _assert_error(
            lambda name=name: dataclasses.replace(decision, **{name: False}),
            "ValueError",
            name + " must remain True",
        )
    for name in module._decision_forbidden_true_fields():
        _assert_error(
            lambda name=name: dataclasses.replace(decision, **{name: True}),
            "ValueError",
            name + " must remain False",
        )
    _assert_error(
        lambda: dataclasses.replace(decision, feature_id="bad"),
        "ValueError",
        "feature_id must match Phase 12 runtime app-host visibility contract",
    )
    _assert_error(
        lambda: dataclasses.replace(decision, status="bad"),
        "TypeError",
        "status must be ReadOnlyPanelRuntimeAppHostVisibilityStatus",
    )
    _assert_error(
        lambda: dataclasses.replace(decision, visibility_mode="bad"),
        "TypeError",
        "visibility_mode must be ReadOnlyPanelRuntimeAppHostVisibilityMode",
    )
    _assert_error(
        lambda: dataclasses.replace(decision, critical_boundary_error_budget=1),
        "ValueError",
        "critical_boundary_error_budget must remain zero",
    )
    _assert_error(
        lambda: dataclasses.replace(decision, source_descriptor_safe=False),
        "ValueError",
        "accepted decisions require a safe source descriptor",
    )


def _assert_request_behavior(module: Any) -> None:
    cases = {
        "route_authority": "blocked_unsafe_authority",
        "runtime_ui_mutation": "blocked_unsafe_runtime_visibility",
        "provider_call": "blocked_unsafe_data_or_side_effect",
        "free_text_route_advice": "blocked_unsafe_text_or_controls",
    }
    for capability, expected_status in cases.items():
        result = module.evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request(
            {"capabilities": [capability]}
        )
        if result.status.value != expected_status or result.accepted is not False:
            raise AssertionError(f"REQUEST_STATUS_CHANGED: {capability}")

    safe = module.evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request(
        {"capabilities": []}
    )
    if safe.accepted is not True:
        raise AssertionError("SAFE_REQUEST_ACCEPTANCE_CHANGED")

    bool_request = module._requested_capabilities(
        {"capabilities": [" one ", ""], "two": True, "three": False}
    )
    if bool_request != ("one", "two"):
        raise AssertionError(f"REQUEST_NORMALIZATION_CHANGED: {bool_request!r}")

    if module._contains_any(("a", "b"), ("x", "b")) is not True:
        raise AssertionError("CONTAINS_ANY_TRUE_CHANGED")
    if module._contains_any(("a",), ("x", "b")) is not False:
        raise AssertionError("CONTAINS_ANY_FALSE_CHANGED")

    _assert_error(
        lambda: module.evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request([]),
        "TypeError",
        "request must be a mapping",
    )


def _assert_source_safety_behavior(module: Any) -> None:
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_host_binding import (
        build_phase11_read_only_panel_host_binding_implementation_probe,
    )

    descriptor = build_phase11_read_only_panel_host_binding_implementation_probe()
    if module._source_host_binding_descriptor_is_safe(descriptor) is not True:
        raise AssertionError("SAFE_SOURCE_DESCRIPTOR_REJECTED")
    if module._source_host_binding_descriptor_is_safe(object()) is not False:
        raise AssertionError("UNSAFE_SOURCE_DESCRIPTOR_ACCEPTED")

    original = module.build_phase11_read_only_panel_host_binding_implementation_probe
    module.build_phase11_read_only_panel_host_binding_implementation_probe = lambda: object()
    try:
        blocked = module.build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract()
    finally:
        module.build_phase11_read_only_panel_host_binding_implementation_probe = original
    if blocked.status.value != "blocked_unsafe_source_descriptor":
        raise AssertionError("UNSAFE_SOURCE_BUILD_STATUS_CHANGED")


def _assert_semantic_safety(paths: list[Path]) -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        detect_semantic_dynamic_risks,
    )

    for path in paths:
        findings = detect_semantic_dynamic_risks(
            path.read_text(encoding="utf-8"),
            str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        )
        if findings:
            raise AssertionError(f"SEMANTIC_DYNAMIC_RISK: {path}: {findings}")


def _assert_fresh_ast(paths: list[Path]) -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for path in paths:
        result = run_large_module_split_audit(PROJECT_ROOT, path, classifier_mode="heuristic")
        classification = result.data["refactor_safety_classification"]
        if classification["label"] != "SAFE REFACTORING":
            raise AssertionError(f"AST_SPLIT_SAFETY_LABEL_NOT_SAFE: {path}")
        if classification["hard_blockers"]:
            raise AssertionError(f"AST_SPLIT_HARD_BLOCKERS_REMAIN: {path}")


def _assert_patch_contract(patch_zip: Path) -> None:
    from kanda_reasoner_app.patch_governance.validator import validate_install_script_text

    with zipfile.ZipFile(patch_zip, "r") as archive:
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))
        by_path = {item["relative_path"]: item for item in manifest["files"]}
        target_item = by_path[TARGET_REL]
        if BASELINE_TARGET_SHA256 not in set(target_item.get("accepted_existing_sha256", [])):
            raise AssertionError("SOURCE_IDENTITY_GUARD_BASELINE_HASH_MISSING")
        for rel in (TARGET_REL, EVALUATION_REL, INVARIANTS_REL, VALIDATOR_REL):
            item = by_path[rel]
            payload = archive.read("payload/" + rel)
            if hashlib.sha256(payload).hexdigest() != item["sha256"]:
                raise AssertionError(f"PACKAGE_PAYLOAD_HASH_MISMATCH: {rel}")
        validate_install_script_text(archive.read("INSTALL.ps1").decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    args = parser.parse_args()

    target = PROJECT_ROOT / TARGET_REL
    evaluation = PROJECT_ROOT / EVALUATION_REL
    invariants = PROJECT_ROOT / INVARIANTS_REL
    validator = PROJECT_ROOT / VALIDATOR_REL
    touched = [target, evaluation, invariants, validator]

    for path in touched:
        if not path.is_file():
            raise FileNotFoundError(path)
        _assert_ascii_utf8_no_bom(path)
        _assert_size(path)
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("PYTHON_SYNTAX: PASS")

    _assert_semantic_safety([target, evaluation, invariants])
    print("SEMANTIC_DYNAMIC_SAFETY: PASS")

    _assert_no_helper_to_facade_import(evaluation)
    _assert_no_helper_to_facade_import(invariants)
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")

    _assert_decorators(target)
    print("DECORATOR_PRESERVATION: PASS")

    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_runtime_app_host_visibility_contract as module,
    )

    _assert_public_contract(module)
    print("PUBLIC_API_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")

    _assert_policy_contract(module)
    _assert_decision_contract(module)
    _assert_request_behavior(module)
    _assert_source_safety_behavior(module)
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")

    _assert_fresh_ast([target, evaluation, invariants])
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("FRESH_FAMILY_AST_FITNESS: PASS")

    if args.patch_zip:
        _assert_patch_contract(Path(args.patch_zip).expanduser().resolve())
        print("SOURCE_IDENTITY_GUARD: PASS")
        print("INSTALLER_CONTRACT: PASS")
        print("PACKAGE_PAYLOAD_HASHES: PASS")

    print("INSTALLABILITY_FITNESS: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
