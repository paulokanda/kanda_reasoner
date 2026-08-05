# project-path: kanda_reasoner_app/error_memory_gui/_intake_actions_mixin.py
"""Pending-intake and general action mixin for the Error Memory tab.

This module extracts low/medium-risk wrappers while preserving their original
method names for helper-module compatibility.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root
from kanda_reasoner_app.error_memory_gui._clipboard_export import (
    copy_ai_assisted_intake_error_draft_to_clipboard,
    copy_error_lesson_intake_blueprint_to_clipboard,
    show_action_done,
)
from kanda_reasoner_app.error_memory_gui._correction_guard import (
    active_ready_missing_text,
    apply_heuristic_correction_to_error_editor,
    check_against_lessons,
    heuristic_correction_result_for_editor,
    operation_phase_for_guard,
    show_repeat_guard_report,
)
from kanda_reasoner_app.error_memory_gui._intake_blueprint import (
    error_lesson_intake_blueprint_clipboard_text,
    read_error_memory_intake_template_file,
)
from kanda_reasoner_app.error_memory_gui._memorize_flow import (
    candidate_text_for_memorize,
    clear_ai_assisted_intake_after_memorize,
    consume_loaded_pending_intake_file_if_matches,
    memorize_error_from_text_window,
    resolve_duplicate_memorize_candidate,
    save_active_ready_lesson,
)
from kanda_reasoner_app.error_memory_gui._pending_loader import (
    delete_pending_file_quietly,
    lesson_id_exists_in_lessons,
    load_pending_ai_assisted_error_lesson_intake,
    load_pending_ai_assisted_error_lesson_intake_now as load_pending_ai_assisted_error_lesson_intake_now_impl,
    show_duplicate_pending_intake_warning,
)
from kanda_reasoner_app.error_memory_gui._pending_rows import draft_lesson_from_pending_raw_text
from kanda_reasoner_app.error_memory_gui._pending_sources import (
    candidate_pending_ai_assisted_intake_dirs,
    delete_matching_pending_intake_files,
    pending_file_matches_draft_identity,
    pending_intake_files_for_candidate_dirs,
    safe_pending_lesson_id_from_file,
)
from kanda_reasoner_app.error_memory_gui._project_roots import existing_directory_from_text
from kanda_reasoner_app.error_memory_gui._table_view import (
    lesson_json_text_for_windows,
    set_ai_assisted_intake_and_error_editor_from_pending_text,
)
from kanda_reasoner_app.error_memory_gui._text_payloads import (
    json_payload_from_text,
    lesson_id_from_text_lenient,
    pending_file_updated_text,
    summary_from_pending_raw_text,
    validation_evidence_is_passing,
)
from kanda_reasoner_app.error_memory_gui._lesson_actions import undo_lesson_action

PENDING_AI_ASSISTED_INTAKE_DIR_NAME = 'pending_ai_assisted_error_lesson_intake'
PENDING_AI_ASSISTED_INTAKE_SUFFIXES = {'.json', '.txt', '.md'}

__all__ = [
    'ErrorMemoryIntakeActionsMixin',
    'PENDING_AI_ASSISTED_INTAKE_DIR_NAME',
    'PENDING_AI_ASSISTED_INTAKE_SUFFIXES',
]


class ErrorMemoryIntakeActionsMixin:
    """Pending-intake and general action wrappers for ErrorMemoryTab."""

    def _existing_directory_from_text(cls, text: str) -> Path | None:
        """Return a safe existing project source directory, or None."""
        return existing_directory_from_text(
            text,
            pending_dir_name=PENDING_AI_ASSISTED_INTAKE_DIR_NAME,
        )

    def _show_action_done(self, title: str, message: str, detail_text: str='') -> None:
        """Support show action done behavior.
        
        Parameters
        ----------
        title : str
            The title value.
        message : str
            The message text.
        detail_text : str, optional
            The optional detail text value.
        """
        
        show_action_done(self, title, message, detail_text)

    def _pending_ai_assisted_error_lesson_intake_dir(self) -> Path:
        """Return the primary pending intake folder for the selected Project."""
        return resolve_project_error_memory_root(self._require_project_root()) / PENDING_AI_ASSISTED_INTAKE_DIR_NAME

    def _candidate_pending_ai_assisted_intake_dirs(self) -> list[Path]:
        """Return pending-intake folders only for the selected Project.

        No Project selected: pending intake scanning is disabled. This prevents
        the Tool source working directory from being mistaken for a Project.
        """
        root = self._current_project_root()
        if root is None:
            return []
        return candidate_pending_ai_assisted_intake_dirs(
            [root],
            pending_dir_name=PENDING_AI_ASSISTED_INTAKE_DIR_NAME,
        )

    def load_pending_ai_assisted_error_lesson_intake_now(self, project_root: str | Path | None=None) -> bool:
        """Load the pending ai assisted error lesson intake now.
        
        Parameters
        ----------
        project_root : str | Path | None, optional
            The project root path.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return load_pending_ai_assisted_error_lesson_intake_now_impl(self, project_root)

    def _load_pending_ai_assisted_error_lesson_intake(self, *, mirror_loaded_json_to_error_editor: bool=False) -> bool:
        """Support load pending ai assisted error lesson intake behavior.
        
        Parameters
        ----------
        mirror_loaded_json_to_error_editor : bool, optional
            The optional mirror loaded json to error editor value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return load_pending_ai_assisted_error_lesson_intake(
            self,
            mirror_loaded_json_to_error_editor=mirror_loaded_json_to_error_editor,
        )

    def _lesson_json_text_for_windows(self, lesson: dict[str, Any]) -> str:
        """Support lesson json text for windows behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return lesson_json_text_for_windows(lesson)

    def _set_ai_assisted_intake_and_error_editor_from_pending_text(self, formatted_text: str, lesson: dict[str, Any]) -> None:
        """Support set ai assisted intake and error editor from pending text behavior.
        
        Parameters
        ----------
        formatted_text : str
            The formatted text value.
        lesson : dict[str, Any]
            The lesson value.
        """
        
        set_ai_assisted_intake_and_error_editor_from_pending_text(self, formatted_text, lesson)

    def _read_error_memory_intake_template_file(self, filename: str) -> str:
        """Read one Error Memory intake prompt template from the active prompt library."""
        return read_error_memory_intake_template_file(
            self._current_project_root(),
            filename,
            module_file=__file__,
        )

    def _error_lesson_intake_blueprint_clipboard_text(self, *, context_text: str = "") -> str:
        """Return clipboard text that instructs AI how to create active-ready intake JSON."""
        return error_lesson_intake_blueprint_clipboard_text(
            self._current_project_root(),
            context_text=context_text,
            module_file=__file__,
        )

    def _copy_error_lesson_intake_blueprint_to_clipboard(self) -> None:
        """Support copy error lesson intake blueprint to clipboard behavior.
        """
        
        copy_error_lesson_intake_blueprint_to_clipboard(self)

    def _active_ready_missing_text(self, lesson: dict[str, Any], *, limit: int=20) -> str:
        """Support active ready missing text behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        limit : int, optional
            The optional limit value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return active_ready_missing_text(lesson, limit=limit)

    def _show_duplicate_pending_intake_warning(self, lesson_id: str, pending_file: Path) -> None:
        """Support show duplicate pending intake warning behavior.
        
        Parameters
        ----------
        lesson_id : str
            The lesson id value.
        pending_file : Path
            The pending file value.
        """
        
        show_duplicate_pending_intake_warning(self, lesson_id, pending_file)

    def _lesson_id_exists_in_lessons(self, lesson_id: str) -> bool:
        """Support lesson id exists in lessons behavior.
        
        Parameters
        ----------
        lesson_id : str
            The lesson id value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return lesson_id_exists_in_lessons(self, lesson_id)

    def _safe_pending_lesson_id_from_file(self, pending_file: Path) -> str:
        """Return a stable draft lesson_id for a raw pending intake file."""
        return safe_pending_lesson_id_from_file(pending_file)

    def _pending_file_updated_text(self, pending_file: Path) -> str:
        """Return a stable UTC mtime string for a pending file."""
        return pending_file_updated_text(pending_file)

    def _summary_from_pending_raw_text(self, text: str, pending_file: Path) -> str:
        """Return a short row summary for raw pending evidence."""
        return summary_from_pending_raw_text(text, pending_file)

    def _draft_lesson_from_pending_raw_text(self, pending_file: Path, raw_text: str) -> dict[str, Any]:
        """Build an editable draft lesson from a raw pending evidence file."""
        return draft_lesson_from_pending_raw_text(
            pending_file,
            raw_text,
            project_slug=self._require_project_root().name,
        )

    def _delete_pending_file_quietly(self, path: Path) -> bool:
        """Support delete pending file quietly behavior.
        
        Parameters
        ----------
        path : Path
            The file or folder path.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return delete_pending_file_quietly(path)

    def _heuristic_correction_result_for_editor(self):
        """Support heuristic correction result for editor behavior.
        """
        
        return heuristic_correction_result_for_editor(self)

    def _apply_heuristic_correction_to_error_editor(self) -> None:
        """Support apply heuristic correction to error editor behavior.
        """
        
        apply_heuristic_correction_to_error_editor(self)

    def _copy_ai_assisted_intake_error_draft_to_clipboard(self) -> None:
        """Support copy ai assisted intake error draft to clipboard behavior.
        """
        
        copy_ai_assisted_intake_error_draft_to_clipboard(self)

    def _dismiss_loaded_pending_intake_file_for_session(self) -> None:
        """Prevent the currently loaded pending source from reappearing this session."""
        marker = str(self._loaded_pending_intake_file or '').strip()
        lesson_id = str(self._loaded_pending_intake_lesson_id or '').strip()
        text = self.raw_error_edit.toPlainText().strip()
        if marker:
            self._dismissed_pending_intake_files.add(marker)
            self._last_dismissed_pending_intake_file = marker
        if lesson_id:
            self._dismissed_pending_intake_lesson_ids.add(lesson_id)
            self._last_dismissed_pending_intake_lesson_id = lesson_id
        if text:
            self._last_dismissed_pending_intake_text = text
        self._loaded_pending_intake_file = ''
        self._loaded_pending_intake_lesson_id = ''

    def _clean_both_work_windows_from_clean_button(self) -> None:
        """Clear intake and editor panes from either Clean button."""
        self._dismiss_loaded_pending_intake_file_for_session()
        self.raw_error_edit.clear()
        self.received_preview_edit.clear()
        self._last_received_lesson = None
        self._selected_lesson_id = ''
        self._refresh_heuristic_correction_button_state()

    def _clean_intake_window(self) -> None:
        """Clear both work windows and suppress the loaded pending source."""
        self._clean_both_work_windows_from_clean_button()

    def _lesson_id_from_text_lenient(self, text: str) -> str:
        """Return lesson_id from wrapped or raw JSON without active-ready checks."""
        return lesson_id_from_text_lenient(text)

    def _pending_intake_files_for_all_candidate_dirs(self) -> list[Path]:
        """Return all pending intake files visible to the loader."""
        return pending_intake_files_for_candidate_dirs(
            self._candidate_pending_ai_assisted_intake_dirs(),
            allowed_suffixes=PENDING_AI_ASSISTED_INTAKE_SUFFIXES,
        )

    def _pending_file_matches_draft_identity(self, path: Path, lesson_ids: set[str], visible_texts: list[str], explicit_paths: list[str]) -> bool:
        """Return whether one pending source belongs to the draft being deleted."""
        return pending_file_matches_draft_identity(path, lesson_ids, visible_texts, explicit_paths)

    def _delete_matching_pending_intake_files(self, lesson_ids: set[str], visible_texts: list[str], explicit_paths: list[str]) -> tuple[int, list[str]]:
        """Delete every staged pending intake file for the current draft."""
        deleted_count, failures, dismissed_markers = delete_matching_pending_intake_files(
            lesson_ids,
            visible_texts,
            explicit_paths,
            self._pending_intake_files_for_all_candidate_dirs(),
        )
        self._dismissed_pending_intake_files.update(dismissed_markers)
        return (deleted_count, failures)

    def _json_payload_from_text(self, text: str) -> dict[str, Any] | None:
        """Return one JSON object from a text window when possible."""
        return json_payload_from_text(text)

    def _candidate_text_for_memorize(self) -> tuple[str, str]:
        """Support candidate text for memorize behavior.
        
        Returns
        -------
        tuple[str, str]
            The tuple of values.
        """
        
        return candidate_text_for_memorize(self)

    def _save_active_ready_lesson(self, lesson: dict[str, Any], success_prefix: str) -> Path | None:
        """Support save active ready lesson behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        success_prefix : str
            The success prefix value.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        return save_active_ready_lesson(self, lesson, success_prefix)

    def _consume_loaded_pending_intake_file_if_matches(self, lesson: dict[str, Any], *, allow_lesson_id_change: bool=False) -> bool:
        """Support consume loaded pending intake file if matches behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        allow_lesson_id_change : bool, optional
            The optional allow lesson id change value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return consume_loaded_pending_intake_file_if_matches(self, lesson, allow_lesson_id_change=allow_lesson_id_change)

    def _clear_ai_assisted_intake_after_memorize(self, lesson: dict[str, Any]) -> None:
        """Support clear ai assisted intake after memorize behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        """
        
        clear_ai_assisted_intake_after_memorize(self, lesson)

    def _resolve_duplicate_memorize_candidate(self, lesson: dict[str, Any]):
        """Consume duplicate Memorize Error candidates before saving.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The candidate lesson.
        """

        return resolve_duplicate_memorize_candidate(self, lesson)

    def _memorize_error_from_text_window(self) -> None:
        """Support memorize error from text window behavior.
        """
        
        memorize_error_from_text_window(self)

    def _validation_evidence_is_passing(self, lesson: dict[str, Any]) -> bool:
        """Return whether lesson evidence is strong enough for active status."""
        return validation_evidence_is_passing(lesson)

    def _undo_lesson_action(self) -> None:
        """Support undo lesson action behavior.
        """
        
        undo_lesson_action(self)

    def _operation_phase_for_guard(self, raw_text: str) -> str:
        """Support operation phase for guard behavior.
        
        Parameters
        ----------
        raw_text : str
            The raw text value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return operation_phase_for_guard(self, raw_text)

    def _check_against_lessons(self) -> None:
        """Support check against lessons behavior.
        """
        
        check_against_lessons(self)

    def _show_repeat_guard_report(self, report: dict[str, Any]) -> None:
        """Support show repeat guard report behavior.
        
        Parameters
        ----------
        report : dict[str, Any]
            The report value.
        """
        
        show_repeat_guard_report(self, report)

