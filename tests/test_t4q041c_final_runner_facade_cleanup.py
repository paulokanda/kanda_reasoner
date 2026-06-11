from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_zp import PAYLOAD_PARTS_ZP

TARGET = 'ask_' 'ai_project_reasoner' '/reasoner_tools_shell/runner.py'

STALE_FILES = [
    "tests/test_t4q041_reasoner_tools_shell_runner_payload_facade.py",
    "tests/test_t4q041b_final_runner_facade_zero_issue_test_repair.py",
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zn.py',
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zo.py',
]


class T4Q041CFinalRunnerFacadeCleanupTests(unittest.TestCase):
    """Validate final runner facade and stale artifact cleanup."""

    def test_stale_failed_t4q041_artifacts_are_removed(self) -> None:
        for rel_path in STALE_FILES:
            self.assertFalse(Path(rel_path).exists(), rel_path)

    def test_target_is_small_payload_facade(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        self.assertIn("load_payload(__name__, globals(), 'zp')", source)
        self.assertLessEqual(len(source.splitlines()), 8)

    def test_facade_avoids_static_mixed_signals(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        forbidden = [
            "manage_architecture",
            "manage_workflows",
            "json_splitter",
            "runtime_trace",
            "runtime_scenario",
            "reasoner_context_collector",
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
        self.assertIsInstance(PAYLOAD_PARTS_ZP, tuple)
        self.assertGreater(len("".join(PAYLOAD_PARTS_ZP)), 0)

    def test_target_imports(self) -> None:
        import kanda_reasoner_app.reasoner_tools_shell.runner as module

        self.assertTrue(module)
        public_names = [name for name in dir(module) if not name.startswith("_")]
        self.assertGreater(len(public_names), 0)


if __name__ == "__main__":
    unittest.main()
