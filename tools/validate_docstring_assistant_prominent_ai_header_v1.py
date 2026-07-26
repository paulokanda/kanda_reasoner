#!/usr/bin/env python3
"""Validate the Docstring AI group restored above Run Options in the left column."""

from __future__ import annotations

import argparse
import gc
import os
import sys
from pathlib import Path

FEATURE_ID = "docstring-assistant-ai-group-left-column-v1"


def require(condition: bool, message: str) -> None:
    """Raise a focused assertion when one contract is absent."""
    if not condition:
        raise AssertionError(message)


def validate_static(root: Path) -> None:
    """Validate source-level ownership and requested layout contracts."""
    shell_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
    runtime_path = root / (
        "kanda_reasoner_app/reasoner_tools_gui_shell/"
        "_docstring_ai_header_runtime.py"
    )
    layout_path = root / "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py"
    shell = shell_path.read_text(encoding="utf-8")
    runtime = runtime_path.read_text(encoding="utf-8")
    layout = layout_path.read_text(encoding="utf-8")

    require("install_docstring_header_surface" in shell, "header surface not installed")
    require("bind_embedded_docstring_widget" in shell, "embedded widget not bound")
    blueprint_block = shell.split("if spec.source_hint in {", 1)[1].split("}:", 1)[0]
    require(
        "_DOCSTRINGS_GUI_SOURCE" not in blueprint_block,
        "legacy header AI model blueprint still enabled for Docstring Assistant",
    )
    for text in (
        "Heuristic Activated",
        "Local AI Activated",
        "Web AI Activated",
        "docstring_ai_assistant_left_group",
        "_heuristic_radio",
        "_local_ai_radio",
        "_web_ai_radio",
        "QPropertyAnimation",
        "setLoopCount(-1)",
        "font-weight: 700",
    ):
        require(text in runtime, "missing retained header contract: " + text)
    require(
        "docstring_ai_header_detail_host" not in runtime,
        "obsolete full-width AI header host still present",
    )
    require(
        "detail_layout.addWidget(group)" not in runtime,
        "AI Assistant group still moved to the full-width header",
    )
    ai_add = "left_layout.addWidget(_build_ai_group(window))"
    options_add = "left_layout.addWidget(_build_options_group(window))"
    require(ai_add in layout and options_add in layout, "left-column groups missing")
    require(layout.index(ai_add) < layout.index(options_add), "AI Assistant is not above Run Options")

    print("DOCSTRING_HEADER_LEGACY_MODEL_CONTROLS_REMOVED: PASS")
    print("DOCSTRING_AI_GROUP_LEFT_COLUMN: PASS")
    print("DOCSTRING_AI_GROUP_ABOVE_RUN_OPTIONS: PASS")
    print("DOCSTRING_MODE_ONLY_CONTROLS: PASS")
    print("DOCSTRING_ACTIVATION_BADGE_CONTRACT: PASS")


def _stop_thread(owner: object, attribute: str) -> None:
    """Stop one known test-owned worker thread before Qt teardown."""
    thread = getattr(owner, attribute, None)
    if thread is None:
        return
    running = getattr(thread, "isRunning", None)
    if not callable(running) or not running():
        return
    request_interruption = getattr(thread, "requestInterruption", None)
    if callable(request_interruption):
        request_interruption()
    quit_method = getattr(thread, "quit", None)
    if callable(quit_method):
        quit_method()
    wait_method = getattr(thread, "wait", None)
    if callable(wait_method):
        require(bool(wait_method(3000)), "Qt worker did not stop during validator cleanup")


def _cleanup_real_qt(app: object, shell: object, widget: object, created_app: bool) -> None:
    """Stop animations/workers and drain deferred deletes before interpreter exit."""
    from PySide6.QtCore import QCoreApplication, QEvent

    if widget is not None:
        for attribute in (
            "_docstring_ai_thread",
            "_worker_thread",
            "_ai_catalog_thread",
            "_model_catalog_thread",
        ):
            _stop_thread(widget, attribute)

    animation = getattr(shell, "_docstring_ai_status_animation", None)
    if animation is not None:
        stop_method = getattr(animation, "stop", None)
        if callable(stop_method):
            stop_method()
        target_method = getattr(animation, "setTargetObject", None)
        if callable(target_method):
            target_method(None)
        delete_method = getattr(animation, "deleteLater", None)
        if callable(delete_method):
            delete_method()
        shell._docstring_ai_status_animation = None

    badge = getattr(shell, "_docstring_ai_status_label", None)
    if badge is not None:
        badge.setGraphicsEffect(None)
    shell._docstring_ai_status_effect = None

    if widget is not None:
        widget.hide()
        widget.close()
    shell.hide()
    shell.close()
    shell.deleteLater()

    app.processEvents()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    app.processEvents()
    if created_app:
        app.closeAllWindows()
        app.processEvents()
        app.quit()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()
    gc.collect()


def _group_by_title(widget: object, title: str) -> object | None:
    """Return one QGroupBox whose visible title matches exactly."""
    from PySide6.QtWidgets import QGroupBox

    for group in widget.findChildren(QGroupBox):
        if str(group.title() or "").strip() == title:
            return group
    return None


def validate_real_qt(root: Path) -> None:
    """Validate the real lazy-tab route and requested left-column placement."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QAbstractAnimation
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("REAL_DOCSTRING_AI_GROUP_LEFT_COLUMN: SKIPPED_NO_PYSIDE6")
        return

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs import LazyToolTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

    existing_app = QApplication.instance()
    created_app = existing_app is None
    app = existing_app or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    spec = next(item for item in TOOLS if item.tab_id == "docstring_assistant")
    shell = LazyToolTab(spec, lambda *_args: None)
    widget = None
    try:
        shell.show()
        app.processEvents()
        require(shell.load_tool(), "real Docstring Assistant lazy route did not load")
        app.processEvents()

        widget = shell._embedded_widget
        require(widget is not None, "embedded Docstring Assistant missing")
        badge = shell._docstring_ai_status_label
        group = shell._docstring_ai_assistant_left_group
        options = _group_by_title(widget, "Run Options")

        require(shell.tab_header_template.ai_model_combo is None, "legacy header model combo visible")
        require(
            shell.tab_header_template.refresh_ai_models_button is None,
            "legacy header refresh button visible",
        )
        require(shell.help_button is not None and shell.help_button.isVisible(), "Help missing")
        require(options is not None, "Run Options group missing")
        require(group.parentWidget() is options.parentWidget(), "AI Assistant is not in the left column")
        left_layout = group.parentWidget().layout()
        require(left_layout is not None, "left-column layout missing")
        require(left_layout.indexOf(group) < left_layout.indexOf(options), "AI Assistant is not above Run Options")
        require(group.isVisible(), "AI Assistant group hidden")
        require(widget._heuristic_radio.isVisible(), "Heuristic mode missing")
        require(widget._local_ai_radio.isVisible(), "Local AI mode missing")
        require(widget._web_ai_radio.isVisible(), "Web AI mode missing")

        title_index = shell.header_row.indexOf(shell.tab_header_template.title_label)
        badge_index = shell.header_row.indexOf(badge)
        project_index = shell.header_row.indexOf(shell.tab_header_template.project_root_host)
        require(title_index < badge_index < project_index, "activation badge is not after title")

        require(badge.text() == "Heuristic Activated", "initial heuristic badge missing")
        widget._local_ai_radio.setChecked(True)
        app.processEvents()
        require(badge.text() == "Local AI Activated", "Local AI badge transition failed")
        widget._web_ai_radio.setChecked(True)
        app.processEvents()
        require(badge.text() == "Web AI Activated", "Web AI badge transition failed")
        widget._heuristic_radio.setChecked(True)
        app.processEvents()
        require(badge.text() == "Heuristic Activated", "heuristic badge restoration failed")

        animation = shell._docstring_ai_status_animation
        require(animation.loopCount() == -1, "activation badge animation does not loop")
        require(animation.duration() >= 1600, "activation badge animation is not slow")
        require(animation.state() == QAbstractAnimation.Running, "activation badge is not flashing")

        print("DOCSTRING_HEADER_HELP_PRESERVED: PASS")
        print("DOCSTRING_HEADER_PROJECT_CONTROLS_PRESERVED: PASS")
        print("DOCSTRING_ACTIVATION_BADGE_TRANSITIONS: PASS")
        print("DOCSTRING_ACTIVATION_BADGE_SLOW_FLASH: PASS")
        print("REAL_DOCSTRING_AI_GROUP_LEFT_COLUMN: PASS")
    finally:
        _cleanup_real_qt(app, shell, widget, created_app)
        print("DOCSTRING_HEADER_QT_TEARDOWN_CLEAN: PASS")


def main() -> int:
    """Run static and real-widget validation when PySide6 is available."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    validate_static(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    sys.stdout.flush()
    sys.stderr.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
