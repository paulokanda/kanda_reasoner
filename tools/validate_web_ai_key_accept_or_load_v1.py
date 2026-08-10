# project-path: tools/validate_web_ai_key_accept_or_load_v1.py
"""Validate dual pasted-key and environment-key button behavior."""

from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

FEATURE_ID = "web-ai-key-accept-or-load-v1"


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def source(root: Path, relative: str) -> str:
    """Read one UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate the source-level UX and secret-safety contract."""
    paths = (
        "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",
        "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py",
    )
    for relative in paths:
        text = source(root, relative)
        ast.parse(text, filename=relative)
        require(text.isascii(), "non-ASCII source: " + relative)
        require(
            'QPushButton("Use Key / Load Environment")' in text,
            "dual-purpose button label missing: " + relative,
        )
        require(
            "def _accept_or_load_key(self)" in text,
            "dual-purpose handler missing: " + relative,
        )
        require(
            "pasted_key = self.api_key_edit.text().strip()" in text,
            "pasted-key branch missing: " + relative,
        )
        require(
            "self._controller.load_environment_key()" in text,
            "environment fallback missing: " + relative,
        )
        require("QMessageBox" not in text, "blocking key popup remains: " + relative)
        require(len(text.splitlines()) <= 500, "module exceeds 500 lines: " + relative)
    help_text = source(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/config_ai.md",
    )
    require("Use Key / Load Environment" in help_text, "help label missing")
    require("blocking modal dialog" in help_text, "inline failure help missing")
    print("WEB_AI_KEY_DUAL_METHOD_STATIC: PASS")
    print("WEB_AI_KEY_BLOCKING_MODAL_ABSENT: PASS")
    print("WEB_AI_KEY_HELP_IN_SYNC: PASS")


def validate_real_qt(root: Path) -> None:
    """Exercise pasted, environment, and missing-key behavior in real Qt."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.reasoner_engine.config_direct_web_ai_tab import (
        ConfigDirectWebAITab,
    )
    from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
    from kanda_reasoner_app.web_ai_configuration import (
        WebAIConfigurationController,
        install_application_web_ai_configuration,
    )

    app = QApplication.instance() or QApplication([])
    controller = WebAIConfigurationController(app)
    install_application_web_ai_configuration(controller)
    direct = ConfigDirectWebAITab(controller=controller)
    gateway = ConfigWebAITab()
    old_gemini = os.environ.pop("GEMINI_API_KEY", None)
    old_openrouter = os.environ.pop("OPENROUTER_API_KEY", None)
    try:
        controller.set_gateway_id("gemini")
        direct._render_all()
        direct.api_key_edit.setText("manual-gemini-secret")
        direct.load_env_button.click()
        require(
            controller.api_key() == "manual-gemini-secret",
            "pasted Gemini key not accepted",
        )
        require(
            controller.credential_source() == "manual session field",
            "pasted Gemini source mismatch",
        )
        require(
            "Accepted the pasted API key" in direct.status_label.text(),
            "pasted Gemini status missing",
        )
        print("WEB_AI_PASTED_KEY_ACCEPTED: PASS")

        direct.api_key_edit.clear()
        os.environ["GEMINI_API_KEY"] = "environment-gemini-secret"
        direct.load_env_button.click()
        require(
            controller.api_key() == "environment-gemini-secret",
            "Gemini environment key not loaded",
        )
        require(
            controller.credential_source() == "current process",
            "Gemini environment source mismatch",
        )
        print("WEB_AI_ENVIRONMENT_KEY_LOADED: PASS")

        direct.api_key_edit.clear()
        os.environ.pop("GEMINI_API_KEY", None)
        direct.load_env_button.click()
        require(
            "was not found" in direct.status_label.text(),
            "missing Gemini key not reported inline",
        )
        require(
            all(widget.windowTitle() != "Environment key not found" for widget in app.topLevelWidgets()),
            "blocking missing-key dialog exists",
        )
        print("WEB_AI_MISSING_KEY_INLINE_STATUS: PASS")

        controller.set_gateway_id("openrouter")
        gateway._render_all()
        gateway.api_key_edit.setText("manual-openrouter-secret")
        gateway.load_env_button.click()
        require(
            controller.api_key() == "manual-openrouter-secret",
            "pasted gateway key not accepted",
        )
        print("WEB_AI_GATEWAY_KEY_DUAL_METHOD: PASS")
        print("WEB_AI_KEY_ACCEPT_OR_LOAD_REAL_QT: PASS")
    finally:
        if old_gemini is not None:
            os.environ["GEMINI_API_KEY"] = old_gemini
        else:
            os.environ.pop("GEMINI_API_KEY", None)
        if old_openrouter is not None:
            os.environ["OPENROUTER_API_KEY"] = old_openrouter
        else:
            os.environ.pop("OPENROUTER_API_KEY", None)
        direct.close()
        gateway.close()
        direct.deleteLater()
        gateway.deleteLater()
        app.processEvents()


def main() -> int:
    """Run focused validation."""
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
