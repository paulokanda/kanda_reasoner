# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_state.py
"""Private persisted-state helpers for the Reasoner tools main window."""

from __future__ import annotations

import json
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    canonical_tool_support_root,
)

from ..app_constants import _PREFS_FILENAME, _PROJECT_ROOT

__all__: list[str] = []


class _WindowStateMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    @staticmethod
    def _legacy_prefs_path() -> Path:
        """Return the retired Tool-source preference path for migration only."""
        return _PROJECT_ROOT / _PREFS_FILENAME

    @staticmethod
    def _prefs_path() -> Path:
        """Return the Tool-owned preference path outside Tool source."""
        return canonical_tool_support_root(_PROJECT_ROOT) / _PREFS_FILENAME

    @classmethod
    def _migrate_legacy_prefs_if_needed(cls) -> None:
        """Copy legacy preferences to Tool Support without deleting history."""
        source = cls._legacy_prefs_path()
        target = cls._prefs_path()
        if target.exists() or not source.exists() or not source.is_file():
            return
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return
        if not isinstance(payload, dict):
            return
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        except OSError:
            return

    def _load_prefs(self) -> dict:
        """Load Tool-owned shell preferences after safe legacy migration."""
        self._migrate_legacy_prefs_if_needed()
        path = self._prefs_path()
        try:
            if path.exists():
                payload = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(payload, dict):
                    return payload
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass
        return {}

    def _save_prefs(self) -> None:
        """Persist lightweight shell state outside the Tool source tree."""
        path = self._prefs_path()
        boundary = getattr(self, "current_project_boundary", None)
        payload = {
            "last_project_root": (
                str(self.current_project_root)
                if self.current_project_root is not None
                else ""
            ),
            "project_selection_mode": (
                boundary.selection_mode.value if boundary is not None else ""
            ),
            "stable_project_id": (
                boundary.active_project_id if boundary is not None else ""
            ),
            "project_root_fingerprint": (
                boundary.active_project_root_fingerprint
                if boundary is not None
                else ""
            ),
        }
        tab_order = getattr(self, "_prefs", {}).get("tab_order", [])
        if isinstance(tab_order, list):
            payload["tab_order"] = [
                str(tab_id)
                for tab_id in tab_order
                if str(tab_id).strip()
            ]
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                existing = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(existing, dict):
                    existing.update(payload)
                    payload = existing
            temporary = path.with_name(path.name + ".tmp")
            temporary.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            temporary.replace(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass

    @staticmethod
    def _accept_close_event_safely(event) -> None:
        """Accept a Qt close event without letting cleanup block exit."""
        try:
            event.accept()
        except Exception:
            pass

    def closeEvent(self, event) -> None:
        """Persist lightweight state while keeping shutdown non-blocking."""
        try:
            self._save_prefs()
        except KeyboardInterrupt:
            self._accept_close_event_safely(event)
            return
        except Exception:
            pass

        try:
            super().closeEvent(event)
        except KeyboardInterrupt:
            self._accept_close_event_safely(event)
        except Exception:
            self._accept_close_event_safely(event)
