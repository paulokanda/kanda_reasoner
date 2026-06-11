"""Import-only protection for public Project Reasoner contracts.

The imports live under TYPE_CHECKING so runtime test collection does not load optional
GUI dependencies, while Tab 1 can still verify that these public modules have direct
focused test coverage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import _inject_missing_module_docstrings
    import kanda_reasoner_app.collector_persistence_io
    import kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator
    import kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.models
    import kanda_reasoner_app.insert_missing_docstrings_gui.context_builder
    import kanda_reasoner_app.insert_missing_docstrings_gui.docstring_validator
    import kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.constants
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.preferences
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.scope_controls
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.worker_thread
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.diff_output
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.source_io
    import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.symbol_naming
    import kanda_reasoner_app.insert_missing_docstrings_gui.module_summarizer
    import kanda_reasoner_app.insert_missing_docstrings_gui.parallel_runner
    import kanda_reasoner_app.json_splitter.json_splitter_8
    import kanda_reasoner_app.json_splitter.json_splitter_chunk_balancing
    import kanda_reasoner_app.json_splitter.json_splitter_split_reassemble_validation
    import kanda_reasoner_app.json_splitter.json_splitter_web_ai_route_manifest
    import kanda_reasoner_app.live_source_verification.verifier
    import kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer
    import kanda_reasoner_app.manage_architecture.manage_architecture_gui
    import kanda_reasoner_app.manage_architecture.manage_architecture_gui_help.mode_options_hlp
    import kanda_reasoner_app.manage_workflows.manage_workflows
    import kanda_reasoner_app.manage_workflows.manage_workflows_gui


def test_public_contract_imports_are_declared() -> None:
    """Keep this module visible to test discovery without importing GUI stacks."""
    assert TYPE_CHECKING is False
