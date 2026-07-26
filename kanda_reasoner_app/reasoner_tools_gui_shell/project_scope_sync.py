# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py
"""Canonical active-Project synchronization and transient UI reset helpers."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QListWidget,
    QPlainTextEdit,
    QTableWidget,
    QTextEdit,
    QTreeWidget,
    QWidget,
)

__all__ = [
    "PROJECT_SCOPED_TAB_IDS",
    "ProjectSwitchBlock",
    "apply_project_root_to_widget",
    "project_switch_block",
    "reset_project_scoped_widget",
]


PROJECT_SCOPED_TAB_IDS = frozenset(
    {
        "architecture_review",
        "workflow_review",
        "docstring_assistant",
        "project_structure_map",
        "project_structure_3d",
        "project_web_ai",
        "error_memory",
        "refactor_report",
        "project_qa",
        "freeze_feature_after_update",
        "exclusion_rules",
    }
)


@dataclass(frozen=True)
class ProjectSwitchBlock:
    """Describe one loaded tab that currently forbids a Project switch."""

    tab_id: str
    reason: str


def project_switch_block(
    tab_id: str,
    widget: QWidget,
) -> ProjectSwitchBlock | None:
    """Return a fail-closed block for unsafe active Project work."""
    if tab_id not in PROJECT_SCOPED_TAB_IDS:
        return None

    if tab_id == "project_web_ai":
        session = getattr(widget, "_project_session", None)
        if bool(getattr(session, "transaction_blocks_project_switch", False)):
            transaction_id = (
                str(getattr(session, "open_transaction_id", "") or "")
                or str(getattr(session, "unresolved_transaction_id", "") or "")
            )
            return ProjectSwitchBlock(
                tab_id,
                "Governed Apply transaction must settle first"
                + (": " + transaction_id if transaction_id else ""),
            )
        return None

    if tab_id == "error_memory":
        with contextlib.suppress(Exception):
            from kanda_reasoner_app.error_memory_gui._ai_correction_action import (
                _job_for,
            )

            if _job_for(widget) is not None:
                return ProjectSwitchBlock(
                    tab_id,
                    "Error Memory AI correction is still running",
                )

    if bool(getattr(widget, "_analysis_running", False)):
        return ProjectSwitchBlock(tab_id, "analysis is still running")

    freeze_thread = getattr(widget, "_local_freeze_ai_thread", None)
    if freeze_thread is not None:
        with contextlib.suppress(Exception):
            if freeze_thread.is_alive():
                return ProjectSwitchBlock(tab_id, "Freeze formulary AI is still running")

    for attr_name in (
        "_worker_thread",
        "_ai_review_thread",
        "_docstring_ai_thread",
        "_ai_correction_thread",
        "_thread",
    ):
        thread = getattr(widget, attr_name, None)
        if thread is None:
            continue
        running = False
        if callable(getattr(thread, "isRunning", None)):
            with contextlib.suppress(Exception):
                running = bool(thread.isRunning())
        elif callable(getattr(thread, "is_alive", None)):
            with contextlib.suppress(Exception):
                running = bool(thread.is_alive())
        else:
            # An unknown asynchronous owner fails closed until its lifecycle is
            # represented by a supported running-state facade.
            running = True
        if running:
            return ProjectSwitchBlock(
                tab_id,
                attr_name.removeprefix("_").replace("_", " ") + " is still running",
            )

    process = getattr(widget, "_process", None)
    if process is not None:
        running = True
        with contextlib.suppress(Exception):
            running = int(process.state()) != 0
        if running:
            return ProjectSwitchBlock(tab_id, "collector process is still running")

    return None


def apply_project_root_to_widget(widget: QWidget, project_root: Path) -> None:
    """Notify one loaded widget through its public Project-root facade."""
    setter = getattr(widget, "set_project_root", None)
    if callable(setter):
        setter(project_root)


def reset_project_scoped_widget(tab_id: str, widget: QWidget) -> None:
    """Clear only transient old-Project state from one loaded tab."""
    if tab_id not in PROJECT_SCOPED_TAB_IDS:
        return

    if tab_id == "project_web_ai":
        # Its frozen root-change lifecycle owns epoch invalidation, worker
        # settlement, chat/provenance clearing, Shadow cleanup, and stale result
        # rejection when the canonical field is updated.
        return

    _close_project_scoped_dialogs(widget)

    if tab_id == "error_memory":
        _reset_error_memory(widget)
    elif tab_id == "freeze_feature_after_update":
        _reset_freeze_tab(widget)
    elif tab_id == "project_qa":
        _reset_project_qa(widget)
    elif tab_id == "architecture_review":
        _reset_architecture(widget)
    elif tab_id == "docstring_assistant":
        _reset_docstrings(widget)

    _clear_project_text_surfaces(widget)
    _clear_project_collection_surfaces(widget)


def _close_project_scoped_dialogs(widget: QWidget) -> None:
    """Close known child dialogs that carry old Project identity."""
    for attr_name in (
        "_local_freeze_dialog",
        "_what_to_say_dialog",
        "_manual_review_dialog",
        "_change_preview_dialog",
        "_apply_confirmation_dialog",
    ):
        dialog = getattr(widget, attr_name, None)
        if dialog is None:
            continue
        with contextlib.suppress(Exception):
            dialog.close()
        with contextlib.suppress(Exception):
            setattr(widget, attr_name, None)


def _reset_error_memory(widget: QWidget) -> None:
    """Clear Error Memory editor/session state without deleting durable lessons."""
    try:
        from kanda_reasoner_app.error_memory_gui._window_sync import (
            clear_error_memory_work_windows,
        )

        clear_error_memory_work_windows(widget)
    except Exception:
        pass

    for attr_name in (
        "_dismissed_pending_intake_files",
        "_dismissed_pending_intake_lesson_ids",
        "_warned_duplicate_pending_intake_lesson_ids",
    ):
        value = getattr(widget, attr_name, None)
        with contextlib.suppress(Exception):
            value.clear()

    for attr_name, empty in (
        ("_last_dismissed_pending_intake_file", ""),
        ("_last_dismissed_pending_intake_lesson_id", ""),
        ("_last_dismissed_pending_intake_text", ""),
        ("_loaded_pending_intake_file", ""),
        ("_loaded_pending_intake_lesson_id", ""),
        ("_last_received_lesson", None),
        ("_selected_lesson_id", ""),
        ("_undo_deleted_lesson", None),
    ):
        with contextlib.suppress(Exception):
            setattr(widget, attr_name, empty)

    with contextlib.suppress(Exception):
        generation = int(
            getattr(widget, "_error_memory_ai_correction_generation", 0) or 0
        )
        widget._error_memory_ai_correction_generation = generation + 1


def _reset_freeze_tab(widget: QWidget) -> None:
    """Clear staged Freeze state without writing or deleting Project memory."""
    with contextlib.suppress(Exception):
        widget._set_pending_staged_action(None, None)

    poll_timer = getattr(widget, "_local_freeze_ai_poll_timer", None)
    if poll_timer is not None:
        with contextlib.suppress(Exception):
            poll_timer.stop()
        with contextlib.suppress(Exception):
            poll_timer.deleteLater()

    with contextlib.suppress(Exception):
        generation = int(getattr(widget, "_local_freeze_ai_generation", 0) or 0)
        widget._local_freeze_ai_generation = generation + 1

    for attr_name, empty in (
        ("_local_freeze_preview", None),
        ("_last_output_folder", None),
        ("_pending_staged_project_root", None),
        ("_pending_staged_action", None),
        ("_local_freeze_ai_request_id", None),
        ("_local_freeze_ai_identity", None),
        ("_local_freeze_ai_result_queue", None),
        ("_local_freeze_ai_poll_timer", None),
        ("_local_freeze_ai_thread", None),
        ("_what_to_say_text_edit", None),
    ):
        with contextlib.suppress(Exception):
            setattr(widget, attr_name, empty)

    status_label = getattr(widget, "status_label", None)
    with contextlib.suppress(Exception):
        status_label.setText("Not checked yet")


def _reset_project_qa(widget: QWidget) -> None:
    """Clear Local AI conversation and visual evidence for the old Project."""
    clear_memory = getattr(widget, "clear_memory", None)
    if callable(clear_memory):
        with contextlib.suppress(Exception):
            clear_memory()
    clear_visuals = getattr(widget, "clear_visuals_only", None)
    if callable(clear_visuals):
        with contextlib.suppress(Exception):
            clear_visuals()
    question = getattr(widget, "question_edit", None)
    with contextlib.suppress(Exception):
        question.clear()


def _reset_architecture(widget: QWidget) -> None:
    """Clear Architecture review targets and transient handoff state."""
    for attr_name, empty in (
        ("_large_module_targets", []),
        ("_large_module_target_index", -1),
        ("_large_module_target_source", "none"),
        ("_last_large_module_split_handoff", ""),
        ("_last_mode_run", ""),
    ):
        with contextlib.suppress(Exception):
            setattr(widget, attr_name, empty)


def _reset_docstrings(widget: QWidget) -> None:
    """Clear Docstring review identity and transient report state."""
    for attr_name, empty in (
        ("_review_items", []),
        ("_review_index", -1),
        ("_last_report_path", ""),
        ("_last_result", None),
    ):
        if hasattr(widget, attr_name):
            with contextlib.suppress(Exception):
                setattr(widget, attr_name, empty)


def _owned_surfaces(widget: QWidget, surface_type: type[QWidget]) -> list[QWidget]:
    """Return Qt descendants and direct Python-owned surfaces exactly once."""
    surfaces: list[QWidget] = []
    seen: set[int] = set()

    try:
        descendants = widget.findChildren(surface_type)
    except Exception:
        descendants = []

    direct_values = getattr(widget, "__dict__", {}).values()
    for candidate in (*descendants, *direct_values):
        if not isinstance(candidate, surface_type) or id(candidate) in seen:
            continue
        surfaces.append(candidate)
        seen.add(id(candidate))

    return surfaces


def _clear_project_text_surfaces(widget: QWidget) -> None:
    """Clear project-derived text surfaces, including direct widget owners."""
    for editor_type in (QPlainTextEdit, QTextEdit):
        for editor in _owned_surfaces(widget, editor_type):
            if bool(editor.property("kanda_preserve_across_project_switch")):
                continue
            with contextlib.suppress(Exception):
                editor.clear()


def _clear_project_collection_surfaces(widget: QWidget) -> None:
    """Clear project-derived collections without losing table headers."""
    for item_list in _owned_surfaces(widget, QListWidget):
        if bool(item_list.property("kanda_preserve_across_project_switch")):
            continue
        with contextlib.suppress(Exception):
            item_list.clear()

    for tree in _owned_surfaces(widget, QTreeWidget):
        if bool(tree.property("kanda_preserve_across_project_switch")):
            continue
        with contextlib.suppress(Exception):
            tree.clear()

    for table in _owned_surfaces(widget, QTableWidget):
        if bool(table.property("kanda_preserve_across_project_switch")):
            continue
        with contextlib.suppress(Exception):
            table.clearContents()
            table.setRowCount(0)
