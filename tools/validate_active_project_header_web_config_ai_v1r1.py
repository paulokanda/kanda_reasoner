# project-path: tools/validate_active_project_header_web_config_ai_v1r1.py
"""Validate complete Active Project headers in Web AI and Config AI."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "active-project-header-web-config-ai-v1r1"

SOURCE_FILES = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_shell_chrome.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "tools/validate_active_project_header_web_config_ai_v1r1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_source(root: Path, relative: str) -> str:
    """Read one required source file."""
    path = root / relative
    require(path.is_file(), "Missing source file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate source structure and module-size contracts."""
    texts = {relative: read_source(root, relative) for relative in SOURCE_FILES}
    for relative, text in texts.items():
        ast.parse(text, filename=relative)
        require(
            len(text.splitlines()) <= 500,
            relative + " exceeds 500 physical lines",
        )
    print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_PYTHON_SYNTAX: PASS")
    print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_MODULE_SIZE: PASS")

    chrome = texts[SOURCE_FILES[0]]
    relocation = texts[SOURCE_FILES[1]]
    lazy_tabs = texts[SOURCE_FILES[2]]

    for marker in (
        "_ACTIVE_PROJECT_BUTTON_ONLY_SOURCES = {",
        "_CONFIG_AI_GUI_SOURCE,",
        "_WEB_AI_GUI_SOURCE,",
    ):
        require(marker in chrome, "Header source marker missing: " + marker)

    for marker in (
        "def _install_active_project_proxy_identity",
        'QLabel("Active Project:")',
        'QLineEdit()',
        "path_edit.setReadOnly(True)",
        'color: #0B3D91; font-weight: bold;',
        'color: #9DC08B; font-weight: bold;',
        "self.active_project_label = label",
        "self.active_project_path_edit = path_edit",
        "self._install_active_project_proxy_identity(destination_layout)",
    ):
        require(marker in relocation, "Proxy identity marker missing: " + marker)

    for marker in (
        "self.active_project_label: QLabel | None = None",
        "self.active_project_path_edit: QLineEdit | None = None",
        'path_text = str(active_root) if active_root is not None else ""',
        "self.active_project_path_edit.setText(path_text)",
        'path_text or "No active Project selected."',
    ):
        require(marker in lazy_tabs, "Proxy synchronization marker missing: " + marker)

    print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_SOURCE_MAPPING: PASS")
    print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_IDENTITY_CONTRACT: PASS")
    print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_SYNC_CONTRACT: PASS")


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
    """Exercise complete Web AI and Config AI headers with real Qt."""
    configure_qt()
    try:
        from PySide6.QtWidgets import QApplication, QLineEdit
    except ImportError:
        print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_REAL_QT: NOT_APPLICABLE")
        return

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.reasoner_tools_gui_shell._lazy_tab_shell_chrome import (
        _CONFIG_AI_GUI_SOURCE,
        _WEB_AI_GUI_SOURCE,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs import LazyToolTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import ToolSpec

    app = QApplication.instance() or QApplication([])
    active_root: list[object] = [Path("C:/KANDA/TestProject")]
    tabs: list[LazyToolTab] = []

    cases = (
        ("Web AI", "project_web_ai", _WEB_AI_GUI_SOURCE),
        ("Config AI", "config_web_ai", _CONFIG_AI_GUI_SOURCE),
    )
    for title, tab_id, source_hint in cases:
        tab = LazyToolTab(
            ToolSpec(
                step_title=title,
                source_hint=source_hint,
                tab_id=tab_id,
            ),
            lambda *_args: None,
            select_project_handler=lambda: None,
            eject_project_handler=lambda: None,
            active_project_provider=lambda: active_root[0],
        )
        app.processEvents()

        label = tab.active_project_label
        path_edit = tab.active_project_path_edit
        select_button = tab.active_project_select_button
        eject_button = tab.active_project_eject_button
        layout = tab.tab_header_template.project_root_layout

        require(label is not None, title + " Active Project label missing")
        require(path_edit is not None, title + " Active Project path missing")
        require(isinstance(path_edit, QLineEdit), title + " path is not QLineEdit")
        require(label.text() == "Active Project:", title + " label mismatch")
        require("#0B3D91" in label.styleSheet(), title + " label color mismatch")
        require("font-weight: bold" in label.styleSheet(), title + " label not bold")
        require(path_edit.isReadOnly(), title + " path must be read-only")
        require("#9DC08B" in path_edit.styleSheet(), title + " path color mismatch")
        require("font-weight: bold" in path_edit.styleSheet(), title + " path not bold")
        require(
            path_edit.text() == str(active_root[0]),
            title + " active path did not synchronize",
        )

        indexes = [
            layout.indexOf(label),
            layout.indexOf(path_edit),
            layout.indexOf(select_button),
            layout.indexOf(eject_button),
        ]
        require(all(index >= 0 for index in indexes), title + " header member missing")
        require(indexes == sorted(indexes), title + " header order mismatch")

        active_root[0] = None
        tab.refresh_active_project_controls(None)
        require(path_edit.text() == "", title + " path not cleared under NONE")
        require(
            not eject_button.isEnabled(),
            title + " Eject remained enabled under NONE",
        )

        active_root[0] = Path("D:/Projects/SecondProject")
        tab.refresh_active_project_controls(active_root[0])
        require(
            path_edit.text() == str(active_root[0]),
            title + " path did not refresh after Project switch",
        )
        require(eject_button.isEnabled(), title + " Eject did not re-enable")
        tabs.append(tab)

    for tab in tabs:
        tab.close()
        tab.deleteLater()
    app.processEvents()
    print("ACTIVE_PROJECT_WEB_CONFIG_HEADER_REAL_QT: PASS")


def main() -> int:
    """Run the focused complete-header regression."""
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
