# project-path: kanda_reasoner_app/reasoner_engine/index_loader_help/index_builders.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

__all__ = [
    "build_boundary_indexes",
    "build_core_file_and_symbol_indexes",
    "build_hotspot_indexes",
    "build_import_and_call_graph_indexes",
    "build_runtime_indexes",
    "build_snippet_lookup_index",
    "build_ui_action_indexes",
    "build_widget_indexes",
]

import warnings
from typing import Any


def rebuild_indexes(index: Any) -> None:
    """Support rebuild indexes behavior.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    index.files_by_path.clear()
    index.files_by_module.clear()
    index.symbol_details.clear()
    index.symbol_to_file.clear()
    index.import_graph_out.clear()
    index.call_graph_out.clear()

    index.widgets_by_file.clear()
    index.ui_actions_by_file.clear()
    index.boundaries_by_file.clear()
    index.runtime_events_by_file.clear()
    index.runtime_signal_connections_by_sender.clear()
    index.runtime_signal_connections_by_receiver.clear()
    index.hotspots_by_file.clear()
    index.snippets_by_file.clear()

    if not index.index_data:
        return

    build_core_file_and_symbol_indexes(index)
    build_snippet_lookup_index(index)
    build_import_and_call_graph_indexes(index)
    build_widget_indexes(index)
    build_ui_action_indexes(index)
    build_boundary_indexes(index)
    build_runtime_indexes(index)
    build_hotspot_indexes(index)

    if not index.files_by_path:
        warnings.warn(
            "files_by_path is empty after loading. "
            "The JSON may be incomplete or missing the 'files' top-level key. "
            "Retrieval precision will be severely degraded.",
            RuntimeWarning,
            stacklevel=2,
        )


def build_snippet_lookup_index(index: Any) -> None:
    """
    Build a file-path keyed snippet lookup from snippet_index so later
    retrieval can serve code snippets directly from the assembled JSON.
    """
    for symbol_name, rec in index._safe_dict(index.snippet_index).items():
        if not isinstance(rec, dict):
            continue

        path = index._safe_text(rec.get("file"))
        if not path:
            continue

        snippet_text = index._safe_text(rec.get("snippet"))
        if not snippet_text:
            continue

        index.snippets_by_file[path].append(
            {
                "symbol_name": index._safe_text(symbol_name),
                "line": index._safe_int(rec.get("line_start"), 1),
                "line_end": index._safe_int(rec.get("line_end"), 1),
                "snippet": snippet_text,
            }
        )


def build_core_file_and_symbol_indexes(index: Any) -> None:
    """Build a core file and symbol indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    for file_record in index._safe_list(index.index_data.get("files")):
        if not isinstance(file_record, dict):
            continue

        path = index._safe_text(file_record.get("path"))
        module_name = index._safe_text(file_record.get("module_name"))

        if path:
            index.files_by_path[path] = file_record
        if module_name:
            index.files_by_module[module_name] = file_record

        for fn in index._safe_list(file_record.get("functions")):
            if not isinstance(fn, dict):
                continue
            qualname = index._safe_text(fn.get("qualname"))
            if qualname:
                index.symbol_details[qualname] = {
                    "file": path,
                    "line": index._safe_int(fn.get("lineno"), 1),
                    "kind": "function",
                    "record": fn,
                }
                if path:
                    index.symbol_to_file[qualname].add(path)

        for cls in index._safe_list(file_record.get("classes")):
            if not isinstance(cls, dict):
                continue

            cls_name = index._safe_text(cls.get("name"))
            if cls_name:
                index.symbol_details[cls_name] = {
                    "file": path,
                    "line": index._safe_int(cls.get("lineno"), 1),
                    "kind": "class",
                    "record": cls,
                }
                if path:
                    index.symbol_to_file[cls_name].add(path)

            for method in index._safe_list(cls.get("methods")):
                if not isinstance(method, dict):
                    continue
                qualname = index._safe_text(method.get("qualname"))
                if qualname:
                    index.symbol_details[qualname] = {
                        "file": path,
                        "line": index._safe_int(method.get("lineno"), 1),
                        "kind": "method",
                        "record": method,
                    }
                    if path:
                        index.symbol_to_file[qualname].add(path)


def build_import_and_call_graph_indexes(index: Any) -> None:
    """Build a import and call graph indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    for src_module, targets in index._safe_dict(index.index_data.get("import_graph")).items():
        src_path = index.resolve_module_to_path(str(src_module)) or str(src_module)
        for target in index._safe_list(targets):
            target_text = index._safe_text(target)
            if target_text:
                index.import_graph_out[src_path].add(target_text)

    for edge in index._safe_list(index.index_data.get("call_edges")):
        if not isinstance(edge, dict):
            continue
        from_file = index._safe_text(edge.get("from_file"))
        to_call = index._safe_text(edge.get("to_call"))
        if from_file and to_call:
            index.call_graph_out[from_file].add(to_call)


def build_widget_indexes(index: Any) -> None:
    """Build a widget indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    for file_path, widget_data in index.widget_registry.items():
        file_key = index._safe_text(file_path)
        if not file_key:
            continue

        if isinstance(widget_data, dict):
            record = {"file": file_key, "record": widget_data}
            index.widgets_by_file[file_key].append(record)
        elif isinstance(widget_data, list):
            for item in widget_data:
                if isinstance(item, dict):
                    index.widgets_by_file[file_key].append({"file": file_key, "record": item})


def build_ui_action_indexes(index: Any) -> None:
    """Build a ui action indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    for file_path, action_data in index.ui_action_index.items():
        file_key = index._safe_text(file_path)
        if not file_key:
            continue

        if isinstance(action_data, list):
            for item in action_data:
                if isinstance(item, dict):
                    index.ui_actions_by_file[file_key].append(item)
        elif isinstance(action_data, dict):
            index.ui_actions_by_file[file_key].append(action_data)


def build_boundary_indexes(index: Any) -> None:
    """Build a boundary indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    for file_path, boundary_data in index.boundary_index.items():
        file_key = index._safe_text(file_path)
        if not file_key:
            continue

        if isinstance(boundary_data, list):
            for item in boundary_data:
                if isinstance(item, dict):
                    index.boundaries_by_file[file_key].append(item)
        elif isinstance(boundary_data, dict):
            index.boundaries_by_file[file_key].append(boundary_data)


def build_runtime_indexes(index: Any) -> None:
    """Build a runtime indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    for item in index.runtime_signal_connections:
        if not isinstance(item, dict):
            continue

        normalized_source_file = index._resolve_runtime_source_file(
            str(item.get("source_file", "")).strip()
        )
        if normalized_source_file:
            item["source_file"] = normalized_source_file

        sender_name = index._safe_text(item.get("sender_name"))
        receiver_name = index._safe_text(item.get("receiver_name"))

        if sender_name:
            index.runtime_signal_connections_by_sender[sender_name].append(item)
        if receiver_name:
            index.runtime_signal_connections_by_receiver[receiver_name].append(item)

        if normalized_source_file:
            index.runtime_events_by_file[normalized_source_file].append(
                {
                    "type": "signal_connection",
                    "event_type": "signal_connection",
                    "source_file": normalized_source_file,
                    "source_symbol": index._safe_text(item.get("slot_name")),
                    "object_name": sender_name,
                    "object_type": index._safe_text(item.get("sender_type")),
                    "message": index._safe_text(item.get("signal_name"))
                    + " -> "
                    + index._safe_text(item.get("slot_name")),
                    "record": item,
                }
            )

    raw_events = index._safe_list(index.runtime_trace_raw.get("events"))
    for event in raw_events:
        if not isinstance(event, dict):
            continue

        normalized_source_file = index._resolve_runtime_source_file(
            str(event.get("source_file", "")).strip()
        )
        if normalized_source_file:
            event["source_file"] = normalized_source_file
            index.runtime_events_by_file[normalized_source_file].append(event)

    for snapshot in index.runtime_state_snapshots:
        if not isinstance(snapshot, dict):
            continue

        state = index._safe_dict(snapshot.get("state"))
        source_file = index._resolve_runtime_source_file(
            index._safe_text(state.get("source_file"))
        )
        if source_file:
            index.runtime_events_by_file[source_file].append(
                {
                    "type": "state_snapshot",
                    "event_type": "state_snapshot",
                    "source_file": source_file,
                    "record": snapshot,
                }
            )


def build_hotspot_indexes(index: Any) -> None:
    """Build a hotspot indexes.
    
    Parameters
    ----------
    index : Any
        The index value.
    """
    
    hotspot_groups = [
        index.widget_hotspots,
        index.widget_text_hotspots,
        index.widget_layout_hotspots,
        index.widget_ui_action_hotspots,
        index.ui_action_hotspots,
        index.boundary_violation_hotspots,
        index.orchestration_hotspots,
        index.state_mutation_hotspots,
        index.persistence_io_hotspots,
        index.event_propagation_hotspots,
        index.legacy_shadow_hotspots,
        index.overlap_hotspots,
        index.feature_hotspots,
        index.migration_transition_hotspots,
        index.schema_risk_hotspots,
        index.state_lifecycle_hotspots,
        index.high_risk_edit_hotspots,
        index.untested_critical_hotspots,
        index.runtime_scenario_hotspots,
        index.runtime_feature_attribution_hotspots,
    ]

    for hotspot_list in hotspot_groups:
        for item in hotspot_list:
            if not isinstance(item, dict):
                continue

            file_candidates = [
                index._safe_text(item.get("file")),
                index._safe_text(item.get("path")),
                index._safe_text(item.get("source_file")),
            ]

            for file_key in file_candidates:
                if file_key:
                    index.hotspots_by_file[file_key].append(item)
                    break

