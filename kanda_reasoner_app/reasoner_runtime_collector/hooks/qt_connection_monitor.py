# project-path: kanda_reasoner_app/reasoner_runtime_collector/hooks/qt_connection_monitor.py
"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

import sys
import unittest
import os
from pathlib import Path

def _resolve_project_root() -> str:
    """Support resolve project root behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    value = os.environ.get("DEVTOOLS_PROJECT_ROOT", "").strip()
    if not value:
        raise RuntimeError(
            "Set DEVTOOLS_PROJECT_ROOT before using this module."
        )
    return str(Path(value).expanduser().resolve())


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
if __name__ == "__main__":
    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))

from runtime_trace_api import configure_runtime_trace, get_runtime_trace_writer
from qt_hooks.qt_connection_monitor import (
    install_qt_connection_monitor,
    uninstall_qt_connection_monitor,
)


class TestQtConnectionMonitor(unittest.TestCase):
    """Represent test qt connection monitor."""
    
    def test_install_and_uninstall_are_safe(self) -> None:
        """Support test install and uninstall are safe behavior.
        """
        
        configure_runtime_trace(
            project_root=_resolve_project_root(),
            output_path="",
            entry_script="test_qt_connection_monitor.py",
        )

        installed = install_qt_connection_monitor()
        self.assertIn(installed, (True, False))

        uninstalled = uninstall_qt_connection_monitor()
        self.assertIn(uninstalled, (True, False))

    def test_trace_signal_connection_storage(self) -> None:
        """Support test trace signal connection storage behavior.
        """
        
        writer = configure_runtime_trace(
            project_root=_resolve_project_root(),
            output_path="",
            entry_script="test_qt_connection_monitor.py",
        )

        writer.trace_signal_connection(
            sender_type="QPushButton",
            sender_name="run_button",
            signal_name="clicked",
            receiver_type="CollectorRunnerWindow",
            receiver_name="main_window",
            slot_name="_run_collector",
            source_file="runner.py",
            source_line=42,
            extra={"mode": "test"},
        )

        payload = writer.build_payload()
        self.assertIn("signal_connections", payload)
        self.assertEqual(len(payload["signal_connections"]), 1)
        self.assertEqual(payload["signal_connections"][0]["signal_name"], "clicked")
        self.assertEqual(payload["signal_connections"][0]["slot_name"], "_run_collector")


if __name__ == "__main__":
    unittest.main()
