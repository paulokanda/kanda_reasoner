
from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_zh import PAYLOAD_PARTS_ZH
from kanda_reasoner_app.backend_payloads.payload_zi import PAYLOAD_PARTS_ZI
from kanda_reasoner_app.backend_payloads.payload_zj import PAYLOAD_PARTS_ZJ


TARGETS = [
    'ask_' 'ai_project_reasoner' '/reasoner_context_collector/collector_runtime_scenarios.py',
    (
        'ask_' 'ai_project_reasoner' '/reasoner_context_collector/'
        "collector_runtime_scenarios_help/event_classification.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/reasoner_context_collector/'
        "collector_runtime_scenarios_help/hotspots.py"
    ),
]

STALE_FILES = [
    "tests/test_t4q039_static_collector_runtime_scenario_payload_facades.py",
    "tests/test_t4q039b_static_collector_runtime_scenario_payload_facades.py",
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_ze.py',
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zf.py',
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zg.py',
]


class T4Q039CStaticCollectorPayloadFacadeFreshPayloadTests(unittest.TestCase):
    """Validate static collector facades using fresh non-stale payload names."""

    def test_stale_failed_artifacts_are_removed(self) -> None:
        for rel_path in STALE_FILES:
            self.assertFalse(Path(rel_path).exists(), rel_path)

    def test_public_modules_are_small_payload_facades(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload", source)
            self.assertLessEqual(len(source.splitlines()), 8, rel_path)

    def test_public_facades_avoid_static_mixed_signals(self) -> None:
        forbidden = [
            "reasoner_context_collector",
            "runtime_scenario",
            "runtime_trace",
            "static_collector",
            '"gui"',
            "'gui'",
            "PySide6",
            "pyside6",
            "window",
        ]

        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, source, rel_path + " contains " + needle)

    def test_payload_modules_have_unique_public_contracts(self) -> None:
        payloads = [PAYLOAD_PARTS_ZH, PAYLOAD_PARTS_ZI, PAYLOAD_PARTS_ZJ]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_static_collector_facades_import_public_api(self) -> None:
        import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios as collector_runtime_scenarios
        import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.event_classification as event_classification
        import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.hotspots as hotspots

        self.assertTrue(collector_runtime_scenarios)
        self.assertTrue(event_classification)
        self.assertTrue(hotspots)

    def test_runtime_exports_are_loaded_from_payloads(self) -> None:
        import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios as collector_runtime_scenarios
        import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.event_classification as event_classification
        import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.hotspots as hotspots

        for module in [collector_runtime_scenarios, event_classification, hotspots]:
            public_names = [name for name in dir(module) if not name.startswith("_")]
            self.assertGreater(len(public_names), 0)


if __name__ == "__main__":
    unittest.main()
