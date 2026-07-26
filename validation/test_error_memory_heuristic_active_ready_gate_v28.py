"""Validate Error Memory heuristic active-ready gate patch v28."""

from __future__ import annotations

import argparse
from pathlib import Path
import py_compile

FEATURE_ID = "error-memory-heuristic-active-ready-gate-v28"
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
    py_compile.compile(str(source_path), doraise=True)
    text = read_text(source_path)

    require(
        "active_ready(dict(result.lesson or {}))" in text,
        "heuristic button state does not require active-ready result",
    )
    require(
        "it cannot make the lesson active-ready" in text,
        "draft-only heuristic guidance is missing",
    )
    require(
        "Heuristic Correction will not claim success or save this as active" in text,
        "heuristic apply path does not block draft-only overclaim",
    )
    require(
        "Deterministic correction produced an active-ready lesson" in text,
        "active-ready heuristic success message missing",
    )
    require(
        "Memorize Error saves only active-ready lessons as active" in text,
        "Memorize Error active-only guidance missing",
    )
    require(
        "self._save_draft_lesson_from_partial(\n                    lesson," not in text,
        "Memorize Error still saves draft lessons directly",
    )
    require(
        "Level 1 deterministic correction applied" not in text,
        "old overclaiming heuristic message remains",
    )
    require(
        "Saved draft Error Memory lesson from Error Editor" not in text,
        "old draft-save-through-Memorize message remains",
    )
    require(
        "The corrected lesson is still a draft. Click Memorize Error or Mark Draft" not in text,
        "old misleading heuristic draft instruction remains",
    )
    require(
        "python validation/test_error_memory_heuristic_active_ready_gate_v28.py" in read_text(project_root / "bundle_manifest.json"),
        "bundle manifest does not use forward-slash validation command",
    )

    print(EXPECTED_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
