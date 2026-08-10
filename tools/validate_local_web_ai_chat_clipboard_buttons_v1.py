"""Validate visible Paste/Copy text buttons in Local AI and Project Web AI."""

from __future__ import annotations

import argparse
import os
import py_compile
import sys
import time
from pathlib import Path

FEATURE_ID = "local-web-ai-chat-clipboard-buttons-v1"
FILES = (
    "kanda_reasoner_app/reasoner_engine/chat_clipboard_actions.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/local_ai_clipboard_actions.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_clipboard_actions.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/signal_wiring.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def static_checks(root: Path) -> None:
    for rel in FILES:
        path = root / rel
        require(path.is_file(), "Missing clipboard source: " + rel)
        py_compile.compile(str(path), doraise=True)
        require(len(path.read_text(encoding="utf-8").splitlines()) <= 500,
                "Source module exceeds 500 lines: " + rel)
    local_ui = (root / FILES[3]).read_text(encoding="utf-8")
    web_ui = (root / FILES[5]).read_text(encoding="utf-8")
    web_chat = (root / FILES[6]).read_text(encoding="utf-8")
    require('QPushButton("Paste")' in local_ui, "Local Paste button missing")
    require('QPushButton("Copy")' in local_ui, "Local draft Copy button missing")
    require('QPushButton("Copy question")' in local_ui,
            "Local selected-question Copy button missing")
    require('QPushButton("Copy answer")' in local_ui,
            "Local answer Copy button missing")
    require('QPushButton("Paste")' in web_ui, "Web Paste button missing")
    require('QPushButton("Copy")' in web_ui, "Web draft Copy button missing")
    require('"Project Conversation"' in web_ui and '"Web Advisory Config"' in web_ui,
            "Web AI two-subtab layout was not preserved")
    require("web_access_combo" in web_ui and "web_provider_combo" in web_ui
            and "web_model_combo" in web_ui,
            "Web AI provider/model selectors were not preserved")
    require("render_project_web_ai_message_html" in web_chat,
            "Web per-message Copy renderer missing")
    require("connect_project_web_ai_clipboard_actions" in web_chat,
            "Web clipboard actions are not connected")
    print("CHAT_CLIPBOARD_BUTTONS_STATIC: PASS")
    print("CHAT_CLIPBOARD_MODULE_SIZE: PASS")


def real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        from PySide6.QtCore import QThread, QUrl
        from PySide6.QtWidgets import QApplication, QPushButton
    except ModuleNotFoundError:
        print("LOCAL_WEB_AI_CHAT_CLIPBOARD_REAL_QT: SKIPPED_NO_PYSIDE6")
        return
    from kanda_reasoner_app.local_ai_configuration import (
        LocalAIConfigurationController,
        install_application_local_ai_configuration,
    )

    class MemorySettings:
        def __init__(self) -> None:
            self.values: dict[str, object] = {}
        def value(self, key: str, default: object = None) -> object:
            return self.values.get(key, default)
        def setValue(self, key: str, value: object) -> None:
            self.values[key] = value

    class FakeRegistry:
        def __init__(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
        def list_models(self) -> list[str]:
            return ["fake-local-model"]

    app = QApplication.instance() or QApplication([])
    controller = LocalAIConfigurationController(
        app, settings=MemorySettings(), registry_factory=FakeRegistry
    )
    install_application_local_ai_configuration(controller)

    import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window as local_module
    from kanda_reasoner_app.reasoner_engine.v10_models import ConversationTurn, RetrievalBundle
    local_module.LocalModelRegistry = FakeRegistry
    local = local_module.JsonProjectReasonerV10()
    deadline = time.monotonic() + 3.0
    while controller._catalog_thread is not None and time.monotonic() < deadline:
        app.processEvents()
        QThread.msleep(10)
    app.processEvents()

    for name in (
        "paste_question_button", "copy_draft_button",
        "copy_history_question_button", "copy_answer_button",
    ):
        require(isinstance(getattr(local, name), QPushButton),
                "Missing Local AI clipboard button: " + name)
    app.clipboard().setText("clipboard local")
    local.question_edit.setText("start ")
    local.question_edit.setCursorPosition(len(local.question_edit.text()))
    local.paste_question_button.click()
    require(local.question_edit.text() == "start clipboard local",
            "Local Paste did not insert at the question cursor")
    local.copy_draft_button.click()
    require(app.clipboard().text() == "start clipboard local",
            "Local draft Copy failed")

    local.memory.add_turn(ConversationTurn(
        question="stored local question", answer="stored local answer",
        prompt="prompt", retrieval=RetrievalBundle(), selected_model="fake-local-model"
    ))
    local.answer_presenter.refresh_history_list(local)
    local.history_list.setCurrentRow(0)
    app.processEvents()
    local.copy_history_question_button.click()
    require(app.clipboard().text() == "stored local question",
            "Local selected-question Copy failed")
    local.answer_box.setPlainText("visible local answer")
    local.copy_answer_button.click()
    require(app.clipboard().text() == "visible local answer",
            "Local answer Copy failed")
    print("LOCAL_AI_CHAT_CLIPBOARD_REAL_QT: PASS")

    from kanda_reasoner_app.reasoner_engine.project_web_ai_conversations import (
        _ChatMessage,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab
    web = ProjectWebAITab()
    require(web.web_ai_subtabs.count() == 2,
            "Web AI two-subtab layout regressed")
    require(web.web_access_combo is not None and web.web_provider_combo is not None
            and web.web_model_combo is not None,
            "Web AI provider/model selectors regressed")
    for name in ("paste_question_button", "copy_question_button"):
        require(isinstance(getattr(web, name), QPushButton),
                "Missing Web AI clipboard button: " + name)
    app.clipboard().setText("clipboard web")
    web.question_edit.setPlainText("start ")
    cursor = web.question_edit.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    web.question_edit.setTextCursor(cursor)
    web.paste_question_button.click()
    require(web.question_edit.toPlainText() == "start clipboard web",
            "Web Paste did not insert at the question cursor")
    web.copy_question_button.click()
    require(app.clipboard().text() == "start clipboard web",
            "Web draft Copy failed")

    session = web._active_chat()
    session.messages = [
        _ChatMessage(role="user", content="sent web question"),
        _ChatMessage(role="assistant", content="returned web answer"),
    ]
    web._render_active_chat()
    source = web.answer_box.toHtml()
    require(source.count("copy-message-") >= 2,
            "Web message cards do not expose Copy actions")
    web.answer_box.anchorClicked.emit(QUrl("copy-message-0"))
    require(app.clipboard().text() == "sent web question",
            "Web sent-question Copy failed")
    web.answer_box.anchorClicked.emit(QUrl("copy-message-1"))
    require(app.clipboard().text() == "returned web answer",
            "Web answer Copy failed")
    print("WEB_AI_CHAT_CLIPBOARD_REAL_QT: PASS")
    print("WEB_AI_EACH_MESSAGE_COPY_REAL_QT: PASS")

    web.close()
    local.close()
    app.processEvents()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    static_checks(root)
    real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
