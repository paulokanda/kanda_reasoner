# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/__init__.py
"""Implementation package for the root Reasoner tools GUI shell."""

from __future__ import annotations

__all__: list[str] = []

_EXPORTS = {
    "APP_DISPLAY_NAME": "app_constants",
    "APP_ICON_PATH": "app_constants",
    "APP_TITLE_DETAIL": "app_constants",
    "IgnoreRulesTab": "ignore_rules_tab",
    "LazyToolTab": "lazy_tabs",
    "ReasonerToolsWindow": "main_window",
    "TOOLS": "tool_specs",
    "ToolLoadErrorPanel": "error_panels",
    "ToolSpec": "tool_specs",
    "main": "launch",
}


def __getattr__(name: str):
    """Support getattr behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    """
    
    if name not in _EXPORTS:
        raise AttributeError(name)
    module_name = _EXPORTS[name]
    module = __import__(
        __name__ + "." + module_name,
        fromlist=[name],
    )
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Support dir behavior.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return sorted(list(globals()) + __all__)
