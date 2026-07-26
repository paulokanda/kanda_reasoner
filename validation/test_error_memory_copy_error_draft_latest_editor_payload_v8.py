"""Validate Copy Last Error/Draft strips old prompt wrappers.

The button must copy only the latest Error Editor payload.  If the editor still
contains the old AI formulary prompt, it must extract the embedded raw_error_text
from Current error/draft JSON rather than copying the prompt itself.
"""

from __future__ import annotations

import json
from pathlib import Path
import importlib.util

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
HELPER_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory" / "editor_clipboard.py"

spec = importlib.util.spec_from_file_location("kanda_editor_clipboard_for_validation", HELPER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load editor_clipboard helper for validation.")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
ERROR_DRAFT_MARKER = helper.ERROR_DRAFT_MARKER
extract_error_editor_text_for_ai = helper.extract_error_editor_text_for_ai


def _method_block(source: str, name: str) -> str:
    marker = "    def " + name + "("
    start = source.index(marker)
    next_start = source.find("\n    def ", start + 1)
    if next_start == -1:
        return source[start:]
    return source[start:next_start]


def test_prompt_wrapper_is_stripped() -> None:
    inner_error = json.dumps(
        {
            "correct_fix": "Use --patch-zip.",
            "root_cause": "latest_freeze_hint.json was stale.",
            "status": "active",
        },
        indent=2,
        sort_keys=True,
    )
    old_prompt = (
        "You are a specialist in KANDA Reasoner.\n\n"
        "Task:\nReview the error/context.\n\n"
        "Return format - strict copy/paste contract.\n\n"
        + ERROR_DRAFT_MARKER
        + "\n"
        + json.dumps(
            {
                "status": "active",
                "raw_error_text": inner_error,
                "operation_phase": "validation",
                "symptom": "",
                "root_cause": "",
            },
            indent=2,
            sort_keys=True,
        )
    )
    copied = extract_error_editor_text_for_ai(old_prompt)
    if copied != inner_error:
        raise AssertionError("Old AI prompt wrapper must be stripped to embedded raw_error_text.")
    for forbidden in ["You are a specialist", "Task:", "Return format", ERROR_DRAFT_MARKER]:
        if forbidden in copied:
            raise AssertionError("Prompt wrapper leaked into copied payload: " + forbidden)


def test_latest_prompt_payload_wins() -> None:
    first = ERROR_DRAFT_MARKER + "\n" + json.dumps({"raw_error_text": "FIRST_ERROR"})
    second = ERROR_DRAFT_MARKER + "\n" + json.dumps({"raw_error_text": "SECOND_ERROR"})
    copied = extract_error_editor_text_for_ai(first + "\n\n" + second)
    if copied != "SECOND_ERROR":
        raise AssertionError("The latest embedded error/draft payload must win.")


def test_plain_editor_text_is_preserved() -> None:
    plain = "Traceback line 1\nAttributeError: QTextCursor has no attribute Start"
    if extract_error_editor_text_for_ai("\n" + plain + "\n") != plain:
        raise AssertionError("Plain Error Editor text must be copied unchanged except outer whitespace.")


def test_last_receive_ready_block_wins() -> None:
    block1 = "KANDA_ERROR_LESSON_JSON_BEGIN\n{\"status\": \"draft\", \"raw_error_text\": \"ONE\"}\nKANDA_ERROR_LESSON_JSON_END"
    block2 = "KANDA_ERROR_LESSON_JSON_BEGIN\n{\"status\": \"draft\", \"raw_error_text\": \"TWO\"}\nKANDA_ERROR_LESSON_JSON_END"
    copied = extract_error_editor_text_for_ai(block1 + "\nnoise\n" + block2)
    if '"TWO"' not in copied or '"ONE"' in copied:
        raise AssertionError("The last receive-ready block must be copied when multiple blocks are present.")


def test_gui_wiring() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    if "build_error_lesson_ai_form_prompt" in source:
        raise AssertionError("Copy error/draft to AI must not import or call the prompt builder.")
    if "_copy_formulary_prompt_to_ai" in source:
        raise AssertionError("Old prompt-copy handler name remains wired or defined.")
    if "copy_formulary_button.clicked.connect(self._copy_error_editor_text_to_ai)" not in source:
        raise AssertionError("Copy button must be wired to _copy_error_editor_text_to_ai.")
    if "Copy Last Error/Draft to AI" not in source:
        raise AssertionError("Button label must reflect latest error/draft payload contract.")
    if "Old prompt wrappers are stripped before copying" not in source:
        raise AssertionError("Tooltip must state old prompt wrapper stripping behavior.")

    block = _method_block(source, "_copy_error_editor_text_to_ai")
    required = [
        "editor_text = self.received_preview_edit.toPlainText()",
        "payload_text = extract_error_editor_text_for_ai(editor_text)",
        "QApplication.clipboard().setText(payload_text)",
        "Prompt wrappers were not copied.",
    ]
    missing = [fragment for fragment in required if fragment not in block]
    if missing:
        raise AssertionError("Handler missing required payload-only fragments: " + "; ".join(missing))
    forbidden = [
        "build_error_lesson_ai_form_prompt",
        "selected_project_root",
        "raw_error_text=editor",
        "operation_phase=",
        "ERROR_LESSON_JSON_BEGIN",
        "ERROR_LESSON_JSON_END",
        "QApplication.clipboard().setText(editor_text)",
    ]
    for fragment in forbidden:
        if fragment in block:
            raise AssertionError("Handler still contains old prompt/raw-copy behavior: " + fragment)

    export_block = _method_block(source, "_export_for_ai")
    if "textCursor().Start" in export_block:
        raise AssertionError("QTextCursor Start regression returned in _export_for_ai.")
    if "write_error_memory_ai_send_files" in export_block or "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("Complete Error Memory export must not regress to second_prompt_files.")


def main() -> None:
    test_prompt_wrapper_is_stripped()
    test_latest_prompt_payload_wins()
    test_plain_editor_text_is_preserved()
    test_last_receive_ready_block_wins()
    test_gui_wiring()
    print("VALIDATION OK: error-memory-copy-error-draft-latest-editor-payload-v8")
    print("ERROR_MEMORY_COPY_DRAFT: latest editor payload only")
    print("ERROR_MEMORY_COPY_DRAFT_NO_PROMPT_WRAPPER: enforced")
    print("ERROR_MEMORY_COPY_DRAFT_EXTRACTS_RAW_ERROR_TEXT: enforced")
    print("ERROR_MEMORY_EXPORT_PREVIOUS_GUARDS: preserved")


if __name__ == "__main__":
    main()
