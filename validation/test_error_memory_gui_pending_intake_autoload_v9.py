from __future__ import annotations

import json
import sys
from pathlib import Path

FEATURE_ID = "error-memory-gui-pending-intake-autoload-v9"
PENDING_DIR_NAME = "pending_ai_assisted_error_lesson_intake"
PENDING_FILE_NAME = "KANDA_ERROR_LESSON_JSON_freeze_intake_script_syntaxerror_exitcode_guard_v9.txt"
BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
END = "KANDA_ERROR_LESSON_JSON_END"


def _project_analysis_evidence_root(project_root: Path) -> Path:
    drive_root = Path(project_root.anchor or str(project_root)).resolve(strict=False)
    return drive_root / (project_root.name + "_show_project_to_AI")


def _extract_lesson(text: str) -> dict:
    if BEGIN not in text or END not in text:
        raise AssertionError("pending intake file is missing KANDA_ERROR_LESSON_JSON markers")
    json_text = text.split(BEGIN, 1)[1].split(END, 1)[0].strip()
    payload = json.loads(json_text)
    if not isinstance(payload, dict):
        raise AssertionError("pending intake JSON is not an object")
    return payload


def main() -> int:
    project_root = Path(sys.argv[1]).resolve(strict=False) if len(sys.argv) > 1 else Path.cwd().resolve(strict=False)
    source = project_root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    if not source.exists():
        raise AssertionError("missing Error Memory GUI source: " + str(source))
    text = source.read_text(encoding="utf-8")
    required_source_markers = [
        "PENDING_AI_ASSISTED_INTAKE_DIR_NAME",
        "pending_ai_assisted_error_lesson_intake",
        "def _load_pending_ai_assisted_error_lesson_intake",
        "self._load_pending_ai_assisted_error_lesson_intake()",
        "self.raw_error_edit.setPlainText(formatted_text)",
        "self.received_preview_edit.setPlainText(json.dumps(lesson",
        "Memorize Error remains",
    ]
    for marker in required_source_markers:
        if marker not in text:
            raise AssertionError("missing GUI source marker: " + marker)

    if "save_lesson(self._current_project_root(), lesson)" in text.split("def _load_pending_ai_assisted_error_lesson_intake", 1)[1].split("def _reload_table", 1)[0]:
        raise AssertionError("pending intake autoload must not save the lesson")

    pending_file = _project_analysis_evidence_root(project_root) / "project_error_memory" / PENDING_DIR_NAME / PENDING_FILE_NAME
    if not pending_file.exists():
        raise AssertionError("pending intake file was not staged: " + str(pending_file))
    pending_text = pending_file.read_text(encoding="utf-8-sig")
    lesson = _extract_lesson(pending_text)
    if lesson.get("status") != "active":
        raise AssertionError("lesson status must be active")
    if lesson.get("operation_phase") != "install":
        raise AssertionError("lesson operation_phase must be install")
    for field in ("raw_error_text", "symptom", "root_cause", "correct_fix", "do_not_repeat_rule", "prevention_triggers", "validation_evidence"):
        if field not in lesson:
            raise AssertionError("missing lesson field: " + field)
    combined = pending_text + "\n" + str(lesson.get("raw_error_text", ""))
    for marker in ("validation_evidence =", "SyntaxError: invalid syntax", "FREEZE INTAKE PREP OK"):
        if marker not in combined:
            raise AssertionError("pending lesson does not preserve evidence marker: " + marker)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: PENDING_INTAKE_READY")
    print("Pending intake file:")
    print(str(pending_file))
    print("Expected GUI result after restart/opening Error Memory tab:")
    print("- AI-assisted error lesson intake is populated")
    print("- Error Editor is populated")
    print("- Lessons is unchanged until Memorize Error is clicked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
