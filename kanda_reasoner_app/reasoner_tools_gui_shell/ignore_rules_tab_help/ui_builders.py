"""UI construction helpers for the ignore-rules tab."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesUiMixin",
]

from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout


class IgnoreRulesUiMixin:
    """Build and wire the ignore-rules tab user interface."""

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)

        project_scope_row = QHBoxLayout()
        project_scope_row.addWidget(self.project_root_label, 0)
        project_scope_row.addWidget(self.project_root_edit, 0)
        project_scope_row.addWidget(self.project_root_search_button, 0)
        project_scope_row.addSpacing(16)
        project_scope_row.addWidget(self.project_scope_label, 1)
        main_layout.addLayout(project_scope_row)

        folder_group = QGroupBox(
            "These folders are not part of the project and must be ignored"
        )
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(self.folder_list)
        folder_btns = QHBoxLayout()
        folder_btns.addWidget(self._make_button("Add Folder (browse)", self._add_folder))
        folder_btns.addWidget(self._make_button("Edit Folder", self._edit_folder))
        folder_btns.addWidget(
            self._make_button("Remove Folder", self._remove_folder)
        )
        folder_btns.addWidget(
            self._make_button(
                "Clear All Folders",
                lambda: self._clear_list(self.folder_list, "folders"),
            )
        )
        folder_layout.addLayout(folder_btns)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)

        file_group = QGroupBox(
            "These files are not part of the project and must be ignored"
        )
        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_list)
        file_btns = QHBoxLayout()
        file_btns.addWidget(self._make_button("Add File (browse)", self._add_file))
        file_btns.addWidget(self._make_button("Edit File", self._edit_file))
        file_btns.addWidget(self._make_button("Remove File", self._remove_file))
        file_btns.addWidget(
            self._make_button(
                "Clear All Files",
                lambda: self._clear_list(self.file_list, "files"),
            )
        )
        file_layout.addLayout(file_btns)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        ext_group = QGroupBox(
            "These extensions are not part of the project and must be ignored"
        )
        ext_layout = QVBoxLayout()
        ext_layout.addWidget(self.ext_list)
        ext_btns = QHBoxLayout()
        ext_btns.addWidget(
            self._make_button("Add Extension (text)", self._add_extension)
        )
        ext_btns.addWidget(self._make_button("Edit Extension", self._edit_extension))
        ext_btns.addWidget(
            self._make_button("Remove Extension", self._remove_extension)
        )
        ext_btns.addWidget(
            self._make_button(
                "Clear All Extensions",
                lambda: self._clear_list(self.ext_list, "extensions"),
            )
        )
        ext_layout.addLayout(ext_btns)
        ext_group.setLayout(ext_layout)
        main_layout.addWidget(ext_group)

        global_btns = QHBoxLayout()
        save_btn = QPushButton("Save Rules (auto-save is on - optional)")
        save_btn.clicked.connect(self._save_rules)
        reset_btn = QPushButton("Reset to Defaults (auto-saved)")
        reset_btn.clicked.connect(self._reset_defaults)
        global_btns.addWidget(save_btn)
        global_btns.addWidget(reset_btn)
        global_btns.addStretch()
        main_layout.addLayout(global_btns)

        self.setLayout(main_layout)

    def _make_button(self, text: str, slot) -> QPushButton:
        """Create a button and connect it to a slot."""
        btn = QPushButton(text)
        btn.clicked.connect(slot)
        return btn
