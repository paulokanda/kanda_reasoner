# project-path: tools/validate_engineering_diagnostics_history_qthread_real_qt_v2.py
"""Real Qt heartbeat validator for Engineering Diagnostics history loading."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import time


FEATURE_ID = (
    "kanda-reasoner-engineering-diagnostics-history-qthread-freeze-repair-v2"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _view(run_id: str) -> object:
    comparison = SimpleNamespace(
        status="NO_BASELINE",
        new_issue_fingerprints=(),
        persistent_issue_fingerprints=(),
        resolved_issue_fingerprints=(),
    )
    run = SimpleNamespace(
        run_id=run_id,
        finding_count=0,
    )
    return SimpleNamespace(
        run=run,
        findings=(),
        comparison=comparison,
        groups=(),
        grouping_generation=0,
        lifecycle=None,
    )


def validate(project_root: Path) -> None:
    """Exercise the real panel while a deliberately slow run view loads."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    from PySide6.QtCore import QEventLoop, QThread, QTimer
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.engineering_diagnostics_gui.engineering_diagnostics_tab import (
        create_engineering_diagnostics_panel,
    )

    app = QApplication.instance() or QApplication([])
    gui_thread = app.thread()

    class SlowController:
        def __init__(self) -> None:
            self.calls: list[str] = []
            self.gui_thread_calls: list[bool] = []

        def load_run_view(self, _project_root: str, run_id: str) -> object:
            self.calls.append(str(run_id))
            self.gui_thread_calls.append(QThread.currentThread() is gui_thread)
            if str(run_id) == "run-old":
                time.sleep(0.65)
            else:
                time.sleep(0.15)
            return _view(str(run_id))

    controller = SlowController()
    beats = {"count": 0}

    with tempfile.TemporaryDirectory(prefix="kanda_diag_qthread_") as temp_dir:
        panel = create_engineering_diagnostics_panel(
            project_root_provider=lambda: temp_dir,
            controller=controller,
            defer_initial_refresh=True,
        )
        panel.show()
        app.processEvents()

        actions = panel.engineering_diagnostics_history_actions
        heartbeat = QTimer()
        heartbeat.setInterval(25)
        heartbeat.timeout.connect(
            lambda: beats.__setitem__("count", beats["count"] + 1)
        )
        heartbeat.start()

        try:
            started = time.monotonic()
            actions.render_run("run-old")
            launch_elapsed = time.monotonic() - started
            _require(
                launch_elapsed < 0.30,
                "HISTORY_RENDER_BLOCKED_GUI:" + f"{launch_elapsed:.3f}",
            )

            QTimer.singleShot(
                80,
                lambda: actions.render_run("run-new"),
            )
            loop = QEventLoop()
            QTimer.singleShot(1600, loop.quit)
            loop.exec()

            _require(
                beats["count"] >= 20,
                "GUI_HEARTBEAT_STARVED:" + str(beats["count"]),
            )
            _require(
                controller.calls == ["run-old", "run-new"],
                "SERIAL_WORKER_CALL_ORDER_INVALID:" + repr(controller.calls),
            )
            _require(
                not any(controller.gui_thread_calls),
                "RUN_VIEW_EXECUTED_ON_GUI_THREAD",
            )
            status = panel.engineering_diagnostics_status_label.text()
            _require(
                status == "History loaded: run-new",
                "STALE_RESULT_REJECTION_FAILED:" + status,
            )
        finally:
            heartbeat.stop()
            actions.close()
            settle = QEventLoop()
            QTimer.singleShot(100, settle.quit)
            settle.exec()
            panel.close()
            app.processEvents()

    print("ENGINEERING_DIAGNOSTICS_HISTORY_EVENT_LOOP_RESPONSIVE: PASS")
    print("ENGINEERING_DIAGNOSTICS_RUN_VIEW_WORKER_THREAD: PASS")
    print("ENGINEERING_DIAGNOSTICS_HISTORY_SERIAL_RUNTIME: PASS")
    print("ENGINEERING_DIAGNOSTICS_HISTORY_STALE_RESULT_RUNTIME_REJECTION: PASS")
    print("ENGINEERING_DIAGNOSTICS_HISTORY_GUI_APPLY_THREAD: PASS")
    print("REAL_QT_WIDGET_HEARTBEAT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    validate(project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
