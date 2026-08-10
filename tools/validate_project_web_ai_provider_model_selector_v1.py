# project-path: tools/validate_project_web_ai_provider_model_selector_v1.py
"""Validate mirrored provider and model selectors in canonical Project Web AI."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "project-web-ai-provider-model-selector-v1"


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def source(root: Path, relative: str) -> str:
    """Read one UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate mirrored-selector ownership and no-secret boundaries."""
    ui_rel = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
    bridge_rel = (
        "kanda_reasoner_app/reasoner_engine/"
        "project_web_ai_configuration_selector.py"
    )
    tab_rel = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
    for relative in (ui_rel, bridge_rel, tab_rel):
        text = source(root, relative)
        ast.parse(text, filename=relative)
        require(text.isascii(), "non-ASCII source: " + relative)
        require(len(text.splitlines()) <= 500, "module exceeds 500 lines: " + relative)

    ui = source(root, ui_rel)
    bridge = source(root, bridge_rel)
    tab = source(root, tab_rel)
    for marker in (
        "projectWebAIAccessCombo",
        "projectWebAIProviderCombo",
        "projectWebAIModelCombo",
        "projectWebAIRefreshModelsButton",
    ):
        require(marker in ui, "selector UI missing: " + marker)
    for forbidden in (
        "api_key_edit",
        "load_env_button",
        "free_access_checkbox",
        "base_url_edit",
    ):
        require(forbidden not in ui, "secret configuration leaked into Web AI: " + forbidden)
    for marker in (
        "provider_profiles",
        "owner._web_config.set_gateway_id",
        "owner._web_config.set_selected_model_id",
        "owner._web_config.refresh_models",
    ):
        require(marker in bridge, "central selector bridge missing: " + marker)
    require("web_selector.connect(self)" in tab, "selector bridge not connected")
    require("web_selector.render(self)" in tab, "selector bridge not rendered")
    print("PROJECT_WEB_AI_SELECTOR_UI_STATIC: PASS")
    print("PROJECT_WEB_AI_SELECTOR_CENTRAL_OWNER_STATIC: PASS")
    print("PROJECT_WEB_AI_SELECTOR_NO_SECRET_CONTROLS: PASS")


def validate_real_qt(root: Path) -> None:
    """Exercise gateway/direct/provider/model selection through real widgets."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from PySide6.QtCore import QCoreApplication, QEvent
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import (
        ProjectWebAITab,
    )
    from kanda_reasoner_app.web_ai_configuration import (
        WebAIConfigurationController,
        install_application_web_ai_configuration,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

    app = QApplication.instance() or QApplication([])
    controller = WebAIConfigurationController(app)
    install_application_web_ai_configuration(controller)
    tab = ProjectWebAITab()
    try:
        require(tab.web_access_combo.currentData() == "gateway", "gateway access not shown")
        require(tab.web_provider_combo.count() == 2, "gateway providers missing")
        require(tab.web_provider_combo.currentData() == "openrouter", "OpenRouter not selected")

        gateway_model = ModelDescriptor(
            gateway_id="openrouter",
            model_id="openai/gpt-oss-20b:free",
            display_name="GPT OSS 20B Free",
            free_status=True,
            catalog_timestamp="fixture",
        )
        controller._all_models = [gateway_model]
        controller._selected_model_id = gateway_model.model_id
        controller._touch()
        app.processEvents()
        require(tab.web_model_combo.count() == 1, "gateway model not mirrored")
        require(
            tab.web_model_combo.currentData().model_id == gateway_model.model_id,
            "gateway model selection mismatch",
        )

        direct_index = tab.web_access_combo.findData("direct")
        tab.web_access_combo.setCurrentIndex(direct_index)
        app.processEvents()
        require(controller.profile().provider_class == "direct", "direct access not activated")
        require(tab.web_provider_combo.count() == 4, "direct providers missing")
        require(tab.web_provider_combo.currentData() == "gemini", "Gemini not selected")

        direct_model = ModelDescriptor(
            gateway_id="gemini",
            model_id="gemini-3.5-flash",
            display_name="Gemini 3.5 Flash",
            free_status=True,
            free_access_label="Gemini Free Tier",
            catalog_timestamp="fixture",
        )
        controller._all_models = [direct_model]
        controller._selected_model_id = direct_model.model_id
        controller._touch()
        app.processEvents()
        require(tab.web_model_combo.count() == 1, "direct model not mirrored")
        require(
            tab.web_model_combo.currentData().model_id == direct_model.model_id,
            "direct model selection mismatch",
        )

        groq_index = tab.web_provider_combo.findData("groq")
        tab.web_provider_combo.setCurrentIndex(groq_index)
        app.processEvents()
        require(controller.gateway_id() == "groq", "provider selector did not update controller")
        require(not hasattr(tab, "api_key_edit"), "Project Web AI owns a key field")
        print("PROJECT_WEB_AI_GATEWAY_SELECTOR_REAL_QT: PASS")
        print("PROJECT_WEB_AI_DIRECT_PROVIDER_SELECTOR_REAL_QT: PASS")
        print("PROJECT_WEB_AI_MODEL_SELECTOR_REAL_QT: PASS")
        print("PROJECT_WEB_AI_SELECTOR_SINGLE_OWNER_REAL_QT: PASS")
    finally:
        tab.close()
        tab.deleteLater()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()


def main() -> int:
    """Run focused static and real-widget validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    validate_static(root)
    validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
