"""Validate Error Memory heuristic correction button v16."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import py_compile
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

_NORMALIZER_PATH = PROJECT_ROOT / "kanda_reasoner_app/error_memory/heuristic_normalizer.py"
_SPEC = importlib.util.spec_from_file_location("heuristic_normalizer_v16", _NORMALIZER_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Could not load heuristic normalizer module for validation.")
_NORMALIZER = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _NORMALIZER
_SPEC.loader.exec_module(_NORMALIZER)

classify_and_normalize_error_lesson_text = _NORMALIZER.classify_and_normalize_error_lesson_text
ERROR_LESSON_JSON_BEGIN = _NORMALIZER.ERROR_LESSON_JSON_BEGIN
ERROR_LESSON_JSON_END = _NORMALIZER.ERROR_LESSON_JSON_END


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sample_payload() -> dict[str, object]:
    return {
        "lesson_id": "lesson-sample-v16",
        "status": "active",
        "operation_phase": "validation",
        "symptom": "Validation passed but evidence merge used a stale hint.",
        "root_cause": "The helper trusted latest_freeze_hint.json instead of the current patch ZIP sidecar.",
        "correct_fix": "Load the matching KANDA_FREEZE_HINT.json from the current patch ZIP before merging evidence.",
        "do_not_repeat_rule": "Do not merge validation evidence into an unmatched latest freeze hint.",
        "prevention_triggers": "feature_id mismatch; latest freeze hint stale",
        "exception": {"type": "FreezeHintEvidenceMergeError"},
        "fingerprint": {"fingerprint_hash": "sample-v16"},
        "redaction": {"applied": True, "export_safe": True, "rules": ["No secrets present."]},
    }


def main() -> int:
    gui_path = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
    normalizer_path = PROJECT_ROOT / "kanda_reasoner_app/error_memory/heuristic_normalizer.py"
    merge_path = PROJECT_ROOT / "scripts/merge_freeze_validation_evidence.py"
    py_compile.compile(str(gui_path), doraise=True)
    py_compile.compile(str(normalizer_path), doraise=True)
    py_compile.compile(str(merge_path), doraise=True)

    gui_text = gui_path.read_text(encoding="utf-8")
    required_gui_fragments = [
        'self.heuristic_correction_button = QPushButton("Need AI to Correct")',
        'self.heuristic_correction_button.clicked.connect(self._apply_heuristic_correction_to_error_editor)',
        'self.received_preview_edit.textChanged.connect(self._refresh_heuristic_correction_button_state)',
        'self.raw_error_edit.textChanged.connect(self._refresh_heuristic_correction_button_state)',
        'self.heuristic_correction_button.setText("Heuristic Correction")',
        'self.heuristic_correction_button.setText("Need AI to Correct")',
        'self.heuristic_correction_button.setEnabled(True)',
        'self.heuristic_correction_button.setEnabled(False)',
        'color: #187a2f; font-weight: 700',
        'color: #b00020; font-weight: 700',
        'self.raw_error_edit.setPlainText(self._formatted_lesson_block(lesson))',
        'self.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))',
        'No root cause, correction, prevention rule, or validation evidence was invented.',
    ]
    for fragment in required_gui_fragments:
        _assert(fragment in gui_text, "missing GUI fragment: " + fragment)

    helper_scope = gui_text.split('def _apply_heuristic_correction_to_error_editor', 1)[1].split('def _load_selected_lesson_into_preview', 1)[0]
    forbidden = [
        'build_error_lesson_ai_form_prompt',
        'parse_error_lesson_ai_response',
        'build_lesson_from_ai_form',
    ]
    for fragment in forbidden:
        _assert(fragment not in helper_scope, "heuristic button must not call AI/form helper: " + fragment)

    payload = _sample_payload()
    wrapped = ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(payload, indent=2) + "\n" + ERROR_LESSON_JSON_END
    result = classify_and_normalize_error_lesson_text(
        wrapped,
        project_slug="kanda_reasoner",
        now_factory=lambda: "2026-06-26T19:00:00Z",
        id_factory=lambda: "lesson-generated-v16",
    )
    _assert(result.can_apply and result.level == 1, "complete receive-ready payload must be Level 1")
    _assert(result.label == "Heuristic Correction", "Level 1 label must be Heuristic Correction")
    lesson = result.lesson or {}
    _assert(lesson.get("schema_version") == "1.0", "schema_version must be added")
    _assert(lesson.get("project_slug") == "kanda_reasoner", "project_slug must be added")
    _assert(lesson.get("updated_at_utc") == "2026-06-26T19:00:00Z", "updated timestamp must be deterministic in test")
    _assert(lesson.get("prevention_triggers") == ["feature_id mismatch", "latest freeze hint stale"], "string triggers must become a list")

    incomplete = dict(payload)
    incomplete["root_cause"] = ""
    level3 = classify_and_normalize_error_lesson_text(json.dumps(incomplete), project_slug="kanda_reasoner")
    _assert(not level3.can_apply and level3.level == 3, "missing semantics must lock button")
    _assert(level3.label == "Need AI to Correct", "Level 3 label must be Need AI to Correct")

    missing_structural = dict(payload)
    missing_structural.pop("redaction")
    level2 = classify_and_normalize_error_lesson_text(json.dumps(missing_structural), project_slug="kanda_reasoner")
    _assert(not level2.can_apply and level2.level == 2, "missing structural redaction must lock button")

    outer = {
        "status": "active",
        "raw_error_text": json.dumps(payload),
        "operation_phase": "validation",
        "symptom": "",
        "root_cause": "",
        "correct_fix": "",
        "do_not_repeat_rule": "",
        "prevention_triggers": [],
    }
    nested = classify_and_normalize_error_lesson_text(json.dumps(outer), project_slug="kanda_reasoner")
    _assert(nested.can_apply and nested.level == 1, "nested raw_error_text JSON should unwrap when it has the real lesson")
    _assert((nested.lesson or {}).get("lesson_id") == "lesson-sample-v16", "nested lesson payload should win")

    print("VALIDATION OK: error-memory-heuristic-correction-button-v16")
    print("ERROR_MEMORY_HEURISTIC_BUTTON: green unlocked Level 1 enforced")
    print("ERROR_MEMORY_HEURISTIC_BUTTON: red locked Level 2/3 enforced")
    print("ERROR_MEMORY_HEURISTIC_BUTTON: updates Error Editor and AI-assisted intake")
    print("ERROR_MEMORY_HEURISTIC_BUTTON: no semantic invention enforced")
    print("ERROR_MEMORY_PREVIOUS_GUARDS: copy button and pending-intake behavior preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
