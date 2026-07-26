# project-path: kanda_reasoner_app/manage_architecture/warning_resolver_cancel_gui.py
"""GUI projection helpers for Warning Resolver cancellation lifecycle."""

from __future__ import annotations

from typing import Any

__all__ = [
    "bind_warning_resolver_cancel_controller",
    "cancel_warning_resolver",
]


def cancel_warning_resolver(window: Any) -> None:
    """Request cancellation from the shared Warning Resolver controller."""
    controller = window._warning_resolver_controller()
    if not controller.running:
        window.statusBar().showMessage("No Warning Resolver is running")
        return
    if not controller.cancellable:
        window.statusBar().showMessage(
            "Confirmed Warning Resolver apply verification cannot be cancelled"
        )
        return
    if not controller.cancel():
        window.statusBar().showMessage("Warning Resolver cancellation is already pending")
        return
    output = getattr(window, "_output", None)
    if output is not None:
        output.appendPlainText("\n[cancel requested] Warning Resolver\n")
    window.statusBar().showMessage("Cancelling Warning Resolver...")


def bind_warning_resolver_cancel_controller(window: Any, controller: Any) -> None:
    """Bind one controller lifecycle to the dedicated cancel button."""
    controller.state_changed.connect(
        lambda running, cancel_requested, cancellable: _project_state(
            window, running, cancel_requested, cancellable
        )
    )
    controller.cancelled.connect(lambda: _project_cancelled(window))
    _project_state(
        window,
        controller.running,
        controller.cancel_requested,
        controller.cancellable,
    )


def _project_state(
    window: Any,
    running: bool,
    cancel_requested: bool,
    cancellable: bool,
) -> None:
    """Project controller state into the dedicated cancel button."""
    button = getattr(window, "_warning_resolver_cancel_btn", None)
    if button is None:
        return
    button.setText("Cancelling..." if cancel_requested else "Cancel Resolver")
    button.setEnabled(bool(running and cancellable and not cancel_requested))


def _project_cancelled(window: Any) -> None:
    """Report settled user cancellation without treating it as resolver failure."""
    output = getattr(window, "_output", None)
    if output is not None:
        output.appendPlainText("\nResolver cancelled by user.\n")
    window.statusBar().showMessage("Warning Resolver cancelled by user")
