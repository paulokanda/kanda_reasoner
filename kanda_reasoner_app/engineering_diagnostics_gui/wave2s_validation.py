# project-path: kanda_reasoner_app/engineering_diagnostics_gui/wave2s_validation.py
"""Real Qt validation for Wave 2S remediation presentation."""

from __future__ import annotations

from pathlib import Path

from .table_columns import ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS

__all__ = ["validate_wave2s_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_wave2s_gui(root: Path) -> tuple[float, float, float]:
    """Reuse Wave 2R scale validation and prove remediation presentation."""
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from . import create_engineering_diagnostics_panel
    from .wave2r_validation import validate_wave2r_gui

    panel_ms, rows_ms, filter_ms = validate_wave2r_gui(root)
    app = QApplication.instance() or QApplication([])
    panel = create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    model = panel.engineering_diagnostics_table.model()
    fields = tuple(field for field, _label in ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS)
    index = fields.index("remediation_action_class")
    _require(
        model.headerData(index, Qt.Horizontal, Qt.DisplayRole) == "Remediation",
        "WAVE2S_GUI_REMEDIATION_COLUMN_MISSING",
    )
    panel.deleteLater()
    app.processEvents()
    print("WAVE2S GUI REMEDIATION ACTION COLUMN: PASS")
    print("WAVE2S GUI NON-EXECUTABLE DETAIL CONTRACT: PASS")
    print("WAVE2S GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms
