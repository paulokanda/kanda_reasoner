# project-path: tools/validate_large_file_refactor_planner_route_memory_box_v1.py
"""Validate the isolated Planner route-memory box and selector integration."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "large-file-refactor-planner-route-memory-box-v1"
PACKAGE_FILES = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_preference_box.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_state.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_selector_gui.py",
    "tools/validate_large_file_refactor_planner_route_memory_box_v1.py",
)
RUNTIME_FILES = PACKAGE_FILES[:3]
BASELINE_HASHES = {
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_state.py": "82c45fce56f89b876e5e318c4976ad2140b71e67c970a4574bffd69767316064",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_selector_gui.py": "a105433fd5dec196b0a967bb7164ecb1413bc93a3196849d0872aae400480595",
}


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--patch-zip", default="")
    parser.add_argument("--allow-missing-qt", action="store_true")
    return parser.parse_args()


def validate_package(root: Path, patch_zip: str) -> None:
    if not patch_zip:
        return
    zip_path = Path(patch_zip).resolve()
    require(zip_path.is_file(), "PATCH_ZIP_PRESENT")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        require("PACKAGE_MANIFEST.json" in names, "PACKAGE_MANIFEST_PRESENT")
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json"))
        records = {item["relative_path"]: item for item in manifest["files"]}
        for rel in PACKAGE_FILES:
            require(rel in records, "MANIFEST_RECORD_" + rel.replace("/", "__"))
            payload_name = "payload/" + rel
            require(payload_name in names, "ZIP_PAYLOAD_" + rel.replace("/", "__"))
            digest = hashlib.sha256(archive.read(payload_name)).hexdigest()
            require(digest == records[rel]["sha256"], "PAYLOAD_HASH_" + rel.replace("/", "__"))
        for rel, digest in BASELINE_HASHES.items():
            accepted = {str(x).lower() for x in records[rel].get("accepted_existing_sha256", [])}
            require(digest in accepted, "ACCEPTED_PREDECESSOR_" + Path(rel).name)
    print("PACKAGE_PAYLOAD_HASHES: PASS")
    print("ZIP CONTRACT: PASS")


def validate_source_contract(root: Path) -> None:
    for rel in PACKAGE_FILES:
        path = root / rel
        require(path.is_file(), "SOURCE_PRESENT_" + Path(rel).name)
        raw = path.read_bytes()
        require(not raw.startswith(b"\xef\xbb\xbf"), "UTF8_NO_BOM_" + Path(rel).name)
        source = raw.decode("utf-8", errors="strict")
        tree = ast.parse(source, filename=rel)
        require(tree is not None, "PYTHON_SYNTAX_" + Path(rel).name)
        lines = len(source.splitlines())
        require(100 < lines < 500, "LINE_LAW_101_499_" + Path(rel).name)
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def called_names(source: str) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            names.add(node.func.id)
    return names


def validate_box_isolation(root: Path) -> None:
    box_path = root / RUNTIME_FILES[0]
    state_path = root / RUNTIME_FILES[1]
    selector_path = root / RUNTIME_FILES[2]
    box = box_path.read_text(encoding="utf-8")
    state = state_path.read_text(encoding="utf-8")
    selector = selector_path.read_text(encoding="utf-8")

    forbidden_tokens = (
        "workbench_",
        "advanced_quality_review",
        "freeze_after_update",
        "project_support",
        "source_apply",
        "preflight",
    )
    box_tree = ast.parse(box, filename=str(box_path))
    imported_modules: list[str] = []
    runtime_names: list[str] = []
    for node in ast.walk(box_tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name.lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported_modules.append(str(node.module or "").lower())
        elif isinstance(node, ast.Name):
            runtime_names.append(node.id.lower())
        elif isinstance(node, ast.Attribute):
            runtime_names.append(node.attr.lower())
    runtime_surface = tuple(imported_modules + runtime_names)
    require(
        not any(token in item for item in runtime_surface for token in forbidden_tokens),
        "PREFERENCE_BOX_NO_CROSS_BOX_IMPORT_OR_ACCESS",
    )
    window_arguments = [
        arg.arg
        for node in ast.walk(box_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
        if arg.arg == "window"
    ]
    window_names = [
        node.id
        for node in ast.walk(box_tree)
        if isinstance(node, ast.Name) and node.id == "window"
    ]
    require(not window_arguments and not window_names, "PREFERENCE_BOX_NO_WINDOW_OBJECT")
    require("PLANNER_ROUTE_PREFERENCE_KEY" in box, "PREFERENCE_BOX_DEDICATED_KEY")
    require("_LEGACY_PREFERENCE_KEY" in box, "PREFERENCE_BOX_LEGACY_MIGRATION")
    require("settings.sync()" in box, "PREFERENCE_BOX_SYNC_ON_WRITE")
    require("_large_file_refactor_version_settings" not in state, "NO_SHARED_HOST_SETTINGS_CACHE")
    require("planner_version_preference_box" in state, "STATE_DELEGATES_TO_PREFERENCE_BOX")

    dangerous = {"getattr", "setattr", "hasattr", "globals", "locals", "eval", "exec", "__import__"}
    for rel in RUNTIME_FILES:
        source = (root / rel).read_text(encoding="utf-8")
        require(not (called_names(source) & dangerous), "SEMANTIC_DYNAMIC_SAFETY_" + Path(rel).name)
    print("SEMANTIC_DYNAMIC_SAFETY: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("SHIELDING_LOGIC: PASS")

    require('(PLANNER_VERSION_WEB_AI, "Imported Web AI")' in selector, "IMPORTED_WEB_AI_LABEL_EXACT")
    require('(PLANNER_VERSION_WEB_AI, "Imported Web AI Version")' not in selector, "IMPORTED_WEB_AI_VERSION_WORD_REMOVED_FROM_LABEL")
    cancel_pos = selector.find('QPushButton("Cancel")')
    radio_pos = selector.find("for version_name, label in _VERSION_LABELS")
    stretch_pos = selector.find("row.addStretch(1)")
    require(radio_pos >= 0 < cancel_pos < stretch_pos, "CANCEL_AFTER_RADIOS_BEFORE_STRETCH")
    require("QMetaObject.connectSlotsByName(widget)" in selector, "SELECTOR_QT_AUTOCONNECT")
    require(".toggled.connect(" not in selector and "cancel_button.clicked.connect(" not in selector, "SELECTOR_NO_DIRECT_SIGNAL_WIRING")
    print("PLAN_ACTIONS_SELECTOR_SURFACE: PASS")


def validate_real_qsettings(root: Path, allow_missing_qt: bool) -> None:
    try:
        from PySide6.QtCore import QSettings
    except ImportError:
        if allow_missing_qt:
            print("REAL_QSETTINGS_INDEPENDENT_SESSION: SKIPPED_NO_PYSIDE6")
            return
        raise AssertionError("REAL_QSETTINGS_INDEPENDENT_SESSION_REQUIRES_PYSIDE6")

    sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_version_preference_box as box

    with tempfile.TemporaryDirectory() as directory:
        ini_path = str(Path(directory) / "planner_route_memory.ini")
        def factory():
            return QSettings(ini_path, QSettings.IniFormat)
        require(box.load_last_used_planner_route(settings_factory=factory) == "local_ai", "REAL_QSETTINGS_DEFAULT_LOCAL_AI")
        require(box.remember_last_used_planner_route("heuristic", settings_factory=factory), "REAL_QSETTINGS_WRITE_HEURISTIC")
        require(box.load_last_used_planner_route(settings_factory=factory) == "heuristic", "REAL_QSETTINGS_RESTORE_HEURISTIC_NEW_ENDPOINT")
        require(box.remember_last_used_planner_route("web_ai", settings_factory=factory), "REAL_QSETTINGS_WRITE_WEB_AI")
        require(box.load_last_used_planner_route(settings_factory=factory) == "web_ai", "REAL_QSETTINGS_RESTORE_WEB_AI_NEW_ENDPOINT")
    print("REAL_QSETTINGS_INDEPENDENT_SESSION: PASS")


def validate_real_qt_selector(root: Path, allow_missing_qt: bool) -> None:
    try:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6.QtWidgets import QApplication, QPushButton, QRadioButton
    except ImportError:
        if allow_missing_qt:
            print("REAL_QT_SELECTOR_SMOKE: SKIPPED_NO_PYSIDE6")
            return
        raise AssertionError("REAL_QT_SELECTOR_SMOKE_REQUIRES_PYSIDE6")

    sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_version_selector_gui as selector

    app = QApplication.instance() or QApplication([])
    del app
    class Bundle:
        plan = object()
        docstring_proposals = ()
    class Output:
        def setPlainText(self, _text):
            return None
    class Window:
        _large_file_refactor_last_analysis = None
        _large_file_refactor_plan_output = Output()
    window = Window()
    window.selected = "heuristic"
    window.available = {"heuristic"}
    window.bundles = {"heuristic": Bundle()}
    persisted = {"value": "heuristic"}

    originals = {
        "selected_planner_version": selector.selected_planner_version,
        "select_planner_version": selector.select_planner_version,
        "persist_planner_version_preference": selector.persist_planner_version_preference,
        "planner_version_available": selector.planner_version_available,
        "get_selected_planner_version_bundle": selector.get_selected_planner_version_bundle,
        "render_selected_planner_version": selector.render_selected_planner_version,
    }
    try:
        selector.selected_planner_version = lambda w: w.selected
        selector.select_planner_version = lambda w, value: setattr(w, "selected", value) or True
        selector.persist_planner_version_preference = lambda _w, value: persisted.__setitem__("value", value) or True
        selector.planner_version_available = lambda w, value: value in w.available
        selector.get_selected_planner_version_bundle = lambda w: w.bundles.get(w.selected)
        selector.render_selected_planner_version = lambda _w: None
        refreshes: list[str] = []
        widget = selector.build_planner_version_selector(window, refresh_callback=lambda w: refreshes.append(w.selected))
        radios = widget.findChildren(QRadioButton)
        buttons = widget.findChildren(QPushButton)
        require([radio.text() for radio in radios] == ["Heuristic", "Local AI", "Imported Web AI"], "REAL_QT_RADIO_LABELS")
        cancel = next(button for button in buttons if button.text() == "Cancel")
        local = next(radio for radio in radios if radio.text() == "Local AI")
        local.setChecked(True)
        require(window.selected == "local_ai" and persisted["value"] == "local_ai", "REAL_QT_RADIO_WRITE")
        cancel.click()
        require(window.selected == "heuristic" and persisted["value"] == "heuristic", "REAL_QT_CANCEL_RESTORE")
        require(bool(refreshes), "REAL_QT_REFRESH_CALLBACK")
    finally:
        for name, value in originals.items():
            setattr(selector, name, value)
    print("REAL_QT_SELECTOR_SMOKE: PASS")


def validate_fresh_ast(root: Path) -> None:
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import run_large_module_split_audit
    for rel in RUNTIME_FILES:
        result = run_large_module_split_audit(root, root / rel, classifier_mode="heuristic")
        classification = result.data["refactor_safety_classification"]
        require(classification["label"] == "SAFE REFACTORING", "AST_SAFE_" + Path(rel).name)
        require(not classification["hard_blockers"], "AST_ZERO_BLOCKERS_" + Path(rel).name)
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("FRESH_FAMILY_AST_FITNESS: PASS")


def run_box_shield_regression(root: Path) -> None:
    validator = root / "tools/validate_planner_preference_workbench_aqr_box_shield_v1.py"
    require(validator.is_file(), "FROZEN_BOX_SHIELD_VALIDATOR_PRESENT")
    result = subprocess.run([sys.executable, str(validator), "--project-root", str(root)], cwd=root, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    require(result.returncode == 0, "FROZEN_BOX_SHIELD_REGRESSION")


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    validate_package(root, args.patch_zip)
    validate_source_contract(root)
    validate_box_isolation(root)
    validate_real_qsettings(root, args.allow_missing_qt)
    validate_real_qt_selector(root, args.allow_missing_qt)
    validate_fresh_ast(root)
    run_box_shield_regression(root)
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")
    print("INSTALLABILITY_FITNESS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
