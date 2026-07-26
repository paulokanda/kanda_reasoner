# project-path: tools/validate_project_web_ai_chat_layout_v1.py
"""Focused validation for the Project Web AI sidebar-and-chat layout."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

FEATURE_ID = "project-web-ai-chat-layout-v1"
UI_RELATIVE = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
CONTROLLER_RELATIVE = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
VALIDATOR_RELATIVE = "tools/validate_project_web_ai_chat_layout_v1.py"
TOUCHED_CODE = (UI_RELATIVE, VALIDATOR_RELATIVE)


def _assert(condition: bool, message: str) -> None:
    """Raise one focused validation error when a contract is false."""
    if not condition:
        raise AssertionError(message)


def _sha256(path: Path) -> str:
    """Return the exact SHA-256 of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_static_layout_contract(root: Path) -> None:
    """Validate source-level presentation and ownership boundaries."""
    ui_source = (root / UI_RELATIVE).read_text(encoding="utf-8")
    controller_source = (root / CONTROLLER_RELATIVE).read_text(encoding="utf-8")

    required_ui_markers = (
        'setObjectName("projectWebAITab")',
        'setObjectName("projectWebAISidebar")',
        'setObjectName("projectWebAIChatCanvas")',
        'setObjectName("projectWebAIConversation")',
        'setObjectName("projectWebAIComposer")',
        'setObjectName("projectWebAISendButton")',
        "QStyle.StandardPixmap.SP_ArrowUp",
        "QSplitter(Qt.Orientation.Horizontal)",
        "splitter.setSizes([360, 1180])",
        "background: #0d0d0d",
        "Message Web AI",
    )
    for marker in required_ui_markers:
        _assert(marker in ui_source, "missing chat-layout source marker: " + marker)

    forbidden_ui_markers = (
        "urllib.request",
        "stream_chat_completion",
        "fetch_gateway_models",
        "load_project_web_ai_context",
        "write_text(",
        "write_bytes(",
    )
    for marker in forbidden_ui_markers:
        _assert(marker not in ui_source, "presentation module owns forbidden logic: " + marker)

    required_controller_markers = (
        "_active_request_identity",
        "ProjectWebAIRequestIdentity",
        "_event_is_current",
        "load_project_web_ai_context",
        "build_project_messages",
        "QThread",
    )
    for marker in required_controller_markers:
        _assert(marker in controller_source, "existing controller contract missing: " + marker)

    _assert(
        "urllib.request" not in controller_source,
        "controller unexpectedly owns a second HTTP client",
    )
    print("CHATGPT_LIKE_LEFT_OPTIONS_LAYOUT: PASS")
    print("DOMINANT_BLACK_CHAT_CANVAS: PASS")
    print("UP_ARROW_SEND_CONTROL: PASS")
    print("PRESENTATION_ONLY_OWNER_BOUNDARY: PASS")
    print("BRICK_WALL_PROVIDER_RUNTIME_UNCHANGED: PASS")
    print("MCARD_STALE_RESULT_GUARD_PRESERVED: PASS")


def _validate_module_sizes(root: Path) -> None:
    """Enforce the project's strict physical-line delivery constraint."""
    for relative in TOUCHED_CODE:
        path = root / relative
        _assert(path.is_file(), "missing touched source: " + relative)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        _assert(
            0 < line_count <= 500,
            f"module-size violation {relative}: {line_count}",
        )
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _validate_real_widget() -> None:
    """Instantiate the real widget and verify visible layout contracts."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab

    app = QApplication.instance() or QApplication([])
    widget = ProjectWebAITab()
    widget.resize(1320, 820)
    widget.show()
    app.processEvents()

    _assert(widget.objectName() == "projectWebAITab", "tab object identity mismatch")
    _assert(
        widget.main_splitter.orientation() == Qt.Orientation.Horizontal,
        "main splitter is not horizontal",
    )
    _assert(widget.main_splitter.widget(0) is widget.sidebar_panel, "sidebar is not left")
    _assert(widget.main_splitter.widget(1) is widget.chat_panel, "chat canvas is not right")
    _assert(widget.sidebar_panel.maximumWidth() <= 410, "sidebar is not bounded")
    _assert(widget.chat_panel.minimumWidth() >= 620, "chat canvas is not dominant")
    _assert(widget.answer_box.objectName() == "projectWebAIConversation", "answer identity")
    _assert(widget.answer_box.isReadOnly(), "conversation output must remain read-only")
    _assert(widget.question_edit.objectName() == "projectWebAIComposer", "composer identity")
    _assert(not widget.send_button.icon().isNull(), "send control has no up-arrow icon")
    _assert(
        widget.send_button.accessibleName() == "Send to Web AI",
        "send arrow lacks accessible action name",
    )
    _assert(widget.send_button.width() == 44, "send arrow width changed")
    _assert(widget.send_button.height() == 44, "send arrow height changed")
    _assert(not widget.send_button.isEnabled(), "send must remain fail-closed initially")
    _assert(hasattr(widget, "open_web_config_button"), "Config Web AI shortcut was lost")
    _assert("Open Config Web AI" in widget.open_web_config_button.text(), "central config action missing")
    _assert(not hasattr(widget, "gateway_combo"), "duplicate gateway controls remain in Project Web AI")
    _assert("#0d0d0d" in widget.styleSheet(), "dark chat theme is not installed")

    widget.close()
    app.processEvents()
    print("REAL_PROJECT_WEB_AI_CHAT_LAYOUT_WIDGET: PASS")
    print("LEFT_SIDEBAR_RIGHT_CHAT_ORDER: PASS")
    print("SEND_CONTROL_FAILS_CLOSED: PASS")


def main() -> int:
    """Run static, real-widget, and source-immutability validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--static-only", action="store_true")
    arguments = parser.parse_args()

    root = Path(arguments.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    before = {
        relative: _sha256(root / relative)
        for relative in (*TOUCHED_CODE, CONTROLLER_RELATIVE)
        if (root / relative).is_file()
    }

    os.chdir(root)
    _validate_static_layout_contract(root)
    _validate_module_sizes(root)
    if not arguments.static_only:
        _validate_real_widget()

    after = {relative: _sha256(root / relative) for relative in before}
    _assert(before == after, "chat-layout validation mutated Tool source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
