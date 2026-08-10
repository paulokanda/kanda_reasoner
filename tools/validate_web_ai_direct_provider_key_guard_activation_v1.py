# project-path: tools/validate_web_ai_direct_provider_key_guard_activation_v1.py
"""Validate direct-provider activation, key retention, and default free guard."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "web-ai-direct-provider-key-guard-activation-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    direct_rel = "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py"
    controller_rel = "kanda_reasoner_app/web_ai_configuration.py"
    direct = source(root, direct_rel)
    controller = source(root, controller_rel)
    for relative, text in ((direct_rel, direct), (controller_rel, controller)):
        ast.parse(text, filename=relative)
        require(text.isascii(), "non-ASCII source: " + relative)
        require(len(text.splitlines()) <= 500, "module exceeds 500 lines: " + relative)
    for token in (
        "def _activate_selected_provider(self)",
        "self._activate_selected_provider()",
        "selected_is_active",
        "The guard starts enabled by default",
        "Require an unbilled Gemini Free Tier project.",
    ):
        require(token in direct, "direct activation contract missing: " + token)
    require(
        "self._free_access_confirmations.get(self._gateway_id, True)" in controller,
        "default free-access guard missing",
    )
    print("DIRECT_PROVIDER_DISPLAY_SELECTION_ACTIVATION_STATIC: PASS")
    print("DIRECT_PROVIDER_DEFAULT_FREE_GUARD_STATIC: PASS")


def validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.reasoner_engine.config_direct_web_ai_tab import (
        ConfigDirectWebAITab,
    )
    from kanda_reasoner_app.web_ai_configuration import (
        WebAIConfigurationController,
        install_application_web_ai_configuration,
    )

    app = QApplication.instance() or QApplication([])
    controller = WebAIConfigurationController(app)
    install_application_web_ai_configuration(controller)
    direct = ConfigDirectWebAITab(controller=controller)
    try:
        require(controller.gateway_id() == "openrouter", "baseline provider mismatch")
        require(direct.provider_combo.currentData() == "gemini", "Gemini not displayed")
        require(direct.free_access_checkbox.isEnabled(), "guard unavailable before activation")
        require(direct.free_access_checkbox.isChecked(), "guard not checked by default")
        print("DIRECT_PROVIDER_FREE_GUARD_AVAILABLE_DEFAULT_CHECKED: PASS")

        secret = "manual-gemini-secret"
        direct.api_key_edit.setText(secret)
        direct.load_env_button.click()
        require(controller.gateway_id() == "gemini", "displayed Gemini not activated")
        require(controller.api_key() == secret, "pasted Gemini key not accepted")
        require(direct.api_key_edit.text() == secret, "accepted key disappeared from masked field")
        require(
            "Key loaded for this session" in direct.credential_status.text(),
            "loaded-key confirmation missing",
        )
        require(direct.free_access_checkbox.isEnabled(), "active guard unavailable")
        require(direct.free_access_checkbox.isChecked(), "active guard not checked")
        require(controller.free_access_confirmed(), "controller guard not enabled")
        print("DIRECT_PROVIDER_PASTED_KEY_ACTIVATES_DISPLAYED_PROVIDER: PASS")
        print("DIRECT_PROVIDER_ACCEPTED_KEY_REMAINS_MASKED_VISIBLE: PASS")

        direct.free_access_checkbox.setChecked(False)
        app.processEvents()
        require(not controller.free_access_confirmed(), "explicit guard disable ignored")
        controller.set_gateway_id("mistral")
        require(controller.free_access_confirmed(), "new provider guard not defaulted on")
        controller.set_gateway_id("gemini")
        require(not controller.free_access_confirmed(), "explicit provider guard choice lost")
        print("DIRECT_PROVIDER_FREE_GUARD_EXPLICIT_OVERRIDE_PRESERVED: PASS")
        print("WEB_AI_DIRECT_PROVIDER_KEY_GUARD_REAL_QT: PASS")
    finally:
        direct.close()
        direct.deleteLater()
        app.processEvents()


def main() -> int:
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
