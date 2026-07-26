# project-path: tools/validate_planning_pipeline_cancel_preference_success_window_repair_v1.py
"""Validate Planner cancel, route persistence, and success-window import repair."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from typing import Any

FEATURE_ID = "planning-pipeline-cancel-preference-success-window-repair-v1"

MANAGE_GUI = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"
)
LIFECYCLE = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_card_lifecycle.py"
)
PLANNER_BOX = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
)
SELECTOR = PLANNER_BOX / "planner_version_selector_gui.py"
SHELL = PLANNER_BOX / "gui_shell.py"
CANCEL = PLANNER_BOX / "planner_background_cancel.py"
PREFERENCE = PLANNER_BOX / "planner_version_preference_box.py"
VALIDATOR = Path("tools") / Path(__file__).name

EXPECTED_PAYLOAD = {
    MANAGE_GUI,
    LIFECYCLE,
    SELECTOR,
    SHELL,
    CANCEL,
    VALIDATOR,
}
EXPECTED_ROOT_FILES = {
    "INSTALL.ps1",
    "KANDA_FREEZE_HINT.json",
    "PATCH_MANIFEST.json",
    "README.txt",
    "VALIDATE.ps1",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read(project_root: Path, relative_path: Path) -> str:
    return (project_root / relative_path).read_text(encoding="utf-8")


def _validate_success_window_import(project_root: Path) -> None:
    tree = ast.parse(_read(project_root, MANAGE_GUI), filename=str(MANAGE_GUI))
    imported: set[str] = set()
    calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == (
            "kanda_reasoner_app.templates.floating_windows"
        ):
            imported.update(alias.name for alias in node.names)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "show_auto_close_action_window":
                calls += 1
    _assert(
        "show_auto_close_action_window" in imported,
        "manage_architecture_gui does not import show_auto_close_action_window",
    )
    _assert(calls == 1, "success handler auto-close call count changed")
    print("NAMEERROR_SUCCESS_WINDOW_IMPORT: PASS")


def _method_node(tree: ast.AST, class_name: str, method_name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return child
    raise SystemExit("VALIDATION ERROR: method not found: " + method_name)


def _validate_selector_contract(project_root: Path) -> None:
    text = _read(project_root, SELECTOR)
    tree = ast.parse(text, filename=str(SELECTOR))
    method = _method_node(
        tree,
        "_PlannerVersionSelectorWidget",
        "on_largeFilePlannerVersionSelectionCancelButton_clicked",
    )
    names = {
        node.id
        for node in ast.walk(method)
        if isinstance(node, ast.Name)
    }
    attrs = {
        node.attr
        for node in ast.walk(method)
        if isinstance(node, ast.Attribute)
    }
    _assert("_restore_entry_selection" not in text, "obsolete route-restore helper remains")
    _assert("Restore the route" not in text, "obsolete Cancel tooltip remains")
    _assert("_cancel_callback" in attrs, "Cancel slot does not call cancel owner")
    _assert(
        "persist_planner_version_preference" not in names,
        "Cancel slot still persists or changes a route",
    )
    _assert(
        "_large_file_refactor_cancel_button" in text,
        "Cancel button is not projected from active work state",
    )
    print("PLANNER_CANCEL_NO_ROUTE_MUTATION: PASS")
    print("PLANNER_CANCEL_BUTTON_RUNNING_STATE_PROJECTION: PASS")


def _validate_lifecycle_contract(project_root: Path) -> None:
    text = _read(project_root, LIFECYCLE)
    _assert(
        "selected_version = selected_planner_version(window)" in text,
        "lifecycle does not snapshot the current route before clearing results",
    )
    _assert(
        "window._large_file_refactor_selected_version = selected_version" in text,
        "lifecycle does not restore the snapped route",
    )
    _assert(
        'window._large_file_refactor_selected_version = "local_ai"' not in text,
        "lifecycle still hardcodes Local AI and shunts persistence",
    )
    _assert(
        "planner_background_cancel" in text,
        "lifecycle still owns duplicated Planner cancellation logic",
    )
    print("PLANNER_LIFECYCLE_HARDCODED_ROUTE_SHUNT_REMOVED: PASS")


def _validate_shell_contract(project_root: Path) -> None:
    text = _read(project_root, SHELL)
    _assert(
        "from .planner_background_cancel import cancel_planner_background_work" in text,
        "Planning pipeline does not import its cancellation owner",
    )
    _assert(
        "cancel_callback=lambda target: cancel_planner_background_work(" in text,
        "Cancel button is not wired to Planner cancellation",
    )
    _assert(
        "user_visible=True" in text,
        "user cancellation does not provide visible settlement feedback",
    )
    print("PLANNING_PIPELINE_CANCEL_WIRING: PASS")


def _load_cancel_namespace(project_root: Path) -> dict[str, Any]:
    source = _read(project_root, CANCEL)
    tree = ast.parse(source, filename=str(CANCEL))
    filtered: list[ast.stmt] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level == 1:
            continue
        filtered.append(node)
    tree.body = filtered
    ast.fix_missing_locations(tree)
    sonar_calls: list[str] = []
    namespace: dict[str, Any] = {
        "__name__": "planner_background_cancel_validation",
        "finish_planner_sonar_error": lambda _window, message: sonar_calls.append(message),
    }
    exec(compile(tree, str(CANCEL), "exec"), namespace)
    namespace["_sonar_calls"] = sonar_calls
    return namespace


class _FakeTimer:
    def __init__(self) -> None:
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


class _FakeOutput:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def appendPlainText(self, message: str) -> None:
        self.messages.append(message)


class _FakeStatusBar:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def showMessage(self, message: str) -> None:
        self.messages.append(message)


def _cancel_window(*, split: bool, local_ai: bool) -> SimpleNamespace:
    status = _FakeStatusBar()
    window = SimpleNamespace(
        _large_file_refactor_selected_version="heuristic",
        _large_file_refactor_split_plan_running=split,
        _large_file_refactor_split_plan_request_id=object() if split else None,
        _large_file_refactor_split_plan_timer=_FakeTimer(),
        _large_file_refactor_ai_review_running=local_ai,
        _large_file_refactor_ai_review_request_id=object() if local_ai else None,
        _large_file_refactor_ai_review_timer=_FakeTimer(),
        _large_file_refactor_plan_output=_FakeOutput(),
        statusBar=lambda: status,
    )
    window._validation_status_bar = status
    return window


def _validate_cancel_runtime(project_root: Path) -> None:
    namespace = _load_cancel_namespace(project_root)
    cancel = namespace["cancel_planner_background_work"]

    for split, local_ai, marker in (
        (True, False, "PLANNER_CANCEL_SPLIT_PLAN"),
        (False, True, "PLANNER_CANCEL_LOCAL_AI_REVIEW"),
    ):
        window = _cancel_window(split=split, local_ai=local_ai)
        refreshes: list[object] = []
        selected_before = window._large_file_refactor_selected_version
        result = cancel(
            window,
            refresh_callback=lambda active: refreshes.append(active),
            user_visible=True,
        )
        _assert(result, marker + " did not report cancellation")
        _assert(
            not window._large_file_refactor_split_plan_running,
            marker + " left split generation running",
        )
        _assert(
            not window._large_file_refactor_ai_review_running,
            marker + " left Local AI review running",
        )
        _assert(
            window._large_file_refactor_split_plan_request_id is None,
            marker + " did not invalidate split request ownership",
        )
        _assert(
            window._large_file_refactor_ai_review_request_id is None,
            marker + " did not invalidate Local AI request ownership",
        )
        _assert(
            window._large_file_refactor_selected_version == selected_before,
            marker + " changed selected version",
        )
        _assert(len(refreshes) == 1, marker + " did not refresh exactly once")
        _assert(
            any("CANCELED:" in item for item in window._large_file_refactor_plan_output.messages),
            marker + " did not show cancellation feedback",
        )
        print(marker + ": PASS")

    idle = _cancel_window(split=False, local_ai=False)
    _assert(not cancel(idle, user_visible=True), "idle Cancel reported active work")
    _assert(
        idle._large_file_refactor_selected_version == "heuristic",
        "idle Cancel changed the selected route",
    )
    print("PLANNER_CANCEL_ROUTE_STABILITY: PASS")


def _load_lifecycle_namespace(project_root: Path) -> dict[str, Any]:
    source = _read(project_root, LIFECYCLE)
    tree = ast.parse(source, filename=str(LIFECYCLE))
    filtered: list[ast.stmt] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith(
            "kanda_reasoner_app"
        ):
            continue
        filtered.append(node)
    tree.body = filtered
    ast.fix_missing_locations(tree)
    namespace: dict[str, Any] = {
        "__name__": "architecture_review_card_lifecycle_validation",
        "_cancel_planner_background_work": lambda _window: False,
        "selected_planner_version": lambda window: str(
            window._large_file_refactor_selected_version
        ),
    }
    exec(compile(tree, str(LIFECYCLE), "exec"), namespace)
    return namespace


def _validate_lifecycle_runtime(project_root: Path) -> None:
    namespace = _load_lifecycle_namespace(project_root)
    clear_results = namespace["_clear_planner_results"]
    for route in ("heuristic", "local_ai", "web_ai"):
        window = SimpleNamespace(
            _large_file_refactor_selected_version=route,
            _large_file_refactor_planner_candidates=["candidate"],
            _large_file_refactor_warning_targets=["warning"],
            _large_file_refactor_warning_input_gate_open=True,
        )
        clear_results(window, clear_candidates=True)
        _assert(
            window._large_file_refactor_selected_version == route,
            "lifecycle clear changed selected route: " + route,
        )
    print("PLANNER_LIFECYCLE_SELECTION_RUNTIME_PRESERVED: PASS")


class _MemorySettings:
    def __init__(self, store: dict[str, str]) -> None:
        self._store = store
        self.sync_count = 0

    def value(self, key: str, default: str = "") -> str:
        return self._store.get(key, default)

    def setValue(self, key: str, value: str) -> None:
        self._store[key] = value

    def sync(self) -> None:
        self.sync_count += 1


def _load_preference_namespace(project_root: Path) -> dict[str, Any]:
    source = _read(project_root, PREFERENCE)
    tree = ast.parse(source, filename=str(PREFERENCE))
    namespace: dict[str, Any] = {"__name__": "planner_preference_validation"}
    exec(compile(tree, str(PREFERENCE), "exec"), namespace)
    return namespace


def _validate_preference_sessions(project_root: Path) -> None:
    namespace = _load_preference_namespace(project_root)
    store: dict[str, str] = {}
    factory = lambda: _MemorySettings(store)
    remember = namespace["remember_last_used_planner_route"]
    load = namespace["load_last_used_planner_route"]
    for route in ("heuristic", "web_ai", "local_ai"):
        _assert(remember(route, settings_factory=factory), "could not persist " + route)
        _assert(load(settings_factory=factory) == route, "could not restore " + route)
    print("PLANNER_PREFERENCE_BOX_SESSION_RESTORE: PASS")


def _validate_source_health(project_root: Path) -> None:
    for relative_path in EXPECTED_PAYLOAD:
        path = project_root / relative_path
        _assert(path.is_file(), "missing installed file: " + str(relative_path))
        raw = path.read_bytes()
        _assert(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM: " + str(relative_path))
        raw.decode("ascii")
        if path.suffix == ".py":
            compile(raw, str(relative_path), "exec")
        line_count = len(raw.splitlines())
        _assert(line_count <= 500, "module exceeds 500 lines: " + str(relative_path))
    print("PYTHON_SYNTAX: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_MODULES_MAX_500_LINES: PASS")


def _validate_zip_contract(project_root: Path, patch_zip: Path) -> None:
    _assert(patch_zip.is_file(), "patch ZIP not found: " + str(patch_zip))
    with zipfile.ZipFile(patch_zip) as archive:
        names = archive.namelist()
        _assert(len(names) == len(set(names)), "duplicate ZIP members")
        for name in names:
            path = PurePosixPath(name)
            _assert(not path.is_absolute(), "absolute ZIP member: " + name)
            _assert(".." not in path.parts, "path traversal ZIP member: " + name)
        root_files = {name for name in names if "/" not in name and not name.endswith("/")}
        _assert(
            EXPECTED_ROOT_FILES.issubset(root_files),
            "required root files missing from ZIP",
        )
        _assert(
            "payload/KANDA_FREEZE_HINT.json" not in names,
            "freeze hint duplicated inside payload",
        )
        payload_paths = {
            Path(name.removeprefix("payload/"))
            for name in names
            if name.startswith("payload/")
            and not name.endswith("/")
            and not name.startswith("payload/error_memory_receive_blocks/")
        }
        _assert(payload_paths == EXPECTED_PAYLOAD, "unexpected payload file set")
        manifest = json.loads(archive.read("PATCH_MANIFEST.json").decode("utf-8"))
        _assert(manifest.get("feature_id") == FEATURE_ID, "manifest feature ID mismatch")
        entries = manifest.get("files", [])
        _assert(isinstance(entries, list), "manifest files must be a list")
        by_path = {Path(item["path"]): item for item in entries}
        _assert(set(by_path) == EXPECTED_PAYLOAD, "manifest file set mismatch")
        for relative_path, item in by_path.items():
            payload_name = "payload/" + relative_path.as_posix()
            payload = archive.read(payload_name)
            _assert(
                _sha256(payload) == item.get("new_sha256"),
                "payload hash mismatch: " + str(relative_path),
            )
            installed = (project_root / relative_path).read_bytes()
            _assert(
                _sha256(installed) == item.get("new_sha256"),
                "installed source is not in sync: " + str(relative_path),
            )
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
        _assert(hint.get("feature_id") == FEATURE_ID, "freeze hint feature ID mismatch")
        error_blocks = [
            name for name in names
            if name.startswith("payload/error_memory_receive_blocks/")
            and not name.endswith("/")
        ]
        _assert(len(error_blocks) == 2, "Error Memory intake pair missing")
    print("PATCH_ZIP_CONTRACT: PASS")
    print("KANDA_FREEZE_HINT_ROOT_ONLY: PASS")
    print("ERROR_MEMORY_INTAKE_PAIR: PASS")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    project_root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    _validate_success_window_import(project_root)
    _validate_selector_contract(project_root)
    _validate_lifecycle_contract(project_root)
    _validate_shell_contract(project_root)
    _validate_cancel_runtime(project_root)
    _validate_lifecycle_runtime(project_root)
    _validate_preference_sessions(project_root)
    _validate_source_health(project_root)
    _validate_zip_contract(project_root, patch_zip)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
