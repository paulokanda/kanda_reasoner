# project-path: tools/validate_large_file_refactor_planner_version_preference_real_session_owner_repair_v1.py
"""Validate real-session Planner version preference ownership and persistence."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_version_state as state  # noqa: E402

BOX = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)
ARCHITECTURE_WINDOW = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "manage_architecture_gui.py"
)


class SessionSettings:
    """Independent settings objects backed by one process-persistent namespace."""

    stores: dict[tuple[str, str], dict[str, str]] = {}
    sync_calls = 0

    def __init__(self, organization: str, application: str) -> None:
        self.namespace = (organization, application)
        self.values = self.stores.setdefault(self.namespace, {})

    def value(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)

    def setValue(self, key: str, value: str) -> None:
        self.values[key] = value

    def sync(self) -> None:
        type(self).sync_calls += 1


class ExplicitSettings:
    """Window-owned settings double used to prove explicit owner precedence."""

    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.sync_calls = 0

    def value(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)

    def setValue(self, key: str, value: str) -> None:
        self.values[key] = value

    def sync(self) -> None:
        self.sync_calls += 1


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def _static_contract() -> None:
    text = (BOX / "planner_version_state.py").read_text(encoding="utf-8")
    architecture_text = ARCHITECTURE_WINDOW.read_text(encoding="utf-8")

    _assert(
        "_planner_version_settings_owner(window)" in text,
        "Planner preference does not resolve a real settings owner",
    )
    _assert(
        'PLANNER_VERSION_SETTINGS_ORGANIZATION = "Kanda"' in text,
        "shared settings organization is missing",
    )
    _assert(
        'PLANNER_VERSION_SETTINGS_APPLICATION = "ProjectReasonerV10"' in text,
        "shared settings application is missing",
    )
    _assert(
        "settings = _new_planner_version_settings()" in text,
        "Planner has no fallback QSettings owner for ArchitectureManagerWindow",
    )
    _assert(
        "sync = getattr(settings, \"sync\", None)" in text,
        "persist path does not synchronize QSettings",
    )
    _assert(
        "self.settings =" not in architecture_text,
        "production ArchitectureManagerWindow unexpectedly owns self.settings; validator assumptions require review",
    )
    print("PLANNER_VERSION_PRODUCTION_WINDOW_MISSING_GENERIC_SETTINGS_REPRODUCED: PASS")
    print("PLANNER_VERSION_REAL_SETTINGS_OWNER_FALLBACK_PRESENT: PASS")
    print("PLANNER_VERSION_QSETTINGS_NAMESPACE_STABLE: PASS")
    print("PLANNER_VERSION_PERSIST_SYNC_PRESENT: PASS")


def _session_contract() -> None:
    original_factory = state._new_planner_version_settings
    SessionSettings.stores.clear()
    SessionSettings.sync_calls = 0
    state._new_planner_version_settings = lambda: SessionSettings(
        state.PLANNER_VERSION_SETTINGS_ORGANIZATION,
        state.PLANNER_VERSION_SETTINGS_APPLICATION,
    )
    try:
        first_window = SimpleNamespace()
        state.initialize_planner_version_state(first_window)
        _assert(
            state.selected_planner_version(first_window) == state.PLANNER_VERSION_LOCAL_AI,
            "missing preference did not default to Local AI",
        )
        _assert(
            state.persist_planner_version_preference(
                first_window,
                state.PLANNER_VERSION_HEURISTIC,
            ),
            "window without settings could not persist Heuristic preference",
        )
        _assert(SessionSettings.sync_calls == 1, "persist did not sync settings")

        second_window = SimpleNamespace()
        state.initialize_planner_version_state(second_window)
        _assert(
            state.selected_planner_version(second_window) == state.PLANNER_VERSION_HEURISTIC,
            "Heuristic preference did not survive an independent window session",
        )

        _assert(
            state.persist_planner_version_preference(
                second_window,
                state.PLANNER_VERSION_WEB_AI,
            ),
            "second session could not persist Web AI preference",
        )
        third_window = SimpleNamespace()
        state.initialize_planner_version_state(third_window)
        _assert(
            state.selected_planner_version(third_window) == state.PLANNER_VERSION_WEB_AI,
            "Web AI preference did not survive a second independent session boundary",
        )
        print("PLANNER_VERSION_HEURISTIC_PERSISTS_ACROSS_INDEPENDENT_SESSIONS: PASS")
        print("PLANNER_VERSION_WEB_AI_PERSISTS_ACROSS_INDEPENDENT_SESSIONS: PASS")
        print("PLANNER_VERSION_REAL_SESSION_OWNER_SYNCED: PASS")

        state.select_planner_version(third_window, state.PLANNER_VERSION_LOCAL_AI)
        fourth_window = SimpleNamespace()
        state.initialize_planner_version_state(fourth_window)
        _assert(
            state.selected_planner_version(fourth_window) == state.PLANNER_VERSION_WEB_AI,
            "internal selection change overwrote the persisted user preference",
        )
        print("PLANNER_VERSION_INTERNAL_SELECTION_STILL_DOES_NOT_OVERWRITE_PREFERENCE: PASS")

        namespace = (
            state.PLANNER_VERSION_SETTINGS_ORGANIZATION,
            state.PLANNER_VERSION_SETTINGS_APPLICATION,
        )
        SessionSettings.stores[namespace][state.PLANNER_VERSION_PREFERENCE_KEY] = "obsolete-label"
        invalid_window = SimpleNamespace()
        state.initialize_planner_version_state(invalid_window)
        _assert(
            state.selected_planner_version(invalid_window) == state.PLANNER_VERSION_LOCAL_AI,
            "invalid stored value did not fail safely to Local AI",
        )
        print("PLANNER_VERSION_INVALID_REAL_SESSION_VALUE_FALLS_BACK_LOCAL_AI: PASS")
    finally:
        state._new_planner_version_settings = original_factory


def _explicit_owner_contract() -> None:
    explicit = ExplicitSettings()
    window = SimpleNamespace(settings=explicit)
    state.initialize_planner_version_state(window)
    _assert(
        state.persist_planner_version_preference(window, state.PLANNER_VERSION_HEURISTIC),
        "explicit window settings owner could not persist preference",
    )
    _assert(
        explicit.values.get(state.PLANNER_VERSION_PREFERENCE_KEY)
        == state.PLANNER_VERSION_HEURISTIC,
        "explicit settings owner did not receive preference",
    )
    _assert(explicit.sync_calls == 1, "explicit settings owner was not synced")
    print("PLANNER_VERSION_EXPLICIT_WINDOW_SETTINGS_OWNER_PRESERVED: PASS")


def _size_and_encoding_contract() -> None:
    touched = (
        BOX / "planner_version_state.py",
        PROJECT_ROOT
        / "tools"
        / "validate_large_file_refactor_planner_version_preference_real_session_owner_repair_v1.py",
    )
    for path in touched:
        raw = path.read_bytes()
        _assert(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM found: {path}")
        raw.decode("ascii")
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        _assert(line_count <= 500, f"module exceeds 500 physical lines: {path}")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_MODULES_MAX_500_LINES: PASS")


def main() -> None:
    _static_contract()
    _session_contract()
    _explicit_owner_contract()
    _size_and_encoding_contract()
    print("PLANNER_VERSION_PREFERENCE_REAL_SESSION_OWNER_REPAIR: PASS")
    print(
        "VALIDATION OK: "
        "large-file-refactor-planner-version-preference-real-session-owner-repair-v1"
    )
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
