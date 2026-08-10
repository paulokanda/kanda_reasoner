"""Validate that Paste keeps Local AI Ask and Web AI Send usable."""

from __future__ import annotations

import argparse
import os
import py_compile
import sys
from pathlib import Path

FEATURE_ID = "local-web-ai-paste-send-state-repair-v1"
FILES = (
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/local_ai_clipboard_actions.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_clipboard_actions.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/signal_wiring.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def static_checks(root: Path) -> None:
    for rel in FILES:
        path = root / rel
        require(path.is_file(), "Missing source: " + rel)
        py_compile.compile(str(path), doraise=True)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "Source module exceeds 500 lines: " + rel,
        )

    local_actions = (root / FILES[0]).read_text(encoding="utf-8")
    web_actions = (root / FILES[1]).read_text(encoding="utf-8")
    local_wiring = (root / FILES[2]).read_text(encoding="utf-8")
    web_tab = (root / FILES[3]).read_text(encoding="utf-8")

    require(
        'getattr(window, "_refresh_workflow_controls", None)' in local_actions,
        "Local Paste does not explicitly refresh the Ask gate",
    )
    require(
        'getattr(owner, "_update_send_state", None)' in web_actions,
        "Web Paste does not explicitly refresh the Send gate",
    )
    require(
        "ask_ai_button.clicked.connect(window.ask_local_ai)" in local_wiring,
        "Canonical Local AI Ask handler is not connected",
    )
    require(
        "send_button.clicked.connect(self.send_question)" in web_tab,
        "Canonical Web AI Send handler is not connected",
    )
    require(
        "lambda _checked=False: _paste_question(window)" in local_actions,
        "Local Paste signal is not tolerant of QPushButton.clicked(bool)",
    )
    require(
        "lambda _checked=False: _paste_question(owner)" in web_actions,
        "Web Paste signal is not tolerant of QPushButton.clicked(bool)",
    )
    print("PASTE_SEND_STATE_STATIC: PASS")
    print("PASTE_SEND_CANONICAL_HANDLERS_PRESERVED: PASS")
    print("PASTE_SEND_MODULE_SIZE: PASS")


def real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QLineEdit,
            QListWidget,
            QMainWindow,
            QPlainTextEdit,
            QPushButton,
            QTextBrowser,
            QWidget,
        )
    except ModuleNotFoundError:
        print("PASTE_SEND_STATE_REAL_QT: SKIPPED_NO_PYSIDE6")
        return

    from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.local_ai_clipboard_actions import (
        connect_local_ai_clipboard_actions,
    )
    from kanda_reasoner_app.reasoner_engine.project_web_ai_clipboard_actions import (
        connect_project_web_ai_clipboard_actions,
    )

    class Memory:
        def turns(self) -> tuple[object, ...]:
            return ()

    class LocalOwner(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.question_edit = QLineEdit()
            self.answer_box = QPlainTextEdit()
            self.history_list = QListWidget()
            self.paste_question_button = QPushButton("Paste")
            self.copy_draft_button = QPushButton("Copy")
            self.copy_history_question_button = QPushButton("Copy question")
            self.copy_answer_button = QPushButton("Copy answer")
            self.ask_ai_button = QPushButton("Send")
            self.memory = Memory()
            self.refresh_count = 0

        def _refresh_workflow_controls(self) -> None:
            self.refresh_count += 1
            self.ask_ai_button.setEnabled(bool(self.question_edit.text().strip()))

    class WebOwner(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.question_edit = QPlainTextEdit()
            self.answer_box = QTextBrowser()
            self.paste_question_button = QPushButton("Paste")
            self.copy_question_button = QPushButton("Copy")
            self.send_button = QPushButton("Send")
            self.status_value = QLabel()
            self.refresh_count = 0

        def _update_send_state(self) -> None:
            self.refresh_count += 1
            self.send_button.setEnabled(
                bool(self.question_edit.toPlainText().strip())
            )

        def _active_chat(self) -> object:
            class Chat:
                messages: list[object] = []
            return Chat()

    app = QApplication.instance() or QApplication([])

    local = LocalOwner()
    connect_local_ai_clipboard_actions(local)
    local.question_edit.clear()
    local._refresh_workflow_controls()
    require(not local.ask_ai_button.isEnabled(), "Local Ask should start disabled")
    local_before = local.refresh_count
    app.clipboard().setText("local pasted question")
    local.paste_question_button.click()
    app.processEvents()
    require(
        local.question_edit.text() == "local pasted question",
        "Local Paste did not populate the question",
    )
    require(
        local.refresh_count > local_before,
        "Local Paste did not recalculate the Ask gate",
    )
    require(local.ask_ai_button.isEnabled(), "Local Ask stayed disabled after Paste")
    local_clicks: list[bool] = []
    local.ask_ai_button.clicked.connect(lambda checked=False: local_clicks.append(bool(checked)))
    local.ask_ai_button.click()
    app.processEvents()
    require(len(local_clicks) == 1, "Local Ask did not emit after Paste")
    print("LOCAL_AI_PASTE_SEND_REAL_QT: PASS")

    web = WebOwner()
    connect_project_web_ai_clipboard_actions(web)
    web.question_edit.clear()
    web._update_send_state()
    require(not web.send_button.isEnabled(), "Web Send should start disabled")
    web_before = web.refresh_count
    app.clipboard().setText("web pasted question")
    web.paste_question_button.click()
    app.processEvents()
    require(
        web.question_edit.toPlainText() == "web pasted question",
        "Web Paste did not populate the question",
    )
    require(
        web.refresh_count > web_before,
        "Web Paste did not recalculate the Send gate",
    )
    require(web.send_button.isEnabled(), "Web Send stayed disabled after Paste")
    web_clicks: list[bool] = []
    web.send_button.clicked.connect(lambda checked=False: web_clicks.append(bool(checked)))
    web.send_button.click()
    app.processEvents()
    require(len(web_clicks) == 1, "Web Send did not emit after Paste")
    print("WEB_AI_PASTE_SEND_REAL_QT: PASS")
    print("PASTE_SEND_STATE_REAL_QT: PASS")

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
