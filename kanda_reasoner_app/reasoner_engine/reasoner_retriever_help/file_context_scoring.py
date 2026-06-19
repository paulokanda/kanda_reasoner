"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help
# PURPOSE       : Provide advanced file-context and runtime scoring helpers for retriever ranking.
# EXPORTS       : get_runtime_anchor_summary, collect_file_context_blobs, score_advanced_file_context, score_runtime_signal_matches
# DEPENDS ON    : query_text.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    norm_text,
    tokenize_query,
)

__all__ = [
    "get_runtime_anchor_summary",
    "collect_file_context_blobs",
    "score_advanced_file_context",
    "score_runtime_signal_matches",
]


def get_runtime_anchor_summary(idx, path: str, limit: int = 12) -> tuple[list[str], list[str]]:
    runtime_events = idx.runtime_events_by_file.get(path, [])

    preferred_order: list[str] = []
    secondary_order: list[str] = []
    previews: list[str] = []

    seen_preferred: set[str] = set()
    seen_secondary: set[str] = set()
    seen_previews: set[str] = set()

    preferred_exact_terms = [
        "runtime_runner_probe_apply_button",
        "runtime_runner_probe_line_edit",
        "runtime_runner_probe_close_button",
        "on_apply_clicked",
        "on_text_changed",
        "on_close_clicked",
    ]

    for item in runtime_events:
        if not isinstance(item, dict):
            continue

        source_symbol = str(item.get("source_symbol", "")).strip()
        object_name = str(item.get("object_name", "")).strip()
        event_type = str(item.get("event_type", "")).strip()
        message = str(item.get("message", "")).strip()

        candidates = [source_symbol, object_name, event_type]

        for value in candidates:
            if not value:
                continue

            if value in preferred_exact_terms:
                if value not in seen_preferred:
                    seen_preferred.add(value)
                    preferred_order.append(value)
                continue

            if value not in seen_secondary:
                seen_secondary.add(value)
                secondary_order.append(value)

        if message and message not in seen_previews:
            seen_previews.add(message)
            previews.append(message)

    anchors = preferred_order + secondary_order
    return anchors[:limit], previews[:limit]



def collect_file_context_blobs(idx, path: str) -> dict[str, str]:
    widgets = idx.widgets_by_file.get(path, [])
    ui_actions = idx.ui_actions_by_file.get(path, [])
    boundaries = idx.boundaries_by_file.get(path, [])
    runtime_events = idx.runtime_events_by_file.get(path, [])
    hotspots = idx.hotspots_by_file.get(path, [])

    widget_blob_parts: list[str] = []
    for item in widgets[:80]:
        record = item.get("record", {}) if isinstance(item, dict) else {}
        if isinstance(record, dict):
            widget_blob_parts.append(str(record.get("object_name", "")))
            widget_blob_parts.append(str(record.get("widget_type", "")))
            widget_blob_parts.append(str(record.get("text", "")))
            widget_blob_parts.append(str(record.get("label", "")))

    ui_blob_parts: list[str] = []
    for item in ui_actions[:80]:
        if isinstance(item, dict):
            ui_blob_parts.append(str(item.get("action", "")))
            ui_blob_parts.append(str(item.get("signal", "")))
            ui_blob_parts.append(str(item.get("slot", "")))
            ui_blob_parts.append(str(item.get("handler", "")))
            ui_blob_parts.append(str(item.get("target", "")))

    boundary_blob_parts: list[str] = []
    for item in boundaries[:80]:
        if isinstance(item, dict):
            boundary_blob_parts.append(str(item.get("boundary_role", "")))
            boundary_blob_parts.append(str(item.get("role", "")))
            boundary_blob_parts.append(str(item.get("layer", "")))
            boundary_blob_parts.append(str(item.get("kind", "")))

    runtime_blob_parts: list[str] = []
    for item in runtime_events[:80]:
        if isinstance(item, dict):
            runtime_blob_parts.append(str(item.get("event_type", "")))
            runtime_blob_parts.append(str(item.get("type", "")))
            runtime_blob_parts.append(str(item.get("message", "")))
            runtime_blob_parts.append(str(item.get("source_symbol", "")))
            runtime_blob_parts.append(str(item.get("object_name", "")))
            runtime_blob_parts.append(str(item.get("object_type", "")))

    hotspot_blob_parts: list[str] = []
    for item in hotspots[:80]:
        if isinstance(item, dict):
            hotspot_blob_parts.append(str(item.get("kind", "")))
            hotspot_blob_parts.append(str(item.get("feature", "")))
            hotspot_blob_parts.append(str(item.get("reason", "")))
            hotspot_blob_parts.append(str(item.get("message", "")))
            hotspot_blob_parts.append(str(item.get("summary", "")))

    return {
        "widgets": norm_text(" ".join(widget_blob_parts)),
        "ui_actions": norm_text(" ".join(ui_blob_parts)),
        "boundaries": norm_text(" ".join(boundary_blob_parts)),
        "runtime": norm_text(" ".join(runtime_blob_parts)),
        "hotspots": norm_text(" ".join(hotspot_blob_parts)),
    }



def score_advanced_file_context(idx, q: str,
    path: str,
    tokens: list[str],
    reasons: list[str],
) -> int:
    score = 0

    ctx = collect_file_context_blobs(idx, path)

    widget_blob = ctx["widgets"]
    ui_blob = ctx["ui_actions"]
    boundary_blob = ctx["boundaries"]
    runtime_blob = ctx["runtime"]
    hotspot_blob = ctx["hotspots"]

    all_advanced = " ".join(
        [widget_blob, ui_blob, boundary_blob, runtime_blob, hotspot_blob]
    )

    for token in tokens:
        if token and token in all_advanced:
            score += 2
            reasons.append("advanced-token:" + token)

    runtime_terms = [
        "runtime",
        "trace",
        "signal",
        "slot",
        "snapshot",
        "event",
        "clicked",
        "textchanged",
    ]
    if any(term in q for term in runtime_terms):
        if runtime_blob:
            score += 30
            reasons.append("runtime-context-boost")
        if ui_blob:
            score += 20
            reasons.append("runtime-ui-action-boost")

    widget_terms = [
        "widget",
        "button",
        "line edit",
        "lineedit",
        "label",
        "combobox",
        "dropdown",
        "layout",
        "tab",
    ]

    # Boost the main window builder file for "main window class" questions
    main_window_terms = ["main window", "mainwindow", "main_window"]
    if any(term in q for term in main_window_terms):
        if "main_window_builder" in path or "eeg_main_window" in path:
            score += 400
            reasons.append("main-window-builder-boost")
        # Penalise kanda_main for "main window class" questions -
        # it is the entry script not the window class definition
        if "kanda_main" in path and "class" in q:
            score -= 300
            reasons.append("kanda-main-window-class-penalty")

    # Boost notebook/tab files for tab switching questions
    tab_switch_terms = ["tab switch", "tab switching", "switching logic", "tab management"]
    if any(term in q for term in tab_switch_terms):
        if "notebook" in path or "tab_base" in path or "tab_template" in path:
            score += 200
            reasons.append("tab-switch-boost")

    if any(term in q for term in widget_terms):
        if widget_blob:
            score += 28
            reasons.append("widget-context-boost")
        if ui_blob:
            score += 18
            reasons.append("widget-ui-action-boost")

            # Boost files with button/label widget registry entries for list queries
            list_widget_terms = [
                "list all", "list the", "show all", "show me all",
                "all buttons", "all widgets", "all labels",
            ]
            if any(term in q for term in list_widget_terms):
                widget_entries = idx.widgets_by_file.get(path, [])
                button_entries = [
                    w for w in widget_entries
                    if str(w.get("widget_type", "")).lower() in
                       {"qpushbutton", "qtoolbutton", "qcheckbox", "qradiobutton"}
                ]
                if button_entries:
                    score += 120
                    reasons.append("widget-registry-button-boost")
                label_entries = [
                    w for w in widget_entries
                    if str(w.get("widget_type", "")).lower() == "qlabel"
                ]
                if label_entries:
                    score += 40
                    reasons.append("widget-registry-label-boost")

    boundary_terms = [
        "boundary",
        "controller",
        "service",
        "domain",
        "orchestration",
        "orchestrator",
        "layer",
        "architecture",
        "responsibility split",
    ]
    if any(term in q for term in boundary_terms):
        if boundary_blob:
            score += 30
            reasons.append("boundary-context-boost")
        if hotspot_blob:
            score += 10
            reasons.append("boundary-hotspot-boost")

    hotspot_terms = [
        "hotspot",
        "risk",
        "high risk",
        "overlap",
        "legacy",
        "conflict",
        "migration",
        "schema",
        "impact",
        "untested",
    ]
    if any(term in q for term in hotspot_terms):
        if hotspot_blob:
            score += 26
            reasons.append("hotspot-context-boost")

    return score



def score_runtime_signal_matches(idx, q: str,
    reasons: list[str],
) -> tuple[int, set[str]]:
    score = 0
    matched_paths: set[str] = set()

    raw_events = idx.get_runtime_trace_events()
    signal_connections = idx.runtime_signal_connections

    for item in signal_connections[:200]:
        if not isinstance(item, dict):
            continue

        sender_name = norm_text(item.get("sender_name", ""))
        signal_name = norm_text(item.get("signal_name", ""))
        slot_name = norm_text(item.get("slot_name", ""))
        source_file = str(item.get("source_file", "")).strip()

        combined = " ".join([sender_name, signal_name, slot_name, norm_text(source_file)])

        if combined and any(term in combined for term in tokenize_query(q)):
            score += 4
            reasons.append("runtime-signal-match")
            if source_file:
                matched_paths.add(source_file)

    for event in raw_events[:300]:
        if not isinstance(event, dict):
            continue

        source_file = str(event.get("source_file", "")).strip()
        combined = " ".join(
            [
                norm_text(event.get("event_type", "")),
                norm_text(event.get("type", "")),
                norm_text(event.get("message", "")),
                norm_text(event.get("source_symbol", "")),
                norm_text(event.get("object_name", "")),
                norm_text(event.get("object_type", "")),
            ]
        )
        if combined and any(term in combined for term in tokenize_query(q)):
            score += 2
            reasons.append("runtime-event-match")
            if source_file:
                matched_paths.add(source_file)

    return score, matched_paths








