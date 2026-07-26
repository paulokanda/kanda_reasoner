from __future__ import annotations

import json
import sys
from pathlib import Path

FEATURE_ID = "error-memory-gui-pending-intake-root-sync-v10"
PENDING_DIR_NAME = "pending_ai_assisted_error_lesson_intake"
PENDING_FILE_NAME = "KANDA_ERROR_LESSON_JSON_freeze_intake_script_syntaxerror_exitcode_guard_v10.txt"
BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
END = "KANDA_ERROR_LESSON_JSON_END"


def _project_analysis_evidence_root(project_root: Path) -> Path:
    # Windows production path: E:\<project>_show_project_to_AI.
    # Sandbox path: sibling folder beside the temporary project root.
    if project_root.drive:
        drive_root = Path(project_root.anchor).resolve(strict=False)
        return drive_root / (project_root.name + "_show_project_to_AI")
    return project_root.parent / (project_root.name + "_show_project_to_AI")


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
        "self.project_root_edit = self.project_root_value_label",
        "self.project_root_value_label.textChanged.connect(self._on_project_root_field_changed)",
        "def _on_project_root_field_changed",
        "def showEvent",
        "self._refresh_paths()",
        "def _current_project_root",
        "field.text().strip()",
        "self._load_pending_ai_assisted_error_lesson_intake()",
        "resolve_project_error_memory_root(self._current_project_root()) / PENDING_AI_ASSISTED_INTAKE_DIR_NAME",
        "self.raw_error_edit.setPlainText(formatted_text)",
        "self.received_preview_edit.setPlainText(json.dumps(lesson",
    ]
    for marker in required_source_markers:
        if marker not in text:
            raise AssertionError("missing GUI source marker: " + marker)

    set_project_root_block = text.split("def set_project_root", 1)[1].split("def _on_project_root_field_changed", 1)[0]
    if "self._syncing_project_root_field = True" not in set_project_root_block:
        raise AssertionError("set_project_root must guard project root field synchronization")
    if "self._refresh_paths()" not in set_project_root_block:
        raise AssertionError("set_project_root must refresh paths after root propagation")

    pending_block = text.split("def _load_pending_ai_assisted_error_lesson_intake", 1)[1].split("def _reload_table", 1)[0]
    if "save_lesson(" in pending_block:
        raise AssertionError("pending intake autoload must not save the lesson")
    if "self.raw_error_edit.clear()" not in pending_block or "self.received_preview_edit.clear()" not in pending_block:
        raise AssertionError("autoload must replace previous intake/editor content before loading pending lesson")

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
    print("STATUS: PENDING_INTAKE_ROOT_SYNC_READY")
    print("Pending intake file:")
    print(str(pending_file))
    print("Expected GUI result after restart/opening Error Memory tab:")
    print("- AI-assisted error lesson intake is populated")
    print("- Error Editor is populated")
    print("- Lessons is unchanged until Memorize Error is clicked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
