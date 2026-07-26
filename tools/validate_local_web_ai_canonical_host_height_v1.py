# project-path: tools/validate_local_web_ai_canonical_host_height_v1.py
"""Validate canonical host-height containment for Local AI and Project Web AI."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys

FEATURE_ID = "local-web-ai-canonical-host-height-v1"
GUI_SUPPORT = Path("kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py")
LOCAL_UI = Path(
    "kanda_reasoner_app/reasoner_engine/"
    "ai_reasoner_main_window_help/ui_builder.py"
)
WEB_UI = Path(
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _source(root: Path, relative: Path) -> str:
    path = root / relative
    _require(path.is_file(), "Missing source: " + relative.as_posix())
    text = path.read_text(encoding="utf-8", errors="strict")
    compile(text, str(path), "exec")
    ast.parse(text, filename=str(path))
    return text


def _validate_static(root: Path) -> None:
    support = _source(root, GUI_SUPPORT)
    local_ui = _source(root, LOCAL_UI)
    web_ui = _source(root, WEB_UI)

    for fragment in (
        'contain_host_height = bool(widget.property("kandaContainHostHeight"))',
        "QSizePolicy.Ignored",
        "widget.setMinimumHeight(0)",
    ):
        _require(fragment in support, "Missing embedded host-height contract: " + fragment)

    for fragment in (
        'window.setProperty("kandaContainHostHeight", True)',
        "window.setMinimumHeight(0)",
        'scroll.setObjectName("projectQaBodyScrollArea")',
        "scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)",
    ):
        _require(fragment in local_ui, "Missing Local AI height contract: " + fragment)

    for fragment in (
        'owner.setProperty("kandaContainHostHeight", True)',
        "owner.setMinimumSize(1080, 0)",
        'owner.setObjectName("projectWebAITab")',
    ):
        _require(fragment in web_ui, "Missing Project Web AI height contract: " + fragment)

    _require(
        "owner.setMinimumSize(1080, 700)" not in web_ui,
        "Project Web AI still exports a 700px minimum host height.",
    )
    print("CANONICAL_EMBEDDED_HEIGHT_OWNER: PASS")
    print("LOCAL_AI_HOST_HEIGHT_OPT_IN: PASS")
    print("PROJECT_WEB_AI_HOST_HEIGHT_OPT_IN: PASS")
    print("PROJECT_WEB_AI_700PX_MINIMUM_REMOVED: PASS")


def _process_events(app, count: int = 8) -> None:
    for _ in range(count):
        app.processEvents()


def _validate_qt(root: Path) -> bool:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication, QSizePolicy
    except ModuleNotFoundError:
        print("REAL_LOCAL_WEB_AI_CANONICAL_HOST_HEIGHT: SKIPPED_NO_PYSIDE6")
        return False

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window import (
        ReasonerToolsWindow,
    )

    app = QApplication.instance() or QApplication([])
    window = ReasonerToolsWindow()
    window.resize(1200, 760)
    window.show()
    _process_events(app)

    baseline = (int(window.width()), int(window.height()))
    indices = {
        "brain": window._tab_index_by_tab_id["brain_navigator"],
        "local": window._tab_index_by_tab_id["project_qa"],
        "web": window._tab_index_by_tab_id["project_web_ai"],
    }

    def activate(name: str, *, require_lazy: bool):
        index = indices[name]
        window.tabs.setCurrentIndex(index)
        page = window._lazy_page_for_tab_index(index)
        if page is None:
            _require(
                not require_lazy,
                name + " target tab is not backed by a lazy page.",
            )
            active_widget = window.tabs.widget(index)
            _require(active_widget is not None, name + " tab widget is missing.")
        else:
            _require(page.ensure_loaded(), name + " failed to load.")
            active_widget = page._embedded_widget
            if require_lazy:
                _require(
                    active_widget is not None,
                    name + " embedded widget is missing after lazy load.",
                )
        _process_events(app)
        _require(
            (int(window.width()), int(window.height())) == baseline,
            name + " changed canonical host size from " + str(baseline)
            + " to " + str((int(window.width()), int(window.height()))),
        )
        return active_widget

    activate("brain", require_lazy=False)
    local = activate("local", require_lazy=True)
    web = activate("web", require_lazy=True)
    activate("local", require_lazy=True)
    activate("brain", require_lazy=False)
    print("REFERENCE_EAGER_TAB_SUPPORTED: PASS")
    print("LOCAL_WEB_AI_LAZY_TARGETS_CONFIRMED: PASS")

    for label, widget in (("Local AI", local), ("Project Web AI", web)):
        _require(widget is not None, label + " embedded widget is missing.")
        _require(
            bool(widget.property("kandaContainHostHeight")),
            label + " host-height property is missing.",
        )
        _require(widget.minimumHeight() == 0, label + " minimum height is not zero.")
        _require(
            widget.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Ignored,
            label + " embedded vertical size pressure is not ignored.",
        )

    window.close()
    _process_events(app, 3)
    print("REAL_LOCAL_AI_CANONICAL_HOST_HEIGHT: PASS")
    print("REAL_PROJECT_WEB_AI_CANONICAL_HOST_HEIGHT: PASS")
    print("REAL_LOCAL_WEB_AI_TAB_SWITCH_HEIGHT_STABLE: PASS")
    print("REAL_CANONICAL_HOST_SIZE_PRESERVED: PASS")
    return True


def validate(project_root: Path) -> None:
    root = project_root.expanduser().resolve()
    _require(root.is_dir(), "Project root is not a directory: " + str(root))
    _validate_static(root)
    _validate_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        validate(Path(args.project_root))
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID + " - " + str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
