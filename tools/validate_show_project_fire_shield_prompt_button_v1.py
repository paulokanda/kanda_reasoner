# project-path: tools/validate_show_project_fire_shield_prompt_button_v1.py
"""Validate the surgical Show Project Fire Shield clipboard button."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import py_compile
import subprocess
import sys
import types
from pathlib import Path

FEATURE_ID = "show-project-fire-shield-prompt-copy-button-v1"
HELPER_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "project_tool_boundary_prompt_button_private_impl.py"
)
CANON_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/project_tool_boundary_canon.md"
)
OLD_VALIDATOR_REL = Path(
    "tools/validate_show_project_tool_project_prompt_button_v1r3.py"
)
AI_POLICY_VALIDATOR_REL = Path(
    "tools/validate_fire_shield_ai_policy_enforcement_v1.py"
)
EXPECTED_CANON_SHA256 = (
    "86bba659250680c844b70e2874938686d7c0f92ef81555161c3d2a80e14a80af"
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


def validate_source(root: Path) -> None:
    helper = read(root, HELPER_REL)
    canon_path = root / CANON_REL
    canon = read(root, CANON_REL)
    gate(
        "FIRE_SHIELD_BUTTON_CANON_HASH_PINNED",
        sha(canon_path) == EXPECTED_CANON_SHA256,
    )
    required = (
        '"key": "fire_shield"',
        '"label": "Fire Shield"',
        '"prompt_code": "KPR-12-001"',
        '"prompt_id": "project_tool_boundary_canon"',
        '"relative_path": _PROMPT_REL',
        '"## Explicit code-placement and cross-write rule"',
        '"## Fire Shield programmatic authority"',
    )
    for marker in required:
        gate("FIRE_SHIELD_BUTTON_HELPER_MARKER " + marker, marker in helper)
    gate(
        "FIRE_SHIELD_BUTTON_LEFT_OF_BRICK_WALL",
        helper.index('"key": "fire_shield"')
        < helper.index('"key": "brick_wall"'),
    )
    gate(
        "FIRE_SHIELD_BUTTON_NO_NEW_PROMPT_OWNER",
        "fire_shield_prompt.md" not in helper
        and "fire_shield_canon.md" not in helper,
    )
    canon_required = (
        "## Explicit code-placement and cross-write rule",
        "Never write KANDA Tool code into an external selected Project source tree.",
        "### KANDA Reasoner self-hosting exception",
        "## Fire Shield programmatic authority",
        "kanda_reasoner_app.project_fire_shield",
        "Path-string equality alone is never sufficient.",
    )
    for marker in canon_required:
        gate("FIRE_SHIELD_BUTTON_CANON_MARKER " + marker, marker in canon)
    gate("FIRE_SHIELD_BUTTON_HELPER_ASCII", helper.isascii())
    gate("FIRE_SHIELD_BUTTON_HELPER_MAX500", len(helper.splitlines()) <= 500)


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
    module_name = (
        "kanda_reasoner_app.reasoner_tools_shell.runner_help."
        "project_tool_boundary_prompt_button_private_impl"
    )
    sys.modules.pop(module_name, None)
    helper = importlib.import_module(module_name)
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
    row = layout.insertions[0][1]
    labels = [
        item[1].text()
        for item in row.items
        if item[0] == "widget"
    ]
    gate(
        "FIRE_SHIELD_BUTTON_RUNTIME_LEFT_OF_BRICK_WALL",
        labels.index("Fire Shield") + 1 == labels.index("Brick Wall"),
    )
    gate(
        "FIRE_SHIELD_BUTTON_RUNTIME_ATTRIBUTE",
        window.copy_fire_shield_button.text() == "Fire Shield",
    )
    gate(
        "FIRE_SHIELD_BUTTON_RUNTIME_ORANGE_BOLD",
        window.copy_fire_shield_button.font().bold
        and window.copy_fire_shield_button.palette().values[
            _Palette.ButtonText
        ].value == "#ff4d00",
    )
    gate(
        "FIRE_SHIELD_BUTTON_RUNTIME_NO_WIDTH_MUTATION",
        window.width_sentinel == 777,
    )
    window.copy_fire_shield_button.click()
    copied = _Application.clipboard_owner.text
    required = (
        "KANDA_FIRE_SHIELD_PROMPT_CONTEXT_BEGIN",
        "Prompt code: KPR-12-001",
        "Prompt id: project_tool_boundary_canon",
        "## Explicit code-placement and cross-write rule",
        "Never write KANDA Tool code into an external selected Project source tree.",
        "### KANDA Reasoner self-hosting exception",
        "## Fire Shield programmatic authority",
        "kanda_reasoner_app.project_fire_shield",
        "Path-string equality alone is never sufficient.",
        "KANDA_FIRE_SHIELD_PROMPT_CONTEXT_END",
    )
    for marker in required:
        gate("FIRE_SHIELD_BUTTON_CLIPBOARD_MARKER " + marker, marker in copied)
    gate(
        "FIRE_SHIELD_BUTTON_CLIPBOARD_BOUNDED",
        "## Portable-distribution ownership" not in copied,
    )
    gate(
        "FIRE_SHIELD_BUTTON_STATUS_FEEDBACK",
        "Copied Fire Shield prompt context"
        in window.first_prompt_status_label.value,
    )
    window.copy_brick_wall_button.click()
    gate(
        "FIRE_SHIELD_BUTTON_BRICK_WALL_NEIGHBOR_PRESERVED",
        "KANDA_BRICK_WALL_PROMPT_CONTEXT_BEGIN"
        in _Application.clipboard_owner.text,
    )
    helper.install_control(window)
    gate("FIRE_SHIELD_BUTTON_RUNTIME_IDEMPOTENT", len(layout.insertions) == 1)


def run_regression(root: Path, relative: Path, marker: str) -> None:
    path = root / relative
    gate(marker + "_PRESENT", path.is_file())
    result = subprocess.run(
        [sys.executable, str(path), str(root)]
        if relative == OLD_VALIDATOR_REL
        else [sys.executable, str(path), "--project-root", str(root)],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
    gate(marker, result.returncode == 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    validate_source(root)
    validate_runtime(root)
    py_compile.compile(str(root / HELPER_REL), doraise=True)
    py_compile.compile(str(root / Path(__file__).relative_to(root)), doraise=True)
    print("FIRE_SHIELD_BUTTON_COMPILE: PASS")
    run_regression(
        root,
        OLD_VALIDATOR_REL,
        "SHOW_PROJECT_TOOL_PROJECT_BUTTON_REGRESSION",
    )
    run_regression(
        root,
        AI_POLICY_VALIDATOR_REL,
        "FIRE_SHIELD_AI_POLICY_REGRESSION",
    )
    print("FIRE_SHIELD_BUTTON_NO_NEW_PROMPT_OWNER: PASS")
    print("SHOW_PROJECT_FIRE_SHIELD_PROMPT_BUTTON: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
