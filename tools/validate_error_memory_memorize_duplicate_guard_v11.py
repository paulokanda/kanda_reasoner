# project-path: tools/validate_error_memory_memorize_duplicate_guard_v11.py
"""Focused validation for Error Memory duplicate guard v11."""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
import py_compile
import sys
import types
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "_memorize_duplicate_guard.py"
MARKER = "VALIDATION OK: error-memory-memorize-duplicate-guard-v11"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _install_stub_modules(stored_lessons: list[dict[str, Any]]) -> None:
    app_pkg = types.ModuleType("kanda_reasoner_app")
    app_pkg.__path__ = []
    error_memory_pkg = types.ModuleType("kanda_reasoner_app.error_memory")
    error_memory_pkg.__path__ = []
    gui_pkg = types.ModuleType("kanda_reasoner_app.error_memory_gui")
    gui_pkg.__path__ = []
    store_mod = types.ModuleType("kanda_reasoner_app.error_memory.store")

    def list_lessons(_root: str, *, include_inactive: bool = True):
        _assert(include_inactive is True, "Duplicate guard must include inactive lessons")
        return stored_lessons

    store_mod.list_lessons = list_lessons
    sys.modules["kanda_reasoner_app"] = app_pkg
    sys.modules["kanda_reasoner_app.error_memory"] = error_memory_pkg
    sys.modules["kanda_reasoner_app.error_memory_gui"] = gui_pkg
    sys.modules["kanda_reasoner_app.error_memory.store"] = store_mod


def _load_guard(stored_lessons: list[dict[str, Any]]):
    _install_stub_modules(stored_lessons)
    sys.modules.pop("guard_under_test", None)
    spec = importlib.util.spec_from_file_location("guard_under_test", GUARD_PATH)
    _assert(spec is not None and spec.loader is not None, "Could not build import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules["guard_under_test"] = module
    spec.loader.exec_module(module)
    return module


def _lesson(
    lesson_id: str,
    raw: str = "same raw error",
    phase: str = "validation",
    fingerprint_hash: str = "same-hash",
    status: str = "draft",
) -> dict[str, Any]:
    return {
        "lesson_id": lesson_id,
        "status": status,
        "operation_phase": phase,
        "raw_error_text": raw,
        "symptom": raw,
        "do_not_repeat_rule": "do not repeat " + raw,
        "fingerprint": {"fingerprint_hash": fingerprint_hash},
    }


def _validate_source_hygiene() -> None:
    _assert(GUARD_PATH.exists(), "Duplicate guard file missing")
    _assert(_line_count(GUARD_PATH) <= 500, "Duplicate guard exceeds 500 lines")
    py_compile.compile(str(GUARD_PATH), doraise=True)
    tree = ast.parse(GUARD_PATH.read_text(encoding="utf-8"))
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    _assert("find_memorize_duplicate" in names, "Missing find_memorize_duplicate")
    source = GUARD_PATH.read_text(encoding="utf-8")
    _assert("len(matches) < 2" in source, "Guard must require at least two stored matches")
    _assert("same lesson_id target" in source, "Same lesson_id must be treated as target")


def _validate_single_same_lesson_is_update_target() -> None:
    candidate = _lesson("lesson-alpha")
    module = _load_guard([_lesson("lesson-alpha", status="draft")])
    result = module.find_memorize_duplicate("E:/kanda_reasoner", candidate)
    _assert(result is None, "One same lesson_id must not be treated as duplicate")


def _validate_one_external_match_is_not_enough() -> None:
    candidate = _lesson("lesson-alpha")
    module = _load_guard([_lesson("lesson-beta")])
    result = module.find_memorize_duplicate("E:/kanda_reasoner", candidate)
    _assert(result is None, "One matching stored lesson must not trigger deletion")


def _validate_two_matches_trigger_duplicate() -> None:
    candidate = _lesson("lesson-alpha")
    stored = [
        _lesson("lesson-alpha", status="draft"),
        _lesson("lesson-beta", status="active"),
    ]
    module = _load_guard(stored)
    result = module.find_memorize_duplicate("E:/kanda_reasoner", candidate)
    _assert(result is not None, "Two stored matches must trigger duplicate guard")
    _assert(result.lesson_id == "lesson-beta", "Preferred match should not be same-id target")
    _assert("stored matching Lessons: 2" in result.reason, "Match count must be visible")


def _validate_two_text_matches_trigger_duplicate() -> None:
    candidate = _lesson("lesson-new", raw="Root cleanliness was forgotten", fingerprint_hash="new-hash")
    stored = [
        _lesson("lesson-one", raw="Root cleanliness was forgotten", fingerprint_hash="one"),
        _lesson("lesson-two", raw="Root cleanliness was forgotten", fingerprint_hash="two"),
    ]
    module = _load_guard(stored)
    result = module.find_memorize_duplicate("E:/kanda_reasoner", candidate)
    _assert(result is not None, "Two same-error text matches must trigger duplicate guard")


def main() -> int:
    _validate_source_hygiene()
    _validate_single_same_lesson_is_update_target()
    _validate_one_external_match_is_not_enough()
    _validate_two_matches_trigger_duplicate()
    _validate_two_text_matches_trigger_duplicate()
    print(MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
