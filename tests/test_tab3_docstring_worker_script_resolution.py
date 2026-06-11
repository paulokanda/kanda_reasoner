"""Focused tests for Tab 3 docstring worker script path resolution."""

from __future__ import annotations

import base64
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_WORKER = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings.py"
)
LEGACY_TOKEN = "ask_ai_project_reasoner"
CANONICAL_TOKEN = "kanda_reasoner_app"
PAYLOAD_T = PROJECT_ROOT / "kanda_reasoner_app" / "backend_payloads" / "payload_t.py"
GUI_SUPPORT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "gui_support.py"
)


def _decoded_payload_t_source() -> str:
    namespace: dict[str, object] = {}
    exec(PAYLOAD_T.read_text(encoding="utf-8"), namespace)
    encoded_parts = namespace["PAYLOAD_PARTS_T"]
    if not isinstance(encoded_parts, tuple):
        raise TypeError("PAYLOAD_PARTS_T must be a tuple.")
    encoded = "".join(str(part) for part in encoded_parts)
    return base64.b64decode(encoded.encode("ascii")).decode("utf-8")


class Tab3DocstringWorkerScriptResolutionTests(unittest.TestCase):
    """Verify Tab 3 resolves its worker through the canonical package."""

    def test_canonical_worker_file_exists(self) -> None:
        self.assertTrue(CANONICAL_WORKER.exists(), CANONICAL_WORKER)

    def test_tab3_status_label_resolver_uses_canonical_constant(self) -> None:
        source = GUI_SUPPORT.read_text(encoding="utf-8")
        function_source = source.split("def _docstring_worker_script_path", 1)[1]
        function_source = function_source.split("def _help_catalog_path", 1)[0]
        self.assertIn("CANONICAL_PACKAGE_NAME", function_source)
        self.assertNotIn("LEGACY_PACKAGE_NAME", function_source)
        self.assertNotIn(LEGACY_TOKEN, function_source)

    def test_tab3_window_payload_uses_canonical_worker_helper(self) -> None:
        decoded_source = _decoded_payload_t_source()
        self.assertIn("def _canonical_worker_script_path()", decoded_source)
        self.assertIn(CANONICAL_TOKEN, decoded_source)
        self.assertNotIn(
            "Path(__file__).resolve().parent.parent / DEFAULT_WORKER_NAME",
            decoded_source,
        )


if __name__ == "__main__":
    unittest.main()
