"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/reasoner_engine\ai_reasoner_main_window.py
# MANIFEST      : kanda_reasoner_app/reasoner_engine\ai_reasoner_main_window_help.json
# HELP FOLDER   : kanda_reasoner_app/reasoner_engine\main_window_help
# PURPOSE       : Profile detection, override resolution, and retriever rebuild coordination.
# EXPORTS       : ProfileRefreshResult, ProfileController
# DEPENDS ON    : state_models.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.state_models import (
    ProfileSelectionState,
)
from kanda_reasoner_app.reasoner_engine.project_profile import (
    ProjectProfile,
    get_project_profile,
    infer_project_profile,
    iter_project_profiles,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever import ProjectRetriever

__all__ = ["ProfileRefreshResult", "ProfileController"]


@dataclass
class ProfileRefreshResult:
    retriever: ProjectRetriever
    state: ProfileSelectionState
    detected_label_text: str
    active_label_text: str
    override_enabled: bool
    reset_enabled: bool


class ProfileController:
    def available_profile_names(self) -> list[str]:
        names: list[str] = []
        for profile in iter_project_profiles():
            profile_name = str(getattr(profile, "name", "")).strip()
            if profile_name:
                names.append(profile_name)
        return sorted(set(names))

    def _selected_override_name(self, combo_text: str) -> str:
        text = str(combo_text).strip()
        if not text or text.lower() in {"auto", "automatic", "(auto)"}:
            return ""
        return text

    def _detect_project_profile(self, project_index) -> ProjectProfile:
        project_summary = (
            project_index.project_summary
            if isinstance(getattr(project_index, "project_summary", None), dict)
            else {}
        )
        return infer_project_profile(
            project_root=str(project_summary.get("project_root", "")).strip(),
            project_summary=project_summary,
            packaging_metadata=getattr(project_index, "packaging_metadata", {}) or {},
            documentation_intent=getattr(project_index, "documentation_intent", {}) or {},
        )

    def build_refresh_result(
        self,
        *,
        project_index,
        current_override_name: str,
    ) -> ProfileRefreshResult:
        detected_profile = self._detect_project_profile(project_index)
        override_name = self._selected_override_name(current_override_name)
        active_profile = (
            get_project_profile(override_name) if override_name else detected_profile
        )

        retriever = ProjectRetriever(project_index, project_profile=active_profile)
        state = ProfileSelectionState(
            detected_profile_name=detected_profile.name,
            active_profile_name=active_profile.name,
            manual_profile_name=override_name,
        )

        active_label_text = active_profile.name + (" (manual)" if override_name else " (auto)")
        return ProfileRefreshResult(
            retriever=retriever,
            state=state,
            detected_label_text=detected_profile.name or "unknown",
            active_label_text=active_label_text or "unknown",
            override_enabled=bool(getattr(project_index, "index_data", None)),
            reset_enabled=bool(override_name),
        )

    def refresh_controls(self, window) -> None:
        combo = window.profile_override_combo
        current_manual = getattr(window, "_manual_project_profile_name", "")
        current_selection = combo.currentText().strip()

        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Auto")
        for name in self.available_profile_names():
            combo.addItem(name)

        desired = current_manual or current_selection or "Auto"
        idx = combo.findText(desired)
        combo.setCurrentIndex(idx if idx >= 0 else 0)
        combo.blockSignals(False)

        if not window.project_index.index_data:
            window.detected_profile_value_label.setText("Not loaded")
            window.active_profile_value_label.setText("Not loaded")
            combo.setEnabled(False)
            window.reset_profile_override_button.setEnabled(False)
            return

        result = self.build_refresh_result(
            project_index=window.project_index,
            current_override_name=combo.currentText(),
        )
        window.retriever = result.retriever
        window.profile_state = result.state
        window.detected_profile_value_label.setText(result.detected_label_text)
        window.active_profile_value_label.setText(result.active_label_text)
        combo.setEnabled(result.override_enabled and not window._analysis_running)
        window.reset_profile_override_button.setEnabled(
            result.reset_enabled and not window._analysis_running
        )

    def on_profile_override_changed(self, window) -> None:
        if not window.project_index.index_data:
            return

        self.refresh_controls(window)
        if window._manual_project_profile_name:
            window._append_log(
                "Project profile override set: " + window._manual_project_profile_name
            )
        else:
            window._append_log(
                "Project profile override cleared. Using auto-detected profile."
            )

    def reset_profile_override(self, window) -> None:
        window.profile_override_combo.blockSignals(True)
        window.profile_override_combo.setCurrentIndex(0)
        window.profile_override_combo.blockSignals(False)
        window._manual_project_profile_name = ""
        self.refresh_controls(window)
        window._append_log("Project profile override reset to auto.")







