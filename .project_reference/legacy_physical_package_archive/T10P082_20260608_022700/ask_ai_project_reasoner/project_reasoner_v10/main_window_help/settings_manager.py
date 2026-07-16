"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\main_window_help
# PURPOSE       : Persist and restore window settings for ai_reasoner_main_window.
# EXPORTS       : WindowSettingsManager
# DEPENDS ON    : state_models.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

__all__ = ["WindowSettingsManager"]


class WindowSettingsManager:
    def restore(self, window) -> None:
        settings = window.settings

        def _set_text(attr_name: str, key: str) -> None:
            widget = getattr(window, attr_name, None)
            if widget is None:
                return
            value = settings.value(key, "", type=str)
            if value:
                widget.setText(value)

        _set_text("json_path_edit", "json_path")
        _set_text("cache_dir_edit", "cache_dir")
        _set_text("governance_path_edit", "governance_path")
        _set_text("project_root_edit", "project_root")

        saved_model = settings.value("selected_model", "", type=str)
        if saved_model:
            idx = window.model_combo.findText(saved_model)
            if idx >= 0:
                window.model_combo.setCurrentIndex(idx)

        prefer_code = settings.value("prefer_code", True, type=bool)
        if prefer_code:
            window.prefer_code_radio.setChecked(True)
        else:
            window.prefer_prose_radio.setChecked(True)

        verbosity = settings.value("verbosity", "Concise", type=str)
        idx = window.verbosity_combo.findText(verbosity)
        if idx >= 0:
            window.verbosity_combo.setCurrentIndex(idx)

        window.debug_checkbox.setChecked(settings.value("debug", False, type=bool))
        window.analysis_auto_load_checkbox.setChecked(
            settings.value("analysis_auto_load", True, type=bool)
        )

    def save(self, window) -> None:
        if not getattr(window, "_settings_ready", False):
            return

        settings = window.settings
        settings.setValue("json_path", window.json_path_edit.text().strip())
        settings.setValue("cache_dir", window.cache_dir_edit.text().strip())
        settings.setValue("governance_path", window.governance_path_edit.text().strip())
        settings.setValue("project_root", window.project_root_edit.text().strip())
        settings.setValue("selected_model", window.model_combo.currentText().strip())
        settings.setValue("prefer_code", window.prefer_code_radio.isChecked())
        settings.setValue("verbosity", window.verbosity_combo.currentText().strip())
        settings.setValue("debug", window.debug_checkbox.isChecked())
        settings.setValue(
            "analysis_auto_load", window.analysis_auto_load_checkbox.isChecked()
        )
        settings.sync()






