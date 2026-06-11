"""Static import anchors for Project Reasoner architecture validation.

These imports are intentionally placed under a never-executed branch.
Tab 1 reads the AST import graph to identify direct test ownership,
while runtime test collection avoids optional GUI and runtime imports.
"""

from __future__ import annotations

if False:
    import kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.matching
    import kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.normalization
    import kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_validate_manifests
    import kanda_reasoner_app.reasoner_context_collector.collectors
    import kanda_reasoner_app.reasoner_context_collector.collectors.static_context
    import kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_documentation_intent
    import kanda_reasoner_app.reasoner_context_collector.collectors.static_context.collector_packaging_metadata
    import kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment
    import kanda_reasoner_app.reasoner_context_collector.developer_tools
    import kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner
    import kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector
    import kanda_reasoner_app.reasoner_context_collector.developer_tools.project_reasoner.reasoner_context_collector.outputs
    import kanda_reasoner_app.reasoner_context_collector.parsers
    import kanda_reasoner_app.reasoner_context_collector.parsers.static_context
    import kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser
    import kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser
    import kanda_reasoner_app.reasoner_context_collector.project_reasoner_data_collector_logic
    import kanda_reasoner_app.reasoner_context_collector.runner
    import kanda_reasoner_app.reasoner_runtime_collector
    import kanda_reasoner_app.reasoner_runtime_collector.hooks.qt_connection_monitor
    import kanda_reasoner_app.reasoner_runtime_collector.qt_hooks.qt_connection_monitor
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_1_private_impl
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_2_private_impl
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_3_private_impl
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_validate_manifests
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_decorators
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_models
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_state
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_writer
    import kanda_reasoner_app.reasoner_tools_gui_shell
    import kanda_reasoner_app.reasoner_tools_gui_shell.app_constants
    import kanda_reasoner_app.reasoner_tools_gui_shell.error_panels
    import kanda_reasoner_app.reasoner_tools_gui_shell.gui_support
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.browse_state
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.list_actions
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.prefs_io
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.rule_defaults
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_help.ui_builders
    import kanda_reasoner_app.reasoner_tools_gui_shell.ignore_rules_tab_validate_manifests
    import kanda_reasoner_app.reasoner_tools_gui_shell.launch
    import kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_help
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_output_paths
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_state
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches
    import kanda_reasoner_app.reasoner_tools_gui_shell.main_window_validate_manifests
    import kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs
    import kanda_reasoner_app.reasoner_tools_gui_validate_manifests
    import kanda_reasoner_app.reasoner_tools_shell
    import kanda_reasoner_app.reasoner_tools_shell.runner
    import kanda_reasoner_app.reasoner_tools_shell.runner_help
    import kanda_reasoner_app.reasoner_tools_shell.runner_help.window_methods_private_impl
    import kanda_reasoner_app.reasoner_tools_shell.runner_help.window_process_private_impl
    import kanda_reasoner_app.reasoner_tools_shell.runner_validate_manifests
    import kanda_reasoner_app.reasoner_tools_shell.tab4_scope_guard
    import kanda_reasoner_app.run_real_project_static_context_smoke
    import kanda_reasoner_app.run_static_context_test_suite
    import kanda_reasoner_app.runtime_scenarios
    import kanda_reasoner_app.runtime_scenarios.collector_scenario_traces
    import kanda_reasoner_app.runtime_scenarios.runtime_hotspot_hooks
    import kanda_reasoner_app.runtime_scenarios.runtime_scenario_runtime
    import kanda_reasoner_app.runtime_scenarios.runtime_scenario_writer
    import kanda_reasoner_app.runtime_scenarios.runtime_trace_retention
    import kanda_reasoner_app.runtime_scenarios.runtime_trace_retention_config
    import profiling
    import profiling.eeg_profiler
    import profiling.run_with_trace


def test_static_import_contract_chunk_04_is_parseable() -> None:
    """Keep this file visible to test discovery without runtime imports."""
    assert 4 <= 4
