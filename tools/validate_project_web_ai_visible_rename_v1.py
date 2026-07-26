"""Validate the user-visible Project Web AI to Web AI rename."""

from __future__ import annotations

import argparse
from pathlib import Path


FEATURE_ID = "project-web-ai-visible-rename-web-ai-v1"


def require(condition: bool, message: str) -> None:
    """Raise when one rename contract fails."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read one required UTF-8 source file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    """Validate visible labels while preserving internal architecture names."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    app = root / "kanda_reasoner_app"

    tool_specs = read_text(
        app / "reasoner_tools_gui_shell" / "tool_specs.py"
    )
    ui = read_text(
        app / "reasoner_engine" / "project_web_ai_tab_ui.py"
    )
    conversations = read_text(
        app / "reasoner_engine" / "project_web_ai_conversations.py"
    )
    preview = read_text(
        app / "reasoner_engine" / "project_web_ai_change_preview.py"
    )
    floating = read_text(
        app / "reasoner_tools_gui_shell" / "brain_navigator"
        / "assets" / "brain_visual_floating_window.py"
    )
    mapping = read_text(
        app / "reasoner_tools_gui_shell" / "brain_region_mapping"
        / "_mapping_data.py"
    )

    require('step_title="Web AI"' in tool_specs, "Tab title is not Web AI.")
    require(
        'step_title="Project Web AI"' not in tool_specs,
        "Old tab title remains.",
    )
    print("WEB_AI_TAB_TITLE: PASS")

    require('QLabel("Web AI")' in ui, "Sidebar title is not Web AI.")
    require(
        'setPlaceholderText("Message Web AI")' in ui,
        "Message placeholder is not Web AI.",
    )
    print("WEB_AI_PRIMARY_UI_LABELS: PASS")

    require('else "Web AI"' in conversations, "Assistant label is not Web AI.")
    require(
        'setWindowTitle("Web AI - Shadow Preview")' in preview,
        "Shadow Preview title is not Web AI.",
    )
    print("WEB_AI_SECONDARY_UI_LABELS: PASS")

    require('"Web AI"' in floating, "Brain Navigator label is not Web AI.")
    require(
        '"target_tab_label": "Web AI"' in mapping,
        "Brain mapping target label is not Web AI.",
    )
    require(
        '"tooltip_text": "Central sulcus -> Web AI"' in mapping,
        "Brain mapping tooltip is not Web AI.",
    )
    print("WEB_AI_BRAIN_NAVIGATOR_LABELS: PASS")

    require(
        "class ProjectWebAITab" in read_text(
            app / "reasoner_engine" / "project_web_ai_tab.py"
        ),
        "Internal ProjectWebAITab architecture name changed unexpectedly.",
    )
    require(
        'tab_id="project_web_ai"' in tool_specs,
        "Internal project_web_ai tab ID changed unexpectedly.",
    )
    print("WEB_AI_INTERNAL_ARCHITECTURE_PRESERVED: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
