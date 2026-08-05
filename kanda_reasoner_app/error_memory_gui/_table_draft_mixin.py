# project-path: kanda_reasoner_app/error_memory_gui/_table_draft_mixin.py
"""Table, draft cleanup, receive/import, and export mixin for Error Memory tab."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.error_memory.store import list_lessons
from kanda_reasoner_app.error_memory_gui._clipboard_export import (
    copy_complete_error_memory_json_to_clipboard,
    copy_error_draft_to_clipboard,
    export_for_ai,
    show_active_ready_failure_copy_window,
)
from kanda_reasoner_app.error_memory_gui._draft_deletion import (
    delete_matching_canonical_draft_lessons,
    draft_delete_identity_from_sources,
)
from kanda_reasoner_app.error_memory_gui._intake_blueprint import error_memory_prompt_template_dir
from kanda_reasoner_app.error_memory_gui._lesson_actions import (
    delete_selected_lesson,
    lesson_from_preview_or_selection,
    save_draft_lesson_from_partial,
    save_preview_lesson,
    set_selected_lesson_status,
    supersede_selected_lesson,
)
from kanda_reasoner_app.error_memory_gui._lesson_imports import (
    formatted_import_text_for_window,
    formatted_text_from_manifested_lesson_zip,
)
from kanda_reasoner_app.error_memory_gui._lesson_payloads import (
    canonical_draft_lesson_from_partial,
    lesson_from_formatted_text,
    text_is_formatted_error_lesson_payload,
)
from kanda_reasoner_app.error_memory_gui._memorize_flow import select_saved_active_lesson_row
from kanda_reasoner_app.error_memory_gui._pending_loader import load_pending_intake_row_into_editor
from kanda_reasoner_app.error_memory_gui._pending_rows import pending_lesson_rows_for_table
from kanda_reasoner_app.error_memory_gui._receive_import import (
    import_error_lesson_zip,
    receive_formulary_from_ai,
)
from kanda_reasoner_app.error_memory_gui._table_view import (
    formatted_lesson_block,
    lesson_from_current_windows_or_selection,
    lesson_id_for_row,
    load_selected_lesson_into_preview,
    reload_table,
    row_kind_for_row,
    selected_lesson_id_from_table,
)
from kanda_reasoner_app.error_memory_gui._text_payloads import text_has_formatted_lesson_payload

__all__ = ['ErrorMemoryTableDraftMixin']


ERROR_MEMORY_ROW_KIND_ROLE = Qt.UserRole + 1
ERROR_MEMORY_PENDING_PATH_ROLE = Qt.UserRole + 2


class ErrorMemoryTableDraftMixin:
    """Table, draft, receive/import, and export wrappers for ErrorMemoryTab."""

    def _copy_complete_error_memory_json_to_clipboard(self, text: str) -> None:
        """Support copy complete error memory json to clipboard behavior.
        
        Parameters
        ----------
        text : str
            The text value.
        """
        
        copy_complete_error_memory_json_to_clipboard(text)

    def _reload_table(self) -> None:
        """Support reload table behavior.
        """
        
        reload_table(
            self,
            row_kind_role=ERROR_MEMORY_ROW_KIND_ROLE,
            pending_path_role=ERROR_MEMORY_PENDING_PATH_ROLE,
        )

    def _row_kind_for_row(self, row: int) -> str:
        """Support row kind for row behavior.
        
        Parameters
        ----------
        row : int
            The row data.
        
        Returns
        -------
        str
            The string result.
        """
        
        return row_kind_for_row(
            self.lessons_table,
            row,
            row_kind_role=ERROR_MEMORY_ROW_KIND_ROLE,
        )

    def _lesson_id_for_row(self, row: int) -> str:
        """Support lesson id for row behavior.
        
        Parameters
        ----------
        row : int
            The row data.
        
        Returns
        -------
        str
            The string result.
        """
        
        return lesson_id_for_row(self, row)

    def _selected_lesson_id_from_table(self) -> str:
        """Support selected lesson id from table behavior.
        
        Returns
        -------
        str
            The string result.
        """
        
        return selected_lesson_id_from_table(self)

    def _formatted_lesson_block(self, lesson: dict[str, Any]) -> str:
        """Support formatted lesson block behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return formatted_lesson_block(lesson)

    def _error_memory_prompt_template_dir(self) -> Path:
        """Return the prompt-library folder containing Error Memory intake templates."""
        return error_memory_prompt_template_dir(self._current_project_root(), module_file=__file__)

    def _show_active_ready_failure_copy_window(self, *, source_label: str, lesson: dict[str, Any]) -> None:
        """Support show active ready failure copy window behavior.
        
        Parameters
        ----------
        source_label : str
            The source label value.
        lesson : dict[str, Any]
            The lesson value.
        """
        
        show_active_ready_failure_copy_window(self, source_label=source_label, lesson=lesson)

    def _pending_lesson_rows_for_table(self) -> list[dict[str, str]]:
        """Return virtual Lessons rows for pending intake files waiting for edition."""
        try:
            existing_lesson_ids = {
                str(item.get('lesson_id', '')).strip()
                for item in list_lessons(self._current_project_root(), include_inactive=True)
                if isinstance(item, dict) and str(item.get('lesson_id', '')).strip()
            }
        except Exception:
            existing_lesson_ids = set()
        return pending_lesson_rows_for_table(
            self._pending_intake_files_for_all_candidate_dirs(),
            self._dismissed_pending_intake_files,
            existing_lesson_ids,
            is_formatted_lesson_payload=self._text_is_formatted_error_lesson_payload,
            lesson_from_formatted_text=self._lesson_from_formatted_text,
        )

    def _load_pending_intake_row_into_editor(self, pending_file: Path, row_kind: str, *, show_duplicate_warning: bool=True) -> bool:
        """Support load pending intake row into editor behavior.
        
        Parameters
        ----------
        pending_file : Path
            The pending file value.
        row_kind : str
            The row kind value.
        show_duplicate_warning : bool, optional
            The optional show duplicate warning value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return load_pending_intake_row_into_editor(
            self,
            pending_file,
            row_kind,
            show_duplicate_warning=show_duplicate_warning,
        )

    def _load_selected_lesson_into_preview(self) -> None:
        """Support load selected lesson into preview behavior.
        """
        
        load_selected_lesson_into_preview(self)

    def _copy_error_draft_to_clipboard(self) -> None:
        """Support copy error draft to clipboard behavior.
        """
        
        copy_error_draft_to_clipboard(self)

    def _clean_error_editor(self) -> None:
        """Clear both work windows from the Error Editor Clean button."""
        self._clean_both_work_windows_from_clean_button()

    def _lesson_from_current_windows_or_selection(self) -> dict[str, Any] | None:
        """Return the lesson currently visible in Error Editor, intake, or table."""
        for text in (self.received_preview_edit.toPlainText(), self.raw_error_edit.toPlainText()):
            stripped = str(text or '').strip()
            if not stripped:
                continue
            try:
                lesson = self._lesson_from_formatted_text(stripped)
            except Exception:
                continue
            if isinstance(lesson, dict) and str(lesson.get('lesson_id', '')).strip():
                return dict(lesson)
        return self._lesson_from_preview_or_selection()

    def _draft_delete_identity_from_windows(self) -> tuple[set[str], list[str], list[str]]:
        """Collect all identifiers that describe the current/dismissed draft."""
        return draft_delete_identity_from_sources(
            raw_error_text=self.raw_error_edit.toPlainText(),
            received_preview_text=self.received_preview_edit.toPlainText(),
            last_dismissed_pending_intake_text=self._last_dismissed_pending_intake_text,
            loaded_pending_intake_lesson_id=self._loaded_pending_intake_lesson_id,
            last_dismissed_pending_intake_lesson_id=self._last_dismissed_pending_intake_lesson_id,
            selected_lesson_id=self._selected_lesson_id,
            current_lesson=self._lesson_from_current_windows_or_selection(),
            loaded_pending_intake_file=self._loaded_pending_intake_file,
            last_dismissed_pending_intake_file=self._last_dismissed_pending_intake_file,
            lesson_id_from_text=self._lesson_id_from_text_lenient,
        )

    def _delete_matching_canonical_draft_lessons(self, lesson_ids: set[str]) -> tuple[int, list[str], list[str]]:
        """Delete matching saved draft or invalid-active lesson records."""
        return delete_matching_canonical_draft_lessons(self._current_project_root(), lesson_ids)

    def _delete_current_draft_completely(self) -> None:
        """Delete the current draft from all Error Memory draft/pending surfaces.

        This is intentionally stronger than Clean.  It removes the disk-backed
        pending source files, removes matching saved draft or invalid-active
        canonical lesson records, clears both text windows, clears table
        selection, resets pending state, rebuilds the index, and prevents the
        same deleted draft from being reloaded when tabs change.
        """
        lesson_ids, visible_texts, explicit_paths = self._draft_delete_identity_from_windows()
        if not lesson_ids and (not visible_texts) and (not explicit_paths):
            QMessageBox.information(self, 'Delete draft', 'No pending draft, visible draft text, or selected draft lesson is loaded.')
            return
        display_id = ', '.join(sorted(lesson_ids)) if lesson_ids else 'current visible/pending draft'
        answer = QMessageBox.question(self, 'Delete draft completely', 'Delete the current Error Memory draft completely?\n\n' + display_id + '\n\nThis removes AI-assisted intake text, Error Editor text, matching pending intake source files, matching draft/invalid saved lesson records, and stale list entries. Active-ready saved lessons are preserved.')
        if answer != QMessageBox.Yes:
            return
        deleted_pending, pending_failures = self._delete_matching_pending_intake_files(lesson_ids, visible_texts, explicit_paths)
        deleted_store, skipped_store, store_failures = self._delete_matching_canonical_draft_lessons(lesson_ids)
        for lesson_id in lesson_ids:
            self._dismissed_pending_intake_lesson_ids.add(lesson_id)
        for marker in explicit_paths:
            if marker:
                self._dismissed_pending_intake_files.add(marker)
        self._selected_lesson_id = ''
        self._last_received_lesson = None
        self._loaded_pending_intake_file = ''
        self._loaded_pending_intake_lesson_id = ''
        self._last_dismissed_pending_intake_file = ''
        self._last_dismissed_pending_intake_lesson_id = ''
        self._last_dismissed_pending_intake_text = ''
        self.raw_error_edit.clear()
        self.received_preview_edit.clear()
        self.lessons_table.clearSelection()
        self._reload_table()
        details = ['Pending intake files deleted: ' + str(deleted_pending), 'Canonical draft/invalid lesson records deleted: ' + str(deleted_store)]
        if skipped_store:
            details.append('Saved active-ready lessons preserved: ' + '; '.join(skipped_store))
        if pending_failures or store_failures:
            details.append('Delete failures: ' + '; '.join(pending_failures + store_failures))
            QMessageBox.warning(self, 'Delete draft', 'Draft cleanup finished with warnings.\n\n' + '\n'.join(details))
            return
        self._show_action_done('Delete draft', 'Draft deleted completely.', '\n'.join(details))

    def _receive_formulary_from_ai(self) -> None:
        """Support receive formulary from ai behavior.
        """
        
        receive_formulary_from_ai(self)

    def _text_has_formatted_lesson_payload(self, text: str) -> bool:
        """Support text has formatted lesson payload behavior.
        
        Parameters
        ----------
        text : str
            The text value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return text_has_formatted_lesson_payload(text)

    def _lesson_from_formatted_text(self, text: str) -> dict[str, Any]:
        """Build a lesson from either canonical lesson JSON or AI formulary JSON."""
        return lesson_from_formatted_text(text, selected_project_root=self._current_project_root())

    def _canonical_draft_lesson_from_partial(self, lesson: dict[str, Any], *, source_text: str='') -> dict[str, Any]:
        """Return a schema-saveable draft lesson without inventing semantics."""
        return canonical_draft_lesson_from_partial(
            lesson,
            project_slug=self._require_project_root().name,
            source_text=source_text,
        )

    def _text_is_formatted_error_lesson_payload(self, text: str) -> bool:
        """Return whether text is a formatted Error Memory lesson, not just any JSON."""
        return text_is_formatted_error_lesson_payload(text, selected_project_root=self._current_project_root())

    def _select_saved_active_lesson_row(self, lesson_id: str) -> bool:
        """Support select saved active lesson row behavior.
        
        Parameters
        ----------
        lesson_id : str
            The lesson id value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return select_saved_active_lesson_row(self, lesson_id)

    def _formatted_text_from_manifested_lesson_zip(self, source: Path) -> str:
        """Return the manifest-declared Error Lesson receive block when present."""
        return formatted_text_from_manifested_lesson_zip(
            source,
            is_formatted_lesson_payload=self._text_is_formatted_error_lesson_payload,
        )

    def _formatted_import_text_for_window(self, selected: str) -> str:
        """Return formatted Error Memory lesson text from a selected ZIP/JSON/TXT/MD file."""
        return formatted_import_text_for_window(
            selected,
            is_formatted_lesson_payload=self._text_is_formatted_error_lesson_payload,
        )

    def _import_error_lesson_zip(self) -> None:
        """Support import error lesson zip behavior.
        """
        
        import_error_lesson_zip(self)

    def _save_preview_lesson(self) -> None:
        """Support save preview lesson behavior.
        """
        
        save_preview_lesson(self)

    def _delete_selected_lesson(self) -> None:
        """Support delete selected lesson behavior.
        """
        
        delete_selected_lesson(self)

    def _lesson_from_preview_or_selection(self) -> dict[str, Any] | None:
        """Support lesson from preview or selection behavior.
        
        Returns
        -------
        dict[str, Any] | None
            The mapped values.
        """
        
        return lesson_from_preview_or_selection(self)

    def _save_draft_lesson_from_partial(self, lesson: dict[str, Any], *, source_text: str, success_prefix: str) -> Path | None:
        """Support save draft lesson from partial behavior.
        
        Parameters
        ----------
        lesson : dict[str, Any]
            The lesson value.
        source_text : str
            The source text.
        success_prefix : str
            The success prefix value.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        return save_draft_lesson_from_partial(self, lesson, source_text=source_text, success_prefix=success_prefix)

    def _set_selected_lesson_status(self, status: str) -> None:
        """Support set selected lesson status behavior.
        
        Parameters
        ----------
        status : str
            The status value.
        """
        
        set_selected_lesson_status(self, status)

    def _supersede_selected_lesson(self) -> None:
        """Support supersede selected lesson behavior.
        """
        
        supersede_selected_lesson(self)

    def _export_for_ai(self) -> None:
        """Support export for ai behavior.
        """
        
        export_for_ai(self)

