"""
Root public launcher for the KANDA Reasoner tools GUI.

Implementation details live in kanda_reasoner_app.reasoner_tools_gui_shell.
The public names below are loaded lazily so importing this root module does not
load Qt until a GUI object is actually requested.
"""

from __future__ import annotations

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
    return sorted(list(globals()) + __all__)


def main() -> int:
    from kanda_reasoner_app.reasoner_tools_gui_shell.launch import main as launch_main

    return launch_main()




if __name__ == "__main__":
    raise SystemExit(main())
