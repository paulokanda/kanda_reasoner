# project-path: tools/validate_large_file_refactor_planner_version_preference_real_widget_v1.py
"""Real PySide validation for persisted Planner version radio selection."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit  # noqa: E402

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_selector_gui import (  # noqa: E402
    build_planner_version_selector,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (  # noqa: E402
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_PREFERENCE_KEY,
    PLANNER_VERSION_WEB_AI,
    initialize_planner_version_state,
)


class FakeSettings:
    """Minimal settings store compatible with the Planner preference adapter."""

    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self.values = dict(initial or {})

    def value(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)

    def setValue(self, key: str, value: str) -> None:
        self.values[key] = value


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def _build(settings: FakeSettings) -> tuple[object, object]:
    window = SimpleNamespace(
        settings=settings,
        _large_file_refactor_plan_output=QPlainTextEdit(),
    )
    initialize_planner_version_state(window)
    widget = build_planner_version_selector(window, refresh_callback=lambda _window: None)
    return window, widget


def main() -> None:
    app = QApplication.instance() or QApplication([])
    _assert(app is not None, "QApplication could not start")

    settings = FakeSettings({PLANNER_VERSION_PREFERENCE_KEY: PLANNER_VERSION_HEURISTIC})
    window, widget = _build(settings)
    radios = window._large_file_refactor_version_radios
    _assert(radios[PLANNER_VERSION_HEURISTIC].isChecked(), "saved Heuristic radio not restored")
    print("PLANNER_VERSION_REAL_WIDGET_RESTORES_HEURISTIC: PASS")

    radios[PLANNER_VERSION_WEB_AI].click()
    app.processEvents()
    _assert(
        settings.values.get(PLANNER_VERSION_PREFERENCE_KEY) == PLANNER_VERSION_WEB_AI,
        "Web AI radio click did not persist stable ID",
    )
    widget.close()

    rebuilt, rebuilt_widget = _build(settings)
    rebuilt_radios = rebuilt._large_file_refactor_version_radios
    _assert(rebuilt_radios[PLANNER_VERSION_WEB_AI].isChecked(), "Web AI radio not restored")
    _assert(not rebuilt_radios[PLANNER_VERSION_LOCAL_AI].isChecked(), "Local AI incorrectly reset restored selection")
    print("PLANNER_VERSION_REAL_WIDGET_SELECTION_SURVIVES_REBUILD: PASS")

    rebuilt_widget.close()
    print("PLANNER_VERSION_PREFERENCE_REAL_WIDGET: PASS")
    print("VALIDATION OK: large-file-refactor-planner-version-preference-real-widget-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
