"""Regression tests for Receive Formulary from AI parse-error feedback."""

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"


class FreezeFormularyParseErrorFeedbackTests(unittest.TestCase):
    def test_parse_error_message_tells_user_to_ask_ai_to_do_it_again(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        self.assertIn("Ask AI to do it again.", source)
        self.assertIn("return exactly one valid JSON object", source)
        self.assertIn("with no markdown, no prose, and no extra text", source)

    def test_parse_error_message_keeps_exact_freeze_json_markers(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        self.assertIn("KANDA_FREEZE_FORM_JSON_BEGIN", source)
        self.assertIn("KANDA_FREEZE_FORM_JSON_END", source)
        self.assertNotIn("KAnUA_FREEZE_FORM_JSON_END", source)
        self.assertNotIn("KANDA_FREEZE_FORM_JSON_BEGIM", source)

    def test_parse_error_still_exposes_original_error_details(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        self.assertIn('f"Error: {exc}"', source)
        self.assertIn("Could not parse AI formulary", source)


if __name__ == "__main__":
    unittest.main()
