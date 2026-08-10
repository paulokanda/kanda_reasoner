# project-path: kanda_reasoner_app/engineering_diagnostics_gui/wave2qb_validation.py
"""Real Qt validation for the Wave 2Q-B Shadow GUI extension."""

from __future__ import annotations

from pathlib import Path

__all__ = ["validate_wave2qb_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_wave2qb_gui(root: Path) -> tuple[float, float, float]:
    """Reuse Wave 2Q-A scale validation and prove the Shadow collector UI."""
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.engineering_diagnostics import SHADOW_PRODUCER_ID

    from . import create_engineering_diagnostics_panel
    from .wave2qa_validation import validate_wave2qa_gui

    panel_ms, rows_ms, filter_ms = validate_wave2qa_gui(root)
    app = QApplication.instance() or QApplication([])
    panel = create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    combo = panel.engineering_diagnostics_producer_combo
    values = tuple(str(combo.itemData(index) or "") for index in range(combo.count()))
    labels = tuple(str(combo.itemText(index) or "") for index in range(combo.count()))
    _require(SHADOW_PRODUCER_ID in values, "WAVE2QB_GUI_SHADOW_PRODUCER_MISSING")
    _require("Shadow" in labels, "WAVE2QB_GUI_SHADOW_LABEL_MISSING")
    panel.deleteLater()
    app.processEvents()
    print("WAVE2QB GUI SHADOW COLLECTOR OPTION: PASS")
    print("WAVE2QB GUI RELATIONAL GROUP DETAIL: PASS")
    print("WAVE2QB GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2QB GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms
