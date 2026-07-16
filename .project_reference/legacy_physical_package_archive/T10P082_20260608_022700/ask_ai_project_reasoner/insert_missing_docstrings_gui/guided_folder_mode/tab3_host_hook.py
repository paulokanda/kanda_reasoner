
"""Safe Mode host hook for the Tab 3 docstring GUI.

This module is intentionally defensive. It can be called by the real Tab 3
window, but it does not require the window to expose any specific widget type.
When no compatible layout is available, it returns a safe no-op result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .gui_bridge import SafeModeButtonState, SafeModeGuiSnapshot
from .gui_mount import (
    SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE,
    SAFE_MODE_PANEL_ATTR,
    SafeModeMountResult,
    mount_safe_mode_panel,
    refresh_safe_mode_panel,
)
from .gui_panel import SafeModePanelCallbacks


SAFE_MODE_HOST_HOOK_STATUS_INSTALLED = "installed"
SAFE_MODE_HOST_HOOK_STATUS_ALREADY_INSTALLED = "already_installed"
SAFE_MODE_HOST_HOOK_STATUS_REFRESHED = "refreshed"
SAFE_MODE_HOST_HOOK_STATUS_UNINSTALLED = "uninstalled"
SAFE_MODE_HOST_HOOK_STATUS_NOT_AVAILABLE = "not_available"
SAFE_MODE_HOST_HOOK_STATUS_FAILED = "failed"

SAFE_MODE_HOST_HOOK_ATTR = "_safe_mode_tab3_host_hook"
SAFE_MODE_HOST_SNAPSHOT_PROVIDER_ATTR = "_safe_mode_snapshot_provider"
SAFE_MODE_HOST_BUTTON_PROVIDER_ATTR = "_safe_mode_button_provider"
SAFE_MODE_HOST_CALLBACKS_ATTR = "_safe_mode_panel_callbacks"


SnapshotProvider = Callable[[], SafeModeGuiSnapshot]
ButtonStateProvider = Callable[[], SafeModeButtonState]


@dataclass(frozen=True)
class SafeModeTab3HostHookResult:
    """Represent the result of a Safe Mode Tab 3 host-hook operation."""

    success: bool
    status: str
    message: str = ""
    mount_result: SafeModeMountResult | None = None
    error: str = ""


def install_safe_mode_tab3_host_hook(
    host: object,
    callbacks: SafeModePanelCallbacks | None = None,
    snapshot_provider: SnapshotProvider | None = None,
    button_state_provider: ButtonStateProvider | None = None,
    panel_factory: object | None = None,
) -> SafeModeTab3HostHookResult:
    """Install Safe Mode panel support on a Tab 3 host if possible."""
    if getattr(host, SAFE_MODE_HOST_HOOK_ATTR, False):
        return SafeModeTab3HostHookResult(
            success=True,
            status=SAFE_MODE_HOST_HOOK_STATUS_ALREADY_INSTALLED,
            message="Safe Mode Tab 3 host hook is already installed.",
        )

    try:
        if callbacks is not None:
            setattr(host, SAFE_MODE_HOST_CALLBACKS_ATTR, callbacks)
        if snapshot_provider is not None:
            setattr(host, SAFE_MODE_HOST_SNAPSHOT_PROVIDER_ATTR, snapshot_provider)
        if button_state_provider is not None:
            setattr(host, SAFE_MODE_HOST_BUTTON_PROVIDER_ATTR, button_state_provider)

        mount_result = mount_safe_mode_panel(
            host=host,
            callbacks=callbacks,
            panel_factory=panel_factory,
        )
        if not mount_result.success:
            status = SAFE_MODE_HOST_HOOK_STATUS_NOT_AVAILABLE
            if mount_result.status != SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE:
                status = SAFE_MODE_HOST_HOOK_STATUS_FAILED
            return SafeModeTab3HostHookResult(
                success=False,
                status=status,
                message=mount_result.message,
                mount_result=mount_result,
                error=mount_result.error,
            )

        setattr(host, SAFE_MODE_HOST_HOOK_ATTR, True)

        if snapshot_provider is not None and button_state_provider is not None:
            refresh_result = refresh_safe_mode_tab3_host_hook(host)
            if not refresh_result.success:
                return refresh_result

        return SafeModeTab3HostHookResult(
            success=True,
            status=SAFE_MODE_HOST_HOOK_STATUS_INSTALLED,
            message="Safe Mode Tab 3 host hook installed.",
            mount_result=mount_result,
        )

    except Exception as exc:
        return SafeModeTab3HostHookResult(
            success=False,
            status=SAFE_MODE_HOST_HOOK_STATUS_FAILED,
            error=str(exc),
        )


def refresh_safe_mode_tab3_host_hook(host: object) -> SafeModeTab3HostHookResult:
    """Refresh the Safe Mode panel on a Tab 3 host using stored providers."""
    snapshot_provider = getattr(host, SAFE_MODE_HOST_SNAPSHOT_PROVIDER_ATTR, None)
    button_state_provider = getattr(host, SAFE_MODE_HOST_BUTTON_PROVIDER_ATTR, None)

    if not callable(snapshot_provider) or not callable(button_state_provider):
        return SafeModeTab3HostHookResult(
            success=False,
            status=SAFE_MODE_HOST_HOOK_STATUS_NOT_AVAILABLE,
            message="Safe Mode refresh providers are not installed.",
        )

    try:
        snapshot = snapshot_provider()
        buttons = button_state_provider()
        mount_result = refresh_safe_mode_panel(host, snapshot, buttons)
    except Exception as exc:
        return SafeModeTab3HostHookResult(
            success=False,
            status=SAFE_MODE_HOST_HOOK_STATUS_FAILED,
            error=str(exc),
        )

    if not mount_result.success:
        return SafeModeTab3HostHookResult(
            success=False,
            status=SAFE_MODE_HOST_HOOK_STATUS_NOT_AVAILABLE,
            message=mount_result.message,
            mount_result=mount_result,
            error=mount_result.error,
        )

    return SafeModeTab3HostHookResult(
        success=True,
        status=SAFE_MODE_HOST_HOOK_STATUS_REFRESHED,
        message="Safe Mode Tab 3 host hook refreshed.",
        mount_result=mount_result,
    )


def uninstall_safe_mode_tab3_host_hook(host: object) -> SafeModeTab3HostHookResult:
    """Remove Safe Mode host-hook attributes without destroying GUI widgets."""
    removed_any = False
    for attr_name in (
        SAFE_MODE_HOST_HOOK_ATTR,
        SAFE_MODE_HOST_SNAPSHOT_PROVIDER_ATTR,
        SAFE_MODE_HOST_BUTTON_PROVIDER_ATTR,
        SAFE_MODE_HOST_CALLBACKS_ATTR,
        SAFE_MODE_PANEL_ATTR,
    ):
        if hasattr(host, attr_name):
            try:
                delattr(host, attr_name)
                removed_any = True
            except Exception as exc:
                return SafeModeTab3HostHookResult(
                    success=False,
                    status=SAFE_MODE_HOST_HOOK_STATUS_FAILED,
                    error=str(exc),
                )

    return SafeModeTab3HostHookResult(
        success=True,
        status=SAFE_MODE_HOST_HOOK_STATUS_UNINSTALLED,
        message="Safe Mode host hook removed." if removed_any else "Safe Mode host hook was not installed.",
    )


def tab3_host_hook_is_installed(host: object) -> bool:
    """Return True when the Safe Mode Tab 3 host hook is installed."""
    return bool(getattr(host, SAFE_MODE_HOST_HOOK_ATTR, False))
