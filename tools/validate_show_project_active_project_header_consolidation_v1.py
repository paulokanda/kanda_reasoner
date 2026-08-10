# project-path: tools/validate_show_project_active_project_header_consolidation_v1.py
"""Validate the consolidated Active Project controls in Show Project to AI."""

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
    """Validate source ownership, captions, layout, and module size."""
    main_text = read_text(root, MAIN_WINDOW)
    patches_text = read_text(root, WINDOW_PATCHES)
    safe_eject_text = read_text(root, SAFE_EJECT_VALIDATOR)

    for relative_path, source_text in (
        (MAIN_WINDOW, main_text),
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

    required_patches = (
        'project_label.setText("Active Project:")',
        '"color: #0B3D91; font-weight: bold; padding-left: 4px;"',
        'project_edit.setStyleSheet("color: #9DC08B; font-weight: bold;")',
        'browse_button.hide()',
        "for control in (self.select_project_button, self.eject_project_button):",
        "header_layout.insertWidget(insert_index, control, 0)",
        "control.show()",
    )
    for marker in required_patches:
        require(marker in patches_text, "Header integration marker missing: " + marker)
    require(
        "'backup_show_project_button'" in patches_text,
        "Backup Show Project control was not preserved",
    )
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
    """Exercise the actual collector-header relocation helper with Qt widgets."""
    configure_qt()
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QPushButton,
            QWidget,
        )
    except ImportError:
        print("SHOW_PROJECT_ACTIVE_HEADER_REAL_QT: NOT_APPLICABLE")
        return

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches import (
        _WindowToolPatchesMixin,
    )

    app = QApplication.instance() or QApplication([])

    class CollectorWidget(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.header_host = QWidget(self)
            self.header_layout = QHBoxLayout(self.header_host)
            self.project_root_label = QLabel("Project Root:")
            self.project_root_edit = QLineEdit()
            self.browse_project_button = QPushButton("Browse...")
            self.backup_show_project_button = QPushButton("Backup Show Project")
            for control in (
                self.project_root_label,
                self.project_root_edit,
                self.browse_project_button,
                self.backup_show_project_button,
            ):
                self.header_layout.addWidget(control)

    class Harness(_WindowToolPatchesMixin):
        def __init__(self) -> None:
            self.current_project_root = None
            self.select_project_button = QPushButton("Select Active Project")
            self.eject_project_button = QPushButton("Eject Active Project")
            self.eject_project_button.setEnabled(False)

        @staticmethod
        def _normalize_project_root(_text: str):
            return None

        @staticmethod
        def _bind_project_root_field(_field) -> None:
            return None

    widget = CollectorWidget()
    harness = Harness()
    harness._patch_collector_widget(widget)
    app.processEvents()

    layout = widget.header_layout
    edit_index = layout.indexOf(widget.project_root_edit)
    select_index = layout.indexOf(harness.select_project_button)
    eject_index = layout.indexOf(harness.eject_project_button)
    backup_index = layout.indexOf(widget.backup_show_project_button)

    require(widget.project_root_label.text() == "Active Project:", "Label mismatch")
    require("#0B3D91" in widget.project_root_label.styleSheet(), "Blue label missing")
    require("font-weight: bold" in widget.project_root_label.styleSheet(), "Bold label missing")
    require("#9DC08B" in widget.project_root_edit.styleSheet(), "Green path missing")
    require("font-weight: bold" in widget.project_root_edit.styleSheet(), "Bold path missing")
    require(widget.project_root_edit.text() == "", "No-Project path must stay blank")
    require(layout.indexOf(widget.browse_project_button) == -1, "Browse remains in header")
    require(widget.browse_project_button.isHidden(), "Browse is not hidden")
    require(select_index == edit_index + 1, "Select button is not after the path")
    require(eject_index == select_index + 1, "Eject button is not after Select")
    require(backup_index == eject_index + 1, "Backup button order changed")
    require(not harness.select_project_button.isHidden(), "Select button is hidden")
    require(not harness.eject_project_button.isHidden(), "Eject button is hidden")
    require(not harness.eject_project_button.isEnabled(), "Eject must stay disabled for NONE")

    widget.close()
    widget.deleteLater()
    harness.select_project_button.deleteLater()
    harness.eject_project_button.deleteLater()
    app.processEvents()
    print("SHOW_PROJECT_ACTIVE_HEADER_REAL_QT: PASS")


def main() -> int:
    """Run the focused consolidation regression."""
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
