"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\main_window_help
# PURPOSE       : State models for window session, profile selection, and analysis lifecycle.
# EXPORTS       : WindowSessionState, ProfileSelectionState, AnalysisState
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass, field

from kanda_reasoner_app.reasoner_engine.v10_models import RetrievalBundle

__all__ = ["WindowSessionState", "ProfileSelectionState", "AnalysisState"]


@dataclass
class WindowSessionState:
    last_bundle: RetrievalBundle = field(default_factory=RetrievalBundle)
    last_prompt: str = ""
    last_selected_model: str = ""
    pending_question: str = ""

    def clear_visual_state(self) -> None:
        self.last_bundle = RetrievalBundle()
        self.last_prompt = ""
        self.last_selected_model = ""
        self.pending_question = ""


@dataclass
class ProfileSelectionState:
    detected_profile_name: str = ""
    active_profile_name: str = ""
    manual_profile_name: str = ""


@dataclass
class AnalysisState:
    is_running: bool = False
    last_generated_json_path: str = ""






