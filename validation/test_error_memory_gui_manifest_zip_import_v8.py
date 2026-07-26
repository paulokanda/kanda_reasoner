from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path

ERROR_BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
ERROR_END = "KANDA_ERROR_LESSON_JSON_END"


def assert_contains(text: str, needle: str, message: str) -> None:
    if needle not in text:
        raise AssertionError(message + f" Missing: {needle}")


def section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index) if end in text[start_index + len(start):] else len(text)
    return text[start_index:end_index]


def read_manifest_receive_block(zip_path: Path) -> str:
    with zipfile.ZipFile(zip_path) as archive:
        manifest = json.loads(archive.read("bundle_manifest.json").decode("utf-8-sig"))
        if manifest.get("artifact_type") != "formatted_error_memory_lesson_zip":
            raise AssertionError("Wrong artifact_type")
        receive_block = manifest.get("receive_block")
        if not receive_block:
            raise AssertionError("Missing receive_block")
        text = archive.read(receive_block).decode("utf-8-sig")
        if ERROR_BEGIN not in text or ERROR_END not in text:
            raise AssertionError("Missing KANDA_ERROR_LESSON_JSON markers")
        return text


def build_test_zip(path: Path) -> None:
    lesson = {
        "status": "active",
        "raw_error_text": "validation_evidence =\\nSyntaxError: invalid syntax\\nFREEZE INTAKE PREP OK",
        "operation_phase": "install",
        "symptom": "Generated freeze intake helper failed, then wrapper printed false success.",
        "root_cause": "The generated helper left validation_evidence empty and the wrapper did not gate success on child exit code.",
        "wrong_assumption": "Assumed generated helper execution failure would automatically stop success output.",
        "correct_fix": "Use JSON payload files for complex data and check exit code plus expected artifact before success output.",
        "long_term_prevention": "Generated helper workflows must compile, execute, and verify output before printing success.",
        "do_not_repeat_rule": "Do not print success after a generated helper failure or missing output artifact.",
        "prevention_triggers": ["validation_evidence =", "SyntaxError: invalid syntax", "FREEZE INTAKE PREP OK"],
        "validation_evidence": ["VALIDATION OK: test direct Error Lesson ZIP import"],
        "regression_check": {"type": "validation_command", "command": "python validation/test_error_memory_gui_manifest_zip_import_v8.py", "expected_marker": "VALIDATION OK: error-memory-gui-manifest-zip-import-v8", "required_before_freeze": False},
        "source_patch_zip": "",
        "install_command_summary": "Direct lesson ZIP is staged for GUI import only.",
        "validation_command_summary": "Validation checks manifest-declared receive_block extraction.",
        "notes": "Test lesson for manifest-first ZIP import."
    }
    receive = ERROR_BEGIN + "\n" + json.dumps(lesson, indent=2, ensure_ascii=False) + "\n" + ERROR_END + "\n"
    manifest = {
        "schema_version": "1.0",
        "artifact_type": "formatted_error_memory_lesson_zip",
        "feature_id": "test-direct-error-lesson-zip",
        "intended_gui_path": "Error Memory tab -> Import Error Lesson ZIP -> AI-assisted intake + Error Editor",
        "operation_phase": "install",
        "receive_block": "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_test.txt"
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("bundle_manifest.json", json.dumps(manifest, indent=2))
        archive.writestr("payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_test.txt", receive)
        archive.writestr("payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_test.txt", lesson["raw_error_text"])


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    gui_path = project_root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    source = gui_path.read_text(encoding="utf-8")

    assert_contains(source, "def _formatted_text_from_manifested_lesson_zip", "GUI must have manifest-first ZIP import helper.")
    assert_contains(source, 'artifact_type", "")).strip() != "formatted_error_memory_lesson_zip"', "GUI must recognize direct Error Lesson ZIP artifact type.")
    assert_contains(source, 'receive_block = str(manifest.get("receive_block", ""))', "GUI must read manifest receive_block.")

    formatted_import = section(source, "def _formatted_import_text_for_window", "def _import_error_lesson_zip")
    assert_contains(formatted_import, "manifested_text = self._formatted_text_from_manifested_lesson_zip(source)", "ZIP import must prefer manifest-declared receive block before scanning.")
    assert_contains(formatted_import, "if manifested_text:", "ZIP import must return manifested text when valid.")

    import_section = section(source, "def _import_error_lesson_zip", "def _save_preview_lesson")
    assert_contains(import_section, "self.raw_error_edit.setPlainText(formatted_text)", "Import must populate AI-assisted error lesson intake.")
    assert_contains(import_section, "self.received_preview_edit.setPlainText(json.dumps(lesson", "Import must populate Error Editor.")
    assert_contains(import_section, "It was not saved yet", "Import must not save directly before Memorize Error.")

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "test_error_lesson.zip"
        build_test_zip(zip_path)
        receive = read_manifest_receive_block(zip_path)
        if "validation_evidence =" not in receive:
            raise AssertionError("Receive block did not preserve raw error evidence")
        if "SyntaxError: invalid syntax" not in receive:
            raise AssertionError("Receive block did not preserve SyntaxError evidence")
        if "FREEZE INTAKE PREP OK" not in receive:
            raise AssertionError("Receive block did not preserve false success evidence")

    print("VALIDATION OK: error-memory-gui-manifest-zip-import-v8")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
