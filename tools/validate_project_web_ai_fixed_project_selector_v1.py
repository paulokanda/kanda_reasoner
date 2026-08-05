# project-path: tools/validate_project_web_ai_fixed_project_selector_v1.py
"""Validate the synchronized Project selector in the advisory configuration subtab."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "project-web-ai-fixed-project-selector-v1"
UI = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
CONTROLLER = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
SHELL_SYNC = "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py"
SHELL_ROOT = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "main_window_help/window_project_root.py"
)
MAIN_WINDOW = "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py"
VALIDATOR = "tools/validate_project_web_ai_fixed_project_selector_v1.py"
TOUCHED = (UI, VALIDATOR)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static(root: Path) -> None:
    ui = (root / UI).read_text(encoding="utf-8")
    controller = (root / CONTROLLER).read_text(encoding="utf-8")
    shell_sync = (root / SHELL_SYNC).read_text(encoding="utf-8")
    shell_root = (root / SHELL_ROOT).read_text(encoding="utf-8")
    main_window = (root / MAIN_WINDOW).read_text(encoding="utf-8")

    required = (
        'setObjectName("projectWebAIProjectRootEdit")',
        'QPushButton("Browse...")',
        'setObjectName("projectWebAIProjectBrowseButton")',
        'setObjectName("projectWebAIProjectSelector")',
        'setObjectName("projectWebAIAdvisoryConfigPage")',
        'setObjectName("projectWebAISettingsScroll")',
        'content_layout.addWidget(_project_selector(owner))',
        'owner.project_selector_panel = frame',
        'owner.settings_scroll = scroll',
        'Shared across all Project tabs',
    )
    for marker in required:
        require(marker in ui, "missing advisory selector marker: " + marker)
    require(
        ui.count("owner.project_root_edit = QLineEdit()") == 1,
        "Project Web AI must own exactly one root editor",
    )
    require(
        ui.count("path_row.addWidget(owner.project_root_edit, 1)") == 1,
        "canonical root editor is duplicated or missing",
    )
    require(
        "_conversation_sidebar(owner)" in ui,
        "conversation sidebar contract missing",
    )
    print("PROJECT_SELECTOR_MOVED_TO_ADVISORY_SUBTAB: PASS")
    print("SINGLE_CANONICAL_PROJECT_ROOT_CONTROL: PASS")
    print("PROJECT_SELECTOR_FULL_WIDTH_CONFIG_CONTEXT: PASS")

    for marker in (
        "self.pick_project_button.clicked.connect(self._pick_project)",
        "QFileDialog.getExistingDirectory",
        "self.project_root_edit.setText(selected)",
        "self.project_root_edit.textChanged.connect(self._on_project_root_changed)",
        "request_guarded_project_switch(self, text)",
    ):
        require(marker in controller, "Browse/root lifecycle missing: " + marker)
    require('"project_web_ai"' in shell_sync, "Project Web AI shell scope missing")
    require('"project_root_edit"' in main_window, "shell root field contract missing")
    require(
        "_on_any_project_root_text_changed" in shell_root,
        "canonical shell root propagation owner missing",
    )
    print("PROJECT_BROWSE_ACTION_WIRED: PASS")
    print("SHELL_PROJECT_ROOT_SYNC_CONTRACT_PRESERVED: PASS")

    for relative in TOUCHED:
        path = root / relative
        ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        lines = len(path.read_text(encoding="utf-8").splitlines())
        require(0 < lines <= 500, f"module-size violation {relative}: {lines}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    from PySide6.QtWidgets import QApplication, QFileDialog

    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab

    app = QApplication.instance() or QApplication([])
    widget = ProjectWebAITab()
    widget.resize(1440, 900)
    widget.show()
    app.processEvents()

    require(
        not widget.project_selector_panel.isVisibleTo(widget),
        "Project selector leaked into the conversation subtab",
    )
    widget.web_ai_subtabs.setCurrentIndex(1)
    app.processEvents()
    require(widget.project_selector_panel.isVisibleTo(widget), "selector panel hidden")
    require(widget.project_root_edit.isVisibleTo(widget), "Project root editor hidden")
    require(widget.pick_project_button.isVisibleTo(widget), "Browse button hidden")
    require(widget.pick_project_button.text() == "Browse...", "Browse label mismatch")
    require(
        widget.settings_scroll.isAncestorOf(widget.project_root_edit),
        "Project root editor is not owned by the advisory page",
    )
    require(
        widget.advisory_config_page.isAncestorOf(widget.project_root_edit),
        "Project selector is outside the advisory subtab",
    )
    print("REAL_QT_PROJECT_SELECTOR_ADVISORY_SUBTAB: PASS")
    print("REAL_QT_PROJECT_SELECTOR_HIDDEN_FROM_CONVERSATION: PASS")

    original = QFileDialog.getExistingDirectory
    with tempfile.TemporaryDirectory(prefix="kanda-project-selector-") as temporary:
        selected = str(Path(temporary).resolve())
        QFileDialog.getExistingDirectory = staticmethod(
            lambda *_args, **_kwargs: selected
        )
        try:
            widget.pick_project_button.click()
            app.processEvents()
        finally:
            QFileDialog.getExistingDirectory = original
        require(
            Path(widget.project_root_edit.text()).resolve() == Path(selected),
            "Browse did not publish the selected Project root",
        )
    print("REAL_QT_PROJECT_BROWSE_SETS_ROOT: PASS")

    widget.close()
    app.processEvents()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    before = {
        relative: sha256(root / relative)
        for relative in (*TOUCHED, CONTROLLER, SHELL_SYNC, SHELL_ROOT, MAIN_WINDOW)
        if (root / relative).is_file()
    }
    os.chdir(root)
    validate_static(root)
    if not args.static_only:
        validate_real_qt()
    after = {relative: sha256(root / relative) for relative in before}
    require(before == after, "selector validation mutated Tool source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
