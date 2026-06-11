"""Human-readable explanation for the scan-only missing-docstrings workflow."""

MODE_OPTIONS_HELP_TEXT = {
    "scan": "Finds files, classes, and functions that are missing docstrings.",
}


def tool_limitations_summary() -> str:
    """Return the user-facing Tab 3 workflow safety summary."""
    return (
        "Tab 3 scan only finds missing docstrings and creates review material.\n"
        "Draft generation, review approval, dry-run preview, and source apply are "
        "separate steps.\n"
        "Source files should only be modified by the final Apply Approved "
        "Docstrings to Source Files action."
    )
