# project-path: tools/validate_planner_preference_workbench_aqr_box_shield_v1.py
"""Validate Planner preference persistence cannot mutate Workbench AQR ownership."""
from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace

__all__ = [
    "main",
]

FEATURE_ID = "planner-preference-workbench-aqr-box-shield-repair-v1"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import planner_version_state as state  # noqa: E402
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_context import (  # noqa: E402
    stage_correction_needed,
)


class Output:
    """Minimal read-only text output."""

    def __init__(self, text: str) -> None:
        self._text = text

    def toPlainText(self) -> str:
        return self._text


class SettingsEndpoint:
    """Independent settings endpoint backed by one durable mapping."""

    def __init__(self, backing: dict[str, str]) -> None:
        self._backing = backing
        self.sync_count = 0

    def value(self, key: str, default=None):
        return self._backing.get(key, default)

    def setValue(self, key: str, value: str) -> None:
        self._backing[key] = value

    def sync(self) -> None:
        self.sync_count += 1


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _window() -> SimpleNamespace:
    return SimpleNamespace(
        _large_file_refactor_workbench_advanced_quality_review=None,
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="ruff failed",
        _large_file_refactor_workbench_aqr_stage_states={"RUFF": "FAILED"},
        _large_file_refactor_workbench_aqr_output=Output("AQR failed"),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
    )


def _workbench_state(window: object) -> dict[str, object]:
    return {
        name: value
        for name, value in vars(window).items()
        if name.startswith("_large_file_refactor_workbench_")
    }


def main() -> int:
    backing: dict[str, str] = {}
    original_factory = state._new_planner_version_settings
    state._new_planner_version_settings = lambda: SettingsEndpoint(backing)
    try:
        first = _window()
        require(
            stage_correction_needed(first, "ADVANCED_QUALITY_REVIEW", "E:/project"),
            "AQR_TERMINAL_FAILURE_CORRECTABLE_BEFORE_PLANNER_PREFERENCE_WRITE",
        )
        workbench_before = _workbench_state(first)
        session_before = first._large_file_refactor_workbench_aqr_correction_session

        state.initialize_planner_version_state(first)
        require(
            state.persist_planner_version_preference(first, state.PLANNER_VERSION_HEURISTIC),
            "PLANNER_PREFERENCE_WRITE_SUCCEEDS_WITH_ISOLATED_ENDPOINT",
        )
        state.initialize_planner_version_state(first)
        require(
            state.selected_planner_version(first) == state.PLANNER_VERSION_HEURISTIC,
            "PLANNER_PREFERENCE_RESTORES_WITHOUT_WORKBENCH_READ",
        )
        require(
            not hasattr(first, "_large_file_refactor_version_settings"),
            "PLANNER_QSETTINGS_NOT_CACHED_ON_SHARED_ARCHITECTURE_WINDOW",
        )

        for name, value in workbench_before.items():
            require(
                getattr(first, name) is value,
                "WORKBENCH_STATE_IDENTITY_PRESERVED_" + name.removeprefix("_large_file_refactor_workbench_").upper(),
            )
        require(
            first._large_file_refactor_workbench_aqr_correction_session is session_before,
            "AQR_CORRECTION_SESSION_IDENTITY_PRESERVED_BY_PLANNER_PREFERENCE",
        )
        require(
            stage_correction_needed(first, "ADVANCED_QUALITY_REVIEW", "E:/project"),
            "AQR_CORRECTION_ROUTE_REMAINS_AVAILABLE_AFTER_PLANNER_PREFERENCE_WRITE",
        )

        second = SimpleNamespace()
        state.initialize_planner_version_state(second)
        require(
            state.selected_planner_version(second) == state.PLANNER_VERSION_HEURISTIC,
            "PLANNER_PREFERENCE_RESTORES_IN_INDEPENDENT_SESSION",
        )
        require(
            not any(name.startswith("_large_file_refactor_workbench_") for name in vars(second)),
            "PLANNER_SESSION_RESTORE_CREATES_NO_WORKBENCH_STATE",
        )
    finally:
        state._new_planner_version_settings = original_factory

    source = (ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_state.py").read_text(encoding="utf-8")
    require(
        "_PLANNER_VERSION_SETTINGS_ATTR" not in source
        and "setattr(window, _PLANNER_VERSION_SETTINGS_ATTR" not in source,
        "NO_HIDDEN_MUTABLE_SETTINGS_CACHE_ON_SHARED_WINDOW",
    )
    print("PLANNER_PREFERENCE_WORKBENCH_AQR_BOX_SHIELD: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
