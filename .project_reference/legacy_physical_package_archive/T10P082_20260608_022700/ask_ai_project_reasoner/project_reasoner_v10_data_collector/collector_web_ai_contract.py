"""Web-AI collector output contract audit helpers.

This module is an audit/contract gate for the canonical Project Reasoner
collector output created by the GUI action "4. Fourth step: collect project
structure".

It does not change collector output. It defines additive validation rules so
future web-AI awareness indexes can be added safely without breaking the
canonical JSON export used by web AI.
"""

from __future__ import annotations

from typing import Any, Mapping

__all__ = [
    "CANONICAL_JSON_ROLE",
    "KEY_CLASSIFICATIONS",
    "LARGE_SECTION_KEYS",
    "RECOMMENDED_FUTURE_WEB_AI_KEYS",
    "REQUIRED_TOP_LEVEL_KEYS",
    "build_collector_output_audit",
    "validate_collector_output_contract",
]

CANONICAL_JSON_ROLE = "web_ai_export"

REQUIRED_TOP_LEVEL_KEYS = (
    "collector_info",
    "collector_scope",
    "warning_index",
    "project_summary",
    "collection_config",
    "files",
    "packaging_metadata",
    "documentation_intent",
    "limitations",
    "symbol_index",
    "import_graph",
    "call_edges",
    "keyword_index",
    "semantic_roles",
    "qt_signal_map",
    "widget_registry",
    "widget_summary",
    "widget_hotspots",
    "widget_text_index",
    "widget_text_hotspots",
    "widget_layout_index",
    "widget_layout_hotspots",
    "widget_ui_action_bridge",
    "widget_ui_action_hotspots",
    "ui_action_index",
    "ui_action_summary",
    "ui_action_hotspots",
    "attribute_state_map",
    "object_ownership",
    "execution_chains",
    "subsystems",
    "symbol_summaries",
    "source_file_index",
    "edit_ready_symbol_index",
    "edit_ready_source_summary",
    "snippet_index",
    "duplicate_symbols",
    "test_links",
    "bucket_index",
    "bucket_summary",
    "bucket_insights",
    "entry_bucket_flows",
    "entry_bucket_flow_summary",
    "boundary_index",
    "boundary_summary",
    "boundary_handoffs",
    "boundary_violation_index",
    "boundary_violation_summary",
    "boundary_violation_hotspots",
    "orchestration_index",
    "orchestration_summary",
    "orchestration_hotspots",
    "state_mutation_index",
    "state_mutation_summary",
    "state_mutation_hotspots",
    "persistence_io_index",
    "persistence_io_summary",
    "persistence_io_hotspots",
    "event_propagation_index",
    "event_propagation_summary",
    "event_propagation_hotspots",
    "canonical_conflict_index",
    "canonical_conflict_summary",
    "legacy_shadow_hotspots",
    "responsibility_overlap_index",
    "responsibility_overlap_summary",
    "overlap_hotspots",
    "feature_registry",
    "feature_summary",
    "feature_hotspots",
    "implementation_chronology_index",
    "implementation_chronology_summary",
    "migration_transition_hotspots",
    "config_schema_registry",
    "config_schema_summary",
    "schema_risk_hotspots",
    "state_lifecycle_index",
    "state_lifecycle_summary",
    "state_lifecycle_hotspots",
    "change_impact_index",
    "change_impact_summary",
    "high_risk_edit_hotspots",
    "active_code_index",
    "active_code_summary",
    "untested_critical_hotspots",
    "runtime_feature_attribution_index",
    "runtime_feature_attribution_summary",
    "runtime_feature_attribution_hotspots",
    "collector_insights",
    "runtime_scenario_index",
    "runtime_scenario_summary",
    "runtime_scenario_hotspots",
    "runtime_trace_summary",
    "runtime_signal_connections",
    "runtime_state_snapshots",
    "runtime_call_stack_index",
    "runtime_trace_raw_path",
    "runtime_trace_raw_counts",
    "runtime_trace_raw",
    "errors",
)

RECOMMENDED_FUTURE_WEB_AI_KEYS = (
    "web_ai_schema_version",
    "web_ai_symbol_index",
    "primary_definition_index",
    "entry_points_detail",
    "stable_evidence_id_index",
    "web_ai_file_responsibility_index",
    "web_ai_test_protection_index",
    "web_ai_ui_flow_index",
    "web_ai_readme",
)

LARGE_SECTION_KEYS = (
    "files",
    "call_edges",
    "attribute_state_map",
    "widget_registry",
    "widget_text_index",
    "widget_layout_index",
    "responsibility_overlap_index",
)

KEY_CLASSIFICATIONS = {
    "collector_info": "collector_metadata",
    "collector_scope": "collector_metadata",
    "warning_index": "source_parse_quality",
    "project_summary": "summary",
    "collection_config": "collector_metadata",
    "files": "source_corpus",
    "packaging_metadata": "packaging_metadata",
    "documentation_intent": "documentation_intent",
    "limitations": "collector_metadata",
    "symbol_index": "symbol_navigation",
    "import_graph": "static_dependency_graph",
    "call_edges": "static_call_graph",
    "semantic_roles": "source_heuristic",
    "qt_signal_map": "static_ui_signal_map",
    "widget_registry": "static_ui_widget_index",
    "widget_text_index": "static_ui_widget_index",
    "widget_layout_index": "static_ui_widget_index",
    "widget_ui_action_bridge": "static_ui_action_bridge",
    "ui_action_index": "static_ui_action_bridge",
    "attribute_state_map": "static_state_index",
    "object_ownership": "static_ownership_index",
    "execution_chains": "static_execution_flow",
    "subsystems": "subsystem_summary",
    "symbol_summaries": "symbol_summary",
    "source_file_index": "source_excerpt_index",
    "edit_ready_symbol_index": "source_excerpt_index",
    "snippet_index": "source_excerpt_index",
    "duplicate_symbols": "duplicate_detection",
    "test_links": "test_linking",
    "bucket_index": "subsystem_summary",
    "boundary_index": "architecture_boundary",
    "orchestration_index": "architecture_orchestration",
    "state_mutation_index": "static_state_index",
    "persistence_io_index": "static_persistence_index",
    "event_propagation_index": "static_event_flow",
    "canonical_conflict_index": "canonical_conflict_detection",
    "responsibility_overlap_index": "responsibility_overlap_detection",
    "feature_registry": "feature_mapping",
    "implementation_chronology_index": "implementation_status",
    "config_schema_registry": "configuration_schema",
    "state_lifecycle_index": "static_state_lifecycle",
    "change_impact_index": "change_impact",
    "active_code_index": "active_code_detection",
    "runtime_scenario_index": "runtime_scenario_evidence",
    "runtime_feature_attribution_index": "runtime_feature_evidence",
    "collector_insights": "summary",
}


def _safe_len(value: Any) -> int:
    """Return a defensive length for common containers."""
    if isinstance(value, (dict, list, tuple, set)):
        return len(value)
    return 0


def _classify_key(key: str) -> str:
    """Return a stable classification for a top-level collector key."""
    if key in KEY_CLASSIFICATIONS:
        return KEY_CLASSIFICATIONS[key]

    if key.endswith("_summary"):
        return "summary"

    if key.endswith("_hotspots") or key.endswith("_hotspot"):
        return "hotspot_summary"

    if key.endswith("_index"):
        return "index"

    if key.endswith("_counts") or key.endswith("_count"):
        return "summary"

    return "unclassified"


def validate_collector_output_contract(output: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the additive web-AI collector output contract.

    Missing recommended future keys are reported but do not fail this contract.
    The contract fails only when existing required canonical output keys are
    missing or when the payload is not mapping-like.
    """
    if not isinstance(output, Mapping):
        return {
            "ok": False,
            "error": "Collector output must be a mapping.",
            "missing_required_keys": list(REQUIRED_TOP_LEVEL_KEYS),
            "missing_recommended_future_keys": list(RECOMMENDED_FUTURE_WEB_AI_KEYS),
            "present_recommended_future_keys": [],
            "top_level_key_count": 0,
        }

    keys = set(str(key) for key in output.keys())
    required = set(REQUIRED_TOP_LEVEL_KEYS)
    future = set(RECOMMENDED_FUTURE_WEB_AI_KEYS)

    missing_required = sorted(required - keys)
    present_future = sorted(future & keys)
    missing_future = sorted(future - keys)

    return {
        "ok": not missing_required,
        "canonical_json_role": CANONICAL_JSON_ROLE,
        "top_level_key_count": len(keys),
        "required_key_count": len(REQUIRED_TOP_LEVEL_KEYS),
        "missing_required_keys": missing_required,
        "present_recommended_future_keys": present_future,
        "missing_recommended_future_keys": missing_future,
        "large_section_keys_present": sorted(set(LARGE_SECTION_KEYS) & keys),
        "additive_only_rule": (
            "Recommended future web-AI keys are optional and additive. "
            "They must not replace existing collector output keys."
        ),
    }


def build_collector_output_audit(output: Mapping[str, Any]) -> dict[str, Any]:
    """Build an audit summary for the collector output shape."""
    validation = validate_collector_output_contract(output)

    if not isinstance(output, Mapping):
        return {
            "validation": validation,
            "key_classification_counts": {},
            "top_level_keys": [],
            "large_sections": {},
        }

    key_classification_counts: dict[str, int] = {}
    key_rows: list[dict[str, Any]] = []

    for key in sorted(str(item) for item in output.keys()):
        classification = _classify_key(key)
        key_classification_counts[classification] = (
            key_classification_counts.get(classification, 0) + 1
        )
        value = output.get(key)
        key_rows.append(
            {
                "key": key,
                "classification": classification,
                "value_type": type(value).__name__,
                "item_count": _safe_len(value),
                "is_large_section_candidate": key in LARGE_SECTION_KEYS,
                "is_required_current_key": key in REQUIRED_TOP_LEVEL_KEYS,
                "is_recommended_future_key": key in RECOMMENDED_FUTURE_WEB_AI_KEYS,
            }
        )

    large_sections = {
        key: {
            "value_type": type(output.get(key)).__name__,
            "item_count": _safe_len(output.get(key)),
        }
        for key in LARGE_SECTION_KEYS
        if key in output
    }

    return {
        "validation": validation,
        "key_classification_counts": dict(sorted(key_classification_counts.items())),
        "top_level_keys": key_rows,
        "large_sections": large_sections,
        "recommended_first_additive_keys": [
            "web_ai_symbol_index",
            "stable_evidence_id_index",
            "primary_definition_index",
            "entry_points_detail",
        ],
    }
