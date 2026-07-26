# project-path: kanda_reasoner_app/manage_architecture/warning_resolver_split_control.py
"""Split control for deterministic and model-assisted warning resolver routes."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import Any

__all__ = [
    "WarningResolverSplitWidgets",
    "build_warning_resolver_split_control",
]


@dataclass(frozen=True, slots=True)
class WarningResolverSplitWidgets:
    """Widget bundle returned to the Architecture Review layout."""

    container: Any
    main_button: Any
    dropdown_button: Any
    cancel_button: Any


def _qt_widgets_module() -> Any:
    """Load Qt widgets only when the Architecture Review GUI is built."""
    return import_module("PySide6.QtWidgets")


def build_warning_resolver_split_control(
    parent: Any,
    *,
    heuristic_callback: Callable[[], None],
    model_callback: Callable[[], None],
    cancel_callback: Callable[[], None],
    web_callback: Callable[[], None] | None = None,
) -> WarningResolverSplitWidgets:
    """Build one main route button plus a three-option resolver menu."""
    qt = _qt_widgets_module()
    container = qt.QWidget(parent)
    layout = qt.QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    state = {"route": "heuristic"}

    main_button = qt.QPushButton("Warning Heuristic Resolver", container)
    main_button.setObjectName(
        "architecture_review_warning_heuristic_resolver_button"
    )
    main_button.setToolTip(
        "Run the selected warning resolver route. Use the arrow to choose Heuristic, Local AI, or Web AI."
    )

    dropdown_button = qt.QToolButton(container)
    dropdown_button.setObjectName(
        "architecture_review_warning_resolver_dropdown_button"
    )
    dropdown_button.setText(chr(0x25BE))
    dropdown_button.setFixedWidth(24)
    dropdown_button.setToolTip(
        "Choose Warning Heuristic Resolver, Warning Local AI Resolver, or Web AI Resolver."
    )
    dropdown_button.setPopupMode(qt.QToolButton.InstantPopup)

    menu = qt.QMenu(dropdown_button)
    heuristic_action = menu.addAction("Warning Heuristic Resolver")
    model_action = menu.addAction("Warning Local AI Resolver")
    web_action = None
    if web_callback is not None:
        web_action = menu.addAction("Web AI resolver")
    dropdown_button.setMenu(menu)

    cancel_button = qt.QPushButton("Cancel Resolver", container)
    cancel_button.setObjectName(
        "architecture_review_warning_resolver_cancel_button"
    )
    cancel_button.setToolTip(
        "Cancel the active Warning Resolver analysis route."
    )
    cancel_button.setStyleSheet(
        "QPushButton { color: #C2185B; font-weight: bold; } "
        "QPushButton:disabled { color: #9A9A9A; }"
    )
    cancel_button.setEnabled(False)
    cancel_button.clicked.connect(cancel_callback)

    def run_selected() -> None:
        if state["route"] == "model":
            model_callback()
            return
        if state["route"] == "web" and web_callback is not None:
            web_callback()
            return
        heuristic_callback()

    def select_heuristic_and_run() -> None:
        state["route"] = "heuristic"
        main_button.setText("Warning Heuristic Resolver")
        heuristic_callback()

    def select_model_and_run() -> None:
        state["route"] = "model"
        main_button.setText("Warning Local AI Resolver")
        model_callback()

    def select_web_and_run() -> None:
        state["route"] = "web"
        main_button.setText("Web AI resolver")
        if web_callback is not None:
            web_callback()

    main_button.clicked.connect(run_selected)
    heuristic_action.triggered.connect(select_heuristic_and_run)
    model_action.triggered.connect(select_model_and_run)
    if web_action is not None:
        web_action.triggered.connect(select_web_and_run)

    layout.addWidget(main_button)
    layout.addWidget(dropdown_button)
    layout.addWidget(cancel_button)

    return WarningResolverSplitWidgets(
        container=container,
        main_button=main_button,
        dropdown_button=dropdown_button,
        cancel_button=cancel_button,
    )
