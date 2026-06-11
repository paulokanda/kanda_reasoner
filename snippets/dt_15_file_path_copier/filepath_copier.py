#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filepath_copier.py (PySide6)

#### - Purpose - ####
Creates a small PySide6 GUI to collect relative file paths inside your project and append them to a user‑named .txt list under file_path_copier/.

#### - How it works (quick) - ####
1) On launch, you can open an existing .txt (button) or create a new one. The file lives under file_path_copier/ and is opened in append mode.
2) Use a single "Select…" button (with a dropdown) to choose either Files or a Folder:
   - Files → pick one or more files (filtered to .py .md .txt .json)
   - Folder → recursively adds allowed files from the chosen folder
3) Only files inside the project root are accepted. Paths are written relative to the project root, one per line, as soon as they are added.
4) Buttons: OK, Cancel, Close (all close; data is appended immediately when selected).
5) You can switch the output list anytime with the "Output…" button: create a new list or select an existing .txt.

#### - Notes - ####
- Project root is detected as two levels up from this file (the folder that contains ``).
- Items outside the project are skipped.
- Allowed extensions only: .py .md .txt .json
- The list shows what was appended in the current session; opening an existing .txt loads it into the viewer so you continue editing.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List
import shutil

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut, QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QToolButton,
    QMenu,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)

from send2trash import send2trash

# -------------------------------
# Config
# -------------------------------
ALLOWED_EXTS = {".py", ".md", ".txt", ".json"}
NAME_FILTER = "Code/Text files (*.py *.md *.txt *.json)"
TXT_FILTER = "Text files (*.txt)"
# Use LF newlines for consistency across OSes
FORCE_LF_NEWLINES = True
FULL_NAME = "Path Collector"
# -------------------------------
# Utilities
# -------------------------------

#### - get_project_root: detect project root as two levels up from this file - ####
def get_project_root() -> Path:
    this_file = Path(__file__).resolve()
    # Expected structure: <project_root>/file_path_copier/filepath_copier.py
    project_root = this_file.parents[2] if len(this_file.parents) >= 3 else this_file.parent
    return project_root

#### - ensure_output_dir: make sure file_path_copier exists - ####
def ensure_output_dir() -> Path:
    project_root = get_project_root()
    out_dir = project_root / "dev_tools" / "file_path_copier"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

#### - is_inside_project: verify a path is under project_root - ####
def is_inside_project(p: Path, project_root: Path) -> bool:
    try:
        p_abs = p.resolve()
        root_abs = project_root.resolve()
        return root_abs in p_abs.parents or p_abs == root_abs
    except Exception:
        return False

#### - is_allowed_file: extension filter - ####
def is_allowed_file(p: Path) -> bool:
    return p.suffix.lower() in ALLOWED_EXTS

#### - iter_files_in_folder: yield allowed files within a folder recursively - ####
def iter_files_in_folder(folder: Path) -> Iterable[Path]:
    for root, _dirs, files in os.walk(folder):
        for f in files:
            path = Path(root) / f
            if is_allowed_file(path):
                yield path

#### - validate_and_relativize: keep order, filter, and return relative paths - ####
def validate_and_relativize(files: Iterable[Path], project_root: Path) -> List[str]:
    rels: List[str] = []
    for f in files:
        try:
            if is_allowed_file(f) and is_inside_project(f, project_root):
                rels.append(os.path.relpath(f.resolve(), project_root.resolve()))
        except Exception:
            pass
    return rels


# -------------------------------
# GUI App (PySide6)
# -------------------------------

class PathCollectorWindow(QWidget):
    #### - __init__: set up window, ask/choose list file, open file handle - ####
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"🧩 {FULL_NAME}")
        self.resize(800, 560)
        self.setMinimumSize(560, 380)

        self.project_root: Path = get_project_root()
        self.output_dir: Path = ensure_output_dir()
        self.output_file: Path | None = None

        # Build UI first (so the Open button is visible immediately)
        self._build_ui()

        # On start: offer to open an existing .txt (button is also available anytime)
        # If user declines or fails, fall back to creating a new list.
        if not self.on_open_existing_at_start():
            self.on_new_list(initial=True)

        self._update_status()

    def on_copy_to(self) -> None:
        """Copies all files listed in the current output .txt to a single selected folder (flat structure)."""
        if not self.output_file or not self.output_file.exists():
            QMessageBox.warning(self, "No file", "No output list is loaded.")
            return

        target_dir = QFileDialog.getExistingDirectory(self, "Select destination folder")
        if not target_dir:
            return

        dest = Path(target_dir)
        copied, failed = 0, 0
        failed_paths = []
        name_collisions = {}

        try:
            with self.output_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    rel_path = line.strip()
                    if not rel_path:
                        continue
                    src_path = self.project_root / rel_path
                    if not src_path.exists():
                        failed += 1
                        failed_paths.append(rel_path)
                        continue

                    dest_path = dest / src_path.name

                    # Handle filename collision by renaming with suffix
                    if dest_path.exists():
                        suffix = 1
                        stem = src_path.stem
                        ext = src_path.suffix
                        while True:
                            alt_path = dest / f"{stem}_{suffix}{ext}"
                            if not alt_path.exists():
                                dest_path = alt_path
                                name_collisions[src_path.name] = dest_path.name
                                break
                            suffix += 1

                    try:
                        shutil.copy2(src_path, dest_path)
                        copied += 1
                    except Exception:
                        failed += 1
                        failed_paths.append(rel_path)

        except Exception as e:
            QMessageBox.critical(self, "Copy error", f"Could not read from list:\n{e}")
            return

        msg = f"Copied {copied} file(s) to {dest}."
        if name_collisions:
            msg += "\nRenamed due to name collisions:\n" + "\n".join(
                f"{k} → {v}" for k, v in name_collisions.items()
            )
        if failed:
            msg += f"\nFailed to copy {failed} file(s)."
            msg += "\nExamples:\n" + "\n".join(failed_paths[:5])
        QMessageBox.information(self, "Copy complete", msg)
        self._update_status(msg)

    #### - _set_output_file: set file path, create if needed, update label and viewer - ####
    def _set_output_file(self, path: Path, create_if_missing: bool = False, load_into_viewer: bool = True) -> None:
        try:
            if create_if_missing:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch(exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not prepare file: {path}\n{e}")

            raise SystemExit(1)
        self.output_file = path
        self.lbl_output.setText(f"Appending to: {self.output_file}")
        if load_into_viewer:
            self._load_list_into_viewer(self.output_file)

    #### - _load_list_into_viewer: populate session list from existing .txt - ####
    def _load_list_into_viewer(self, path: Path) -> None:
        """Populate the session list from an existing .txt file."""
        self.listbox.clear()
        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    # strip newlines and spaces
                    line = line.rstrip("\r\n ").strip()
                    if line:  # only add non-empty lines
                        QListWidgetItem(line, self.listbox)
        except FileNotFoundError:
            # No problem—new file
            pass
        except Exception as e:
            QMessageBox.warning(self, "Read error", f"Could not read {path}:\n{e}")
    #### - _build_ui: layout elements - ####
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        # Info labels
        self.lbl_project = QLabel(f"Project root: {self.project_root}")
        self.lbl_project.setTextInteractionFlags(Qt.TextSelectableByMouse)
        root.addWidget(self.lbl_project)

        self.lbl_output = QLabel("Appending to: (no list selected)")
        self.lbl_output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_output.setStyleSheet("color: gray;")
        root.addWidget(self.lbl_output)

        # Buttons row
        row = QHBoxLayout()

        # Open saved .txt (explicit button requested for startup)
        self.btn_open_existing = QPushButton("Open saved .txt…")
        self.btn_open_existing.clicked.connect(self.on_use_existing)
        row.addWidget(self.btn_open_existing)

        # Select… split-button with dropdown (Files / Folder)
        self.btn_select = QToolButton()
        self.btn_select.setText("Select…")
        self.btn_select.setPopupMode(QToolButton.MenuButtonPopup)
        select_menu = QMenu(self.btn_select)

        act_files = QAction("Files…", self)
        act_files.triggered.connect(self.on_select_files)
        select_menu.addAction(act_files)

        act_folder = QAction("Folder…", self)
        act_folder.triggered.connect(self.on_select_folder)
        select_menu.addAction(act_folder)

        self.btn_select.setMenu(select_menu)
        self.btn_select.clicked.connect(self.on_select_files)  # default click = files
        row.addWidget(self.btn_select)

        # Output… split-button (New list… / Use existing .txt…)
        self.btn_output = QToolButton()
        self.btn_output.setText("Output…")
        self.btn_output.setPopupMode(QToolButton.MenuButtonPopup)
        output_menu = QMenu(self.btn_output)

        act_new = QAction("New list…", self)
        act_new.triggered.connect(self.on_new_list)
        output_menu.addAction(act_new)

        act_existing = QAction("Use existing .txt…", self)
        act_existing.triggered.connect(self.on_use_existing)
        output_menu.addAction(act_existing)

        self.btn_output.setMenu(output_menu)
        self.btn_output.clicked.connect(self.on_new_list)  # default click = new list
        row.addWidget(self.btn_output)

        self.btn_clear = QPushButton("Clear List (session)")
        self.btn_clear.clicked.connect(self.on_clear_list)
        row.addWidget(self.btn_clear)

        self.btn_copy_to = QPushButton("Copy To…")
        self.btn_copy_to.clicked.connect(self.on_copy_to)
        row.addWidget(self.btn_copy_to)

        row.addStretch(1)
        root.addLayout(row)

        # Session list
        root.addWidget(QLabel("Appended this session:"))
        self.listbox = QListWidget()
        root.addWidget(self.listbox, 1)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setMinimumHeight(22)
        root.addWidget(self.status_label)

        # Bottom action buttons
        bottom = QHBoxLayout()
        bottom.addStretch(1)

        self.btn_start_over = QPushButton("Start Over")
        self.btn_start_over.clicked.connect(self.on_start_over)
        bottom.addWidget(self.btn_start_over)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.close)
        bottom.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.close)
        bottom.addWidget(self.btn_cancel)

        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        bottom.addWidget(self.btn_close)

        root.addLayout(bottom)

        # ESC to close
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self.close)

    #### - _update_status: helper to set status text - ####
    def _update_status(self, text: str | None = None) -> None:
        self.status_label.setText(text or "Ready")

    def on_start_over(self) -> None:
        """Resets session and optionally moves output file to trash (safely)."""
        if self.output_file and self.output_file.exists():
            choice = QMessageBox.question(
                self,
                "Delete file?",
                f"Do you want to move the current output file to trash?\n\n{self.output_file}",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel,
            )
            if choice == QMessageBox.Cancel:
                self._update_status("Start over cancelled.")
                return
            if choice == QMessageBox.Yes:
                try:
                    if not os.access(self.output_file, os.W_OK):
                        raise PermissionError("File is read-only.")
                    send2trash(str(self.output_file))
                    QMessageBox.information(self, "Deleted", "Output file moved to trash.")
                except Exception as e:
                    QMessageBox.warning(self, "Delete error", f"Could not delete file:\n{e}")
                    self._update_status("File not deleted.")
                    return

        # Reset GUI state
        self.output_file = None
        self.listbox.clear()
        self.lbl_output.setText("Appending to: (no list selected)")
        self._update_status("Reset complete. Please select a new or existing .txt.")

    #### - _append_paths: write a sequence of files to the output file - ####
    def _append_paths(self, files: List[Path]) -> None:
        if not files or not self.output_file or not self.output_file.exists():
            self._update_status("No valid output file set.")
            return

        rels = validate_and_relativize(files, self.project_root)
        appended = 0
        skipped = len(files) - len(rels)

        try:
            if rels:
                newline_style = "\n" if FORCE_LF_NEWLINES else None
                with self.output_file.open("a", encoding="utf-8", newline=newline_style) as fh:
                    for rel in rels:
                        fh.write(rel + "\n")
                        QListWidgetItem(rel, self.listbox)
                        appended += 1
                    fh.flush()
        except Exception as e:
            QMessageBox.critical(self, "Write error", f"Could not append to {self.output_file}:\n{e}")
            return

        msg = f"Appended {appended} item(s)."
        if skipped:
            msg += f" Skipped {skipped} outside project or not allowed."
        self._update_status(msg)

    def on_select_files(self) -> None:
        from pathlib import Path
        from PySide6.QtWidgets import QFileDialog
        from shared.file_dialog_context import (
            get_default_dialog_dir,
            update_last_used_dir,
            restore_last_used_dir,
        )
        import shared.global_signal_bus as gsb

        project_root = gsb.PROJECT_ROOT

        # ---------------------------------------------------------
        # Determine start directory
        # ---------------------------------------------------------
        if project_root:
            restore_last_used_dir(project_root)
            start_dir = get_default_dialog_dir(project_root)
        else:
            start_dir = Path.cwd()

        # ---------------------------------------------------------
        # Open dialog
        # ---------------------------------------------------------
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select file(s)",
            str(start_dir),
            "Python Files (*.py);;All Files (*)",
        )

        if not files:
            return

        paths = [Path(p).resolve() for p in files]

        # ---------------------------------------------------------
        # Security: ensure files are inside project
        # ---------------------------------------------------------
        if project_root:
            valid_paths = []
            for p in paths:
                try:
                    p.relative_to(project_root.resolve())
                    valid_paths.append(p)
                except ValueError:
                    pass
            paths = valid_paths

        if not paths:
            return

        # ---------------------------------------------------------
        # Remember last used directory
        # ---------------------------------------------------------
        if project_root:
            update_last_used_dir(paths[0], project_root)

        # ---------------------------------------------------------
        # Continue original behavior
        # ---------------------------------------------------------
        self._append_paths(paths)

    #### - on_select_folder: choose a folder and add all nested files - ####
    def on_select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select a folder")
        if not folder:
            return
        folder_p = Path(folder)
        files_iter = iter_files_in_folder(folder_p)
        files_sorted = sorted(files_iter, key=lambda p: os.path.relpath(p, self.project_root))
        self._append_paths(list(files_sorted))

    #### - on_clear_list: clear only the session list (does not edit the file) - ####
    def on_clear_list(self) -> None:
        """Clears the session list view but not the file content."""
        self.listbox.clear()
        self._update_status("Session list cleared (file unchanged).")

        # Optionally reload the file to reflect real content (avoids desync)
        if self.output_file and self.output_file.exists():
            self._load_list_into_viewer(self.output_file)

    #### - on_new_list: prompt for a new .txt name in the output folder - ####
    def on_new_list(self, initial: bool = False) -> None:
        default_name = (self.output_file.stem if self.output_file else "paths_list") if not initial else "paths_list"
        fname, ok = QInputDialog.getText(
            self,
            "New list",
            f"Enter the name for the .txt list (no extension).\nIt will be created under: {self.output_dir}",
            text=default_name,
        )
        if not ok:
            # If first-time and user cancelled, just leave without a list
            return
        fname = (fname or default_name).strip()
        if not fname.lower().endswith(".txt"):
            fname += ".txt"
        self._set_output_file(self.output_dir / fname, create_if_missing=True, load_into_viewer=True)

    #### - on_open_existing_at_start: offer opening an existing list at startup - ####
    def on_open_existing_at_start(self) -> bool:
        # Try a soft prompt using a question box
        box = QMessageBox(self)
        box.setWindowTitle("Open existing list?")
        box.setText("Do you want to open an already-saved .txt to continue editing?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.Yes)
        choice = box.exec()
        if choice != QMessageBox.Yes:
            return False
        return self._use_existing_dialog()

    #### - on_use_existing: choose an existing .txt from the output folder - ####
    def on_use_existing(self) -> None:
        self._use_existing_dialog()

    def _use_existing_dialog(self) -> bool:
        from shared.file_dialog_context import (
            get_default_dialog_dir,
            update_last_used_dir,
            restore_last_used_dir,
        )
        import shared.global_signal_bus as gsb

        try:
            project_root = gsb.PROJECT_ROOT

            # ---------------------------------------------------------
            # Determine dialog start directory
            # ---------------------------------------------------------
            if project_root:
                restore_last_used_dir(project_root)
                start_dir = get_default_dialog_dir(project_root)
            else:
                start_dir = self.output_dir

            path_str, _ = QFileDialog.getOpenFileName(
                self,
                "Select existing .txt",
                str(start_dir),
                filter=TXT_FILTER,
            )

            if not path_str:
                return False

            p = Path(path_str).resolve()

            # ---------------------------------------------------------
            # Enforce selection inside designated output directory
            # ---------------------------------------------------------
            try:
                p.relative_to(self.output_dir.resolve())
            except Exception:
                QMessageBox.warning(
                    self,
                    "Invalid location",
                    f"Please select a .txt inside:\n{self.output_dir}",
                )
                return False

            # ---------------------------------------------------------
            # Persist last used directory (project-safe)
            # ---------------------------------------------------------
            if project_root:
                update_last_used_dir(p, project_root)

            self._set_output_file(
                p,
                create_if_missing=True,
                load_into_viewer=True,
            )

            return True

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            return False

# -------------------------------
# Entrypoint
# -------------------------------

def main() -> None:
    app = QApplication([])
    win = PathCollectorWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
