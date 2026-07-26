# project-path: tools/validate_config_web_ai_central_v1.py
"""Validate one central Config Web AI owner and mode-only workflow controls."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

FEATURE_ID = "config-web-ai-central-v1r2"

__all__ = ["main", "validate_real_qt", "validate_static"]


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    """Return one UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate ownership, registration, deduplication, and boundaries."""
    controller = read(root, "kanda_reasoner_app/web_ai_configuration.py")
    config_tab = read(root, "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py")
    config_ai_tab = read(root, "kanda_reasoner_app/reasoner_engine/config_ai_tab.py")
    project_tab = read(root, "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py")
    project_ui = read(root, "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py")
    doc_controls = read(root, "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py")
    shell = read(root, "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py")
    specs = read(root, "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py")

    for marker in (
        "class WebAIConfigurationController(QObject)",
        "class WebAIConfigurationSnapshot",
        "ProjectWebAIModelCatalogWorker",
        "resolve_environment_key",
        "selected_model_id",
        "credential_available",
        "structured_output_supported",
    ):
        require(marker in controller, "central owner missing: " + marker)
    require("active_project_root" not in controller, "central config stores Project identity")
    require("project_support" not in controller.lower(), "central config owns Project Support")
    print("ONE_CANONICAL_WEB_AI_CONFIGURATION_OWNER: PASS")
    print("NO_PROJECT_IDENTITY_STORED_IN_GLOBAL_CONFIG: PASS")

    for marker in (
        'step_title="Config AI"',
        'tab_id="config_web_ai"',
        'class_candidates=("ConfigAITab",)',
    ):
        require(marker in specs, "Config AI registration missing: " + marker)
    for marker in (
        "ConfigWebAITab()",
        'addTab(self.web_ai_tab, "Config Web AI")',
        'addTab(self.local_ai_tab, "Config Local AI")',
    ):
        require(marker in config_ai_tab, "Config AI composition missing: " + marker)
    require("WebAIConfigurationController(self)" in shell, "shell does not own controller")
    require("install_application_web_ai_configuration" in shell, "app owner not installed")
    print("CONFIG_WEB_AI_TAB_REGISTERED: PASS")
    print("APPLICATION_SCOPED_CONFIGURATION_OWNER: PASS")

    for marker in (
        'QPushButton("Load Environment Key")',
        'QPushButton("Refresh Models")',
        'QCheckBox("Free models only")',
        'setEchoMode(QLineEdit.EchoMode.Password)',
        "gateway_profiles()",
    ):
        require(marker in config_tab, "central config UI missing: " + marker)
    print("CENTRAL_GATEWAY_KEY_MODEL_CONTROLS: PASS")
    for marker in (
        'background-color: #1d2128;',
        'viewport.setStyleSheet("background-color: #1d2128;")',
        'Qt.WidgetAttribute.WA_StyledBackground',
        'QPalette.ColorRole.Window',
    ):
        require(marker in config_tab, "central popup opacity contract missing: " + marker)
    print("CENTRAL_WEB_AI_OPAQUE_POPUP_CONTRACT: PASS")

    require("gateway_combo" not in project_ui, "Project Web AI retains editable gateway control")
    require("api_key_edit" not in project_ui, "Project Web AI retains editable key control")
    require("model_combo" not in project_ui, "Project Web AI retains editable model control")
    require("open_web_config_button" in project_ui, "Project Web AI Config shortcut missing")
    require("application_web_ai_configuration" in project_tab, "Project Web AI ignores central owner")
    require("ProjectWebAIModelCatalogWorker" not in project_tab, "Project Web AI owns duplicate catalog")
    require("resolve_environment_key" not in project_tab, "Project Web AI owns duplicate credential resolver")
    print("PROJECT_WEB_AI_USES_SHARED_CONFIGURATION: PASS")
    print("PROJECT_WEB_AI_NO_DUPLICATE_CONFIG_CONTROLS: PASS")

    for marker in (
        'QRadioButton("Heuristic")',
        'QRadioButton("Local AI")',
        'QRadioButton("Web AI")',
        'QPushButton("Open Config AI")',
    ):
        require(marker in doc_controls, "Docstring mode-only UI missing: " + marker)
    require("ProjectWebAIModelCatalogWorker" not in doc_controls, "Docstring owns duplicate catalog")
    require("resolve_environment_key" not in doc_controls, "Docstring owns duplicate key resolver")
    require(
        "owner._web_ai_configuration = _controller(owner)" in doc_controls,
        "Docstring central configuration symbol is unresolved",
    )
    print("DOCSTRING_CENTRAL_CONFIG_SYMBOL_RESOLVED: PASS")
    print("DOCSTRING_MODE_ONLY_WEB_AI_SELECTION: PASS")
    print("NO_DUPLICATE_DOCSTRING_WEB_CONFIGURATION: PASS")

    changed = (
        "kanda_reasoner_app/web_ai_configuration.py",
        "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/config_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/config_local_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/_docstring_ai_header_runtime.py",
    )
    for relative in changed:
        lines = len(read(root, relative).splitlines())
        require(0 < lines <= 500, relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt(root: Path) -> None:
    """Exercise the real shell-level shared controller and two consumers."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent, Qt
        from PySide6.QtGui import QPalette
        from PySide6.QtWidgets import QApplication, QLineEdit
    except ImportError as exc:
        raise AssertionError("PySide6 is required for real-widget validation") from exc

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui import MissingDocstringsWindow
    from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    app = QApplication.instance() or QApplication([])
    config = ConfigWebAITab()
    project = ProjectWebAITab()
    doc = MissingDocstringsWindow()
    try:
        controller = application_web_ai_configuration()
        require(config._controller is controller, "Config tab controller mismatch")
        require(project._web_config is controller, "Project Web AI controller mismatch")
        require(doc._web_ai_configuration is controller, "Docstring controller mismatch")
        require(config.gateway_combo.count() == 2, "gateway options missing")
        require(config.api_key_edit.echoMode() == QLineEdit.EchoMode.Password, "key is visible")
        for combo in (config.gateway_combo, config.model_combo):
            popup = combo.view()
            viewport = popup.viewport()
            popup_style = "".join(popup.styleSheet().lower().split())
            viewport_style = "".join(viewport.styleSheet().lower().split())
            require(
                "background-color:#1d2128" in popup_style,
                "central dropdown popup lacks direct opaque background",
            )
            require(
                "background-color:#1d2128" in viewport_style,
                "central dropdown viewport lacks direct opaque background",
            )
            require(
                popup.testAttribute(Qt.WidgetAttribute.WA_StyledBackground),
                "central dropdown popup lacks styled-background contract",
            )
            require(
                viewport.testAttribute(Qt.WidgetAttribute.WA_StyledBackground),
                "central dropdown viewport lacks styled-background contract",
            )
            for surface, label in ((popup, "popup"), (viewport, "viewport")):
                palette = surface.palette()
                require(
                    palette.color(QPalette.ColorRole.Base).alpha() == 255,
                    "central dropdown " + label + " Base is transparent",
                )
                require(
                    palette.color(QPalette.ColorRole.Window).alpha() == 255,
                    "central dropdown " + label + " Window is transparent",
                )
        print("REAL_CENTRAL_WEB_AI_OPAQUE_POPUPS: PASS")
        require(not hasattr(project, "gateway_combo"), "Project Web AI duplicate gateway control")
        require(doc._heuristic_radio.isChecked(), "Docstring heuristic default missing")

        model = ModelDescriptor(
            gateway_id="openrouter",
            model_id="fixture/model",
            display_name="Fixture Model",
            free_status=True,
            supported_parameters=("response_format",),
            catalog_timestamp="fixture",
        )
        controller._all_models = [model]
        controller._selected_model_id = model.model_id
        controller._touch()
        app.processEvents()
        require("fixture/model" in project.web_config_summary_value.text(), "Project summary did not update")
        doc._web_ai_radio.setChecked(True)
        app.processEvents()
        require("fixture/model" in doc._web_ai_summary_label.text(), "Docstring summary did not update")
        require(doc._ai_enabled_checkbox.isChecked(), "Docstring compatibility state missing")
        print("SHARED_CONFIGURATION_PROPAGATES_TO_CONSUMERS: PASS")
        print("REAL_CONFIG_WEB_AI_TAB: PASS")
        print("REAL_PROJECT_WEB_AI_CENTRAL_CONFIG: PASS")
        print("REAL_DOCSTRING_MODE_ONLY_CONFIG: PASS")
    finally:
        for widget in (doc, project, config):
            widget.close()
            widget.deleteLater()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    print("CONFIG_WEB_AI_QT_TEARDOWN_CLEAN: PASS")


def main() -> int:
    """Run static and real-widget validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    validate_static(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
