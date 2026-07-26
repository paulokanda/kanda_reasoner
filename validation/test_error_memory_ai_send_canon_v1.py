"""Validation for Error Memory AI-send canon v1."""

from __future__ import annotations

import json
import sys
import tempfile
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import zipfile

from kanda_reasoner_app.error_memory.exporter import write_error_memory_ai_send_files
from kanda_reasoner_app.error_memory.models import build_lesson
from kanda_reasoner_app.error_memory.paths import (
    resolve_project_error_memory_root,
    resolve_second_prompt_files_root,
)
from kanda_reasoner_app.error_memory.scrubber import scrub_text
from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
from kanda_reasoner_app.project_analysis_evidence_paths import project_analysis_evidence_root


def _make_project_root() -> Path:
    base = Path(tempfile.mkdtemp(prefix="kanda_error_memory_test_"))
    root = base / ("Sample Project " + uuid.uuid4().hex[:8])
    root.mkdir(parents=True)
    return root


def test_dynamic_paths_and_no_source_tree_memory() -> None:
    root = _make_project_root()
    show_root = project_analysis_evidence_root(root)
    memory_root = resolve_project_error_memory_root(root)
    assert memory_root == show_root / "project_error_memory"
    assert resolve_second_prompt_files_root(root) == show_root / "second_prompt_files"
    assert "project_freeze_ledger" not in str(memory_root)
    assert memory_root.name == "project_error_memory"
    assert memory_root.parent.name.endswith("_show_project_to_AI")
    assert "sample_project" in memory_root.parent.name


def test_scrubber_masks_sensitive_export_text() -> None:
    text = r"C:\Users\Rafael\project\file.py API_KEY=sk-secret123456 email@test.com 192.168.0.1"
    result = scrub_text(text)
    assert "Rafael" not in result.text
    assert "email@test.com" not in result.text
    assert "192.168.0.1" not in result.text
    assert "sk-secret" not in result.text
    assert "<USER>" in result.text
    assert "<EMAIL>" in result.text
    assert "<IP>" in result.text
    assert "<SECRET>" in result.text


def test_save_lesson_and_export_compact_plus_full_zip() -> None:
    root = _make_project_root()
    lesson = build_lesson(
        selected_project_root=root,
        raw_error_text='Traceback\n  File "C:/Users/Rafael/Sample Project/kanda_reasoner_app/gui.py", line 77, in test_gui_state\nKeyError: missing_state',
        operation_phase="validation",
        symptom="Validation failed with missing GUI state key.",
        root_cause="The state producer did not return the key expected by validation.",
        correct_fix="Return the key from the producer and validate with regression test.",
        do_not_repeat_rule="When adding validation-visible GUI state, update producer and validation together.",
        prevention_triggers=["KeyError in GUI state", "missing validation-visible key"],
        validation_evidence=["VALIDATION OK: error memory test"],
        status="active",
    )
    saved_path = save_lesson(root, lesson)
    assert saved_path.exists()
    assert len(list_lessons(root, include_inactive=False)) == 1

    destination = resolve_second_prompt_files_root(root)
    result = write_error_memory_ai_send_files(root, destination)
    assert result["ok"] is True
    compact = Path(result["compact_json"])
    prompt = Path(result["prompt_md"])
    manifest = Path(result["manifest_json"])
    full_zip = Path(result["full_zip"])
    assert compact.exists()
    assert prompt.exists()
    assert manifest.exists()
    assert full_zip.exists()

    compact_payload = json.loads(compact.read_text(encoding="utf-8"))
    assert compact_payload["artifact_type"] == "error_memory_ai_export"
    assert compact_payload["lessons"][0]["lesson_id"] == lesson["lesson_id"]
    assert compact_payload["derived_from"]["redaction_applied"] is True
    assert "Full Error Memory ZIP" in prompt.read_text(encoding="utf-8")

    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert manifest_payload["compact_error_memory_always_read"] is True
    assert manifest_payload["full_error_memory_zip_open_policy"] == "open_only_when_needed"

    with zipfile.ZipFile(full_zip) as archive:
        names = archive.namelist()
    assert "project_error_memory/lessons_index.json" in names
    assert any(name.startswith("project_error_memory/lessons/lesson-") for name in names)


def main() -> int:
    test_dynamic_paths_and_no_source_tree_memory()
    test_scrubber_masks_sensitive_export_text()
    test_save_lesson_and_export_compact_plus_full_zip()
    print("VALIDATION OK: error-memory-ai-send-canon-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
