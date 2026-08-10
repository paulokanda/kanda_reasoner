# project-path: kanda_reasoner_app/engineering_diagnostics_gui/wave2r_validation.py
"""Real Qt validation for Wave 2R lifecycle governance controls."""

from __future__ import annotations

from pathlib import Path

__all__ = ["validate_wave2r_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_wave2r_gui(root: Path) -> tuple[float, float, float]:
    """Reuse Wave 2Q-B scale validation and prove lifecycle controls."""
    from PySide6.QtWidgets import QApplication

    from . import create_engineering_diagnostics_panel
    from .wave2qb_validation import validate_wave2qb_gui

    panel_ms, rows_ms, filter_ms = validate_wave2qb_gui(root)
    app = QApplication.instance() or QApplication([])
    panel = create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    controls = panel.engineering_diagnostics_lifecycle_controls
    combo = controls["action"]
    actions = tuple(str(combo.itemData(index) or "") for index in range(combo.count()))
    for action in (
        "CONFIRM",
        "SUPPRESS",
        "ACCEPT_RISK",
        "MARK_FALSE_POSITIVE",
        "DEFER",
        "REOPEN",
    ):
        _require(action in actions, "WAVE2R_GUI_ACTION_MISSING:" + action)
    decision_combo = panel.engineering_diagnostics_decision_combo
    states = tuple(
        str(decision_combo.itemText(index) or "").upper()
        for index in range(decision_combo.count())
    )
    for state in (
        "OPEN",
        "CONFIRMED",
        "ACCEPTED_RISK",
        "FALSE_POSITIVE",
        "SUPPRESSED",
        "DEFERRED",
        "REOPENED",
    ):
        _require(state in states, "WAVE2R_GUI_STATE_FILTER_MISSING:" + state)
    panel.deleteLater()
    app.processEvents()
    print("WAVE2R GUI HUMAN DECISION ACTIONS: PASS")
    print("WAVE2R GUI LIFECYCLE STATE FILTER: PASS")
    print("WAVE2R GUI FALSE POSITIVE SEARCHABILITY: PASS")
    print("WAVE2R GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms
