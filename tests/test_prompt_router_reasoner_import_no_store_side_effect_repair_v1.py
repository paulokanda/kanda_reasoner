"""Validation tests for Prompt Router Reasoner Import No-Store Side-Effect Repair v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import REVIEW_FOLDER_NAME

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "prompt_router_reasoner_gui"
    / "prompt_router_reasoner_tab.py"
)
PYSIDE_AVAILABLE = importlib.util.find_spec("PySide6") is not None


def _source_text() -> str:
    return TAB_SOURCE_PATH.read_text(encoding="utf-8")


def test_import_availability_source_checks_review_dir_before_store_creation() -> None:
    source = _source_text()
    assert "def _latest_import_dataset_file_text" in source
    assert "review_dir = project_root / REVIEW_FOLDER_NAME" in source
    assert "if not review_dir.exists():" in source
    assert "A disabled import button must not create" in source


def test_import_buttons_do_not_create_review_store_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert TAB_SOURCE_PATH.exists()
        return

    from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        state = widget.get_import_review_dataset_state()

        assert not (root / REVIEW_FOLDER_NAME).exists()
        assert state["latest_dataset_file"] == ""
        assert state["preview_import_enabled"] is False
        assert state["import_enabled"] is False
        assert "No Prompt Router Reasoner review store" in widget.review_list_status_label.text()


def test_import_repair_does_not_expose_forbidden_runtime_authority() -> None:
    source = _source_text()
    forbidden = [
        "ask_local_ai",
        "project_freeze_ledger",
        "frozen_features_memory",
        "router_with_ml_radio.setEnabled(True)",
    ]
    for text in forbidden:
        assert text not in source


if __name__ == "__main__":
    test_import_availability_source_checks_review_dir_before_store_creation()
    test_import_buttons_do_not_create_review_store_if_pyside_available()
    test_import_repair_does_not_expose_forbidden_runtime_authority()
    print("VALIDATION OK: prompt router reasoner import no-store side-effect repair")
