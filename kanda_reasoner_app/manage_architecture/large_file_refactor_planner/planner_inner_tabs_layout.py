# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_inner_tabs_layout.py
"""Planner-local child-tab composition for the Large File Refactor Planner GUI.

This module owns layout composition only. It does not create Planner state,
change workflow gates, call analysis logic, or reach into other Architecture
Review boxes. The reusable inner-tab template is consumed only through its
public contract.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.templates.inner_tabs_template import (
    InnerTabSpec,
    build_inner_tab_row,
)

__all__ = ["PlannerInnerTabs", "build_planner_inner_tabs"]


@dataclass(frozen=True)
class PlannerInnerTabs:
    """Return the Planner-local inner-tab host and its public GUI handles."""

    root: QWidget
    stack: QStackedWidget
    buttons: tuple[Any, ...]
    send_web_ai_split_button: Any | None


def build_planner_inner_tabs(
    input_analysis_sections: Sequence[Any],
    plan_action_sections: Sequence[Any],
    *,
    send_web_ai_split_callback: Callable[[], None] | None = None,
) -> PlannerInnerTabs:
    """Build two child tabs from the Planner's existing section widgets."""
    root = QWidget()
    root.setMinimumWidth(0)
    root.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)

    root_layout = QVBoxLayout(root)
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.setSpacing(0)

    stack = QStackedWidget()
    stack.setMinimumWidth(0)
    stack.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)

    input_page = _build_page(input_analysis_sections, first_stretch=2)
    plan_page = _build_page(plan_action_sections, first_stretch=2)
    stack.addWidget(input_page)
    stack.addWidget(plan_page)

    tab_row = QHBoxLayout()
    tab_row.setContentsMargins(0, 0, 0, 0)
    tab_row.setSpacing(2)
    buttons = build_inner_tab_row(
        tab_row,
        QPushButton,
        (
            InnerTabSpec("Input & Analysis", "largeFilePlannerInputAnalysisTab"),
            InnerTabSpec("Plan & Actions", "largeFilePlannerPlanActionsTab"),
        ),
        stack=stack,
        initial_index=0,
        add_stretch=False,
    )
    send_button = _build_send_web_ai_split_button(send_web_ai_split_callback)
    if send_button is not None:
        tab_row.addWidget(send_button, 0)
    tab_row.addStretch(1)

    root_layout.addLayout(tab_row)
    root_layout.addWidget(stack, 1)
    return PlannerInnerTabs(
        root=root,
        stack=stack,
        buttons=tuple(buttons),
        send_web_ai_split_button=send_button,
    )


def _build_send_web_ai_split_button(
    callback: Callable[[], None] | None,
) -> QPushButton | None:
    """Build the orange-text Web AI split wrapper action beside Plan & Actions."""
    if callback is None:
        return None
    button = QPushButton("Send Web Ai to split file")
    button.setObjectName("largeFilePlannerSendWebAiSplitFileButton")
    button.setStyleSheet("color: #FF8C00; font-weight: bold;")
    button.setToolTip(
        "Copy the canonical Web AI bundle blueprint plus current planning package."
    )
    button.clicked.connect(callback)
    return button


def _build_page(sections: Sequence[Any], *, first_stretch: int) -> QWidget:
    """Place existing Planner sections on one shrinkable local page."""
    page = QWidget()
    page.setMinimumWidth(0)
    page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)

    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 6, 0, 0)
    layout.setSpacing(8)

    for index, section in enumerate(sections):
        stretch = first_stretch if index == 0 else 1
        layout.addWidget(section, stretch)

    return page
