"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

__all__ = [
    "load_full_sections",
]

from typing import Any


def load_full_sections(index: Any) -> None:
    if not index.index_data:
        return

    get = index.index_data.get
    sd = index._safe_dict
    sl = index._safe_list
    st = index._safe_text

    index.collector_info = sd(get("collector_info"))
    index.collection_config = sd(get("collection_config"))
    index.packaging_metadata = sd(get("packaging_metadata"))
    index.documentation_intent = sd(get("documentation_intent"))
    index.warning_index = sd(get("warning_index"))
    index.keyword_index = sd(get("keyword_index"))

    index.qt_signal_map = sl(get("qt_signal_map"))

    index.widget_registry = sd(get("widget_registry"))
    index.widget_summary = sd(get("widget_summary"))
    index.widget_hotspots = sl(get("widget_hotspots"))
    index.widget_text_index = sd(get("widget_text_index"))
    index.widget_text_hotspots = sl(get("widget_text_hotspots"))
    index.widget_layout_index = sd(get("widget_layout_index"))
    index.widget_layout_hotspots = sl(get("widget_layout_hotspots"))
    index.widget_ui_action_bridge = sd(get("widget_ui_action_bridge"))
    index.widget_ui_action_hotspots = sl(get("widget_ui_action_hotspots"))

    index.ui_action_index = sd(get("ui_action_index"))
    index.ui_action_summary = sd(get("ui_action_summary"))
    index.ui_action_hotspots = sl(get("ui_action_hotspots"))

    index.attribute_state_map = sd(get("attribute_state_map"))
    index.object_ownership = sd(get("object_ownership"))

    index.execution_chains = sd(get("execution_chains"))
    index.subsystems = sl(get("subsystems"))

    index.symbol_summaries = sd(get("symbol_summaries"))
    index.snippet_index = sd(get("snippet_index"))
    index.duplicate_symbols = sl(get("duplicate_symbols"))
    index.test_links = sd(get("test_links"))

    index.bucket_index = sd(get("bucket_index"))
    index.bucket_summary = sd(get("bucket_summary"))
    index.bucket_insights = sd(get("bucket_insights"))
    index.entry_bucket_flows = sd(get("entry_bucket_flows"))
    index.entry_bucket_flow_summary = sd(get("entry_bucket_flow_summary"))

    index.boundary_index = sd(get("boundary_index"))
    index.boundary_summary = sd(get("boundary_summary"))
    index.boundary_handoffs = sl(get("boundary_handoffs"))
    index.boundary_violation_index = sd(get("boundary_violation_index"))
    index.boundary_violation_summary = sd(get("boundary_violation_summary"))
    index.boundary_violation_hotspots = sl(get("boundary_violation_hotspots"))

    index.orchestration_index = sd(get("orchestration_index"))
    index.orchestration_summary = sd(get("orchestration_summary"))
    index.orchestration_hotspots = sl(get("orchestration_hotspots"))

    index.state_mutation_index = sd(get("state_mutation_index"))
    index.state_mutation_summary = sd(get("state_mutation_summary"))
    index.state_mutation_hotspots = sl(get("state_mutation_hotspots"))

    index.persistence_io_index = sd(get("persistence_io_index"))
    index.persistence_io_summary = sd(get("persistence_io_summary"))
    index.persistence_io_hotspots = sl(get("persistence_io_hotspots"))

    index.event_propagation_index = sd(get("event_propagation_index"))
    index.event_propagation_summary = sd(get("event_propagation_summary"))
    index.event_propagation_hotspots = sl(get("event_propagation_hotspots"))

    index.canonical_conflict_index = sd(get("canonical_conflict_index"))
    index.canonical_conflict_summary = sd(get("canonical_conflict_summary"))
    index.legacy_shadow_hotspots = sl(get("legacy_shadow_hotspots"))

    index.responsibility_overlap_index = sd(get("responsibility_overlap_index"))
    index.responsibility_overlap_summary = sd(get("responsibility_overlap_summary"))
    index.overlap_hotspots = sl(get("overlap_hotspots"))

    index.feature_registry = sd(get("feature_registry"))
    index.feature_summary = sd(get("feature_summary"))
    index.feature_hotspots = sl(get("feature_hotspots"))

    index.implementation_chronology_index = sd(get("implementation_chronology_index"))
    index.implementation_chronology_summary = sd(get("implementation_chronology_summary"))
    index.migration_transition_hotspots = sl(get("migration_transition_hotspots"))

    index.config_schema_registry = sd(get("config_schema_registry"))
    index.config_schema_summary = sd(get("config_schema_summary"))
    index.schema_risk_hotspots = sl(get("schema_risk_hotspots"))

    index.state_lifecycle_index = sd(get("state_lifecycle_index"))
    index.state_lifecycle_summary = sd(get("state_lifecycle_summary"))
    index.state_lifecycle_hotspots = sl(get("state_lifecycle_hotspots"))

    index.change_impact_index = sd(get("change_impact_index"))
    index.change_impact_summary = sd(get("change_impact_summary"))
    index.high_risk_edit_hotspots = sl(get("high_risk_edit_hotspots"))

    index.active_code_index = sd(get("active_code_index"))
    index.active_code_summary = sd(get("active_code_summary"))
    index.untested_critical_hotspots = sl(get("untested_critical_hotspots"))

    index.runtime_scenario_index = sd(get("runtime_scenario_index"))
    index.runtime_scenario_summary = sd(get("runtime_scenario_summary"))
    index.runtime_scenario_hotspots = sl(get("runtime_scenario_hotspots"))

    index.runtime_feature_attribution_index = sd(get("runtime_feature_attribution_index"))
    index.runtime_feature_attribution_summary = sd(get("runtime_feature_attribution_summary"))
    index.runtime_feature_attribution_hotspots = sl(get("runtime_feature_attribution_hotspots"))

    index.runtime_trace_summary = sd(get("runtime_trace_summary"))
    index.runtime_signal_connections = sl(get("runtime_signal_connections"))
    index.runtime_state_snapshots = sl(get("runtime_state_snapshots"))
    index.runtime_call_stack_index = sd(get("runtime_call_stack_index"))

    index.runtime_trace_raw = sd(get("runtime_trace_raw"))
    index.runtime_trace_raw_path = st(get("runtime_trace_raw_path"))
    index.runtime_trace_raw_counts = sd(get("runtime_trace_raw_counts"))

    index.collector_insights = sd(get("collector_insights"))
    index.errors = sl(get("errors"))

    index.section_presence_map = {
        name: index.index_data.get(name) is not None
        for name in index.section_names
    }

