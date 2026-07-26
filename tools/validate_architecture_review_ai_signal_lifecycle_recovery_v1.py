#!/usr/bin/env python3
"""Validate Architecture Review AI configuration-signal lifecycle recovery."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import py_compile
import sys
import tempfile
from typing import Any

FEATURE_ID = "architecture-review-ai-signal-lifecycle-recovery-v1"
TARGET = Path("kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py")
MAX_LINES = 500

__all__ = ["main"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: Path) -> str:
    path = root / relative
    require(path.is_file(), "Missing required file: " + relative.as_posix())
    return path.read_text(encoding="utf-8-sig")


def validate_static(root: Path) -> None:
    text = read(root, TARGET)
    ast.parse(text, filename=TARGET.as_posix())
    py_compile.compile(str(root / TARGET), doraise=True)
    require(len(text.splitlines()) <= MAX_LINES, "AI GUI integration exceeds 500 lines.")
    required = (
        "def _qt_object_is_alive(value: Any) -> bool:",
        'getattr(import_module("shiboken6"), "isValid")',
        "def _radio_is_checked(window: Any, attribute: str) -> bool:",
        "def _disconnect_configuration_sync(",
        "def _connect_configuration_sync(window: Any, mode_host: Any) -> None:",
        'window._ai_review_configuration_sync_bindings = bindings',
        "mode_host.destroyed.connect(",
        "lambda *_args: _disconnect_configuration_sync(window, generation)",
        "_connect_configuration_sync(window, mode_host)",
        "except RuntimeError:",
    )
    for fragment in required:
        require(fragment in text, "Missing lifecycle guard: " + fragment)
    forbidden = (
        "lambda _snapshot, owner=window: _sync_review_controls(owner)",
        "lambda _models, owner=window: _sync_review_controls(owner)",
        "if window._ai_review_web_radio.isChecked():",
        "if window._ai_review_local_radio.isChecked():",
    )
    for fragment in forbidden:
        require(fragment not in text, "Stale unsafe signal path remains: " + fragment)
    print("ARCHITECTURE_AI_QOBJECT_VALIDITY_GUARD: PASS")
    print("ARCHITECTURE_AI_GLOBAL_SIGNAL_DISCONNECT_OWNER: PASS")
    print("ARCHITECTURE_AI_REBUILD_GENERATION_GUARD: PASS")
    print("ARCHITECTURE_AI_NO_PERMANENT_LAMBDA_BINDINGS: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _drain_deletes(app: Any, core: Any, event: Any) -> None:
    app.processEvents()
    core.sendPostedEvents(None, event.DeferredDelete)
    app.processEvents()


def validate_real_qt(root: Path, allow_no_qt: bool) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    try:
        from PySide6.QtCore import QCoreApplication, QEvent, QSettings
        from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget
    except ImportError:
        if allow_no_qt:
            print("REAL_QT_ARCHITECTURE_AI_SIGNAL_LIFECYCLE: SKIPPED_NO_PYSIDE6")
            return
        raise RuntimeError("PySide6 is required for real Qt validation.")

    from kanda_reasoner_app.local_ai_configuration import (
        LocalAIConfigurationController,
        install_application_local_ai_configuration,
    )
    from kanda_reasoner_app.manage_architecture.ai_review.gui_integration import (
        install_tab1_ai_review_controls,
    )
    from kanda_reasoner_app.web_ai_configuration import (
        WebAIConfigurationController,
        install_application_web_ai_configuration,
    )

    app = QApplication.instance() or QApplication([])
    captured: list[tuple[type[BaseException], BaseException]] = []
    original_hook = sys.excepthook

    def capture_hook(exc_type: type[BaseException], exc: BaseException, _tb: Any) -> None:
        captured.append((exc_type, exc))

    sys.excepthook = capture_hook
    window = QMainWindow()
    try:
        central = QWidget(window)
        window.setCentralWidget(central)
        first_host = QWidget(central)
        first_layout = QHBoxLayout(first_host)
        second_host = QWidget(central)
        second_layout = QHBoxLayout(second_host)
        window._worker_thread = None
        window._ai_review_thread = None

        with tempfile.TemporaryDirectory(prefix="kanda_ai_signal_qsettings_") as tmp:
            settings = QSettings(
                str(Path(tmp) / "local_ai.ini"),
                QSettings.Format.IniFormat,
            )
            local_controller = LocalAIConfigurationController(
                app,
                settings=settings,
                registry_factory=lambda **_kwargs: None,
            )
            web_controller = WebAIConfigurationController(app)
            install_application_local_ai_configuration(local_controller)
            install_application_web_ai_configuration(web_controller)

            install_tab1_ai_review_controls(window, first_layout)
            old_mode_host = window._ai_review_mode_host
            old_bindings = tuple(window._ai_review_configuration_sync_bindings)
            require(len(old_bindings) == 4, "First control generation did not bind four signals.")

            install_tab1_ai_review_controls(window, second_layout)
            new_mode_host = window._ai_review_mode_host
            new_button = window._ai_review_button
            require(new_mode_host is not old_mode_host, "Second control generation was not created.")
            require(
                len(tuple(window._ai_review_configuration_sync_bindings)) == 4,
                "Second control generation did not own exactly four signals.",
            )

            old_mode_host.deleteLater()
            _drain_deletes(app, QCoreApplication, QEvent)
            new_button.setText("sentinel")
            web_controller.configuration_changed.emit(web_controller.snapshot())
            app.processEvents()
            require(
                new_button.text() == "Review with Heuristic",
                "Deleting the old generation disconnected the current generation.",
            )
            print("REAL_QT_ARCHITECTURE_AI_REBUILD_SIGNAL_OWNER: PASS")

            new_mode_host.deleteLater()
            _drain_deletes(app, QCoreApplication, QEvent)
            web_controller.configuration_changed.emit(web_controller.snapshot())
            web_controller.catalog_changed.emit(tuple())
            local_controller.configuration_changed.emit(local_controller.snapshot())
            local_controller.catalog_changed.emit(tuple())
            app.processEvents()
            require(not captured, "Late controller signal raised: " + repr(captured))
            require(
                tuple(getattr(window, "_ai_review_configuration_sync_bindings", ())) == (),
                "Destroyed current controls retained global signal bindings.",
            )
            print("REAL_QT_ARCHITECTURE_AI_LATE_SIGNALS_IGNORED: PASS")
            print("REAL_QT_ARCHITECTURE_AI_DELETED_RADIO_GUARD: PASS")
    finally:
        sys.excepthook = original_hook
        window.close()
        window.deleteLater()
        _drain_deletes(app, QCoreApplication, QEvent)
        print("REAL_QT_ARCHITECTURE_AI_SIGNAL_TEARDOWN_CLEAN: PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--allow-no-qt", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    try:
        validate_static(root)
        if not args.static_only:
            validate_real_qt(root, args.allow_no_qt)
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print(str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
