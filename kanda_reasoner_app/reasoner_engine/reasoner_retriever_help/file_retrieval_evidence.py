# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval_evidence.py
r"""Compact file evidence rendering for ProjectRetriever file retrieval."""
from __future__ import annotations

import re

__all__ = []


def build_compact_file_evidence(retriever, path: str, reasons: list[str]) -> str:
    """Build a compact file evidence.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    path : str
        The file or folder path.
    reasons : list[str]
        The reasons value.
    
    Returns
    -------
    str
        The string result.
    """
    
    file_record = retriever.idx.files_by_path.get(path, {})
    if not isinstance(file_record, dict):
        file_record = {}

    roles = retriever.idx.semantic_roles.get(path, {}).get("roles", [])
    advanced_ctx = retriever._collect_file_context_blobs(path)
    runtime_anchors, runtime_previews = retriever._get_runtime_anchor_summary(
        path,
        limit=12,
    )

    lines: list[str] = []
    lines.append("Path: " + path)

    module_name = file_record.get(
        "module_name",
        path[:-3].replace("\\", ".").replace("/", ".")
        if path.endswith(".py")
        else path,
    )

    lines.append("Module: " + str(module_name))
    lines.append("Reasons: " + ", ".join(sorted(set(reasons))))

    if roles:
        lines.append("Roles: " + ", ".join(roles))

    entry_markers = file_record.get("entry_markers", [])
    if entry_markers:
        lines.append("Entry markers: " + "; ".join(entry_markers[:6]))

    top_functions: list[str] = []
    for fn in file_record.get("functions", [])[:8]:
        top_functions.append(fn.get("qualname", "") + "@" + str(fn.get("lineno", "")))
    if top_functions:
        lines.append("Functions: " + " | ".join(top_functions))

    top_classes: list[str] = []
    for cls in file_record.get("classes", [])[:6]:
        class_text = cls.get("name", "") + "@" + str(cls.get("lineno", ""))
        methods = cls.get("methods", [])[:4]
        if methods:
            class_text += " methods=" + ",".join([m.get("name", "") for m in methods])
        top_classes.append(class_text)
    if top_classes:
        lines.append("Classes: " + " | ".join(top_classes))

    imports_out = sorted(retriever.idx.import_graph_out.get(path, []))
    if imports_out:
        lines.append("Imports out: " + " | ".join(imports_out[:8]))

    calls_out = sorted(retriever.idx.call_graph_out.get(path, []))
    if calls_out:
        lines.append("Calls out: " + " | ".join(calls_out[:10]))

    docstring = str(file_record.get("docstring", "")).strip()
    if docstring:
        docstring = re.sub(r"\s+", " ", docstring)
        lines.append("Docstring: " + docstring[:500])

    widget_count = len(retriever.idx.widgets_by_file.get(path, []))
    ui_action_count = len(retriever.idx.ui_actions_by_file.get(path, []))
    boundary_count = len(retriever.idx.boundaries_by_file.get(path, []))
    runtime_event_count = len(retriever.idx.runtime_events_by_file.get(path, []))
    hotspot_count = len(retriever.idx.hotspots_by_file.get(path, []))

    lines.append(
        "Advanced context: "
        + f"widgets={widget_count}, "
        + f"ui_actions={ui_action_count}, "
        + f"boundaries={boundary_count}, "
        + f"runtime_events={runtime_event_count}, "
        + f"hotspots={hotspot_count}"
    )

    if advanced_ctx["widgets"]:
        lines.append("Widget context: " + advanced_ctx["widgets"][:350])

    if advanced_ctx["ui_actions"]:
        lines.append("UI action context: " + advanced_ctx["ui_actions"][:350])

    if advanced_ctx["boundaries"]:
        lines.append("Boundary context: " + advanced_ctx["boundaries"][:250])

    if runtime_anchors:
        lines.append("Runtime anchors: " + " | ".join(runtime_anchors))

    if runtime_previews:
        lines.append("Runtime preview: " + " | ".join(runtime_previews[:4]))

    if advanced_ctx["runtime"]:
        lines.append("Runtime context: " + advanced_ctx["runtime"][:800])

    if advanced_ctx["hotspots"]:
        lines.append("Hotspot context: " + advanced_ctx["hotspots"][:250])

    qt_signal_map = getattr(retriever.idx, "qt_signal_map", [])
    if isinstance(qt_signal_map, list):
        sig_lines: list[str] = []
        for sig_record in qt_signal_map:
            if not isinstance(sig_record, dict):
                continue
            if str(sig_record.get("source_file", "")).strip() != path:
                continue
            sig_name = str(sig_record.get("signal_name", "")).strip()
            target = str(sig_record.get("target", "")).strip()
            src_sym = str(sig_record.get("source_symbol", "")).strip()
            if sig_name or target:
                sig_lines.append(
                    sig_name
                    + (" -> " + target if target else "")
                    + (" [" + src_sym + "]" if src_sym else "")
                )
        if sig_lines:
            lines.append("Qt signals: " + " | ".join(sig_lines[:12]))

    return "\n".join(lines)
