"""Validate Main Workbench refactoring path clipboard correction."""
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

__all__ = [
    "main",
]

FEATURE_ID = "planner-main-workbench-refactoring-path-clipboard-v1"
LESSON_ID = "lesson-main-workbench-refactoring-folder-wrong-owner-v1"
GUI_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "gui_shell.py"
)
HELPER_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_refactoring_folder_button.py"
)
NEW_IMPORT = (
    "from .main_workbench_refactoring_folder_button import "
    "build_main_workbench_controls"
)
OLD_IMPORT = "from .main_workbench_gui import build_main_workbench_controls"
VALIDATOR_RELATIVE = Path(
    "tools/validate_planner_main_workbench_refactoring_path_clipboard_v1.py"
)
LEGACY_VALIDATOR_RELATIVE = Path(
    "tools/validate_planner_main_workbench_refactoring_folder_button_v1.py"
)
ERROR_MEMORY_MEMBER = (
    "KANDA_ERROR_LESSON_JSON_main-workbench-refactoring-folder-wrong-owner-v1.txt"
)
EXPECTED_MEMBERS = {
    "KANDA_FREEZE_HINT.json",
    ERROR_MEMORY_MEMBER,
    HELPER_RELATIVE.as_posix(),
    VALIDATOR_RELATIVE.as_posix(),
    LEGACY_VALIDATOR_RELATIVE.as_posix(),
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_static(project_root: Path) -> None:
    gui_path = project_root / GUI_RELATIVE
    helper_path = project_root / HELPER_RELATIVE
    _assert(gui_path.is_file(), "gui_shell.py missing")
    _assert(helper_path.is_file(), "composition helper missing")
    gui_text = gui_path.read_text(encoding="utf-8")
    helper_text = helper_path.read_text(encoding="utf-8")
    _assert(gui_text.count(NEW_IMPORT) == 1, "GUI adapter import not unique")
    _assert(OLD_IMPORT not in gui_text, "legacy direct GUI builder import remains")
    _assert(
        gui_text.count(
            "layout.addWidget(build_main_workbench_controls(window))"
        )
        == 1,
        "Main Workbench insertion call changed",
    )
    helper_lines = len(helper_text.splitlines())
    _assert(101 <= helper_lines <= 499, "helper violates 101-499 line law")
    ast.parse(gui_text, filename=str(gui_path))
    tree = ast.parse(helper_text, filename=str(helper_path))
    functions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    required = {
        "build_main_workbench_controls",
        "_copy_main_workbench_artifact_paths",
        "_result_paths",
        "_format_clipboard_paths",
        "_shared_button_layout",
    }
    _assert(required <= functions, "required path-copy functions missing")
    _assert(
        "_large_file_refactor_main_workbench_package_result" in helper_text,
        "Main Workbench package-result owner missing",
    )
    _assert(
        "QApplication.clipboard().setText(clipboard_text)" in helper_text,
        "clipboard write missing",
    )
    _assert("WORKSPACE FOLDER:" in helper_text, "workspace label missing")
    _assert("CURRENT EXCHANGE FOLDER:" in helper_text, "exchange label missing")
    _assert('"ZIP:"' in helper_text, "ZIP label missing")
    _assert("INSTRUCTION FILE:" in helper_text, "instruction label missing")
    _assert('"MANIFEST:"' in helper_text, "manifest label missing")
    _assert(
        "original_button.click()" not in helper_text,
        "legacy folder-opening delegation remains",
    )
    _assert(
        "_large_file_refactor_workbench_ai_exchange_folder_button" not in helper_text,
        "legacy external-exchange owner remains",
    )
    print("GUI_SHELL_MAIN_WORKBENCH_ADAPTER_BINDING: PASS")
    print("MAIN_WORKBENCH_PACKAGE_RESULT_OWNER_STATIC: PASS")
    print("LEGACY_FOLDER_DELEGATION_REMOVED_STATIC: PASS")
    print("CLIPBOARD_PATH_PAYLOAD_STATIC: PASS")
    print("TOUCHED_SOURCE_MODULE_LINE_LAW_101_499: PASS")


class _FakeEvent:
    def __init__(self, event_type: int) -> None:
        self._event_type = event_type

    def _qt_event_type(self) -> int:
        return self._event_type

setattr(_FakeEvent, "type", _FakeEvent._qt_event_type)



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
        self.object_name = ""
        self.tooltip = ""

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
        self._widget = widget
        self._layout = layout

    def layout(self) -> Any:
        return self._layout


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
            if item._widget is widget:
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
                if isinstance(item._widget, cls):
                    found.append(item._widget)
                if item._layout is not None:
                    visit(item._layout)

        visit(self._layout)
        return found


def _load_helper_with_fakes(project_root: Path):
    package_name = (
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    )
    qtcore = types.ModuleType("PySide6.QtCore")
    qtcore.QEvent = _FakeQEvent
    qtcore.QObject = _FakeQObject
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtwidgets.QApplication = _FakeApplication
    qtwidgets.QLayout = _FakeLayout
    qtwidgets.QPushButton = _FakeButton
    qtwidgets.QWidget = _FakeWidget
    pyside = types.ModuleType("PySide6")
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets

    original_module_name = package_name + ".main_workbench_gui"
    original_module = types.ModuleType(original_module_name)

    def original_builder(window: Any) -> _FakeWidget:
        root_layout = _FakeLayout()
        row = _FakeLayout()
        cancel = _FakeButton("Cancel Main Workbench")
        send = _FakeButton("Send Complete Project to Web AI")
        send.setEnabled(False)
        row.addWidget(cancel)
        row.addWidget(send)
        root_layout.addLayout(row)
        return _FakeWidget(root_layout)

    original_module.build_main_workbench_controls = original_builder
    sys.modules[original_module_name] = original_module

    helper_name = package_name + ".main_workbench_refactoring_folder_button"
    helper_path = project_root / HELPER_RELATIVE
    spec = importlib.util.spec_from_file_location(helper_name, helper_path)
    _assert(spec is not None and spec.loader is not None, "helper spec unavailable")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package_name
    sys.modules[helper_name] = module
    spec.loader.exec_module(module)
    return module


def _button_by_text(root: _FakeWidget, text: str) -> _FakeButton:
    matches = [
        button
        for button in root.findChildren(_FakeButton)
        if button.text() == text
    ]
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
    row = root.layout().itemAt(0).layout()
    labels = [item._widget.text() for item in row.items]
    _assert(
        labels == [
            "Cancel Main Workbench",
            "Refactoring Folder",
            "Send Complete Project to Web AI",
        ],
        "Plan Action button order changed: " + repr(labels),
    )
    duplicate = _button_by_text(root, "Refactoring Folder")
    send = _button_by_text(root, "Send Complete Project to Web AI")
    _assert(not duplicate.isEnabled(), "path button did not mirror disabled send state")
    send.setEnabled(True)
    _assert(duplicate.isEnabled(), "path button did not mirror enabled send state")

    duplicate.click()
    _assert(
        output.text.startswith("REFACTORING PATHS NOT READY"),
        "missing package result was not explained",
    )
    _assert(_FakeApplication.clipboard().text == "", "clipboard changed without result")

    window._large_file_refactor_main_workbench_package_result = types.SimpleNamespace(
        workspace_root="E:/support/workspace",
        exchange_root="E:/support/workspace/EXCH-0007",
        zip_path="E:/support/workspace/EXCH-0007__candidates_to_ai.zip",
        prompt_path="E:/support/workspace/EXCH-0007/EXTERNAL_AI_TASK.md",
        manifest_path="E:/support/workspace/EXCH-0007/EXCHANGE_MANIFEST.json",
    )
    duplicate.click()
    copied = _FakeApplication.clipboard().text
    for expected in (
        "MAIN WORKBENCH REFACTORING PATHS",
        "E:/support/workspace",
        "E:/support/workspace/EXCH-0007",
        "E:/support/workspace/EXCH-0007__candidates_to_ai.zip",
        "E:/support/workspace/EXCH-0007/EXTERNAL_AI_TASK.md",
        "E:/support/workspace/EXCH-0007/EXCHANGE_MANIFEST.json",
    ):
        _assert(expected in copied, "clipboard payload missing: " + expected)
    _assert(
        output.text == "MAIN WORKBENCH REFACTORING PATHS COPIED\n\n" + copied,
        "visible output does not match clipboard payload",
    )
    send.setEnabled(False)
    _assert(not duplicate.isEnabled(), "path button did not mirror running state")
    module.build_main_workbench_controls(window)
    print("PLAN_ACTION_BUTTON_ORDER_RUNTIME: PASS")
    print("MAIN_WORKBENCH_SEND_STATE_MIRROR_RUNTIME: PASS")
    print("MISSING_PACKAGE_RESULT_VISIBLE_RUNTIME: PASS")
    print("MAIN_WORKBENCH_PATHS_CLIPBOARD_RUNTIME: PASS")


def _extract_lesson_payload(text: str) -> dict[str, Any]:
    begin = "KANDA_ERROR_LESSON_JSON_BEGIN"
    end = "KANDA_ERROR_LESSON_JSON_END"
    _assert(text.count(begin) == 1 and text.count(end) == 1, "lesson markers invalid")
    payload_text = text.split(begin, 1)[1].split(end, 1)[0].strip()
    payload = json.loads(payload_text)
    _assert(isinstance(payload, dict), "lesson payload is not an object")
    return payload


def _validate_patch_zip(project_root: Path, patch_zip: Path) -> None:
    _assert(patch_zip.is_file(), "patch ZIP missing")
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = {
            info.filename
            for info in archive.infolist()
            if not info.is_dir()
        }
        _assert(
            names == EXPECTED_MEMBERS,
            "patch ZIP members changed: " + repr(sorted(names)),
        )
        for relative in (
            HELPER_RELATIVE,
            VALIDATOR_RELATIVE,
            LEGACY_VALIDATOR_RELATIVE,
        ):
            installed = (project_root / relative).read_bytes()
            packaged = archive.read(relative.as_posix())
            _assert(
                installed == packaged,
                "packaged source mismatch: " + relative.as_posix(),
            )
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
        _assert(hint.get("feature_id") == FEATURE_ID, "freeze hint feature mismatch")
        lesson_text = archive.read(ERROR_MEMORY_MEMBER).decode("utf-8")
        lesson = _extract_lesson_payload(lesson_text)
        _assert(lesson.get("lesson_id") == LESSON_ID, "Error Memory lesson mismatch")
        _assert(lesson.get("status") == "draft", "pre-local lesson must remain draft")
    print("PATCH_ZIP_EXACT_MEMBER_CONTRACT: PASS")
    print("PATCH_ZIP_SOURCE_IDENTITY: PASS")
    print("FREEZE_HINT_FEATURE_BINDING: PASS")
    print("ERROR_MEMORY_DRAFT_INTAKE_BINDING: PASS")


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
        _validate_patch_zip(project_root, patch_zip)
    except Exception as error:
        print("VALIDATION FAILED: " + type(error).__name__ + ": " + str(error))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
