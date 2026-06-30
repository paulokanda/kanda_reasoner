# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_state.py
"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

import logging

from typing import Any


def collect_visualizer_state(visualizer: Any) -> dict[str, Any]:
    """Support collect visualizer state behavior.
    
    Parameters
    ----------
    visualizer : Any
        The visualizer value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    state: dict[str, Any] = {}

    state["main_window_exists"] = getattr(visualizer, "main_window", None) is not None
    state["notebook_exists"] = getattr(visualizer, "notebook", None) is not None
    state["splash_exists"] = getattr(visualizer, "splash", None) is not None
    state["timeline_widget_exists"] = getattr(visualizer, "timeline_widget", None) is not None
    state["canvas_exists"] = getattr(visualizer, "canvas", None) is not None
    state["raw_exists"] = getattr(visualizer, "raw", None) is not None
    state["data_exists"] = getattr(visualizer, "data", None) is not None

    state["current_start"] = getattr(visualizer, "current_start", None)
    state["window_size"] = getattr(visualizer, "window_size", None)
    state["amplitude_scale"] = getattr(visualizer, "amplitude_scale", None)
    state["total_duration"] = getattr(visualizer, "total_duration", None)

    notebook = getattr(visualizer, "notebook", None)
    if notebook is not None:
        try:
            state["current_tab"] = notebook.tabText(notebook.currentIndex())
        except Exception:
            logging.exception("Boundary failure in collect_visualizer_state")
            state["current_tab"] = ""
    else:
        state["current_tab"] = ""

    return state
