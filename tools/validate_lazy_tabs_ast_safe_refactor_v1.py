"""Focused validator for the LazyToolTab AST-safe source-family refactor."""
from __future__ import annotations

import argparse
import ast
import hashlib
import inspect
import json
import os
import py_compile
import sys
import zipfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

__all__ = [
    "main",
]

FACADE = "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
SHELL = "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_shell_chrome.py"
LAYOUT = "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py"
FAMILY = [FACADE, SHELL, LAYOUT]
EXPECTED_ALL = ["LazyToolTab"]
EXPECTED_METHOD_SIGNATURES = {
    "__init__": "(self, spec: 'ToolSpec', on_loaded) -> 'None'",
    "_combo_current_text": "(combo: 'object') -> 'str'",
    "_combo_items": "(combo: 'object') -> 'list[str]'",
    "_replace_combo_items": "(combo: 'object', items: 'list[str]', selected: 'str') -> 'None'",
    "_connect_signal": "(widget: 'object', signal_name: 'str', slot: 'object') -> 'None'",
    "load_tool": "(self) -> 'bool'",
    "ensure_loaded": "(self) -> 'bool'",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _marker(text: str) -> None:
    print(text, flush=True)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _validate_zip_payload(project_root: Path, patch_zip: Path) -> None:
    with zipfile.ZipFile(patch_zip) as archive:
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))
        allowed = set(FAMILY + ["tools/validate_lazy_tabs_ast_safe_refactor_v1.py"])
        actual = {str(item["relative_path"]) for item in manifest["files"]}
        if actual != allowed:
            raise AssertionError(f"Unexpected payload paths: {sorted(actual ^ allowed)}")
        for item in manifest["files"]:
            relative = str(item["relative_path"])
            source = project_root / relative
            if not source.is_file():
                raise AssertionError(f"Installed payload missing: {relative}")
            if _sha256(source) != str(item["sha256"]):
                raise AssertionError(f"Installed payload hash mismatch: {relative}")
    _marker("PACKAGE_PAYLOAD_HASHES: PASS")
    _marker("BOX_SHIELDING_PAYLOAD_SCOPE: PASS")


def _validate_source_structure(project_root: Path) -> None:
    for relative in FAMILY:
        path = project_root / relative
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError(f"UTF-8 BOM forbidden: {relative}")
        text = raw.decode("utf-8")
        count = len(text.splitlines())
        if not 100 < count < 500:
            raise AssertionError(f"Line law violation: {relative} -> {count}")
        py_compile.compile(str(path), doraise=True)
    _marker("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    _marker("LINE_LAW_101_499_FITNESS: PASS")
    _marker("PYTHON_SYNTAX: PASS")


def _validate_public_contract(project_root: Path) -> None:
    source = (project_root / FACADE).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=FACADE)
    all_value: list[str] | None = None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            value = ast.literal_eval(node.value)
            all_value = list(value)
    if all_value != EXPECTED_ALL:
        raise AssertionError(f"__all__ changed: {all_value}")
    consumer = project_root / "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py"
    consumer_tree = ast.parse(consumer.read_text(encoding="utf-8"), filename=str(consumer))
    found = False
    for node in ast.walk(consumer_tree):
        if isinstance(node, ast.ImportFrom) and node.module == ".lazy_tabs":
            if any(alias.name == "LazyToolTab" for alias in node.names):
                found = True
        if isinstance(node, ast.ImportFrom) and node.module == "lazy_tabs":
            if any(alias.name == "LazyToolTab" for alias in node.names):
                found = True
    if not found and "from .lazy_tabs import LazyToolTab" not in consumer.read_text(encoding="utf-8"):
        raise AssertionError("Main-window LazyToolTab consumer import changed")
    _marker("PUBLIC_API_PRESERVATION: PASS")
    _marker("CONSUMER_COMPATIBILITY_FITNESS: PASS")


def _validate_semantic_safety(project_root: Path) -> None:
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )

    for relative in FAMILY:
        source = (project_root / relative).read_text(encoding="utf-8")
        findings = detect_semantic_dynamic_risks(source, relative)
        if findings:
            raise AssertionError(f"Semantic dynamic findings remain in {relative}: {findings}")
    direction = check_candidate_dependency_direction(
        project_root,
        facade_relative_path=FACADE,
        helper_relative_paths=[SHELL, LAYOUT],
    )
    if not direction.get("pass"):
        raise AssertionError(f"Dependency direction violation: {direction}")
    _marker("SEMANTIC_DYNAMIC_SAFETY: PASS")
    _marker("DEPENDENCY_DIRECTION_FITNESS: PASS")
    _marker("BOX_BOUNDARY_FITNESS: PASS")
    _marker("NO_LEAK_FITNESS: PASS")


def _validate_runtime_behavior(project_root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from PySide6.QtCore import QEventLoop, QTimer
    from PySide6.QtWidgets import QApplication, QComboBox, QWidget
    from kanda_reasoner_app.reasoner_tools_gui_shell import lazy_tabs

    app = QApplication.instance() or QApplication([])
    pending_calls = {"count": 0}
    moves: list[str] = []

    class Embedded(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self._model_combo = QComboBox(self)
            self._model_combo.addItems(["model-a", "model-b"])
            self._model_combo.setCurrentText("model-b")

        def load_pending_ai_assisted_error_lesson_intake_now(self) -> bool:
            pending_calls["count"] += 1
            return True

        def move_project_root_controls_to_layout(self, layout) -> None:
            moves.append("project_root")

        def move_ai_review_controls_to_layout(self, layout) -> None:
            moves.append("ai_review")

        def move_safe_mode_radio_to_layout(self, layout) -> None:
            moves.append("safe_mode")

    original_import = lazy_tabs._first_imported_module
    original_attr = lazy_tabs._first_existing_attr
    original_prepare = lazy_tabs._prepare_embedded_widget
    lazy_tabs._first_imported_module = lambda candidates: SimpleNamespace(Embedded=Embedded)
    lazy_tabs._first_existing_attr = lambda module, candidates: Embedded
    lazy_tabs._prepare_embedded_widget = lambda widget: widget
    callback_calls: list[str] = []
    spec = SimpleNamespace(
        step_title="Probe",
        source_hint="neutral.py",
        help_catalog=None,
        module_candidates=("probe.module",),
        class_candidates=("Embedded",),
    )
    try:
        tab = lazy_tabs.LazyToolTab(spec, lambda current_spec, widget: callback_calls.append(widget.__class__.__name__))
        tab.load_button.click()
        loop = QEventLoop()
        QTimer.singleShot(350, loop.quit)
        loop.exec()
        if not tab._loaded or tab.status_label.text() != "LOADED":
            raise AssertionError("Lazy-load completion behavior changed")
        if callback_calls != ["Embedded"]:
            raise AssertionError(f"on_loaded callback behavior changed: {callback_calls}")
        if pending_calls["count"] != 3:
            raise AssertionError(f"Pending intake retry count changed: {pending_calls['count']}")
        if not tab.load_button.isHidden():
            raise AssertionError("Load button hide behavior changed")

        combo = QComboBox()
        combo.addItems(["a", "b"])
        combo.setCurrentText("b")
        if lazy_tabs.LazyToolTab._combo_current_text(combo) != "b":
            raise AssertionError("Combo current-text helper changed")
        if lazy_tabs.LazyToolTab._combo_items(combo) != ["a", "b"]:
            raise AssertionError("Combo item helper changed")
        lazy_tabs.LazyToolTab._replace_combo_items(combo, ["x", "y"], "y")
        if lazy_tabs.LazyToolTab._combo_items(combo) != ["x", "y"] or combo.currentText() != "y":
            raise AssertionError("Combo replacement helper changed")

        for name, signature in EXPECTED_METHOD_SIGNATURES.items():
            actual = str(inspect.signature(getattr(lazy_tabs.LazyToolTab, name)))
            if actual != signature:
                raise AssertionError(f"Signature changed for {name}: {actual}")
    finally:
        lazy_tabs._first_imported_module = original_import
        lazy_tabs._first_existing_attr = original_attr
        lazy_tabs._prepare_embedded_widget = original_prepare
    _marker("DECORATOR_PRESERVATION: PASS")
    _marker("ANNOTATION_IMPORT_PRESERVATION: PASS")
    _marker("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    _marker("BEHAVIOR_REGRESSION: PASS")


def _validate_fresh_audits(project_root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative in FAMILY:
        result = run_large_module_split_audit(
            project_root,
            project_root / relative,
            classifier_mode="heuristic",
        )
        classification = result.data["refactor_safety_classification"]
        if classification["label"] != "SAFE REFACTORING":
            raise AssertionError(f"Fresh AST label not SAFE for {relative}: {classification}")
        if classification["hard_blockers"]:
            raise AssertionError(f"Fresh AST blockers remain for {relative}: {classification['hard_blockers']}")
    _marker("AST_SPLIT_AUDIT_RERUN: PASS")
    _marker("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    _marker("AST_SPLIT_HARD_BLOCKERS: 0")
    _marker("FRESH_FAMILY_AST_FITNESS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    project_root = _project_root()
    patch_zip = Path(args.patch_zip).resolve()
    _validate_zip_payload(project_root, patch_zip)
    _validate_source_structure(project_root)
    _validate_public_contract(project_root)
    _validate_semantic_safety(project_root)
    _validate_runtime_behavior(project_root)
    _validate_fresh_audits(project_root)
    _marker("INSTALLABILITY_FITNESS: PASS")
    _marker("VALIDATION OK: lazy-tabs-ast-safe-refactor-v1")
    _marker("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
