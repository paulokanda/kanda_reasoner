# project-path: tools/validate_active_project_controls_requested_tabs_v1.py
"""Validate Active Project controls across the requested KANDA tabs."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "active-project-controls-requested-tabs-v1"

SOURCE_FILES = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_project_root.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py",
    "tools/validate_global_project_switch_settlement_safe_eject_v1.py",
    "tools/validate_active_project_controls_requested_tabs_v1.py",
)

TARGET_METHODS = (
    "_move_tab1_project_root_controls_to_header_row",
    "_move_tab3_project_root_controls_to_header_row",
    "_move_show_project_project_root_controls_to_header_row",
    "_move_error_memory_project_root_controls_to_header_row",
    "_move_freeze_after_update_project_root_controls_to_header_row",
    "_move_project_qa_project_root_controls_to_header_row",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_source(root: Path, relative: str) -> str:
    """Read one required UTF-8 source file."""
    path = root / relative
    require(path.is_file(), "Missing source file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate syntax, module size, ownership, captions, and mappings."""
    texts = {relative: read_source(root, relative) for relative in SOURCE_FILES}
    for relative, text in texts.items():
        ast.parse(text, filename=relative)
        require(
            len(text.splitlines()) <= 500,
            relative + " exceeds 500 physical lines",
        )
    print("ACTIVE_PROJECT_REQUESTED_TABS_PYTHON_SYNTAX: PASS")
    print("ACTIVE_PROJECT_REQUESTED_TABS_MODULE_SIZE: PASS")

    main = texts[SOURCE_FILES[0]]
    lazy_tabs = texts[SOURCE_FILES[1]]
    relocation = texts[SOURCE_FILES[2]]
    project_root = texts[SOURCE_FILES[3]]
    patches = texts[SOURCE_FILES[4]]

    for marker in (
        "project_controls = QWidget()",
        "project_controls_layout",
        "root.addWidget(project_controls)",
    ):
        require(marker not in main, "Legacy top Project container remains: " + marker)
    require(
        "select_project_handler=self._select_active_project" in main
        and "eject_project_handler=self._eject_active_project" in main,
        "Lazy tabs do not receive shell-owned Project commands",
    )
    print("LEGACY_TOP_ACTIVE_PROJECT_CONTAINER_REMOVED: PASS")
    print("SHELL_PROJECT_COMMAND_AUTHORITY_REUSED: PASS")

    for marker in (
        "self._select_project_handler = select_project_handler",
        "self._eject_project_handler = eject_project_handler",
        "def request_select_active_project",
        "def request_eject_active_project",
        "def refresh_active_project_controls",
    ):
        require(marker in lazy_tabs, "Lazy tab command marker missing: " + marker)

    for method_name in TARGET_METHODS:
        require(
            method_name in relocation,
            "Requested tab relocation method missing: " + method_name,
        )
    for marker in (
        'label.setText("Active Project:")',
        '"color: #0B3D91; font-weight: bold; padding-left: 4px;"',
        'path_widget.setStyleSheet("color: #9DC08B; font-weight: bold;")',
        'QPushButton("Select Active Project")',
        'QPushButton("Eject Active Project")',
        "browse_button.hide()",
        "self.refresh_active_project_controls()",
    ):
        require(marker in relocation, "Shared header marker missing: " + marker)
    print("REQUESTED_TAB_HEADER_MAPPING: PASS")
    print("ACTIVE_PROJECT_LABEL_AND_PATH_STYLE: PASS")
    print("BROWSE_REPLACED_BY_SELECT_AND_EJECT: PASS")

    require(
        'for page in getattr(self, "_pages", []):' in project_root
        and 'refresh(root)' in project_root,
        "Proxy command enabled state is not synchronized from shell authority",
    )
    print("ACTIVE_PROJECT_PROXY_STATE_SYNC: PASS")

    require(
        "_install_collector_active_project_controls" not in patches,
        "Obsolete collector-only button relocation remains",
    )
    require(
        "'backup_show_project_button'" in patches,
        "Backup Show Project visibility contract was lost",
    )
    print("SHOW_PROJECT_BACKUP_CONTROL_PRESERVED: PASS")


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
    """Exercise every requested header mapping with real Qt widgets."""
    configure_qt()
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QLineEdit,
            QPushButton,
            QWidget,
        )
    except ImportError:
        print("ACTIVE_PROJECT_REQUESTED_TABS_REAL_QT: NOT_APPLICABLE")
        return

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.reasoner_tools_gui_shell._lazy_tab_shell_chrome import (
        _ARCHITECTURE_GUI_SOURCE,
        _CONTEXT_COLLECTOR_GUI_SOURCE,
        _DOCSTRINGS_GUI_SOURCE,
        _ERROR_MEMORY_GUI_SOURCE,
        _FREEZE_AFTER_UPDATE_GUI_SOURCE,
        _PROJECT_QA_GUI_SOURCE,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs import LazyToolTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import ToolSpec

    app = QApplication.instance() or QApplication([])
    active_root: list[object] = [Path("C:/KANDA/TestProject")]
    select_calls: list[str] = []
    eject_calls: list[str] = []

    class HeaderFixture(QWidget):
        def __init__(
            self,
            label_name: str,
            path_name: str,
            browse_name: str,
            *,
            trailing_name: str = "",
        ) -> None:
            super().__init__()
            label = QLabel("Project Root:")
            path = QLineEdit("C:/KANDA/TestProject")
            browse = QPushButton("Browse...")
            setattr(self, label_name, label)
            setattr(self, path_name, path)
            setattr(self, browse_name, browse)
            self._fixture_controls = [label, path, browse]
            if trailing_name:
                trailing = QPushButton("Trailing Action")
                setattr(self, trailing_name, trailing)
                self._fixture_controls.append(trailing)
            self._project_root_controls_moved_to_host = False
            self._project_root_controls_moved = False

        def move_project_root_controls_to_layout(self, layout) -> None:
            for control in self._fixture_controls:
                layout.addWidget(control, 0)

    cases = (
        (
            "Audit Project",
            "architecture_review",
            _ARCHITECTURE_GUI_SOURCE,
            "_move_tab1_project_root_controls_to_header_row",
            "_root_path_label",
            "_root_path_edit",
            "_browse_root_btn",
            "",
        ),
        (
            "Docstring Assistant",
            "docstring_assistant",
            _DOCSTRINGS_GUI_SOURCE,
            "_move_tab3_project_root_controls_to_header_row",
            "_root_path_label",
            "_root_path_edit",
            "_browse_root_button",
            "",
        ),
        (
            "Show Project to AI",
            "show_project",
            _CONTEXT_COLLECTOR_GUI_SOURCE,
            "_move_show_project_project_root_controls_to_header_row",
            "project_root_label",
            "project_root_edit",
            "browse_project_button",
            "backup_show_project_button",
        ),
        (
            "Error Memory",
            "error_memory",
            _ERROR_MEMORY_GUI_SOURCE,
            "_move_error_memory_project_root_controls_to_header_row",
            "project_root_header_label",
            "project_root_value_label",
            "search_project_button",
            "",
        ),
        (
            "Freeze Feature After Update",
            "freeze_after_update",
            _FREEZE_AFTER_UPDATE_GUI_SOURCE,
            "_move_freeze_after_update_project_root_controls_to_header_row",
            "project_root_header_label",
            "project_root_edit",
            "search_project_button",
            "",
        ),
        (
            "Local AI",
            "project_qa",
            _PROJECT_QA_GUI_SOURCE,
            "_move_project_qa_project_root_controls_to_header_row",
            "project_root_label",
            "project_root_edit",
            "pick_project_root_button",
            "run_analysis_button",
        ),
    )

    tabs: list[LazyToolTab] = []
    fixtures: list[HeaderFixture] = []
    for (
        title,
        tab_id,
        source_hint,
        method_name,
        label_name,
        path_name,
        browse_name,
        trailing_name,
    ) in cases:
        spec = ToolSpec(
            step_title=title,
            source_hint=source_hint,
            tab_id=tab_id,
        )
        tab = LazyToolTab(
            spec,
            lambda *_args: None,
            select_project_handler=lambda t=title: select_calls.append(t),
            eject_project_handler=lambda t=title: eject_calls.append(t),
            active_project_provider=lambda: active_root[0],
        )
        fixture = HeaderFixture(
            label_name,
            path_name,
            browse_name,
            trailing_name=trailing_name,
        )
        getattr(tab, method_name)(fixture)
        app.processEvents()

        label = getattr(fixture, label_name)
        path_widget = getattr(fixture, path_name)
        browse = getattr(fixture, browse_name)
        layout = tab.tab_header_template.project_root_layout
        select_button = tab.active_project_select_button
        eject_button = tab.active_project_eject_button

        require(label.text() == "Active Project:", title + " label mismatch")
        require("#0B3D91" in label.styleSheet(), title + " blue label missing")
        require("font-weight: bold" in label.styleSheet(), title + " bold label missing")
        require("#9DC08B" in path_widget.styleSheet(), title + " green path missing")
        require("font-weight: bold" in path_widget.styleSheet(), title + " bold path missing")
        require(browse.isHidden(), title + " Browse button remains visible")
        require(select_button is not None, title + " Select button missing")
        require(eject_button is not None, title + " Eject button missing")
        require(
            layout.indexOf(select_button) == layout.indexOf(path_widget) + 1,
            title + " Select button order mismatch",
        )
        require(
            layout.indexOf(eject_button) == layout.indexOf(select_button) + 1,
            title + " Eject button order mismatch",
        )
        require(eject_button.isEnabled(), title + " Eject should be enabled")
        select_button.click()
        eject_button.click()

        tabs.append(tab)
        fixtures.append(fixture)

    require(len(select_calls) == len(cases), "Select callbacks did not reach shell authority")
    require(len(eject_calls) == len(cases), "Eject callbacks did not reach shell authority")

    active_root[0] = None
    for tab in tabs:
        tab.refresh_active_project_controls(None)
        require(
            tab.active_project_eject_button is not None
            and not tab.active_project_eject_button.isEnabled(),
            "Eject remained enabled after Project NONE",
        )

    for fixture in fixtures:
        fixture.close()
        fixture.deleteLater()
    for tab in tabs:
        tab.close()
        tab.deleteLater()
    app.processEvents()
    print("ACTIVE_PROJECT_REQUESTED_TABS_REAL_QT: PASS")


def main() -> int:
    """Run the requested multi-tab Active Project regression."""
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
