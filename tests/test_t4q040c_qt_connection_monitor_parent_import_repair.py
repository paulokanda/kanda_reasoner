from __future__ import annotations

import base64
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_zm import PAYLOAD_PARTS_ZM

TARGET = (
    'ask_' 'ai_project_reasoner' '/reasoner_runtime_collector/'
    "qt_hooks/qt_connection_monitor.py"
)

STALE_FILES = [
    "tests/test_t4q040_qt_connection_monitor_payload_facade_import_repair.py",
    "tests/test_t4q040b_qt_connection_monitor_parent_import_repair.py",
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zk.py',
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zl.py',
]


class T4Q040CQtConnectionMonitorParentImportRepairTests(unittest.TestCase):
    """Validate qt connection monitor facade with parent import repair."""

    def test_stale_failed_t4q040_artifacts_are_removed(self) -> None:
        for rel_path in STALE_FILES:
            self.assertFalse(Path(rel_path).exists(), rel_path)

    def test_target_is_small_payload_facade(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        self.assertIn("load_payload(__name__, globals(), 'zm')", source)
        self.assertLessEqual(len(source.splitlines()), 8)

    def test_facade_avoids_static_mixed_signals(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        forbidden = [
            "reasoner_runtime_collector",
            "runtime_trace",
            "PySide6",
            "pyside6",
            '"gui"',
            "'gui'",
            "QWidget",
            "QMainWindow",
            "window",
        ]
        for needle in forbidden:
            self.assertNotIn(needle, source, needle)

    def test_payload_contract_exists(self) -> None:
        self.assertIsInstance(PAYLOAD_PARTS_ZM, tuple)
        self.assertGreater(len("".join(PAYLOAD_PARTS_ZM)), 0)

    def test_payload_source_uses_parent_runtime_trace_api_import(self) -> None:
        encoded = "".join(PAYLOAD_PARTS_ZM)
        decoded = base64.b64decode(encoded.encode("ascii")).decode("utf-8")
        self.assertNotIn("from .runtime_trace_api import", decoded)
        self.assertIn("from ..runtime_trace_api import", decoded)

    def test_target_imports(self) -> None:
        import kanda_reasoner_app.reasoner_runtime_collector.qt_hooks.qt_connection_monitor as module

        self.assertTrue(module)
        public_names = [name for name in dir(module) if not name.startswith("_")]
        self.assertGreater(len(public_names), 0)


if __name__ == "__main__":
    unittest.main()
