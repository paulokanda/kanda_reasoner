# project-path: kanda_reasoner_app/templates/inner_tabs_template.py
"""Reusable compact inner-tab template for GUI subtab rows.

Use this module when a page needs local tabs inside a larger main tab. The
active inner tab is blue, inactive inner tabs are gray, and selecting a tab can
also switch a stacked page host to the matching index.

The template is intentionally passive. It does not create Qt imports, does not
modify any existing tab by itself, and does not bypass caller-owned validation
or confirmation behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

__all__ = [
    "INNER_TAB_ACTIVE_STYLE",
    "INNER_TAB_HEIGHT",
    "INNER_TAB_INACTIVE_STYLE",
    "INNER_TAB_STYLE_FRAGMENT",
    "InnerTabSpec",
    "apply_inner_tab_state",
    "build_inner_tab_row",
    "configure_inner_tab_button",
    "select_inner_tab",
    "wire_inner_tab_buttons",
]

INNER_TAB_HEIGHT = 24
INNER_TAB_STYLE_FRAGMENT = (
    "border-top-left-radius: 4px; border-top-right-radius: 4px; "
    "padding: 1px 8px; min-height: 20px; max-height: 24px;"
)
INNER_TAB_ACTIVE_STYLE = (
    "QPushButton {"
    "background-color: #1F4E79; color: #FFFFFF; font-weight: 600; "
    "border: 1px solid #163B5C; border-bottom: 1px solid #1F4E79; "
    + INNER_TAB_STYLE_FRAGMENT
    + "}"
)
INNER_TAB_INACTIVE_STYLE = (
    "QPushButton {"
    "background-color: #ECEFF3; color: #2F343A; font-weight: 500; "
    "border: 1px solid #C8CDD4; border-bottom: 1px solid #AEB4BC; "
    + INNER_TAB_STYLE_FRAGMENT
    + "}"
    "QPushButton:hover { background-color: #E1E5EA; }"
)


@dataclass(frozen=True)
class InnerTabSpec:
    """Describe one reusable inner tab button."""

    label: str
    object_name: str


def configure_inner_tab_button(button: Any) -> Any:
    """Apply the compact fixed-height shape to one inner tab button."""
    button.setMinimumHeight(INNER_TAB_HEIGHT)
    button.setMaximumHeight(INNER_TAB_HEIGHT)
    button.setCheckable(True)
    return button


def apply_inner_tab_state(button: Any, active: bool) -> None:
    """Apply blue active or gray inactive state to one inner tab button."""
    button.setChecked(active)
    button.setStyleSheet(
        INNER_TAB_ACTIVE_STYLE if active else INNER_TAB_INACTIVE_STYLE
    )


def select_inner_tab(
    buttons: Sequence[Any],
    active_index: int,
    *,
    stack: Any | None = None,
    on_selected: Callable[[int], None] | None = None,
) -> None:
    """Mark one inner tab active and optionally switch the matching stack page."""
    if active_index < 0 or active_index >= len(buttons):
        raise IndexError("active_index is outside the inner-tab button list")

    for index, button in enumerate(buttons):
        apply_inner_tab_state(button, index == active_index)

    if stack is not None:
        stack.setCurrentIndex(active_index)
    if on_selected is not None:
        on_selected(active_index)


def wire_inner_tab_buttons(
    buttons: Sequence[Any],
    *,
    stack: Any | None = None,
    on_selected: Callable[[int], None] | None = None,
    initial_index: int = 0,
) -> None:
    """Connect button clicks so the clicked inner tab becomes active."""
    for index, button in enumerate(buttons):
        button.clicked.connect(
            lambda checked=False, selected_index=index: select_inner_tab(
                buttons,
                selected_index,
                stack=stack,
                on_selected=on_selected,
            )
        )
    select_inner_tab(
        buttons,
        initial_index,
        stack=stack,
        on_selected=on_selected,
    )


def build_inner_tab_row(
    row_layout: Any,
    button_factory: Callable[[str], Any],
    specs: Sequence[InnerTabSpec],
    *,
    stack: Any | None = None,
    on_selected: Callable[[int], None] | None = None,
    initial_index: int = 0,
    add_stretch: bool = True,
) -> list[Any]:
    """Build a compact blue/gray inner-tab row from reusable tab specs."""
    buttons: list[Any] = []
    for spec in specs:
        button = button_factory(spec.label)
        button.setObjectName(spec.object_name)
        configure_inner_tab_button(button)
        row_layout.addWidget(button, 0)
        buttons.append(button)

    if add_stretch:
        row_layout.addStretch(1)

    wire_inner_tab_buttons(
        buttons,
        stack=stack,
        on_selected=on_selected,
        initial_index=initial_index,
    )
    return buttons
