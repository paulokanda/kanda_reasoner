"""Regression tests for Tab 3 runtime boundary imports."""

from __future__ import annotations

from importlib import import_module

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    layout_builder,
    report_review_panel,
)


class _Widget:
    def __init__(self) -> None:
        self.enabled: bool | None = None

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)


def test_layout_facade_public_control_delegate() -> None:
    """Verify the layout facade exposes public behavior only."""
    owner = type("Owner", (), {})()
    widgets = []
    for name in (
        "_base_url_edit",
        "_model_combo",
        "_refresh_models_button",
        "_config_path_edit",
        "_load_config_button",
        "_save_config_button",
        "_include_private_checkbox",
        "_min_confidence_combo",
        "_no_uncertain_checkbox",
    ):
        widget = _Widget()
        widgets.append(widget)
        setattr(owner, name, widget)

    layout_builder.set_ai_controls_enabled(owner, False)

    assert all(widget.enabled is False for widget in widgets)


def test_report_facade_basic_review_helpers_delegate() -> None:
    """Verify simple report helper calls still work through the facade."""
    row = {"generation_source": "fallback", "status": "fallback_review_required"}
    status = report_review_panel.review_status_for_row(row)
    assert isinstance(status, str)
    assert status


def test_runtime_modules_import_through_project_package() -> None:
    """Verify Tab 3 runtime modules import through project-owned packages."""
    layout_runtime = import_module("kanda_reasoner_app.tab3_manual_review_runtime.layout_runtime")
    report_runtime = import_module("kanda_reasoner_app.tab3_manual_review_runtime.report_panel_runtime")
    assert layout_runtime.__name__.endswith("layout_runtime")
    assert report_runtime.__name__.endswith("report_panel_runtime")


def test_runtime_modules_do_not_expose_stale_reasoner_tools_gui_marker() -> None:
    """Verify stale reasoner_tools_gui runtime ownership did not return."""
    layout_runtime = import_module("kanda_reasoner_app.tab3_manual_review_runtime.layout_runtime")
    report_runtime = import_module("kanda_reasoner_app.tab3_manual_review_runtime.report_panel_runtime")
    assert "reasoner_tools_gui" not in getattr(layout_runtime, "TAB3_LAYOUT_RUNTIME_RELOCATED", "")
    assert "reasoner_tools_gui" not in getattr(report_runtime, "TAB3_REPORT_PANEL_RUNTIME_RELOCATED", "")


def main() -> int:
    """Run the Tab 3 runtime-boundary regression tests without pytest."""
    test_layout_facade_public_control_delegate()
    test_report_facade_basic_review_helpers_delegate()
    test_runtime_modules_import_through_project_package()
    test_runtime_modules_do_not_expose_stale_reasoner_tools_gui_marker()
    print("Tab 3 runtime boundary repair tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
