# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_qa_copy_error_ask_controller.py
"""Copyable error handling for Project Q&A Ask Local AI.

This helper owns the Project Q&A ask-button error presentation path. It keeps
the large main window module untouched and routes ask-time errors through a
floating Copy and Close window so diagnostics can be pasted into an AI chat.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.project_json_path_resolver import (
    current_project_root_from_window,
    resolve_project_json_path,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.session_service import (
    SessionExecutionError,
)
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

__all__ = [
    "ask_local_ai_with_copy_errors",
    "install_project_qa_copy_error_ask_handler",
]


def _widget_text(widget: Any) -> str:
    """Return stripped widget text without assuming a concrete Qt type."""
    if widget is None:
        return ""
    text_attr = getattr(widget, "text", None)
    if callable(text_attr):
        return str(text_attr()).strip()
    return str(widget).strip()




def _selected_local_ai_model(window: Any) -> str:
    """Return the global Config Local AI model without using a UI selector."""
    resolver = getattr(window, "selected_local_ai_model", None)
    if callable(resolver):
        return str(resolver() or "").strip()
    controller = getattr(window, "_local_ai_configuration", None)
    snapshot = controller.snapshot() if controller is not None else None
    return str(getattr(snapshot, "model_id", "") or "").strip()

def _expected_json_detail(window: Any) -> str:
    """Return diagnostic path details for the selected Project Q&A root."""
    project_root = current_project_root_from_window(window)
    if project_root is None:
        return "Selected project root: not set"

    try:
        resolution = resolve_project_json_path(project_root)
    except Exception as exc:
        return (
            "Selected project root: "
            + str(project_root)
            + "\nProject Q&A JSON resolution failed: "
            + str(exc)
        )

    folder = Path(resolution.canonical_json.parent)
    if folder.is_dir():
        names = sorted(path.name for path in folder.glob("*.json"))[:25]
        found_text = ", ".join(names) if names else "none"
    else:
        found_text = "folder does not exist"

    return (
        "Selected project root: "
        + str(project_root)
        + "\nExpected local-AI JSON: "
        + str(resolution.local_ai_json)
        + "\nExpected canonical JSON: "
        + str(resolution.canonical_json)
        + "\nEvidence folder: "
        + str(folder)
        + "\nJSON files currently found there: "
        + found_text
    )


def _show_project_qa_error(window: Any, *, title: str, message: str) -> None:
    """Show a copy-and-close diagnostic floating window."""
    path_text = _widget_text(getattr(window, "json_path_edit", None))
    question_text = _widget_text(getattr(window, "question_edit", None))
    model_text = _selected_local_ai_model(window)
    detail = (
        "Error message:\n"
        + str(message)
        + "\n\nCurrent JSON field: "
        + (path_text or "not set")
        + "\nCurrent question: "
        + (question_text or "not set")
        + "\nSelected model: "
        + (model_text or "not set")
        + "\n\n"
        + _expected_json_detail(window)
    )
    try:
        append_log = getattr(window, "_append_log", None)
        if callable(append_log):
            append_log(title + ": " + str(message))
    except Exception:
        pass

    dialog = show_error_copy_close_window(
        window,
        title=title,
        message=str(message),
        detail_text=detail,
        clipboard_text=title + "\n\n" + detail,
        button_text="Copy and Close",
        modal=True,
    )
    try:
        window._project_qa_error_dialog = dialog
    except Exception:
        pass


def _session_error_title(message: str) -> str:
    """Return a stable title for a Local AI session error."""
    if message == "No relevant evidence was retrieved.":
        return "Local AI no evidence"
    if message == "Please load a JSON file first.":
        return "Local AI JSON not loaded"
    if message == "Please type a question.":
        return "Local AI question missing"
    if message == "Please select a model.":
        return "Local AI model missing"
    return "Local AI session error"


def ask_local_ai_with_copy_errors(window: Any) -> None:
    """Run Ask Local AI with copyable diagnostic error windows."""
    if bool(getattr(window, "_analysis_running", False)):
        _show_project_qa_error(
            window,
            title="Local AI analysis running",
            message="Please wait for the current analysis to finish.",
        )
        return

    question = window.question_edit.text().strip()
    selected_model = _selected_local_ai_model(window)

    try:
        window.runtime_controller.ensure_project_json_loaded_for_question(window)
    except Exception as exc:
        _show_project_qa_error(
            window,
            title="Local AI JSON load failed",
            message=str(exc),
        )
        return

    try:
        result = window.session_service.execute(window, question, selected_model)
    except SessionExecutionError as exc:
        message = str(exc)
        _show_project_qa_error(
            window,
            title=_session_error_title(message),
            message=message,
        )
        return

    for line in result.log_messages:
        window._append_log(line)

    window._last_bundle = result.bundle
    window._last_prompt = result.prompt
    window._last_selected_model = result.selected_model
    window._pending_question = result.question

    window.answer_presenter.populate_evidence_lists(window, result.bundle)
    window.prompt_preview.setPlainText(result.prompt)

    if result.route == "ranked":
        window.answer_box.setPlainText(result.answer_text)
        window.prompt_preview.clear()
        return

    window.answer_box.setPlainText(result.answer_text)
    window.ai.ask(result.prompt, result.selected_model)


def install_project_qa_copy_error_ask_handler(window: Any) -> Callable[[], None]:
    """Install the copy-error Ask handler on one Project Q&A window."""
    def _ask_local_ai() -> None:
        ask_local_ai_with_copy_errors(window)

    window.ask_local_ai = _ask_local_ai
    return _ask_local_ai
