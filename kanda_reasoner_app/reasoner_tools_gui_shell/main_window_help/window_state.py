"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""

from __future__ import annotations

from pathlib import Path
import json

from ..app_constants import _PREFS_FILENAME, _PROJECT_ROOT

__all__: list[str] = []


class _WindowStateMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    @staticmethod
    def _prefs_path() -> Path:
        try:
            return _PROJECT_ROOT / _PREFS_FILENAME
        except Exception:
            return _PROJECT_ROOT / _PREFS_FILENAME

    def _load_prefs(self) -> dict:
        path = self._prefs_path()
        try:
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {}

    def _save_prefs(self) -> None:
        path = self._prefs_path()
        payload = {
            "last_project_root": str(self.current_project_root) if self.current_project_root else "",
        }
        # Note: project_ignore_rules are saved directly by IgnoreRulesTab; we do not overwrite them here.
        try:
            # merge with existing prefs to preserve ignore_rules
            if path.exists():
                existing = json.loads(path.read_text(encoding="utf-8"))
                existing.update(payload)
                payload = existing
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    @staticmethod
    def _accept_close_event_safely(event) -> None:
        """Accept a Qt close event without letting shutdown cleanup block exit."""
        try:
            event.accept()
        except Exception:
            pass

    def closeEvent(self, event) -> None:
        """Persist lightweight window state while keeping shutdown non-blocking.

        PyCharm/Qt can surface a noisy KeyboardInterrupt traceback if the
        process is interrupted while Python is inside this close hook.  Closing
        the main window should never be blocked by preference-write failures or
        late shutdown interruptions, so this handler saves preferences on a
        best-effort basis and then accepts the close event if anything goes
        wrong during shutdown.
        """
        try:
            self._save_prefs()
        except KeyboardInterrupt:
            self._accept_close_event_safely(event)
            return
        except Exception:
            # Preference persistence is best-effort only; never block closing.
            pass

        try:
            super().closeEvent(event)
        except KeyboardInterrupt:
            self._accept_close_event_safely(event)
        except Exception:
            self._accept_close_event_safely(event)
