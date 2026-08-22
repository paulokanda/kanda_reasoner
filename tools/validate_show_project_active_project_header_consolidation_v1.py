# project-path: tools/validate_show_project_active_project_header_consolidation_v1.py
"""Validate the current Show Project Active Project header integration."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "show-project-active-project-header-consolidation-v1"
MAIN_WINDOW = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py"
)
LAYOUT_RELOCATION = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "_lazy_tab_layout_relocation.py"
)
WINDOW_PATCHES = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/"
    "window_tool_patches.py"
)
SAFE_EJECT_VALIDATOR = Path(
    "tools/validate_global_project_switch_settlement_safe_eject_v1.py"
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_text(root: Path, relative_path: Path) -> str:
    """Read one required UTF-8 source file."""
    path = root / relative_path
    require(path.is_file(), "Missing source file: " + str(relative_path))
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate current header ownership, styling, and shell commands."""
    main_text = read_text(root, MAIN_WINDOW)
    relocation_text = read_text(root, LAYOUT_RELOCATION)
    patches_text = read_text(root, WINDOW_PATCHES)
    safe_eject_text = read_text(root, SAFE_EJECT_VALIDATOR)

    for relative_path, source_text in (
        (MAIN_WINDOW, main_text),
        (LAYOUT_RELOCATION, relocation_text),
        (WINDOW_PATCHES, patches_text),
        (SAFE_EJECT_VALIDATOR, safe_eject_text),
    ):
        ast.parse(source_text, filename=str(relative_path))
        require(
            len(source_text.splitlines()) <= 500,
            str(relative_path) + " exceeds 500 physical lines",
        )
    print("SHOW_PROJECT_ACTIVE_HEADER_PYTHON_SYNTAX: PASS")
    print("SHOW_PROJECT_ACTIVE_HEADER_MODULE_SIZE: PASS")

    forbidden_top_row = (
        "project_controls = QWidget()",
        "project_controls_layout",
        "active_project_value",
        "root.addWidget(project_controls)",
    )
    for marker in forbidden_top_row:
        require(marker not in main_text, "Legacy top Project row remains: " + marker)
    print("LEGACY_TOP_ACTIVE_PROJECT_CONTAINER_REMOVED: PASS")

    required_main = (
        'QPushButton("Select Active Project", central)',
        'QPushButton("Eject Active Project", central)',
        "self.select_project_button.clicked.connect(self._select_active_project)",
        "self.eject_project_button.clicked.connect(self._eject_active_project)",
        "self.select_project_button.hide()",
        "self.eject_project_button.hide()",
    )
    for marker in required_main:
        require(marker in main_text, "Shell Project command marker missing: " + marker)
    print("SHELL_PROJECT_COMMANDS_PRESERVED: PASS")

    required_relocation = (
        "def _move_show_project_project_root_controls_to_header_row",
        'label=getattr(widget, "project_root_label", None)',
        'path_widget=getattr(widget, "project_root_edit", None)',
        'browse_button=getattr(widget, "browse_project_button", None)',
        'label.setText("Active Project:")',
        '"color: #0B3D91; "',
        '"color: #166534; "',
        "browse_button.hide()",
        "destination_layout.insertWidget(insert_index, select_button, 0)",
        "destination_layout.insertWidget(insert_index + 1, eject_button, 0)",
    )
    for marker in required_relocation:
        require(
            marker in relocation_text,
            "Current header integration marker missing: " + marker,
        )
    require(
        "project_label.setText(\"Active Project:\")" not in patches_text,
        "Legacy Show Project header styling still owned by window_tool_patches",
    )
    require(
        "'backup_show_project_button'" in patches_text,
        "Backup Show Project visibility preservation is missing",
    )
    print("SHOW_PROJECT_ACTIVE_HEADER_CURRENT_OWNER: PASS")
    print("SHOW_PROJECT_ACTIVE_HEADER_STRONG_GREEN_STYLE: PASS")
    print("SHOW_PROJECT_ACTIVE_PROJECT_HEADER_CONTRACT: PASS")

    require(
        'QPushButton("Select Active Project", central)' in safe_eject_text
        and 'QPushButton("Eject Active Project", central)' in safe_eject_text,
        "Safe-eject validator does not track the current captions",
    )
    print("SAFE_EJECT_VALIDATOR_CAPTION_SYNC: PASS")


def configure_qt() -> None:
    """Configure deterministic offscreen Qt behavior."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name != "nt":
        return
    for candidate in (
        Path(os.environ.get("WINDIR", "")) / "Fonts",
        Path("C:/Windows/Fonts"),
    ):
        if candidate.is_dir():
            os.environ.setdefault("QT_QPA_FONTDIR", str(candidate))
            return


def validate_real_qt(root: Path) -> None:
    """Exercise the current LazyToolTab Show Project relocation path."""
    configure_qt()
    try:
        from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget
    except ImportError:
        print("SHOW_PROJECT_ACTIVE_HEADER_REAL_QT: NOT_APPLICABLE")
        return

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.reasoner_tools_gui_shell._lazy_tab_shell_chrome import (
        _CONTEXT_COLLECTOR_GUI_SOURCE,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs import LazyToolTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import ToolSpec

    app = QApplication.instance() or QApplication([])
    select_calls: list[str] = []
    eject_calls: list[str] = []

    class CollectorFixture(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.project_root_label = QLabel("Project Root:")
            self.project_root_edit = QLineEdit("")
            self.browse_project_button = QPushButton("Browse...")
            self.backup_show_project_button = QPushButton("Backup Show Project")
            self._fixture_controls = (
                self.project_root_label,
                self.project_root_edit,
                self.browse_project_button,
                self.backup_show_project_button,
            )

        def move_project_root_controls_to_layout(self, layout) -> None:
            for control in self._fixture_controls:
                layout.addWidget(control, 0)

    spec = ToolSpec(
        step_title="Show Project to AI",
        source_hint=_CONTEXT_COLLECTOR_GUI_SOURCE,
        tab_id="show_project",
    )
    tab = LazyToolTab(
        spec,
        lambda *_args: None,
        select_project_handler=lambda: select_calls.append("select"),
        eject_project_handler=lambda: eject_calls.append("eject"),
        active_project_provider=lambda: None,
    )
    widget = CollectorFixture()
    tab._move_show_project_project_root_controls_to_header_row(widget)
    app.processEvents()

    layout = tab.tab_header_template.project_root_layout
    select_button = tab.active_project_select_button
    eject_button = tab.active_project_eject_button

    require(widget.project_root_label.text() == "Active Project:", "Label mismatch")
    require("#0B3D91" in widget.project_root_label.styleSheet(), "Blue label missing")
    require("font-weight: 700" in widget.project_root_label.styleSheet(), "Bold label missing")
    require("#166534" in widget.project_root_edit.styleSheet(), "Strong-green path missing")
    require("font-weight: 700" in widget.project_root_edit.styleSheet(), "Bold path missing")
    require(widget.project_root_edit.text() == "", "No-Project path must stay blank")
    require(widget.browse_project_button.isHidden(), "Browse is not hidden")
    require(select_button is not None, "Select button missing")
    require(eject_button is not None, "Eject button missing")
    require(
        layout.indexOf(select_button) == layout.indexOf(widget.project_root_edit) + 1,
        "Select button is not after the path",
    )
    require(
        layout.indexOf(eject_button) == layout.indexOf(select_button) + 1,
        "Eject button is not after Select",
    )
    require(
        layout.indexOf(widget.backup_show_project_button) == layout.indexOf(eject_button) + 1,
        "Backup button order changed",
    )
    require(not select_button.isHidden(), "Select button is hidden")
    require(not eject_button.isHidden(), "Eject button is hidden")
    require(not eject_button.isEnabled(), "Eject must stay disabled for NONE")

    select_button.click()
    require(select_calls == ["select"], "Select callback did not reach shell authority")
    require(eject_calls == [], "Disabled Eject unexpectedly invoked shell authority")

    widget.close()
    tab.close()
    widget.deleteLater()
    tab.deleteLater()
    app.processEvents()
    print("SHOW_PROJECT_ACTIVE_HEADER_REAL_QT: PASS")


def main() -> int:
    """Run the current header-consolidation regression."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    require(root.is_dir(), "Project root does not exist: " + str(root))
    validate_static(root)
    validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
