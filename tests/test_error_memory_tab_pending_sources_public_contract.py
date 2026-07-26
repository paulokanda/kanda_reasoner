"""Static and behavioral contracts for Error Memory pending source helpers."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.error_memory_gui._pending_sources import (
    candidate_pending_ai_assisted_intake_dirs,
    delete_matching_pending_intake_files,
    pending_file_matches_draft_identity,
    pending_intake_files_for_candidate_dirs,
    safe_pending_lesson_id_from_file,
)


def test_safe_pending_lesson_id_from_file_normalizes_name() -> None:
    lesson_id = safe_pending_lesson_id_from_file(Path("RAW_ERROR_EVIDENCE_My Bad File!!.txt"))
    assert lesson_id == "lesson-pending-my-bad-file"


def test_pending_intake_files_deduplicates_and_filters_suffixes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        keep = folder / "lesson.json"
        skip = folder / "ignore.bin"
        keep.write_text("{}", encoding="utf-8")
        skip.write_text("x", encoding="utf-8")
        files = pending_intake_files_for_candidate_dirs([folder, folder], allowed_suffixes={".json", ".txt"})
        assert files == [keep]


def test_pending_file_identity_matches_explicit_path_and_lesson_id() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        pending = folder / "draft.json"
        pending.write_text('{"lesson_id": "lesson-x"}', encoding="utf-8")
        assert pending_file_matches_draft_identity(pending, {"lesson-x"}, [], []) is True
        assert pending_file_matches_draft_identity(pending, set(), [], [str(pending)]) is True


def test_delete_matching_pending_files_returns_dismissed_markers() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        pending = folder / "draft.json"
        pending.write_text('{"lesson_id": "lesson-delete-me"}', encoding="utf-8")
        deleted, failures, dismissed = delete_matching_pending_intake_files(
            {"lesson-delete-me"},
            [],
            [],
            [pending],
        )
        assert deleted == 1
        assert failures == []
        assert str(pending.resolve(strict=False)) in dismissed
        assert not pending.exists()


def test_candidate_pending_dirs_keeps_order_without_duplicates() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        dirs = candidate_pending_ai_assisted_intake_dirs([root, root], pending_dir_name="pending_ai_assisted_error_lesson_intake")
        normalized = [str(item) for item in dirs]
        assert len(normalized) == len(set(item.casefold() for item in normalized))


if __name__ == "__main__":
    test_safe_pending_lesson_id_from_file_normalizes_name()
    test_pending_intake_files_deduplicates_and_filters_suffixes()
    test_pending_file_identity_matches_explicit_path_and_lesson_id()
    test_delete_matching_pending_files_returns_dismissed_markers()
    test_candidate_pending_dirs_keeps_order_without_duplicates()
