"""Regression tests for canonical backend payload loading."""

from __future__ import annotations

import base64
import types
import unittest
from pathlib import Path
from unittest import mock

from kanda_reasoner_app.backend_payloads import loader


class BackendPayloadLoaderCanonicalImportTests(unittest.TestCase):
    """Validate canonical import routing for encoded backend payloads."""

    def test_load_payload_imports_payload_through_canonical_package(self) -> None:
        payload_source = "RESULT = 'loaded through canonical package'\n"
        encoded = base64.b64encode(payload_source.encode("utf-8")).decode("ascii")
        fake_payload_module = types.SimpleNamespace(PAYLOAD_PARTS_DEMO=(encoded,))

        imported_names: list[str] = []

        def fake_import_module(module_name: str) -> object:
            imported_names.append(module_name)
            return fake_payload_module

        target_globals: dict[str, object] = {}

        with mock.patch.object(loader.importlib, "import_module", fake_import_module):
            loader.load_payload("demo_module", target_globals, "demo")

        self.assertEqual(
            imported_names,
            ["kanda_reasoner_app.backend_payloads.payload_demo"],
        )
        self.assertEqual(target_globals["RESULT"], "loaded through canonical package")

    def test_loader_source_does_not_hardcode_legacy_payload_import_path(self) -> None:
        legacy_token = "ask_ai" + "_project_reasoner"
        source = Path(loader.__file__).read_text(encoding="utf-8")

        self.assertNotIn(legacy_token + ".backend_payloads.payload_", source)
        self.assertIn("kanda_reasoner_app.backend_payloads.payload_", source)


if __name__ == "__main__":
    unittest.main()
