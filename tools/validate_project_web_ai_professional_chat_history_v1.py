# project-path: tools/validate_project_web_ai_professional_chat_history_v1.py
"""Validate the professional Project Web AI UI and memory-only chat list."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "project-web-ai-professional-chat-history-v1"
CONTROLLER = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
UI = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
THEME = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_theme.py"
CREDENTIALS = "kanda_reasoner_app/web_ai_credentials.py"
CONVERSATIONS = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py"
)
VALIDATOR = "tools/validate_project_web_ai_professional_chat_history_v1.py"
TOUCHED_CODE = (CONTROLLER, UI, THEME, CONVERSATIONS, CREDENTIALS, VALIDATOR)


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    """Return one exact source fingerprint."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static_contract(root: Path) -> None:
    """Validate professional design, history, and owner boundaries."""
    controller = (root / CONTROLLER).read_text(encoding="utf-8")
    ui = (root / UI).read_text(encoding="utf-8")
    theme = (root / THEME).read_text(encoding="utf-8")
    conversations = (root / CONVERSATIONS).read_text(encoding="utf-8")
    credentials = (root / CREDENTIALS).read_text(encoding="utf-8")
    config_ui = (root / "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py").read_text(encoding="utf-8")

    required_ui = (
        'setObjectName("projectWebAIChatList")',
        'setObjectName("projectWebAINewChatButton")',
        'QTextBrowser()',
        'QStyle.StandardPixmap.SP_ArrowUp',
        'owner.open_web_config_button = QPushButton("Open Config Web AI")',
        'owner.web_config_summary_value',
        'setObjectName("projectWebAIBadge")',
        'splitter.setSizes([360, 1180])',
        'Message Web AI',
    )
    for marker in required_ui:
        require(marker in ui, "missing professional UI marker: " + marker)
    for marker in ("_force_opaque_combo(self.gateway_combo)", "_force_opaque_combo(self.model_combo)"):
        require(marker in config_ui, "central Config Web AI popup contract missing: " + marker)

    required_theme = (
        'font-family: "Segoe UI Variable Text", "Segoe UI", sans-serif;',
        'QComboBox QAbstractItemView {',
        'background-color: #1d2128;',
        'QListWidget#projectWebAIChatList',
        'QPushButton#projectWebAISendButton',
        'background: #10a37f;',
        'QTextBrowser#projectWebAIConversation',
    )
    for marker in required_theme:
        require(marker in theme, "missing professional theme marker: " + marker)

    required_controller = (
        "ProjectWebAIChatHistoryMixin",
        "self._initialize_chat_history()",
        "self._connect_chat_history_signals()",
        "self._begin_chat_turn(question)",
        "def _event_is_current",
        "self._active_request_identity",
        "ProjectWebAIRequestIdentity",
        "build_project_messages",
        "application_web_ai_configuration",
        "self._web_config",
        "open_web_config_button",
    )
    for marker in required_controller:
        require(marker in controller, "missing controller contract: " + marker)

    require("HKEY_CURRENT_USER" in credentials, "shared Windows User lookup missing")
    require(
        "os.environ[clean_name] = value" in credentials,
        "shared credential owner does not update the current session",
    )

    required_conversations = (
        "class ProjectWebAIChatHistoryMixin",
        "class _ChatStore",
        "def new_chat",
        "def load_selected_chat",
        "def delete_selected_chat",
        "def save_selected_chat",
        "def _begin_chat_turn",
        "self.question_edit.clear()",
        "def _render_active_chat",
        "def _export_target_is_protected",
        "target.write_text(self._markdown_for(session), encoding=\"utf-8\")",
        "Project Support",
        "self._protected_export_roots()",
    )
    for marker in required_conversations:
        require(marker in conversations, "missing conversation contract: " + marker)

    forbidden_ui = (
        "urllib.request",
        "stream_chat_completion",
        "fetch_gateway_models",
        "load_project_web_ai_context",
        "write_text(",
        "write_bytes(",
    )
    for marker in forbidden_ui:
        require(marker not in ui, "presentation owns forbidden logic: " + marker)

    require("urllib.request" not in controller, "controller owns a second HTTP client")
    require("write_text(" not in controller, "controller writes files directly")
    require("write_bytes(" not in controller, "controller writes bytes directly")
    require("winreg.SetValueEx" not in controller, "credential persistence introduced")
    require("api_key_edit" not in conversations, "chat export can reach credential field")
    require("OPENROUTER_API_KEY" not in conversations, "chat export names a secret")

    tree = ast.parse(conversations, filename=CONVERSATIONS)
    write_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"write_text", "write_bytes"}
    ]
    require(len(write_calls) == 1, "automatic or duplicate chat persistence detected")

    print("PROFESSIONAL_FONT_AND_VISUAL_HIERARCHY: PASS")
    print("OPAQUE_GATEWAY_AND_MODEL_DROPDOWNS: PASS")
    print("CHAT_LIST_BELOW_NEW_CHAT: PASS")
    print("CHAT_LOAD_DELETE_SAVE_ACTIONS: PASS")
    print("MEMORY_ONLY_DEFAULT_PERSISTENCE: PASS")
    print("EXPLICIT_MARKDOWN_EXPORT_ONLY: PASS")
    print("TOOL_PROJECT_SUPPORT_DAILY_EXPORT_GUARD: PASS")
    print("PROVIDER_RUNTIME_UNCHANGED: PASS")
    print("WINDOWS_USER_KEY_RESOLUTION_PRESERVED: PASS")
    print("MCARD_STALE_RESULT_GUARD_PRESERVED: PASS")


def validate_module_sizes(root: Path) -> None:
    """Enforce strict physical-line limits for all touched source."""
    for relative in TOUCHED_CODE:
        path = root / relative
        require(path.is_file(), "missing touched source: " + relative)
        count = len(path.read_text(encoding="utf-8").splitlines())
        require(0 < count <= 500, f"module-size violation {relative}: {count}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _fake_context(project: Path, support: Path):
    """Return a bounded context fixture for widget-only tests."""
    from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot

    return ContextSnapshot(
        tool_project_slug="kanda_reasoner",
        tool_source_root=str(project.parent / "tool"),
        project_slug="demo",
        project_id="project-id-1",
        project_root=str(project),
        project_root_fingerprint="root-fingerprint-1",
        support_root=str(support),
        daily_work_root=str(project.parent / "demo_delete_after_daily_work"),
        self_hosting_mode=False,
        support_identity_status="VERIFIED",
        collector_status="CURRENT",
        snapshot_id="snapshot-1",
        context_hash="a" * 64,
        generated_at_utc="2026-07-19T00:00:00Z",
        trusted_boundary_text="Tool: kanda_reasoner\nActive Project: demo",
        context_text="UNTRUSTED PROJECT EVIDENCE\nfixture",
        context_bytes=32,
        artifacts_loaded=("demo__ai_briefing.json",),
        omitted_sections=("exact source files",),
    )


def _fake_request_identity(session_id: str):
    """Return one complete immutable Tool/Project request card."""
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ProjectWebAIRequestIdentity,
    )

    return ProjectWebAIRequestIdentity(
        request_id="request-1",
        session_id=session_id,
        project_id="project-id-1",
        project_slug="demo",
        project_root_fingerprint="root-fingerprint-1",
        support_root="",
        snapshot_id="snapshot-1",
        context_hash="a" * 64,
        gateway_id="openrouter",
        model_id="fixture/model",
        privacy_approval_id="approval-1",
        created_at_utc="2026-07-20T00:00:00Z",
        project_epoch=0,
    )


def _fake_result():
    """Return one provider result without network access."""
    from kanda_reasoner_app.web_ai_provider_contracts import ChatResult, ChatUsage

    return ChatResult(
        request_id="request-1",
        gateway_id="openrouter",
        requested_model="fixture/model",
        returned_model="fixture/model",
        content="The routing owner is isolated from the presentation layer.",
        finish_reason="stop",
        response_id="response-1",
        usage=ChatUsage(total_tokens=12, provider_name="fixture"),
    )


def validate_real_widget(root: Path) -> None:
    """Exercise the real widget without network or real credentials."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    from PySide6.QtCore import Qt
    from PySide6.QtGui import QPalette
    from PySide6.QtWidgets import QApplication, QMessageBox

    import kanda_reasoner_app.reasoner_engine.project_web_ai_conversations as chat_module
    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab
    from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration

    app = QApplication.instance() or QApplication([])
    config = ConfigWebAITab()
    controller = application_web_ai_configuration()
    widget = ProjectWebAITab()
    widget.resize(1400, 880)
    widget.show()
    app.processEvents()

    require(widget.chat_list.count() == 1, "initial chat was not created")
    require(widget.chat_list.currentRow() == 0, "initial chat is not selected")
    require(widget.answer_box.isReadOnly(), "conversation canvas is editable")
    require(widget.clear_button.text().endswith("New chat"), "New chat action missing")
    require(not widget.send_button.icon().isNull(), "send arrow icon missing")

    for combo in (config.gateway_combo, config.model_combo):
        popup = combo.view()
        viewport = popup.viewport()
        normalized_popup_style = "".join(popup.styleSheet().lower().split())
        normalized_viewport_style = "".join(viewport.styleSheet().lower().split())

        require(
            "background-color:#1d2128" in normalized_popup_style,
            "dropdown popup lacks a direct opaque background style",
        )
        require(
            "background-color:#1d2128" in normalized_viewport_style,
            "dropdown viewport lacks a direct opaque background style",
        )

        popup_base = popup.palette().color(QPalette.ColorRole.Base)
        popup_window = popup.palette().color(QPalette.ColorRole.Window)
        require(
            popup.testAttribute(Qt.WidgetAttribute.WA_StyledBackground),
            "dropdown popup does not opt into styled backgrounds",
        )
        require(
            popup.autoFillBackground(),
            "dropdown popup does not auto-fill its background",
        )
        require(popup_base.alpha() == 255, "dropdown popup Base is transparent")
        require(popup_window.alpha() == 255, "dropdown popup Window is transparent")

        viewport_base = viewport.palette().color(QPalette.ColorRole.Base)
        viewport_window = viewport.palette().color(QPalette.ColorRole.Window)
        require(
            viewport.testAttribute(Qt.WidgetAttribute.WA_StyledBackground),
            "dropdown viewport does not opt into styled backgrounds",
        )
        require(
            "background-color:#1d2128" in normalized_viewport_style,
            "dropdown viewport lacks its direct solid background contract",
        )
        require(
            viewport_base.alpha() == 255,
            "dropdown viewport Base is transparent",
        )
        require(
            viewport_window.alpha() == 255,
            "dropdown viewport Window is transparent",
        )
    print("REAL_OPAQUE_DROPDOWN_PALETTE: PASS")
    print("VIEWPORT_STYLESHEET_OPACITY_CONTRACT: PASS")
    print("PLATFORM_STABLE_DROPDOWN_VALIDATION: PASS")

    with tempfile.TemporaryDirectory(prefix="kanda_web_ai_chat_") as temporary:
        base = Path(temporary)
        project = base / "demo"
        support = base / "demo_show_project_to_AI"
        export_dir = base / "exports"
        project.mkdir()
        support.mkdir()
        export_dir.mkdir()

        widget.project_root_edit.blockSignals(True)
        widget.project_root_edit.setText(str(project))
        widget.project_root_edit.blockSignals(False)
        widget._context = _fake_context(project, support)
        widget._project_session.bind_snapshot(widget._context)
        from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor
        model = ModelDescriptor(
            gateway_id="openrouter",
            model_id="fixture/model",
            display_name="Fixture Model",
            free_status=True,
        )
        controller._all_models = [model]
        controller._selected_model_id = model.model_id
        controller._touch()
        selected_fixture = controller.selected_model()
        require(
            selected_fixture is not None
            and selected_fixture.model_id == model.model_id
            and selected_fixture.free_status,
            "central free-only fixture model is not visible",
        )
        print("CENTRAL_FREE_ONLY_FIXTURE_MODEL_VISIBLE: PASS")
        identity = _fake_request_identity(widget._active_chat().session_id)
        identity = identity.__class__(
            **{
                **identity.__dict__,
                "support_root": str(support),
                "project_epoch": widget._project_session.project_epoch,
            }
        )
        widget._active_request_identity = identity
        widget._active_config_revision = controller.snapshot().revision
        widget._active_question = "How does routing work?"
        widget.question_edit.setPlainText(widget._active_question)
        widget._begin_chat_turn(widget._active_question)

        require(not widget.question_edit.toPlainText(), "composer was not cleared")
        require("How does routing work?" in widget.answer_box.toPlainText(),
                "user question was not inserted into the chat log")
        require(widget.chat_list.item(0).text() != "New chat",
                "chat title was not derived from the first question")
        print("SEND_CLEARS_COMPOSER_AND_LOGS_USER_TURN: PASS")

        widget._request_mode = "prepare_changes"
        widget._on_chat_completed(identity, _fake_result())
        require(
            not widget._history,
            "Prepare Changes result entered normal chat model history",
        )
        print("PREPARE_CHANGES_RESULT_CANNOT_COMMIT_CHAT_HISTORY: PASS")

        widget._request_mode = "chat"
        widget._on_chat_completed(identity, _fake_result())
        require(len(widget._history) == 2, "completed pair was not added to model history")
        require("routing owner" in widget.answer_box.toPlainText(),
                "assistant response was not rendered in chat")
        print("NORMAL_CHAT_FIXTURE_MODE_BOUND: PASS")
        print("ASSISTANT_RESPONSE_COMMITS_TO_CHAT_LOG: PASS")

        completed_id = widget._active_chat_id
        widget._chat_thread = None
        widget.new_chat()
        require(widget.chat_list.count() == 2, "new chat was not listed")
        require("How does routing work?" not in widget.answer_box.toPlainText(),
                "new chat retained the prior transcript")
        require("Ask about your project" in widget.answer_box.toPlainText(),
                "new chat empty state is missing")

        for row in range(widget.chat_list.count()):
            item = widget.chat_list.item(row)
            if str(item.data(Qt.ItemDataRole.UserRole) or "") == completed_id:
                widget.chat_list.setCurrentRow(row)
                break
        widget.load_selected_chat()
        require(widget._active_chat_id == completed_id, "Load did not activate chat")
        require("How does routing work?" in widget.answer_box.toPlainText(),
                "loaded chat transcript is missing")
        print("CHAT_CREATE_LIST_AND_LOAD: PASS")

        export_path = export_dir / "saved-chat.md"
        original_dialog = chat_module.QFileDialog
        original_message_box = chat_module.QMessageBox

        class FakeDialog:
            @staticmethod
            def getSaveFileName(*_args, **_kwargs):
                return str(export_path), "Markdown files (*.md)"

        class FakeMessageBox:
            StandardButton = QMessageBox.StandardButton

            @staticmethod
            def warning(*_args, **_kwargs):
                return None

            @staticmethod
            def question(*_args, **_kwargs):
                return QMessageBox.StandardButton.Yes

        try:
            chat_module.QFileDialog = FakeDialog
            chat_module.QMessageBox = FakeMessageBox
            controller.set_api_key("secret-must-not-export")
            widget.save_selected_chat()
            require(export_path.is_file(), "Markdown export was not written")
            exported = export_path.read_text(encoding="utf-8")
            require("## You" in exported, "user role missing from Markdown")
            require("## Web AI" in exported,
                    "assistant role missing from Markdown")
            require("secret-must-not-export" not in exported,
                    "credential leaked into Markdown export")
            require(widget._export_target_is_protected(project / "chat.md"),
                    "project-source export guard failed")
            require(widget._export_target_is_protected(support / "chat.md"),
                    "Project Support export guard failed")
            require(
                widget._export_target_is_protected(
                    Path(widget._context.tool_source_root) / "chat.md"
                ),
                "Tool source export guard failed",
            )
            require(
                widget._export_target_is_protected(
                    Path(widget._context.daily_work_root) / "chat.md"
                ),
                "daily-work export guard failed",
            )
            print("USER_CHOSEN_MARKDOWN_EXPORT: PASS")
            print("MARKDOWN_EXPORT_EXCLUDES_CREDENTIALS: PASS")

            before_delete = widget.chat_list.count()
            widget.delete_selected_chat()
            require(widget.chat_list.count() == before_delete - 1,
                    "Delete did not remove selected chat")
            print("CHAT_DELETE_ACTION: PASS")
        finally:
            chat_module.QFileDialog = original_dialog
            chat_module.QMessageBox = original_message_box

    widget.close()
    config.close()
    app.processEvents()
    print("REAL_PROJECT_WEB_AI_PROFESSIONAL_CHAT_WIDGET: PASS")


def main() -> int:
    """Run static, real-widget, and source-immutability validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--static-only", action="store_true")
    arguments = parser.parse_args()

    root = Path(arguments.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    before = {relative: sha256(root / relative) for relative in TOUCHED_CODE}

    os.chdir(root)
    validate_static_contract(root)
    validate_module_sizes(root)
    if not arguments.static_only:
        validate_real_widget(root)

    after = {relative: sha256(root / relative) for relative in TOUCHED_CODE}
    require(before == after, "professional chat validation mutated Tool source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
