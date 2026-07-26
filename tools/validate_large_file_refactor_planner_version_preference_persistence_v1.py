# project-path: tools/validate_large_file_refactor_planner_version_preference_persistence_v1.py
"""Validate persisted Planner version selection and safe restoration semantics."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_PREFERENCE_KEY,
    PLANNER_VERSION_WEB_AI,
    initialize_planner_version_state,
    persist_planner_version_preference,
    select_planner_version,
    selected_planner_version,
    stored_planner_version_preference,
)

BOX = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"


class FakeSettings:
    """Minimal QSettings-compatible test double."""

    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self.values = dict(initial or {})

    def value(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)

    def setValue(self, key: str, value: str) -> None:
        self.values[key] = value


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def _static_contract() -> None:
    state_text = (BOX / "planner_version_state.py").read_text(encoding="utf-8")
    selector_text = (BOX / "planner_version_selector_gui.py").read_text(encoding="utf-8")

    _assert(
        'PLANNER_VERSION_PREFERENCE_KEY = "large_file_refactor_planner/selected_version"'
        in state_text,
        "stable preference key missing",
    )
    _assert(
        "stored_planner_version_preference(window)" in state_text,
        "Planner initialization does not hydrate persisted version selection",
    )
    _assert(
        "persist_planner_version_preference(window, version_name)" in selector_text,
        "explicit selector changes are not persisted by the GUI adapter",
    )
    _assert(
        "selected = selected_planner_version(window)" in selector_text,
        "selector does not hydrate checked state from Planner state owner",
    )
    _assert(
        "radios[selected].setChecked(True)" in selector_text,
        "selector does not restore non-default saved selections",
    )
    print("PLANNER_VERSION_PREFERENCE_SINGLE_STATE_OWNER: PASS")
    print("PLANNER_VERSION_SELECTOR_HYDRATES_FROM_STABLE_ID: PASS")


def _runtime_contract() -> None:
    settings = FakeSettings({PLANNER_VERSION_PREFERENCE_KEY: PLANNER_VERSION_HEURISTIC})
    first_window = SimpleNamespace(settings=settings)
    initialize_planner_version_state(first_window)
    _assert(
        selected_planner_version(first_window) == PLANNER_VERSION_HEURISTIC,
        "saved Heuristic selection was not restored",
    )
    print("PLANNER_VERSION_RESTORES_HEURISTIC_SELECTION: PASS")

    select_planner_version(first_window, PLANNER_VERSION_WEB_AI)
    _assert(
        settings.values.get(PLANNER_VERSION_PREFERENCE_KEY) == PLANNER_VERSION_HEURISTIC,
        "internal selection unexpectedly overwrote user preference",
    )
    persist_planner_version_preference(first_window, PLANNER_VERSION_WEB_AI)
    _assert(
        settings.values.get(PLANNER_VERSION_PREFERENCE_KEY) == PLANNER_VERSION_WEB_AI,
        "Web AI selection was not persisted as stable ID",
    )
    second_window = SimpleNamespace(settings=settings)
    initialize_planner_version_state(second_window)
    _assert(
        selected_planner_version(second_window) == PLANNER_VERSION_WEB_AI,
        "persisted Web AI selection did not survive Planner rebuild",
    )
    print("PLANNER_VERSION_INTERNAL_SELECTION_DOES_NOT_OVERWRITE_PREFERENCE: PASS")
    print("PLANNER_VERSION_SELECTION_PERSISTS_ACROSS_REBUILD: PASS")

    empty_window = SimpleNamespace(settings=FakeSettings())
    initialize_planner_version_state(empty_window)
    _assert(
        selected_planner_version(empty_window) == PLANNER_VERSION_LOCAL_AI,
        "missing preference did not fall back to Local AI",
    )

    invalid_settings = FakeSettings({PLANNER_VERSION_PREFERENCE_KEY: "Old Display Label"})
    invalid_window = SimpleNamespace(settings=invalid_settings)
    initialize_planner_version_state(invalid_window)
    _assert(
        stored_planner_version_preference(invalid_window) == PLANNER_VERSION_LOCAL_AI,
        "invalid saved preference did not fail safely to Local AI",
    )
    _assert(
        selected_planner_version(invalid_window) == PLANNER_VERSION_LOCAL_AI,
        "invalid saved preference contaminated active selection",
    )
    print("PLANNER_VERSION_MISSING_OR_INVALID_FALLBACK_LOCAL_AI: PASS")


def _size_and_encoding_contract() -> None:
    touched = (
        BOX / "planner_version_state.py",
        BOX / "planner_version_selector_gui.py",
        PROJECT_ROOT / "tools" / "validate_large_file_refactor_planner_version_preference_persistence_v1.py",
    )
    for path in touched:
        raw = path.read_bytes()
        _assert(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM found: {path}")
        raw.decode("ascii")
        lines = path.read_text(encoding="utf-8").splitlines()
        _assert(len(lines) <= 500, f"module exceeds 500 physical lines: {path}")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")


def main() -> None:
    _static_contract()
    _runtime_contract()
    _size_and_encoding_contract()
    print("PLANNER_VERSION_PREFERENCE_PERSISTENCE: PASS")
    print("VALIDATION OK: large-file-refactor-planner-version-preference-persistence-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
