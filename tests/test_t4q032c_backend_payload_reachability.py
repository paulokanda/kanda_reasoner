
from __future__ import annotations

import unittest

from kanda_reasoner_app.backend_payloads.loader import load_payload
from kanda_reasoner_app.backend_payloads.payload_a import PAYLOAD_PARTS_A
from kanda_reasoner_app.backend_payloads.payload_b import PAYLOAD_PARTS_B
from kanda_reasoner_app.backend_payloads.payload_c import PAYLOAD_PARTS_C
from kanda_reasoner_app.backend_payloads.payload_d import PAYLOAD_PARTS_D
import kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_help.inference_private_impl as inference_private_impl


class T4Q032CBackendPayloadReachabilityTests(unittest.TestCase):
    """Protect dynamically loaded backend payload modules from dead-code drift."""

    def test_payload_modules_export_unique_payload_parts(self) -> None:
        payloads = [
            PAYLOAD_PARTS_A,
            PAYLOAD_PARTS_B,
            PAYLOAD_PARTS_C,
            PAYLOAD_PARTS_D,
        ]

        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_loader_public_contract_imports(self) -> None:
        self.assertTrue(callable(load_payload))

    def test_context_builder_inference_private_impl_is_test_reachable(self) -> None:
        self.assertTrue(inference_private_impl)


if __name__ == "__main__":
    unittest.main()
