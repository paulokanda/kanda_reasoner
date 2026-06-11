"""
PROJECT  : Architecture Manager Developer Tool
FILE     : mode_options_hlp.py
PREFIX   : architecture_gui_help_
OWNS     : Human-readable explanations for the GUI mode options.
EXPOSES  : MODE_OPTIONS_HELP_TEXT, mode_help_summary
DEPENDS  : none
USED BY  : manage_architecture_gui.py, developers using the tool
SEE ALSO : ARCHITECTURE.md > Navigation Quick-Reference
"""

__all__ = ["MODE_OPTIONS_HELP_TEXT", "mode_help_summary"]

MODE_OPTIONS_HELP_TEXT = {
    "validate": (
        "Checks the project tree for structural problems before writing anything. "
        "Use this first."
    ),
    "diff": (
        "Shows the exact file changes that would be generated without modifying the project."
    ),
    "scan": (
        "Prints the full architecture manifest JSON for inspection or debugging."
    ),
    "write": (
        "Writes architecture_manifest.json, ARCHITECTURE.md, and minimal package __init__.py facades. "
        "Use only after validate and diff look correct."
    ),
}


def mode_help_summary() -> str:
    return (
        "validate: check the project tree for architecture problems\n"
        "diff: preview generated file changes\n"
        "scan: print the manifest JSON\n"
        "write: update manifest, ARCHITECTURE.md, and minimal __init__.py files\n\n"
        "This GUI always uses the sibling worker script manage_architecture.py automatically."
    )
