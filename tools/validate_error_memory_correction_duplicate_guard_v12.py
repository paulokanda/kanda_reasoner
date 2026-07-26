# project-path: tools/validate_error_memory_correction_duplicate_guard_v12.py
"""Focused validation for Error Memory correction duplicate guard v12."""
from __future__ import annotations

import ast
import importlib
import py_compile
import sys
import types
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TOUCHED = [
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_correction_guard.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "tools/validate_error_memory_correction_duplicate_guard_v12.py",
]


@dataclass(frozen=True)
class CheckResult:
    """One focused validation check result."""

    name: str
    ok: bool
    detail: str = ""


class FakeTextEdit:
    """Minimal text edit double for clear-window validation."""

    def __init__(self) -> None:
        self.text = "loaded"
        self.clear_count = 0

    def clear(self) -> None:
        self.text = ""
        self.clear_count += 1


class FakeTab:
    """Small Error Memory tab double used by the duplicate cleanup helper."""

    def __init__(self) -> None:
        self._project_root = PROJECT_ROOT
        self._loaded_pending_intake_file = "pending.json"
        self._loaded_pending_intake_lesson_id = "lesson-old"
        self._last_received_lesson = {"lesson_id": "lesson-old"}
        self._selected_lesson_id = "lesson-old"
        self.raw_error_edit = FakeTextEdit()
        self.received_preview_edit = FakeTextEdit()
        self.consume_calls = 0
        self.reload_calls = 0
        self.messages: list[tuple[str, str, str]] = []

    def _current_project_root(self) -> Path:
        return PROJECT_ROOT

    def _consume_loaded_pending_intake_file_if_matches(self, lesson, *, allow_lesson_id_change=False):
        self.consume_calls += 1
        self._loaded_pending_intake_file = ""
        self._loaded_pending_intake_lesson_id = ""
        return bool(allow_lesson_id_change and lesson.get("lesson_id"))

    def _reload_table(self) -> None:
        self.reload_calls += 1

    def _show_action_done(self, title: str, message: str, detail_text: str = "") -> None:
        self.messages.append((title, message, detail_text))

    def _refresh_heuristic_correction_button_state(self) -> None:
        return None


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def check_compile_and_ast() -> CheckResult:
    """Compile and AST-parse all touched files without broad test discovery."""
    for rel in TOUCHED:
        path = PROJECT_ROOT / rel
        if not path.exists():
            return CheckResult("compile-and-ast", False, "missing " + rel)
        if _line_count(path) > 500:
            return CheckResult("compile-and-ast", False, rel + " exceeds 500 lines")
        py_compile.compile(str(path), doraise=True)
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return CheckResult("compile-and-ast", True)


def check_static_wiring() -> CheckResult:
    """Confirm both correction entry points call the shared duplicate guard."""
    heuristic = (PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/_correction_guard.py").read_text(encoding="utf-8")
    ai_action = (PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py").read_text(encoding="utf-8")
    required_pairs = [
        (heuristic, "consume_duplicate_correction_candidate(\n        tab,\n        lesson,\n        action_label=\"Heuristic Correction\""),
        (ai_action, "consume_duplicate_correction_candidate(\n        tab,\n        dict(result.lesson_block.lesson),\n        action_label=\"Correct with AI\""),
    ]
    for text, needle in required_pairs:
        if needle not in text:
            return CheckResult("static-wiring", False, "missing duplicate guard call")
    if ai_action.find("consume_duplicate_correction_candidate") > ai_action.find("apply_corrected_lesson_to_work_windows"):
        return CheckResult("static-wiring", False, "AI action applies windows before duplicate cleanup")
    return CheckResult("static-wiring", True)


def _install_store_stub() -> None:
    """Install a tiny store stub when the extracted sandbox lacks the package."""
    package = types.ModuleType("kanda_reasoner_app.error_memory")
    package.__path__ = []
    store = types.ModuleType("kanda_reasoner_app.error_memory.store")
    store.list_lessons = lambda *args, **kwargs: []
    sys.modules.setdefault("kanda_reasoner_app.error_memory", package)
    sys.modules.setdefault("kanda_reasoner_app.error_memory.store", store)


def check_duplicate_cleanup_behavior() -> CheckResult:
    """Exercise the shared duplicate guard with a fake tab and match."""
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    _install_store_stub()
    module = importlib.import_module("kanda_reasoner_app.error_memory_gui._correction_duplicate_guard")
    match_type = importlib.import_module(
        "kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard"
    ).DuplicateLessonMatch

    original = module.find_memorize_duplicate
    try:
        module.find_memorize_duplicate = lambda root, lesson: match_type(
            lesson_id="lesson-existing",
            status="draft",
            reason="stored matching Lessons: 2",
        )
        tab = FakeTab()
        result = module.consume_duplicate_correction_candidate(
            tab,
            {"lesson_id": "lesson-new"},
            action_label="Correct with AI",
        )
        if not result:
            return CheckResult("duplicate-cleanup-behavior", False, "guard returned false")
        if tab.consume_calls != 1 or tab.reload_calls != 1:
            return CheckResult("duplicate-cleanup-behavior", False, "pending candidate was not consumed/reloaded")
        if tab.raw_error_edit.clear_count != 1 or tab.received_preview_edit.clear_count != 1:
            return CheckResult("duplicate-cleanup-behavior", False, "both work windows were not cleared")
        if not tab.messages or "Candidate deleted" not in tab.messages[0][1]:
            return CheckResult("duplicate-cleanup-behavior", False, "user message was not shown")

        module.find_memorize_duplicate = lambda root, lesson: None
        tab2 = FakeTab()
        result2 = module.consume_duplicate_correction_candidate(
            tab2,
            {"lesson_id": "lesson-new"},
            action_label="Heuristic Correction",
        )
        if result2 or tab2.consume_calls:
            return CheckResult("duplicate-cleanup-behavior", False, "non-duplicate candidate was consumed")
    finally:
        module.find_memorize_duplicate = original
    return CheckResult("duplicate-cleanup-behavior", True)


def main() -> int:
    checks = [
        check_compile_and_ast(),
        check_static_wiring(),
        check_duplicate_cleanup_behavior(),
    ]
    failures = [check for check in checks if not check.ok]
    if failures:
        for failure in failures:
            print("VALIDATION ERROR:", failure.name, failure.detail)
        return 1
    print("VALIDATION OK: error-memory-correction-duplicate-guard-v12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
