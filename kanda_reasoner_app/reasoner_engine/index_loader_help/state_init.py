# project-path: kanda_reasoner_app/reasoner_engine/index_loader_help/state_init.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

__all__ = [
    "initialize_index_state",
]

from collections import defaultdict
from typing import Any


def initialize_index_state(index: Any) -> None:
    """Support initialize index state behavior.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    index.index_data = None
    index.project_root = ""

    # Backward-compatible core indexes already expected by retriever/UI
    index.files_by_path = {}
    index.files_by_module = {}
    index.semantic_roles = {}
    index.symbol_details = {}
    index.symbol_to_file = defaultdict(set)
    index.import_graph_out = defaultdict(set)
    index.call_graph_out = defaultdict(set)

    # Full JSON reading support
    index.top_level_sections = {}
    index.section_names = []

    # Raw top-level sections
    index.project_summary = {}
    index.collector_info = {}
    index.collection_config = {}
    index.packaging_metadata = {}
    index.documentation_intent = {}
    index.warning_index = {}
    index.keyword_index = {}
    index.qt_signal_map = []
    index.widget_registry = {}
    index.widget_summary = {}
    index.widget_hotspots = []
    index.widget_text_index = {}
    index.widget_text_hotspots = []
    index.widget_layout_index = {}
    index.widget_layout_hotspots = []
    index.widget_ui_action_bridge = {}
    index.widget_ui_action_hotspots = []
    index.ui_action_index = {}
    index.ui_action_summary = {}
    index.ui_action_hotspots = []
    index.attribute_state_map = {}
    index.object_ownership = {}
    index.execution_chains = {}
    index.subsystems = []
    index.symbol_summaries = {}
    index.snippet_index = {}
    index.duplicate_symbols = []
    index.test_links = {}
    index.bucket_index = {}
    index.bucket_summary = {}
    index.bucket_insights = {}
    index.entry_bucket_flows = {}
    index.entry_bucket_flow_summary = {}
    index.boundary_index = {}
    index.boundary_summary = {}
    index.boundary_handoffs = []
    index.boundary_violation_index = {}
    index.boundary_violation_summary = {}
    index.boundary_violation_hotspots = []
    index.orchestration_index = {}
    index.orchestration_summary = {}
    index.orchestration_hotspots = []
    index.state_mutation_index = {}
    index.state_mutation_summary = {}
    index.state_mutation_hotspots = []
    index.persistence_io_index = {}
    index.persistence_io_summary = {}
    index.persistence_io_hotspots = []
    index.event_propagation_index = {}
    index.event_propagation_summary = {}
    index.event_propagation_hotspots = []
    index.canonical_conflict_index = {}
    index.canonical_conflict_summary = {}
    index.legacy_shadow_hotspots = []
    index.responsibility_overlap_index = {}
    index.responsibility_overlap_summary = {}
    index.overlap_hotspots = []
    index.feature_registry = {}
    index.feature_summary = {}
    index.feature_hotspots = []
    index.implementation_chronology_index = {}
    index.implementation_chronology_summary = {}
    index.migration_transition_hotspots = []
    index.config_schema_registry = {}
    index.config_schema_summary = {}
    index.schema_risk_hotspots = []
    index.state_lifecycle_index = {}
    index.state_lifecycle_summary = {}
    index.state_lifecycle_hotspots = []
    index.change_impact_index = {}
    index.change_impact_summary = {}
    index.high_risk_edit_hotspots = []
    index.active_code_index = {}
    index.active_code_summary = {}
    index.untested_critical_hotspots = []
    index.runtime_scenario_index = {}
    index.runtime_scenario_summary = {}
    index.runtime_scenario_hotspots = []
    index.runtime_feature_attribution_index = {}
    index.runtime_feature_attribution_summary = {}
    index.runtime_feature_attribution_hotspots = []
    index.runtime_trace_summary = {}
    index.runtime_signal_connections = []
    index.runtime_state_snapshots = []
    index.runtime_call_stack_index = {}

    # Fully merged raw runtime trace, if present in canonical JSON
    index.runtime_trace_raw = {}
    index.runtime_trace_raw_path = ""
    index.runtime_trace_raw_counts = {}

    index.collector_insights = {}
    index.errors = []

    # Convenience indexes for advanced querying later
    index.widgets_by_file = defaultdict(list)
    index.ui_actions_by_file = defaultdict(list)
    index.boundaries_by_file = defaultdict(list)
    index.runtime_events_by_file = defaultdict(list)
    index.runtime_signal_connections_by_sender = defaultdict(list)
    index.runtime_signal_connections_by_receiver = defaultdict(list)

    index.hotspots_by_file = defaultdict(list)
    index.section_presence_map = {}
    index.snippets_by_file = defaultdict(list)

    index.token_to_files = defaultdict(set)

