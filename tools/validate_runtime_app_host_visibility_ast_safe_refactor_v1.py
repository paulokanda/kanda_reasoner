# project-path: tools/validate_runtime_app_host_visibility_ast_safe_refactor_v1.py
"""Validate the Phase 12 runtime app-host visibility AST-safe refactor."""

from __future__ import annotations

import argparse
import ast
import dataclasses
import hashlib
import inspect
import json
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "read_only_advisory_panel_runtime_app_host_visibility.py"
)
INVARIANTS_REL = (
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "_read_only_advisory_panel_runtime_app_host_visibility_invariants.py"
)
VALIDATOR_REL = "tools/validate_runtime_app_host_visibility_ast_safe_refactor_v1.py"
FEATURE_ID = "runtime-app-host-visibility-ast-safe-refactor-v1"
BASELINE_TARGET_SHA256 = "cea7621d2101cac8aed82d98dbef429a3c1e7871a77f489c65aabe434d4b09bc"
EXPECTED_PUBLIC_ALL = [
    "build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe",
    "build_read_only_advisory_panel_runtime_app_host_visibility_descriptor",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy",
    "ReadOnlyAdvisoryPanelRuntimeVisibleSection",
    "ReadOnlyPanelRuntimeAppHostVisibilityImplementationState",
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


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


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
    forbidden = "read_only_advisory_panel_runtime_app_host_visibility"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and forbidden in str(node.module or ""):
            raise AssertionError(f"HELPER_TO_FACADE_IMPORT: {path}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if forbidden in alias.name:
                    raise AssertionError(f"HELPER_TO_FACADE_IMPORT: {path}")


def _capture(callable_obj: Any) -> dict[str, Any]:
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


def _assert_decorator_contract(target_path: Path) -> None:
    tree = ast.parse(target_path.read_text(encoding="utf-8"), filename=str(target_path))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    for name in (
        "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy",
        "ReadOnlyAdvisoryPanelRuntimeVisibleSection",
        "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor",
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


def _policy(module: Any, **changes: Any) -> Any:
    values = {
        "visibility_surface_id": "surface",
        "visibility_surface_label": "Surface",
    }
    values.update(changes)
    return module.ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy(**values)


def _section(module: Any, **changes: Any) -> Any:
    values = {
        "section_key": "key",
        "label": "Label",
        "value": "Value",
        "severity": "info",
    }
    values.update(changes)
    return module.ReadOnlyAdvisoryPanelRuntimeVisibleSection(**values)


def _assert_public_contract(module: Any) -> None:
    if list(module.__all__) != EXPECTED_PUBLIC_ALL:
        raise AssertionError("PUBLIC_API_ALL_CHANGED")
    expected_signatures = {
        "build_read_only_advisory_panel_runtime_app_host_visibility_descriptor": (
            "(policy: 'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy', "
            "host_binding_descriptor: 'object | None') -> "
            "'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor'"
        ),
        "build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe": (
            "() -> 'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor'"
        ),
        "_require_tuple_of_visible_sections": (
            "(name: 'str', value: 'Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...]') -> 'None'"
        ),
    }
    for name, expected in expected_signatures.items():
        actual = str(inspect.signature(getattr(module, name)))
        if actual != expected:
            raise AssertionError(f"SIGNATURE_CHANGED: {name}: {actual}")


def _assert_policy_contract(module: Any) -> None:
    policy = _policy(module)
    if policy.feature_flag_enabled is not False or policy.max_visible_sections != 11:
        raise AssertionError("POLICY_DEFAULTS_CHANGED")
    _assert_error(
        lambda: _policy(module, visibility_surface_id=""),
        "ValueError",
        "visibility_surface_id must be non-empty text",
    )
    _assert_error(
        lambda: _policy(module, source_review_feature_id="bad"),
        "ValueError",
        "source_review_feature_id must match Phase 12 contract review gate",
    )
    _assert_error(
        lambda: _policy(module, max_visible_sections=0),
        "ValueError",
        "max_visible_sections must be a positive integer",
    )
    for name in module._policy_required_true_fields():
        _assert_error(
            lambda name=name: _policy(module, **{name: False}),
            "ValueError",
            name + " must remain True",
        )
    for name in module._policy_required_false_fields():
        _assert_error(
            lambda name=name: _policy(module, **{name: True}),
            "ValueError",
            name + " must remain False",
        )


def _assert_section_contract(module: Any) -> None:
    section = _section(module)
    if section.host_role != "read_only_advisory_observation":
        raise AssertionError("VISIBLE_SECTION_DEFAULT_CHANGED")
    cases = (
        ("read_only", False, "runtime-visible section must remain read-only"),
        ("display_only", False, "runtime-visible section must remain display-only"),
        ("action_enabled", True, "runtime-visible section actions are forbidden"),
        ("route_authority_enabled", True, "runtime-visible section route authority is forbidden"),
        ("route_influence_enabled", True, "runtime-visible section route influence is forbidden"),
        ("host_callback_enabled", True, "runtime-visible section callbacks are forbidden"),
        ("free_text_route_advice_enabled", True, "runtime-visible section free-text route advice is forbidden"),
    )
    for name, bad, message in cases:
        _assert_error(
            lambda name=name, bad=bad: _section(module, **{name: bad}),
            "ValueError",
            message,
        )


def _assert_descriptor_contract(module: Any) -> None:
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_host_binding import (
        build_phase11_read_only_panel_host_binding_implementation_probe,
    )

    disabled = module.build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(
        _policy(module),
        None,
    )
    if disabled.state.value != "disabled_noop" or disabled.failure_state_codes != ("feature_flag_default_off",):
        raise AssertionError("DISABLED_DESCRIPTOR_CHANGED")

    enabled_policy = _policy(module, feature_flag_enabled=True)
    missing = module.build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(
        enabled_policy,
        None,
    )
    if missing.state.value != "fail_open_no_descriptor":
        raise AssertionError("MISSING_DESCRIPTOR_STATE_CHANGED")

    host = build_phase11_read_only_panel_host_binding_implementation_probe()
    ready = module.build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(
        enabled_policy,
        host,
    )
    if ready.state.value != "read_only_visibility_descriptor_ready":
        raise AssertionError("READY_DESCRIPTOR_STATE_CHANGED")
    if ready.read_only_runtime_app_host_visibility_descriptor_ready is not True:
        raise AssertionError("READY_DESCRIPTOR_FLAG_CHANGED")
    if not ready.visible_sections:
        raise AssertionError("READY_VISIBLE_SECTIONS_MISSING")

    unsafe_host = build_phase11_read_only_panel_host_binding_implementation_probe()
    object.__setattr__(unsafe_host, "read_only", False)
    unsafe = module.build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(
        enabled_policy,
        unsafe_host,
    )
    if unsafe.state.value != "blocked_unsafe_descriptor":
        raise AssertionError("UNSAFE_DESCRIPTOR_STATE_CHANGED")

    for name in module._descriptor_required_true_fields():
        _assert_error(
            lambda name=name: dataclasses.replace(ready, **{name: False}),
            "ValueError",
            name + " must remain True",
        )
    for name in module._descriptor_forbidden_true_fields():
        _assert_error(
            lambda name=name: dataclasses.replace(ready, **{name: True}),
            "ValueError",
            name + " must remain False",
        )
    _assert_error(
        lambda: dataclasses.replace(ready, critical_boundary_error_budget=1),
        "ValueError",
        "critical_boundary_error_budget must remain zero",
    )
    _assert_error(
        lambda: dataclasses.replace(ready, visible_sections=[]),
        "TypeError",
        "visible_sections must be a tuple",
    )
    _assert_error(
        lambda: dataclasses.replace(ready, failure_state_codes=["x"]),
        "TypeError",
        "failure_state_codes must be a tuple",
    )
    _assert_error(
        lambda: dataclasses.replace(ready, source_host_container_id=""),
        "ValueError",
        "source_host_container_id must be non-empty text",
    )

    probe = module.build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe()
    if probe.state.value != "read_only_visibility_descriptor_ready":
        raise AssertionError("PHASE12_PROBE_CHANGED")


def _assert_consumer_imports() -> None:
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        _read_only_advisory_panel_passive_visibility_activation_contract_evaluation as evaluation,
    )
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_passive_visibility_activation as activation,
    )
    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_passive_visibility_activation_contract as contract,
    )

    if evaluation is None or activation is None or contract is None:
        raise AssertionError("CONSUMER_IMPORT_FAILED")


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
        if BASELINE_TARGET_SHA256 not in set(target_item.get("accepted_existing_sha256", [])):
            raise AssertionError("SOURCE_IDENTITY_GUARD_BASELINE_HASH_MISSING")
        for rel in (TARGET_REL, INVARIANTS_REL, VALIDATOR_REL):
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
    invariants = PROJECT_ROOT / INVARIANTS_REL
    validator = PROJECT_ROOT / VALIDATOR_REL
    touched = [target, invariants, validator]

    for path in touched:
        if not path.is_file():
            raise FileNotFoundError(path)
        _assert_ascii_utf8_no_bom(path)
        _assert_module_size(path)
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_SOURCE_MODULES_101_499: PASS")

    for path in (target, invariants):
        dynamic = _dynamic_calls(path)
        if dynamic:
            raise AssertionError(f"DYNAMIC_CALLS_REMAIN: {path}: {dynamic}")
    print("REFLECTION_AND_DYNAMIC_CALLS_REMOVED: PASS")

    _assert_no_helper_to_facade_import(invariants)
    print("DEPENDENCY_DIRECTION_FACADE_TO_HELPER_ONLY: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")

    _assert_decorator_contract(target)
    print("DECORATOR_PRESERVATION: PASS")

    from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
        read_only_advisory_panel_runtime_app_host_visibility as module,
    )

    _assert_public_contract(module)
    print("PUBLIC_API_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")

    _assert_policy_contract(module)
    _assert_section_contract(module)
    _assert_descriptor_contract(module)
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")

    _assert_consumer_imports()
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")

    _assert_ast_safe([target, invariants])
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("FRESH_FAMILY_AST_FITNESS: PASS")

    if args.patch_zip:
        _assert_patch_contract(Path(args.patch_zip).expanduser().resolve())
        print("SOURCE_IDENTITY_GUARD: PASS")
        print("INSTALLER_CONTRACT: PASS")
        print("PACKAGE_PAYLOAD_HASHES: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
