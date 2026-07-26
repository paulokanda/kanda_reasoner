"""Validate live Error Memory pending-intake refresh without launching Qt."""

from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path

from kanda_reasoner_app.error_memory_gui._pending_live_refresh import (
    initialize_pending_intake_live_refresh,
    refresh_pending_intake_live,
)
from kanda_reasoner_app.error_memory_gui._text_payloads import (
    lesson_id_from_text_lenient,
)

FEATURE_ID = "error-memory-gui-pending-intake-live-refresh-v1"
BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
END = "KANDA_ERROR_LESSON_JSON_END"


class FakeEditor:
    """Minimal plain-text editor double."""

    def __init__(self) -> None:
        self.text = ""

    def toPlainText(self) -> str:
        return self.text


class FakeTab:
    """Minimal host double for the live refresh bridge."""

    def __init__(self, pending_dir: Path) -> None:
        self.pending_dir = pending_dir
        self._pending_live_refresh_snapshot = None
        self._dismissed_pending_intake_files: set[str] = set()
        self._dismissed_pending_intake_lesson_ids: set[str] = set()
        self._loaded_pending_intake_file = ""
        self.raw_error_edit = FakeEditor()
        self.received_preview_edit = FakeEditor()
        self.reload_count = 0
        self.load_count = 0

    def _pending_intake_files_for_all_candidate_dirs(self) -> list[Path]:
        return sorted(path for path in self.pending_dir.iterdir() if path.is_file())

    def _lesson_id_from_text_lenient(self, text: str) -> str:
        return lesson_id_from_text_lenient(text)

    def _reload_table(self) -> None:
        self.reload_count += 1

    def load_pending_ai_assisted_error_lesson_intake_now(self) -> bool:
        self.load_count += 1
        return True


def _lesson_text(lesson_id: str, symptom: str) -> str:
    payload = {
        "schema_version": "1.0",
        "project_slug": "sample_project",
        "lesson_id": lesson_id,
        "status": "active",
        "symptom": symptom,
        "do_not_repeat_rule": "Refresh live pending intake without restart.",
    }
    return BEGIN + "\n" + json.dumps(payload, indent=2) + "\n" + END + "\n"


def test_new_pending_file_triggers_existing_loader() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        pending_dir = Path(temp_dir)
        tab = FakeTab(pending_dir)
        initialize_pending_intake_live_refresh(tab)

        if refresh_pending_intake_live(tab):
            raise AssertionError("Unchanged empty intake must not trigger refresh.")

        lesson_path = pending_dir / "KANDA_ERROR_LESSON_JSON_live_refresh_v1.txt"
        lesson_path.write_text(
            _lesson_text("lesson-live-refresh-v1", "first"),
            encoding="utf-8",
        )

        if not refresh_pending_intake_live(tab):
            raise AssertionError("New pending lesson did not invoke the trusted loader.")
        if tab.reload_count != 1 or tab.load_count != 1:
            raise AssertionError("Live refresh did not reload table and loader exactly once.")

        if refresh_pending_intake_live(tab):
            raise AssertionError("Stable snapshot must not repeatedly reload the same intake.")
        if tab.reload_count != 1 or tab.load_count != 1:
            raise AssertionError("Stable snapshot caused repeated refresh work.")


def test_changed_pending_file_clears_only_stale_dismissal() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        pending_dir = Path(temp_dir)
        tab = FakeTab(pending_dir)
        lesson_id = "lesson-live-refresh-revised-v1"
        lesson_path = pending_dir / "KANDA_ERROR_LESSON_JSON_live_refresh_revised_v1.txt"
        lesson_path.write_text(_lesson_text(lesson_id, "before"), encoding="utf-8")
        initialize_pending_intake_live_refresh(tab)

        marker = str(lesson_path.resolve(strict=False))
        tab._dismissed_pending_intake_files.add(marker)
        tab._dismissed_pending_intake_lesson_ids.add(lesson_id)
        tab._dismissed_pending_intake_lesson_ids.add("unrelated-lesson")

        time.sleep(0.01)
        lesson_path.write_text(_lesson_text(lesson_id, "after changed payload"), encoding="utf-8")

        if not refresh_pending_intake_live(tab):
            raise AssertionError("Changed pending lesson did not invoke live refresh.")
        if marker in tab._dismissed_pending_intake_files:
            raise AssertionError("Changed file remained blocked by stale dismissed-path state.")
        if lesson_id in tab._dismissed_pending_intake_lesson_ids:
            raise AssertionError("Changed lesson remained blocked by stale dismissed-id state.")
        if "unrelated-lesson" not in tab._dismissed_pending_intake_lesson_ids:
            raise AssertionError("Live refresh cleared unrelated dismissed lesson state.")



def test_busy_work_windows_defer_without_losing_new_intake() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        pending_dir = Path(temp_dir)
        tab = FakeTab(pending_dir)
        initialize_pending_intake_live_refresh(tab)
        tab.raw_error_edit.text = "user is reviewing another error"

        lesson_path = pending_dir / "KANDA_ERROR_LESSON_JSON_live_refresh_deferred_v1.txt"
        lesson_path.write_text(
            _lesson_text("lesson-live-refresh-deferred-v1", "deferred"),
            encoding="utf-8",
        )

        if refresh_pending_intake_live(tab):
            raise AssertionError("Live refresh overwrote a busy work window.")
        if tab.load_count != 0:
            raise AssertionError("Trusted loader ran while work windows were busy.")
        if tab.reload_count != 1:
            raise AssertionError("Pending table did not refresh for deferred intake.")

        tab.raw_error_edit.text = ""
        if not refresh_pending_intake_live(tab):
            raise AssertionError("Deferred pending intake did not load after window cleared.")
        if tab.load_count != 1:
            raise AssertionError("Deferred intake loader count is incorrect.")

def test_gui_source_starts_box_local_live_refresh_timer() -> None:
    project_root = Path(__file__).resolve().parents[1]
    source = (
        project_root
        / "kanda_reasoner_app"
        / "error_memory_gui"
        / "error_memory_tab.py"
    ).read_text(encoding="utf-8")

    required = [
        "initialize_pending_intake_live_refresh(self)",
        "self._pending_intake_live_refresh_timer = QTimer(self)",
        "self._pending_intake_live_refresh_timer.setInterval(500)",
        "self._pending_intake_live_refresh_timer.timeout.connect(self._refresh_pending_intake_live)",
        "return refresh_pending_intake_live(self)",
    ]
    for fragment in required:
        if fragment not in source:
            raise AssertionError("Missing live refresh GUI integration marker: " + fragment)

    if len(source.splitlines()) > 500:
        raise AssertionError("error_memory_tab.py exceeds the 500-line hard limit.")


def main() -> int:
    test_new_pending_file_triggers_existing_loader()
    test_changed_pending_file_clears_only_stale_dismissal()
    test_busy_work_windows_defer_without_losing_new_intake()
    test_gui_source_starts_box_local_live_refresh_timer()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ERROR_MEMORY_LIVE_REFRESH: pending file create/change auto-load path ready")
    print("ERROR_MEMORY_HUMAN_GATE: Memorize Error remains the only canonical save action")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
