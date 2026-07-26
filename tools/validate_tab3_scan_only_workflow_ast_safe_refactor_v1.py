# project-path: tools/validate_tab3_scan_only_workflow_ast_safe_refactor_v1.py
"""Focused validation for the Tab 3 scan-only workflow AST-safe refactor."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType
from typing import Any
import zipfile

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT_TEXT = str(PROJECT_ROOT)
if PROJECT_ROOT_TEXT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_TEXT)

FEATURE_ID = "tab3-scan-only-workflow-ast-safe-refactor-v1"
FACADE_REL = "kanda_reasoner_app/tab3_manual_review_runtime/scan_only_workflow.py"
CONTROLS_REL = "kanda_reasoner_app/tab3_manual_review_runtime/scan_controls_runtime.py"
LIFECYCLE_REL = "kanda_reasoner_app/tab3_manual_review_runtime/scan_report_lifecycle_runtime.py"
LAYOUT_REL = "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py"
BASELINE_MEMBER = "validation_baseline/scan_only_workflow.py"
EXPECTED_OLD_SHA256 = "d38bc3c1d9a3959fb86522871cd258a9ce86bdee5bd4d0af3f993d7404008194"
EXPECTED_FACADE_SHA256 = "0e5bc4141edcbabcf5ac9b9a9f856dd87ee66679d5d0e06f708c4f6004b24a18"
EXPECTED_CONTROLS_SHA256 = "1535a82c6de0678e7ca9651102335c5da94e3bd92422f78b4508ede25d427b2f"
EXPECTED_LIFECYCLE_SHA256 = "516dbabb5093c183cb25e7c4d38d146d48e4f46ead94fea22df737eb05450658"
EXPECTED_ALL = (
    "SCAN_MODE",
    "SCAN_DIFF_WRITE_MODES",
    "DEFAULT_SCAN_REPORT_NAME",
    "configure_scan_diff_write_controls",
    "configure_scan_only_controls",
    "ensure_scan_report_path",
    "prepare_scan_report_lifecycle",
    "refresh_selected_mode_controls",
    "run_scan_only_mode",
    "run_scan_selected_mode",
    "use_project_root_as_scan_scope",
)


class WidgetDouble:
    """Small Qt-like widget double used by characterization cases."""

    def __init__(self, text: str = "") -> None:
        self.text_value = text
        self.current_text = text
        self.current = ""
        self.items: list[str] = []
        self.enabled = True
        self.checked = False
        self.visible = True
        self.clear_calls = 0

    def text(self) -> str:
        return self.text_value

    def setText(self, value: str) -> None:
        self.text_value = str(value)

    def currentText(self) -> str:
        return self.current_text

    def setCurrentText(self, value: str) -> None:
        self.current_text = str(value)

    def clear(self) -> None:
        self.items = []
        self.current_text = ""
        self.clear_calls += 1

    def addItem(self, value: str) -> None:
        self.items.append(str(value))
        if not self.current_text:
            self.current_text = str(value)

    def setEnabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)

    def setChecked(self, checked: bool) -> None:
        self.checked = bool(checked)

    def hide(self) -> None:
        self.visible = False

    def show(self) -> None:
        self.visible = True


class OwnerDouble:
    """Tab 3 owner double with the stable fields used by the workflow."""

    def __init__(self, project_root: Path, report_text: str = "") -> None:
        self._mode_combo = WidgetDouble("diff")
        self._confirm_write_checkbox = WidgetDouble()
        self._run_button = WidgetDouble("Run selected mode")
        self._scope_combo = WidgetDouble("Target path")
        self._target_path_edit = WidgetDouble("pkg/module.py")
        self._root_path_edit = WidgetDouble(str(project_root))
        self._report_path_edit = WidgetDouble(report_text)
        self._module_checkbox = WidgetDouble()
        self._class_checkbox = WidgetDouble()
        self._function_checkbox = WidgetDouble()
        self._file_address_checkbox = WidgetDouble()
        self.output: list[str] = []
        self.load_calls = 0
        self.save_pref_calls = 0

    def _append_text(self, text: str) -> None:
        self.output.append(str(text))

    def _load_report_rows(self) -> None:
        self.load_calls += 1

    def _save_prefs(self) -> None:
        self.save_pref_calls += 1


class OwnerWithoutReportPath:
    """Compatibility owner without the report path edit field."""

    def __init__(self) -> None:
        self.output: list[str] = []

    def _append_text(self, text: str) -> None:
        self.output.append(str(text))


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _load_baseline_module(patch_zip: Path) -> ModuleType:
    with zipfile.ZipFile(patch_zip, "r") as archive:
        source = archive.read(BASELINE_MEMBER)
    assert _sha256_bytes(source) == EXPECTED_OLD_SHA256
    with tempfile.TemporaryDirectory(prefix="kanda_scan_baseline_") as folder:
        path = Path(folder) / "scan_only_workflow_baseline.py"
        path.write_bytes(source)
        spec = importlib.util.spec_from_file_location("kanda_validation_scan_baseline", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def _candidate_module() -> ModuleType:
    from kanda_reasoner_app.tab3_manual_review_runtime import scan_only_workflow

    return scan_only_workflow


def _ast_contract(source: str) -> dict[str, Any]:
    tree = ast.parse(source)
    all_symbols: list[str] = []
    function_contracts: dict[str, dict[str, Any]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            if "__all__" in names and isinstance(node.value, (ast.List, ast.Tuple)):
                all_symbols = [
                    str(item.value)
                    for item in node.value.elts
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                ]
        if isinstance(node, ast.FunctionDef) and node.name in EXPECTED_ALL:
            function_contracts[node.name] = {
                "args": [arg.arg for arg in node.args.args],
                "defaults": [ast.unparse(item) for item in node.args.defaults],
                "annotations": {
                    arg.arg: ast.unparse(arg.annotation)
                    for arg in node.args.args
                    if arg.annotation is not None
                },
                "returns": ast.unparse(node.returns) if node.returns is not None else "",
                "decorators": [ast.unparse(item) for item in node.decorator_list],
            }
    return {"all": all_symbols, "functions": function_contracts}


def _widget_snapshot(owner: OwnerDouble) -> dict[str, Any]:
    return {
        "mode_items": list(owner._mode_combo.items),
        "mode_current": owner._mode_combo.current_text,
        "mode_enabled": owner._mode_combo.enabled,
        "mode_visible": owner._mode_combo.visible,
        "confirm_enabled": owner._confirm_write_checkbox.enabled,
        "confirm_checked": owner._confirm_write_checkbox.checked,
        "confirm_visible": owner._confirm_write_checkbox.visible,
        "button_text": owner._run_button.text_value,
        "scope": owner._scope_combo.current_text,
        "target": owner._target_path_edit.text_value,
        "labels": [
            owner._module_checkbox.text_value,
            owner._class_checkbox.text_value,
            owner._function_checkbox.text_value,
            owner._file_address_checkbox.text_value,
        ],
        "output": list(owner.output),
        "load_calls": owner.load_calls,
        "save_pref_calls": owner.save_pref_calls,
        "report_text": owner._report_path_edit.text_value,
    }


def _control_cases(module: ModuleType, root: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    owner = OwnerDouble(root)
    module.configure_scan_diff_write_controls(owner)
    results["configure_full"] = _widget_snapshot(owner)

    module.refresh_selected_mode_controls(owner, "write")
    results["refresh_write"] = _widget_snapshot(owner)
    module.refresh_selected_mode_controls(owner, "scan")
    results["refresh_scan"] = _widget_snapshot(owner)

    owner = OwnerDouble(root)
    module.configure_scan_only_controls(owner)
    results["configure_scan_only"] = _widget_snapshot(owner)

    owner = OwnerDouble(root)
    module.use_project_root_as_scan_scope(owner)
    results["project_scope"] = _widget_snapshot(owner)
    return results


def _ensure_path_cases(module: ModuleType, root: Path, outside: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    owner = OwnerDouble(root, str(root / "inside.jsonl"))
    accepted = module.ensure_scan_report_path(owner, chooser=lambda _owner, _default: outside / "report")
    results["outside_selected"] = {"accepted": accepted, "snapshot": _widget_snapshot(owner)}

    owner = OwnerDouble(root)
    rejected = module.ensure_scan_report_path(owner, chooser=lambda _owner, _default: root / "inside.jsonl")
    results["inside_rejected"] = {"accepted": rejected, "snapshot": _widget_snapshot(owner)}

    owner_without = OwnerWithoutReportPath()
    passthrough = module.ensure_scan_report_path(owner_without, chooser=lambda _owner, _default: None)
    results["no_report_edit"] = {"accepted": passthrough, "output": list(owner_without.output)}
    return results


def _lifecycle_cases(module: ModuleType, base: Path) -> dict[str, Any]:
    root = base / "project"
    outside = base / "reports"
    root.mkdir(parents=True, exist_ok=True)
    outside.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {}

    empty_owner = OwnerDouble(root)
    empty_owner._root_path_edit.setText("")
    results["empty_root"] = {
        "result": module.prepare_scan_report_lifecycle(empty_owner),
        "snapshot": _widget_snapshot(empty_owner),
    }

    previous = outside / "previous.jsonl"
    previous.write_text("old\n", encoding="utf-8")
    reuse_owner = OwnerDouble(root, str(previous))
    reuse_result = module.prepare_scan_report_lifecycle(
        reuse_owner,
        reuse_prompt=lambda _owner, _path: True,
    )
    results["reuse"] = {"result": reuse_result, "snapshot": _widget_snapshot(reuse_owner)}

    delete_path = outside / "delete.jsonl"
    delete_path.write_text("old\n", encoding="utf-8")
    delete_owner = OwnerDouble(root, str(delete_path))
    delete_result = module.prepare_scan_report_lifecycle(
        delete_owner,
        reuse_prompt=lambda _owner, _path: False,
        previous_action_prompt=lambda _owner, _path: "delete",
        folder_chooser=lambda _owner, _default: outside,
        now_provider=lambda: __import_datetime(),
    )
    results["delete"] = {
        "result": delete_result,
        "old_exists": delete_path.exists(),
        "snapshot": _widget_snapshot(delete_owner),
    }

    leave_path = outside / "leave.jsonl"
    leave_path.write_text("old\n", encoding="utf-8")
    leave_owner = OwnerDouble(root, str(leave_path))
    leave_result = module.prepare_scan_report_lifecycle(
        leave_owner,
        reuse_prompt=lambda _owner, _path: False,
        previous_action_prompt=lambda _owner, _path: "leave",
        folder_chooser=lambda _owner, _default: outside,
        now_provider=lambda: __import_datetime(),
    )
    results["leave"] = {
        "result": leave_result,
        "old_exists": leave_path.exists(),
        "snapshot": _widget_snapshot(leave_owner),
    }
    return results


def __import_datetime() -> Any:
    from datetime import datetime

    return datetime(2026, 7, 11, 2, 30, 45)


def _run_mode_cases(module: ModuleType, base: Path) -> dict[str, Any]:
    root = base / "project"
    outside = base / "reports"
    root.mkdir(parents=True, exist_ok=True)
    outside.mkdir(parents=True, exist_ok=True)
    calls: list[str] = []

    def legacy(_owner: object, mode: str) -> str:
        calls.append(mode)
        return "legacy:" + mode

    owner = OwnerDouble(root)
    selected_result = module.run_scan_selected_mode(
        owner,
        legacy,
        chooser=lambda _owner, _default: outside / "selected.jsonl",
    )
    selected = {"result": selected_result, "calls": list(calls), "snapshot": _widget_snapshot(owner)}

    calls.clear()
    owner = OwnerDouble(root)
    only_result = module.run_scan_only_mode(
        owner,
        "write",
        legacy,
        chooser=lambda _owner, _default: outside / "only.jsonl",
    )
    only = {"result": only_result, "calls": list(calls), "snapshot": _widget_snapshot(owner)}
    return {"selected": selected, "only": only}


def _behavior_snapshot(module: ModuleType, base: Path) -> dict[str, Any]:
    return {
        "controls": _control_cases(module, base / "project"),
        "ensure": _ensure_path_cases(module, base / "project", base / "reports"),
        "lifecycle": _lifecycle_cases(module, base / "lifecycle"),
        "run_modes": _run_mode_cases(module, base / "run_modes"),
    }


def _assert_source_identity(patch_zip: Path) -> None:
    expected = {
        FACADE_REL: EXPECTED_FACADE_SHA256,
        CONTROLS_REL: EXPECTED_CONTROLS_SHA256,
        LIFECYCLE_REL: EXPECTED_LIFECYCLE_SHA256,
    }
    for relative_path, digest in expected.items():
        assert _sha256(PROJECT_ROOT / relative_path) == digest, relative_path
    with zipfile.ZipFile(patch_zip, "r") as archive:
        baseline = archive.read(BASELINE_MEMBER)
    assert _sha256_bytes(baseline) == EXPECTED_OLD_SHA256
    print("SOURCE_IDENTITY_GUARD: PASS")


def _assert_package_contract(patch_zip: Path) -> None:
    from kanda_reasoner_app.patch_governance.validator import validate_patch_zip

    report = validate_patch_zip(patch_zip)
    assert report.get("ok") is True
    assert report.get("feature_id") == FEATURE_ID
    print("ZIP CONTRACT: PASS")


def _assert_public_contract(patch_zip: Path) -> None:
    with zipfile.ZipFile(patch_zip, "r") as archive:
        baseline_source = archive.read(BASELINE_MEMBER).decode("utf-8")
    candidate_source = (PROJECT_ROOT / FACADE_REL).read_text(encoding="utf-8")
    assert _ast_contract(candidate_source) == _ast_contract(baseline_source)
    candidate = _candidate_module()
    assert tuple(candidate.__all__) == EXPECTED_ALL
    assert candidate.SCAN_MODE == "scan"
    assert candidate.SCAN_DIFF_WRITE_MODES == ("scan", "diff", "write")
    assert candidate.DEFAULT_SCAN_REPORT_NAME == "missing_docstrings_report.jsonl"
    print("PUBLIC_API_PRESERVATION: PASS")
    print("DECORATOR_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")


def _assert_consumer_compatibility() -> None:
    source = (PROJECT_ROOT / LAYOUT_REL).read_text(encoding="utf-8")
    assert '".scan_only_workflow"' in source
    assert "_scan_only_runtime().configure_scan_diff_write_controls(window)" in source
    assert "_scan_only_runtime().refresh_selected_mode_controls(window)" in source
    candidate = _candidate_module()
    assert callable(candidate.configure_scan_diff_write_controls)
    assert callable(candidate.refresh_selected_mode_controls)
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")


def _assert_behavior_equivalence(patch_zip: Path) -> None:
    baseline = _load_baseline_module(patch_zip)
    candidate = _candidate_module()
    with tempfile.TemporaryDirectory(prefix="kanda_scan_behavior_") as folder:
        root = Path(folder)
        baseline_root = root / "baseline"
        candidate_root = root / "candidate"
        baseline_snapshot = _behavior_snapshot(baseline, baseline_root)
        candidate_snapshot = _behavior_snapshot(candidate, candidate_root)
    baseline_token = json.dumps(str(baseline_root))[1:-1]
    candidate_token = json.dumps(str(candidate_root))[1:-1]
    baseline_text = json.dumps(baseline_snapshot, indent=2, sort_keys=True).replace(baseline_token, "<CASE_ROOT>")
    candidate_text = json.dumps(candidate_snapshot, indent=2, sort_keys=True).replace(candidate_token, "<CASE_ROOT>")
    windows_root = r"C:\Temp\case\baseline"
    windows_text = json.dumps({"path": windows_root + r"\report.jsonl"})
    assert windows_text.replace(json.dumps(windows_root)[1:-1], "<CASE_ROOT>") == '{"path": "<CASE_ROOT>\\\\report.jsonl"}'
    assert candidate_text == baseline_text, (baseline_text, candidate_text)
    print("BEHAVIOR_PATH_ROOT_NORMALIZATION: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _assert_family_fitness() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_ast_safe_refactor_routine import (
        verify_candidate_family,
    )

    family = [FACADE_REL, CONTROLS_REL, LIFECYCLE_REL]
    report = verify_candidate_family(
        PROJECT_ROOT,
        family,
        facade_relative_path=FACADE_REL,
        helper_relative_paths=[CONTROLS_REL, LIFECYCLE_REL],
    )
    assert report.get("pass") is True, report
    assert not report.get("failures"), report
    for item in report.get("fresh_audits", []):
        assert item.get("label") == "SAFE REFACTORING", item
        assert not item.get("hard_blockers"), item
    print("PYTHON_SYNTAX: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("INITIAL_RISK_STATE_REPAIRED: PASS")


def _assert_qt_import_ownership() -> None:
    controls_source = (PROJECT_ROOT / CONTROLS_REL).read_text(encoding="utf-8")
    lifecycle_source = (PROJECT_ROOT / LIFECYCLE_REL).read_text(encoding="utf-8")
    assert "from PySide6.QtWidgets import QMessageBox" in controls_source
    assert "from PySide6.QtWidgets import QMessageBox" in lifecycle_source
    assert "from PySide6.QtWidgets import QFileDialog" in lifecycle_source
    try:
        from PySide6.QtWidgets import QFileDialog, QMessageBox

        assert QFileDialog is not None and QMessageBox is not None
        print("REAL_PYSIDE6_QT_WIDGETS_IMPORT_SMOKE: PASS")
    except ImportError:
        print("REAL_PYSIDE6_QT_WIDGETS_IMPORT_SMOKE: SKIP - PySide6 unavailable on this host")
    print("QT_IMPORT_OWNERSHIP: PASS")


def _run(patch_zip: Path) -> None:
    _assert_package_contract(patch_zip)
    _assert_source_identity(patch_zip)
    _assert_public_contract(patch_zip)
    _assert_consumer_compatibility()
    _assert_behavior_equivalence(patch_zip)
    _assert_qt_import_ownership()
    _assert_family_fitness()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    _run(Path(args.patch_zip).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
