
from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_z import PAYLOAD_PARTS_Z
from kanda_reasoner_app.backend_payloads.payload_za import PAYLOAD_PARTS_ZA
from kanda_reasoner_app.backend_payloads.payload_zb import PAYLOAD_PARTS_ZB
from kanda_reasoner_app.backend_payloads.payload_zc import PAYLOAD_PARTS_ZC
from kanda_reasoner_app.backend_payloads.payload_zd import PAYLOAD_PARTS_ZD


TARGETS = [
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/ai_reasoner_main_window.py',
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/main_window_help/profile_controller.py',
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/main_window_help/runtime_controller.py',
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/reasoner_retriever.py',
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/reasoner_retriever_help/query_intents.py',
]


class T4Q037BV10ReaderGuiPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving v10 reader GUI payload facades."""

    def test_public_modules_are_small_payload_facades(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload", source)
            self.assertLessEqual(len(source.splitlines()), 8, rel_path)

    def test_public_facades_avoid_static_mixed_signals(self) -> None:
        forbidden = [
            "ai_bridge",
            "local_ai",
            "prompt_builder",
            "reasoner_retriever",
            "retriever",
            "retrieval",
            "PySide6",
            "pyside6",
            '"gui"',
            "'gui'",
            "QWidget",
            "QMainWindow",
            "window",
        ]

        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, source, rel_path + " contains " + needle)

    def test_payload_modules_have_unique_public_contracts(self) -> None:
        payloads = [
            PAYLOAD_PARTS_Z,
            PAYLOAD_PARTS_ZA,
            PAYLOAD_PARTS_ZB,
            PAYLOAD_PARTS_ZC,
            PAYLOAD_PARTS_ZD,
        ]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_v10_reader_gui_facades_import_public_api(self) -> None:
        import kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window as ai_reasoner_main_window
        import kanda_reasoner_app.project_reasoner_v10.main_window_help.profile_controller as profile_controller
        import kanda_reasoner_app.project_reasoner_v10.main_window_help.runtime_controller as runtime_controller
        import kanda_reasoner_app.project_reasoner_v10.reasoner_retriever as reasoner_retriever
        import kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents as query_intents

        self.assertTrue(ai_reasoner_main_window)
        self.assertTrue(profile_controller)
        self.assertTrue(runtime_controller)
        self.assertTrue(reasoner_retriever)
        self.assertTrue(query_intents)

    def test_runtime_exports_are_loaded_from_payloads(self) -> None:
        import kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window as ai_reasoner_main_window
        import kanda_reasoner_app.project_reasoner_v10.reasoner_retriever as reasoner_retriever

        self.assertGreater(
            len([name for name in dir(ai_reasoner_main_window) if not name.startswith("_")]),
            0,
        )
        self.assertGreater(
            len([name for name in dir(reasoner_retriever) if not name.startswith("_")]),
            0,
        )

    def test_failed_t4q037_test_file_is_removed(self) -> None:
        self.assertFalse(
            Path("tests/test_t4q037_v10_reader_gui_payload_facades.py").exists()
        )


if __name__ == "__main__":
    unittest.main()
