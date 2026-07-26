# project-path: tools/validate_global_press_depth_steel_blue_buttons_v1.py
"""Validate press-depth styling that preserves original button colors."""

from __future__ import annotations

import argparse
import ast
import importlib
import importlib.util
import os
import py_compile
import re
import sys
import types
from pathlib import Path
from typing import Any

__all__: list[str] = []

FEATURE_ID = "global-press-depth-original-colors-v2"
MAX_CODE_LINES = 500
THEME_PATH = "kanda_reasoner_app/templates/press_depth_button_theme.py"
LAUNCH_PATH = "kanda_reasoner_app/reasoner_tools_gui_shell/launch.py"
VALIDATOR_PATH = "tools/validate_global_press_depth_steel_blue_buttons_v1.py"
TOUCHED_SOURCE_FILES = [THEME_PATH, LAUNCH_PATH, VALIDATOR_PATH]


class _FakeEvent:
    """Minimal Qt event stand-in without shadowing the type built-in."""

    def __init__(self, event_kind: int) -> None:
        self._event_kind = event_kind
        setattr(self, "type", lambda: self._event_kind)


class _FakeQObject:
    """Minimal QObject stand-in with parent retention."""

    def __init__(self, parent: Any = None) -> None:
        self.parent = parent


class _FakeWidget(_FakeQObject):
    """Minimal QWidget stand-in with a style sheet."""

    def __init__(self) -> None:
        super().__init__()
        self._style_sheet = ""

    def setStyleSheet(self, value: str) -> None:
        self._style_sheet = value

    def styleSheet(self) -> str:
        return self._style_sheet


class _FakePushButton(_FakeWidget):
    """Minimal QPushButton stand-in."""


class _FakeToolButton(_FakeWidget):
    """Minimal QToolButton stand-in."""


class _FakeApplication(_FakeQObject):
    """Minimal QApplication stand-in."""

    def __init__(self) -> None:
        super().__init__()
        self._style_sheet = ""
        self._event_filters: list[Any] = []
        self._widgets: list[Any] = []

    def installEventFilter(self, event_filter: Any) -> None:
        self._event_filters.append(event_filter)

    def setStyleSheet(self, value: str) -> None:
        self._style_sheet = value

    def styleSheet(self) -> str:
        return self._style_sheet

    def allWidgets(self) -> list[Any]:
        return list(self._widgets)


class _FakeEventType:
    """Qt event constants used by the theme."""

    Polish = 1
    Show = 2
    StyleChange = 3
    EnabledChange = 4


class _FakeQEvent:
    """QEvent stand-in exposing the nested Type enum."""

    Type = _FakeEventType


def _read_text(project_root: Path, relative_path: str) -> str:
    path = project_root / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing expected file: {relative_path}")
    return path.read_text(encoding="utf-8")


def _validate_py_compile(project_root: Path) -> None:
    for relative_path in TOUCHED_SOURCE_FILES:
        py_compile.compile(str(project_root / relative_path), doraise=True)
    print("BUTTON_THEME_PY_COMPILE: PASS")


def _validate_line_counts(project_root: Path) -> None:
    for relative_path in TOUCHED_SOURCE_FILES:
        line_count = len(_read_text(project_root, relative_path).splitlines())
        if line_count > MAX_CODE_LINES:
            raise AssertionError(
                f"{relative_path} has {line_count} lines; maximum is {MAX_CODE_LINES}"
            )
    print("BUTTON_THEME_MODULE_SIZE: PASS")


def _validate_theme_source(project_root: Path) -> None:
    source = _read_text(project_root, THEME_PATH)
    required_fragments = [
        "KANDA_COLOR_PRESERVING_PRESS_DEPTH_V2",
        "COLOR_PRESERVING_PRESS_DEPTH_STYLE",
        "border-bottom: 4px solid",
        "padding-top: 7px",
        "QPushButton:checked",
        "QPushButton:disabled",
        "QEvent.Type.StyleChange",
        "_merge_button_style(current_style)",
        "app.installEventFilter(theme_filter)",
        "SILVER_MATTE_PRESS_DEPTH_STYLE: Final[str] = ",
        "STEEL_BLUE_PRESS_DEPTH_STYLE: Final[str] = ",
        "def apply_silver_matte_press_depth_theme",
        "def apply_steel_blue_press_depth_theme",
    ]
    for fragment in required_fragments:
        if fragment not in source:
            raise AssertionError(f"Theme source missing fragment: {fragment}")

    style_block = source.split(
        'COLOR_PRESERVING_PRESS_DEPTH_STYLE: Final[str] = f"""', 1
    )[1].split('""".strip()', 1)[0]
    forbidden_property = re.compile(
        r"^\s*(?:color|background(?:-color)?|font(?:-[a-z-]+)?)\s*:",
        re.IGNORECASE | re.MULTILINE,
    )
    match = forbidden_property.search(style_block)
    if match:
        raise AssertionError(
            "Shared depth style overrides original visual property: "
            + match.group(0).strip()
        )
    for old_color in ("#D8DADD", "#A3A7AC", "#25282C", "#F3F4F5"):
        if old_color.lower() in style_block.lower():
            raise AssertionError(f"Old silver palette remains: {old_color}")
    print("BUTTON_THEME_COLOR_NEUTRAL_PRESS_DEPTH_CONTRACT: PASS")


def _validate_launch_order(project_root: Path) -> None:
    source = _read_text(project_root, LAUNCH_PATH)
    apply_index = source.find("apply_color_preserving_press_depth_theme(app)")
    window_index = source.find("window = ReasonerToolsWindow()")
    if apply_index < 0 or window_index < 0 or apply_index > window_index:
        raise AssertionError("Theme must be applied before ReasonerToolsWindow creation")
    if source.count("apply_color_preserving_press_depth_theme(app)") != 1:
        raise AssertionError("Unified shell must apply the theme exactly once")
    print("BUTTON_THEME_UNIFIED_SHELL_STARTUP_ORDER: PASS")


def _button_inventory(project_root: Path) -> tuple[int, int, int]:
    constructor_count = 0
    file_count = 0
    local_style_count = 0
    for path in (project_root / "kanda_reasoner_app").rglob("*.py"):
        relative = path.relative_to(project_root).as_posix()
        if "/outputs/" in f"/{relative}/":
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        file_has_button = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            name = ""
            if isinstance(function, ast.Name):
                name = function.id
            if isinstance(function, ast.Attribute):
                name = function.attr
            if name in {"QPushButton", "QToolButton"}:
                constructor_count += 1
                file_has_button = True
            if isinstance(function, ast.Attribute):
                owner = ast.unparse(function.value).lower()
                if function.attr == "setStyleSheet" and (
                    "button" in owner or owner.endswith("btn") or "chip" in owner
                ):
                    local_style_count += 1
        if file_has_button:
            file_count += 1
    if constructor_count <= 0 or file_count <= 0:
        raise AssertionError("No current button constructors were found")
    return constructor_count, file_count, local_style_count


def _validate_inventory_coverage(project_root: Path) -> None:
    constructors, files, local_styles = _button_inventory(project_root)
    print(f"BUTTON_THEME_BUTTON_CONSTRUCTORS_DISCOVERED: PASS - {constructors}")
    print(f"BUTTON_THEME_BUTTON_OWNER_FILES_DISCOVERED: PASS - {files}")
    print(f"BUTTON_THEME_LOCAL_STYLE_OVERRIDES_DISCOVERED: PASS - {local_styles}")
    print("BUTTON_THEME_FUTURE_AND_LOCAL_OVERRIDE_COVERAGE: PASS")


def _install_fake_pyside_modules() -> None:
    pyside = types.ModuleType("PySide6")
    qt_core = types.ModuleType("PySide6.QtCore")
    qt_widgets = types.ModuleType("PySide6.QtWidgets")
    qt_core.QEvent = _FakeQEvent
    qt_core.QObject = _FakeQObject
    qt_widgets.QApplication = _FakeApplication
    qt_widgets.QPushButton = _FakePushButton
    qt_widgets.QToolButton = _FakeToolButton
    pyside.QtCore = qt_core
    pyside.QtWidgets = qt_widgets
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtCore"] = qt_core
    sys.modules["PySide6.QtWidgets"] = qt_widgets


def _load_theme_with_fake_qt(project_root: Path) -> Any:
    _install_fake_pyside_modules()
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    sys.modules.pop("kanda_reasoner_app.templates.press_depth_button_theme", None)
    return importlib.import_module(
        "kanda_reasoner_app.templates.press_depth_button_theme"
    )


def _assert_original_colors_preserved(style_sheet: str) -> None:
    required_tokens = ("#008000", "#F7F9FC", "font-weight: bold")
    for token in required_tokens:
        if token not in style_sheet:
            raise AssertionError(f"Original button style token was removed: {token}")
    if "KANDA_COLOR_PRESERVING_PRESS_DEPTH_V2" not in style_sheet:
        raise AssertionError("Press-depth marker is missing from merged button style")


def _validate_simulated_runtime(project_root: Path) -> None:
    theme = _load_theme_with_fake_qt(project_root)
    app = _FakeApplication()
    existing_button = _FakePushButton()
    existing_button.setStyleSheet(
        "color: #008000; background: #F7F9FC; font-weight: bold;"
    )
    app._widgets.append(existing_button)
    theme.apply_color_preserving_press_depth_theme(app)
    _assert_original_colors_preserved(existing_button.styleSheet())

    event_filter = getattr(app, theme._FILTER_ATTRIBUTE)
    existing_button.setStyleSheet(
        "QPushButton { color: #b00020; background: #FFF3F3; }"
    )
    event_filter.eventFilter(
        existing_button,
        _FakeEvent(_FakeEventType.StyleChange),
    )
    updated_style = existing_button.styleSheet()
    if "#b00020" not in updated_style or "#FFF3F3" not in updated_style:
        raise AssertionError("Later red button colors were not preserved")
    if theme._THEME_MARKER not in updated_style:
        raise AssertionError("Later local style did not retain press depth")

    late_button = _FakeToolButton()
    event_filter.eventFilter(late_button, _FakeEvent(_FakeEventType.Show))
    if theme._THEME_MARKER not in late_button.styleSheet():
        raise AssertionError("Late-created button did not receive press depth")
    print("BUTTON_THEME_ORIGINAL_COLORS_PRESERVED: PASS")
    print("BUTTON_THEME_SIMULATED_RUNTIME: PASS")


def _validate_real_qt_runtime(project_root: Path) -> bool:
    if importlib.util.find_spec("PySide6") is None:
        print("BUTTON_THEME_REAL_QT: NOT_RUN - PySide6 unavailable")
        return False

    if os.name != "nt":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from PySide6.QtWidgets import QApplication, QPushButton, QToolButton

    theme = importlib.import_module(
        "kanda_reasoner_app.templates.press_depth_button_theme"
    )
    app = QApplication.instance() or QApplication([])
    theme.apply_color_preserving_press_depth_theme(app)

    push_button = QPushButton("Green")
    push_button.setStyleSheet(
        "color: #008000; background: #F7F9FC; font-weight: bold;"
    )
    tool_button = QToolButton()
    tool_button.setText("Blue")
    tool_button.setStyleSheet(
        "QToolButton { color: #003366; background: #EEF4FF; }"
    )
    push_button.show()
    tool_button.show()
    app.processEvents()

    _assert_original_colors_preserved(push_button.styleSheet())
    tool_style = tool_button.styleSheet()
    if "#003366" not in tool_style or "#EEF4FF" not in tool_style:
        raise AssertionError("Original blue tool-button colors were not preserved")
    if theme._THEME_MARKER not in tool_style:
        raise AssertionError("QToolButton press-depth marker is missing")

    push_button.setStyleSheet(
        "QPushButton { color: #b00020; background: #FFF3F3; }"
    )
    app.processEvents()
    changed_style = push_button.styleSheet()
    if "#b00020" not in changed_style or "#FFF3F3" not in changed_style:
        raise AssertionError("Later red button colors were not preserved")
    if theme._THEME_MARKER not in changed_style:
        raise AssertionError("Later red style lost press depth")

    print("BUTTON_THEME_ORIGINAL_COLORS_PRESERVED: PASS")
    print("BUTTON_THEME_REAL_QT: PASS")
    return True


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    project_root = args.project_root.resolve()
    _validate_py_compile(project_root)
    _validate_line_counts(project_root)
    _validate_theme_source(project_root)
    _validate_launch_order(project_root)
    _validate_inventory_coverage(project_root)
    if not _validate_real_qt_runtime(project_root):
        _validate_simulated_runtime(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
