"""Native destination-folder selection for Portable publication."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from portable.errors import PortableBuildError


def _windows_folder_picker(initial_directory: Path) -> Path:
    """Open a native folder picker and return the selected directory."""

    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as exc:
        raise PortableBuildError(
            "Python tkinter is unavailable; the destination folder picker "
            "cannot open."
        ) from exc

    root = tk.Tk()
    root.withdraw()
    root.update_idletasks()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass

    try:
        selected = filedialog.askdirectory(
            parent=root,
            title=(
                "Select folder for "
                "KandaReasoner-Windows-Portable.zip"
            ),
            initialdir=str(initial_directory),
            mustexist=True,
        )
    finally:
        root.destroy()

    if not selected:
        raise PortableBuildError(
            "Portable destination-folder selection was cancelled."
        )
    return Path(selected).resolve()


def _verify_writable(directory: Path) -> None:
    """Fail before building when the selected destination is not writable."""

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=".kanda_portable_write_probe_",
            dir=directory,
            delete=False,
        ) as handle:
            probe = Path(handle.name)
            handle.write(b"KANDA_PORTABLE_DESTINATION_PROBE")
        probe.unlink()
    except OSError as exc:
        raise PortableBuildError(
            f"Selected Portable destination is not writable: {directory}"
        ) from exc


def select_output_directory(
    project_root: Path,
    requested_directory: Path | None,
) -> Path:
    """Select and validate the final Portable destination folder."""

    project = project_root.resolve()
    default_directory = Path(project.anchor).resolve()
    selected = (
        requested_directory.resolve()
        if requested_directory is not None
        else _windows_folder_picker(default_directory)
    )

    if not selected.is_dir():
        raise PortableBuildError(
            f"Selected Portable destination folder does not exist: {selected}"
        )
    if os.name != "nt":
        raise PortableBuildError(
            "The native Portable destination picker is supported on Windows."
        )

    _verify_writable(selected)
    print(f"PORTABLE DESTINATION FOLDER SELECTED: {selected}")
    print("PORTABLE DESTINATION FOLDER WRITABLE: PASS")
    return selected
