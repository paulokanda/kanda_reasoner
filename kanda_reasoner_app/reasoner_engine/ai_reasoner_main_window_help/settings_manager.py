# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/settings_manager.py
"""Persist Local AI settings without owning active Project selection."""

from __future__ import annotations

from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRegistry,
    ProjectSelectionRegistryError,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.project_json_path_resolver import (
    is_deprecated_project_json_path,
)

__all__ = ["WindowSettingsManager"]


def _registered_project_root() -> str:
    """Return the Tool-owned active Project root or an empty value."""
    try:
        boundary = ProjectSelectionRegistry().resolve_current_boundary()
    except ProjectSelectionRegistryError:
        return ""
    if boundary is None:
        return ""
    return str(boundary.active_project_root)


class WindowSettingsManager:
    """Persist Local AI preferences while deferring Project authority."""

    def restore(self, window) -> None:
        """Restore non-authoritative preferences and current Project state."""
        settings = window.settings

        def _set_text(attr_name: str, key: str) -> None:
            widget = getattr(window, attr_name, None)
            if widget is None:
                return
            value = settings.value(key, "", type=str)
            widget.setText(value or "")

        project_root = _registered_project_root()
        project_widget = getattr(window, "project_root_edit", None)
        if project_widget is not None:
            project_widget.setText(project_root)

        json_widget = getattr(window, "json_path_edit", None)
        saved_json_path = settings.value("json_path", "", type=str)
        if json_widget is not None:
            if (
                project_root
                and saved_json_path
                and not is_deprecated_project_json_path(saved_json_path)
            ):
                json_widget.setText(saved_json_path)
            else:
                json_widget.setText("")

        _set_text("cache_dir_edit", "cache_dir")
        _set_text("governance_path_edit", "governance_path")

        prefer_code = settings.value("prefer_code", True, type=bool)
        if prefer_code:
            window.prefer_code_radio.setChecked(True)
        else:
            window.prefer_prose_radio.setChecked(True)

        verbosity = settings.value("verbosity", "Concise", type=str)
        idx = window.verbosity_combo.findText(verbosity)
        if idx >= 0:
            window.verbosity_combo.setCurrentIndex(idx)

        window.debug_checkbox.setChecked(
            settings.value("debug", False, type=bool)
        )
        window.analysis_auto_load_checkbox.setChecked(
            settings.value("analysis_auto_load", True, type=bool)
        )

    def save(self, window) -> None:
        """Save Local AI preferences without persisting Project authority."""
        if not getattr(window, "_settings_ready", False):
            return

        settings = window.settings
        project_root = window.project_root_edit.text().strip()
        json_path = window.json_path_edit.text().strip() if project_root else ""
        if is_deprecated_project_json_path(json_path):
            json_path = ""
        settings.setValue("json_path", json_path)
        settings.setValue("cache_dir", window.cache_dir_edit.text().strip())
        settings.setValue(
            "governance_path",
            window.governance_path_edit.text().strip(),
        )
        settings.remove("project_root")
        settings.setValue("prefer_code", window.prefer_code_radio.isChecked())
        settings.setValue("verbosity", window.verbosity_combo.currentText().strip())
        settings.setValue("debug", window.debug_checkbox.isChecked())
        settings.setValue(
            "analysis_auto_load",
            window.analysis_auto_load_checkbox.isChecked(),
        )
        settings.sync()
