"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from typing import Any

from .prompt_classification import norm_text

__all__ = ["append_widget_registry_section"]


def _iter_filtered_widgets(
    widget_registry: dict[str, Any],
    subsystem_filters: list[str],
):
    for widget_id, record in widget_registry.items():
        widget_type = str(record.get("widget_type", "")).strip()
        if not widget_type:
            continue

        source_file = (
            widget_id.split("::")[0]
            if "::" in widget_id
            else str(record.get("source_file", "")).strip()
        )

        if subsystem_filters and not any(fragment in source_file for fragment in subsystem_filters):
            continue

        yield widget_id, record, widget_type, source_file


def append_widget_registry_section(
    lines: list[str],
    question: str,
    widget_registry: dict[str, Any] | None,
) -> None:
    if not widget_registry:
        return

    # Lazy import to avoid import-time cycles.
    from kanda_reasoner_app.reasoner_engine.query_router import (
        is_widget_listing_question,
    )

    if not is_widget_listing_question(question):
        return

    q_low = norm_text(question)
    subsystem_filters: list[str] = []
    subsystem_keywords = {
        "filter panel": "filter_panel",
        "filter_panel": "filter_panel",
        "shell": "shell/",
        "navbar": "navbar",
        "plugins": "plugins/",
        "common": "common/",
        "core": "core/",
        "montage": "montage",
        "statistics": "statistics",
        "amplitude": "amplitude",
        "eeg traces": "eeg_traces",
        "notebook": "notebook",
    }

    for keyword, path_fragment in subsystem_keywords.items():
        if keyword in q_low:
            subsystem_filters.append(path_fragment)

    lines.append("WIDGET REGISTRY")
    if subsystem_filters:
        lines.append(
            "Structured widget data filtered to the requested subsystem. "
            "The file path in each entry determines which subsystem the widget belongs to. "
            "List ALL entries below - a widget belongs to the filter panel if its file path "
            "contains 'filter_panel', to shell if it contains 'shell/', etc. "
            "List ALL matching entries including those with label=(none). "
            "Do not skip any entry. "
            "Do not mark any entry as INSUFFICIENT_EVIDENCE - all data here is authoritative and complete."
        )
    else:
        lines.append(
            "Structured widget data from the project. "
            "Use the file path to determine which subsystem each widget belongs to. "
            "List ALL entries below including those with label=(none). "
            "Do not skip any entry. "
            "Do not mark any entry as INSUFFICIENT_EVIDENCE - all data here is authoritative and complete."
        )

    for _, record, widget_type, source_file in _iter_filtered_widgets(
        widget_registry,
        subsystem_filters,
    ):
        variable_name = str(record.get("variable_name", "")).strip()
        display_text = str(record.get("display_text", "") or "").strip()
        label_text = (
            f"label={display_text!r}"
            if display_text
            else "label=(no label text - still include this entry)"
        )

        lines.append(
            widget_type
            + " | " + variable_name
            + " | " + label_text
            + " | file=" + source_file
        )

    lines.append("")


