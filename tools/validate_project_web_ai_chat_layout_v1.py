# project-path: tools/validate_project_web_ai_chat_layout_v1.py
"""Validate the Project Web AI conversation-first subtab layout."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

FEATURE_ID = "project-web-ai-chat-layout-v1"
UI = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
CONTROLLER = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
VALIDATOR = "tools/validate_project_web_ai_chat_layout_v1.py"
TOUCHED = (UI, VALIDATOR)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static(root: Path) -> None:
    ui = (root / UI).read_text(encoding="utf-8")
    controller = (root / CONTROLLER).read_text(encoding="utf-8")
    required = (
        'QTabWidget()',
        'setObjectName("projectWebAISubtabs")',
        '"Project Conversation"',
        '"Web Advisory Config"',
        'setObjectName("projectWebAIConversationPage")',
        'setObjectName("projectWebAIAdvisoryConfigPage")',
        'setObjectName("projectWebAISidebar")',
        'setObjectName("projectWebAIChatCanvas")',
        'setObjectName("projectWebAIConversation")',
        'setObjectName("projectWebAIComposer")',
        'QSplitter(Qt.Orientation.Horizontal)',
        'splitter.setSizes([320, 1200])',
        'background: #0d0d0d',
        'Message Web AI',
    )
    for marker in required:
        require(marker in ui, "missing conversation layout marker: " + marker)
    require(
        ui.index('tabs.addTab(_conversation_page(owner), "Project Conversation")')
        < ui.index('tabs.addTab(_advisory_config_page(owner), "Web Advisory Config")'),
        "conversation must be the first Web AI subtab",
    )
    forbidden = (
        "urllib.request",
        "stream_chat_completion",
        "fetch_gateway_models",
        "load_project_web_ai_context",
        "write_text(",
        "write_bytes(",
    )
    for marker in forbidden:
        require(marker not in ui, "presentation module owns forbidden logic: " + marker)
    for marker in (
        "_active_request_identity",
        "ProjectWebAIRequestIdentity",
        "_event_is_current",
        "load_project_web_ai_context",
        "build_project_messages",
        "QThread",
    ):
        require(marker in controller, "controller contract missing: " + marker)
    print("PROJECT_WEB_AI_CONVERSATION_SUBTAB_STATIC: PASS")
    print("PROJECT_WEB_AI_ADVISORY_SUBTAB_STATIC: PASS")
    print("PROJECT_WEB_AI_PRESENTATION_ONLY_BOUNDARY: PASS")

    for relative in TOUCHED:
        path = root / relative
        lines = len(path.read_text(encoding="utf-8").splitlines())
        require(0 < lines <= 500, f"module-size violation {relative}: {lines}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab

    app = QApplication.instance() or QApplication([])
    widget = ProjectWebAITab()
    widget.resize(1440, 900)
    widget.show()
    app.processEvents()

    require(widget.web_ai_subtabs.count() == 2, "Web AI subtab count mismatch")
    require(widget.web_ai_subtabs.tabText(0) == "Project Conversation", "chat tab label")
    require(widget.web_ai_subtabs.tabText(1) == "Web Advisory Config", "config tab label")
    require(widget.web_ai_subtabs.currentIndex() == 0, "conversation is not default")
    require(widget.conversation_page.isVisibleTo(widget), "conversation page hidden")
    require(
        widget.main_splitter.orientation() == Qt.Orientation.Horizontal,
        "conversation splitter is not horizontal",
    )
    require(widget.main_splitter.widget(0) is widget.sidebar_panel, "history is not left")
    require(widget.main_splitter.widget(1) is widget.chat_panel, "chat is not right")
    require(widget.sidebar_panel.maximumWidth() <= 360, "history panel too wide")
    require(widget.chat_panel.minimumWidth() >= 620, "chat canvas is not dominant")
    require(widget.answer_box.isReadOnly(), "conversation output must remain read-only")
    require(not widget.send_button.icon().isNull(), "send button icon missing")
    require(not widget.send_button.isEnabled(), "send must fail closed initially")
    require(
        not widget.conversation_page.isAncestorOf(widget.project_root_edit),
        "advisory controls leaked into conversation subtab",
    )
    print("REAL_QT_PROJECT_CONVERSATION_SUBTAB: PASS")
    print("REAL_QT_CONVERSATION_ONLY_SURFACE: PASS")
    print("REAL_QT_SEND_CONTROL_FAILS_CLOSED: PASS")

    widget.close()
    app.processEvents()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    before = {
        relative: sha256(root / relative)
        for relative in (*TOUCHED, CONTROLLER)
        if (root / relative).is_file()
    }
    os.chdir(root)
    validate_static(root)
    if not args.static_only:
        validate_real_qt()
    after = {relative: sha256(root / relative) for relative in before}
    require(before == after, "chat-layout validation mutated Tool source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
