# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab_help/browse_state.py
"""Persist browse-dialog state for the ignore-rules tab."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesBrowseStateMixin",
]


class IgnoreRulesBrowseStateMixin:
    """Provide last-browse-path persistence for ignore-rules dialogs."""

    def _get_last_browse_path(self) -> str:
        """Return the last used browse directory from prefs, or empty string."""
        data = self._read_prefs()
        return str(data.get("last_browse_path", "") or "")

    def _set_last_browse_path(self, path: str) -> None:
        """Store the last used browse directory in prefs."""
        try:
            data = self._read_prefs()
            data["last_browse_path"] = path
            self._write_prefs(data)
        except Exception:
            pass
