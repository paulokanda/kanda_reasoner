# project-path: kanda_reasoner_app/engineering_diagnostics_gui/wave2qa_validation.py
"""Real Qt validation owned by the Engineering Diagnostics GUI Box."""

from __future__ import annotations

from pathlib import Path
import time

__all__ = ["validate_wave2qa_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_wave2qa_gui(root: Path) -> tuple[float, float, float]:
    """Exercise the real Qt factory and 25,000-row grouping filter."""
    from PySide6.QtCore import QElapsedTimer
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.engineering_diagnostics import (
        BOM_PRODUCER_ID,
        DiagnosticFindingRecord,
        DiagnosticGroupRecord,
    )

    from . import DiagnosticFindingView, create_engineering_diagnostics_panel

    app = QApplication.instance() or QApplication([])
    started = time.perf_counter()
    panel = create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    panel_ms = (time.perf_counter() - started) * 1000.0
    _require(
        hasattr(panel, "engineering_diagnostics_group_combo"),
        "GUI_GROUP_FILTER_MISSING",
    )
    buttons = getattr(panel, "engineering_diagnostics_grouping_buttons", {})
    _require(
        set(buttons) == {"create", "move", "ungroup", "review"},
        "GUI_GROUPING_ACTIONS_MISSING",
    )
    group = DiagnosticGroupRecord(
        "group-a",
        "project",
        BOM_PRODUCER_ID,
        "scope",
        "DETERMINISTIC",
        "bom.rule_file.v1",
        "BOM_UTF8 in pkg/a.py",
        "high",
        tuple("issue-" + str(index) for index in range(25000)),
        evidence={"root_cause_claimed": False},
    )
    rows = tuple(
        DiagnosticFindingView(
            DiagnosticFindingRecord(
                "scale-run",
                "issue-" + str(index),
                "evidence-" + str(index),
                "BOM_UTF8",
                "pkg/file_" + str(index).zfill(5) + ".py",
                "Synthetic finding " + str(index),
                "warning",
                "high",
                "BOM_UTF8",
                "",
                "location-" + str(index),
                "bom",
                1,
                {},
                "Review.",
            ),
            "current",
            groups=(group,),
        )
        for index in range(25000)
    )
    model = panel.engineering_diagnostics_table.model()
    timer = QElapsedTimer()
    timer.start()
    model.set_rows(rows)
    app.processEvents()
    rows_ms = float(timer.elapsed())
    timer.restart()
    model.set_filters(
        "all", "all", "all", "all", "all", "deterministic", "24998"
    )
    _require(model.rowCount() == 1, "GUI_GROUP_FILTER_RESULT_MISMATCH")
    app.processEvents()
    filter_ms = float(timer.elapsed())
    _require(panel_ms < 2000.0, "GUI_PANEL_CREATION_TARGET_EXCEEDED")
    _require(rows_ms < 2000.0, "GUI_25000_ROW_TARGET_EXCEEDED")
    _require(filter_ms < 500.0, "GUI_FILTER_TARGET_EXCEEDED")
    panel.deleteLater()
    app.processEvents()
    print("ENGINEERING DIAGNOSTICS GUI COMPLETE IMPORT GRAPH: PASS")
    print("ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS")
    print("WAVE2QA GUI GROUP FILTER: PASS")
    print("WAVE2QA GUI MANUAL GROUPING ACTIONS: PASS")
    print("WAVE2QA GUI DIRECT INDEXED MODEL: PASS")
    print("WAVE2QA GUI 25000 ROW INITIALIZATION MS: " + f"{rows_ms:.1f}")
    print("WAVE2QA GUI FILTER UPDATE MS: " + f"{filter_ms:.1f}")
    print("WAVE2QA GUI PANEL CREATION MS: " + f"{panel_ms:.1f}")
    print("WAVE2QA GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms
