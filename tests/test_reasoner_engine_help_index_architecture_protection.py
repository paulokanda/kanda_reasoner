"""Architecture protection tests for canonical reasoner_engine help_index modules."""

import unittest

import kanda_reasoner_app.reasoner_engine.help_index as canonical_help_index
import kanda_reasoner_app.reasoner_engine.help_index_help.help_index_data as canonical_help_index_data
import kanda_reasoner_app.reasoner_engine.help_index_help.help_index_normalization as canonical_help_index_normalization
import kanda_reasoner_app.reasoner_engine.help_index_help.help_index_raw as canonical_help_index_raw


class ReasonerEngineHelpIndexArchitectureProtectionTests(unittest.TestCase):
    """Protect canonical help_index public contracts after migration."""

    def test_canonical_help_index_public_contracts_are_directly_importable(self):
        self.assertTrue(hasattr(canonical_help_index, "HELP_INDEX"))
        self.assertTrue(hasattr(canonical_help_index_data, "HELP_INDEX"))
        self.assertTrue(hasattr(canonical_help_index_normalization, "normalize_help_payload"))
        self.assertTrue(hasattr(canonical_help_index_normalization, "normalize_help_text"))
        self.assertTrue(hasattr(canonical_help_index_raw, "RAW_HELP_INDEX"))

    def test_normalization_public_functions_are_callable(self):
        self.assertTrue(callable(canonical_help_index_normalization.normalize_help_payload))
        self.assertTrue(callable(canonical_help_index_normalization.normalize_help_text))

    def test_canonical_help_index_payload_is_available(self):
        self.assertIsNotNone(canonical_help_index.HELP_INDEX)
        self.assertIsNotNone(canonical_help_index_data.HELP_INDEX)
        self.assertIsNotNone(canonical_help_index_raw.RAW_HELP_INDEX)


if __name__ == "__main__":
    unittest.main()
