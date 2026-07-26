from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"

text = SOURCE.read_text(encoding="utf-8")


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)


require(
    "def _set_ai_assisted_intake_and_error_editor_from_pending_text" in text,
    "missing pending-text intake renderer",
)
require(
    "def _set_ai_assisted_intake_and_error_editor_to_same_lesson_json" not in text,
    "old same-json mirror renderer must be removed",
)
require(
    "self.raw_error_edit.setPlainText(formatted_text.strip())" in text,
    "AI-assisted intake must render the pending receive-ready text exactly enough to preserve wrapper/layout",
)
require(
    "self.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))" in text,
    "Error Editor must remain normalized editable JSON",
)
require(
    "self._set_ai_assisted_intake_and_error_editor_from_pending_text(formatted_text, lesson)" in text,
    "pending loader must call the split intake/editor renderer with formatted_text",
)
require(
    "self._load_pending_ai_assisted_error_lesson_intake(mirror_loaded_json_to_error_editor=True)" in text,
    "post-Memorize auto-advance path must remain wired",
)
require(
    "self.raw_error_edit.setPlainText(lesson_json)" not in text,
    "AI-assisted intake must not be populated with raw editor JSON",
)
require(
    "KANDA_ERROR_LESSON_JSON_BEGIN / KANDA_ERROR_LESSON_JSON_END wrapper" in text,
    "renderer doc must preserve receive-ready wrapper contract",
)
require(
    "def _copy_ai_assisted_intake_error_draft_to_clipboard" in text,
    "v18 AI-assisted intake copy button must be preserved",
)
require(
    "QApplication.clipboard().setText(intake_text)" in text,
    "v18 intake copy button must still copy intake text",
)
require(
    "def _copy_error_draft_to_clipboard" in text,
    "existing Error Editor copy button must be preserved",
)
require(
    "def _apply_heuristic_correction_to_error_editor" in text,
    "heuristic correction guard must be preserved",
)

print("VALIDATION OK: error-memory-ai-intake-pending-format-v19")
print("ERROR_MEMORY_AI_INTAKE_PENDING_FORMAT: pending file layout preserved in AI-assisted intake")
print("ERROR_MEMORY_AI_INTAKE_PENDING_FORMAT: KANDA_ERROR_LESSON_JSON wrapper preserved")
print("ERROR_MEMORY_AI_INTAKE_PENDING_FORMAT: Error Editor remains normalized JSON")
print("ERROR_MEMORY_AI_INTAKE_PENDING_FORMAT: post-Memorize auto-load uses split renderer")
print("ERROR_MEMORY_PREVIOUS_GUARDS: intake copy, editor copy, heuristic, pending consume preserved")
