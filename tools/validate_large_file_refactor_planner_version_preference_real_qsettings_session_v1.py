# project-path: tools/validate_large_file_refactor_planner_version_preference_real_qsettings_session_v1.py
"""Validate Planner version preference through independent real QSettings sessions."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtCore import QSettings  # noqa: E402

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_version_state as state  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def main() -> None:
    original_factory = state._new_planner_version_settings
    with tempfile.TemporaryDirectory(prefix="kanda_planner_version_settings_") as temp_dir:
        ini_path = Path(temp_dir) / "planner-version-session.ini"
        state._new_planner_version_settings = lambda: QSettings(
            str(ini_path),
            QSettings.IniFormat,
        )
        try:
            first = SimpleNamespace()
            state.initialize_planner_version_state(first)
            _assert(
                state.selected_planner_version(first) == state.PLANNER_VERSION_LOCAL_AI,
                "fresh real QSettings session did not default to Local AI",
            )
            _assert(
                state.persist_planner_version_preference(
                    first,
                    state.PLANNER_VERSION_HEURISTIC,
                ),
                "first real QSettings session could not persist Heuristic",
            )
            del first

            second = SimpleNamespace()
            state.initialize_planner_version_state(second)
            _assert(
                state.selected_planner_version(second) == state.PLANNER_VERSION_HEURISTIC,
                "Heuristic did not restore from an independent real QSettings object",
            )
            print("PLANNER_VERSION_REAL_QSETTINGS_HEURISTIC_SESSION_RESTORE: PASS")

            _assert(
                state.persist_planner_version_preference(
                    second,
                    state.PLANNER_VERSION_WEB_AI,
                ),
                "second real QSettings session could not persist Web AI",
            )
            del second

            third = SimpleNamespace()
            state.initialize_planner_version_state(third)
            _assert(
                state.selected_planner_version(third) == state.PLANNER_VERSION_WEB_AI,
                "Web AI did not restore from a later independent real QSettings object",
            )
            print("PLANNER_VERSION_REAL_QSETTINGS_WEB_AI_SESSION_RESTORE: PASS")

            state.select_planner_version(third, state.PLANNER_VERSION_LOCAL_AI)
            del third
            fourth = SimpleNamespace()
            state.initialize_planner_version_state(fourth)
            _assert(
                state.selected_planner_version(fourth) == state.PLANNER_VERSION_WEB_AI,
                "internal Local AI selection overwrote persisted Web AI preference",
            )
            print("PLANNER_VERSION_REAL_QSETTINGS_INTERNAL_SELECTION_NONPERSISTING: PASS")
        finally:
            state._new_planner_version_settings = original_factory

    print("PLANNER_VERSION_REAL_QSETTINGS_SESSION: PASS")
    print(
        "VALIDATION OK: "
        "large-file-refactor-planner-version-preference-real-qsettings-session-v1"
    )
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
