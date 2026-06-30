# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/mode_options_hlp.py
"""Human-readable explanation for the missing-docstrings workflow modes."""

MODE_OPTIONS_HELP_TEXT = {
    "scan": "Finds files, classes, and functions that are missing docstrings.",
    "diff": "Previews the exact source diff for docstrings that would be inserted.",
    "write": "Writes safe missing-docstring insertions into source files after validation.",
}


def tool_limitations_summary() -> str:
    """Return the user-facing Tab 3 workflow safety summary."""
    return (
        "Tab 3 can scan for missing docstrings, preview the exact diff, or write "
        "validated missing-docstring insertions.\n"
        "Write mode parses the generated source and rejects any change that would "
        "alter the non-docstring AST."
    )
