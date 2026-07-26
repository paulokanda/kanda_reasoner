# project-path: tools/validate_inner_tabs_template_v1.py
"""Validate the reusable inner-tabs template contract."""
from __future__ import annotations

__all__: list[str] = []

import importlib
import py_compile
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_CODE_LINES = 500
TOUCHED_SOURCE_FILES = [
    "kanda_reasoner_app/templates/__init__.py",
    "kanda_reasoner_app/templates/inner_tabs_template.py",
    "tools/validate_inner_tabs_template_v1.py",
]


class FakeSignal:
    """Small signal stand-in for testing click wiring without Qt."""

    def __init__(self) -> None:
        """Create an empty callback list."""
        self._callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        """Store a connected callback."""
        self._callbacks.append(callback)

    def emit(self) -> None:
        """Run connected callbacks."""
        for callback in self._callbacks:
            callback(False)


class FakeButton:
    """Small button stand-in for testing the inner-tab template."""

    def __init__(self, label: str) -> None:
        """Create a fake button with a label."""
        self.label = label
        self.clicked = FakeSignal()
        self.checked = False
        self.maximum_height = 0
        self.minimum_height = 0
        self.object_name = ""
        self.style_sheet = ""
        self.checkable = False

    def setCheckable(self, value: bool) -> None:
        """Store the checkable flag."""
        self.checkable = value

    def setChecked(self, value: bool) -> None:
        """Store the checked flag."""
        self.checked = value

    def setMaximumHeight(self, value: int) -> None:
        """Store maximum height."""
        self.maximum_height = value

    def setMinimumHeight(self, value: int) -> None:
        """Store minimum height."""
        self.minimum_height = value

    def setObjectName(self, value: str) -> None:
        """Store the object name."""
        self.object_name = value

    def setStyleSheet(self, value: str) -> None:
        """Store the style sheet."""
        self.style_sheet = value


class FakeLayout:
    """Small layout stand-in for testing row construction."""

    def __init__(self) -> None:
        """Create an empty layout record."""
        self.widgets: list[object] = []
        self.stretches: list[int] = []

    def addStretch(self, value: int) -> None:
        """Record a stretch value."""
        self.stretches.append(value)

    def addWidget(self, widget: object, stretch: int) -> None:
        """Record a widget and stretch value."""
        self.widgets.append((widget, stretch))


class FakeStack:
    """Small stack stand-in for testing current page selection."""

    def __init__(self) -> None:
        """Create a stack with no selected index."""
        self.current_index = -1

    def setCurrentIndex(self, value: int) -> None:
        """Store the active stack index."""
        self.current_index = value


def _read_project_text(relative_path: str) -> str:
    """Read one project file as UTF-8 text."""
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing expected file: {relative_path}")
    return path.read_text(encoding="utf-8")


def _line_count(text: str) -> int:
    """Return the physical line count for source text."""
    return len(text.splitlines())


def _ensure_project_root_on_path() -> None:
    """Insert the project root for local imports."""
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)


def _validate_py_compile() -> None:
    """Compile touched Python files without importing GUI dependencies."""
    for relative_path in TOUCHED_SOURCE_FILES:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def _validate_line_counts() -> None:
    """Ensure touched source files stay within the active size canon."""
    for relative_path in TOUCHED_SOURCE_FILES:
        count = _line_count(_read_project_text(relative_path))
        if count > MAX_CODE_LINES:
            raise AssertionError(
                f"{relative_path} has {count} lines; maximum is {MAX_CODE_LINES}"
            )


def _validate_style_contract(template: object) -> None:
    """Ensure the template preserves the accepted inner-tab visual contract."""
    if template.INNER_TAB_HEIGHT != 24:
        raise AssertionError("Inner-tab height must remain 24")
    for fragment in [
        "#1F4E79",
        "#ECEFF3",
        "padding: 1px 8px",
        "max-height: 24px",
        "QPushButton:hover",
    ]:
        combined = template.INNER_TAB_ACTIVE_STYLE + template.INNER_TAB_INACTIVE_STYLE
        if fragment not in combined:
            raise AssertionError(f"Template style missing fragment: {fragment}")


def _validate_click_behavior(template: object) -> None:
    """Ensure clicking a gray inactive tab makes it blue and active."""
    layout = FakeLayout()
    stack = FakeStack()
    selected_indexes: list[int] = []
    specs = [
        template.InnerTabSpec("Run Selected Mode", "inner_tab_run_selected_mode"),
        template.InnerTabSpec(
            "Large Module AST Split Audit",
            "inner_tab_large_module_ast_split_audit",
        ),
    ]
    buttons = template.build_inner_tab_row(
        layout,
        FakeButton,
        specs,
        stack=stack,
        on_selected=selected_indexes.append,
        initial_index=0,
    )

    if len(buttons) != 2:
        raise AssertionError("Template did not create two inner-tab buttons")
    if not buttons[0].checked or buttons[1].checked:
        raise AssertionError("Initial inner-tab state is not correct")
    if "#1F4E79" not in buttons[0].style_sheet:
        raise AssertionError("Active initial tab is not blue")
    if "#ECEFF3" not in buttons[1].style_sheet:
        raise AssertionError("Inactive initial tab is not gray")
    if buttons[0].minimum_height != 24 or buttons[0].maximum_height != 24:
        raise AssertionError("Initial button height is not compact and fixed")

    buttons[1].clicked.emit()
    if buttons[0].checked or not buttons[1].checked:
        raise AssertionError("Clicked inner tab did not become the only active tab")
    if "#ECEFF3" not in buttons[0].style_sheet:
        raise AssertionError("Old active tab did not become gray")
    if "#1F4E79" not in buttons[1].style_sheet:
        raise AssertionError("Clicked inner tab did not become blue")
    if stack.current_index != 1:
        raise AssertionError("Stack did not switch to clicked inner-tab index")
    if selected_indexes[-1] != 1:
        raise AssertionError("Selection callback did not receive clicked index")


def main() -> int:
    """Run focused validation for the inner-tabs template."""
    _validate_py_compile()
    _validate_line_counts()
    _ensure_project_root_on_path()
    template = importlib.import_module("kanda_reasoner_app.templates.inner_tabs_template")
    exported_template = importlib.import_module("kanda_reasoner_app.templates")
    if exported_template.InnerTabSpec is not template.InnerTabSpec:
        raise AssertionError("Templates package does not re-export InnerTabSpec")
    _validate_style_contract(template)
    _validate_click_behavior(template)
    print("VALIDATION OK: inner-tabs-template-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
