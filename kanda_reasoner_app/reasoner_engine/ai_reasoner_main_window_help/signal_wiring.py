# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/signal_wiring.py
"""Signal wiring for the Project Reasoner main window."""

from __future__ import annotations

from typing import Any

__all__ = ["connect_main_window_signals"]


def connect_main_window_signals(window: Any) -> None:
    """Connect all main window widget signals to their current callbacks."""
    window.pick_project_root_button.clicked.connect(window.pick_project_root)
    window.run_analysis_button.clicked.connect(window.run_analysis)
    window.load_button.clicked.connect(window.load_json)
    window.static_context_button.clicked.connect(window.show_static_context_dialog)
    window.profile_override_combo.currentTextChanged.connect(window._on_profile_override_changed)
    window.reset_profile_override_button.clicked.connect(window._reset_profile_override)

    if hasattr(window, "ensure_local_ai_json_button"):
        window.ensure_local_ai_json_button.clicked.connect(
            lambda: window.runtime_controller.ensure_local_ai_json_copy(window)
        )
    if hasattr(window, "refresh_local_ai_json_button"):
        window.refresh_local_ai_json_button.clicked.connect(
            lambda: window.runtime_controller.refresh_local_ai_json_copy(window)
        )

    window.ask_ai_button.clicked.connect(window.ask_local_ai)
    window.clear_button.clicked.connect(window.clear_visuals_only)
    window.clear_memory_button.clicked.connect(window.clear_memory)

    window.pick_cache_dir_button.clicked.connect(window.pick_cache_dir)
    window.pick_governance_button.clicked.connect(window.pick_governance_path)
    window.refresh_models_button.clicked.connect(window.refresh_models)
    window.help_button.clicked.connect(window.show_help_dialog)

    window.quick_startup_button.clicked.connect(
        lambda: window._run_quick_question("Explain startup chain for the app step by step.")
    )
    window.quick_topomap_button.clicked.connect(
        lambda: window._run_quick_question("Explain topomap chain and how it is wired into the app.")
    )
    window.quick_timeline_button.clicked.connect(
        lambda: window._run_quick_question("Explain timeline chain and the flow between timeline modules.")
    )
    window.quick_responsibility_button.clicked.connect(
        lambda: window._run_quick_question("Create a responsibility map of the main modules in this app.")
    )
    window.quick_uncertainty_button.clicked.connect(
        lambda: window._run_quick_question("Create an uncertainty report about the architecture based on current evidence.")
    )

    window.question_edit.returnPressed.connect(window.ask_local_ai)
    window.file_evidence_list.currentItemChanged.connect(
        lambda current, _previous: window.answer_presenter.show_selected_file_detail(window, current)
    )
    window.symbol_evidence_list.currentItemChanged.connect(
        lambda current, _previous: window.answer_presenter.show_selected_symbol_detail(window, current)
    )
    window.history_list.currentItemChanged.connect(
        lambda current, _previous: window.answer_presenter.show_selected_history_turn(window, current)
    )

    window.ai.bridge.answer_ready.connect(window._on_ai_answer_ready)
    window.ai.bridge.token_ready.connect(window._on_ai_token_ready)
    window.ai.bridge.error_ready.connect(window._on_ai_error_ready)
    window.ai.bridge.status_ready.connect(window._append_log)

    window.model_combo.currentTextChanged.connect(window._save_last_config)
    window.prefer_code_radio.toggled.connect(window._save_last_config)
    window.prefer_prose_radio.toggled.connect(window._save_last_config)
    window.verbosity_combo.currentTextChanged.connect(window._save_last_config)
    window.debug_checkbox.toggled.connect(window._save_last_config)
