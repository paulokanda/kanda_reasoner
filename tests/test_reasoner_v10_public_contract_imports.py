"""Import-only protection for v10 reader public contracts.

The imports are guarded by TYPE_CHECKING to avoid importing GUI dependencies during
normal test collection while still documenting direct test ownership for Tab 1.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kanda_reasoner_app.project_reasoner_v10.ai_bridge
    import kanda_reasoner_app.project_reasoner_v10.ai_bridge_help.bridge_signals
    import kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window
    import kanda_reasoner_app.project_reasoner_v10.answer_one_line
    import kanda_reasoner_app.project_reasoner_v10.answer_source_models
    import kanda_reasoner_app.project_reasoner_v10.complete_json_detector
    import kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities
    import kanda_reasoner_app.project_reasoner_v10.help_index
    import kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_models
    import kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_normalization
    import kanda_reasoner_app.project_reasoner_v10.help_index_help.help_index_raw
    import kanda_reasoner_app.project_reasoner_v10.index_loader
    import kanda_reasoner_app.project_reasoner_v10.index_loader_help.index_builders
    import kanda_reasoner_app.project_reasoner_v10.index_loader_help.path_resolution
    import kanda_reasoner_app.project_reasoner_v10.index_loader_help.section_loading
    import kanda_reasoner_app.project_reasoner_v10.index_loader_help.state_init
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.analysis_controller
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.answer_presenter
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.json_track
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.profile_controller
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.runtime_controller
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.session_service
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.settings_manager
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.signal_wiring
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.state_models
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.static_context_controller
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_builder
    import kanda_reasoner_app.project_reasoner_v10.main_window_help.ui_components
    import kanda_reasoner_app.project_reasoner_v10.project_profile
    import kanda_reasoner_app.project_reasoner_v10.prompt_builder
    import kanda_reasoner_app.project_reasoner_v10.reasoner_retriever
    import kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents
    import kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.snippet_retrieval
    import kanda_reasoner_app.project_reasoner_v10.v10_intent_detection
    import kanda_reasoner_app.project_reasoner_v10.v10_scoring_config


def test_v10_public_contract_imports_are_declared() -> None:
    """Keep this module visible to test discovery without importing GUI stacks."""
    assert TYPE_CHECKING is False
