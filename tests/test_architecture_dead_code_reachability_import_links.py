"""Static reachability links for active modules deferred from deletion.

Imports stay under TYPE_CHECKING so architecture validation can see explicit
reachability evidence without importing GUI/runtime-heavy modules at runtime.
These links are not behavior tests and must not be treated as deletion approval.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kanda_reasoner_app.daily_rfctr_report.daily_refactor_report
    import kanda_reasoner_app.patch_governance.installer_template
    import kanda_reasoner_app.project_intelligence.symbol_indexer
    import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.event_classification
    import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.hotspots
    import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.normalization
    import kanda_reasoner_app.reasoner_context_collector.collector_widget_registry_help.widget_registry_methods_part_1_private_impl
    import kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.indexing
    import kanda_reasoner_app.reasoner_context_collector.collector_widget_ui_action_bridge_help.matching
    import kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_stats
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_impl_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_1_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_2_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_3_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_1_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_2_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_3_private_impl
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.symbol_retrieval_support_private_impl
    import kanda_reasoner_app.reasoner_engine.v10_intent_detection
    import kanda_reasoner_app.reasoner_engine.v10_scoring_config
    import kanda_reasoner_app.reasoner_runtime_collector.hooks.qt_connection_monitor
    import kanda_reasoner_app.reasoner_runtime_collector.qt_hooks.qt_connection_monitor
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_decorators
    import kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_state
    import kanda_reasoner_app.reasoner_symbol_atlas._related_file_finder_support
    import kanda_reasoner_app.reasoner_symbol_atlas.evidence_migration
    import kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.boundary_guard
    import kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_advisor_comparison
    import kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_guarded_runtime_display
    import kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_real_adapter_candidate
    import kanda_reasoner_app.routing_signal_scorer.prompt_intake_boundary.prompt_artifact_contract
    import kanda_reasoner_app.routing_signal_scorer.prompt_intake_boundary.prompt_output_firewall
    import kanda_reasoner_app.tab3_manual_review_runtime.layout_runtime
    import kanda_reasoner_app.tab3_manual_review_runtime.report_panel_runtime
    import kanda_reasoner_app.tab3_manual_review_runtime.scan_report_lifecycle_runtime
    import scripts.merge_freeze_validation_evidence
    import scripts.migrate_freeze_after_update_external_root
    import tools._query_intents_refactor_spec_v1
    import tools.ask_ai_project_reasoner_deletion_dry_run


def test_dead_code_reachability_links_are_static() -> None:
    """Keep this test module runtime-safe."""
    assert TYPE_CHECKING is False
