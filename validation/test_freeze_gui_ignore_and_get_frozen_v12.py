from __future__ import annotations

import ast
from pathlib import Path

EXPECTED_MARKER = "VALIDATION OK: freeze-gui-ignore-and-get-frozen-v12"
EXPECTED_STATUS = "STATUS: IN_SYNC"
FREEZE_TAB_REL = Path("kanda_reasoner_app") / "freeze_after_update_gui" / "freeze_after_update_tab.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    root = Path.cwd().resolve()
    freeze_tab = root / FREEZE_TAB_REL
    require(freeze_tab.is_file(), "freeze_after_update_tab.py missing")
    text = freeze_tab.read_text(encoding="utf-8")
    ast.parse(text)

    required_snippets = [
        "self.get_last_freeze_button = QPushButton(\"Get Last Freeze\")",
        "self.get_all_frozen_button = QPushButton(\"Get All Frozen\")",
        "self.help_button = QPushButton(\"Help\")",
        "self.project_root_header_label = QLabel(\"Project Root:\")",
        "self.search_project_button = QPushButton(\"Search\")",
        "def move_project_root_controls_to_layout",
        "def set_project_root",
        "def _copy_last_freeze_snippet",
        "def _copy_all_frozen_snippets",
        "KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN",
        "KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END",
        "ignore_freeze_button = QPushButton(\"Ignore this Freeze\")",
        "def ignore_this_freeze",
        "write_confirmed_freeze_entry(project_root, preview, confirmation=True)",
        "mark_latest_freeze_hint_used(project_root, freeze_id=\"ignored-by-human\")",
        "ignore_freeze_button.clicked.connect(ignore_this_freeze)",
        "entry_files(project_root)",
        "parse_frontmatter",
    ]
    for snippet in required_snippets:
        require(snippet in text, "Missing required freeze GUI snippet: " + snippet)

    require(text.index("self.help_button = QPushButton(\"Help\")") < text.index("self.get_last_freeze_button = QPushButton(\"Get Last Freeze\")"), "Get buttons must be placed beside Help in header")
    require(text.index("self.get_last_freeze_button = QPushButton(\"Get Last Freeze\")") < text.index("self.get_all_frozen_button = QPushButton(\"Get All Frozen\")"), "Get Last Freeze must precede Get All Frozen")
    require(text.index("button_row.addWidget(confirm_write_button)") < text.index("button_row.addWidget(ignore_freeze_button)"), "Ignore button must sit right after Confirm and Write")
    require("Confirm and Write still requires human confirmation" in text, "Human confirmation gate text missing")
    print(EXPECTED_MARKER)
    print(EXPECTED_STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
