"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

__all__ = [
    "build_runtime_scenario_hotspots",
    "build_runtime_scenario_index",
    "build_runtime_scenario_summary",
]

load_payload(__name__, globals(), 'zh')

# Make dynamic payload exports visible to static architecture validators.
build_runtime_scenario_hotspots = globals().get("build_runtime_scenario_hotspots")
build_runtime_scenario_index = globals().get("build_runtime_scenario_index")
build_runtime_scenario_summary = globals().get("build_runtime_scenario_summary")
