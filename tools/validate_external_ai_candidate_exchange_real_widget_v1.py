"""Validate real PySide controls for outbound External AI Candidate Exchange."""
from __future__ import annotations

import os
from pathlib import Path
import sys
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _configure_offscreen_font_directory() -> str:
    if os.name != "nt":
        return "NOT_REQUIRED_NON_WINDOWS"
    configured = os.environ.get("QT_QPA_FONTDIR", "").strip()
    if configured:
        path = Path(configured)
        if not path.is_dir():
            raise RuntimeError("QT_QPA_FONTDIR_DOES_NOT_EXIST:" + str(path))
        return str(path)
    candidates = []
    for name in ("WINDIR", "SystemRoot"):
        value = os.environ.get(name, "").strip()
        if value:
            candidate = Path(value) / "Fonts"
            if candidate not in candidates:
                candidates.append(candidate)
    for candidate in candidates:
        if candidate.is_dir():
            os.environ["QT_QPA_FONTDIR"] = str(candidate)
            return str(candidate)
    raise RuntimeError(
        "QT_OFFSCREEN_FONT_DIRECTORY_NOT_FOUND:"
        + "|".join(str(item) for item in candidates)
    )


FONTDIR = _configure_offscreen_font_directory()
print("AI_EXCHANGE_QT_OFFSCREEN_FONTDIR_READY: PASS")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtWidgets import QApplication, QMainWindow  # noqa: E402

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.external_ai_candidate_exchange_gui import (  # noqa: E402
    build_external_ai_candidate_exchange_box,
    sync_external_ai_candidate_exchange_controls,
)

FEATURE_ID = "external-ai-candidate-exchange-real-widget-v1"


def main() -> None:
    app = QApplication.instance() or QApplication([])
    window = QMainWindow()
    box = build_external_ai_candidate_exchange_box(
        window,
        lambda _window: str(PROJECT_ROOT),
    )
    box.show()
    app.processEvents()

    copy_button = window._large_file_refactor_workbench_ai_exchange_copy_button
    folder_button = window._large_file_refactor_workbench_ai_exchange_folder_button
    path_button = window._large_file_refactor_workbench_ai_exchange_path_button
    clean_button = window._large_file_refactor_workbench_ai_exchange_clean_button
    assert not copy_button.isEnabled()
    assert not folder_button.isEnabled()
    assert not path_button.isEnabled()
    assert not clean_button.isEnabled()
    print("AI_EXCHANGE_REAL_WIDGET_INITIAL_FAIL_CLOSED: PASS")

    window._large_file_refactor_workbench_completion_evidence = object()
    window._large_file_refactor_workbench_aqr_context = object()
    window._large_file_refactor_workbench_advanced_quality_review = object()
    window._large_file_refactor_workbench_real_preview = object()
    window._large_file_refactor_workbench_plan_snapshot = object()
    sync_external_ai_candidate_exchange_controls(window)
    app.processEvents()
    assert copy_button.isEnabled()
    assert not folder_button.isEnabled()
    assert not path_button.isEnabled()
    assert not clean_button.isEnabled()
    print("AI_EXCHANGE_REAL_WIDGET_COPY_READY_AFTER_EVIDENCE: PASS")

    exchange_root = PROJECT_ROOT / "_release9_widget_exchange_fixture"
    exchange_root.mkdir(exist_ok=True)
    window._large_file_refactor_workbench_ai_exchange_result = SimpleNamespace(
        exchange_root=str(exchange_root)
    )
    sync_external_ai_candidate_exchange_controls(window)
    app.processEvents()
    assert copy_button.isEnabled()
    assert folder_button.isEnabled()
    assert path_button.isEnabled()
    assert clean_button.isEnabled()
    print("AI_EXCHANGE_REAL_WIDGET_FOLDER_CONTROLS_READY: PASS")

    box.close()
    app.processEvents()
    try:
        exchange_root.rmdir()
    except OSError:
        pass
    print("EXTERNAL_AI_CANDIDATE_EXCHANGE_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
