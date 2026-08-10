# project-path: tools/validate_active_project_buttons_web_config_ai_v1.py
"""Validate Active Project buttons in Web AI and Config AI headers."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "active-project-buttons-web-config-ai-v1"

SOURCE_FILES = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_shell_chrome.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "tools/validate_active_project_buttons_web_config_ai_v1.py",
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
    """Validate source structure, ownership, and module-size contracts."""
    texts = {relative: read_source(root, relative) for relative in SOURCE_FILES}
    for relative, text in texts.items():
        ast.parse(text, filename=relative)
        require(
            len(text.splitlines()) <= 500,
            relative + " exceeds 500 physical lines",
        )
    print("ACTIVE_PROJECT_WEB_CONFIG_AI_PYTHON_SYNTAX: PASS")
    print("ACTIVE_PROJECT_WEB_CONFIG_AI_MODULE_SIZE: PASS")

    chrome = texts[SOURCE_FILES[0]]
    relocation = texts[SOURCE_FILES[1]]
    lazy_tabs = texts[SOURCE_FILES[2]]

    for marker in (
        '_CONFIG_AI_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_engine/config_ai_tab.py"',
        '_WEB_AI_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_engine/project_web_ai_tab.py"',
        "_ACTIVE_PROJECT_BUTTON_ONLY_SOURCES = {",
        "_CONFIG_AI_GUI_SOURCE,",
        "_WEB_AI_GUI_SOURCE,",
    ):
        require(marker in chrome, "Header source marker missing: " + marker)
    print("WEB_CONFIG_AI_HEADER_SOURCE_MAPPING: PASS")

    for marker in (
        "def _install_title_active_project_buttons",
        "self.spec.source_hint not in _ACTIVE_PROJECT_BUTTON_ONLY_SOURCES",
        "def _install_active_project_command_buttons",
        'QPushButton("Select Active Project")',
        'QPushButton("Eject Active Project")',
        "select_button.clicked.connect(self.request_select_active_project)",
        "eject_button.clicked.connect(self.request_eject_active_project)",
        "self.refresh_active_project_controls()",
    ):
        require(marker in relocation, "Button ownership marker missing: " + marker)
    require(
        "self._install_title_active_project_buttons()" in lazy_tabs,
        "Web AI and Config AI title buttons are not installed during tab construction",
    )
    require(
        "def request_select_active_project" in lazy_tabs
        and "def request_eject_active_project" in lazy_tabs,
        "Shell-owned command proxies are missing",
    )
    print("WEB_CONFIG_AI_SHELL_COMMAND_REUSE: PASS")
    print("WEB_CONFIG_AI_BUTTONS_INSTALLED_BEFORE_TOOL_LOAD: PASS")


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
    """Exercise Web AI and Config AI header proxies with real Qt widgets."""
    configure_qt()
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("ACTIVE_PROJECT_WEB_CONFIG_AI_REAL_QT: NOT_APPLICABLE")
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
    select_calls: list[str] = []
    eject_calls: list[str] = []
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
            select_project_handler=lambda t=title: select_calls.append(t),
            eject_project_handler=lambda t=title: eject_calls.append(t),
            active_project_provider=lambda: active_root[0],
        )
        app.processEvents()

        select_button = tab.active_project_select_button
        eject_button = tab.active_project_eject_button
        layout = tab.tab_header_template.project_root_layout

        require(select_button is not None, title + " Select button missing")
        require(eject_button is not None, title + " Eject button missing")
        require(
            select_button.text() == "Select Active Project",
            title + " Select caption mismatch",
        )
        require(
            eject_button.text() == "Eject Active Project",
            title + " Eject caption mismatch",
        )
        require(layout.indexOf(select_button) >= 0, title + " Select not in header")
        require(
            layout.indexOf(eject_button) == layout.indexOf(select_button) + 1,
            title + " button order mismatch",
        )
        require(eject_button.isEnabled(), title + " Eject should be enabled")
        select_button.click()
        eject_button.click()
        tabs.append(tab)

    require(len(select_calls) == len(cases), "Select callbacks missed shell authority")
    require(len(eject_calls) == len(cases), "Eject callbacks missed shell authority")

    active_root[0] = None
    for tab in tabs:
        tab.refresh_active_project_controls(None)
        require(
            tab.active_project_select_button is not None
            and tab.active_project_select_button.isEnabled(),
            "Select should remain enabled under Project NONE",
        )
        require(
            tab.active_project_eject_button is not None
            and not tab.active_project_eject_button.isEnabled(),
            "Eject remained enabled under Project NONE",
        )
        tab.close()
        tab.deleteLater()
    app.processEvents()
    print("ACTIVE_PROJECT_WEB_CONFIG_AI_REAL_QT: PASS")


def main() -> int:
    """Run the focused Web AI and Config AI header regression."""
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
