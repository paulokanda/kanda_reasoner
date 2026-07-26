"""Static and behavioral contracts for Error Memory draft deletion helpers."""
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _draft_deletion


def test_draft_deletion_helper_is_private_non_gui_contract() -> None:
    source = Path(_draft_deletion.__file__).read_text(encoding="utf-8")

    assert "PySide" not in source
    assert "Qt" not in source
    assert "error_memory_tab" not in source
    assert "ErrorMemoryTab" not in source


def test_draft_delete_identity_collects_text_ids_markers_and_selected_lesson() -> None:
    lesson_ids, visible_texts, explicit_paths = _draft_deletion.draft_delete_identity_from_sources(
        raw_error_text='{"lesson_id": "raw-id"}',
        received_preview_text='plain visible draft',
        last_dismissed_pending_intake_text='{"lesson_id": "dismissed-id"}',
        loaded_pending_intake_lesson_id="loaded-id",
        last_dismissed_pending_intake_lesson_id="dismissed-marker-id",
        selected_lesson_id="selected-id",
        current_lesson={"lesson_id": "current-id"},
        loaded_pending_intake_file="/tmp/pending/raw.txt",
        last_dismissed_pending_intake_file="/tmp/pending/raw.txt",
        lesson_id_from_text=lambda text: "raw-id" if "raw-id" in text else ("dismissed-id" if "dismissed-id" in text else ""),
    )

    assert lesson_ids == {
        "raw-id",
        "dismissed-id",
        "loaded-id",
        "dismissed-marker-id",
        "selected-id",
        "current-id",
    }
    assert visible_texts == [
        '{"lesson_id": "raw-id"}',
        "plain visible draft",
        '{"lesson_id": "dismissed-id"}',
    ]
    assert explicit_paths == ["/tmp/pending/raw.txt"]


def test_delete_matching_canonical_draft_lessons_preserves_active_ready(monkeypatch) -> None:
    calls: list[tuple[str, object]] = []
    lessons_by_call = {
        "draft-id": {"lesson_id": "draft-id", "status": "draft"},
        "active-id": {"lesson_id": "active-id", "status": "active"},
    }

    def fake_list_lessons(root, include_inactive=False):
        calls.append(("list", include_inactive))
        return list(lessons_by_call.values())

    def fake_active_ready(lesson):
        return lesson.get("lesson_id") == "active-id"

    def fake_delete_lesson(root, lesson_id):
        calls.append(("delete", lesson_id))
        return {"lesson_id": lesson_id}

    def fake_rebuild_index(root):
        calls.append(("rebuild", str(root)))

    monkeypatch.setattr(_draft_deletion, "list_lessons", fake_list_lessons)
    monkeypatch.setattr(_draft_deletion, "active_ready", fake_active_ready)
    monkeypatch.setattr(_draft_deletion, "delete_lesson", fake_delete_lesson)
    monkeypatch.setattr(_draft_deletion, "rebuild_index", fake_rebuild_index)

    deleted_count, skipped, failures = _draft_deletion.delete_matching_canonical_draft_lessons(
        Path("/tmp/project"),
        {"draft-id", "active-id", ""},
    )

    assert deleted_count == 1
    assert skipped == ["active-id (active-ready saved lesson preserved)"]
    assert failures == []
    assert ("delete", "draft-id") in calls
    assert ("delete", "active-id") not in calls
    assert any(item[0] == "rebuild" for item in calls)
