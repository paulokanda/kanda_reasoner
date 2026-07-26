"""Validate New Local Freeze Entry action-button gating.

This validation is intentionally static and import-free so it can run on a
clean development machine without requiring PySide6 to be installed. It checks
that the GUI source disables and greys both governed freeze action buttons until
there is a clean writable preview.
"""

from __future__ import annotations

from pathlib import Path
import py_compile


FEATURE_ID = "freeze-local-entry-action-buttons-v1"
SOURCE_PATH = Path(
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py"
)


REQUIRED_SNIPPETS = [
    "FREEZE_DISABLED_ACTION_STYLE = \"color: #808080; font-weight: bold;\"",
    "confirm_write_button.setStyleSheet(FREEZE_DISABLED_ACTION_STYLE)",
    "ignore_freeze_button.setStyleSheet(FREEZE_DISABLED_ACTION_STYLE)",
    "ignore_freeze_button.setEnabled(False)",
    "def set_freeze_action_buttons_state(can_confirm: bool, can_ignore: bool, reason: str = \"\") -> None:",
    "def disable_freeze_action_buttons(reason: str = \"\") -> None:",
    "disable_freeze_action_buttons(\"No writable freeze preview has been generated yet.\")",
    "set_freeze_action_buttons_state(True, True)",
    "disable_freeze_action_buttons(reason)",
    "No writable freeze entry is available. Fix missing fields or validation evidence first.",
    "Freeze preview validation blocked writing. Fix the errors before confirming or ignoring this freeze.",
    "Freeze draft was ignored by the human.",
]


FORBIDDEN_SNIPPETS = [
    "ignore_freeze_button.setStyleSheet(\"color: #B00020; font-weight: bold;\")",
]


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a readable validation failure."""
    if not condition:
        raise AssertionError(message)


def main() -> int:
    """Run static contract checks for the GUI button-state patch."""
    require(SOURCE_PATH.is_file(), "Missing source file: " + str(SOURCE_PATH))
    text = SOURCE_PATH.read_text(encoding="utf-8", errors="replace")

    py_compile.compile(str(SOURCE_PATH), doraise=True)

    for snippet in REQUIRED_SNIPPETS:
        require(snippet in text, "Missing required snippet: " + snippet)

    for snippet in FORBIDDEN_SNIPPETS:
        require(snippet not in text, "Forbidden stale snippet remains: " + snippet)

    helper_index = text.find("def set_freeze_action_buttons_state")
    preview_index = text.find("def preview_local_freeze")
    confirm_ok_index = text.find("set_freeze_action_buttons_state(True, True)")
    require(helper_index >= 0, "Button-state helper not found.")
    require(preview_index > helper_index, "Preview function should use the earlier button-state helper.")
    require(confirm_ok_index > preview_index, "Confirm/ignore enablement should occur only inside preview validation flow.")

    writable_phrase = "if result.get(\"ok\") and result.get(\"is_writable\")"
    validation_phrase = "if validation_result.get(\"ok\")"
    require(writable_phrase in text, "Writable preview guard is missing.")
    require(validation_phrase in text, "Preview validation guard is missing.")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
