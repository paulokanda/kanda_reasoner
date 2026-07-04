# project-path: reasoner_tools_gui.py
"""
Root public launcher for the KANDA Reasoner tools GUI.

Implementation details live in kanda_reasoner_app.reasoner_tools_gui_shell.
The public names below are loaded lazily so importing this root module does not
load Qt until a GUI object is actually requested.
"""


from __future__ import annotations

import warnings


def _configure_known_warning_filters() -> None:
    """Suppress a known GUI-startup invalid-escape warning.

    Python 3.12 can report invalid escape sequences from dynamically parsed
    source snippets as ``<unknown>`` warnings during GUI startup. The launcher
    filters only the observed noisy left-bracket escape SyntaxWarning so unrelated warnings
    remain visible.
    """

    warnings.filterwarnings(
        "ignore",
        message=r"invalid escape sequence '\\\['",
        category=SyntaxWarning,
    )


_configure_known_warning_filters()

__all__ = [
    "main",
]

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
        "kanda_reasoner_app.reasoner_tools_gui_shell." + module_name,
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


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    from kanda_reasoner_app.reasoner_tools_gui_shell.launch import main as launch_main

    return launch_main()




if __name__ == "__main__":
    raise SystemExit(main())
