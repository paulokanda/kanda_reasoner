"""Validate Error Memory state-machine guidance patch v27."""

from __future__ import annotations

import argparse
from pathlib import Path

FEATURE_ID = "error-memory-state-machine-guidance-v27"
EXPECTED_MARKER = "VALIDATION OK: " + FEATURE_ID


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read UTF-8 text with replacement for robust validation."""
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    source_path = project_root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    require(source_path.exists(), "error_memory_tab.py not found")
    text = read_text(source_path)

    require("def _active_ready_missing_text" in text, "missing active-ready missing-field helper")
    require("def _lesson_id_exists_in_lessons" in text, "missing Lessons-store lesson_id lookup helper")
    require("def _delete_pending_file_quietly" in text, "missing quiet pending file deletion helper")
    require("self._lesson_id_exists_in_lessons(lesson_id)" in text, "pending loader does not skip already-saved lesson_id")
    require("self._delete_pending_file_quietly(candidate)" in text, "pending loader does not delete skipped duplicate pending file")
    require("Draft normalization was applied, but this is not an active correction." in text, "heuristic correction still overclaims active correction")
    require("lesson[\"promotion_status\"] = \"needs_ai_review\"" in text, "heuristic correction does not mark needs_ai_review")
    require("payload[\"promotion_status\"] = \"needs_ai_review\"" in text, "draft canonicalization does not mark needs_ai_review")
    require("Memorize Error saves only active-ready lessons as active." in text, "Memorize Error draft branch is not active-only")
    require("Use Mark Draft to preserve this draft in Lessons" in text, "draft user guidance missing Mark Draft route")
    require("self._save_draft_lesson_from_partial(\n                    lesson," not in text, "Memorize Error still saves draft lessons directly")
    require("Saved as draft and consumed the matching pending intake source when present." in text, "Mark Draft message does not confirm pending consumption")
    require("Missing active-ready items:" in text, "missing active-ready detail reporting")
    require("Click Memorize Error or Mark Draft to save it as a draft" not in text, "old overpromising heuristic message remains")
    require("Memorize Error saves active lessons as active and saves draft lessons" not in text, "old Memorize tooltip remains")

    print(EXPECTED_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
