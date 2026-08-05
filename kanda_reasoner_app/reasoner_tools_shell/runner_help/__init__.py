# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/__init__.py
"""Private helper modules for reasoner_tools_shell.runner."""

from __future__ import annotations

__all__ = []


def _install_tool_project_button_wrapper() -> None:
    """Wrap the existing Show Project UI builder without replacing its source."""
    try:
        from . import project_tool_boundary_prompt_button_private_impl as _button
        from . import window_methods_private_impl as _window_methods
    except Exception:
        return

    original = getattr(_window_methods, "_build_ui", None)
    if original is None:
        return
    if getattr(original, "_kanda_tool_project_button_wrapped", False):
        return

    def _build_ui_with_tool_project_button(window):
        result = original(window)
        _button.install_control(window)
        return result

    setattr(
        _build_ui_with_tool_project_button,
        "_kanda_tool_project_button_wrapped",
        True,
    )
    setattr(
        _build_ui_with_tool_project_button,
        "_kanda_tool_project_button_original",
        original,
    )
    _window_methods._build_ui = _build_ui_with_tool_project_button


_install_tool_project_button_wrapper()
