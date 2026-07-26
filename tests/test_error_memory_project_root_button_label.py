"""Source contract for the Error Memory project-root browse button label."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERROR_MEMORY_TAB = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"


def test_error_memory_project_root_button_label_is_browse_project_folder() -> None:
    """Error Memory should not show the old generic Search label."""
    source = ERROR_MEMORY_TAB.read_text(encoding="utf-8")

    assert "self.search_project_button = QPushButton('browse project folder')" in source
    assert "self.search_project_button = QPushButton('Search')" not in source


if __name__ == "__main__":
    test_error_memory_project_root_button_label_is_browse_project_folder()
    print("Error Memory project-root button label test passed.")
