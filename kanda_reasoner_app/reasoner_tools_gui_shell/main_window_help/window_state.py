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
        shell_width = 0
        shell_height = 0
        try:
            normal_geometry = self.normalGeometry()
            shell_width = int(normal_geometry.width())
            shell_height = int(normal_geometry.height())
        except Exception:
            try:
                shell_width = int(self.width())
                shell_height = int(self.height())
            except Exception:
                pass

        payload = {
            "shell_width": shell_width,
            "shell_height": shell_height,
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

    def _configuration_shutdown_controllers(self) -> tuple[object, ...]:
        """Return application-scoped configuration owners with Qt workers."""
        controllers = (
            getattr(self, "_local_ai_configuration", None),
            getattr(self, "_web_ai_configuration", None),
        )
        return tuple(controller for controller in controllers if controller is not None)

    def _configuration_shutdown_ready(self) -> bool:
        """Return whether every application configuration worker has settled."""
        for controller in self._configuration_shutdown_controllers():
            ready = getattr(controller, "shutdown_ready", None)
            if callable(ready) and not bool(ready()):
                return False
        return True

    def _connect_configuration_shutdown_retry(self, controller: object) -> None:
        """Connect one settlement signal to the deferred close retry once."""
        connected = getattr(
            self,
            "_configuration_shutdown_signal_owners",
            None,
        )
        if not isinstance(connected, set):
            connected = set()
            self._configuration_shutdown_signal_owners = connected

        identity = id(controller)
        if identity in connected:
            return

        signal = getattr(controller, "catalog_refresh_settled", None)
        if signal is None:
            return
        try:
            signal.connect(self._retry_close_after_configuration_shutdown)
        except Exception:
            return
        connected.add(identity)

    def _begin_configuration_shutdown(self) -> bool:
        """Request cooperative settlement and report whether close may proceed."""
        ready_now = True
        for controller in self._configuration_shutdown_controllers():
            self._connect_configuration_shutdown_retry(controller)
            begin = getattr(controller, "begin_shutdown", None)
            if callable(begin) and not bool(begin()):
                ready_now = False
        return ready_now and self._configuration_shutdown_ready()

    def _retry_close_after_configuration_shutdown(self) -> None:
        """Retry an ignored close only after every configuration QThread settles."""
        if not bool(
            getattr(
                self,
                "_close_waiting_for_configuration_shutdown",
                False,
            )
        ):
            return
        if not self._configuration_shutdown_ready():
            return
        self._close_waiting_for_configuration_shutdown = False
        try:
            from PySide6.QtCore import QTimer

            QTimer.singleShot(0, self.close)
        except Exception:
            self.close()

    def _loaded_tool_shutdown_targets(self) -> tuple[object, ...]:
        """Return loaded embedded tools exactly once for shell teardown."""
        registry = getattr(self, "_loaded_tools_by_tab_id", {})
        values = registry.values() if isinstance(registry, dict) else ()
        targets: list[object] = []
        seen: set[int] = set()
        for widget in values:
            identity = id(widget)
            if identity in seen:
                continue
            seen.add(identity)
            targets.append(widget)
        return tuple(targets)

    def _embedded_tool_shutdown_ready(self, widget: object) -> bool:
        """Run an optional worker protocol before child closeEvent."""
        begin = getattr(widget, "begin_shutdown", None)
        if callable(begin):
            try:
                if not bool(begin()):
                    return False
            except RuntimeError:
                return True
            except Exception:
                return False

        ready = getattr(widget, "shutdown_ready", None)
        if callable(ready):
            try:
                return bool(ready())
            except RuntimeError:
                return True
            except Exception:
                return False
        return True

    def _close_loaded_tools_for_shell_shutdown(self) -> bool:
        """Settle embedded workers, then deliver child closeEvent cleanup."""
        completed = getattr(
            self,
            "_embedded_tool_shutdown_completed",
            None,
        )
        if not isinstance(completed, set):
            completed = set()
            self._embedded_tool_shutdown_completed = completed

        ready = True
        for widget in self._loaded_tool_shutdown_targets():
            identity = id(widget)
            if identity in completed:
                continue
            if not self._embedded_tool_shutdown_ready(widget):
                ready = False
                continue
            close = getattr(widget, "close", None)
            if not callable(close):
                completed.add(identity)
                continue
            try:
                accepted = close()
            except RuntimeError:
                completed.add(identity)
                continue
            except Exception:
                ready = False
                continue
            if accepted is False:
                ready = False
                continue
            completed.add(identity)
        return ready

    def _schedule_embedded_tool_shutdown_retry(self) -> None:
        """Retry shell close without blocking while a child rejects close."""
        if bool(
            getattr(
                self,
                "_embedded_tool_shutdown_retry_scheduled",
                False,
            )
        ):
            return
        self._embedded_tool_shutdown_retry_scheduled = True

        def retry() -> None:
            self._embedded_tool_shutdown_retry_scheduled = False
            self.close()

        try:
            from PySide6.QtCore import QTimer

            QTimer.singleShot(25, retry)
        except Exception:
            retry()

    def _begin_visual_shutdown(self) -> None:
        """Dismiss the main GUI immediately while safe teardown continues."""
        if bool(getattr(self, "_visual_shutdown_started", False)):
            return
        self._visual_shutdown_started = True
        try:
            self.hide()
        except Exception:
            pass

    def _quit_application_after_safe_close(self) -> None:
        """End the desktop event loop only after all workers have settled."""
        try:
            from PySide6.QtWidgets import QApplication

            app = QApplication.instance()
            if app is not None:
                app.quit()
        except Exception:
            pass

    def closeEvent(self, event) -> None:
        """Dismiss immediately, then settle workers before final destruction."""
        self._begin_visual_shutdown()
        try:
            self._save_prefs()
        except KeyboardInterrupt:
            self._accept_close_event_safely(event)
            return
        except Exception:
            pass

        if not self._configuration_shutdown_ready():
            self._close_waiting_for_configuration_shutdown = True
            if not self._begin_configuration_shutdown():
                try:
                    event.ignore()
                except Exception:
                    pass
                return
            self._close_waiting_for_configuration_shutdown = False

        if not self._close_loaded_tools_for_shell_shutdown():
            try:
                event.ignore()
            except Exception:
                pass
            self._schedule_embedded_tool_shutdown_retry()
            return

        try:
            super().closeEvent(event)
        except KeyboardInterrupt:
            self._accept_close_event_safely(event)
        except Exception:
            self._accept_close_event_safely(event)
        self._quit_application_after_safe_close()
