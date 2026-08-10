# project-path: tools/validate_project_web_ai_conversation_advisory_subtabs_v1.py
"""Validate spacious Project Conversation and Web Advisory Config subtabs."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import sys
from pathlib import Path

FEATURE_ID = "project-web-ai-conversation-advisory-subtabs-v1"
UI = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py"
THEME = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_theme.py"
CONTROLLER = "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py"
SELECTOR = (
    "kanda_reasoner_app/reasoner_engine/"
    "project_web_ai_configuration_selector.py"
)
VALIDATOR = "tools/validate_project_web_ai_conversation_advisory_subtabs_v1.py"
FILES = (UI, THEME, VALIDATOR)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static(root: Path) -> None:
    ui = (root / UI).read_text(encoding="utf-8")
    theme = (root / THEME).read_text(encoding="utf-8")
    controller = (root / CONTROLLER).read_text(encoding="utf-8")
    selector = (root / SELECTOR).read_text(encoding="utf-8")

    for marker in (
        'tabs.addTab(_conversation_page(owner), "Project Conversation")',
        'tabs.addTab(_advisory_config_page(owner), "Web Advisory Config")',
        'owner.web_ai_subtabs = tabs',
        'owner.conversation_page = page',
        'owner.advisory_config_page = page',
        'owner.advisory_config_splitter = columns',
        'owner.context_details.setMinimumHeight(260)',
        'owner.provenance_box.setMinimumHeight(420)',
        'content_layout.addWidget(_project_selector(owner))',
        'left_layout.addWidget(_project_context_section(owner), 1)',
        'left_layout.addWidget(_provider_section(owner))',
        'right_layout.addWidget(_details_section(owner), 1)',
    ):
        require(marker in ui, "missing subtab contract: " + marker)
    require(
        "settings_scroll.setMaximumHeight" not in ui,
        "advisory configuration remains vertically capped",
    )
    require(
        ui.index("root.addWidget(_chat_history_panel(owner), 1)")
        < ui.index("owner.sidebar_panel = sidebar"),
        "conversation history panel is detached",
    )
    require(
        "_project_context_section(owner)" not in ui[
            ui.index("def _conversation_sidebar"):ui.index("def _composer")
        ],
        "context data remains below chat history",
    )
    require(
        "_provider_section(owner)" not in ui[
            ui.index("def _conversation_sidebar"):ui.index("def _composer")
        ],
        "provider configuration remains below chat history",
    )
    print("WEB_AI_TWO_SUBTAB_COMPOSITION_STATIC: PASS")
    print("WEB_AI_CONVERSATION_SURFACE_UNCLUTTERED_STATIC: PASS")
    print("WEB_AI_ADVISORY_CONTENT_UNCAPPED_STATIC: PASS")

    for marker in (
        "QTabWidget#projectWebAISubtabs::pane",
        "QTabWidget#projectWebAISubtabs QTabBar::tab:selected",
        "QWidget#projectWebAIAdvisoryConfigPage",
        "QSplitter#projectWebAIAdvisorySplitter::handle",
    ):
        require(marker in theme, "missing subtab theme marker: " + marker)
    print("WEB_AI_SUBTAB_THEME_STATIC: PASS")

    for marker in (
        "web_selector.connect(self)",
        "web_selector.render(self)",
        "self._web_config.configuration_changed.connect",
    ):
        require(marker in controller, "central controller integration missing: " + marker)
    require("owner._web_config" in selector, "selector bridge lost central owner")
    require("QLineEdit" not in selector, "selector bridge owns a secret field")
    print("WEB_AI_SINGLE_CONFIGURATION_OWNER_STATIC: PASS")

    for relative in FILES:
        path = root / relative
        ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        lines = len(path.read_text(encoding="utf-8").splitlines())
        require(0 < lines <= 500, f"module-size violation {relative}: {lines}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_real_qt() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab

    app = QApplication.instance() or QApplication([])
    widget = ProjectWebAITab()
    widget.resize(1500, 920)
    widget.show()
    app.processEvents()

    require(widget.web_ai_subtabs.count() == 2, "subtab count mismatch")
    require(widget.web_ai_subtabs.currentWidget() is widget.conversation_page, "default page")
    require(widget.answer_box.isVisibleTo(widget), "conversation output hidden")
    require(widget.chat_list.isVisibleTo(widget), "chat history hidden")
    require(not widget.project_root_edit.isVisibleTo(widget), "config leaked into conversation")
    require(not widget.web_access_combo.isVisibleTo(widget), "provider leaked into conversation")
    print("REAL_QT_WEB_AI_PROJECT_CONVERSATION_SUBTAB: PASS")

    widget.web_ai_subtabs.setCurrentWidget(widget.advisory_config_page)
    app.processEvents()
    require(widget.project_root_edit.isVisibleTo(widget), "Project selector hidden")
    require(widget.context_details.isVisibleTo(widget), "context details hidden")
    require(widget.web_access_combo.isVisibleTo(widget), "access selector hidden")
    require(widget.web_provider_combo.isVisibleTo(widget), "provider selector hidden")
    require(widget.web_model_combo.isVisibleTo(widget), "model selector hidden")
    require(widget.provenance_box.isVisibleTo(widget), "response details hidden")
    require(widget.settings_scroll.maximumHeight() > 1000, "advisory scroll is capped")
    require(widget.context_details.height() >= 220, "context detail area too short")
    require(widget.provenance_box.height() >= 360, "provenance area too short")
    require(
        widget.advisory_config_splitter.width() >= 900,
        "advisory configuration does not use the working width",
    )
    print("REAL_QT_WEB_AI_ADVISORY_CONFIG_SUBTAB: PASS")
    print("REAL_QT_WEB_AI_ADVISORY_CONTENT_WIDE: PASS")
    print("REAL_QT_WEB_AI_CONFIG_CONTROLS_VISIBLE: PASS")

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
        for relative in (*FILES, CONTROLLER, SELECTOR)
        if (root / relative).is_file()
    }
    os.chdir(root)
    validate_static(root)
    if not args.static_only:
        validate_real_qt()
    after = {relative: sha256(root / relative) for relative in before}
    require(before == after, "subtab validation mutated Tool source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
