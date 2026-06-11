"""Read-only Prompt Library tab with 3D cube dashboard launchers."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from .group_catalog import PromptGroup, filter_items_for_group, load_prompt_groups
from .group_dashboard import PromptGroupDashboard
from .group_window import PromptGroupWindow
from .library_catalog import PromptLibraryItem, load_prompt_library_items
from .library_paths import prompt_library_root

__all__ = [
    "PromptLibraryTab",
]


class PromptLibraryTab(QWidget):
    """Read-only GUI tab that launches grouped Prompt Library windows."""

    def __init__(self, library_root: Path | None = None) -> None:
        """Create the Prompt Library group dashboard.

        Args:
            library_root: Optional prompt_library root override for tests.
        """
        super().__init__()
        self.library_root = library_root or prompt_library_root()
        self.items: list[PromptLibraryItem] = []
        self.groups: list[PromptGroup] = []
        self.group_windows: list[PromptGroupWindow] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title = QLabel("Prompt Engineering Library")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Read-only visual dashboard for grouped, project-agnostic prompts. "
            "Click a native 3D group cube to open a floating Engineering Library window. "
            "This tab does not edit code, run prompts, or update governance."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        button_row = QHBoxLayout()
        self.reload_button = QPushButton("Reload Groups")
        self.reload_button.clicked.connect(self.reload_library)
        button_row.addWidget(self.reload_button)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        self.dashboard = PromptGroupDashboard()
        self.dashboard.group_activated.connect(self.open_group_window)
        layout.addWidget(self.dashboard, 1)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.reload_library()

    def reload_library(self) -> None:
        """Reload prompt groups and prompt-library items from disk."""
        self.items = load_prompt_library_items(self.library_root)
        self.groups = load_prompt_groups(self.library_root)
        counts: dict[str, int] = {}
        for group in self.groups:
            counts[group.group_id] = len(filter_items_for_group(group, self.items))
        self.dashboard.set_groups(self.groups, counts)

        if self.groups:
            self.status_label.setText(
                "Loaded "
                + str(len(self.groups))
                + " prompt groups and "
                + str(len(self.items))
                + " prompt-library text assets from "
                + str(self.library_root)
            )
        else:
            self.status_label.setText(
                "No prompt groups found. Expected catalog: "
                + str(self.library_root / "groups" / "PROMPT_GROUPS.json")
            )

    def open_group_window(self, group: PromptGroup) -> None:
        """Open a floating read-only library window for one group."""
        items = filter_items_for_group(group, self.items)
        window = PromptGroupWindow(group, items, self.library_root)
        window.destroyed.connect(lambda _obj=None, win=window: self._forget_window(win))
        self.group_windows.append(window)
        window.show()
        self.status_label.setText("Opened group window: " + group.display_name)

    def _forget_window(self, window: PromptGroupWindow) -> None:
        """Forget a closed group window reference."""
        self.group_windows = [item for item in self.group_windows if item is not window]
