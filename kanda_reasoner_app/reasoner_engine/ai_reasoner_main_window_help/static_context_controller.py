# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/static_context_controller.py
"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\main_window_help
# PURPOSE       : Static-context availability, labels, and dialog presentation.
# EXPORTS       : StaticContextController
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.reasoner_engine.v10_static_context_dialog import (
    StaticContextDialog,
)

__all__ = ["StaticContextController"]


class StaticContextController:
    """Represent static context controller."""
    
    def _has_packaging_metadata(self, project_index) -> bool:
        """Support has packaging metadata behavior.
        
        Parameters
        ----------
        project_index : object
            The project index value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return bool(getattr(project_index, "packaging_metadata", {}) or {})

    def _has_documentation_intent(self, project_index) -> bool:
        """Support has documentation intent behavior.
        
        Parameters
        ----------
        project_index : object
            The project index value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return bool(getattr(project_index, "documentation_intent", {}) or {})

    def refresh_controls(self, window) -> None:
        """Support refresh controls behavior.
        
        Parameters
        ----------
        window : object
            The window value.
        """
        
        if not window.project_index.index_data:
            window.static_context_summary_value_label.setText("Not loaded")
            window.static_context_packaging_value_label.setText("Unknown")
            window.static_context_docs_value_label.setText("Unknown")
            window.static_context_button.setEnabled(False)
            return

        has_packaging = self._has_packaging_metadata(window.project_index)
        has_documentation = self._has_documentation_intent(window.project_index)

        if has_packaging and has_documentation:
            summary_text = "Available"
        elif has_packaging or has_documentation:
            summary_text = "Partial"
        else:
            summary_text = "Missing"

        window.static_context_summary_value_label.setText(summary_text)
        window.static_context_packaging_value_label.setText(
            "Present" if has_packaging else "Missing"
        )
        window.static_context_docs_value_label.setText(
            "Present" if has_documentation else "Missing"
        )
        if not window._analysis_running:
            window.static_context_button.setEnabled(True)

    def show_dialog(self, window) -> None:
        """Show the dialog.
        
        Parameters
        ----------
        window : object
            The window value.
        """
        
        if not window.project_index.index_data:
            QMessageBox.warning(window, "No JSON", "Please load a JSON file first.")
            return

        if getattr(window, "_static_context_dialog", None) is None:
            window._static_context_dialog = StaticContextDialog(parent=window)

        dialog = window._static_context_dialog
        if hasattr(dialog, "set_context"):
            dialog.set_context(
                index=window.project_index,
                detected_profile_name=window._detected_project_profile_name,
                active_profile_name=window._active_project_profile_name,
            )
        elif hasattr(dialog, "set_index"):
            dialog.set_index(window.project_index)

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()






