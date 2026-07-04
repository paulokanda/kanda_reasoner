# kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
"""Qt GUI for scanning, previewing, and inserting missing docstrings.

AI CONTEXT - REFACTORED MODULE

This module has been decomposed into submodules.
MANIFEST : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/

Read the manifest before editing any logic here.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from .insert_missing_docstrings_gui_help.ai_settings import (
    build_ai_config,
    load_config_from_file as _ai_settings_load_config_from_file,
    ollama_tags_url,
    persist_runtime_config,
    refresh_models as _ai_settings_refresh_models,
    save_config_to_file as _ai_settings_save_config_to_file,
)
from .insert_missing_docstrings_gui_help.dialogs import (
    browse_report_path as _dialogs_browse_report_path,
    browse_root as _dialogs_browse_root,
    save_output as _dialogs_save_output,
    show_help as _dialogs_show_help,
)
from .insert_missing_docstrings_gui_help.layout_builder import (
    build_ui,
    set_ai_controls_enabled,
    wire_events,
)
from .insert_missing_docstrings_gui_help.preferences import (
    load_prefs,
    prefs_path,
    save_prefs,
)
from .insert_missing_docstrings_gui_help.report_review_panel import (
    load_report_rows,
    matches_review_filter,
    populate_review_list,
    refresh_review_summary,
    row_needs_review,
    show_review_item_details,
)
from .insert_missing_docstrings_gui_help.run_controls import (
    append_text,
    cleanup_worker,
    effective_report_path,
    handle_worker_error,
    handle_worker_success,
    run_mode as _run_controls_run_mode,
    run_selected_mode as _run_controls_run_selected_mode,
)
from .insert_missing_docstrings_gui_help.scope_controls import (
    browse_target_path as _scope_controls_browse_target_path,
    effective_target_module,
    effective_target_package,
    update_scope_controls,
)
from .insert_missing_docstrings_gui_help.window_state import (
    current_prefs_payload,
    initialize_window,
)
from .insert_missing_docstrings_gui_help.worker_thread import DocstringRunWorker

__all__ = ["DocstringRunWorker", "MissingDocstringsWindow", "main"]


class MissingDocstringsWindow(QMainWindow):
    """Main window for scanning and inserting missing docstrings."""

    def __init__(self) -> None:
        """Initialize the GUI shell and delegated widgets."""
        super().__init__()
        initialize_window(self)
        # T4Q024_SAFE_MODE_ACTUAL_TAB3_WIRING
        from .guided_folder_mode.actual_tab3_wiring import install_safe_mode_actual_tab3_wiring
        self._safe_mode_actual_tab3_wiring_result = install_safe_mode_actual_tab3_wiring(self)


    def move_safe_mode_radio_to_layout(
        self,
        destination_layout,
        insert_index: int | None = None,
    ) -> None:
        """Move the Tab 1 audit source radio control into the host header."""
        from .guided_folder_mode.actual_tab3_wiring import move_safe_mode_radio_to_layout

        move_safe_mode_radio_to_layout(self, destination_layout, insert_index)

    def move_project_root_controls_to_layout(
        self,
        destination_layout,
        insert_index: int | None = None,
    ) -> None:
        """Move Docstring Assistant Project Root controls into the host header."""
        if getattr(self, "_project_root_controls_moved_to_host", False):
            return

        self._root_path_label.setParent(None)
        self._root_path_edit.setParent(None)
        self._browse_root_button.setParent(None)

        if insert_index is None:
            destination_layout.addSpacing(12)
            destination_layout.addWidget(self._root_path_label, 0)
            destination_layout.addWidget(self._root_path_edit, 0)
            destination_layout.addWidget(self._browse_root_button, 0)
        else:
            destination_layout.insertSpacing(insert_index, 12)
            destination_layout.insertWidget(insert_index + 1, self._root_path_label, 0)
            destination_layout.insertWidget(insert_index + 2, self._root_path_edit, 0)
            destination_layout.insertWidget(insert_index + 3, self._browse_root_button, 0)

        self._project_root_controls_moved_to_host = True

    def _prefs_path(self):
        """Return the standalone GUI preference file path."""
        return prefs_path(__file__)

    def _load_prefs(self):
        """Load persisted standalone GUI preferences."""
        return load_prefs(self._prefs_path())

    def _current_prefs_payload(self):
        """Build the current standalone GUI preferences payload."""
        return current_prefs_payload(self)

    def _save_prefs(self) -> None:
        """Persist the current standalone GUI preferences."""
        save_prefs(self._prefs_path(), self._current_prefs_payload())

    def _build_ui(self) -> None:
        """Build the adaptive Qt interface."""
        build_ui(self)

    def _wire_events(self) -> None:
        """Connect widgets to GUI actions and persistence hooks."""
        wire_events(self)

    def _set_ai_controls_enabled(self, enabled: bool) -> None:
        """Enable or disable local AI configuration controls."""
        set_ai_controls_enabled(self, enabled)

    def _update_scope_controls(self, value: str | None = None) -> None:
        """Update controls that depend on the selected run scope."""
        update_scope_controls(self, value)

    def _ollama_tags_url(self, base_url: str) -> str:
        """Build the Ollama model-tags URL for a base endpoint."""
        return ollama_tags_url(self, base_url)

    def refresh_models(self) -> None:
        """Refresh the local model combo box."""
        _ai_settings_refresh_models(self)

    def _build_ai_config(self):
        """Build an AIConfig object from current GUI controls."""
        return build_ai_config(self)

    def _persist_runtime_config(self):
        """Persist a temporary AIConfig for worker execution."""
        return persist_runtime_config(self)

    def load_config_from_file(self) -> None:
        """Load AI settings from a JSON config file."""
        _ai_settings_load_config_from_file(self)

    def save_config_to_file(self) -> None:
        """Save AI settings to a JSON config file."""
        _ai_settings_save_config_to_file(self)

    def _effective_target_module(self) -> str | None:
        """Return the selected module target when module scope is active."""
        return effective_target_module(self)

    def _effective_target_package(self) -> str | None:
        """Return the selected package target when package scope is active."""
        return effective_target_package(self)

    def browse_target_path(self) -> None:
        """Browse for the active module or package target."""
        _scope_controls_browse_target_path(self)

    def browse_report_path(self) -> None:
        """Browse for the JSONL run report path."""
        _dialogs_browse_report_path(self)

    def browse_root(self) -> None:
        """Browse for the project root."""
        _dialogs_browse_root(self)

    def refresh_tab1_audit_docstring_source(self, checked: bool | None = None):
        """Refresh missing-docstring targets from the Tab 1 audit."""
        from .insert_missing_docstrings_gui_help.tab1_audit_docstring_source import (
            refresh_tab1_audit_docstring_source,
        )

        return refresh_tab1_audit_docstring_source(self, checked)

    def run_selected_mode(self) -> None:
        """Run the mode currently selected in the mode combo box."""
        _run_controls_run_selected_mode(self)

    def _effective_report_path(self) -> str:
        """Return the explicit or default JSONL report path."""
        return effective_report_path(self)

    def run_mode(self, mode: str) -> None:
        """Run scan, diff, or write mode."""
        _run_controls_run_mode(self, mode)

    def _append_text(self, text: str) -> None:
        """Append text to the output console."""
        append_text(self, text)

    def _load_report_rows(self) -> None:
        """Load JSONL report rows into the review pane."""
        load_report_rows(self)

    def _refresh_review_summary(self) -> None:
        """Refresh the review summary label."""
        refresh_review_summary(self)

    def _row_needs_review(self, row: dict) -> bool:
        """Return whether a report row needs manual review."""
        return row_needs_review(self, row)

    def _matches_review_filter(self, row: dict) -> bool:
        """Return whether a report row matches the current filter."""
        return matches_review_filter(self, row)

    def _populate_review_list(self) -> None:
        """Populate the review list from loaded report rows."""
        populate_review_list(self)

    def _show_review_item_details(self, current, previous) -> None:
        """Show JSON details for the selected review row."""
        show_review_item_details(self, current, previous)

    def _handle_worker_success(self, mode: str) -> None:
        """Handle successful worker completion."""
        handle_worker_success(self, mode)

    def _handle_worker_error(self, mode: str, details: str) -> None:
        """Handle worker completion with errors."""
        handle_worker_error(self, mode, details)

    def _cleanup_worker(self) -> None:
        """Release worker and worker thread references."""
        cleanup_worker(self)

    def show_help(self) -> None:
        """Show help for modes, AI settings, scope, and review workflow."""
        _dialogs_show_help(self)

    def save_output(self) -> None:
        """Save the output console text to a file."""
        _dialogs_save_output(self)


def main() -> int:
    """Run the standalone missing-docstrings GUI application."""
    app = QApplication(sys.argv)
    window = MissingDocstringsWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
