# project-path: tools/validate_show_project_tool_project_prompt_button_v1r3.py
"""Validate the live-window-preserving Tool x Project clipboard button."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import py_compile
import sys
import types
from pathlib import Path

FEATURE_ID = "show-project-tool-project-prompt-copy-button-v1r3"
INIT_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/__init__.py"
)
WINDOW_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "project_tool_boundary_prompt_button_private_impl.py"
)
HELP_MANIFEST_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help.json"
)
ROUTING_REL = Path(
    "kanda_prompt_workspace/prompt_library/ROUTING/"
    "prompt_navigation_index.json"
)
CANON_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/project_tool_boundary_canon.md"
)


def gate(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def read(root: Path, relative: Path) -> str:
    path = root / relative
    if not path.is_file():
        raise AssertionError("Missing file: " + str(relative))
    return path.read_text(encoding="utf-8-sig")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_initializer(root: Path) -> None:
    text = read(root, INIT_REL)
    required = (
        "def _install_tool_project_button_wrapper()",
        "from . import window_methods_private_impl as _window_methods",
        "from . import project_tool_boundary_prompt_button_private_impl as _button",
        "result = original(window)",
        "_button.install_control(window)",
        "_window_methods._build_ui = _build_ui_with_tool_project_button",
        "_install_tool_project_button_wrapper()",
    )
    for marker in required:
        gate("TOOL_PROJECT_INITIALIZER_MARKER " + marker, marker in text)
    gate(
        "TOOL_PROJECT_LIVE_WINDOW_OWNER_NOT_REPLACED",
        "project_root_row.addWidget" not in text,
    )


def validate_window_owner(root: Path) -> None:
    text = read(root, WINDOW_REL)
    required = (
        "def _build_ui(self)",
        'self.copy_machine_card_logic_button = QPushButton("Logic")',
        "project_root_row.addWidget(self.copy_machine_card_logic_button)",
        "collector_layout.addLayout(project_root_row)",
    )
    for marker in required:
        gate("LIVE_WINDOW_OWNER_MARKER " + marker, marker in text)
    gate(
        "LIVE_WINDOW_OWNER_DIRECT_TOOL_PROJECT_PATCH_ABSENT",
        "project_tool_boundary_prompt_button_private_impl" not in text,
    )


def validate_helper(root: Path) -> None:
    text = read(root, HELPER_REL)
    required = (
        'QPushButton("Tool x Project")',
        'QColor("#ff4d00")',
        "font.setBold(True)",
        "row = QHBoxLayout()",
        "row.addStretch(1)",
        "collector_layout.insertLayout(1, row)",
        "copy_project_tool_boundary_to_clipboard(window)",
        "Path(__file__).resolve().parents[3]",
    )
    for marker in required:
        gate("TOOL_PROJECT_HELPER_MARKER " + marker, marker in text)
    forbidden = (
        "setMinimumWidth",
        "setMaximumWidth",
        "setFixedWidth",
        "resize(",
        "setGeometry(",
        "project_root_edit",
    )
    for marker in forbidden:
        gate("GUI_WIDTH_AND_PROJECT_AUTHORITY_ABSENT " + marker, marker not in text)
    gate(
        "TOOL_PROJECT_BUTTON_SEPARATE_ROW_NO_WIDTH_CHANGE",
        "collector_layout.insertLayout(1, row)" in text,
    )


def validate_canonical_prompt(root: Path) -> None:
    text = read(root, CANON_REL)
    required = (
        "Prompt ID: project_tool_boundary_canon",
        "Prompt code: KPR-12-001",
        "## Explicit code-placement and cross-write rule",
        "Never write KANDA Tool code into an external selected Project source tree.",
        "Never write external selected-Project code into KANDA Tool source.",
        "### Project Support handoff exception",
        "<project_name>_show_project_to_AI",
        "### KANDA Reasoner self-hosting exception",
    )
    for marker in required:
        gate("LIVE_CANONICAL_PROMPT_MARKER " + marker, marker in text)
    print("LIVE_CANONICAL_PROMPT_STRUCTURAL_CONTRACT: PASS")


def validate_wrapper(root: Path) -> None:
    module_name = (
        "kanda_reasoner_app.reasoner_tools_shell.runner_help."
        "project_tool_boundary_prompt_button_private_impl"
    )
    helper = importlib.import_module(module_name)
    wrapper = helper.build_project_tool_boundary_wrapper()
    canon = read(root, CANON_REL).rstrip()
    gate("TOOL_PROJECT_WRAPPER_EXACT_CANON", canon in wrapper)
    gate(
        "TOOL_PROJECT_WRAPPER_MARKERS",
        wrapper.count("KANDA_PROJECT_TOOL_BOUNDARY_BEGIN") == 1
        and wrapper.count("KANDA_PROJECT_TOOL_BOUNDARY_END") == 1,
    )


class _Signal:
    def __init__(self) -> None:
        self.callback = None

    def connect(self, callback) -> None:
        self.callback = callback

    def emit(self) -> None:
        if self.callback is not None:
            self.callback()


class _Palette:
    ButtonText = 1

    def __init__(self) -> None:
        self.values = {}

    def setColor(self, role, color) -> None:
        self.values[role] = color


class _Font:
    def __init__(self) -> None:
        self.bold = False

    def setBold(self, value: bool) -> None:
        self.bold = bool(value)


class _Button:
    def __init__(self, text: str) -> None:
        self._text = text
        self._palette = _Palette()
        self._font = _Font()
        self.tooltip = ""
        self.clicked = _Signal()

    def text(self) -> str:
        return self._text

    def palette(self):
        return self._palette

    def setPalette(self, palette) -> None:
        self._palette = palette

    def font(self):
        return self._font

    def setFont(self, font) -> None:
        self._font = font

    def setToolTip(self, text: str) -> None:
        self.tooltip = text

    def click(self) -> None:
        self.clicked.emit()


class _Row:
    def __init__(self) -> None:
        self.items = []

    def addStretch(self, value: int) -> None:
        self.items.append(("stretch", value))

    def addWidget(self, widget) -> None:
        self.items.append(("widget", widget))


class _Layout:
    def __init__(self) -> None:
        self.insertions = []

    def insertLayout(self, index: int, row) -> None:
        self.insertions.append((index, row))


class _Tab:
    def __init__(self, layout) -> None:
        self._layout = layout

    def layout(self):
        return self._layout


class _Tabs:
    def __init__(self, tab) -> None:
        self._tab = tab

    def count(self) -> int:
        return 1

    def widget(self, index: int):
        return self._tab if index == 0 else None


class _Clipboard:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, text: str) -> None:
        self.text = text


class _Application:
    clipboard_owner = _Clipboard()

    @classmethod
    def clipboard(cls):
        return cls.clipboard_owner


class _Color:
    def __init__(self, value: str) -> None:
        self.value = value


def install_fake_qt() -> None:
    pyside = types.ModuleType("PySide6")
    qtgui = types.ModuleType("PySide6.QtGui")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtgui.QColor = _Color
    qtgui.QPalette = _Palette
    qtwidgets.QHBoxLayout = _Row
    qtwidgets.QPushButton = _Button
    qtwidgets.QApplication = _Application
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtGui"] = qtgui
    sys.modules["PySide6.QtWidgets"] = qtwidgets


def validate_runtime(root: Path) -> None:
    install_fake_qt()
    package_name = "kanda_reasoner_app.reasoner_tools_shell.runner_help"
    window_name = package_name + ".window_methods_private_impl"
    helper_name = package_name + ".project_tool_boundary_prompt_button_private_impl"
    for name in (package_name, window_name, helper_name):
        sys.modules.pop(name, None)

    package = importlib.import_module(package_name)
    window_module = importlib.import_module(window_name)
    helper = importlib.import_module(helper_name)
    gate(
        "TOOL_PROJECT_RUNTIME_WRAPPER_INSTALLED",
        getattr(window_module._build_ui, "_kanda_tool_project_button_wrapped", False),
    )

    layout = _Layout()

    class Status:
        def __init__(self) -> None:
            self.value = ""

        def setText(self, value: str) -> None:
            self.value = value

    class Window:
        def __init__(self) -> None:
            self.tabs = _Tabs(_Tab(layout))
            self.first_prompt_status_label = Status()
            self.logged = []
            self.width_sentinel = 777

        def _append_log(self, message: str) -> None:
            self.logged.append(message)

    window = Window()
    helper.install_control(window)
    gate("TOOL_PROJECT_RUNTIME_SECOND_ROW", layout.insertions[0][0] == 1)
    gate(
        "TOOL_PROJECT_RUNTIME_BUTTON_TEXT",
        window.copy_project_tool_boundary_button.text() == "Tool x Project",
    )
    gate(
        "TOOL_PROJECT_RUNTIME_NO_WINDOW_WIDTH_MUTATION",
        window.width_sentinel == 777,
    )
    gate(
        "TOOL_PROJECT_RUNTIME_ORANGE_BOLD",
        window.copy_project_tool_boundary_button.font().bold
        and window.copy_project_tool_boundary_button.palette().values[
            _Palette.ButtonText
        ].value == "#ff4d00",
    )
    window.copy_project_tool_boundary_button.click()
    gate(
        "TOOL_PROJECT_RUNTIME_CLIPBOARD",
        "Prompt code: KPR-12-001" in _Application.clipboard_owner.text,
    )
    gate(
        "TOOL_PROJECT_RUNTIME_STATUS",
        "Copied Tool x Project boundary prompt"
        in window.first_prompt_status_label.value,
    )
    helper.install_control(window)
    gate("TOOL_PROJECT_RUNTIME_IDEMPOTENT_CONTROL", len(layout.insertions) == 1)
    print("TOOL_PROJECT_GUI_RUNTIME: PASS")


def validate_routing_index(root: Path) -> None:
    data = json.loads(read(root, ROUTING_REL))
    entries = data.get("entries") if isinstance(data, dict) else None
    gate("ROUTING_INDEX_ENTRIES_LIST", isinstance(entries, list))
    expected = {
        "project_tool_boundary_canon": (
            "KPR-12-001",
            "ACTIVE_PROMPTS/12_generalized_project_canons/"
            "project_tool_boundary_canon.md",
        ),
        "project_tool_boundary_startup_bridge": (
            "KPR-12-006",
            "ACTIVE_PROMPTS/12_generalized_project_canons/"
            "project_tool_boundary_startup_bridge.md",
        ),
    }
    for prompt_id, (prompt_code, relative_path) in expected.items():
        matches = [
            item
            for item in entries
            if isinstance(item, dict)
            and item.get("prompt_id") == prompt_id
            and item.get("prompt_code") == prompt_code
            and item.get("relative_path") == relative_path
        ]
        gate("ROUTING_INDEX_REGISTRATION " + prompt_id, len(matches) == 1)
    print("ROUTING_INDEX_STRUCTURAL_REGISTRATION: PASS")


def validate_package_scripts(package_root: Path) -> None:
    names = (
        "RUN_INSTALL.ps1",
        "INSTALL.ps1",
        "RUN_VALIDATE.ps1",
        "VALIDATE.ps1",
        "PREPARE_FREEZE.ps1",
        "NATIVE_PROCESS.ps1",
    )
    for name in names:
        path = package_root / name
        gate("POWERSHELL_SCRIPT_PRESENT " + name, path.is_file())
        raw = path.read_bytes()
        forbidden = [byte for byte in raw if byte < 32 and byte not in (9, 10, 13)]
        gate("POWERSHELL_CONTROL_CHARACTERS_ABSENT " + name, not forbidden)
    validate = read(package_root, Path("VALIDATE.ps1"))
    required = (
        '$ToolsRoot = Join-Path $ProjectPath "tools"',
        '$FeatureValidator = Join-Path $ToolsRoot "validate_show_project_tool_project_prompt_button_v1r3.py"',
        '$ScriptsRoot = Join-Path $ProjectPath "scripts"',
        '$ZipValidator = Join-Path $ScriptsRoot "validate_patch_zip.py"',
    )
    for marker in required:
        gate("VALIDATOR_PATH_TOKEN " + marker, marker in validate)
    gate("VERTICAL_TAB_BYTE_ABSENT", b"\x0b" not in validate.encode("utf-8"))
    gate("CONCATENATED_TOOLSVALIDATE_PATH_ABSENT", "toolsvalidate_" not in validate)
    print("POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS")
    print("VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS")


def validate_sizes(root: Path) -> None:
    for relative in (INIT_REL, HELPER_REL):
        gate(
            "MODULE_SIZE_LE_500 " + str(relative),
            len(read(root, relative).splitlines()) <= 500,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--package-root", type=Path)
    args = parser.parse_args()
    root = args.project_root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    validate_initializer(root)
    validate_window_owner(root)
    validate_helper(root)
    validate_canonical_prompt(root)
    validate_wrapper(root)
    validate_runtime(root)
    validate_routing_index(root)
    if args.package_root is not None:
        validate_package_scripts(args.package_root.resolve())
    validate_sizes(root)
    py_compile.compile(str(root / INIT_REL), doraise=True)
    py_compile.compile(str(root / HELPER_REL), doraise=True)
    py_compile.compile(str(root / "tools" / Path(__file__).name), doraise=True)
    print("LIVE_WINDOW_OWNER_PRESERVED: PASS")
    print("LIVE_CANONICAL_PROMPT_PRESERVED: PASS")
    print("SHOW_PROJECT_TOOL_PROJECT_GUI_CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
