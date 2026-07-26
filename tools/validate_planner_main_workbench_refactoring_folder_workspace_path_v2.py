"""Validate the Main Workbench Refactoring Folder workspace-path behavior."""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path
import sys
import types
from typing import Any
import zipfile

FEATURE_ID = "planner-main-workbench-refactoring-folder-workspace-path-v2"
PATCH_NAME = "kanda_planner_main_workbench_refactoring_folder_workspace_path_v2"
HELPER_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_refactoring_folder_button.py"
)
VALIDATOR_RELATIVE = Path(
    "tools/validate_planner_main_workbench_refactoring_folder_workspace_path_v2.py"
)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_static(project_root: Path) -> None:
    helper_path = project_root / HELPER_RELATIVE
    _assert(helper_path.is_file(), "Main Workbench path button helper is missing")
    raw = helper_path.read_bytes()
    _assert(not raw.startswith(b"\xef\xbb\xbf"), "helper has UTF-8 BOM")
    text = raw.decode("utf-8")
    text.encode("ascii")
    lines = text.splitlines()
    _assert(101 <= len(lines) <= 499, "helper violates 101-499 line law")
    tree = ast.parse(text, filename=str(helper_path))
    function_names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    _assert(
        "_copy_main_workbench_artifact_paths" in function_names,
        "button callback is missing",
    )
    _assert(
        "_workspace_folder_path" in function_names,
        "workspace-path extractor is missing",
    )
    _assert(
        "_large_file_refactor_main_workbench_package_result" in text,
        "Main Workbench package-result owner is missing",
    )
    _assert(
        "QApplication.clipboard().setText(workspace_path)" in text,
        "workspace path is not copied to the clipboard",
    )
    _assert(
        "_set_output(window, workspace_path)" in text,
        "workspace path is not projected directly to the visible output",
    )
    for stale_text in (
        "MAIN WORKBENCH REFACTORING PATHS",
        "WORKSPACE FOLDER:",
        "CURRENT EXCHANGE FOLDER:",
        "INSTRUCTION FILE:",
        "MANIFEST:",
    ):
        _assert(stale_text not in text, "stale multi-path report remains: " + stale_text)
    print("MAIN_WORKBENCH_PACKAGE_RESULT_OWNER_STATIC: PASS")
    print("MAIN_WORKBENCH_WORKSPACE_PATH_ONLY_STATIC: PASS")
    print("MULTIPATH_REPORT_REMOVED_STATIC: PASS")
    print("TOUCHED_SOURCE_MODULE_LINE_LAW_101_499: PASS")


class _FakeEvent:
    def __init__(self, event_type: int) -> None:
        self._event_type = event_type

    def _qt_event_type(self) -> int:
        return self._event_type


_FakeEvent.type = _FakeEvent._qt_event_type


class _FakeQObject:
    def __init__(self, parent: Any = None) -> None:
        self.parent = parent


class _FakeQEvent:
    EnabledChange = 98


class _FakeSignal:
    def __init__(self) -> None:
        self._slots: list[Any] = []

    def connect(self, slot: Any) -> None:
        self._slots.append(slot)

    def emit(self) -> None:
        for slot in list(self._slots):
            slot()


class _FakeButton(_FakeQObject):
    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text
        self._enabled = True
        self._filters: list[Any] = []
        self.clicked = _FakeSignal()
        self.tooltip = ""
        self.object_name = ""

    def text(self) -> str:
        return self._text

    def setObjectName(self, value: str) -> None:
        self.object_name = value

    def setToolTip(self, value: str) -> None:
        self.tooltip = value

    def setEnabled(self, enabled: bool) -> None:
        changed = self._enabled != bool(enabled)
        self._enabled = bool(enabled)
        if changed:
            event = _FakeEvent(_FakeQEvent.EnabledChange)
            for event_filter in list(self._filters):
                event_filter.eventFilter(self, event)

    def isEnabled(self) -> bool:
        return self._enabled

    def installEventFilter(self, event_filter: Any) -> None:
        self._filters.append(event_filter)

    def click(self) -> None:
        if self._enabled:
            self.clicked.emit()


class _FakeClipboard:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, text: str) -> None:
        self.text = str(text)


class _FakeApplication:
    clipboard_object = _FakeClipboard()

    @classmethod
    def clipboard(cls) -> _FakeClipboard:
        return cls.clipboard_object


class _FakeOutput:
    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, text: str) -> None:
        self.text = str(text)


class _FakeLayoutItem:
    def __init__(self, widget: Any = None, layout: Any = None) -> None:
        self.widget = widget
        self.child_layout = layout

    def layout(self) -> Any:
        return self.child_layout


class _FakeLayout:
    def __init__(self) -> None:
        self.items: list[_FakeLayoutItem] = []

    def addWidget(self, widget: Any) -> None:
        self.items.append(_FakeLayoutItem(widget=widget))

    def addLayout(self, layout: Any) -> None:
        self.items.append(_FakeLayoutItem(layout=layout))

    def insertWidget(self, index: int, widget: Any) -> None:
        self.items.insert(index, _FakeLayoutItem(widget=widget))

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> _FakeLayoutItem:
        return self.items[index]

    def indexOf(self, widget: Any) -> int:
        for index, item in enumerate(self.items):
            if item.widget is widget:
                return index
        return -1


class _FakeWidget(_FakeQObject):
    def __init__(self, layout: _FakeLayout) -> None:
        super().__init__()
        self._layout = layout

    def layout(self) -> _FakeLayout:
        return self._layout

    def findChildren(self, cls: Any) -> list[Any]:
        found: list[Any] = []

        def visit(layout: _FakeLayout) -> None:
            for item in layout.items:
                if isinstance(item.widget, cls):
                    found.append(item.widget)
                if item.child_layout is not None:
                    visit(item.child_layout)

        visit(self._layout)
        return found


def _load_helper_with_fakes(project_root: Path):
    package = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    qtcore = types.ModuleType("PySide6.QtCore")
    qtcore.QEvent = _FakeQEvent
    qtcore.QObject = _FakeQObject
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtwidgets.QApplication = _FakeApplication
    qtwidgets.QLayout = _FakeLayout
    qtwidgets.QPushButton = _FakeButton
    qtwidgets.QWidget = _FakeWidget
    sys.modules["PySide6"] = types.ModuleType("PySide6")
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets

    original_name = package + ".main_workbench_gui"
    original = types.ModuleType(original_name)

    def build_controls(window: Any) -> _FakeWidget:
        root_layout = _FakeLayout()
        row = _FakeLayout()
        cancel = _FakeButton("Cancel Main Workbench")
        send = _FakeButton("Send Complete Project to Web AI")
        send.setEnabled(False)
        row.addWidget(cancel)
        row.addWidget(send)
        root_layout.addLayout(row)
        return _FakeWidget(root_layout)

    original.build_main_workbench_controls = build_controls
    sys.modules[original_name] = original

    helper_name = package + ".main_workbench_refactoring_folder_button"
    spec = importlib.util.spec_from_file_location(
        helper_name,
        project_root / HELPER_RELATIVE,
    )
    _assert(spec is not None and spec.loader is not None, "helper spec unavailable")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package
    sys.modules[helper_name] = module
    spec.loader.exec_module(module)
    return module


def _button(root: _FakeWidget, text: str) -> _FakeButton:
    matches = [item for item in root.findChildren(_FakeButton) if item.text() == text]
    _assert(len(matches) == 1, "button match invalid: " + text)
    return matches[0]


def _validate_runtime(project_root: Path) -> None:
    _FakeApplication.clipboard_object = _FakeClipboard()
    module = _load_helper_with_fakes(project_root)
    output = _FakeOutput()
    window = types.SimpleNamespace(
        _large_file_refactor_main_workbench_output=output,
        _large_file_refactor_main_workbench_package_result=None,
    )
    root = module.build_main_workbench_controls(window)
    folder = _button(root, "Refactoring Folder")
    send = _button(root, "Send Complete Project to Web AI")
    _assert(not folder.isEnabled(), "folder button did not mirror disabled send state")
    send.setEnabled(True)
    _assert(folder.isEnabled(), "folder button did not mirror enabled send state")

    folder.click()
    _assert(
        output.text.startswith("REFACTORING FOLDER NOT READY"),
        "missing package result feedback changed",
    )
    _assert(_FakeApplication.clipboard().text == "", "clipboard changed without result")

    workspace = "E:/support/ai_refactoring_exchange/module__card"
    window._large_file_refactor_main_workbench_package_result = types.SimpleNamespace(
        workspace_root=workspace,
        exchange_root=workspace + "/EXCH-0001",
        zip_path=workspace + "/EXCH-0001__candidates_to_ai.zip",
        prompt_path=workspace + "/EXCH-0001/EXTERNAL_AI_TASK.md",
        manifest_path=workspace + "/EXCH-0001/EXCHANGE_MANIFEST.json",
    )
    folder.click()
    _assert(_FakeApplication.clipboard().text == workspace, "clipboard is not exact workspace path")
    _assert(output.text == workspace, "visible output is not exact workspace path")
    _assert("EXCH-0001" not in output.text, "exchange detail leaked into folder output")
    print("MAIN_WORKBENCH_SEND_STATE_MIRROR_RUNTIME: PASS")
    print("MISSING_PACKAGE_RESULT_VISIBLE_RUNTIME: PASS")
    print("MAIN_WORKBENCH_WORKSPACE_PATH_CLIPBOARD_RUNTIME: PASS")
    print("MAIN_WORKBENCH_WORKSPACE_PATH_VISIBLE_RUNTIME: PASS")


def _validate_patch_identity(project_root: Path, patch_zip: Path) -> None:
    _assert(patch_zip.is_file(), "patch ZIP missing")
    with zipfile.ZipFile(patch_zip, "r") as archive:
        manifest = json.loads(archive.read("PATCH_CONTENT_MANIFEST.json"))
        _assert(manifest.get("feature_id") == FEATURE_ID, "feature_id mismatch")
        _assert(manifest.get("patch_name") == PATCH_NAME, "patch_name mismatch")
        paths = {item.get("path") for item in manifest.get("files", [])}
        _assert(HELPER_RELATIVE.as_posix() in paths, "helper missing from manifest")
        _assert(VALIDATOR_RELATIVE.as_posix() in paths, "validator missing from manifest")
        for relative in (HELPER_RELATIVE, VALIDATOR_RELATIVE):
            installed = (project_root / relative).read_bytes()
            packaged = archive.read("payload/" + relative.as_posix())
            _assert(installed == packaged, "packaged payload mismatch: " + relative.as_posix())
    print("PATCH_FEATURE_IDENTITY: PASS")
    print("PATCH_PAYLOAD_SOURCE_IDENTITY: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    try:
        _validate_static(project_root)
        _validate_runtime(project_root)
        _validate_patch_identity(project_root, patch_zip)
    except Exception as error:
        print("VALIDATION FAILED: " + type(error).__name__ + ": " + str(error))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
