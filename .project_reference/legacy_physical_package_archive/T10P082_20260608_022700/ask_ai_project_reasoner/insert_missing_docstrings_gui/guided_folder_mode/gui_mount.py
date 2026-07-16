
"""Safe Mode GUI mounting helpers.

This module mounts the Safe Mode visual panel into an existing GUI host only
when a compatible layout is available. It is intentionally defensive so that a
working Tab 3 window is not broken by missing optional Safe Mode widgets.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .gui_bridge import SafeModeButtonState, SafeModeGuiSnapshot
from .gui_panel import (
    SafeModePanelCallbacks,
    apply_safe_mode_panel_model,
    build_safe_mode_panel_model,
    create_safe_mode_panel_widget,
)


SAFE_MODE_PANEL_ATTR = "_safe_mode_panel_widget"
SAFE_MODE_MOUNT_STATUS_MOUNTED = "mounted"
SAFE_MODE_MOUNT_STATUS_ALREADY_MOUNTED = "already_mounted"
SAFE_MODE_MOUNT_STATUS_REFRESHED = "refreshed"
SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE = "not_available"
SAFE_MODE_MOUNT_STATUS_FAILED = "failed"

DEFAULT_LAYOUT_ATTRS = (
    "safe_mode_layout",
    "docstring_safe_mode_layout",
    "guided_folder_mode_layout",
    "docstring_tools_layout",
    "main_layout",
    "vertical_layout",
    "verticalLayout",
    "central_layout",
)


@dataclass(frozen=True)
class SafeModeMountResult:
    """Represent the result of a Safe Mode GUI mount or refresh action."""

    success: bool
    status: str
    message: str = ""
    panel: object | None = None
    layout_attr: str = ""
    error: str = ""


PanelFactory = Callable[[object | None, SafeModePanelCallbacks | None], object]


def mount_safe_mode_panel(
    host: object,
    callbacks: SafeModePanelCallbacks | None = None,
    panel_factory: PanelFactory | None = None,
    layout_attr_names: tuple[str, ...] = DEFAULT_LAYOUT_ATTRS,
) -> SafeModeMountResult:
    """Mount the Safe Mode panel into a host object if a layout is available."""
    existing = getattr(host, SAFE_MODE_PANEL_ATTR, None)
    if existing is not None:
        return SafeModeMountResult(
            success=True,
            status=SAFE_MODE_MOUNT_STATUS_ALREADY_MOUNTED,
            message="Safe Mode panel is already mounted.",
            panel=existing,
        )

    layout, layout_attr = _find_mount_layout(host, layout_attr_names)
    if layout is None:
        return SafeModeMountResult(
            success=False,
            status=SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE,
            message="No compatible layout was found for Safe Mode panel mounting.",
        )

    factory = panel_factory or create_safe_mode_panel_widget

    try:
        panel = factory(host, callbacks)
        layout.addWidget(panel)
        setattr(host, SAFE_MODE_PANEL_ATTR, panel)
    except Exception as exc:
        return SafeModeMountResult(
            success=False,
            status=SAFE_MODE_MOUNT_STATUS_FAILED,
            error=str(exc),
        )

    return SafeModeMountResult(
        success=True,
        status=SAFE_MODE_MOUNT_STATUS_MOUNTED,
        message="Safe Mode panel mounted.",
        panel=panel,
        layout_attr=layout_attr,
    )


def refresh_safe_mode_panel(
    host: object,
    snapshot: SafeModeGuiSnapshot,
    buttons: SafeModeButtonState,
) -> SafeModeMountResult:
    """Refresh an already-mounted Safe Mode panel."""
    panel = getattr(host, SAFE_MODE_PANEL_ATTR, None)
    if panel is None:
        return SafeModeMountResult(
            success=False,
            status=SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE,
            message="Safe Mode panel is not mounted.",
        )

    try:
        model = build_safe_mode_panel_model(snapshot, buttons)
        apply_safe_mode_panel_model(panel, model)
    except Exception as exc:
        return SafeModeMountResult(
            success=False,
            status=SAFE_MODE_MOUNT_STATUS_FAILED,
            panel=panel,
            error=str(exc),
        )

    return SafeModeMountResult(
        success=True,
        status=SAFE_MODE_MOUNT_STATUS_REFRESHED,
        message="Safe Mode panel refreshed.",
        panel=panel,
    )


def safe_mode_panel_is_mounted(host: object) -> bool:
    """Return True when a host already has a mounted Safe Mode panel."""
    return getattr(host, SAFE_MODE_PANEL_ATTR, None) is not None


def _find_mount_layout(
    host: object,
    layout_attr_names: tuple[str, ...],
) -> tuple[object | None, str]:
    for attr_name in layout_attr_names:
        layout = getattr(host, attr_name, None)
        if _is_mountable_layout(layout):
            return layout, attr_name

    layout_method = getattr(host, "layout", None)
    if callable(layout_method):
        try:
            layout = layout_method()
        except Exception:
            layout = None
        if _is_mountable_layout(layout):
            return layout, "layout()"

    return None, ""


def _is_mountable_layout(value: object) -> bool:
    return value is not None and callable(getattr(value, "addWidget", None))
