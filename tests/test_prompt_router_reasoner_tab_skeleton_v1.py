"""Validation tests for Prompt Router Reasoner Tab Skeleton v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    ROUTER_WITH_HEURISTICS,
    ROUTER_WITH_HELP_OF_ML,
    ROUTER_WITH_ML,
)
from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

PROMPT_ROUTER_REASONER_TAB_TITLE = "Prompt Router Reasoner"
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


def test_prompt_router_reasoner_tab_is_registered_as_lazy_tool() -> None:
    matching = [spec for spec in TOOLS if getattr(spec, "tab_id", "") == "prompt_router_reasoner"]
    assert len(matching) == 1
    spec = matching[0]
    assert spec.step_title == PROMPT_ROUTER_REASONER_TAB_TITLE
    assert spec.tab_kind == "lazy_tool"
    assert spec.module_candidates == (
        "kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab",
    )
    assert spec.class_candidates == ("PromptRouterReasonerTab",)


def test_prompt_router_reasoner_tab_source_declares_required_controls() -> None:
    source = _source_text()
    required_text = [
        "class PromptRouterReasonerTab(QWidget)",
        "PromptRouterReasonerTabContract",
        "Router with heuristics",
        "Router with help of ML",
        "Router with ML - LOCKED",
        "Generator text review queue",
        "Heuristic/default selected prompt",
        "ML selected prompt",
        "Heuristics correct",
        "ML correct",
        "Both acceptable / unclear",
        "Ask AI",
        "Save review",
        "Undo last save",
        "Heuristics correctness: 0%",
        "ML correctness: 0%",
        "ML Pilot Readiness: LOCKED",
        "wired_to_runtime_router=False",
    ]
    for text in required_text:
        assert text in source


def test_prompt_router_reasoner_tab_source_has_no_runtime_router_wiring() -> None:
    source = _source_text()
    forbidden_runtime_wiring = [
        "SessionService(",
        "route_query_intent(",
        ".execute(",
        "ask_local_ai",
        "set_mode(",
        "create_pending_review(",
        "project_freeze_ledger",
        "frozen_features_memory",
    ]
    for text in forbidden_runtime_wiring:
        assert text not in source


def test_prompt_router_reasoner_tab_qt_widget_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert TAB_SOURCE_PATH.exists()
        return

    from PySide6.QtWidgets import (  # type: ignore[import-not-found]
        QApplication,
        QGroupBox,
        QPushButton,
        QRadioButton,
        QSplitter,
    )
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    widget = PromptRouterReasonerTab()
    assert widget.objectName() == "PromptRouterReasonerTab"
    assert widget.contract().to_dict() == {
        "tab_title": PROMPT_ROUTER_REASONER_TAB_TITLE,
        "default_router_mode": ROUTER_WITH_HEURISTICS,
        "ml_mode_locked": True,
        "has_three_columns": True,
        "has_review_controls": True,
        "has_ask_ai_button": True,
        "has_readiness_bars": True,
        "wired_to_runtime_router": False,
    }
    assert widget.get_declared_router_modes() == (
        ROUTER_WITH_HEURISTICS,
        ROUTER_WITH_HELP_OF_ML,
        ROUTER_WITH_ML,
    )
    assert widget.is_ml_pilot_control_locked() is True
    assert widget.router_with_heuristics_radio.isChecked() is True
    assert widget.router_with_ml_radio.isEnabled() is False

    splitter = widget.findChild(QSplitter, "prompt_router_reasoner_three_column_splitter")
    assert splitter is not None
    assert splitter.count() == 3

    group_titles = {group.title() for group in widget.findChildren(QGroupBox)}
    assert "Generator text review queue" in group_titles
    assert "Heuristic/default selected prompt" in group_titles
    assert "ML selected prompt" in group_titles

    radio_texts = {button.text() for button in widget.findChildren(QRadioButton)}
    assert "Router with heuristics" in radio_texts
    assert "Router with help of ML" in radio_texts
    assert "Router with ML - LOCKED" in radio_texts
    assert "Heuristics correct" in radio_texts
    assert "ML correct" in radio_texts
    assert "Both acceptable / unclear" in radio_texts

    button_texts = {button.text() for button in widget.findChildren(QPushButton)}
    assert "Ask AI" in button_texts
    assert "Save review" in button_texts
    assert "Undo last save" in button_texts


def test_prompt_router_reasoner_tab_skeleton_does_not_create_review_store(tmp_path: Path) -> None:
    before = set(tmp_path.rglob("*"))
    if PYSIDE_AVAILABLE:
        from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]
        from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
            PromptRouterReasonerTab,
        )
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        widget = PromptRouterReasonerTab()
        assert widget.contract().wired_to_runtime_router is False
    else:
        assert TAB_SOURCE_PATH.exists()
    after = set(tmp_path.rglob("*"))
    assert after == before


if __name__ == "__main__":
    import tempfile

    test_prompt_router_reasoner_tab_is_registered_as_lazy_tool()
    test_prompt_router_reasoner_tab_source_declares_required_controls()
    test_prompt_router_reasoner_tab_source_has_no_runtime_router_wiring()
    test_prompt_router_reasoner_tab_qt_widget_if_pyside_available()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        test_prompt_router_reasoner_tab_skeleton_does_not_create_review_store(Path(temp_dir))
    print("VALIDATION OK: prompt router reasoner tab skeleton")
