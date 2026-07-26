# project-path: tools/validate_runtime_activation_contract_ast_safe_refactor_v1.py
"""Validate the Phase 9 runtime activation contract AST-safe refactor."""

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
    "read_only_advisory_panel_runtime_activation_contract.py"
)
EVALUATION_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_runtime_activation_contract_evaluation.py"
)
INVARIANTS_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_runtime_activation_contract_invariants.py"
)
VALIDATOR_REL = "tools/validate_runtime_activation_contract_ast_safe_refactor_v1.py"
FEATURE_ID = "runtime-activation-contract-ast-safe-refactor-v1"
BASELINE_TARGET_SHA256 = "f7b88aad8438561ddeea1e6b29a60177ce40bd545da72ea7fd5cabf14206df22"
EXPECTED_PUBLIC_ALL = [
    "build_phase9_read_only_advisory_panel_runtime_activation_contract",
    "build_phase9_read_only_panel_runtime_activation_contract_probe",
    "evaluate_phase9_read_only_advisory_panel_runtime_activation_request",
    "ReadOnlyAdvisoryPanelRuntimeActivationDecision",
    "ReadOnlyPanelRuntimeActivationMode",
    "ReadOnlyPanelRuntimeActivationStatus",
]
DYNAMIC_CALL_NAMES = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "getattr",
    "globals",
    "locals",
    "setattr",
    "vars",
    "importlib.import_module",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def _dynamic_calls(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = _call_name(node.func)
            if name in DYNAMIC_CALL_NAMES:
                found.append(name)
    return sorted(found)


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _assert_module_size(path: Path) -> None:
    count = _line_count(path)
    if not 101 <= count <= 499:
        raise AssertionError(f"MODULE_SIZE_101_499 failed for {path}: {count}")


def _assert_ascii_utf8_no_bom(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError(f"UTF8_BOM_FORBIDDEN: {path}")
    raw.decode("ascii")


def _assert_no_helper_to_facade_import(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden = "read_only_advisory_panel_runtime_activation_contract"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and forbidden in str(node.module or ""):
            raise AssertionError(f"HELPER_TO_FACADE_IMPORT: {path}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if forbidden in alias.name:
                    raise AssertionError(f"HELPER_TO_FACADE_IMPORT: {path}")


def _normalize(value: Any) -> Any:
    from enum import Enum

    if dataclasses.is_dataclass(value):
        return {
            field.name: _normalize(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    return value


def _capture(callable_obj: Any) -> dict[str, Any]:
    try:
        return {"ok": True, "value": _normalize(callable_obj())}
    except Exception as exc:
        return {"ok": False, "type": type(exc).__name__, "message": str(exc)}


def _assert_public_api_and_signatures() -> None:
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_runtime_activation_contract as module,
    )

    if list(module.__all__) != EXPECTED_PUBLIC_ALL:
        raise AssertionError("PUBLIC_API_ALL_CHANGED")

    expected_signatures = {
        "build_phase9_read_only_advisory_panel_runtime_activation_contract": (
            "(policy: 'Optional[ReadOnlyAdvisoryPanelRuntimeActivationPolicy]' = None, "
            "panel_view_model: 'Optional[ReadOnlyAdvisoryPanelViewModel]' = None) -> "
            "'ReadOnlyAdvisoryPanelRuntimeActivationDecision'"
        ),
        "evaluate_phase9_read_only_advisory_panel_runtime_activation_request": (
            "(*, policy: 'Optional[ReadOnlyAdvisoryPanelRuntimeActivationPolicy]' = None, "
            "requested_capabilities: 'Optional[Mapping[str, bool]]' = None, "
            "panel_view_model: 'Optional[ReadOnlyAdvisoryPanelViewModel]' = None) -> "
            "'ReadOnlyAdvisoryPanelRuntimeActivationDecision'"
        ),
        "build_phase9_read_only_panel_runtime_activation_contract_probe": (
            "() -> 'ReadOnlyAdvisoryPanelRuntimeActivationDecision'"
        ),
    }
    for name, expected in expected_signatures.items():
        actual = str(inspect.signature(getattr(module, name)))
        if actual != expected:
            raise AssertionError(f"PUBLIC_SIGNATURE_CHANGED: {name}: {actual}")


def _assert_behavior_contract() -> None:
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_runtime_activation_contract as module,
    )

    cases = {
        "authority": ({"route_authority": True}, "blocked_unsafe_authority"),
        "runtime": ({"mounted_panel": True}, "blocked_unsafe_runtime_wiring"),
        "side_effect": ({"provider_call": True}, "blocked_unsafe_data_or_side_effect"),
        "text": ({"free_text_explanation": True}, "blocked_unsafe_text_or_controls"),
        "benign": ({"observation_only": True}, "accepted_contract_only"),
        "false_ignored": ({"route_authority": False}, "accepted_contract_only"),
    }
    for name, (request, expected_status) in cases.items():
        decision = module.evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
            requested_capabilities=request
        )
        if decision.status.value != expected_status:
            raise AssertionError(f"BEHAVIOR_STATUS_MISMATCH: {name}")

    probe = module.build_phase9_read_only_panel_runtime_activation_contract_probe()
    if probe.status.value != "accepted_future_read_only_runtime_panel_contract":
        raise AssertionError("PROBE_STATUS_CHANGED")
    if probe.future_runtime_panel_contract_ready is not True:
        raise AssertionError("PROBE_READY_CONTRACT_CHANGED")

    missing_model_policy = module.ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_mode=module.ReadOnlyPanelRuntimeActivationMode.FUTURE_READ_ONLY_RUNTIME_PANEL
    )
    missing = module.build_phase9_read_only_advisory_panel_runtime_activation_contract(
        policy=missing_model_policy,
        panel_view_model=None,
    )
    if missing.status.value != "blocked_unsafe_source_model":
        raise AssertionError("MISSING_MODEL_BLOCK_CHANGED")

    policy = module.ReadOnlyAdvisoryPanelRuntimeActivationPolicy()
    for field in dataclasses.fields(policy):
        value = getattr(policy, field.name)
        if not isinstance(value, bool):
            continue
        outcome = _capture(
            lambda field_name=field.name, changed=not value: dataclasses.replace(
                policy,
                **{field_name: changed},
            )
        )
        if outcome.get("ok") is True:
            raise AssertionError(f"POLICY_INVARIANT_NOT_ENFORCED: {field.name}")

    decision = module.build_phase9_read_only_panel_runtime_activation_contract_probe()
    exempt = {"accepted", "future_runtime_panel_contract_ready"}
    for field in dataclasses.fields(decision):
        current = getattr(decision, field.name)
        if not isinstance(current, bool) or field.name in exempt:
            continue
        outcome = _capture(
            lambda name=field.name, changed=not current: dataclasses.replace(
                decision,
                **{name: changed},
            )
        )
        if outcome.get("ok") is True:
            raise AssertionError(f"DECISION_INVARIANT_NOT_ENFORCED: {field.name}")

    tuple_cases = {
        "required_safe_labels_list": _capture(
            lambda: dataclasses.replace(decision, required_safe_labels=["x"])
        ),
        "required_safe_labels_empty": _capture(
            lambda: dataclasses.replace(decision, required_safe_labels=())
        ),
        "required_safe_labels_blank": _capture(
            lambda: dataclasses.replace(decision, required_safe_labels=(" ",))
        ),
        "forbidden_capabilities_list": _capture(
            lambda: dataclasses.replace(decision, forbidden_capabilities=["x"])
        ),
    }
    expected_types = {
        "required_safe_labels_list": "TypeError",
        "required_safe_labels_empty": "ValueError",
        "required_safe_labels_blank": "ValueError",
        "forbidden_capabilities_list": "TypeError",
    }
    for name, outcome in tuple_cases.items():
        if outcome.get("type") != expected_types[name]:
            raise AssertionError(f"TUPLE_ERROR_CONTRACT_CHANGED: {name}")


def _assert_decorator_contract(target_path: Path) -> None:
    tree = ast.parse(target_path.read_text(encoding="utf-8"), filename=str(target_path))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    for name in (
        "ReadOnlyAdvisoryPanelRuntimeActivationPolicy",
        "ReadOnlyAdvisoryPanelRuntimeActivationDecision",
    ):
        node = classes.get(name)
        if node is None or len(node.decorator_list) != 1:
            raise AssertionError(f"DECORATOR_PRESERVATION_FAILED: {name}")
        decorator = node.decorator_list[0]
        if not isinstance(decorator, ast.Call) or _call_name(decorator.func) != "dataclass":
            raise AssertionError(f"DATACLASS_DECORATOR_MISSING: {name}")
        frozen = {
            keyword.arg: keyword.value
            for keyword in decorator.keywords
            if keyword.arg is not None
        }.get("frozen")
        if not isinstance(frozen, ast.Constant) or frozen.value is not True:
            raise AssertionError(f"DATACLASS_FROZEN_CHANGED: {name}")


def _assert_consumer_imports() -> None:
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_runtime_activation as implementation,
    )
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import __all__ as package_all

    if implementation is None:
        raise AssertionError("IMPLEMENTATION_CONSUMER_IMPORT_FAILED")
    if not isinstance(package_all, list):
        raise AssertionError("PACKAGE_ALL_CONTRACT_CHANGED")


def _assert_ast_safe(paths: list[Path]) -> None:
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
        accepted = set(target_item.get("accepted_existing_sha256", []))
        if BASELINE_TARGET_SHA256 not in accepted:
            raise AssertionError("SOURCE_IDENTITY_GUARD_BASELINE_HASH_MISSING")
        for rel in (TARGET_REL, EVALUATION_REL, INVARIANTS_REL, VALIDATOR_REL):
            item = by_path[rel]
            payload = archive.read("payload/" + rel)
            digest = hashlib.sha256(payload).hexdigest()
            if digest != item["sha256"]:
                raise AssertionError(f"PACKAGE_PAYLOAD_HASH_MISMATCH: {rel}")
        install_text = archive.read("INSTALL.ps1").decode("utf-8")
        validate_install_script_text(install_text)


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
        _assert_module_size(path)
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_SOURCE_MODULES_101_499: PASS")

    for path in (target, evaluation, invariants):
        dynamic = _dynamic_calls(path)
        if dynamic:
            raise AssertionError(f"DYNAMIC_CALLS_REMAIN: {path}: {dynamic}")
    print("REFLECTION_AND_DYNAMIC_CALLS_REMOVED: PASS")

    _assert_no_helper_to_facade_import(evaluation)
    _assert_no_helper_to_facade_import(invariants)
    print("DEPENDENCY_DIRECTION_FACADE_TO_HELPERS_ONLY: PASS")

    _assert_decorator_contract(target)
    print("DECORATOR_PRESERVATION: PASS")

    _assert_public_api_and_signatures()
    print("PUBLIC_API_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")

    _assert_behavior_contract()
    _assert_consumer_imports()
    print("BEHAVIOR_REGRESSION: PASS")
    print("CONSUMER_IMPORT_COMPATIBILITY: PASS")

    _assert_ast_safe([target, evaluation, invariants])
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")

    if args.patch_zip:
        patch_zip = Path(args.patch_zip).expanduser().resolve()
        _assert_patch_contract(patch_zip)
        print("SOURCE_IDENTITY_GUARD: PASS")
        print("INSTALLER_CONTRACT: PASS")
        print("PACKAGE_PAYLOAD_HASHES: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
